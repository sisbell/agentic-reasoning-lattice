"""ASN class membership (operator-edited at _workspace/asn-classes.yaml).

The YAML declares one or more classes; each class is a list of ASN
numbers. `core` is the implicit default for any ASN not listed under
another class — `core` is never declared explicitly in the YAML (any
such section is silently ignored) but CAN be excluded like any other
class.

Any class name is valid:

    operations:
      - 87
      - 88
    protocols:
      - 86
      - 94
    consult:        # arbitrary class for a bounded experiment
      - 68
      - 69

The runner's `--exclude` flag (or `EXCLUDE_CLASSES` env var) drops
any combination of classes from the walk. Examples:

    EXCLUDE_CLASSES=operations,protocols       # leaves consult + core
    EXCLUDE_CLASSES=core,operations,protocols  # leaves only consult

Used by `note-scheduler.py --dag`, `dag_status.py`, and the continuous
runner wrapper.
"""

from __future__ import annotations

import re
from typing import Dict, List, Set

from lib.shared.paths import WORKSPACE


CLASSES_YAML = WORKSPACE / "_workspace" / "asn-classes.yaml"

CORE = "core"


_SECTION_RE = re.compile(r"^([a-z][a-z0-9-]*)\s*:\s*(\[\s*\])?\s*(?:#.*)?$")
_LIST_ITEM_RE = re.compile(r"^\s*-\s*(\d+)\s*(?:#.*)?$")


def _parse_yaml() -> Dict[str, List[int]]:
    """Parse the YAML by hand — any `name: [int list]` section. Returns
    a dict mapping class name → list of ASN ids. `core` is implicit
    (never appears as a key); if declared as a section, it's silently
    ignored to enforce the "core is the default" rule.
    """
    out: Dict[str, List[int]] = {}
    if not CLASSES_YAML.exists():
        return out
    current = None
    with open(CLASSES_YAML) as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            m = _SECTION_RE.match(line)
            if m:
                name = m.group(1)
                if name == CORE:
                    current = None
                    continue
                current = name
                if current not in out:
                    out[current] = []
                continue
            m = _LIST_ITEM_RE.match(line)
            if m and current is not None:
                out[current].append(int(m.group(1)))
    return out


def class_for(asn_number: int) -> str:
    """Return the class label for a given ASN number. Defaults to core.

    If an ASN is (mis-)listed in multiple classes, returns the first
    match in YAML declaration order (Python dict preserves insertion
    order since 3.7).
    """
    data = _parse_yaml()
    for cls, members in data.items():
        if asn_number in members:
            return cls
    return CORE


def parse_exclude_arg(value: str | None) -> Set[str]:
    """Parse a comma-separated --exclude value into a set of class labels.

    Empty / None / 'none' yields an empty set. `core` is always valid
    (acts as "exclude all unlisted ASNs"). Any other token must name
    a class actually declared in the YAML.
    """
    if value is None or not value.strip() or value.strip().lower() == "none":
        return set()
    declared = set(_parse_yaml().keys())
    valid_choices = declared | {CORE}
    out: Set[str] = set()
    for token in value.split(","):
        t = token.strip().lower()
        if not t:
            continue
        if t not in valid_choices:
            valid_str = ", ".join(sorted(valid_choices))
            raise ValueError(
                f"invalid --exclude class {t!r}; "
                f"must be one of: {valid_str}",
            )
        out.add(t)
    return out


def apply_exclude(
    asn_labels: List[str],
    excluded_classes: Set[str],
) -> List[str]:
    """Filter an ordered list of ASN labels (`ASN-NNNN` form), dropping
    any whose class is in excluded_classes. Order preserved.

    Notes:
    - core can be excluded if explicitly listed; unrecognized ASN
      numbers default to core and get dropped when core is excluded.
    """
    if not excluded_classes:
        return list(asn_labels)
    out: List[str] = []
    label_pat = re.compile(r"ASN-(\d+)")
    for label in asn_labels:
        m = label_pat.match(label)
        if not m:
            out.append(label)
            continue
        cls = class_for(int(m.group(1)))
        if cls in excluded_classes:
            continue
        out.append(label)
    return out
