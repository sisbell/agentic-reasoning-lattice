"""Disassemble — read section YAMLs, write per-property file pairs.

Blueprinting step: reads the enriched section YAML files from decompose+enrich,
writes per-property .yaml (metadata) + .md (body + formal contract) pairs.

Usage (standalone):
    python scripts/lib/blueprinting/disassemble.py 36
    python scripts/lib/blueprinting/disassemble.py 36 --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, BLUEPRINTS_DIR
from lib.shared.common import find_asn, label_to_filename, dump_yaml, step_commit_asn


def disassemble_asn(asn_num, dry_run=False):
    """Read section YAMLs, write per-property .yaml + .md pairs."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    sections_dir = BLUEPRINTS_DIR / asn_label / "sections"
    properties_dir = BLUEPRINTS_DIR / asn_label / "properties"

    if not sections_dir.exists():
        print(f"  No sections directory — run decompose first", file=sys.stderr)
        return False

    print(f"\n  [DISASSEMBLE] {asn_label}", file=sys.stderr)
    print(f"  Sections: {sections_dir.relative_to(WORKSPACE)}", file=sys.stderr)
    print(f"  Output:   {properties_dir.relative_to(WORKSPACE)}", file=sys.stderr)

    if not dry_run:
        properties_dir.mkdir(parents=True, exist_ok=True)

    # Collect all properties from section YAMLs
    prop_count = 0
    structural_count = 0

    for yaml_path in sorted(sections_dir.glob("*.yaml")):
        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        if not data:
            continue

        properties = data.get("properties", [])

        if properties:
            for prop in properties:
                label = prop.get("label", "")
                if not label:
                    print(f"    WARNING: property without label in {yaml_path.name}",
                          file=sys.stderr)
                    continue

                stem = label_to_filename(label).replace(".md", "")

                # Build metadata dict
                meta = {
                    "label": label,
                    "name": prop.get("name", ""),
                }
                if prop.get("type"):
                    meta["type"] = prop["type"]
                if prop.get("depends"):
                    meta["depends"] = prop["depends"]
                else:
                    meta["depends"] = []
                if prop.get("vocabulary"):
                    meta["vocabulary"] = prop["vocabulary"]
                if prop.get("literature_citations"):
                    meta["literature_citations"] = prop["literature_citations"]

                # Body markdown (formal contract is included in body)
                md_content = prop.get("body", "").rstrip()

                if dry_run:
                    print(f"    {stem}.yaml + {stem}.md  ({label})", file=sys.stderr)
                else:
                    dump_yaml(meta, properties_dir / f"{stem}.yaml")
                    (properties_dir / f"{stem}.md").write_text(md_content + "\n")
                    print(f"    {stem}.yaml + {stem}.md", file=sys.stderr)

                prop_count += 1

    # Copy structural sections (no properties — preamble, table, worked example, etc.)
    for md_path in sorted(sections_dir.glob("*.md")):
        yaml_path = md_path.with_suffix(".yaml")

        # Structural = has no YAML, or YAML has no properties
        is_structural = False
        if not yaml_path.exists():
            is_structural = True
        else:
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            if not data or not data.get("properties"):
                is_structural = True

        if is_structural:
            # Extract slug from filename: "00-preamble.md" → "preamble"
            name = md_path.stem
            if "-" in name:
                slug = name.split("-", 1)[1]
            else:
                slug = name
            out_name = f"_{slug}.md"

            if dry_run:
                print(f"    {out_name}  (structural)", file=sys.stderr)
            else:
                shutil.copy2(md_path, properties_dir / out_name)
                print(f"    {out_name}  (structural)", file=sys.stderr)

            structural_count += 1

    print(f"\n  [DISASSEMBLE] {prop_count} properties, {structural_count} structural files",
          file=sys.stderr)

    if not dry_run:
        step_commit_asn(asn_num, hint="disassemble")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Disassemble section YAMLs into per-property file pairs")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be written without writing")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = disassemble_asn(asn_num, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
