#!/usr/bin/env python3
"""
Absorb an extension ASN back into its base and update the source.

Reads the extension's project model to find:
  - extends: the base/parent ASN
  - source: the ASN that originally derived these claims (optional)

Pipeline:
  1. Integrate extension claims into base reasoning doc (Claude agent)
  2. Review/revise the integration
  3. Re-export the base
  4. Update source ASN citations (Claude agent, if source field set)
  5. Clean up extension artifacts

Usage:
    python scripts/note-absorb.py 57
    python scripts/note-absorb.py 57 --dry-run
"""

import re
import subprocess
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import (WORKSPACE, NOTE_DIR, MANIFESTS_DIR,
                   REVIEWS_DIR, LATTICE_PROMPTS, prompt_path,
                   load_state, note_yaml, claim_statements)
from lib.shared.common import find_asn, log_usage, read_file
from lib.shared.git_ops import step_commit
from lib.shared.invoke_claude import invoke_claude, invoke_claude_agent


ABSORB_BASE_TEMPLATE = prompt_path("discovery/absorb/merge-extension.md")
ABSORB_REVIEW_TEMPLATE = prompt_path("discovery/absorb/review.md")
ABSORB_REVISE_TEMPLATE = prompt_path("discovery/absorb/revise.md")
ABSORB_SOURCE_TEMPLATE = prompt_path("discovery/absorb/update-citations-in-source.md")


def parse_extension_labels(ext_content):
    """Extract claim labels from the extension ASN's registry."""
    labels = []
    in_table = False
    for line in ext_content.splitlines():
        lower = line.lower()
        if "statement registry" in lower or "claims introduced" in lower:
            in_table = False
            continue
        if line.startswith("| ") and ("Label" in line or "label" in line):
            in_table = True
            continue
        if in_table and re.match(r"\|[-\s|]+\|", line):
            continue
        if in_table and line.startswith("|"):
            parts = [c.strip() for c in line.split("|")]
            if len(parts) >= 3 and parts[1]:
                status = parts[-2] if len(parts) >= 5 else parts[-1]
                if "cited" not in status.lower():
                    for sub in parts[1].split(","):
                        sub = sub.strip()
                        if sub:
                            labels.append(sub)
        elif in_table and not line.startswith("|") and line.strip():
            break
    return labels


def validate(ext_num):
    """Validate the extension ASN. Returns (base_num, source_num, ext_path)."""
    ext_label = f"ASN-{ext_num:04d}"

    state = load_state(ext_num)
    if not state:
        print(f"  [ERROR] {ext_label} has no state file (extends/source)",
              file=sys.stderr)
        sys.exit(1)

    base_num = state.get("extends")
    if base_num is None:
        print(f"  [ERROR] {ext_label} is not an extension ASN "
              f"(no extends field in state.yaml)", file=sys.stderr)
        sys.exit(1)

    source_num = state.get("source")

    # Extension reasoning doc exists
    ext_path, _ = find_asn(str(ext_num))
    if ext_path is None:
        print(f"  [ERROR] {ext_label} reasoning doc not found",
              file=sys.stderr)
        sys.exit(1)

    # Base reasoning doc exists
    base_path, _ = find_asn(str(base_num))
    if base_path is None:
        print(f"  [ERROR] Base ASN-{int(base_num):04d} reasoning doc "
              f"not found", file=sys.stderr)
        sys.exit(1)

    return base_num, source_num, ext_path, base_path


def step_integrate(ext_num, base_num, ext_path, base_path, model, effort):
    """Step 1: Claude agent integrates extension claims into base."""
    ext_label = f"ASN-{ext_num:04d}"
    base_label = f"ASN-{int(base_num):04d}"

    ext_content = ext_path.read_text()
    date = time.strftime("%Y-%m-%d")

    template = read_file(ABSORB_BASE_TEMPLATE)
    if not template:
        print("  [ERROR] Absorb base prompt template not found",
              file=sys.stderr)
        return False

    prompt = (template
              .replace("{{ext_content}}", ext_content)
              .replace("{{base_path}}", str(base_path))
              .replace("{{date}}", date))

    print(f"  [INTEGRATE] {ext_label} claims into {base_label}",
          file=sys.stderr)

    data, elapsed = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Edit,Grep",
        max_turns=20,
    )

    if data is None:
        print(f"  [ERROR] Integration failed", file=sys.stderr)
        return False

    log_usage("absorb-integrate", elapsed, ext=ext_num, base=base_num)
    print(f"  [INTEGRATED] {base_label} updated", file=sys.stderr)
    return True


def step_integration_review(base_num, base_path, claim_labels,
                            model, effort):
    """Step 2a: Targeted integration review (not generic review).

    Writes review to the lattice's discovery/review/ASN-NNNN/ directory for traceability.
    """
    from lib.shared.paths import VOCABULARY, REVIEWS_DIR, next_review_number
    from lib.shared.foundation import load_foundation_for_note
    from lib.shared.campaign import resolve_campaign

    base_label = f"ASN-{int(base_num):04d}"
    base_content = base_path.read_text()
    vocabulary = read_file(resolve_campaign(base_num).vocabulary_path)
    foundation = load_foundation_for_note(base_path, base_num)

    template = read_file(ABSORB_REVIEW_TEMPLATE)
    if not template:
        print("  [ERROR] Integration review prompt not found",
              file=sys.stderr)
        return None

    prompt = (template
              .replace("{{asn_content}}", base_content)
              .replace("{{claim_labels}}", ", ".join(claim_labels))
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{foundation_statements}}", foundation))

    print(f"  [REVIEW] Integration review of {base_label}...",
          file=sys.stderr)

    text, elapsed = invoke_claude(
        prompt, model=model, effort=effort)

    if not text:
        print(f"  [WARN] Integration review produced no output",
              file=sys.stderr)
        return None

    log_usage("absorb-review", elapsed, base=base_num)

    # Write review to file
    review_dir = REVIEWS_DIR / base_label
    review_dir.mkdir(parents=True, exist_ok=True)
    review_num = next_review_number(base_label, kind="note")
    review_path = review_dir / f"review-{review_num}.md"
    review_path.write_text(text + "\n")
    print(f"  [WROTE] {review_path.relative_to(WORKSPACE)}",
          file=sys.stderr)

    # Check verdict
    if "VERDICT: CONVERGED" in text:
        print(f"  [CONVERGED] Integration is clean", file=sys.stderr)
        return "CONVERGED"

    print(f"  [REVISE] Integration issues found", file=sys.stderr)
    return text


def step_integration_revise(base_num, base_path, claim_labels,
                            review_text, model, effort):
    """Step 2b: Fix integration issues found by review."""
    from lib.shared.paths import VOCABULARY
    from lib.shared.foundation import load_foundation_for_note
    from lib.shared.campaign import resolve_campaign

    base_label = f"ASN-{int(base_num):04d}"
    vocabulary = read_file(resolve_campaign(base_num).vocabulary_path)
    foundation = load_foundation_for_note(base_path, base_num)

    template = read_file(ABSORB_REVISE_TEMPLATE)
    if not template:
        print("  [ERROR] Integration revise prompt not found",
              file=sys.stderr)
        return False

    prompt = (template
              .replace("{{vocabulary}}", vocabulary)
              .replace("{{foundation_statements}}", foundation)
              .replace("{{base_path}}", str(base_path))
              .replace("{{claim_labels}}", ", ".join(claim_labels))
              .replace("{{review_content}}", review_text))

    print(f"  [REVISE] Fixing integration issues in {base_label}...",
          file=sys.stderr)

    data, elapsed = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Edit,Grep",
        max_turns=20,
    )

    if data is None:
        print(f"  [WARN] Integration revise failed", file=sys.stderr)
        return False

    log_usage("absorb-revise", elapsed, base=base_num)
    return True


def step_review_revise(base_num, base_path, claim_labels,
                       max_cycles, model, effort):
    """Step 2: Integration review/revise loop."""
    for cycle in range(1, max_cycles + 1):
        print(f"\n  --- Integration cycle {cycle}/{max_cycles} ---",
              file=sys.stderr)

        result = step_integration_review(base_num, base_path,
                                         claim_labels, model, effort)

        if result is None:
            print(f"  [WARN] Review failed, continuing", file=sys.stderr)
            return False

        if result == "CONVERGED":
            return True

        # Revise
        ok = step_integration_revise(base_num, base_path, claim_labels,
                                     result, model, effort)
        if not ok:
            print(f"  [WARN] Revise failed at cycle {cycle}",
                  file=sys.stderr)
            return False

        step_commit(f"absorb(asn): integration revise cycle {cycle} "
                    f"for ASN-{int(base_num):04d}")

    print(f"  [WARN] Did not converge after {max_cycles} cycles",
          file=sys.stderr)
    return False


def step_export(base_num):
    """Step 3: Re-export the base ASN."""
    print(f"  [EXPORT] Re-exporting ASN-{int(base_num):04d}...",
          file=sys.stderr)

    cmd = [sys.executable,
           str(WORKSPACE / "scripts" / "normalize.py"),
           str(base_num)]
    result = subprocess.run(cmd, capture_output=False, text=True,
                            cwd=str(WORKSPACE))

    if result.returncode != 0:
        print(f"  [WARN] Export failed", file=sys.stderr)
        return False
    return True


def step_update_source(ext_num, source_num, base_num, ext_path,
                       model, effort):
    """Step 4: Update source ASN to cite instead of derive."""
    ext_label = f"ASN-{ext_num:04d}"
    base_label = f"ASN-{int(base_num):04d}"
    source_label = f"ASN-{int(source_num):04d}"

    source_path, _ = find_asn(str(source_num))
    if source_path is None:
        print(f"  [WARN] Source {source_label} not found, skipping",
              file=sys.stderr)
        return False

    ext_content = ext_path.read_text()
    claim_labels = parse_extension_labels(ext_content)

    if not claim_labels:
        print(f"  [WARN] No introduced claims found in {ext_label}",
              file=sys.stderr)
        return False

    template = read_file(ABSORB_SOURCE_TEMPLATE)
    if not template:
        print("  [ERROR] Absorb source prompt template not found",
              file=sys.stderr)
        return False

    prompt = (template
              .replace("{{ext_label}}", ext_label)
              .replace("{{source_label}}", source_label)
              .replace("{{base_label}}", base_label)
              .replace("{{ext_content}}", ext_content)
              .replace("{{claim_labels}}", ", ".join(claim_labels))
              .replace("{{source_path}}", str(source_path)))

    print(f"  [UPDATE] {source_label} — citing from {base_label}",
          file=sys.stderr)

    data, elapsed = invoke_claude_agent(
        prompt,
        model=model,
        effort=effort,
        tools="Read,Edit,Grep",
        max_turns=20,
    )

    if data is None:
        print(f"  [WARN] Source update failed", file=sys.stderr)
        return False

    log_usage("absorb-source", elapsed, ext=ext_num, source=source_num,
              base=base_num)
    print(f"  [UPDATED] {source_label}", file=sys.stderr)
    return True


def step_cleanup(ext_num):
    """Step 5: Remove extension's project model and export file."""
    ext_label = f"ASN-{ext_num:04d}"

    yaml_path = note_yaml(ext_num)
    if yaml_path.exists():
        yaml_path.unlink()
        print(f"  [REMOVED] {yaml_path.relative_to(WORKSPACE)}",
              file=sys.stderr)

    export_path = claim_statements(ext_num)
    if export_path.exists():
        export_path.unlink()
        print(f"  [REMOVED] {export_path.relative_to(WORKSPACE)}",
              file=sys.stderr)

    # Reasoning doc kept as trace artifact
    # Review dir kept as trace artifact
