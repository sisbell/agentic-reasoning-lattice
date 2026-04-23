"""End-of-cone compress hook.

Strips accumulated meta-commentary bloat from claim files using the
compress prompt at `prompts/shared/formalization/compress.md`. Runs
once per cone at the end of regional-review's loop, compressing only
the files that changed during the cone.

The compress prompt is tested and load-bearing (see commit a2b4d9fb,
which used it to reduce ASN-0034 from 190,940 → 51,326 words). This
module wires it into the pipeline; the prompt itself is unchanged.
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.paths import WORKSPACE, prompt_path
from shared.common import invoke_claude, step_commit_asn


COMPRESS_TEMPLATE_PATH = prompt_path("formalization/compress.md")

# Refuse to write a compressed result that shrinks below this fraction
# of the original. Guards against truncated or malformed LLM responses.
MIN_RATIO = 0.20


def _build_prompt(file_content):
    template = COMPRESS_TEMPLATE_PATH.read_text()
    return f"{template}\n\n{file_content}\n"


def _strip_fence(text):
    """Some models emit a leading/trailing code fence despite instructions;
    strip it so the written content is raw markdown."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Drop first fence line
        lines = lines[1:]
        # Drop trailing fence if present
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text


def compress_file(path):
    """Run the compress prompt on one markdown file.

    Returns True if the file was rewritten (content changed and passed
    length-ratio sanity check); False if unchanged or refused.
    """
    original = path.read_text()
    if not original.strip():
        return False

    prompt = _build_prompt(original)
    print(f"  [COMPRESS] {path.name}...", end="", file=sys.stderr, flush=True)

    output, elapsed = invoke_claude(prompt, model="opus", effort="max")
    print(f" {elapsed:.0f}s", file=sys.stderr)

    if not output:
        print(f"    [compress empty response] skipping", file=sys.stderr)
        return False

    cleaned = _strip_fence(output)
    if not cleaned.endswith("\n"):
        cleaned += "\n"

    if cleaned == original:
        return False

    ratio = len(cleaned) / max(len(original), 1)
    if ratio < MIN_RATIO:
        print(f"    [compress suspicious: {ratio:.0%} of original] "
              f"refusing to write", file=sys.stderr)
        return False

    path.write_text(cleaned)
    print(f"    [compressed] {len(original)} → {len(cleaned)} chars "
          f"({ratio:.0%})", file=sys.stderr)
    return True


def _git_head_sha():
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(WORKSPACE), capture_output=True, text=True,
    )
    return result.stdout.strip()


def _changed_md_files(claim_dir, baseline_sha):
    """Return .md files in claim_dir that changed since baseline_sha."""
    result = subprocess.run(
        ["git", "diff", "--name-only", baseline_sha, "HEAD", "--", str(claim_dir)],
        cwd=str(WORKSPACE), capture_output=True, text=True,
    )
    out = []
    for line in result.stdout.strip().split("\n"):
        if not line or not line.endswith(".md"):
            continue
        path = WORKSPACE / line
        if path.exists() and not path.name.startswith("_"):
            out.append(path)
    return out


def compress_changed_files_since(claim_dir, baseline_sha, asn_num,
                                  apex_label=None, dry_run=False):
    """Compress .md files changed since baseline_sha. Commit once at end.

    Returns number of files actually compressed.
    """
    if dry_run:
        return 0

    files = _changed_md_files(claim_dir, baseline_sha)
    if not files:
        return 0

    print(f"\n  [COMPRESS] post-cone pass on {len(files)} changed file(s)",
          file=sys.stderr)
    compressed = 0
    for path in files:
        try:
            if compress_file(path):
                compressed += 1
        except Exception as e:
            print(f"    [compress error on {path.name}] {e}", file=sys.stderr)
            continue

    if compressed == 0:
        print(f"  [COMPRESS] no files changed by compress pass", file=sys.stderr)
        return 0

    hint = (f"compress(asn): post-cone cleanup on {apex_label} "
            f"({compressed} file{'s' if compressed != 1 else ''})"
            if apex_label else
            f"compress(asn): post-cone cleanup ({compressed} files)")
    step_commit_asn(asn_num, hint=hint)
    return compressed
