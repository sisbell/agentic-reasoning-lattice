#!/usr/bin/env python3
"""
Extract Definition — extract narrative definitions to standalone files.

Reads the lint inline report for definition findings, then for each:
1. Extract: rewrite narrative, create new definition section in the file
2. Disassemble: split the file into separate definition files

Run `python scripts/lint.py inline 34` first to build the report.

Usage:
    python scripts/extract-definition.py 34              # extract all flagged
    python scripts/extract-definition.py 34 --label TA-assoc  # single property
    python scripts/extract-definition.py 34 --dry-run    # show what would be extracted
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    WORKSPACE,
    blueprint_properties_dir, lint_path,
)
from lib.shared.common import find_asn, step_commit_asn, load_property_names, filename_to_label, label_to_filename
from lib.blueprinting.lint import _parse_inline_report

PROMPT_PATH = (WORKSPACE / "scripts" / "prompts" / "blueprinting"
               / "extract-definition.md")


def _parse_promotion_plan(plan_path, section):
    """Parse a promotion plan section into {source_label: [target_labels]}."""
    if not plan_path.exists():
        return {}

    text = plan_path.read_text()
    result = {}
    in_section = False
    for line in text.split("\n"):
        if line.strip().startswith("## "):
            in_section = line.strip().lstrip("# ").strip().lower() == section.lower()
            continue
        if not in_section:
            continue
        m = re.match(r'^- (\S+)\s*→\s*(.+)', line.strip())
        if m:
            source = m.group(1)
            targets = [t.strip() for t in m.group(2).split(",")]
            result[source] = targets
    return result


def _extract_one(prop_file, label, findings, vocabulary, table):
    """Extract definitions from one property file. Returns rewritten content."""
    template = PROMPT_PATH.read_text()
    content = prop_file.read_text()

    findings_text = "\n".join(
        f"- {r['kind']} | {r['label']} | {r['name']} | {r['description']}"
        for r in findings
    )

    prompt = (template
              .replace("{{content}}", content)
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{table}}", table)
              .replace("{{findings}}", findings_text))

    print(f"  [EXTRACT] {label} — {len(findings)} definitions...",
          file=sys.stderr)

    cmd = [
        "claude", "--print", "--model", "claude-opus-4-6",
        "--tools", "",
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
        print(f"    FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return None, elapsed

    new_content = result.stdout.strip()

    # Strip tool_call markup if LLM leaked it
    if "<tool_call>" in new_content:
        try:
            tc_start = new_content.index('{"name"')
            tc_end = new_content.index("</tool_call>")
            tc_data = json.loads(new_content[tc_start:tc_end].strip())
            extracted = tc_data.get("arguments", {}).get("content", "")
            if extracted:
                new_content = extracted
                print(f"    (extracted from tool_call)", file=sys.stderr)
        except (ValueError, json.JSONDecodeError):
            pass

    if len(new_content) < len(content) * 0.5:
        print(f"    REJECTED (output too short)", file=sys.stderr)
        return None, elapsed

    print(f"    Done ({elapsed:.0f}s)", file=sys.stderr)
    return new_content, elapsed


def _split_table_marker(output, blueprint_dir):
    """Split LLM output at === TABLE === marker, append rows to _table.md.

    Returns the file content (everything before the marker).
    """
    table_path = blueprint_dir / "_table.md"

    if "=== TABLE ===" not in output:
        return output

    parts = output.split("=== TABLE ===", 1)
    content = parts[0].strip()
    table_section = parts[1].strip() if len(parts) > 1 else ""

    # Extract table rows (skip header and separator lines)
    new_rows = []
    for line in table_section.split("\n"):
        stripped = line.strip()
        if (stripped.startswith("|")
                and not re.match(r'\|\s*Label\s*\|', stripped)
                and not re.match(r'\|\s*-', stripped)):
            new_rows.append(stripped)

    if new_rows and table_path.exists():
        existing = table_path.read_text().rstrip().split("\n")
        existing.extend(new_rows)
        table_path.write_text("\n".join(existing) + "\n")
        print(f"    [TABLE] Added {len(new_rows)} entries", file=sys.stderr)

    return content


def _disassemble_one(prop_file, blueprint_dir):
    """Mechanically split a property file at --- markers into separate files."""
    content = prop_file.read_text()

    chunks = re.split(r'\n---\n', content)
    if len(chunks) <= 1:
        print(f"    [DISASSEMBLE] No --- markers — single definition",
              file=sys.stderr)
        return []

    new_files = []
    _prop_names = load_property_names(blueprint_dir)
    source_label = filename_to_label(prop_file.name, _prop_names)

    for i, chunk in enumerate(chunks):
        stripped = chunk.strip()
        if not stripped:
            continue

        if i == 0:
            # First chunk is the source property — overwrite the file
            prop_file.write_text(stripped + "\n")
            continue

        # Extract name from definition header: **Definition (Name).**
        m = re.match(r'^\*\*Definition\s*\(([^)]+)\)', stripped)
        if not m:
            # Try property header: **LABEL (Name).**
            m = re.match(r'^\*\*(\S+)\s*\(', stripped)
        if m:
            label = m.group(1).strip()
            filename = label_to_filename(label)
        else:
            filename = f"{source_label}-def{i}.md"

        out_path = blueprint_dir / filename
        out_path.write_text(stripped + "\n")
        new_files.append(filename)
        print(f"    [DISASSEMBLE] Created {filename}", file=sys.stderr)

    return new_files


def main():
    parser = argparse.ArgumentParser(
        description="Extract Definition — extract narrative definitions "
                    "to standalone files")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--label", help="Extract for a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan only, show findings without extracting")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    blueprint_dir = blueprint_properties_dir(asn_label)
    if not blueprint_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        sys.exit(1)

    print(f"\n  [EXTRACT-DEFINITION] {asn_label}", file=sys.stderr)
    print(f"  Blueprint: {blueprint_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # Load vocabulary and table
    vocab_path = blueprint_dir / "_vocabulary.md"
    vocabulary = (vocab_path.read_text() if vocab_path.exists()
                  else "(no vocabulary file)")

    table_path = blueprint_dir / "_table.md"
    table = table_path.read_text() if table_path.exists() else "(no table file)"

    # Read inline findings for LLM context
    report_path = lint_path(asn_label, "inline")
    if not report_path.exists():
        print(f"  No inline lint report. Run: python scripts/lint.py inline {asn_num}",
              file=sys.stderr)
        sys.exit(1)

    all_findings = _parse_inline_report(report_path)

    # Determine which labels to act on
    plan_path = blueprint_dir.parent / "lint" / "promotion-plan.md"
    plan = _parse_promotion_plan(plan_path, "Extract")

    if plan:
        print(f"  Reading promotion plan: {plan_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        source_labels = set(plan.keys())
    elif args.label:
        source_labels = {args.label}
    else:
        print(f"  No promotion plan found and no --label specified.",
              file=sys.stderr)
        print(f"  Create: {plan_path.relative_to(WORKSPACE)}", file=sys.stderr)
        sys.exit(1)

    # Build candidates from plan + inline findings
    candidates = []
    for label in sorted(source_labels):
        if label not in all_findings:
            print(f"  WARNING: {label} not in inline report, skipping",
                  file=sys.stderr)
            continue
        findings = all_findings[label]
        definitions = [f for f in findings if f["kind"] == "definition"]
        if not definitions:
            print(f"  WARNING: {label} has no definition findings, skipping",
                  file=sys.stderr)
            continue
        prop_file = blueprint_dir / (label + ".md")
        if not prop_file.exists():
            print(f"  WARNING: {label}.md not found, skipping", file=sys.stderr)
            continue
        candidates.append((label, prop_file, definitions))

    if not candidates:
        print(f"\n  Nothing to extract.", file=sys.stderr)
        return

    print(f"  {len(candidates)} files with definitions to extract.",
          file=sys.stderr)

    if args.dry_run:
        for label, f, findings in candidates:
            for fd in findings:
                print(f"    {label} → {fd['label']} ({fd['name']}): "
                      f"{fd['description']}", file=sys.stderr)
        return

    # Extract each: extract → disassemble
    for label, prop_file, findings in candidates:
        print(f"\n  --- {label} ---", file=sys.stderr)

        new_content, elapsed = _extract_one(
            prop_file, label, findings, vocabulary, table)
        if new_content is None:
            continue

        # Split at === TABLE === marker, append rows to _table.md
        new_content = _split_table_marker(new_content, blueprint_dir)
        prop_file.write_text(new_content + "\n")

        # Disassemble (split file into separate definition files)
        new_files = _disassemble_one(prop_file, blueprint_dir)

        # Reload table for next iteration
        if table_path.exists():
            table = table_path.read_text()

    step_commit_asn(asn_num, hint="extract-definition")

    print(f"\n  [EXTRACT-DEFINITION] Done", file=sys.stderr)


if __name__ == "__main__":
    main()
