#!/usr/bin/env python3
"""Run the cone-review trigger across an ASN.

Three modes:
    (default)            predicate-driven convergence loop until quiescent
    --force [LABELS]     force-pass on all apexes, or just the named ones
    --force-from LABEL   force-pass on LABEL and every later apex (topo order)

Discovery:
    --apexes             print qualifying apexes in topological order

Usage:
    python scripts/claim-cone-sweep.py 36
    python scripts/claim-cone-sweep.py 36 --force
    python scripts/claim-cone-sweep.py 36 --force T7,T9
    python scripts/claim-cone-sweep.py 36 --force-from T9
    python scripts/claim-cone-sweep.py 36 --apexes
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.protocols.febe.session import open_session
from lib.runner import Scope, asn, run_force_pass, run_until_quiescent
from lib.shared.paths import LATTICE
from lib.triggers import apex_labels_in_topological_order, cone_review


def _resolve_force_scope(asn_label: str, args) -> Scope:
    """Build the Scope for a force-pass invocation.

    --force        → all apexes (Scope with labels=None)
    --force LABELS → exactly those labels
    --force-from L → L and every later apex in topological order
    """
    if args.force_from:
        with open_session(LATTICE) as session:
            apexes = apex_labels_in_topological_order(session, asn_label)
        if args.force_from not in apexes:
            print(
                f"  [ERROR] {args.force_from!r} is not an apex in {asn_label}.",
                file=sys.stderr,
            )
            print(f"  Apexes: {', '.join(apexes) or '(none)'}",
                  file=sys.stderr)
            sys.exit(1)
        idx = apexes.index(args.force_from)
        return Scope(asn_label=asn_label, labels=frozenset(apexes[idx:]))

    if args.force == "ALL":
        return Scope(asn_label=asn_label)

    labels = frozenset(s.strip() for s in args.force.split(",") if s.strip())
    return Scope(asn_label=asn_label, labels=labels)


def main():
    parser = argparse.ArgumentParser(
        description="Cone-review sweep across an ASN.",
    )
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    parser.add_argument(
        "--force", nargs="?", const="ALL", default=None,
        help="Force-pass: bare = all apexes, with LABELS = exactly those.",
    )
    parser.add_argument(
        "--force-from", metavar="LABEL",
        help="Force-pass on LABEL and every topologically-later apex.",
    )
    parser.add_argument(
        "--apexes", action="store_true",
        help="Print qualifying apexes in topological order and exit.",
    )
    parser.add_argument("--max-iterations", type=int, default=100)
    args = parser.parse_args()

    asn_num = int(re.sub(r"\D", "", args.asn))
    asn_label = f"ASN-{asn_num:04d}"

    if args.apexes:
        with open_session(LATTICE) as session:
            for label in apex_labels_in_topological_order(session, asn_label):
                print(label)
        return

    if args.force is not None or args.force_from is not None:
        scope = _resolve_force_scope(asn_label, args)
        result = run_force_pass(triggers=[cone_review], scope=scope)
    else:
        result = run_until_quiescent(
            triggers=[cone_review],
            scope=asn(asn_num),
            max_iterations=args.max_iterations,
        )

    print(
        f"\n  [SWEEP] iterations={result.iterations} "
        f"fires={len(result.fires)} errors={len(result.errors)}",
        file=sys.stderr,
    )
    sys.exit(0 if not result.errors else 1)


if __name__ == "__main__":
    main()
