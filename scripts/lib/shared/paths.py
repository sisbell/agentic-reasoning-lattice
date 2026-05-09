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
# Substrate-citizen patches. Split by target kind (note/claim) so that:
#   - the operator's directory choice declares intent (note vs claim)
#   - filenames don't collide between a note-targeted and claim-targeted
#     patch with the same stem
#   - substrate dirs are homogeneous in classifier subtype
# Operator drops a patch md into PATCH_INBOX_{NOTE,CLAIM} (workspace,
# gitignored); the matching agent promotes it to PATCH_{NOTE,CLAIM}_DIR
# (substrate citizen, committed) on fire.
PATCH_NOTE_DIR = DOCUVERSE_DOCS_DIR / "patch" / "note"
PATCH_CLAIM_DIR = DOCUVERSE_DOCS_DIR / "patch" / "claim"

# Substrate-citizen extract spec docs. Operator drops the spec md into
# EXTRACT_INBOX (workspace, gitignored); NoteExtractAgent promotes it to
# EXTRACT_DIR on fire. The spec doc carries the operator's scout-output:
# extract_from / create_note / absorb_into / claims plus rationale prose.
EXTRACT_DIR = DOCUVERSE_DOCS_DIR / "extract"

# Substrate-citizen absorb spec docs. Operator drops the spec md into
# ABSORB_INBOX (workspace, gitignored); NoteAbsorbAgent promotes it to
# ABSORB_DIR on fire. The spec doc carries the operator's scout-output:
# which extension to absorb plus rationale prose justifying readiness.
ABSORB_DIR = DOCUVERSE_DOCS_DIR / "absorb"

# Substrate-citizen clone spec docs. Operator drops the spec md into
# CLONE_INBOX (workspace, gitignored); NoteCloneAgent promotes it to
# CLONE_DIR on fire. The spec doc carries the operator's scout-output:
# clone_from / create_note plus rationale prose for the clone.
CLONE_DIR = DOCUVERSE_DOCS_DIR / "clone"

# Loop work products. Sibling to _docuverse/. Holds artifacts produced
# by the refinement/derivation loops that aren't themselves
# substrate-classified documents (scratch caches, intermediate state).
WORKSPACE_DIR = LATTICE / "_workspace"
PATCH_INBOX_NOTE = WORKSPACE_DIR / "patches" / "note"
PATCH_INBOX_CLAIM = WORKSPACE_DIR / "patches" / "claim"
EXTRACT_INBOX = WORKSPACE_DIR / "extracts"
ABSORB_INBOX = WORKSPACE_DIR / "absorbs"
CLONE_INBOX = WORKSPACE_DIR / "clones"

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

# Structural-audit aggregate docs (classified by `review.structural`).
# Same parent type as content reviews (review.content) but separate
# storage namespace for filesystem clarity. Per-finding violation docs
# co-locate under CLAIM_FINDINGS_DIR using a `audit-N` token in place
# of `review-N`.
CLAIM_AUDITS_DIR = DOCUVERSE_DOCS_DIR / "audit" / "claims"

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
    from lib.lattice.labels import format_label
    return PROMOTION_DIR / format_label(asn_num) / f"{kind}.md"


# Citation-resolve operation outputs (classified by `citation.resolve`).
# One doc per resolve run, named `<claim-label>-<run-N>.md` under the
# claim's ASN directory.
CITATION_RESOLVE_DIR = DOCUVERSE_DOCS_DIR / "citation-resolve" / "claims"

# Signature-resolve operation outputs. Same shape as CITATION_RESOLVE_DIR:
# one doc per resolve run, named `<claim-label>-<run-N>.md`.
SIGNATURE_RESOLVE_DIR = DOCUVERSE_DOCS_DIR / "signature-resolve" / "claims"

# Claim-contract operation outputs (annotate-type lift). One doc per
# fire, named `<claim-label>-<run-N>.md`. The fire emits the
# `contract.<kind>` classifier on the claim doc; this dir is the
# audit-trail companion.
CLAIM_CONTRACT_DIR = DOCUVERSE_DOCS_DIR / "claim-contract" / "claims"

# Claim formal-contract synthesis outputs (produce-contract lift). One
# doc per fire, named `<claim-label>-<run-N>.md`. The fire edits the
# claim md to add the `*Formal Contract:*` section; this dir is the
# audit-trail companion.
FORMAL_CONTRACT_DIR = DOCUVERSE_DOCS_DIR / "claim-formal-contract" / "claims"


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


def audit_doc_path(asn_label, claim_label, audit_num):
    """Path to an audit aggregate doc emitted by ClaimStructuralAuditAgent.

    Stored under `_docuverse/documents/audit/claims/<asn>/<claim>-<n>.md`.
    Per-claim numbering: each claim has its own audit history, numbered
    independently. The audit doc carries `review.structural` classifier
    and `review.coverage` link to the claim it covered.
    """
    return CLAIM_AUDITS_DIR / asn_label / f"{claim_label}-{audit_num}.md"


def next_audit_number(asn_label, claim_label):
    """Find the next audit number for this claim. Walks existing audit
    docs under <asn>/<claim>-*.md."""
    audit_subdir = CLAIM_AUDITS_DIR / asn_label
    if not audit_subdir.exists():
        return 1
    nums = []
    for p in audit_subdir.glob(f"{claim_label}-*.md"):
        m = re.search(rf"{re.escape(claim_label)}-(\d+)\.md$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


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


def consultation_dir(asn):
    """Per-ASN consultation directory. Accepts int or `<prefix>-NNNN` label."""
    from lib.lattice.labels import format_label, label_pattern
    if isinstance(asn, str) and label_pattern().fullmatch(asn):
        return CONSULTATIONS_DIR / asn
    return CONSULTATIONS_DIR / format_label(asn)


def claim_docs_dir(asn):
    """Per-ASN claim files directory under the substrate document store.

    Accepts int or `<prefix>-NNNN` label. Holds the per-claim body markdown
    plus `<stem>.{label,name,description}.md` sidecars. Reviews, caches, and
    structural section files stay alongside under
    `claim-convergence/<asn>/` (work products, not substrate-managed).
    """
    from lib.lattice.labels import format_label, label_pattern
    if isinstance(asn, str) and label_pattern().fullmatch(asn):
        return CLAIM_DIR / asn
    return CLAIM_DIR / format_label(asn)


def inquiry_doc_path(asn_num):
    """Path to a substrate-managed inquiry doc (md + frontmatter)."""
    from lib.lattice.labels import format_label
    return INQUIRY_DIR / f"{format_label(asn_num)}.md"


def claim_statements(asn_num):
    """Lattice path to a note's `statements` attribute sidecar.

    Lives next to the note doc under
    `_docuverse/documents/note/<note-stem>.statements.md`.
    Substrate-citizen; the note's outgoing `statements` link points
    at it.

    Reads at this path return the LLM-extracted content (which can
    be stale relative to current substrate state post-derivation).
    For up-to-date "what does this ASN say?" content, walk the
    note's `statements` link + supersession chain to the head and
    use `read_doc` instead — the head is the transclusion.claim-
    statements doc post-derivation.
    """
    from .common import find_asn
    from lib.lattice.labels import format_label
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        raise FileNotFoundError(
            f"no note found for {format_label(asn_num)}; cannot resolve "
            f"statements sidecar path"
        )
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


