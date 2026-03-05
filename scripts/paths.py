"""Shared vault path constants for all pipeline scripts."""

import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
VAULT = WORKSPACE / "vault"

# Model artifacts (top-level deliverables)
ASNS_DIR = VAULT / "asns"
DAFNY_DIR = VAULT / "proofs"
VOCABULARY = VAULT / "vocabulary.md"

# Stage 1: Promote
INQUIRIES_FILE = VAULT / "1-promote" / "inquiries.yaml"
PROMOTE_DIR = VAULT / "1-promote"

# Stage 2: Review
REVIEWS_DIR = VAULT / "2-review"

# Stage 3: Modeling
ALLOY_DIR = VAULT / "3-modeling" / "alloy"
DAFNY_DISCOVERY_DIR = VAULT / "3-modeling" / "dafny"
CONTRACTS_DIR = VAULT / "3-modeling" / "contracts"
STATEMENTS_DIR = VAULT / "3-modeling" / "formal-statements"
VERIFICATION_DIR = VAULT / "3-modeling" / "verification"
MODULES_REGISTRY = VAULT / "3-modeling" / "modules.md"

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
