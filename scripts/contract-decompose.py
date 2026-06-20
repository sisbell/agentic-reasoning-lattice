#!/usr/bin/env python3
"""Decompose a module design into one self-contained unit per public method.

Mirrors the claim pipeline's `claim_decompose`: instead of feeding the whole
design.md into every contract derivation, split it once into per-method units —
each holding only that method's signature + algorithm slice + the invariants it
touches + its intra-module `calls`. Later stages (classify / produce / validate)
read the small unit, not the 300-line design (the context cut), and the `calls`
fix the callee-before-caller order.

Sources: ONLY the design under _design/. Never vault/.

    python scripts/contract-decompose.py M1 --out _workspace/m1-methods
    python scripts/contract-decompose.py M1            # → _design/module-designs/M1/methods/
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude            # noqa: E402

OUT_ROOT = ROOT / "_design" / "module-designs"
PROMPT = ROOT / "prompts/shared/contracts/decompose.md"
_FENCE = re.compile(r"^```[a-zA-Z]*\s*|\s*```$", re.MULTILINE)


def _norm(m: str) -> str:
    m = m.strip()
    return m.upper() if m.lower().startswith("m") else f"M{m}"


def _unit_md(m: dict) -> str:
    """Render one method's YAML entry as a self-contained unit document."""
    label = m["label"]
    sig = (m.get("signature") or "").strip()
    algo = (m.get("algorithm") or "").strip()
    inv = (m.get("invariants") or "").strip()
    calls = m.get("calls") or []
    parts = [f"# Method unit — `{label}`", "", "## Signature", "", f"```rust\n{sig}\n```", "",
             "## Algorithm", "", algo or "_(none beyond the signature)_"]
    if inv:
        parts += ["", "## Invariants", "", inv]
    parts += ["", "## Intra-module calls", "",
              (", ".join(f"`{c}`" for c in calls) if calls else "_(leaf — no same-module callees)_")]
    return "\n".join(parts) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("module", help="module id (M1)")
    ap.add_argument("--out", default=None,
                    help="output dir (default _design/module-designs/<mid>/methods)")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="max", help="faithful extraction across the whole design → max")
    args = ap.parse_args()

    mid = _norm(args.module)
    design_p = OUT_ROOT / mid / "design.md"
    if not design_p.exists():
        sys.exit(f"error: {design_p.relative_to(ROOT)} missing")

    prompt = (PROMPT.read_text()
              .replace("{{module_id}}", mid)
              .replace("{{design}}", design_p.read_text()))

    for attempt in range(1, 4):
        r = invoke_claude(prompt, model=args.model, effort=args.effort, output_format="json")
        if not (r.ok and r.text.strip()):
            print(f"  [decompose] {mid} attempt {attempt}/3 failed (ok={r.ok})", file=sys.stderr)
            continue
        text = _FENCE.sub("", r.text.strip())
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            print(f"  [decompose] {mid} attempt {attempt}: bad YAML ({e})", file=sys.stderr)
            continue
        break
    else:
        sys.exit(f"error: {mid} decompose failed")

    methods = data.get("methods", []) or []
    out_dir = (ROOT / args.out) if args.out else (OUT_ROOT / mid / "methods")
    out_dir.mkdir(parents=True, exist_ok=True)

    index = {"module": mid, "methods": {}}
    for m in methods:
        label = m.get("label")
        if not label:
            continue
        (out_dir / f"{label}.md").write_text(_unit_md(m))
        index["methods"][label] = {"calls": [c for c in (m.get("calls") or [])]}
    (out_dir / "_index.yaml").write_text(yaml.safe_dump(index, sort_keys=True))

    print(f"  [decompose] {mid} [{r.elapsed:.0f}s] {len(index['methods'])} methods "
          f"(in:{r.usage['input_tokens']} out:{r.usage['output_tokens']} ${r.cost:.4f}) "
          f"→ {out_dir.relative_to(ROOT)}", file=sys.stderr)
    for label, info in sorted(index["methods"].items()):
        calls = info["calls"]
        print(f"    {label}{'  → ' + ', '.join(calls) if calls else ''}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
