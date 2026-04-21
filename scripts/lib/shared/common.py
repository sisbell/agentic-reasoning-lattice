"""Shared utilities for pipeline scripts — extracted from duplicated definitions."""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, NOTES_DIR, USAGE_LOG,
    REVIEWS_DIR, BLUEPRINTS_DIR, FORMALIZATION_DIR,
    CONSULTATIONS_DIR, MANIFESTS_DIR, EXAMPLES_DIR,
)


# Custom YAML dumper — uses block scalars (|) for multiline strings
class BlockDumper(yaml.Dumper):
    pass

def _block_str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)

BlockDumper.add_representer(str, _block_str_representer)


def dump_yaml(data, path):
    """Write YAML with block scalars for multiline strings."""
    with open(path, "w") as f:
        yaml.dump(data, f, Dumper=BlockDumper, default_flow_style=False,
                  allow_unicode=True, sort_keys=False, width=120)


def build_label_index(claim_dir):
    """Scan YAML files in a directory, return {label: filename_stem} dict."""
    index = {}
    for yf in Path(claim_dir).glob("*.yaml"):
        with open(yf) as f:
            data = yaml.safe_load(f)
        if data and "label" in data:
            index[data["label"]] = yf.stem
    return index


def load_claim_metadata(claim_dir, label=None):
    """Load YAML metadata for one or all claims.

    If label is given, returns single dict (or None if not found).
    If label is None, returns {label: dict} for all claims.
    """
    claim_dir = Path(claim_dir)
    if label is not None:
        index = build_label_index(claim_dir)
        stem = index.get(label)
        if stem is None:
            return None
        yf = claim_dir / f"{stem}.yaml"
        with open(yf) as f:
            return yaml.safe_load(f)

    result = {}
    for yf in sorted(claim_dir.glob("*.yaml")):
        with open(yf) as f:
            data = yaml.safe_load(f)
        if data and "label" in data:
            result[data["label"]] = data
    return result


def aggregate_vocabulary(claim_dir):
    """Read vocabulary field from all claim YAMLs, return formatted markdown string.

    Aggregates all vocabulary entries across all claims into a single
    string suitable for passing to LLM prompts. Sorted alphabetically,
    deduplicated by symbol.
    """
    claim_dir = Path(claim_dir)
    seen = {}  # symbol → meaning (dedup)

    for yf in sorted(claim_dir.glob("*.yaml")):
        with open(yf) as f:
            data = yaml.safe_load(f)
        if not data:
            continue
        for entry in data.get("vocabulary", []) or []:
            if isinstance(entry, dict) and "symbol" in entry and "meaning" in entry:
                sym = entry["symbol"]
                if sym not in seen:
                    seen[sym] = entry["meaning"]

    if not seen:
        return "(no vocabulary)"

    lines = []
    for sym in sorted(seen.keys()):
        lines.append(f"- **{sym}** — {seen[sym]}")
    return "\n".join(lines)


def read_file(path):
    """Read file, return '' on FileNotFoundError."""
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def concat_md_files(directory):
    """Concatenate all .md files under a directory (recursive),
    each headed by filename stem.
    """
    return "\n\n".join(
        f"### {f.stem}\n{f.read_text()}"
        for f in sorted(Path(directory).rglob("*.md"))
    )




def find_asn(asn_id, asns_dir=None):
    """Find ASN by number. Accepts 9, 09, 0009, ASN-0009, or full path.

    Returns (path, label).
    """
    if isinstance(asn_id, (str, Path)):
        path = Path(asn_id)
        if path.exists():
            label = re.match(r"(ASN-\d+)", path.stem)
            return path, label.group(1) if label else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = f"ASN-{int(num):04d}"
    d = asns_dir or NOTES_DIR
    matches = sorted(d.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


MODEL_FLAGS = {
    "opus": "claude-opus-4-7",
    "sonnet": "claude-sonnet-4-6",
}


def invoke_claude(prompt, *, model="opus", effort="max", tools=None):
    """Call claude --print (single-turn, no tools by default). Returns (text, elapsed)."""
    model_flag = MODEL_FLAGS.get(model, model)

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
        return text, elapsed
    except (json.JSONDecodeError, KeyError):
        return result.stdout.strip(), elapsed


def invoke_claude_agent(prompt, *, model="opus", effort="max",
                        tools="Read,Write,Bash", max_turns=12, cwd=None):
    """Call claude -p (agent mode). Returns (json_data, elapsed)."""
    model_flag = MODEL_FLAGS.get(model, model)

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


def parallel_llm_calls(items, worker_fn, max_workers=10):
    """Run LLM calls in parallel over a list of items.

    worker_fn(item) → (label, result) — called in thread pool.
    Returns list of (label, result) in original item order.
    Prints progress with thread-safe locking.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading

    print_lock = threading.Lock()
    results = {}  # index → (label, result)

    def _wrapped(idx, item):
        label, result = worker_fn(item)
        with print_lock:
            print(f"    {label}...", file=sys.stderr)
        return idx, label, result

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(_wrapped, i, item): i
            for i, item in enumerate(items)
        }
        for future in as_completed(futures):
            try:
                idx, label, result = future.result()
                results[idx] = (label, result)
            except Exception as e:
                idx = futures[future]
                print(f"    [ERROR] item {idx}: {e}", file=sys.stderr)
                results[idx] = ("?", None)

    # Return in original order
    return [results[i] for i in sorted(results.keys())]


def assemble_readonly(asn_label):
    """Concatenate per-claim files from lattices/xanadu/formalization/ for read-only use.

    Returns assembled text (preamble + structural sections + claims).
    Used by cross-cutting scripts that need the whole-ASN view.
    """
    from lib.shared.paths import FORMALIZATION_DIR

    claim_dir = FORMALIZATION_DIR / asn_label
    if not claim_dir.exists():
        return ""

    parts = []

    # Structural files first
    for f in sorted(claim_dir.glob("_*.md")):
        parts.append(f.read_text().strip())

    # Claim files alphabetically
    for f in sorted(claim_dir.glob("*.md")):
        if not f.name.startswith("_"):
            parts.append(f.read_text().strip())

    return "\n\n---\n\n".join(parts)


def load_claim_sections(claim_dir):
    """Load per-claim files into a dict, indexed by both filename stem
    and original label (from YAML metadata).

    Lookup by either filename stem or label will work.
    """
    claim_dir = Path(claim_dir)
    label_index = build_label_index(claim_dir)
    stem_to_label = {stem: lbl for lbl, stem in label_index.items()}
    sections = {}
    for f in sorted(claim_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        content = f.read_text()
        stem = f.name.replace(".md", "")
        sections[stem] = content
        # Also index by original label if different from stem
        label = stem_to_label.get(stem, stem)
        if label != stem:
            sections[label] = content
    return sections


def extract_claim_sections(asn_text, known_labels=None, truncate=True):
    """Extract the derivation text for each claim.

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
    """Table-driven section extraction using known claim labels.

    For each label, finds the bold header line (any format) and captures
    text up to the next known label or section header.
    """
    # Build label-specific patterns and find their positions
    label_positions = []
    for label in labels:
        # Pattern 1: **LABEL followed by space, (, or * — standard claim header
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


def stage_asn_files(label):
    """Stage git files scoped to a single ASN. Returns True if anything staged.

    `glob.glob` matches both the markdown note file and any directories
    named `ASN-NNNN`; `git add` on a directory stages its contents.
    """
    import glob
    patterns = [
        NOTES_DIR / f"{label}-*",
        REVIEWS_DIR / label,
        BLUEPRINTS_DIR / label,
        FORMALIZATION_DIR / label,
        CONSULTATIONS_DIR / label,
        MANIFESTS_DIR / label,
        EXAMPLES_DIR / label,
    ]
    staged = False
    for p in patterns:
        matches = glob.glob(str(p))
        if matches:
            result = subprocess.run(
                ["git", "add"] + matches,
                capture_output=True, text=True, cwd=str(WORKSPACE),
            )
            if result.returncode == 0:
                staged = True
    return staged


def step_commit_asn(asn_id, hint=""):
    """Stage and commit only files belonging to a specific ASN.

    Stages files matching the ASN's known directory patterns, then
    runs commit.py for the commit message. For concurrent safety —
    two ASN pipelines won't include each other's changes.
    """
    label = f"ASN-{int(asn_id):04d}"
    if not stage_asn_files(label):
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

    Stages all lattices/xanadu/ changes. For ASN-scoped commits, use
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
    """Run gather_evidence.py via subprocess. Returns consultation path or None."""
    consult_script = WORKSPACE / "scripts" / "lib" / "revise" / "gather_evidence.py"
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


