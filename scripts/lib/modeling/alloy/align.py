"""Contract alignment — align Alloy model with formal contract."""

import os
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import WORKSPACE

from .common import invoke_claude, read_file, ALLOY_JAR_DEFAULT
from .check import check, classify_alloy_error
from .validate import validate

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "modeling" / "alloy"
ALIGN_TEMPLATE = PROMPTS_DIR / "align-with-contract.md"


def align(als_path, errors, formal_contract, syntax_ref="",
          model="opus", effort="high", max_turns=12):
    """Run align-with-contract agent on an Alloy model."""
    alloy_jar = os.environ.get("ALLOY_JAR", ALLOY_JAR_DEFAULT)
    alloy_code = read_file(als_path)
    template = read_file(ALIGN_TEMPLATE)

    prompt = (template
        .replace("{{als_path}}", str(als_path))
        .replace("{{alloy_code}}", alloy_code)
        .replace("{{errors}}", errors)
        .replace("{{formal_contract}}", formal_contract or "(not available)")
        .replace("{{syntax_reference}}", syntax_ref)
        .replace("{{als_dir}}", str(als_path.parent))
        .replace("{{alloy_jar}}", alloy_jar)
        .replace("{{als_name}}", als_path.name))

    success, elapsed, cost = invoke_claude(
        prompt, als_path, model=model, effort=effort,
        max_turns=max_turns)

    return success, elapsed, cost


def align_validate_cycle(als_path, formal_contract, label,
                          syntax_ref="", model="opus", effort="high",
                          max_cycles=3):
    """Validate contract, then align -> check -> validate cycle if FLAG.

    Returns (contract_result, reason, total_cost).
    """
    alloy_source = als_path.read_text()
    rec, reason, _ = validate(alloy_source, formal_contract, label)
    contract_result = rec.upper()
    total_cost = 0
    print(f" {contract_result}", file=sys.stderr,
          end="" if rec == "flag" else "\n", flush=True)

    for cycle in range(1, max_cycles + 1):
        if rec != "flag":
            break

        print(f"\n    [{label}] align cycle {cycle}...",
              file=sys.stderr, end="", flush=True)
        flag_errors = f"Contract validation failed:\n{reason}"
        ok, a_elapsed, a_cost = align(
            als_path, flag_errors, formal_contract,
            syntax_ref=syntax_ref, model=model, effort=effort)
        total_cost += a_cost

        # Re-check with Alloy
        alloy_output, _ = check(als_path)
        if alloy_output is None:
            print(f" (no alloy)", file=sys.stderr)
            contract_result = "ERROR"
            break

        # Check for syntax/type errors — feed back to align
        status, summary = classify_alloy_error(alloy_output)
        if status == "syntax-error":
            print(f" SYNTAX ERROR", file=sys.stderr, end="", flush=True)
            reason = alloy_output
            rec = "flag"
            contract_result = "SYNTAX_ERROR"
            continue

        # Re-validate contract
        alloy_source = als_path.read_text()
        rec, reason, _ = validate(alloy_source, formal_contract, label)
        contract_result = rec.upper()
        print(f" {contract_result}", file=sys.stderr,
              end="" if rec == "flag" else "\n", flush=True)

    return contract_result, reason, total_cost
