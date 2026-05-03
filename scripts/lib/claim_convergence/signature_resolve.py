"""Signature Resolve — populate per-claim non-logical symbol signatures.

For each claim, Sonnet reads the prose and identifies which non-logical
symbols the claim *introduces* — distinct from symbols it borrows from
upstream deps and from notation primitives. Output is a structured list
that the orchestrator writes to the claim's `<label>.signature.md`
sidecar and emits as a `signature` substrate link.

The signature graph is what the existing `declared-symbols-resolve`
validator consumes: every symbol used in a claim's Formal Contract
must trace through the citation closure to a claim that owns it (or be
a notation primitive). Without populated signatures, the validator has
no ownership data and silently passes symbols whose owners aren't
cited — the gap that let OrdinalDisplacement → NAT-carrier and T1 →
NAT-carrier escape 600+ reviews.

This stage runs as a one-shot bulk populate (sweep) and per-claim on
demand. Cone-review's safety net catches gaps the resolver missed.

Step functions for the orchestrator (scripts/claim-signature-resolve.py):
- run_resolve: one claim, full pipeline
- run_sweep: iterate every claim in the ASN
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import (
    LATTICE, CLAIM_DIR, SIGNATURE_RESOLVE_DIR,
    prompt_path, claim_doc_path,
)
from lib.shared.common import (
    find_asn, build_label_index, read_file, invoke_claude,
    strip_code_fence, step_commit_asn,
)
from lib.backend.store import Store, attributed_to
from lib.backend.populate import build_cross_asn_label_index
from lib.backend.predicates import active_links
from lib.backend.emit import emit_attribute
from lib.backend.notation import read_notation


PROMPT_TEMPLATE = prompt_path("claim-convergence/signature-resolve.md")


# ---------------------------------------------------------------------------
# Substrate queries

def _claim_signature_text(claim_dir, claim_label):
    """Read the existing signature sidecar for this claim, if any."""
    sidecar = claim_dir / f"{claim_label}.signature.md"
    if not sidecar.exists():
        return ""
    return sidecar.read_text().strip()


def _transitive_dep_signatures(store, claim_md_rel, label_index, asn_label):
    """Collect signature sidecar contents for every claim transitively
    cited from this one (via citation.depends, same-ASN only).

    Returns a list of (label, signature_text) tuples for upstream claims
    that have a non-empty signature sidecar."""
    rev_index = {addr: label for label, addr in label_index.items()}
    claim_dir = CLAIM_DIR / asn_label
    asn_label_set = set(build_label_index(claim_dir).keys())

    claim_addr = store.path_to_addr.get(claim_md_rel)
    if claim_addr is None:
        return []
    visited = {claim_addr}
    queue = [claim_addr]
    upstream = []
    while queue:
        cur = queue.pop(0)
        for link in active_links(store.state, "citation.depends", from_set=[cur]):
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
# Prompt rendering + Sonnet invocation

def _format_upstream_sigs(upstream):
    """Render the upstream signatures block for the prompt."""
    if not upstream:
        return "(none — this is a foundation claim or has no upstream signatures)"
    return "\n\n".join(f"### {label}\n{sig}" for label, sig in upstream)


def _format_notation_primitives(primitives):
    """Render the notation primitives list for the prompt."""
    if not primitives:
        return "(none registered)"
    return "\n".join(f"- `{p}`" for p in primitives)


def _render_prompt(claim_md_content, notation_primitives, upstream_sigs,
                   existing_signature):
    template = read_file(PROMPT_TEMPLATE)
    return (template
            .replace("{{claim_md_content}}", claim_md_content)
            .replace("{{notation_primitives}}",
                     _format_notation_primitives(notation_primitives))
            .replace("{{upstream_signatures}}",
                     _format_upstream_sigs(upstream_sigs))
            .replace("{{existing_signature}}",
                     existing_signature or "(none)"))


def _call_sonnet(prompt, model):
    text, elapsed = invoke_claude(
        prompt, model=model, effort="high", tools="Read",
    )
    if not text:
        raise RuntimeError(f"Sonnet returned empty after {elapsed:.0f}s")
    return text, elapsed


# ---------------------------------------------------------------------------
# Response parsing

def _parse_response(text):
    """Parse Sonnet's INTRODUCES / REMOVES YAML output. Returns
    (introduces, removes) — lists of dicts. Fails loudly on malformed
    output."""
    text = text.strip()
    intro_idx = text.find("INTRODUCES:")
    rem_idx = text.find("REMOVES:")
    if intro_idx < 0:
        raise ValueError(f"missing INTRODUCES: header:\n{text}")
    if rem_idx < 0:
        raise ValueError(f"missing REMOVES: header:\n{text}")
    if rem_idx < intro_idx:
        raise ValueError("REMOVES appears before INTRODUCES")

    intro_yaml = strip_code_fence(
        text[intro_idx + len("INTRODUCES:"):rem_idx].strip()
    )
    rem_yaml = strip_code_fence(
        text[rem_idx + len("REMOVES:"):].strip()
    )

    try:
        introduces = yaml.safe_load(intro_yaml) or []
        removes = yaml.safe_load(rem_yaml) or []
    except yaml.YAMLError as e:
        raise ValueError(
            f"YAML parse error: {e}\n"
            f"--- INTRODUCES ---\n{intro_yaml}\n"
            f"--- REMOVES ---\n{rem_yaml}"
        )

    if not isinstance(introduces, list):
        raise ValueError(
            f"INTRODUCES must be a list, got "
            f"{type(introduces).__name__}: {introduces!r}\n"
            f"--- raw block ---\n{intro_yaml}"
        )
    if not isinstance(removes, list):
        raise ValueError(
            f"REMOVES must be a list, got "
            f"{type(removes).__name__}: {removes!r}\n"
            f"--- raw block ---\n{rem_yaml}"
        )

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
        # Stash the parsed symbol on the entry so callers don't re-parse.
        entry["symbol"] = m.group(1)

    for entry in removes:
        if not isinstance(entry, dict):
            raise ValueError(f"REMOVES entry not a dict: {entry}")
        for field in ("symbol", "reason"):
            if field not in entry:
                raise ValueError(f"REMOVES entry missing {field!r}: {entry}")

    return introduces, removes


# ---------------------------------------------------------------------------
# Sidecar manipulation

def _existing_sidecar_bullets(claim_dir, claim_label):
    """Return [(symbol, bullet_line), ...] from the existing sidecar.

    The bullet_line is the complete `- \`<sym>\` — <role>` line as
    written. We index by symbol so adds/removes can target by symbol;
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


def _render_sidecar(symbol_bullet_pairs):
    """Render the signature sidecar markdown from a list of
    (symbol, bullet_line) pairs. The bullet_line is written verbatim."""
    if not symbol_bullet_pairs:
        return ""
    return "\n".join(b for _, b in symbol_bullet_pairs) + "\n"


# ---------------------------------------------------------------------------
# Resolve doc persistence

def _next_run_num(asn_label, claim_label):
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


def _persist_resolve_doc(asn_label, claim_label, sonnet_output, model):
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
        print(f"  {claim_label}.md not found at {claim_md_full}", file=sys.stderr)
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    claim_md_content = claim_md_full.read_text()
    existing_signature = _claim_signature_text(claim_dir, claim_label)

    store = Store(LATTICE)
    label_index = build_cross_asn_label_index(store)
    upstream_sigs = _transitive_dep_signatures(
        store, claim_md_rel, label_index, asn_label,
    )
    notation_primitives = read_notation(store)

    prompt = _render_prompt(
        claim_md_content, notation_primitives, upstream_sigs, existing_signature,
    )

    print(f"  [SIG-RESOLVE] {asn_label}/{claim_label} ({model})...",
          end="", file=sys.stderr, flush=True)
    text, elapsed = _call_sonnet(prompt, model=model)
    print(f" ({elapsed:.0f}s)", file=sys.stderr)

    introduces, removes = _parse_response(text)

    if not introduces and not removes:
        # No changes — sidecar already reflects truth (whether populated
        # or absent). No write, no resolve doc, no commit.
        print(f"  [SIG-RESOLVE] {claim_label}: no changes",
              file=sys.stderr)
        return "ok"

    # Compute new sidecar content from existing + introduces - removes.
    # Each entry is (symbol, full_bullet_line). Symbol is the key for
    # add/remove; the bullet is what gets written verbatim.
    existing = _existing_sidecar_bullets(claim_dir, claim_label)
    bullets_by_symbol = dict(existing)

    for entry in removes:
        bullets_by_symbol.pop(entry["symbol"], None)

    for entry in introduces:
        bullets_by_symbol[entry["symbol"]] = entry["bullet"]

    new_pairs = [(s, bullets_by_symbol[s]) for s in bullets_by_symbol]
    new_sidecar_text = _render_sidecar(new_pairs)

    # If sidecar would be empty after removes, write empty (the sidecar
    # file is allowed to be empty; the substrate link stays).
    store = Store(LATTICE)
    emit_attribute(store, claim_md_rel, "signature", new_sidecar_text.rstrip())

    resolve_path, run_num = _persist_resolve_doc(
        asn_label, claim_label, text, model,
    )

    n_intro = len(introduces)
    n_rem = len(removes)
    print(f"  [SIG-RESOLVE] {claim_label}: {n_intro} introduced, "
          f"{n_rem} removed, run {run_num}", file=sys.stderr)

    step_commit_asn(
        asn_num,
        hint=(f"signature-resolve(asn): ASN-{asn_num:04d}/{claim_label} — "
              f"{n_intro} introduced, {n_rem} removed"),
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
    print(f"\n  [SIG-RESOLVE-SWEEP] {asn_label} — {len(labels)} claims",
          file=sys.stderr)

    for label in labels:
        run_resolve(asn_num, label, model=model)

    return "ok"
