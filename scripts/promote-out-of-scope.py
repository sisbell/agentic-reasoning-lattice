#!/usr/bin/env python3
"""
Promote Out-of-Scope — evaluate review deferrals for new ASN creation.

Reads OUT_OF_SCOPE items from an ASN's reviews, asks Claude which warrant
their own ASN, creates note.yaml for each promoted item.

Usage:
    python scripts/promote-out-of-scope.py 34
    python scripts/promote-out-of-scope.py 34 --dry-run
    python scripts/promote-out-of-scope.py 34 --model sonnet
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, REVIEWS_DIR, LATTICE_PROMPTS
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.git_ops import step_commit_asn
from lib.shared.invoke_claude import invoke_claude
from lib.maturation.promotion_promote import (
    load_existing_inquiries, next_asn_number, parse_promoted,
    create_note_yaml, load_existing_promotion, save_promotion_report,
)

PROMPTS_DIR = LATTICE_PROMPTS / "discovery" / "promotion"
TEMPLATE = PROMPTS_DIR / "promote-out-of-scope.md"


def _collect_out_of_scope(asn_label):
    """Collect OUT_OF_SCOPE sections from all reviews for an ASN.

    Returns formatted text with source labels.
    """
    review_dir = REVIEWS_DIR / asn_label
    if not review_dir.exists():
        return ""

    parts = []
    for review_path in sorted(review_dir.glob("review-*.md")):
        text = review_path.read_text()
        # Find OUT_OF_SCOPE section
        m = re.search(r'## OUT_OF_SCOPE\b(.*?)(?=\n## |\Z)',
                      text, re.DOTALL)
        if m:
            section = m.group(1).strip()
            if section:
                parts.append(f"### From {review_path.name}\n\n{section}")

    return "\n\n---\n\n".join(parts) if parts else "(none)"


def main():
    parser = argparse.ArgumentParser(
        description="Promote review out-of-scope items into new ASNs")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show promotion report without creating files")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    # Load template
    template = read_file(TEMPLATE)
    if not template:
        print(f"  Prompt template not found: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)

    # Collect out-of-scope items from reviews
    defer_items = _collect_out_of_scope(asn_label)
    if defer_items == "(none)":
        print(f"  No OUT_OF_SCOPE items found in reviews for {asn_label}",
              file=sys.stderr)
        sys.exit(0)

    # Load existing inquiries for dedup context
    inquiries_text = load_existing_inquiries()

    # Load existing promotion for this ASN
    existing_promotion = load_existing_promotion(asn_num, "out-of-scope")

    # Build prompt
    prompt = (template
              .replace("{{defer_items}}", defer_items)
              .replace("{{inquiries}}", inquiries_text)
              .replace("{{existing_promotion}}", existing_promotion or "(none)"))

    print(f"  [PROMOTE] {asn_label} — out-of-scope", file=sys.stderr)
    print(f"  Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Would invoke {args.model}", file=sys.stderr)
        sys.exit(0)

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)
    log_usage("promote-out-of-scope", elapsed, asn=asn_num)

    if not text:
        print(f"  No output from {args.model}", file=sys.stderr)
        sys.exit(1)

    # Parse promoted items
    promoted = parse_promoted(text)

    if promoted:
        print(f"\n  {len(promoted)} new ASN(s) promoted:", file=sys.stderr)
        cur_num = next_asn_number()
        for item in promoted:
            if "title" not in item or "question" not in item:
                print(f"  [SKIP] Incomplete item: {item}", file=sys.stderr)
                continue
            area = item.get("area", "")
            nelson = item.get("nelson", 10)
            gregory = item.get("gregory", 10)
            print(f"    ASN-{cur_num:04d}: {item['title']} [{area}]",
                  file=sys.stderr)
            create_note_yaml(cur_num, item["title"], item["question"],
                                area, asn_num, nelson=nelson, gregory=gregory)
            cur_num += 1
    else:
        print(f"\n  No new ASNs promoted from {asn_label}", file=sys.stderr)

    # Save promotion report
    save_promotion_report(asn_num, "out-of-scope", text)

    # Commit
    step_commit_asn(asn_num, f"promote(out-of-scope): {asn_label}")

    print(f"\n  [NEXT] Run ./run/generate-index.sh to update index",
          file=sys.stderr)


if __name__ == "__main__":
    main()
