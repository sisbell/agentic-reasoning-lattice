"""Note-review agent body.

One LLM invocation: assemble prompt (template + ASN content + vocab +
foundation + open issues + scope hints), call Claude with --tools "",
validate the response structure, parse out the verdict and finding
sections.

Public entry: `run_note_review(asn_path, asn_label, *, model, effort)
-> (verdict, text, elapsed)`.

Also exports `extract_note_findings(text)` for orchestrator-side
parsing of a stored review document into (title, cls, body) tuples.
"""

from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path
from typing import List, Tuple

from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.foundation import load_foundation_for_note
from lib.shared.paths import LATTICE_PROMPTS, WORKSPACE, load_inquiry


PROMPTS_DIR = LATTICE_PROMPTS / "discovery"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"


def run_note_review(
    asn_path: Path,
    asn_label: str,
    *,
    model: str = "opus",
    effort: str = "max",
) -> Tuple[str, str, float]:
    """Run a single review pass on a note. Returns (verdict, text, elapsed).

    Assembles the prompt (template + vocab + foundation + scope/hints),
    invokes Claude, validates the response structure, strips preamble,
    parses the VERDICT line. Pure with respect to the substrate — no
    file writes, no link emission. Caller is responsible for committing
    the review and emitting findings.

    On invocation failure or malformed response, returns
    ("ERROR", text, elapsed) with text possibly None.
    """
    asn_content = asn_path.read_text()
    vocabulary = read_file(resolve_campaign(asn_label).vocabulary_path)
    asn_number = int(asn_label.replace("ASN-", ""))
    out_of_scope = _load_out_of_scope(asn_number)
    foundation = load_foundation_for_note(asn_path, asn_number)

    prompt = _build_prompt(
        asn_content, vocabulary,
        out_of_scope=out_of_scope,
        foundation=foundation,
    )
    text, elapsed = _invoke_claude(prompt, model=model, effort=effort)
    if not text:
        return "ERROR", None, elapsed

    text = _strip_preamble(text)
    error = _validate_review(text)
    if error:
        import sys
        print(f"  MALFORMED REVIEW: {error}", file=sys.stderr)
        return "ERROR", text, elapsed

    m = re.search(r"^VERDICT:\s*(\w+)", text, re.MULTILINE)
    verdict = m.group(1).upper() if m else "REVISE"
    return verdict, text, elapsed


def extract_note_findings(text: str) -> List[Tuple[str, str, str]]:
    """Extract note-review findings, classified by parent section.

    Note reviews have top-level `## REVISE` and `## OUT_OF_SCOPE` sections,
    each containing `### Title` subheadings. Returns list of
    (title, cls, body) tuples where cls ∈ {"REVISE", "OUT_OF_SCOPE"}.
    Other top-level sections (e.g. `## RESOLVED`) are ignored — they
    are not findings against the note.
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


# ---------------------------------------------------------------------------
# Prompt context loaders


def _load_out_of_scope(asn_number: int) -> str:
    """Look up out_of_scope for an ASN from its inquiry frontmatter."""
    return load_inquiry(asn_number).get("out_of_scope", "")


# ---------------------------------------------------------------------------
# Prompt rendering


def _build_prompt(
    asn_content: str, vocabulary: str, out_of_scope: str = "",
    foundation: str = "",
) -> str:
    """Assemble review prompt from template + injected content.

    Caller supplies `foundation` directly. The template's foundation
    slot can be empty if the ASN has no upstream deps.
    """
    template_path = REVIEW_TEMPLATE
    template = read_file(template_path)
    if not template:
        import sys
        print(
            f"  Review prompt template not found at "
            f"{template_path.relative_to(WORKSPACE)}",
            file=sys.stderr,
        )
        sys.exit(1)

    scope_note = (
        f"\n\n## Scope\n\nThe following topics are OUT OF SCOPE for this "
        f"ASN. Do not flag missing coverage for them. If the ASN defines "
        f"claims for these topics, flag them as OUT_OF_SCOPE: "
        f"{out_of_scope}"
        if out_of_scope else ""
    )

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{vocabulary}}", vocabulary
    ).replace(
        "{{foundation_statements}}", foundation
    ) + scope_note


# ---------------------------------------------------------------------------
# Response validation


def _strip_preamble(text: str) -> str:
    """Strip any tool-use preamble before the review header."""
    marker = re.search(r"^# Review of ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def _validate_review(text: str):
    """Check that review text has required structure. Returns error message or None."""
    if not re.search(r"^# Review of ASN-\d+", text, re.MULTILINE):
        return "missing '# Review of ASN-NNNN' header"
    if not re.search(r"^VERDICT:\s*\w+", text, re.MULTILINE):
        return "missing VERDICT line"
    if not (
        re.search(r"^## REVISE", text, re.MULTILINE)
        or re.search(r"^## OUT_OF_SCOPE", text, re.MULTILINE)
    ):
        return "missing ## REVISE or ## OUT_OF_SCOPE section"
    return None


# ---------------------------------------------------------------------------
# Claude invocation


def _invoke_claude(prompt: str, *, model: str, effort: str):
    """Call claude --print with --tools "". Returns (text, elapsed)."""
    import sys
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
        print(
            f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
            file=sys.stderr,
        )
        if result.stderr:
            for line in result.stderr.strip().split("\n"):
                print(f"    stderr: {line}", file=sys.stderr)
        if result.stdout:
            stdout_len = len(result.stdout)
            print(
                f"    stdout: {stdout_len} chars partial output",
                file=sys.stderr,
            )
            tail = result.stdout[-500:]
            print(f"    stdout tail: ...{tail}", file=sys.stderr)
        else:
            print("    stdout: empty", file=sys.stderr)
        return "", elapsed

    print(f"  [{elapsed:.0f}s]", file=sys.stderr)
    return result.stdout.strip(), elapsed
