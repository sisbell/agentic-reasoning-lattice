"""Shared vault path constants for all pipeline scripts."""

from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
VAULT = WORKSPACE / "vault"

# Modeling — the model artifacts
ASNS_DIR = VAULT / "asns"
DAFNY_DIR = VAULT / "dafny"
VOCABULARY = VAULT / "vocabulary.md"

# Discovery — working artifacts of building the model
INQUIRIES_FILE = VAULT / "inquiries.yaml"
CONSULT_DIR = VAULT / "consultations"
TRANSCRIPTS_DIR = VAULT / "transcripts"
REVIEWS_DIR = VAULT / "reviews"
TRIAGE_DIR = VAULT / "triage"

# Formalization — working artifacts of encoding the model
CONTRACTS_DIR = VAULT / "contracts"
EXTRACTS_DIR = VAULT / "extracts"

# Shared
USAGE_LOG = VAULT / "usage-log.jsonl"
