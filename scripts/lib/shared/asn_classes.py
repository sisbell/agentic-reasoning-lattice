"""ASN class membership (operator-edited at _workspace/asn-classes.yaml).

Three classes: core (default), operations, protocols. Notes default to
core; only non-core members are listed in the YAML. The runner's
--exclude flag (or EXCLUDE_CLASSES env var) drops the listed classes
from the walk. core is always included.

Used by `note-scheduler.py --dag`, `dag_status.py`, and the continuous
runner wrapper.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Set

from lib.shared.paths import WORKSPACE


CLASSES_YAML = WORKSPACE / "_workspace" / "asn-classes.yaml"

CORE = "core"
OPERATIONS = "operations"
PROTOCOLS = "protocols"

KNOWN_CLASSES = (CORE, OPERATIONS, PROTOCOLS)
EXCLUDABLE_CLASSES = (OPERATIONS, PROTOCOLS)  # core is always included


def _parse_yaml() -> Dict[str, List[int]]:
    """Parse the YAML by hand — `operations:` / `protocols:` sections,
    each a list of integers. Avoids a yaml-lib dependency for a tiny
    fixed-shape file.
    """
    out: Dict[str, List[int]] = {OPERATIONS: [], PROTOCOLS: []}
    if not CLASSES_YAML.exists():
        return out
    current = None
    list_item = re.compile(r"^\s*-\s*(\d+)\s*(?:#.*)?$")
    section = re.compile(r"^(operations|protocols)\s*:\s*(\[\s*\])?\s*$")
    with open(CLASSES_YAML) as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            m = section.match(line)
            if m:
                current = m.group(1)
                continue
            m = list_item.match(line)
            if m and current in (OPERATIONS, PROTOCOLS):
                out[current].append(int(m.group(1)))
    return out


def class_for(asn_number: int) -> str:
    """Return the class label for a given ASN number. Defaults to core."""
    data = _parse_yaml()
    if asn_number in data[OPERATIONS]:
        return OPERATIONS
    if asn_number in data[PROTOCOLS]:
        return PROTOCOLS
    return CORE


def parse_exclude_arg(value: str | None) -> Set[str]:
    """Parse a comma-separated --exclude value into a set of class
    labels. Empty / None / 'none' yields an empty set."""
    if value is None or not value.strip() or value.strip().lower() == "none":
        return set()
    out: Set[str] = set()
    for token in value.split(","):
        t = token.strip().lower()
        if not t:
            continue
        if t not in EXCLUDABLE_CLASSES:
            valid = ",".join(EXCLUDABLE_CLASSES)
            raise ValueError(
                f"invalid --exclude class {t!r}; "
                f"must be one of: {valid}"
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
    - core is never excluded (passing 'core' is rejected at the
      parse_exclude_arg layer).
    - Unrecognized ASN numbers default to core and are kept.
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
