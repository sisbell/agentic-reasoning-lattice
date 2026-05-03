#!/usr/bin/env python3
"""
Revise an ASN based on review feedback.

Loads the discovery prompt (methodology, notation, rigor standards),
injects vocabulary, appends the review content, and runs claude -p
with tools so the agent can read the ASN, make targeted fixes, and
consult the configured channels if needed.

Usage:
    python scripts/lib/review_revise.py 9              # ASN-0009 + latest review
    python scripts/lib/review_revise.py 9 review-1     # ASN-0009 + specific review
    python scripts/lib/review_revise.py 9 -m sonnet    # use sonnet instead of opus
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
from lib.shared.paths import WORKSPACE, LATTICE, VOCABULARY, REVIEWS_DIR, USAGE_LOG, NOTE_DIR, LATTICE_PROMPTS, sorted_reviews, find_review
from lib.shared.campaign import resolve_campaign
from lib.shared.common import find_asn, read_file
from lib.shared.foundation import load_foundation_for_note
from lib.backend.predicates import unresolved_revise_comments
from lib.backend.store import default_store

PROMPTS_DIR = LATTICE_PROMPTS / "discovery"
DISCOVERY_PROMPT = PROMPTS_DIR / "instructions.md"

MODEL = "claude-opus-4-7"


def build_prompt(asn_path, findings, vocab, consultation_content=None, asn_number=None):
    """Build revise prompt: discovery methodology + per-finding instructions.

    `findings` is a list of (comment_id, title, body) tuples — one per
    open `comment.revise` link on the note. The agent is instructed to
    address each in the note md and call convergence-link-resolution.py per finding to close
    the comment in the substrate.
    """
    skill_body = read_file(DISCOVERY_PROMPT)
    if not skill_body:
        print(f"  Discovery prompt not found at {DISCOVERY_PROMPT.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    parts = [skill_body]

    if vocab:
        parts.append(f"## Shared Vocabulary\n\n{vocab}")

    foundation = load_foundation_for_note(asn_path, asn_number)
    if foundation:
        parts.append(foundation)

    rel_path = asn_path.relative_to(WORKSPACE)
    asn_label = re.match(r"(ASN-\d+)", asn_path.stem).group(1)

    assignment = f"""## Your Assignment: REVISE {asn_label}

You are revising an existing ASN based on per-finding review feedback.
Read the ASN at `{rel_path}`, then address each finding below.

**Do not rewrite the ASN from scratch.** Make targeted fixes per finding.
Preserve the existing structure, notation, and reasoning where it is not
affected by the finding.

Write the revised ASN back to `{rel_path}`.

For each finding below, after you have addressed it (either by editing
the note or by deciding the finding is incorrect), close the
corresponding comment in the link store:

  python scripts/convergence-link-resolution.py accept --comment-id <id>
  python scripts/convergence-link-resolution.py reject --comment-id <id> --rationale "<one or two sentences>"

`accept` means you applied the fix; `reject` means the finding is
incorrect and you wrote a rationale instead. Do this once per finding."""

    if consultation_content:
        assignment += f"""

## Consultation Results

The following expert consultations were conducted based on the review.
Use these answers as evidence when addressing the corresponding findings.

{consultation_content}"""

    assignment += "\n\n## Findings\n"
    for n, (comment_id, title, body) in enumerate(findings, 1):
        assignment += (
            f"\n### Finding {n}: {title}\n"
            f"**Comment ID:** `{comment_id}`\n\n"
            f"{body}\n"
        )

    parts.append(assignment)

    return "\n\n".join(parts)


def invoke_claude(prompt, model=None, effort="max"):
    """Run claude -p with tools. Returns parsed JSON output."""
    use_model = model or MODEL
    cmd = [
        "claude", "-p",
        "--model", use_model,
        "--output-format", "json",
        "--allowedTools", "Edit,Bash,Write,Read,Glob,Grep",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, elapsed

    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)
        num_turns = data.get("num_turns", 0)

        print(f"  [{elapsed:.0f}s] in:{inp} out:{out} turns:{num_turns} ${cost:.4f}",
              file=sys.stderr)

        return data, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return None, elapsed


def log_usage(asn_label, elapsed, data):
    """Append a usage entry to the log."""
    if data is None:
        return
    usage = data.get("usage", {})
    cost = data.get("total_cost_usd", 0)
    inp = (usage.get("input_tokens", 0) +
           usage.get("cache_read_input_tokens", 0) +
           usage.get("cache_creation_input_tokens", 0))
    out = usage.get("output_tokens", 0)

    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "revise",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
            "input_tokens": inp,
            "output_tokens": out,
            "num_turns": data.get("num_turns", 0),
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def collect_open_revises(store, note_rel):
    """Return list of (comment_addr, title, body) for unresolved revise comments
    on the note.

    Reads each comment's source finding doc to get the finding text. Title
    is the first non-blank line of the body, stripped of `### ` if present.
    """
    items = []
    note_addr = store.path_to_addr.get(note_rel)
    if note_addr is None:
        return items
    for c in unresolved_revise_comments(store.state, note_addr):
        if not c.from_set:
            continue
        finding_addr = c.from_set[0]
        finding_rel = store.path_for_addr(finding_addr)
        if not finding_rel:
            continue
        finding_full = LATTICE / finding_rel
        if not finding_full.exists():
            print(f"  [SKIP] finding doc missing: {finding_rel}",
                  file=sys.stderr)
            continue
        body = finding_full.read_text().strip()
        first_line = body.splitlines()[0] if body else ""
        title = re.sub(r"^#+\s*", "", first_line).strip() or "(untitled)"
        items.append((c.addr, title, body))
    return items


def run_revise_pass(asn_path, asn_label, findings, *,
                    model="opus", effort="max", consultation_content=None):
    """Run one reviser invocation that addresses `findings`.

    Sets PROTOCOL_ASN_LABEL env var. The agent
    closes each comment via `convergence-link-resolution.py --comment-id <id>` per the prompt.
    Returns (data, elapsed) from invoke_claude — caller logs usage and
    re-queries the substrate for remaining open revises.
    """
    asn_num = int(re.sub(r"[^0-9]", "", asn_label))
    vocab = read_file(resolve_campaign(asn_label).vocabulary_path)
    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))

    prompt = build_prompt(asn_path, findings, vocab, consultation_content,
                          asn_number=asn_num)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens)",
          file=sys.stderr)

    model_flag = {
        "opus": "claude-opus-4-7",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    os.environ["PROTOCOL_ASN_LABEL"] = asn_label

    return invoke_claude(prompt, model=model_flag, effort=effort)


def main():
    parser = argparse.ArgumentParser(description="Revise an ASN based on review feedback")
    parser.add_argument("asn", help="ASN number (e.g., 9, 0009, ASN-0009)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--consultation",
                        help="Path to consultation results file (from consult_for_revision.py)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in {NOTE_DIR.relative_to(WORKSPACE)}/", file=sys.stderr)
        sys.exit(1)

    note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))

    store = default_store(LATTICE)
    findings = collect_open_revises(store, note_rel)

    if not findings:
        print(f"  [CONVERGED] No open revise comments on {asn_label}",
              file=sys.stderr)
        print(str(asn_path))
        sys.exit(2)

    print(f"  [REVISE] {asn_label} ({asn_path.name}) — "
          f"{len(findings)} open finding(s)", file=sys.stderr)

    consultation_content = None
    if args.consultation:
        consultation_content = read_file(args.consultation)
        if not consultation_content:
            print(f"  Warning: consultation file not found: {args.consultation}",
                  file=sys.stderr)
            consultation_content = None
        else:
            print(f"  [CONSULTATION] {Path(args.consultation).name}",
                  file=sys.stderr)

    data, elapsed = run_revise_pass(
        asn_path, asn_label, findings,
        model=args.model, effort=args.effort,
        consultation_content=consultation_content,
    )
    if data is None:
        print("  Revision failed", file=sys.stderr)
        sys.exit(1)
    log_usage(asn_label, elapsed, data)

    store = default_store(LATTICE)
    remaining = collect_open_revises(store, note_rel)

    closed_count = len(findings) - len(remaining)
    print(f"  [CLOSED] {closed_count}/{len(findings)} comment(s) "
          f"resolved this session", file=sys.stderr)

    if remaining:
        print(f"  [OPEN] {len(remaining)} comment(s) still need revision:",
              file=sys.stderr)
        for _, title, _ in remaining:
            print(f"    - {title}", file=sys.stderr)

    print(str(asn_path))
    if not remaining:
        sys.exit(2)  # convergence signal


if __name__ == "__main__":
    main()
