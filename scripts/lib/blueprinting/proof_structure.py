"""
Proof structure — decompose proofs into explicit stages.

Post-split blueprinting step: reads per-property files, restructures
each proof into numbered stages for Dafny translation.

Usage (standalone):
    python scripts/proof-structure.py 34
    python scripts/proof-structure.py 34 --label T1
    python scripts/proof-structure.py 34 --dry-run
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
from lib.shared.paths import WORKSPACE, USAGE_LOG, blueprint_properties_dir
from lib.shared.common import find_asn, step_commit_asn

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "blueprinting"
TEMPLATE = PROMPTS_DIR / "proof-structure.md"

# Skip files shorter than this (definitions, stubs)
MIN_CONTENT_SIZE = 500

# Status keywords that indicate no proof to structure
SKIP_STATUSES = {"axiom", "design requirement"}


def _is_definition(content):
    """Check if the property file is a definition (no proof to structure)."""
    # Definition headers: **Definition (Name).**
    if re.search(r'^\*\*Definition\s', content, re.MULTILINE):
        return True
    return False


def _is_axiom_or_design(content):
    """Check if the property has axiom/design-requirement status."""
    lower = content.lower()
    for status in SKIP_STATUSES:
        if status in lower:
            # Check if it appears in a formal contract Axiom field
            if re.search(r'\*Axiom:\*', content):
                return True
            # Check status in property table context
            if re.search(r'status.*' + re.escape(status), lower):
                return True
    return False


def _label_from_filename(filename):
    """Extract property label from filename: T0a.md → T0a."""
    return filename.replace(".md", "")


def proof_structure(asn_num, label=None, dry_run=False):
    """Structure proofs in per-property blueprint files."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    prop_dir = blueprint_properties_dir(asn_label)
    if not prop_dir.exists():
        print(f"  No blueprint directory for {asn_label}",
              file=sys.stderr)
        return False

    # Load vocabulary if available
    vocab_path = prop_dir / "_vocabulary.md"
    vocabulary = vocab_path.read_text() if vocab_path.exists() else "(no vocabulary file)"

    # Collect property files (skip _*.md structural files)
    prop_files = sorted(
        f for f in prop_dir.glob("*.md")
        if not f.name.startswith("_")
    )

    if label:
        prop_files = [f for f in prop_files if _label_from_filename(f.name) == label]

    template = TEMPLATE.read_text()

    print(f"\n  [PROOF-STRUCTURE] {asn_label}: {len(prop_files)} property files",
          file=sys.stderr)

    if dry_run:
        for f in prop_files:
            content = f.read_text()
            size = len(content)
            skip = ""
            if size < MIN_CONTENT_SIZE:
                skip = " (skip: too short)"
            elif _is_definition(content):
                skip = " (skip: definition)"
            elif _is_axiom_or_design(content):
                skip = " (skip: axiom/design)"
            print(f"    {f.name:40s} {size:6d}B{skip}", file=sys.stderr)
        return True

    total_elapsed = 0
    structured = 0
    skipped = 0

    for f in prop_files:
        prop_label = _label_from_filename(f.name)
        content = f.read_text()

        # Skip short files, definitions, axioms
        if len(content) < MIN_CONTENT_SIZE:
            skipped += 1
            continue
        if _is_definition(content):
            skipped += 1
            continue
        if _is_axiom_or_design(content):
            skipped += 1
            continue

        print(f"    {prop_label}...", end="", file=sys.stderr, flush=True)

        prompt = (template
                  .replace("{{vocabulary}}", vocabulary)
                  .replace("{{content}}", content))

        cmd = [
            "claude", "--print",
            "--model", "claude-sonnet-4-6",
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
        total_elapsed += elapsed

        if result.returncode != 0:
            print(f" FAILED ({elapsed:.0f}s)", file=sys.stderr)
            continue

        new_content = result.stdout.strip()

        # Basic sanity: output should be substantial
        if len(new_content) < len(content) * 0.5:
            print(f" REJECTED (output too short: {len(new_content)}B vs {len(content)}B)",
                  file=sys.stderr)
            continue

        if new_content == content.strip():
            print(f" unchanged ({elapsed:.0f}s)", file=sys.stderr)
            skipped += 1
            continue

        f.write_text(new_content + "\n")
        structured += 1
        print(f" done ({elapsed:.0f}s)", file=sys.stderr)

    print(f"\n  [PROOF-STRUCTURE] {structured} structured, {skipped} skipped, "
          f"{total_elapsed:.0f}s total", file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "proof-structure",
            "asn": asn_label,
            "elapsed_s": round(total_elapsed, 1),
            "structured": structured,
            "skipped": skipped,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Proof structure — decompose proofs into explicit stages")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--label", help="Structure a single property only")
    parser.add_argument("--dry-run", action="store_true",
                        help="List property files without processing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = proof_structure(asn_num, label=args.label, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
