#!/usr/bin/env python3
"""Status of the design-digest pipeline over design-classes.yaml.

For each note: number, title, class, whether a design exists, how many
review/revise passes it has had. No dependencies, no verdict — just progress.

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


# Same tolerant verdict parse + 2-consecutive gate as design-digest.py.
_VERDICT_RE = re.compile(r"VERDICT:\s*\**\s*(CONVERGED|REVISE)\b", re.IGNORECASE)
CONVERGE_N = 2


def _converged(rdir: Path) -> bool:
    """True iff the most recent CONVERGE_N reviews are all CONVERGED."""
    ks = sorted(int(m.group(1)) for p in rdir.glob("review-*.md")
                for m in [re.match(r"review-(\d+)\.md$", p.name)] if m)
    streak = 0
    for k in reversed(ks):
        v = _VERDICT_RE.findall((rdir / f"review-{k}.md").read_text())
        if v and v[-1].upper() == "CONVERGED":
            streak += 1
        else:
            break
    return streak >= CONVERGE_N


def _state(asn: int):
    label = f"ASN-{asn:04d}"
    design = (DESIGN_ROOT / "designs" / label / "design.md").exists()
    rdir = DESIGN_ROOT / "reviews" / label
    n = len(list(rdir.glob("review-*.md")))
    return design, n, _converged(rdir) if n else False


def main():
    ap = argparse.ArgumentParser(description="Design-digest pipeline status.")
    ap.add_argument("--classes", help="comma-list of classes (default: all)")
    args = ap.parse_args()

    cf = CLASSES_YAML if CLASSES_YAML.exists() else FALLBACK_CLASSES
    data = yaml.safe_load(cf.read_text())
    include = set(args.classes.split(",")) if args.classes else set(data)
    rows = sorted({(int(n), cls) for cls, members in data.items()
                   if cls in include for n in members})

    hdr = (f"{'#':<3} {'ASN':<9} {'title':<36} {'class':<12} "
           f"{'design':<7} {'passes':<7} {'state':<10}")
    print(hdr)
    print("─" * len(hdr))
    have = none = converged = 0
    for i, (n, cls) in enumerate(rows, 1):
        design, nr, conv = _state(n)
        have += 1 if design else 0
        none += 0 if design else 1
        converged += 1 if conv else 0
        title = _title(n)
        title = title[:35] + "…" if len(title) > 36 else title
        state = "CONVERGED" if conv else ("reviewing" if nr else "-")
        print(f"{i:<3} ASN-{n:04d}  {title:<36} {cls:<12} "
              f"{'yes' if design else '-':<7} {nr:<7} {state:<10}")
    print("─" * len(hdr))
    print(f"{len(rows)} notes — have-design:{have} not-started:{none} "
          f"converged:{converged}", file=sys.stderr)


if __name__ == "__main__":
    main()
