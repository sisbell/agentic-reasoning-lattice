#!/usr/bin/env python3
"""
Extract claims from a source ASN into a new extension ASN.

Usage:
    python scripts/note-extend.py -s 53 -t 57 -b 34 --claims D0,D1
    python scripts/note-extend.py --source 53 --target 57 --base 34 --claims D0,D1
"""

import argparse
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.note_convergence.manage.extend import (
    parse_registry_labels, validate, derive_names, compute_depends,
    build_prompt, strip_preamble, write_manifest,
)
from lib.shared.paths import WORKSPACE, NOTES_DIR, formal_stmts
from lib.shared.common import read_file, find_asn, invoke_claude, log_usage, step_commit
from lib.shared.foundation import load_foundation_for_note


def main():
    parser = argparse.ArgumentParser(
        description="Extract claims from a source ASN into a new "
                    "extension ASN")
    parser.add_argument("-s", "--source", type=int, required=True,
                        help="Source ASN number (where claims live now)")
    parser.add_argument("-t", "--target", type=int, required=True,
                        help="New ASN number to create")
    parser.add_argument("-b", "--base", type=int, required=True,
                        help="Base ASN that the new extension extends")
    parser.add_argument("--claims", required=True,
                        help="Comma-separated claim labels to extract")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    claim_labels = [p.strip() for p in args.claims.split(",")]

    # Validate
    source_path, source_content, base_manifest = validate(
        args.source, args.target, args.base, claim_labels)

    base_title = base_manifest.get("title", "")
    slug, ext_title = derive_names(base_title, args.base)
    depends = compute_depends(args.base)

    # Load foundation context
    base_label = f"ASN-{args.base:04d}"
    base_stmt_path = formal_stmts(args.base)
    base_statements = read_file(base_stmt_path) or "(No base export available)"

    # Load foundation for the base's dependencies
    base_path, _ = find_asn(str(args.base))
    foundation_stmts = (
        load_foundation_for_note(base_path, args.base) if depends else ""
    )

    # Build prompt
    target_label = f"ASN-{args.target:04d}"
    source_label = f"ASN-{args.source:04d}"

    print(f"  [EXTEND] {target_label} (extends {base_label}, "
          f"claims {', '.join(claim_labels)} from {source_label})",
          file=sys.stderr)

    prompt = build_prompt(source_content, claim_labels, args.target,
                          args.base, args.source, base_title, ext_title,
                          base_statements, foundation_stmts)

    print(f"  Prompt: {len(prompt) // 1024}KB "
          f"(~{len(prompt) // 4} tokens est.)", file=sys.stderr)

    if args.dry_run:
        print(f'  [DRY RUN] Would invoke {args.model}', file=sys.stderr)
        print(f"  Target: {target_label} ({ext_title})", file=sys.stderr)
        print(f"  Slug: {slug}", file=sys.stderr)
        print(f"  Depends: {depends}", file=sys.stderr)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model,
                                  effort=args.effort)
    if not text:
        print("  [ERROR] No extension ASN produced", file=sys.stderr)
        sys.exit(1)

    # Strip preamble
    text = strip_preamble(text)

    # Write reasoning doc
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    asn_path = NOTES_DIR / f"{target_label}-{slug}.md"
    asn_path.write_text(text + "\n")
    print(f"  [WROTE] {asn_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Write project model
    yaml_path = write_manifest(args.target, ext_title, args.base,
                               args.source, depends, claim_labels)
    print(f"  [WROTE] {yaml_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Log usage
    log_usage("extend", elapsed, source=args.source, target=args.target,
              base=args.base, claims=claim_labels)

    # Commit
    print(f"\n  === COMMIT ===", file=sys.stderr)
    step_commit(f"extend(asn): {target_label} extract "
                f"{', '.join(claim_labels)} from {source_label} "
                f"into {base_label} extension")

    # Hints
    print(f"\n  [NEXT] Review: python scripts/note-review.py {args.target}",
          file=sys.stderr)
    print(f"  [NEXT] Or review/revise loop: "
          f"python scripts/note-revise.py {args.target} --converge",
          file=sys.stderr)
    print(f"  [NEXT] Then export: python scripts/normalize.py {args.target}",
          file=sys.stderr)
    print(f"  [NEXT] Then absorb: python scripts/absorb.py {args.target}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
