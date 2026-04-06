#!/usr/bin/env python3
"""
Surface check — foundation consistency audit.

Checks stale labels, structural drift, local redefinitions, registry
misclassification, missing dependencies, exhaustiveness gaps.

Output goes to vault/audit/surface/<timestamp>/.

Usage:
    python scripts/audit/surface.py 36
    python scripts/audit/surface.py 36 --dry-run
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
from lib.shared.paths import WORKSPACE, USAGE_LOG
from lib.shared.common import find_asn
from lib.shared.foundation import load_foundation_statements
from lib.shared.paths import load_manifest

PROMPT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "shared" / "dependency-report.md"
AUDIT_DIR = WORKSPACE / "vault" / "audit" / "surface"


def main():
    parser = argparse.ArgumentParser(
        description="Surface check — foundation consistency audit")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        sys.exit(1)

    foundation = load_foundation_statements(asn_num)
    if not foundation:
        print(f"  [SURFACE] No foundation statements for {asn_label}",
              file=sys.stderr)
        sys.exit(1)

    if not PROMPT_TEMPLATE.exists():
        print(f"  [SURFACE] Template not found: {PROMPT_TEMPLATE}",
              file=sys.stderr)
        sys.exit(1)

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    template = PROMPT_TEMPLATE.read_text()
    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_path.read_text())
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str))

    print(f"  [SURFACE] {asn_label}: {len(prompt) // 1024}KB prompt",
          file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Would send to sonnet", file=sys.stderr)
        return

    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
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
        print(f"  [SURFACE] FAILED ({elapsed:.0f}s)", file=sys.stderr)
        sys.exit(1)

    text = result.stdout.strip()

    # Write report
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    out_dir = AUDIT_DIR / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{asn_label}.md"
    out_path.write_text(text + "\n")

    # Check result
    if "RESULT: CLEAN" in text:
        print(f"  [SURFACE] Clean ({elapsed:.0f}s)", file=sys.stderr)
    else:
        m = re.search(r"RESULT:\s*(\d+)\s*FINDING", text)
        count = m.group(1) if m else "?"
        print(f"  [SURFACE] {count} findings ({elapsed:.0f}s)", file=sys.stderr)

    print(f"  [SURFACE] Report: {out_path.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "surface-audit",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    # Print report
    print(text)


if __name__ == "__main__":
    main()
