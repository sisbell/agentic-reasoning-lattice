"""
Format normalization gate — review/revise cycle + mechanical assembly.

Pipeline:
1. Format review/revise (sonnet) — fix headers, status vocab, add missing entries
2. Formal statements assembly (mechanical) — table + sections → formal-statements.md

Usage (standalone):
    python scripts/lib/normalize_format.py 43
    python scripts/lib/normalize_format.py 43 --review-only
    python scripts/lib/normalize_format.py 43 --assemble-only
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, REVIEWS_DIR, formal_stmts, asn_dir
from lib.shared.common import find_asn, extract_property_sections

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
REVIEW_TEMPLATE = PROMPTS_DIR / "normalize-format.md"
REVISE_TEMPLATE = PROMPTS_DIR / "normalize-format-revise.md"

MAX_CYCLES = 30


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
        timeout=None,
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
# Format review/revise cycle (LLM, sonnet)
# ---------------------------------------------------------------------------

def _format_review_path(asn_label):
    """Path to format review findings file."""
    return REVIEWS_DIR / asn_label / "format-review.md"


def step_format_review(asn_num):
    """Run format review. Returns (is_clean, findings_text).

    Saves findings to vault/2-review/ASN-NNNN/format-review.md.
    """
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

    # Save findings to disk
    review_path = _format_review_path(asn_label)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(text)

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
# Formal statements assembly (mechanical)
# ---------------------------------------------------------------------------

def _is_definition(label, asn_text):
    """Check if a label has a **Definition (Label).** header in the prose."""
    pattern = re.compile(
        r'^\*\*Definition\s*\(' + re.escape(label) + r'\)',
        re.MULTILINE
    )
    return bool(pattern.search(asn_text))


def assemble_formal_statements(asn_num):
    """Mechanically assemble formal-statements.md from table + sections.

    Iterates the property table, extracts derivation sections, assembles
    output. Definitions identified by **Definition (Name).** prose headers.
    No LLM involved — every table label gets a section.

    Returns the output path, or None on failure.
    """
    from lib.formalization.deps import find_property_table, parse_table_row, detect_columns

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

        # Check if this is a definition (from prose header)
        is_def = _is_definition(label, text)

        properties.append({
            "label": label,
            "name": name or label,
            "statement": statement,
            "is_definition": is_def,
        })
        labels.append(label)

    # Extract derivation sections (full text, no truncation)
    sections = extract_property_sections(text, known_labels=labels, truncate=False)

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

        if prop["is_definition"]:
            parts.append(f"## {label} — {name} (DEFINITION, function)\n")
        else:
            parts.append(f"## {label} — {name}\n")

        if label in sections:
            section = sections[label]
            section_lines = section.split("\n")
            # Extract content from the bold header line (formal statement is often there)
            # then include the rest of the section
            body_lines = []
            for i, line in enumerate(section_lines):
                if i == 0 and line.strip().startswith("**") and (label in line):
                    # Strip bold markers, extract content after the header
                    # e.g., **T1 (Name).** formal statement here...
                    stripped = re.sub(r'^\*\*.*?\.\*\*\s*', '', line.strip())
                    if stripped:
                        body_lines.append(stripped)
                    continue
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

    raw_output = "\n".join(parts) + "\n"

    # Trim narrative via LLM in chunks
    # Split raw output into batches by ## headers
    raw_sections = re.split(r'(?=^## )', raw_output, flags=re.MULTILINE)
    raw_sections = [s for s in raw_sections if s.strip()]

    BATCH_SIZE = 5
    trim_template = (PROMPTS_DIR / "trim-statements.md").read_text()
    trimmed_parts = []
    total_elapsed = 0

    for batch_start in range(0, len(raw_sections), BATCH_SIZE):
        batch = raw_sections[batch_start:batch_start + BATCH_SIZE]
        batch_text = "\n".join(batch)
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(raw_sections) + BATCH_SIZE - 1) // BATCH_SIZE

        prompt = (trim_template
                  .replace("{{sections}}", batch_text)
                  .replace("{{output_path}}", ""))  # not used in --print mode

        print(f"  [TRIM] Batch {batch_num}/{total_batches} "
              f"({len(batch)} sections, {len(batch_text) // 1024}KB)...",
              file=sys.stderr)

        trimmed, elapsed = _invoke_claude(prompt, model="sonnet", effort="high")
        total_elapsed += elapsed

        if trimmed:
            trimmed_parts.append(trimmed)
        else:
            # Fallback: use raw batch
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
    out_dir = asn_dir(asn_num)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = formal_stmts(asn_num)
    out_path.write_text(output)
    print(f"  [ASSEMBLE] {out_path.relative_to(WORKSPACE)} "
          f"({len(properties)} properties, "
          f"{len(raw_output) // 1024}KB → {len(output) // 1024}KB)",
          file=sys.stderr)

    # Post-verification: count property headers vs table labels
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
    """Run format normalization. Returns True if clean.

    Format review/revise cycle (up to 30 cycles).
    Findings saved to vault/2-review/ASN-NNNN/format-review.md.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return True  # nothing to normalize

    # Clean prior format review
    review_path = _format_review_path(asn_label)
    if review_path.exists():
        review_path.unlink()

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
        description="Format normalization — review/revise + mechanical assembly")
    parser.add_argument("asn", help="ASN number (e.g., 43)")
    parser.add_argument("--review-only", action="store_true",
                        help="Run review only, don't revise")
    parser.add_argument("--assemble-only", action="store_true",
                        help="Run formal statements assembly only")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.review_only:
        is_clean, findings = step_format_review(asn_num)
        if findings:
            print(findings)
        sys.exit(0 if is_clean else 1)

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
