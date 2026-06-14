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
import re
import subprocess
import sys
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


def _commit(paths, message, enabled):
    if not enabled:
        return
    rels = [str(p.relative_to(ROOT)) for p in paths]
    subprocess.run(["git", "add", *rels], cwd=ROOT, check=True)
    # nothing staged (e.g. identical re-write) → skip the commit
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=ROOT, check=True)
    print(f"  [commit] {message}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Generate a design digest for an ASN note.")
    ap.add_argument("--asn", type=int, required=True)
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="max", help="low|medium|high|xhigh|max")
    ap.add_argument("--max-cycles", type=int, default=3,
                    help="max review/revise cycles (early-exit on SHIP)")
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
    print(f"[design-digest] {label} ({title}) | note {len(note)//1024}KB | "
          f"evidence answers: {ev_n} | model={args.model} effort={args.effort} "
          f"max-cycles={args.max_cycles} commit={commit}", file=sys.stderr)

    print("[design-digest] producing...", file=sys.stderr)
    digest = _call("producer", base, args.effort, args.model)
    design_md.write_text(digest.rstrip() + "\n")
    _commit([design_md], f"design({label.lower()}): initial design digest", commit)

    for k in range(1, args.max_cycles + 1):
        print(f"[design-digest] review cycle {k}/{args.max_cycles}...", file=sys.stderr)
        review = _call("reviewer", {**base, "digest": digest}, args.effort, args.model)
        m = re.search(r"^VERDICT:\s*(\w+)", review, re.MULTILINE)
        verdict = m.group(1).upper() if m else "SHIP"
        review_md = review_dir / f"review-{k}.md"
        review_md.write_text(review.rstrip() + "\n")
        _commit([review_md], f"design-review({label.lower()}): review-{k} — {verdict}", commit)
        if verdict == "SHIP":
            print(f"[design-digest] SHIP at cycle {k} — done", file=sys.stderr)
            break
        print(f"[design-digest] REVISE — applying review-{k}...", file=sys.stderr)
        digest = _call("reviser", {**base, "digest": digest, "review": review},
                       args.effort, args.model)
        design_md.write_text(digest.rstrip() + "\n")
        _commit([design_md], f"design-revise({label.lower()}): apply review-{k}", commit)
    else:
        print(f"[design-digest] hit max-cycles ({args.max_cycles}) without SHIP",
              file=sys.stderr)

    print(f"[design-digest] wrote {design_md.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
