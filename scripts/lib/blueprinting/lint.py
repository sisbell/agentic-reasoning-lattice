"""
Blueprinting lint — status classification and dependency checks.

Two subcommands:
  status — verify property Status column is correct (per-ASN, opus)
  deps   — find undeclared foundation dependencies (global, sonnet)

Usage:
    python scripts/lint.py status 34
    python scripts/lint.py status 34 --dry-run
    python scripts/lint.py deps
    python scripts/lint.py deps 34 36 40
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, USAGE_LOG, PROJECT_MODEL_DIR,
    load_manifest, formal_stmts,
    blueprint_properties_dir, blueprint_lint_dir, blueprint_global_lint_dir,
    lint_path, lint_global_path,
)
from lib.shared.common import find_asn, extract_property_sections
from lib.formalization.core.build_dependency_graph import (
    find_property_table, parse_table_row, detect_columns,
)

PROMPTS_DIR = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "lint"
STATUS_TEMPLATE = PROMPTS_DIR / "status.md"
DEPS_TEMPLATE = PROMPTS_DIR / "deps.md"


# ---------------------------------------------------------------------------
# Status lint (from audit/classify.py)
# ---------------------------------------------------------------------------

def _classify_one(label, status, section):
    """Classify a single property. Returns (recommendation, reason, elapsed)."""
    template = STATUS_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{status}}", status)
              .replace("{{section}}", section))

    cmd = [
        "claude", "--print", "--model", "claude-opus-4-6",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        return "error", f"opus failed ({elapsed:.0f}s)", elapsed

    # Parse response — expect "RECOMMENDATION | REASON"
    line = result.stdout.strip()
    line = re.sub(r'^```\s*', '', line)
    line = re.sub(r'\s*```$', '', line)
    line = line.strip()

    if "|" in line:
        parts = line.split("|", 1)
        rec = parts[0].strip().lower()
        reason = parts[1].strip()
    else:
        rec = line.strip().lower()
        reason = ""

    return rec, reason, elapsed


def lint_status(asn_num, dry_run=False):
    """Run status lint on an ASN. Returns output path or None."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    text = asn_path.read_text()
    rows = find_property_table(text)
    if rows is None:
        print(f"  No property table in {asn_path.name}", file=sys.stderr)
        return None

    header = parse_table_row(rows[0])
    cols = detect_columns(header)
    data_rows = rows[2:]

    # Collect labels and statuses
    properties = []
    labels = []
    for row in data_rows:
        cells = parse_table_row(row)
        if len(cells) < 2:
            continue
        label = cells[0].strip().strip("`*")
        if not label:
            continue
        status = cells[-1].strip()
        labels.append(label)
        properties.append({"label": label, "status": status})

    sections = extract_property_sections(text, known_labels=labels,
                                          truncate=False)

    print(f"  [LINT-STATUS] {asn_label}: {len(properties)} properties",
          file=sys.stderr)

    if dry_run:
        for prop in properties:
            section = sections.get(prop["label"], "")
            print(f"  {prop['label']:30s} status={prop['status']:30s} "
                  f"section={len(section)}B", file=sys.stderr)
        return None

    # Set up output file
    out_path = lint_path(asn_label, "status")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w") as f:
        f.write(f"# Status Lint — {asn_label}\n\n")
        f.write(f"*Audited: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write("| Label | Current Status | Recommendation | Reason |\n")
        f.write("|-------|---------------|----------------|--------|\n")

    total_elapsed = 0
    changes = 0

    for i, prop in enumerate(properties, 1):
        label = prop["label"]
        status = prop["status"]
        section = sections.get(label, "(no section found)")

        print(f"  [{i}/{len(properties)}] {label}...",
              end="", file=sys.stderr, flush=True)

        rec, reason, elapsed = _classify_one(label, status, section)
        total_elapsed += elapsed

        marker = ""
        if rec not in ("ok", "error"):
            if rec != status.lower():
                marker = " **"
                changes += 1

        row = f"| {label} | {status} | {rec}{marker} | {reason} |"
        print(f" → {rec} ({elapsed:.0f}s)", file=sys.stderr)

        with open(out_path, "a") as f:
            f.write(row + "\n")

    with open(out_path, "a") as f:
        f.write(f"\n*{len(properties)} properties audited in "
                f"{total_elapsed:.0f}s. {changes} recommended changes.*\n")

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "lint-status",
            "asn": asn_label,
            "elapsed_s": round(total_elapsed, 1),
            "properties": len(properties),
            "changes": changes,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    print(f"\n  [LINT-STATUS] Report: {out_path.relative_to(WORKSPACE)}",
          file=sys.stderr)
    print(f"  [LINT-STATUS] {changes} recommended changes out of "
          f"{len(properties)} properties", file=sys.stderr)

    return str(out_path)


# ---------------------------------------------------------------------------
# Deps lint (from audit/dependency.py)
# ---------------------------------------------------------------------------

def _build_label_map():
    """Scan all exports and build maps of labels.

    Returns:
        label_map: label → first source ASN (for dependency checking)
        label_sources: label → set of all ASNs that define it (for collision detection)
    """
    label_map = {}
    label_sources = {}

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


def _scan_reasoning_doc(asn_path, label_map):
    """Scan a reasoning doc for label references."""
    text = asn_path.read_text()
    found = {}
    for label, source_asn in label_map.items():
        pattern = r'(?<![A-Za-z])' + re.escape(label) + r'(?![A-Za-z0-9_])'
        if re.search(pattern, text):
            found[label] = source_asn
    return found


def _get_active_asns():
    """Get active ASN numbers from project model yamls."""
    active = []
    for path in PROJECT_MODEL_DIR.glob("ASN-*/project.yaml"):
        m = re.match(r"ASN-(\d+)", path.parent.name)
        if m:
            active.append(int(m.group(1)))
    return sorted(active)


def _get_dep_chain(asn_num):
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


def _check_asn(asn_num, label_map):
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
    dep_chain = _get_dep_chain(asn_num)
    used_labels = _scan_reasoning_doc(asn_path, label_map)

    transitive = {}
    uncertain = {}

    for label, source_asn in used_labels.items():
        if source_asn == asn_num:
            continue
        if source_asn in declared_deps:
            continue
        if source_asn in dep_chain:
            transitive.setdefault(source_asn, []).append(label)
        else:
            uncertain.setdefault(source_asn, []).append(label)

    t_list = [{"source": s, "labels": sorted(ls)}
              for s, ls in sorted(transitive.items())]
    u_list = [{"source": s, "labels": sorted(ls)}
              for s, ls in sorted(uncertain.items())]

    return t_list, u_list


def _format_findings(findings):
    """Format findings as text for display and LLM prompt."""
    lines = []
    for f in findings:
        src = f"ASN-{f['source']:04d}"
        labels = ", ".join(f["labels"])
        lines.append(f"- FLAGGED {src}: uses [{labels}]")
    return "\n".join(lines)


def _load_declared_exports(depends):
    """Load exports for all declared dependencies."""
    parts = []
    for dep in sorted(depends):
        dep_label = f"ASN-{dep:04d}"
        export_path = formal_stmts(dep)
        if export_path.exists():
            parts.append(f"### {dep_label}\n\n{export_path.read_text()}")
    return "\n\n---\n\n".join(parts) if parts else "(no exports found)"


def _verify_with_llm(asn_num, findings):
    """Run sonnet to classify flagged findings."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return None

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)

    template = DEPS_TEMPLATE.read_text()
    findings_text = _format_findings(findings)
    declared_exports = _load_declared_exports(depends)

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


def _generate_action_report(transitive_summary, llm_results, clean_list, ts):
    """Use sonnet to produce a clean action report from all findings."""
    parts = [f"# Dependency Lint Results — {ts}\n"]

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


def lint_deps(asn_nums=None):
    """Run dependency lint across ASNs. Returns output directory path."""
    if not asn_nums:
        asn_nums = _get_active_asns()

    label_map, label_sources = _build_label_map()
    print(f"\n  Label map: {len(label_map)} labels from "
          f"{len(set(label_map.values()))} exports\n")

    clean_count = 0
    clean_list = []
    all_flagged = []
    all_uncertain = []

    for num in asn_nums:
        asn_path, asn_label = find_asn(str(num))
        if asn_path is None:
            continue

        transitive, uncertain = _check_asn(num, label_map)
        if transitive is None:
            continue

        if not transitive and not uncertain:
            clean_count += 1
            clean_list.append(f"ASN-{num:04d}")
            continue

        manifest = load_manifest(num)
        declared = manifest.get("depends", [])

        scan_lines = [f"# Dependency Lint — {asn_label}\n",
                      f"Declared depends: [{', '.join(str(d) for d in declared)}]\n"]

        has_output = False

        if transitive:
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
    print(f"\n  Summary: {clean_count} clean, "
          f"{len([f for f in all_flagged if f[1]])} missing (transitive), "
          f"{len(all_uncertain)} uncertain\n")

    # LLM verification pass on uncertain
    llm_results = {}

    if all_uncertain:
        print(f"  === LLM Verification ({len(all_uncertain)} ASNs) ===\n")
        for num, findings, scan_lines in all_uncertain:
            label = f"ASN-{num:04d}"
            result = _verify_with_llm(num, findings)
            if result:
                print(f"\n  {label}:\n")
                print(result)
                print()
                scan_lines.append(f"\n## LLM Verification\n\n{result}")
                llm_results[num] = result

    # Write per-ASN reports
    for num, _, scan_lines in all_flagged:
        asn_label = f"ASN-{num:04d}"
        report_path = lint_path(asn_label, "deps")
        report_path.parent.mkdir(parents=True, exist_ok=True)
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
    ts = time.strftime("%Y-%m-%d %H:%M")
    action_report = _generate_action_report(
        transitive_summary, llm_results, clean_list, ts)

    if action_report:
        print(action_report)
        action_path = lint_global_path("deps-global")
        action_path.parent.mkdir(parents=True, exist_ok=True)
        action_path.write_text(action_report + "\n")
        print(f"\n  Action report: {action_path.relative_to(WORKSPACE)}\n")

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "lint-deps",
            "asns": len(asn_nums),
            "flagged": len(all_flagged),
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Inline lint (scan for embedded results in per-property files)
# ---------------------------------------------------------------------------

SCAN_TEMPLATE = WORKSPACE / "scripts" / "prompts" / "blueprinting" / "promote-inline" / "scan.md"

# Minimum file size to consider for inline scan
_INLINE_MIN_SIZE = 500


def _extract_post_contract(content):
    """Extract content after the formal contract in a property file."""
    marker = "*Formal Contract:*"
    idx = content.find(marker)
    if idx == -1:
        return None

    after_marker = content[idx:]
    lines = after_marker.split("\n")
    contract_lines = []
    post_lines = []
    in_contract = True

    for i, line in enumerate(lines):
        if i == 0:
            contract_lines.append(line)
            continue
        if in_contract:
            stripped = line.strip()
            if stripped.startswith("- *") or stripped.startswith("*") or not stripped:
                contract_lines.append(line)
            else:
                in_contract = False
                post_lines.append(line)
        else:
            post_lines.append(line)

    post_content = "\n".join(post_lines).strip()
    return post_content if post_content else None


def _scan_property_file(label, content):
    """Scan a property file for inline results. Returns list of findings."""
    template = SCAN_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{content}}", content))

    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        return [], elapsed

    text = result.stdout.strip()
    if not text or "(none)" in text:
        return [], elapsed

    findings = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            findings.append({
                "kind": parts[0],
                "label": parts[1],
                "name": parts[2],
                "description": parts[3],
            })

    return findings, elapsed


def lint_inline(asn_num, dry_run=False):
    """Scan per-property blueprint files for embedded results."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    prop_dir = blueprint_properties_dir(asn_label)
    if not prop_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        return None

    # Collect property files (skip _*.md structural files)
    prop_files = sorted(
        f for f in prop_dir.glob("*.md")
        if not f.name.startswith("_")
    )

    print(f"  [LINT-INLINE] {asn_label}: {len(prop_files)} property files",
          file=sys.stderr)

    # Mechanical pre-filter: check for post-contract content
    candidates = []
    for f in prop_files:
        content = f.read_text()
        if len(content) < _INLINE_MIN_SIZE:
            continue
        post = _extract_post_contract(content)
        if post:
            label = f.name.replace(".md", "")
            candidates.append((label, f, content, len(post)))

    print(f"  [LINT-INLINE] {len(candidates)} files with post-contract content",
          file=sys.stderr)

    if dry_run:
        for label, f, content, post_size in candidates:
            print(f"    {label:30s} {len(content):6d}B  post-contract: {post_size}B",
                  file=sys.stderr)
        return None

    # Scan candidates with sonnet
    all_findings = []
    total_elapsed = 0

    for label, f, content, _ in candidates:
        print(f"    {label}...", end="", file=sys.stderr, flush=True)
        findings, elapsed = _scan_property_file(label, content)
        total_elapsed += elapsed

        derived = [fd for fd in findings if fd["kind"] == "derived"]
        commentary = [fd for fd in findings if fd["kind"] == "commentary"]

        if derived:
            print(f" {len(derived)} derived, {len(commentary)} commentary ({elapsed:.0f}s)",
                  file=sys.stderr)
            all_findings.append((label, findings))
        else:
            print(f" clean ({elapsed:.0f}s)", file=sys.stderr)

    # Write report
    out_path = lint_path(asn_label, "inline")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w") as rf:
        rf.write(f"# Inline Lint — {asn_label}\n\n")
        rf.write(f"*Scanned: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")

        if not all_findings:
            rf.write("No embedded results found.\n")
        else:
            for label, findings in all_findings:
                rf.write(f"## {label}\n\n")
                for fd in findings:
                    rf.write(f"- **{fd['kind']}** | {fd['label']} | "
                             f"{fd['name']} | {fd['description']}\n")
                rf.write("\n")

        rf.write(f"\n*{len(candidates)} files scanned in {total_elapsed:.0f}s. "
                 f"{len(all_findings)} with embedded results.*\n")

    print(f"\n  [LINT-INLINE] Report: {out_path.relative_to(WORKSPACE)}",
          file=sys.stderr)
    print(f"  [LINT-INLINE] {len(all_findings)} properties with embedded results",
          file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "lint-inline",
            "asn": asn_label,
            "elapsed_s": round(total_elapsed, 1),
            "candidates": len(candidates),
            "with_findings": len(all_findings),
        }
        with open(USAGE_LOG, "a") as wf:
            wf.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return str(out_path)


# ---------------------------------------------------------------------------
# Unformalized lint (LLM scan of monolithic ASN for undeclared properties)
# ---------------------------------------------------------------------------

UNFORMALIZED_TEMPLATE = PROMPTS_DIR / "unformalized.md"


def lint_unformalized(asn_num):
    """Scan monolithic ASN for properties that exist in prose but aren't declared.

    Uses sonnet to read the ASN and identify content that defines or asserts
    a property but lacks a bold header and/or table entry.
    Returns findings text (empty string if clean).
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    template = UNFORMALIZED_TEMPLATE.read_text()
    asn_content = asn_path.read_text()
    prompt = template.replace("{{asn_content}}", asn_content)

    print(f"\n  [LINT-UNFORMALIZED] Scanning {asn_label}...", file=sys.stderr)

    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [LINT-UNFORMALIZED] FAILED ({elapsed:.0f}s)", file=sys.stderr)
        return None

    text = result.stdout.strip()

    # Write report
    out_path = lint_path(asn_label, "unformalized")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"# Unformalized Properties — {asn_label}\n\n"
                        f"*Scanned: {time.strftime('%Y-%m-%d %H:%M')}*\n\n"
                        f"{text}\n")

    # Print to console
    is_clean = "RESULT: CLEAN" in text
    if is_clean:
        print(f"  [LINT-UNFORMALIZED] CLEAN ({elapsed:.0f}s)", file=sys.stderr)
    else:
        print(f"  [LINT-UNFORMALIZED] Findings ({elapsed:.0f}s):", file=sys.stderr)
        for line in text.strip().split("\n"):
            if line.strip():
                print(f"    {line.strip()}", file=sys.stderr)

    print(f"  Report: {out_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "lint-unformalized",
            "asn": asn_label,
            "elapsed_s": round(elapsed, 1),
            "clean": is_clean,
        }
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return "" if is_clean else text


# ---------------------------------------------------------------------------
# Missing dependency lint (per-property LLM check on blueprint files)
# ---------------------------------------------------------------------------

MISSING_TEMPLATE = PROMPTS_DIR / "missing.md"


def lint_missing(asn_num):
    """Check per-property blueprint files for references to undeclared labels.

    For each property file, sends content + declared labels to sonnet.
    Returns list of (label, missing_refs) tuples. Empty list if clean.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    prop_dir = blueprint_properties_dir(asn_label)
    if not prop_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        return None

    # Read declared labels from _table.md
    table_path = prop_dir / "_table.md"
    if not table_path.exists():
        print(f"  No _table.md in blueprint", file=sys.stderr)
        return None

    table_text = table_path.read_text()
    declared_labels = []
    for line in table_text.split("\n"):
        if line.strip().startswith("|") and not line.strip().startswith("| Label") and not line.strip().startswith("|---"):
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 2 and cells[1].strip():
                declared_labels.append(cells[1].strip().strip("`*"))

    declared_str = ", ".join(declared_labels)

    # Collect property files
    prop_files = sorted(
        f for f in prop_dir.glob("*.md")
        if not f.name.startswith("_")
    )

    template = MISSING_TEMPLATE.read_text()

    print(f"\n  [LINT-MISSING] {asn_label}: {len(prop_files)} property files, "
          f"{len(declared_labels)} declared labels", file=sys.stderr)

    all_missing = []
    total_elapsed = 0

    for f in prop_files:
        label = f.name.replace(".md", "")
        content = f.read_text()

        if len(content.strip()) < 100:
            continue

        prompt = (template
                  .replace("{{declared_labels}}", declared_str)
                  .replace("{{label}}", label)
                  .replace("{{content}}", content))

        print(f"    {label}...", end="", file=sys.stderr, flush=True)

        cmd = [
            "claude", "--print", "--model", "claude-sonnet-4-6",
        ]
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

        start = time.time()
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, env=env,
        )
        elapsed = time.time() - start
        total_elapsed += elapsed

        if result.returncode != 0:
            print(f" error ({elapsed:.0f}s)", file=sys.stderr)
            continue

        text = result.stdout.strip()

        if "RESULT: CLEAN" in text:
            print(f" clean ({elapsed:.0f}s)", file=sys.stderr)
        else:
            missing_refs = [line.strip() for line in text.split("\n")
                           if line.strip().startswith("MISSING:")]
            if missing_refs:
                print(f" {len(missing_refs)} missing ({elapsed:.0f}s)",
                      file=sys.stderr)
                all_missing.append((label, missing_refs))
            else:
                print(f" clean ({elapsed:.0f}s)", file=sys.stderr)

    # Write report
    out_path = lint_path(asn_label, "missing")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w") as rf:
        rf.write(f"# Missing Dependencies — {asn_label}\n\n")
        rf.write(f"*Scanned: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")

        if not all_missing:
            rf.write("No missing dependencies found.\n")
        else:
            # Collect unique missing labels across all files
            missing_labels = {}
            for label, refs in all_missing:
                for ref in refs:
                    rf.write(f"- **{label}**: {ref}\n")
            rf.write(f"\n*{len(prop_files)} files scanned in {total_elapsed:.0f}s.*\n")

    # Print summary
    if all_missing:
        # Deduplicate missing labels
        unique_missing = set()
        for _, refs in all_missing:
            for ref in refs:
                # Extract label from "MISSING: LABEL — context"
                parts = ref.replace("MISSING:", "").strip().split("—")
                if parts:
                    unique_missing.add(parts[0].strip())

        print(f"\n  [LINT-MISSING] {len(unique_missing)} undeclared label(s):",
              file=sys.stderr)
        for m in sorted(unique_missing):
            print(f"    {m}", file=sys.stderr)
    else:
        print(f"\n  [LINT-MISSING] CLEAN", file=sys.stderr)

    print(f"  Report: {out_path.relative_to(WORKSPACE)}", file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "lint-missing",
            "asn": asn_label,
            "elapsed_s": round(total_elapsed, 1),
            "files_scanned": len(prop_files),
            "missing_count": len(all_missing),
        }
        with open(USAGE_LOG, "a") as wf:
            wf.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return all_missing


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Blueprinting lint — status, dependency, and inline checks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status subcommand
    sp_status = subparsers.add_parser("status",
        help="Lint property Status column for one ASN")
    sp_status.add_argument("asn", help="ASN number (e.g., 34)")
    sp_status.add_argument("--dry-run", action="store_true",
        help="Show properties without invoking Claude")

    # deps subcommand
    sp_deps = subparsers.add_parser("deps",
        help="Lint dependency declarations across ASNs")
    sp_deps.add_argument("asns", nargs="*", type=int,
        help="ASN numbers to check (default: all active)")

    # inline subcommand
    sp_inline = subparsers.add_parser("inline",
        help="Scan blueprint files for embedded results to promote")
    sp_inline.add_argument("asn", help="ASN number (e.g., 34)")
    sp_inline.add_argument("--dry-run", action="store_true",
        help="Show candidates without invoking Claude")

    # unformalized subcommand
    sp_unformalized = subparsers.add_parser("unformalized",
        help="Scan monolithic ASN for undeclared properties (LLM)")
    sp_unformalized.add_argument("asn", help="ASN number (e.g., 34)")

    # missing subcommand
    sp_missing = subparsers.add_parser("missing",
        help="Check blueprint files for references to undeclared labels (LLM)")
    sp_missing.add_argument("asn", help="ASN number (e.g., 34)")

    args = parser.parse_args()

    if args.command == "status":
        asn_num = int(re.sub(r"[^0-9]", "", args.asn))
        lint_status(asn_num, dry_run=args.dry_run)
    elif args.command == "deps":
        lint_deps(asn_nums=args.asns if args.asns else None)
    elif args.command == "inline":
        asn_num = int(re.sub(r"[^0-9]", "", args.asn))
        lint_inline(asn_num, dry_run=args.dry_run)
    elif args.command == "unformalized":
        asn_num = int(re.sub(r"[^0-9]", "", args.asn))
        findings = lint_unformalized(asn_num)
        if findings:
            sys.exit(1)
    elif args.command == "missing":
        asn_num = int(re.sub(r"[^0-9]", "", args.asn))
        findings = lint_missing(asn_num)
        if findings:
            sys.exit(1)


if __name__ == "__main__":
    main()
