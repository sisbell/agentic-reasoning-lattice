"""Claim signature-resolve producer — per-claim signature sidecars.

Fires per-claim with a stale (or absent) signature sidecar. One fire =
gather context (existing sidecar, transitive dep signatures, notation
primitives), dispatch the LLM to produce introduces/removes, attest
the new sidecar via attest_attribute (create-or-advance: first call
creates the link, subsequent advances the supersession chain),
persist the resolve-doc audit trail, commit.

Caste: producer. Working surface: claim md content + upstream
signature sidecars. Identity grant: signature sidecar (created or
chain-advanced via attest_attribute). Predicate-fired by the runner
on stale claims.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import ClassVar, List, NamedTuple, Tuple

from lib.agents.base import Agent, AgentResult
from lib.backend.addressing import Address
from lib.lattice.attributes import attest_attribute
from lib.lattice.labels import build_cross_asn_label_index
from lib.lattice.notation import read_notation
from lib.protocols.febe.protocol import Session
from lib.shared.claim_files import build_label_index
from lib.shared.common import read_file
from lib.shared.git_ops import step_commit_asn
from lib.shared.llm_response import invoke_text, parse_two_sections
from lib.shared.paths import (
    CLAIM_DIR, LATTICE, SIGNATURE_RESOLVE_DIR, prompt_path,
)


SIGNATURE_MODEL = "sonnet"
PROMPT_TEMPLATE = prompt_path("agents/producers/claim_signature_resolve.md")


# ─── LLM helper ─────────────────────────────────────────────────────


class SignatureChanges(NamedTuple):
    introduces: list
    removes: list
    raw_text: str
    elapsed_seconds: float


def extract_signature_changes(
    claim_md_content: str,
    notation_primitives: list,
    upstream_signatures: List[Tuple[str, str]],
    existing_signature: str,
    *,
    model: str = "sonnet",
) -> SignatureChanges:
    """Run Sonnet against the signature-resolve prompt; return parsed
    INTRODUCES / REMOVES.

    `upstream_signatures` is `[(label, signature_text), ...]` for each
    upstream claim with a populated signature sidecar.

    Raises on malformed LLM output (missing headers, YAML parse errors,
    malformed entries) — no graceful degradation.
    """
    prompt = _render_prompt(
        claim_md_content, notation_primitives, upstream_signatures,
        existing_signature,
    )
    raw_text, elapsed = invoke_text(prompt, model=model, tools="Read")
    introduces, removes = parse_two_sections(
        raw_text, "INTRODUCES", "REMOVES",
    )
    _validate_introduces(introduces)
    _validate_removes(removes)
    return SignatureChanges(
        introduces=introduces,
        removes=removes,
        raw_text=raw_text,
        elapsed_seconds=elapsed,
    )


def _format_upstream_sigs(upstream: List[Tuple[str, str]]) -> str:
    if not upstream:
        return (
            "(none — this is a foundation claim or has no upstream signatures)"
        )
    return "\n\n".join(f"### {label}\n{sig}" for label, sig in upstream)


def _format_notation_primitives(primitives: list) -> str:
    if not primitives:
        return "(none registered)"
    return "\n".join(f"- `{p}`" for p in primitives)


def _render_prompt(
    claim_md_content: str,
    notation_primitives: list,
    upstream_sigs: List[Tuple[str, str]],
    existing_signature: str,
) -> str:
    template = read_file(PROMPT_TEMPLATE)
    return (
        template
        .replace("{{claim_md_content}}", claim_md_content)
        .replace(
            "{{notation_primitives}}",
            _format_notation_primitives(notation_primitives),
        )
        .replace(
            "{{upstream_signatures}}",
            _format_upstream_sigs(upstream_sigs),
        )
        .replace("{{existing_signature}}", existing_signature or "(none)")
    )


def _validate_introduces(introduces: list) -> None:
    """Per-entry validation; mutates entries to add a parsed `symbol`."""
    for entry in introduces:
        if not isinstance(entry, dict):
            raise ValueError(f"INTRODUCES entry not a dict: {entry}")
        if "bullet" not in entry:
            raise ValueError(f"INTRODUCES entry missing 'bullet': {entry}")
        bullet = entry["bullet"]
        if not isinstance(bullet, str) or not bullet.startswith("- `"):
            raise ValueError(
                f"INTRODUCES bullet must start with '- `<symbol>`': {entry}"
            )
        m = re.match(r"^- `([^`]+)`", bullet)
        if not m:
            raise ValueError(
                f"INTRODUCES bullet has no parseable symbol: {bullet!r}"
            )
        entry["symbol"] = m.group(1)


def _validate_removes(removes: list) -> None:
    for entry in removes:
        if not isinstance(entry, dict):
            raise ValueError(f"REMOVES entry not a dict: {entry}")
        for field in ("symbol", "reason"):
            if field not in entry:
                raise ValueError(f"REMOVES entry missing {field!r}: {entry}")


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

    from lib.predicates.versions import version_head

    claim_addr = session.get_addr_for_path(claim_md_rel)
    if claim_addr is None:
        return []
    state = session.state

    def _base(addr):
        cur = addr
        while state.parent.get(cur) is not None:
            cur = state.parent[cur]
        return cur

    # Citations are emitted from version_head and target version_head.
    # BFS at base-identity granularity; query each step from the
    # current head; resolve cited targets back to base.
    visited = {claim_addr}
    queue = [claim_addr]
    upstream = []
    while queue:
        cur = queue.pop(0)
        cur_head = version_head(session, cur)
        for link in session.active_links(
            "citation.depends", from_set=[cur_head],
        ):
            for target in link.to_set:
                target_base = _base(target)
                if target_base in visited:
                    continue
                visited.add(target_base)
                label = rev_index.get(target_base)
                if label and label in asn_label_set:
                    sig = _claim_signature_text(claim_dir, label)
                    if sig:
                        upstream.append((label, sig))
                    queue.append(target_base)
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
    notation primitives, dispatches the LLM, attests the new sidecar
    via attest_attribute (which advances the sidecar's supersession
    chain so signature_is_fresh flips True), persists the resolve-doc
    audit trail, commits per fire.
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

        # Compute the new sidecar text from existing + LLM delta. On
        # no-op (zero introduces, zero removes), this equals the
        # existing — but we still attest, because the LLM ran and
        # confirmed the sidecar is correct at this revision.
        existing = _existing_sidecar_bullets(claim_dir, claim_label)
        bullets_by_symbol = dict(existing)
        for entry in result.removes:
            bullets_by_symbol.pop(entry["symbol"], None)
        for entry in result.introduces:
            bullets_by_symbol[entry["symbol"]] = entry["bullet"]

        new_pairs = [(s, bullets_by_symbol[s]) for s in bullets_by_symbol]
        new_sidecar_text = _render_sidecar(new_pairs)

        # attest_attribute is the create-or-advance helper; it advances
        # the sidecar's supersession chain so signature_is_fresh reads
        # True. Unconditional — even on zero LLM delta, the agent ran
        # and the attestation matters.
        attest_attribute(
            session, claim_rel, "signature", new_sidecar_text.rstrip(),
        )

        _, run_num = _persist_resolve_doc(
            asn_label, claim_label, result.raw_text, self.model,
        )

        n_intro = len(result.introduces)
        n_rem = len(result.removes)
        if n_intro == 0 and n_rem == 0:
            summary = "re-attested, no changes"
        else:
            summary = f"{n_intro} introduced, {n_rem} removed"
        print(
            f"  [SIG-RESOLVE] {claim_label}: {summary}, run {run_num}",
            file=sys.stderr,
        )

        step_commit_asn(
            asn_num,
            hint=(
                f"signature-resolve(asn): {asn_label}/{claim_label} — "
                f"{summary}"
            ),
        )

        return AgentResult(
            success=True,
            detail=f"introduced={n_intro} removed={n_rem}",
        )
