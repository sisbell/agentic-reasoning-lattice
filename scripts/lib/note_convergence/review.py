#!/usr/bin/env python3
"""
Review an ASN for rigor — Dijkstra-style proof checking.

Loads the ASN content and shared vocabulary, injects them into a review
prompt template, and invokes claude --print with --tools "" (review is
pure analysis, no file access needed).

Results written to the lattice's discovery/review/ directory for traceability.

Usage:
    python scripts/lib/review_check.py 4
    python scripts/lib/review_check.py 9 --model sonnet
    python scripts/lib/review_check.py 9 --effort high
    python scripts/lib/review_check.py 4 --dry-run
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, VOCABULARY, REVIEWS_DIR, USAGE_LOG, MANIFESTS_DIR, NOTES_DIR, NOTE_FINDINGS_DIR, LATTICE_PROMPTS, sorted_reviews, load_inquiry, open_issues_path
from lib.shared.campaign import resolve_campaign
from lib.shared.common import find_asn, read_file
from lib.shared.foundation import load_foundation_for_note
from lib.store.emit import emit_note_findings, emit_review
from lib.store.store import default_store

PROMPTS_DIR = LATTICE_PROMPTS / "discovery"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"


def load_out_of_scope(asn_number):
    """Look up out_of_scope for an ASN from its inquiry frontmatter."""
    return load_inquiry(asn_number).get("out_of_scope", "")


def load_open_issues(asn_number):
    """Load open issues file for an ASN. Returns content or empty string."""
    path = open_issues_path(asn_number)
    if path.exists():
        content = path.read_text().strip()
        if content:
            return content
    return "(none)"


def process_resolved_issues(asn_number, review_text):
    """Remove resolved issues from the open issues file.

    Parses the ## RESOLVED section of a review. For each resolved issue,
    removes the matching ### heading and its content from the open issues file.
    """
    # Find ## RESOLVED section
    resolved_match = re.search(r"^## RESOLVED\s*\n(.*?)(?=^## |\Z)",
                               review_text, re.MULTILINE | re.DOTALL)
    if not resolved_match:
        return

    # Extract resolved issue titles
    resolved_titles = re.findall(r"^### (.+)$", resolved_match.group(1),
                                 re.MULTILINE)
    if not resolved_titles:
        return

    issues_path = open_issues_path(asn_number)
    if not issues_path.exists():
        return

    content = issues_path.read_text()
    original = content

    for title in resolved_titles:
        # Remove the ### heading and everything until the next ### or end
        pattern = rf"^### {re.escape(title)}\s*\n.*?(?=^### |\Z)"
        content = re.sub(pattern, "", content, flags=re.MULTILINE | re.DOTALL)
        print(f"  [RESOLVED] Removed: {title}", file=sys.stderr)

    content = content.strip()
    if content != original.strip():
        if content:
            issues_path.write_text(content + "\n")
        else:
            # All issues resolved — remove the file
            issues_path.unlink()
            print(f"  [RESOLVED] All open issues resolved — file removed",
                  file=sys.stderr)



def build_prompt(asn_content, vocabulary, out_of_scope="",
                 asn_number=None, general=False, foundation=""):
    """Assemble review prompt from template + injected content.

    Caller supplies `foundation` directly (typically via
    `load_foundation_for_note`). The template's foundation slot can be
    empty if the ASN has no upstream deps.
    """
    template_path = REVIEW_TEMPLATE
    template = read_file(template_path)
    if not template:
        print(f"  Review prompt template not found at {template_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    open_issues = load_open_issues(asn_number) if asn_number else "(none)"

    scope_note = (f"\n\n## Scope\n\nThe following topics are OUT OF SCOPE for this ASN. "
                  f"Do not flag missing coverage for them. If the ASN defines claims "
                  f"for these topics, flag them as OUT_OF_SCOPE: {out_of_scope}"
                  if out_of_scope else "")

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{vocabulary}}", vocabulary
    ).replace(
        "{{foundation_statements}}", foundation
    ).replace(
        "{{open_issues}}", open_issues
    ) + scope_note


def strip_preamble(text):
    """Strip any tool-use preamble before the review header."""
    marker = re.search(r"^# Review of ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def validate_review(text):
    """Check that review text has required structure. Returns error message or None."""
    if not re.search(r"^# Review of ASN-\d+", text, re.MULTILINE):
        return "missing '# Review of ASN-NNNN' header"
    if not re.search(r"^VERDICT:\s*\w+", text, re.MULTILINE):
        return "missing VERDICT line"
    if not (re.search(r"^## REVISE", text, re.MULTILINE) or
            re.search(r"^## OUT_OF_SCOPE", text, re.MULTILINE)):
        return "missing ## REVISE or ## OUT_OF_SCOPE section"
    return None


def run_note_review(asn_path, asn_label, *, model="opus", effort="max"):
    """Run a single review pass on a note. Returns (verdict, text, elapsed).

    Assembles the prompt (template + vocab + foundation + scope/hints),
    invokes Claude, validates the response structure, strips preamble,
    parses the VERDICT line. Pure with respect to the substrate — no
    file writes, no link emission. Caller commits with `commit_note_review`.

    On invocation failure or malformed response, returns ("ERROR", text, elapsed)
    with text possibly None.
    """
    asn_content = asn_path.read_text()
    vocabulary = read_file(resolve_campaign(asn_label).vocabulary_path)
    asn_number = int(asn_label.replace("ASN-", ""))
    out_of_scope = load_out_of_scope(asn_number)
    foundation = load_foundation_for_note(asn_path, asn_number)

    prompt = build_prompt(
        asn_content, vocabulary,
        out_of_scope=out_of_scope, asn_number=asn_number,
        foundation=foundation,
    )
    text, elapsed = invoke_claude(prompt, model=model, effort=effort)
    if not text:
        return "ERROR", None, elapsed

    text = strip_preamble(text)
    error = validate_review(text)
    if error:
        print(f"  MALFORMED REVIEW: {error}", file=sys.stderr)
        return "ERROR", text, elapsed

    m = re.search(r"^VERDICT:\s*(\w+)", text, re.MULTILINE)
    verdict = m.group(1).upper() if m else "REVISE"
    return verdict, text, elapsed


def commit_note_review(store, asn_path, asn_label, text):
    """Write the review file (sequential numbering) and emit substrate
    links: `review` classifier on the file, `comment.{revise|out-of-scope}`
    per finding. Returns (review_path, findings).

    Caller passes a store so the convergence orchestrator can share one
    store instance across the cycle. Single-pass invocations
    (note-review.py) open their own store via `with default_store()`.
    """
    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
    existing = sorted_reviews(asn_label)
    next_num = 1
    for f in existing:
        m = re.search(r"review-(\d+)\.md$", f.name)
        if m:
            next_num = max(next_num, int(m.group(1)) + 1)
    output_path = REVIEWS_DIR / asn_label / f"review-{next_num}.md"
    output_path.write_text(text + "\n")

    findings = extract_note_findings(text)
    review_stem = f"review-{next_num}"
    emit_review(store, output_path)
    emit_note_findings(
        store, asn_path, findings,
        asn_label=asn_label, review_stem=review_stem,
        findings_dir=NOTE_FINDINGS_DIR,
    )
    return output_path, findings


def extract_note_findings(text):
    """Extract note-review findings, classified by parent section.

    Note reviews have top-level `## REVISE` and `## OUT_OF_SCOPE` sections,
    each containing `### Title` subheadings. Returns list of
    (title, cls, body) tuples where cls ∈ {"REVISE", "OUT_OF_SCOPE"}.
    Other top-level sections (e.g. `## RESOLVED`) are ignored — they are
    not findings against the note.
    """
    findings = []
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    for part in parts[1:]:  # skip preamble before first ##
        section_lines = part.split("\n", 1)
        section_header = section_lines[0].strip()
        section_body = section_lines[1] if len(section_lines) > 1 else ""
        if section_header == "REVISE":
            cls = "REVISE"
        elif section_header == "OUT_OF_SCOPE":
            cls = "OUT_OF_SCOPE"
        else:
            continue
        finding_parts = re.split(r"^### ", section_body, flags=re.MULTILINE)
        for fpart in finding_parts[1:]:
            lines = fpart.strip().split("\n", 1)
            title = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            findings.append((title, cls, f"### {title}\n{body}"))
    return findings


def invoke_claude(prompt, model="opus", effort="max"):
    """Call claude --print with --tools "". Returns plain text response."""
    model_flag = {
        "opus": "claude-opus-4-7",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "--print",
        "--model", model_flag,
        "--tools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n"):
                print(f"    stderr: {line}", file=sys.stderr)
        if result.stdout:
            stdout_len = len(result.stdout)
            print(f"    stdout: {stdout_len} chars partial output",
                  file=sys.stderr)
            # Show last 500 chars to see where it stopped
            tail = result.stdout[-500:]
            print(f"    stdout tail: ...{tail}", file=sys.stderr)
        else:
            print(f"    stdout: empty", file=sys.stderr)
        return "", elapsed

    print(f"  [{elapsed:.0f}s]", file=sys.stderr)
    return result.stdout.strip(), elapsed


def log_usage(asn_label, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "review",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(description="Review an ASN for rigor")
    parser.add_argument("asn", help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompt size without invoking Claude")
    args = parser.parse_args()

    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in {NOTES_DIR.relative_to(WORKSPACE)}/",
              file=sys.stderr)
        sys.exit(1)

    print(f"  [REVIEW] {asn_label}", file=sys.stderr)
    asn_number = int(asn_label.replace("ASN-", ""))
    out_of_scope = load_out_of_scope(asn_number)
    if out_of_scope:
        print(f"  [SCOPE] Out of scope: {out_of_scope}", file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Would invoke {args.model} with --tools "" effort {args.effort}",
              file=sys.stderr)
        return

    verdict, text, elapsed = run_note_review(
        asn_path, asn_label, model=args.model, effort=args.effort,
    )
    if verdict == "ERROR" or not text:
        print("  No review produced", file=sys.stderr)
        sys.exit(1)

    with default_store() as store:
        output_path, findings = commit_note_review(store, asn_path, asn_label, text)

    if findings:
        revise_count = sum(1 for _, c, _ in findings if c == "REVISE")
        oos_count = len(findings) - revise_count
        print(
            f"  [FINDINGS] {revise_count} REVISE, {oos_count} OUT_OF_SCOPE "
            f"emitted to {NOTE_FINDINGS_DIR.relative_to(WORKSPACE)}/"
            f"{asn_label}/{output_path.parent.name}/",
            file=sys.stderr,
        )

    process_resolved_issues(asn_number, text)
    print(f"  [VERDICT] {verdict}", file=sys.stderr)
    log_usage(asn_label, elapsed)

    # Print output file path to stdout (for pipeline consumption)
    print(str(output_path))
    print(f"  [WROTE] {output_path.relative_to(WORKSPACE)}", file=sys.stderr)

    if verdict == "CONVERGED":
        sys.exit(2)


if __name__ == "__main__":
    main()
