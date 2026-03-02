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
TRIAGE_DIR = VAULT / "discovery" / "triage"

# Formalization — working artifacts of encoding the model
CONTRACTS_DIR = VAULT / "formalization" / "contracts"
EXTRACTS_DIR = VAULT / "formalization" / "extracts"

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
