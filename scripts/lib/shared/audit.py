"""
Audit utilities — open issues management and foundation consistency checks.

Provides:
- Open issues file management (_append_open_issues, _load_open_issues, clear_open_issues)
- Foundation audit steps (surface_check, find_extensions, verify_transfer, audit)

Used by: discovery/revise.py, formalization/verify.py, formalization/run.py,
         audit/surface.py
"""

import re
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (WORKSPACE, REVIEWS_DIR,
                   load_manifest, next_review_number,
                   open_issues_path)
from lib.shared.common import read_file, find_asn, invoke_claude, log_usage
from lib.shared.foundation import load_foundation_statements


PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
SURFACE_CHECK_TEMPLATE = PROMPTS_DIR / "surface-check.md"
DOMAIN_EXTENSIONS_TEMPLATE = PROMPTS_DIR / "domain-extensions.md"
TRANSFER_VERIFICATION_TEMPLATE = PROMPTS_DIR / "transfer-verification.md"
AUDIT_TEMPLATE = PROMPTS_DIR / "foundation-audit.md"


# ---------------------------------------------------------------------------
# Open issues management
# ---------------------------------------------------------------------------

def _load_open_issues(asn_num):
    """Load existing open issues for an ASN. Returns content or empty string."""
    path = open_issues_path(asn_num)
    if path.exists():
        return path.read_text().strip()
    return ""


def _append_open_issues(asn_num, new_issues):
    """Append new issues to the open issues file."""
    path = open_issues_path(asn_num)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = ""
    if path.exists():
        existing = path.read_text().strip()

    if existing:
        content = existing + "\n\n" + new_issues.strip() + "\n"
    else:
        content = new_issues.strip() + "\n"

    path.write_text(content)
    print(f"  [WROTE] {path.relative_to(WORKSPACE)}", file=sys.stderr)


def clear_open_issues(asn_num):
    """Clear the open issues file."""
    path = open_issues_path(asn_num)
    if path.exists():
        path.unlink()
        print(f"  [CLEARED] {path.relative_to(WORKSPACE)}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Sonnet check runner
# ---------------------------------------------------------------------------

def _run_sonnet_check(asn_num, asn_path, asn_label, template_path,
                      step_name, clean_marker, effort="high",
                      has_open_issues=False):
    """Run a sonnet check from a template. Returns True if findings found.

    Common logic for surface-check, domain-extensions, and transfer-verification.
    """
    foundation = load_foundation_statements(asn_num)
    if not foundation:
        return False

    if not template_path.exists():
        print(f"  [{step_name}] Template not found: {template_path}",
              file=sys.stderr)
        return False

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    template = template_path.read_text()
    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_path.read_text())
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str))

    if has_open_issues:
        open_issues = _load_open_issues(asn_num)
        prompt = prompt.replace("{{open_issues}}", open_issues or "(none)")

    print(f"  [{step_name}] Running on {asn_label}...", file=sys.stderr)

    text, elapsed = invoke_claude(prompt, model="sonnet", effort=effort)

    if not text:
        print(f"  [{step_name}] No output ({elapsed:.0f}s)", file=sys.stderr)
        return False

    log_usage(f"audit-{step_name.lower()}", elapsed, asn=asn_num)

    # Write as review file for the record
    review_dir = REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(text + "\n")
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Check for clean marker
    if clean_marker and clean_marker in text:
        print(f"  [{step_name}] Clean ({elapsed:.0f}s)", file=sys.stderr)
        return False

    # Append raw output to open issues
    _append_open_issues(asn_num, text)
    print(f"  [{step_name}] Findings appended ({elapsed:.0f}s)",
          file=sys.stderr)
    return True


# ---------------------------------------------------------------------------
# Audit steps
# ---------------------------------------------------------------------------

def step_surface_check(asn_num, asn_path, asn_label):
    """Surface check (sonnet): stale labels, drift, registry, deps, exhaustiveness.

    Returns True if findings were found, False if CLEAN.
    """
    return _run_sonnet_check(
        asn_num, asn_path, asn_label,
        SURFACE_CHECK_TEMPLATE,
        step_name="SURFACE",
        clean_marker="RESULT: CLEAN",
    )


def step_find_extensions(asn_num, asn_path, asn_label):
    """Domain extension finder (sonnet): list all extensions and claimed analogs.

    Returns True if extensions were found, False if none.
    """
    return _run_sonnet_check(
        asn_num, asn_path, asn_label,
        DOMAIN_EXTENSIONS_TEMPLATE,
        step_name="EXTENSIONS",
        clean_marker="NO EXTENSIONS FOUND",
    )


def step_verify_transfer(asn_num, asn_path, asn_label):
    """Transfer verification (sonnet, CoT): verify each domain extension is sound.

    Returns True if gaps were found, False if all verified or no extensions.
    """
    return _run_sonnet_check(
        asn_num, asn_path, asn_label,
        TRANSFER_VERIFICATION_TEMPLATE,
        step_name="TRANSFER",
        clean_marker="ALL VERIFIED",
        effort="max",
    )


def step_audit(asn_num, asn_path, asn_label):
    """Run an open-ended foundation audit via opus.

    Reads the ASN, foundation, and accumulated open issues.
    Finds cross-boundary issues the structured checks missed.
    """
    foundation = load_foundation_statements(asn_num)
    if not foundation:
        print(f"  [ERROR] No foundation statements loaded for {asn_label}",
              file=sys.stderr)
        return False

    template = read_file(AUDIT_TEMPLATE)
    if not template:
        print("  [ERROR] Audit prompt template not found", file=sys.stderr)
        return False

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    open_issues = _load_open_issues(asn_num)
    if not open_issues:
        open_issues = "(none)"

    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_path.read_text())
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str)
              .replace("{{open_issues}}", open_issues))

    print(f"  [AUDIT] Open-ended audit of {asn_label}...",
          file=sys.stderr)

    text, elapsed = invoke_claude(prompt, model="opus", effort="high")

    if not text:
        print(f"  [AUDIT] No output ({elapsed:.0f}s)", file=sys.stderr)
        return False

    log_usage("audit-open", elapsed, asn=asn_num)

    if "NO NEW ISSUES" in text:
        print(f"  [AUDIT] No new issues found ({elapsed:.0f}s)",
              file=sys.stderr)
        return True

    # Append new issues to open issues file
    _append_open_issues(asn_num, text)
    print(f"  [AUDIT] New issues appended ({elapsed:.0f}s)", file=sys.stderr)
    return True
