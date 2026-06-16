#!/usr/bin/env python3
"""Module Design — the detailed, build-spec design for ONE module.

Phase B of build-out. Phase A (design-modules.py) produced the module
decomposition — the boundaries, what each module owns, the seams. This loop
fills in ONE module at build-spec altitude: the public interface, the core
data model, the internal design, the invariants, and the resolved cross-note
conflicts — the artifact a builder (or the implementation loop) actually
builds from.

It is driven by `_design/modules/modules.yaml` — the structured module-DAG
derived from the converged decomposition:

    modules:
      M1: { name: Address & Span Algebra, sources: [34, 45, 53], depends_on: [] }
      M3: { name: Namespace, sources: [40, 93, 34, 42, 103], depends_on: [M1, M2] }
    build_order: [M1, M2, M3, ...]

Evidence fed to the loop for module M:
  - the whole decomposition (modules.md) — M's brief + its seams to neighbors;
  - each of M's source notes' design digests (+ claim-statements with
    --with-statements, for extra contract precision);
  - each upstream module's already-converged detailed design — the concrete
    interface M builds against (run modules in build_order so these exist).

Convergence by stochastic quiescence (2 consecutive CONVERGED), resume-safe,
per-stage commits — same shape as design-digest.py / design-modules.py.

    python scripts/module-design.py M1
    python scripts/module-design.py M3 --with-statements
    python scripts/module-design.py 5 --max-reviews 8 --no-commit
"""

import argparse
import random
import re
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude

DESIGNS_DIR = ROOT / "_design" / "designs"
CLAIM_DIR = ROOT / "_docuverse/documents/1.1/1/claim"
NOTE_DIR = ROOT / "_docuverse/documents/1.1/1/note"
MODULES_DIR = ROOT / "_design" / "modules"
MODULES_MD = MODULES_DIR / "modules.md"
MODULES_YAML = MODULES_DIR / "modules.yaml"
OUT_ROOT = ROOT / "_design" / "module-designs"
PROMPTS = ROOT / "prompts/shared/module-design"

CONVERGE_N = 2


def _stop_flag(mid: str) -> Path:
    return ROOT / "_workspace" / f"module-design.{mid}.stop"


# --- module structure --------------------------------------------------------
def _load_modules() -> dict:
    if not MODULES_YAML.exists():
        sys.exit(f"error: {MODULES_YAML.relative_to(ROOT)} not found — derive it "
                 f"from the converged decomposition first (transcribe modules.md).")
    data = yaml.safe_load(MODULES_YAML.read_text()) or {}
    mods = data.get("modules") or {}
    if not mods:
        sys.exit(f"error: no `modules:` map in {MODULES_YAML.relative_to(ROOT)}")
    return mods


def _norm_mid(raw: str, mods: dict) -> str:
    """Accept M3 / m3 / 3 -> the canonical key present in modules.yaml."""
    cand = raw if raw.upper().startswith("M") else f"M{raw}"
    cand = "M" + cand[1:].lstrip("0") if cand[1:].lstrip("0") else cand
    for k in mods:
        if k.upper() == cand.upper():
            return k
    sys.exit(f"error: module {raw!r} not in {sorted(mods)}")


# --- evidence ----------------------------------------------------------------
def _design_digest(asn: int) -> str:
    p = DESIGNS_DIR / f"ASN-{asn:04d}" / "design.md"
    return p.read_text().strip() if p.exists() else f"(no design digest for ASN-{asn:04d})"


def _statements(asn: int) -> str:
    """Best-available formal contract: claim-statements aggregate preferred,
    else the note .statements.md sidecar, else nothing."""
    claim = CLAIM_DIR / f"ASN-{asn:04d}" / "_statements.md"
    if claim.exists():
        return claim.read_text().strip()
    side = list(NOTE_DIR.glob(f"ASN-{asn:04d}-*.statements.md"))
    return side[0].read_text().strip() if side else ""


def _sources_blob(asns: list[int], with_statements: bool) -> str:
    parts = []
    for asn in asns:
        body = f"## ASN-{asn:04d} — design digest\n\n{_design_digest(asn)}"
        if with_statements:
            st = _statements(asn)
            if st:
                body += f"\n\n## ASN-{asn:04d} — formal statements\n\n{st}"
        parts.append(body)
    return "\n\n---\n\n".join(parts)


def _upstream_blob(mids: list[str], mods: dict) -> str:
    """Each upstream module's converged detailed design — the interface this
    module builds against. If one isn't designed yet, fall back to its
    decomposition brief and say so loudly (run in build_order to avoid this)."""
    if not mids:
        return "(this module is a foundation — it depends on no other module.)"
    parts = []
    for mid in mids:
        p = OUT_ROOT / mid / "design.md"
        if p.exists():
            parts.append(f"## {mid} — {mods.get(mid, {}).get('name', '')} "
                         f"(detailed design — build against this interface)\n\n"
                         f"{p.read_text().strip()}")
        else:
            parts.append(f"## {mid} — {mods.get(mid, {}).get('name', '')} "
                         f"(NOT YET DESIGNED — only its decomposition brief is "
                         f"available; treat its seams as provisional)")
    return "\n\n---\n\n".join(parts)


# --- convergence helpers (mirror design-modules.py) --------------------------
_VERDICT_RE = re.compile(r"VERDICT:\s*\**\s*(CONVERGED|REVISE)\b", re.IGNORECASE)


def _is_converged(text: str) -> bool:
    m = _VERDICT_RE.findall(text)
    return bool(m) and m[-1].upper() == "CONVERGED"


def _verdict_converged(p: Path) -> bool:
    return p.exists() and _is_converged(p.read_text())


def _highest_review(review_dir: Path) -> int:
    n = 0
    for p in review_dir.glob("review-*.md"):
        m = re.match(r"review-(\d+)\.md$", p.name)
        if m:
            n = max(n, int(m.group(1)))
    return n


def _trailing_converged(review_dir: Path, upto: int) -> int:
    streak, k = 0, upto
    while k >= 1 and _verdict_converged(review_dir / f"review-{k}.md"):
        streak += 1
        k -= 1
    return streak


def _last_revised(design_md: Path, commit: bool, highest: int) -> int:
    if not commit:
        return highest
    r = subprocess.run(["git", "log", "--format=%s", "--",
                        str(design_md.relative_to(ROOT))],
                       cwd=ROOT, capture_output=True, text=True)
    ks = [int(m.group(1))
          for line in r.stdout.splitlines()
          for m in [re.search(r"apply review-(\d+)", line)] if m]
    return max(ks) if ks else 0


def _resume_state(design_md: Path, review_dir: Path, commit: bool) -> tuple[int, int]:
    highest = _highest_review(review_dir)
    if highest == 0:
        return 1, 0
    if not _verdict_converged(review_dir / f"review-{highest}.md"):
        if _last_revised(design_md, commit, highest) < highest:
            return highest, _trailing_converged(review_dir, highest - 1)
    return highest + 1, _trailing_converged(review_dir, highest)


# --- claude + git ------------------------------------------------------------
def _call(prompt_name: str, subs: dict, effort: str, model: str,
          retries: int = 4) -> str:
    tmpl = (PROMPTS / f"{prompt_name}.md").read_text()
    for k, v in subs.items():
        tmpl = tmpl.replace("{{" + k + "}}", v)
    last = ""
    for attempt in range(1, retries + 1):
        r = invoke_claude(tmpl, model=model, effort=effort, output_format="json")
        if r.ok and r.text.strip():
            print(f"  [{prompt_name}] [{r.elapsed:.0f}s] "
                  f"in:{r.usage['input_tokens']} out:{r.usage['output_tokens']} "
                  f"${r.cost:.4f}", file=sys.stderr)
            return r.text.strip()
        last = f"ok={r.ok}, {len(r.text)} chars"
        if attempt < retries:
            wait = 15 * attempt
            print(f"  [{prompt_name}] attempt {attempt}/{retries} failed "
                  f"({last}) — retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    sys.exit(f"error: {prompt_name} failed after {retries} attempts — {last}. "
             f"Re-run to resume from the last committed stage.")


def _git(args):
    last = None
    for _ in range(40):
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            return r
        last = (r.stderr or "") + (r.stdout or "")
        if "index.lock" in last or "another git process" in last:
            time.sleep(0.3 + random.random() * 0.5)
            continue
        raise RuntimeError(f"git {args[0]} failed: {last.strip()}")
    raise RuntimeError(f"git {args[0]}: gave up on index.lock — {last.strip()}")


def _commit(paths, message, enabled):
    if not enabled:
        return
    rels = [str(p.relative_to(ROOT)) for p in paths]
    _git(["add", *rels])
    if subprocess.run(["git", "diff", "--cached", "--quiet", "--", *rels],
                      cwd=ROOT).returncode == 0:
        return
    _git(["commit", "-q", "-m", message, "--", *rels])
    print(f"  [commit] {message}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(
        description="Detailed build-spec design for one module (Phase B).")
    ap.add_argument("module", help="module id (M3, m3, or 3)")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="max", help="low|medium|high|xhigh|max")
    ap.add_argument("--with-statements", action="store_true",
                    help="also feed each source note's formal claim-statements "
                         "(more precise contracts, much larger context)")
    ap.add_argument("--max-reviews", type=int, default=8)
    ap.add_argument("--no-commit", action="store_true")
    args = ap.parse_args()
    commit = not args.no_commit

    mods = _load_modules()
    mid = _norm_mid(args.module, mods)
    m = mods[mid]
    name = m.get("name", mid)
    sources = m.get("sources", []) or []
    deps = m.get("depends_on", []) or []

    if not MODULES_MD.exists():
        sys.exit(f"error: {MODULES_MD.relative_to(ROOT)} missing (the decomposition).")
    decomposition = MODULES_MD.read_text().strip()
    sources_blob = _sources_blob(sources, args.with_statements)
    upstream_blob = _upstream_blob(deps, mods)

    out_dir = OUT_ROOT / mid
    review_dir = out_dir / "reviews"
    out_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    design_md = out_dir / "design.md"

    base = dict(module_id=mid, module_name=name, decomposition=decomposition,
                sources=sources_blob, upstream=upstream_blob)

    missing_up = [d for d in deps if not (OUT_ROOT / d / "design.md").exists()]
    if design_md.exists():
        design = design_md.read_text()
        resumed = True
    else:
        design = None
        resumed = False
    next_k, clean_streak = _resume_state(design_md, review_dir, commit)

    ev_kb = (len(decomposition) + len(sources_blob) + len(upstream_blob)) // 1024
    print(f"[module-design] {mid} ({name}) | sources {sources} | depends {deps or '—'} | "
          f"evidence ~{ev_kb}KB{' +statements' if args.with_statements else ''} | "
          f"{'RESUMING' if resumed else 'fresh'} (next review {next_k}, "
          f"{clean_streak}/{CONVERGE_N} clean) → cap {args.max_reviews} | "
          f"commit={commit}", file=sys.stderr)
    if missing_up:
        print(f"[module-design] WARNING: upstream {missing_up} not yet designed — "
              f"their seams are provisional. Run in build_order to avoid this.",
              file=sys.stderr)

    if _stop_flag(mid).exists():
        print(f"[module-design] stop requested — {mid} exiting before work.",
              file=sys.stderr)
        return

    if not resumed:
        print(f"[module-design] producing detailed design for {mid}...", file=sys.stderr)
        design = _call("producer", base, args.effort, args.model)
        design_md.write_text(design.rstrip() + "\n")
        _commit([design_md], f"module-design({mid}): initial detailed design", commit)

    while clean_streak < CONVERGE_N and next_k <= args.max_reviews:
        if _stop_flag(mid).exists():
            print(f"[module-design] stop requested — {mid} draining at clean boundary "
                  f"(next review {next_k}).", file=sys.stderr)
            return
        print(f"[module-design] {mid} review {next_k} (cap {args.max_reviews}, "
              f"{clean_streak}/{CONVERGE_N} clean)...", file=sys.stderr)
        review = _call("reviewer", {**base, "design": design}, args.effort, args.model)
        review_md = review_dir / f"review-{next_k}.md"
        review_md.write_text(review.rstrip() + "\n")
        _commit([review_md], f"module-design-review({mid}): review-{next_k}", commit)
        if _is_converged(review):
            clean_streak += 1
            print(f"[module-design] {mid} review {next_k}: CONVERGED "
                  f"({clean_streak}/{CONVERGE_N})", file=sys.stderr)
        else:
            clean_streak = 0
            print(f"[module-design] {mid} applying review-{next_k}...", file=sys.stderr)
            design = _call("reviser", {**base, "design": design, "review": review},
                           args.effort, args.model)
            design_md.write_text(design.rstrip() + "\n")
            _commit([design_md], f"module-design-revise({mid}): apply review-{next_k}",
                    commit)
        next_k += 1

    if clean_streak >= CONVERGE_N:
        print(f"[module-design] {mid} CONVERGED — {CONVERGE_N} consecutive clean. "
              f"{design_md.relative_to(ROOT)}", file=sys.stderr)
    else:
        print(f"[module-design] {mid} hit review cap {args.max_reviews} without "
              f"convergence. {design_md.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
