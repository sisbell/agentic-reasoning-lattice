"""
Cross-cutting Review step — whole-ASN deep structural analysis.

Reads the entire ASN + foundation and finds issues that per-property
pipelines can't catch: carrier-set conflation, precondition chain gaps,
arguments that assume what they prove, missing cases.

Step functions for the orchestrator (scripts/cross-review.py):
- run_review: run Opus deep review, return findings text
- extract_findings: parse findings into (title, text) tuples
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, load_manifest
from lib.shared.common import read_file, invoke_claude
from lib.shared.foundation import load_foundation_statements

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization" / "cross-review"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"


def run_review(asn_num, asn_path, asn_label, previous_findings=""):
    """Run Opus deep review. Returns (findings_text, elapsed) or (None, elapsed)."""
    foundation = load_foundation_statements(asn_num)
    if not foundation:
        print(f"  [ERROR] No foundation statements for {asn_label}",
              file=sys.stderr)
        return None, 0

    template = read_file(REVIEW_TEMPLATE)
    if not template:
        print(f"  [ERROR] Audit template not found", file=sys.stderr)
        return None, 0

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    # Pass previous findings so reviewer doesn't repeat them
    prior = previous_findings if previous_findings else "(none)"

    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_path.read_text())
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str)
              .replace("{{previous_findings}}", prior))

    print(f"  [REVIEW] Reading ASN + foundation (Opus)...",
          end="", file=sys.stderr, flush=True)

    text, elapsed = invoke_claude(prompt, model="opus", effort="high")

    if not text:
        print(f" error ({elapsed:.0f}s)", file=sys.stderr)
        return None, elapsed

    if "NO NEW ISSUES" in text:
        print(f" NO NEW ISSUES ({elapsed:.0f}s)", file=sys.stderr)
        return None, elapsed

    # Count findings (### headers)
    finding_count = len(re.findall(r'^### ', text, re.MULTILINE))
    print(f" {finding_count} findings ({elapsed:.0f}s)", file=sys.stderr)

    return text, elapsed


def extract_findings(text):
    """Extract individual findings from review output.

    Returns list of (title, finding_text) tuples.
    """
    findings = []
    parts = re.split(r'^### ', text, flags=re.MULTILINE)
    for part in parts[1:]:  # skip preamble before first ###
        lines = part.strip().split('\n', 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        findings.append((title, f"### {title}\n{body}"))
    return findings
