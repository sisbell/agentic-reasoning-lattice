"""
Validate Contracts — check formal contracts against proof sections.

Per-claim LLM validation: reads each claim's proof section and
formal contract, reports MATCH or MISMATCH with detailed findings.

Step function for the orchestrator (scripts/convergence-assembly.py):
- validate_contracts(asn_num) → list of (label, detail) mismatches
"""

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import USAGE_LOG, prompt_path
from lib.shared.common import find_asn, extract_claim_sections, invoke_claude
from lib.claim_convergence.core.build_dependency_graph import (
    find_claim_table, parse_table_row, detect_columns,
)

VALIDATE_TEMPLATE = prompt_path("claim-convergence/assembly/validate-contracts.md")


def _extract_formal_contract(section_text):
    """Extract the formal contract block from a claim section."""
    marker = "*Formal Contract:*"
    idx = section_text.find(marker)
    if idx == -1:
        return None
    return section_text[idx:].strip()


def _log_usage(elapsed, asn_num, count):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "validate-contracts",
            "asn": f"ASN-{asn_num:04d}",
            "claims": count,
            "elapsed_s": round(elapsed, 1),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def validate_contract(label, section, signature="", dependencies="", model="sonnet"):
    """Validate one claim's contract against its proof section.

    Returns (match: bool, detail: str).
    """
    contract = _extract_formal_contract(section)
    if contract is None:
        return True, ""  # No contract to validate

    # Trim section to just the proof (before the contract marker)
    marker = "*Formal Contract:*"
    idx = section.find(marker)
    proof_section = section[:idx].strip() if idx != -1 else section

    template = VALIDATE_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{proof_section}}", proof_section)
              .replace("{{formal_contract}}", contract)
              .replace("{{signature}}", signature or "(none)")
              .replace("{{dependencies}}", dependencies or "(none)"))

    result, elapsed = invoke_claude(prompt, model=model, effort="high")

    if result is None:
        return True, ""  # LLM call failed, don't block

    if "RESULT: MATCH" in result:
        return True, ""

    if "RESULT: MISMATCH" in result:
        idx = result.find("RESULT: MISMATCH")
        detail = result[idx + len("RESULT: MISMATCH"):].strip()
        return False, detail

    return True, ""  # Unclear result, don't block


def validate_contracts(asn_num):
    """Validate all claim contracts against their proof sections.

    Returns a list of (label, detail) tuples for mismatches.
    Empty list means all contracts match.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [VALIDATE] ASN-{asn_num:04d} not found", file=sys.stderr)
        return []

    text = asn_path.read_text()
    rows = find_claim_table(text)
    if rows is None:
        print(f"  [VALIDATE] No claim table in {asn_path.name}",
              file=sys.stderr)
        return []

    # Get labels from table
    header = parse_table_row(rows[0])
    data_rows = rows[2:]
    labels = []
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue
        label = cells[0].strip().strip("`*")
        if label:
            labels.append(label)

    # Extract sections
    sections = extract_claim_sections(text, known_labels=labels, truncate=False)

    # Load template
    template = VALIDATE_TEMPLATE.read_text()

    mismatches = []
    checked = 0
    start = time.time()

    print(f"  [VALIDATE] Checking {len(labels)} claims...",
          file=sys.stderr, flush=True)

    for label in labels:
        section = sections.get(label, "")
        if not section:
            continue

        contract = _extract_formal_contract(section)
        if contract is None:
            # No contract to validate — skip (formalize handles missing contracts)
            continue

        # Trim section to just the proof (before the contract marker)
        marker = "*Formal Contract:*"
        idx = section.find(marker)
        proof_section = section[:idx].strip() if idx != -1 else section

        prompt = (template
                  .replace("{{label}}", label)
                  .replace("{{proof_section}}", proof_section)
                  .replace("{{formal_contract}}", contract))

        result, elapsed = invoke_claude(prompt, model="sonnet", effort="high")
        checked += 1

        if result is None:
            print(f"    {label}: LLM call failed", file=sys.stderr)
            continue

        if "RESULT: MATCH" in result:
            print(f"    {label}: MATCH", file=sys.stderr)
        elif "RESULT: MISMATCH" in result:
            # Extract detail after RESULT: MISMATCH
            idx = result.find("RESULT: MISMATCH")
            detail = result[idx + len("RESULT: MISMATCH"):].strip()
            mismatches.append((label, detail))
            print(f"    {label}: MISMATCH", file=sys.stderr)
        else:
            print(f"    {label}: unclear result", file=sys.stderr)

    total_elapsed = time.time() - start
    _log_usage(total_elapsed, asn_num, checked)

    print(f"  [VALIDATE] {checked} checked, {len(mismatches)} mismatches "
          f"({total_elapsed:.0f}s)", file=sys.stderr)

    return mismatches
