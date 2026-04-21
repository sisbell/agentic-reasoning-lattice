#!/usr/bin/env python3
"""
Decompose an inquiry into focused questions, then consult both channels
(theory and evidence).

Generic orchestrator: decomposes via the per-domain theory and evidence
channel modules, merges questions into a labeled list, filters for scope,
dispatches (theory in parallel, evidence sequential — the evidence calls
each run KB + source in parallel internally), saves per-question answers,
assembles a combined output.

Domain-specific logic (role identity, prompt composition, source loading,
citation formats) lives in domains/<LATTICE>/scripts/theory.py and
evidence.py. The orchestrator knows only role names: "theory" and
"evidence".

Usage:
    python scripts/lib/discovery/decompose.py --inquiry-id 4
    python scripts/lib/discovery/decompose.py "What must INSERT preserve and establish?"
    python scripts/lib/discovery/decompose.py --inquiry-id 4 --theory 5 --evidence 5
    python scripts/lib/discovery/decompose.py --inquiry-id 4 --dry-run
"""

import argparse
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, CONSULTATIONS_DIR, DOMAIN_PROMPTS, DOMAIN,
    load_manifest, load_excluded_covers,
)
from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.consult import (
    invoke_claude, get_total_usage, reset_total_usage,
    load_domain_consult_modules,
)

theory, evidence = load_domain_consult_modules(DOMAIN)

PROMPTS_DIR = DOMAIN_PROMPTS / "discovery" / "consultation"


def load_inquiry(inquiry_id):
    """Load inquiry from project model manifest."""
    manifest = load_manifest(inquiry_id)
    if not manifest:
        print(f"  [ERROR] Manifest not found for ASN-{inquiry_id:04d}",
              file=sys.stderr)
        sys.exit(1)
    inquiry = manifest.get("consultations", {})
    return {
        "id": inquiry_id,
        "title": manifest.get("title", ""),
        "question": inquiry.get("question", ""),
        "out_of_scope": manifest.get("out_of_scope", ""),
        "agents": inquiry.get("agents", {}),
    }


# ─── Step 1: Decompose ──────────────────────────────────────────

def filter_questions(inquiry_text, out_of_scope, questions, covers_text=""):
    """Filter questions for scope. Returns filtered list of (role, question) tuples."""
    template = read_file(PROMPTS_DIR / "filter-questions.md")
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


def decompose_inquiry(inquiry_text, num_theory=10, num_evidence=10, model="opus",
                      out_of_scope="", asn_id=None):
    """Two-pass decompose: theory channel then evidence channel.

    Each per-domain module owns its own question-generation prompt and
    vocabulary fence. This orchestrator just calls them and merges results.
    """
    campaign = resolve_campaign(asn_id)
    theory_channel = campaign.theory_channel
    evidence_channel = campaign.evidence_channel

    theory_qs = theory.generate_questions(
        inquiry_text, theory_channel, n=num_theory, model=model, out_of_scope=out_of_scope,
    )
    evidence_qs = evidence.generate_questions(
        inquiry_text, evidence_channel, n=num_evidence, model=model, out_of_scope=out_of_scope,
    )

    all_qs = [("theory", q) for q in theory_qs] + [("evidence", q) for q in evidence_qs]

    covers_text = load_excluded_covers(asn_id) if asn_id else ""
    if (out_of_scope or covers_text) and all_qs:
        all_qs = filter_questions(inquiry_text, out_of_scope, all_qs,
                                  covers_text=covers_text)

    return all_qs


def parse_questions(response, default_role="evidence"):
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


def run_consultations(questions, consult_dir, asn_id, theory_model="opus",
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
                answer = theory.run_consultation(
                    q, theory_channel, label=f"Q{idx + 1}:theory",
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
            answer = evidence.run_consultation(
                question, evidence_channel, label=f"Q{i + 1}:evidence",
                model=evidence_model, effort=effort,
            )
            results[i] = (role, question, answer)
            _save_answer(consult_dir, i, role, question, answer)

        print(f"  [EVIDENCE] All done", file=sys.stderr)

    return results


# ─── Step 3: Combine ────────────────────────────────────────────

def build_combined_output(inquiry_text, inquiry_title, questions, results):
    """Build the combined consultation answers markdown."""
    parts = []

    parts.append(f"# Consultation Answers — {inquiry_title}")
    parts.append("")
    parts.append(f"**Inquiry:** {inquiry_text}")
    parts.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    theory_count = sum(1 for r, _ in questions if r == "theory")
    evidence_count = len(questions) - theory_count
    parts.append(f"**Questions:** {len(questions)} "
                 f"({theory_count} theory, {evidence_count} evidence)")
    parts.append("")

    for i, (role, question, answer) in enumerate(results, 1):
        parts.append("---")
        parts.append("")
        parts.append(f"## Question {i} [{role}]")
        parts.append("")
        parts.append(f"> {question}")
        parts.append("")
        parts.append(f"### Answer ({role})")
        parts.append("")
        parts.append(answer.strip() if answer else "[No answer]")
        parts.append("")

    return "\n".join(parts)


# ─── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Consult experts: decompose inquiry → run theory and evidence consultations")
    parser.add_argument("question", nargs="?", help="The inquiry question")
    parser.add_argument("--inquiry-id", type=int,
                        help="Load inquiry by ID from manifest")
    parser.add_argument("--theory", type=int, default=None,
                        help="Number of theory questions (overrides manifest, default: 10)")
    parser.add_argument("--evidence", type=int, default=None,
                        help="Number of evidence questions (overrides manifest, default: 10)")
    # Backward-compat aliases (xanadu's previous authority-named flags)
    parser.add_argument("--nelson", type=int, default=None, dest="theory",
                        help=argparse.SUPPRESS)
    parser.add_argument("--gregory", type=int, default=None, dest="evidence",
                        help=argparse.SUPPRESS)
    parser.add_argument("--model", "-m", default="opus",
                        choices=["sonnet", "opus"],
                        help="Model for question generation (default: opus)")
    parser.add_argument("--output", "-o",
                        help="Output file path (default: consultations/ASN-NNNN/consultation/answers.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate and save questions, don't run consultations")
    parser.add_argument("--regenerate", action="store_true",
                        help="Regenerate questions even if a saved questions file exists")
    args = parser.parse_args()

    inquiry_title = "Ad-hoc inquiry"
    asn_label = "adhoc"
    num_theory = 10
    num_evidence = 10
    out_of_scope = ""
    asn_id = None

    if args.inquiry_id:
        inquiry = load_inquiry(args.inquiry_id)
        inquiry_text = inquiry["question"]
        inquiry_title = inquiry["title"]
        asn_label = f"{args.inquiry_id:04d}"
        asn_id = args.inquiry_id
        out_of_scope = inquiry.get("out_of_scope", "")
        agents = inquiry.get("agents", {})
        # Manifest may use legacy "nelson"/"gregory" keys or the new "theory"/"evidence".
        num_theory = agents.get("theory", agents.get("nelson", 10))
        num_evidence = agents.get("evidence", agents.get("gregory", 10))
    elif args.question:
        inquiry_text = args.question
    else:
        parser.error("Provide a question or --inquiry-id")

    if args.theory is not None:
        num_theory = args.theory
    if args.evidence is not None:
        num_evidence = args.evidence

    reset_total_usage()
    total_start = time.time()

    existing_questions_path = (CONSULTATIONS_DIR / f"ASN-{asn_label}"
                               / "consultation" / "questions.md")
    if not args.dry_run and existing_questions_path.exists() and not args.regenerate:
        print(f"  [LOAD] Using existing questions from "
              f"{existing_questions_path.relative_to(WORKSPACE)}", file=sys.stderr)
        existing_text = existing_questions_path.read_text()
        questions = parse_questions(existing_text)
    else:
        questions = decompose_inquiry(inquiry_text,
                                      num_theory=num_theory,
                                      num_evidence=num_evidence,
                                      model=args.model,
                                      out_of_scope=out_of_scope,
                                      asn_id=asn_id)

    if not questions:
        print("  [ERROR] No questions generated", file=sys.stderr)
        sys.exit(1)

    theory_qs = sum(1 for r, _ in questions if r == "theory")
    evidence_qs = len(questions) - theory_qs
    print(f"  [OK] {len(questions)} questions "
          f"({theory_qs} theory, {evidence_qs} evidence)", file=sys.stderr)
    print("", file=sys.stderr)

    for i, (role, q) in enumerate(questions, 1):
        print(f"  {i}. [{role}] {q}", file=sys.stderr)

    print("", file=sys.stderr)

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
    print(f"  [SAVED] {questions_path.relative_to(WORKSPACE)}", file=sys.stderr)

    if args.dry_run:
        for i, (role, q) in enumerate(questions, 1):
            print(f"{i}. [{role}] {q}")
        return

    print(f"  [CONSULT] Firing {len(questions)} consultations...",
          file=sys.stderr)
    consult_start = time.time()
    results = run_consultations(questions, init_dir, asn_id)
    consult_elapsed = time.time() - consult_start
    print(f"  [CONSULT] All done ({consult_elapsed:.0f}s)", file=sys.stderr)

    combined = build_combined_output(inquiry_text, inquiry_title, questions, results)

    output_path = args.output or str(init_dir / "answers.md")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(combined)

    total_elapsed = time.time() - total_start

    print("", file=sys.stderr)
    print(f"  {'=' * 50}", file=sys.stderr)
    print(f"  EXPERT CONSULTATION COMPLETE", file=sys.stderr)
    print(f"  {'=' * 50}", file=sys.stderr)
    print(f"  Questions: {len(questions)} "
          f"({theory_qs} theory, {evidence_qs} evidence)", file=sys.stderr)
    print(f"  Decompose: {consult_start - total_start:.0f}s", file=sys.stderr)
    print(f"  Consultations: {consult_elapsed:.0f}s (parallel)", file=sys.stderr)
    print(f"  Total: {total_elapsed:.0f}s ({total_elapsed / 60:.1f}min)",
          file=sys.stderr)

    totals = get_total_usage()
    if totals["calls"] > 0:
        print(f"  Total cost: ${totals['cost_usd']:.4f} "
              f"({totals['calls']} calls)", file=sys.stderr)

    print(f"  Output: {output_path}", file=sys.stderr)
    print(f"  Log dir: {output_dir}", file=sys.stderr)

    print(str(Path(output_path).resolve()))


if __name__ == "__main__":
    main()
