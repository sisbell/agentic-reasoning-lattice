"""Citation Resolve — type each claim-label reference in a claim's prose.

For each claim in the ASN, Sonnet identifies label references in the
prose and types each as `depends` (claim's correctness rests on the
cited claim) or `forward` (claim names a downstream concept).

Per-claim outputs:
- .md edits: insert bullets in `*Depends:*` and `*Forward References:*`
  sections; remove bullets for retractions
- Substrate: `citation.depends` / `citation.forward` links, `retraction`
  links for invalidated classifications, `provenance.derivation` from the
  resolve doc to each emitted link, and `citation.resolve` classifier on
  the resolve doc itself
- Persisted resolve doc at
  `_docuverse/documents/citation-resolve/claims/<asn>/<claim>-<N>.md`
  (sequential N per claim; only written when changes were applied)
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.shared.paths import (
    LATTICE, CLAIM_DIR, CITATION_RESOLVE_DIR,
    prompt_path, claim_doc_path,
)
from lib.shared.common import (
    find_asn, build_label_index, read_file, invoke_claude,
    strip_code_fence, step_commit_asn,
)
from lib.store.store import Store, attributed_to
from lib.store.populate import build_cross_asn_label_index
from lib.store.queries import active_links
from lib.store.cite import emit_citation
from lib.store.retract import emit_retraction


PROMPT_TEMPLATE = prompt_path("claim-convergence/citation-resolve.md")

DEPENDS_HEADER = "- *Depends:*"
FORWARD_HEADER = "- *Forward References:*"


# ---------------------------------------------------------------------------
# Substrate queries

def _existing_classifications(store, claim_md_rel, label_index):
    """Return (depends_labels, forwards_labels) sourced from substrate."""
    rev_index = {p: l for l, p in label_index.items()}
    depends = []
    forwards = []
    for link in active_links(store, "citation.depends", from_set=[claim_md_rel]):
        if link["to_set"] and link["to_set"][0] in rev_index:
            depends.append(rev_index[link["to_set"][0]])
    for link in active_links(store, "citation.forward", from_set=[claim_md_rel]):
        if link["to_set"] and link["to_set"][0] in rev_index:
            forwards.append(rev_index[link["to_set"][0]])
    return sorted(depends), sorted(forwards)


# ---------------------------------------------------------------------------
# Prompt rendering + Sonnet invocation

def _format_label_list(labels):
    """Format label list as one-per-line bullets, or '(none)' if empty."""
    if not labels:
        return "(none)"
    return "\n".join(f"- {label}" for label in labels)


def _render_prompt(claim_md_content, claim_dir, claims_root, depends, forwards):
    template = read_file(PROMPT_TEMPLATE)
    return (template
            .replace("{{claim_md_content}}", claim_md_content)
            .replace("{{claim_dir}}", str(claim_dir))
            .replace("{{claims_root}}", str(claims_root))
            .replace("{{existing_depends}}", _format_label_list(depends))
            .replace("{{existing_forwards}}", _format_label_list(forwards)))


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
    """Parse Sonnet's CLASSIFICATIONS / RETRACTIONS YAML output.

    Returns (classifications, retractions) — lists of dicts. Fails loudly
    on malformed output.
    """
    text = text.strip()
    cls_idx = text.find("CLASSIFICATIONS:")
    ret_idx = text.find("RETRACTIONS:")
    if cls_idx < 0:
        raise ValueError(f"missing CLASSIFICATIONS: header in response:\n{text}")
    if ret_idx < 0:
        raise ValueError(f"missing RETRACTIONS: header in response:\n{text}")
    if ret_idx < cls_idx:
        raise ValueError("RETRACTIONS appears before CLASSIFICATIONS in response")

    cls_yaml = strip_code_fence(
        text[cls_idx + len("CLASSIFICATIONS:"):ret_idx].strip()
    )
    ret_yaml = strip_code_fence(
        text[ret_idx + len("RETRACTIONS:"):].strip()
    )

    try:
        classifications = yaml.safe_load(cls_yaml) or []
        retractions = yaml.safe_load(ret_yaml) or []
    except yaml.YAMLError as e:
        raise ValueError(
            f"YAML parse error: {e}\n"
            f"--- CLASSIFICATIONS ---\n{cls_yaml}\n"
            f"--- RETRACTIONS ---\n{ret_yaml}"
        )

    if not isinstance(classifications, list):
        raise ValueError(
            f"CLASSIFICATIONS must be a list, got "
            f"{type(classifications).__name__}: {classifications!r}\n"
            f"--- raw block ---\n{cls_yaml}"
        )
    if not isinstance(retractions, list):
        raise ValueError(
            f"RETRACTIONS must be a list, got "
            f"{type(retractions).__name__}: {retractions!r}\n"
            f"--- raw block ---\n{ret_yaml}"
        )

    for c in classifications:
        if not isinstance(c, dict):
            raise ValueError(f"classification entry not a dict: {c}")
        for field in ("label", "direction", "bullet"):
            if field not in c:
                raise ValueError(f"classification missing {field!r}: {c}")
        if c["direction"] not in ("depends", "forward"):
            raise ValueError(f"invalid direction in classification: {c}")

    for r in retractions:
        if not isinstance(r, dict):
            raise ValueError(f"retraction entry not a dict: {r}")
        for field in ("label", "direction"):
            if field not in r:
                raise ValueError(f"retraction missing {field!r}: {r}")
        if r["direction"] not in ("depends", "forward"):
            raise ValueError(f"invalid direction in retraction: {r}")

    return classifications, retractions


def _validate_labels(classifications, retractions, label_index):
    """Every emitted label must resolve in the cross-ASN label index."""
    for c in classifications:
        if c["label"] not in label_index:
            raise ValueError(
                f"unknown label in classification: {c['label']!r}"
            )
    for r in retractions:
        if r["label"] not in label_index:
            raise ValueError(
                f"unknown label in retraction: {r['label']!r}"
            )


# ---------------------------------------------------------------------------
# .md section editing

def _find_section(lines, header):
    """Locate a `- *<Field>:*` section.

    Returns (start_idx, last_bullet_idx) where:
    - start_idx is the line of the header itself
    - last_bullet_idx is the index of the last `  - ` sub-bullet (or
      start_idx itself if the section is empty so far)

    Returns None if the section header is not present.
    """
    for i, line in enumerate(lines):
        if line.strip() == header.strip():
            last_bullet_idx = i
            for j in range(i + 1, len(lines)):
                ln = lines[j]
                if ln.startswith("  - "):
                    last_bullet_idx = j
                elif ln.startswith("    ") or ln.strip() == "":
                    continue
                else:
                    break
            return (i, last_bullet_idx)
    return None


def _bullet_label(bullet_line):
    """Extract the label from a `  - LABEL ...` bullet line."""
    return bullet_line[4:].split(None, 1)[0]


def _apply_changes(claim_md_path, classifications, retractions):
    """Apply classifications (insert bullets) and retractions (remove
    bullets) to the claim's .md.

    Retractions are applied first (so a reclassify works correctly:
    retract old direction, insert new direction).
    """
    lines = claim_md_path.read_text().split("\n")

    for r in retractions:
        header = DEPENDS_HEADER if r["direction"] == "depends" else FORWARD_HEADER
        section = _find_section(lines, header)
        if section is None:
            raise ValueError(
                f"retraction target section {header!r} not in {claim_md_path}"
            )
        start_idx, last_bullet_idx = section
        removed = False
        for j in range(start_idx + 1, last_bullet_idx + 1):
            line = lines[j]
            if line.startswith("  - ") and _bullet_label(line) == r["label"]:
                del lines[j]
                removed = True
                break
        if not removed:
            raise ValueError(
                f"no bullet for {r['label']!r} in {header!r} of {claim_md_path}"
            )

    depends_to_add = [c for c in classifications if c["direction"] == "depends"]
    forwards_to_add = [c for c in classifications if c["direction"] == "forward"]

    if depends_to_add:
        section = _find_section(lines, DEPENDS_HEADER)
        if section is None:
            raise ValueError(
                f"no {DEPENDS_HEADER!r} section in {claim_md_path}; "
                f"cannot add depends bullets"
            )
        _, last_bullet_idx = section
        for c in reversed(depends_to_add):
            lines.insert(last_bullet_idx + 1, "  " + c["bullet"].lstrip())

    if forwards_to_add:
        section = _find_section(lines, FORWARD_HEADER)
        if section is None:
            depends_section = _find_section(lines, DEPENDS_HEADER)
            if depends_section is None:
                raise ValueError(
                    f"cannot create {FORWARD_HEADER!r}: no {DEPENDS_HEADER!r} "
                    f"to anchor it after in {claim_md_path}"
                )
            _, depends_last = depends_section
            new_block = [FORWARD_HEADER]
            for c in forwards_to_add:
                new_block.append("  " + c["bullet"].lstrip())
            for ln in reversed(new_block):
                lines.insert(depends_last + 1, ln)
        else:
            _, last_bullet_idx = section
            for c in reversed(forwards_to_add):
                lines.insert(last_bullet_idx + 1, "  " + c["bullet"].lstrip())

    claim_md_path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Resolve doc persistence

def _next_resolve_run(asn_label, claim_label):
    """Return the next sequential run number for this claim."""
    asn_dir = CITATION_RESOLVE_DIR / asn_label
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
    """Write the resolve doc with a small header + raw Sonnet output."""
    run_num = _next_resolve_run(asn_label, claim_label)
    asn_dir = CITATION_RESOLVE_DIR / asn_label
    asn_dir.mkdir(parents=True, exist_ok=True)
    path = asn_dir / f"{claim_label}-{run_num}.md"

    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    content = (
        f"# Citation Resolve — {asn_label}/{claim_label} — run {run_num}\n"
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
# Substrate emission

def _emit_substrate(store, claim_md_rel, classifications, retractions,
                    resolve_doc_rel, label_index):
    """Emit substrate links for one resolve operation.

    Order:
    1. `citation.resolve` classifier on the resolve doc
    2. `citation.depends` / `citation.forward` for each classification
    3. `retraction` for each retraction
    4. `provenance.derivation` from the resolve doc to each emitted
       citation/retraction link
    """
    store.make_link(
        from_set=[],
        to_set=[resolve_doc_rel],
        type_set=["citation.resolve"],
    )

    derivation_targets = []
    for c in classifications:
        link_id, _ = emit_citation(
            store, claim_md_rel, c["label"], label_index,
            direction=c["direction"],
        )
        derivation_targets.append(link_id)
    for r in retractions:
        link_id, _ = emit_retraction(
            store, claim_md_rel, r["label"], label_index,
            direction=r["direction"],
        )
        derivation_targets.append(link_id)

    for link_id in derivation_targets:
        store.make_link(
            from_set=[resolve_doc_rel],
            to_set=[link_id],
            type_set=["provenance.derivation"],
        )


# ---------------------------------------------------------------------------
# Entrypoints

@attributed_to("citation-resolve")
def run_classification(asn_num, claim_label, model="sonnet"):
    """Run citation-resolve on one claim. Returns "ok" on completion
    (no-op or applied), "failed" on error."""
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

    claim_md_content = claim_md_full.read_text()

    store = Store()
    try:
        label_index = build_cross_asn_label_index(store=store)
        depends, forwards = _existing_classifications(
            store, claim_md_rel, label_index,
        )
    finally:
        store.close()

    claim_dir = claim_md_full.parent
    claims_root = claim_dir.parent
    prompt = _render_prompt(
        claim_md_content, claim_dir, claims_root, depends, forwards,
    )

    print(f"  [RESOLVE] {asn_label}/{claim_label} ({model})...",
          end="", file=sys.stderr, flush=True)
    text, elapsed = _call_sonnet(prompt, model=model)
    print(f" ({elapsed:.0f}s)", file=sys.stderr)

    classifications, retractions = _parse_response(text)

    if not classifications and not retractions:
        print(f"  [RESOLVE] {claim_label}: no changes", file=sys.stderr)
        return "ok"

    store = Store()
    try:
        label_index = build_cross_asn_label_index(store=store)
        _validate_labels(classifications, retractions, label_index)
    finally:
        store.close()

    _apply_changes(claim_md_full, classifications, retractions)

    resolve_path, run_num = _persist_resolve_doc(
        asn_label, claim_label, text, model,
    )
    resolve_rel = str(resolve_path.relative_to(LATTICE))

    store = Store()
    try:
        label_index = build_cross_asn_label_index(store=store)
        _emit_substrate(
            store, claim_md_rel, classifications, retractions,
            resolve_rel, label_index,
        )
    finally:
        store.close()

    n_class = len(classifications)
    n_retr = len(retractions)
    print(f"  [RESOLVE] {claim_label}: {n_class} classifications, "
          f"{n_retr} retractions, run {run_num}", file=sys.stderr)

    step_commit_asn(
        asn_num,
        hint=(f"citation-resolve(asn): ASN-{asn_num:04d}/{claim_label} — "
              f"{n_class} classifications, {n_retr} retractions"),
    )
    return "ok"


@attributed_to("citation-resolve")
def run_sweep(asn_num, model="sonnet"):
    """Iterate every claim in the ASN; run citation-resolve on each."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return "failed"

    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        print(f"  {claim_dir} not found", file=sys.stderr)
        return "failed"

    labels = sorted(build_label_index(claim_dir).keys())
    print(f"\n  [RESOLVE-SWEEP] {asn_label} — {len(labels)} claims",
          file=sys.stderr)

    for label in labels:
        run_classification(asn_num, label, model=model)

    return "ok"
