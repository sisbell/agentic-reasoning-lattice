"""
Rebase review step — four review passes producing unified findings.

Pass 1: Mechanical (deterministic) — stale labels, missing deps, undeclared ASNs
Pass 2: Cross-reference (LLM) — name mismatches, local redefinitions
Pass 3: Extension (LLM) — extends/parallels claims verified semantically
Pass 4: Dependency report (LLM) — structural drift, registry misclassification

Step functions for the orchestrator (scripts/formalization-rebase.py):
- run_review: run all four passes, return list of Finding objects
"""

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import FORMALIZATION_DIR, DOMAIN_PROMPTS, formal_stmts, load_manifest, dep_graph
from lib.shared.common import find_asn, assemble_readonly, read_file
from lib.shared.foundation import load_foundation_statements
from lib.formalization.core.build_dependency_graph import generate_discovery_deps
from lib.formalization.core.finding import Finding
from lib.blueprinting.lint import build_label_map, scan_reasoning_doc, get_dep_chain

PROMPTS_DIR = DOMAIN_PROMPTS / "rebase"
REVIEW_TEMPLATE = PROMPTS_DIR / "review.md"
DEP_REPORT_TEMPLATE = DOMAIN_PROMPTS / "shared" / "dependency-report.md"
EXT_PROMPT_TEMPLATE = DOMAIN_PROMPTS / "formalization" / "rebase" / "verify-extension.md"


# ---------------------------------------------------------------------------
# Extension claims — inlined from core/extensions.py
# ---------------------------------------------------------------------------

@dataclass
class _ExtensionClaim:
    local_label: str
    local_type: str  # "extends" or "parallels"
    foundation_label: str
    foundation_asn: int
    foundation_name: str
    context: str  # surrounding prose from ASN


def _load_deps_yaml(asn_num):
    """Load deps YAML. Returns dict or None."""
    path = dep_graph(asn_num)
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def _extract_prose_context(asn_text, label, max_chars=1500):
    """Extract prose around a claim label from the ASN text.

    Finds the claim definition (**LABEL — Name.**) and captures
    the surrounding text.
    """
    # Find the claim section
    pattern = re.compile(
        r'\*\*' + re.escape(label) + r'\s*(?:—|–|-)',
        re.MULTILINE
    )
    m = pattern.search(asn_text)
    if not m:
        # Try without bold
        pattern = re.compile(r'^' + re.escape(label) + r'\s*(?:—|–|-)', re.MULTILINE)
        m = pattern.search(asn_text)
    if not m:
        return f"[claim section for {label} not found in ASN]"

    start = m.start()

    # Capture forward until next claim or section header
    next_prop = re.search(r'\n\*\*[A-Z]', asn_text[start + 10:])
    next_section = re.search(r'\n## ', asn_text[start + 10:])

    end = len(asn_text)
    if next_prop:
        end = min(end, start + 10 + next_prop.start())
    if next_section:
        end = min(end, start + 10 + next_section.start())

    text = asn_text[start:end].strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "\n[...truncated...]"

    return text


def extract_claims(asn_num):
    """Extract all extension/parallel claims from an ASN.

    Returns list of _ExtensionClaim.
    """
    deps = _load_deps_yaml(asn_num)
    if deps is None:
        print(f"  [ERROR] No deps YAML for ASN-{asn_num:04d}", file=sys.stderr)
        return []

    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ERROR] ASN-{asn_num:04d} not found", file=sys.stderr)
        return []

    # Use assembled per-claim files if available
    asn_text = assemble_readonly(asn_label)
    if not asn_text:
        asn_text = asn_path.read_text()
    claims = []

    # Source 1: deps YAML extends/parallels entries
    for label, claim_data in deps["claims"].items():
        for rel_type in ("extends", "parallels"):
            rel = claim_data.get(rel_type)
            if not rel:
                continue

            foundation_label = rel.get("label", "")
            foundation_asn = rel.get("asn")
            foundation_name = rel.get("name", "")

            if not foundation_label or not foundation_asn:
                continue

            context = _extract_prose_context(asn_text, label)

            claims.append(_ExtensionClaim(
                local_label=label,
                local_type=rel_type,
                foundation_label=foundation_label,
                foundation_asn=foundation_asn,
                foundation_name=foundation_name,
                context=context,
            ))

    # Source 2: prose keyword scan for parallels/analogs not in deps YAML
    seen = {(c.local_label, c.foundation_label) for c in claims}
    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])

    # Build label→asn map from dependency exports
    label_to_asn = {}
    for dep_id in depends:
        stmt_path = formal_stmts(dep_id)
        if not stmt_path.exists():
            continue
        text = stmt_path.read_text()
        for m in re.finditer(r'^## (\S+) — ', text, re.MULTILINE):
            label_to_asn[m.group(1)] = dep_id

    # Scan prose for parallel/analog claims
    parallel_pattern = re.compile(
        r'(?:parallels?|analog(?:ous)?\s+(?:of|to)?|mirrors?|same\s+(?:role|argument|reasoning)\s+as)\s+'
        r'(\S+)(?:\s+(?:for|in|from))?\s*(?:\((?:[^,]+,\s*)?ASN-(\d{4})\))?',
        re.IGNORECASE
    )

    for label, claim_data in deps["claims"].items():
        context = _extract_prose_context(asn_text, label, max_chars=2000)

        for m in parallel_pattern.finditer(context):
            foundation_label = m.group(1).strip(".,;:()")
            foundation_asn = int(m.group(2)) if m.group(2) else label_to_asn.get(foundation_label)

            if not foundation_asn:
                continue

            if (label, foundation_label) in seen:
                continue

            seen.add((label, foundation_label))
            claims.append(_ExtensionClaim(
                local_label=label,
                local_type="parallels",
                foundation_label=foundation_label,
                foundation_asn=foundation_asn,
                foundation_name="",
                context=context,
            ))

    return claims


def _load_foundation_statement(foundation_label, foundation_asn):
    """Load a specific foundation claim's statement from its export."""
    stmt_path = formal_stmts(foundation_asn)
    if not stmt_path.exists():
        return f"[export not found for ASN-{foundation_asn:04d}]"

    text = stmt_path.read_text()

    # Find the section for this label
    pattern = re.compile(
        r'^## ' + re.escape(foundation_label) + r'\s*—\s*(.+?)(?=\n## |\Z)',
        re.MULTILINE | re.DOTALL
    )
    m = pattern.search(text)
    if m:
        section = m.group(0).strip()
        if len(section) > 2000:
            section = section[:2000] + "\n[...truncated...]"
        return section

    return f"[claim {foundation_label} not found in ASN-{foundation_asn:04d} export]"


def verify_claims(claims, model="sonnet", effort="high", batch_size=3):
    """Run focused LLM verification on extension claims.

    Returns list of (claim, verdict, explanation) tuples.
    """
    template = read_file(EXT_PROMPT_TEMPLATE)
    if not template:
        print(f"  [ERROR] Prompt template not found: {EXT_PROMPT_TEMPLATE}",
              file=sys.stderr)
        return []

    results = []

    # Process in batches
    for i in range(0, len(claims), batch_size):
        batch = claims[i:i + batch_size]

        # Build prompt for this batch
        sections = []
        for j, claim in enumerate(batch, 1):
            foundation_stmt = _load_foundation_statement(
                claim.foundation_label, claim.foundation_asn)

            sections.append(f"""### Claim {j}
**Local claim**: {claim.local_label} ({claim.local_type} {claim.foundation_label} from ASN-{claim.foundation_asn:04d})
**Foundation claim**:
{foundation_stmt}

**Local context**:
{claim.context}
""")

        claims_text = "\n---\n".join(sections)
        prompt = template.replace("{{claims}}", claims_text)
        prompt = prompt.replace("{{count}}", str(len(batch)))

        # Call LLM
        model_flag = {"opus": "claude-opus-4-7", "sonnet": "claude-sonnet-4-6"}.get(model, model)
        cmd = ["claude", "--print", "--model", model_flag,
               "--output-format", "json", "--tools", ""]

        env = os.environ.copy()
        env.pop("CLAUDECODE", None)
        env["DISABLE_AUTOUPDATER"] = "1"
        if effort:
            env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

        start = time.time()
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, env=env,
            timeout=None,
        )
        elapsed = time.time() - start

        if result.returncode != 0:
            print(f"  [VERIFY] Batch {i // batch_size + 1} FAILED ({elapsed:.0f}s)",
                  file=sys.stderr)
            for claim in batch:
                results.append((claim, "ERROR", "LLM call failed"))
            continue

        # Parse response
        try:
            data = json.loads(result.stdout)
            response_text = data.get("result", result.stdout)
        except (json.JSONDecodeError, KeyError):
            response_text = result.stdout

        # Extract verdicts: look for VERIFIED or GAP patterns
        for j, claim in enumerate(batch, 1):
            verdict_pattern = re.compile(
                rf'(?:Claim\s*{j}|{re.escape(claim.local_label)})\s*[:\-]\s*(VERIFIED|GAP)\s*[:\-]?\s*(.*?)(?=(?:Claim\s*\d|$))',
                re.DOTALL | re.IGNORECASE
            )
            vm = verdict_pattern.search(response_text)
            if vm:
                verdict = vm.group(1).upper()
                explanation = vm.group(2).strip()[:200]
                results.append((claim, verdict, explanation))
            else:
                results.append((claim, "UNCLEAR", "Could not parse verdict"))

        print(f"  [VERIFY] Batch {i // batch_size + 1}: "
              f"{sum(1 for _, v, _ in results[-len(batch):] if v == 'VERIFIED')} verified, "
              f"{sum(1 for _, v, _ in results[-len(batch):] if v == 'GAP')} gaps "
              f"({elapsed:.0f}s)", file=sys.stderr)

    return results


def format_findings(results):
    """Format GAP results as findings for open-issues.md."""
    lines = []
    for claim, verdict, explanation in results:
        if verdict == "GAP":
            lines.append(f"### Finding: [{claim.local_type}] {claim.local_label} "
                         f"→ {claim.foundation_label} (ASN-{claim.foundation_asn:04d})")
            lines.append(f"**Type**: domain extension gap")
            lines.append(f"**Detail**: {explanation}")
            lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Mechanical checks — inlined from core/mechanical.py
# ---------------------------------------------------------------------------

def _check_stale_labels(deps, label_map, dep_chain):
    """Check 1: every label in follows_from must exist in a dependency's export.

    Labels that are local (defined in the same ASN's deps) are OK.
    Labels from dependency ASNs must appear in their exports.
    """
    findings = []
    asn_num = deps["asn"]

    # Build set of local labels (defined in this ASN)
    local_labels = set(deps["claims"].keys())

    for claim_label, claim_data in deps["claims"].items():
        for ref_label in claim_data.get("follows_from", []):
            # Local reference — OK
            if ref_label in local_labels:
                continue

            # Check if label exists in any dependency's export
            if ref_label in label_map:
                source = label_map[ref_label]
                if source not in dep_chain and source != asn_num:
                    findings.append(Finding(
                        category="undeclared-asn",
                        label=ref_label,
                        source_asn=source,
                        location=f"deps:{claim_label}",
                        detail=f"Claim {claim_label} references {ref_label} "
                               f"from ASN-{source:04d}, which is not in depends "
                               f"(declared: {deps['depends']})"
                    ))
            else:
                findings.append(Finding(
                    category="stale-label",
                    label=ref_label,
                    source_asn=None,
                    location=f"deps:{claim_label}",
                    detail=f"Claim {claim_label} references {ref_label} "
                           f"which does not exist in any active ASN's export"
                ))

        # Check extends/parallels references
        for rel_type in ("extends", "parallels"):
            rel = claim_data.get(rel_type)
            if not rel:
                continue
            ref_label = rel.get("label", "")
            ref_asn = rel.get("asn")
            if ref_label and ref_label not in label_map:
                findings.append(Finding(
                    category="stale-label",
                    label=ref_label,
                    source_asn=ref_asn,
                    location=f"deps:{claim_label}.{rel_type}",
                    detail=f"Claim {claim_label} {rel_type} {ref_label} "
                           f"which does not exist in any active ASN's export"
                ))
            if ref_asn and ref_asn not in dep_chain:
                findings.append(Finding(
                    category="undeclared-asn",
                    label=ref_label,
                    source_asn=ref_asn,
                    location=f"deps:{claim_label}.{rel_type}",
                    detail=f"Claim {claim_label} {rel_type} references "
                           f"ASN-{ref_asn:04d} which is not in depends"
                ))

    return findings


def _check_prose_citations(asn_num, deps, label_map, dep_chain):
    """Check 2: ASN prose cites foundation labels not in the deps YAML.

    Find labels referenced in the prose that come from dependency ASNs
    but are not declared in the claim table's follows_from.
    """
    findings = []
    asn_path, _ = find_asn(str(asn_num))
    if asn_path is None:
        return findings

    # Get all labels referenced in prose
    prose_refs = scan_reasoning_doc(asn_path, label_map)

    # Build the set of all labels declared in deps YAML follows_from
    declared_labels = set()
    for claim_data in deps["claims"].values():
        declared_labels.update(claim_data.get("follows_from", []))
        for rel_type in ("extends", "parallels"):
            rel = claim_data.get(rel_type)
            if rel and rel.get("label"):
                declared_labels.add(rel["label"])

    # Also include local labels
    local_labels = set(deps["claims"].keys())

    for ref_label, source_asn in prose_refs.items():
        # Skip if it's a local label
        if ref_label in local_labels:
            continue

        # Skip if it's from the ASN itself
        if source_asn == asn_num:
            continue

        # Skip if it's already declared in deps YAML
        if ref_label in declared_labels:
            continue

        # Skip if it's not from a dependency (could be a different context)
        if source_asn not in dep_chain:
            continue

        findings.append(Finding(
            category="prose-only",
            label=ref_label,
            source_asn=source_asn,
            location="prose",
            detail=f"Prose cites {ref_label} (ASN-{source_asn:04d}) "
                   f"but no claim table entry lists it in follows_from"
        ))

    return findings


def check_asn(asn_num, verbose=False):
    """Run all mechanical checks on an ASN. Returns list of Findings."""
    deps = _load_deps_yaml(asn_num)
    if deps is None:
        print(f"  [ERROR] No deps YAML for ASN-{asn_num:04d} — "
              f"run: python scripts/lib/rebase_deps.py {asn_num}",
              file=sys.stderr)
        return None

    label_map, _ = build_label_map()
    dep_chain = get_dep_chain(asn_num)

    if verbose:
        print(f"  [INFO] ASN-{asn_num:04d}: {len(deps['claims'])} claims, "
              f"depends: {deps['depends']}, dep chain: {sorted(dep_chain)}",
              file=sys.stderr)
        print(f"  [INFO] Label map: {len(label_map)} labels across active ASNs",
              file=sys.stderr)

    findings = []

    # Check 1: stale labels and undeclared ASN references
    findings.extend(_check_stale_labels(deps, label_map, dep_chain))

    # Check 2: prose citations not in deps YAML
    findings.extend(_check_prose_citations(asn_num, deps, label_map, dep_chain))

    return findings


# ---------------------------------------------------------------------------
# Review passes
# ---------------------------------------------------------------------------

def run_review(asn_num, target_labels=None):
    """Run all four review passes. Returns list of Finding objects."""
    findings = []

    # Pass 1: Mechanical (deterministic)
    print(f"  [MECHANICAL]", end="", file=sys.stderr, flush=True)
    mechanical = check_asn(asn_num)
    if mechanical:
        findings.extend(mechanical)
        print(f" {len(mechanical)} findings", file=sys.stderr)
    else:
        print(f" clean", file=sys.stderr)

    # Pass 2: Cross-reference (LLM)
    print(f"  [CROSS-REF]", end="", file=sys.stderr, flush=True)
    xref = _check_cross_references(asn_num, target_labels)
    if xref:
        findings.extend(xref)
        print(f" {len(xref)} findings", file=sys.stderr)
    else:
        print(f" clean", file=sys.stderr)

    # Pass 3: Extension (LLM)
    print(f"  [EXTENSION]", end="", file=sys.stderr, flush=True)
    ext = _check_extensions(asn_num)
    if ext:
        findings.extend(ext)
        print(f" {len(ext)} findings", file=sys.stderr)
    else:
        print(f" clean", file=sys.stderr)

    # Pass 4: Dependency report (LLM, whole-ASN)
    print(f"  [DEP-REPORT]", end="", file=sys.stderr, flush=True)
    dep_report = _check_dependency_report(asn_num)
    if dep_report:
        findings.extend(dep_report)
        print(f" {len(dep_report)} findings", file=sys.stderr)
    else:
        print(f" clean", file=sys.stderr)

    # Filter to target labels if specified
    if target_labels:
        findings = [f for f in findings if f.label in target_labels]

    return findings


def _check_cross_references(asn_num, target_labels=None):
    """Pass 2: Cross-reference check."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return []

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", [])
    if not depends:
        return []

    # Load upstream canonical names and sections
    upstream_names = {}
    upstream_sections = {}
    for dep_num in depends:
        stmts_path = formal_stmts(dep_num)
        if not stmts_path.exists():
            continue
        stmts_text = stmts_path.read_text()

        dep_labels = []
        for line in stmts_text.split("\n"):
            m = re.match(r'^##\s+(.+?)\s+\u2014\s+(.+?)(?:\s+\(|$)', line)
            if m:
                label = m.group(1).strip()
                name = m.group(2).strip()
                dep_labels.append(label)
                pascal = re.match(r'^([A-Z][a-zA-Z0-9]+)', name)
                if pascal:
                    upstream_names[label] = pascal.group(1)

        sections = extract_claim_sections(
            stmts_text, known_labels=dep_labels, truncate=False)
        for label, section in sections.items():
            upstream_sections[label] = (dep_num, section)

    if not upstream_names:
        return []

    # Use assembled per-claim files if available
    asn_text = assemble_readonly(asn_label)
    if not asn_text:
        asn_text = asn_path.read_text()

    deps_data = generate_discovery_deps(asn_num)
    if not deps_data:
        return []

    findings = []

    # Sub-check (a): Inline name mismatches
    for up_label, canonical_name in upstream_names.items():
        pattern = re.compile(
            r'(?:\*\*)?'
            + re.escape(up_label)
            + r'\s+\(([A-Z][a-zA-Z]+)\)'
        )
        for m in pattern.finditer(asn_text):
            cited_name = m.group(1)
            if cited_name != canonical_name:
                line_num = asn_text[:m.start()].count('\n') + 1
                claim_label = _find_containing_claim(
                    deps_data, asn_text, m.start())
                if target_labels and claim_label and claim_label not in target_labels:
                    continue
                findings.append(Finding(
                    category="name-mismatch",
                    label=claim_label or up_label,
                    source_asn=None,
                    location=f"prose:L{line_num}",
                    detail=(f"{up_label} cited as \"{cited_name}\" but "
                            f"upstream canonical name is \"{canonical_name}\". "
                            f"**Required**: Replace \"{up_label} ({cited_name})\" "
                            f"with \"{up_label} ({canonical_name})\" everywhere "
                            f"in this claim section."),
                ))
                break

    # Sub-check (b): Redefinition check
    for label, claim_data in deps_data.get("claims", {}).items():
        if target_labels and label not in target_labels:
            continue
        local_name = claim_data.get("name", "")
        if not local_name:
            continue
        for up_label, canonical_name in upstream_names.items():
            if local_name == canonical_name or local_name == up_label:
                status = claim_data.get("status", "")
                if status in ("cited", "corollary", "confirms"):
                    continue
                dep_num = (upstream_sections[up_label][0]
                           if up_label in upstream_sections else None)
                dep_str = f"ASN-{dep_num:04d}" if dep_num else "upstream"
                findings.append(Finding(
                    category="redefinition",
                    label=label,
                    source_asn=dep_num,
                    location=f"redefines:{up_label}",
                    detail=(f"Local claim {label} ({local_name}) has the same "
                            f"name as upstream {up_label} ({canonical_name}) from "
                            f"{dep_str}. If these are the same claim, "
                            f"{label} should cite the upstream rather than re-derive "
                            f"it locally. "
                            f"**Required**: If {label} proves the same invariant as "
                            f"upstream {up_label}, change its status to 'cited' and "
                            f"add a citation to {dep_str} {up_label}. If it "
                            f"proves something different despite the same name, rename "
                            f"it to avoid confusion."),
                ))

    # Sub-check (c): LLM semantic check
    template = REVIEW_TEMPLATE.read_text()
    all_labels = list(deps_data.get("claims", {}).keys())

    # Read per-claim files if available
    claim_dir = FORMALIZATION_DIR / asn_label
    if claim_dir.exists():
        from lib.shared.common import load_claim_sections
        local_sections = load_claim_sections(claim_dir)
    else:
        from lib.shared.common import extract_claim_sections
        local_sections = extract_claim_sections(
            asn_text, known_labels=all_labels, truncate=False)

    for label, claim_data in deps_data.get("claims", {}).items():
        if target_labels and label not in target_labels:
            continue

        follows_from_asns = claim_data.get("follows_from_asns", [])
        if not follows_from_asns:
            continue

        local_section = local_sections.get(label, "")
        if not local_section:
            continue

        follows_from = claim_data.get("follows_from", [])
        for ref_label in follows_from:
            if ref_label not in upstream_sections:
                continue

            dep_num, upstream_section = upstream_sections[ref_label]

            prompt = (template
                .replace("{{claim_label}}", label)
                .replace("{{claim_section}}", local_section[:3000])
                .replace("{{upstream_label}}", ref_label)
                .replace("{{upstream_asn}}", str(dep_num))
                .replace("{{upstream_contract}}", upstream_section[:3000]))

            rec, reason = _run_review_check(prompt, label)
            if rec == "flag":
                findings.append(Finding(
                    category="cross-ref",
                    label=label,
                    source_asn=dep_num,
                    location=f"ref:{ref_label}",
                    detail=reason,
                ))

    return findings


def _find_containing_claim(deps_data, asn_text, char_offset):
    """Find which claim section contains a given character offset."""
    props = []
    for m in re.finditer(r'\*\*(\S+)\s*(?:\(|—|–|-)', asn_text):
        label = m.group(1)
        if label in deps_data.get("claims", {}):
            props.append((m.start(), label))

    if not props:
        return None

    result = None
    for pos, label in props:
        if pos <= char_offset:
            result = label
        else:
            break
    return result


def _check_extensions(asn_num):
    """Pass 3: Extension verification."""
    claims = extract_claims(asn_num)
    if not claims:
        return []

    results = verify_claims(claims, model="sonnet", effort="high")
    findings = []
    for claim, verdict, explanation in results:
        if verdict == "GAP":
            findings.append(Finding(
                category="extension-gap",
                label=claim.local_label,
                source_asn=claim.foundation_asn,
                location=f"extends:{claim.foundation_label}",
                detail=explanation,
            ))

    return findings


def _run_review_check(prompt, label):
    """Run a single LLM review check. Returns (rec, reason)."""
    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )

    if result.returncode != 0:
        return "error", f"review failed for {label}"

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

    return rec, reason


def _check_dependency_report(asn_num):
    """Pass 4: Dependency report (LLM, whole-ASN)."""
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        return []

    manifest = load_manifest(asn_num)
    depends = manifest.get("depends", []) if manifest else []
    if not depends:
        return []

    foundation = load_foundation_statements(asn_num)
    if not foundation:
        return []

    # Use assembled per-claim files if available
    asn_content = assemble_readonly(asn_label)
    if not asn_content:
        asn_content = asn_path.read_text()

    template = DEP_REPORT_TEMPLATE.read_text()
    depends_str = ", ".join(f"ASN-{d:04d}" for d in depends)
    prompt = (template
              .replace("{{foundation_statements}}", foundation)
              .replace("{{asn_content}}", asn_content)
              .replace("{{asn_label}}", asn_label)
              .replace("{{depends}}", depends_str))

    cmd = [
        "claude", "--print", "--model", "claude-sonnet-4-6",
    ]
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )

    if result.returncode != 0:
        return []

    text = result.stdout.strip()

    if "RESULT: CLEAN" in text:
        return []

    # Return as a single finding containing the full report text.
    # The reviser reads the whole report and applies fixes — no
    # per-finding label extraction needed.
    m = re.search(r'RESULT:\s*(\d+)\s*FINDING', text)
    count = int(m.group(1)) if m else 1

    findings = [Finding(
        category="dep-report",
        label="",
        source_asn=None,
        location="dep-report",
        detail=text,
    )]

    return findings
