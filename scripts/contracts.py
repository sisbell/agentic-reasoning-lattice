#!/usr/bin/env python3
"""Derive per-method Design-by-Contract specs for a module, callee-before-caller,
with a produce → validate → revise convergence cycle (mirrors claim refinement).

Inputs per method (the decompose output + the backing sidecar):
  - its UNIT (units_dir/<method>.md: signature + algorithm + invariants) as the context cut,
  - the contracts of the methods it CALLS (already derived this run — composed in so the
    method discharges each callee's precondition; the cross-method alignment check),
  - its BACKING, per the module's backing.yaml:
      mode: transcribe → ASN-0034 has VERIFIED Dafny: the pre/post are a faithful
                         transcription of the Dafny requires/ensures (ASN-0034 is our only Dafny).
      mode: derive     → no Dafny (ASN-0053 span algebra; everything outside M1): derive from
                         the unit and DISCHARGE callee preconditions.

Per method the cycle is:
  produce.md  →  (validate.md [Bertrand Meyer: MATCH | MISMATCH+findings]  →  revise.md)*
  until MATCH or --max-cycles. The buckets (callee-before-caller) come from the decompose's
  _index.yaml call graph ∪ backing.yaml's `calls` (which patch operator edges the structural
  decompose under-counts, e.g. `<` → cmp).

Sources: ONLY _design/ + verification/dafny/. Never vault/.
Output: <out>/<method>.md (one per method; default _design/module-designs/<mid>/contracts).

    python scripts/contract-decompose.py M1 --out _workspace/m1-methods   # 1. decompose first
    python scripts/contracts.py M1 --units _workspace/m1-methods --dry-run # 2. print bucket plan
    python scripts/contracts.py M1 --units _workspace/m1-methods --only sub cmp from_endpoints
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude            # noqa: E402
from lib.shared.topological_sort import topological_levels    # noqa: E402

OUT_ROOT = ROOT / "_design" / "module-designs"
PRODUCE_PROMPT = ROOT / "prompts/shared/contracts/produce.md"
VALIDATE_PROMPT = ROOT / "prompts/shared/contracts/validate.md"
REVISE_PROMPT = ROOT / "prompts/shared/contracts/revise.md"
ALIGN_PROMPT = ROOT / "prompts/shared/contracts/align.md"
DAFNY_DIR = ROOT / "verification" / "dafny" / "ASN-0034"
# Sources: _design/ (designs), verification/dafny/ (proofs), _docuverse/ (substrate: the
# note claims + statements — the richer Dijkstra narrative behind the Dafny / design). Never vault/.
DOCU = ROOT / "_docuverse" / "documents" / "1.1" / "1"


def _claim_body(asn: int, label: str) -> str | None:
    """A single ASN claim's Dijkstra body + formal contract (transcribe-side reference narrative)."""
    p = DOCU / "claim" / f"ASN-{asn:04d}" / f"{label}.md"
    return p.read_text().strip() if p.exists() else None


def _note_statements(asn: int) -> str | None:
    """An ASN note's formal statements (derive-side authoritative backing, e.g. ASN-0053 span algebra)."""
    hits = sorted((DOCU / "note").glob(f"ASN-{asn:04d}-*.statements.md"))
    return hits[0].read_text().strip() if hits else None

_FENCE = re.compile(r"^```[a-zA-Z]*\s*|\s*```$", re.MULTILINE)
_RESULT_RE = re.compile(r"RESULT:\s*(MATCH|MISMATCH)", re.IGNORECASE)
_ALIGN_RESULT_RE = re.compile(r"RESULT:\s*(ALIGNED|MISALIGNED)", re.IGNORECASE)
_REVISE_RE = re.compile(r"(?mi)^\W*REVISE\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+)$")
_INCONSISTENCY_RE = re.compile(r"(?m)^\W*INCONSISTENCY:")


def _formal_section(contract: str) -> str:
    """The §1 Formal Contract block (pre/post/frame/invariant) — the compact cross-method view."""
    m = re.search(r"(?ms)^#+\s*1\.\s*Formal Contract.*?(?=^#+\s*2\.)", contract)
    return m.group(0).strip() if m else contract.strip()


def _norm(m: str) -> str:
    m = m.strip()
    return m.upper() if m.lower().startswith("m") else f"M{m}"


def _fill(tmpl: str, **subs) -> str:
    for k, v in subs.items():
        tmpl = tmpl.replace("{{" + k + "}}", v)
    return tmpl


def _invoke(prompt: str, model: str, effort: str, label: str):
    """One LLM call; strip a leading fence; exit on hard failure (re-run resumes)."""
    r = invoke_claude(prompt, model=model, effort=effort, output_format="json")
    if not (r.ok and r.text.strip()):
        sys.exit(f"error: {label} failed (ok={r.ok}) — re-run to resume")
    text = r.text.strip()
    text = _FENCE.sub("", text) if text.startswith("```") else text
    return text, r


def _backing_blob(method: str, spec: dict) -> str:
    """The authoritative-spec section for produce.md's {{backing}}, with a mode directive."""
    mode = spec.get("mode", "derive")
    if mode == "transcribe":
        files = spec.get("dafny", []) or []
        bodies = []
        for fn in files:
            p = DAFNY_DIR / fn
            if not p.exists():
                print(f"  [contracts] WARNING: backing dafny {fn} missing for {method}", file=sys.stderr)
                continue
            bodies.append(f"### {fn}\n```dafny\n{p.read_text().strip()}\n```")
        joined = "\n\n".join(bodies)
        blob = (
            "## Verified backing — ASN-0034 Dafny (TRANSCRIBE, do not re-derive)\n\n"
            "The following Dafny is machine-verified. Your contract's preconditions and "
            "postconditions MUST be a faithful transcription of these `requires`/`ensures` "
            "clauses into Rust DbC — translate the quantifiers and bounds exactly; do not "
            "weaken, strengthen, or invent. Where an `ensures` is an unbounded quantifier, "
            "render it as a `// spec:` property-test line. Map the Dafny name to the idiomatic "
            f"Rust name of `{method}`.\n\n{joined}"
        )
        # Append the source claim(s) — the Dijkstra narrative + formal contract behind the Dafny.
        # AUTHORITY stays with the Dafny above; the claim is reference for wording/intent only.
        claim_bodies = []
        for lbl in (spec.get("claims") or []):
            body = _claim_body(34, lbl)
            if body:
                claim_bodies.append(f"### Claim {lbl} (ASN-0034)\n\n{body}")
            else:
                print(f"  [contracts] WARNING: claim {lbl} missing for {method}", file=sys.stderr)
        if claim_bodies:
            blob += ("\n\n## Reference narrative — the ASN-0034 claim(s) behind that Dafny "
                     "(context for wording/intent; the Dafny above remains authoritative — do not "
                     "let the prose override a verified `ensures`)\n\n" + "\n\n---\n\n".join(claim_bodies))
        return blob
    # derive mode — no verified Dafny. Authoritative backing = the note's formal statements
    # (_docuverse, e.g. ASN-0053 span algebra), falling back to the design unit if absent.
    asn = spec.get("asn")
    label = f"ASN-{asn:04d}" if asn else "the design"
    stmts = _note_statements(asn) if asn else None
    head = (
        f"## Backing — {label} (DERIVE; no verified Dafny exists for this method)\n\n"
        "There is NO machine-checked backing for this method (the span algebra is unproven). "
        "Derive the contract faithfully from the note's formal statements below (the authoritative "
        "spec) together with the design algorithm/invariants above, and in §3 DISCHARGE each callee's "
        "precondition against the callee's transcribed contract — that cross-check (span op vs the "
        "tumbler contracts it composes) is the point. Flag any `INCONSISTENCY:` where a callee "
        "precondition cannot be cleanly established."
    )
    if stmts:
        return head + f"\n\n## {label} — formal statements (authoritative)\n\n{stmts}"
    if asn:
        print(f"  [contracts] WARNING: no {label} statements in _docuverse — derive from design only",
              file=sys.stderr)
    return head + "\n\n_(No separate statements file; derive from the design above.)_"


def _load(mid: str, units_dir: Path):
    """Assemble the per-method spec from the decompose output + the backing sidecar.

    - units_dir/_index.yaml      → the authoritative method set + intra-module call graph.
    - units_dir/<method>.md      → the self-contained unit, fed as {{design}} (the context cut).
    - <mid>/backing.yaml         → per-method {mode, dafny, asn}; its `calls`, if any, are
                                   UNIONED into _index's (the structural decompose under-counts
                                   operator comparisons like `<` → compare; backing patches them).
    """
    index_p = units_dir / "_index.yaml"
    if not index_p.exists():
        sys.exit(f"error: {index_p.relative_to(ROOT)} missing — run "
                 f"`contract-decompose.py {mid} --out {units_dir.relative_to(ROOT)}` first")
    index = (yaml.safe_load(index_p.read_text()) or {}).get("methods", {}) or {}

    backing_p = OUT_ROOT / mid / "backing.yaml"
    backing = {}
    if backing_p.exists():
        backing = (yaml.safe_load(backing_p.read_text()) or {}).get("methods", {}) or {}

    methods = {}
    for m, info in index.items():
        unit_p = units_dir / f"{m}.md"
        if not unit_p.exists():
            print(f"  [contracts] WARNING: no unit file for {m} — skipping", file=sys.stderr)
            continue
        b = backing.get(m, {})
        calls = sorted(set(info.get("calls") or []) | set(b.get("calls") or []))
        methods[m] = {"unit": unit_p.read_text(), "calls": calls,
                      "mode": b.get("mode", "derive"), "dafny": b.get("dafny", []),
                      "asn": b.get("asn"), "_backed": bool(b)}
    return methods


def _callees_blob(mid: str, calls, derived: dict) -> str:
    names = [c for c in calls if c in derived]
    return "\n\n---\n\n".join(
        f"### Contract of `{mid}::{c}`\n\n{derived[c]}" for c in names
    ) or "_(No intra-module callees — this is a leaf method.)_"


def _run_align(mid, methods, derived, out_dir, args, align_tmpl, revise_tmpl):
    """Module-level cross-method consistency loop (the claim_structural_revise analogue):
    align(all contracts) → REVISE <method> findings → revise each → re-align, until ALIGNED."""
    graph = "\n".join(f"{m} → {', '.join(methods[m]['calls']) or '(leaf)'}"
                      for m in sorted(derived))
    for rnd in range(1, args.align_cycles + 1):
        blob = "\n\n---\n\n".join(f"### `{mid}::{m}`\n\n{_formal_section(derived[m])}"
                                  for m in sorted(derived))
        atext, ar = _invoke(_fill(align_tmpl, module_id=mid, call_graph=graph, contracts=blob),
                            args.model, args.effort, f"align round {rnd}")
        mo = _ALIGN_RESULT_RE.search(atext)
        if mo and mo.group(1).upper() == "ALIGNED":
            print(f"[contracts] align round {rnd}: ALIGNED ✓  ${ar.cost:.4f}", file=sys.stderr)
            return
        fixes = _REVISE_RE.findall(atext)
        fixes = [(m, f) for m, f in fixes if m in methods]
        if not fixes:
            print(f"[contracts] align round {rnd}: MISALIGNED but no actionable REVISE lines — "
                  f"stopping (${ar.cost:.4f})", file=sys.stderr)
            return
        print(f"[contracts] align round {rnd}: MISALIGNED — revising "
              f"{', '.join(m for m, _ in fixes)}  ${ar.cost:.4f}", file=sys.stderr)
        for method, finding in fixes:
            spec = methods[method]
            contract, rr = _invoke(
                _fill(revise_tmpl, module_id=mid, method=method, unit=spec["unit"],
                      backing=_backing_blob(method, spec),
                      callees=_callees_blob(mid, spec["calls"], derived),
                      contract=derived[method],
                      findings=f"CROSS-METHOD ALIGNMENT finding (fix this without breaking the "
                               f"single-method contract):\n- {finding}"),
                args.model, args.effort, f"align-revise {method}")
            (out_dir / f"{method}.md").write_text(contract.rstrip() + "\n")
            derived[method] = contract
            print(f"  [align] revised {method}  ${rr.cost:.4f}", file=sys.stderr)
    print(f"[contracts] align: still MISALIGNED after {args.align_cycles} rounds", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("module", help="module id (M1)")
    ap.add_argument("--units", default=None,
                    help="per-method units dir (default _design/module-designs/<mid>/methods); "
                         "the contract-decompose.py output (_index.yaml + <method>.md)")
    ap.add_argument("--only", nargs="*", help="restrict to these methods (still derives in order)")
    ap.add_argument("--out", default=None,
                    help="output dir (default _design/module-designs/<mid>/contracts); "
                         "use _workspace/... to verify before promoting")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="max", help="contract derivation is a reasoning task → max")
    ap.add_argument("--max-cycles", type=int, default=4,
                    help="produce → (validate → revise)* convergence cap per method (default 4)")
    ap.add_argument("--align", action="store_true",
                    help="after deriving, run the module-level cross-method alignment loop "
                         "(caller↔callee precondition agreement, shared-type invariants, conventions)")
    ap.add_argument("--align-only", action="store_true",
                    help="skip derivation; run the alignment loop over the EXISTING contracts in "
                         "--out (use to re-align after a partial --only re-run changed a method)")
    ap.add_argument("--align-cycles", type=int, default=3,
                    help="align → revise → re-align convergence cap (default 3)")
    ap.add_argument("--dry-run", action="store_true", help="print the bucket plan and exit")
    args = ap.parse_args()

    mid = _norm(args.module)
    units_dir = (ROOT / args.units) if args.units else (OUT_ROOT / mid / "methods")
    methods = _load(mid, units_dir)

    # Buckets over the (index ∪ backing) call edges (callee-before-caller).
    deps = {"claims": {m: {"follows_from": [c for c in s["calls"] if c in methods]}
                       for m, s in methods.items()}}
    levels = [lvl for lvl in topological_levels(deps) if lvl]

    want = set(_norm_methods(args.only)) if args.only else set(methods)

    unbacked = sorted(m for m in want if m in methods and not methods[m]["_backed"])
    if unbacked:
        print(f"[contracts] NOTE: {len(unbacked)} requested method(s) have no backing.yaml entry "
              f"→ defaulting to DERIVE mode (no Dafny transcribe): {', '.join(unbacked)}",
              file=sys.stderr)

    print(f"[contracts] {mid}: {len(methods)} methods, {len(levels)} buckets (units: "
          f"{units_dir.relative_to(ROOT)})", file=sys.stderr)
    for i, lvl in enumerate(levels):
        tagged = [f"{m}[{methods[m]['mode'][0]}]" for m in sorted(lvl)]
        print(f"  bucket {i}: {', '.join(tagged)}", file=sys.stderr)
    if args.dry_run:
        return 0

    out_dir = (ROOT / args.out) if args.out else (OUT_ROOT / mid / "contracts")
    out_dir.mkdir(parents=True, exist_ok=True)
    produce_tmpl = PRODUCE_PROMPT.read_text()
    validate_tmpl = VALIDATE_PROMPT.read_text()
    revise_tmpl = REVISE_PROMPT.read_text()
    align_tmpl = ALIGN_PROMPT.read_text()
    derived: dict[str, str] = {}   # method -> contract text (for callee composition)

    if args.align_only:
        for m in methods:
            p = out_dir / f"{m}.md"
            if p.exists():
                derived[m] = p.read_text()
        if not derived:
            sys.exit(f"error: --align-only but no contracts in {out_dir.relative_to(ROOT)}")
        print(f"[contracts] --align-only: loaded {len(derived)} existing contracts", file=sys.stderr)
        _run_align(mid, methods, derived, out_dir, args, align_tmpl, revise_tmpl)
        return 0

    for i, lvl in enumerate(levels):
        for method in sorted(lvl):
            spec = methods[method]
            # Compose callee contracts already produced this run.
            callee_names = [c for c in spec["calls"] if c in derived]
            callees_blob = _callees_blob(mid, spec["calls"], derived)

            if method not in want:
                # Still load a prior contract if present (so a partial --only run composes).
                prior = out_dir / f"{method}.md"
                if prior.exists():
                    derived[method] = prior.read_text()
                continue

            mode, unit, backing_blob = spec["mode"], spec["unit"], _backing_blob(method, spec)
            base = dict(module_id=mid, method=method, unit=unit,
                        backing=backing_blob, callees=callees_blob)

            # 1. PRODUCE
            print(f"[contracts] bucket {i} · {method} ({mode}, {len(callee_names)} callees): produce...",
                  file=sys.stderr)
            contract, r = _invoke(_fill(produce_tmpl, design=unit, **base),
                                  args.model, args.effort, f"{method} produce")
            spent, status = r.cost, "unvalidated"

            # 2. (VALIDATE → REVISE)* until MATCH or cap (the Meyer cycle, per claim refinement)
            for cycle in range(1, args.max_cycles + 1):
                vtext, vr = _invoke(_fill(validate_tmpl, contract=contract, **base),
                                    args.model, args.effort, f"{method} validate {cycle}")
                spent += vr.cost
                mo = _RESULT_RE.search(vtext)
                matched = bool(mo) and mo.group(1).upper() == "MATCH"
                if matched:
                    status = f"MATCH@cycle{cycle}"
                    break
                findings = vtext[mo.end():].strip() if mo else vtext
                if cycle == args.max_cycles:
                    status = f"MISMATCH after {cycle} cycles"
                    break
                print(f"  [{method}] validate {cycle}: MISMATCH → revise", file=sys.stderr)
                contract, rr = _invoke(_fill(revise_tmpl, contract=contract, findings=findings, **base),
                                       args.model, args.effort, f"{method} revise {cycle}")
                spent += rr.cost

            (out_dir / f"{method}.md").write_text(contract.rstrip() + "\n")
            derived[method] = contract
            inc = bool(_INCONSISTENCY_RE.search(contract))
            print(f"  [{method}] {status}  ${spent:.4f}"
                  f"{'  ⚠ INCONSISTENCY' if inc else ''}", file=sys.stderr)

    print(f"\n[contracts] {mid}: {len(want & set(derived))} contracts → "
          f"{out_dir.relative_to(ROOT)}", file=sys.stderr)

    if args.align:
        print(f"[contracts] {mid}: cross-method alignment pass...", file=sys.stderr)
        _run_align(mid, methods, derived, out_dir, args, align_tmpl, revise_tmpl)
    return 0


def _norm_methods(names):
    return [n.strip() for n in (names or [])]


if __name__ == "__main__":
    raise SystemExit(main())
