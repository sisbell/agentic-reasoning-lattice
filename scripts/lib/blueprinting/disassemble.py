"""Disassemble ASN — split on boundary markers, classify chunks.

Blueprinting step: mechanically splits the ASN at `---` boundary markers
(inserted by format), then classifies each chunk. Property chunks get
written to per-property files. Ambiguous chunks are flagged.

Usage (standalone):
    python scripts/lib/blueprinting/disassemble.py 34
    python scripts/lib/blueprinting/disassemble.py 34 --dry-run
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, blueprint_properties_dir
from lib.shared.common import find_asn, step_commit_asn


def _extract_table(text):
    """Extract the property table block from text."""
    lines = text.split("\n")
    table_lines = []
    in_table = False
    for line in lines:
        if re.match(r"\|\s*Label\s*\|", line):
            in_table = True
        if in_table:
            if line.strip().startswith("|"):
                table_lines.append(line)
            elif table_lines:
                break
    return "\n".join(table_lines) if table_lines else None


def _classify_chunk(chunk):
    """Classify a chunk split by --- markers.

    Returns (kind, label, content) where kind is:
      'property' — has **LABEL (Name).** header
      'definition' — has **Definition (Name).** header
      'section' — starts with ## or ### header
      'unknown' — can't classify mechanically
    """
    stripped = chunk.strip()
    if not stripped:
        return ("empty", "", "")

    # Definition header first (before general property match):
    # **Definition (Name).** — use the name as label
    m = re.match(r'^\*\*Definition\s*\(([^)]+)\)\.\*\*', stripped)
    if m:
        name = m.group(1).strip()
        return ("definition", name, stripped)

    # Property header: **LABEL (PascalCaseName).**
    # .+? handles labels with spaces/parens like vpos(S, o)
    # [A-Z][A-Za-z0-9]+ anchors on the PascalCase name
    m = re.match(r'^\*\*(.+?)\s+\(([A-Z][A-Za-z0-9]+)\)\.\*\*', stripped)
    if m:
        label = m.group(1)
        return ("property", label, stripped)

    # Also match **LABEL — Name.** format (em-dash style)
    m = re.match(r'^\*\*(.+?)\s+[\u2014\u2013-]\s*', stripped)
    if m:
        label = m.group(1)
        return ("property", label, stripped)

    # Section header: ## or ###
    m = re.match(r'^#{2,3}\s+', stripped)
    if m:
        return ("section", "", stripped)

    return ("unknown", "", stripped)


def _label_to_filename(label):
    """Convert label to filename — delegates to shared function."""
    from lib.shared.common import label_to_filename
    return label_to_filename(label)


def disassemble_asn(asn_num, dry_run=False):
    """Disassemble an ASN into per-property files.

    Mechanically splits on --- markers, classifies each chunk,
    writes property files. Flags ambiguous chunks.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    output_dir = blueprint_properties_dir(asn_label)
    text = asn_path.read_text()

    print(f"\n  [DISASSEMBLE] {asn_label}", file=sys.stderr)
    print(f"  Source: {asn_path.relative_to(WORKSPACE)}", file=sys.stderr)
    print(f"  Output: {output_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    # Split on --- markers
    # The first chunk is the preamble (before any ---)
    raw_chunks = re.split(r'\n---\n', text)

    if len(raw_chunks) < 2:
        print(f"  [DISASSEMBLE] No --- markers found. Run format first.",
              file=sys.stderr)
        return False

    # The preamble may contain the first property (no --- before it).
    # Split preamble at the first bold property/definition header.
    preamble_raw = raw_chunks[0]
    first_prop_match = re.search(
        r'^(\*\*\S+\s*\([^)]+\)\.\*\*|\*\*Definition\s*\([^)]+\)\.\*\*)',
        preamble_raw, re.MULTILINE)
    if first_prop_match:
        preamble = preamble_raw[:first_prop_match.start()].rstrip()
        first_chunk = preamble_raw[first_prop_match.start():]
        chunks = [first_chunk] + raw_chunks[1:]
    else:
        preamble = preamble_raw
        chunks = raw_chunks[1:]

    print(f"  {len(chunks)} chunks after split", file=sys.stderr)

    # Extract table from preamble
    table = _extract_table(text)

    # Classify each chunk
    classified = []
    for chunk in chunks:
        kind, label, content = _classify_chunk(chunk)
        classified.append((kind, label, content))

    # Absorb section chunks into the next property
    # (section headers that introduce context for the following property)
    merged = []
    pending_sections = []
    for kind, label, content in classified:
        if kind == "section":
            pending_sections.append(content)
        elif kind in ("property", "definition"):
            if pending_sections:
                # Prepend section context to this property
                content = "\n\n".join(pending_sections) + "\n\n" + content
                pending_sections = []
            merged.append((kind, label, content))
        else:
            merged.append((kind, label, content))

    if dry_run:
        for kind, label, content in merged:
            size = len(content)
            if kind == "property":
                print(f"    {_label_to_filename(label):30s} property  {size:6d}B",
                      file=sys.stderr)
            elif kind == "definition":
                print(f"    {_label_to_filename(label):30s} definition {size:6d}B",
                      file=sys.stderr)
            elif kind == "unknown":
                preview = content[:80].replace("\n", " ")
                print(f"    {'???':30s} UNKNOWN   {size:6d}B  {preview}",
                      file=sys.stderr)
        if pending_sections:
            print(f"    {len(pending_sections)} trailing section(s)",
                  file=sys.stderr)
        return True

    # Write files
    output_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    flagged = 0

    # Preamble (everything before first ---, minus the table)
    preamble_text = preamble.strip()
    if table:
        preamble_text = preamble_text.replace(table, "").strip()
    (output_dir / "_preamble.md").write_text(preamble_text + "\n")

    # Table
    if table:
        (output_dir / "_table.md").write_text(table + "\n")

    # Trailing sections (not absorbed into a property — write to structural files)
    for section_content in pending_sections:
        # Extract ## header to determine filename
        header_match = re.match(r'^#{2,3}\s+(.+)', section_content.strip())
        if header_match:
            header_name = header_match.group(1).strip()
            # Convert to filename: "Worked example" → _worked-example.md
            filename = "_" + re.sub(r'[^a-z0-9]+', '-', header_name.lower()).strip('-') + ".md"
        else:
            filename = "_section.md"
        (output_dir / filename).write_text(section_content.strip() + "\n")
        print(f"    {filename} (structural)", file=sys.stderr)

    # Property and definition files
    issues = []
    for kind, label, content in merged:
        if kind in ("property", "definition"):
            filename = _label_to_filename(label)
            (output_dir / filename).write_text(content.strip() + "\n")
            written += 1
            print(f"    {filename}", file=sys.stderr)
        elif kind == "unknown":
            flagged += 1
            preview = content[:100].replace("\n", " ")
            issues.append(f"UNKNOWN chunk ({len(content)}B): {preview}")
            # Write to a flagged file for manual review
            (output_dir / f"_flagged-{flagged}.md").write_text(content.strip() + "\n")
            print(f"    _flagged-{flagged}.md  *** NEEDS REVIEW ***",
                  file=sys.stderr)

    # Write issues report if any
    if issues:
        report = (f"# Disassembly Issues — {asn_label}\n\n"
                  + "\n".join(f"- {i}" for i in issues) + "\n")
        (output_dir / "_issues.md").write_text(report)

    # Generate _property_names.md from _table.md
    from lib.shared.common import generate_property_names
    mapping, warnings = generate_property_names(output_dir)
    for w in warnings:
        print(f"    WARNING: {w}", file=sys.stderr)
    print(f"  [DISASSEMBLE] {len(mapping)} property names mapped", file=sys.stderr)

    print(f"\n  [DISASSEMBLE] {written} property files, {flagged} flagged",
          file=sys.stderr)

    step_commit_asn(asn_num, hint="disassemble")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Disassemble ASN into per-property files")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show classification without writing files")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = disassemble_asn(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
