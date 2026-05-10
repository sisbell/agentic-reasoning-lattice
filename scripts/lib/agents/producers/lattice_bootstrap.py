"""Lattice-bootstrap producer — provision the canonical agent corpus
into a lattice.

Operator-gated producer. One fire = pick the next canonical agent
spec that isn't yet provisioned for the target lattice and provision
it: write the doc body to the lattice's authorial subtree, register
the path, emit the `agent` classifier plus `agent.caste.<value>` and
optional `agent.scope.<value>` subtypes from the spec's frontmatter.

The runner walks fires-to-quiescence: each fire provisions one
agent; predicate flips False until the lattice carries the full
canonical set.

Caste: producer (one-shot identity grant per fire). Scope:
`agent.scope.lattice` — operates over a whole lattice's authorial
subtree rather than a per-note/claim/inquiry resource.

Operator workflow today (pre-trigger-registration):

    python scripts/lattice-bootstrap.py --lattice <name>

The CLI instantiates this agent and walks the canonical set.
Trigger-registration so a runner walks new lattice docs
automatically is deferred to a future arc that adds `lattice` to
the runner Scope.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, List, Optional

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.backend.emit import (
    emit_agent, emit_agent_caste, emit_agent_scope,
)
from lib.protocols.febe.protocol import Session


@dataclass
class CanonicalSpec:
    """One canonical agent spec read from lattice-bootstrap/agents/."""

    role: str
    caste: str
    scope: Optional[str]
    body: str


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_after_frontmatter)."""
    match = re.match(r"^---\s*\n(.*?\n)---\s*\n(.*)$", text, re.DOTALL)
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


def read_canonical_specs(corpus_dir: Path) -> List[CanonicalSpec]:
    """Load every canonical agent doc from a corpus directory."""
    specs: List[CanonicalSpec] = []
    for path in sorted(corpus_dir.glob("*.md")):
        text = path.read_text()
        fm, _body = _parse_frontmatter(text)
        caste = fm.get("caste")
        if caste is None:
            print(
                f"  [LATTICE-BOOTSTRAP] {path.name}: missing 'caste:' "
                f"in frontmatter; skipping",
                file=sys.stderr,
            )
            continue
        scope = fm.get("scope") or None
        specs.append(CanonicalSpec(
            role=path.stem, caste=caste, scope=scope, body=text,
        ))
    return specs


def first_missing_spec(
    session: Session,
    specs: List[CanonicalSpec],
    node: str,
    user: str,
) -> Optional[CanonicalSpec]:
    """Return the first canonical spec that hasn't been provisioned for
    this lattice (no path registered for its target address), or None
    when the lattice carries the full canonical set.
    """
    for spec in specs:
        rel = f"_docuverse/documents/{node}/{user}/agent/{spec.role}.md"
        if session.get_addr_for_path(rel) is None:
            return spec
    return None


def is_lattice_bootstrapped(
    session: Session,
    specs: List[CanonicalSpec],
    node: str,
    user: str,
) -> bool:
    """Predicate: True iff every canonical spec is provisioned for this
    lattice (so the agent should NOT fire). False when at least one
    spec is missing.
    """
    return first_missing_spec(session, specs, node, user) is None


def _provision_one(
    session: Session,
    spec: CanonicalSpec,
    node: str,
    user: str,
    *,
    repo_root: Path,
) -> str:
    """Provision one canonical agent into the lattice's authorial subtree.

    Writes the spec body to disk, registers the path, emits classifiers.
    Returns a status string for logging.
    """
    rel = f"_docuverse/documents/{node}/{user}/agent/{spec.role}.md"
    abs_path = repo_root / rel

    # Filesystem state: write the file.
    fs_status = "unchanged"
    if not abs_path.exists():
        fs_status = "created"
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(spec.body)
    else:
        existing = abs_path.read_text()
        if existing != spec.body:
            fs_status = "updated"
            abs_path.write_text(spec.body)

    # Substrate state: register path + emit classifiers.
    addr = session.get_addr_for_path(rel)
    if addr is None:
        addr = session.register_path(rel)
        path_status = "registered"
    else:
        path_status = "already-registered"

    if fs_status == "updated":
        session.register_version(addr)

    _, agent_created = emit_agent(session.store, addr)
    _, caste_created = emit_agent_caste(
        session.store, addr, spec.caste,
    )
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


class LatticeBootstrapAgent(Agent):
    """One canonical-agent provision per fire.

    Producer caste, lattice-scoped. Fires repeatedly on the same
    lattice doc until the predicate `is_lattice_bootstrapped` returns
    True (i.e., every canonical spec has a registered path in the
    lattice's authorial subtree).

    The agent reads its canonical corpus from `lattice-bootstrap/
    agents/` at repo root; per-fire it picks the first missing spec
    and provisions it. Idempotent — re-running on a fully-bootstrapped
    lattice does nothing.
    """

    role: ClassVar[str] = "lattice-bootstrap"

    def __init__(
        self,
        corpus_dir: Path,
        repo_root: Path,
        node_user: tuple[str, str],
    ) -> None:
        self.corpus_dir = corpus_dir
        self.repo_root = repo_root
        self.node, self.user = node_user
        self._specs: Optional[List[CanonicalSpec]] = None

    @property
    def specs(self) -> List[CanonicalSpec]:
        if self._specs is None:
            self._specs = read_canonical_specs(self.corpus_dir)
        return self._specs

    def run(
        self, session: Session, lattice_doc_addr: Address,
    ) -> AgentResult:
        spec = first_missing_spec(
            session, self.specs, self.node, self.user,
        )
        if spec is None:
            return AgentResult(
                success=True,
                detail=f"already-bootstrapped (n={len(self.specs)})",
            )

        status = _provision_one(
            session, spec, self.node, self.user, repo_root=self.repo_root,
        )
        return AgentResult(success=True, detail=status)
