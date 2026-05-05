"""Shared lattice path constants for all pipeline scripts."""

import os
import re
from pathlib import Path

import yaml

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

# Lattice identity — parameterized via LATTICE env var, defaults to "xanadu".
# A second lattice (e.g. materials) switches every lattice-scoped path at once.
LATTICE_NAME = os.environ.get("LATTICE", "xanadu")
LATTICE = WORKSPACE / "lattices" / LATTICE_NAME
CHANNELS_DIR = WORKSPACE / "channels"

# Pipeline-stage prompts tier — shared defaults plus per-lattice overrides.
# Resolver prefers lattice-specific overrides.
SHARED_PROMPTS = WORKSPACE / "prompts" / "shared"
LATTICE_PROMPTS = WORKSPACE / "prompts" / LATTICE_NAME


def prompt_path(subpath):
    """Resolve a prompt subpath to a Path.

    Prefers a lattice-specific override under LATTICE_PROMPTS if it exists;
    otherwise returns the shared path under SHARED_PROMPTS. Neither file is
    required to exist — callers handle missing-file errors at read time.
    """
    lattice = LATTICE_PROMPTS / subpath
    if lattice.exists():
        return lattice
    return SHARED_PROMPTS / subpath

# Discovery stage
CONSULTATIONS_DIR = LATTICE / "_docuverse" / "documents" / "consultation"
PATCHES_DIR = LATTICE / "discovery" / "patches"

# Per-lattice files
VOCABULARY = LATTICE / "vocabulary.md"
LATTICE_CONFIG = LATTICE / "config.yaml"

# Verification stage
ALLOY_DIR = LATTICE / "verification" / "alloy"
DAFNY_DIR = LATTICE / "verification" / "dafny"
PROOFS_DIR = LATTICE / "verification" / "proofs"                     # promoted/curated
PROOFS_STAGING_DIR = LATTICE / "verification" / "proofs-staging"     # Level 2 builds, pre-curation
PROOF_IMPORTS = PROOFS_STAGING_DIR / "imports.md"

# Implementation stage (Xanadu-specific — reference Rust impl)
EXAMPLES_DIR = LATTICE / "implementation" / "examples"
TEST_CASES_DIR = LATTICE / "implementation" / "test-cases"
TRANSLATION_DIR = LATTICE / "implementation" / "translation"

# Per-note manifests (metadata, statements, deps, issues)
MANIFESTS_DIR = LATTICE / "manifests"

# Requirements (Nelson feature extraction)
REQUIREMENTS_DIR = LATTICE / "requirements"

# Operational
USAGE_LOG = LATTICE / "usage-log.jsonl"

# The docuverse — Nelson's term for the universe of typed, linked
# documents. The substrate (links.jsonl + index.db) plus all
# substrate-classified documents live here.
DOCUVERSE_DIR = LATTICE / "_docuverse"
DOCUVERSE_LOG = DOCUVERSE_DIR / "links.jsonl"
DOCUVERSE_INDEX = DOCUVERSE_DIR / "index.db"
# Substrate-classified documents live under _docuverse/documents/.
# Structural state (links.jsonl, index.db) sits alongside as a sibling.
DOCUVERSE_DOCS_DIR = DOCUVERSE_DIR / "documents"
RATIONALE_DIR = DOCUVERSE_DOCS_DIR / "rationale"
AGENT_DIR = DOCUVERSE_DOCS_DIR / "agent"
CAMPAIGN_DIR = DOCUVERSE_DOCS_DIR / "campaign"
INQUIRY_DIR = DOCUVERSE_DOCS_DIR / "inquiry"
NOTE_DIR = DOCUVERSE_DOCS_DIR / "note"
CLAIM_DIR = DOCUVERSE_DOCS_DIR / "claim"

# Loop work products. Sibling to _docuverse/. Holds artifacts produced
# by the convergence/decomposition loops that aren't themselves
# substrate-classified documents (scratch caches, intermediate state).
WORKSPACE_DIR = LATTICE / "_workspace"

# Aggregate review docs (classified by `review`). Split by inquiry-target
# kind so review numbering and substrate queries are scoped per kind.
CLAIM_REVIEWS_DIR = DOCUVERSE_DOCS_DIR / "review" / "claims"
NOTE_REVIEWS_DIR = DOCUVERSE_DOCS_DIR / "review" / "notes"
REVIEWS_DIR = NOTE_REVIEWS_DIR  # legacy alias, prefer NOTE_REVIEWS_DIR

# Per-finding decomposition outputs (classified by `finding`, related to
# their target by `comment.<kind>`). Each per-review subdirectory pairs
# with the matching aggregate doc by the shared `review-N` token.
CLAIM_FINDINGS_DIR = DOCUVERSE_DOCS_DIR / "finding" / "claims"
NOTE_FINDINGS_DIR = DOCUVERSE_DOCS_DIR / "finding" / "notes"

# Transclusion-rendered documents (tagged by `transclusion.<kind>`).
# The substrate path is a citizen address; no on-disk file is
# written — the registered renderer supplies content at read time.
TRANSCLUSION_DIR = DOCUVERSE_DOCS_DIR / "transclusion"


def transclusion_path(asn_label: str, kind: str) -> Path:
    """Lattice-relative path for a transclusion doc (no file on disk).

    Used as the path argument to `register_path` when emitting a
    transclusion; gives the doc a stable substrate address.
    """
    return TRANSCLUSION_DIR / asn_label / f"{kind}.md"


# Promotion reports (classified by `promotion.<kind>`). One doc per
# (source ASN, kind), where kind ∈ {out-of-scope, open-questions}.
# Holds the LLM's promote/decline verdicts plus rationale; re-runs
# overwrite. See docs/hypergraph-protocol/promotion.md.
PROMOTION_DIR = DOCUVERSE_DOCS_DIR / "promotion"


def promotion_doc_path(asn_num, kind: str) -> Path:
    """Lattice-relative path for a promotion report doc.

    Stable per (source ASN, kind) — re-running the same promotion
    overwrites the same path, keeping the substrate address constant.
    """
    return PROMOTION_DIR / f"ASN-{int(asn_num):04d}" / f"{kind}.md"


# Citation-resolve operation outputs (classified by `citation.resolve`).
# One doc per resolve run, named `<claim-label>-<run-N>.md` under the
# claim's ASN directory.
CITATION_RESOLVE_DIR = DOCUVERSE_DOCS_DIR / "citation-resolve" / "claims"

# Signature-resolve operation outputs. Same shape as CITATION_RESOLVE_DIR:
# one doc per resolve run, named `<claim-label>-<run-N>.md`.
SIGNATURE_RESOLVE_DIR = DOCUVERSE_DOCS_DIR / "signature-resolve" / "claims"

# Claim convergence workspace — caches and intermediate prose artifacts
# the convergence pipeline writes (per-ASN _contract-cache.json,
# _summary-cache.json, etc.). Workspace-shaped: regeneratable, not
# substrate citizens.
CLAIM_CONVERGENCE_DIR = WORKSPACE_DIR / "claim-convergence"

# Claim derivation audit trail (per-section content + LLM analyses).
# Derivation's intermediate state lives here; the per-claim outputs
# go to the docuverse (CLAIM_DIR) directly in D2.
CLAIM_DERIVATION_DIR = WORKSPACE_DIR / "claim-derivation"


def _findings_dir_for_kind(kind):
    if kind == "claim":
        return CLAIM_FINDINGS_DIR
    if kind == "note":
        return NOTE_FINDINGS_DIR
    raise ValueError(f"unknown findings kind: {kind!r}")


def _reviews_dir_for_kind(kind):
    if kind == "claim":
        return CLAIM_REVIEWS_DIR
    if kind == "note":
        return NOTE_REVIEWS_DIR
    raise ValueError(f"unknown review kind: {kind!r}")


def agent_doc_path(role):
    """Lattice-relative path to an agent doc by role name.

    The substrate identifies an agent by its doc address (lattice-relative
    string), so callers wiring up `XANADU_AGENT_DOC` or invoking `emit_agent`
    use this to get the canonical form.
    """
    return str((AGENT_DIR / f"{role}.md").relative_to(LATTICE))


def review_aggregate_path(asn_label, review_num, *, kind):
    """Path to a review event's aggregate doc under the docuverse review dir.

    `kind` selects the namespace: "claim" or "note". Returns the path
    `<reviews_dir>/<asn_label>/review-<n>.md`.
    """
    return _reviews_dir_for_kind(kind) / asn_label / f"review-{review_num}.md"


def claim_doc_path(asn_label, label):
    """Lattice-relative path to a claim's body markdown by (ASN, label).

    Returns the canonical convention path
    `_docuverse/documents/claim/<asn_label>/<label>.md` as a string.
    Pure construction — does not check whether the file exists. Suitable
    for both already-existing claims (the path is always conventional)
    and freshly-created ones the LLM has just written under the same
    convention.

    Used by the link-emit CLIs (cite, retract, classify, label, name,
    description) to translate their --label argument into the substrate
    address. Per the Xanadu-aligned design, callers pass labels rather
    than path strings; the path convention is the local-reference's
    way of mapping label-as-identity to a filesystem address.
    """
    return f"_docuverse/documents/claim/{asn_label}/{label}.md"


def note_dir(asn_num):
    """Per-note manifest directory."""
    return MANIFESTS_DIR / f"ASN-{int(asn_num):04d}"


def consultation_dir(asn):
    """Per-ASN consultation directory. Accepts int or ASN-NNNN label."""
    if isinstance(asn, str) and asn.startswith("ASN-"):
        return CONSULTATIONS_DIR / asn
    return CONSULTATIONS_DIR / f"ASN-{int(asn):04d}"


def claim_docs_dir(asn):
    """Per-ASN claim files directory under the substrate document store.

    Accepts int or ASN-NNNN label. Holds the per-claim body markdown plus
    `<stem>.{label,name,description}.md` sidecars. Reviews, caches, and
    structural section files stay alongside under
    `claim-convergence/<asn>/` (work products, not substrate-managed).
    """
    if isinstance(asn, str) and asn.startswith("ASN-"):
        return CLAIM_DIR / asn
    return CLAIM_DIR / f"ASN-{int(asn):04d}"


def note_yaml(asn_num):
    """Legacy path to a note's metadata YAML. Pre-Phase-2 inquiry refactor.
    Should not be referenced by new code — use inquiry_doc_path.
    """
    return note_dir(asn_num) / "note.yaml"


def inquiry_doc_path(asn_num):
    """Path to a substrate-managed inquiry doc (md + frontmatter)."""
    return INQUIRY_DIR / f"ASN-{int(asn_num):04d}.md"


def claim_statements(asn_num):
    """Lattice path to a note's `statements` attribute sidecar.

    The sidecar holds the LLM-extracted formal statements for the
    note. Lives next to the note doc under
    `_docuverse/documents/note/<note-stem>.statements.md`. Substrate-
    citizen; the note's outgoing `statements` link points at it.

    Reads at this path return the LLM-extracted content (which can
    be stale relative to current substrate state post-derivation).
    For up-to-date "what does this ASN say?" content, walk the
    note's `statements` link + supersession chain to the head and
    use `read_doc` instead — the head is the transclusion.claim-
    statements doc post-derivation.
    """
    from .common import find_asn
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return note_dir(asn_num) / "claim-statements.md"
    return asn_path.parent / f"{asn_path.stem}.statements.md"


def _review_sort_key(path):
    """Extract numeric review number for sorting. review-9 < review-13."""
    m = re.search(r"review-(\d+)\.md$", path.name)
    return int(m.group(1)) if m else 0


def sorted_reviews(asn_label, reviews_dir=None):
    """Return review files for an ASN, sorted by numeric review number."""
    d = reviews_dir or REVIEWS_DIR
    note_subdir = d / asn_label
    if not note_subdir.exists():
        return []
    return sorted(note_subdir.glob("review-*.md"), key=_review_sort_key)


def sanitize_filename(label, name):
    """Build a filename-safe string from label and name.

    E.g. ('T1', 'LexicographicOrder') -> 'T1-LexicographicOrder'
         ('TA1-strict', 'StrictOrderPreservation') -> 'TA1-strict-StrictOrderPreservation'
         ('Prefix ordering extension', 'PrefixOrderingExtension') -> 'PrefixOrderingExtension'
    """
    # If label is already a short code (T1, TA3, T10a, TA1-strict, etc.), use it
    if re.match(r"^[A-Z]+\w*(-\w+)?$", label):
        return re.sub(r"[^A-Za-z0-9_-]", "", f"{label}-{name}")
    # Multi-word label — just use name
    return re.sub(r"[^A-Za-z0-9_-]", "", name)


def find_review(asn_label, review_spec=None):
    """Find review file by spec. If review_spec is None, returns the latest review.

    Otherwise tries: literal path, REVIEWS_DIR/asn_label/{spec}.md, and
    REVIEWS_DIR/asn_label/{spec}. Returns None if not found.
    """
    if review_spec is None:
        reviews = sorted_reviews(asn_label)
        return reviews[-1] if reviews else None

    path = Path(review_spec)
    if path.exists():
        return path

    for candidate in (REVIEWS_DIR / asn_label / f"{review_spec}.md",
                      REVIEWS_DIR / asn_label / review_spec):
        if candidate.exists():
            return candidate
    return None


def next_review_number(asn_label, *, kind, reviews_dir=None):
    """Find the next review number for this ASN.

    `kind` selects the findings namespace ("claim" or "note"); numbering is
    independent per kind. Sources from two places, taking max+1 across both:
      1. Legacy review files (review-N.md) under `reviews_dir` if provided —
         caller-supplied path, typically `claim-convergence/<asn>/reviews/`.
         Not written by current code, but historical numbers are respected.
      2. Current review directories (review-N/) under the kind's findings dir.
    """
    nums = []

    # Legacy review files (numbered review-N.md). Caller passes the dir.
    if reviews_dir is not None and Path(reviews_dir).exists():
        for p in Path(reviews_dir).glob("review-*.md"):
            m = re.search(r"review-(\d+)\.md$", p.name)
            if m:
                nums.append(int(m.group(1)))

    # Current review directories (review-N/ under <kind findings>/asn).
    findings_subdir = _findings_dir_for_kind(kind) / asn_label
    if findings_subdir.exists():
        for p in findings_subdir.glob("review-*"):
            if not p.is_dir():
                continue
            m = re.search(r"review-(\d+)$", p.name)
            if m:
                nums.append(int(m.group(1)))

    return max(nums, default=0) + 1


def load_inquiry(asn_id):
    """Load inquiry frontmatter for an ASN. Returns dict or empty dict."""
    from lib.shared.frontmatter import read_doc_frontmatter
    return read_doc_frontmatter(inquiry_doc_path(asn_id))


def load_lattice_config():
    """Load the lattice-level config.yaml. Returns dict or empty dict."""
    try:
        with open(LATTICE_CONFIG) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def campaign_dir(name):
    """Path to a campaign's substrate-managed directory.

    Holds the descriptor (campaign.md with frontmatter + body) and the
    bridge vocabulary (vocabulary.md). Substrate emits a `campaign`
    classifier on the descriptor; inquiries link to it via the
    `campaign` link type.
    """
    return CAMPAIGN_DIR / name


def campaign_doc_path(name):
    """Path to a campaign's descriptor doc."""
    return campaign_dir(name) / "campaign.md"


def campaign_vocab(name):
    """Path to a campaign's bridge vocabulary."""
    return campaign_dir(name) / "vocabulary.md"


def load_channel_meta(channel_name):
    """Read and parse a channel's meta.yaml. Raises FileNotFoundError if
    the file is missing."""
    meta_path = CHANNELS_DIR / channel_name / "meta.yaml"
    try:
        return yaml.safe_load(meta_path.read_text()) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"channel meta.yaml not found: {meta_path}")


