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
CONSULTATIONS_DIR = LATTICE / "discovery" / "consultations"
NOTES_DIR = LATTICE / "discovery" / "notes"
REVIEWS_DIR = LATTICE / "discovery" / "review"
PATCHES_DIR = LATTICE / "discovery" / "patches"

# Per-lattice files
VOCABULARY = LATTICE / "vocabulary.md"
LATTICE_CONFIG = LATTICE / "config.yaml"

# Blueprinting stage
BLUEPRINTS_DIR = LATTICE / "blueprinting"

# Claim convergence stage
CLAIM_CONVERGENCE_DIR = LATTICE / "claim-convergence"

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

# Protocol substrate store (claim convergence protocol stage 1 — bootstrap toward Xanadu)
STORE_DIR = LATTICE / "_store"
STORE_LOG = STORE_DIR / "links.jsonl"
STORE_INDEX = STORE_DIR / "index.db"
# Substrate-managed documents live under _store/documents/. Structural
# state (links.jsonl, index.db) and diagnostic artifacts (_failures/) sit
# alongside as siblings; documents are the content the substrate's links
# reference.
STORE_DOCS_DIR = STORE_DIR / "documents"
RATIONALES_DIR = STORE_DOCS_DIR / "rationales"
AGENTS_DIR = STORE_DOCS_DIR / "agents"
CAMPAIGNS_DIR = STORE_DOCS_DIR / "campaigns"
INQUIRIES_DIR = STORE_DOCS_DIR / "inquiries"

# Findings split by inquiry-target kind: claim convergence vs note convergence.
# Each kind owns its own ASN namespace under documents/findings/, so review
# numbering and substrate queries are scoped per kind.
CLAIM_FINDINGS_DIR = STORE_DOCS_DIR / "findings" / "claims"
NOTE_FINDINGS_DIR = STORE_DOCS_DIR / "findings" / "notes"


def _findings_dir_for_kind(kind):
    if kind == "claim":
        return CLAIM_FINDINGS_DIR
    if kind == "note":
        return NOTE_FINDINGS_DIR
    raise ValueError(f"unknown findings kind: {kind!r}")


def agent_doc_path(role):
    """Workspace-relative path to an agent doc by role name.

    The substrate identifies an agent by its doc address (workspace-relative
    string), so callers wiring up `XANADU_AGENT_DOC` or invoking `emit_agent`
    use this to get the canonical form.
    """
    return str((AGENTS_DIR / f"{role}.md").relative_to(WORKSPACE))


def review_meta_path(asn_label, review_num, *, kind):
    """Path to a review event's _meta.md under the substrate findings dir.

    `kind` selects the findings namespace: "claim" or "note".
    """
    return _findings_dir_for_kind(kind) / asn_label / f"review-{review_num}" / "_meta.md"


def note_dir(asn_num):
    """Per-note manifest directory."""
    return MANIFESTS_DIR / f"ASN-{int(asn_num):04d}"


def consultation_dir(asn):
    """Per-ASN consultation directory. Accepts int or ASN-NNNN label."""
    if isinstance(asn, str) and asn.startswith("ASN-"):
        return CONSULTATIONS_DIR / asn
    return CONSULTATIONS_DIR / f"ASN-{int(asn):04d}"


def note_yaml(asn_num):
    """Legacy path to a note's metadata YAML. Pre-Phase-2 inquiry refactor.
    Should not be referenced by new code — use inquiry_doc_path / state_yaml.
    """
    return note_dir(asn_num) / "note.yaml"


def inquiry_doc_path(asn_num):
    """Path to a substrate-managed inquiry doc (md + frontmatter)."""
    return INQUIRIES_DIR / f"ASN-{int(asn_num):04d}.md"


def state_yaml(asn_num):
    """Path to a per-ASN operational state file (machine-written cache).

    Holds last_consistency_check, last_pipeline_run, etc. — fields that
    don't go to substrate and don't belong in the inquiry doc. Sibling
    of formal-statements.md and dependency-graph.yaml under
    `manifests/ASN-NNNN/`.
    """
    return note_dir(asn_num) / "state.yaml"


def dep_graph(asn_num):
    """Path to ASN dependency graph YAML."""
    return note_dir(asn_num) / "dependency-graph.yaml"


def formal_stmts(asn_num):
    """Path to ASN formal statements export."""
    return note_dir(asn_num) / "formal-statements.md"


def open_issues_path(asn_num):
    """Path to ASN open issues file."""
    return note_dir(asn_num) / "open-issues.md"


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


def blueprint_claims_dir(asn_label):
    """Per-ASN blueprint claims directory."""
    return BLUEPRINTS_DIR / asn_label / "claims"


def blueprint_lint_dir(asn_label):
    """Per-ASN blueprint lint directory."""
    return BLUEPRINTS_DIR / asn_label / "lint"


def blueprint_global_lint_dir():
    """Global blueprint lint directory (cross-ASN results)."""
    return BLUEPRINTS_DIR / "lint"


def lint_path(asn_label, kind):
    """Path to a per-ASN lint result file (e.g., status.md, deps.md, inline.md)."""
    return blueprint_lint_dir(asn_label) / f"{kind}.md"


def lint_global_path(kind):
    """Path to a global lint result file (e.g., deps-global.md)."""
    return blueprint_global_lint_dir() / f"{kind}.md"


def load_inquiry(asn_id):
    """Load inquiry frontmatter for an ASN. Returns dict or empty dict.
    The inquiry-content fields only — operational state lives in
    state.yaml (load via `load_state`)."""
    from lib.shared.common import read_doc_frontmatter
    return read_doc_frontmatter(inquiry_doc_path(asn_id))


def load_state(asn_id):
    """Load per-ASN operational state. Returns dict or empty dict."""
    path = state_yaml(asn_id)
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


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
    return CAMPAIGNS_DIR / name


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


