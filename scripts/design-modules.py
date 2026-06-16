#!/usr/bin/env python3
"""Design Modules — derive the engine's module decomposition from the design corpus.

Phase A of the build-out: read every converged Design Digest and produce a
single HIGH-LEVEL module manifest — what the modules ARE (responsibility,
source ASNs, dependencies, key components, seams), not their full internal
design. The output is the module-DAG that the per-module fill-in loops then
build out.

Plain-file pipeline, same shape as design-digest.py (no tumblers, no
links.jsonl). One converging document, not per-ASN:

    _design/modules/modules.md            (the manifest, updated in place)
    _design/modules/reviews/review-K.md   (sequenced reviews)

Convergence by stochastic quiescence: review -> revise until CONVERGE_N
consecutive reviews return `VERDICT: CONVERGED`. A CONVERGED review applies
no revise; a REVISE review resets the streak and is applied. --max-reviews
is a hard backstop, not a target.

    python scripts/design-modules.py
    python scripts/design-modules.py --max-reviews 10 --effort max
    python scripts/design-modules.py --no-commit
"""

import argparse
import random
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude

DESIGNS_DIR = ROOT / "_design" / "designs"
PROMPTS = ROOT / "prompts/shared/design-modules"
OUT_DIR = ROOT / "_design" / "modules"
MODULES_MD = OUT_DIR / "modules.md"
REVIEW_DIR = OUT_DIR / "reviews"
STOP_FLAG = ROOT / "_workspace" / "design-modules.stop"

# Consecutive CONVERGED reviews required to stop — the stochastic-quiescence
# gate (same value the note + design-digest pipelines settled on, n=2).
CONVERGE_N = 2


def _stop_requested() -> bool:
    return STOP_FLAG.exists()


def _corpus() -> tuple[str, int]:
    """All converged design digests, concatenated with ASN headers, sorted by
    ASN. Returns (blob, count). This is the producer/reviewer evidence: you
    cannot partition into modules without seeing the whole corpus at once."""
    parts, n = [], 0
    for d in sorted(DESIGNS_DIR.glob("ASN-*/design.md")):
        label = d.parent.name
        parts.append(f"# ===== {label} =====\n\n{d.read_text().strip()}")
        n += 1
    if not n:
        sys.exit(f"error: no design digests found under {DESIGNS_DIR}")
    return "\n\n".join(parts), n


# --- convergence helpers (mirror design-digest.py) ---------------------------
_VERDICT_RE = re.compile(r"VERDICT:\s*\**\s*(CONVERGED|REVISE)\b", re.IGNORECASE)


def _is_converged(review_text: str) -> bool:
    """True iff the LAST verdict line is CONVERGED. FAIL-SAFE: missing/malformed
    verdict reads as NOT converged (treated as REVISE), so a parse miss only
    wastes a pass, never falsely converges."""
    m = _VERDICT_RE.findall(review_text)
    return bool(m) and m[-1].upper() == "CONVERGED"


def _verdict_converged(p: Path) -> bool:
    return p.exists() and _is_converged(p.read_text())


def _highest_review() -> int:
    n = 0
    for p in REVIEW_DIR.glob("review-*.md"):
        m = re.match(r"review-(\d+)\.md$", p.name)
        if m:
            n = max(n, int(m.group(1)))
    return n


def _trailing_converged(upto: int) -> int:
    streak, k = 0, upto
    while k >= 1 and _verdict_converged(REVIEW_DIR / f"review-{k}.md"):
        streak += 1
        k -= 1
    return streak


def _last_revised(commit: bool, highest: int) -> int:
    """Highest review-K whose revise was committed (per git log on modules.md),
    else 0 — so an interrupted REVISE whose revise never landed is redone."""
    if not commit:
        return highest
    r = subprocess.run(["git", "log", "--format=%s", "--",
                        str(MODULES_MD.relative_to(ROOT))],
                       cwd=ROOT, capture_output=True, text=True)
    ks = [int(m.group(1))
          for line in r.stdout.splitlines()
          for m in [re.search(r"apply review-(\d+)", line)] if m]
    return max(ks) if ks else 0


def _resume_state(commit: bool) -> tuple[int, int]:
    """(next_k, clean_streak): next review number + trailing CONVERGED streak.
    Redoes an interrupted REVISE whose revise never committed."""
    highest = _highest_review()
    if highest == 0:
        return 1, 0
    if not _verdict_converged(REVIEW_DIR / f"review-{highest}.md"):
        if _last_revised(commit, highest) < highest:
            return highest, _trailing_converged(highest - 1)
    return highest + 1, _trailing_converged(highest)


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
                  f"({last}) — retrying in {wait}s "
                  f"(work so far is committed; safe to resume)", file=sys.stderr)
            time.sleep(wait)
    sys.exit(f"error: {prompt_name} failed after {retries} attempts — {last}. "
             f"Re-run to resume from the last committed stage.")


def _git(args):
    """git with retry through a concurrent index.lock (the note runner may be
    committing in parallel)."""
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
        description="Derive the engine module decomposition from the design corpus.")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="max", help="low|medium|high|xhigh|max")
    ap.add_argument("--max-reviews", type=int, default=10,
                    help="HARD CAP on total reviews (backstop); the loop normally "
                         f"stops earlier, at {CONVERGE_N} consecutive CONVERGED reviews. "
                         "Resumes from existing manifest/reviews; never clobbers.")
    ap.add_argument("--no-commit", action="store_true", help="skip git commits")
    args = ap.parse_args()
    commit = not args.no_commit

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    designs, n_designs = _corpus()
    base = dict(designs=designs)

    if MODULES_MD.exists():
        manifest = MODULES_MD.read_text()
        resumed = True
    else:
        manifest = None
        resumed = False
    next_k, clean_streak = _resume_state(commit)

    print(f"[design-modules] {n_designs} design digests | corpus {len(designs)//1024}KB | "
          f"model={args.model} effort={args.effort} | "
          f"{'RESUMING' if resumed else 'fresh'} (next review {next_k}, "
          f"{clean_streak}/{CONVERGE_N} clean) → cap {args.max_reviews} | "
          f"commit={commit}", file=sys.stderr)

    if _stop_requested():
        print("[design-modules] stop requested — exiting before work "
              "(nothing in flight; resume-safe)", file=sys.stderr)
        return

    if not resumed:
        print("[design-modules] producing module decomposition...", file=sys.stderr)
        manifest = _call("producer", base, args.effort, args.model)
        MODULES_MD.write_text(manifest.rstrip() + "\n")
        _commit([MODULES_MD], "modules: initial module decomposition", commit)

    while clean_streak < CONVERGE_N and next_k <= args.max_reviews:
        if _stop_requested():
            print(f"[design-modules] stop requested — draining at clean boundary "
                  f"(next review {next_k}); committed and resume-safe", file=sys.stderr)
            return
        print(f"[design-modules] review {next_k} (cap {args.max_reviews}, "
              f"{clean_streak}/{CONVERGE_N} clean)...", file=sys.stderr)
        review = _call("reviewer", {**base, "modules": manifest}, args.effort, args.model)
        review_md = REVIEW_DIR / f"review-{next_k}.md"
        review_md.write_text(review.rstrip() + "\n")
        _commit([review_md], f"modules-review: review-{next_k}", commit)
        if _is_converged(review):
            clean_streak += 1
            print(f"[design-modules] review {next_k}: CONVERGED "
                  f"({clean_streak}/{CONVERGE_N})", file=sys.stderr)
        else:
            clean_streak = 0
            print(f"[design-modules] applying review-{next_k}...", file=sys.stderr)
            manifest = _call("reviser", {**base, "modules": manifest, "review": review},
                             args.effort, args.model)
            MODULES_MD.write_text(manifest.rstrip() + "\n")
            _commit([MODULES_MD], f"modules-revise: apply review-{next_k}", commit)
        next_k += 1

    if clean_streak >= CONVERGE_N:
        print(f"[design-modules] CONVERGED — {CONVERGE_N} consecutive clean reviews. "
              f"{MODULES_MD.relative_to(ROOT)}", file=sys.stderr)
    else:
        print(f"[design-modules] hit review cap {args.max_reviews} without convergence "
              f"(bump --max-reviews to continue). {MODULES_MD.relative_to(ROOT)}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
