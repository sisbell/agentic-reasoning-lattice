"""
Produce Statements step — extract formal statements from a discovery ASN
using LLM to parse narrative reasoning into structured statements.

Step function for the orchestrator (scripts/note-assembly.py):
- export_one: invoke Claude with produce-statements.md prompt, write formal-statements.md
"""

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, USAGE_LOG, NOTE_DIR, prompt_path, formal_stmts, note_dir
from lib.shared.common import find_asn, invoke_claude

TEMPLATE = prompt_path("discovery/assembly/produce-statements.md")


def _build_prompt(asn_content):
    """Assemble export prompt from template + ASN content."""
    template = TEMPLATE.read_text()
    return template.replace("{{asn_content}}", asn_content)


def _strip_preamble(text):
    """Strip any preamble before the statements header."""
    marker = re.search(r"^# ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def _log_usage(asn_label, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "export-statements",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def export_one(asn_id, model="sonnet", effort="high", dry_run=False):
    """Export statements for a single ASN. Returns (asn_label, True) or (asn_id, False)."""
    asn_path, asn_label = find_asn(asn_id)
    if asn_path is None:
        print(f"  No ASN found for {asn_id} in {NOTE_DIR.relative_to(WORKSPACE)}/",
              file=sys.stderr)
        return asn_id, False

    asn_content = asn_path.read_text()

    # Build prompt
    print(f"  [EXPORT] {asn_label}", file=sys.stderr)
    prompt = _build_prompt(asn_content)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if dry_run:
        print(f"  [DRY RUN] Would invoke {model}",
              file=sys.stderr)
        return asn_label, True

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=model, effort=effort)

    if not text:
        print(f"  No statements extracted for {asn_label}", file=sys.stderr)
        return asn_label, False

    # Strip any preamble
    text = _strip_preamble(text)

    # Add source metadata after the title
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", asn_content)
    all_dates = re.findall(r"\d{4}-\d{2}-\d{2}",
                           date_match.group(0)) if date_match else []
    asn_date = all_dates[-1] if all_dates else "unknown"

    source_line = (f"\n*Source: {asn_path.name} (revised {asn_date}) — "
                   f"Extracted: {time.strftime('%Y-%m-%d')}*\n")
    lines = text.split("\n", 1)
    if len(lines) == 2:
        text = lines[0] + "\n" + source_line + lines[1]
    else:
        text = text + "\n" + source_line

    # Write output
    asn_num = int(re.sub(r"[^0-9]", "", asn_label))
    note_dir(asn_num).mkdir(parents=True, exist_ok=True)
    out_path = formal_stmts(asn_num)
    out_path.write_text(text + "\n")

    # Log usage
    _log_usage(asn_label, elapsed)

    print(str(out_path))
    print(f"  [WROTE] {out_path.relative_to(WORKSPACE)}", file=sys.stderr)

    return asn_label, True
