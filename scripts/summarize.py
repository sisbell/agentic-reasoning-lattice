#!/usr/bin/env python3
"""
Summarize — generate summaries for claim YAMLs.

Reads each claim's .md body and formal contract, generates a 1-3
sentence summary via LLM, writes it to the summary field in the .yaml.

Summaries enable mechanical foundation export — no LLM-based assembly
needed between ASNs.

Usage:
    python scripts/summarize.py 34
    python scripts/summarize.py 34 --force
    python scripts/summarize.py 36 --dry-run
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, CLAIM_CONVERGENCE_DIR, CLAIM_DIR, prompt_path
from lib.shared.common import (
    find_asn, build_label_index, load_claim_metadata,
    dump_yaml, invoke_claude, step_commit_asn,
)

SUMMARIZE_TEMPLATE = prompt_path("claim-convergence/summarize.md")
BATCH_SIZE = 5


def _compute_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _load_cache(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_cache(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _extract_statement_and_contract(md_text):
    """Extract the header/statement and formal contract, skip the proof."""
    lines = md_text.strip().split("\n")

    # Header + first paragraph (the statement)
    statement_lines = []
    in_statement = True
    for line in lines:
        if in_statement:
            statement_lines.append(line)
            if line.strip() == "" and len(statement_lines) > 2:
                in_statement = False
        # Look for formal contract
        if line.strip().startswith("*Formal Contract:*"):
            # Grab from here to end
            idx = lines.index(line)
            contract = "\n".join(lines[idx:]).strip()
            break
    else:
        contract = ""

    statement = "\n".join(statement_lines).strip()
    return statement, contract


def _build_batch_text(batch, claim_dir, label_index, all_metadata):
    """Build the claims text for a batch of labels."""
    parts = []
    for label in batch:
        meta = all_metadata.get(label, {})
        stem = label_index.get(label, label)
        md_path = claim_dir / f"{stem}.md"

        if not md_path.exists():
            continue

        md_text = md_path.read_text()
        statement, contract = _extract_statement_and_contract(md_text)

        name = meta.get("name", label)
        prop_type = meta.get("type", "unknown")
        depends = meta.get("depends", [])
        deps_str = ", ".join(str(d) for d in depends) if depends else "(none)"

        part = f"### {label} ({name}) — {prop_type}\n"
        part += f"Depends: {deps_str}\n\n"
        part += statement + "\n"
        if contract:
            part += "\n" + contract
        parts.append(part)

    return "\n\n---\n\n".join(parts)


def _parse_summaries(response_text):
    """Parse LLM response into {label: summary} dict."""
    summaries = {}
    for line in response_text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        # Match "LABEL: summary" or "LABEL (Name): summary"
        match = re.match(r'^([A-Za-z0-9_\-().Σ₀]+)\s*(?:\([^)]*\))?\s*:\s*(.+)$', line)
        if match:
            summaries[match.group(1)] = match.group(2).strip()
    return summaries


def run_summarize(asn_num, force=False, dry_run=False):
    """Generate summaries for claims that need them."""
    _, asn_label = find_asn(str(asn_num))
    if asn_label is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return False

    claim_dir = CLAIM_DIR / asn_label
    cc_dir = CLAIM_CONVERGENCE_DIR / asn_label
    if not claim_dir.exists():
        print(f"  No claim doc directory for {asn_label}", file=sys.stderr)
        return False

    label_index = build_label_index(claim_dir)
    all_metadata = load_claim_metadata(claim_dir)
    cc_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cc_dir / "_summary-cache.json"
    cache = {} if force else _load_cache(cache_path)

    print(f"\n  [SUMMARIZE] {asn_label} — {len(all_metadata)} claims",
          file=sys.stderr)

    # Determine which claims need summarization
    needs_summary = []
    for label, meta in all_metadata.items():
        stem = label_index.get(label, label)
        md_path = claim_dir / f"{stem}.md"
        if not md_path.exists():
            continue

        md_hash = _compute_hash(md_path.read_text())
        has_summary = bool(meta.get("summary"))

        if has_summary and cache.get(label) == md_hash and not force:
            continue

        needs_summary.append((label, md_hash))

    if not needs_summary:
        print(f"  All {len(all_metadata)} claims have current summaries.",
              file=sys.stderr)
        return True

    print(f"  {len(needs_summary)} claims need summarization.",
          file=sys.stderr)

    if dry_run:
        for label, _ in needs_summary:
            print(f"    {label}", file=sys.stderr)
        return True

    # Batch and summarize
    template = SUMMARIZE_TEMPLATE.read_text()
    labels_only = [label for label, _ in needs_summary]
    hash_map = {label: h for label, h in needs_summary}
    total_summarized = 0
    start_time = time.time()

    for batch_start in range(0, len(labels_only), BATCH_SIZE):
        batch = labels_only[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(labels_only) + BATCH_SIZE - 1) // BATCH_SIZE

        batch_text = _build_batch_text(batch, claim_dir, label_index, all_metadata)
        prompt = template.replace("{{claims}}", batch_text)

        print(f"  [BATCH {batch_num}/{total_batches}] {', '.join(batch)}...",
              end="", file=sys.stderr, flush=True)

        response, elapsed = invoke_claude(prompt, model="sonnet", effort="high")

        if not response:
            print(f" failed ({elapsed:.0f}s)", file=sys.stderr)
            continue

        summaries = _parse_summaries(response)
        print(f" {len(summaries)} summaries ({elapsed:.0f}s)", file=sys.stderr)

        # Build name→label reverse map for fuzzy matching
        name_to_label = {}
        for l in batch:
            meta = all_metadata.get(l, {})
            name = meta.get("name", "")
            if name:
                name_to_label[name] = l

        # Write summaries to YAMLs
        for label in batch:
            summary = summaries.get(label)
            if not summary:
                # Try matching by name (LLM sometimes uses name instead of label)
                name = all_metadata.get(label, {}).get("name", "")
                summary = summaries.get(name)
            if not summary:
                print(f"    WARNING: no summary for {label}", file=sys.stderr)
                continue
            summaries[label] = summary  # normalize key for cache

            stem = label_index.get(label, label)
            yaml_path = claim_dir / f"{stem}.yaml"
            if not yaml_path.exists():
                continue

            # Read, update, write
            import yaml
            with open(yaml_path) as f:
                data = yaml.safe_load(f) or {}

            data["summary"] = summaries[label]
            dump_yaml(data, yaml_path)

            cache[label] = hash_map[label]
            total_summarized += 1

        _save_cache(cache_path, cache)

    elapsed = time.time() - start_time
    print(f"\n  [SUMMARIZE] {total_summarized} summaries written in {elapsed:.0f}s",
          file=sys.stderr)

    if total_summarized > 0:
        step_commit_asn(asn_num, hint="summarize")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Summarize — generate summaries for claim YAMLs")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--force", action="store_true",
                        help="Re-summarize all claims (ignore cache)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be summarized, don't run")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))
    ok = run_summarize(asn_num, force=args.force, dry_run=args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
