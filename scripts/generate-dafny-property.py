#!/usr/bin/env python3
"""
Generate Dafny declarations incrementally — one agent call per ASN property.

For each property in the ASN contract, builds the prompt, launches a Claude
agent with Read/Write/Bash tools, and lets it write + verify + fix the .dfy
file autonomously. Skips properties whose output file already exists.

Requires: contract + extract (run contract-asn.py and extract-properties.py first)

Usage:
    python scripts/generate-dafny-property.py 1
    python scripts/generate-dafny-property.py ASN-0001 --property T5
    python scripts/generate-dafny-property.py 1 --with-alloy --dry-run
    python scripts/generate-dafny-property.py 1 --force  # regenerate all
    python scripts/generate-dafny-property.py 1 --force --no-revise  # generate + review only
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

from paths import (WORKSPACE, ASNS_DIR, CONTRACTS_DIR, EXTRACTS_DIR, DAFNY_DIR,
                    ALLOY_DIR, DAFNY_DISCOVERY_DIR, REVIEWS_DIR, USAGE_LOG,
                    MODULES_REGISTRY, next_review_number, sanitize_filename)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
TEMPLATE = PROMPTS_DIR / "generate-dafny-property.md"
DAFNY_REFERENCE = PROMPTS_DIR / "dafny-reference.dfy"
DAFNY_REVIEW_TEMPLATE = PROMPTS_DIR / "write-dafny-review.md"

CONSULT_SCRIPT = WORKSPACE / "scripts" / "consult_for_revision.py"
REVISE_SCRIPT = WORKSPACE / "scripts" / "revise-asn.py"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn_files(asn_id):
    """Find contract and extract for an ASN. Returns (contract_path, extract_path, label)."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None, None
    label = f"ASN-{int(num):04d}"
    contract = CONTRACTS_DIR / f"{label}-contract.md"
    extract = EXTRACTS_DIR / f"{label}-extract.md"
    return (
        contract if contract.exists() else None,
        extract if extract.exists() else None,
        label,
    )


def parse_contract(text):
    """Parse contract markdown table into list of row dicts."""
    rows = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("|") or line.startswith("|--") or "ASN Label" in line:
            continue
        if re.match(r"\|[\s-]+\|", line):
            continue
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) >= 4:
            rows.append({
                "label": cols[0],
                "dafny_name": cols[1],
                "type": cols[2],
                "construct": cols[3],
                "notes": cols[4] if len(cols) > 4 else "",
            })
    return rows


def find_module_for_asn(asn_label, registry_text):
    """Find the target Dafny module for an ASN from the registry."""
    for line in registry_text.split("\n"):
        if asn_label in line and "|" in line:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 1:
                return cols[0]
    return None


def find_alloy_model(asn_label, dafny_name, label):
    """Find Alloy .als file for a specific property."""
    asn_dir = ALLOY_DIR / asn_label
    if not asn_dir.exists():
        return ""

    run_dirs = sorted(
        asn_dir.glob("modeling-*"),
        key=lambda p: int(p.name.split("-")[1]),
    )
    if not run_dirs:
        return ""

    latest = run_dirs[-1]
    candidates = [
        f"{label}-{dafny_name}.als",
        f"{dafny_name}.als",
        f"{label}.als",
    ]

    for name in candidates:
        path = latest / name
        if path.exists():
            return path.read_text()

    return ""


def build_property_prompt(template, registry, stable_root, stable_root_filename,
                          row, extract, alloy_model=""):
    """Assemble prompt for a single property."""
    prompt = template

    # Handle {{#if alloy_model}} conditional
    if alloy_model:
        prompt = re.sub(r"\{\{#if alloy_model\}\}", "", prompt)
        prompt = re.sub(r"\{\{/if\}\}", "", prompt, count=1)
    else:
        prompt = re.sub(
            r"\{\{#if alloy_model\}\}.*?\{\{/if\}\}", "", prompt,
            flags=re.DOTALL, count=1,
        )

    # Format contract row as markdown table
    contract_table = (
        "| ASN Label | Dafny Name | Type | Construct | Notes |\n"
        "|-----------|------------|------|-----------|-------|\n"
        f"| {row['label']} | {row['dafny_name']} | {row['type']}"
        f" | {row['construct']} | {row['notes']} |"
    )

    dafny_ref = read_file(DAFNY_REFERENCE)

    return (
        prompt
        .replace("{{dafny_reference}}", dafny_ref)
        .replace("{{module_registry}}", registry)
        .replace("{{stable_root_filename}}", stable_root_filename)
        .replace("{{stable_root}}", stable_root)
        .replace("{{contract_row}}", contract_table)
        .replace("{{extract_entry}}", extract)
        .replace("{{alloy_model}}", alloy_model)
    )


def invoke_agent(prompt, out_path, model="sonnet", effort="max", max_turns=12):
    """Launch a Claude agent with tools to write + verify the .dfy file."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--tools", "Read,Write,Bash",
        "--allowedTools", "Read,Write,Bash",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    # Append agent instructions — write, verify, fix loop
    full_prompt = f"""{prompt}

Write the Dafny module to: {out_path}

After writing, run `dafny verify {out_path}` to check it. If verification
fails, read the errors, fix the code, and re-verify. Repeat until it
verifies with 0 errors.

If the property has a constructively provable existential, include a proof
lemma that provides the witness.

After verification succeeds, compare what you proved against the ASN property
statement. If you added preconditions, strengthened invariants, or weakened the
conclusion to make the proof work, add a comment starting with
`// DIVERGENCE: ` near the relevant code explaining what changed and why.
Do not create separate notes files — keep divergences inline in the .dfy file.
"""

    start = time.time()
    result = subprocess.run(
        cmd, input=full_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False, elapsed, 0

    # Parse JSON for usage stats
    cost = 0
    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)
        print(f" [{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr, end="", flush=True)
        subtype = data.get("subtype", "")
        if subtype and subtype != "success":
            print(f" [{subtype}]", file=sys.stderr, end="", flush=True)
    except (json.JSONDecodeError, KeyError):
        print(f" [{elapsed:.0f}s]", file=sys.stderr, end="", flush=True)

    return out_path.exists(), elapsed, cost


def verify_dafny(path):
    """Run dafny verify. Returns (success, output)."""
    try:
        result = subprocess.run(
            ["dafny", "verify", str(path)],
            capture_output=True, text=True, timeout=120,
            cwd=str(WORKSPACE),
        )
        output = (result.stdout + result.stderr).strip()
        ok = result.returncode == 0 or re.search(r"\d+ verified, 0 errors", output)
        has_errors = bool(re.search(r"^.*Error:.*$", output, re.MULTILINE))
        return bool(ok) and not has_errors, output
    except subprocess.TimeoutExpired:
        return False, "verification timed out (120s)"


def extract_divergences(dfy_path):
    """Use Sonnet to extract divergence markers from a .dfy file.

    The proof author is instructed to leave // DIVERGENCE: comments when they
    change something to make the proof work. This function uses a cheap Sonnet
    call to find those markers regardless of exact formatting (casing, spacing,
    block vs line comments, variant spellings) and extract them as structured
    JSON.

    Returns list of (line_number, divergence_text) tuples.
    """
    try:
        dfy_source = dfy_path.read_text()
    except (FileNotFoundError, OSError):
        return []

    if not dfy_source.strip():
        return []

    prompt = f"""Extract divergence markers from this Dafny source file.

The proof author was instructed to leave comments when the proof diverges
from the original specification — where they added preconditions, strengthened
invariants, or weakened conclusions to make the proof work.

These are typically formatted as `// DIVERGENCE: <description>` but may use
variations: different casing, block comments, dashes instead of colons, or
other phrasings like "NOTE: diverges from ASN", "CHANGED:", "added
precondition", etc.

Find ALL such markers. Only include comments that describe an actual change
to what is being proved — ignore normal code comments, proof hints, and
documentation.

Dafny source ({dfy_path.name}):
```dafny
{dfy_source}
```

Reply with ONLY a JSON array. Each element: {{"line": <number>, "text": "<description>"}}.
If no divergence markers found, reply with [].
No markdown fences, no commentary — just the JSON array."""

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--max-turns", "1",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "low"

    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, env=env,
            cwd=str(WORKSPACE), timeout=60,
        )
        if result.returncode != 0:
            return []

        # Parse the agent JSON wrapper, then extract the result text
        data = json.loads(result.stdout)
        text = data.get("result", "")

        # The result text should be a JSON array
        items = json.loads(text)
        if not isinstance(items, list):
            return []

        divergences = []
        for item in items:
            if isinstance(item, dict) and "text" in item:
                line = item.get("line", 0)
                divergences.append((int(line), str(item["text"])))
        return divergences

    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError,
            ValueError, TypeError):
        return []


def next_dafny_gen_number(asn_label):
    """Find the next Dafny divergence number for this ASN."""
    asn_dir = DAFNY_DISCOVERY_DIR / asn_label
    if not asn_dir.exists():
        return 1
    existing = sorted(asn_dir.glob("divergence-*"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"divergence-(\d+)$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def write_divergence_file(gen_dir, label, dafny_name, divergences):
    """Write a .divergences.md file to the discovery generation directory.

    Only called when divergences exist. Creates the directory on first use.
    """
    gen_dir.mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(label, dafny_name)
    div_path = gen_dir / f"{filename}.divergences.md"

    lines = [f"# Divergences — {label} ({dafny_name})\n"]
    for line_num, text in divergences:
        lines.append(f"- **Line {line_num}**: {text}")
    lines.append("")

    div_path.write_text("\n".join(lines))


def log_usage(asn_label, dafny_name, elapsed, verified, cost):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "generate-dafny-property",
            "asn": asn_label,
            "property": dafny_name,
            "elapsed_s": round(elapsed, 1),
            "verified": verified,
            "cost_usd": cost,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def find_asn_path(asn_label):
    """Find the ASN markdown file for a label like ASN-0001."""
    candidates = sorted(ASNS_DIR.glob(f"{asn_label}*.md"))
    return candidates[0] if candidates else None


def build_dafny_review_evidence(results, extract_text):
    """Build divergence evidence and verified summary for the review prompt.

    Returns (evidence_text, verified_summary).
    """
    evidence_parts = []

    for r in results:
        if not r["divergences"]:
            continue

        part = [f"### {r['label']} — {r['dafny_name']}\n"]

        # Include divergence comments with surrounding Dafny code
        dfy_path = r["dfy_path"]
        if dfy_path.exists():
            lines = dfy_path.read_text().split("\n")
            for line_num, div_text in r["divergences"]:
                part.append(f"**Divergence** (line {line_num}): {div_text}\n")
                # Show context: 3 lines before and after
                start = max(0, line_num - 4)
                end = min(len(lines), line_num + 3)
                snippet = "\n".join(
                    f"{'→ ' if i + 1 == line_num else '  '}{lines[i]}"
                    for i in range(start, end)
                )
                part.append(f"```dafny\n{snippet}\n```\n")

        evidence_parts.append("\n".join(part))

    evidence_text = "\n---\n\n".join(evidence_parts) if evidence_parts else "None"

    # Verified-clean summary
    clean = [r for r in results if r["verified"] and not r["divergences"]]
    if clean:
        labels = ", ".join(r["label"] for r in clean)
        verified_summary = (
            f"{len(clean)} properties verified without divergences: {labels}"
        )
    else:
        verified_summary = "None"

    return evidence_text, verified_summary


def generate_dafny_review(asn_label, results, extract_text,
                           asn_path=None, model="opus"):
    """Generate a review analyzing Dafny divergences.

    Returns the review path, or None if no divergences.
    """
    div_results = [r for r in results if r["divergences"]]
    if not div_results:
        return None

    template = read_file(DAFNY_REVIEW_TEMPLATE)
    if not template:
        print("  Review template not found at "
              "scripts/prompts/formalization/write-dafny-review.md",
              file=sys.stderr)
        return None

    # ASN text for context
    asn_text = ""
    if asn_path:
        asn_text = read_file(asn_path)
    if not asn_text:
        asn_text = extract_text

    evidence_text, verified_summary = build_dafny_review_evidence(
        results, extract_text)

    prompt = template.replace(
        "{{asn_text}}", asn_text
    ).replace(
        "{{divergence_evidence}}", evidence_text
    ).replace(
        "{{verified_summary}}", verified_summary
    )

    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"

    print(f"\n  [REVIEW] Calling {model} to analyze {len(div_results)} "
          f"divergence(s)...", file=sys.stderr)

    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", "4",
        "--tools", "Read,Write",
        "--allowedTools", "Read,Write",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    full_prompt = f"""{prompt}

Write the review to: {review_path}
"""

    result = subprocess.run(
        cmd, input=full_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )

    if result.returncode != 0 or not review_path.exists():
        print(f"  [REVIEW] LLM review generation failed", file=sys.stderr)
        return None

    return review_path


def step_consult(asn_id, review_path):
    """Run consult_for_revision.py. Returns consultation path or None."""
    print(f"\n  === CONSULT ===", file=sys.stderr)
    cmd = [sys.executable, str(CONSULT_SCRIPT), str(asn_id)]

    review_name = Path(review_path).stem
    m = re.search(r"(review-\d+)", review_name)
    if m:
        cmd.append(m.group(1))

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [CONSULT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    consultation_path = result.stdout.strip()
    if consultation_path and Path(consultation_path).exists():
        return consultation_path
    return None


def step_revise(asn_id, consultation_path=None):
    """Run revise-asn.py. Returns (asn_path, converged)."""
    print(f"\n  === REVISE ===", file=sys.stderr)
    cmd = [sys.executable, str(REVISE_SCRIPT), str(asn_id)]
    if consultation_path:
        cmd.extend(["--consultation", consultation_path])

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    converged = result.returncode == 2

    if result.returncode not in (0, 2):
        print(f"  [REVISE] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    asn_path = result.stdout.strip()
    if asn_path and Path(asn_path).exists():
        return asn_path, converged
    return None, False


def step_commit(hint=""):
    """Run commit.py."""
    print(f"\n  === COMMIT ===", file=sys.stderr)
    cmd = [sys.executable, str(COMMIT_SCRIPT)]
    if hint:
        cmd.append(hint)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [COMMIT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if result.stdout.strip():
        print(f"  {result.stdout.strip()}", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dafny declarations incrementally per ASN property")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--property", "-p",
                        help="Generate only this property (ASN label, e.g., T5)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--max-turns", type=int, default=12,
                        help="Max agent turns per property (default: 12)")
    parser.add_argument("--with-alloy", action="store_true",
                        help="Inject Alloy model as reference for each property")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate even if output file exists")
    parser.add_argument("--no-revise", action="store_true",
                        help="Stop after review, skip consult/revise/commit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without invoking Claude")
    args = parser.parse_args()

    # --- Locate inputs ---

    contract_path, extract_path, asn_label = find_asn_files(args.asn)
    if contract_path is None:
        print(f"  No contract found for {args.asn} in {CONTRACTS_DIR.relative_to(WORKSPACE)}/",
              file=sys.stderr)
        print(f"  Run: python scripts/contract-asn.py {args.asn}", file=sys.stderr)
        sys.exit(1)
    if extract_path is None:
        print(f"  No extract found for {args.asn} in {EXTRACTS_DIR.relative_to(WORKSPACE)}/",
              file=sys.stderr)
        print(f"  Run: python scripts/extract-properties.py {args.asn}", file=sys.stderr)
        sys.exit(1)

    template_text = read_file(TEMPLATE)
    if not template_text:
        print("  Prompt template not found: scripts/prompts/formalization/generate-dafny-property.md",
              file=sys.stderr)
        sys.exit(1)

    registry_text = read_file(MODULES_REGISTRY)
    if not registry_text:
        print("  Module registry not found: vault/3-modeling/modules.md", file=sys.stderr)
        sys.exit(1)

    # --- Parse inputs ---

    contract_rows = parse_contract(contract_path.read_text())
    extract_text = extract_path.read_text()

    if not contract_rows:
        print(f"  No properties found in contract {contract_path.name}", file=sys.stderr)
        sys.exit(1)

    # Target module from registry
    module_name = find_module_for_asn(asn_label, registry_text)
    if not module_name:
        print(f"  No module found for {asn_label} in registry", file=sys.stderr)
        sys.exit(1)

    module_dir = DAFNY_DIR / module_name
    stable_root_path = module_dir / f"{module_name}.dfy"
    stable_root = read_file(stable_root_path)
    if not stable_root:
        print(f"  Stable root not found: {stable_root_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    # Filter to single property if requested
    if args.property:
        contract_rows = [r for r in contract_rows
                         if r["label"] == args.property
                         or r["dafny_name"] == args.property]
        if not contract_rows:
            print(f"  Property '{args.property}' not found in contract", file=sys.stderr)
            sys.exit(1)

    # --- Generate ---

    gen_num = next_dafny_gen_number(asn_label)
    gen_dir = DAFNY_DISCOVERY_DIR / asn_label / f"divergence-{gen_num}"
    # gen_dir created lazily — only when a divergence is found

    print(f"  [DAFNY-PROPERTY] {asn_label} → {module_name}/ (divergence-{gen_num})",
          file=sys.stderr)
    print(f"  Properties: {len(contract_rows)}", file=sys.stderr)

    generated = 0
    skipped = 0
    failed = 0
    verified_ok = 0
    total_cost = 0
    results = []

    for row in contract_rows:
        label = row["label"]
        dafny_name = row["dafny_name"]
        out_path = module_dir / f"{dafny_name}.dfy"

        # Skip existing
        if out_path.exists() and not args.force:
            print(f"  [SKIP] {label} → {dafny_name} (exists)", file=sys.stderr)
            skipped += 1
            continue

        # Alloy model (optional)
        alloy_model = ""
        if args.with_alloy:
            alloy_model = find_alloy_model(asn_label, dafny_name, label)

        # Build prompt
        prompt = build_property_prompt(
            template_text, registry_text, stable_root, stable_root_path.name,
            row, extract_text, alloy_model,
        )

        if args.dry_run:
            alloy_flag = " +alloy" if alloy_model else ""
            print(f"  [DRY] {label} → {dafny_name}.dfy"
                  f" (~{len(prompt) // 4} tokens){alloy_flag}",
                  file=sys.stderr)
            continue

        # Launch agent — it writes, verifies, and fixes autonomously
        module_dir.mkdir(parents=True, exist_ok=True)
        print(f"  [{label}] {dafny_name}...",
              file=sys.stderr, end="", flush=True)
        wrote, elapsed, cost = invoke_agent(
            prompt, out_path,
            model=args.model, effort=args.effort, max_turns=args.max_turns,
        )
        total_cost += cost

        if not wrote:
            print(f" no file written", file=sys.stderr)
            failed += 1
            continue

        # Final verification (agent should have already verified, but confirm)
        ok, vout = verify_dafny(out_path)
        divergences = extract_divergences(out_path) if ok else []

        if divergences:
            write_divergence_file(gen_dir, label, dafny_name, divergences)

        if ok:
            m = re.search(r"(\d+) verified", vout)
            n = m.group(1) if m else "?"
            div_tag = f" +{len(divergences)}div" if divergences else ""
            print(f" verified({n}){div_tag}", file=sys.stderr)
            verified_ok += 1
        else:
            print(f" UNVERIFIED", file=sys.stderr)
            for line in vout.split("\n"):
                if re.search(r"Error:", line):
                    print(f"    {line.strip()}", file=sys.stderr)
                    break

        generated += 1
        results.append({
            "label": label,
            "dafny_name": dafny_name,
            "dfy_path": out_path,
            "verified": ok,
            "divergences": divergences,
        })
        log_usage(asn_label, dafny_name, elapsed, ok, cost)

    # Summary
    div_count = sum(1 for r in results if r["divergences"])
    if not args.dry_run:
        print(f"\n  Done: {generated} generated, {skipped} skipped, {failed} failed",
              file=sys.stderr)
        if generated > 0:
            print(f"  Verified: {verified_ok}/{generated}", file=sys.stderr)
            if div_count:
                print(f"  Divergences: {div_count} properties with divergences",
                      file=sys.stderr)
            print(f"  Cost: ${total_cost:.2f}", file=sys.stderr)

    # --- Post-generation review pipeline ---
    if not args.dry_run and div_count > 0:
        review_path = generate_dafny_review(
            asn_label, results, extract_text,
            asn_path=find_asn_path(asn_label), model=args.model,
        )
        if review_path:
            print(f"\n  [REVIEW] {review_path.relative_to(WORKSPACE)}",
                  file=sys.stderr)

            if not args.no_revise:
                consultation_path = step_consult(args.asn, str(review_path))
                asn_result, converged = step_revise(
                    args.asn, consultation_path=consultation_path)
                if converged:
                    print(f"  [PIPELINE] Revise made no changes",
                          file=sys.stderr)
                step_commit(f"dafny(asn): {asn_label} — "
                            f"Dafny verify + revise")
    elif not args.dry_run and generated > 0 and not args.no_revise:
        step_commit(f"dafny(asn): {asn_label} — "
                    f"all properties verified clean")


if __name__ == "__main__":
    main()
