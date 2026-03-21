#!/usr/bin/env python3
"""
Supersede an ASN — copy project model and consultations to a new ASN number.

The old ASN is marked as deprecated. The new ASN gets:
  - A copy of the project model YAML (with updated ASN number)
  - A copy of consultation questions (if they exist)
  - The old ASN's project model is removed

Usage:
    python scripts/supersede.py --source 48 --target 59
    python scripts/supersede.py -s 48 -t 59
    python scripts/supersede.py -s 48 -t 59 --dry-run
"""

import argparse
import re
import shutil
import sys
import yaml

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, PROJECT_MODEL_DIR,
                   load_manifest)
from lib.common import step_commit

CONSULTATIONS_DIR = WORKSPACE / "vault" / "0-consultations"


def validate(source_num, target_num):
    """Validate source exists and target doesn't."""
    source_label = f"ASN-{source_num:04d}"
    target_label = f"ASN-{target_num:04d}"

    # Source project model must exist
    source_yaml = PROJECT_MODEL_DIR / f"{source_label}.yaml"
    if not source_yaml.exists():
        print(f"  [ERROR] {source_label} has no project model",
              file=sys.stderr)
        sys.exit(1)

    # Target must not exist
    target_yaml = PROJECT_MODEL_DIR / f"{target_label}.yaml"
    if target_yaml.exists():
        print(f"  [ERROR] {target_label} already exists in project model",
              file=sys.stderr)
        sys.exit(1)

    target_asns = list(ASNS_DIR.glob(f"{target_label}-*.md"))
    if target_asns:
        print(f"  [ERROR] {target_label} already exists in reasoning docs",
              file=sys.stderr)
        sys.exit(1)

    return source_label, target_label


def copy_project_model(source_num, target_num, source_label, target_label):
    """Copy project model YAML with updated ASN number."""
    source_yaml = PROJECT_MODEL_DIR / f"{source_label}.yaml"
    target_yaml = PROJECT_MODEL_DIR / f"{target_label}.yaml"

    content = source_yaml.read_text()

    # Update ASN number in the header comment
    content = content.replace(f"# {source_label}", f"# {target_label}")

    target_yaml.write_text(content)
    print(f"  [COPIED] {source_yaml.relative_to(WORKSPACE)} → "
          f"{target_yaml.relative_to(WORKSPACE)}", file=sys.stderr)

    return target_yaml


def copy_consultations(source_num, target_num, source_label, target_label):
    """Copy entire consultation directory (questions + answers) if it exists."""
    source_consult = CONSULTATIONS_DIR / source_label / "consultation"
    target_consult = CONSULTATIONS_DIR / target_label / "consultation"

    if not source_consult.exists():
        print(f"  [SKIP] No consultations for {source_label}",
              file=sys.stderr)
        return False

    # Copy entire consultation directory
    if target_consult.exists():
        shutil.rmtree(target_consult)
    shutil.copytree(source_consult, target_consult)

    # Update ASN references in all copied files
    copied_count = 0
    for filepath in target_consult.rglob("*.md"):
        content = filepath.read_text()
        if source_label in content:
            content = content.replace(source_label, target_label)
            filepath.write_text(content)
        copied_count += 1

    print(f"  [COPIED] consultation ({copied_count} files) → "
          f"{target_consult.relative_to(WORKSPACE)}", file=sys.stderr)

    return True


def remove_source(source_label):
    """Remove the source project model."""
    source_yaml = PROJECT_MODEL_DIR / f"{source_label}.yaml"
    if source_yaml.exists():
        source_yaml.unlink()
        print(f"  [REMOVED] {source_yaml.relative_to(WORKSPACE)}",
              file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Supersede an ASN with a new ASN number")
    parser.add_argument("-s", "--source", type=int, required=True,
                        help="Source ASN number to supersede")
    parser.add_argument("-t", "--target", type=int, required=True,
                        help="Target ASN number (the replacement)")
    parser.add_argument("--keep", action="store_true",
                        help="Keep the source project model (for comparison)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without doing it")
    args = parser.parse_args()

    source_label, target_label = validate(args.source, args.target)

    print(f"  [SUPERSEDE] {source_label} → {target_label}", file=sys.stderr)
    if args.keep:
        print(f"  [KEEP] Source project model will be preserved",
              file=sys.stderr)

    if args.dry_run:
        action = "copy project model and questions"
        if not args.keep:
            action += ", remove source"
        print(f"  [DRY RUN] Would {action}", file=sys.stderr)
        return

    # Copy project model
    copy_project_model(args.source, args.target, source_label, target_label)

    # Copy consultations/questions
    copy_consultations(args.source, args.target, source_label, target_label)

    # Remove source project model (unless --keep)
    if not args.keep:
        remove_source(source_label)

    # Commit
    print(f"\n  === COMMIT ===", file=sys.stderr)
    step_commit(f"supersede(asn): {source_label} → {target_label}")

    print(f"\n  [DONE] {source_label} superseded by {target_label}",
          file=sys.stderr)
    print(f"  [NEXT] Generate questions: ./run/questions.sh {args.target}",
          file=sys.stderr)
    print(f"  [NEXT] Or consult+draft: python scripts/draft.py "
          f"--inquiries {args.target} --resume consult", file=sys.stderr)


if __name__ == "__main__":
    main()
