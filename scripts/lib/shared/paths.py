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
DOMAIN = WORKSPACE / "domains" / LATTICE_NAME
DOMAIN_PROMPTS = DOMAIN / "prompts"
CHANNELS_DIR = DOMAIN / "channels"

# Discovery stage
CONSULTATIONS_DIR = LATTICE / "discovery" / "consultations"
NOTES_DIR = LATTICE / "discovery" / "notes"
REVIEWS_DIR = LATTICE / "discovery" / "review"
PATCHES_DIR = LATTICE / "discovery" / "patches"

# Per-lattice files
VOCABULARY = LATTICE / "vocabulary.md"

# Blueprinting stage
BLUEPRINTS_DIR = LATTICE / "blueprinting"

# Formalization stage
FORMALIZATION_DIR = LATTICE / "formalization"

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


def note_dir(asn_num):
    """Per-note manifest directory."""
    return MANIFESTS_DIR / f"ASN-{int(asn_num):04d}"


def consultation_dir(asn):
    """Per-ASN consultation directory. Accepts int or ASN-NNNN label."""
    if isinstance(asn, str) and asn.startswith("ASN-"):
        return CONSULTATIONS_DIR / asn
    return CONSULTATIONS_DIR / f"ASN-{int(asn):04d}"


def note_yaml(asn_num):
    """Path to a note's metadata YAML."""
    return note_dir(asn_num) / "note.yaml"


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


def next_review_number(asn_label, reviews_dir=None):
    """Find the next review number for this ASN (shared sequence with all reviews)."""
    if reviews_dir is not None:
        note_subdir = reviews_dir
    else:
        note_subdir = REVIEWS_DIR / asn_label
    if not note_subdir.exists():
        return 1
    existing = sorted(note_subdir.glob("review-*.md"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"review-(\d+)\.md$", p.name)
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


def load_manifest(asn_id):
    """Load a note's manifest YAML. Returns dict or empty dict."""
    path = note_yaml(asn_id)
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def load_excluded_covers(asn_id):
    """Load combined covers text for an ASN's depends + already_covered.

    Reads the manifest for asn_id, collects all ASN IDs from
    depends and already_covered, then reads each of those manifests'
    covers field. Returns a combined string for the question filter.
    """
    manifest = load_manifest(asn_id)
    dep_ids = manifest.get("depends", [])
    ac_ids = manifest.get("already_covered", [])
    all_ids = set(dep_ids + ac_ids)

    if not all_ids:
        return ""

    covers = []
    for ref_id in sorted(all_ids):
        ref = load_manifest(ref_id)
        c = ref.get("covers", "")
        if c:
            covers.append(f"ASN-{int(ref_id):04d}: {c}")
    return "\n".join(covers)
