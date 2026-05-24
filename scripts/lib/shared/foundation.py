"""Load foundation ASN statements for injection into prompts.

Reads metadata via `load_claim_metadata` (substrate-sourced — name from
the substrate name link, summary from the description sidecar) and the
Formal Contract section from each claim's .md.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.lattice.labels import extract_label_digits, format_label
from lib.shared.paths import WORKSPACE, CLAIM_DIR, LATTICE
from lib.shared.claim_files import build_label_index, load_claim_metadata


def find_extensions(base_id):
    """Find all ASNs that extend a given base ASN.

    Reverse-walks `extends` substrate links targeting the base note's
    address; resolves each from-side note path to an ASN number.
    Returns sorted list of ASN ids.
    """
    from lib.protocols.febe.session import open_session
    from lib.shared.common import find_asn
    base_path, _ = find_asn(str(base_id))
    if base_path is None:
        return []
    base_rel = str(base_path.relative_to(WORKSPACE))
    extensions = []
    with open_session(LATTICE) as session:
        base_addr = session.get_addr_for_path(base_rel)
        if base_addr is None:
            return []
        for link in session.active_links("extends", to_set=[base_addr]):
            if not link.from_set:
                continue
            ext_path = session.get_path_for_addr(link.from_set[0])
            if ext_path is None:
                continue
            digits = extract_label_digits(ext_path)
            if digits:
                extensions.append(int(digits))
    return sorted(extensions)


def _extract_formal_contract(md_text):
    """Extract *Formal Contract:* section from .md text."""
    marker = "*Formal Contract:*"
    idx = md_text.find(marker)
    if idx == -1:
        return ""
    return md_text[idx:].strip()


def _load_claim_statement(dep_asn_num, label):
    """Load one claim's foundation statement from per-claim files.

    Returns formatted section text or None if not found.
    """
    asn_label = format_label(dep_asn_num)
    claim_dir = CLAIM_DIR / asn_label
    if not claim_dir.exists():
        return None

    meta = load_claim_metadata(claim_dir, label=label)
    if not meta or not meta.get("summary"):
        return None

    label_index = build_label_index(claim_dir)
    stem = label_index.get(label)
    if not stem:
        return None

    md_path = claim_dir / f"{stem}.md"
    if not md_path.exists():
        return None

    contract = _extract_formal_contract(md_path.read_text())
    name = meta.get("name", label)
    summary = meta["summary"]

    section = f"## {label} — {name}\n\n{summary}"
    if contract:
        section += f"\n\n{contract}"
    return section


def _dep_ids_with_extensions(asn_id, dep_ids=None):
    """Get all dependency ASN IDs including extensions.

    `dep_ids` must be supplied (sourced from substrate citations on the
    relevant doc — note md, claim files aggregate, or inquiry md). The
    manifest depends: field no longer exists post-Phase-2; callers
    should route through `load_foundation_for_note` /
    `load_foundation_for_claim_asn` which derive dep_ids from substrate.
    """
    if dep_ids is None:
        dep_ids = []
    all_ids = []
    for dep_id in dep_ids:
        all_ids.append(dep_id)
        for ext_id in find_extensions(dep_id):
            if ext_id != asn_id:
                all_ids.append(ext_id)
    return all_ids


def load_foundation_statements(asn_id, dep_ids=None):
    """Load all foundation statements from per-claim files.

    Reads substrate-sourced summaries (description sidecars) + .md
    formal contracts for every claim in each dependency ASN. Errors if
    summaries are missing.

    `dep_ids` overrides the manifest `depends:` read — note-side
    callers pass substrate-derived ids via `note_dep_asn_ids`; claim-side
    callers omit and the manifest is consulted (legacy path).
    """
    all_dep_ids = _dep_ids_with_extensions(asn_id, dep_ids=dep_ids)
    if not all_dep_ids:
        return ""

    sections = []
    for dep_id in all_dep_ids:
        asn_label = format_label(dep_id)
        claim_dir = CLAIM_DIR / asn_label
        if not claim_dir.exists():
            print(f"  [ERROR] No claim doc dir for {asn_label}",
                  file=sys.stderr)
            continue

        all_meta = load_claim_metadata(claim_dir)
        if not all_meta:
            print(f"  [ERROR] No claim metadata for {asn_label}",
                  file=sys.stderr)
            continue

        missing = [l for l, m in all_meta.items() if not m.get("summary")]
        if missing:
            print(f"  [ERROR] {asn_label} missing summaries for "
                  f"{len(missing)} claims — "
                  f"run: python scripts/summarize.py {dep_id}",
                  file=sys.stderr)
            sys.exit(1)

        for label in all_meta:
            stmt = _load_claim_statement(dep_id, label)
            if stmt:
                sections.append(stmt)

    return "\n\n---\n\n".join(sections)


def load_foundation_for_note(asn_path, asn_id):
    """Load foundation statements for a note, sourcing dep ASN ids from
    substrate citations on the note md.

    For each dep ASN: walk `note → statements → supersession_head`
    and read the resulting doc. When the dep has been derived, the
    chain head is the claims.statements aggregate; when it hasn't,
    the chain head is the original operator-drafted statements
    sidecar. The substrate's supersession chain routes between the
    two without the loader needing to distinguish.

    Falls back to an empty string when the note has no citations.
    """
    from lib.lattice.labels import note_dep_asn_ids
    from lib.lattice.render import read_doc
    from lib.predicates import latest_doc_head, statements_sidecar_of
    from lib.protocols.febe.session import open_session
    from lib.shared.common import find_asn
    from lib.shared.paths import LATTICE, WORKSPACE
    note_rel = str(asn_path.resolve().relative_to(Path(WORKSPACE).resolve()))
    with open_session(LATTICE) as session:
        store = session.store
        note_addr = store.path_to_addr.get(note_rel)
        if note_addr is None:
            return ""
        dep_ids = note_dep_asn_ids(store, note_addr)

        # Print the load plan up front so the operator can see — at fire
        # time — exactly which deps will surface in the foundation block.
        # Retired deps are already filtered out at note_dep_asn_ids; this
        # log line is the positive complement to the skip warnings below.
        if dep_ids:
            import sys
            asn_label = format_label(asn_id)
            dep_labels = ", ".join(f"ASN-{d:04d}" for d in dep_ids)
            print(
                f"  [FOUNDATION] {asn_label}: loading {len(dep_ids)} deps "
                f"[{dep_labels}]",
                file=sys.stderr,
            )

        sections = []
        skipped = []
        for dep_id in dep_ids:
            dep_path, _ = find_asn(str(dep_id))
            if dep_path is None:
                skipped.append((dep_id, "no on-disk note file"))
                continue
            dep_rel = str(
                dep_path.resolve().relative_to(
                    Path(WORKSPACE).resolve(),
                ),
            )
            dep_note_addr = store.path_to_addr.get(dep_rel)
            if dep_note_addr is None:
                skipped.append((dep_id, "note not path-registered"))
                continue
            sidecar = statements_sidecar_of(session, dep_note_addr)
            if sidecar is None:
                skipped.append((dep_id, "no statements sidecar"))
                continue
            # Substrate walk: latest_doc_head crosses the sidecar →
            # aggregate bridge (if derived) and normalizes any version
            # markers in the supersession chain back to their identity
            # address — version markers carry no file, so reading the
            # raw supersession_head can drop a dep silently when the
            # sidecar has been register_version'd but not decomposed.
            head = latest_doc_head(session, sidecar)
            sections.append(read_doc(session, head))

        # Loader-side coverage assertion. Silent skips here are how the
        # foundation-loader bug of 2026-05-23 went undetected — ASN-0047
        # disappeared from the prompt and the reviewer hallucinated a
        # false finding. Surface every skip at fire time so the operator
        # sees it in the runner log; the operator's downstream diagnostic
        # `scripts/diagnostics/foundation_coverage.py` walks the whole
        # lattice with the same logic for on-demand audits.
        if skipped:
            import sys
            asn_label = format_label(asn_id)
            for dep_id, reason in skipped:
                print(
                    f"  [FOUNDATION] {asn_label}: dep "
                    f"ASN-{dep_id:04d} unresolvable — {reason}",
                    file=sys.stderr,
                )
    return "\n\n".join(sections)


def load_foundation_for_claim_asn(asn_id):
    """Load foundation statements for a claim ASN, sourcing dep ASN ids
    from per-claim substrate citations aggregated up to ASN granularity.

    Parallels `load_foundation_for_note`. The claim-side aggregation is
    the union of cross-ASN citations sourced from any claim md in this
    ASN's docuverse claim directory.
    """
    from lib.lattice.labels import aggregate_asn_deps
    from lib.protocols.febe.session import open_session
    from lib.shared.paths import LATTICE
    asn_label = format_label(asn_id)
    with open_session(LATTICE) as session:
        store = session.store  # for emit_* (Pass 2 will migrate)
        dep_ids = aggregate_asn_deps(store, asn_label)
    return load_foundation_statements(asn_id, dep_ids=dep_ids)


def claim_asn_dep_ids(asn_id):
    """Substrate-aggregated dep ASN ids for a claim ASN.

    Standalone form for callers that need the dep id list without the
    full foundation text (e.g., load_foundation_for_labels which takes
    labels separately).
    """
    from lib.lattice.labels import aggregate_asn_deps
    from lib.protocols.febe.session import open_session
    from lib.shared.paths import LATTICE
    asn_label = format_label(asn_id)
    with open_session(LATTICE) as session:
        store = session.store  # for emit_* (Pass 2 will migrate)
        return aggregate_asn_deps(store, asn_label)


def load_foundation_for_labels(asn_id, labels, dep_ids=None):
    """Load foundation statements for specific labels from per-claim files.

    Reads the substrate-sourced summary + .md formal contract for each
    label. Warns if a label is not found in any dependency ASN.

    `dep_ids` override behaves the same as in `load_foundation_statements`.
    """
    if not labels:
        return ""

    all_dep_ids = _dep_ids_with_extensions(asn_id, dep_ids=dep_ids)
    if not all_dep_ids:
        return ""

    sections = []
    for label in labels:
        found = False
        for dep_id in all_dep_ids:
            stmt = _load_claim_statement(dep_id, label)
            if stmt:
                sections.append(stmt)
                found = True
                break
        if not found:
            print(f"  [WARNING] Foundation label '{label}' not found — "
                  f"run: python scripts/summarize.py on dependency",
                  file=sys.stderr)

    return "\n\n---\n\n".join(sections)
