#!/usr/bin/env python3
"""Lattice-bootstrap protocol — provision agent docs onto a lattice.

Reads the canonical agent specifications under `lattice-bootstrap/agents/`
(at repo root) and ensures each lattice carries:

  - The agent doc file at `_docuverse/documents/agent/<role>.md`.
    Content is the canonical body; if the lattice's existing copy
    differs, register_version is called on the doc address (version
    chain advances) and the new content is written to disk.
  - The path registered in `paths.json`.
  - The `agent` classifier (idempotent — no-op if present).
  - The `agent.caste.<value>` classifier from frontmatter (idempotent).
  - The `agent.scope.<value>` classifier from frontmatter (idempotent;
    skipped if frontmatter has no `scope:`).
  - A `lattice` membership link (idempotent).

Each canonical agent doc carries YAML frontmatter:

    ---
    caste: producer | refiner | scout | worker
    scope: note | claim | inquiry      # optional
    ---

    # Operator-facing prose body...

Replaces the prior `setup-agent-scopes.py`, which only handled the
scope classifier on cone-review and full-review. This script is the
canonical entry point for new-lattice setup AND for re-syncing
existing lattices when canonical docs change.

Idempotent: re-running on a lattice with up-to-date content is a
no-op. The script logs each agent's per-lattice status (added,
already-current, content-updated).

Usage:
    python scripts/lattice-bootstrap.py
    python scripts/lattice-bootstrap.py --lattice lattices/materials
    python scripts/lattice-bootstrap.py --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.backend.emit import (
    emit_agent, emit_agent_caste, emit_agent_scope,
)
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE_NODE, LATTICE_USER


REPO_ROOT = Path(__file__).resolve().parent.parent
BOOTSTRAP_DIR = REPO_ROOT / "lattice-bootstrap"
BOOTSTRAP_AGENTS = BOOTSTRAP_DIR / "agents"


@dataclass
class AgentSpec:
    role: str           # e.g., "cone-review"
    caste: str          # producer / refiner / scout / worker
    scope: Optional[str]  # note / claim / inquiry, or None
    body: str           # markdown body without frontmatter


def _parse_frontmatter(text: str) -> Tuple[dict, str]:
    """Return (frontmatter_dict, body_after_frontmatter)."""
    match = re.match(
        r"^---\s*\n(.*?\n)---\s*\n(.*)$", text, re.DOTALL,
    )
    if not match:
        return {}, text
    fm_block = match.group(1)
    body = match.group(2)
    fm: dict = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip()
    return fm, body


def _read_specs() -> List[AgentSpec]:
    """Load every canonical agent doc from BOOTSTRAP_AGENTS."""
    specs: List[AgentSpec] = []
    for path in sorted(BOOTSTRAP_AGENTS.glob("*.md")):
        text = path.read_text()
        fm, body = _parse_frontmatter(text)
        caste = fm.get("caste")
        if caste is None:
            print(
                f"  [BOOTSTRAP] {path.name}: missing 'caste:' in "
                f"frontmatter; skipping",
                file=sys.stderr,
            )
            continue
        scope = fm.get("scope") or None
        role = path.stem
        specs.append(AgentSpec(
            role=role, caste=caste, scope=scope, body=text,
        ))
    return specs


def _bootstrap_one(
    session, lattice_root: Path, spec: AgentSpec, *, dry_run: bool,
) -> str:
    """Apply one agent's bootstrap to the target lattice.

    Returns a status string for logging.
    """
    rel = f"_docuverse/documents/{LATTICE_NODE}/{LATTICE_USER}/agent/{spec.role}.md"
    # Substrate lives at repo root in the unified-docuverse layout;
    # `lattice_root` is the lattice's non-substrate content dir.
    abs_path = REPO_ROOT / rel

    # Filesystem state: write or update the file.
    fs_status = "unchanged"
    if not abs_path.exists():
        fs_status = "created"
        if not dry_run:
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            abs_path.write_text(spec.body)
    else:
        existing = abs_path.read_text()
        if existing != spec.body:
            fs_status = "updated"
            if not dry_run:
                abs_path.write_text(spec.body)

    if dry_run:
        return f"{spec.role}: dry-run (fs would be {fs_status})"

    # Substrate state: register path + emit classifiers.
    addr = session.get_addr_for_path(rel)
    if addr is None:
        addr = session.register_path(rel)
        path_status = "registered"
    else:
        path_status = "already-registered"

    # Version-chain advance on real content change (post-creation).
    if fs_status == "updated":
        session.register_version(addr)

    # agent classifier (idempotent).
    _, agent_created = emit_agent(session.store, addr)
    # agent.caste.<value>
    _, caste_created = emit_agent_caste(
        session.store, addr, spec.caste,
    )
    # agent.scope.<value> (optional)
    scope_emitted = False
    if spec.scope is not None:
        _, scope_emitted = emit_agent_scope(
            session.store, addr, spec.scope,
        )

    parts = [f"fs={fs_status}", f"path={path_status}"]
    if agent_created:
        parts.append("agent+")
    if caste_created:
        parts.append(f"caste.{spec.caste}+")
    if spec.scope is not None and scope_emitted:
        parts.append(f"scope.{spec.scope}+")
    return f"{spec.role}: {', '.join(parts)}"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="lattice-bootstrap",
        description=(
            "Provision agent docs + classifiers onto a lattice from "
            "the canonical lattice-bootstrap/agents/ source."
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

    specs = _read_specs()
    if not specs:
        print(
            f"  [BOOTSTRAP] no agent specs in {BOOTSTRAP_AGENTS}",
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
        for spec in specs:
            status = _bootstrap_one(
                session=None, lattice_root=lattice_root, spec=spec,
                dry_run=True,
            )
            print(f"  [BOOTSTRAP] {status}", file=sys.stderr)
        return 0

    with open_session(lattice_root) as session:
        for spec in specs:
            status = _bootstrap_one(
                session=session, lattice_root=lattice_root, spec=spec,
                dry_run=False,
            )
            print(f"  [BOOTSTRAP] {status}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
