#!/usr/bin/env python3
"""
Promote Open Questions — evaluate ASN open questions for new ASN creation.

Reads an ASN's open questions section, asks Claude which warrant their own
ASN, creates note.yaml for each promoted question.

Usage:
    python scripts/promote-open-questions.py 34
    python scripts/promote-open-questions.py 34 --dry-run
    python scripts/promote-open-questions.py 34 --model sonnet
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE
from lib.shared.common import find_asn, invoke_claude, read_file, log_usage, step_commit_asn
from lib.discovery.promotion.promote import (
    load_existing_inquiries, next_asn_number, parse_promoted,
    create_note_yaml, load_existing_promotion, save_promotion_report,
)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery" / "promotion"
TEMPLATE = PROMPTS_DIR / "promote-open-questions.md"


def main():
    parser = argparse.ArgumentParser(
        description="Promote ASN open questions into new ASNs")
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

    # Read ASN content
    asn_content = asn_path.read_text()

    # Load template
    template = read_file(TEMPLATE)
    if not template:
        print(f"  Prompt template not found: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)

    # Load existing inquiries for dedup context
    inquiries_text = load_existing_inquiries()

    # Load existing promotion for this ASN
    existing_promotion = load_existing_promotion(asn_num, "open-questions")

    # Build prompt
    prompt = (template
              .replace("{{asn_content}}", asn_content)
              .replace("{{inquiries}}", inquiries_text)
              .replace("{{existing_promotion}}", existing_promotion or "(none)"))

    print(f"  [PROMOTE] {asn_label} — open questions", file=sys.stderr)
    print(f"  Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Would invoke {args.model}", file=sys.stderr)
        sys.exit(0)

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)
    log_usage("promote-open-questions", elapsed, asn=asn_num)

    if not text:
        print(f"  No output from {args.model}", file=sys.stderr)
        sys.exit(1)

    # Parse promoted items
    promoted = parse_promoted(text)

    if promoted:
        print(f"\n  {len(promoted)} new ASN(s) promoted:", file=sys.stderr)
        cur_num = next_asn_number()
        created = []
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
            created.append(cur_num)
            cur_num += 1
    else:
        print(f"\n  No new ASNs promoted from {asn_label}", file=sys.stderr)

    # Save promotion report
    save_promotion_report(asn_num, "open-questions", text)

    # Commit
    step_commit_asn(asn_num, f"promote(open-questions): {asn_label}")

    print(f"\n  [NEXT] Run ./run/generate-index.sh to update index",
          file=sys.stderr)


if __name__ == "__main__":
    main()
