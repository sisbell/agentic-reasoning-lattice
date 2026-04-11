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
from lib.shared.common import find_asn, extract_property_sections, load_property_names, filename_to_label
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
        rec = parts[0].strip().strip("`*").lower()
        reason = parts[1].strip()
    else:
        rec = line.strip().strip("`*").lower()
        reason = ""

    return rec, reason, elapsed


def lint_status(asn_num, dry_run=False, formalization=False):
    """Run status lint on an ASN. Returns output path or None.

    formalization: if True, read from vault/3-formalization/ per-property files
    instead of the monolithic ASN.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    if formalization:
        from lib.shared.paths import FORMALIZATION_DIR
        prop_dir = FORMALIZATION_DIR / asn_label
        table_path = prop_dir / "_table.md"
        if not table_path.exists():
            print(f"  No _table.md in {prop_dir}", file=sys.stderr)
            return None
        table_text = table_path.read_text()
        rows = find_property_table(table_text)
        if rows is None:
            print(f"  No property table in _table.md", file=sys.stderr)
            return None
        # Read sections from per-property files (normalized lookup)
        from lib.shared.common import load_property_sections
        sections = load_property_sections(prop_dir)
    else:
        text = asn_path.read_text()
        rows = find_property_table(text)
        if rows is None:
            print(f"  No property table in {asn_path.name}", file=sys.stderr)
            return None
        sections = None  # built below after labels collected

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

    if not formalization:
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
    if formalization:
        from lib.shared.paths import FORMALIZATION_DIR
        out_path = FORMALIZATION_DIR / asn_label / "reviews" / "status-lint.md"
    else:
        out_path = lint_path(asn_label, "status")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w") as f:
        f.write(f"# Status Lint — {asn_label}\n\n")
        f.write(f"*Audited: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write("| Label | Current Status | Recommendation | Reason |\n")
        f.write("|-------|---------------|----------------|--------|\n")

    def _check_status(prop):
        label = prop["label"]
        status = prop["status"]
        # Normalize label for file lookup: T0(a) -> T0a, Def-Span -> Span
        norm = label.replace("(", "").replace(")", "")
        if norm.startswith("Def-"):
            norm = norm[4:]
        section = sections.get(label) or sections.get(norm) or "(no section found)"
        rec, reason, elapsed = _classify_one(label, status, section)
        return label, (status, rec, reason)

    from lib.shared.common import parallel_llm_calls
    results = parallel_llm_calls(properties, _check_status, max_workers=10)

    changes = 0
    rows = []
    for label, data in results:
        if data is None:
            continue
        status, rec, reason = data
        marker = ""
        if rec not in ("ok", "error"):
            if rec != status.lower():
                marker = " **"
                changes += 1
        rows.append(f"| {label} | {status} | {rec}{marker} | {reason} |")

    with open(out_path, "a") as f:
        for row in rows:
            f.write(row + "\n")
        f.write(f"\n*{len(properties)} properties audited. "
                f"{changes} recommended changes.*\n")

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "lint-status",
            "asn": asn_label,
            "elapsed_s": 0,
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

def build_label_map():
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


def scan_reasoning_doc(asn_path, label_map):
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
    dep_chain = get_dep_chain(asn_num)
    used_labels = scan_reasoning_doc(asn_path, label_map)

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

    label_map, label_sources = build_label_map()
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


def _scan_property_file(label, content, model="claude-sonnet-4-6"):
    """Scan a property file for inline results. Returns list of findings."""
    template = SCAN_TEMPLATE.read_text()
    prompt = (template
              .replace("{{label}}", label)
              .replace("{{content}}", content))

    cmd = [
        "claude", "--print", "--model", model,
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


def _parse_inline_report(report_path):
    """Parse an existing inline lint report into {label: [findings]}."""
    if not report_path.exists():
        return {}

    existing = {}
    current_label = None
    for line in report_path.read_text().split("\n"):
        m = re.match(r'^## (.+)', line)
        if m:
            current_label = m.group(1).strip()
            if current_label not in existing:
                existing[current_label] = []
            continue
        if current_label and line.strip().startswith("- **"):
            # Parse: - **kind** | label | name | description
            parts = line.strip().lstrip("- ").split("|")
            if len(parts) >= 4:
                kind_raw = parts[0].strip()
                kind = re.sub(r'\*\*', '', kind_raw).strip()
                existing[current_label].append({
                    "kind": kind,
                    "label": parts[1].strip(),
                    "name": parts[2].strip(),
                    "description": parts[3].strip(),
                })
    return existing


def _dedup_key(fd):
    """Dedup key for a finding. Uses (kind, label) for actionable findings,
    (kind, description) for commentary (which has no stable label)."""
    if fd["kind"] in ("derived", "definition") and fd["label"] and fd["label"] != "—":
        return (fd["kind"], fd["label"])
    return (fd["kind"], fd["name"])


def _merge_findings(existing, new_findings):
    """Merge new findings into existing, deduplicating by stable keys."""
    merged = {}
    # Start with existing
    for label, findings in existing.items():
        merged[label] = list(findings)

    new_count = 0
    for label, findings in new_findings:
        if label not in merged:
            merged[label] = []
        existing_keys = {_dedup_key(f) for f in merged[label]}
        for fd in findings:
            key = _dedup_key(fd)
            if key not in existing_keys:
                merged[label].append(fd)
                existing_keys.add(key)
                new_count += 1

    # Remove labels with no actionable findings
    merged = {label: findings for label, findings in merged.items()
              if any(f["kind"] in ("derived", "definition") for f in findings)}

    return merged, new_count


def lint_inline(asn_num, dry_run=False, model="claude-sonnet-4-6"):
    """Scan per-property blueprint files for embedded results.

    Merges new findings with any existing report — findings accumulate
    across runs rather than being overwritten.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    prop_dir = blueprint_properties_dir(asn_label)
    if not prop_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        return None
    _prop_names = load_property_names(prop_dir)

    # Collect all files — property files AND structural files
    # (except _table.md, _preamble.md, _vocabulary.md which are metadata)
    skip_structural = {"_table.md", "_preamble.md", "_vocabulary.md"}
    prop_files = sorted(
        f for f in prop_dir.glob("*.md")
        if f.name not in skip_structural
    )

    print(f"  [LINT-INLINE] {asn_label}: {len(prop_files)} files to scan",
          file=sys.stderr)

    candidates = []
    for f in prop_files:
        content = f.read_text()
        if not content.strip():
            continue
        label = filename_to_label(f.name, _prop_names)
        candidates.append((label, f, content))

    print(f"  [LINT-INLINE] {len(candidates)} files to scan",
          file=sys.stderr)

    if dry_run:
        for label, f, content in candidates:
            print(f"    {label:30s} {len(content):6d}B", file=sys.stderr)
        return None

    # Scan all candidates in parallel
    def _check_inline(item):
        label, f, content = item
        findings, elapsed = _scan_property_file(label, content, model=model)
        actionable = [fd for fd in findings if fd["kind"] in ("derived", "definition")]
        return label, findings if actionable else []

    from lib.shared.common import parallel_llm_calls
    results = parallel_llm_calls(candidates, _check_inline, max_workers=10)

    new_findings = [(label, findings) for label, findings in results if findings]

    # Merge with existing report
    out_path = lint_path(asn_label, "inline")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = _parse_inline_report(out_path)
    # Dedup existing report (may have accumulated duplicates from prior runs)
    for label in existing:
        seen = set()
        deduped = []
        for fd in existing[label]:
            key = _dedup_key(fd)
            if key not in seen:
                deduped.append(fd)
                seen.add(key)
        existing[label] = deduped
    merged, new_count = _merge_findings(existing, new_findings)

    # Write merged report
    with open(out_path, "w") as rf:
        rf.write(f"# Inline Lint — {asn_label}\n\n")
        rf.write(f"*Last scanned: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")

        if not merged:
            rf.write("No embedded results found.\n")
        else:
            for label in sorted(merged.keys()):
                findings = merged[label]
                rf.write(f"## {label}\n\n")
                for fd in findings:
                    rf.write(f"- **{fd['kind']}** | {fd['label']} | "
                             f"{fd['name']} | {fd['description']}\n")
                rf.write("\n")

        rf.write(f"\n*{len(candidates)} files scanned. "
                 f"{len(merged)} with embedded results.*\n")

    print(f"\n  [LINT-INLINE] Report: {out_path.relative_to(WORKSPACE)}",
          file=sys.stderr)
    print(f"  [LINT-INLINE] {len(merged)} properties with embedded results"
          f" ({new_count} new)", file=sys.stderr)

    # Log usage
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": "lint-inline",
            "asn": asn_label,
            "elapsed_s": 0,
            "candidates": len(candidates),
            "with_findings": len(merged),
            "new_findings": new_count,
        }
        with open(USAGE_LOG, "a") as wf:
            wf.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return new_count



# ---------------------------------------------------------------------------
# Missing dependency lint (per-property LLM check on blueprint files)
# ---------------------------------------------------------------------------

MISSING_TEMPLATE = PROMPTS_DIR / "missing.md"


def _parse_missing_report(report_path):
    """Parse existing missing lint report into {(source, missing_label): line}."""
    if not report_path.exists():
        return {}

    existing = {}
    for line in report_path.read_text().split("\n"):
        m = re.match(r'^- \*\*(\S+)\*\*:\s*(MISSING:\s*\S+.*)', line.strip())
        if m:
            source = m.group(1)
            ref_text = m.group(2).strip()
            # Extract missing label from "MISSING: LABEL — context"
            parts = ref_text.replace("MISSING:", "").strip().split("—")
            missing_label = parts[0].strip() if parts else ""
            key = (source, missing_label)
            if key not in existing:
                existing[key] = line.strip()
    return existing


def _labels_from_table(table_path):
    """Extract labels from a _table.md file."""
    labels = []
    for line in table_path.read_text().split("\n"):
        if (line.strip().startswith("|")
                and not line.strip().startswith("| Label")
                and not line.strip().startswith("|---")):
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 2 and cells[1].strip():
                labels.append(cells[1].strip().strip("`*"))
    return labels


def lint_missing(asn_num, model="claude-opus-4-6"):
    """Check per-property blueprint files for references to undeclared labels.

    Merges new findings with any existing report — findings accumulate
    across runs. For each property file, sends content + declared labels
    to LLM. Returns list of (label, missing_refs) tuples.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    prop_dir = blueprint_properties_dir(asn_label)
    if not prop_dir.exists():
        print(f"  No blueprint directory for {asn_label}", file=sys.stderr)
        return None
    _prop_names = load_property_names(prop_dir)

    # Read declared labels from _table.md
    table_path = prop_dir / "_table.md"
    if not table_path.exists():
        print(f"  No _table.md in blueprint", file=sys.stderr)
        return None

    declared_labels = _labels_from_table(table_path)

    # Include upstream ASN labels from dependencies
    from lib.shared.paths import PROJECT_MODEL_DIR, FORMALIZATION_DIR
    project_yaml = PROJECT_MODEL_DIR / asn_label / "project.yaml"
    if project_yaml.exists():
        for line in project_yaml.read_text().split("\n"):
            if line.startswith("depends:"):
                dep_nums = re.findall(r'\d+', line)
                for dep_num in dep_nums:
                    dep_label = f"ASN-{int(dep_num):04d}"
                    dep_table = FORMALIZATION_DIR / dep_label / "_table.md"
                    if dep_table.exists():
                        upstream = _labels_from_table(dep_table)
                        declared_labels.extend(upstream)
                        print(f"  [LINT-MISSING] +{len(upstream)} labels from {dep_label}",
                              file=sys.stderr)

    declared_str = ", ".join(declared_labels)

    # Collect property files
    prop_files = sorted(
        f for f in prop_dir.glob("*.md")
        if not f.name.startswith("_")
    )

    template = MISSING_TEMPLATE.read_text()

    print(f"\n  [LINT-MISSING] {asn_label}: {len(prop_files)} property files, "
          f"{len(declared_labels)} declared labels", file=sys.stderr)

    # Filter to files worth scanning
    candidates = []
    for f in prop_files:
        content = f.read_text()
        if len(content.strip()) >= 100:
            candidates.append(f)

    def _check_one(f):
        label = filename_to_label(f.name, _prop_names)
        content = f.read_text()
        prompt = (template
                  .replace("{{declared_labels}}", declared_str)
                  .replace("{{label}}", label)
                  .replace("{{content}}", content))

        cmd = ["claude", "--print", "--model", model]
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, env=env,
        )
        if result.returncode != 0:
            return label, None

        text = result.stdout.strip()
        if "RESULT: CLEAN" in text:
            return label, []

        missing_refs = [line.strip() for line in text.split("\n")
                       if line.strip().startswith("MISSING:")]
        return label, missing_refs

    from lib.shared.common import parallel_llm_calls
    results = parallel_llm_calls(candidates, _check_one, max_workers=10)

    all_missing = []
    for label, refs in results:
        if refs:
            all_missing.append((label, refs))

    # Merge with existing report
    out_path = lint_path(asn_label, "missing")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = _parse_missing_report(out_path)

    new_count = 0
    for label, refs in all_missing:
        for ref in refs:
            parts = ref.replace("MISSING:", "").strip().split("—")
            missing_label = parts[0].strip() if parts else ""
            key = (label, missing_label)
            if key not in existing:
                existing[key] = f"- **{label}**: {ref}"
                new_count += 1

    # Write merged report (only when there are new findings or no report exists)
    if new_count > 0 or not out_path.exists():
        with open(out_path, "w") as rf:
            rf.write(f"# Missing Dependencies — {asn_label}\n\n")
            rf.write(f"*Last scanned: {time.strftime('%Y-%m-%d %H:%M')}*\n\n")

            if not existing:
                rf.write("No missing dependencies found.\n")
            else:
                for key in sorted(existing.keys()):
                    rf.write(f"{existing[key]}\n")
                rf.write(f"\n*{len(prop_files)} files scanned.*\n")

    # Print summary
    unique_missing = set(k[1] for k in existing.keys())
    if unique_missing:
        print(f"\n  [LINT-MISSING] {len(unique_missing)} undeclared label(s)"
              f" ({new_count} new):", file=sys.stderr)
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
            "elapsed_s": 0,
            "files_scanned": len(prop_files),
            "missing_count": len(all_missing),
        }
        with open(USAGE_LOG, "a") as wf:
            wf.write(json.dumps(entry) + "\n")
    except OSError:
        pass

    return new_count


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
    sp_status.add_argument("--formalization", action="store_true",
        help="Read from vault/3-formalization/ instead of blueprint/ASN")

    # deps subcommand
    sp_deps = subparsers.add_parser("deps",
        help="Lint dependency declarations across ASNs")
    sp_deps.add_argument("asns", nargs="*", type=int,
        help="ASN numbers to check (default: all active)")

    # inline subcommand
    sp_inline = subparsers.add_parser("inline",
        help="Scan blueprint files for embedded results to promote")
    sp_inline.add_argument("asn", help="ASN number (e.g., 34)")
    sp_inline.add_argument("--cycles", type=int, default=3,
        help="Number of scan cycles to run (default: 3)")
    sp_inline.add_argument("--model", default="claude-sonnet-4-6",
        help="Model to use (default: claude-sonnet-4-6)")
    sp_inline.add_argument("--dry-run", action="store_true",
        help="Show candidates without invoking Claude")

    # missing subcommand
    sp_missing = subparsers.add_parser("missing",
        help="Check blueprint files for references to undeclared labels (LLM)")
    sp_missing.add_argument("asn", help="ASN number (e.g., 34)")
    sp_missing.add_argument("--cycles", type=int, default=3,
        help="Number of scan cycles to run (default: 3)")
    sp_missing.add_argument("--model", default="claude-opus-4-6",
        help="Model to use (default: claude-opus-4-6)")

    args = parser.parse_args()

    from lib.shared.common import step_commit_asn

    if args.command == "status":
        asn_num = int(re.sub(r"[^0-9]", "", args.asn))
        lint_status(asn_num, dry_run=args.dry_run,
                    formalization=getattr(args, 'formalization', False))
        step_commit_asn(asn_num, hint="lint-status")
    elif args.command == "deps":
        lint_deps(asn_nums=args.asns if args.asns else None)
    elif args.command == "inline":
        asn_num = int(re.sub(r"[^0-9]", "", args.asn))
        if args.dry_run:
            lint_inline(asn_num, dry_run=True)
        else:
            for cycle in range(1, args.cycles + 1):
                print(f"\n  === Cycle {cycle}/{args.cycles} ===",
                      file=sys.stderr)
                new_count = lint_inline(asn_num, model=args.model)
                if new_count > 0:
                    step_commit_asn(asn_num, hint="lint-inline")
    elif args.command == "missing":
        asn_num = int(re.sub(r"[^0-9]", "", args.asn))
        for cycle in range(1, args.cycles + 1):
            print(f"\n  === Cycle {cycle}/{args.cycles} ===",
                  file=sys.stderr)
            new_count = lint_missing(asn_num, model=args.model)
            if new_count > 0:
                step_commit_asn(asn_num, hint="lint-missing")


if __name__ == "__main__":
    main()
