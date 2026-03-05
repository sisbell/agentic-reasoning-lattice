"""Shared vault path constants for all pipeline scripts."""

import re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
VAULT = WORKSPACE / "vault"

# Modeling — the model artifacts
ASNS_DIR = VAULT / "modeling" / "asns"
DAFNY_DIR = VAULT / "modeling" / "dafny"
VOCABULARY = VAULT / "modeling" / "vocabulary.md"

# Discovery — working artifacts of building the model
INQUIRIES_FILE = VAULT / "discovery" / "inquiries.yaml"
CONSULT_DIR = VAULT / "discovery" / "consultations"
TRANSCRIPTS_DIR = VAULT / "discovery" / "transcripts"
REVIEWS_DIR = VAULT / "discovery" / "reviews"
PROMOTE_DIR = VAULT / "discovery" / "promotions"
ALLOY_DIR = VAULT / "discovery" / "alloy"
DAFNY_DISCOVERY_DIR = VAULT / "discovery" / "dafny"

# Formalization — working artifacts of encoding the model
CONTRACTS_DIR = VAULT / "formalization" / "contracts"
EXTRACTS_DIR = VAULT / "formalization" / "extracts"
VERIFICATION_DIR = VAULT / "formalization" / "verification"

# Requirements — Nelson's design features
REQUIREMENTS_DIR = VAULT / "requirements"

# Shared
USAGE_LOG = VAULT / "usage-log.jsonl"


def _review_sort_key(path):
    """Extract numeric review number for sorting. review-9 < review-13."""
    m = re.search(r"-review-(\d+)\.md$", path.name)
    return int(m.group(1)) if m else 0


def sorted_reviews(asn_label, reviews_dir=None):
    """Return review files for an ASN, sorted by numeric review number."""
    d = reviews_dir or REVIEWS_DIR
    return sorted(d.glob(f"{asn_label}-review-*.md"), key=_review_sort_key)


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
    existing = sorted(REVIEWS_DIR.glob(f"{asn_label}-review-*.md"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"-review-(\d+)\.md$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1
