#!/usr/bin/env python3
"""Status of the design-digest pipeline over design-classes.yaml.

For each note: number, title, class, whether a design exists, how many
reviews it has, and the latest verdict. No dependencies — just progress.

    python scripts/design-digest-status.py
    python scripts/design-digest-status.py --classes foundations
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CLASSES_YAML = ROOT / "_workspace/design-classes.yaml"
FALLBACK_CLASSES = ROOT / "_workspace/asn-classes.yaml"
NOTE_DIR = ROOT / "_docuverse/documents/1.1/1/note"
DESIGN_ROOT = ROOT / "_design"


def _title(asn: int) -> str:
    hits = [p for p in NOTE_DIR.glob(f"ASN-{asn:04d}-*.md")
            if ".statements." not in p.name]
    if not hits:
        return "(no note)"
    first = hits[0].read_text().splitlines()[0] if hits[0].stat().st_size else ""
    return re.sub(r"^#\s*ASN-\d+:\s*", "", first).strip() or "(untitled)"


def _state(asn: int):
    label = f"ASN-{asn:04d}"
    design = (DESIGN_ROOT / "designs" / label / "design.md").exists()
    rdir = DESIGN_ROOT / "reviews" / label
    reviews = sorted(rdir.glob("review-*.md"),
                     key=lambda p: int(re.search(r"(\d+)", p.name).group(1)))
    n = len(reviews)
    last = "-"
    if reviews:
        hits = re.findall(r"VERDICT:\s*\**\s*(SHIP|REVISE)\b",
                          reviews[-1].read_text(), re.IGNORECASE)
        last = hits[-1].upper() if hits else "?"
    return design, n, last


def main():
    ap = argparse.ArgumentParser(description="Design-digest pipeline status.")
    ap.add_argument("--classes", help="comma-list of classes (default: all)")
    args = ap.parse_args()

    cf = CLASSES_YAML if CLASSES_YAML.exists() else FALLBACK_CLASSES
    data = yaml.safe_load(cf.read_text())
    include = set(args.classes.split(",")) if args.classes else set(data)
    rows = sorted({(int(n), cls) for cls, members in data.items()
                   if cls in include for n in members})

    hdr = f"{'#':<3} {'ASN':<9} {'title':<34} {'class':<12} {'design':<7} {'reviews':<8} {'last':<7}"
    print(hdr)
    print("─" * len(hdr))
    shipped = drafted = none = 0
    for i, (n, cls) in enumerate(rows, 1):
        design, nr, last = _state(n)
        if not design:
            none += 1
        elif last == "SHIP":
            shipped += 1
        else:
            drafted += 1
        title = _title(n)
        title = title[:33] + "…" if len(title) > 34 else title
        print(f"{i:<3} ASN-{n:04d}  {title:<34} {cls:<12} "
              f"{'yes' if design else '-':<7} {nr:<8} {last:<7}")
    print("─" * len(hdr))
    print(f"{len(rows)} notes — shipped:{shipped} in-progress:{drafted} not-started:{none}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
