#!/usr/bin/env python3
"""Lattice-bootstrap CLI — provision the canonical agent corpus into a
lattice.

Thin wrapper around `LatticeBootstrapAgent` (lib/agents/producers/
lattice_bootstrap.py). The agent provisions one canonical spec per
fire; this CLI walks fires-until-quiescent for the requested lattice.

Reads canonical specs from `lattice-bootstrap/agents/` (at repo
root). Each canonical doc carries YAML frontmatter:

    ---
    caste: producer | refiner | scout | worker
    scope: note | claim | inquiry | lattice    # optional
    ---

    # Operator-facing prose body...

For each canonical spec, the agent ensures the lattice carries:

  - The agent doc body at
    `_docuverse/documents/<node>/<user>/agent/<role>.md`.
    On content drift from a previously-provisioned doc, advances the
    version chain.
  - The path registered in `paths.json`.
  - The `agent` classifier (idempotent).
  - `agent.caste.<value>` (idempotent).
  - `agent.scope.<value>` (idempotent; skipped if frontmatter has no
    `scope:`).

Idempotent: re-running on a fully-bootstrapped lattice is a no-op
(or a content sync if canonical specs have advanced).

Usage:
    python scripts/lattice-bootstrap.py
    python scripts/lattice-bootstrap.py --lattice materials
    python scripts/lattice-bootstrap.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.agents.producers.lattice_bootstrap import (
    LatticeBootstrapAgent,
    first_missing_spec,
    is_lattice_bootstrapped,
    read_canonical_specs,
)
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE_NODE, LATTICE_USER


REPO_ROOT = Path(__file__).resolve().parent.parent
BOOTSTRAP_DIR = REPO_ROOT / "lattice-bootstrap"
BOOTSTRAP_AGENTS = BOOTSTRAP_DIR / "agents"


def _lattice_doc_addr(session, node: str, user: str, lattice_name: str):
    """Return the lattice doc's substrate address, or None if missing."""
    rel = (
        f"_docuverse/documents/{node}/{user}/lattice/{lattice_name}.md"
    )
    return session.get_addr_for_path(rel)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="lattice-bootstrap",
        description=(
            "Provision the canonical agent corpus into a lattice via "
            "LatticeBootstrapAgent (one canonical spec per fire; "
            "walks fires-until-quiescent)."
        ),
    )
    parser.add_argument(
        "--lattice", default="xanadu",
        help="Active lattice name (default: xanadu).",
    )
    parser.add_argument(
        "--lattice-dir", type=Path,
        help="Override the lattice directory (default: lattices/<name>).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Report what would change without writing.",
    )
    args = parser.parse_args()

    lattice_root = (
        args.lattice_dir or (REPO_ROOT / "lattices" / args.lattice)
    ).resolve()
    if not lattice_root.exists():
        print(
            f"  [BOOTSTRAP] lattice not found at {lattice_root}",
            file=sys.stderr,
        )
        return 1

    specs = read_canonical_specs(BOOTSTRAP_AGENTS)
    if not specs:
        print(
            f"  [BOOTSTRAP] no canonical specs in {BOOTSTRAP_AGENTS}",
            file=sys.stderr,
        )
        return 1

    print(
        f"  [BOOTSTRAP] target lattice: {lattice_root}",
        file=sys.stderr,
    )
    print(
        f"  [BOOTSTRAP] {len(specs)} canonical agents to bootstrap",
        file=sys.stderr,
    )

    if args.dry_run:
        # Dry-run doesn't open a session. Report which specs would be
        # provisioned by inspecting filesystem only (skips substrate-
        # idempotency checks; reports paths missing/present on disk).
        for spec in specs:
            rel = (
                f"_docuverse/documents/{LATTICE_NODE}/{LATTICE_USER}/"
                f"agent/{spec.role}.md"
            )
            abs_path = REPO_ROOT / rel
            if not abs_path.exists():
                fs_status = "would be created"
            else:
                existing = abs_path.read_text()
                fs_status = (
                    "would be updated"
                    if existing != spec.body else "unchanged"
                )
            print(
                f"  [BOOTSTRAP] {spec.role}: dry-run ({fs_status})",
                file=sys.stderr,
            )
        return 0

    agent = LatticeBootstrapAgent(
        corpus_dir=BOOTSTRAP_AGENTS,
        repo_root=REPO_ROOT,
        node_user=(LATTICE_NODE, LATTICE_USER),
    )

    with open_session(lattice_root) as session:
        lattice_addr = _lattice_doc_addr(
            session, LATTICE_NODE, LATTICE_USER, args.lattice,
        )
        if lattice_addr is None:
            print(
                f"  [BOOTSTRAP] lattice doc not registered for "
                f"{args.lattice}; bootstrapping anyway",
                file=sys.stderr,
            )

        # Walk fires until predicate is satisfied (no missing specs).
        max_fires = len(specs) + 1  # +1 safety
        fires = 0
        while not is_lattice_bootstrapped(
            session, agent.specs, LATTICE_NODE, LATTICE_USER,
        ):
            if fires >= max_fires:
                print(
                    f"  [BOOTSTRAP] runaway: {fires} fires without "
                    f"reaching quiescence",
                    file=sys.stderr,
                )
                return 1
            result = agent(session=session, addr=lattice_addr)
            print(f"  [BOOTSTRAP] {result.detail}", file=sys.stderr)
            if not result.success:
                return 1
            fires += 1

        if fires == 0:
            print(
                f"  [BOOTSTRAP] already bootstrapped (no missing specs)",
                file=sys.stderr,
            )
        else:
            print(
                f"  [BOOTSTRAP] done — {fires} fire(s) to quiescence",
                file=sys.stderr,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
