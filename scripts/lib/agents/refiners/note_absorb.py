"""Note-absorb refiner — merge an extension's claims back into its base.

Operator-gated refiner at lattice scope. One fire = promote a workspace
absorb spec md to a substrate-citizen `absorb` doc, integrate the
extension's claims into base, run a one-shot integration review that
emits findings as substrate, update source citations, retire the
extension, commit.

The agent does NOT drive convergence on the integrated base. The
post-integration review's findings sit in substrate as open
`comment.revise` links waiting for `note_revise` to fire on the next
runner walk.

Caste: refiner (lattice-scope). Per agent-castes.md: "Absorb —
recruits Refiner. Integrate an extension's material back into its
base; retire the extension... No new identity is granted." The spec
doc emission is incidental audit-trail infrastructure; the
caste-defining act is closing the integration question.

Identity grants per fire (incidental):

  - `absorb` classifier on the spec doc (workspace → substrate)
  - One-shot integration review:
      `review` classifier + `review.coverage(review → base)`
      `provenance.derivation(F=[spec], G=[review])`
      per-finding `finding` + `comment.revise` decomposition

Closure-side emissions (the actual refiner work):

  - Content edits to base note (extension claims integrated)
  - Content edits to source note (citations rewritten)
  - `retired` classifier on the extension
  - `provenance.absorb(F=[spec_doc], G=[base])` — audit edge

Operator workflow:

  1. Drop a spec md into `_workspace/absorbs/<filename>.md`:

     ```yaml
     ---
     absorb: 57
     ---

     # Why this extension is ready to merge back

     [Operator's scout-reasoning prose: convergence evidence,
      integration readiness, etc.]
     ```

  2. Run `python scripts/note-absorb.py --spec <filename>`.
  3. Drive convergence on integration findings via the relevant
     triggers — `note_review`, `note_consult`, `note_revise` — each
     invoked through `scripts/run-trigger.py NAME <base-asn>` (or
     wait for daemon).
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import ClassVar, List, Tuple

from lib.agents.base import Agent, AgentResult
from lib.agents.producers.note_review import extract_note_findings
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_absorb, emit_derivation, emit_provenance_absorb, emit_retired,
    emit_review, emit_review_coverage,
)
from lib.shared.prompts import read_prompt
from lib.lattice.findings import record_one_finding
from lib.lattice.labels import extract_label_digits, format_label
from lib.protocols.febe.protocol import Session
from lib.shared.campaign import resolve_campaign
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.foundation import FoundationError, load_foundation
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.invoke_claude import invoke_claude, invoke_claude_agent
from lib.shared.paths import (
    ABSORB_DIR, ABSORB_INBOX, LATTICE, NOTE_FINDINGS_DIR, NOTE_REVIEWS_DIR,
    WORKSPACE, claim_statements, next_review_number, prompt_path,
)


ABSORB_MODEL = "opus"
ABSORB_EFFORT = "max"

INTEGRATE_TEMPLATE = prompt_path(
    "agents/refiners/note_absorb/merge-extension.md",
)
REVIEW_TEMPLATE = prompt_path("agents/refiners/note_absorb/review.md")
SOURCE_UPDATE_TEMPLATE = prompt_path(
    "agents/refiners/note_absorb/update-citations-in-source.md",
)


# ─── Spec promotion (workspace → substrate) ────────────────────────


def _promote_spec_to_substrate(
    session: Session, spec_filename: str,
):
    """Copy the workspace spec md into the substrate doc tree, register
    its path, emit `absorb` classifier. Returns (substrate_path,
    spec_addr) or None if missing.
    """
    workspace_path = ABSORB_INBOX / spec_filename
    if not workspace_path.exists():
        print(
            f"  [ERROR] Absorb spec not found in workspace: "
            f"{workspace_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return None

    ABSORB_DIR.mkdir(parents=True, exist_ok=True)
    substrate_path = ABSORB_DIR / spec_filename
    shutil.copy2(workspace_path, substrate_path)

    substrate_rel = str(substrate_path.resolve().relative_to(WORKSPACE.resolve()))
    spec_addr = session.store.register_path(substrate_rel)
    emit_absorb(session.store, spec_addr)

    print(
        f"  [PROMOTE] {workspace_path.relative_to(WORKSPACE)} → "
        f"{substrate_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return substrate_path, spec_addr


# ─── Extension lineage resolution ──────────────────────────────────


def _asn_num_from_path(path: str | None) -> int | None:
    if path is None:
        return None
    digits = extract_label_digits(path)
    return int(digits) if digits else None


def _resolve_lineage(
    session: Session, ext_num: int,
) -> Tuple[Address, int, int | None, Path, Path] | None:
    """Read the extension's substrate `extends` and `source` links to
    resolve base + (optional) source. Returns
    (ext_addr, base_num, source_num, ext_path, base_path) or None
    on error."""
    ext_label = format_label(ext_num)
    ext_path, _ = find_asn(str(ext_num))
    if ext_path is None:
        print(
            f"  [ERROR] {ext_label} note file not found", file=sys.stderr,
        )
        return None

    ext_rel = str(ext_path.relative_to(WORKSPACE))
    ext_addr = session.get_addr_for_path(ext_rel)
    if ext_addr is None:
        print(
            f"  [ERROR] {ext_label} not registered in substrate",
            file=sys.stderr,
        )
        return None

    extends_links = session.active_links("extends", from_set=[ext_addr])
    if not extends_links or not extends_links[0].to_set:
        print(
            f"  [ERROR] {ext_label} has no `extends` link "
            f"(not an extension ASN)",
            file=sys.stderr,
        )
        return None
    base_addr = extends_links[0].to_set[0]
    base_num = _asn_num_from_path(session.get_path_for_addr(base_addr))
    if base_num is None:
        print(
            f"  [ERROR] {ext_label} extends-link target not resolvable",
            file=sys.stderr,
        )
        return None

    source_links = session.active_links("source", from_set=[ext_addr])
    source_nums = [
        _asn_num_from_path(session.get_path_for_addr(link.to_set[0]))
        for link in source_links if link.to_set
    ]
    source_nums = [n for n in source_nums if n is not None]
    source_num = source_nums[0] if source_nums else None

    base_path, _ = find_asn(str(base_num))
    if base_path is None:
        print(
            f"  [ERROR] base {format_label(base_num)} note file not found",
            file=sys.stderr,
        )
        return None

    return ext_addr, base_num, source_num, ext_path, base_path


# ─── Step 1: Integrate ────────────────────────────────────────────


def _parse_extension_labels(ext_content: str) -> List[str]:
    """Extract claim labels from the extension's statement registry,
    skipping rows whose status is 'cited' (those are references, not
    introduced claims)."""
    labels = []
    in_table = False
    for line in ext_content.splitlines():
        lower = line.lower()
        if "statement registry" in lower or "claims introduced" in lower:
            in_table = False
            continue
        if line.startswith("| ") and ("Label" in line or "label" in line):
            in_table = True
            continue
        if in_table and re.match(r"\|[-\s|]+\|", line):
            continue
        if in_table and line.startswith("|"):
            parts = [c.strip() for c in line.split("|")]
            if len(parts) >= 3 and parts[1]:
                status = parts[-2] if len(parts) >= 5 else parts[-1]
                if "cited" not in status.lower():
                    for sub in parts[1].split(","):
                        sub = sub.strip()
                        if sub:
                            labels.append(sub)
        elif in_table and not line.startswith("|") and line.strip():
            break
    return labels


def _integrate(
    ext_path: Path, base_path: Path, ext_label: str, base_label: str,
    *, model: str, effort: str,
) -> bool:
    """Step 1: LLM integrates extension's claims into base's reasoning doc."""
    template = read_prompt(INTEGRATE_TEMPLATE)
    if not template:
        print("  [ERROR] Integrate prompt template not found", file=sys.stderr)
        return False

    prompt = (
        template
        .replace("{{ext_content}}", ext_path.read_text())
        .replace("{{base_path}}", str(base_path))
        .replace("{{date}}", time.strftime("%Y-%m-%d"))
    )

    print(
        f"  [INTEGRATE] {ext_label} claims into {base_label}",
        file=sys.stderr,
    )
    response = invoke_claude_agent(
        prompt, model=model, effort=effort,
        tools="Read,Edit,Grep", max_turns=20,
    )
    if response.data is None:
        print("  [ERROR] Integration failed", file=sys.stderr)
        return False
    print(f"  [INTEGRATED] {base_label} updated", file=sys.stderr)
    return True


# ─── Step 2: One-shot integration review (emits findings) ──────────


def _integration_review(
    base_num: int, base_path: Path, base_label: str, claim_labels: List[str],
    *, model: str, effort: str,
) -> str | None:
    """Step 2: One-shot review of integrated content. Returns review
    text or None on LLM failure. The review's output is emitted as
    proper substrate findings; convergence is the runner's job."""
    template = read_prompt(REVIEW_TEMPLATE)
    if not template:
        print(
            "  [ERROR] Integration review prompt not found",
            file=sys.stderr,
        )
        return None

    vocabulary = read_file(resolve_campaign(base_num).vocabulary_path)
    try:
        foundation = load_foundation(base_num)
    except FoundationError as e:
        print(
            f"  [FOUNDATION] {base_label}: {e}",
            file=sys.stderr,
        )
        return None

    prompt = (
        template
        .replace("{{asn_content}}", base_path.read_text())
        .replace("{{claim_labels}}", ", ".join(claim_labels))
        .replace("{{vocabulary}}", vocabulary)
        .replace("{{foundation_statements}}", foundation)
    )

    print(f"  [REVIEW] Integration review of {base_label}...", file=sys.stderr)
    result = invoke_claude(prompt, model=model, effort=effort)
    if not result.text:
        print("  [WARN] Integration review produced no output", file=sys.stderr)
        return None
    log_usage("absorb-review", result.elapsed, base=base_num)
    return result.text


def _emit_review_with_findings(
    session: Session, base_label: str, base_addr: Address,
    spec_addr: Address, review_text: str,
) -> Tuple[Address, int]:
    """Persist integration review + emit review classifier + coverage +
    per-finding decomposition. Adds a provenance.derivation(spec → review)
    audit edge so the review ties back to the absorb fire.

    Returns (review_addr, n_findings).
    """
    next_n = next_review_number(base_label, kind="note")
    review_dir = NOTE_REVIEWS_DIR / base_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / f"review-{next_n}.md"
    body = review_text + "\n"

    review_rel = str(review_path.relative_to(session.store.lattice_dir))
    session.update_document(review_rel, body)
    review_addr = session.register_path(review_rel)
    emit_review(session.store, review_addr)
    emit_review_coverage(session.store, review_addr, base_addr)
    emit_derivation(session.store, spec_addr, review_addr)

    findings = extract_note_findings(review_text)
    findings_root = NOTE_FINDINGS_DIR / base_label / f"review-{next_n}"
    for n, (_title, cls, fbody) in enumerate(findings):
        finding_rel = str(
            (findings_root / f"{n}.md").relative_to(session.store.lattice_dir)
        )
        comment_kind = (
            "out-of-scope" if (cls or "REVISE").upper() == "OUT_OF_SCOPE"
            else "revise"
        )
        record_one_finding(
            session,
            finding_path_rel=finding_rel,
            body=fbody,
            target_addr=base_addr,
            review_addr=review_addr,
            comment_kind=comment_kind,
        )

    revise_count = sum(
        1 for _, c, _ in findings if (c or "").upper() == "REVISE"
    )
    print(
        f"  [REVIEW] {base_label} {review_path.name} — "
        f"{revise_count} REVISE finding(s)",
        file=sys.stderr,
    )
    return review_addr, len(findings)


# ─── Step 3: Re-export base ────────────────────────────────────────


def _re_export(base_num: int, base_label: str) -> None:
    """Subprocess to existing note-assembly.py."""
    print(f"  [EXPORT] Re-exporting {base_label}...", file=sys.stderr)
    cmd = [
        sys.executable,
        str(WORKSPACE / "scripts" / "note-assembly.py"),
        str(base_num),
    ]
    subprocess.run(cmd, capture_output=False, text=True, cwd=str(WORKSPACE))


# ─── Step 4: Update source citations ───────────────────────────────


def _update_source_citations(
    ext_path: Path, ext_label: str, source_num: int, base_label: str,
    *, model: str, effort: str,
) -> bool:
    """Rewrite the source ASN's now-extracted claims as citations to base."""
    source_label = format_label(source_num)
    source_path, _ = find_asn(str(source_num))
    if source_path is None:
        print(
            f"  [WARN] Source {source_label} not found, skipping",
            file=sys.stderr,
        )
        return False

    ext_content = ext_path.read_text()
    claim_labels = _parse_extension_labels(ext_content)
    if not claim_labels:
        print(
            f"  [WARN] No introduced claims found in {ext_label}",
            file=sys.stderr,
        )
        return False

    template = read_prompt(SOURCE_UPDATE_TEMPLATE)
    if not template:
        print(
            "  [ERROR] Source-update prompt template not found",
            file=sys.stderr,
        )
        return False

    prompt = (
        template
        .replace("{{ext_label}}", ext_label)
        .replace("{{source_label}}", source_label)
        .replace("{{base_label}}", base_label)
        .replace("{{ext_content}}", ext_content)
        .replace("{{claim_labels}}", ", ".join(claim_labels))
        .replace("{{source_path}}", str(source_path))
    )

    print(
        f"  [UPDATE] {source_label} — citing from {base_label}",
        file=sys.stderr,
    )
    response = invoke_claude_agent(
        prompt, model=model, effort=effort,
        tools="Read,Edit,Grep", max_turns=20,
    )
    if response.data is None:
        print("  [WARN] Source update failed", file=sys.stderr)
        return False
    print(f"  [UPDATED] {source_label}", file=sys.stderr)
    return True


# ─── Step 5: Retire extension (cleanup statements sidecar) ─────────


def _retire_extension(
    session: Session, ext_addr: Address, ext_num: int, ext_label: str,
) -> None:
    """Mark extension retired in substrate; clean up its statements
    sidecar. The reasoning doc and review dir stay as trace artifacts."""
    emit_retired(session.store, ext_addr)

    sidecar_path = claim_statements(ext_num)
    if sidecar_path.exists():
        sidecar_path.unlink()
        print(
            f"  [REMOVED] {sidecar_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
    print(f"  [RETIRED] {ext_label}", file=sys.stderr)


# ─── Agent class ───────────────────────────────────────────────────


class NoteAbsorbAgent(Agent):
    """One absorb per fire — refiner at lattice scope (operator-gated).

    Reads operator intent from a workspace spec md (just `absorb: <ext>`
    + rationale), promotes it to substrate, integrates the extension's
    claims into base, files a one-shot integration review whose findings
    are emitted as substrate, updates source citations, retires the
    extension. Does not drive convergence on the integrated base; the
    runner walks afterward via note_revise.
    """

    role: ClassVar[str] = "note-absorb"

    def __init__(
        self, *,
        model: str = ABSORB_MODEL,
        effort: str = ABSORB_EFFORT,
    ):
        self.model = model
        self.effort = effort

    def run(
        self, session: Session, addr: Address,
        *, spec_filename: str,
    ) -> AgentResult:
        # Operator-gated: addr is unused (the spec doc carries the
        # extension target). Accepted to match Agent dispatch surface.
        del addr

        # 1. Promote workspace spec → substrate
        promotion = _promote_spec_to_substrate(session, spec_filename)
        if promotion is None:
            return AgentResult(success=False, detail="spec-not-in-workspace")
        substrate_path, spec_addr = promotion

        # 2. Parse spec frontmatter
        fm, _body = read_doc_with_frontmatter(substrate_path)
        try:
            ext_num = int(fm["absorb"])
        except (KeyError, ValueError, TypeError) as e:
            return AgentResult(
                success=False,
                detail=f"spec-frontmatter-malformed: {e}",
            )

        # 3. Resolve extension lineage from substrate
        lineage = _resolve_lineage(session, ext_num)
        if lineage is None:
            return AgentResult(success=False, detail="lineage-resolution-failed")
        ext_addr, base_num, source_num, ext_path, base_path = lineage
        ext_label = format_label(ext_num)
        base_label = format_label(base_num)

        os.environ.setdefault("PROTOCOL_ASN_LABEL", base_label)

        # 4. Integrate extension claims into base
        ok = _integrate(
            ext_path, base_path, ext_label, base_label,
            model=self.model, effort=self.effort,
        )
        if not ok:
            return AgentResult(success=False, detail="integrate-failed")
        # Base note's body was edited; advance its supersession chain
        # so cascade-fresh detects the absorb.
        base_rel_for_version = str(base_path.relative_to(WORKSPACE))
        base_addr_for_version = session.get_addr_for_path(base_rel_for_version)
        if base_addr_for_version is not None:
            session.register_version(base_addr_for_version)
        log_usage("absorb-integrate", 0, ext=ext_num, base=base_num)

        # 5. One-shot integration review (emits findings as substrate)
        ext_content = ext_path.read_text()
        claim_labels = _parse_extension_labels(ext_content)
        review_text = _integration_review(
            base_num, base_path, base_label, claim_labels,
            model=self.model, effort=self.effort,
        )
        n_findings = 0
        review_addr = None
        if review_text is not None:
            base_rel = str(base_path.relative_to(WORKSPACE))
            base_addr = session.get_addr_for_path(base_rel)
            review_addr, n_findings = _emit_review_with_findings(
                session, base_label, base_addr, spec_addr, review_text,
            )

        # 6. Re-export base
        _re_export(base_num, base_label)

        # 7. Update source citations (if source recorded)
        if source_num is not None:
            _update_source_citations(
                ext_path, ext_label, source_num, base_label,
                model=self.model, effort=self.effort,
            )

        # 8. Retire extension + emit provenance.absorb
        _retire_extension(session, ext_addr, ext_num, ext_label)
        base_rel = str(base_path.relative_to(WORKSPACE))
        base_addr = session.get_addr_for_path(base_rel)
        emit_provenance_absorb(session.store, spec_addr, base_addr)

        # 9. Final commit
        log_usage("absorb-complete", 0, ext=ext_num, base=base_num)

        return AgentResult(
            success=True,
            detail=(
                f"absorbed={ext_label} into={base_label} "
                f"findings={n_findings}"
                + (f" review={review_addr}" if review_addr else "")
            ),
        )
