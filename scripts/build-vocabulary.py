#!/usr/bin/env python3
"""
Build Vocabulary — scan blueprint property files for notation definitions.

Sends each property file to sonnet, collects definitions, deduplicates,
writes _vocabulary.md.

Usage:
    python scripts/build-vocabulary.py 34
    python scripts/build-vocabulary.py 34 --dry-run
"""

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, blueprint_properties_dir
from lib.shared.common import find_asn, step_commit_asn, load_property_names, filename_to_label

TEMPLATE = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "vocabulary.md"


def _scan_file(label, content, template):
    """Send one property file to sonnet for vocabulary extraction."""
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{content}}", content))

    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
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
        return [], elapsed

    text = result.stdout.strip()
    if "(none)" in text:
        return [], elapsed

    entries = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        if "|" in line:
            parts = [p.strip() for p in line.split("|", 1)]
            if len(parts) == 2 and parts[0]:
                entries.append((parts[0], parts[1]))

    return entries, elapsed


def build_vocabulary(asn_num, dry_run=False):
    """Scan property files and build _vocabulary.md."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    prop_dir = blueprint_properties_dir(asn_label)
    if not prop_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        return False

    structural_skip = {"_table.md", "_preamble.md", "_vocabulary.md"}
    prop_files = sorted(
        f for f in prop_dir.glob("*.md")
        if not f.name.startswith("_")
    )
    structural_files = sorted(
        f for f in prop_dir.glob("_*.md")
        if f.name not in structural_skip
    )
    prop_files = prop_files + structural_files

    template = TEMPLATE.read_text()

    print(f"\n  [VOCABULARY] {asn_label}: {len(prop_files)} property files",
          file=sys.stderr)

    if dry_run:
        for f in prop_files:
            print(f"    {f.name}", file=sys.stderr)
        return True

    # Filter to files worth scanning
    _prop_names = load_property_names(prop_dir)
    candidates = [f for f in prop_files if len(f.read_text().strip()) >= 50]

    def _scan_one(f):
        label = filename_to_label(f.name, _prop_names)
        content = f.read_text()
        entries, elapsed = _scan_file(label, content, template)
        return label, entries

    from lib.shared.common import parallel_llm_calls
    results = parallel_llm_calls(candidates, _scan_one, max_workers=10)

    all_entries = {}
    for label, entries in results:
        if entries:
            for symbol, defn in entries:
                if symbol not in all_entries:
                    all_entries[symbol] = defn

    # Write _vocabulary.md
    vocab_path = prop_dir / "_vocabulary.md"
    with open(vocab_path, "w") as f:
        f.write(f"# Vocabulary — {asn_label}\n\n")
        for symbol in sorted(all_entries.keys()):
            f.write(f"- **{symbol}** — {all_entries[symbol]}\n")

    print(f"\n  [VOCABULARY] {len(all_entries)} definitions extracted",
          file=sys.stderr)
    print(f"  Written: {vocab_path.relative_to(WORKSPACE)}", file=sys.stderr)

    step_commit_asn(asn_num, hint="vocabulary")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Build vocabulary from blueprint property files")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List files without scanning")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = build_vocabulary(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
