#!/usr/bin/env python3
"""
Alloy review pipeline — generate+check → review → consult → revise → commit.

Per-property: parses the extract into individual properties, generates one .als
per property using an agentic Claude session (with Bash access to run Alloy
and self-fix syntax errors), produces a review if failures remain, then feeds
the review into the consult → revise → commit cycle.

Requires: formal statements in vault/project-model/ASN-NNNN/ (run normalize.py first)
Requires: Alloy installed at /Applications/Alloy.app (macOS) or ALLOY_JAR set.

Usage:
    python scripts/run-alloy-review.py 1                    # full pipeline
    python scripts/run-alloy-review.py 1 --property T1      # single property
    python scripts/run-alloy-review.py 1 --no-revise         # stop after check + review
    python scripts/run-alloy-review.py 1 --skip-check       # generate only
    python scripts/run-alloy-review.py 1 --dry-run           # show property list
    python scripts/run-alloy-review.py 1 --all-in-one        # monolithic mode
    python scripts/run-alloy-review.py 1 --max-turns 16      # more agentic turns
    python scripts/run-alloy-review.py 1 --no-cleanup         # keep Alloy artifacts for debugging
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import (WORKSPACE, ASNS_DIR, ALLOY_DIR, REVIEWS_DIR,
                    USAGE_LOG, sorted_reviews, next_review_number,
                    sanitize_filename, formal_stmts)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "formalization"
TEMPLATE = PROMPTS_DIR / "check-alloy.md"
PROPERTY_TEMPLATE = PROMPTS_DIR / "check-alloy-property.md"
REVIEW_TEMPLATE = PROMPTS_DIR / "write-alloy-review.md"
SYNTAX_REF = PROMPTS_DIR / "alloy-syntax.md"

ALLOY_JAR_DEFAULT = (
    "/Applications/Alloy.app/Contents/Resources/org.alloytools.alloy.dist.jar"
)


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


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


# Header patterns:
#   ## LABEL — Name (TYPE, construct)    — with type
#   ## LABEL — Name                      — without type
#   ## LABEL — Name (DEFINITION, function) — definition
_PROP_WITH_TYPE_RE = re.compile(
    r"^##\s+(.+?)\s+—\s+(\w+)\s+\((\w+),\s+(.+?)\)\s*$"
)
_PROP_NO_TYPE_RE = re.compile(
    r"^##\s+(.+?)\s+—\s+(.+?)\s*$"
)


def parse_extract(text):
    """Parse an extract into definitions and properties.

    Returns dict with:
      definitions: str — all definition sections concatenated
      properties: list[dict] — each with label, name, type, construct, body
    """
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)

    definitions = []
    properties = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        first_line = section.split("\n", 1)[0]

        # Check for definition (DEFINITION in type tag)
        m = _PROP_WITH_TYPE_RE.match(first_line)
        if m and m.group(3) == "DEFINITION":
            definitions.append(section)
            continue

        # Legacy: ## Definition — Name
        if section.startswith("## Definition"):
            definitions.append(section)
            continue

        # Property with type tag
        if m:
            properties.append({
                "label": m.group(1),
                "name": m.group(2),
                "type": m.group(3),
                "construct": m.group(4),
                "body": section,
            })
            continue

        # Property without type tag
        m2 = _PROP_NO_TYPE_RE.match(first_line)
        if m2:
            properties.append({
                "label": m2.group(1),
                "name": m2.group(2),
                "type": "",
                "construct": "",
                "body": section,
            })

    return {
        "definitions": "\n\n".join(definitions),
        "properties": properties,
    }


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


AGENT_TIMEOUT = 900  # 15 minutes


def invoke_claude(prompt, out_path, model="opus", effort=None,
                  max_turns=12, write_instruction=None,
                  tools="Read,Write,Bash", timeout=AGENT_TIMEOUT):
    """Call claude -p in agent mode to generate a file.

    Default tools include Bash so the agent can self-check Alloy models.
    Returns (success, elapsed, cost).  On timeout raises subprocess.TimeoutExpired.
    """
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--tools", tools,
        "--allowedTools", tools,
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort or "high"

    if write_instruction:
        full_prompt = f"""{prompt}

{write_instruction}: {out_path}
"""
    else:
        full_prompt = f"""{prompt}

Write the complete Alloy model to: {out_path}
"""

    start = time.time()
    result = subprocess.run(
        cmd, input=full_prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE), timeout=timeout,
    )
    elapsed = time.time() - start

    cost = 0.0
    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False, elapsed, cost

    # Parse JSON for usage stats
    try:
        data = json.loads(result.stdout)
        usage = data.get("usage", {})
        cost = data.get("total_cost_usd", 0) or 0.0
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

    return True, elapsed, cost


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
              prop_label=None, cost=0.0, model=None):
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
        if cost:
            entry["cost_usd"] = round(cost, 4)
        if model:
            entry["model"] = model
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
        "model": None,
        "checks": 0,
        "llm_elapsed": 0.0,
        "alloy_elapsed": 0.0,
        "cost": 0.0,
        "als_path": out_dir / f"{filename}.als",
    }


def generate_one(result, prop, definitions, asn_label, args,
                  syntax_ref=""):
    """Generate and self-check the .als file for a single property.

    The agent writes the model, runs Alloy, and fixes syntax errors
    autonomously.  The script then runs a final Alloy check to confirm
    and classify the result (pass / counterexample / syntax-error).

    Mutates result in place. Returns result.
    """
    als_path = result["als_path"]

    prompt = build_property_prompt(definitions, prop, syntax_ref=syntax_ref)

    # Append agent self-check instructions
    alloy_jar = os.environ.get("ALLOY_JAR", ALLOY_JAR_DEFAULT)
    prompt += f"""

## Self-check instructions

After writing the Alloy model to `{als_path}`, verify it by running:

    cd {als_path.parent} && java -jar {alloy_jar} exec -f {als_path.name}

**If you see syntax or type errors**: fix the model and re-run the checker.
Repeat until the model is syntactically valid.

**If you see counterexamples** (SAT on a check command): this is a valid
result — it means the property does not hold. Do NOT modify the model to
avoid counterexamples. Leave the model as-is and stop.

**If all checks show UNSAT**: the property holds within scope. Stop.
"""

    print(f"\n  [{prop['label']}] {prop['name']}  "
          f"({len(prompt) // 1024}KB prompt)", file=sys.stderr)

    if args.dry_run:
        result["status"] = "dry-run"
        return result

    # Skip generation if file already exists (--recheck or --run with prior results)
    if als_path.exists() and (args.recheck or args.run is not None):
        print(f"    [REUSE] {als_path.name}", file=sys.stderr)
    else:
        model_used = args.model
        print(f"    [LLM] generating ({model_used})...", file=sys.stderr)
        try:
            success, llm_elapsed, cost = invoke_claude(
                prompt, als_path, model_used, args.effort,
                max_turns=args.max_turns)
        except subprocess.TimeoutExpired:
            llm_elapsed = AGENT_TIMEOUT
            cost = 0.0
            success = False
            print(f"    [TIMEOUT] {model_used} timed out after "
                  f"{AGENT_TIMEOUT // 60}min", file=sys.stderr)

            # Remove any partial file from timed-out agent
            if als_path.exists():
                als_path.unlink()

            # Fallback to sonnet
            if model_used != "sonnet":
                model_used = "sonnet"
                print(f"    [FALLBACK] retrying with {model_used}...",
                      file=sys.stderr)
                try:
                    success, fallback_elapsed, cost = invoke_claude(
                        prompt, als_path, model_used, args.effort,
                        max_turns=args.max_turns)
                    llm_elapsed += fallback_elapsed
                except subprocess.TimeoutExpired:
                    llm_elapsed += AGENT_TIMEOUT
                    print(f"    [TIMEOUT] {model_used} also timed out",
                          file=sys.stderr)

                model_used = f"{args.model}\u2192sonnet"

        result["llm_elapsed"] = llm_elapsed
        result["cost"] = cost
        result["model"] = model_used

        if not success or not als_path.exists():
            print(f"    No model generated", file=sys.stderr)
            result["status"] = "gen-fail"
            log_usage(asn_label, llm_elapsed, 0, False,
                      prop_label=prop["label"], cost=cost,
                      model=model_used)
            return result

        print(f"    [WROTE] {als_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Final Alloy check to confirm and classify
    if not args.skip_check:
        alloy_output, alloy_elapsed = run_alloy(als_path)
        result["alloy_elapsed"] = alloy_elapsed

        if alloy_output is None:
            result["status"] = "no-alloy"
            log_usage(asn_label, result["llm_elapsed"], 0, False,
                      prop_label=prop["label"], cost=result.get("cost", 0),
                      model=result.get("model"))
            return result

        status, summary = classify_alloy_error(alloy_output)
        result["alloy_output"] = alloy_output
        result["checks"] = len([s for s in summary
                                if re.search(r"\bSAT\b", s)
                                and not re.search(r"\bUNSAT\b", s)])

        for line in summary:
            print(f"    {line}", file=sys.stderr)

        result["status"] = status
        has_ce = status == "counterexample"
        log_usage(asn_label, result["llm_elapsed"], alloy_elapsed,
                  has_ce, prop_label=prop["label"],
                  cost=result.get("cost", 0),
                  model=result.get("model"))
    else:
        result["status"] = "generated"
        log_usage(asn_label, result["llm_elapsed"], 0, False,
                  prop_label=prop["label"], cost=result.get("cost", 0),
                  model=result.get("model"))

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
        cost = r.get("cost", 0)
        cost_str = f"${cost:.4f}" if cost else ""
        model_str = r.get("model", "") or ""
        detail = ", ".join(filter(None, [checks_str, elapsed_str, cost_str,
                                         model_str]))
        detail_str = f"  ({detail})" if detail else ""
        print(f"  {r['label']:<14s} {r['name']:<30s} {status}{detail_str}",
              file=sys.stderr)

    # Totals
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    total_cost = sum(r.get("cost", 0) for r in results)

    parts = []
    for status in ["pass", "syntax-error", "counterexample", "gen-fail",
                    "generated", "dry-run"]:
        if status in counts:
            parts.append(f"{STATUS_DISPLAY[status]}: {counts[status]}")
    parts.append(f"Total: {len(results)}")
    if total_cost:
        parts.append(f"${total_cost:.4f}")

    print(f"\n  {' | '.join(parts)}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


def next_run_number(asn_label):
    """Find the next Alloy modeling number for this ASN (independent of review numbers)."""
    existing = sorted((ALLOY_DIR / asn_label).glob("modeling-*"))
    if not existing:
        return 1
    nums = []
    for p in existing:
        m = re.search(r"modeling-(\d+)$", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def build_review_evidence(results, properties):
    """Build the counterexample evidence section for the review prompt.

    Returns (evidence_text, passed_summary).
    """
    prop_by_label = {p["label"]: p for p in properties}
    evidence_parts = []
    issue_num = 0

    failures = [r for r in results
                if r["status"] in ("counterexample", "syntax-error")]

    for r in failures:
        issue_num += 1
        prop = prop_by_label.get(r["label"], {})
        try:
            als_rel = r["als_path"].relative_to(WORKSPACE)
        except ValueError:
            als_rel = r["als_path"]

        part = [f"### {r['label']} — {r['name']} ({r['status']})\n"]

        # ASN property statement
        prop_body = prop.get("body", "")
        if prop_body:
            part.append("**ASN property statement**:\n")
            part.append(prop_body.strip())
            part.append("")

        # Alloy model source
        als_path = r.get("als_path")
        if als_path and als_path.exists():
            als_source = als_path.read_text()
            part.append(f"**Alloy model** (`{als_rel}`):\n```alloy")
            part.append(als_source.strip())
            part.append("```\n")

        # Checker output
        alloy_out = r.get("alloy_output", "")
        if alloy_out:
            part.append("**Alloy checker output**:\n```")
            part.append(alloy_out[:2000])
            part.append("```\n")

        evidence_parts.append("\n".join(part))

    evidence_text = "\n---\n\n".join(evidence_parts) if evidence_parts else "None"

    # Passed summary
    passed = [r for r in results if r["status"] == "pass"]
    if passed:
        labels = ", ".join(r["label"] for r in passed)
        passed_summary = (
            f"{len(passed)} properties passed bounded check (no "
            f"counterexamples within scope): {labels}"
        )
    else:
        passed_summary = "None"

    return evidence_text, passed_summary


def generate_review(asn_label, results, properties, run_num=None,
                    asn_path=None, model="opus", effort=None):
    """Generate a review by calling an LLM to analyze counterexample evidence.

    Accumulates all counterexample data (ASN property, Alloy model, checker
    output), injects it alongside the full ASN, and asks Opus to write an
    intelligent review that classifies each finding.

    Returns the review path, or None if all passed.
    """
    failures = [r for r in results
                if r["status"] in ("counterexample", "syntax-error")]
    if not failures:
        return None

    # Load review prompt template
    template = read_file(REVIEW_TEMPLATE)
    if not template:
        print("  Review template not found at "
              "scripts/prompts/formalization/write-alloy-review.md",
              file=sys.stderr)
        return None

    # Read the full ASN for context
    asn_text = ""
    if asn_path:
        asn_text = read_file(asn_path)
    if not asn_text:
        # Fallback to extract
        asn_num = int(re.search(r'\d+', asn_label).group())
        asn_text = read_file(formal_stmts(asn_num))

    # Build evidence from results
    evidence_text, passed_summary = build_review_evidence(results, properties)

    # Assemble prompt
    prompt = template.replace(
        "{{asn_text}}", asn_text
    ).replace(
        "{{counterexample_evidence}}", evidence_text
    ).replace(
        "{{passed_summary}}", passed_summary
    )

    # Determine review path
    (REVIEWS_DIR / asn_label).mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(asn_label)
    review_path = REVIEWS_DIR / asn_label / f"review-{review_num}.md"

    print(f"  [REVIEW] Calling {model} to analyze {len(failures)} "
          f"counterexample(s)...", file=sys.stderr)
    print(f"  [REVIEW] Prompt: {len(prompt) // 1024}KB", file=sys.stderr)

    success, elapsed, _cost = invoke_claude(
        prompt, review_path, model=model, effort=effort,
        write_instruction="Write the review to",
        tools="Read,Write")

    if not success or not review_path.exists():
        print(f"  [REVIEW] LLM review generation failed", file=sys.stderr)
        return None

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
    success, llm_elapsed, _cost = invoke_claude(prompt, als_path,
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


COMMIT_SCRIPT = WORKSPACE / "scripts" / "commit.py"


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


def cleanup_property_artifacts(als_path):
    """Remove Alloy build artifacts for a single property.

    Alloy creates a subdirectory named after the .als file (without extension)
    for counterexample output. Remove it after each property check.
    """
    artifact_dir = als_path.parent / als_path.stem
    if artifact_dir.is_dir():
        shutil.rmtree(artifact_dir)
        print(f"    [CLEANUP] {artifact_dir.name}/", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Alloy models from ASN and run bounded checking")
    parser.add_argument("asn",
                        help="ASN number (e.g., 4, 0004, ASN-0004) or path")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"],
                        help="Model (default: opus)")
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
                        help="(deprecated — Alloy now always stops after review)")
    parser.add_argument("--recheck", action="store_true",
                        help="Reuse existing .als files, skip generation")
    parser.add_argument("--max-turns", type=int, default=12,
                        help="Max agentic turns for generation (default: 12)")
    parser.add_argument("--run", type=int, default=None,
                        help="Use specific run number (for incremental runs)")
    parser.add_argument("--no-cleanup", action="store_true",
                        help="Keep Alloy build artifacts (removed by default)")
    args = parser.parse_args()

    # Find ASN
    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"  No ASN found for {args.asn} in vault/1-reasoning-docs/",
              file=sys.stderr)
        sys.exit(1)

    # Load extract
    asn_num = int(re.search(r'\d+', asn_label).group())
    extract_path = formal_stmts(asn_num)
    extract = read_file(extract_path)
    if not extract:
        print(f"  No extract found at {extract_path.relative_to(WORKSPACE)}",
              file=sys.stderr)
        print(f"  Run: python scripts/normalize.py {args.asn}",
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

    if args.run is not None:
        run_num = args.run
        out_dir = ALLOY_DIR / asn_label / f"modeling-{run_num}"
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"  [RUN] Using modeling-{run_num}", file=sys.stderr)
    elif args.recheck:
        # Find the latest modeling directory
        existing = sorted(
            (ALLOY_DIR / asn_label).glob("modeling-*"),
            key=lambda p: int(re.search(r"modeling-(\d+)", p.name).group(1))
                if re.search(r"modeling-(\d+)", p.name) else 0
        )
        if not existing:
            print("  No existing modeling directory to recheck", file=sys.stderr)
            sys.exit(1)
        out_dir = existing[-1]
        m = re.search(r"modeling-(\d+)", out_dir.name)
        run_num = int(m.group(1)) if m else 1
        print(f"  [RECHECK] Using {out_dir.name}", file=sys.stderr)
    else:
        run_num = next_run_number(asn_label)
        out_dir = ALLOY_DIR / asn_label / f"modeling-{run_num}"
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"  {asn_label} — {len(properties)} properties, "
          f"definitions {len(definitions)}B", file=sys.stderr)

    # Generate + self-check all .als files (agent writes, runs Alloy, fixes)
    results = []
    for prop in properties:
        result = make_result(prop, out_dir)
        generate_one(result, prop, definitions, asn_label, args,
                      syntax_ref=syntax_ref)
        if not args.no_cleanup:
            cleanup_property_artifacts(result["als_path"])
        results.append(result)

    # Summary
    any_counterexample = any(r["status"] == "counterexample"
                             for r in results)

    if len(results) > 1 or args.dry_run:
        print_summary(asn_label, results)

    # Phase 3: Generate review + commit
    if not args.skip_check and not args.dry_run:
        if args.no_revise:
            print("  Note: --no-revise is deprecated; Alloy now always stops after review.",
                  file=sys.stderr)

        review_path = generate_review(asn_label, results, properties,
                                       run_num=run_num,
                                       asn_path=asn_path)
        if review_path:
            print(f"\n  [REVIEW] {review_path.relative_to(WORKSPACE)}",
                  file=sys.stderr)
            step_commit(f"alloy(asn): {asn_label} — Alloy check + review")
            if any_counterexample:
                print(f"  REVISE items found. Run: python scripts/revise.py {args.asn}",
                      file=sys.stderr)
        else:
            print(f"\n  [REVIEW] All checks passed — no review generated",
                  file=sys.stderr)
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
