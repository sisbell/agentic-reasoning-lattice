"""Shared vault path constants for all pipeline scripts."""

import re
from pathlib import Path

import yaml

WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
VAULT = WORKSPACE / "vault"

# Stage 0: Consultations (merged transcripts)
EXPERTS_DIR = VAULT / "0-consultations"

# Stage 1: Reasoning documents (ASNs)
ASNS_DIR = VAULT / "1-reasoning-docs"
VOCABULARY = VAULT / "vocabulary.md"

# Stage 2: Review
REVIEWS_DIR = VAULT / "1-reasoning-docs-review"

# Blueprinting
BLUEPRINTS_DIR = VAULT / "2-blueprints"

# Stage 3: Formalization (per-claim working copies)
FORMALIZATION_DIR = VAULT / "3-formalization"

# Stage 3: Verification
ALLOY_DIR = VAULT / "3-verification" / "alloy"
DAFNY_DIR = VAULT / "3-verification" / "dafny"


# Stage 4: Proofs staging (Level 2 builds, pre-curation)
PROOFS_DIR = VAULT / "4-proofs-staging"
PROOF_IMPORTS = PROOFS_DIR / "imports.md"

# Stage 6: Worked Examples
EXAMPLES_DIR = VAULT / "6-examples"

# Stage 7: Test Cases
TESTCASES_DIR = VAULT / "7-test-cases"

# Per-ASN project model (manifests, statements, deps, issues)
PROJECT_MODEL_DIR = VAULT / "project-model"


def asn_dir(asn_num):
    """Per-ASN project model directory."""
    return PROJECT_MODEL_DIR / f"ASN-{int(asn_num):04d}"


def project_yaml(asn_num):
    """Path to ASN project manifest."""
    return asn_dir(asn_num) / "project.yaml"


def dep_graph(asn_num):
    """Path to ASN dependency graph YAML."""
    return asn_dir(asn_num) / "dependency-graph.yaml"


def formal_stmts(asn_num):
    """Path to ASN formal statements export."""
    return asn_dir(asn_num) / "formal-statements.md"


def open_issues_path(asn_num):
    """Path to ASN open issues file."""
    return asn_dir(asn_num) / "open-issues.md"

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


def next_review_number(asn_label, reviews_dir=None):
    """Find the next review number for this ASN (shared sequence with all reviews)."""
    if reviews_dir is not None:
        asn_dir = reviews_dir
    else:
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


def blueprint_properties_dir(asn_label):
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
    """Load a manifest file for an ASN. Returns dict or empty dict."""
    path = project_yaml(asn_id)
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
