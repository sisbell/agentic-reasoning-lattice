"""
Dafny translate step — prompt building + single-claim translation.

Step functions for the dafny orchestrator (scripts/dafny.py):
- build_claim_list_from_asn: parse ASN table into claim rows
- build_claim_prompt: assemble prompt for one claim
- translate_one: launch Claude agent to write + verify one .dfy file
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import (WORKSPACE, FORMALIZATION_DIR, PROOFS_DIR, USAGE_LOG,
                    LATTICE_PROMPTS, load_manifest)
from lib.shared.common import find_asn, assemble_readonly, build_label_index, load_claim_metadata
from lib.verification.dafny.common import read_file

PROMPTS_DIR = LATTICE_PROMPTS / "verification" / "dafny"
TEMPLATE = PROMPTS_DIR / "translate-claim.md"
DAFNY_REFERENCE = PROMPTS_DIR / "dafny-reference.dfy"


def build_claim_list_from_asn(asn_num):
    """Build claim list from per-claim files in lattices/xanadu/formalization/.

    Reads per-claim YAML for metadata, .md files for contract type detection.

    Returns list of row dicts with keys: label, proof_label, type, construct, notes.
    """
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        return []

    claim_dir = FORMALIZATION_DIR / asn_label
    if not claim_dir.exists():
        return []

    # Read metadata from per-claim YAMLs
    metadata = load_claim_metadata(claim_dir)
    if not metadata:
        return []

    # Read per-claim .md files for contract type detection
    _label_index = build_label_index(claim_dir)
    _filename_to_label = {f"{stem}.md": lbl for lbl, stem in _label_index.items()}
    claim_contents = {}
    for f in claim_dir.glob("*.md"):
        if not f.name.startswith("_"):
            claim_contents[_filename_to_label.get(f.name, f.stem)] = f.read_text()

    rows = []
    for label, data in metadata.items():
        status = data.get("type", "").lower()

        # proof_label from YAML name, or extract from header, or sanitize label
        proof_label = data.get("name", "")
        if not proof_label:
            content = claim_contents.get(label, "")
            m = re.search(r'^\*\*\S+\s*\(([A-Z][a-zA-Z0-9]+)\)', content, re.MULTILINE)
            if m:
                proof_label = m.group(1)
        if not proof_label and re.match(r'^[A-Z][a-z].*[A-Z]', label):
            proof_label = label
        if not proof_label:
            proof_label = re.sub(r'[^a-zA-Z0-9]', '', label)

        # Derive Dafny type from YAML type + formal contract in .md
        content = claim_contents.get(label, "")
        has_pre = bool(re.search(r'\*\s*Preconditions?\s*:\s*\*', content))
        has_post = bool(re.search(r'\*\s*Postconditions?\s*:\s*\*', content))
        has_inv = bool(re.search(r'\*\s*Invariants?\s*:\s*\*', content))
        has_def = bool(re.search(r'\*\s*Definition\s*:\s*\*', content))
        has_axiom = bool(re.search(r'\*\s*Axioms?\s*:\s*\*', content))

        if status in ("axiom", "design-requirement"):
            type_tag = "AXIOM"
            construct = "axiom"
        elif has_def:
            type_tag = "DEF"
            construct = "function"
        elif has_inv:
            type_tag = "INV"
            construct = "predicate"
        elif has_pre and has_post:
            type_tag = "LEMMA"
            construct = "lemma"
        elif has_axiom:
            type_tag = "AXIOM"
            construct = "axiom"
        else:
            type_tag = "LEMMA"
            construct = "lemma"

        rows.append({
            "label": label,
            "proof_label": proof_label,
            "type": type_tag,
            "construct": construct,
            "notes": status,
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


def build_claim_prompt(template, row, extract, dep_context=""):
    """Assemble prompt for a single claim."""
    prompt = template

    # Format claim row as markdown table
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
        .replace("{{index_row}}", index_table)
        .replace("{{extract_entry}}", extract)
        .replace("{{dep_context}}", dep_context)
    )


def translate_one(prompt, out_path, model="sonnet", effort="max", max_turns=12):
    """Launch a Claude agent with tools to write + verify the .dfy file."""
    model_flag = {
        "opus": "claude-opus-4-7",
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
   with its body, plus any accompanying lemmas the claim requires
   (e.g., a "strict total order" claim needs irreflexivity,
   transitivity, trichotomy, and asymmetry lemmas). Start every lemma
   body empty `{{ }}`. Write to disk, then run `dafny verify {out_path}`.

2. If ALL declarations verify, you are done.

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

5. If a different approach is needed, try a helper lemma, restructured
   cases, or a different decomposition. Do not pile on assertions.

Do NOT weaken `ensures` clauses, strengthen `requires` clauses, or
add `assume` statements. The formal contract is authoritative.
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
