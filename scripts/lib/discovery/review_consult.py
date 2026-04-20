#!/usr/bin/env python3
"""
Consult experts for revision — categorize REVISE items and run targeted consultations.

Reads a review's REVISE items + the ASN, uses Claude to categorize which items need
expert consultation vs. which are internally fixable, then runs targeted Nelson/Gregory
consultations for items that need external evidence. Produces a results file for the
revise agent to consume.

Usage:
    python scripts/lib/review_consult.py 9              # latest review
    python scripts/lib/review_consult.py 9 review-3     # specific review
    python scripts/lib/review_consult.py 9 --dry-run    # categorize only, no consultations
    python scripts/lib/review_consult.py 9 --model sonnet  # override model (default: opus)
"""

import argparse
import re
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
# Import expert consultation functions from consult
from lib.discovery.consult import (
    _invoke_claude,
    _run_nelson,
    _run_gregory,
    _total_usage,
    _usage_lock,
    log_usage,
)

from lib.shared.paths import NOTES_DIR, REVIEWS_DIR, CONSULTATIONS_DIR, sorted_reviews


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(NOTES_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def find_review(asn_label, review_spec=None):
    """Find review file. If review_spec is None, use latest."""
    if review_spec is None:
        reviews = sorted_reviews(asn_label)
        return reviews[-1] if reviews else None

    path = Path(review_spec)
    if path.exists():
        return path

    candidate = REVIEWS_DIR / asn_label / f"{review_spec}.md"
    if candidate.exists():
        return candidate

    candidate = REVIEWS_DIR / asn_label / review_spec
    if candidate.exists():
        return candidate

    candidate = REVIEWS_DIR / asn_label / f"{review_spec}.md"
    if candidate.exists():
        return candidate

    return None


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


# ─── Step 1: Categorize ──────────────────────────────────────────

def build_categorization_prompt(asn_content, revise_section):
    """Build the prompt to categorize REVISE items."""
    return f"""You are categorizing review findings to determine which need expert consultation before revision.

## Categories

- **INTERNAL** — Fixable from the ASN's own content. The fix is derivable from definitions, proofs, or reasoning already present in the ASN. Examples: inconsistent notation, missing case in a proof that can be filled from existing definitions, a precondition that follows from an already-stated claim.

- **NELSON** — Needs Nelson consultation. The fix requires understanding Ted Nelson's design intent — what the system was *meant* to do, what semantic constraints the designer intended. Nelson has access to Literary Machines and Nelson's concept notes. Examples: "Was this operation intended to be total or partial?", "Does the design require this ordering to be strict?"

- **GREGORY** — Needs Gregory consultation. The fix requires evidence from the udanax-green implementation — what the code actually does, what constraints it enforces, what edge cases it handles. Gregory has access to the knowledge base synthesis and the udanax-green C source. Examples: "Does the allocator enforce single-depth increment?", "What does INSERT do when the span crosses a boundary?"

- **BOTH** — Needs both Nelson and Gregory. The fix requires both design intent and implementation evidence. Example: "The axiom says X but the code does Y — was this intentional divergence or a bug?"

## ASN Content

{asn_content}

## REVISE Items

{revise_section}

## Instructions

For each REVISE issue, output a categorization block in exactly this format:

```
## Issue N: [title from review]
Category: INTERNAL|NELSON|GREGORY|BOTH
Reason: [1-2 sentences explaining why this category]
```

For NELSON items, add:
```
Nelson question: [one focused question for Nelson]
```

For GREGORY items, add:
```
Gregory question: [one focused question for Gregory]
```

For BOTH items, add both:
```
Nelson question: [one focused question for Nelson]
Gregory question: [one focused question for Gregory]
```

Do not add questions for INTERNAL items.

Output ONLY the categorization blocks, nothing else."""


def parse_categorization(response):
    """Parse categorization response into structured items.

    Returns list of dicts with keys: number, title, category, reason,
    nelson_question, gregory_question.
    """
    items = []
    current = None

    for line in response.split("\n"):
        line = line.strip()

        # New issue header
        m = re.match(r"##\s+Issue\s+(\d+):\s*(.+)", line)
        if m:
            if current:
                items.append(current)
            current = {
                "number": int(m.group(1)),
                "title": m.group(2).strip(),
                "category": None,
                "reason": None,
                "nelson_question": None,
                "gregory_question": None,
            }
            continue

        if current is None:
            continue

        # Category
        m = re.match(r"Category:\s*(\w+)", line)
        if m:
            current["category"] = m.group(1).upper()
            continue

        # Reason
        m = re.match(r"Reason:\s*(.+)", line)
        if m:
            current["reason"] = m.group(1).strip()
            continue

        # Nelson question
        m = re.match(r"Nelson question:\s*(.+)", line)
        if m:
            current["nelson_question"] = m.group(1).strip()
            continue

        # Gregory question
        m = re.match(r"Gregory question:\s*(.+)", line)
        if m:
            current["gregory_question"] = m.group(1).strip()
            continue

    if current:
        items.append(current)

    return items


# ─── Step 2: Run consultations ───────────────────────────────────

def run_targeted_consultations(items, model="opus"):
    """Run expert consultations for items that need them.

    Nelson consultations run in parallel (no tools).
    Gregory consultations run sequentially (code exploration uses tools).

    Mutates items in place, adding 'nelson_answer' and 'gregory_answer' keys.
    """
    # Collect Nelson and Gregory work
    nelson_work = []  # (item_index, question)
    gregory_work = []  # (item_index, question)

    for i, item in enumerate(items):
        cat = item["category"]
        if cat in ("NELSON", "BOTH") and item.get("nelson_question"):
            nelson_work.append((i, item["nelson_question"]))
        if cat in ("GREGORY", "BOTH") and item.get("gregory_question"):
            gregory_work.append((i, item["gregory_question"]))

    # Nelson in parallel
    if nelson_work:
        print(f"  [NELSON] Firing {len(nelson_work)} consultations in parallel...",
              file=sys.stderr)
        threads = []

        for idx, (item_idx, question) in enumerate(nelson_work):
            def run_n(ii=item_idx, q=question, n=idx + 1):
                answer = _run_nelson(q, n, model=model, effort="max")
                items[ii]["nelson_answer"] = answer
            t = threading.Thread(target=run_n)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        print(f"  [NELSON] All done", file=sys.stderr)

    # Gregory sequentially (each runs KB + code in parallel internally)
    if gregory_work:
        print(f"  [GREGORY] Running {len(gregory_work)} consultations sequentially...",
              file=sys.stderr)
        for idx, (item_idx, question) in enumerate(gregory_work):
            answer = _run_gregory(question, idx + 1, model="sonnet", effort="max")
            items[item_idx]["gregory_answer"] = answer
        print(f"  [GREGORY] All done", file=sys.stderr)


# ─── Step 3: Write results ───────────────────────────────────────

def build_results(asn_label, review_path, items):
    """Build the consultation results markdown file."""
    review_name = Path(review_path).name
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    internal_count = sum(1 for it in items if it["category"] == "INTERNAL")
    consulted = [it for it in items if it["category"] != "INTERNAL"]
    nelson_count = sum(1 for it in items if it["category"] in ("NELSON", "BOTH"))
    gregory_count = sum(1 for it in items if it["category"] in ("GREGORY", "BOTH"))

    parts = []
    parts.append(f"# Revision Consultation — {asn_label}")
    parts.append(f"")
    parts.append(f"**Review:** {review_name}")
    parts.append(f"**Date:** {now}")
    parts.append(f"")
    parts.append(f"## Summary")
    parts.append(f"")
    parts.append(f"{len(items)} REVISE items analyzed: "
                 f"{internal_count} internal, {len(consulted)} consulted "
                 f"({nelson_count} nelson, {gregory_count} gregory)")
    parts.append(f"")

    if not consulted:
        parts.append("All REVISE items are internally fixable — "
                     "no expert consultation needed.")
        parts.append("")
        return "\n".join(parts)

    parts.append("## Consultation Results")
    parts.append("")

    for item in items:
        if item["category"] == "INTERNAL":
            continue

        parts.append(f"### Issue {item['number']}: {item['title']}")
        parts.append(f"")
        parts.append(f"**Category:** {item['category']}")
        parts.append(f"**Reason:** {item.get('reason', '')}")
        parts.append(f"")

        if item.get("nelson_question"):
            parts.append(f"**Nelson question:** {item['nelson_question']}")
            parts.append(f"")
            parts.append(f"**Nelson's Answer:**")
            parts.append(f"")
            answer = item.get("nelson_answer", "[consultation not run]")
            parts.append(answer.strip() if answer else "[No answer]")
            parts.append(f"")

        if item.get("gregory_question"):
            parts.append(f"**Gregory question:** {item['gregory_question']}")
            parts.append(f"")
            parts.append(f"**Gregory's Answer:**")
            parts.append(f"")
            answer = item.get("gregory_answer", "[consultation not run]")
            parts.append(answer.strip() if answer else "[No answer]")
            parts.append(f"")

    return "\n".join(parts)


# ─── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Categorize review findings and run targeted expert consultations")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("review", nargs="?",
                        help="Review identifier (e.g., review-3) — omit for latest")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model for categorization (default: opus)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Categorize only, don't run consultations")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in lattices/xanadu/discovery/notes/", file=sys.stderr)
        sys.exit(1)

    # Find review
    review_path = find_review(asn_label, args.review)
    if review_path is None:
        if args.review:
            print(f"  Review not found: {args.review} for {asn_label}",
                  file=sys.stderr)
        else:
            print(f"  No reviews found for {asn_label} in lattices/xanadu/discovery/review/",
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

    # Step 1: Categorize REVISE items
    print(f"  [CATEGORIZE] Building prompt...", file=sys.stderr)
    prompt = build_categorization_prompt(asn_content, revise_section)
    print(f"  [CATEGORIZE] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

    response = _invoke_claude(
        prompt, model=args.model, effort="max",
        allow_tools=False, label="categorize",
    )

    if not response:
        print(f"  [CATEGORIZE] Failed", file=sys.stderr)
        sys.exit(1)

    # Save categorization output
    output_dir = CONSULTATIONS_DIR / asn_label
    output_dir.mkdir(parents=True, exist_ok=True)
    consult_subdir = output_dir / f"consultation-{review_num}"
    consult_subdir.mkdir(parents=True, exist_ok=True)
    cat_path = consult_subdir / "assessment.md"
    cat_path.write_text(
        f"# Revision Categorization — {asn_label} review-{review_num}\n\n"
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"{response}\n"
    )
    print(f"  [CATEGORIZE] Saved to {cat_path}", file=sys.stderr)

    # Parse categorization
    items = parse_categorization(response)
    if not items:
        print(f"  [CATEGORIZE] No items parsed from response", file=sys.stderr)
        sys.exit(1)

    internal_count = sum(1 for it in items if it["category"] == "INTERNAL")
    consult_count = len(items) - internal_count
    print(f"  [CATEGORIZE] {len(items)} items: "
          f"{internal_count} internal, {consult_count} need consultation",
          file=sys.stderr)

    for item in items:
        tag = item["category"]
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
        run_targeted_consultations(items, model=args.model)
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

    with _usage_lock:
        if _total_usage["calls"] > 0:
            print(f"  Total cost: ${_total_usage['cost_usd']:.4f} "
                  f"({_total_usage['calls']} calls)", file=sys.stderr)

    print(f"  Output: {results_path}", file=sys.stderr)

    # Print the output file path to stdout (for pipeline consumption)
    print(str(results_path.resolve()))


if __name__ == "__main__":
    main()
