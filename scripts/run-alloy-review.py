#!/usr/bin/env python3
"""
Alloy review pipeline — generate → check → repair → review → consult → revise → commit.

Per-property: parses the extract into individual properties, generates one .als
per property, checks each with a tiered repair loop, produces a review if failures
remain, then feeds the review into the consult → revise → commit cycle.

Requires: extract file in vault/formalization/extracts/ (run extract-properties.py first)
Requires: Alloy installed at /Applications/Alloy.app (macOS) or ALLOY_JAR set.

Usage:
    python scripts/run-alloy-review.py 1                    # full pipeline
    python scripts/run-alloy-review.py 1 --property T1      # single property
    python scripts/run-alloy-review.py 1 --no-revise         # stop after check + review
    python scripts/run-alloy-review.py 1 --skip-check       # generate only
    python scripts/run-alloy-review.py 1 --dry-run           # show property list
    python scripts/run-alloy-review.py 1 --all-in-one        # monolithic mode
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

from pathlib import Path

from paths import WORKSPACE, ASNS_DIR, ALLOY_DIR, EXTRACTS_DIR, REVIEWS_DIR, USAGE_LOG, sorted_reviews

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
TEMPLATE = PROMPTS_DIR / "check-alloy.md"
PROPERTY_TEMPLATE = PROMPTS_DIR / "check-alloy-property.md"
FIX_TEMPLATE = PROMPTS_DIR / "fix-alloy.md"
SYNTAX_REF = PROMPTS_DIR / "alloy-syntax.md"

MAX_TIER1 = 3
MAX_TIER2 = 2

ALLOY_JAR_DEFAULT = (
    "/Applications/Alloy.app/Contents/Resources/org.alloytools.alloy.dist.jar"
)


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def annotate_errors(alloy_output, als_path):
    """Enrich Alloy error output with the offending source lines.

    Alloy errors say 'at line N column C' but don't show the source.
    This parses those references and appends the actual line for context.
    """
    source_lines = read_file(als_path).split("\n")
    if not source_lines:
        return alloy_output

    annotations = []
    for m in re.finditer(r"at line (\d+) column (\d+)", alloy_output):
        lineno = int(m.group(1))
        col = int(m.group(2))
        if 1 <= lineno <= len(source_lines):
            src = source_lines[lineno - 1]
            pointer = " " * (col - 1) + "^"
            annotations.append(
                f"Line {lineno}: {src}\n"
                f"        {pointer}"
            )

    if annotations:
        return alloy_output + "\n\nSource context:\n" + "\n".join(annotations)
    return alloy_output


def find_asn(asn_id):
    """Find ASN file by number. Accepts 9, 09, 0009, ASN-0009, or full path."""
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


def derive_output_name(asn_path):
    """ASN-0004-content-insertion.md -> ContentInsertion"""
    stem = Path(asn_path).stem
    name = re.sub(r"^ASN-\d+-", "", stem)
    return "".join(w.capitalize() for w in name.split("-"))


# Header pattern: ## LABEL — Name (TYPE, construct)
_PROP_RE = re.compile(
    r"^##\s+(.+?)\s+—\s+(\w+)\s+\((\w+),\s+(.+?)\)\s*$"
)


def parse_extract(text):
    """Parse an extract into definitions and properties.

    Returns dict with:
      definitions: str — all '## Definition — *' sections concatenated
      properties: list[dict] — each with label, name, type, construct, body
    """
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)

    definitions = []
    properties = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Check for definition sections
        if section.startswith("## Definition"):
            definitions.append(section)
            continue

        # Check for property header
        first_line = section.split("\n", 1)[0]
        m = _PROP_RE.match(first_line)
        if m:
            properties.append({
                "label": m.group(1),
                "name": m.group(2),
                "type": m.group(3),
                "construct": m.group(4),
                "body": section,
            })

    return {
        "definitions": "\n\n".join(definitions),
        "properties": properties,
    }


def sanitize_filename(label, name):
    """Build a filename-safe string from label and name.

    E.g. ('T1', 'LexicographicOrder') -> 'T1-LexicographicOrder'
         ('TA1-strict', 'StrictOrderPreservation') -> 'TA1-strict-StrictOrderPreservation'
         ('Prefix ordering extension', 'PrefixOrderingExtension') -> 'PrefixOrderingExtension'
    """
    # If label is already a short code (T1, TA3, T10a, TA1-strict, etc.), use it
    if re.match(r"^[A-Z]+\w*(-\w+)?$", label):
        return re.sub(r"[^A-Za-z0-9_-]", "", f"{label}-{name}")
    # Multi-word label (e.g. "Prefix ordering extension") — just use name
    return re.sub(r"[^A-Za-z0-9_-]", "", name)


def build_property_prompt(definitions, prop, syntax_ref=""):
    """Assemble prompt for a single property from per-property template."""
    template = read_file(PROPERTY_TEMPLATE)
    if not template:
        print("  Prompt template not found at "
              "scripts/prompts/formalization/check-alloy-property.md",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{syntax_reference}}", syntax_ref
    ).replace(
        "{{definitions}}", definitions
    ).replace(
        "{{property}}", prop["body"]
    )


def build_fix_prompt(als_path, errors, definitions=None, prop=None,
                     syntax_ref=""):
    """Assemble a fix prompt for a failed Alloy model.

    Tier 1 (no definitions/prop): errors + .als code only.
    Tier 2 (with definitions/prop): adds property context.
    """
    template = read_file(FIX_TEMPLATE)
    if not template:
        print("  Fix template not found at "
              "scripts/prompts/formalization/fix-alloy.md",
              file=sys.stderr)
        return None

    alloy_code = read_file(als_path)

    # Handle conditional property context section
    property_context = ""
    if definitions and prop:
        property_context = definitions + "\n\n" + prop["body"]

    if property_context:
        template = re.sub(r"\{\{#if property_context\}\}", "", template)
        template = re.sub(r"\{\{/if\}\}", "", template, count=1)
    else:
        template = re.sub(
            r"\{\{#if property_context\}\}.*?\{\{/if\}\}", "", template,
            flags=re.DOTALL, count=1)

    return template.replace(
        "{{syntax_reference}}", syntax_ref
    ).replace(
        "{{alloy_code}}", alloy_code
    ).replace(
        "{{errors}}", errors
    ).replace(
        "{{property_context}}", property_context
    )


def classify_alloy_error(alloy_output):
    """Classify Alloy output as syntax-error, counterexample, or pass."""
    if not alloy_output:
        return "pass", []

    has_syntax_error = any(
        "syntax error" in line.lower() or "parse error" in line.lower()
        or "type error" in line.lower()
        for line in alloy_output.split("\n")
    )

    has_counterexample, summary = parse_alloy_results(alloy_output)

    if has_syntax_error:
        return "syntax-error", summary
    elif has_counterexample:
        return "counterexample", summary
    else:
        return "pass", summary


def build_prompt(extract, output_name, with_reference=False):
    """Assemble prompt from template + injected content."""
    template = read_file(TEMPLATE)
    if not template:
        print("  Prompt template not found at "
              "scripts/prompts/formalization/check-alloy.md", file=sys.stderr)
        sys.exit(1)

    # Optionally load reference model
    reference_model = ""
    if with_reference:
        ref_path = PROMPTS_DIR / "alloy-reference.als"
        reference_model = read_file(ref_path)
        if not reference_model:
            print("  Warning: no reference model at "
                  "scripts/prompts/formalization/alloy-reference.als",
                  file=sys.stderr)

    # Handle conditional reference section
    if reference_model:
        template = re.sub(r"\{\{#if reference_model\}\}", "", template)
        template = re.sub(r"\{\{/if\}\}", "", template, count=1)
    else:
        template = re.sub(
            r"\{\{#if reference_model\}\}.*?\{\{/if\}\}", "", template,
            flags=re.DOTALL, count=1)

    return template.replace(
        "{{reference_model}}", reference_model
    ).replace(
        "{{extract}}", extract
    ).replace(
        "{{output_name}}", output_name
    )


def invoke_claude(prompt, out_path, model="sonnet", effort=None,
                  is_fix=False):
    """Call claude -p with Write tool to generate the .als file directly."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", "16",
        "--tools", "Read,Write",
        "--allowedTools", "Read,Write",
        "--effort", effort or "high",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    if is_fix:
        full_prompt = f"""{prompt}

First read the file at: {out_path}
Then write the corrected Alloy model to: {out_path}
"""
    else:
        full_prompt = f"""{prompt}

Write the complete Alloy model to: {out_path}
"""

    start = time.time()
    result = subprocess.run(
        cmd, input=full_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False, elapsed

    # Parse JSON for usage stats
    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0)
        inp = (usage.get("input_tokens", 0) +
               usage.get("cache_read_input_tokens", 0) +
               usage.get("cache_creation_input_tokens", 0))
        out = usage.get("output_tokens", 0)
        print(f"  [{elapsed:.0f}s] in:{inp} out:{out} ${cost:.4f}",
              file=sys.stderr)
        # Log subtype on failure (e.g., error_max_turns)
        subtype = data.get("subtype", "")
        if subtype and subtype != "success":
            print(f"  [WARN] stop: {subtype}", file=sys.stderr)
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s]", file=sys.stderr)

    return True, elapsed


def run_alloy(als_path):
    """Run the Alloy checker on the generated model.

    Returns (output_text, elapsed) or (None, 0) if Alloy not available.
    """
    alloy_jar = os.environ.get("ALLOY_JAR", ALLOY_JAR_DEFAULT)
    if not Path(alloy_jar).exists():
        print("  Alloy not installed — skipping check", file=sys.stderr)
        print(f"  Set ALLOY_JAR or install Alloy.app", file=sys.stderr)
        return None, 0.0

    print("  [ALLOY] running checker...", file=sys.stderr)
    start = time.time()
    try:
        result = subprocess.run(
            ["java", "-jar", str(alloy_jar), "exec", "-f", str(als_path)],
            capture_output=True, text=True, timeout=120,
            cwd=str(Path(als_path).parent),
        )
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"  [ALLOY] TIMEOUT ({elapsed:.0f}s)", file=sys.stderr)
        return "Type error: model timed out (scope too large or infinite recursion)", elapsed
    elapsed = time.time() - start
    print(f"  [ALLOY] {elapsed:.0f}s", file=sys.stderr)

    output = (result.stdout or "") + "\n" + (result.stderr or "")
    return output.strip(), elapsed


def parse_alloy_results(output):
    """Parse Alloy output to detect counterexamples.

    Returns (has_counterexample, summary_lines).

    The Alloy CLI checker reports results like:
      01. check Irreflexive              0       UNSAT
      02. check Total                    1/1     SAT
    SAT on a check command means a counterexample was found.
    UNSAT means the assertion holds within scope.
    """
    if not output:
        return False, []

    lines = output.strip().split("\n")
    has_counterexample = False
    summary = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Detect SAT on check commands = counterexample found
        if re.search(r"check\s+\S+.*\bSAT\b", line):
            summary.append(line)
            # SAT (not UNSAT) on a check = counterexample
            if not re.search(r"\bUNSAT\b", line):
                has_counterexample = True
        elif re.search(r"check\s+\S+.*\bUNSAT\b", line):
            summary.append(line)
        # Legacy format: "Counterexample found" / "No counterexample found"
        elif "counterexample" in line.lower():
            summary.append(line)
            if "no counterexample" not in line.lower():
                has_counterexample = True
        elif "instance found" in line.lower():
            summary.append(line)
        elif "no instance found" in line.lower():
            summary.append(line)
        elif "executing" in line.lower():
            summary.append(line)

    return has_counterexample, summary


def log_usage(asn_label, llm_elapsed, alloy_elapsed, has_counterexample,
              prop_label=None):
    """Append a usage entry to the log."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "check-alloy",
            "asn": asn_label,
            "llm_elapsed_s": round(llm_elapsed, 1),
            "alloy_elapsed_s": round(alloy_elapsed, 1),
            "counterexample": has_counterexample,
        }
        if prop_label:
            entry["property"] = prop_label
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def make_result(prop, out_dir):
    """Create a result dict for a property."""
    filename = sanitize_filename(prop["label"], prop["name"])
    return {
        "label": prop["label"],
        "name": prop["name"],
        "status": None,
        "checks": 0,
        "llm_elapsed": 0.0,
        "alloy_elapsed": 0.0,
        "als_path": out_dir / f"{filename}.als",
    }


def generate_one(result, prop, definitions, asn_label, args,
                  syntax_ref=""):
    """Generate the .als file for a single property.

    Mutates result in place. Returns result.
    """
    als_path = result["als_path"]

    prompt = build_property_prompt(definitions, prop, syntax_ref=syntax_ref)
    print(f"\n  [{prop['label']}] {prop['name']}  "
          f"({len(prompt) // 1024}KB prompt)", file=sys.stderr)

    if args.dry_run:
        result["status"] = "dry-run"
        return result

    # Skip generation if file exists and --recheck
    if args.recheck and als_path.exists():
        print(f"    [REUSE] {als_path.name}", file=sys.stderr)
        result["status"] = "generated"
        return result

    print(f"    [LLM] generating ({args.model})...", file=sys.stderr)
    success, llm_elapsed = invoke_claude(prompt, als_path,
                                          args.model, args.effort)
    result["llm_elapsed"] = llm_elapsed

    if not success or not als_path.exists():
        print(f"    No model generated", file=sys.stderr)
        result["status"] = "gen-fail"
        log_usage(asn_label, llm_elapsed, 0, False,
                  prop_label=prop["label"])
        return result

    print(f"    [WROTE] {als_path.relative_to(WORKSPACE)}", file=sys.stderr)
    result["status"] = "generated"
    log_usage(asn_label, llm_elapsed, 0, False,
              prop_label=prop["label"])
    return result


def check_one(result, asn_label, prop=None, definitions=None, args=None,
              syntax_ref=""):
    """Run Alloy checker on one generated .als file, with repair loop.

    Tier 1 (syntax/type, up to MAX_TIER1): fix with error + .als only.
    Tier 2 (persistent, up to MAX_TIER2): fix with full property context.
    Counterexamples go straight to result (not fixable by retry).

    Mutates result in place. Returns result.
    """
    als_path = result["als_path"]
    label = result["label"]

    if not als_path.exists():
        return result

    tier1_attempts = 0
    tier2_attempts = 0
    model = args.model if args else "sonnet"
    effort = args.effort if args else None

    while True:
        tier_label = ""
        if tier1_attempts or tier2_attempts:
            tier_label = (f" [T1:{tier1_attempts}/{MAX_TIER1}"
                          f" T2:{tier2_attempts}/{MAX_TIER2}]")
        print(f"\n  [{label}] checking {als_path.name}...{tier_label}",
              file=sys.stderr)

        alloy_output, alloy_elapsed = run_alloy(als_path)
        result["alloy_elapsed"] += alloy_elapsed

        if alloy_output is None:
            result["status"] = "no-alloy"
            return result

        status, summary = classify_alloy_error(alloy_output)
        result["alloy_output"] = alloy_output
        result["checks"] = len([s for s in summary
                                if re.search(r"\bSAT\b", s)
                                and not re.search(r"\bUNSAT\b", s)])

        for line in summary:
            print(f"    {line}", file=sys.stderr)

        # Pass or counterexample — done
        if status == "pass":
            result["status"] = "pass"
            log_usage(asn_label, result["llm_elapsed"], result["alloy_elapsed"],
                      False, prop_label=label)
            return result

        if status == "counterexample":
            result["status"] = "counterexample"
            log_usage(asn_label, result["llm_elapsed"], result["alloy_elapsed"],
                      True, prop_label=label)
            return result

        # Syntax/type error — attempt repair
        # Annotate error output with source lines for the fix agent
        annotated_errors = annotate_errors(alloy_output, als_path)

        # Print error output
        for line in alloy_output.split("\n"):
            line = line.strip()
            if line and not line.startswith("at "):
                print(f"    {line}", file=sys.stderr)

        # Tier 1: minimal fix (error + code only)
        if tier1_attempts < MAX_TIER1:
            tier1_attempts += 1
            print(f"    [FIX] Tier 1 attempt {tier1_attempts}/{MAX_TIER1}",
                  file=sys.stderr)
            fix_prompt = build_fix_prompt(als_path, annotated_errors,
                                         syntax_ref=syntax_ref)
            if fix_prompt:
                success, fix_elapsed = invoke_claude(
                    fix_prompt, als_path, model, effort, is_fix=True)
                result["llm_elapsed"] += fix_elapsed
                if success and als_path.exists():
                    continue  # Re-check
            # Fix failed — fall through to tier 2

        # Tier 2: fix with full context
        if tier2_attempts < MAX_TIER2 and prop and definitions:
            tier2_attempts += 1
            print(f"    [FIX] Tier 2 attempt {tier2_attempts}/{MAX_TIER2}",
                  file=sys.stderr)
            fix_prompt = build_fix_prompt(
                als_path, annotated_errors, definitions, prop,
                syntax_ref=syntax_ref)
            if fix_prompt:
                success, fix_elapsed = invoke_claude(
                    fix_prompt, als_path, model, effort, is_fix=True)
                result["llm_elapsed"] += fix_elapsed
                if success and als_path.exists():
                    continue  # Re-check

        # Exhausted all retries — escalate
        print(f"    [ESCALATE] Retries exhausted "
              f"(T1:{tier1_attempts} T2:{tier2_attempts})",
              file=sys.stderr)
        result["status"] = "syntax-error"
        log_usage(asn_label, result["llm_elapsed"], result["alloy_elapsed"],
                  False, prop_label=label)
        return result


def print_summary(asn_label, results):
    """Print a summary table to stderr."""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  {asn_label} Alloy Check ({len(results)} properties)",
          file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    STATUS_DISPLAY = {
        "pass": "pass",
        "counterexample": "COUNTEREXAMPLE",
        "syntax-error": "SYNTAX ERROR",
        "gen-fail": "GEN FAIL",
        "no-alloy": "no-alloy",
        "generated": "generated",
        "dry-run": "dry-run",
    }

    for r in results:
        status = STATUS_DISPLAY.get(r["status"], r["status"])
        checks_str = (f"{r['checks']} checks" if r["checks"]
                      else "")
        total = r["llm_elapsed"] + r["alloy_elapsed"]
        elapsed_str = f"{total:.0f}s" if total else ""
        detail = ", ".join(filter(None, [checks_str, elapsed_str]))
        detail_str = f"  ({detail})" if detail else ""
        print(f"  {r['label']:<14s} {r['name']:<30s} {status}{detail_str}",
              file=sys.stderr)

    # Totals
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    parts = []
    for status in ["pass", "syntax-error", "counterexample", "gen-fail",
                    "generated", "dry-run"]:
        if status in counts:
            parts.append(f"{STATUS_DISPLAY[status]}: {counts[status]}")
    parts.append(f"Total: {len(results)}")

    print(f"\n  {' | '.join(parts)}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


def next_review_number(asn_label):
    """Find the next review number for this ASN (shared sequence with all reviews)."""
    existing = sorted(REVIEWS_DIR.glob(f"{asn_label}-review-*.md"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"-review-(\d+)\.md$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def next_run_number(asn_label):
    """Find the next Alloy run number for this ASN (independent of review numbers)."""
    existing = sorted((ALLOY_DIR / asn_label).glob("run-*"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"run-(\d+)$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def generate_review(asn_label, results, properties, run_num=None):
    """Generate a review markdown from Alloy check results.

    Only produces a review if there are counterexamples or syntax errors.
    Returns the review path, or None if all passed.
    """
    failures = [r for r in results
                if r["status"] in ("counterexample", "syntax-error")]
    if not failures:
        return None

    # Build a property lookup for body text
    prop_by_label = {p["label"]: p for p in properties}

    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = REVIEWS_DIR / f"{asn_label}-review-{review_num}.md"

    lines = [f"# Review of {asn_label}\n"]
    if run_num is not None:
        lines.append(f"Based on Alloy run-{run_num}\n")
    lines.append("## REVISE\n")

    issue_num = 0
    for r in failures:
        issue_num += 1
        prop = prop_by_label.get(r["label"], {})
        prop_type = prop.get("type", "?")
        try:
            als_rel = r["als_path"].relative_to(WORKSPACE)
        except ValueError:
            als_rel = r["als_path"]

        if r["status"] == "counterexample":
            lines.append(
                f"### Issue {issue_num}: {r['label']} — "
                f"Alloy counterexample\n"
            )
            lines.append(
                f"**{asn_label}, {r['label']} {r['name']}** ({prop_type}): "
                f"Alloy bounded model checking found a counterexample.\n"
            )
            lines.append(
                f"**Problem**: The Alloy model at `{als_rel}` produced a "
                f"counterexample at bounded scope, suggesting the property "
                f"as stated may be too strong, missing a precondition, or "
                f"the model may not faithfully represent the ASN's intent.\n"
            )
            # Include ASN property statement
            prop_body = prop.get("body", "")
            if prop_body:
                lines.append("**ASN property statement**:\n")
                lines.append(prop_body.strip())
                lines.append("")
            # Include Alloy model source
            als_path = r.get("als_path")
            if als_path and als_path.exists():
                als_source = als_path.read_text()
                lines.append(f"**Alloy model** (`{als_rel}`):\n```alloy")
                lines.append(als_source.strip())
                lines.append("```\n")
            # Include Alloy checker output
            alloy_out = r.get("alloy_output", "")
            if alloy_out:
                lines.append("**Alloy checker output**:\n```")
                lines.append(alloy_out[:2000])
                lines.append("```\n")
            lines.append(
                f"**Required**: Investigate whether the counterexample "
                f"reveals a genuine spec issue (missing precondition, "
                f"over-strong claim) or a modeling artifact. If the "
                f"property needs revision, update the formal statement "
                f"in the ASN.\n"
            )
        elif r["status"] == "syntax-error":
            lines.append(
                f"### Issue {issue_num}: {r['label']} — "
                f"Alloy syntax/type error\n"
            )
            lines.append(
                f"**{asn_label}, {r['label']} {r['name']}** ({prop_type}): "
                f"The generated Alloy model has a syntax or type error.\n"
            )
            # Include error details
            alloy_out = r.get("alloy_output", "")
            error_lines = [
                l.strip() for l in alloy_out.split("\n")
                if "error" in l.lower()
                and not l.strip().startswith("---")
            ][:5]
            if error_lines:
                lines.append(
                    f"**Problem**: "
                    + "; ".join(error_lines) + "\n"
                )
            else:
                lines.append(
                    f"**Problem**: Alloy could not parse or type-check "
                    f"the model at `{als_rel}`.\n"
                )
            lines.append(
                f"**Required**: Regenerate the Alloy model. If the error "
                f"persists across regenerations, the property statement "
                f"in the ASN may be ambiguous or under-specified.\n"
            )

    # DEFER section for passes (informational)
    passed = [r for r in results if r["status"] == "pass"]
    if passed:
        lines.append("## DEFER\n")
        lines.append(
            f"### Topic 1: {len(passed)} properties passed bounded check\n"
        )
        labels = ", ".join(r["label"] for r in passed)
        lines.append(
            f"Properties {labels} passed Alloy bounded model checking "
            f"with no counterexamples found. Note: bounded checking is "
            f"not a proof — it only searches within a finite scope.\n"
        )
        lines.append(
            f"**Why defer**: No action needed. Passing bounded check "
            f"increases confidence but does not constitute verification.\n"
        )

    verdict = "CONVERGED" if not failures else "REVISE"
    lines.append(f"VERDICT: {verdict}\n")

    review_path.write_text("\n".join(lines))
    return review_path


def run_all_in_one(args, asn_path, asn_label, extract):
    """Original monolithic generation mode."""
    output_name = derive_output_name(asn_path)
    als_path = ALLOY_DIR / f"{output_name}.als"

    print(f"  [ALLOY] {asn_label} -> {output_name}.als (all-in-one)",
          file=sys.stderr)

    prompt = build_prompt(extract, output_name,
                          with_reference=args.with_reference)
    print(f"  Prompt: {len(prompt) // 1024}KB (~{len(prompt) // 4} tokens est.)",
          file=sys.stderr)

    if args.dry_run:
        print(f"  [DRY RUN] Would invoke {args.model} with -p --allowedTools Write",
              file=sys.stderr)
        return

    ALLOY_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  [LLM] generating model ({args.model})...", file=sys.stderr)
    success, llm_elapsed = invoke_claude(prompt, als_path,
                                          args.model, args.effort)

    if not success or not als_path.exists():
        print("  No Alloy model generated", file=sys.stderr)
        sys.exit(1)

    print(f"  [WROTE] {als_path.relative_to(WORKSPACE)}", file=sys.stderr)

    if args.skip_check:
        log_usage(asn_label, llm_elapsed, 0, False)
        print(str(als_path))
        return

    alloy_output, alloy_elapsed = run_alloy(als_path)
    if alloy_output is None:
        log_usage(asn_label, llm_elapsed, 0, False)
        print(str(als_path))
        return

    has_counterexample, summary = parse_alloy_results(alloy_output)
    log_usage(asn_label, llm_elapsed, alloy_elapsed, has_counterexample)
    print(str(als_path))

    if has_counterexample:
        print(f"  [RESULT] COUNTEREXAMPLE FOUND", file=sys.stderr)
    else:
        print(f"  [RESULT] No counterexamples", file=sys.stderr)

    for line in summary:
        print(f"    {line}", file=sys.stderr)

    if has_counterexample:
        sys.exit(2)


CONSULT_SCRIPT = WORKSPACE / "scripts" / "consult_for_revision.py"
REVISE_SCRIPT = WORKSPACE / "scripts" / "revise-asn.py"
COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


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
        description="Generate Alloy models from ASN and run bounded checking")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="sonnet",
                        choices=["opus", "sonnet"],
                        help="Model (default: sonnet)")
    parser.add_argument("--effort", default=None,
                        help="Thinking effort level")
    parser.add_argument("--with-reference", action="store_true",
                        help="Include reference model in prompt for syntax grounding")
    parser.add_argument("--skip-check", action="store_true",
                        help="Generate model only, don't run Alloy")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show property list and prompt sizes")
    parser.add_argument("--property", "-p", default=None,
                        help="Check specific properties by label, comma-separated (e.g., T1,T3,TA0)")
    parser.add_argument("--all-in-one", action="store_true",
                        help="Monolithic mode: single .als for all properties")
    parser.add_argument("--no-revise", action="store_true",
                        help="Stop after check + review, skip consult/revise/commit")
    parser.add_argument("--recheck", action="store_true",
                        help="Reuse existing .als files, skip generation")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/modeling/asns/",
              file=sys.stderr)
        sys.exit(1)

    # Load extract
    extract_path = EXTRACTS_DIR / f"{asn_label}-extract.md"
    extract = read_file(extract_path)
    if not extract:
        print(f"  No extract found at {extract_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        print(f"  Run: python scripts/extract-properties.py {args.asn}",
              file=sys.stderr)
        sys.exit(1)

    # All-in-one mode: original monolithic behavior
    if args.all_in_one:
        run_all_in_one(args, asn_path, asn_label, extract)
        return

    # Load syntax reference for prompt injection
    syntax_ref = read_file(SYNTAX_REF)
    if not syntax_ref:
        print("  Warning: no syntax reference at "
              "scripts/prompts/formalization/alloy-syntax.md",
              file=sys.stderr)

    # Per-property mode
    parsed = parse_extract(extract)
    properties = parsed["properties"]
    definitions = parsed["definitions"]

    if not properties:
        print(f"  No properties found in extract", file=sys.stderr)
        sys.exit(1)

    # Filter to specific properties if requested
    if args.property:
        targets = [t.strip() for t in args.property.split(",")]
        matches = []
        for target in targets:
            found = [p for p in properties if p["label"] == target]
            if not found:
                # Try case-insensitive prefix match
                found = [p for p in properties
                         if p["label"].lower().startswith(target.lower())]
            if not found:
                print(f"  No property matching '{target}'", file=sys.stderr)
                print(f"  Available: {', '.join(p['label'] for p in properties)}",
                      file=sys.stderr)
                sys.exit(1)
            matches.extend(found)
        properties = matches

    if args.recheck:
        # Find the latest run directory
        existing = sorted(
            (ALLOY_DIR / asn_label).glob("run-*"),
            key=lambda p: int(re.search(r"run-(\d+)", p.name).group(1))
                if re.search(r"run-(\d+)", p.name) else 0
        )
        if not existing:
            print("  No existing run directory to recheck", file=sys.stderr)
            sys.exit(1)
        out_dir = existing[-1]
        m = re.search(r"run-(\d+)", out_dir.name)
        run_num = int(m.group(1)) if m else 1
        print(f"  [RECHECK] Using {out_dir.name}", file=sys.stderr)
    else:
        run_num = next_run_number(asn_label)
        out_dir = ALLOY_DIR / asn_label / f"run-{run_num}"
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"  {asn_label} — {len(properties)} properties, "
          f"definitions {len(definitions)}B", file=sys.stderr)

    # Phase 1: Generate all .als files
    results = []
    for prop in properties:
        result = make_result(prop, out_dir)
        generate_one(result, prop, definitions, asn_label, args,
                      syntax_ref=syntax_ref)
        results.append(result)

    gen_count = sum(1 for r in results if r["status"] == "generated")
    if not args.dry_run:
        print(f"\n  Generated {gen_count}/{len(results)} models",
              file=sys.stderr)

    # Phase 2: Check all generated .als files (with repair loop)
    prop_by_label = {p["label"]: p for p in properties}
    if not args.skip_check and not args.dry_run:
        checkable = [r for r in results if r["status"] == "generated"]
        if checkable:
            print(f"\n  {'='*50}", file=sys.stderr)
            print(f"  Checking {len(checkable)} models...", file=sys.stderr)
            print(f"  {'='*50}", file=sys.stderr)
            for result in checkable:
                prop = prop_by_label.get(result["label"])
                check_one(result, asn_label,
                          prop=prop, definitions=definitions, args=args,
                          syntax_ref=syntax_ref)

    # Summary
    any_counterexample = any(r["status"] == "counterexample"
                             for r in results)

    if len(results) > 1 or args.dry_run:
        print_summary(asn_label, results)

    # Phase 3: Generate review → consult → revise → commit
    if not args.skip_check and not args.dry_run:
        review_path = generate_review(asn_label, results, properties,
                                       run_num=run_num)
        if review_path:
            print(f"\n  [REVIEW] {review_path.relative_to(WORKSPACE)}",
                  file=sys.stderr)

            if not args.no_revise:
                # Consult
                consultation_path = step_consult(args.asn,
                                                  str(review_path))

                # Revise
                asn_result, revise_converged = step_revise(
                    args.asn, consultation_path=consultation_path)

                if revise_converged:
                    print(f"  [PIPELINE] Revise made no changes",
                          file=sys.stderr)

                # Commit
                step_commit(f"alloy(asn): {asn_label} — "
                            f"Alloy check + revise")
        else:
            print(f"\n  [REVIEW] All checks passed — no review generated",
                  file=sys.stderr)
            if not args.no_revise:
                step_commit(f"alloy(asn): {asn_label} — "
                            f"all properties pass bounded check")

    # Output: list of generated .als paths (for scripting)
    for r in results:
        if r["als_path"].exists():
            print(str(r["als_path"]))

    if any_counterexample:
        sys.exit(2)


if __name__ == "__main__":
    main()
