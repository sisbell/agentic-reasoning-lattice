"""Shared lattice path constants for all pipeline scripts."""

import os
import re
from pathlib import Path

import yaml

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

# Lattice identity — resolved from (in priority order):
#   1. `--lattice <name>` (or `--lattice=<name>`) in sys.argv
#   2. `LATTICE` env var
#   3. default "xanadu"
# Centralized here so every CLI inherits --lattice support automatically.
# CLIs can still register `--lattice` with argparse for --help visibility,
# but the resolution above runs at module-load time and binds LATTICE_NAME
# before any path constants are computed.


def _resolve_lattice_name() -> str:
    import sys
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--lattice" and i + 1 < len(args):
            return args[i + 1]
        if args[i].startswith("--lattice="):
            return args[i].split("=", 1)[1]
        i += 1
    return os.environ.get("LATTICE", "xanadu")


LATTICE_NAME = _resolve_lattice_name()
LATTICE = WORKSPACE / "lattices" / LATTICE_NAME
CHANNELS_DIR = WORKSPACE / "channels"

# Per-lattice (node, user) tumbler prefix — partitions document paths
# in the substrate so two lattices' content doesn't collide on disk.
# Hardcoded today; will move into lattice-doc frontmatter when lattice
# docs become the substrate config source.
_NODE_USER_PREFIX = {
    "xanadu": ("1.1", "1"),
    "materials": ("1.2", "1"),
}
LATTICE_NODE, LATTICE_USER = _NODE_USER_PREFIX.get(LATTICE_NAME, ("1.1", "1"))

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

# Per-lattice files
VOCABULARY = LATTICE / "vocabulary.md"

# Verification stage
# Dafny moved to repo-root /verification/dafny/ for fresh regeneration.
# Alloy + proofs constants still point at the legacy LATTICE-relative
# locations (now under _archive/verification/...) — those subsystems
# are not in active scope.
ALLOY_DIR = LATTICE / "verification" / "alloy"
DAFNY_DIR = WORKSPACE / "verification" / "dafny"
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
# substrate-classified documents live here. Single unified instance
# at repo root; lattices co-reside via the (node, user) author
# partition under documents/.
DOCUVERSE_DIR = WORKSPACE / "_docuverse"
DOCUVERSE_LOG = DOCUVERSE_DIR / "links.jsonl"
DOCUVERSE_INDEX = DOCUVERSE_DIR / "index.db"
# Substrate-classified documents live under _docuverse/documents/.
# Structural state (links.jsonl, index.db) sits alongside as a sibling.
DOCUVERSE_DOCS_DIR = DOCUVERSE_DIR / "documents"
# Author-scoped subtree: each (node, user) owns their own document tree.
# Document type directories (agent/, claim/, note/, ...) live inside the
# author's subtree. Two lattices co-residing in one docuverse don't
# collide on filenames because they're under different (node, user)
# prefixes.
DOCUVERSE_AUTHOR_DIR = DOCUVERSE_DOCS_DIR / LATTICE_NODE / LATTICE_USER
RATIONALE_DIR = DOCUVERSE_AUTHOR_DIR / "rationale"
AGENT_DIR = DOCUVERSE_AUTHOR_DIR / "agent"
CAMPAIGN_DIR = DOCUVERSE_AUTHOR_DIR / "campaign"
INQUIRY_DIR = DOCUVERSE_AUTHOR_DIR / "inquiry"
NOTE_DIR = DOCUVERSE_AUTHOR_DIR / "note"
CLAIM_DIR = DOCUVERSE_AUTHOR_DIR / "claim"
MOTIFS_DIR = DOCUVERSE_AUTHOR_DIR / "motifs"  # scout snapshot docs
MOTIF_DIR = DOCUVERSE_AUTHOR_DIR / "motif"    # materialized motif docs + sidecars
# Discovery-stage consultation directory.
CONSULTATIONS_DIR = DOCUVERSE_AUTHOR_DIR / "consultation"
# Substrate-citizen patches. Split by target kind (note/claim) so that:
#   - the operator's directory choice declares intent (note vs claim)
#   - filenames don't collide between a note-targeted and claim-targeted
#     patch with the same stem
#   - substrate dirs are homogeneous in classifier subtype
# Operator drops a patch md into PATCH_INBOX_{NOTE,CLAIM} (workspace,
# gitignored); the matching agent promotes it to PATCH_{NOTE,CLAIM}_DIR
# (substrate citizen, committed) on fire.
PATCH_NOTE_DIR = DOCUVERSE_AUTHOR_DIR / "patch" / "note"
PATCH_CLAIM_DIR = DOCUVERSE_AUTHOR_DIR / "patch" / "claim"

# Substrate-citizen extract spec docs. Operator drops the spec md into
# EXTRACT_INBOX (workspace, gitignored); NoteExtractAgent promotes it to
# EXTRACT_DIR on fire. The spec doc carries the operator's scout-output:
# extract_from / create_note / absorb_into / claims plus rationale prose.
EXTRACT_DIR = DOCUVERSE_AUTHOR_DIR / "extract"

# Substrate-citizen absorb spec docs. Operator drops the spec md into
# ABSORB_INBOX (workspace, gitignored); NoteAbsorbAgent promotes it to
# ABSORB_DIR on fire. The spec doc carries the operator's scout-output:
# which extension to absorb plus rationale prose justifying readiness.
ABSORB_DIR = DOCUVERSE_AUTHOR_DIR / "absorb"

# Substrate-citizen clone spec docs. Operator drops the spec md into
# CLONE_INBOX (workspace, gitignored); NoteCloneAgent promotes it to
# CLONE_DIR on fire. The spec doc carries the operator's scout-output:
# clone_from / create_note plus rationale prose for the clone.
CLONE_DIR = DOCUVERSE_AUTHOR_DIR / "clone"

# Substrate-citizen import spec docs. Operator drops the spec md into
# IMPORT_INBOX (workspace, gitignored); NoteImportAgent promotes it to
# IMPORT_DIR on fire. The spec doc carries the operator's scout-output:
# source_doc / create_note / title / depends plus rationale prose.
# Lifts an external doc (anywhere in the repo) into the note set.
IMPORT_DIR = DOCUVERSE_AUTHOR_DIR / "import"

# Loop work products. Sibling to _docuverse/. Holds artifacts produced
# by the refinement/derivation loops that aren't themselves
# substrate-classified documents (scratch caches, intermediate state).
WORKSPACE_DIR = WORKSPACE / "_workspace"
PATCH_INBOX_NOTE = WORKSPACE_DIR / "patches" / "note"
PATCH_INBOX_CLAIM = WORKSPACE_DIR / "patches" / "claim"
EXTRACT_INBOX = WORKSPACE_DIR / "extracts"
ABSORB_INBOX = WORKSPACE_DIR / "absorbs"
CLONE_INBOX = WORKSPACE_DIR / "clones"
IMPORT_INBOX = WORKSPACE_DIR / "imports"

# Per-worker substrate-emission buffer. During a fire, each worker
# appends emissions to its own pending file rather than the canonical
# `_docuverse/links.jsonl`. At commit step, the worker holds a brief
# substrate-write lock, appends pending → canonical, truncates pending,
# then runs the path-scoped commit. This isolates one worker's
# emissions from another worker's commit — multiple workers writing in
# parallel no longer cross-contaminate each other's commits.
#
# Lifecycle: pending files are operator-local scratch (lives under the
# gitignored `_workspace/`). At runner startup the per-worker files
# are truncated — any unflushed emissions from a previous worker death
# are discarded (the death-cleanup tools handle pre-death substrate
# state that DID land in canonical before death).
WORKER_PENDING_DIR = WORKSPACE_DIR


def worker_pending_jsonl(worker_idx):
    """Path to the per-worker pending substrate-emissions file.

    Returns None when worker_idx is None — for non-runner contexts
    (operator CLI tools, tests) emit goes straight to canonical
    `_docuverse/links.jsonl`.
    """
    if worker_idx is None:
        return None
    return WORKER_PENDING_DIR / f"links.worker-{int(worker_idx)}.jsonl"

# Aggregate review docs (classified by `review`). Split by inquiry-target
# kind so review numbering and substrate queries are scoped per kind.
CLAIM_REVIEWS_DIR = DOCUVERSE_AUTHOR_DIR / "review" / "claims"
NOTE_REVIEWS_DIR = DOCUVERSE_AUTHOR_DIR / "review" / "notes"
REVIEWS_DIR = NOTE_REVIEWS_DIR  # legacy alias, prefer NOTE_REVIEWS_DIR

# Per-finding decomposition outputs (classified by `finding`, related to
# their target by `comment.<kind>`). Each per-review subdirectory pairs
# with the matching aggregate doc by the shared `review-N` token.
CLAIM_FINDINGS_DIR = DOCUVERSE_AUTHOR_DIR / "finding" / "claims"
NOTE_FINDINGS_DIR = DOCUVERSE_AUTHOR_DIR / "finding" / "notes"

# Structural-audit aggregate docs (classified by `review.structural`).
# Same parent type as content reviews (review.content) but separate
# storage namespace for filesystem clarity. Per-finding violation docs
# co-locate under CLAIM_FINDINGS_DIR using a `audit-N` token in place
# of `review-N`.
CLAIM_AUDITS_DIR = DOCUVERSE_AUTHOR_DIR / "audit" / "claims"

def claim_statements_aggregate_path(asn_label: str) -> Path:
    """Lattice-relative path for an ASN's `claims.statements` aggregate doc.

    Lives next to the per-claim files under `claim/<asn>/_statements.md`.
    Leading underscore distinguishes the aggregate from per-claim files
    (`T2.md`, `TumblerSub.md`, etc.) that share the directory. The doc
    is generated (not live-rendered) and is a substrate citizen with its
    own supersession chain.
    """
    return CLAIM_DIR / asn_label / "_statements.md"


# Promotion reports (classified by `promotion.<kind>`). One doc per
# (source ASN, kind), where kind ∈ {out-of-scope, open-questions}.
# Holds the LLM's promote/decline verdicts plus rationale; re-runs
# overwrite. See docs/hypergraph-protocol/promotion.md.
PROMOTION_DIR = DOCUVERSE_AUTHOR_DIR / "promotion"


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
CITATION_RESOLVE_DIR = DOCUVERSE_AUTHOR_DIR / "citation-resolve" / "claims"

# Signature-resolve operation outputs. Same shape as CITATION_RESOLVE_DIR:
# one doc per resolve run, named `<claim-label>-<run-N>.md`.
SIGNATURE_RESOLVE_DIR = DOCUVERSE_AUTHOR_DIR / "signature-resolve" / "claims"

# Claim-contract operation outputs (annotate-type lift). One doc per
# fire, named `<claim-label>-<run-N>.md`. The fire emits the
# `contract.<kind>` classifier on the claim doc; this dir is the
# audit-trail companion.
CLAIM_CONTRACT_DIR = DOCUVERSE_AUTHOR_DIR / "claim-contract" / "claims"

# Claim formal-contract synthesis outputs (produce-contract lift). One
# doc per fire, named `<claim-label>-<run-N>.md`. The fire edits the
# claim md to add the `*Formal Contract:*` section; this dir is the
# audit-trail companion.
FORMAL_CONTRACT_DIR = DOCUVERSE_AUTHOR_DIR / "claim-formal-contract" / "claims"


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
    """Docuverse-relative path to an agent doc by role name.

    The substrate identifies an agent by its doc address — a path
    relative to WORKSPACE (the docuverse's root parent), so callers
    wiring up `XANADU_AGENT_DOC` or invoking `emit_agent` use this to
    get the canonical form. Includes the active lattice's
    (node, user) prefix.
    """
    return str((AGENT_DIR / f"{role}.md").relative_to(WORKSPACE))


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
    `_docuverse/documents/<node>/<user>/claim/<asn_label>/<label>.md` as
    a string. Pure construction — does not check whether the file exists.
    Suitable for both already-existing claims (the path is always
    conventional) and freshly-created ones the LLM has just written
    under the same convention.

    Used by the link-emit CLIs (cite, retract, classify, label, name,
    description) to translate their --label argument into the substrate
    address. Per the Xanadu-aligned design, callers pass labels rather
    than path strings; the path convention is the local-reference's
    way of mapping label-as-identity to a filesystem address.
    """
    return (
        f"_docuverse/documents/{LATTICE_NODE}/{LATTICE_USER}/"
        f"claim/{asn_label}/{label}.md"
    )


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

    `kind` selects both the reviews dir and the findings namespace
    ("claim" or "note"); numbering is independent per kind. Sources
    from three places, taking max+1 across all:
      1. Current review files (review-N.md) under the kind's reviews
         dir. CONVERGED reviews leave a file here but no findings
         directory, so this scan is required to avoid overwriting them.
      2. Legacy review files (review-N.md) under `reviews_dir` if
         provided — caller-supplied path. Retained for callers that
         track auxiliary review locations alongside the kind's primary
         dir.
      3. Current review directories (review-N/) under the kind's
         findings dir.
    """
    nums = []

    # Current review files under the kind's reviews dir.
    primary_reviews = _reviews_dir_for_kind(kind) / asn_label
    if primary_reviews.exists():
        for p in primary_reviews.glob("review-*.md"):
            m = re.search(r"review-(\d+)\.md$", p.name)
            if m:
                nums.append(int(m.group(1)))

    # Auxiliary review files (numbered review-N.md). Caller passes the dir.
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


