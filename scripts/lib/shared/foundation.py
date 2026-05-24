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
    should route through `load_foundation` (note-side) /
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


def load_foundation_for_claim_asn(asn_id):
    """Load foundation statements for a claim ASN, sourcing dep ASN ids
    from per-claim substrate citations aggregated up to ASN granularity.

    Parallels `load_foundation` (note-side). The claim-side aggregation is
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


# ─────────────────────────────────────────────────────────────────────
# New foundation loader (substrate-only, inquiry-emit, hard-fail).
#
# Reads inquiry frontmatter `depends:` as the declarative source,
# queries substrate `citation.depends` from the inquiry address,
# walks substrate for sidecar + supersession_head, reads the
# resolved file. Falls back to note-side substrate citations for
# hand-authored protocol notes with no inquiry file (LEGACY path,
# logged to stderr).
#
# Raises `FoundationError` on any failure — never returns `""`
# except when `depends: []` is declared (legitimate foundation ASN).
# ─────────────────────────────────────────────────────────────────────


class FoundationError(Exception):
    """Foundation loading failed.

    Always raised with a precise message naming the ASN and the
    failing layer (input / spec / resolution / output). Never caught
    silently — callers should let it propagate so the runner aborts
    the fire and surfaces the failure to the operator.
    """


def _validate_asn_id(asn_id) -> int:
    """Layer 1 gate: caller-provided asn_id is a positive int."""
    if not isinstance(asn_id, int) or isinstance(asn_id, bool):
        raise FoundationError(
            f"asn_id must be int, got {type(asn_id).__name__}: {asn_id!r}",
        )
    if asn_id <= 0:
        raise FoundationError(f"asn_id must be positive, got {asn_id}")
    return asn_id


def _validate_dep_ids(parent_id: int, raw_list) -> list[int]:
    """Layer 2 gate: each dep id in the declared list is a positive,
    non-self int. Accepts int or numeric string; rejects empty strings,
    None, floats, and self-references. Returns a sorted unique list."""
    if not isinstance(raw_list, list):
        raise FoundationError(
            f"ASN-{parent_id:04d} `depends:` must be a list, "
            f"got {type(raw_list).__name__}: {raw_list!r}",
        )
    out: set[int] = set()
    for raw in raw_list:
        if isinstance(raw, bool) or raw is None:
            raise FoundationError(
                f"ASN-{parent_id:04d} `depends:` contains invalid entry "
                f"{raw!r}",
            )
        if isinstance(raw, str):
            stripped = raw.strip()
            if not stripped:
                raise FoundationError(
                    f"ASN-{parent_id:04d} `depends:` contains empty string",
                )
            try:
                n = int(stripped)
            except ValueError:
                raise FoundationError(
                    f"ASN-{parent_id:04d} `depends:` entry {raw!r} "
                    f"is not numeric",
                )
        elif isinstance(raw, int):
            n = raw
        else:
            raise FoundationError(
                f"ASN-{parent_id:04d} `depends:` entry has unsupported "
                f"type {type(raw).__name__}: {raw!r}",
            )
        if n <= 0:
            raise FoundationError(
                f"ASN-{parent_id:04d} `depends:` entry {n} is non-positive",
            )
        if n == parent_id:
            raise FoundationError(
                f"ASN-{parent_id:04d} `depends:` is self-referential",
            )
        out.add(n)
    return sorted(out)


def _read_inquiry_depends(asn_id: int) -> list[int]:
    """Layer 2 gate (continued): read inquiry frontmatter, return the
    validated dep list. Raises if the inquiry is missing or has no
    `depends:` key."""
    from lib.shared.frontmatter import read_doc_with_frontmatter
    from lib.shared.paths import inquiry_doc_path

    inq_path = inquiry_doc_path(asn_id)
    if not inq_path.exists():
        raise FoundationError(
            f"ASN-{asn_id:04d}: inquiry file missing at {inq_path}",
        )
    try:
        fm, _body = read_doc_with_frontmatter(inq_path)
    except Exception as e:
        raise FoundationError(
            f"ASN-{asn_id:04d}: cannot read inquiry frontmatter: "
            f"{type(e).__name__}: {e}",
        )
    if fm is None:
        raise FoundationError(
            f"ASN-{asn_id:04d}: inquiry has no frontmatter ({inq_path})",
        )
    if "depends" not in fm:
        raise FoundationError(
            f"ASN-{asn_id:04d}: inquiry frontmatter missing `depends:` "
            f"key ({inq_path}). Add `depends: []` for foundation ASNs.",
        )
    raw = fm["depends"] if fm["depends"] is not None else []
    return _validate_dep_ids(asn_id, raw)


def _resolve_dep_to_file(session, parent_id: int, dep_id: int) -> tuple:
    """Layer 3 gate: walk substrate for one dep.

    Returns `(path, content)` for the dep's statements file (sidecar
    or supersession-resolved aggregate). Raises on any failure.
    """
    from lib.predicates import latest_doc_head, statements_sidecar_of
    from lib.backend.predicates import active_links
    from lib.shared.common import find_asn
    from lib.shared.paths import WORKSPACE

    store = session.store
    label = f"ASN-{dep_id:04d}"

    dep_path, _ = find_asn(str(dep_id))
    if dep_path is None:
        raise FoundationError(
            f"ASN-{parent_id:04d} declares dep {label} but no note "
            f"file exists on disk",
        )
    dep_rel = str(dep_path.resolve().relative_to(Path(WORKSPACE).resolve()))
    dep_note_addr = store.path_to_addr.get(dep_rel)
    if dep_note_addr is None:
        raise FoundationError(
            f"ASN-{parent_id:04d} declares dep {label}: note file "
            f"{dep_rel} is not path-registered in substrate",
        )

    if active_links(store.state, "retired", to_set=[dep_note_addr]):
        raise FoundationError(
            f"ASN-{parent_id:04d} declares dep {label} which is retired",
        )

    sidecar = statements_sidecar_of(session, dep_note_addr)
    if sidecar is None:
        raise FoundationError(
            f"ASN-{parent_id:04d} declares dep {label} but its note "
            f"has no statements sidecar",
        )

    head = latest_doc_head(session, sidecar)
    head_path_rel = store.path_for_addr(head)
    if head_path_rel is None:
        raise FoundationError(
            f"ASN-{parent_id:04d} dep {label}: supersession_head "
            f"{head} has no registered path",
        )

    head_path = Path(WORKSPACE) / head_path_rel
    if not head_path.exists():
        raise FoundationError(
            f"ASN-{parent_id:04d} dep {label}: statements file "
            f"{head_path} does not exist on disk",
        )

    content = head_path.read_text()
    if not content.strip():
        raise FoundationError(
            f"ASN-{parent_id:04d} dep {label}: statements file "
            f"{head_path} is empty",
        )
    return (head_path_rel, content)


def _query_inquiry_deps(session, asn_id: int) -> list[int]:
    """Layer 2 gate: substrate must declare deps matching frontmatter.

    Queries active `citation.depends` from the inquiry address,
    iterating every link's `to_set` (handles both fan-out and
    one-per-target shapes). Returns sorted unique dep ASN ids.
    """
    from lib.backend.predicates import active_links
    from lib.lattice.labels import label_pattern
    from lib.shared.paths import WORKSPACE, inquiry_doc_path

    store = session.store
    inq_path = inquiry_doc_path(asn_id)
    inq_rel = str(inq_path.resolve().relative_to(Path(WORKSPACE).resolve()))
    inq_addr = store.path_to_addr.get(inq_rel)
    if inq_addr is None:
        raise FoundationError(
            f"ASN-{asn_id:04d}: inquiry {inq_rel} not path-registered "
            f"in substrate",
        )

    pattern = label_pattern()
    seen: set[int] = set()
    for link in active_links(
        store.state, "citation.depends", from_set=[inq_addr],
    ):
        for target in link.to_set:
            tpath = store.path_for_addr(target)
            if tpath is None:
                continue
            m = pattern.search(tpath)
            if not m:
                continue
            seen.add(int(m.group(1)))
    return sorted(seen)


def load_foundation(asn_id: int) -> str:
    """Load foundation statements for an ASN by id (new contract).

    Reads `depends:` from the ASN's inquiry frontmatter, validates
    substrate citation.depends matches, resolves each dep through
    substrate (note → sidecar → supersession_head → path), reads each
    file, and returns the concatenated prose in id-sorted order.

    Raises FoundationError (a subclass of Exception) on any failure:
      - asn_id is not a positive int
      - inquiry file missing or malformed
      - `depends:` field missing from frontmatter
      - any dep id invalid (non-int, non-positive, self-ref, empty)
      - substrate dep set does not match frontmatter declaration
      - any dep's note file or substrate registration missing
      - any dep is retired
      - any dep's statements sidecar missing
      - any dep's resolved file missing or empty

    Returns `""` ONLY when `depends: []` is declared (legitimate
    foundation-ASN case). Every other code path either returns
    non-empty content or raises.
    """
    from lib.protocols.febe.session import open_session
    from lib.shared.paths import LATTICE

    _validate_asn_id(asn_id)

    with open_session(LATTICE) as session:
        # Layer 2 — declarative source (inquiry frontmatter; falls back
        # to note-side substrate for hand-authored protocol notes).
        declared = _resolve_declared_deps(session, asn_id)
        if not declared:
            return ""

        # Layer 3 — per-dep resolution
        sections = []
        for dep_id in declared:
            _path, content = _resolve_dep_to_file(session, asn_id, dep_id)
            sections.append(content)

    # Layer 4 — output gate
    result = "\n\n".join(sections)
    if not result.strip():
        # Defensive — unreachable given non-empty declared + per-dep
        # non-empty check above, but guards against future regressions
        # if the per-dep check is ever loosened.
        raise FoundationError(
            f"ASN-{asn_id:04d}: foundation resolution produced empty "
            f"result despite {len(declared)} declared deps",
        )
    return result


def _resolve_declared_deps(session, asn_id: int) -> list[int]:
    """Determine the declared dep list for an ASN.

    Primary path: inquiry frontmatter declares `depends:` and the
    substrate citation.depends mirror must match it. This is the
    canonical convention for inquiry-driven ASNs.

    LEGACY fallback: when no inquiry file exists (hand-authored
    protocol notes), reads citation.depends directly from the note
    address — substrate IS the spec in this case, no frontmatter to
    validate against. Logged to stderr so the operator sees fallback
    usage; should disappear once protocol notes are brought under a
    declarative spec convention.

    Raises FoundationError when neither path can resolve.
    """
    from lib.shared.paths import inquiry_doc_path

    inq_path = inquiry_doc_path(asn_id)
    if inq_path.exists():
        declared = _read_inquiry_depends(asn_id)
        if declared:
            substrate_deps = _query_inquiry_deps(session, asn_id)
            if set(substrate_deps) != set(declared):
                missing_in_substrate = sorted(set(declared) - set(substrate_deps))
                extra_in_substrate = sorted(set(substrate_deps) - set(declared))
                raise FoundationError(
                    f"ASN-{asn_id:04d}: substrate citation.depends "
                    f"{substrate_deps} does not match frontmatter "
                    f"{declared}. "
                    f"Missing in substrate: {missing_in_substrate}. "
                    f"Extra in substrate: {extra_in_substrate}. "
                    f"Run `asn-sync-deps {asn_id}` to reconcile.",
                )
        return declared

    # LEGACY fallback — hand-authored protocol note
    deps = _read_note_side_depends(session, asn_id)
    print(
        f"  [FOUNDATION] {format_label(asn_id)}: using LEGACY note-side "
        f"substrate (no inquiry file); {len(deps)} dep(s) → "
        f"{[f'ASN-{d:04d}' for d in deps]}",
        file=sys.stderr,
    )
    return deps


def _read_note_side_depends(session, asn_id: int) -> list[int]:
    """Read citation.depends directly from the note address.

    Used by the LEGACY fallback path in `_resolve_declared_deps`. The
    note address is the source-of-truth for dep declarations under the
    pre-inquiry convention used by hand-authored protocol notes.

    The substrate-returned list is well-formed by construction
    (note_dep_asn_ids filters retired + self-refs, returns sorted
    positive ints), but we still route it through `_validate_dep_ids`
    as defense-in-depth: same gate the inquiry path uses, applied
    uniformly so future regressions in note_dep_asn_ids (e.g., looser
    filtering) can't slip invalid dep ids past the loader.
    """
    from lib.lattice.labels import note_dep_asn_ids
    from lib.shared.paths import NOTE_DIR, WORKSPACE

    label = format_label(asn_id)
    note_prefix = str(NOTE_DIR.relative_to(WORKSPACE)) + f"/{label}-"
    note_addr = None
    for path, addr in session.store.path_to_addr.items():
        if path.startswith(note_prefix) and not path.endswith(".statements.md"):
            note_addr = addr
            break
    if note_addr is None:
        raise FoundationError(
            f"ASN-{asn_id:04d}: no inquiry file AND no note in substrate "
            f"— nothing to load",
        )
    raw_deps = note_dep_asn_ids(session.store, note_addr)
    return _validate_dep_ids(asn_id, raw_deps)
