#!/usr/bin/env python3
"""Design Digest — turn a spec note into an architecture/build digest.

Plain-file pipeline that borrows the _docuverse *directory* pattern
(no tumbler addresses, no links.jsonl, no paths.json):

    _design/designs/ASN-NNNN/design.md     (the digest, updated in place)
    _design/reviews/ASN-NNNN/review-K.md   (sequenced reviews)

All Lampson-primed (one persona throughout). Per-note independent.
Commits after each stage so the history reads produce → review → revise.

    python scripts/design-digest.py --asn 36
    python scripts/design-digest.py --asn 116 --max-cycles 5 --effort max
    python scripts/design-digest.py --asn 116 --no-commit   # skip git

Run standalone (not alongside the substrate runner — both commit).
"""

import argparse
import fcntl
import re
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude

NOTE_DIR = ROOT / "_docuverse/documents/1.1/1/note"
CONSULT_DIR = ROOT / "_docuverse/documents/1.1/1/consultation"
PROMPTS = ROOT / "prompts/shared/design-digest"
DESIGN_ROOT = ROOT / "_design"


def _note_paths(asn: int):
    label = f"ASN-{asn:04d}"
    notes = [p for p in NOTE_DIR.glob(f"{label}-*.md")
             if ".statements." not in p.name]
    stmts = [p for p in NOTE_DIR.glob(f"{label}-*.statements.md")]
    if not notes:
        sys.exit(f"error: no note found for {label} in {NOTE_DIR}")
    return notes[0], (stmts[0] if stmts else None)


def _highest_review(review_dir: Path) -> int:
    """Largest K among existing review-K.md, or 0 if none — for resume."""
    n = 0
    for p in review_dir.glob("review-*.md"):
        m = re.match(r"review-(\d+)\.md$", p.name)
        if m:
            n = max(n, int(m.group(1)))
    return n


def _evidence(asn: int) -> str:
    d = CONSULT_DIR / f"ASN-{asn:04d}"
    if not d.is_dir():
        return ""
    files = sorted(d.glob("**/answer-*-evidence.md"))
    return "\n\n".join(f.read_text().strip() for f in files) if files else ""


def _call(prompt_name: str, subs: dict, effort: str, model: str) -> str:
    tmpl = (PROMPTS / f"{prompt_name}.md").read_text()
    for k, v in subs.items():
        tmpl = tmpl.replace("{{" + k + "}}", v)
    r = invoke_claude(tmpl, model=model, effort=effort, output_format="json")
    if not r.ok or not r.text.strip():
        sys.exit(f"error: {prompt_name} returned empty/failed "
                 f"(ok={r.ok}, {len(r.text)} chars)")
    print(f"  [{prompt_name}] [{r.elapsed:.0f}s] "
          f"in:{r.usage['input_tokens']} out:{r.usage['output_tokens']} "
          f"${r.cost:.4f}", file=sys.stderr)
    return r.text.strip()


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


def _git_commit(rels, message):
    subprocess.run(["git", "add", *rels], cwd=ROOT, check=True)
    # Scope BOTH the change-check and the commit to these paths with
    # `-- <paths>`, so the design pipeline can never sweep up another
    # committer's staged files (e.g. the substrate runner committing
    # links.jsonl concurrently) — `git commit -- <paths>` ignores the rest
    # of the index. Skip when these paths have nothing new vs HEAD.
    if subprocess.run(["git", "diff", "--cached", "--quiet", "--", *rels],
                      cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "commit", "-q", "-m", message, "--", *rels],
                   cwd=ROOT, check=True)
    print(f"  [commit] {message}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Generate a design digest for an ASN note.")
    ap.add_argument("--asn", type=int, required=True)
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="max", help="low|medium|high|xhigh|max")
    ap.add_argument("--max-reviews", type=int, default=2,
                    help="total review cap. Re-run later with a HIGHER value to "
                         "add more reviews — it resumes from the existing design "
                         "and reviews, never clobbering them. Early-exit on SHIP.")
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
    done = _highest_review(review_dir)

    print(f"[design-digest] {label} ({title}) | note {len(note)//1024}KB | "
          f"evidence answers: {ev_n} | model={args.model} effort={args.effort} | "
          f"{'RESUMING' if resumed else 'fresh'} (have {done} review(s)) → "
          f"max-reviews={args.max_reviews} | commit={commit}", file=sys.stderr)

    if not resumed:
        print("[design-digest] producing...", file=sys.stderr)
        digest = _call("producer", base, args.effort, args.model)
        design_md.write_text(digest.rstrip() + "\n")
        _commit([design_md], f"design({label.lower()}): initial design digest", commit)

    if done >= args.max_reviews:
        print(f"[design-digest] already at {done} review(s) >= --max-reviews "
              f"{args.max_reviews}. Bump --max-reviews to add more. Nothing to do.",
              file=sys.stderr)
        return

    for k in range(done + 1, args.max_reviews + 1):
        print(f"[design-digest] review {k}/{args.max_reviews}...", file=sys.stderr)
        review = _call("reviewer", {**base, "digest": digest}, args.effort, args.model)
        m = re.search(r"^VERDICT:\s*(\w+)", review, re.MULTILINE)
        verdict = m.group(1).upper() if m else "SHIP"
        review_md = review_dir / f"review-{k}.md"
        review_md.write_text(review.rstrip() + "\n")
        _commit([review_md], f"design-review({label.lower()}): review-{k} — {verdict}", commit)
        if verdict == "SHIP":
            print(f"[design-digest] SHIP at review {k} — done", file=sys.stderr)
            break
        print(f"[design-digest] REVISE — applying review-{k}...", file=sys.stderr)
        digest = _call("reviser", {**base, "digest": digest, "review": review},
                       args.effort, args.model)
        design_md.write_text(digest.rstrip() + "\n")
        _commit([design_md], f"design-revise({label.lower()}): apply review-{k}", commit)
    else:
        print(f"[design-digest] reached --max-reviews ({args.max_reviews}) without SHIP",
              file=sys.stderr)

    print(f"[design-digest] wrote {design_md.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
