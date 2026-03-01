#!/usr/bin/env python3
"""
Triage review DEFER items for a single ASN — decide which spawn new inquiries.

Extracts DEFER sections from the ASN's review files, checks against existing
inquiries and previous triage, invokes Claude to evaluate each topic, and
updates inquiries.yaml for qualifying topics.

Usage:
    python scripts/triage-defers.py 4
    python scripts/triage-defers.py 14 --dry-run
    python scripts/triage-defers.py 4 --model sonnet
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import yaml

from pathlib import Path

from paths import WORKSPACE, REVIEWS_DIR, INQUIRIES_FILE, TRIAGE_DIR, USAGE_LOG

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts"
TRIAGE_TEMPLATE = PROMPTS_DIR / "triage-defers.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn_label(asn_id):
    """Normalize ASN identifier to label like ASN-0004."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None
    return f"ASN-{int(num):04d}"


def extract_defers(reviews_dir, asn_label):
    """Extract DEFER sections from an ASN's review files.

    Returns a string with each defer block labeled by source review.
    """
    review_files = sorted(reviews_dir.glob(f"{asn_label}-review-*.md"))
    if not review_files:
        return ""

    blocks = []
    for rf in review_files:
        text = rf.read_text()
        # Find the ## DEFER section
        defer_match = re.search(r"^## DEFER\b.*$", text, re.MULTILINE)
        if not defer_match:
            continue

        # Extract from ## DEFER to end of file or next ## section
        rest = text[defer_match.end():]
        next_section = re.search(r"^## ", rest, re.MULTILINE)
        if next_section:
            defer_content = rest[:next_section.start()].strip()
        else:
            # Strip META line if present at end
            defer_content = re.sub(r"\nMETA:.*$", "", rest).strip()

        if not defer_content:
            continue

        # Label with source file
        label = rf.stem  # e.g. ASN-0004-review-2
        blocks.append(f"### From {label}\n\n{defer_content}")

    return "\n\n".join(blocks)


def load_inquiries():
    """Load inquiries.yaml and return (data_dict, raw_text)."""
    raw = read_file(INQUIRIES_FILE)
    if not raw:
        return {"inquiries": []}, ""
    data = yaml.safe_load(raw)
    return data, raw


def next_inquiry_id(data):
    """Compute the next available inquiry ID."""
    max_id = 0
    for inq in data.get("inquiries", []):
        if inq.get("id", 0) > max_id:
            max_id = inq["id"]
    return max_id + 1


def build_prompt(defer_items, inquiries_text, existing_triage):
    """Assemble triage prompt from template + injected content."""
    template = read_file(TRIAGE_TEMPLATE)
    if not template:
        print("  Triage prompt template not found at scripts/prompts/triage-defers.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{defer_items}}", defer_items
    ).replace(
        "{{inquiries}}", inquiries_text
    ).replace(
        "{{existing_triage}}", existing_triage or "(No previous triage.)"
    )


def strip_preamble(text):
    """Strip any preamble before the triage header."""
    marker = re.search(r"^# Triage: Review Deferrals", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def invoke_claude(prompt, model="opus", effort="max"):
    """Call claude --print with --tools "". Returns plain text response."""
    model_flag = {
        "opus": "claude-opus-4-6",
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
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return "", elapsed

    print(f"  [{elapsed:.0f}s]", file=sys.stderr)
    return result.stdout.strip(), elapsed


def parse_promoted(text):
    """Extract promoted inquiry metadata from triage markdown."""
    inquiries = []
    in_promoted = False
    current = None

    for line in text.split("\n"):
        stripped = line.strip()

        if stripped.startswith("## Promoted"):
            in_promoted = True
            continue
        if stripped.startswith("## Declined"):
            in_promoted = False
            if current:
                inquiries.append(current)
                current = None
            continue

        if not in_promoted:
            continue

        # New promoted topic
        if stripped.startswith("- **"):
            if current:
                inquiries.append(current)
            current = {}
            continue

        if current is None:
            continue

        # Parse metadata lines
        if stripped.startswith("- Title:"):
            current["title"] = stripped[len("- Title:"):].strip()
        elif stripped.startswith("- Question:"):
            current["question"] = stripped[len("- Question:"):].strip()
        elif stripped.startswith("- Area:"):
            current["area"] = stripped[len("- Area:"):].strip()
        elif stripped.startswith("- Nelson:"):
            current["nelson"] = int(stripped[len("- Nelson:"):].strip())
        elif stripped.startswith("- Gregory:"):
            current["gregory"] = int(stripped[len("- Gregory:"):].strip())

    if current:
        inquiries.append(current)

    return inquiries


def append_inquiry_yaml(data, inquiry, next_id):
    """Append a new inquiry to the YAML data structure."""
    entry = {
        "id": next_id,
        "title": inquiry["title"],
        "question": inquiry["question"],
        "area": inquiry["area"],
        "source": "review-defer triage",
    }
    nelson = inquiry.get("nelson", 10)
    gregory = inquiry.get("gregory", 10)
    if nelson != 10 or gregory != 10:
        entry["agents"] = {"nelson": nelson, "gregory": gregory}

    data["inquiries"].append(entry)
    return entry


def write_inquiries_yaml(data):
    """Write inquiries.yaml preserving the header comments."""
    header = """# Inquiries — Abstract questions that drive ASN generation
#
# Each inquiry produces one independent ASN.
# Questions are framed abstractly to prevent implementation drift.
# New inquiries can be added from ASN open questions.
#
# agents.nelson — number of Nelson sub-questions (default: 10)
# agents.gregory — number of Gregory sub-questions (default: 10)
# Set either to 0 to skip that expert. Set to 1 for a focused follow-up.

"""
    lines = ["inquiries:"]
    for inq in data["inquiries"]:
        lines.append(f"  - id: {inq['id']}")
        lines.append(f'    title: "{inq["title"]}"')
        q = inq["question"]
        lines.append(f'    question: "{q}"')
        lines.append(f"    area: {inq['area']}")
        if "source" in inq:
            lines.append(f'    source: "{inq["source"]}"')
        if "agents" in inq:
            agents = inq["agents"]
            lines.append("    agents:")
            lines.append(f"      nelson: {agents.get('nelson', 10)}")
            lines.append(f"      gregory: {agents.get('gregory', 10)}")
        lines.append("")

    INQUIRIES_FILE.write_text(header + "\n".join(lines) + "\n")


def log_usage(asn_label, elapsed):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "triage-defers",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Triage review DEFER items into new inquiries")
    parser.add_argument("asn", help="ASN number (e.g., 4, 0004, ASN-0004)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show extracted defers and prompt size without invoking Claude")
    args = parser.parse_args()

    # Resolve ASN label
    asn_label = find_asn_label(args.asn)
    if not asn_label:
        print(f"  Invalid ASN identifier: {args.asn}", file=sys.stderr)
        sys.exit(1)

    # Extract DEFER sections from this ASN's reviews
    defer_items = extract_defers(REVIEWS_DIR, asn_label)
    if not defer_items:
        print(f"  No DEFER sections found in {asn_label} reviews", file=sys.stderr)
        sys.exit(0)

    # Count defer topics
    topic_count = len(re.findall(r"^### Topic \d+", defer_items, re.MULTILINE))
    review_count = len(re.findall(r"^### From ", defer_items, re.MULTILINE))
    print(f"  [TRIAGE-DEFERS] {asn_label}: {topic_count} topics from {review_count} reviews",
          file=sys.stderr)

    # Load inquiries and existing triage for this ASN
    inq_data, inq_text = load_inquiries()
    triage_path = TRIAGE_DIR / f"{asn_label}-defers.md"
    existing_triage = read_file(triage_path)

    # Build prompt
    prompt = build_prompt(defer_items, inq_text, existing_triage)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if args.dry_run:
        print(f"\n  [DRY RUN] Would invoke {args.model} with --tools \"\"",
              file=sys.stderr)
        print("\n--- Extracted DEFER items ---\n")
        print(defer_items)
        return

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)

    if not text:
        print("  No response produced", file=sys.stderr)
        sys.exit(1)

    # Strip any preamble
    text = strip_preamble(text)

    # Parse promoted inquiries
    promoted = parse_promoted(text)

    # Display summary
    if promoted:
        print(f"\n  {len(promoted)} new inquiry/inquiries:", file=sys.stderr)
        for ni in promoted:
            n = ni.get("nelson", 10)
            g = ni.get("gregory", 10)
            print(f"    -> {ni.get('title', '?')} [{ni.get('area', '?')}] "
                  f"(nelson:{n} gregory:{g})", file=sys.stderr)
    else:
        print(f"\n  No new inquiries from {asn_label} deferrals", file=sys.stderr)

    # Write triage file (one per ASN, updated in place)
    TRIAGE_DIR.mkdir(parents=True, exist_ok=True)
    triage_path.write_text(text + "\n")
    print(f"  [WROTE] {triage_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Update inquiries.yaml if promoted
    if promoted:
        cur_id = next_inquiry_id(inq_data)
        for ni in promoted:
            if "title" in ni and "question" in ni and "area" in ni:
                append_inquiry_yaml(inq_data, ni, cur_id)
                print(f"  [ADD] Inquiry {cur_id}: {ni['title']}", file=sys.stderr)
                cur_id += 1

        write_inquiries_yaml(inq_data)
        print(f"  [UPDATED] {INQUIRIES_FILE.relative_to(WORKSPACE)}",
              file=sys.stderr)

    # Log usage
    log_usage(asn_label, elapsed)

    # Print full triage report
    print(text)


if __name__ == "__main__":
    main()
