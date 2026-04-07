"""Disassemble ASN — break a monolithic ASN into per-property files via LLM.

Blueprinting step: uses sonnet with Read/Write/Glob tools to semantically
disassemble each property into its own file.

Usage (standalone):
    python scripts/lib/blueprinting/disassemble.py 34
    python scripts/lib/blueprinting/disassemble.py 34 --dry-run
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
from lib.shared.paths import WORKSPACE, blueprint_properties_dir
from lib.shared.common import find_asn

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "blueprinting"
DISASSEMBLE_TEMPLATE = PROMPTS_DIR / "disassemble.md"


def disassemble_asn(asn_num, dry_run=False):
    """Disassemble an ASN into per-property files."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    output_dir = blueprint_properties_dir(asn_label)
    template = DISASSEMBLE_TEMPLATE.read_text()
    rel_asn = asn_path.relative_to(WORKSPACE)
    rel_out = output_dir.relative_to(WORKSPACE)

    prompt = (template
              .replace("{{asn_path}}", str(rel_asn))
              .replace("{{output_dir}}", str(rel_out)))

    print(f"\n  [DISASSEMBLE] {asn_label}", file=sys.stderr)
    print(f"  Source: {rel_asn}", file=sys.stderr)
    print(f"  Output: {rel_out}", file=sys.stderr)

    if dry_run:
        print(f"\n  [DRY RUN] Would invoke sonnet to disassemble {asn_label}",
              file=sys.stderr)
        print(f"  Prompt: {len(prompt)} chars", file=sys.stderr)
        return True

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--allowedTools", "Read,Write,Glob",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [DISASSEMBLE] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return False

    # Extract response
    try:
        data = json.loads(result.stdout)
        response = data.get("result", result.stdout)
    except (json.JSONDecodeError, KeyError):
        response = result.stdout

    print(f"\n  [DISASSEMBLE] Done ({elapsed:.0f}s)", file=sys.stderr)
    print(f"\n{response}", file=sys.stderr)

    # Count output files
    if output_dir.exists():
        files = list(output_dir.glob("*.md"))
        print(f"\n  {len(files)} files created in {rel_out}",
              file=sys.stderr)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Disassemble ASN into per-property files")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without invoking LLM")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = disassemble_asn(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
