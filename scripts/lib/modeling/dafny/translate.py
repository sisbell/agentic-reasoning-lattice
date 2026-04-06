"""
Dafny translate step — prompt building + single-property translation.

Step functions for the dafny orchestrator (scripts/dafny.py):
- build_property_list_from_asn: parse ASN table into property rows
- read_proof_modules: load .dfy proof module sources
- build_property_prompt: assemble prompt for one property
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
from lib.shared.paths import (WORKSPACE, PROOFS_DIR, USAGE_LOG,
                    load_manifest, formal_stmts)
from lib.modeling.dafny.common import read_file

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "modeling" / "dafny"
TEMPLATE = PROMPTS_DIR / "translate-property.md"
DAFNY_REFERENCE = PROMPTS_DIR / "dafny-reference.dfy"


def build_property_list_from_asn(asn_num):
    """Build property list from ASN table + formal contracts.

    Reads the property table for labels/status, and formal-statements.md
    for contract types.

    Returns list of row dicts with keys: label, proof_label, type, construct, notes.
    """
    from lib.shared.common import find_asn, extract_property_sections
    from lib.formalization.core.build_dependency_graph import (find_property_table, parse_table_row,
                                              detect_columns)

    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return []

    text = asn_path.read_text()
    table_rows = find_property_table(text)
    if table_rows is None:
        return []

    header = parse_table_row(table_rows[0])
    cols = detect_columns(header)
    has_name = "name" in cols
    has_type = "type" in cols
    data_rows = table_rows[2:]

    # Load formal-statements for contract scanning and name extraction
    stmts_path = formal_stmts(int(re.sub(r"[^0-9]", "", str(asn_num))))
    stmts_text = read_file(stmts_path) if stmts_path else ""

    # Get labels and table names for section extraction
    labels = []
    table_names = {}  # label -> PascalCase name from Name column
    for row in data_rows:
        cells = parse_table_row(row)
        if cells and cells[0].strip():
            label = cells[0].strip().strip("`*")
            labels.append(label)
            if has_name and len(cells) > cols["name"]:
                name_val = cells[cols["name"]].strip()
                if name_val:
                    table_names[label] = name_val

    # Extract PascalCase names from formal-statements headers (fallback)
    # Format: ## LABEL — PascalCaseName or ## LABEL — PascalCaseName (TYPE, construct)
    stmts_names = {}
    for line in stmts_text.split("\n"):
        m = re.match(r'^##\s+(.+?)\s+\u2014\s+([A-Z][a-zA-Z0-9]+)', line)
        if m:
            name = m.group(2)
            if re.match(r'^[A-Z][a-z]+[A-Z]', name):
                stmts_names[m.group(1)] = name

    # Extract sections from formal-statements for contract scanning
    stmts_sections = {}
    if stmts_text:
        stmts_sections = extract_property_sections(
            stmts_text, known_labels=labels, truncate=False)

    rows = []
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue
        label = cells[0].strip().strip("`*")
        if not label:
            continue

        status = cells[-1].strip().lower()
        # Statement: everything between fixed columns and status
        fixed_cols = {0}
        if has_name:
            fixed_cols.add(cols["name"])
        if has_type:
            fixed_cols.add(cols["type"])
        stmt_start = max(fixed_cols) + 1
        statement = "|".join(cells[stmt_start:-1]).strip() if len(cells) > stmt_start + 1 else ""

        # Extract proof_label (PascalCase name)
        # Prefer: Name column > formal-statements header > PascalCase label > sanitized label
        proof_label = table_names.get(label, "")
        if not proof_label:
            proof_label = stmts_names.get(label, "")
        if not proof_label and re.match(r'^[A-Z][a-z].*[A-Z]', label):
            proof_label = label
        if not proof_label:
            proof_label = re.sub(r'[^a-zA-Z0-9]', '', label)

        # Derive type from status + formal contract
        section = stmts_sections.get(label, "")
        has_pre = bool(re.search(r'\*\s*Preconditions?\s*:\s*\*', section))
        has_post = bool(re.search(r'\*\s*Postconditions?\s*:\s*\*', section))
        has_inv = bool(re.search(r'\*\s*Invariants?\s*:\s*\*', section))
        has_def = bool(re.search(r'\*\s*Definition\s*:\s*\*', section))
        has_axiom = bool(re.search(r'\*\s*Axioms?\s*:\s*\*', section))

        if status in ("axiom", "design requirement"):
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
            "notes": cells[-1].strip(),  # raw Status text
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
    """Read .dfy files for listed proof modules.

    Module names map to files: TumblerAlgebra -> TumblerAlgebra.dfy,
    TumblerOrder -> TumblerOrder.dfy, etc. All files live under
    vault/5-proofs/TumblerAlgebra/ (the shared directory).

    Returns a dict of {relative_path: source} and a formatted text block
    for prompt injection. Paths are relative to WORKSPACE.
    """
    modules = {}
    seen = set()
    for mod_name in module_names:
        # Try as a directory first (backward compat)
        mod_dir = PROOFS_DIR / mod_name
        if mod_dir.is_dir():
            for dfy_file in sorted(mod_dir.glob("*.dfy")):
                content = read_file(dfy_file)
                if content.strip() and dfy_file not in seen:
                    seen.add(dfy_file)
                    rel_path = str(dfy_file.relative_to(WORKSPACE))
                    modules[rel_path] = content
        else:
            # Try as a .dfy file under any proofs subdirectory
            found = False
            for dfy_file in PROOFS_DIR.rglob(f"{mod_name}.dfy"):
                found = True
                content = read_file(dfy_file)
                if content.strip() and dfy_file not in seen:
                    seen.add(dfy_file)
                    rel_path = str(dfy_file.relative_to(WORKSPACE))
                    modules[rel_path] = content
            if not found:
                print(f"  Warning: proof module not found: {mod_name}",
                      file=sys.stderr)

    # Format as prompt text — show path so LLM can compute includes
    parts = []
    for rel_path, source in modules.items():
        parts.append(f"### `{rel_path}`\n\n```dafny\n{source}\n```")

    return modules, "\n\n".join(parts)


def build_property_prompt(template, imports_map, proof_modules_text,
                          row, extract, dep_context=""):
    """Assemble prompt for a single property."""
    prompt = template

    # Format property row as markdown table
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
        .replace("{{dep_context}}", dep_context)
    )


def translate_one(prompt, out_path, model="sonnet", effort="max", max_turns=12):
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
