"""Shared utilities for pipeline scripts — extracted from duplicated definitions."""

import json
import os
import re
import subprocess
import sys
import time
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import (
    WORKSPACE, NOTE_DIR, USAGE_LOG,
    CLAIM_REVIEWS_DIR, NOTE_REVIEWS_DIR,
    CLAIM_CONVERGENCE_DIR, CLAIM_DIR,
    CONSULTATIONS_DIR, MANIFESTS_DIR, EXAMPLES_DIR,
    CLAIM_FINDINGS_DIR, NOTE_FINDINGS_DIR,
    CITATION_RESOLVE_DIR, SIGNATURE_RESOLVE_DIR,
    RATIONALE_DIR, DOCUVERSE_LOG,
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


from lib.backend.schema import ATTRIBUTE_SUFFIXES as _ATTR_SUFFIXES


def _is_claim_md(name):
    return (not name.startswith("_")
            and name.endswith(".md")
            and not name.endswith(_ATTR_SUFFIXES))


def build_label_index(claim_dir):
    """Return {label: filename_stem} for an ASN's claims.

    The filename stem is the label in the post-yaml architecture, so
    this is an identity map keyed by every claim md in the directory.
    """
    return {
        p.stem: p.stem
        for p in Path(claim_dir).glob("*.md")
        if _is_claim_md(p.name)
    }


def load_claim_metadata(claim_dir, label=None):
    """Load substrate-sourced metadata for one or all claims.

    Returns a dict (or {label: dict}) with keys:
    - label   : filename stem
    - name    : first line of <stem>.name.md (substrate name link's doc)
    - summary : full content of <stem>.description.md (legacy alias —
                callers historically read this from yaml.summary; the
                substrate equivalent is the description link)
    - type    : the contract.<kind> classifier on the claim's md path

    All fields are optional; absent ones simply don't appear in the dict.
    """
    claim_dir = Path(claim_dir)

    def _read_sidecar_first_line(stem, kind):
        doc = claim_dir / f"{stem}.{kind}.md"
        if not doc.exists():
            return None
        content = doc.read_text().strip()
        if not content:
            return None
        return content.split("\n", 1)[0].strip() or None

    def _read_sidecar_full(stem, kind):
        doc = claim_dir / f"{stem}.{kind}.md"
        if not doc.exists():
            return None
        content = doc.read_text().strip()
        return content or None

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from lib.backend.store import Store
    from lib.protocols.febe.session import Session
    from lib.predicates import current_contract_kind
    from lib.shared.paths import LATTICE

    lattice = Path(LATTICE).resolve()

    def _build(session, stem):
        result = {"label": stem}
        name = _read_sidecar_first_line(stem, "name")
        if name:
            result["name"] = name
        desc = _read_sidecar_full(stem, "description")
        if desc:
            result["summary"] = desc
        md_rel = str(
            (claim_dir / f"{stem}.md").resolve().relative_to(lattice)
        )
        addr = session.get_addr_for_path(md_rel)
        if addr is not None:
            kind = current_contract_kind(session, addr)
            if kind:
                result["type"] = kind
        return result

    with Store(LATTICE) as store:
        session = Session(store)
        if label is not None:
            if not (claim_dir / f"{label}.md").exists():
                return None
            return _build(session, label)
        return {
            p.stem: _build(session, p.stem)
            for p in sorted(claim_dir.glob("*.md"))
            if _is_claim_md(p.name)
        }


def aggregate_signature(claim_dir):
    """Concatenate per-claim signature sidecars into a single markdown
    block suitable for the `{{signature}}` substitution in claim
    convergence's contract-review and validate-contracts prompts.

    A claim's signature is the set of non-logical symbols (constants,
    function symbols, relation symbols) the claim introduces — formal
    logic's precise term for what's recorded in the sidecar.

    Reads `<label>.signature.md` sidecars under `claim_dir`. Each
    sidecar contains markdown bullets identifying the symbols
    introduced by that claim. The aggregator renders one section per
    claim that has a signature sidecar; claims without signatures
    contribute nothing.

    Returns "(no signature)" when no signature sidecars exist.
    """
    claim_dir = Path(claim_dir)
    if not claim_dir.exists():
        return "(no signature)"
    parts = []
    for f in sorted(claim_dir.glob("*.signature.md")):
        stem = f.name.removesuffix(".signature.md")
        body = f.read_text().strip()
        if not body:
            continue
        parts.append(f"### {stem}\n\n{body}")
    return "\n\n".join(parts) if parts else "(no signature)"


def read_file(path):
    """Read file, return '' on FileNotFoundError."""
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return ""


def parse_frontmatter(text):
    """Parse `---\\n<yaml>\\n---\\n<body>` markdown frontmatter.

    Returns (frontmatter_dict, body_str). If the text doesn't start with
    `---`, returns ({}, text) — treats the whole thing as body. Used for
    inquiry/campaign descriptor docs.
    """
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text
    rest = text.split("---\n", 2)
    if len(rest) < 3:
        return {}, text
    _, fm_text, body = rest
    fm = yaml.safe_load(fm_text) or {}
    if not isinstance(fm, dict):
        return {}, text
    return fm, body.lstrip("\n")


def write_frontmatter(fm, body=""):
    """Format `---\\n<yaml>\\n---\\n<body>` text. Inverse of parse_frontmatter."""
    fm_text = yaml.safe_dump(
        fm, default_flow_style=False, sort_keys=False, allow_unicode=True,
    )
    if body and not body.endswith("\n"):
        body = body + "\n"
    return f"---\n{fm_text}---\n\n{body}"


def read_doc_frontmatter(path):
    """Read frontmatter dict from a markdown doc. Returns {} on missing
    file or malformed frontmatter."""
    text = read_file(path)
    fm, _ = parse_frontmatter(text)
    return fm


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
    d = asns_dir or NOTE_DIR
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
            for line in result.stderr.strip().split("\n")[:5]:
                print(f"    stderr: {line}", file=sys.stderr)
        if result.stdout:
            for line in result.stdout.strip().split("\n")[:5]:
                print(f"    stdout: {line[:300]}", file=sys.stderr)
        return "", elapsed

    try:
        data = json.loads(result.stdout)
        if data.get("is_error"):
            print(f"  FAILED (is_error in JSON, {elapsed:.0f}s)", file=sys.stderr)
            print(f"    api_error_status: {data.get('api_error_status')}", file=sys.stderr)
            print(f"    result: {str(data.get('result', ''))[:300]}", file=sys.stderr)
            return "", elapsed
        text = data.get("result", "")
        return text, elapsed
    except (json.JSONDecodeError, KeyError):
        return result.stdout.strip(), elapsed


def strip_code_fence(text):
    """Strip leading/trailing ``` code fences from an LLM response.

    Handles opening ``` on its own line (with optional language tag) and
    closing ``` either on its own line or appended to the last line.
    """
    text = text.strip()
    if text.startswith("```"):
        nl = text.find("\n")
        if nl == -1:
            return ""
        text = text[nl + 1:]
    if text.endswith("```"):
        text = text[:-3].rstrip()
    return text


def git_head_sha(cwd=None):
    """Return the current HEAD SHA. cwd defaults to WORKSPACE."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(cwd or WORKSPACE), capture_output=True, text=True,
    )
    return result.stdout.strip()


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
    """Concatenate the source-note structural sections + per-claim files
    for read-only whole-ASN consumption.

    Returns assembled text (structural sections first, then claim bodies).
    Used by cross-cutting scripts that need the whole-ASN view.
    """
    from lib.shared.paths import (
        CLAIM_CONVERGENCE_DIR, CLAIM_DIR, CLAIM_DERIVATION_DIR,
    )

    cc_dir = CLAIM_CONVERGENCE_DIR / asn_label
    structural_dir = CLAIM_DERIVATION_DIR / asn_label / "structural"
    docs_dir = CLAIM_DIR / asn_label

    parts = []

    # Structural sections (preamble, worked example, etc.) — sections of
    # the source note that contain no claims. Produced by transclude as
    # workspace artifacts.
    if structural_dir.exists():
        for f in sorted(structural_dir.glob("*.md")):
            parts.append(f.read_text().strip())
    # Legacy fallback: pre-D2 lattices kept structural files alongside
    # the convergence loop's caches under claim-convergence/<asn>/_*.md.
    elif cc_dir.exists():
        for f in sorted(cc_dir.glob("_*.md")):
            parts.append(f.read_text().strip())

    # Claim body files live in the substrate document store.
    if docs_dir.exists():
        for f in sorted(docs_dir.glob("*.md")):
            if f.name.startswith("_"):
                continue
            if f.name.endswith(_ATTR_SUFFIXES):
                continue
            parts.append(f.read_text().strip())

    return "\n\n---\n\n".join(parts) if parts else ""


def load_claim_sections(claim_dir):
    """Load per-claim md files into a {stem: content} dict.

    Label = filename stem in the post-yaml architecture, so a single
    key per claim is sufficient.
    """
    claim_dir = Path(claim_dir)
    sections = {}
    for f in sorted(claim_dir.glob("*.md")):
        if not _is_claim_md(f.name):
            continue
        sections[f.stem] = f.read_text()
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
        NOTE_DIR / f"{label}-*",
        CLAIM_REVIEWS_DIR / label,
        NOTE_REVIEWS_DIR / label,
        CLAIM_CONVERGENCE_DIR / label,
        CLAIM_DIR / label,
        CONSULTATIONS_DIR / label,
        MANIFESTS_DIR / label,
        EXAMPLES_DIR / label,
        CLAIM_FINDINGS_DIR / label,
        NOTE_FINDINGS_DIR / label,
        CITATION_RESOLVE_DIR / label,
        SIGNATURE_RESOLVE_DIR / label,
        RATIONALE_DIR / label,
        DOCUVERSE_LOG,
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


def step_commit_asn(asn_id, hint="", *, max_attempts=3, backoff_seconds=(5, 15)):
    """Stage and commit only files belonging to a specific ASN.

    Stages files matching the ASN's known directory patterns, then runs
    commit.py for the commit message. For concurrent safety — two ASN
    pipelines won't include each other's changes.

    Retries the commit-script subprocess up to `max_attempts` times when
    it exits non-zero. Most failures are transient (LLM API rate limit,
    network blip during message generation). Sleeps `backoff_seconds[i]`
    between attempts; iterates with the last value if attempts exceed
    the tuple's length.

    The substrate writes that preceded this call have already happened —
    if the commit can't land at all, those writes leave substrate ahead
    of git until a later commit picks up the staged-but-uncommitted
    files. Retry is the cheap defense against that drift.
    """
    label = f"ASN-{int(asn_id):04d}"
    if not stage_asn_files(label):
        print(f"  [COMMIT] No changes for {label}", file=sys.stderr)
        return False

    commit_script = WORKSPACE / "scripts" / "commit.py"
    cmd = [sys.executable, str(commit_script)]
    if hint:
        cmd.append(hint)

    last_result = None
    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            wait = backoff_seconds[min(attempt - 2, len(backoff_seconds) - 1)]
            print(f"  [COMMIT] retry {attempt}/{max_attempts} after {wait}s...",
                  file=sys.stderr)
            time.sleep(wait)

        last_result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(WORKSPACE),
        )
        if last_result.returncode == 0:
            break
        print(f"  [COMMIT] attempt {attempt}/{max_attempts} failed",
              file=sys.stderr)
        if last_result.stderr:
            for line in last_result.stderr.strip().split("\n")[:3]:
                print(f"    {line}", file=sys.stderr)

    if last_result is None or last_result.returncode != 0:
        print(f"  [COMMIT] FAILED after {max_attempts} attempts — "
              f"changes left staged for next commit", file=sys.stderr)
        return False

    if last_result.stderr:
        for line in last_result.stderr.strip().split("\n"):
            print(f"  {line}", file=sys.stderr)

    if last_result.stdout.strip():
        print(f"  {last_result.stdout.strip()}", file=sys.stderr)
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
    consult_script = WORKSPACE / "scripts" / "lib" / "consultation" / "evidence" / "gather_evidence.py"
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


