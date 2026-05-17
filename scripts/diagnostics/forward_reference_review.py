#!/usr/bin/env python3
"""Forward-reference review diagnostic — operator-invoked.

Walks the active-notes DAG and runs a structural-bloat scan on each note
that (a) has a body file on disk and (b) does not yet have a
claims.statements aggregate (i.e., has not been claim-refined). For each
qualifying note, dispatches an LLM pass that flags forward-reference and
placement-management prose patterns (contract splits, non-circularity
justifications, axiom-rationale accretion, imagined-case prose, use-site
inventories, relocated-not-removed paragraphs).

Output:
  - Console: per-note progress line + final summary.
  - Workspace artifact:
      _workspace/diagnostics/forward-reference-review/<YYYYMMDD-HHMMSS>/
      <ASN>.md per note + index.md aggregating verdicts.

Usage:
  # Walk every qualifying note in the lattice
  python3 scripts/diagnostics/forward_reference_review.py

  # Run on a single ASN for testing the prompt (no skip predicates)
  python3 scripts/diagnostics/forward_reference_review.py --asn 47
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import time
from datetime import datetime, timezone
from glob import glob
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.lattice.labels import format_label
from lib.shared.invoke_claude import invoke_claude
from lib.shared.paths import WORKSPACE, WORKSPACE_DIR


PROMPT_PATH = (
    WORKSPACE / "prompts" / "shared" / "diagnostics"
    / "forward_reference_review.md"
)
OUTPUT_ROOT = WORKSPACE_DIR / "diagnostics" / "forward-reference-review"


def _find_note_file(asn_label: str) -> Path | None:
    """Resolve note body path for an ASN label, or None if no draft yet.

    Returns an absolute path so callers can compose with WORKSPACE.
    """
    pattern = str(
        WORKSPACE / "_docuverse" / "documents" / "1.1" / "1" / "note"
        / f"{asn_label}-*.md"
    )
    for f in glob(pattern):
        if ".statements." in f or ".motif." in f:
            continue
        return Path(f).resolve()
    return None


def _has_claims_statements(asn_label: str) -> bool:
    """True iff a claims.statements aggregate exists for this ASN."""
    return (
        WORKSPACE / "_docuverse" / "documents" / "1.1" / "1"
        / "claim" / asn_label / "_statements.md"
    ).exists()


def _topo_sorted_active() -> list[str]:
    """Reuse note-scheduler's topo-sorted active-notes walker."""
    scheduler_path = (
        Path(__file__).resolve().parent.parent / "note-scheduler.py"
    )
    spec = importlib.util.spec_from_file_location(
        "note_scheduler", scheduler_path,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._active_notes_topo_sorted()


def _qualifying_asns() -> list[str]:
    """Active ASN labels in topo order that qualify for diagnosis:
    have a note body AND no claims.statements aggregate."""
    return [
        a for a in _topo_sorted_active()
        if _find_note_file(a) and not _has_claims_statements(a)
    ]


def _parse_verdict(text: str) -> str:
    for v in ("HEAVY", "LIGHT", "CLEAN"):
        if f"VERDICT: {v}" in text:
            return v
    return "?"


def _diagnose(
    asn_label: str, output_dir: Path, model: str = "sonnet",
) -> tuple[str, int, float]:
    """Run one LLM pass on the note. Returns (verdict, findings, elapsed_s).

    Writes per-note output to `output_dir/<asn>.md`. Returns ("skip", 0, 0)
    when the note body is missing (caller should handle separately for
    bulk-walk vs single-ASN modes).
    """
    note_path = _find_note_file(asn_label)
    if note_path is None:
        print(f"  [FR-DIAG] {asn_label} — no note file", file=sys.stderr)
        return "skip", 0, 0.0

    note_content = note_path.read_text()
    prompt = PROMPT_PATH.read_text()
    prompt = prompt.replace("{{asn_label}}", asn_label)
    prompt = prompt.replace("{{note_content}}", note_content)

    print(
        f"  [FR-DIAG] {asn_label} ({len(note_content.splitlines())} lines, "
        f"{model})...",
        end="", file=sys.stderr, flush=True,
    )
    start = time.time()
    response = invoke_claude(
        prompt, model=model, effort="high",
        tools="", output_format=None,
    )
    elapsed = time.time() - start

    text = (response.text or "").strip()
    findings = text.count("\n### ")
    if text.startswith("### "):
        findings += 1
    verdict = _parse_verdict(text)

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{asn_label}.md"
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    workspace_root = WORKSPACE.resolve()
    try:
        note_rel = note_path.resolve().relative_to(workspace_root)
    except ValueError:
        note_rel = note_path
    out_path.write_text(
        f"# Forward-Reference Review — {asn_label}\n\n"
        f"*{ts}*\n"
        f"*Note: {note_rel}*\n"
        f"*Size: {len(note_content.splitlines())} lines*\n"
        f"*Elapsed: {elapsed:.0f}s*\n"
        f"*Model: {model}, effort=high*\n\n"
        f"---\n\n"
        f"{text}\n"
    )

    print(
        f" {verdict} ({findings} finding{'s' if findings != 1 else ''}, "
        f"{elapsed:.0f}s)",
        file=sys.stderr,
    )
    return verdict, findings, elapsed


def _write_index(
    output_dir: Path, results: list[tuple[str, str, int, float]],
) -> Path:
    """Write index.md aggregating per-note verdicts. Sorted heaviest first."""
    order = {"HEAVY": 0, "LIGHT": 1, "CLEAN": 2, "?": 3, "skip": 4}
    sorted_results = sorted(
        results, key=lambda r: (order.get(r[1], 9), -r[2]),
    )
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        f"# Forward-Reference Review — Index\n\n",
        f"*{ts}*\n",
        f"*{len(results)} note(s) analyzed*\n\n",
        "| ASN | Verdict | Findings | Elapsed |\n",
        "|-----|---------|----------|---------|\n",
    ]
    total_elapsed = 0.0
    for asn, v, f, e in sorted_results:
        lines.append(f"| {asn} | {v} | {f} | {e:.0f}s |\n")
        total_elapsed += e
    lines.append(f"\n**Total elapsed:** {total_elapsed:.0f}s\n")
    index_path = output_dir / "index.md"
    index_path.write_text("".join(lines))
    return index_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Forward-reference review diagnostic",
    )
    parser.add_argument(
        "--asn", type=int, default=None,
        help=(
            "Run on a single ASN (e.g., 47) for prompt testing. Skip "
            "predicates are bypassed. Default: walk the DAG."
        ),
    )
    parser.add_argument(
        "--model", default="sonnet",
        help="LLM to invoke (default: sonnet). Use 'opus' for higher fidelity.",
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = OUTPUT_ROOT / timestamp

    if args.asn is not None:
        asn_label = format_label(args.asn)
        verdict, findings, elapsed = _diagnose(
            asn_label, output_dir, model=args.model,
        )
        if verdict != "skip":
            print(
                f"\n  Output: "
                f"{(output_dir / f'{asn_label}.md').resolve().relative_to(WORKSPACE.resolve())}",
                file=sys.stderr,
            )
        return 0 if verdict != "skip" else 1

    # DAG walk
    asn_labels = _qualifying_asns()
    if not asn_labels:
        print(
            "  [FR-DIAG] no notes qualify (need note body + no "
            "claims.statements aggregate)",
            file=sys.stderr,
        )
        return 0
    print(
        f"  [FR-DIAG] {len(asn_labels)} note(s) to diagnose",
        file=sys.stderr,
    )

    results: list[tuple[str, str, int, float]] = []
    for asn_label in asn_labels:
        verdict, findings, elapsed = _diagnose(
            asn_label, output_dir, model=args.model,
        )
        results.append((asn_label, verdict, findings, elapsed))

    index_path = _write_index(output_dir, results)
    print(
        f"\n  Output: {output_dir.resolve().relative_to(WORKSPACE.resolve())}",
        file=sys.stderr,
    )
    print(
        f"  Index:  {index_path.resolve().relative_to(WORKSPACE.resolve())}",
        file=sys.stderr,
    )

    heavy = sum(1 for _, v, *_ in results if v == "HEAVY")
    light = sum(1 for _, v, *_ in results if v == "LIGHT")
    clean = sum(1 for _, v, *_ in results if v == "CLEAN")
    print(
        f"  Summary: HEAVY={heavy}  LIGHT={light}  CLEAN={clean}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
