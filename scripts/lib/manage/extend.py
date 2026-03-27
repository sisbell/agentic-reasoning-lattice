#!/usr/bin/env python3
"""
Extract properties from a source ASN into a new extension ASN.

Usage:
    python scripts/extend.py -s 53 -t 57 -b 34 --properties D0,D1
    python scripts/extend.py --source 53 --target 57 --base 34 --properties D0,D1
"""

import argparse
import re
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, PROJECT_MODEL_DIR,
                   load_manifest, project_yaml, formal_stmts)
from lib.common import read_file, find_asn, invoke_claude, log_usage, step_commit
from lib.foundation import find_extensions, load_foundation_statements


PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
EXTEND_TEMPLATE = PROMPTS_DIR / "extend.md"


def parse_registry_labels(asn_content):
    """Extract property labels from the statement registry table."""
    labels = []
    in_table = False
    for line in asn_content.splitlines():
        lower = line.lower()
        if "statement registry" in lower or "properties introduced" in lower:
            in_table = False  # reset — next table is the one
            continue
        if line.startswith("| ") and ("Label" in line or "label" in line):
            in_table = True
            continue
        if in_table and re.match(r"\|[-\s|]+\|", line):
            continue  # separator row
        if in_table and line.startswith("|"):
            parts = [c.strip() for c in line.split("|")]
            # parts[0] is empty (before first |), parts[1] is label
            if len(parts) >= 3 and parts[1]:
                for sub in parts[1].split(","):
                    sub = sub.strip()
                    if sub:
                        labels.append(sub)
        elif in_table and not line.startswith("|") and line.strip():
            break  # end of table
    return labels


def validate(source_num, target_num, base_num, property_labels):
    """Validate inputs. Returns (source_path, source_content) or exits."""
    # Source != base
    if source_num == base_num:
        print(f"  [ERROR] Source and base cannot be the same ASN",
              file=sys.stderr)
        sys.exit(1)

    # Source ASN exists
    source_path, source_label = find_asn(str(source_num))
    if source_path is None:
        print(f"  [ERROR] Source ASN-{source_num:04d} not found in "
              f"vault/1-reasoning-docs/", file=sys.stderr)
        sys.exit(1)

    # Base manifest exists
    base_manifest = load_manifest(base_num)
    if not base_manifest:
        print(f"  [ERROR] Base ASN-{base_num:04d} has no project model",
              file=sys.stderr)
        sys.exit(1)

    # Target does not exist
    target_label = f"ASN-{target_num:04d}"
    target_yaml = project_yaml(target_num)
    target_asns = list(ASNS_DIR.glob(f"{target_label}-*.md"))
    if target_yaml.exists():
        print(f"  [ERROR] {target_label} already exists in project model",
              file=sys.stderr)
        sys.exit(1)
    if target_asns:
        print(f"  [ERROR] {target_label} already exists in reasoning docs",
              file=sys.stderr)
        sys.exit(1)

    # Property labels exist in source registry
    source_content = source_path.read_text()
    registry_labels = parse_registry_labels(source_content)
    missing = [p for p in property_labels if p not in registry_labels]
    if missing:
        print(f"  [ERROR] Properties not found in source registry: "
              f"{', '.join(missing)}", file=sys.stderr)
        print(f"  Available labels: {', '.join(registry_labels)}",
              file=sys.stderr)
        sys.exit(1)

    return source_path, source_content, base_manifest


def derive_names(base_title, base_num):
    """Compute slug and title for the new extension."""
    existing = find_extensions(base_num)
    n = len(existing)
    base_slug = base_title.lower().replace(" ", "-")
    slug = f"{base_slug}-{n}"
    title = f"{base_title} {n}"
    return slug, title


def compute_depends(base_num):
    """Compute depends list: base's own depends + base itself."""
    base_manifest = load_manifest(base_num)
    deps = set(base_manifest.get("depends", []))
    deps.add(base_num)
    return sorted(deps)


def build_prompt(source_content, property_labels, target_num, base_num,
                 source_num, base_title, ext_title, base_statements,
                 foundation_stmts):
    """Build the extraction prompt from the template."""
    template = read_file(EXTEND_TEMPLATE)
    if not template:
        print("  [ERROR] Prompt template not found", file=sys.stderr)
        sys.exit(1)

    target_label = f"ASN-{target_num:04d}"
    base_label = f"ASN-{base_num:04d}"
    source_label = f"ASN-{source_num:04d}"
    date = time.strftime("%Y-%m-%d")

    return (template
            .replace("{{source_content}}", source_content)
            .replace("{{foundation_statements}}", foundation_stmts)
            .replace("{{base_statements}}", base_statements)
            .replace("{{properties}}", ", ".join(property_labels))
            .replace("{{target_label}}", target_label)
            .replace("{{base_label}}", base_label)
            .replace("{{base_title}}", base_title)
            .replace("{{source_label}}", source_label)
            .replace("{{ext_title}}", ext_title)
            .replace("{{date}}", date))


def strip_preamble(text):
    """Strip any preamble before the ASN header."""
    marker = re.search(r"^# ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def write_manifest(target_num, title, base_num, source_num, depends,
                   properties):
    """Write the project model YAML for the new extension."""
    target_label = f"ASN-{target_num:04d}"
    base_label = f"ASN-{base_num:04d}"
    source_label = f"ASN-{source_num:04d}"
    dep_list = ", ".join(str(d) for d in depends)

    content = (
        f"# {target_label} — {title}\n"
        f'title: "{title}"\n'
        f"extends: {base_num}\n"
        f"source: {source_num}\n"
        f"depends: [{dep_list}]\n"
        f"\n"
        f"inquiry:\n"
        f'  question: "Extension of {base_label}: '
        f'properties {", ".join(properties)} from {source_label}."\n'
    )

    path = project_yaml(target_num)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Extract properties from a source ASN into a new "
                    "extension ASN")
    parser.add_argument("-s", "--source", type=int, required=True,
                        help="Source ASN number (where properties live now)")
    parser.add_argument("-t", "--target", type=int, required=True,
                        help="New ASN number to create")
    parser.add_argument("-b", "--base", type=int, required=True,
                        help="Base ASN that the new extension extends")
    parser.add_argument("--properties", required=True,
                        help="Comma-separated property labels to extract")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    property_labels = [p.strip() for p in args.properties.split(",")]

    # Validate
    source_path, source_content, base_manifest = validate(
        args.source, args.target, args.base, property_labels)

    base_title = base_manifest.get("title", "")
    slug, ext_title = derive_names(base_title, args.base)
    depends = compute_depends(args.base)

    # Load foundation context
    base_label = f"ASN-{args.base:04d}"
    base_stmt_path = formal_stmts(args.base)
    base_statements = read_file(base_stmt_path) or "(No base export available)"

    # Load foundation for the base's dependencies
    foundation_stmts = load_foundation_statements(args.base) if depends else ""

    # Build prompt
    target_label = f"ASN-{args.target:04d}"
    source_label = f"ASN-{args.source:04d}"

    print(f"  [EXTEND] {target_label} (extends {base_label}, "
          f"properties {', '.join(property_labels)} from {source_label})",
          file=sys.stderr)

    prompt = build_prompt(source_content, property_labels, args.target,
                          args.base, args.source, base_title, ext_title,
                          base_statements, foundation_stmts)

    print(f"  Prompt: {len(prompt) // 1024}KB "
          f"(~{len(prompt) // 4} tokens est.)", file=sys.stderr)

    if args.dry_run:
        print(f'  [DRY RUN] Would invoke {args.model}', file=sys.stderr)
        print(f"  Target: {target_label} ({ext_title})", file=sys.stderr)
        print(f"  Slug: {slug}", file=sys.stderr)
        print(f"  Depends: {depends}", file=sys.stderr)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model,
                                  effort=args.effort)
    if not text:
        print("  [ERROR] No extension ASN produced", file=sys.stderr)
        sys.exit(1)

    # Strip preamble
    text = strip_preamble(text)

    # Write reasoning doc
    ASNS_DIR.mkdir(parents=True, exist_ok=True)
    asn_path = ASNS_DIR / f"{target_label}-{slug}.md"
    asn_path.write_text(text + "\n")
    print(f"  [WROTE] {asn_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Write project model
    yaml_path = write_manifest(args.target, ext_title, args.base,
                               args.source, depends, property_labels)
    print(f"  [WROTE] {yaml_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Log usage
    log_usage("extend", elapsed, source=args.source, target=args.target,
              base=args.base, properties=property_labels)

    # Commit
    print(f"\n  === COMMIT ===", file=sys.stderr)
    step_commit(f"extend(asn): {target_label} extract "
                f"{', '.join(property_labels)} from {source_label} "
                f"into {base_label} extension")

    # Hints
    print(f"\n  [NEXT] Review: python scripts/review.py {args.target}",
          file=sys.stderr)
    print(f"  [NEXT] Or review/revise loop: "
          f"python scripts/revise.py {args.target} --converge",
          file=sys.stderr)
    print(f"  [NEXT] Then export: python scripts/normalize.py {args.target}",
          file=sys.stderr)
    print(f"  [NEXT] Then absorb: python scripts/absorb.py {args.target}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
