"""Decompose ASN — split by section headers, analyze each section.

Blueprinting step: mechanically splits the ASN at ## headers, then runs
parallel LLM calls to produce a YAML structural analysis for each section.

Usage (standalone):
    python scripts/lib/blueprinting/decompose.py 36
"""

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, BLUEPRINTS_DIR
from lib.shared.common import find_asn, invoke_claude, parallel_llm_calls, step_commit_asn


PROMPT_PATH = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "decompose.md"

# Sections that are structural — no LLM analysis needed
SKIP_HEADERS = {
    "PREAMBLE",
    "Claims Introduced",
    "Open Questions",
    "Worked example",
}


def _is_structural(header):
    """Check if a section header is known-structural (skip LLM)."""
    return header in SKIP_HEADERS


def split_sections(text):
    """Mechanical split on ## headers. Returns [(header, content), ...]."""
    sections = []
    current_header = "PREAMBLE"
    current_lines = []

    for line in text.split("\n"):
        if line.startswith("## "):
            sections.append((current_header, "\n".join(current_lines)))
            current_header = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    # Last section
    sections.append((current_header, "\n".join(current_lines)))
    return sections


def _slugify(header):
    """Convert header to filename slug: 'Two components of state' → 'two-components-of-state'."""
    slug = header.lower().replace(" ", "-").replace("/", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def analyze_section(section_content):
    """Call LLM to produce YAML analysis of a section. Returns YAML string or None.

    Returns None if LLM fails or finds no claims.
    """
    prompt_template = PROMPT_PATH.read_text()
    prompt = prompt_template.replace("{{section_content}}", section_content)

    result, elapsed = invoke_claude(prompt, model="sonnet", effort="high")

    if not result:
        return None

    # Strip code fences if present
    text = result.strip()
    if text.startswith("```"):
        first_nl = text.index("\n")
        text = text[first_nl + 1:]
    if text.endswith("```"):
        text = text[:-3].rstrip()

    # Skip if no claims found
    if "- label:" not in text:
        return None

    return text


def _make_worker(sections_dir):
    """Create a worker that writes YAML files as they complete."""
    def _worker(item):
        idx, header, content = item
        slug = _slugify(header)
        label = f"{idx:02d}-{slug}"
        yaml_text = analyze_section(content)
        if yaml_text:
            yaml_path = sections_dir / f"{label}.yaml"
            yaml_path.write_text(yaml_text + "\n")
        return label, yaml_text
    return _worker


def decompose_asn(asn_num):
    """Decompose an ASN into sections with YAML analysis.

    1. Copy ASN to vault/2-blueprints/ASN-NNNN/source.md
    2. Split on ## headers → section .md files
    3. Parallel LLM calls → section .yaml files
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    # Setup directories
    bp_dir = BLUEPRINTS_DIR / asn_label
    sections_dir = bp_dir / "sections"
    sections_dir.mkdir(parents=True, exist_ok=True)

    # Copy source
    asn_text = asn_path.read_text()
    source_path = bp_dir / "source.md"
    source_path.write_text(asn_text)

    print(f"\n  [DECOMPOSE] {asn_label}", file=sys.stderr)
    print(f"  Source: {asn_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Step 1: Mechanical split
    sections = split_sections(asn_text)
    print(f"  {len(sections)} sections found", file=sys.stderr)

    # Write section .md files, collect items for LLM analysis
    items = []
    skipped = 0
    for i, (header, content) in enumerate(sections):
        if header == "PREAMBLE":
            slug = "preamble"
        else:
            slug = _slugify(header)
        filename = f"{i:02d}-{slug}"
        md_path = sections_dir / f"{filename}.md"
        md_path.write_text(content.strip() + "\n")
        lines = len(content.strip().split("\n"))

        if _is_structural(header):
            print(f"    {filename}.md  ({lines} lines) [structural, skip]", file=sys.stderr)
            skipped += 1
        else:
            print(f"    {filename}.md  ({lines} lines)", file=sys.stderr)
            items.append((i, header, content.strip()))

    # Step 2: Parallel LLM analysis (only non-structural sections)
    print(f"\n  Analyzing {len(items)} sections in parallel ({skipped} structural skipped)...",
          file=sys.stderr)
    start = time.time()
    worker = _make_worker(sections_dir)
    results = parallel_llm_calls(items, worker, max_workers=5)
    elapsed = time.time() - start

    # Summary (files already written by workers)
    total_props = 0
    yaml_count = 0
    for label, yaml_text in results:
        if yaml_text:
            prop_count = yaml_text.count("- label:")
            total_props += prop_count
            yaml_count += 1

    print(f"\n  [DECOMPOSE] {len(sections)} sections, {yaml_count} with claims, "
          f"{total_props} total claims, {elapsed:.0f}s",
          file=sys.stderr)

    step_commit_asn(asn_num, hint="decompose")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Decompose ASN into sections with YAML analysis")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = decompose_asn(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
