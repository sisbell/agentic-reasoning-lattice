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


def label_to_filename(label):
    """Convert property label to filename: T0(a) → T0a.md, vpos(S, o) → vpos-S-o.md."""
    name = label.replace("(", "").replace(")", "")
    name = name.replace(",", "").replace(" ", "-")
    name = re.sub(r'-+', '-', name).strip("-")
    return name + ".md"


PROPERTY_NAMES_FILE = "_property_names.md"


def load_property_names(prop_dir):
    """Read _property_names.md → {filename_stem: original_label}. Returns {} if missing."""
    path = Path(prop_dir) / PROPERTY_NAMES_FILE
    if not path.exists():
        return {}
    mapping = {}
    for line in path.read_text().split("\n"):
        line = line.strip()
        if not line.startswith("|") or line.startswith("| Filename") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) >= 3 and cells[1] and cells[2]:
            stem = cells[1].replace(".md", "")
            mapping[stem] = cells[2]
    return mapping


def save_property_names(prop_dir, mapping):
    """Write _property_names.md as markdown table, sorted by filename."""
    prop_dir = Path(prop_dir)
    lines = [
        "# Property Names\n",
        "| Filename | Label |",
        "|----------|-------|",
    ]
    for stem in sorted(mapping.keys()):
        lines.append(f"| {stem}.md | {mapping[stem]} |")
    (prop_dir / PROPERTY_NAMES_FILE).write_text("\n".join(lines) + "\n")


def generate_property_names(prop_dir):
    """Regenerate _property_names.md from _table.md in prop_dir.

    Reads labels from the table, applies label_to_filename() to get stems,
    checks each file exists, writes the mapping.
    Returns (mapping, warnings) where warnings is a list of strings.
    """
    prop_dir = Path(prop_dir)
    table_path = prop_dir / "_table.md"
    if not table_path.exists():
        return {}, ["_table.md not found"]

    mapping = {}
    warnings = []
    for line in table_path.read_text().split("\n"):
        line = line.strip()
        if not line.startswith("|") or line.startswith("| Label") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 2 or not cells[1].strip():
            continue
        label = cells[1].strip().strip("`*")
        filename = label_to_filename(label)
        stem = filename.replace(".md", "")
        if (prop_dir / filename).exists():
            mapping[stem] = label
        else:
            warnings.append(f"table label '{label}' → {filename} not found")

    # Check for property files without table entries
    for f in sorted(prop_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        stem = f.name.replace(".md", "")
        if stem not in mapping:
            warnings.append(f"file {f.name} has no table entry")

    save_property_names(prop_dir, mapping)
    return mapping, warnings


def filename_to_label(filename, mapping):
    """Look up filename in mapping, fall back to stem if not found."""
    stem = filename.replace(".md", "") if filename.endswith(".md") else filename
    return mapping.get(stem, stem)


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
        return text, elapsed
    except (json.JSONDecodeError, KeyError):
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
    """Concatenate per-property files from vault/3-formalization/ for read-only use.

    Returns assembled text in table order (preamble, table, properties).
    Used by cross-cutting scripts that need the whole-ASN view.
    """
    from lib.shared.paths import FORMALIZATION_DIR

    prop_dir = FORMALIZATION_DIR / asn_label
    if not prop_dir.exists():
        return ""

    parts = []

    # Structural files first
    for name in ["_preamble.md", "_table.md"]:
        f = prop_dir / name
        if f.exists():
            parts.append(f.read_text().strip())

    # Property files in table label order
    table_path = prop_dir / "_table.md"
    if table_path.exists():
        table_text = table_path.read_text()
        ordered_labels = []
        for line in table_text.split("\n"):
            if (line.strip().startswith("|")
                    and not line.strip().startswith("| Label")
                    and not line.strip().startswith("|---")):
                cells = [c.strip() for c in line.split("|")]
                if len(cells) >= 2 and cells[1].strip():
                    label = cells[1].strip().strip("`*")
                    ordered_labels.append(label)

        for label in ordered_labels:
            filename = label_to_filename(label)
            f = prop_dir / filename
            if f.exists():
                parts.append(f.read_text().strip())
    else:
        # No table — read all property files alphabetically
        for f in sorted(prop_dir.glob("*.md")):
            if not f.name.startswith("_"):
                parts.append(f.read_text().strip())

    return "\n\n---\n\n".join(parts)


def load_property_sections(prop_dir):
    """Load per-property files into a dict, indexed by both filename stem
    and original label (from _property_names.md when available).

    Handles the mismatch between table labels like vpos(S, o) and filenames
    like vpos-S-o.md. Lookup by either form will work.
    """
    prop_dir = Path(prop_dir)
    mapping = load_property_names(prop_dir)
    sections = {}
    for f in sorted(prop_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        content = f.read_text()
        stem = f.name.replace(".md", "")
        sections[stem] = content
        # Also index by original label if different from stem
        label = mapping.get(stem, stem)
        if label != stem:
            sections[label] = content
    # Fallback heuristic for ASNs without _property_names.md:
    # T0a -> also indexed as T0(a)
    if not mapping:
        import re as _re
        for fname in list(sections.keys()):
            m = _re.match(r'^([A-Z]+\d+)([a-z])$', fname)
            if m:
                paren_label = f"{m.group(1)}({m.group(2)})"
                if paren_label not in sections:
                    sections[paren_label] = sections[fname]
    return sections


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
        f"vault/1-reasoning-docs-review/{label}/",
        f"vault/2-blueprints/{label}/",
        f"vault/3-formalization/{label}/",
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


