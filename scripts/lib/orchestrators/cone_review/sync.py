"""Sync substrate citation links to a claim's *Depends:* / *Forward References:*
sections.

The .md is the source of truth for what citation links should exist;
this brings substrate into agreement. Used as a safety net after
agentic revise operations: the reviser may edit prose without
emitting matching substrate calls.

Drift detection is set-comparison, not history-based — distributed-safe.
Two processes editing different claims don't interfere because their
substrate writes are scoped to different from-paths.

Claim-convergence-specific: knows the `*Depends:*` and
`*Forward References:*` markdown bullet conventions used by claim
files in this project. Not a substrate primitive — composes
substrate calls (active_links, emit_citation, emit_retraction) plus
the claim-document format the project uses.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from lib.backend.addressing import Address
from lib.backend.emit import emit_citation, emit_retraction
from lib.backend.predicates import active_links
from lib.backend.store import Store

_DEPENDS_HEADER = "- *Depends:*"
_FORWARD_HEADER = "- *Forward References:*"


def _md_labels_in_section(md_text: str, header: str) -> set[str]:
    """The set of bullet labels in a `*<Field>:*` section.

    Empty if the header is absent. The label is the first
    whitespace-delimited token after the `  - ` prefix.
    """
    in_section = False
    labels: set[str] = set()
    for line in md_text.split("\n"):
        if line.strip() == header.strip():
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("  - "):
            labels.add(line[4:].split(None, 1)[0])
        elif line.startswith("    ") or line.strip() == "":
            continue
        else:
            break
    return labels


def _substrate_labels(
    store: Store,
    claim_addr: Address,
    type_str: str,
    rev_index: Dict[Address, str],
) -> set[str]:
    """Labels currently active in the substrate as `type_str` citations
    from claim_addr."""
    out: set[str] = set()
    for link in active_links(store.state, type_str, from_set=[claim_addr]):
        for cited in link.to_set:
            if cited in rev_index:
                out.add(rev_index[cited])
    return out


def sync_claim_citations(
    store: Store,
    claim_addr: Address,
    label_index: Dict[str, Address],
) -> Optional[dict]:
    """Bring substrate `citation.depends` and `citation.forward` into
    agreement with the claim's md `*Depends:*` / `*Forward References:*`
    sections.

    For each direction:
    - Labels in .md but not in active substrate → emit citation
    - Labels in active substrate but not in .md → emit retraction

    Labels in .md that don't resolve in `label_index` are skipped.

    Returns a changes dict, or None if the .md file isn't on disk.
    """
    claim_path = store.path_for_addr(claim_addr)
    if claim_path is None:
        return None
    full_path = store.lattice_dir / claim_path
    if not full_path.exists():
        return None

    rev_index: Dict[Address, str] = {addr: lbl for lbl, addr in label_index.items()}
    md_text = full_path.read_text()

    md_depends = _md_labels_in_section(md_text, _DEPENDS_HEADER)
    md_forwards = _md_labels_in_section(md_text, _FORWARD_HEADER)
    sub_depends = _substrate_labels(
        store, claim_addr, "citation.depends", rev_index,
    )
    sub_forwards = _substrate_labels(
        store, claim_addr, "citation.forward", rev_index,
    )

    changes = {
        "depends": {"added": [], "retracted": []},
        "forward": {"added": [], "retracted": []},
    }

    for label in sorted(md_depends - sub_depends):
        if label not in label_index:
            continue
        emit_citation(
            store, claim_addr, label_index[label], direction="depends",
        )
        changes["depends"]["added"].append(label)

    for label in sorted(sub_depends - md_depends):
        if label not in label_index:
            continue
        # Find the active citation link to retract
        for link in active_links(
            store.state, "citation.depends",
            from_set=[claim_addr], to_set=[label_index[label]],
        ):
            emit_retraction(store, claim_addr, link.addr)
            changes["depends"]["retracted"].append(label)
            break  # only retract once per label

    for label in sorted(md_forwards - sub_forwards):
        if label not in label_index:
            continue
        emit_citation(
            store, claim_addr, label_index[label], direction="forward",
        )
        changes["forward"]["added"].append(label)

    for label in sorted(sub_forwards - md_forwards):
        if label not in label_index:
            continue
        for link in active_links(
            store.state, "citation.forward",
            from_set=[claim_addr], to_set=[label_index[label]],
        ):
            emit_retraction(store, claim_addr, link.addr)
            changes["forward"]["retracted"].append(label)
            break

    return changes
