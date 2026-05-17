#!/usr/bin/env python3
"""Run a single trigger against an ASN scope, to quiescence.

Per-trigger CLI: the operator-facing primitive for invoking the
runner. Looks up the trigger by name from `lib.triggers`, builds the
Scope, walks `run_until_quiescent` (or `run_force_pass` under
`--force`) until quiescent, prints a one-line status, exits.

The architecture is one process = one trigger. Cross-trigger
coordination is stigmergic — substrate state, not shared trigger
lists. Operator invokes per trigger; predicates handle ordering.

Usage:
    python scripts/run-trigger.py NAME ASN [--claim LABEL] [--force]

Args:
    NAME    — trigger registry name (e.g., cone_review, full_review,
              claim_describe). Hyphens or underscores accepted; the
              registry lookup normalizes.
    ASN     — ASN number (e.g., 36, 0036, ASN-0036).

Flags:
    --claim LABEL    — Restrict scope to one claim's label. Only
                       valid for triggers whose `supports_claim_filter`
                       is True (cone_review, claim_describe, etc.).
    --force          — Force-pass: fire every (trigger, addr) in scope
                       regardless of predicate. For claim-scope triggers
                       this requires --claim (bare ASN-wide --force at
                       claim-scope is the easy way to thrash the LLM).
                       Note-scope triggers (note_statements, etc.) yield
                       a single address — bare --force is allowed there.
    --max-iterations N — Cap on runner passes (default 100).

Examples:
    python scripts/run-trigger.py cone_review 36
    python scripts/run-trigger.py claim_describe 36 --claim T7
    python scripts/run-trigger.py cone_review 36 --claim T7 --force
    python scripts/run-trigger.py note_statements 43 --force
"""

from __future__ import annotations

import argparse
import re
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import triggers as triggers_module
from lib.lattice.labels import format_label
from lib.runner import Scope, Trigger, run_force_pass, run_until_quiescent
from lib.runner.run import request_shutdown


def _install_shutdown_handlers() -> None:
    """Trap SIGTERM/SIGINT to request graceful runner shutdown.

    Same behavior as note-scheduler.py: signal flips the runner's
    shutdown flag; current fire completes; runner returns before
    starting another. Use SIGKILL to abort mid-fire.
    """
    def _handler(signum, _frame):
        sig_name = signal.Signals(signum).name
        print(
            f"\n  [run-trigger] {sig_name} received — finishing current "
            f"fire then exiting (use SIGKILL to abort sooner)",
            file=sys.stderr,
        )
        request_shutdown()

    signal.signal(signal.SIGTERM, _handler)
    signal.signal(signal.SIGINT, _handler)


def _resolve_trigger(name: str) -> Trigger:
    """Look up a trigger by name in `lib.triggers`.

    Accepts hyphenated or underscored names; the registry exposes
    underscored Python identifiers.
    """
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
    _install_shutdown_handlers()

    parser = argparse.ArgumentParser(
        prog="run-trigger",
        description=(
            "Run one trigger against an ASN to quiescence. "
            "One trigger per process; coordination is stigmergic."
        ),
    )
    parser.add_argument(
        "trigger",
        help="Trigger registry name (e.g., cone_review, claim_describe)",
    )
    parser.add_argument(
        "asn",
        help="ASN number (e.g., 36, 0036, ASN-0036)",
    )
    parser.add_argument(
        "--claim", metavar="LABEL",
        help="Restrict to one claim label (claim-scope triggers only)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help=(
            "Force-pass: fire ignoring predicate. Requires --claim for "
            "claim-scope triggers (bare ASN-wide force can thrash)."
        ),
    )
    parser.add_argument(
        "--max-iterations", type=int, default=100,
        help="Max runner passes (default 100)",
    )
    parser.add_argument(
        "--no-commit", action="store_true",
        help="Skip the per-fire auto-commit (default: commit after each fire).",
    )
    args = parser.parse_args()

    trigger = _resolve_trigger(args.trigger)

    if args.claim and not trigger.supports_claim_filter:
        parser.error(
            f"trigger {trigger.name!r} does not support --claim "
            f"(its scope_query does not honor scope.labels)"
        )
    if args.force and not args.claim and trigger.supports_claim_filter:
        parser.error(
            f"--force requires --claim for {trigger.name!r} "
            f"(claim-scope trigger; bare ASN-wide force can thrash)"
        )

    asn_num = int(re.sub(r"\D", "", args.asn))
    asn_label = format_label(asn_num)
    labels = frozenset({args.claim}) if args.claim else None
    scope = Scope(asn_label=asn_label, labels=labels)

    auto_commit = not args.no_commit
    if args.force:
        result = run_force_pass(
            triggers=[trigger], scope=scope, auto_commit=auto_commit,
        )
    else:
        result = run_until_quiescent(
            triggers=[trigger], scope=scope,
            max_iterations=args.max_iterations,
            auto_commit=auto_commit,
        )

    print(
        f"\n  [{trigger.name}] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)} "
        f"quiescent={result.quiescent}",
        file=sys.stderr,
    )
    return 0 if (result.quiescent or args.force) and not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
