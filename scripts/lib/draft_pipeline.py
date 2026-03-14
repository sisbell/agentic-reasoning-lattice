#!/usr/bin/env python3
"""
ASN pipeline — questions → consult → discover → commit.

Orchestrates ASN production by calling step scripts:
  1. Questions: decompose inquiry into sub-questions (preview only)
  2. Consult: run all expert consultations (includes question generation)
  3. Discover: synthesize consultation answers into a formal ASN
  4. Commit: commit vault changes

Specify a step to run up to and including that step:
    python scripts/draft.py --inquiries 4 questions    # preview sub-questions
    python scripts/draft.py --inquiries 4 consult      # questions + consultations
    python scripts/draft.py --inquiries 4 discover     # consult + discover
    python scripts/draft.py --inquiries 4              # full pipeline (all steps)
    python scripts/draft.py                            # all inquiries, full pipeline

Resume from a specific step (skip earlier steps):
    python scripts/draft.py --inquiries 4 --resume discover  # skip consult
    python scripts/draft.py --inquiries 4 --resume commit    # just commit
"""

import argparse
import json
import os
import subprocess
import sys
import time
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import WORKSPACE, ASNS_DIR, USAGE_LOG, PROJECT_MODEL_DIR, load_manifest

CONSULT_SCRIPT = WORKSPACE / "scripts" / "lib" / "draft_consult.py"
DISCOVER_SCRIPT = WORKSPACE / "scripts" / "lib" / "draft_discover.py"
COMMIT_PROMPT = WORKSPACE / "scripts" / "prompts" / "commit.md"

COMMIT_MODEL = "claude-sonnet-4-6"

STEPS = ["questions", "consult", "discover", "commit"]


def read_file(path):
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def load_prompt(path):
    """Load prompt template file."""
    content = read_file(path)
    if not content:
        print(f"  [ERROR] Prompt not found: {path}", file=sys.stderr)
        sys.exit(1)
    return content


def load_inquiries():
    """Load all ASN definitions from project model directory."""
    import re
    inquiries = []
    for path in sorted(PROJECT_MODEL_DIR.glob("ASN-*.yaml")):
        m = re.match(r"ASN-(\d+)", path.stem)
        if not m:
            continue
        asn_id = int(m.group(1))
        manifest = load_manifest(asn_id)
        if not manifest:
            continue
        inquiry = manifest.get("inquiry", {})
        if not inquiry.get("question"):
            continue
        inquiries.append({
            "id": asn_id,
            "title": manifest.get("title", ""),
            "area": "",
            "question": inquiry.get("question", ""),
            "out_of_scope": manifest.get("out_of_scope", ""),
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


def step_commit(hint=""):
    """Commit vault changes. Returns True if committed."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "vault/"],
        capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if not result.stdout.strip():
        print(f"  [COMMIT] nothing to commit")
        return True

    skill_body = load_prompt(COMMIT_PROMPT)
    prompt = f"""{skill_body}

## Context

{hint}

Check for changes in vault/, read the diffs, and commit with a descriptive message.
"""

    cmd = [
        "claude", "-p",
        "--model", COMMIT_MODEL,
        "--output-format", "json",
        "--max-turns", "8",
        "--allowedTools", "Bash,Read",
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env["CLAUDE_CODE_EFFORT_LEVEL"] = "high"

    print(f"  [COMMIT] reading diff, generating message...")
    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(WORKSPACE),
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  [COMMIT] failed ({elapsed:.0f}s) — changes left unstaged")
        return False

    print(f"  [COMMIT] done ({elapsed:.0f}s)")
    return True


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
        return step_questions(inquiry)

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
        step_commit(f"ASN-{asn_number:04d} {title}")

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

    ASNS_DIR.mkdir(parents=True, exist_ok=True)

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
