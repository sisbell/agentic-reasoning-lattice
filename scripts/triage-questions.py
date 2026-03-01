#!/usr/bin/env python3
"""
Triage ASN open questions — decide which spawn new inquiries.

Reads an ASN's open questions, checks what's already been triaged,
invokes Claude to evaluate each question, and updates inquiries.yaml
and vault/discovery/triage/ASN-NNNN.md for qualifying questions.

Usage:
    python scripts/triage-questions.py 12
    python scripts/triage-questions.py 13 --dry-run
    python scripts/triage-questions.py 4 --model sonnet
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

from paths import WORKSPACE, ASNS_DIR, INQUIRIES_FILE, TRIAGE_DIR, USAGE_LOG

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts"
TRIAGE_TEMPLATE = PROMPTS_DIR / "triage-questions.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id):
    """Find ASN file by number."""
    path = Path(asn_id)
    if path.exists():
        label = re.match(r"(ASN-\d+)", path.stem)
        return path, label.group(1) if label else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    matches = sorted(ASNS_DIR.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


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


def build_prompt(asn_content, inquiries_text, existing_triage):
    """Assemble triage prompt from template + injected content."""
    template = read_file(TRIAGE_TEMPLATE)
    if not template:
        print("  Triage prompt template not found at scripts/prompts/triage-questions.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{asn_content}}", asn_content
    ).replace(
        "{{inquiries}}", inquiries_text
    ).replace(
        "{{existing_triage}}", existing_triage
    )


def invoke_claude(prompt, model="opus", effort="max"):
    """Call claude --print. Returns plain text response."""
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

        # New promoted question
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
        "source": f"ASN triage",
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
            "skill": "triage-questions",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Triage ASN open questions into new inquiries")
    parser.add_argument("asn", help="ASN number (e.g., 12, 0012, ASN-0012)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show output without updating files")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/modeling/asns/", file=sys.stderr)
        sys.exit(1)

    asn_content = asn_path.read_text()

    # Load current state
    inq_data, inq_text = load_inquiries()
    existing_triage = read_file(TRIAGE_DIR / f"{asn_label}.md")

    # Build prompt
    print(f"  [TRIAGE] {asn_label}", file=sys.stderr)
    prompt = build_prompt(asn_content, inq_text, existing_triage)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    # Invoke Claude
    text, elapsed = invoke_claude(prompt, model=args.model, effort=args.effort)

    if not text:
        print("  No response produced", file=sys.stderr)
        sys.exit(1)

    # Parse promoted inquiries from markdown
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
        print(f"\n  No new inquiries from {asn_label}", file=sys.stderr)

    if args.dry_run:
        print(f"\n  [DRY RUN] Would write triage file", file=sys.stderr)
        print(text)
        log_usage(asn_label, elapsed)
        return

    # Write triage file (Claude's output directly)
    TRIAGE_DIR.mkdir(parents=True, exist_ok=True)
    triage_path = TRIAGE_DIR / f"{asn_label}.md"
    triage_path.write_text(text + "\n")
    print(f"  [UPDATED] {triage_path.relative_to(WORKSPACE)}", file=sys.stderr)

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

    # Print full output
    print(text)


if __name__ == "__main__":
    main()
