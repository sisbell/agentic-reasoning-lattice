#!/usr/bin/env python3
"""One-off migration: lift yaml.label / yaml.name / yaml.summary into the
substrate as `label`, `name`, `description` attribute links + sibling docs.

For each claim yaml in scope:
  - Always: read yaml.label and the filename stem; emit `label` link to
    `<stem>.label.md`. Mismatches between yaml.label and the stem are
    logged and the claim's label migration is skipped (the substrate
    doesn't override authoritative-but-disagreeing data).
  - If yaml.name present: emit `name` link to `<stem>.name.md`.
  - If yaml.summary present: emit `description` link to `<stem>.description.md`.
    (Field rename happens at the boundary: yaml uses `summary`, substrate
    uses `description`.)

Default mode is `--dry-run` (no writes). `--apply` performs the migration.

Idempotent. Safe to re-run; existing matching links are no-ops.

Usage:

    python3 scripts/migrate-yaml-attributes-to-substrate.py --dry-run
    python3 scripts/migrate-yaml-attributes-to-substrate.py --asn 34 --apply
    python3 scripts/migrate-yaml-attributes-to-substrate.py --apply  # all ASNs
"""

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import CLAIM_CONVERGENCE_DIR, WORKSPACE
from store.attributes import emit_attribute
from store.store import Store


def _claim_yamls(asn_filter=None):
    """Yield (asn_label, yaml_path) for every claim yaml in scope."""
    if not CLAIM_CONVERGENCE_DIR.exists():
        return
    for asn_dir in sorted(p for p in CLAIM_CONVERGENCE_DIR.iterdir() if p.is_dir()):
        if not asn_dir.name.startswith("ASN-"):
            continue
        if asn_filter is not None and asn_dir.name != asn_filter:
            continue
        for yaml_path in sorted(asn_dir.glob("*.yaml")):
            if yaml_path.name.startswith("_"):
                continue
            yield asn_dir.name, yaml_path


def _load_yaml(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"  ! failed to parse {path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asn", help="restrict to one ASN (e.g., 34)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true",
                      help="write to substrate (default is dry-run)")
    mode.add_argument("--dry-run", action="store_true", default=True,
                      help="report only; do not write (default)")
    args = parser.parse_args()

    asn_filter = None
    if args.asn:
        n = int("".join(c for c in args.asn if c.isdigit()))
        asn_filter = f"ASN-{n:04d}"

    apply_mode = args.apply
    label = "APPLY" if apply_mode else "DRY-RUN"
    print(f"[migrate-yaml-attributes] {label}"
          f"{' on ' + asn_filter if asn_filter else ' on all ASNs'}")

    store = Store() if apply_mode else None
    counts = {"claims": 0, "label_emitted": 0, "label_existed": 0,
              "name_emitted": 0, "name_existed": 0, "name_missing": 0,
              "description_emitted": 0, "description_existed": 0,
              "description_missing": 0}
    label_stem_mismatches = []
    name_missing = []
    description_missing = []

    for asn_label, yaml_path in _claim_yamls(asn_filter):
        data = _load_yaml(yaml_path)
        if data is None:
            continue
        counts["claims"] += 1
        stem = yaml_path.stem
        md_path = yaml_path.with_suffix(".md")
        if not md_path.exists():
            print(f"  ! {yaml_path.relative_to(WORKSPACE)}: "
                  f"sibling md missing; skipping", file=sys.stderr)
            continue
        claim_rel = str(md_path.relative_to(WORKSPACE))

        # label
        yaml_label = data.get("label")
        if yaml_label is None:
            print(f"  ! {claim_rel}: yaml.label missing; skipping label",
                  file=sys.stderr)
        elif yaml_label != stem:
            label_stem_mismatches.append(
                (claim_rel, yaml_label, stem)
            )
        else:
            if apply_mode:
                _, created = emit_attribute(
                    store, claim_rel, "label", yaml_label,
                )
                counts["label_emitted" if created else "label_existed"] += 1
            else:
                counts["label_emitted"] += 1  # would-be

        # name
        yaml_name = data.get("name")
        if not yaml_name:
            counts["name_missing"] += 1
            name_missing.append(claim_rel)
        else:
            if apply_mode:
                _, created = emit_attribute(
                    store, claim_rel, "name", yaml_name,
                )
                counts["name_emitted" if created else "name_existed"] += 1
            else:
                counts["name_emitted"] += 1

        # description (from yaml.summary)
        yaml_summary = data.get("summary")
        if not yaml_summary:
            counts["description_missing"] += 1
            description_missing.append(claim_rel)
        else:
            if apply_mode:
                _, created = emit_attribute(
                    store, claim_rel, "description", yaml_summary,
                )
                counts["description_emitted" if created else "description_existed"] += 1
            else:
                counts["description_emitted"] += 1

    if store is not None:
        store.close()

    # Summary
    print()
    print(f"  Claims processed:    {counts['claims']}")
    print(f"  Label   — emit/exist/mismatch: "
          f"{counts['label_emitted']}/{counts['label_existed']}/"
          f"{len(label_stem_mismatches)}")
    print(f"  Name    — emit/exist/missing:  "
          f"{counts['name_emitted']}/{counts['name_existed']}/"
          f"{counts['name_missing']}")
    print(f"  Desc    — emit/exist/missing:  "
          f"{counts['description_emitted']}/{counts['description_existed']}/"
          f"{counts['description_missing']}")

    if label_stem_mismatches:
        print()
        print(f"  LABEL/STEM MISMATCHES ({len(label_stem_mismatches)}) — "
              f"NOT migrated; needs human review:")
        for rel, lbl, stem in label_stem_mismatches:
            print(f"    {rel}: yaml.label={lbl!r} stem={stem!r}")

    if name_missing:
        print()
        print(f"  CLAIMS MISSING yaml.name ({len(name_missing)}) — "
              f"NOT migrated; needs authoring:")
        for rel in name_missing[:20]:
            print(f"    {rel}")
        if len(name_missing) > 20:
            print(f"    ... and {len(name_missing) - 20} more")

    if description_missing:
        print()
        print(f"  CLAIMS MISSING yaml.summary ({len(description_missing)}) — "
              f"NOT migrated; needs authoring:")
        for rel in description_missing[:20]:
            print(f"    {rel}")
        if len(description_missing) > 20:
            print(f"    ... and {len(description_missing) - 20} more")

    print()
    if not apply_mode:
        print("  (dry-run; no writes performed. Use --apply to migrate.)")
    else:
        print("  (migration applied. Substrate diff in lattices/<lattice>/_store/.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
