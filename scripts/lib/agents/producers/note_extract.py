"""Note-extract producer — extract claims from an origin ASN into a new
workshop ASN that will eventually be absorbed into a destination.

Operator-gated pure producer. One fire = promote a workspace extract
spec md to a substrate-citizen `extract` doc, generate the new
workshop ASN via LLM extraction, emit lineage links, commit.

The new ASN goes through the standard runner-walk afterward (note
review → revise convergence) until the operator decides it's ready
to absorb. The agent itself does NOT drive convergence on the new
ASN — it just grants identity.

Caste: pure producer (one-shot identity grant). Identity grants per
fire:

  - `extract` classifier on the spec doc (workspace → substrate
    promotion)
  - `note` classifier on the new workshop ASN
  - `extends(F=[new], G=[absorb_into])` — structural relationship
    encoding "the new ASN extends absorb_into during refine phase"
  - `source(F=[new], G=[extract_from])` — origin lineage
  - `provenance.extract(F=[spec_doc], G=[new])` — audit edge tying
    the spec doc to the new note it produced

Operator workflow:

  1. Drop a spec md into `_workspace/extracts/<filename>.md`
     (gitignored input drop). Frontmatter declares operator intent;
     body holds rationale prose.

     ```yaml
     ---
     create_note: 57
     extract_from: 53
     absorb_into: 34
     claims: [D0, D1, D2]
     ---

     # Why these claims belong as their own ASN

     [Operator's scout-reasoning prose...]
     ```

  2. Run `python scripts/note-extract.py --spec <filename>`.
  3. The new ASN goes through the standard runner walk for its own
     refinement; operator drives absorb when convergence is reached.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import ClassVar, List, Tuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_extends, emit_extract, emit_note, emit_provenance_extract,
    emit_source,
)
from lib.shared.prompts import read_prompt
from lib.protocols.febe.protocol import Session
from lib.lattice.labels import format_label, label_pattern
from lib.shared.campaign import resolve_campaign
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.foundation import (
    FoundationError, find_extensions, load_foundation,
)
from lib.shared.frontmatter import read_doc_with_frontmatter
from lib.shared.git_ops import step_commit
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import (
    EXTRACT_DIR, EXTRACT_INBOX, LATTICE, NOTE_DIR, WORKSPACE,
    inquiry_doc_path, load_inquiry, prompt_path,
)


EXTRACT_MODEL = "opus"
EXTRACT_EFFORT = "max"

EXTRACT_TEMPLATE = prompt_path("agents/producers/note_extract.md")


# ─── Spec parsing ──────────────────────────────────────────────────


def _parse_registry_labels(asn_content: str) -> List[str]:
    """Extract claim labels from the origin ASN's statement registry table."""
    labels = []
    in_table = False
    for line in asn_content.splitlines():
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
                for sub in parts[1].split(","):
                    sub = sub.strip()
                    if sub:
                        labels.append(sub)
        elif in_table and not line.startswith("|") and line.strip():
            break
    return labels


# ─── Spec promotion (workspace → substrate) ────────────────────────


def _promote_spec_to_substrate(
    session: Session, spec_filename: str,
):
    """Copy the workspace spec md into the substrate doc tree, register
    its path, emit `extract` classifier. Returns (substrate_path,
    spec_addr) or None if missing.
    """
    workspace_path = EXTRACT_INBOX / spec_filename
    if not workspace_path.exists():
        print(
            f"  [ERROR] Extract spec not found in workspace: "
            f"{workspace_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        return None

    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    substrate_path = EXTRACT_DIR / spec_filename
    shutil.copy2(workspace_path, substrate_path)

    substrate_rel = str(substrate_path.resolve().relative_to(WORKSPACE.resolve()))
    spec_addr = session.store.register_path(substrate_rel)
    emit_extract(session.store, spec_addr)

    print(
        f"  [PROMOTE] {workspace_path.relative_to(WORKSPACE)} → "
        f"{substrate_path.relative_to(WORKSPACE)}",
        file=sys.stderr,
    )
    return substrate_path, spec_addr


# ─── Validation ────────────────────────────────────────────────────


def _validate_spec(
    extract_from: int, create_note: int, absorb_into: int,
    claim_labels: List[str],
) -> Tuple[Path, str, dict] | None:
    """Validate spec frontmatter. Returns (origin_path, origin_content,
    absorb_into_inquiry) or None on error."""
    if extract_from == absorb_into:
        print(
            f"  [ERROR] extract_from and absorb_into cannot be the same ASN",
            file=sys.stderr,
        )
        return None

    origin_path, _ = find_asn(str(extract_from))
    if origin_path is None:
        print(
            f"  [ERROR] extract_from {format_label(extract_from)} not found",
            file=sys.stderr,
        )
        return None

    absorb_inquiry = load_inquiry(absorb_into)
    if not absorb_inquiry:
        print(
            f"  [ERROR] absorb_into {format_label(absorb_into)} has no inquiry doc",
            file=sys.stderr,
        )
        return None

    new_label = format_label(create_note)
    existing = list(NOTE_DIR.glob(f"{new_label}-*.md"))
    if existing:
        print(
            f"  [ERROR] create_note {new_label} already exists",
            file=sys.stderr,
        )
        return None

    origin_content = origin_path.read_text()
    registry_labels = _parse_registry_labels(origin_content)
    missing = [c for c in claim_labels if c not in registry_labels]
    if missing:
        print(
            f"  [ERROR] Claims not in extract_from registry: "
            f"{', '.join(missing)}",
            file=sys.stderr,
        )
        print(
            f"  Available labels: {', '.join(registry_labels)}",
            file=sys.stderr,
        )
        return None

    return origin_path, origin_content, absorb_inquiry


# ─── Naming derivation ─────────────────────────────────────────────


def _derive_names(
    absorb_title: str, absorb_into: int,
) -> Tuple[str, str]:
    """Compute slug and title for the new workshop ASN.

    The new ASN is named as the n-th extension of absorb_into:
    slug = '<absorb-title-slug>-<n>', title = '<absorb-title> <n>'.
    """
    n = len(find_extensions(absorb_into))
    base_slug = absorb_title.lower().replace(" ", "-")
    return f"{base_slug}-{n}", f"{absorb_title} {n}"


# ─── Prompt build ──────────────────────────────────────────────────


def _build_prompt(
    *, origin_content: str, foundation_statements: str,
    absorb_into_statements: str, claims: List[str],
    new_label: str, new_title: str,
    absorb_into_label: str, absorb_into_title: str,
    origin_label: str, rationale: str,
) -> str | None:
    template = read_prompt(EXTRACT_TEMPLATE)
    if not template:
        print("  [ERROR] Extract prompt template not found", file=sys.stderr)
        return None

    return (
        template
        .replace("{{rationale}}", rationale.strip() or "(none provided)")
        .replace("{{origin_content}}", origin_content)
        .replace("{{foundation_statements}}", foundation_statements)
        .replace("{{absorb_into_statements}}", absorb_into_statements)
        .replace("{{claims}}", ", ".join(claims))
        .replace("{{new_label}}", new_label)
        .replace("{{new_title}}", new_title)
        .replace("{{absorb_into_label}}", absorb_into_label)
        .replace("{{absorb_into_title}}", absorb_into_title)
        .replace("{{origin_label}}", origin_label)
        .replace("{{date}}", time.strftime("%Y-%m-%d"))
    )


def _strip_preamble(text: str) -> str:
    marker = re.search(rf"^# {label_pattern().pattern}", text, re.MULTILINE)
    return text[marker.start():] if marker else text


# ─── Lineage emission ──────────────────────────────────────────────


def _emit_lineage(
    session: Session, *, spec_addr: Address, new_path: Path,
    absorb_into_path: Path, origin_path: Path,
) -> Address:
    """Register the new note's path, emit classifier + lineage links +
    provenance edge. Returns the new note's substrate address."""
    new_rel = str(new_path.relative_to(WORKSPACE))
    absorb_into_rel = str(absorb_into_path.relative_to(WORKSPACE))
    origin_rel = str(origin_path.relative_to(WORKSPACE))

    new_addr = session.store.register_path(new_rel)
    absorb_into_addr = session.get_addr_for_path(absorb_into_rel)
    origin_addr = session.get_addr_for_path(origin_rel)

    emit_note(session.store, new_addr)
    emit_extends(session.store, new_addr, absorb_into_addr)
    emit_source(session.store, new_addr, origin_addr)
    emit_provenance_extract(session.store, spec_addr, new_addr)
    return new_addr


# ─── Agent class ───────────────────────────────────────────────────


class NoteExtractAgent(Agent):
    """One extract per fire — pure producer (operator-gated).

    Reads operator intent from a workspace spec md (extract_from /
    create_note / absorb_into / claims + rationale), promotes the spec
    to substrate, generates the new workshop ASN, emits lineage. Does
    not drive convergence on the new ASN; the runner walks it normally
    afterward.
    """

    role: ClassVar[str] = "note-extract"

    def __init__(
        self, *,
        model: str = EXTRACT_MODEL,
        effort: str = EXTRACT_EFFORT,
    ):
        self.model = model
        self.effort = effort

    def run(
        self, session: Session, addr: Address,
        *, spec_filename: str,
    ) -> AgentResult:
        # `addr` is unused for pure operator-gated producers — the
        # spec doc carries all targeting info. We accept it to match
        # the Agent base shape (predicate-fired agents key on a
        # target addr; pure producers don't but share the dispatch
        # surface).
        del addr

        # Renderers must be registered before we read absorb_into's
        # claim-statements transclusion view.
        import lib.renderers  # noqa: F401
        from lib.renderers.claim_statements import read_claim_statements_view

        # 1. Promote workspace spec → substrate, capture spec address
        promotion = _promote_spec_to_substrate(session, spec_filename)
        if promotion is None:
            return AgentResult(success=False, detail="spec-not-in-workspace")
        substrate_path, spec_addr = promotion

        # 2. Parse spec frontmatter + body
        fm, body = read_doc_with_frontmatter(substrate_path)
        try:
            extract_from = int(fm["extract_from"])
            create_note = int(fm["create_note"])
            absorb_into = int(fm["absorb_into"])
            claim_labels = [str(c).strip() for c in fm["claims"]]
        except (KeyError, ValueError, TypeError) as e:
            return AgentResult(
                success=False,
                detail=f"spec-frontmatter-malformed: {e}",
            )

        # 3. Validate
        validated = _validate_spec(
            extract_from, create_note, absorb_into, claim_labels,
        )
        if validated is None:
            return AgentResult(success=False, detail="validation-failed")
        origin_path, origin_content, absorb_inquiry = validated

        # 4. Derive new ASN's slug + title from absorb_into
        absorb_title = absorb_inquiry.get("title", "")
        new_slug, new_title = _derive_names(absorb_title, absorb_into)

        new_label = format_label(create_note)
        absorb_into_label = format_label(absorb_into)
        origin_label = format_label(extract_from)

        os.environ.setdefault("PROTOCOL_ASN_LABEL", new_label)

        # 5. Load destination context (statements + foundation)
        absorb_into_path, _ = find_asn(str(absorb_into))
        absorb_into_statements = (
            read_claim_statements_view(session, absorb_into_label)
            or "(no claim-statements export available)"
        )
        try:
            foundation = load_foundation(absorb_into)
        except FoundationError as e:
            print(
                f"  [FOUNDATION] {absorb_into_label}: {e}",
                file=sys.stderr,
            )
            return AgentResult(
                success=False,
                detail=f"foundation-load-failed: {e}",
            )

        # 6. Build prompt
        prompt = _build_prompt(
            origin_content=origin_content,
            foundation_statements=foundation,
            absorb_into_statements=absorb_into_statements,
            claims=claim_labels,
            new_label=new_label,
            new_title=new_title,
            absorb_into_label=absorb_into_label,
            absorb_into_title=absorb_title,
            origin_label=origin_label,
            rationale=body,
        )
        if prompt is None:
            return AgentResult(success=False, detail="prompt-template-missing")

        print(
            f"  [EXTRACT] {new_label} (extract_from {origin_label}, "
            f"absorb_into {absorb_into_label}, "
            f"claims {', '.join(claim_labels)})",
            file=sys.stderr,
        )

        # 7. Invoke LLM
        result = invoke_claude(prompt, model=self.model, effort=self.effort)
        if not result.text:
            return AgentResult(success=False, detail="llm-no-output")
        log_usage(
            "extract", result.elapsed,
            extract_from=extract_from, create_note=create_note,
            absorb_into=absorb_into, claims=claim_labels,
        )

        # 8. Write new note file
        text = _strip_preamble(result.text)
        NOTE_DIR.mkdir(parents=True, exist_ok=True)
        new_path = NOTE_DIR / f"{new_label}-{new_slug}.md"
        new_path.write_text(text + "\n")
        print(f"  [WROTE] {new_path.relative_to(WORKSPACE)}", file=sys.stderr)

        # 9. Emit substrate lineage
        _emit_lineage(
            session,
            spec_addr=spec_addr,
            new_path=new_path,
            absorb_into_path=absorb_into_path,
            origin_path=origin_path,
        )
        print(
            f"  [LINEAGE] note classifier; extends → {absorb_into_label}; "
            f"source → {origin_label}; provenance.extract from spec",
            file=sys.stderr,
        )

        # 10. Commit
        step_commit(
            f"extract(asn): {new_label} extract "
            f"{', '.join(claim_labels)} from {origin_label} "
            f"into {absorb_into_label} workshop"
        )

        return AgentResult(
            success=True,
            detail=(
                f"new={new_label} from={origin_label} "
                f"absorb_into={absorb_into_label} "
                f"claims={','.join(claim_labels)}"
            ),
        )
