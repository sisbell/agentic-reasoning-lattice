#!/usr/bin/env python3
"""
Supersede an ASN with a new ASN number.

Usage:
    python scripts/note-supersede.py --source 48 --target 59
    python scripts/note-supersede.py -s 48 -t 59
    python scripts/note-supersede.py -s 48 -t 59 --dry-run
"""

import argparse
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.note_convergence.supersede import (
    validate, copy_project_model, copy_consultations, remove_source,
)
from lib.shared.common import step_commit


def main():
    parser = argparse.ArgumentParser(
        description="Supersede an ASN with a new ASN number")
    parser.add_argument("-s", "--source", type=int, required=True,
                        help="Source ASN number to supersede")
    parser.add_argument("-t", "--target", type=int, required=True,
                        help="Target ASN number (the replacement)")
    parser.add_argument("--keep", action="store_true",
                        help="Keep the source project model (for comparison)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without doing it")
    args = parser.parse_args()

    source_label, target_label = validate(args.source, args.target)

    print(f"  [SUPERSEDE] {source_label} → {target_label}", file=sys.stderr)
    if args.keep:
        print(f"  [KEEP] Source project model will be preserved",
              file=sys.stderr)

    if args.dry_run:
        action = "copy project model and questions"
        if not args.keep:
            action += ", remove source"
        print(f"  [DRY RUN] Would {action}", file=sys.stderr)
        return

    # Copy project model
    copy_project_model(args.source, args.target, source_label, target_label)

    # Copy consultations/questions
    copy_consultations(args.source, args.target, source_label, target_label)

    # Remove source project model (unless --keep)
    if not args.keep:
        remove_source(args.source, source_label)

    # Commit
    print(f"\n  === COMMIT ===", file=sys.stderr)
    step_commit(f"supersede(asn): {source_label} → {target_label}")

    print(f"\n  [DONE] {source_label} superseded by {target_label}",
          file=sys.stderr)
    print(f"  [NEXT] Generate questions: ./run/questions.sh {args.target}",
          file=sys.stderr)
    print(f"  [NEXT] Or consult+draft: python scripts/note-draft.py "
          f"--inquiries {args.target} --resume consult", file=sys.stderr)


if __name__ == "__main__":
    main()
