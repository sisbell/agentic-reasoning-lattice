#!/usr/bin/env python3
"""Build the method-dependency DAG from converged module designs.

A method's contract is composed from the contracts of the methods it calls, so
contract derivation must proceed in dependency order. This extracts the
method-call graph from each converged design (one LLM pass per module — the
calls are explicit in the algorithm sections) and buckets it with the borrowed
`topological_levels`: bucket 0 = leaves (no domain calls), bucket N = methods
that call bucket N-1. Methods in one bucket are independent ⇒ derive in parallel.

The bucketing is `lib/shared/topological_sort.topological_levels` verbatim
(domain-agnostic — takes {label: follows_from}); the only new piece is the
edge extraction. No substrate import: the graph is built in-memory from the
designs and written to _design/method-dag.yaml for inspection.

    python scripts/method-dag.py M2 M3 M4 M5       # M1 appears as leaf callees (it's gold via the oracle)
    python scripts/method-dag.py --all             # every module with a design.md
    python scripts/method-dag.py M5 --effort high
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude
from lib.shared.topological_sort import topological_levels, topological_sort_labels

OUT_ROOT = ROOT / "_design" / "module-designs"
PROMPT = ROOT / "prompts/shared/method-dag/extract.md"
OUT = ROOT / "_design" / "method-dag.yaml"

_FENCE = re.compile(r"^```[a-zA-Z]*\s*|\s*```$", re.MULTILINE)


def extract(mid: str, model: str, effort: str) -> dict | None:
    design = OUT_ROOT / mid / "design.md"
    if not design.exists():
        print(f"[method-dag] {mid}: no design.md — skip", file=sys.stderr)
        return None
    tmpl = PROMPT.read_text().replace("{{module_id}}", mid).replace("{{design}}", design.read_text())
    for attempt in range(1, 4):
        r = invoke_claude(tmpl, model=model, effort=effort, output_format="json")
        if r.ok and r.text.strip():
            text = _FENCE.sub("", r.text.strip())
            try:
                data = yaml.safe_load(text)
            except yaml.YAMLError as e:
                print(f"[method-dag] {mid} attempt {attempt}: bad YAML ({e})", file=sys.stderr)
                continue
            n = len(data.get("methods", []) or [])
            print(f"  [method-dag] {mid} [{r.elapsed:.0f}s] {n} methods "
                  f"(in:{r.usage['input_tokens']} out:{r.usage['output_tokens']} ${r.cost:.4f})",
                  file=sys.stderr)
            return data
        print(f"  [method-dag] {mid} attempt {attempt}/3 failed (ok={r.ok})", file=sys.stderr)
    print(f"[method-dag] {mid}: FAILED", file=sys.stderr)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("modules", nargs="*", help="module ids (M2 M3 ...)")
    ap.add_argument("--all", action="store_true", help="every module with a design.md")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="medium",
                    help="extraction is structural projection — medium is plenty (use max to match house default)")
    args = ap.parse_args()

    if args.all:
        mids = sorted(p.parent.name for p in OUT_ROOT.glob("*/design.md"))
    else:
        mids = [m.upper() if m.lower().startswith("m") else f"M{m}" for m in args.modules]
    if not mids:
        ap.error("give module ids (e.g. M2 M3 M4 M5) or --all")

    edges: dict[str, set[str]] = {}
    for mid in mids:
        data = extract(mid, args.model, args.effort)
        if not data:
            continue
        for m in data.get("methods", []) or []:
            label = m.get("label")
            if not label:
                continue
            edges.setdefault(label, set()).update(m.get("calls", []) or [])

    if not edges:
        sys.exit("error: no edges extracted")

    # Materialize callee-only nodes (e.g. M1::inc referenced but not extracted) as leaves.
    for callees in list(edges.values()):
        for c in callees:
            edges.setdefault(c, set())

    deps_data = {"claims": {lbl: {"follows_from": sorted(c)} for lbl, c in edges.items()}}
    OUT.write_text(yaml.safe_dump(deps_data, sort_keys=True))

    levels = topological_levels(deps_data)
    flat = topological_sort_labels(deps_data)
    total = len(edges)
    width = max((len(l) for l in levels), default=0)
    print(f"\n[method-dag] {total} methods, {len(levels)} buckets, max width {width} "
          f"(derive a bucket in parallel; buckets in order) → {OUT.relative_to(ROOT)}",
          file=sys.stderr)
    for i, lvl in enumerate(levels):
        # show how many are M1 (gold via oracle, skip in derivation) vs to-derive
        m1 = sum(1 for x in lvl if x.startswith("M1::"))
        tag = f"  [{m1} M1/oracle]" if m1 else ""
        print(f"  bucket {i} ({len(lvl)}){tag}: {', '.join(sorted(lvl))}")
    print(f"\n  topo order (flat): {len(flat)} methods", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
