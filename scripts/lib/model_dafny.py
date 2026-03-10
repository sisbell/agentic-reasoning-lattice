#!/usr/bin/env python3
"""
Generate Dafny declarations incrementally — one agent call per ASN property.

For each property in the proof index, builds the prompt, launches a Claude
agent with Read/Write/Bash tools, and lets it write + verify + fix the .dfy
file autonomously. Each run creates a new modeling-N/ directory.

Requires: proof index + extract (run contract-asn.py and extract-properties.py first)

Usage:
    python scripts/generate-dafny-property.py 1
    python scripts/generate-dafny-property.py ASN-0001 --property T5
    python scripts/generate-dafny-property.py 1 --modeling 3       # into existing run
    python scripts/generate-dafny-property.py 1 --dry-run
    python scripts/generate-dafny-property.py 1 --no-alloy          # skip Alloy reference
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, PROOF_INDEX_DIR, STATEMENTS_DIR,
                    PROOFS_DIR, DAFNY_DIR, ALLOY_DIR, REVIEWS_DIR, USAGE_LOG,
                    PROOF_IMPORTS, next_review_number, next_modeling_number,
                    sanitize_filename)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
TEMPLATE = PROMPTS_DIR / "generate-dafny-property.md"
DAFNY_REFERENCE = PROMPTS_DIR / "dafny-reference.dfy"
DAFNY_REVIEW_TEMPLATE = PROMPTS_DIR / "write-dafny-review.md"


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn_files(asn_id):
    """Find proof index and extract for an ASN. Returns (index_path, extract_path, label)."""
    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None, None
    label = f"ASN-{int(num):04d}"
    index = PROOF_INDEX_DIR / f"{label}-proof-index.md"
    extract = STATEMENTS_DIR / f"{label}-statements.md"
    return (
        index if index.exists() else None,
        extract if extract.exists() else None,
        label,
    )


def parse_proof_index(text):
    """Parse proof index markdown table into list of row dicts."""
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
                "proof_label": cols[1],
                "type": cols[2],
                "construct": cols[3],
                "notes": cols[4] if len(cols) > 4 else "",
            })
    return rows


def find_imports_for_asn(asn_label, imports_text):
    """Find additional proof module dependencies for an ASN from imports.md.

    Returns list of module names (may be empty if ASN only needs base modules).
    Returns None if the ASN is not listed at all.
    """
    for line in imports_text.split("\n"):
        if asn_label in line and "|" in line:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 2:
                return [m.strip() for m in cols[1].split(",") if m.strip()]
    return None


def read_proof_modules(module_names):
    """Read all .dfy files from listed proof module directories.

    Returns a dict of {relative_path: source} and a formatted text block
    for prompt injection. Paths are relative to WORKSPACE.
    """
    modules = {}
    for mod_name in module_names:
        mod_dir = PROOFS_DIR / mod_name
        if not mod_dir.exists():
            print(f"  Warning: proof module directory not found: {mod_dir}",
                  file=sys.stderr)
            continue
        for dfy_file in sorted(mod_dir.glob("*.dfy")):
            content = read_file(dfy_file)
            if content.strip():
                rel_path = str(dfy_file.relative_to(WORKSPACE))
                modules[rel_path] = content

    # Format as prompt text — show path so LLM can compute includes
    parts = []
    for rel_path, source in modules.items():
        parts.append(f"### `{rel_path}`\n\n```dafny\n{source}\n```")

    return modules, "\n\n".join(parts)


def find_alloy_model(asn_label, proof_label, label):
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
        f"{label}-{proof_label}.als",
        f"{proof_label}.als",
        f"{label}.als",
    ]

    for name in candidates:
        path = latest / name
        if path.exists():
            return path.read_text()

    return ""


def build_property_prompt(template, imports_map, proof_modules_text,
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

    # Format proof index row as markdown table
    index_table = (
        "| ASN Label | Proof Label | Type | Construct | Notes |\n"
        "|-----------|------------|------|-----------|-------|\n"
        f"| {row['label']} | {row['proof_label']} | {row['type']}"
        f" | {row['construct']} | {row['notes']} |"
    )

    dafny_ref = read_file(DAFNY_REFERENCE)

    return (
        prompt
        .replace("{{dafny_reference}}", dafny_ref)
        .replace("{{imports_map}}", imports_map)
        .replace("{{proof_modules}}", proof_modules_text)
        .replace("{{index_row}}", index_table)
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

## Proof development — build up from nothing

Work in small steps. Each step adds ONE thing, then verifies.

1. Write the module with the full declaration — the predicate or lemma
   with its body, plus any accompanying lemmas the property requires
   (e.g., a "strict total order" property needs irreflexivity,
   transitivity, trichotomy, and asymmetry lemmas). Start every lemma
   body empty `{{ }}`. Write to disk, then run `dafny verify {out_path}`.

2. If ALL declarations verify, you are done. Move to the divergence check.

3. If verification fails, read the error. It tells you exactly what the
   solver cannot prove. Add the MINIMUM to address that one error:
   - A single recursive call
   - One `assert` of an intermediate fact
   - One case split (`if ... {{ }} else {{ }}`)
   - A call to one existing lemma
   Write the updated file. Verify again.

4. Repeat step 3. Never add more than one proof element between
   verifications. If you find yourself writing more than 5 lines
   before verifying, stop — you are guessing instead of listening
   to the solver.

5. If you are stuck after 3 failed attempts on the same error,
   step back: try a different decomposition (a helper lemma with
   its own signature, or restructuring the cases). Do not pile on
   assertions.

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


def run_commit(hint=""):
    """Run commit.py to commit vault changes."""
    cmd = [sys.executable, str(WORKSPACE / "scripts" / "commit.py")]
    if hint:
        cmd.append(hint)
    result = subprocess.run(cmd, cwd=str(WORKSPACE))
    if result.returncode != 0:
        print("  [COMMIT] failed — changes left unstaged", file=sys.stderr)
    return result.returncode == 0


def write_divergence_file(gen_dir, label, proof_label, divergences):
    """Write a .divergences.md file to the modeling directory.

    Only called when divergences exist. Creates the directory on first use.
    Uses proof_label for the filename to match the .dfy file naming convention.
    """
    gen_dir.mkdir(parents=True, exist_ok=True)
    div_path = gen_dir / f"{proof_label}.divergences.md"

    lines = [f"# Divergences — {label} ({proof_label})\n"]
    for line_num, text in divergences:
        lines.append(f"- **Line {line_num}**: {text}")
    lines.append("")

    div_path.write_text("\n".join(lines))


def write_status_file(gen_dir, results, source="generate"):
    """Write or update STATUS.md in the modeling directory.

    Called by both model_dafny.py (after generation) and model_fix.py (after fixes).
    Appends fix attempts to an existing file; overwrites the table on generation.
    """
    status_path = gen_dir / "STATUS.md"
    now = time.strftime("%Y-%m-%d %H:%M")

    # Build the table from results
    verified_count = sum(1 for r in results if r["verified"])
    total = len(results)

    lines = [
        f"# Verification Status — {gen_dir.name}",
        f"",
        f"Updated: {now}",
        f"Verified: {verified_count}/{total}",
        f"",
        f"| Property | Status | Divergences |",
        f"|----------|--------|-------------|",
    ]

    for r in results:
        status = "verified" if r["verified"] else "**UNVERIFIED**"
        divs = ""
        if r["divergences"]:
            # First divergence text, truncated
            div_text = r["divergences"][0][1]
            divs = div_text[:80] + ("..." if len(div_text) > 80 else "")
        lines.append(f"| {r['proof_label']} | {status} | {divs} |")

    lines.append("")

    if source == "generate":
        # Fresh write
        status_path.write_text("\n".join(lines))
    else:
        # Fix: preserve existing content, append fix log entry
        existing = ""
        if status_path.exists():
            existing = status_path.read_text()

        # Find or create Fix Attempts section
        if "## Fix Attempts" not in existing:
            existing = existing.rstrip() + "\n\n## Fix Attempts\n"

        fix_entries = []
        for r in results:
            status = "verified" if r["verified"] else "STILL UNVERIFIED"
            cost = f"${r.get('cost', 0):.2f}" if r.get("cost") else ""
            fix_entries.append(f"- {now}: {r['proof_label']} — {status} {cost}")

        status_path.write_text(existing + "\n".join(fix_entries) + "\n")


def log_usage(asn_label, proof_label, elapsed, verified, cost):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "generate-dafny-property",
            "asn": asn_label,
            "property": proof_label,
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

    Only receives verified results. Returns (evidence_text, verified_summary).
    """
    evidence_parts = []

    for r in results:
        if not r["divergences"]:
            continue

        part = [f"### {r['label']} — {r['proof_label']}\n"]

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
    """Generate a review analyzing divergences and verification failures.

    Returns the review path, or None if nothing to review.
    """
    div_results = [r for r in results if r["divergences"]]

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

    # Collect all generated Dafny source for quality review
    dafny_source_parts = []
    for r in results:
        dfy_path = r["dfy_path"]
        if dfy_path.exists():
            dafny_source_parts.append(
                f"### {r['proof_label']} ({dfy_path.name})\n\n"
                f"```dafny\n{dfy_path.read_text()}\n```"
            )
    dafny_source = "\n\n---\n\n".join(dafny_source_parts) if dafny_source_parts else "None"

    prompt = template.replace(
        "{{asn_text}}", asn_text
    ).replace(
        "{{divergence_evidence}}", evidence_text
    ).replace(
        "{{verified_summary}}", verified_summary
    ).replace(
        "{{dafny_source}}", dafny_source
    )

    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"

    div_count = len(div_results)
    file_count = len([r for r in results if r["dfy_path"].exists()])
    print(f"\n  [REVIEW] Calling {model} to analyze {file_count} verified file(s)"
          f", {div_count} divergence(s)...",
          file=sys.stderr)

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


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dafny declarations incrementally per ASN property")
    parser.add_argument("asn",
                        help="ASN number (e.g., 1, 0001, ASN-0001)")
    parser.add_argument("--property", "-p",
                        help="Generate specific properties, comma-separated (e.g., T5 or T1,T3,TA0)")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
    parser.add_argument("--effort", default="max",
                        help="Thinking effort level (low/medium/high/max)")
    parser.add_argument("--max-turns", type=int, default=24,
                        help="Max agent turns per property (default: 16)")
    parser.add_argument("--modeling", type=int, default=None,
                        help="Target existing modeling-N directory")
    parser.add_argument("--no-alloy", action="store_true",
                        help="Skip injecting Alloy model as reference")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without invoking Claude")
    args = parser.parse_args()

    # --- Locate inputs ---

    index_path, extract_path, asn_label = find_asn_files(args.asn)
    if index_path is None:
        print(f"  No proof index found for {args.asn} in {PROOF_INDEX_DIR.relative_to(WORKSPACE)}/",
              file=sys.stderr)
        print(f"  Run: python scripts/model.py index {args.asn}", file=sys.stderr)
        sys.exit(1)
    if extract_path is None:
        print(f"  No extract found for {args.asn} in {STATEMENTS_DIR.relative_to(WORKSPACE)}/",
              file=sys.stderr)
        print(f"  Run: python scripts/model.py statements {args.asn}", file=sys.stderr)
        sys.exit(1)

    template_text = read_file(TEMPLATE)
    if not template_text:
        print("  Prompt template not found: scripts/prompts/formalization/generate-dafny-property.md",
              file=sys.stderr)
        sys.exit(1)

    imports_text = read_file(PROOF_IMPORTS)
    if not imports_text:
        print("  Proof imports not found: vault/proofs/imports.md", file=sys.stderr)
        sys.exit(1)

    # --- Parse inputs ---

    index_rows = parse_proof_index(index_path.read_text())
    extract_text = extract_path.read_text()

    if not index_rows:
        print(f"  No properties found in proof index {index_path.name}", file=sys.stderr)
        sys.exit(1)

    # Proof module dependencies from imports.md
    module_names = find_imports_for_asn(asn_label, imports_text)
    if module_names is None:
        print(f"  {asn_label} not listed in vault/proofs/imports.md",
              file=sys.stderr)
        sys.exit(1)

    # Always include base modules (TumblerAlgebra + Foundation)
    base_modules = ["TumblerAlgebra", "Foundation"]
    all_modules = base_modules + [m for m in module_names if m not in base_modules]

    proof_modules, proof_modules_text = read_proof_modules(all_modules)

    # Filter to specific properties if requested
    if args.property:
        targets = [t.strip() for t in args.property.split(",")]
        matches = []
        for target in targets:
            found = [r for r in index_rows
                     if r["label"] == target or r["proof_label"] == target]
            if not found:
                # Try prefix match
                found = [r for r in index_rows
                         if r["label"].lower().startswith(target.lower())
                         or r["proof_label"].lower().startswith(target.lower())]
            if not found:
                print(f"  Property '{target}' not found in proof index",
                      file=sys.stderr)
                print(f"  Available: {', '.join(r['label'] for r in index_rows)}",
                      file=sys.stderr)
                sys.exit(1)
            matches.extend(found)
        index_rows = matches

    # --- Generate ---

    if args.modeling is not None:
        gen_num = args.modeling
        gen_dir = DAFNY_DIR / asn_label / f"modeling-{gen_num}"
        if not gen_dir.exists():
            print(f"  modeling-{gen_num} does not exist for {asn_label}",
                  file=sys.stderr)
            sys.exit(1)
    else:
        gen_num = next_modeling_number(asn_label)
        gen_dir = DAFNY_DIR / asn_label / f"modeling-{gen_num}"

    print(f"  [DAFNY-PROPERTY] {asn_label} (modeling-{gen_num})",
          file=sys.stderr)
    print(f"  Imports: {', '.join(module_names)}", file=sys.stderr)
    print(f"  Properties: {len(index_rows)}", file=sys.stderr)

    resuming = args.modeling is not None
    generated = 0
    skipped = 0
    failed = 0
    verified_ok = 0
    total_cost = 0
    results = []

    for row in index_rows:
        label = row["label"]
        proof_label = row["proof_label"]
        out_path = gen_dir / f"{proof_label}.dfy"

        # Skip existing when resuming into an existing run
        if resuming and out_path.exists():
            print(f"  [SKIP] {label} → {proof_label} (exists)", file=sys.stderr)
            skipped += 1
            continue

        # Alloy model (optional)
        alloy_model = ""
        if not args.no_alloy:
            alloy_model = find_alloy_model(asn_label, proof_label, label)

        # Build prompt
        prompt = build_property_prompt(
            template_text, imports_text, proof_modules_text,
            row, extract_text, alloy_model,
        )

        if args.dry_run:
            alloy_flag = " +alloy" if alloy_model else ""
            print(f"  [DRY] {label} → {proof_label}.dfy"
                  f" (~{len(prompt) // 4} tokens){alloy_flag}",
                  file=sys.stderr)
            continue

        # Launch agent — it writes, verifies, and fixes autonomously
        gen_dir.mkdir(parents=True, exist_ok=True)
        print(f"  [{label}] {proof_label}...",
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
        divergences = extract_divergences(out_path)

        if divergences:
            write_divergence_file(gen_dir, label, proof_label, divergences)

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
            "proof_label": proof_label,
            "dfy_path": out_path,
            "verified": ok,
            "divergences": divergences,
        })
        log_usage(asn_label, proof_label, elapsed, ok, cost)

    # Summary
    div_count = sum(1 for r in results if r["divergences"])
    if not args.dry_run:
        skip_msg = f", {skipped} skipped" if skipped else ""
        print(f"\n  Done: {generated} generated{skip_msg}, {failed} failed",
              file=sys.stderr)
        if generated > 0:
            print(f"  Verified: {verified_ok}/{generated}", file=sys.stderr)
            if div_count:
                print(f"  Divergences: {div_count} properties with divergences",
                      file=sys.stderr)
            print(f"  Cost: ${total_cost:.2f}", file=sys.stderr)

    # Write status file and commit
    if not args.dry_run and results:
        write_status_file(gen_dir, results, source="generate")
        print(f"  Status: {gen_dir.name}/STATUS.md", file=sys.stderr)
        run_commit(f"{asn_label} dafny modeling-{gen_num}")


if __name__ == "__main__":
    main()
