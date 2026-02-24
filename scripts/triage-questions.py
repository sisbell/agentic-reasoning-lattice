#!/usr/bin/env python3
"""
Triage ASN open questions — decide which spawn new inquiries.

Reads an ASN's open questions, checks what's already been triaged,
invokes Claude to evaluate each question, and updates inquiries.yaml
and vault/triage/ASN-NNNN.md for qualifying questions.

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

WORKSPACE = Path(__file__).resolve().parent.parent
PROMPTS_DIR = WORKSPACE / "scripts" / "prompts"
TRIAGE_TEMPLATE = PROMPTS_DIR / "triage-questions.md"
ASNS_DIR = WORKSPACE / "vault" / "asns"
INQUIRIES_FILE = WORKSPACE / "vault" / "inquiries.yaml"
TRIAGE_DIR = WORKSPACE / "vault" / "triage"
USAGE_LOG = WORKSPACE / "vault" / "usage-log.jsonl"


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
    """Call claude --print. Returns response text."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "--print",
        "--model", model_flag,
        "--output-format", "json",
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
        return "", elapsed, {}

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)

        print(f"  [{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)

        return text, elapsed, {"input_tokens": inp, "output_tokens": out,
                               "cost_usd": cost}
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return result.stdout, elapsed, {}


def parse_response(text):
    """Extract JSON from Claude's response."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines)

    return json.loads(cleaned)


def append_inquiry_yaml(data, inquiry, next_id):
    """Append a new inquiry to the YAML data structure."""
    entry = {
        "id": next_id,
        "title": inquiry["title"],
        "question": inquiry["question"],
        "area": inquiry["area"],
        "source": inquiry["source"],
    }
    agents = inquiry.get("agents", {})
    nelson = agents.get("nelson", 10)
    gregory = agents.get("gregory", 10)
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


def write_triage_file(asn_label, result):
    """Write the full triage evaluation to vault/triage/ASN-NNNN.md."""
    TRIAGE_DIR.mkdir(parents=True, exist_ok=True)

    evaluated = result.get("evaluated", [])
    new_inquiries = result.get("new_inquiries", [])

    lines = [f"# Triage: {asn_label}", ""]

    # Promoted questions
    promoted = [e for e in evaluated if e.get("qualifies")]
    if promoted:
        lines.append("## Promoted")
        lines.append("")
        for e in promoted:
            # Find the matching inquiry for this question
            matching = [ni for ni in new_inquiries
                        if ni.get("source", "").endswith(
                            e["question"][:40].lower().replace(" ", "-")[:30]
                        )]
            inquiry_ref = ""
            for ni in new_inquiries:
                # Match by rationale or source overlap
                if ni.get("rationale") == e.get("reason"):
                    inquiry_ref = f" → Inquiry: {ni['title']}"
                    break
            if not inquiry_ref and new_inquiries:
                # Fall back to source field matching
                for ni in new_inquiries:
                    src = ni.get("source", "")
                    if any(word in src.lower() for word in
                           e["question"][:50].lower().split()[:5]):
                        inquiry_ref = f" → Inquiry: {ni['title']}"
                        break

            lines.append(f"- **{e['question']}**{inquiry_ref}")
            lines.append(f"  {e['reason']}")
            lines.append("")

    # Declined questions
    declined = [e for e in evaluated if not e.get("qualifies")]
    if declined:
        lines.append("## Declined")
        lines.append("")
        for e in declined:
            lines.append(f"- **{e['question']}**")
            lines.append(f"  {e['reason']}")
            lines.append("")

    out_path = TRIAGE_DIR / f"{asn_label}.md"
    out_path.write_text("\n".join(lines))
    return out_path


def log_usage(asn_label, elapsed, usage):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "triage-questions",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "cost_usd": usage.get("cost_usd", 0),
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
                        help="Show decisions without updating files")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/asns/", file=sys.stderr)
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
    text, elapsed, usage = invoke_claude(prompt, model=args.model,
                                         effort=args.effort)

    if not text:
        print("  No response produced", file=sys.stderr)
        sys.exit(1)

    # Parse response
    try:
        result = parse_response(text)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"  Failed to parse JSON response: {e}", file=sys.stderr)
        print(f"  Raw response:\n{text[:500]}", file=sys.stderr)
        sys.exit(1)

    # Display evaluation
    evaluated = result.get("evaluated", [])
    new_inquiries = result.get("new_inquiries", [])

    print(f"\n  Evaluated {len(evaluated)} open questions:", file=sys.stderr)
    for eq in evaluated:
        status = "YES" if eq["qualifies"] else "no"
        q = eq["question"][:70] + "..." if len(eq["question"]) > 70 else eq["question"]
        print(f"    [{status:>3}] {q}", file=sys.stderr)
        print(f"          {eq['reason']}", file=sys.stderr)

    if not new_inquiries:
        print(f"\n  No new inquiries from {asn_label}", file=sys.stderr)

    if new_inquiries:
        print(f"\n  {len(new_inquiries)} new inquiry/inquiries:", file=sys.stderr)
        for ni in new_inquiries:
            agents = ni.get("agents", {})
            n = agents.get("nelson", 10)
            g = agents.get("gregory", 10)
            print(f"    -> {ni['title']} [{ni['area']}] (nelson:{n} gregory:{g})",
                  file=sys.stderr)
            print(f"       {ni['question'][:80]}...", file=sys.stderr)

    if args.dry_run:
        print(f"\n  [DRY RUN] Would update files", file=sys.stderr)
        print(json.dumps(result, indent=2))
        log_usage(asn_label, elapsed, usage)
        return

    # Write triage file (always — records all decisions)
    triage_path = write_triage_file(asn_label, result)
    print(f"  [UPDATED] {triage_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Update inquiries.yaml (only if new inquiries)
    if new_inquiries:
        cur_id = next_inquiry_id(inq_data)
        for ni in new_inquiries:
            append_inquiry_yaml(inq_data, ni, cur_id)
            print(f"  [ADD] Inquiry {cur_id}: {ni['title']}", file=sys.stderr)
            cur_id += 1

        write_inquiries_yaml(inq_data)
        print(f"  [UPDATED] {INQUIRIES_FILE.relative_to(WORKSPACE)}",
              file=sys.stderr)

    # Log usage
    log_usage(asn_label, elapsed, usage)

    # Print result JSON to stdout for pipeline consumption
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
