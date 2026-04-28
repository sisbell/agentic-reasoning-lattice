#!/usr/bin/env python3
"""Compare manifest depends: against substrate-aggregated deps for each
claim ASN. Surfaces divergences before Phase 3b consumer migration.

For every ASN under lattices/<lattice>/claim-convergence/, the script:

  manifest_deps = sorted({manifest['depends']})
  substrate_deps = aggregate_asn_deps(store, asn_label)

and reports any ASN where the two disagree. Three failure modes:

- manifest has dep N, substrate doesn't: stale manifest declaration
  (or the corresponding citation never made it to substrate)
- substrate has dep N, manifest doesn't: undeclared dep — claim cites
  ASN-N but manifest never declared it
- both differ in ordering only: false alarm (we sort both)

Read-only. Run before migrating consumers to substrate aggregation.

Usage:
    python3 scripts/verify-asn-deps-alignment.py
    LATTICE=materials python3 scripts/verify-asn-deps-alignment.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from shared.paths import CLAIM_CONVERGENCE_DIR, WORKSPACE, load_manifest
from store.populate import aggregate_asn_deps
from store.store import Store


def main():
    print(f"[verify-asn-deps-alignment]")
    print(f"  CLAIM_CONVERGENCE_DIR = {CLAIM_CONVERGENCE_DIR.relative_to(WORKSPACE)}")
    print()

    if not CLAIM_CONVERGENCE_DIR.exists():
        print(f"  no claim-convergence dir at {CLAIM_CONVERGENCE_DIR}",
              file=sys.stderr)
        return 1

    asn_dirs = sorted(
        d for d in CLAIM_CONVERGENCE_DIR.iterdir()
        if d.is_dir() and re.match(r"ASN-\d+", d.name)
    )
    print(f"  Checking {len(asn_dirs)} claim ASN(s)")
    print()

    aligned = 0
    divergent = 0
    issues = []
    with Store() as store:
        for asn_dir in asn_dirs:
            asn_label = asn_dir.name
            asn_id = int(asn_label.split("-")[1])
            manifest = load_manifest(asn_id)
            manifest_deps = sorted(set(manifest.get("depends", []) or []))
            substrate_deps = aggregate_asn_deps(store, asn_label)
            if manifest_deps == substrate_deps:
                aligned += 1
                continue
            divergent += 1
            issues.append((asn_label, manifest_deps, substrate_deps))

    if not issues:
        print(f"  All {aligned} ASNs aligned.")
        return 0

    print(f"  Aligned:   {aligned}")
    print(f"  Divergent: {divergent}")
    print()
    for asn_label, m, s in issues:
        only_m = sorted(set(m) - set(s))
        only_s = sorted(set(s) - set(m))
        print(f"  {asn_label}:")
        if only_m:
            print(f"    manifest only:  {only_m}  "
                  f"(declared but not cited in substrate)")
        if only_s:
            print(f"    substrate only: {only_s}  "
                  f"(cited in claims but not declared in manifest)")
    return 0 if not issues else 2


if __name__ == "__main__":
    sys.exit(main())
