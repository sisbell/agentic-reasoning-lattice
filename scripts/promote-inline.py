#!/usr/bin/env python3
"""
Promote Inline — extract embedded derived results to standalone properties.

Reads the lint inline report for derived findings, then for each:
1. Promote: rewrite narrative, create new property section in the file
2. Format: review/revise fixes labels, headers on the new section
3. Disassemble: split the file into separate property files

Run `python scripts/lint.py inline 34` first to build the report.

Usage:
    python scripts/promote-inline.py 34              # promote all flagged
    python scripts/promote-inline.py 34 --label T10a # single property
    python scripts/promote-inline.py 34 --dry-run    # show what would be promoted
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
    WORKSPACE, USAGE_LOG,
    blueprint_properties_dir, lint_path,
)
from lib.shared.common import find_asn, step_commit_asn, load_property_names, filename_to_label, label_to_filename
from lib.blueprinting.lint import _parse_inline_report

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "promote-inline"
PROMOTE_TEMPLATE = PROMPTS_DIR / "promote.md"


def _parse_promotion_plan(plan_path, section):
    """Parse a promotion plan section into {source_label: [target_labels]}.

    Format:
        ## Promote
        - T0b → T0a
        - T10a → T10a.1, T10a.2, T10a.3
    """
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
DISASSEMBLE_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "disassemble.md"


def _promote_one(prop_file, label, findings, vocabulary, table):
    """Promote inline results in one property file. Returns rewritten content."""
    template = PROMOTE_TEMPLATE.read_text()
    content = prop_file.read_text()

    results_text = "\n".join(
        f"- {r['kind']} | {r['label']} | {r['name']} | {r['description']}"
        for r in findings
    )

    prompt = (template
              .replace("{{content}}", content)
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{table}}", table)
              .replace("{{results}}", results_text))

    print(f"  [PROMOTE] {label} — {len([r for r in findings if r['kind'] == 'derived'])} results...",
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
        import json as _json
        try:
            tc_start = new_content.index('{"name"')
            tc_end = new_content.index("</tool_call>")
            tc_data = _json.loads(new_content[tc_start:tc_end].strip())
            extracted = tc_data.get("arguments", {}).get("content", "")
            if extracted:
                new_content = extracted
                print(f"    (extracted from tool_call)", file=sys.stderr)
        except (ValueError, _json.JSONDecodeError):
            pass

    if len(new_content) < len(content) * 0.5:
        print(f"    REJECTED (output too short)", file=sys.stderr)
        return None, elapsed

    print(f"    Done ({elapsed:.0f}s)", file=sys.stderr)
    return new_content, elapsed


def _format_one(prop_file):
    """Run format review/revise on a single property file. Returns True if clean."""
    from lib.blueprinting.format import step_format_review, step_format_revise

    content = prop_file.read_text()

    # Use format review prompt with file content (print mode)
    review_template = (WORKSPACE / "scripts" / "prompts" / "blueprinting"
                       / "format" / "review.md").read_text()
    prompt = review_template.replace("{{asn_content}}", content)

    cmd = ["claude", "--print", "--model", "claude-sonnet-4-6"]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )

    if result.returncode != 0:
        return True  # skip format on failure

    text = result.stdout.strip()
    if "RESULT: CLEAN" in text:
        print(f"    [FORMAT] Clean", file=sys.stderr)
        return True

    # Has findings — run revise with agent tools
    revise_template = (WORKSPACE / "scripts" / "prompts" / "blueprinting"
                       / "format" / "revise.md").read_text()
    rel_path = prop_file.relative_to(WORKSPACE)
    revise_prompt = (revise_template
                     .replace("{{asn_path}}", str(rel_path))
                     .replace("{{findings}}", text))

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    result = subprocess.run(
        cmd, input=revise_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )

    if result.returncode == 0:
        print(f"    [FORMAT] Revised", file=sys.stderr)
    else:
        print(f"    [FORMAT] Revise failed", file=sys.stderr)

    return True


def _disassemble_one(prop_file, blueprint_dir):
    """Mechanically split a property file at --- markers into separate files."""
    content = prop_file.read_text()

    # Split on --- markers
    chunks = re.split(r'\n---\n', content)
    if len(chunks) <= 1:
        print(f"    [DISASSEMBLE] No --- markers — single property", file=sys.stderr)
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

        # Extract label from header
        m = re.match(r'^\*\*(\S+)\s*\(', stripped)
        if not m:
            m = re.match(r'^\*\*Definition\s*\(([^)]+)\)', stripped)
        if m:
            label = m.group(1)
            filename = label_to_filename(label)
        else:
            filename = f"{source_label}-part{i}.md"

        out_path = blueprint_dir / filename
        out_path.write_text(stripped + "\n")
        new_files.append(filename)
        print(f"    [DISASSEMBLE] Created {filename}", file=sys.stderr)

    return new_files


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
        if stripped.startswith("|") and not re.match(r'\|\s*Label\s*\|', stripped) and not re.match(r'\|\s*-', stripped):
            new_rows.append(stripped)

    if new_rows and table_path.exists():
        existing = table_path.read_text().rstrip().split("\n")
        existing.extend(new_rows)
        table_path.write_text("\n".join(existing) + "\n")
        print(f"    [TABLE] Added {len(new_rows)} entries", file=sys.stderr)

    return content


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

    blueprint_dir = blueprint_properties_dir(asn_label)
    if not blueprint_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        sys.exit(1)

    print(f"\n  [PROMOTE-INLINE] {asn_label}", file=sys.stderr)
    print(f"  Blueprint: {blueprint_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    # Load vocabulary and table
    vocab_path = blueprint_dir / "_vocabulary.md"
    vocabulary = vocab_path.read_text() if vocab_path.exists() else "(no vocabulary file)"

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
    plan = _parse_promotion_plan(plan_path, "Promote")

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
        derived = [f for f in findings if f["kind"] == "derived"]
        if not derived:
            print(f"  WARNING: {label} has no derived findings, skipping",
                  file=sys.stderr)
            continue
        prop_file = blueprint_dir / (label + ".md")
        if not prop_file.exists():
            print(f"  WARNING: {label}.md not found, skipping", file=sys.stderr)
            continue
        candidates.append((label, prop_file, findings))

    if not candidates:
        print(f"\n  Nothing to promote.", file=sys.stderr)
        return

    print(f"  {len(candidates)} properties to promote.",
          file=sys.stderr)

    if args.dry_run:
        for label, f, findings in candidates:
            derived = [fd for fd in findings if fd["kind"] == "derived"]
            for fd in derived:
                print(f"    {label} → {fd['label']} ({fd['name']}): {fd['description']}",
                      file=sys.stderr)
        return

    # Promote each property: promote → format → disassemble
    for label, prop_file, findings in candidates:
        print(f"\n  --- {label} ---", file=sys.stderr)

        # Step 1: Promote (rewrite narrative, create new section in file)
        new_content, elapsed = _promote_one(
            prop_file, label, findings, vocabulary, table)
        if new_content is None:
            continue

        # Split at === TABLE === marker, append rows to _table.md
        new_content = _split_table_marker(new_content, blueprint_dir)
        prop_file.write_text(new_content + "\n")

        # Step 2: Format (fix labels, headers)
        _format_one(prop_file)

        # Step 3: Disassemble (split file into separate property files)
        new_files = _disassemble_one(prop_file, blueprint_dir)

        # Reload table for next iteration
        if table_path.exists():
            table = table_path.read_text()

    step_commit_asn(asn_num, hint="promote-inline")

    print(f"\n  [PROMOTE-INLINE] Done", file=sys.stderr)


if __name__ == "__main__":
    main()
