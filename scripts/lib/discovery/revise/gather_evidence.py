#!/usr/bin/env python3
"""
Gather evidence for revision — assign channels to REVISE findings, consult.

Reads a review's REVISE items + the ASN, asks an LLM to decide which channels
(theory and/or evidence) each finding needs, then runs those channel
consultations. Produces a results file for the revise agent to consume.

Assignment prompt, parser, and display-name logic live in the shared
lib module scripts/lib/discovery/revise/assign_channels.py — tolerant parser
that handles both role-labeled ("Theory"/"Evidence") and channel-named
("Nelson"/"Gregory"/"Maxwell-1867"/...) responses.

Usage:
    python scripts/lib/discovery/revise/gather_evidence.py 9              # latest review
    python scripts/lib/discovery/revise/gather_evidence.py 9 review-3     # specific review
    python scripts/lib/discovery/revise/gather_evidence.py 9 --dry-run    # assign only, no consultations
    python scripts/lib/discovery/revise/gather_evidence.py 9 --model sonnet  # override model (default: opus)
"""

import argparse
import re
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, REVIEWS_DIR, NOTES_DIR, consultation_dir, find_review,
)
from lib.shared.campaign import resolve_campaign
from lib.shared.common import find_asn
from lib.consult import (
    invoke_claude, get_total_usage, dispatch_run_consultation,
)
from lib.discovery.revise import assign_channels


def get_review_number(review_path):
    """Extract review number from filename like ASN-0001-review-6.md."""
    m = re.search(r"review-(\d+)", Path(review_path).stem)
    return int(m.group(1)) if m else 1


def extract_revise_section(review_content):
    """Extract the REVISE section from a review."""
    lines = review_content.split("\n")
    in_revise = False
    revise_lines = []

    for line in lines:
        if line.strip() == "## REVISE":
            in_revise = True
            continue
        if in_revise and line.startswith("## ") and line.strip() != "## REVISE":
            break
        if in_revise:
            revise_lines.append(line)

    return "\n".join(revise_lines).strip()


# ─── Run consultations ───────────────────────────────────

def run_targeted_consultations(items, asn_id, model="opus"):
    """Run channel consultations for items that have questions assigned.

    Theory consultations run in parallel (no tools).
    Evidence consultations run sequentially (each runs KB + code in parallel internally).

    Mutates items in place, populating item['answers'][role].
    """
    campaign = resolve_campaign(asn_id)
    theory_channel = campaign.theory_channel
    evidence_channel = campaign.evidence_channel

    theory_work = []
    evidence_work = []

    for i, item in enumerate(items):
        item.setdefault("answers", {})
        for role, question in item.get("questions", {}).items():
            if role == "theory":
                theory_work.append((i, question))
            elif role == "evidence":
                evidence_work.append((i, question))

    if theory_work:
        print(f"  [THEORY] Firing {len(theory_work)} consultations in parallel...",
              file=sys.stderr)
        threads = []

        for idx, (item_idx, question) in enumerate(theory_work):
            def run_t(ii=item_idx, q=question, n=idx + 1):
                answer = dispatch_run_consultation(
                    theory_channel, q, label=f"Q{n}:theory",
                    model=model, effort="max")
                items[ii]["answers"]["theory"] = answer
            t = threading.Thread(target=run_t)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        print(f"  [THEORY] All done", file=sys.stderr)

    if evidence_work:
        print(f"  [EVIDENCE] Running {len(evidence_work)} consultations sequentially...",
              file=sys.stderr)
        for idx, (item_idx, question) in enumerate(evidence_work):
            answer = dispatch_run_consultation(
                evidence_channel, question, label=f"Q{idx + 1}:evidence",
                model="sonnet", effort="max")
            items[item_idx]["answers"]["evidence"] = answer
        print(f"  [EVIDENCE] All done", file=sys.stderr)


# ─── Write results ───────────────────────────────────────

def build_results(asn_label, review_path, items):
    """Build the consultation results markdown file."""
    display_names = assign_channels.display_names(asn_label)
    review_name = Path(review_path).name
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    consulted = [it for it in items if it["questions"]]
    internal_count = len(items) - len(consulted)
    per_channel = ", ".join(
        f"{sum(1 for it in items if r in it['questions'])} {name.lower()}"
        for r, name in display_names.items()
    )

    parts = [
        f"# Revision Consultation — {asn_label}",
        "",
        f"**Review:** {review_name}",
        f"**Date:** {now}",
        "",
        "## Summary",
        "",
        f"{len(items)} REVISE items analyzed: {internal_count} internal, "
        f"{len(consulted)} consulted ({per_channel})",
        "",
    ]

    if not consulted:
        parts += ["All REVISE items are internally fixable — "
                  "no expert consultation needed.", ""]
        return "\n".join(parts)

    parts += ["## Consultation Results", ""]

    for item in consulted:
        category = assign_channels.category_label(item["questions"].keys(), asn_label)
        parts += [
            f"### Issue {item['number']}: {item['title']}",
            "",
            f"**Category:** {category}",
            f"**Reason:** {item.get('reason', '')}",
            "",
        ]
        answers = item.get("answers", {})
        for role, question in item["questions"].items():
            name = display_names[role]
            answer = (answers.get(role) or "[consultation not run]").strip() or "[No answer]"
            parts += [
                f"**{name} question:** {question}",
                "",
                f"**{name}'s Answer:**",
                "",
                answer,
                "",
            ]

    return "\n".join(parts)


# ─── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Assign channels to review findings and run the targeted consultations")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("review", nargs="?",
                        help="Review identifier (e.g., review-3) — omit for latest")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model for channel assignment (default: opus)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Assign channels only, don't run consultations")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in {NOTES_DIR.relative_to(WORKSPACE)}/", file=sys.stderr)
        sys.exit(1)

    # Find review
    review_path = find_review(asn_label, args.review)
    if review_path is None:
        if args.review:
            print(f"  Review not found: {args.review} for {asn_label}",
                  file=sys.stderr)
        else:
            print(f"  No reviews found for {asn_label} in {REVIEWS_DIR.relative_to(WORKSPACE)}/",
                  file=sys.stderr)
        sys.exit(1)

    review_content = Path(review_path).read_text()
    review_num = get_review_number(review_path)

    # Extract REVISE section
    revise_section = extract_revise_section(review_content)
    if not revise_section:
        print(f"  No REVISE section in {Path(review_path).name}", file=sys.stderr)
        sys.exit(0)

    # Load ASN content
    asn_content = asn_path.read_text()

    print(f"  [CONSULT-REVISION] {asn_label} + {Path(review_path).name}",
          file=sys.stderr)

    total_start = time.time()

    # Step 1: Assign channels to each REVISE item
    print(f"  [ASSIGN] Building prompt...", file=sys.stderr)
    prompt = assign_channels.build_prompt(asn_content, revise_section, asn_label)
    print(f"  [ASSIGN] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

    response, _ = invoke_claude(
        prompt, model=args.model, effort="max",
        allow_tools=False, label="assign",
        skill="gather-evidence:assign",
    )

    if not response:
        print(f"  [ASSIGN] Failed", file=sys.stderr)
        sys.exit(1)

    # Save raw assignment output
    output_dir = consultation_dir(asn_label)
    output_dir.mkdir(parents=True, exist_ok=True)
    consult_subdir = output_dir / f"consultation-{review_num}"
    consult_subdir.mkdir(parents=True, exist_ok=True)
    cat_path = consult_subdir / "assessment.md"
    cat_path.write_text(
        f"# Channel Assignment — {asn_label} review-{review_num}\n\n"
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"{response}\n"
    )
    print(f"  [ASSIGN] Saved to {cat_path}", file=sys.stderr)

    items = assign_channels.parse(response, asn_label)
    if not items:
        print(f"  [ASSIGN] No items parsed from response", file=sys.stderr)
        sys.exit(1)

    internal_count = sum(1 for it in items if not it["questions"])
    consult_count = len(items) - internal_count
    print(f"  [ASSIGN] {len(items)} items: "
          f"{internal_count} internal, {consult_count} need consultation",
          file=sys.stderr)

    for item in items:
        tag = assign_channels.category_label(item["questions"].keys(), asn_label)
        print(f"    Issue {item['number']}: {tag} — {item['title']}",
              file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Skipping consultations", file=sys.stderr)
        # Build results without answers
        results = build_results(asn_label, review_path, items)
        results_path = consult_subdir / "answers.md"
        results_path.write_text(results)
        print(str(results_path.resolve()))
        return

    # Step 2: Run consultations for items that need them
    if consult_count > 0:
        print(f"", file=sys.stderr)
        run_targeted_consultations(items, asn_label, model=args.model)
    else:
        print(f"  [CONSULT] All items internal, no consultations needed",
              file=sys.stderr)

    # Step 3: Write results
    results = build_results(asn_label, review_path, items)
    results_path = consult_subdir / "answers.md"
    results_path.write_text(results)

    total_elapsed = time.time() - total_start

    # Summary
    print(f"", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)
    print(f"  REVISION CONSULTATION COMPLETE", file=sys.stderr)
    print(f"  {'='*50}", file=sys.stderr)
    print(f"  Items: {len(items)} ({internal_count} internal, "
          f"{consult_count} consulted)", file=sys.stderr)
    print(f"  Total: {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)",
          file=sys.stderr)

    totals = get_total_usage()
    if totals["calls"] > 0:
        print(f"  Total cost: ${totals['cost_usd']:.4f} "
              f"({totals['calls']} calls)", file=sys.stderr)

    print(f"  Output: {results_path}", file=sys.stderr)

    # Print the output file path to stdout (for pipeline consumption)
    print(str(results_path.resolve()))


if __name__ == "__main__":
    main()
