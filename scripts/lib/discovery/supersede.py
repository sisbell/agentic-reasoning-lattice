#!/usr/bin/env python3
"""
Supersede an ASN -- copy project model and consultations to a new ASN number.

The old ASN is marked as deprecated. The new ASN gets:
  - A copy of the project model YAML (with updated ASN number)
  - A copy of consultation questions (if they exist)
  - The old ASN's project model is removed

Usage:
    python scripts/discovery-supersede.py --source 48 --target 59
    python scripts/discovery-supersede.py -s 48 -t 59
    python scripts/discovery-supersede.py -s 48 -t 59 --dry-run
"""

import re
import shutil
import sys
import yaml

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (WORKSPACE, NOTES_DIR, MANIFESTS_DIR,
                   CONSULTATIONS_DIR, load_manifest, note_yaml)
from lib.shared.common import step_commit


def validate(source_num, target_num):
    """Validate source exists and target doesn't."""
    source_label = f"ASN-{source_num:04d}"
    target_label = f"ASN-{target_num:04d}"

    # Source project model must exist
    source_yaml = note_yaml(source_num)
    if not source_yaml.exists():
        print(f"  [ERROR] {source_label} has no project model",
              file=sys.stderr)
        sys.exit(1)

    # Target must not exist
    target_yaml = note_yaml(target_num)
    if target_yaml.exists():
        print(f"  [ERROR] {target_label} already exists in project model",
              file=sys.stderr)
        sys.exit(1)

    target_asns = list(NOTES_DIR.glob(f"{target_label}-*.md"))
    if target_asns:
        print(f"  [ERROR] {target_label} already exists in reasoning docs",
              file=sys.stderr)
        sys.exit(1)

    return source_label, target_label


def copy_project_model(source_num, target_num, source_label, target_label):
    """Copy project model YAML with updated ASN number."""
    source_yaml = note_yaml(source_num)
    target_yaml = note_yaml(target_num)

    content = source_yaml.read_text()

    # Update ASN number in the header comment
    content = content.replace(f"# {source_label}", f"# {target_label}")

    target_yaml.parent.mkdir(parents=True, exist_ok=True)
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


def remove_source(source_num, source_label):
    """Remove the source project model."""
    source_yaml = note_yaml(source_num)
    if source_yaml.exists():
        source_yaml.unlink()
        print(f"  [REMOVED] {source_yaml.relative_to(WORKSPACE)}",
              file=sys.stderr)
