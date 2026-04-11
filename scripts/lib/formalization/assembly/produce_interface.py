"""
Produce Interface step — mechanically assemble formal-statements.md from
a formalized ASN, then trim narrative via LLM.

Iterates the property table, extracts derivation sections, assembles
output. Definitions identified by **Definition (Name).** prose headers.

Step function for the orchestrator (scripts/formalization-export.py):
- assemble_formal_statements: parse table + sections → formal-statements.md
"""

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, FORMALIZATION_DIR, USAGE_LOG, formal_stmts, asn_dir
from lib.shared.common import find_asn, invoke_claude, load_property_names, filename_to_label
from lib.formalization.core.build_dependency_graph import find_property_table, parse_table_row, detect_columns

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization" / "assembly"
TRIM_TEMPLATE = PROMPTS_DIR / "produce-interface.md"


def _is_definition(content):
    """Check if property content starts with a Definition header."""
    return bool(re.search(r'^\*\*Definition\s*\(', content.strip(), re.MULTILINE))


def _log_usage(step, elapsed, asn_num):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"assembly-{step}",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def assemble_formal_statements(asn_num):
    """Mechanically assemble formal-statements.md from table + sections.

    Iterates the property table, extracts derivation sections, assembles
    output. Definitions identified by **Definition (Name).** prose headers.

    Returns the output path, or None on failure.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ASSEMBLE] ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    # Read from formalization directory if available
    prop_dir = FORMALIZATION_DIR / asn_label
    if prop_dir.exists():
        table_path = prop_dir / "_table.md"
        table_text = table_path.read_text() if table_path.exists() else ""
    else:
        table_text = asn_path.read_text()

    rows = find_property_table(table_text)
    if rows is None:
        print(f"  [ASSEMBLE] No property table found",
              file=sys.stderr)
        return None

    # Parse table
    header = parse_table_row(rows[0])
    cols = detect_columns(header)
    has_type = "type" in cols
    has_name = "name" in cols
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

        # Read Name column if present
        table_name = ""
        if has_name and len(cells) > cols["name"]:
            table_name = cells[cols["name"]].strip()

        # Statement: everything between fixed columns and status
        fixed_cols = {0}
        if has_name:
            fixed_cols.add(cols["name"])
        if has_type:
            fixed_cols.add(cols["type"])
        stmt_start = max(fixed_cols) + 1
        statement = "|".join(cells[stmt_start:-1]).strip() if len(cells) > stmt_start + 1 else ""

        # Determine name: prefer Name column, then extract from statement, then label
        name = table_name
        if not name and statement:
            m = re.match(r'^([^:.—–]+)', statement)
            if m:
                candidate = m.group(1).strip()
                if len(candidate) >= 2 and candidate[0].isupper():
                    name = candidate[:77] + "..." if len(candidate) > 77 else candidate
        # PascalCase label fallback
        if not name and re.match(r'^[A-Z][a-z].*[A-Z]', label):
            name = label

        properties.append({
            "label": label,
            "name": name or label,
            "statement": statement,
        })
        labels.append(label)

    # Read per-property files if available, otherwise extract from monolithic ASN
    if prop_dir and prop_dir.exists():
        _prop_names = load_property_names(prop_dir)
        sections = {}
        for f in prop_dir.glob("*.md"):
            if not f.name.startswith("_"):
                lbl = filename_to_label(f.name, _prop_names)
                sections[lbl] = f.read_text()
    else:
        from lib.shared.common import extract_property_sections
        text = asn_path.read_text()
        sections = extract_property_sections(text, known_labels=labels, truncate=False)

    # Determine definition status from content
    for prop in properties:
        content = sections.get(prop["label"], "")
        prop["is_definition"] = _is_definition(content) if content else False

    # Get source metadata
    source_text = asn_path.read_text()
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", source_text)
    all_dates = re.findall(r"\d{4}-\d{2}-\d{2}",
                           date_match.group(0) if date_match else "")
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

        if prop["is_definition"]:
            parts.append(f"## {label} — {name} (DEFINITION, function)\n")
        else:
            parts.append(f"## {label} — {name}\n")

        if label in sections:
            section = sections[label]
            section_lines = section.split("\n")
            body_lines = []
            for i, line in enumerate(section_lines):
                if i == 0 and line.strip().startswith("**") and (label in line):
                    stripped = re.sub(r'^\*\*.*?\.\*\*\s*', '', line.strip())
                    if stripped:
                        body_lines.append(stripped)
                    continue
                if line.startswith("## "):
                    body_lines.append("### " + line[3:])
                else:
                    body_lines.append(line)
            body = "\n".join(body_lines).strip()
            if body:
                parts.append(body + "\n")
        elif prop["statement"]:
            parts.append(prop["statement"] + "\n")

    raw_output = "\n".join(parts) + "\n"

    # Trim narrative via LLM in chunks
    raw_sections = re.split(r'(?=^## )', raw_output, flags=re.MULTILINE)
    raw_sections = [s for s in raw_sections if s.strip()]

    BATCH_SIZE = 5
    trim_template = TRIM_TEMPLATE.read_text()
    trimmed_parts = []
    total_elapsed = 0

    for batch_start in range(0, len(raw_sections), BATCH_SIZE):
        batch = raw_sections[batch_start:batch_start + BATCH_SIZE]
        batch_text = "\n".join(batch)
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(raw_sections) + BATCH_SIZE - 1) // BATCH_SIZE

        prompt = (trim_template
                  .replace("{{sections}}", batch_text)
                  .replace("{{output_path}}", ""))

        print(f"  [TRIM] Batch {batch_num}/{total_batches} "
              f"({len(batch)} sections, {len(batch_text) // 1024}KB)...",
              file=sys.stderr)

        trimmed, elapsed = invoke_claude(prompt, model="sonnet", effort="high")
        total_elapsed += elapsed

        if trimmed:
            trimmed_parts.append(trimmed)
        else:
            print(f"  [TRIM] Batch {batch_num} failed — using raw",
                  file=sys.stderr)
            trimmed_parts.append(batch_text)

    _log_usage("trim", total_elapsed, asn_num)

    # Assemble final output
    source_line = (f"*Source: {asn_path.name} (revised {asn_date}) — "
                   f"Extracted: {time.strftime('%Y-%m-%d')}*\n")
    trimmed_body = "\n\n".join(trimmed_parts)
    output = f"# {asn_label} Formal Statements\n\n{source_line}\n{trimmed_body}\n"

    # Write
    out = asn_dir(asn_num)
    out.mkdir(parents=True, exist_ok=True)
    out_path = formal_stmts(asn_num)
    out_path.write_text(output)
    print(f"  [ASSEMBLE] {out_path.relative_to(WORKSPACE)} "
          f"({len(properties)} properties, "
          f"{len(raw_output) // 1024}KB → {len(output) // 1024}KB)",
          file=sys.stderr)

    # Post-verification
    written = out_path.read_text()
    header_count = len(re.findall(r'^## \S+.*? — ', written, re.MULTILINE))
    if header_count != len(properties):
        print(f"  [ASSEMBLE] ERROR: wrote {header_count} property headers but "
              f"table has {len(properties)} properties", file=sys.stderr)
        return None

    return out_path
