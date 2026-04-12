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
from lib.shared.common import find_asn, invoke_claude, build_label_index, load_property_metadata

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

    # Read from formalization directory
    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        print(f"  [ASSEMBLE] No formalization directory for {asn_label}",
              file=sys.stderr)
        return None

    # Read metadata from per-property YAMLs
    metadata = load_property_metadata(prop_dir)
    if not metadata:
        print(f"  [ASSEMBLE] No per-property YAML files found",
              file=sys.stderr)
        return None

    _label_index = build_label_index(prop_dir)
    _filename_to_label = {f"{stem}.md": lbl for lbl, stem in _label_index.items()}

    # Collect labels and metadata
    properties = []
    labels = []
    for label, data in metadata.items():
        name = data.get("name", "")
        if not name and re.match(r'^[A-Z][a-z].*[A-Z]', label):
            name = label
        properties.append({
            "label": label,
            "name": name or label,
            "statement": "",  # statement not stored in YAML — extracted from .md below
        })
        labels.append(label)

    # Read per-property .md files
    sections = {}
    for f in prop_dir.glob("*.md"):
        if not f.name.startswith("_"):
            lbl = _filename_to_label.get(f.name, f.stem)
            sections[lbl] = f.read_text()

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
