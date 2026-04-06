#!/usr/bin/env python3
"""
Per-property Dafny contract review.

Compares each generated .dfy file against its formal contract from
formal-statements.md. Flags mismatches for author review.

Output: vault/3-modeling/dafny/ASN-NNNN/modeling-N/CONTRACT-REVIEW.md

Usage:
    python scripts/lib/modeling/dafny/validate.py 34
    python scripts/lib/modeling/dafny/validate.py 34 --modeling 2
    python scripts/lib/modeling/dafny/validate.py 34 --dry-run
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
from lib.shared.paths import (WORKSPACE, USAGE_LOG,
                   formal_stmts)
from lib.shared.common import find_asn, extract_property_sections
from lib.modeling.dafny.common import find_modeling_dir

PROMPT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "modeling" / "dafny" / "validate-contract.md"


def validate(dafny_source, formal_contract, label):
    """Review a single property. Returns (result, reason, elapsed)."""
    template = PROMPT_TEMPLATE.read_text()
    prompt = (template
              .replace("{{dafny_source}}", dafny_source)
              .replace("{{formal_contract}}", formal_contract))

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


def validate_batch(asn_num, modeling_dir, dry_run=False):
    """Run per-property contract review. Returns path to review file."""
    asn_label = f"ASN-{asn_num:04d}"
    modeling_name = modeling_dir.name

    print(f"  [CONTRACT] {asn_label} ({modeling_name})", file=sys.stderr)

    stmts_path = formal_stmts(asn_num)
    if not stmts_path.exists():
        print(f"  No formal-statements.md for {asn_label}", file=sys.stderr)
        return None

    stmts_text = stmts_path.read_text()

    dfy_files = sorted(modeling_dir.glob("*.dfy"))
    if not dfy_files:
        print(f"  No .dfy files in {modeling_dir}", file=sys.stderr)
        return None

    # Build label map from formal-statements headers
    label_map = {}
    for line in stmts_text.split("\n"):
        m = re.match(r'^##\s+(.+?)\s+\u2014\s+(.+?)(?:\s+\(|$)', line)
        if m:
            label = m.group(1).strip()
            name = m.group(2).strip()
            pascal = re.match(r'^([A-Z][a-zA-Z0-9]+)', name)
            if pascal:
                label_map[pascal.group(1)] = label

    all_labels = list(set(label_map.values()))
    sections = extract_property_sections(stmts_text, known_labels=all_labels,
                                          truncate=False)

    print(f"  Properties: {len(dfy_files)}", file=sys.stderr)

    if dry_run:
        for f in dfy_files:
            stem = f.stem
            label = label_map.get(stem, stem)
            section = sections.get(label, "")
            has_contract = "*Formal Contract:*" in section or "*Preconditions" in section
            print(f"  {stem:30s} \u2192 {label:20s} contract={'yes' if has_contract else 'NO'}",
                  file=sys.stderr)
        return None

    out_path = modeling_dir / "CONTRACT-REVIEW.md"

    with open(out_path, "w") as f:
        f.write(f"# Contract Review \u2014 {asn_label} ({modeling_name})\n\n")
        f.write(f"*Reviewed: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")

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

        if rec == "clean":
            clean_count += 1
            print(f" \u2192 CLEAN ({elapsed:.0f}s)", file=sys.stderr)
        elif rec == "flag":
            flag_count += 1
            print(f" \u2192 FLAG ({elapsed:.0f}s)", file=sys.stderr)
            with open(out_path, "a") as f:
                f.write(f"## {label} \u2014 {stem}\n\n")
                f.write(f"{reason}\n\n")
        else:
            print(f" \u2192 {rec} ({elapsed:.0f}s)", file=sys.stderr)

    total = clean_count + flag_count
    summary = f"{total} properties reviewed: {clean_count} CLEAN, {flag_count} FLAG"

    content = out_path.read_text()
    header_end = content.index("\n\n", content.index("*Reviewed:")) + 2
    content = content[:header_end] + summary + "\n\n" + content[header_end:]
    out_path.write_text(content)

    print(f"\n  {summary}", file=sys.stderr)
    print(f"  Report: {out_path.relative_to(WORKSPACE)}", file=sys.stderr)

    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "dafny-contract-review",
            "asn": asn_label,
            "elapsed_s": round(total_elapsed, 1),
            "properties": total,
            "flags": flag_count,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Per-property Dafny contract review")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Specific modeling-N to review (default: latest)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show property list without reviewing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"

    modeling_dir = find_modeling_dir(asn_label, args.modeling)
    if modeling_dir is None:
        print(f"  No modeling directory found for {asn_label}", file=sys.stderr)
        sys.exit(1)

    validate_batch(asn_num, modeling_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
