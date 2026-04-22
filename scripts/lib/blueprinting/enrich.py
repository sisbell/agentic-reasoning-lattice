"""Enrich claim YAMLs — add type, dependencies, vocabulary.

Blueprinting step: reads the section YAML files from decompose, runs
three focused LLM passes per claim (type, deps, vocab) in parallel.
Updates the YAML files in place.

Usage (standalone):
    python scripts/lib/blueprinting/enrich.py 36
"""

import argparse
import re
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import BLUEPRINTS_DIR, DOMAIN_PROMPTS, prompt_path
from lib.shared.common import find_asn, invoke_claude, parallel_llm_calls, dump_yaml, step_commit_asn


PROMPTS_DIR = DOMAIN_PROMPTS / "blueprinting"


def _load_claims(sections_dir):
    """Load all claims from section YAML files. Returns [(yaml_path, index, prop), ...]."""
    claims = []
    for yaml_path in sorted(sections_dir.glob("*.yaml")):
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        if not data or not data.get("claims"):
            continue
        for i, prop in enumerate(data["claims"]):
            claims.append((yaml_path, i, prop))
    return claims


def _fill_prompt(template_path, prop):
    """Fill a prompt template with claim fields."""
    prompt = template_path.read_text()
    prompt = prompt.replace("{{label}}", str(prop.get("label", "")))
    prompt = prompt.replace("{{name}}", str(prop.get("name", "")))
    prompt = prompt.replace("{{body}}", str(prop.get("body", "")))
    return prompt


def _call_llm(prompt):
    """Call LLM and parse YAML response. Returns dict or None."""
    result, elapsed = invoke_claude(prompt, model="sonnet", effort="high")
    if not result:
        return None

    text = result.strip()
    if text.startswith("```"):
        first_nl = text.index("\n")
        text = text[first_nl + 1:]
    if text.endswith("```"):
        text = text[:-3].rstrip()

    try:
        return yaml.safe_load(text)
    except yaml.YAMLError:
        return None


def _enrich_one(prop, pass_name, template_path):
    """Run a single enrichment pass on a claim."""
    prompt = _fill_prompt(template_path, prop)
    return _call_llm(prompt)


def _run_pass(pass_name, template_path, claims, fields):
    """Run one enrichment pass across all claims in parallel."""
    print(f"\n  Pass: {pass_name} ({len(claims)} claims)...", file=sys.stderr)

    def worker(item):
        yaml_path, index, prop = item
        label = str(prop.get("label", "?"))
        result = _enrich_one(prop, pass_name, template_path)
        return label, (yaml_path, index, result)

    start = time.time()
    results = parallel_llm_calls(claims, worker, max_workers=5)
    elapsed = time.time() - start

    # Collect updates per file
    updates = {}  # yaml_path → {index: result_dict}
    ok = 0
    fail = 0
    for label, (yaml_path, index, result) in results:
        if result:
            if yaml_path not in updates:
                updates[yaml_path] = {}
            updates[yaml_path][index] = result
            ok += 1
        else:
            fail += 1
            print(f"    {label}  FAILED", file=sys.stderr)

    # Apply updates
    for yaml_path, file_updates in updates.items():
        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        for index, result in file_updates.items():
            prop = data["claims"][index]
            for field in fields:
                if field in result:
                    prop[field] = result[field]

        dump_yaml(data, yaml_path)

    print(f"    {pass_name}: {ok} ok, {fail} failed, {elapsed:.0f}s", file=sys.stderr)
    return ok, fail


def enrich_asn(asn_num):
    """Enrich claim YAMLs with type, dependencies, vocabulary (3 passes)."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    sections_dir = BLUEPRINTS_DIR / asn_label / "sections"
    if not sections_dir.exists():
        print(f"  No sections directory — run decompose first", file=sys.stderr)
        return False

    claims = _load_claims(sections_dir)
    print(f"\n  [ENRICH] {asn_label}", file=sys.stderr)
    print(f"  {len(claims)} claims to enrich", file=sys.stderr)

    if not claims:
        print(f"  Nothing to enrich", file=sys.stderr)
        return True

    passes = [
        ("type",  prompt_path("blueprinting/enrich-type.md"),  ["type"]),
        ("deps",  PROMPTS_DIR / "enrich-deps.md",  ["depends", "literature_citations"]),
        ("vocab", PROMPTS_DIR / "enrich-vocab.md",  ["vocabulary"]),
    ]

    total_ok = 0
    total_fail = 0
    start = time.time()

    for pass_name, template_path, fields in passes:
        # Reload claims each pass (files updated by previous pass)
        claims = _load_claims(sections_dir)
        ok, fail = _run_pass(pass_name, template_path, claims, fields)
        total_ok += ok
        total_fail += fail

    elapsed = time.time() - start
    print(f"\n  [ENRICH] 3 passes, {total_ok} total enrichments, {total_fail} failures, {elapsed:.0f}s",
          file=sys.stderr)

    step_commit_asn(asn_num, hint="enrich")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Enrich claim YAMLs with type, dependencies, vocabulary")
    parser.add_argument("asn", help="ASN number (e.g., 36)")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = enrich_asn(asn_num)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
