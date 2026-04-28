#!/usr/bin/env python3
"""
Discovery — synthesize expert consultation answers into a formal note.

Reads consultation answers from the lattice's consultations dir, loads
the domain's discovery prompt template, substitutes placeholders, and
calls claude -p to write the note.

The template (prompts/<lattice>/discovery/instructions.md, with shared
fallback at prompts/shared/discovery/instructions.md) is the
single source of truth for the prompt. Placeholders supplied by this
script: {{consultation_answers}}, {{asn_number}}, {{title}}, {{question}},
{{slug}}, {{foundation_section}}, {{vocabulary_section}}, {{out_of_scope_note}}.

Output: lattices/<lattice>/_store/documents/note/ASN-NNNN-title.md

Usage:
    python scripts/lib/consultation/draft.py --inquiry-id 4
    python scripts/lib/consultation/draft.py --inquiry-id 4 --force
"""

import argparse
import json
import os
import subprocess
import sys
import time
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, NOTE_DIR, VOCABULARY, USAGE_LOG, LATTICE_PROMPTS,
    consultation_dir, inquiry_doc_path,
    load_inquiry as load_inquiry_frontmatter,
)
from lib.shared.campaign import resolve_campaign
from lib.shared.common import read_file
from lib.shared.foundation import load_foundation_for_note
from lib.store.emit import emit_note, emit_synthesis
from lib.store.store import default_store

DISCOVERY_PROMPT = LATTICE_PROMPTS / "discovery" / "instructions.md"

MODEL = "claude-opus-4-7"


def load_prompt(path):
    """Load prompt template file."""
    content = read_file(path)
    if not content:
        print(f"  [ERROR] Prompt not found: {path}", file=sys.stderr)
        sys.exit(1)
    return content


def load_inquiry(inquiry_id):
    """Load inquiry content from substrate-managed inquiry doc."""
    fm = load_inquiry_frontmatter(inquiry_id)
    if not fm:
        print(f"  [ERROR] Inquiry doc not found for ASN-{inquiry_id:04d}",
              file=sys.stderr)
        sys.exit(1)
    return {
        "id": inquiry_id,
        "title": fm.get("title", ""),
        "question": fm.get("question", ""),
        "out_of_scope": fm.get("out_of_scope", ""),
    }


def slugify(title):
    """Convert title to filename-safe slug."""
    return title.lower().replace(" ", "-").replace("(", "").replace(")", "")


def log_usage(skill, asn_label, inquiry_title, area, elapsed, data):
    """Append a usage entry to the log."""
    usage = data.get("usage", {})
    cost = data.get("total_cost_usd", 0)
    inp = (usage.get("input_tokens", 0) +
           usage.get("cache_read_input_tokens", 0) +
           usage.get("cache_creation_input_tokens", 0))
    out = usage.get("output_tokens", 0)

    num_turns = data.get("num_turns", 0)
    print(f"  [{elapsed:.0f}s] in:{inp} out:{out} turns:{num_turns} ${cost:.4f}",
          file=sys.stderr)

    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "skill": skill,
        "asn": asn_label,
        "inquiry": inquiry_title,
        "area": area,
        "elapsed_s": round(elapsed, 1),
        "input_tokens": inp,
        "output_tokens": out,
        "num_turns": num_turns,
        "cost_usd": cost,
    }
    with open(USAGE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return cost


def invoke_claude(prompt, model=None, max_turns=30,
                  tools="Bash,Write,Read,Glob,Grep", effort="max"):
    """Run claude -p and return parsed JSON output."""
    use_model = model or MODEL
    cmd = [
        "claude", "-p",
        "--model", use_model,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--allowedTools", tools,
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
        print(f"  [FAILED] exit {result.returncode} ({elapsed:.0f}s)", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, elapsed

    try:
        data = json.loads(result.stdout)
        return data, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [ERROR] Could not parse JSON output ({elapsed:.0f}s)", file=sys.stderr)
        return None, elapsed


def build_discovery_prompt(inquiry, asn_number, slug, answers_content,
                           foundation, vocab, scope_note):
    """Build the discovery prompt by substituting placeholders in the template.

    The domain's instructions.md is the single source of truth; this function
    just fills in dynamic values. Section separators for the optional
    foundation and vocabulary blocks are encoded inside the substituted value
    (prefixed with \\n\\n) so the template stays clean and empty sections
    disappear cleanly.
    """
    template = load_prompt(DISCOVERY_PROMPT)
    vocab_section = f"\n\n## Shared Vocabulary\n\n{vocab}" if vocab else ""
    foundation_section = f"\n\n{foundation}" if foundation else ""
    return (template
        .replace("{{consultation_answers}}", answers_content)
        .replace("{{asn_number}}", f"ASN-{asn_number:04d}")
        .replace("{{title}}", inquiry["title"])
        .replace("{{question}}", inquiry["question"])
        .replace("{{slug}}", slug)
        .replace("{{foundation_section}}", foundation_section)
        .replace("{{vocabulary_section}}", vocab_section)
        .replace("{{out_of_scope_note}}", scope_note))


def run_discovery(inquiry, asn_number, slug, force=False):
    """Run xan-discovery to write the ASN. Returns path to ASN file or None."""
    outfile = NOTE_DIR / f"ASN-{asn_number:04d}-{slug}.md"

    if outfile.exists() and not force:
        print(f"  [SKIP] {outfile.name} already exists (use --force to overwrite)",
              file=sys.stderr)
        return outfile

    # Require consultation answers
    answers_path = consultation_dir(asn_number) / "consultation" / "answers.md"
    if not answers_path.exists():
        print(f"  [ERROR] No consultation answers at {answers_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        print(f"  Run decompose.py first: python scripts/lib/consultation/decompose.py --inquiry-id {asn_number}",
              file=sys.stderr)
        return None

    answers_content = answers_path.read_text()
    print(f"  [DISCOVERY] Using answers from {answers_path.relative_to(WORKSPACE)}",
          file=sys.stderr)

    vocab = read_file(resolve_campaign(asn_number).vocabulary_path)
    # Foundation deps come from substrate citations on the inquiry md.
    # Pre-draft, the user has already declared deps via cite.py against
    # the inquiry — the inquiry's citation graph is authoritative here.
    foundation = load_foundation_for_note(
        inquiry_doc_path(asn_number), asn_number,
    )
    out_of_scope = inquiry.get("out_of_scope", "")
    scope_note = (f"\n5. The following topics are OUT OF SCOPE for this ASN — "
                  f"do not define claims or operations for them, even if the "
                  f"consultation answers discuss them: {out_of_scope}"
                  if out_of_scope else "")

    prompt = build_discovery_prompt(
        inquiry, asn_number, slug, answers_content,
        foundation, vocab, scope_note,
    )
    print(f"  [DISCOVERY] {len(prompt)} chars (~{len(prompt)//4} tokens)",
          file=sys.stderr)

    data, elapsed = invoke_claude(prompt)
    if data is None:
        return None

    log_usage("discovery", f"ASN-{asn_number:04d}", inquiry["title"],
              inquiry.get("area", ""), elapsed, data)

    # Find the written ASN file
    if outfile.exists():
        print(f"  [OK] {outfile.name} ({outfile.stat().st_size} bytes)",
              file=sys.stderr)
        return outfile

    written = list(NOTE_DIR.glob(f"ASN-{asn_number:04d}-*.md"))
    if written:
        actual = written[0]
        print(f"  [OK] {actual.name} ({actual.stat().st_size} bytes) [different filename]",
              file=sys.stderr)
        return actual

    print(f"  [WARN] ASN file not found — saving raw response", file=sys.stderr)
    response = data.get("result", "")
    if response:
        fallback = NOTE_DIR / f"ASN-{asn_number:04d}-{slug}-response.md"
        fallback.write_text(response)
        return fallback

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Discovery: synthesize expert answers into a formal ASN")
    parser.add_argument("--inquiry-id", type=int, required=True,
                        help="Inquiry ID from inquiries.yaml")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing ASN")
    args = parser.parse_args()

    inquiry = load_inquiry(args.inquiry_id)
    asn_number = inquiry["id"]
    slug = slugify(inquiry["title"])

    NOTE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"ASN-{asn_number:04d}: {inquiry['title']}", file=sys.stderr)

    asn_path = run_discovery(inquiry, asn_number, slug, force=args.force)

    if asn_path:
        with default_store() as store:
            _, note_created = emit_note(store, asn_path)
            if note_created:
                print(f"  [NOTE] classifier emitted", file=sys.stderr)
            inq_path = inquiry_doc_path(asn_number)
            if inq_path.exists():
                _, syn_created = emit_synthesis(store, inq_path, asn_path)
                if syn_created:
                    print(f"  [SYNTHESIS] inquiry → note link emitted",
                          file=sys.stderr)
        # Print the output file path to stdout (for pipeline consumption)
        print(str(asn_path))
    else:
        print("  [FAILED] No ASN produced", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
