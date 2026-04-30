"""Sync substrate citation links to a claim's *Depends:* / *Forward References:* sections.

The .md is the source of truth for what citation links should exist;
this function brings substrate into agreement. Used as a safety net
after agentic revise operations: the reviser may edit prose without
emitting matching substrate calls, and the existing cite/retract CLIs
don't yet support forward direction. Auto-correct ensures drift can't
hide.

Drift detection is set-comparison, not history-based — distributed-safe.
Two processes editing different claims don't interfere because their
substrate writes are scoped to different from-paths.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import LATTICE
from lib.store.queries import active_links
from lib.store.cite import emit_citation
from lib.store.retract import emit_retraction


_DEPENDS_HEADER = "- *Depends:*"
_FORWARD_HEADER = "- *Forward References:*"


def _md_labels_in_section(md_text, header):
    """Return the set of bullet labels present in a `*<Field>:*` section.

    Empty set if the section header is absent. The label is the first
    whitespace-delimited token after the `  - ` prefix.
    """
    lines = md_text.split("\n")
    in_section = False
    labels = set()
    for line in lines:
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


def _substrate_labels(store, claim_md_rel, type_str, rev_index):
    """Return the set of labels currently active in the substrate as
    `type_str` citations from `claim_md_rel`."""
    labels = set()
    for link in active_links(store, type_str, from_set=[claim_md_rel]):
        if link["to_set"] and link["to_set"][0] in rev_index:
            labels.add(rev_index[link["to_set"][0]])
    return labels


def sync_claim_citations(store, claim_md_rel, label_index):
    """Bring substrate `citation.depends` and `citation.forward` into
    agreement with the .md's `*Depends:*` and `*Forward References:*`
    sections.

    For each direction:
    - Labels in .md but not in active substrate → emit citation
    - Labels in active substrate but not in .md → emit retraction

    Labels in .md that don't resolve in `label_index` are skipped (the
    .md may temporarily reference a label that hasn't been registered
    yet; retraction would be wrong, citation would fail validation).

    Returns a dict of changes for logging:
        {
            "depends": {"added": [...], "retracted": [...]},
            "forward": {"added": [...], "retracted": [...]},
        }
    or `None` if the .md file doesn't exist (claim was just deleted).
    """
    full_path = LATTICE / claim_md_rel
    if not full_path.exists():
        return None

    rev_index = {p: l for l, p in label_index.items()}
    md_text = full_path.read_text()

    md_depends = _md_labels_in_section(md_text, _DEPENDS_HEADER)
    md_forwards = _md_labels_in_section(md_text, _FORWARD_HEADER)
    sub_depends = _substrate_labels(store, claim_md_rel, "citation.depends", rev_index)
    sub_forwards = _substrate_labels(store, claim_md_rel, "citation.forward", rev_index)

    changes = {
        "depends": {"added": [], "retracted": []},
        "forward": {"added": [], "retracted": []},
    }

    for label in sorted(md_depends - sub_depends):
        if label not in label_index:
            continue
        emit_citation(store, claim_md_rel, label, label_index, direction="depends")
        changes["depends"]["added"].append(label)
    for label in sorted(sub_depends - md_depends):
        emit_retraction(store, claim_md_rel, label, label_index, direction="depends")
        changes["depends"]["retracted"].append(label)

    for label in sorted(md_forwards - sub_forwards):
        if label not in label_index:
            continue
        emit_citation(store, claim_md_rel, label, label_index, direction="forward")
        changes["forward"]["added"].append(label)
    for label in sorted(sub_forwards - md_forwards):
        emit_retraction(store, claim_md_rel, label, label_index, direction="forward")
        changes["forward"]["retracted"].append(label)

    return changes
