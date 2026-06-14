#!/usr/bin/env python3
"""Design Digest — turn a spec note into an architecture/build digest.

Plain-file pipeline that borrows the _docuverse *directory* pattern
(no tumbler addresses, no links.jsonl, no paths.json):

    _design/designs/ASN-NNNN/design.md     (the digest, updated in place)
    _design/reviews/ASN-NNNN/review-K.md   (sequenced reviews)

All Lampson-primed (one persona throughout). Per-note independent.
Commits after each stage so the history reads produce → review → revise.

Convergence by stochastic quiescence (mirrors the battle-tested note
pipeline): review → revise until CONVERGE_N consecutive reviews return
`VERDICT: CONVERGED` — i.e. only sharpenings remain, no material defect.
A CONVERGED review applies no revise (nothing material to change); a
REVISE review resets the streak and is applied. --max-reviews is a hard
cap / backstop, not a target.

    python scripts/design-digest.py --asn 36
    python scripts/design-digest.py --asn 116 --max-reviews 8 --effort max
    python scripts/design-digest.py --asn 116 --no-commit   # skip git
"""

import argparse
import fcntl
import random
import re
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude

NOTE_DIR = ROOT / "_docuverse/documents/1.1/1/note"
CONSULT_DIR = ROOT / "_docuverse/documents/1.1/1/consultation"
PROMPTS = ROOT / "prompts/shared/design-digest"
DESIGN_ROOT = ROOT / "_design"
STOP_FLAG = ROOT / "_workspace" / "design-digest.stop"

# Consecutive CONVERGED reviews required to stop — the stochastic-quiescence
# gate, same value the note pipeline settled on (last_n_reviews_were_clean,
# n=2): one clean draw from a stochastic reviewer is a coin flip, two
# consecutive is meaningful evidence, three buys diminishing returns.
# See docs/design-notes/stochastic-quiescence.md.
CONVERGE_N = 2


def _stop_requested() -> bool:
    """A graceful-shutdown sentinel checked at clean cycle boundaries.
    `touch _workspace/design-digest.stop` (or the runner's --stop) requests
    a drain: the current cycle finishes and commits, then we exit. Nothing
    is left half-applied, so resume picks up exactly where this left off."""
    return STOP_FLAG.exists()


def _note_paths(asn: int):
    label = f"ASN-{asn:04d}"
    notes = [p for p in NOTE_DIR.glob(f"{label}-*.md")
             if ".statements." not in p.name]
    stmts = [p for p in NOTE_DIR.glob(f"{label}-*.statements.md")]
    if not notes:
        sys.exit(f"error: no note found for {label} in {NOTE_DIR}")
    return notes[0], (stmts[0] if stmts else None)


def _highest_review(review_dir: Path) -> int:
    """Largest K among existing review-K.md, or 0 if none."""
    n = 0
    for p in review_dir.glob("review-*.md"):
        m = re.match(r"review-(\d+)\.md$", p.name)
        if m:
            n = max(n, int(m.group(1)))
    return n


def _last_revised(label: str) -> int:
    """Highest review-K whose revise was committed (per git log), else 0.
    A cycle is complete only when its revise lands — so if a review was
    committed but its revise failed (interrupted run), resume redoes that
    cycle's review+revise rather than skipping it and losing the fixes."""
    design = f"_design/designs/{label}/design.md"
    r = subprocess.run(["git", "log", "--format=%s", "--", design],
                       cwd=ROOT, capture_output=True, text=True)
    ks = [int(m.group(1))
          for line in r.stdout.splitlines()
          for m in [re.search(r"apply review-(\d+)", line)] if m]
    return max(ks) if ks else 0


# Tolerant of bold/spacing (`**VERDICT: CONVERGED**`, `VERDICT:CONVERGED`).
_VERDICT_RE = re.compile(r"VERDICT:\s*\**\s*(CONVERGED|REVISE)\b", re.IGNORECASE)


def _is_converged(review_text: str) -> bool:
    """True iff the review's verdict is CONVERGED (reads the LAST verdict line
    if several appear). FAIL-SAFE: a missing or malformed verdict counts as
    NOT converged (→ treated as REVISE), so a parse miss only wastes a pass,
    never falsely converges — the same fail-safe direction the note pipeline's
    review validation takes. (Legacy pre-verdict reviews therefore read as
    REVISE, so existing runs simply continue toward convergence.)"""
    m = _VERDICT_RE.findall(review_text)
    return bool(m) and m[-1].upper() == "CONVERGED"


def _verdict_converged(review_path: Path) -> bool:
    return review_path.exists() and _is_converged(review_path.read_text())


def _trailing_converged(review_dir: Path, upto: int) -> int:
    """Count consecutive CONVERGED reviews ending at review-`upto` (0 if the
    review at `upto` is REVISE/missing) — the convergence streak to resume."""
    streak, k = 0, upto
    while k >= 1 and _verdict_converged(review_dir / f"review-{k}.md"):
        streak += 1
        k -= 1
    return streak


def _resume_state(label: str, review_dir: Path, commit: bool):
    """Return (next_k, clean_streak): the number of the next review to write,
    and the trailing consecutive-CONVERGED count. Recovers an interrupted
    REVISE whose revise never committed — that cycle is redone (next_k stays
    at the unfinished review), mirroring the old _last_revised recovery."""
    highest = _highest_review(review_dir)
    if highest == 0:
        return 1, 0
    if not _verdict_converged(review_dir / f"review-{highest}.md"):
        # Most recent review is REVISE (or legacy/malformed). Did its revise
        # land? If not (interrupted run), redo this cycle from its review.
        applied = _last_revised(label) if commit else highest
        if applied < highest:
            return highest, _trailing_converged(review_dir, highest - 1)
    # Cycle complete: CONVERGED (no revise expected) or REVISE whose revise
    # committed. Continue at the next review.
    return highest + 1, _trailing_converged(review_dir, highest)


def _evidence(asn: int) -> str:
    d = CONSULT_DIR / f"ASN-{asn:04d}"
    if not d.is_dir():
        return ""
    files = sorted(d.glob("**/answer-*-evidence.md"))
    return "\n\n".join(f.read_text().strip() for f in files) if files else ""


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


_COMMIT_LOCK = ROOT / "_workspace" / "design-digest-commit.lock"


@contextmanager
def _commit_lock():
    """Serialize git commits across concurrent per-ASN workers — only one
    `git add`+`commit` touches the index at a time, so parallel workers
    never collide on .git/index.lock. The expensive LLM calls still run
    fully in parallel; only the brief commit serializes."""
    _COMMIT_LOCK.parent.mkdir(parents=True, exist_ok=True)
    fd = open(_COMMIT_LOCK, "w")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        fd.close()


def _commit(paths, message, enabled):
    if not enabled:
        return
    rels = [str(p.relative_to(ROOT)) for p in paths]
    with _commit_lock():
        _git_commit(rels, message)


def _git(args):
    """Run a git command; retry while another process holds .git/index.lock
    (the substrate runner committing concurrently). Returns CompletedProcess
    of the final attempt; raises only on a non-lock error."""
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


def _git_commit(rels, message):
    # `-- <paths>` scopes both the change-check and the commit to these
    # files, so we never sweep up the substrate runner's staged changes;
    # _git() retries through its concurrent index.lock. Skip when nothing new.
    _git(["add", *rels])
    if subprocess.run(["git", "diff", "--cached", "--quiet", "--", *rels],
                      cwd=ROOT).returncode == 0:
        return
    _git(["commit", "-q", "-m", message, "--", *rels])
    print(f"  [commit] {message}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Generate a design digest for an ASN note.")
    ap.add_argument("--asn", type=int, required=True)
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="max", help="low|medium|high|xhigh|max")
    ap.add_argument("--max-reviews", type=int, default=8,
                    help="HARD CAP on total reviews (a backstop); the loop normally "
                         f"stops earlier, at {CONVERGE_N} consecutive CONVERGED "
                         "reviews. Resumes from existing design/reviews; never "
                         "clobbers. Bump it to keep going past a cap that was hit.")
    ap.add_argument("--no-commit", action="store_true", help="skip git commits")
    args = ap.parse_args()
    commit = not args.no_commit

    note_path, stmt_path = _note_paths(args.asn)
    note = note_path.read_text()
    title = note.splitlines()[0].lstrip("# ").strip()
    statements = stmt_path.read_text() if stmt_path else "(no statements sidecar)"
    evidence = _evidence(args.asn) or "(no evidence-channel consultation for this note)"
    label = f"ASN-{args.asn:04d}"

    design_dir = DESIGN_ROOT / "designs" / label
    review_dir = DESIGN_ROOT / "reviews" / label
    design_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    design_md = design_dir / "design.md"

    base = dict(title=title, note=note, statements=statements, evidence=evidence)
    ev_n = 0 if evidence.startswith("(no ") else evidence.count("[evidence]")

    # Resume if a design already exists; otherwise produce a fresh one.
    # Re-running never re-produces and never overwrites prior reviews.
    if design_md.exists():
        digest = design_md.read_text()
        resumed = True
    else:
        digest = None
        resumed = False
    # Resume: next review number + trailing consecutive-CONVERGED streak.
    # _resume_state redoes an interrupted REVISE whose revise never committed.
    next_k, clean_streak = _resume_state(label, review_dir, commit)

    print(f"[design-digest] {label} ({title}) | note {len(note)//1024}KB | "
          f"evidence answers: {ev_n} | model={args.model} effort={args.effort} | "
          f"{'RESUMING' if resumed else 'fresh'} (next review {next_k}, "
          f"{clean_streak}/{CONVERGE_N} clean) → cap {args.max_reviews} | "
          f"commit={commit}", file=sys.stderr)

    if _stop_requested():
        print(f"[design-digest] stop requested — {label} exiting cleanly before "
              f"any work (nothing in flight; safe to resume)", file=sys.stderr)
        return

    if not resumed:
        print("[design-digest] producing...", file=sys.stderr)
        digest = _call("producer", base, args.effort, args.model)
        design_md.write_text(digest.rstrip() + "\n")
        _commit([design_md], f"design({label.lower()}): initial design digest", commit)

    # Convergence gate (stochastic quiescence): review → revise until
    # CONVERGE_N consecutive reviews come back CONVERGED. A CONVERGED review
    # applies no revise (nothing material left); a REVISE review resets the
    # streak and is applied. --max-reviews is the hard backstop.
    while clean_streak < CONVERGE_N and next_k <= args.max_reviews:
        if _stop_requested():
            print(f"[design-digest] stop requested — {label} draining at a clean "
                  f"boundary (next review {next_k}); committed and resume-safe",
                  file=sys.stderr)
            return
        print(f"[design-digest] review {next_k} (cap {args.max_reviews}, "
              f"{clean_streak}/{CONVERGE_N} clean)...", file=sys.stderr)
        review = _call("reviewer", {**base, "digest": digest}, args.effort, args.model)
        review_md = review_dir / f"review-{next_k}.md"
        review_md.write_text(review.rstrip() + "\n")
        _commit([review_md], f"design-review({label.lower()}): review-{next_k}", commit)
        if _is_converged(review):
            clean_streak += 1
            print(f"[design-digest] review {next_k}: CONVERGED "
                  f"({clean_streak}/{CONVERGE_N})", file=sys.stderr)
        else:
            clean_streak = 0
            print(f"[design-digest] applying review-{next_k}...", file=sys.stderr)
            digest = _call("reviser", {**base, "digest": digest, "review": review},
                           args.effort, args.model)
            design_md.write_text(digest.rstrip() + "\n")
            _commit([design_md], f"design-revise({label.lower()}): apply review-{next_k}",
                    commit)
        next_k += 1

    if clean_streak >= CONVERGE_N:
        print(f"[design-digest] CONVERGED — {CONVERGE_N} consecutive clean reviews. "
              f"{design_md.relative_to(ROOT)}", file=sys.stderr)
    else:
        print(f"[design-digest] hit review cap {args.max_reviews} without convergence "
              f"(still finding material defects — bump --max-reviews to continue). "
              f"{design_md.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
