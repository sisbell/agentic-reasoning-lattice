"""Citation-resolve orchestrator — per-claim and full-ASN sweep.

Mechanical loop that gathers existing classifications from substrate,
dispatches the citation-resolve agent
(`lib/agents/citation_resolve/`), then applies its output: edits the
claim's `.md` Depends/Forward sections, persists the resolve doc, and
emits substrate links (citation.depends/forward, retraction,
citation.resolve, provenance.derivation).

Two entry points:
- `run_classification(asn_num, claim_label)` — one claim
- `run_sweep(asn_num)` — every claim in the ASN
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from lib.provenance import attributed_to
from lib.agents.citation_resolve import extract_citation_classifications
from lib.backend.emit import emit_citation, emit_retraction
from lib.protocols.febe.protocol import Session
from lib.protocols.febe.session import open_session
from lib.lattice.labels import build_cross_asn_label_index
from lib.shared.common import (
    build_label_index, find_asn, step_commit_asn,
)
from lib.shared.paths import (
    CITATION_RESOLVE_DIR, CLAIM_DIR, LATTICE, claim_doc_path,
)


DEPENDS_HEADER = "- *Depends:*"
FORWARD_HEADER = "- *Forward References:*"


# ---------------------------------------------------------------------------
# Substrate queries


def _existing_classifications(
    session: Session, claim_md_rel: str, label_index: dict,
):
    """Return (depends_labels, forwards_labels) sourced from substrate."""
    rev_index = {addr: label for label, addr in label_index.items()}
    claim_addr = session.get_addr_for_path(claim_md_rel)
    if claim_addr is None:
        return [], []
    depends = []
    forwards = []
    for link in session.active_links(
        "citation.depends", from_set=[claim_addr],
    ):
        for cited in link.to_set:
            if cited in rev_index:
                depends.append(rev_index[cited])
    for link in session.active_links(
        "citation.forward", from_set=[claim_addr],
    ):
        for cited in link.to_set:
            if cited in rev_index:
                forwards.append(rev_index[cited])
    return sorted(depends), sorted(forwards)


def _validate_labels(classifications, retractions, label_index):
    """Every emitted label must resolve in the cross-ASN label index."""
    for c in classifications:
        if c["label"] not in label_index:
            raise ValueError(f"unknown label in classification: {c['label']!r}")
    for r in retractions:
        if r["label"] not in label_index:
            raise ValueError(f"unknown label in retraction: {r['label']!r}")


# ---------------------------------------------------------------------------
# .md section editing


def _find_section(lines, header):
    """Locate a `- *<Field>:*` section.

    Returns (start_idx, last_bullet_idx). Returns None if not present.
    """
    for i, line in enumerate(lines):
        if line.strip() == header.strip():
            last_bullet_idx = i
            for j in range(i + 1, len(lines)):
                ln = lines[j]
                if ln.startswith("  - "):
                    last_bullet_idx = j
                elif ln.startswith("    ") or ln.strip() == "":
                    continue
                else:
                    break
            return (i, last_bullet_idx)
    return None


def _bullet_label(bullet_line):
    return bullet_line[4:].split(None, 1)[0]


def _existing_section_labels(lines, header):
    section = _find_section(lines, header)
    if section is None:
        return set()
    start_idx, last_bullet_idx = section
    labels = set()
    for j in range(start_idx + 1, last_bullet_idx + 1):
        line = lines[j]
        if line.startswith("  - "):
            labels.add(_bullet_label(line))
    return labels


def _apply_changes(claim_md_path, classifications, retractions):
    """Apply classifications (insert bullets) and retractions (remove bullets).

    Retractions first (so a reclassify works: retract old direction,
    insert new). Bullet inserts dedup against labels already in the
    target section.
    """
    lines = claim_md_path.read_text().split("\n")

    for r in retractions:
        header = (
            DEPENDS_HEADER if r["direction"] == "depends" else FORWARD_HEADER
        )
        section = _find_section(lines, header)
        if section is None:
            raise ValueError(
                f"retraction target section {header!r} not in {claim_md_path}"
            )
        start_idx, last_bullet_idx = section
        removed = False
        for j in range(start_idx + 1, last_bullet_idx + 1):
            line = lines[j]
            if line.startswith("  - ") and _bullet_label(line) == r["label"]:
                del lines[j]
                removed = True
                break
        if not removed:
            raise ValueError(
                f"no bullet for {r['label']!r} in {header!r} of {claim_md_path}"
            )

    depends_to_add = [
        c for c in classifications if c["direction"] == "depends"
    ]
    forwards_to_add = [
        c for c in classifications if c["direction"] == "forward"
    ]

    if depends_to_add:
        section = _find_section(lines, DEPENDS_HEADER)
        if section is None:
            raise ValueError(
                f"no {DEPENDS_HEADER!r} section in {claim_md_path}; "
                f"cannot add depends bullets"
            )
        existing = _existing_section_labels(lines, DEPENDS_HEADER)
        depends_to_add = [
            c for c in depends_to_add if c["label"] not in existing
        ]
        if depends_to_add:
            _, last_bullet_idx = _find_section(lines, DEPENDS_HEADER)
            for c in reversed(depends_to_add):
                lines.insert(last_bullet_idx + 1, "  " + c["bullet"].lstrip())

    if forwards_to_add:
        existing = _existing_section_labels(lines, FORWARD_HEADER)
        forwards_to_add = [
            c for c in forwards_to_add if c["label"] not in existing
        ]
        if forwards_to_add:
            section = _find_section(lines, FORWARD_HEADER)
            if section is None:
                depends_section = _find_section(lines, DEPENDS_HEADER)
                if depends_section is None:
                    raise ValueError(
                        f"cannot create {FORWARD_HEADER!r}: no "
                        f"{DEPENDS_HEADER!r} to anchor it after in "
                        f"{claim_md_path}"
                    )
                _, depends_last = depends_section
                new_block = [FORWARD_HEADER]
                for c in forwards_to_add:
                    new_block.append("  " + c["bullet"].lstrip())
                for ln in reversed(new_block):
                    lines.insert(depends_last + 1, ln)
            else:
                _, last_bullet_idx = section
                for c in reversed(forwards_to_add):
                    lines.insert(
                        last_bullet_idx + 1, "  " + c["bullet"].lstrip()
                    )

    claim_md_path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Resolve-doc persistence


def _next_resolve_run(asn_label, claim_label):
    asn_dir = CITATION_RESOLVE_DIR / asn_label
    if not asn_dir.exists():
        return 1
    pat = re.compile(rf"^{re.escape(claim_label)}-(\d+)\.md$")
    nums = []
    for p in asn_dir.iterdir():
        m = pat.match(p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) if nums else 0) + 1


def _persist_resolve_doc(asn_label, claim_label, sonnet_output, model):
    """Write the resolve doc with a small header + raw Sonnet output."""
    run_num = _next_resolve_run(asn_label, claim_label)
    asn_dir = CITATION_RESOLVE_DIR / asn_label
    asn_dir.mkdir(parents=True, exist_ok=True)
    path = asn_dir / f"{claim_label}-{run_num}.md"
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    content = (
        f"# Citation Resolve — {asn_label}/{claim_label} — run {run_num}\n"
        f"\n"
        f"*{timestamp}*\n"
        f"*Model: {model}*\n"
        f"\n"
        f"## Output\n"
        f"\n"
        f"{sonnet_output.strip()}\n"
    )
    path.write_text(content)
    return path, run_num


# ---------------------------------------------------------------------------
# Substrate emission


def _emit_substrate(
    session: Session,
    claim_md_rel: str,
    classifications: list,
    retractions: list,
    resolve_doc_rel: str,
    label_index: dict,
):
    """Emit substrate links for one resolve operation.

    Order:
    1. citation.resolve classifier on the resolve doc
    2. citation.depends / citation.forward for each classification
    3. retraction for each retraction
    4. provenance.derivation from the resolve doc to each emitted link
    """
    store = session.store
    resolve_doc_addr = store.register_path(resolve_doc_rel)
    claim_addr = store.register_path(claim_md_rel)

    store.make_link(
        homedoc=resolve_doc_addr,
        from_set=[],
        to_set=[resolve_doc_addr],
        type_="citation.resolve",
    )

    derivation_targets = []
    for c in classifications:
        cited_addr = label_index.get(c["label"])
        if cited_addr is None:
            continue
        link, _ = emit_citation(
            store, claim_addr, cited_addr, direction=c["direction"],
        )
        derivation_targets.append(link.addr)
    for r in retractions:
        cited_addr = label_index.get(r["label"])
        if cited_addr is None:
            continue
        type_str = f"citation.{r['direction']}"
        for cand in session.active_links(
            type_str, from_set=[claim_addr], to_set=[cited_addr],
        ):
            retraction = emit_retraction(store, claim_addr, cand.addr)
            derivation_targets.append(retraction.addr)
            break  # retract one matching link per (claim, target, direction)

    for target_addr in derivation_targets:
        store.make_link(
            homedoc=resolve_doc_addr,
            from_set=[resolve_doc_addr],
            to_set=[target_addr],
            type_="provenance.derivation",
        )


# ---------------------------------------------------------------------------
# Entrypoints


@attributed_to("citation-resolve")
def run_classification(asn_num, claim_label, model="sonnet"):
    """Run citation-resolve on one claim. Returns "ok" or "failed"."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    os.environ.setdefault("PROTOCOL_ASN_LABEL", asn_label)

    claim_md_rel = claim_doc_path(asn_label, claim_label)
    claim_md_full = LATTICE / claim_md_rel
    if not claim_md_full.exists():
        print(
            f"  {claim_label}.md not found at {claim_md_full}",
            file=sys.stderr,
        )
        return "failed"

    claim_md_content = claim_md_full.read_text()

    session = open_session(LATTICE)
    label_index = build_cross_asn_label_index(session.store)
    depends, forwards = _existing_classifications(
        session, claim_md_rel, label_index,
    )

    claim_dir = claim_md_full.parent
    claims_root = claim_dir.parent

    print(
        f"  [RESOLVE] {asn_label}/{claim_label} ({model})...",
        end="", file=sys.stderr, flush=True,
    )
    result = extract_citation_classifications(
        claim_md_content, claim_dir, claims_root, depends, forwards,
        model=model,
    )
    print(f" ({result.elapsed_seconds:.0f}s)", file=sys.stderr)

    if not result.classifications and not result.retractions:
        print(
            f"  [RESOLVE] {claim_label}: no changes",
            file=sys.stderr,
        )
        return "ok"

    _validate_labels(result.classifications, result.retractions, label_index)
    _apply_changes(claim_md_full, result.classifications, result.retractions)

    resolve_path, run_num = _persist_resolve_doc(
        asn_label, claim_label, result.raw_text, model,
    )
    resolve_rel = str(resolve_path.relative_to(LATTICE))

    _emit_substrate(
        session, claim_md_rel, result.classifications, result.retractions,
        resolve_rel, label_index,
    )

    n_class = len(result.classifications)
    n_retr = len(result.retractions)
    print(
        f"  [RESOLVE] {claim_label}: {n_class} classifications, "
        f"{n_retr} retractions, run {run_num}",
        file=sys.stderr,
    )

    step_commit_asn(
        asn_num,
        hint=(
            f"citation-resolve(asn): ASN-{asn_num:04d}/{claim_label} — "
            f"{n_class} classifications, {n_retr} retractions"
        ),
    )
    return "ok"


@attributed_to("citation-resolve")
def run_sweep(asn_num, model="sonnet"):
    """Iterate every claim in the ASN; run citation-resolve on each."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(f"  {claim_dir} not found", file=sys.stderr)
        return "failed"

    labels = sorted(build_label_index(claim_dir).keys())
    print(
        f"\n  [RESOLVE-SWEEP] {asn_label} — {len(labels)} claims",
        file=sys.stderr,
    )

    for label in labels:
        run_classification(asn_num, label, model=model)

    return "ok"
