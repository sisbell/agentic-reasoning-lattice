"""Claim signature-resolve agent — producer for per-claim signature sidecars.

Fires per-claim with a stale (or absent) signature sidecar. One fire =
gather context (existing sidecar, transitive dep signatures, notation
primitives), dispatch the LLM helper to produce introduces/removes,
emit the new sidecar via emit_attribute (which advances the sidecar's
version chain), persist the resolve-doc audit trail, commit.

This is the lifted form of the previous signature_resolve orchestrator.
The substrate queries (transitive dep walking, sidecar reads) and
emission steps (emit_attribute, resolve-doc persistence) all live
inside this agent.

Caste: producer. Working surface: claim md content + upstream
signature sidecars. Identity grant: signature sidecar (created or
version-advanced via emit_attribute). Predicate-fired by the runner
on stale claims.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.lattice.attributes import emit_attribute
from lib.lattice.labels import build_cross_asn_label_index
from lib.lattice.notation import read_notation
from lib.predicates.attributes import signature_sidecar_of
from lib.protocols.febe.protocol import Session
from lib.shared.claim_files import build_label_index
from lib.shared.git_ops import step_commit_asn
from lib.shared.paths import (
    CLAIM_DIR, LATTICE, SIGNATURE_RESOLVE_DIR, claim_doc_path,
)

from .helpers import extract_signature_changes


SIGNATURE_MODEL = "sonnet"


# ─── Substrate / sidecar helpers ────────────────────────────────────


def _claim_signature_text(claim_dir: Path, claim_label: str) -> str:
    """Read the existing signature sidecar for this claim, if any."""
    sidecar = claim_dir / f"{claim_label}.signature.md"
    if not sidecar.exists():
        return ""
    return sidecar.read_text().strip()


def _transitive_dep_signatures(
    session: Session,
    claim_md_rel: str,
    label_index: dict,
    asn_label: str,
) -> list:
    """Collect signature sidecar contents for every claim transitively
    cited from this one (via citation.depends, same-ASN only).

    Returns [(label, signature_text), ...] for upstream claims that
    have a non-empty signature sidecar.
    """
    rev_index = {addr: label for label, addr in label_index.items()}
    claim_dir = CLAIM_DIR / asn_label
    asn_label_set = set(build_label_index(claim_dir).keys())

    claim_addr = session.get_addr_for_path(claim_md_rel)
    if claim_addr is None:
        return []
    visited = {claim_addr}
    queue = [claim_addr]
    upstream = []
    while queue:
        cur = queue.pop(0)
        for link in session.active_links("citation.depends", from_set=[cur]):
            for target in link.to_set:
                if target in visited:
                    continue
                visited.add(target)
                label = rev_index.get(target)
                if label and label in asn_label_set:
                    sig = _claim_signature_text(claim_dir, label)
                    if sig:
                        upstream.append((label, sig))
                    queue.append(target)
    return upstream


_BULLET_RE = re.compile(r"^\s*-\s+`([^`]+)`")


def _existing_sidecar_bullets(claim_dir: Path, claim_label: str) -> list:
    """Return [(symbol, bullet_line), ...] from the existing sidecar."""
    sig_text = _claim_signature_text(claim_dir, claim_label)
    if not sig_text:
        return []
    pairs = []
    for line in sig_text.split("\n"):
        line = line.rstrip()
        m = _BULLET_RE.match(line)
        if m:
            pairs.append((m.group(1), line))
    return pairs


def _render_sidecar(symbol_bullet_pairs: list) -> str:
    """Render the sidecar markdown from (symbol, bullet_line) pairs."""
    if not symbol_bullet_pairs:
        return ""
    return "\n".join(b for _, b in symbol_bullet_pairs) + "\n"


# ─── Resolve-doc persistence (audit trail) ──────────────────────────


def _next_run_num(asn_label: str, claim_label: str) -> int:
    asn_dir = SIGNATURE_RESOLVE_DIR / asn_label
    if not asn_dir.exists():
        return 1
    pat = re.compile(rf"^{re.escape(claim_label)}-(\d+)\.md$")
    nums = []
    for p in asn_dir.iterdir():
        m = pat.match(p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) if nums else 0) + 1


def _persist_resolve_doc(
    asn_label: str, claim_label: str, sonnet_output: str, model: str,
):
    run_num = _next_run_num(asn_label, claim_label)
    asn_dir = SIGNATURE_RESOLVE_DIR / asn_label
    asn_dir.mkdir(parents=True, exist_ok=True)
    path = asn_dir / f"{claim_label}-{run_num}.md"
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    content = (
        f"# Signature Resolve — {asn_label}/{claim_label} — run {run_num}\n"
        f"\n"
        f"*{timestamp}*\n"
        f"*Model: {model}*\n"
        f"\n"
        f"## Output\n"
        f"\n"
        f"{sonnet_output.strip()}\n"
    )
    path.write_text(content)
    return path, run_num


# ─── Agent class ────────────────────────────────────────────────────


class ClaimSignatureResolveAgent(Agent):
    """One claim's signature resolution per fire.

    Reads existing signature sidecar + transitive dep signatures +
    notation primitives, dispatches the LLM helper to produce
    introduces/removes, emits the new sidecar via emit_attribute (which
    advances the sidecar's version chain so signature_is_fresh flips
    True), persists the resolve-doc audit trail, commits per fire.
    """

    role: ClassVar[str] = "claim-signature-resolve"

    def __init__(self, *, model: str = SIGNATURE_MODEL):
        self.model = model

    def run(self, session: Session, claim_addr: Address) -> AgentResult:
        claim_rel = session.get_path_for_addr(claim_addr)
        if claim_rel is None:
            return AgentResult(success=False, detail="no-claim-path")

        m = re.search(r"(ASN-(\d{4}))/([^/]+)\.md$", claim_rel)
        if m is None:
            return AgentResult(success=False, detail="unparseable-claim-path")
        asn_label = m.group(1)
        asn_num = int(m.group(2))
        claim_label = m.group(3)

        os.environ.setdefault("PROTOCOL_ASN_LABEL", asn_label)

        claim_md_full = LATTICE / claim_rel
        if not claim_md_full.exists():
            return AgentResult(success=False, detail="no-claim-file")

        claim_dir = CLAIM_DIR / asn_label
        claim_md_content = claim_md_full.read_text()
        existing_signature = _claim_signature_text(claim_dir, claim_label)

        label_index = build_cross_asn_label_index(session.store)
        upstream_sigs = _transitive_dep_signatures(
            session, claim_rel, label_index, asn_label,
        )
        notation_primitives = read_notation(session.store)

        print(
            f"  [SIG-RESOLVE] {asn_label}/{claim_label} ({self.model})...",
            end="", file=sys.stderr, flush=True,
        )
        result = extract_signature_changes(
            claim_md_content, notation_primitives, upstream_sigs,
            existing_signature, model=self.model,
        )
        print(f" ({result.elapsed_seconds:.0f}s)", file=sys.stderr)

        if not result.introduces and not result.removes:
            print(
                f"  [SIG-RESOLVE] {claim_label}: no changes",
                file=sys.stderr,
            )
            return AgentResult(success=True, detail="no-changes")

        existing = _existing_sidecar_bullets(claim_dir, claim_label)
        bullets_by_symbol = dict(existing)
        for entry in result.removes:
            bullets_by_symbol.pop(entry["symbol"], None)
        for entry in result.introduces:
            bullets_by_symbol[entry["symbol"]] = entry["bullet"]

        new_pairs = [(s, bullets_by_symbol[s]) for s in bullets_by_symbol]
        new_sidecar_text = _render_sidecar(new_pairs)

        # First-time: emit_attribute creates the link + sidecar.
        # Subsequent: register_version advances the signature chain;
        # write the new content to the sidecar file.
        #
        # The chain advance is required: signature_is_fresh compares
        # sidecar chain length to claim chain length. emit_attribute
        # alone does not advance the chain (relaxed-model: chains
        # advance only where a predicate consumes them, and the
        # caller is responsible for opting in). Without the
        # register_version branch, the predicate stays False after
        # any claim edit and the runner re-fires until max_iterations.
        sidecar_addr = signature_sidecar_of(session, claim_addr)
        if sidecar_addr is None:
            emit_attribute(
                session, claim_rel, "signature", new_sidecar_text.rstrip(),
            )
        else:
            session.register_version(sidecar_addr)
            sidecar_path = session.get_path_for_addr(sidecar_addr)
            full_sidecar = session.store.lattice_dir / sidecar_path
            body = new_sidecar_text.rstrip() + "\n"
            full_sidecar.write_text(body)

        _, run_num = _persist_resolve_doc(
            asn_label, claim_label, result.raw_text, self.model,
        )

        n_intro = len(result.introduces)
        n_rem = len(result.removes)
        print(
            f"  [SIG-RESOLVE] {claim_label}: {n_intro} introduced, "
            f"{n_rem} removed, run {run_num}",
            file=sys.stderr,
        )

        step_commit_asn(
            asn_num,
            hint=(
                f"signature-resolve(asn): {asn_label}/{claim_label} — "
                f"{n_intro} introduced, {n_rem} removed"
            ),
        )

        return AgentResult(
            success=True,
            detail=f"introduced={n_intro} removed={n_rem}",
        )
