"""
Alloy translate step — extract parsing, prompt building, single-claim generation.

Step functions for the alloy orchestrator (scripts/alloy.py):
- parse_extract: split formal-statements into definitions + claims
- build_claim_prompt: assemble prompt for one claim
- generate_one: launch Claude agent to write + self-check one .als file
"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE, prompt_path, formal_stmts
from lib.shared.common import find_asn
from lib.verification.alloy.check import check, classify_alloy_error, parse_alloy_results
from lib.verification.alloy.common import (read_file, invoke_claude, log_usage,
    ALLOY_JAR_DEFAULT)

CLAIM_TEMPLATE = prompt_path("verification/alloy/translate-claim.md")
SYNTAX_REF = prompt_path("verification/alloy/syntax-reference.md")


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
    """Parse an extract into definitions and claims.

    Returns dict with:
      definitions: str — all definition sections concatenated
      claims: list[dict] — each with label, name, type, construct, body
    """
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)

    definitions = []
    claims = []

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

        # Claim with type tag
        if m:
            claims.append({
                "label": m.group(1),
                "name": m.group(2),
                "type": m.group(3),
                "construct": m.group(4),
                "body": section,
            })
            continue

        # Claim without type tag
        m2 = _PROP_NO_TYPE_RE.match(first_line)
        if m2:
            claims.append({
                "label": m2.group(1),
                "name": m2.group(2),
                "type": "",
                "construct": "",
                "body": section,
            })

    return {
        "definitions": "\n\n".join(definitions),
        "claims": claims,
    }


def build_claim_prompt(definitions, prop, syntax_ref="", dep_context=""):
    """Assemble prompt for a single claim from per-claim template."""
    template = read_file(CLAIM_TEMPLATE)
    if not template:
        print(f"  Prompt template not found at {CLAIM_TEMPLATE.relative_to(WORKSPACE)}",
              file=sys.stderr)
        sys.exit(1)

    return template.replace(
        "{{syntax_reference}}", syntax_ref
    ).replace(
        "{{definitions}}", definitions
    ).replace(
        "{{dep_context}}", dep_context or "(none)"
    ).replace(
        "{{claim}}", prop["body"]
    )


def generate_one(result, prop, definitions, asn_label, args,
                  syntax_ref="", dep_context=""):
    """Generate and self-check the .als file for a single claim.

    The agent writes the model, runs Alloy, and fixes syntax errors
    autonomously.  The script then runs a final Alloy check to confirm
    and classify the result (pass / counterexample / syntax-error).

    Mutates result in place. Returns result.
    """
    als_path = result["als_path"]

    prompt = build_claim_prompt(definitions, prop, syntax_ref=syntax_ref,
                                   dep_context=dep_context)

    # Append agent self-check instructions
    alloy_jar = os.environ.get("ALLOY_JAR", ALLOY_JAR_DEFAULT)
    prompt += f"""

## Self-check instructions

After writing the Alloy model to `{als_path}`, verify it by running:

    cd {als_path.parent} && java -jar {alloy_jar} exec -f {als_path.name}

**If you see syntax or type errors**: fix the model and re-run the checker.
Repeat until the model is syntactically valid.

**If you see counterexamples** (SAT on a check command): this is a valid
result — it means the claim does not hold. Do NOT modify the model to
avoid counterexamples. Leave the model as-is and stop.

**If all checks show UNSAT**: the claim holds within scope. Stop.
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
            llm_elapsed = 0
            cost = 0.0
            success = False
            print(f"    [TIMEOUT] {model_used} timed out", file=sys.stderr)

            # Remove any partial file from timed-out agent
            if als_path.exists():
                als_path.unlink()

        result["llm_elapsed"] = llm_elapsed
        result["cost"] = cost
        result["model"] = model_used

        if not success or not als_path.exists():
            print(f"    No model generated", file=sys.stderr)
            result["status"] = "gen-fail"
            log_usage(asn_label, llm_elapsed, 0, False,
                      claim_label=prop["label"], cost=cost,
                      model=model_used)
            return result

        print(f"    [WROTE] {als_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Final Alloy check to confirm and classify
    if not args.skip_check:
        alloy_output, alloy_elapsed = check(als_path)
        result["alloy_elapsed"] = alloy_elapsed

        if alloy_output is None:
            result["status"] = "no-alloy"
            log_usage(asn_label, result["llm_elapsed"], 0, False,
                      claim_label=prop["label"], cost=result.get("cost", 0),
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
                  has_ce, claim_label=prop["label"],
                  cost=result.get("cost", 0),
                  model=result.get("model"))
    else:
        result["status"] = "generated"
        log_usage(asn_label, result["llm_elapsed"], 0, False,
                  claim_label=prop["label"], cost=result.get("cost", 0),
                  model=result.get("model"))

    return result
