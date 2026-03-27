#!/usr/bin/env python3
"""
Dependency audit — find property labels used in ASNs that come from
undeclared foundation ASNs.

Two passes:
  1. Deterministic label scan — finds transitive deps and uncertain cases
  2. LLM classification (sonnet) — resolves uncertain as MISSING/COLLISION/LOCAL/CLEAN

Produces an action report: dependencies to add, label collisions to resolve.
Results stored in vault/dependency-audit/<timestamp>/

Usage:
    python scripts/dependency-audit.py              # all active ASNs
    python scripts/dependency-audit.py 47 51 79     # specific ASNs
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import WORKSPACE, ASNS_DIR, PROJECT_MODEL_DIR, load_manifest, formal_stmts
from lib.shared.common import find_asn

PROMPT_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "discovery" / "dependency-audit.md"
AUDIT_DIR = WORKSPACE / "vault" / "dependency-audit"


def build_label_map():
    """Scan all exports and build maps of labels.

    Returns:
        label_map: label → first source ASN (for dependency checking)
        label_sources: label → set of all ASNs that define it (for collision detection)
    """
    label_map = {}       # label -> first asn_num
    label_sources = {}   # label -> set of asn_nums

    active_asns = set()
    for path in PROJECT_MODEL_DIR.glob("ASN-*/project.yaml"):
        m_num = re.match(r"ASN-(\d+)", path.parent.name)
        if m_num:
            active_asns.add(int(m_num.group(1)))

    prop_pattern = re.compile(r'^[A-Z]{1,3}[0-9]+[a-z]?[★\']*(?:-\w+)?$')

    for export_path in sorted(PROJECT_MODEL_DIR.glob("ASN-*/formal-statements.md")):
        m = re.match(r"ASN-(\d+)", export_path.parent.name)
        if not m:
            continue
        asn_num = int(m.group(1))
        if asn_num not in active_asns:
            continue

        text = export_path.read_text()

        for match in re.finditer(r'^## (\S+) — ', text, re.MULTILINE):
            label = match.group(1)
            if prop_pattern.match(label):
                if label not in label_map:
                    label_map[label] = asn_num
                label_sources.setdefault(label, set()).add(asn_num)

        for match in re.finditer(r'^## Definition — \w+ \((\S+?)[\),]', text, re.MULTILINE):
            label = match.group(1)
            if prop_pattern.match(label):
                if label not in label_map:
                    label_map[label] = asn_num
                label_sources.setdefault(label, set()).add(asn_num)

    return label_map, label_sources


def scan_reasoning_doc(asn_path, label_map):
    """Scan a reasoning doc for label references."""
    text = asn_path.read_text()
    found = {}

    for label, source_asn in label_map.items():
        pattern = r'(?<![A-Za-z])' + re.escape(label) + r'(?![A-Za-z0-9_])'
        if re.search(pattern, text):
            found[label] = source_asn

    return found


def get_active_asns():
    """Get active ASN numbers from project model yamls."""
    active = []
    for path in PROJECT_MODEL_DIR.glob("ASN-*/project.yaml"):
        m = re.match(r"ASN-(\d+)", path.parent.name)
        if m:
            active.append(int(m.group(1)))
    return sorted(active)


def get_dep_chain(asn_num):
    """Get the full transitive dependency chain for an ASN."""
    visited = set()

    def walk(num):
        if num in visited:
            return
        visited.add(num)
        m = load_manifest(num)
        if m:
            for dep in m.get("depends", []):
                walk(dep)

    m = load_manifest(asn_num)
    if m:
        for dep in m.get("depends", []):
            walk(dep)

    return visited


def check_asn(asn_num, label_map):
    """Check one ASN for missing dependencies.

    Returns (transitive, uncertain) where:
      transitive — list of {source, labels} that are re-exports through
                   the declared dep chain. Always MISSING by policy.
      uncertain — list of {source, labels} that need LLM to classify.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return None, None

    manifest = load_manifest(asn_num)
    if not manifest:
        return None, None

    declared_deps = set(manifest.get("depends", []))
    dep_chain = get_dep_chain(asn_num)
    used_labels = scan_reasoning_doc(asn_path, label_map)

    transitive = {}  # source_asn -> [labels]
    uncertain = {}   # source_asn -> [labels]

    for label, source_asn in used_labels.items():
        if source_asn == asn_num:
            continue
        if source_asn in declared_deps:
            continue
        # Source is undeclared — is it in the transitive chain?
        if source_asn in dep_chain:
            transitive.setdefault(source_asn, []).append(label)
        else:
            uncertain.setdefault(source_asn, []).append(label)

    t_list = [{"source": s, "labels": sorted(ls)}
              for s, ls in sorted(transitive.items())]
    u_list = [{"source": s, "labels": sorted(ls)}
              for s, ls in sorted(uncertain.items())]

    return t_list, u_list


def format_findings(findings):
    """Format findings as text for display and LLM prompt."""
    lines = []
    for f in findings:
        src = f"ASN-{f['source']:04d}"
        labels = ", ".join(f["labels"])
        lines.append(f"- FLAGGED {src}: uses [{labels}]")
    return "\n".join(lines)


def load_declared_exports(depends):
    """Load exports for all declared dependencies."""
    parts = []
    for dep in sorted(depends):
        dep_label = f"ASN-{dep:04d}"
        export_path = formal_stmts(dep)
        if export_path.exists():
            parts.append(f"### {dep_label}\n\n{export_path.read_text()}")
    return "\n\n---\n\n".join(parts) if parts else "(no exports found)"


def verify_with_llm(asn_num, findings):
    """Run sonnet to classify flagged findings."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return None

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    template = PROMPT_TEMPLATE.read_text()
    findings_text = format_findings(findings)
    declared_exports = load_declared_exports(depends)

    prompt = (template
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str)
              .replace("{{asn_content}}", asn_path.read_text())
              .replace("{{declared_exports}}", declared_exports)
              .replace("{{findings}}", findings_text))

    print(f"    [LLM] Classifying {asn_label}...", end="", flush=True)

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--max-turns", "1",
        "--allowedTools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f" FAILED ({elapsed:.0f}s)")
        return None

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
    except (json.JSONDecodeError, KeyError):
        print(f" parse error ({elapsed:.0f}s)")
        return None

    print(f" done ({elapsed:.0f}s)")
    return text


def generate_action_report(transitive_summary, llm_results, clean_list, ts):
    """Use sonnet to produce a clean action report from all findings."""
    parts = [f"# Dependency Audit Results — {ts}\n"]

    if transitive_summary:
        parts.append("## Deterministic Findings (transitive dependencies)\n")
        parts.append("\n".join(transitive_summary))

    if llm_results:
        parts.append("\n\n## LLM Per-ASN Classifications\n")
        for num in sorted(llm_results.keys()):
            parts.append(f"\n### ASN-{num:04d}\n")
            parts.append(llm_results[num])

    if clean_list:
        parts.append(f"\n\n## Clean ASNs\n\n{', '.join(clean_list)}")

    all_findings = "\n".join(parts)

    prompt = f"""Read the following dependency audit findings and produce a single
action report with four sections. Base the report ONLY on the findings below —
do not infer or add anything.

{all_findings}

Produce a markdown report with these sections:

## Dependencies to Add
List each ASN that needs a new dependency added, what to add, and why.
Include both transitive (deterministic) and LLM-confirmed MISSING findings.
Do NOT include COLLISION or LOCAL — those are not missing dependencies.

## Label Collisions (consider rename)
List labels where different properties share the same name across different ASNs.
Only include LLM-confirmed COLLISION cases. Say which ASNs define the label and
which ASNs are affected.

## Label Overlaps (informational)
List labels where an ASN defines a property locally that shares a name with a
property in another ASN's export. Only include LLM-confirmed LOCAL cases.
Low severity — no action required.

## Clean
List ASNs with no issues.

If a section has no entries, write "(none)".
"""

    cmd = [
        "claude", "-p",
        "--model", "claude-sonnet-4-6",
        "--output-format", "json",
        "--max-turns", "1",
        "--allowedTools", "",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [ACTION REPORT] Failed ({elapsed:.0f}s)", file=sys.stderr)
        return None

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
    except (json.JSONDecodeError, KeyError):
        print(f"  [ACTION REPORT] Parse error ({elapsed:.0f}s)", file=sys.stderr)
        return None

    print(f"  [ACTION REPORT] Generated ({elapsed:.0f}s)", file=sys.stderr)
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Dependency audit — label scan + LLM classification")
    parser.add_argument("asns", nargs="*", type=int,
                        help="ASN numbers to check (default: all active)")
    args = parser.parse_args()

    asn_nums = args.asns if args.asns else get_active_asns()

    # Create output directory
    ts = time.strftime("%Y-%m-%d-%H%M")
    out_dir = AUDIT_DIR / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    label_map, label_sources = build_label_map()
    print(f"\n  Label map: {len(label_map)} labels from "
          f"{len(set(label_map.values()))} exports\n")

    # Detect label collisions across exports
    collisions = {}  # label -> set of ASN nums
    for label, sources in label_sources.items():
        if len(sources) > 1:
            collisions[label] = sources

    clean_count = 0
    transitive_count = 0
    uncertain_count = 0
    clean_list = []
    all_flagged = []      # (asn_num, transitive, scan_lines)
    all_uncertain = []    # (asn_num, findings, scan_lines) for LLM pass

    # Track which ASNs are affected by each collision
    collision_affected = {}  # (label, frozenset(sources)) -> set of affected ASN nums

    for num in asn_nums:
        asn_path, asn_label = find_asn(str(num))
        if asn_path is None:
            continue

        transitive, uncertain = check_asn(num, label_map)
        if transitive is None:
            continue

        # Track collision exposure
        for f in (uncertain or []):
            for label in f["labels"]:
                if label in collisions:
                    key = (label, frozenset(collisions[label]))
                    collision_affected.setdefault(key, set()).add(num)

        if not transitive and not uncertain:
            clean_count += 1
            clean_list.append(f"ASN-{num:04d}")
            continue

        manifest = load_manifest(num)
        declared = manifest.get("depends", [])

        scan_lines = [f"# Dependency Audit — {asn_label}\n",
                      f"Declared depends: [{', '.join(str(d) for d in declared)}]\n"]

        has_output = False

        if transitive:
            transitive_count += 1
            has_output = True
            print(f"  {asn_label}:")
            print(f"    declared deps: [{', '.join(str(d) for d in declared)}]")
            scan_lines.append("\n## Transitive (MISSING — add dependency)\n")
            for f in transitive:
                src = f"ASN-{f['source']:04d}"
                labels = ", ".join(f["labels"])
                print(f"    MISSING {src}: uses [{labels}] (transitive)")
                scan_lines.append(f"- MISSING {src}: uses [{labels}]")

        if uncertain:
            uncertain_count += 1
            has_output = True
            if not transitive:
                print(f"  {asn_label}:")
                print(f"    declared deps: [{', '.join(str(d) for d in declared)}]")
            scan_lines.append("\n## Uncertain (needs LLM verification)\n")
            for f in uncertain:
                src = f"ASN-{f['source']:04d}"
                labels = ", ".join(f["labels"])
                print(f"    UNCERTAIN {src}: uses [{labels}]")
                scan_lines.append(f"- UNCERTAIN {src}: uses [{labels}]")

            all_uncertain.append((num, uncertain, scan_lines))

        if has_output:
            all_flagged.append((num, transitive, scan_lines))
            print()

    if clean_list:
        print(f"  Clean: {', '.join(clean_list)}")
    print(f"\n  Summary: {clean_count} clean, {transitive_count} missing (transitive), "
          f"{uncertain_count} uncertain\n")

    # LLM verification pass on uncertain
    llm_results = {}  # asn_num -> result text

    if all_uncertain:
        print(f"  === LLM Verification ({len(all_uncertain)} ASNs) ===\n")
        for num, findings, scan_lines in all_uncertain:
            label = f"ASN-{num:04d}"
            result = verify_with_llm(num, findings)
            if result:
                print(f"\n  {label}:\n")
                print(result)
                print()
                scan_lines.append(f"\n## LLM Verification\n\n{result}")
                llm_results[num] = result

    # Write per-ASN reports
    for num, _, scan_lines in all_flagged:
        label = f"ASN-{num:04d}"
        report_path = out_dir / f"{label}.md"
        report_path.write_text("\n".join(scan_lines) + "\n")

    # Build transitive summary for the action report prompt
    transitive_summary = []
    for num, transitive, _ in all_flagged:
        for f in (transitive or []):
            src = f"ASN-{f['source']:04d}"
            labels = ", ".join(f["labels"])
            transitive_summary.append(
                f"ASN-{num:04d}: MISSING {src} (uses {labels}) — transitive dependency")

    # Generate action report via LLM
    print(f"\n  === Generating Action Report ===\n")
    action_report = generate_action_report(
        transitive_summary, llm_results, clean_list, ts)

    if action_report:
        print(action_report)
        action_path = out_dir / "action-report.md"
        action_path.write_text(action_report + "\n")

    print(f"\n  Results: {out_dir.relative_to(WORKSPACE)}\n")


if __name__ == "__main__":
    main()
