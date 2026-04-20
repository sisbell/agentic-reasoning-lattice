#!/usr/bin/env python3
"""
Per-claim Dafny contract review.

Compares each generated .dfy file against its formal contract from
per-claim files in lattices/xanadu/formalization/. Flags mismatches for
author review.

Output: per-claim review files in lattices/xanadu/verification/dafny/ASN-NNNN/reviews/

Usage:
    python scripts/lib/verification/dafny/validate.py 34
    python scripts/lib/verification/dafny/validate.py 34 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import (WORKSPACE, FORMALIZATION_DIR, DAFNY_DIR, USAGE_LOG, DOMAIN_PROMPTS)
from lib.shared.common import find_asn, build_label_index

PROMPT_TEMPLATE = DOMAIN_PROMPTS / "verification" / "dafny" / "validate-contract.md"


def validate(dafny_source, formal_contract, label):
    """Review a single claim. Returns (result, reason, elapsed)."""
    template = PROMPT_TEMPLATE.read_text()
    prompt = (template
              .replace("{{dafny_source}}", dafny_source)
              .replace("{{formal_contract}}", formal_contract))

    cmd = [
        "claude", "--print", "--model", "claude-opus-4-7",
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
        return "error", f"opus failed ({elapsed:.0f}s)", elapsed

    text = result.stdout.strip()
    text = re.sub(r'```\s*', '', text).strip()

    # Find the CLEAN or FLAG line anywhere in output
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line = line.strip()
        m = re.match(r'^(CLEAN|FLAG)\s*\|\s*(.*)', line, re.IGNORECASE)
        if m:
            rec = m.group(1).lower()
            # For FLAG: capture the summary line + everything after as detail
            summary = m.group(2).strip()
            detail = "\n".join(lines[i + 1:]).strip()
            reason = f"{summary}\n\n{detail}".strip() if detail else summary
            return rec, reason, elapsed

    # Fallback: treat entire output as result
    if "|" in text:
        parts = text.split("|", 1)
        return parts[0].strip().lower(), parts[1].strip(), elapsed

    return text.strip().lower(), "", elapsed


def validate_batch(asn_num, dfy_dir, dry_run=False):
    """Run per-claim contract review. Returns path to review dir."""
    asn_label = f"ASN-{asn_num:04d}"

    print(f"  [CONTRACT] {asn_label}", file=sys.stderr)

    # Read contract sections from per-claim files
    claim_dir = FORMALIZATION_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No formalization directory for {asn_label}", file=sys.stderr)
        return None

    dfy_files = sorted(dfy_dir.glob("*.dfy"))
    if not dfy_files:
        print(f"  No .dfy files in {dfy_dir}", file=sys.stderr)
        return None

    # Build sections from per-claim files
    _label_index = build_label_index(claim_dir)
    _filename_to_label = {f"{stem}.md": lbl for lbl, stem in _label_index.items()}
    sections = {}
    for f in claim_dir.glob("*.md"):
        if not f.name.startswith("_"):
            sections[_filename_to_label.get(f.name, f.stem)] = f.read_text()

    # Build label map: PascalCase name -> label (for .dfy filename matching)
    label_map = {}
    for label, content in sections.items():
        m = re.search(r'^\*\*\S+\s*\(([A-Z][a-zA-Z0-9]+)\)', content, re.MULTILINE)
        if m:
            label_map[m.group(1)] = label

    print(f"  Claims: {len(dfy_files)}", file=sys.stderr)

    if dry_run:
        for f in dfy_files:
            stem = f.stem
            label = label_map.get(stem, stem)
            section = sections.get(label, "")
            has_contract = "*Formal Contract:*" in section or "*Preconditions" in section
            print(f"  {stem:30s} \u2192 {label:20s} contract={'yes' if has_contract else 'NO'}",
                  file=sys.stderr)
        return None

    review_dir = dfy_dir / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)

    total_elapsed = 0
    clean_count = 0
    flag_count = 0

    for i, dfy_file in enumerate(dfy_files, 1):
        stem = dfy_file.stem
        label = label_map.get(stem, stem)
        section = sections.get(label, "")

        if not section:
            print(f"  [{i}/{len(dfy_files)}] {stem}... \u2192 SKIP (no contract)",
                  file=sys.stderr)
            continue

        dafny_source = dfy_file.read_text()

        print(f"  [{i}/{len(dfy_files)}] {stem}...",
              end="", file=sys.stderr, flush=True)

        rec, reason, elapsed = validate(dafny_source, section, label)
        total_elapsed += elapsed

        review_path = review_dir / f"{label}.md"
        if rec == "clean":
            clean_count += 1
            print(f" \u2192 CLEAN ({elapsed:.0f}s)", file=sys.stderr)
            if review_path.exists():
                review_path.unlink()
        elif rec == "flag":
            flag_count += 1
            print(f" \u2192 FLAG ({elapsed:.0f}s)", file=sys.stderr)
            with open(review_path, "w") as f:
                f.write(f"# {label} \u2014 Contract FLAG\n\n")
                f.write(f"*{time.strftime('%Y-%m-%d %H:%M')}*\n\n")
                f.write(f"{reason}\n")
        else:
            print(f" \u2192 {rec} ({elapsed:.0f}s)", file=sys.stderr)

    total = clean_count + flag_count
    summary = f"{total} claims reviewed: {clean_count} CLEAN, {flag_count} FLAG"

    print(f"\n  {summary}", file=sys.stderr)
    print(f"  Reviews: {review_dir.relative_to(WORKSPACE)}/", file=sys.stderr)

    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "dafny-contract-review",
            "asn": asn_label,
            "elapsed_s": round(total_elapsed, 1),
            "claims": total,
            "flags": flag_count,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return review_dir


def main():
    parser = argparse.ArgumentParser(
        description="Per-claim Dafny contract review")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show claim list without reviewing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"

    dfy_dir = DAFNY_DIR / asn_label
    if not dfy_dir.exists():
        print(f"  No dafny directory found for {asn_label}", file=sys.stderr)
        sys.exit(1)

    validate_batch(asn_num, dfy_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
