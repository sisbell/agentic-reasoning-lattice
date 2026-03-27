"""Shared utilities for pipeline scripts — extracted from duplicated definitions."""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, ASNS_DIR, USAGE_LOG


def read_file(path):
    """Read file, return '' on FileNotFoundError."""
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def find_asn(asn_id, asns_dir=None):
    """Find ASN by number. Accepts 9, 09, 0009, ASN-0009, or full path.

    Returns (path, label).
    """
    path = Path(asn_id)
    if path.exists():
        label = re.match(r"(ASN-\d+)", path.stem)
        return path, label.group(1) if label else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    d = asns_dir or ASNS_DIR
    matches = sorted(d.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


def invoke_claude(prompt, *, model="opus", effort="max", tools=None):
    """Call claude --print (single-turn, no tools by default). Returns (text, elapsed)."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = ["claude", "--print", "--model", model_flag, "--output-format", "json"]
    if tools is not None:
        cmd.extend(["--tools", tools])
    else:
        cmd.extend(["--tools", ""])

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return "", elapsed

    try:
        data = json.loads(result.stdout)
        text = data.get("result", "")
        print(f"  [{elapsed:.0f}s]", file=sys.stderr)
        return text, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s]", file=sys.stderr)
        return result.stdout.strip(), elapsed


def invoke_claude_agent(prompt, *, model="opus", effort="max",
                        tools="Read,Write,Bash", max_turns=12, cwd=None):
    """Call claude -p (agent mode). Returns (json_data, elapsed)."""
    model_flag = {
        "opus": "claude-opus-4-6",
        "sonnet": "claude-sonnet-4-6",
    }.get(model, model)

    cmd = [
        "claude", "-p",
        "--model", model_flag,
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--allowedTools", tools,
    ]

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")
    if effort:
        env["CLAUDE_CODE_EFFORT_LEVEL"] = effort

    start = time.time()
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env,
        cwd=str(cwd or WORKSPACE), timeout=None,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode}, {elapsed:.0f}s)",
              file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, elapsed

    try:
        data = json.loads(result.stdout)
        return data, elapsed
    except (json.JSONDecodeError, KeyError):
        print(f"  [{elapsed:.0f}s] [parse error]", file=sys.stderr)
        return None, elapsed


def log_usage(skill, elapsed, **extra):
    """Append JSONL usage entry to USAGE_LOG."""
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "skill": skill,
            "elapsed_s": round(elapsed, 1),
        }
        entry.update(extra)
        with open(USAGE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass


def extract_property_sections(asn_text, known_labels=None, truncate=True):
    """Extract the derivation text for each property.

    If known_labels is provided, uses label-anchored search (table-driven):
    searches for each label as a bold header start, handling any format.
    Otherwise falls back to generic bold-pattern regex.

    If truncate=False, returns full section text (for assembly).
    If truncate=True (default), caps at 3000 chars (for prose scanning).

    Returns dict of label → derivation text.
    """
    if known_labels:
        return _extract_sections_by_labels(asn_text, known_labels, truncate=truncate)

    sections = {}

    # Fallback: generic pattern matches **LABEL — Name.** or **LABEL (Name).**
    prop_pattern = re.compile(
        r'^\*\*([A-Z][A-Za-z0-9_]*(?:-[A-Za-z0-9]+)*)\s*(?:(?:—|–|-)\s*|\()',
        re.MULTILINE
    )

    matches = list(prop_pattern.finditer(asn_text))

    for i, m in enumerate(matches):
        label = m.group(1).strip("*").strip()
        start = m.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            next_section = re.search(r'^## ', asn_text[start + 1:], re.MULTILINE)
            end = start + 1 + next_section.start() if next_section else len(asn_text)

        text = asn_text[start:end].strip()
        if truncate and len(text) > 3000:
            text = text[:3000] + "\n[...truncated...]"
        sections[label] = text

    return sections


def _extract_sections_by_labels(asn_text, labels, truncate=True):
    """Table-driven section extraction using known property labels.

    For each label, finds the bold header line (any format) and captures
    text up to the next known label or section header.
    """
    # Build label-specific patterns and find their positions
    label_positions = []
    for label in labels:
        # Pattern 1: **LABEL followed by space, (, or * — standard property header
        pattern1 = re.compile(
            r'^\*\*' + re.escape(label) + r'(?:\s|\(|\*)',
            re.MULTILINE
        )
        # Pattern 2: **Definition (LABEL) — definition header
        pattern2 = re.compile(
            r'^\*\*Definition\s*\(' + re.escape(label) + r'\)',
            re.MULTILINE
        )
        m = pattern1.search(asn_text) or pattern2.search(asn_text)
        if m:
            label_positions.append((m.start(), label))

    # Sort by position in document
    label_positions.sort()

    sections = {}
    for i, (start, label) in enumerate(label_positions):
        if i + 1 < len(label_positions):
            end = label_positions[i + 1][0]
        else:
            next_section = re.search(r'^## ', asn_text[start + 1:], re.MULTILINE)
            end = start + 1 + next_section.start() if next_section else len(asn_text)

        text = asn_text[start:end].strip()
        if truncate and len(text) > 3000:
            text = text[:3000] + "\n[...truncated...]"
        sections[label] = text

    return sections


def step_commit_asn(asn_id, hint=""):
    """Stage and commit only files belonging to a specific ASN.

    Stages files matching the ASN's known directory patterns, then
    runs commit.py for the commit message. For concurrent safety —
    two ASN pipelines won't include each other's changes.
    """
    label = f"ASN-{int(asn_id):04d}"
    patterns = [
        f"vault/1-reasoning-docs/{label}-*",
        f"vault/2-review/{label}/",
        f"vault/0-consultations/{label}/",
        f"vault/project-model/{label}/",
        f"vault/6-examples/{label}/",
    ]

    # Stage only this ASN's files
    import glob
    staged = False
    for pattern in patterns:
        matches = glob.glob(str(WORKSPACE / pattern), recursive=True)
        if matches:
            result = subprocess.run(
                ["git", "add"] + matches,
                capture_output=True, text=True, cwd=str(WORKSPACE),
            )
            if result.returncode == 0 and matches:
                staged = True

    # Also stage any directories (git add needs trailing / for dirs)
    for pattern in patterns:
        if pattern.endswith("/"):
            dirpath = WORKSPACE / pattern.rstrip("/")
            if dirpath.exists():
                subprocess.run(
                    ["git", "add", str(dirpath)],
                    capture_output=True, text=True, cwd=str(WORKSPACE),
                )
                staged = True

    if not staged:
        print(f"  [COMMIT] No changes for {label}", file=sys.stderr)
        return False

    # Run commit.py for the message
    commit_script = WORKSPACE / "scripts" / "commit.py"
    cmd = [sys.executable, str(commit_script)]
    if hint:
        cmd.append(hint)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [COMMIT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if result.stdout.strip():
        print(f"  {result.stdout.strip()}", file=sys.stderr)
    return True


def step_commit(hint=""):
    """Run commit.py via subprocess. Returns True if committed.

    Stages all vault/ changes. For ASN-scoped commits, use
    step_commit_asn() instead.
    """
    commit_script = WORKSPACE / "scripts" / "commit.py"
    cmd = [sys.executable, str(commit_script)]
    if hint:
        cmd.append(hint)

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [COMMIT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)
        return False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if result.stdout.strip():
        print(f"  {result.stdout.strip()}", file=sys.stderr)
    return True


def step_consult(asn_id, review_path):
    """Run review_consult.py via subprocess. Returns consultation path or None."""
    consult_script = WORKSPACE / "scripts" / "lib" / "review_consult.py"
    cmd = [sys.executable, str(consult_script), str(asn_id)]

    import re as _re
    review_name = Path(review_path).stem
    m = _re.search(r"(review-\d+)", review_name)
    if m:
        cmd.append(m.group(1))

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )
    if result.returncode != 0:
        print(f"  [CONSULT] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    consultation_path = result.stdout.strip()
    if consultation_path and Path(consultation_path).exists():
        return consultation_path
    return None


def step_revise(asn_id, consultation_path=None):
    """Run review_revise.py via subprocess. Returns (asn_path, converged)."""
    revise_script = WORKSPACE / "scripts" / "lib" / "review_revise.py"
    cmd = [sys.executable, str(revise_script), str(asn_id)]
    if consultation_path:
        cmd.extend(["--consultation", consultation_path])

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
    )

    converged = result.returncode == 2

    if result.returncode not in (0, 2):
        print(f"  [REVISE] FAILED", file=sys.stderr)
        if result.stderr:
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    {line}", file=sys.stderr)
        return None, False

    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    asn_path = result.stdout.strip()
    if asn_path and Path(asn_path).exists():
        return asn_path, converged
    return None, False
