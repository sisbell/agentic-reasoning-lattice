#!/usr/bin/env python3
"""Force-fire a trigger across every addr in a note's scope.

Operator override that bypasses the trigger's predicate AND the
single-claim narrowing that `run-trigger.py --force` requires. One
pass, one process: the trigger's `scope_query` yields every addr
for the named note (ASN), and the agent fires on each regardless
of predicate state.

For the same "I don't trust the predicate" use cases as
`run-trigger.py --force --claim X`, but ASN-wide:

  - LLM-noise: bulk re-run after a known-bad model run.
  - Crash recovery: substrate state may not reflect actual completion.
  - Stale sidecars: regenerate every claim's description after an
    upstream change the freshness predicate doesn't catch.

This is the explicit "thrash the LLM across the whole note" command.
For per-claim overrides, use `run-trigger.py --claim X --force`.

Usage:
    python scripts/force-trigger.py NAME NOTE

Args:
    NAME — trigger registry name (e.g., claim_describe).
    NOTE — note number (e.g., 34, 0034, ASN-0034).

Examples:
    python scripts/force-trigger.py claim_describe 34
    python scripts/force-trigger.py claim_signature_resolve 36
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import triggers as triggers_module
from lib.lattice.labels import format_label
from lib.runner import Scope, Trigger, run_force_pass


def _resolve_trigger(name: str) -> Trigger:
    """Look up a trigger by name; accepts hyphen or underscore."""
    key = name.replace("-", "_")
    obj = getattr(triggers_module, key, None)
    if isinstance(obj, Trigger):
        return obj
    available = [
        n for n in dir(triggers_module)
        if isinstance(getattr(triggers_module, n, None), Trigger)
    ]
    raise SystemExit(
        f"unknown trigger: {name!r}\n"
        f"available: {', '.join(sorted(available))}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="force-trigger",
        description=(
            "Force-fire a trigger across every addr in a note's scope, "
            "ignoring the predicate."
        ),
    )
    parser.add_argument(
        "trigger",
        help="Trigger registry name (e.g., claim_describe)",
    )
    parser.add_argument(
        "note",
        help="Note number (e.g., 34, 0034, ASN-0034)",
    )
    args = parser.parse_args()

    trigger = _resolve_trigger(args.trigger)
    note_num = int(re.sub(r"\D", "", args.note))
    note_label = format_label(note_num)
    scope = Scope(asn_label=note_label, labels=None)

    result = run_force_pass(triggers=[trigger], scope=scope)

    print(
        f"\n  [{trigger.name}] note={note_label} "
        f"fires={len(result.fires)} errors={len(result.errors)}",
        file=sys.stderr,
    )
    return 0 if not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
