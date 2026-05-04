#!/usr/bin/env python3
"""
Absorb an extension ASN back into its base and update the source.

Usage:
    python scripts/note-absorb.py 57
    python scripts/note-absorb.py 57 --dry-run
"""

import argparse
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.maturation.absorb_merge_extension import (
    parse_extension_labels, validate,
    step_integrate, step_review_revise, step_export,
    step_update_source, step_cleanup,
)
from lib.shared.common import log_usage
from lib.shared.git_ops import step_commit


def main():
    parser = argparse.ArgumentParser(
        description="Absorb an extension ASN back into its base")
    parser.add_argument("asn", type=int,
                        help="Extension ASN number to absorb")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--max-cycles", type=int, default=5,
                        help="Max review/revise cycles for integration "
                             "(default: 5)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ext_label = f"ASN-{args.asn:04d}"

    # Validate
    base_num, source_num, ext_path, base_path = validate(args.asn)
    base_label = f"ASN-{int(base_num):04d}"

    print(f"  [ABSORB] {ext_label} → {base_label}", file=sys.stderr)
    if source_num:
        print(f"  [SOURCE] ASN-{int(source_num):04d} — run rebase.py "
              f"{source_num} after absorb to update citations",
              file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Steps: integrate → review/revise → "
              f"export → cleanup", file=sys.stderr)
        return

    # Step 1: Integrate extension into base reasoning doc
    ok = step_integrate(args.asn, base_num, ext_path, base_path,
                        args.model, args.effort)
    if not ok:
        print(f"  [ABORT] Integration failed", file=sys.stderr)
        sys.exit(1)

    step_commit(f"absorb(asn): integrate {ext_label} into {base_label}")

    # Step 2: Review/revise the integration
    ext_content = ext_path.read_text()
    claim_labels = parse_extension_labels(ext_content)
    step_review_revise(base_num, base_path, claim_labels,
                       args.max_cycles, args.model, args.effort)

    # Step 3: Re-export the base
    step_export(base_num)

    # Step 4: Clean up extension artifacts
    step_cleanup(args.asn)
    step_commit(f"absorb(asn): cleanup {ext_label}")

    log_usage("absorb", 0, ext=args.asn, base=base_num)
    print(f"\n  [DONE] {ext_label} absorbed into {base_label}",
          file=sys.stderr)
    if source_num:
        print(f"  [NEXT] Run: ./run/run-discovery.sh {source_num}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
