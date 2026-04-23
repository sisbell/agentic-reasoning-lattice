"""
Local Review step — per-claim 7-point checklist review.

Builds a minimal context (claim section + dependency sections) and
calls opus to review the proof. Returns structured results for the
convergence loop.

Step function for the orchestrator (scripts/local-review.py):
- review_claim: review one claim's proof, return (status, finding_text)
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import USAGE_LOG, prompt_path, formal_stmts
from lib.shared.common import find_asn
from lib.formalization.full_review.review import (
    extract_findings, filter_revise, parse_verdict,
)

REVIEW_TEMPLATE = prompt_path("formalization/local-review/review.md")


def _invoke_opus(prompt, effort="high"):
    """Call claude --print with opus."""
    cmd = [
        "claude", "--print",
        "--model", "claude-opus-4-7",
        "--tools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [REVIEW] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        return "", elapsed

    return result.stdout.strip(), elapsed


def _log_usage(elapsed, asn_num, label=""):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "local-review",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
        }
        if label:
            entry["label"] = label
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def _build_proof_context(asn_num, label, deps_data, sections,
                         foundation_cache=None):
    """Build review context for a single claim.

    Returns (claim_section, dependency_text) where dependency_text
    contains all sections referenced by follows_from.
    """
    claim_data = deps_data.get("claims", {}).get(label, {})
    follows_from = claim_data.get("follows_from", [])

    claim_section = sections.get(label, "")
    if not claim_section:
        return "", ""

    # Collect dependency sections
    dep_parts = []

    # Internal dependencies (same ASN)
    all_labels = set(deps_data.get("claims", {}).keys())
    for dep_label in follows_from:
        if dep_label in all_labels and dep_label in sections:
            dep_parts.append(f"### {dep_label}\n\n{sections[dep_label]}")

    # Foundation dependencies (other ASNs)
    if foundation_cache is None:
        foundation_cache = {}
    depends = deps_data.get("depends", [])
    for dep_asn in depends:
        if dep_asn not in foundation_cache:
            stmt_path = formal_stmts(dep_asn)
            if stmt_path.exists():
                foundation_cache[dep_asn] = stmt_path.read_text()
            else:
                foundation_cache[dep_asn] = ""

    # Extract referenced foundation labels
    for dep_label in follows_from:
        if dep_label not in all_labels:
            for dep_asn in depends:
                ftext = foundation_cache.get(dep_asn, "")
                pattern = re.compile(
                    r'^## ' + re.escape(dep_label) + r'\s*—.*?\n'
                    r'(.*?)(?=^## |\Z)',
                    re.MULTILINE | re.DOTALL
                )
                m = pattern.search(ftext)
                if m:
                    dep_parts.append(
                        f"### {dep_label} (ASN-{dep_asn:04d})\n\n"
                        f"## {dep_label} — ...\n{m.group(1).strip()}"
                    )
                    break

    dependency_text = "\n\n".join(dep_parts) if dep_parts else "(none)"
    return claim_section, dependency_text


def review_claim(asn_num, label, deps_data, sections, foundation_cache=None):
    """Review one claim's proof.

    Returns (verdict, findings):
        verdict   — "CONVERGED" | "OBSERVE" | "REVISE" | "UNKNOWN" | "ERROR"
        findings  — list of (title, cls, body) tuples on non-CONVERGED/ERROR;
                    None on CONVERGED or ERROR.
    """
    asn_label = f"ASN-{asn_num:04d}"

    claim_section, dependency_text = _build_proof_context(
        asn_num, label, deps_data, sections, foundation_cache)

    if not claim_section:
        print(f"  [REVIEW] {label}: no section found — skipping",
              file=sys.stderr)
        return "error", None

    template = REVIEW_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{claim_section}}", claim_section)
              .replace("{{dependency_sections}}", dependency_text))

    print(f"  [REVIEW] {label} ({len(prompt) // 1024}KB)...",
          file=sys.stderr, end="", flush=True)

    text, elapsed = _invoke_opus(prompt)
    _log_usage(elapsed, asn_num, label=label)

    if not text:
        print(f" error ({elapsed:.0f}s)", file=sys.stderr)
        return "ERROR", None

    verdict = parse_verdict(text)

    if verdict == "CONVERGED":
        print(f" verdict=CONVERGED ({elapsed:.0f}s)", file=sys.stderr)
        return "CONVERGED", None

    findings = extract_findings(text)
    n_revise = sum(1 for f in findings if f[1] == "REVISE")
    n_observe = sum(1 for f in findings if f[1] == "OBSERVE")
    counts = f"{len(findings)} finding(s) ({n_revise} REVISE, {n_observe} OBSERVE)"
    print(f" verdict={verdict} ({elapsed:.0f}s) — {counts}",
          file=sys.stderr)
    return verdict, findings
