#!/usr/bin/env python3
"""Test driver for the motif extraction pipeline.

Walks a scout output through Selector → Cluster → Absorb Target.
Dry-run only: no substrate emissions, no `note_extract.py` dispatch.
Saves each LLM call's raw output plus the would-be note_extract spec.

Usage:
    python scripts/test-motif-pipeline.py _workspace/scout-runs/<file>.md
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn, read_file
from lib.shared.foundation import FoundationError, foundation_dep_ids
from lib.shared.invoke_claude import invoke_claude
import yaml
from lib.shared.paths import CLAIM_DIR, LATTICE, WORKSPACE, prompt_path


SELECT_PROMPT = prompt_path("agents/producers/motif_select.md")
LAYER_PROMPT = prompt_path("agents/producers/motif_layer_analyzer.md")
CLUSTER_PROMPT = prompt_path("agents/producers/motif_cluster.md")
ABSORB_PROMPT = prompt_path("agents/producers/motif_absorb_target.md")
OUTPUT_BASE = WORKSPACE / "_workspace" / "motif-pipeline"


def load_yaml(path):
    """Load a YAML document, tolerating a wrapping code fence.

    Some LLM runs wrap the YAML in ```yaml … ``` even when told not
    to. Strip a leading fence and the matching trailing fence, then
    parse. Returns whatever yaml.safe_load returns (dict, list, or
    None).
    """
    text = path.read_text().strip()
    if text.startswith("```"):
        text = re.sub(r"^```[^\n]*\n", "", text, count=1)
        text = re.sub(r"\n```\s*$", "", text)
    return yaml.safe_load(text)


def label_to_num(label):
    """Convert 'ASN-0034' (or similar) to int 34. Returns None on miss."""
    if not label:
        return None
    m = re.search(r"(\d+)", str(label))
    return int(m.group(1)) if m else None


def extract_finding_section(scout_report, motif_label):
    """Return the text of `### Finding N — ...` whose number matches motif_label.

    motif_label is the selector's MOTIF line value, e.g.
    'Finding 1 — Cross-document isolation'.
    """
    m = re.match(r"Finding\s+(\d+)", motif_label)
    if not m:
        return None
    target_n = int(m.group(1))

    lines = scout_report.splitlines()
    start = None
    for i, line in enumerate(lines):
        m2 = re.match(r"###\s+Finding\s+(\d+)\b", line.strip())
        if m2 and int(m2.group(1)) == target_n:
            start = i
            break
    if start is None:
        return None

    end = len(lines)
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if re.match(r"###\s+Finding\s+\d+", s):
            end = j
            break
        if s.startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).rstrip()


def cited_nums_for_finding(scout_fm, motif_id):
    """Return sorted ASN nums for one motif's cited_claims (from scout YAML)."""
    motifs = (scout_fm or {}).get("motifs") or []
    for f in motifs:
        if f.get("id") == motif_id:
            return sorted({
                label_to_num(k) for k in (f.get("cited_claims") or {})
                if label_to_num(k) is not None
            })
    return []


def format_notes_block(asn_nums):
    """Concat input note bodies with separator headers between them."""
    parts = []
    for n in asn_nums:
        path, label = find_asn(str(n))
        if path is None:
            continue
        parts.append(f"### {label}\n\n{path.read_text().rstrip()}\n")
    return "\n---\n\n".join(parts)


def first_cited_seed(finding_text):
    """Extract first `ASN-NNNN[:,] LABEL` pair from a finding's body.

    Tolerates the scout's varying citation styles:
    - `ASN-0059: **I5** (DocumentIsolation)`
    - `ASN-0034, **T8 (AllocationPermanence)**`
    - `ASN-0034: T10a AllocatorDiscipline` (no asterisks)
    - `ASN-0040: S(p,d) Sibling stream` (label with parens)

    The captured label is the first identifier token after the
    colon/comma (optionally bold-wrapped), with any immediately-
    adjacent `(...)` included as part of the label.
    """
    m = re.search(
        r"ASN-(\d+)[:,]\s*(?:\*\*)?\s*"
        r"([A-Za-z][A-Za-z0-9_\-]*(?:\([^)]*\))?)",
        finding_text,
    )
    if not m:
        return None
    return int(m.group(1)), m.group(2)


def parse_layer(text):
    pattern = anchor = push_below = rationale = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("PATTERN:"):
            pattern = s.split(":", 1)[1].strip()
        elif s.startswith("ANCHOR:"):
            anchor = s.split(":", 1)[1].strip()
        elif s.startswith("PUSH_BELOW:"):
            push_below = s.split(":", 1)[1].strip()
        elif s.startswith("RATIONALE:"):
            rationale = s.split(":", 1)[1].strip()
    return pattern, anchor, push_below, rationale


def parse_cluster(text):
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("CLUSTER:"):
            rest = s.split(":", 1)[1].strip()
            return [t.strip() for t in rest.split(",") if t.strip()]
    return []




def note_title(asn_num):
    """Title from the note's first H1, e.g. 'ASN-0036: Strand Model'."""
    path, label = find_asn(str(asn_num))
    if path is None:
        return None
    for line in path.read_text().splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return label


def _extract_from_prose(origin_content, labels):
    """Extract claim bodies from a note's prose by label.

    Recognizes `**LABEL — Name.**` claim markers (operation-style
    notes not yet blueprinted to per-claim files). Body extends until
    the next claim marker (any label) or the next `## ` section
    break, whichever comes first.
    """
    header_re = re.compile(
        r"\*\*\s*([A-Za-z][A-Za-z0-9_\-]*)\s+[—–-]\s+[^*]+\*\*",
    )
    section_re = re.compile(r"^##\s", re.MULTILINE)
    headers = [
        (m.start(), m.group(1)) for m in header_re.finditer(origin_content)
    ]
    sections = [m.start() for m in section_re.finditer(origin_content)]

    chunks = []
    for label in labels:
        start = next(
            (pos for pos, hdr in headers if hdr == label), None,
        )
        if start is None:
            chunks.append(f"(no claim body found for {label} in origin)")
            continue
        end = len(origin_content)
        for pos, _ in headers:
            if start < pos < end:
                end = pos
        for pos in sections:
            if start < pos < end:
                end = pos
        chunks.append(origin_content[start:end].rstrip())
    return "\n\n".join(chunks)


def extract_claim_bodies(asn_num, labels, origin_content):
    """Return concatenated claim bodies for the cluster.

    Blueprinted ASNs (per-claim files under CLAIM_DIR/<asn>/<label>.md)
    win — the per-claim md is the authoritative body and carries the
    Formal Contract / Depends sections the prose may not. Otherwise
    fall back to the note's prose (claim markers like
    `**LABEL — Name.**`).
    """
    asn_label = format_label(asn_num)
    claim_dir = CLAIM_DIR / asn_label
    if claim_dir.is_dir() and any(claim_dir.glob("*.md")):
        chunks = []
        for label in labels:
            path = claim_dir / f"{label}.md"
            if path.exists():
                chunks.append(f"### {label}\n\n{path.read_text().rstrip()}")
            else:
                chunks.append(
                    f"### {label}\n\n(no per-claim file at "
                    f"{path.relative_to(WORKSPACE)})",
                )
        return "\n\n".join(chunks)
    return _extract_from_prose(origin_content, labels)


def format_candidate_destinations(dep_ids):
    if not dep_ids:
        return "(none)"
    sections = []
    for d in dep_ids:
        path, label = find_asn(str(d))
        if path is None:
            sections.append(f"## {format_label(d)} — (note not found)\n")
            continue
        sections.append(
            f"## {format_label(d)} — {note_title(d) or label}\n\n"
            f"{path.read_text().rstrip()}\n",
        )
    return "\n\n---\n\n".join(sections)


def all_transitive_deps(asn_nums):
    """BFS over note-level citation.depends from the given ASN numbers.

    Returns sorted list of every transitively-reachable dep ASN id,
    excluding the input set.
    """
    visited = set()
    queue = list(asn_nums)
    with open_session(LATTICE) as session:
        while queue:
            n = queue.pop()
            if n in visited:
                continue
            visited.add(n)
            try:
                deps = foundation_dep_ids(session, n)
            except FoundationError:
                continue
            queue.extend(d for d in deps if d not in visited)
    return sorted(visited - set(asn_nums))


def run_llm(label, prompt, model, effort, output_path):
    print(f"\n  [{label}] invoking ({len(prompt)//1024} KB)...",
          file=sys.stderr)
    result = invoke_claude(
        prompt, model=model, effort=effort, tools="", output_format=None,
    )
    if not result.text:
        print(f"  [{label}] LLM call failed ({result.elapsed:.0f}s)",
              file=sys.stderr)
        return None
    output_path.write_text(result.text)
    print(f"  [{label}] {result.elapsed:.0f}s, ${result.cost:.4f}",
          file=sys.stderr)
    print(result.text, file=sys.stderr)
    return result.text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scout_run", type=str,
                        help="Path to scout-run markdown")
    parser.add_argument("--model", "-m", default="opus",
                        choices=["opus", "sonnet"])
    parser.add_argument("--effort", default="high",
                        help="Thinking effort (max | high | medium | low)")
    args = parser.parse_args()

    scout_path = Path(args.scout_run)
    if not scout_path.exists():
        scout_path = WORKSPACE / args.scout_run
    if not scout_path.exists():
        print(f"  Scout run not found: {args.scout_run}", file=sys.stderr)
        return 1
    scout_data = load_yaml(scout_path)
    if not isinstance(scout_data, dict) or "motifs" not in scout_data:
        print("  Scout output has no `motifs:` list. "
              "Re-run scout with the updated prompt.", file=sys.stderr)
        return 1
    scout_report = scout_path.read_text()

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_dir = OUTPUT_BASE / f"{timestamp}-{scout_path.stem}"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Output dir: {output_dir.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # All ASN nums mentioned across all motifs — the universe for the
    # Selector to see in {{notes_block}}.
    all_cited_nums = sorted({
        label_to_num(k)
        for f in scout_data["motifs"]
        for k in (f.get("cited_claims") or {})
        if label_to_num(k) is not None
    })

    # --- 1. Selector ---
    notes_block = format_notes_block(all_cited_nums)
    template = read_file(SELECT_PROMPT)
    prompt = (template
              .replace("{{scout_report}}", scout_report)
              .replace("{{notes_block}}", notes_block))
    text = run_llm("1/3 select", prompt, args.model, args.effort,
                   output_dir / "01-select.yaml")
    if text is None:
        return 1
    sel_data = load_yaml(output_dir / "01-select.yaml") or {}
    decision = sel_data.get("decision")
    motif_id = sel_data.get("motif_id")
    motif_name = sel_data.get("motif_name")
    motif = (
        f"Finding {motif_id} — {motif_name}"
        if motif_id and motif_name else None
    )

    if decision != "SELECTED":
        (output_dir / "spec.md").write_text(
            f"# Pipeline halted: {decision}\n\n"
            f"- **Motif:** {motif}\n\n"
            f"{sel_data.get('rationale', '')}",
        )
        print(f"\n  Pipeline halts: {decision}", file=sys.stderr)
        return 0

    cited_nums = cited_nums_for_finding(scout_data, motif_id)
    if not cited_nums:
        print(f"  Selector picked motif_id={motif_id!r} but no matching "
              f"finding in scout YAML.", file=sys.stderr)
        return 1
    notes_block = format_notes_block(cited_nums)

    # Build motif_finding text for downstream agents from the scout's
    # structured motif entry (name + cited_claims + rationale).
    chosen = next(
        (f for f in scout_data["motifs"] if f.get("id") == motif_id),
        {},
    )
    finding_lines = [f"### Motif {motif_id} — {chosen.get('name', '')}"]
    for asn_label, claims in (chosen.get("cited_claims") or {}).items():
        claims_str = (
            ", ".join(str(c) for c in claims)
            if isinstance(claims, list) else claims
        )
        finding_lines.append(f"- **{asn_label}**: {claims_str}")
    if chosen.get("rationale"):
        finding_lines.append("")
        finding_lines.append(chosen["rationale"].rstrip())
    finding_text = "\n".join(finding_lines)

    # --- 2. Base Picker ---
    dep_ids = all_transitive_deps(cited_nums)
    candidate_nums = sorted(set(cited_nums) | set(dep_ids))
    candidates_block = format_candidate_destinations(candidate_nums)

    template = read_file(ABSORB_PROMPT)
    prompt = (template
              .replace("{{motif_finding}}", finding_text)
              .replace("{{candidate_notes}}", candidates_block))
    text = run_llm("2/3 base", prompt, args.model, args.effort,
                   output_dir / "02-base-picker.yaml")
    if text is None:
        return 1
    base_data = load_yaml(output_dir / "02-base-picker.yaml") or {}
    base = base_data.get("base")
    base_rationale = (base_data.get("rationale") or "").strip()

    if base == "STANDALONE":
        case = "STANDALONE"
    elif base and any(format_label(n) == base for n in cited_nums):
        case = "1"
    else:
        case = "2"
    case_descr = {
        "STANDALONE": "STANDALONE (no candidate owns the construct's vocabulary)",
        "1": "1 (base is a cited note — leave canonical, merge others)",
        "2": "2 (base is a dep — merge all cited)",
    }[case]
    print(f"\n  Base: {base}", file=sys.stderr)
    print(f"  Case: {case_descr}", file=sys.stderr)

    # --- 3. Cluster (case-aware) ---
    template = read_file(CLUSTER_PROMPT)
    prompt = (template
              .replace("{{motif_finding}}", finding_text)
              .replace("{{base}}", base or "NONE")
              .replace("{{case}}", case_descr)
              .replace("{{cited_notes}}", notes_block))
    text = run_llm("3/3 cluster", prompt, args.model, args.effort,
                   output_dir / "03-cluster.yaml")
    if text is None:
        return 1
    cluster_data = load_yaml(output_dir / "03-cluster.yaml") or {}
    canonical = cluster_data.get("canonical")
    extract = cluster_data.get("extract_from") or {}
    construct = (cluster_data.get("construct") or "").strip()

    extract_lines = [
        f"- **{asn}**: "
        f"{', '.join(str(c) for c in claims) if isinstance(claims, list) else claims}"
        for asn, claims in (extract or {}).items()
    ]
    spec_lines = [
        "# Motif extraction spec (dry-run)",
        "",
        f"- **Scout run:** `{scout_path.name}`",
        f"- **Selected motif:** {motif}",
        "",
        f"- **Base (extension target):** {base}",
        f"- **Case:** {case_descr}",
        f"- **Base rationale:** {base_rationale}",
        "",
        f"- **Canonical (Case 1 only):** {canonical or 'NONE'}",
        "",
        "## Abstract construct",
        "",
        construct or "(no construct parsed)",
        "",
        "## Extract from",
        "",
        *extract_lines,
        "",
        "## Candidate notes considered",
        "",
        f"Cited: {', '.join(format_label(n) for n in cited_nums)}",
        f"Transitive deps: "
        f"{', '.join(format_label(n) for n in dep_ids) or 'NONE'}",
    ]
    (output_dir / "spec.md").write_text("\n".join(spec_lines) + "\n")
    print(f"\n  Spec: {output_dir.relative_to(WORKSPACE)}/spec.md",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
