"""Signature-resolve orchestrator — per-claim and full-ASN sweep.

Mechanical loop that gathers context (upstream signatures, notation
primitives, existing sidecar), dispatches the signature-resolve agent
(`lib/agents/signature_resolve/`), and applies its output to the
substrate (sidecar update + signature link emission + resolve-doc
persistence + commit).

Two entry points:
- `run_resolve(asn_num, claim_label)` — one claim
- `run_sweep(asn_num)` — every claim in the ASN
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from lib.agent import attributed_to
from lib.agents.signature_resolve import extract_signature_changes
from lib.febe.protocol import Session
from lib.febe.session import open_session
from lib.lattice.attributes import emit_attribute
from lib.lattice.labels import build_cross_asn_label_index
from lib.lattice.notation import read_notation
from lib.shared.common import (
    build_label_index, find_asn, step_commit_asn,
)
from lib.shared.paths import (
    CLAIM_DIR, LATTICE, SIGNATURE_RESOLVE_DIR, claim_doc_path,
)


# ---------------------------------------------------------------------------
# Substrate queries


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


# ---------------------------------------------------------------------------
# Sidecar manipulation


def _existing_sidecar_bullets(claim_dir: Path, claim_label: str) -> list:
    """Return [(symbol, bullet_line), ...] from the existing sidecar.

    The bullet_line is the complete `- \`<sym>\` — <role>` line as
    written. Indexed by symbol so adds/removes can target by symbol;
    the bullet text is the persisted form.
    """
    sig_text = _claim_signature_text(claim_dir, claim_label)
    if not sig_text:
        return []
    pairs = []
    for line in sig_text.split("\n"):
        line = line.rstrip()
        m = re.match(r"^\s*-\s+`([^`]+)`", line)
        if m:
            pairs.append((m.group(1), line))
    return pairs


def _render_sidecar(symbol_bullet_pairs: list) -> str:
    """Render the sidecar markdown from (symbol, bullet_line) pairs.

    The bullet_line is written verbatim. Returns "" for empty input.
    """
    if not symbol_bullet_pairs:
        return ""
    return "\n".join(b for _, b in symbol_bullet_pairs) + "\n"


# ---------------------------------------------------------------------------
# Resolve-doc persistence


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


# ---------------------------------------------------------------------------
# Entrypoints


@attributed_to("signature-resolve")
def run_resolve(asn_num, claim_label, model="sonnet"):
    """Run signature-resolve on one claim. Returns "ok" or "failed"."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    os.environ.setdefault("PROTOCOL_ASN_LABEL", asn_label)

    claim_md_rel = claim_doc_path(asn_label, claim_label)
    claim_md_full = LATTICE / claim_md_rel
    if not claim_md_full.exists():
        print(
            f"  {claim_label}.md not found at {claim_md_full}",
            file=sys.stderr,
        )
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    claim_md_content = claim_md_full.read_text()
    existing_signature = _claim_signature_text(claim_dir, claim_label)

    session = open_session(LATTICE)
    label_index = build_cross_asn_label_index(session.store)
    upstream_sigs = _transitive_dep_signatures(
        session, claim_md_rel, label_index, asn_label,
    )
    notation_primitives = read_notation(session.store)

    print(
        f"  [SIG-RESOLVE] {asn_label}/{claim_label} ({model})...",
        end="", file=sys.stderr, flush=True,
    )
    result = extract_signature_changes(
        claim_md_content, notation_primitives, upstream_sigs,
        existing_signature, model=model,
    )
    print(f" ({result.elapsed_seconds:.0f}s)", file=sys.stderr)

    if not result.introduces and not result.removes:
        # Sidecar already reflects truth — no write, no resolve doc, no commit.
        print(
            f"  [SIG-RESOLVE] {claim_label}: no changes",
            file=sys.stderr,
        )
        return "ok"

    # Compute new sidecar from existing + introduces - removes.
    existing = _existing_sidecar_bullets(claim_dir, claim_label)
    bullets_by_symbol = dict(existing)
    for entry in result.removes:
        bullets_by_symbol.pop(entry["symbol"], None)
    for entry in result.introduces:
        bullets_by_symbol[entry["symbol"]] = entry["bullet"]

    new_pairs = [(s, bullets_by_symbol[s]) for s in bullets_by_symbol]
    new_sidecar_text = _render_sidecar(new_pairs)

    emit_attribute(
        session, claim_md_rel, "signature", new_sidecar_text.rstrip(),
    )

    _, run_num = _persist_resolve_doc(
        asn_label, claim_label, result.raw_text, model,
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
            f"signature-resolve(asn): ASN-{asn_num:04d}/{claim_label} — "
            f"{n_intro} introduced, {n_rem} removed"
        ),
    )
    return "ok"


@attributed_to("signature-resolve")
def run_sweep(asn_num, model="sonnet"):
    """Iterate every claim in the ASN; run signature-resolve on each."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(f"  {claim_dir} not found", file=sys.stderr)
        return "failed"

    labels = sorted(build_label_index(claim_dir).keys())
    print(
        f"\n  [SIG-RESOLVE-SWEEP] {asn_label} — {len(labels)} claims",
        file=sys.stderr,
    )

    for label in labels:
        run_resolve(asn_num, label, model=model)

    return "ok"
