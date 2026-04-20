#!/usr/bin/env python3
"""
Discovery — synthesize expert consultation answers into a formal ASN.

Reads consultation answers from lattices/xanadu/discovery/consultations/ASN-NNNN/consultation/answers.md,
loads the discovery prompt template, and calls claude -p to write
the ASN. Requires consultation answers to exist — run consult-experts.py first.

Output: lattices/xanadu/discovery/notes/ASN-NNNN-title.md

Usage:
    python scripts/lib/draft_discover.py --inquiry-id 4
    python scripts/lib/draft_discover.py --inquiry-id 4 --force   # overwrite existing ASN
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
from lib.shared.paths import WORKSPACE, NOTES_DIR, VOCABULARY, USAGE_LOG, consultation_dir, load_manifest
from lib.shared.foundation import load_foundation_statements

DISCOVERY_PROMPT = WORKSPACE / "scripts" / "prompts" / "discovery" / "instructions.md"

MODEL = "claude-opus-4-7"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def load_prompt(path):
    """Load prompt template file."""
    content = read_file(path)
    if not content:
        print(f"  [ERROR] Prompt not found: {path}", file=sys.stderr)
        sys.exit(1)
    return content


def load_inquiry(inquiry_id):
    """Load inquiry from project model manifest."""
    manifest = load_manifest(inquiry_id)
    if not manifest:
        print(f"  [ERROR] Manifest not found for ASN-{inquiry_id:04d}", file=sys.stderr)
        sys.exit(1)
    inquiry = manifest.get("consultations", {})
    return {
        "id": inquiry_id,
        "title": manifest.get("title", ""),
        "question": inquiry.get("question", ""),
        "out_of_scope": manifest.get("out_of_scope", ""),
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


def build_discovery_prompt(answers_content):
    """Build the discovery skill with consultation answers injected.

    Inserts answers after the Starting Point section (topic → data → method)
    and updates consultation instructions to note answers are available.
    """
    skill_body = load_prompt(DISCOVERY_PROMPT)

    # Insert answers after "## Starting Point" section
    starting_marker = "## Starting Point"
    sp_start = skill_body.find(starting_marker)
    if sp_start != -1:
        sp_end = skill_body.find("---", sp_start)
        if sp_end != -1:
            answers_section = f"""---

## Expert Consultation Answers

Nelson answered questions about design intent; Gregory answered questions about implementation behavior. These answers are your primary input for this ASN.

**Use these results as your foundation.** Synthesize these answers into a formal specification.

<details>
<summary>Consultation Answers (click to expand)</summary>

{answers_content}

</details>

"""
            skill_body = skill_body[:sp_end] + answers_section + skill_body[sp_end:]

    # Update the consultation section to note answers are available
    consult_marker = "### Consultation Order: Nelson First"
    consult_start = skill_body.find(consult_marker)
    if consult_start != -1:
        consult_end = skill_body.find("---", consult_start)
        if consult_end != -1:
            skill_body = skill_body[:consult_start] + """### Expert Answers Available

Consultation answers are provided above. They contain focused answers from Nelson (design intent) and Gregory (implementation evidence) on your topic. **Read them first** — they are your primary evidence base.

Do not run ad-hoc expert consultations during discovery. All consultation was done upstream. Focus on synthesizing the provided answers into a formal specification.

""" + skill_body[consult_end:]

    return skill_body


def run_discovery(inquiry, asn_number, slug, force=False):
    """Run xan-discovery to write the ASN. Returns path to ASN file or None."""
    outfile = NOTES_DIR / f"ASN-{asn_number:04d}-{slug}.md"

    if outfile.exists() and not force:
        print(f"  [SKIP] {outfile.name} already exists (use --force to overwrite)",
              file=sys.stderr)
        return outfile

    # Require consultation answers
    answers_path = consultation_dir(asn_number) / "consultation" / "answers.md"
    if not answers_path.exists():
        print(f"  [ERROR] No consultation answers at {answers_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        print(f"  Run consult-experts.py first: python scripts/consult-experts.py --inquiry-id {asn_number}",
              file=sys.stderr)
        return None

    answers_content = answers_path.read_text()
    skill_body = build_discovery_prompt(answers_content)
    print(f"  [DISCOVERY] Using answers from {answers_path.relative_to(WORKSPACE)}",
          file=sys.stderr)

    vocab = read_file(VOCABULARY)
    prompt_parts = [skill_body]

    if vocab:
        prompt_parts.append(f"## Shared Vocabulary\n\n{vocab}")

    foundation = load_foundation_statements(asn_number)
    if foundation:
        prompt_parts.append(foundation)

    out_of_scope = inquiry.get("out_of_scope", "")
    scope_note = (f"\n5. The following topics are OUT OF SCOPE for this ASN — "
                  f"do not define claims or operations for them, even if the "
                  f"consultation answers discuss them: {out_of_scope}"
                  if out_of_scope else "")

    assignment = f"""## Your Assignment

**ASN Number**: ASN-{asn_number:04d}
**Topic**: {inquiry['title']}
**Question**: {inquiry['question']}

Write ASN-{asn_number:04d} to `lattices/xanadu/discovery/notes/ASN-{asn_number:04d}-{slug}.md`.

Remember:
1. Read the consultation answers above — they are your primary input.
2. Synthesize Nelson's design intent with Gregory's implementation evidence.
3. Derive everything locally — do not reference other ASNs except foundation ASNs (provided above). Use foundation definitions for addressing, ordering, subspaces, and spans.
4. Claims must be abstract — would an alternative implementation need them?{scope_note}
"""
    prompt_parts.append(assignment)

    prompt = "\n\n".join(prompt_parts)
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

    written = list(NOTES_DIR.glob(f"ASN-{asn_number:04d}-*.md"))
    if written:
        actual = written[0]
        print(f"  [OK] {actual.name} ({actual.stat().st_size} bytes) [different filename]",
              file=sys.stderr)
        return actual

    print(f"  [WARN] ASN file not found — saving raw response", file=sys.stderr)
    response = data.get("result", "")
    if response:
        fallback = NOTES_DIR / f"ASN-{asn_number:04d}-{slug}-response.md"
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

    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"ASN-{asn_number:04d}: {inquiry['title']}", file=sys.stderr)

    asn_path = run_discovery(inquiry, asn_number, slug, force=args.force)

    if asn_path:
        # Print the output file path to stdout (for pipeline consumption)
        print(str(asn_path))
    else:
        print("  [FAILED] No ASN produced", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
