#!/usr/bin/env python3
"""
Classification audit — verify property Status column is correct.

For each property, reads the section text and current Status, then asks
whether the classification is correct. Produces a markdown report,
writing results incrementally as each property is classified.

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

CLASSIFY_PROMPT = """You are a Dijkstra-school formal methods reviewer. Your task is to
verify whether a property's Status column correctly reflects its proof obligation.

Work through these steps in order:

## Step 1: Does this property need a proof?

Read the section content and determine:

- **Does it have a proof?** Look for: *Proof.*, ∎, step-by-step derivation,
  case analysis, "we show that", "it follows that". A proof derives the
  property from other properties, axioms, or definitions.

- **Is it a definition?** Look for: computation rules, algorithms, formulas
  that say "define X as..." or specify how something is computed. Definitions
  introduce notation or name a construction. They have no truth value — they
  assign meaning, not assert truth. Definitions do NOT need proofs.

- **Is it a postulate (axiom)?** Look for: "this is an axiom", "we posit",
  "by definition, not by derivation", "accepted without proof". An axiom
  asserts a foundational truth that the rest of the system builds on.
  Axioms do NOT need proofs.

- **Is it a system constraint?** Look for: assertions about system behavior
  (permanence, monotonicity, isolation, allocation rules) with NO proof and
  NO derivation from other properties in this ASN. The constraint may have
  informal justification but cannot be formally derived from the mathematics
  available in this document. These are design requirements.

## Step 2: Is the Status correct?

Based on Step 1:

- If **no proof needed** (definition): Status should be `introduced` or similar.
  Definitions are not axioms. Status is OK if it doesn't say `axiom`.

- If **no proof needed** (axiom/postulate): Status should be `axiom`.
  If Status says `introduced`, recommend `axiom`.

- If **no proof needed** (system constraint): Status should be `design requirement`.
  If Status says `introduced`, recommend `design requirement`.

- If **proof present**: Status is correct as long as it reflects the property
  has been established (e.g., `introduced`, `from X`, `corollary of X`,
  `lemma (from X)`, `theorem from X`). Do not change dependency citations —
  that is a separate concern.

- If **proof needed but missing**: recommend `flag` — the property claims to be
  derived but has no proof. Repair should handle it.

- If **Status says `axiom` but section has a proof**: recommend `introduced` —
  the property is derived, not a postulate.

## Step 3: Check for conflicting evidence

Before giving your final answer, check whether the evidence is consistent:

- Does the proof text contradict the formal contract? (e.g., proof present
  but `*Axiom:*` in the contract says "this is a design constraint")
- Does the prose contradict the Status? (e.g., section says "this is an axiom"
  but Status says `introduced`)
- Does the proof assume what it's trying to prove? (circular — the conclusion
  is stated as a premise or as a "design axiom" within the proof itself)

If evidence conflicts, recommend `flag` and explain all the conflicting signals.
A convincing-looking proof that admits its own conclusion is a design constraint
is not a real proof — it is circular.

## Property

**Label:** {{label}}
**Current Status:** `{{status}}`

### Section Content

{{section}}

## Output

Respond with exactly one line:

```
RECOMMENDATION | REASON
```

Where RECOMMENDATION is one of: axiom, design requirement, OK, flag, introduced
And REASON is a brief explanation. For `flag`, explain the conflicting evidence.
"""


def classify_one(label, status, section):
    """Classify a single property. Returns (recommendation, reason)."""
    prompt = (CLASSIFY_PROMPT
              .replace("{{label}}", label)
              .replace("{{status}}", status)
              .replace("{{section}}", section))

    cmd = [
        "claude", "--print", "--model", "claude-opus-4-6",
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
        return "error", f"sonnet failed ({elapsed:.0f}s)"

    # Parse response — expect "RECOMMENDATION | REASON"
    line = result.stdout.strip()
    # Strip markdown code fences if present
    line = re.sub(r'^```\s*', '', line)
    line = re.sub(r'\s*```$', '', line)
    line = line.strip()

    if "|" in line:
        parts = line.split("|", 1)
        rec = parts[0].strip().lower()
        reason = parts[1].strip()
    else:
        rec = line.strip().lower()
        reason = ""

    return rec, reason, elapsed


def classify_properties(asn_num, dry_run=False):
    """Run classification audit on an ASN."""
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

    # Extract full sections — classification needs complete text
    sections = extract_property_sections(text, known_labels=labels,
                                          truncate=False)

    print(f"  [CLASSIFY] {asn_label}: {len(properties)} properties",
          file=sys.stderr)

    if dry_run:
        for prop in properties:
            section = sections.get(prop["label"], "")
            print(f"  {prop['label']:30s} status={prop['status']:30s} "
                  f"section={len(section)}B", file=sys.stderr)
        return None

    # Set up output file
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = AUDIT_DIR / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{asn_label}.md"

    # Write header
    with open(out_path, "w") as f:
        f.write(f"# Classification Audit — {asn_label}\n\n")
        f.write(f"*Audited: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write("| Label | Current Status | Recommendation | Reason |\n")
        f.write("|-------|---------------|----------------|--------|\n")

    # Classify one by one, appending results
    total_elapsed = 0
    changes = 0

    for i, prop in enumerate(properties, 1):
        label = prop["label"]
        status = prop["status"]
        section = sections.get(label, "(no section found)")

        print(f"  [{i}/{len(properties)}] {label}...",
              end="", file=sys.stderr, flush=True)

        rec, reason, elapsed = classify_one(label, status, section)
        total_elapsed += elapsed

        # Mark changes
        marker = ""
        if rec not in ("ok", "error"):
            if rec != status.lower():
                marker = " **"
                changes += 1

        row = f"| {label} | {status} | {rec}{marker} | {reason} |"

        # Print to stderr
        print(f" → {rec} ({elapsed:.0f}s)", file=sys.stderr)

        # Append to file
        with open(out_path, "a") as f:
            f.write(row + "\n")

    # Write footer
    with open(out_path, "a") as f:
        f.write(f"\n*{len(properties)} properties audited in "
                f"{total_elapsed:.0f}s. {changes} recommended changes.*\n")

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "classify-audit",
            "asn": asn_label,
            "elapsed_s": round(total_elapsed, 1),
            "properties": len(properties),
            "changes": changes,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    print(f"\n  [CLASSIFY] Report: {out_path.relative_to(WORKSPACE)}",
          file=sys.stderr)
    print(f"  [CLASSIFY] {changes} recommended changes out of "
          f"{len(properties)} properties", file=sys.stderr)

    return str(out_path)


def main():
    parser = argparse.ArgumentParser(
        description="Classification audit — verify property Status column")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show properties without invoking Claude")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    classify_properties(asn_num, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
