"""Validate — check per-claim file pairs for completeness and consistency.

Blueprinting step: reads the per-claim .yaml + .md pairs from transclude,
runs mechanical checks. No LLM calls.

Usage (standalone):
    python scripts/lib/claim_derivation/validate.py 36
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import blueprint_claims_dir
from lib.shared.common import find_asn


VALID_TYPES = {"axiom", "definition", "design-requirement", "lemma", "theorem", "corollary", "consequence"}
REQUIRED_FIELDS = {"label", "name", "type", "depends"}


def validate_asn(asn_num):
    """Validate per-claim file pairs. Returns (errors, warnings)."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return [f"ASN-{asn_num:04d} not found"], []

    claims_dir = blueprint_claims_dir(asn_label)
    if not claims_dir.exists():
        return [f"No claims directory — run transclude first"], []

    errors = []
    warnings = []

    # Collect all YAML and MD files
    yaml_files = sorted(f for f in claims_dir.glob("*.yaml"))
    md_files = sorted(f for f in claims_dir.glob("*.md") if not f.name.startswith("_"))
    structural_files = sorted(f for f in claims_dir.glob("_*.md"))

    yaml_stems = {f.stem for f in yaml_files}
    md_stems = {f.stem for f in md_files}

    # 1. Completeness — every .yaml has a .md and vice versa
    for stem in yaml_stems - md_stems:
        errors.append(f"MISSING_MD | {stem}.yaml exists but no {stem}.md")
    for stem in md_stems - yaml_stems:
        errors.append(f"MISSING_YAML | {stem}.md exists but no {stem}.yaml")

    # Load all YAMLs
    all_props = {}  # label → (stem, data)
    labels_seen = {}  # label → stem (for duplicate check)

    for yf in yaml_files:
        try:
            with open(yf) as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            errors.append(f"YAML_ERROR | {yf.name}: {e}")
            continue

        if not data:
            errors.append(f"EMPTY_YAML | {yf.name}")
            continue

        stem = yf.stem
        label = data.get("label", "")

        # 2. Required fields
        for field in REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"MISSING_FIELD | {yf.name}: missing '{field}'")

        # 3. Valid type
        prop_type = data.get("type", "")
        if prop_type and prop_type not in VALID_TYPES:
            errors.append(f"INVALID_TYPE | {yf.name}: type='{prop_type}'")

        # 4. No duplicate labels
        if label:
            if label in labels_seen:
                errors.append(f"DUPLICATE_LABEL | '{label}' in {stem}.yaml and {labels_seen[label]}.yaml")
            else:
                labels_seen[label] = stem
                all_props[label] = (stem, data)

        # 5. Label hygiene
        if label:
            if ' ' in label:
                errors.append(f"BAD_LABEL | {yf.name}: label '{label}' contains spaces")
            if label.endswith('.'):
                errors.append(f"BAD_LABEL | {yf.name}: label '{label}' ends with period")

    # 6. Body not empty
    for mf in md_files:
        content = mf.read_text().strip()
        if not content:
            errors.append(f"EMPTY_BODY | {mf.name}")

    # Dependency validation is deferred — labels are resolved mechanically
    # against upstream ASN claim-convergence directories during promote/claim-convergence.

    return errors, warnings


def print_validation(asn_num):
    """Run validation and print results."""
    _, asn_label = find_asn(str(asn_num))
    errors, warnings = validate_asn(asn_num)

    claims_dir = blueprint_claims_dir(asn_label)
    yaml_count = len(list(claims_dir.glob("*.yaml"))) if claims_dir.exists() else 0
    md_count = len([f for f in claims_dir.glob("*.md") if not f.name.startswith("_")]) if claims_dir.exists() else 0
    structural_count = len(list(claims_dir.glob("_*.md"))) if claims_dir.exists() else 0

    print(f"\n  [VALIDATE] {asn_label}", file=sys.stderr)
    print(f"  {yaml_count} claims, {md_count} .md files, {structural_count} structural",
          file=sys.stderr)

    if errors:
        print(f"\n  ERRORS ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"    ✗ {e}", file=sys.stderr)

    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):", file=sys.stderr)
        for w in warnings:
            print(f"    ! {w}", file=sys.stderr)

    if not errors:
        print(f"\n  RESULT: PASS ({len(errors)} errors, {len(warnings)} warnings)",
              file=sys.stderr)
    else:
        print(f"\n  RESULT: FAIL ({len(errors)} errors, {len(warnings)} warnings)",
              file=sys.stderr)

    return len(errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate per-claim file pairs for completeness and consistency")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = print_validation(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
