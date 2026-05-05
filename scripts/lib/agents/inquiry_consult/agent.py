"""Inquiry-consult agent — initial-draft channel consultation.

Fires when an inquiry has no consultation answer covering it yet.
One fire = decompose the inquiry into questions, run theory +
evidence consultations on each, persist per-Q/A answer docs, emit
substrate facts (consultation.questions, consultation.answer.<role>,
consultation.coverage), commit.

Distinct from `NoteConsultAgent`, which handles the revise-stage
consult on review findings. Both agents share the channel-consult
primitives in `lib/consultation/consult.py` but operate at different
points in the flow.

Channel-specific logic (role identity, prompt composition, source
loading, citation formats) lives in the channel plugin under
`channels/<name>/consultations/consult.py`. This agent knows only role
names: "theory" and "evidence", resolved to channel names via the
ASN's campaign.
"""

from __future__ import annotations

import re
import sys
import threading
import time
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_consultation_answer, emit_consultation_coverage,
    emit_consultation_questions,
)
from lib.consultation.consult import (
    invoke_claude, get_total_usage, reset_total_usage,
    dispatch_generate_questions, dispatch_run_consultation,
)
from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import (
    WORKSPACE, CONSULTATIONS_DIR, LATTICE,
    inquiry_doc_path, prompt_path,
    load_inquiry as load_inquiry_frontmatter,
    load_channel_meta,
)


# ─── Helpers ────────────────────────────────────────────────────


def _channel_default_questions(channel_name, fallback=10):
    """Per-channel default consultation depth.

    Reads `default_questions` from the channel's meta.yaml. The channel
    is the natural home for this — depth reflects the corpus's character
    (broad theory vs specific evidence), not the campaign that binds them.
    """
    try:
        meta = load_channel_meta(channel_name)
    except FileNotFoundError:
        return fallback
    return int(meta.get("default_questions", fallback))


def _load_inquiry_record(inquiry_id):
    """Load inquiry content from the substrate-managed inquiry doc.
    Returns the standard pipeline shape (id/title/question/out_of_scope/agents).
    """
    fm = load_inquiry_frontmatter(inquiry_id)
    if not fm:
        print(f"  [ERROR] Inquiry doc not found for ASN-{inquiry_id:04d}",
              file=sys.stderr)
        return None
    agents = {}
    if "n_theory" in fm:
        agents["theory"] = fm["n_theory"]
    if "n_evidence" in fm:
        agents["evidence"] = fm["n_evidence"]
    return {
        "id": inquiry_id,
        "title": fm.get("title", ""),
        "question": fm.get("question", ""),
        "out_of_scope": fm.get("out_of_scope", ""),
        "agents": agents,
    }


# ─── Step 1: Decompose ──────────────────────────────────────────


def _filter_questions(inquiry_text, out_of_scope, questions, covers_text=""):
    """Filter questions for scope. Returns filtered list of (role, question) tuples."""
    template = read_file(prompt_path("discovery/consultation/filter-questions.md"))
    if not template:
        print("  [WARN] filter-questions.md not found, skipping filter",
              file=sys.stderr)
        return questions

    questions_text = "\n".join(
        f"{i}. [{role}] {q}" for i, (role, q) in enumerate(questions, 1)
    )
    foundation_block = (
        f"## Already Established\n\n"
        f"The following topics are already covered by upstream ASNs. "
        f"Drop questions whose answers are already established:\n\n{covers_text}"
        if covers_text else ""
    )
    prompt = template.format(
        inquiry=inquiry_text,
        out_of_scope=out_of_scope,
        foundation_block=foundation_block,
        questions=questions_text,
    )

    print(f"  [FILTER] Checking {len(questions)} questions against exclusions...",
          file=sys.stderr)
    response, _ = invoke_claude(prompt, model="opus",
                                skill="pre-consult:filter",
                                label="filter")

    if not response:
        print("  [FILTER] No response, keeping all questions", file=sys.stderr)
        return questions

    keep_indices = set()
    for line in response.strip().split("\n"):
        line = line.strip()
        if line.startswith("KEEP"):
            try:
                idx = int(line.split()[1])
                keep_indices.add(idx)
            except (IndexError, ValueError):
                pass

    if not keep_indices:
        print("  [FILTER] No KEEP lines parsed, keeping all questions",
              file=sys.stderr)
        return questions

    filtered = [q for i, q in enumerate(questions, 1) if i in keep_indices]
    dropped = len(questions) - len(filtered)
    if dropped:
        print(f"  [FILTER] Dropped {dropped} out-of-scope questions, "
              f"keeping {len(filtered)}", file=sys.stderr)
    else:
        print(f"  [FILTER] All {len(filtered)} questions in scope",
              file=sys.stderr)

    return filtered


def _decompose_inquiry(inquiry_text, num_theory=10, num_evidence=10, model="opus",
                       out_of_scope="", asn_id=None):
    """Two-pass decompose: theory channel then evidence channel.

    Each per-domain module owns its own question-generation prompt and
    vocabulary fence. This orchestrator just calls them and merges results.
    """
    campaign = resolve_campaign(asn_id)
    theory_channel = campaign.theory_channel
    evidence_channel = campaign.evidence_channel

    theory_qs = dispatch_generate_questions(
        theory_channel, inquiry_text, num_theory, model, out_of_scope)
    evidence_qs = dispatch_generate_questions(
        evidence_channel, inquiry_text, num_evidence, model, out_of_scope)

    all_qs = [("theory", q) for q in theory_qs] + [("evidence", q) for q in evidence_qs]

    if out_of_scope and all_qs:
        all_qs = _filter_questions(inquiry_text, out_of_scope, all_qs)

    return all_qs


def _parse_questions(response, default_role="evidence"):
    """Parse numbered `[role] question` lines. Returns list of (role, question)."""
    questions = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if not line or not (line[0].isdigit() and "." in line[:4]):
            continue
        q = line.split(".", 1)[1].strip()
        if q.startswith("[theory]"):
            questions.append(("theory", q[len("[theory]"):].strip()))
        elif q.startswith("[evidence]"):
            questions.append(("evidence", q[len("[evidence]"):].strip()))
        else:
            questions.append((default_role, q))
    return questions


# ─── Step 2: Consult ────────────────────────────────────────────


def _answer_path(consult_dir, index, role):
    return consult_dir / f"answer-{index + 1:02d}-{role}.md"


def _save_answer(consult_dir, index, role, question, answer):
    path = _answer_path(consult_dir, index, role)
    content = (f"## Question {index + 1} [{role}]\n\n"
               f"> {question}\n\n"
               f"{answer.strip() if answer else '[No answer]'}\n")
    path.write_text(content)
    print(f"  [SAVED] {path.name}", file=sys.stderr)


def _load_existing_answers(consult_dir, questions):
    """Load answers already on disk. Returns dict of index → (role, question, answer)."""
    existing = {}
    for i, (role, question) in enumerate(questions):
        path = _answer_path(consult_dir, i, role)
        if path.exists():
            raw = path.read_text()
            lines = raw.split("\n")
            body_start = 0
            found_quote = False
            for j, line in enumerate(lines):
                if line.startswith(">"):
                    found_quote = True
                elif found_quote and line.strip() == "":
                    body_start = j + 1
                    break
            answer = "\n".join(lines[body_start:]).strip()
            existing[i] = (role, question, answer)
            print(f"  [CACHED] answer-{i + 1:02d}-{role}.md", file=sys.stderr)
    return existing


def _run_consultations(questions, consult_dir, asn_id, theory_model="opus",
                       evidence_model="sonnet", effort="max"):
    """Run all consultations. Theory in parallel, evidence sequential.

    Saves each answer to disk as it completes. Skips questions with existing
    answer files (resume support).

    Theory: no tools, safe to parallelize.
    Evidence: each call runs KB + source in parallel internally. Run
    sequentially across calls because source exploration uses tools.

    The ASN's campaign determines which channels the theory and evidence
    consultations bind to.
    """
    campaign = resolve_campaign(asn_id)
    theory_channel = campaign.theory_channel
    evidence_channel = campaign.evidence_channel

    results = [None] * len(questions)

    existing = _load_existing_answers(consult_dir, questions)
    for i, cached in existing.items():
        results[i] = cached

    if existing:
        print(f"  [RESUME] Skipping {len(existing)} already-completed questions",
              file=sys.stderr)

    theory_indices = [i for i, (r, _) in enumerate(questions)
                      if r == "theory" and i not in existing]
    evidence_indices = [i for i, (r, _) in enumerate(questions)
                        if r == "evidence" and i not in existing]

    if theory_indices:
        print(f"  [THEORY] Firing {len(theory_indices)} calls in parallel...",
              file=sys.stderr)
        threads = []

        for i in theory_indices:
            role, question = questions[i]

            def run_t(idx=i, q=question, r=role):
                answer = dispatch_run_consultation(
                    theory_channel, q,
                    label=f"Q{idx + 1}:theory",
                    model=theory_model, effort=effort,
                )
                results[idx] = (r, q, answer)
                _save_answer(consult_dir, idx, r, q, answer)

            t = threading.Thread(target=run_t)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        print(f"  [THEORY] All done", file=sys.stderr)

    if evidence_indices:
        print(f"  [EVIDENCE] Running {len(evidence_indices)} calls sequentially...",
              file=sys.stderr)
        for i in evidence_indices:
            role, question = questions[i]
            answer = dispatch_run_consultation(
                evidence_channel, question,
                label=f"Q{i + 1}:evidence",
                model=evidence_model, effort=effort,
            )
            results[i] = (role, question, answer)
            _save_answer(consult_dir, i, role, question, answer)

        print(f"  [EVIDENCE] All done", file=sys.stderr)

    return results


# ─── Run for one inquiry ────────────────────────────────────────


def _run_consult_for_inquiry(
    asn_id,
    *,
    model: str = "opus",
    num_theory=None,
    num_evidence=None,
    regenerate: bool = False,
):
    """Run the initial-draft consult flow for one inquiry.

    Returns the consult subdir path on success, None on failure.
    """
    inquiry = _load_inquiry_record(asn_id)
    if not inquiry:
        return None

    inquiry_text = inquiry.get("question", "")
    inquiry_title = inquiry.get("title", f"ASN-{asn_id:04d}")
    asn_label = f"{asn_id:04d}"
    out_of_scope = inquiry.get("out_of_scope", "")
    campaign = resolve_campaign(asn_id)

    if num_theory is None:
        num_theory = _channel_default_questions(campaign.theory_channel)
    if num_evidence is None:
        num_evidence = _channel_default_questions(campaign.evidence_channel)
    agents = inquiry.get("agents", {})
    if "theory" in agents:
        num_theory = agents["theory"]
    if "evidence" in agents:
        num_evidence = agents["evidence"]

    reset_total_usage()
    total_start = time.time()

    existing_questions_path = (
        CONSULTATIONS_DIR / f"ASN-{asn_label}" / "consultation" / "questions.md"
    )
    if existing_questions_path.exists() and not regenerate:
        print(
            f"  [LOAD] Using existing questions from "
            f"{existing_questions_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        questions = _parse_questions(existing_questions_path.read_text())
    else:
        questions = _decompose_inquiry(
            inquiry_text,
            num_theory=num_theory,
            num_evidence=num_evidence,
            model=model,
            out_of_scope=out_of_scope,
            asn_id=asn_id,
        )

    if not questions:
        print("  [ERROR] No questions generated", file=sys.stderr)
        return None

    theory_qs = sum(1 for r, _ in questions if r == "theory")
    evidence_qs = len(questions) - theory_qs
    print(
        f"  [OK] {len(questions)} questions "
        f"({theory_qs} theory, {evidence_qs} evidence)",
        file=sys.stderr,
    )

    for i, (role, q) in enumerate(questions, 1):
        print(f"  {i}. [{role}] {q}", file=sys.stderr)

    output_dir = CONSULTATIONS_DIR / f"ASN-{asn_label}"
    init_dir = output_dir / "consultation"
    init_dir.mkdir(parents=True, exist_ok=True)
    questions_path = init_dir / "questions.md"
    questions_text = "\n".join(
        f"{i}. [{r}] {q}" for i, (r, q) in enumerate(questions, 1)
    )
    questions_path.write_text(
        f"# Sub-Questions — {inquiry_title}\n\n"
        f"**Inquiry:** {inquiry_text}\n\n"
        f"{questions_text}\n"
    )
    print(
        f"  [SAVED] {questions_path.relative_to(WORKSPACE)}", file=sys.stderr,
    )

    session = open_session(LATTICE)
    store = session.store
    questions_rel = str(questions_path.resolve().relative_to(LATTICE.resolve()))
    questions_addr = store.register_path(questions_rel)
    emit_consultation_questions(store, questions_addr)
    inquiry_rel = str(
        inquiry_doc_path(asn_id).resolve().relative_to(LATTICE.resolve())
    )
    inquiry_addr = store.register_path(inquiry_rel)
    emit_consultation_coverage(store, questions_addr, inquiry_addr)

    print(
        f"  [CONSULT] Firing {len(questions)} consultations...",
        file=sys.stderr,
    )
    consult_start = time.time()
    _run_consultations(questions, init_dir, asn_id)
    consult_elapsed = time.time() - consult_start
    print(f"  [CONSULT] All done ({consult_elapsed:.0f}s)", file=sys.stderr)

    session = open_session(LATTICE)
    store = session.store
    inquiry_addr = store.register_path(inquiry_rel)
    for answer_md in sorted(init_dir.glob("answer-*.md")):
        role_match = re.match(
            r"answer-\d+-(theory|evidence)\.md", answer_md.name,
        )
        if role_match is None:
            print(
                f"  [WARN] {answer_md.name}: cannot parse role; "
                f"skipping classifier emit",
                file=sys.stderr,
            )
            continue
        answer_rel = str(answer_md.resolve().relative_to(LATTICE.resolve()))
        answer_addr = store.register_path(answer_rel)
        emit_consultation_answer(store, answer_addr, role_match.group(1))
        emit_consultation_coverage(store, answer_addr, inquiry_addr)

    total_elapsed = time.time() - total_start

    print("", file=sys.stderr)
    print(f"  {'=' * 50}", file=sys.stderr)
    print(f"  EXPERT CONSULTATION COMPLETE", file=sys.stderr)
    print(f"  {'=' * 50}", file=sys.stderr)
    print(
        f"  Questions: {len(questions)} "
        f"({theory_qs} theory, {evidence_qs} evidence)",
        file=sys.stderr,
    )
    print(f"  Decompose: {consult_start - total_start:.0f}s", file=sys.stderr)
    print(
        f"  Consultations: {consult_elapsed:.0f}s (parallel)", file=sys.stderr,
    )
    print(
        f"  Total: {total_elapsed:.0f}s ({total_elapsed / 60:.1f}min)",
        file=sys.stderr,
    )
    return init_dir


# ─── Agent class ────────────────────────────────────────────────


class InquiryConsultAgent(Agent):
    """One initial-draft consult pass on an inquiry that lacks coverage."""

    role: ClassVar[str] = "inquiry-consult"

    def __init__(self, *, model: str = "opus"):
        self.model = model

    def run(self, session: Session, inquiry_addr: Address) -> AgentResult:
        inquiry_path_rel = session.get_path_for_addr(inquiry_addr)
        if inquiry_path_rel is None:
            return AgentResult(success=False, detail="no-inquiry-path")

        m = re.search(r"ASN-(\d{4})", inquiry_path_rel)
        if m is None:
            return AgentResult(success=False, detail="no-asn-label")
        asn_num = int(m.group(1))
        asn_label = f"ASN-{asn_num:04d}"

        print(f"  [INQUIRY-CONSULT] {asn_label}", file=sys.stderr)

        consult_dir = _run_consult_for_inquiry(asn_num, model=self.model)
        if consult_dir is None:
            return AgentResult(success=False, detail="consult-failed")

        step_commit_asn(asn_num, f"inquiry-consult(asn): {asn_label}")

        return AgentResult(
            success=True,
            detail=f"consult dir {consult_dir.name}",
        )
