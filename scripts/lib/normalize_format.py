"""
Format normalization gate — type extraction, table fix, review/revise cycle.

Pipeline:
1. Type extraction (sonnet) — classify property types if table is 3-column
2. Table fix (mechanical) — insert Type column
3. Format review/revise (sonnet) — fix headers + status vocab, up to 30 cycles

Usage (standalone):
    python scripts/lib/normalize_format.py 43
    python scripts/lib/normalize_format.py 43 --review-only
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
from paths import WORKSPACE, USAGE_LOG, formal_stmts, asn_dir
from lib.common import find_asn, extract_property_sections

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
REVIEW_TEMPLATE = PROMPTS_DIR / "normalize-format.md"
REVISE_TEMPLATE = PROMPTS_DIR / "normalize-format-revise.md"
TYPES_TEMPLATE = PROMPTS_DIR / "normalize-types.md"

MAX_CYCLES = 30

# TYPE → Dafny construct mapping
TYPE_TO_CONSTRUCT = {
    "INV": "predicate",
    "LEMMA": "lemma",
    "THEOREM": "lemma",
    "PRE": "requires",
    "POST": "ensures",
    "DEF": "function",
    "FRAME": "predicate",
    "META": "predicate",
}


def _invoke_claude(prompt, model="sonnet", effort="high", tools=False):
    """Call claude --print. If tools=True, allows file read/write."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag]
    if not tools:
        cmd += ["--tools", ""]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=300,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [FORMAT] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        return "", elapsed

    return result.stdout.strip(), elapsed


def _log_usage(step, elapsed, asn_num):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"normalize-{step}",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Step 1: Type extraction (LLM, sonnet)
# ---------------------------------------------------------------------------

def step_extract_types(asn_num):
    """Extract property types via sonnet if table is missing Type column.

    Returns a label→type dict, or None if table already has types.
    """
    from lib.rebase_deps import find_property_table, parse_table_row, detect_columns

    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return None

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        return None

    header = parse_table_row(rows[0])
    cols = detect_columns(header)
    if "type" in cols:
        print(f"  [TYPES] {asn_label} table already has Type column — skipping",
              file=sys.stderr)
        return None

    # Build prompt
    template = TYPES_TEMPLATE.read_text()
    prompt = template.replace("{{asn_content}}", text)

    print(f"  [TYPES] Classifying {asn_label} properties...", file=sys.stderr)
    response, elapsed = _invoke_claude(prompt, model="sonnet", effort="high")
    _log_usage("types", elapsed, asn_num)

    if not response:
        print(f"  [TYPES] No response ({elapsed:.0f}s)", file=sys.stderr)
        return None

    # Parse LABEL: TYPE lines
    type_map = {}
    for line in response.split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        m = re.match(r'^([^:]+):\s*(\w+)', line)
        if m:
            label = m.group(1).strip()
            ptype = m.group(2).strip().upper()
            type_map[label] = ptype

    print(f"  [TYPES] {len(type_map)} types extracted ({elapsed:.0f}s)",
          file=sys.stderr)
    return type_map


# ---------------------------------------------------------------------------
# Step 2: Table column insertion (mechanical)
# ---------------------------------------------------------------------------

def _insert_type_column(asn_text, type_map):
    """Insert Type column into a 3-column property table.

    Transforms:
      | Label | Statement | Status |
    to:
      | Label | Type | Statement | Status |

    Returns modified ASN text.
    """
    from lib.rebase_deps import find_property_table, parse_table_row

    rows = find_property_table(asn_text)
    if rows is None:
        return asn_text

    # Build replacement rows
    new_rows = []

    # Header: insert Type after Label
    new_rows.append("| Label | Type | Statement | Status |")

    # Separator
    new_rows.append("|-------|------|-----------|--------|")

    # Data rows
    for row in rows[2:]:
        cells = parse_table_row(row)
        if len(cells) < 3:
            new_rows.append(row)
            continue

        label = cells[0].strip().strip("`*")
        ptype = type_map.get(label, "")
        # Rebuild: | label | type | statement... | status |
        # Status is always last cell, statement is everything between
        new_rows.append(
            f"| {cells[0].strip()} | {ptype} | "
            f"{'|'.join(cells[1:-1]).strip()} | {cells[-1].strip()} |"
        )

    # Replace the old table in the text
    # Find the exact span of the old table
    lines = asn_text.split("\n")
    table_start = None
    table_end = None

    for i, line in enumerate(lines):
        if re.match(r"\|\s*Label\s*\|", line):
            table_start = i
            break

    if table_start is None:
        return asn_text

    # Find end of table
    for i in range(table_start, len(lines)):
        if not lines[i].strip().startswith("|"):
            table_end = i
            break
    else:
        table_end = len(lines)

    # Replace
    result_lines = lines[:table_start] + new_rows + lines[table_end:]
    return "\n".join(result_lines)


# ---------------------------------------------------------------------------
# Step 3: Format review/revise cycle (LLM, sonnet)
# ---------------------------------------------------------------------------

def step_format_review(asn_num):
    """Run format review. Returns (is_clean, findings_text)."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [FORMAT] ASN-{asn_num:04d} not found", file=sys.stderr)
        return True, ""

    template = REVIEW_TEMPLATE.read_text()
    asn_content = asn_path.read_text()
    prompt = template.replace("{{asn_content}}", asn_content)

    text, elapsed = _invoke_claude(prompt, model="sonnet", effort="high")
    _log_usage("review", elapsed, asn_num)

    if not text:
        return True, ""

    if "RESULT: CLEAN" in text:
        print(f"  [FORMAT] Clean ({elapsed:.0f}s)", file=sys.stderr)
        return True, text

    # Extract finding count
    m = re.search(r"RESULT:\s*(\d+)\s*FINDING", text)
    count = m.group(1) if m else "?"
    print(f"  [FORMAT] {count} findings ({elapsed:.0f}s)", file=sys.stderr)
    return False, text


def step_format_revise(asn_num, findings):
    """Run format revise with agentic tool access. Returns True on success."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return False

    template = REVISE_TEMPLATE.read_text()
    rel_path = asn_path.relative_to(WORKSPACE)
    prompt = (template
              .replace("{{asn_path}}", str(rel_path))
              .replace("{{findings}}", findings))

    print(f"  [FORMAT] Revising {asn_label}...", file=sys.stderr)

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--max-turns", "30",
        "--allowedTools", "Edit,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start
    _log_usage("revise", elapsed, asn_num)

    if result.returncode != 0:
        print(f"  [FORMAT] Revise FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        return False

    print(f"  [FORMAT] Revised ({elapsed:.0f}s)", file=sys.stderr)
    return True


# ---------------------------------------------------------------------------
# Step 5: Formal statements assembly (mechanical)
# ---------------------------------------------------------------------------

def assemble_formal_statements(asn_num):
    """Mechanically assemble formal-statements.md from table + sections.

    Iterates the property table, extracts derivation sections, assembles
    output. No LLM involved — every table label gets a section.

    Returns the output path, or None on failure.
    """
    from lib.rebase_deps import find_property_table, parse_table_row, detect_columns

    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ASSEMBLE] ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        print(f"  [ASSEMBLE] No property table in {asn_path.name}",
              file=sys.stderr)
        return None

    # Parse table
    header = parse_table_row(rows[0])
    cols = detect_columns(header)
    has_type = "type" in cols
    data_rows = rows[2:]

    # Collect labels and metadata
    properties = []
    labels = []
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue
        label = cells[0].strip().strip("`*")
        if not label:
            continue

        ptype = cells[1].strip() if has_type and len(cells) > 2 else ""
        stmt_start = 2 if has_type else 1
        statement = "|".join(cells[stmt_start:-1]).strip() if len(cells) > 2 else ""

        # Extract name from statement
        name = ""
        if statement:
            m = re.match(r'^([^:.—–]+)', statement)
            if m:
                candidate = m.group(1).strip()
                if len(candidate) >= 2 and candidate[0].isupper():
                    name = candidate[:77] + "..." if len(candidate) > 77 else candidate
        # PascalCase label fallback
        if not name and re.match(r'^[A-Z][a-z].*[A-Z]', label):
            name = label

        construct = TYPE_TO_CONSTRUCT.get(ptype.upper(), "predicate") if ptype else "predicate"

        properties.append({
            "label": label,
            "type": ptype,
            "name": name or label,
            "construct": construct,
            "statement": statement,
        })
        labels.append(label)

    # Extract derivation sections
    sections = extract_property_sections(text, known_labels=labels)

    # Get source metadata
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", text)
    all_dates = re.findall(r"\d{4}-\d{2}-\d{2}",
                           date_match.group(0)) if date_match else []
    asn_date = all_dates[-1] if all_dates else "unknown"

    # Assemble output
    parts = [
        f"# {asn_label} Formal Statements\n",
        f"*Source: {asn_path.name} (revised {asn_date}) — "
        f"Extracted: {time.strftime('%Y-%m-%d')}*\n",
    ]

    for prop in properties:
        label = prop["label"]
        name = prop["name"]
        ptype = prop["type"]
        construct = prop["construct"]

        type_suffix = f" ({ptype}, {construct})" if ptype else ""
        parts.append(f"## {label} — {name}{type_suffix}\n")

        if label in sections:
            # Use the derivation text, but strip the header line (already emitted)
            section = sections[label]
            section_lines = section.split("\n")
            # Skip the bold header line
            body_start = 0
            for i, line in enumerate(section_lines):
                if line.strip().startswith("**") and (label in line):
                    body_start = i + 1
                    break
            # Strip ## sub-headers from body (they'd conflict with property headers)
            body_lines = []
            for line in section_lines[body_start:]:
                if line.startswith("## "):
                    body_lines.append("### " + line[3:])  # demote to ###
                else:
                    body_lines.append(line)
            body = "\n".join(body_lines).strip()
            if body:
                parts.append(body + "\n")
        elif prop["statement"]:
            # No prose section — use statement column text
            parts.append(prop["statement"] + "\n")

    output = "\n".join(parts) + "\n"

    # Write
    out_dir = asn_dir(asn_num)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = formal_stmts(asn_num)
    out_path.write_text(output)
    print(f"  [ASSEMBLE] {out_path.relative_to(WORKSPACE)} "
          f"({len(properties)} properties)", file=sys.stderr)

    # Post-verification: count property headers vs table labels
    # Match only property headers (## LABEL — Name), not prose sub-headers
    written = out_path.read_text()
    header_count = len(re.findall(r'^## \S+.*? — ', written, re.MULTILINE))
    if header_count != len(properties):
        print(f"  [ASSEMBLE] ERROR: wrote {header_count} property headers but "
              f"table has {len(properties)} properties", file=sys.stderr)
        return None

    return out_path


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def normalize_format(asn_num):
    """Run full format normalization. Returns True if clean.

    1. Type extraction (if table is 3-column)
    2. Table fix (mechanical)
    3. Format review/revise cycle (up to 30 cycles)
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return True  # nothing to normalize

    # Step 1-2: Type extraction + table fix
    type_map = step_extract_types(asn_num)
    if type_map:
        text = asn_path.read_text()
        new_text = _insert_type_column(text, type_map)
        if new_text != text:
            asn_path.write_text(new_text)
            print(f"  [TYPES] Inserted Type column into {asn_label}",
                  file=sys.stderr)

    # Step 3: Format review/revise cycle
    print(f"  [FORMAT] Checking {asn_label}...", file=sys.stderr)

    for cycle in range(1, MAX_CYCLES + 1):
        is_clean, findings = step_format_review(asn_num)
        if is_clean:
            return True

        if cycle == MAX_CYCLES:
            print(f"  [FORMAT] Max cycles ({MAX_CYCLES}) reached, "
                  f"still has findings", file=sys.stderr)
            return False

        print(f"  [FORMAT] Cycle {cycle}/{MAX_CYCLES} — revising...",
              file=sys.stderr)
        ok = step_format_revise(asn_num, findings)
        if not ok:
            print(f"  [FORMAT] Revise failed, stopping", file=sys.stderr)
            return False

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Format normalization — type extraction + review/revise")
    parser.add_argument("asn", help="ASN number (e.g., 43)")
    parser.add_argument("--review-only", action="store_true",
                        help="Run review only, don't revise")
    parser.add_argument("--types-only", action="store_true",
                        help="Run type extraction only")
    parser.add_argument("--assemble-only", action="store_true",
                        help="Run formal statements assembly only")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.review_only:
        is_clean, findings = step_format_review(asn_num)
        if findings:
            print(findings)
        sys.exit(0 if is_clean else 1)

    if args.types_only:
        type_map = step_extract_types(asn_num)
        if type_map:
            for label, ptype in type_map.items():
                print(f"  {label}: {ptype}")
        sys.exit(0 if type_map else 1)

    if args.assemble_only:
        path = assemble_formal_statements(asn_num)
        if path:
            print(str(path))
        sys.exit(0 if path else 1)

    ok = normalize_format(asn_num)
    if ok:
        print(f"\n  [FORMAT] ASN-{asn_num:04d} format is clean",
              file=sys.stderr)
    else:
        print(f"\n  [FORMAT] ASN-{asn_num:04d} still has format issues",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
