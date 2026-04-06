#!/usr/bin/env python3
"""
Promote Inline — extract embedded results to standalone properties.

Scans property sections for content after the formal contract (derived
lemmas, consequences, commentary). Promotes derived results to their
own property sections so the formalization pipeline can handle them.

Standalone tool — run before formalization as needed.

Usage:
    python scripts/promote-inline.py 34              # scan + promote all
    python scripts/promote-inline.py 34 --label TA5  # single property
    python scripts/promote-inline.py 34 --dry-run    # scan only
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, REVIEWS_DIR, next_review_number
from lib.shared.common import (find_asn, extract_property_sections,
                                invoke_claude, invoke_claude_agent,
                                step_commit_asn)
from lib.formalization.core.build_dependency_graph import (
    find_property_table, parse_table_row)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization" / "promote-inline"
SCAN_TEMPLATE = PROMPTS_DIR / "scan.md"
PROMOTE_TEMPLATE = PROMPTS_DIR / "promote.md"


def _extract_post_contract(section):
    """Extract content after the formal contract in a property section."""
    marker = "*Formal Contract:*"
    idx = section.find(marker)
    if idx == -1:
        return None

    # Find the end of the contract block — next section header or end
    after_marker = section[idx:]

    # The contract block ends at the next blank line followed by non-contract
    # content, or at a bold header, or at end of section
    lines = after_marker.split("\n")
    contract_lines = []
    post_lines = []
    in_contract = True

    for i, line in enumerate(lines):
        if i == 0:
            contract_lines.append(line)
            continue
        if in_contract:
            stripped = line.strip()
            if stripped.startswith("- *") or stripped.startswith("*") or not stripped:
                contract_lines.append(line)
            else:
                in_contract = False
                post_lines.append(line)
        else:
            post_lines.append(line)

    post_content = "\n".join(post_lines).strip()
    return post_content if post_content else None


def _log_usage(skill, elapsed, asn_num, **extra):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"promote-inline-{skill}",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
            **extra,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def scan_property(label, section):
    """Scan one property's section for inline results. Returns list of findings."""
    template = SCAN_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{section}}", section))

    result, elapsed = invoke_claude(prompt, model="sonnet", effort="high")

    if result is None or "(none)" in result:
        return []

    findings = []
    for line in result.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            findings.append({
                "kind": parts[0],
                "label": parts[1],
                "name": parts[2],
                "description": parts[3],
            })

    return findings


def promote_property(asn_num, label, results):
    """Promote inline results for one property. Returns True if changes made."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = PROMOTE_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)

    # Format results list
    results_text = "\n".join(
        f"- {r['kind']} | {r['label']} | {r['name']} | {r['description']}"
        for r in results
    )

    prompt = (template
              .replace("{{asn_path}}", str(rel_path))
              .replace("{{label}}", label)
              .replace("{{results}}", results_text))

    print(f"  [PROMOTE] {label} — {len([r for r in results if r['kind'] == 'derived'])} results...",
          file=sys.stderr)

    start = time.time()
    data, elapsed = invoke_claude_agent(
        prompt, model="opus", effort="high",
        tools="Edit,Read,Glob,Grep")
    _log_usage("promote", elapsed, asn_num, label=label)

    if data is None:
        print(f"    FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return False

    # Report what was created
    for r in results:
        if r["kind"] == "derived":
            print(f"    Created: {r['label']} ({r['name']})", file=sys.stderr)
        else:
            print(f"    Kept: {r['description']} ({r['kind']})", file=sys.stderr)

    cost = 0
    if isinstance(data, dict):
        cost = data.get("total_cost_usd", 0)
    print(f"    Done ({elapsed:.0f}s, ${cost:.2f})", file=sys.stderr)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Promote Inline — extract embedded results to standalone properties")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--label", help="Promote for a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan only, show findings without promoting")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    print(f"\n  [PROMOTE-INLINE] {asn_label}", file=sys.stderr)

    # Get all property sections
    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        print(f"  No property table found", file=sys.stderr)
        sys.exit(1)

    labels = []
    for row in rows[2:]:
        cells = parse_table_row(row)
        if cells and cells[0].strip():
            labels.append(cells[0].strip().strip("`*"))

    sections = extract_property_sections(text, known_labels=labels, truncate=False)

    # Filter to single label if specified
    if args.label:
        labels = [l for l in labels if l == args.label]

    # Scan for inline results
    MIN_SECTION_SIZE = 2000  # skip small properties unlikely to have embedded results
    print(f"\n  [SCAN] {len(labels)} properties, checking for inline results...",
          file=sys.stderr)

    properties_with_findings = []
    no_content_count = 0

    for label in labels:
        section = sections.get(label, "")
        if not section or len(section) < MIN_SECTION_SIZE:
            no_content_count += 1
            continue

        # Scan with sonnet
        findings = scan_property(label, section)
        if not findings:
            no_content_count += 1
            continue

        derived = [f for f in findings if f["kind"] == "derived"]
        commentary = [f for f in findings if f["kind"] == "commentary"]

        print(f"    {label}: {len(findings)} inline block{'s' if len(findings) != 1 else ''} found",
              file=sys.stderr)
        for f in findings:
            if f["kind"] == "derived":
                print(f"      - {f['label']} ({f['name']}): {f['description']} (derived result)",
                      file=sys.stderr)
            else:
                print(f"      - {f['description']} (commentary — keeping in place)",
                      file=sys.stderr)

        if derived:
            properties_with_findings.append((label, findings))

    if no_content_count:
        print(f"    {no_content_count} properties: no post-contract content",
              file=sys.stderr)

    if not properties_with_findings:
        print(f"\n  Nothing to promote.", file=sys.stderr)
        return

    print(f"\n  {len(properties_with_findings)} properties with results to promote.",
          file=sys.stderr)

    if args.dry_run:
        print(f"\n  [DRY RUN] Would promote {sum(len([f for f in findings if f['kind'] == 'derived']) for _, findings in properties_with_findings)} results.",
              file=sys.stderr)
        return

    # Promote each property
    for label, findings in properties_with_findings:
        ok = promote_property(asn_num, label, findings)
        if ok:
            # Write review
            (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
            review_num = next_review_number(asn_label)
            rev_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"
            with open(rev_path, "w") as rf:
                rf.write(f"# Promote Inline — {asn_label} / {label}\n\n")
                rf.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                for f in findings:
                    if f["kind"] == "derived":
                        rf.write(f"- Promoted: **{f['label']}** ({f['name']}) — {f['description']}\n")
                    else:
                        rf.write(f"- Kept: {f['description']} (commentary)\n")
                rf.write("\n")

            step_commit_asn(asn_num,
                            hint=f"promote-inline {label}: {len([f for f in findings if f['kind'] == 'derived'])} results")

    print(f"\n  [NEXT] Run the formalization pipeline to complete the new properties:",
          file=sys.stderr)
    print(f"  ./run/formalize.sh {asn_num}", file=sys.stderr)


if __name__ == "__main__":
    main()
