"""Shared vault path constants for all pipeline scripts."""

import re
from pathlib import Path

import yaml

WORKSPACE = Path(__file__).resolve().parent.parent
VAULT = WORKSPACE / "vault"

# Model artifacts (top-level deliverables)
ASNS_DIR = VAULT / "asns"
PROOFS_DIR = VAULT / "proofs"
VOCABULARY = VAULT / "vocabulary.md"

# Stage 1: Promote
INQUIRIES_FILE = VAULT / "1-promote" / "inquiries.yaml"
PROMOTE_DIR = VAULT / "1-promote"

# Stage 2: Review
REVIEWS_DIR = VAULT / "2-review"

# Stage 3: Export (formal statements — dependency mechanism)
STATEMENTS_DIR = VAULT / "3-export"

# Stage 4: Modeling
ALLOY_DIR = VAULT / "4-modeling" / "alloy"
DAFNY_DIR = VAULT / "4-modeling" / "dafny"
PROOF_INDEX_DIR = VAULT / "4-modeling" / "proof-index"
VERIFICATION_DIR = VAULT / "4-modeling" / "verification"
PROOF_IMPORTS = PROOFS_DIR / "imports.md"
FOUNDATION_LIST = ASNS_DIR / "foundation.md"

# Stage 5: Worked Examples
EXAMPLES_DIR = VAULT / "5-examples"

# Stage 6: Test Cases
TESTCASES_DIR = VAULT / "6-test-cases"

# Manifests (per-ASN pipeline configuration)
PROJECT_MODEL_DIR = VAULT / "project-model"

# Experts (merged consultations + transcripts)
EXPERTS_DIR = VAULT / "experts"

# Requirements — Nelson's design features
REQUIREMENTS_DIR = VAULT / "requirements"

# Shared
USAGE_LOG = VAULT / "usage-log.jsonl"


def _review_sort_key(path):
    """Extract numeric review number for sorting. review-9 < review-13."""
    m = re.search(r"review-(\d+)\.md$", path.name)
    return int(m.group(1)) if m else 0


def sorted_reviews(asn_label, reviews_dir=None):
    """Return review files for an ASN, sorted by numeric review number."""
    d = reviews_dir or REVIEWS_DIR
    asn_dir = d / asn_label
    if not asn_dir.exists():
        return []
    return sorted(asn_dir.glob("review-*.md"), key=_review_sort_key)


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


def next_review_number(asn_label):
    """Find the next review number for this ASN (shared sequence with all reviews)."""
    asn_dir = REVIEWS_DIR / asn_label
    if not asn_dir.exists():
        return 1
    existing = sorted(asn_dir.glob("review-*.md"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"review-(\d+)\.md$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def next_modeling_number(asn_label):
    """Find the next Dafny modeling number for this ASN."""
    asn_dir = DAFNY_DIR / asn_label
    if not asn_dir.exists():
        return 1
    nums = []
    for p in asn_dir.glob("modeling-*"):
        m = re.search(r"modeling-(\d+)$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def find_latest_modeling_dir(asn_label):
    """Find the latest Dafny modeling directory for an ASN.

    Returns the path to the latest modeling-N dir, or None.
    """
    asn_dir = DAFNY_DIR / asn_label
    if not asn_dir.exists():
        return None
    gen_dirs = []
    for p in asn_dir.glob("modeling-*"):
        m = re.search(r"modeling-(\d+)$", p.name)
        if m:
            gen_dirs.append((int(m.group(1)), p))
    if not gen_dirs:
        return None
    gen_dirs.sort()
    return gen_dirs[-1][1]


def load_manifest(asn_id):
    """Load a manifest file for an ASN. Returns dict or empty dict."""
    path = PROJECT_MODEL_DIR / f"ASN-{int(asn_id):04d}.yaml"
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
