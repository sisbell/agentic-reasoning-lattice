#!/usr/bin/env python3
"""
Classification audit — verify property Status column is correct.

For each property, reads the section text and current Status, then asks
whether the classification is correct. Produces a markdown report.

Results stored in vault/audit/classify/<timestamp>/

Usage:
    python scripts/audit/classify.py 34
    python scripts/audit/classify.py 34 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG
from lib.shared.common import find_asn, extract_property_sections
from lib.formalization.deps import find_property_table, parse_table_row, detect_columns

AUDIT_DIR = WORKSPACE / "vault" / "audit" / "classify"

CLASSIFY_PROMPT = """You are auditing the Status column of a property table in a formal specification.

For each property below, determine whether the Status is correct given the section content.

## Classification Criteria

1. **axiom** — The section explicitly states this is definitional or posited. It introduces a mathematical foundation (carrier set, ordering rule, type definition). No proof is needed or possible — it IS the starting point. The section may have a justification explaining *why* this definition was chosen, but no derivation from other properties.

2. **design requirement** — The section asserts a system behavior guarantee (permanence, monotonicity, isolation, allocation rules) but has no proof and no derivation from other properties in this ASN. The guarantee depends on operations or mechanisms not defined in this ASN. It may have informal justification but cannot be formally derived here.

3. **OK** — The current Status is correct. The property has a proof or derivation, or its Status already cites dependencies (e.g., "from T1, T3", "corollary of T4").

4. **flag** — Ambiguous. The classification is unclear — the property might be an axiom, a design requirement, or a derivable property, but the section doesn't make it obvious. Needs author review.

## Properties

{{properties}}

## Output

For each property, output one line:

```
LABEL | STATUS | RECOMMENDATION | REASON
```

Where RECOMMENDATION is one of: axiom, design requirement, OK, flag
And REASON is a brief explanation (one sentence).

Output all properties, including ones that are OK.
"""


def classify_properties(asn_num, dry_run=False):
    """Run classification audit on an ASN. Returns report text."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        print(f"  No property table in {asn_path.name}", file=sys.stderr)
        return None

    # Parse table
    header = parse_table_row(rows[0])
    cols = detect_columns(header)
    data_rows = rows[2:]

    # Collect labels and statuses
    properties = []
    labels = []
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue
        label = cells[0].strip().strip("`*")
        if not label:
            continue
        status = cells[-1].strip()
        labels.append(label)
        properties.append({"label": label, "status": status})

    # Extract sections (truncated for prompt size)
    sections = extract_property_sections(text, known_labels=labels,
                                          truncate=True)

    # Build prompt
    prop_text = []
    for prop in properties:
        label = prop["label"]
        status = prop["status"]
        section = sections.get(label, "(no section found)")
        # Truncate long sections
        if len(section) > 3000:
            section = section[:3000] + "\n... (truncated)"
        prop_text.append(
            f"### {label}\n"
            f"**Current Status:** `{status}`\n\n"
            f"{section}\n"
        )

    prompt = CLASSIFY_PROMPT.replace("{{properties}}", "\n".join(prop_text))

    print(f"  [CLASSIFY] {asn_label}: {len(properties)} properties, "
          f"{len(prompt) // 1024}KB prompt", file=sys.stderr)

    if dry_run:
        print(f"  [DRY RUN] Would send to sonnet", file=sys.stderr)
        return None

    # Call Claude
    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [CLASSIFY] FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return None

    print(f"  [CLASSIFY] Done ({elapsed:.0f}s)", file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "classify-audit",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    # Build report
    report = [
        f"# Classification Audit — {asn_label}\n",
        f"*Audited: {time.strftime('%Y-%m-%d %H:%M')}*\n",
        f"## Results\n",
        result.stdout.strip(),
        "",
    ]

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Classification audit — verify property Status column")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    report = classify_properties(asn_num, dry_run=args.dry_run)

    if report is None:
        sys.exit(1 if not args.dry_run else 0)

    # Write report
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = AUDIT_DIR / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    asn_label = f"ASN-{asn_num:04d}"
    out_path = out_dir / f"{asn_label}.md"
    out_path.write_text(report)

    print(f"  [CLASSIFY] Report: {out_path.relative_to(WORKSPACE)}",
          file=sys.stderr)
    print(report)


if __name__ == "__main__":
    main()
