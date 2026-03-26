"""
Per-proof verification — verify each property's proof individually.

Processes properties in dependency order. For each property, builds a
minimal context (property section + dependency sections) and calls opus
to verify the proof. Findings go to open-issues and review files.

Usage (standalone):
    python scripts/lib/verify_proofs.py 34
    python scripts/lib/verify_proofs.py 34 --label TA3
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
from paths import (WORKSPACE, USAGE_LOG, REVIEWS_DIR, ASNS_DIR,
                   formal_stmts, open_issues_path, load_manifest,
                   next_review_number)
from lib.common import find_asn, extract_property_sections
from lib.rebase_deps import (find_property_table, parse_table_row,
                              detect_columns, generate_deps)
from lib.rebase_asn import _append_open_issues

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "discovery"
VERIFY_TEMPLATE = PROMPTS_DIR / "verify-proof.md"


def _invoke_opus(prompt, effort="high"):
    """Call claude --print with opus."""
    cmd = [
        "claude", "--print",
        "--model", "claude-opus-4-6",
        "--tools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [VERIFY] FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        return "", elapsed

    return result.stdout.strip(), elapsed


def _log_usage(step, elapsed, asn_num, label=""):
    """Append usage entry."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": f"verify-proof-{step}",
            "asn": f"ASN-{asn_num:04d}",
            "elapsed_s": round(elapsed, 1),
        }
        if label:
            entry["label"] = label
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def build_proof_context(asn_num, label, deps_data, sections,
                        foundation_cache=None):
    """Build verification context for a single property.

    Returns (property_section, dependency_text) where dependency_text
    contains all sections referenced by follows_from.
    """
    prop_data = deps_data.get("properties", {}).get(label, {})
    follows_from = prop_data.get("follows_from", [])
    follows_from_asns = prop_data.get("follows_from_asns", [])

    property_section = sections.get(label, "")
    if not property_section:
        return "", ""

    # Collect dependency sections
    dep_parts = []

    # Internal dependencies (same ASN)
    all_labels = set(deps_data.get("properties", {}).keys())
    for dep_label in follows_from:
        if dep_label in all_labels and dep_label in sections:
            dep_parts.append(f"### {dep_label}\n\n{sections[dep_label]}")

    # Foundation dependencies (other ASNs)
    if foundation_cache is None:
        foundation_cache = {}
    depends = deps_data.get("depends", [])
    for dep_asn in depends:
        if dep_asn not in foundation_cache:
            stmt_path = formal_stmts(dep_asn)
            if stmt_path.exists():
                foundation_cache[dep_asn] = stmt_path.read_text()
            else:
                foundation_cache[dep_asn] = ""

    # Extract referenced foundation labels
    for dep_label in follows_from:
        if dep_label not in all_labels:
            # Look in foundation statements
            for dep_asn in depends:
                ftext = foundation_cache.get(dep_asn, "")
                # Find the section for this label
                pattern = re.compile(
                    r'^## ' + re.escape(dep_label) + r'\s*—.*?\n'
                    r'(.*?)(?=^## |\Z)',
                    re.MULTILINE | re.DOTALL
                )
                m = pattern.search(ftext)
                if m:
                    dep_parts.append(
                        f"### {dep_label} (ASN-{dep_asn:04d})\n\n"
                        f"## {dep_label} — ...\n{m.group(1).strip()}"
                    )
                    break

    dependency_text = "\n\n".join(dep_parts) if dep_parts else "(none)"
    return property_section, dependency_text


def _topological_sort_labels(deps_data):
    """Sort property labels in dependency order (foundations first)."""
    props = deps_data.get("properties", {})
    all_labels = set(props.keys())

    graph = {}
    for label, prop in props.items():
        graph[label] = set(prop.get("follows_from", [])) & all_labels

    result = []
    visited = set()
    visiting = set()

    def visit(node):
        if node in visited:
            return
        if node in visiting:
            return  # cycle — skip, don't block
        visiting.add(node)
        for dep in graph.get(node, set()):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
        result.append(node)

    for label in sorted(graph.keys()):
        visit(label)

    return result


def _read_verification_log(asn_num):
    """Read verified labels from open-issues log.

    Returns set of labels that have been verified (and not subsequently
    found to have issues without resolution).
    """
    path = open_issues_path(asn_num)
    if not path.exists():
        return set()

    text = path.read_text()
    verified = set()
    found_unresolved = set()

    for line in text.split("\n"):
        m = re.match(r'###\s*\[REVIEW-\d+\]\s*\[VERIFIED\]\s*(\S+)', line)
        if m:
            verified.add(m.group(1))
        m = re.match(r'###\s*\[REVIEW-\d+\]\s*\[FOUND\]\s*(\S+)', line)
        if m:
            found_unresolved.add(m.group(1))
        m = re.match(r'###\s*\[REVIEW-\d+\]\s*\[RESOLVED\]\s*(\S+)', line)
        if m:
            found_unresolved.discard(m.group(1))

    # Only count as verified if not currently unresolved
    return verified - found_unresolved


def verify_proof(asn_num, label, deps_data, sections, review_num,
                 foundation_cache=None):
    """Verify a single property's proof.

    Returns: "verified", "found", or "error"
    """
    asn_label = f"ASN-{asn_num:04d}"

    property_section, dependency_text = build_proof_context(
        asn_num, label, deps_data, sections, foundation_cache)

    if not property_section:
        print(f"  [VERIFY] {label}: no section found — skipping",
              file=sys.stderr)
        return "error"

    # Build prompt
    template = VERIFY_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{property_section}}", property_section)
              .replace("{{dependency_sections}}", dependency_text))

    print(f"  [VERIFY] {label} ({len(prompt) // 1024}KB)...",
          file=sys.stderr, end="", flush=True)

    text, elapsed = _invoke_opus(prompt)
    _log_usage("verify", elapsed, asn_num, label=label)

    if not text:
        print(f" error ({elapsed:.0f}s)", file=sys.stderr)
        return "error"

    if "RESULT: VERIFIED" in text:
        print(f" verified ({elapsed:.0f}s)", file=sys.stderr)
        # Log to open-issues
        _append_open_issues(
            asn_num,
            f"### [REVIEW-{review_num}] [VERIFIED] {label}\n"
        )
        return "verified"

    # FOUND — extract the finding
    print(f" FOUND ({elapsed:.0f}s)", file=sys.stderr)

    # Write to open-issues
    _append_open_issues(
        asn_num,
        f"### [REVIEW-{review_num}] [FOUND] {label}\n{text}\n"
    )

    # Write review file
    review_dir = REVIEWS_DIR / asn_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(
        f"# Proof Verification: {label}\n\n{text}\n"
    )
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}",
          file=sys.stderr)

    return "found"


def step_verify_proofs(asn_num, max_revise_cycles=10):
    """Verify all proofs in dependency order.

    For each property: verify, if issues found → revise → re-verify.
    Returns (verified_count, found_count, error_count).
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return 0, 0, 0

    # Generate fresh deps
    deps_data = generate_deps(asn_num)
    if deps_data is None:
        return 0, 0, 0

    # Get all sections (full text)
    text = asn_path.read_text()
    labels = list(deps_data.get("properties", {}).keys())
    sections = extract_property_sections(text, known_labels=labels,
                                          truncate=False)

    # Sort in dependency order
    ordered = _topological_sort_labels(deps_data)

    # Check what's already verified
    already_verified = _read_verification_log(asn_num)

    # Foundation cache for cross-ASN lookups
    foundation_cache = {}

    review_num = next_review_number(asn_label)
    verified = 0
    found = 0
    errors = 0

    print(f"\n  [VERIFY] {asn_label}: {len(ordered)} properties "
          f"({len(already_verified)} already verified)",
          file=sys.stderr)

    for label in ordered:
        if label in already_verified:
            verified += 1
            continue

        result = verify_proof(asn_num, label, deps_data, sections,
                              review_num, foundation_cache)

        if result == "verified":
            verified += 1
        elif result == "found":
            found += 1
            review_num = next_review_number(asn_label)

            # Scoped revise cycle
            for revise_cycle in range(max_revise_cycles):
                print(f"  [REVISE] Fixing {label} "
                      f"(cycle {revise_cycle + 1})...",
                      file=sys.stderr)

                # Run scoped revise
                revise_cmd = [
                    "claude", "-p",
                    "--model", "claude-opus-4-6",
                    "--output-format", "json",
                    "--allowedTools", "Edit,Read,Glob,Grep",
                ]

                revise_prompt = (
                    f"Fix the proof of {label} in the ASN at "
                    f"{asn_path.relative_to(WORKSPACE)}.\n\n"
                    f"The issue found during verification:\n\n"
                    f"{open_issues_path(asn_num).read_text().split(f'[FOUND] {label}')[-1].split('###')[0].strip()}\n\n"
                    f"Fix only this proof. Do not change anything else."
                )

                env = os.environ.copy()
                env.pop("CLAUDECODE", None)
                env["CLAUDE_CODE_EFFORT_LEVEL"] = "max"

                revise_result = subprocess.run(
                    revise_cmd, input=revise_prompt,
                    capture_output=True, text=True, env=env,
                    cwd=str(WORKSPACE),
                )

                if revise_result.returncode != 0:
                    print(f"  [REVISE] Failed", file=sys.stderr)
                    errors += 1
                    break

                # Commit the fix
                from lib.common import step_commit_asn
                step_commit_asn(asn_num,
                                f"fix(asn): {asn_label} — {label} proof fix")

                # Re-read ASN and sections (changed by revise)
                text = asn_path.read_text()
                sections = extract_property_sections(
                    text, known_labels=labels, truncate=False)

                # Regenerate deps (Status column may have changed)
                deps_data = generate_deps(asn_num)

                # Re-verify
                review_num = next_review_number(asn_label)
                re_result = verify_proof(
                    asn_num, label, deps_data, sections,
                    review_num, foundation_cache)

                if re_result == "verified":
                    # Append resolved
                    _append_open_issues(
                        asn_num,
                        f"### [REVIEW-{review_num}] [RESOLVED] {label}\n"
                    )
                    verified += 1
                    found -= 1  # no longer unresolved
                    review_num = next_review_number(asn_label)
                    break
                elif re_result == "found":
                    # Still has issues — loop
                    review_num = next_review_number(asn_label)
                    continue
                else:
                    errors += 1
                    break
            else:
                print(f"  [VERIFY] {label} did not converge after "
                      f"{max_revise_cycles} cycles", file=sys.stderr)
        else:
            errors += 1

    print(f"\n  [VERIFY] Done: {verified} verified, {found} open, "
          f"{errors} errors", file=sys.stderr)
    return verified, found, errors


def main():
    parser = argparse.ArgumentParser(
        description="Per-proof verification — verify each property individually")
    parser.add_argument("asn", help="ASN number (e.g., 34)")
    parser.add_argument("--label", help="Verify a single label only")
    args = parser.parse_args()

    asn_num = int(re.sub(r"[^0-9]", "", args.asn))

    if args.label:
        deps_data = generate_deps(asn_num)
        asn_path, asn_label = find_asn(str(asn_num))
        text = asn_path.read_text()
        labels = list(deps_data.get("properties", {}).keys())
        sections = extract_property_sections(text, known_labels=labels,
                                              truncate=False)
        review_num = next_review_number(asn_label)
        result = verify_proof(asn_num, args.label, deps_data, sections,
                              review_num)
        print(f"\n  Result: {result}")
        sys.exit(0 if result == "verified" else 1)

    v, f, e = step_verify_proofs(asn_num)
    sys.exit(0 if f == 0 and e == 0 else 1)


if __name__ == "__main__":
    main()
