#!/usr/bin/env python3
"""One-shot migration for existing aggregate docs.

Three steps per aggregate:
  1. Add `claims.statements` identity classifier (was previously only
     `transclusion.claim-statements`).
  2. Retire the predecessor `note.statements` sidecar (its supersession
     chain now ends at the aggregate).
  3. Write the mechanically-assembled content to disk via
     `render_claim_statements`. The renderer-registry dispatch was
     retired in favor of real on-disk files; without this write,
     reads of the aggregate would fail (no renderer + no file).

Pre-existing state (from when `claim_decompose` emitted the aggregate
itself): each ASN that ran decompose has a doc carrying
`transclusion.claim-statements`, with `note → derivation → doc` and
`note.statements_sidecar → supersession → doc` already in place.

Run once, then delete this script. After this runs, the aggregate
lifecycle is owned by `ClaimsStatementsRefreshAgent`; future ASNs
get the classifier, retire, and disk write on first claim-quiescence.

Usage:
    python scripts/migrate-claims-statements-classifier.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import emit_claims_statements, emit_retired
from lib.protocols.febe.session import open_session
from lib.renderers.claim_statements import render_claim_statements
from lib.shared.paths import LATTICE


def main() -> int:
    with open_session(LATTICE) as session:
        store = session.store
        # Existing aggregate docs are tagged transclusion.claim-statements;
        # walk that classifier to find them.
        targets = [
            link.to_set[0]
            for link in session.active_links("transclusion.claim-statements")
            if link.to_set
        ]
        if not targets:
            print("  no aggregate docs found; nothing to migrate")
            return 0

        added_classifier = 0
        retired_sidecar = 0
        wrote_content = 0

        for agg in targets:
            already_classified = bool(
                session.active_links("claims.statements", to_set=[agg]),
            )
            if not already_classified:
                emit_claims_statements(store, agg)
                added_classifier += 1

            # Write the mechanically-assembled content to disk
            rel = session.get_path_for_addr(agg)
            if rel is not None:
                full = store.lattice_dir / rel
                full.parent.mkdir(parents=True, exist_ok=True)
                full.write_text(render_claim_statements(session, agg))
                wrote_content += 1

            # Source note via incoming provenance.derivation
            incoming = session.active_links(
                "provenance.derivation", to_set=[agg],
            )
            if not incoming:
                print(f"  WARN: {agg} has no incoming derivation; skip retire")
                continue
            note_addr = incoming[0].from_set[0]

            # note.statements sidecar
            sidecar_addr = None
            for link in session.active_links(
                "statements", from_set=[note_addr],
            ):
                if link.to_set:
                    sidecar_addr = link.to_set[0]
                    break
            if sidecar_addr is None:
                continue

            already_retired = bool(
                session.active_links("retired", to_set=[sidecar_addr]),
            )
            if not already_retired:
                emit_retired(store, sidecar_addr)
                retired_sidecar += 1

        print(
            f"  migrated {len(targets)} aggregates: "
            f"{added_classifier} classifier added, "
            f"{wrote_content} content files written, "
            f"{retired_sidecar} sidecars retired"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
