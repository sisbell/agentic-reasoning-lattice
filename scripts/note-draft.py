#!/usr/bin/env python3
"""
ASN pipeline — questions → consult → discover → commit.

Orchestrates ASN production by calling step scripts:
  1. Questions: decompose inquiry into sub-questions (preview only)
  2. Consult: run all expert consultations (includes question generation)
  3. Discover: synthesize consultation answers into a formal ASN
  4. Commit: commit lattice changes

Specify a step to run up to and including that step:
    python scripts/note-draft.py --inquiries 4 questions    # preview sub-questions
    python scripts/note-draft.py --inquiries 4 consult      # questions + consultations
    python scripts/note-draft.py --inquiries 4 discover     # consult + discover
    python scripts/note-draft.py --inquiries 4              # full pipeline (all steps)
    python scripts/note-draft.py                            # all inquiries, full pipeline

Resume from a specific step (skip earlier steps):
    python scripts/note-draft.py --inquiries 4 --resume discover  # skip consult
    python scripts/note-draft.py --inquiries 4 --resume commit    # just commit
"""

import argparse
import json
import os
import subprocess
import sys
import time
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    WORKSPACE, NOTES_DIR, MANIFESTS_DIR, load_manifest,
)
from lib.note_convergence.steps import step_commit

CONSULT_SCRIPT = WORKSPACE / "scripts" / "lib" / "note_convergence" / "decompose.py"
DISCOVER_SCRIPT = WORKSPACE / "scripts" / "lib" / "note_convergence" / "draft.py"

STEPS = ["questions", "consult", "discover", "commit"]


def load_inquiries():
    """Load all inquiries from the substrate-managed inquiries dir."""
    import re
    from lib.shared.paths import INQUIRIES_DIR
    from lib.shared.common import read_doc_frontmatter
    inquiries = []
    if not INQUIRIES_DIR.exists():
        return inquiries
    for path in sorted(INQUIRIES_DIR.glob("ASN-*.md")):
        m = re.match(r"ASN-(\d+)", path.stem)
        if not m:
            continue
        asn_id = int(m.group(1))
        fm = read_doc_frontmatter(path)
        if not fm or not fm.get("question"):
            continue
        inquiries.append({
            "id": asn_id,
            "title": fm.get("title", ""),
            "area": "",
            "question": fm.get("question", ""),
            "out_of_scope": fm.get("out_of_scope", ""),
        })
    return inquiries


# ─── Steps ────────────────────────────────────────────────────

def step_questions(inquiry):
    """Preview sub-questions via consult-experts.py --dry-run."""
    print(f"  [QUESTIONS] Decomposing inquiry...")

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    cmd = [sys.executable, str(CONSULT_SCRIPT),
           "--inquiry-id", str(inquiry["id"]), "--dry-run"]

    start = time.time()
    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            if line.strip():
                print(f"    {line.strip()}")

    if result.returncode != 0:
        print(f"  [QUESTIONS] FAILED (exit {result.returncode}, {elapsed:.0f}s)")
        return False

    # stdout has the questions
    if result.stdout.strip():
        print(f"\n{result.stdout.strip()}\n")

    print(f"  [QUESTIONS] Done ({elapsed:.0f}s)")
    return True


def step_consult(inquiry):
    """Run consult-experts.py: decompose + consult. Returns True on success."""
    print(f"  [CONSULT] Decomposing inquiry + running consultations...")

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    cmd = [sys.executable, str(CONSULT_SCRIPT),
           "--inquiry-id", str(inquiry["id"])]

    start = time.time()
    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            if line.strip():
                print(f"    {line.strip()}")

    if result.returncode != 0:
        print(f"  [CONSULT] FAILED (exit {result.returncode}, {elapsed:.0f}s)")
        return False

    output_path = result.stdout.strip()
    if output_path and Path(output_path).exists():
        size = Path(output_path).stat().st_size
        print(f"  [CONSULT] Done ({elapsed:.0f}s, {size // 1024}KB)")
        return True

    print(f"  [CONSULT] No output file ({elapsed:.0f}s)")
    return False


def step_discover(inquiry, force=False):
    """Run discover.py. Returns path to ASN file or None."""
    print(f"  [DISCOVER] Running discovery...")

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    cmd = [sys.executable, str(DISCOVER_SCRIPT),
           "--inquiry-id", str(inquiry["id"])]
    if force:
        cmd.append("--force")

    start = time.time()
    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            if line.strip():
                print(f"    {line.strip()}")

    if result.returncode != 0:
        print(f"  [DISCOVER] FAILED (exit {result.returncode}, {elapsed:.0f}s)")
        return None

    asn_path = result.stdout.strip()
    if asn_path and Path(asn_path).exists():
        size = Path(asn_path).stat().st_size
        print(f"  [DISCOVER] Done ({elapsed:.0f}s, {size // 1024}KB)")
        return Path(asn_path)

    print(f"  [DISCOVER] No ASN file ({elapsed:.0f}s)")
    return None


# ─── Pipeline ─────────────────────────────────────────────────

def run_pipeline(inquiry, target_step, resume_from=None, force=False, dry_run=False):
    """Run the pipeline for one inquiry from resume_from to target_step."""
    asn_number = inquiry["id"]
    title = inquiry["title"]
    target_idx = STEPS.index(target_step)
    start_idx = STEPS.index(resume_from) if resume_from else 0

    run_steps = STEPS[start_idx:target_idx + 1]
    steps_label = " → ".join(run_steps)
    print(f"\n{'='*60}")
    print(f"ASN-{asn_number:04d}: {title}")
    print(f"Area: {inquiry['area']}")
    print(f"Steps: {steps_label}")
    print(f"{'='*60}")

    if dry_run:
        print("  [DRY RUN]")
        return True

    # Step: questions (preview only — if this is the target, stop here)
    if "questions" in run_steps and target_step == "questions":
        result = step_questions(inquiry)
        print(f"\n  [NEXT] Run consultation + draft: "
              f"python scripts/note-draft.py --inquiries {asn_number} --resume consult",
              file=sys.stderr)
        return result

    # Step: consult (includes question generation)
    if "consult" in run_steps:
        success = step_consult(inquiry)
        if not success:
            print(f"  [FAILED] Consultation failed — stopping")
            return False

    # Step: discover
    if "discover" in run_steps:
        asn_path = step_discover(inquiry, force=force)
        if asn_path is None:
            return False

    # Step: commit
    if "commit" in run_steps:
        step_commit(f"ASN-{asn_number:04d} {title}", asn_id=asn_number)

    # Hint for next step
    if target_step in ("discover", "commit"):
        print(f"\n  [NEXT] Run review: python scripts/note-review.py {asn_number}",
              file=sys.stderr)
        print(f"  [NEXT] Or review/revise loop: "
              f"python scripts/note-revise.py {asn_number} --converge",
              file=sys.stderr)

    return True


def main():
    parser = argparse.ArgumentParser(description="ASN pipeline runner")
    parser.add_argument("step", nargs="?", default="commit",
                        choices=STEPS,
                        help="Run up to this step (default: commit = all steps)")
    parser.add_argument("--inquiries",
                        help="Comma-separated inquiry IDs (e.g., 1,2,3)")
    parser.add_argument("--resume", choices=STEPS,
                        help="Resume from this step (skip earlier steps)")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing ASN")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would run")
    args = parser.parse_args()

    inquiries = load_inquiries()

    if args.inquiries:
        ids = set(int(x) for x in args.inquiries.split(","))
        inquiries = [i for i in inquiries if i["id"] in ids]

    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    target_idx = STEPS.index(args.step)
    steps_label = " → ".join(STEPS[:target_idx + 1])

    print(f"ASN Pipeline: {len(inquiries)} inquiries")
    print(f"Steps: {steps_label}")

    results = []
    total_start = time.time()

    resume_from = args.resume

    for inquiry in inquiries:
        success = run_pipeline(
            inquiry,
            target_step=args.step,
            resume_from=resume_from,
            force=args.force,
            dry_run=args.dry_run,
        )
        results.append({
            "inquiry": inquiry["title"],
            "asn": inquiry["id"],
            "success": success,
        })

    total_elapsed = time.time() - total_start

    print(f"\n{'='*60}")
    print(f"DONE — {sum(1 for r in results if r['success'])}/{len(results)} succeeded "
          f"({total_elapsed:.0f}s)")
    print(f"{'='*60}")
    for r in results:
        status = "OK" if r["success"] else "FAILED"
        print(f"  ASN-{r['asn']:04d} {r['inquiry']}: {status}")


if __name__ == "__main__":
    main()
