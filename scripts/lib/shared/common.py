"""Cross-cutting tiny utilities — file I/O, ASN lookup, telemetry,
and whole-ASN read-only assembly.

Themed helpers live in sibling modules:
- yaml_io        — block-scalar YAML writer
- claim_files    — per-claim md/sidecar reads + label index
- frontmatter    — `---\\n<yaml>\\n---` parse/write
- invoke_claude  — Claude CLI invocations + parallel batch
- git_ops        — staging, commit, HEAD lookup
"""

import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.backend.schema import ATTRIBUTE_SUFFIXES as _ATTR_SUFFIXES
from lib.shared.paths import NOTE_DIR, USAGE_LOG, CLAIM_DIR


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
    """Find a labeled note by number. Accepts 9, 09, 0009, `<prefix>-0009`,
    or a full path.

    Returns (path, label).
    """
    from lib.lattice.labels import format_label, label_pattern
    if isinstance(asn_id, (str, Path)):
        path = Path(asn_id)
        if path.exists():
            m = label_pattern().match(path.stem)
            return path, m.group(0) if m else path.stem

    num = re.sub(r"[^0-9]", "", str(asn_id))
    if not num:
        return None, None
    label = format_label(int(num))
    d = asns_dir or NOTE_DIR
    matches = sorted(d.glob(f"{label}-*.md"))
    if matches:
        return matches[0], label
    return None, label


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


def assemble_readonly(asn_label, claim_base_dir=None):
    """Concatenate source-note prose + per-claim files for read-only
    whole-ASN consumption.

    Returns the source note's md (preamble, claims-introduced section,
    worked example, and any other prose) followed by each derived
    claim's body. Used by cross-cutting scripts (full review, Dafny
    translation) that need the whole-ASN view.

    `claim_base_dir` overrides the default lattice CLAIM_DIR — used by
    claim-region agents that emit into a non-primary (node, user)
    partition.

    Earlier versions read structural-section files from a workspace
    dir populated by the deleted transclude phase. After the
    orchestrator-elimination arc, the source note md is the only
    canonical source for that prose.
    """
    from lib.lattice.labels import extract_label_digits
    digits = extract_label_digits(asn_label)
    asn_num = int(digits) if digits else 0
    note_path, _ = find_asn(str(asn_num))
    base = claim_base_dir if claim_base_dir is not None else CLAIM_DIR
    docs_dir = base / asn_label

    parts = []
    if note_path is not None and note_path.exists():
        parts.append(note_path.read_text().strip())

    if docs_dir.exists():
        for f in sorted(docs_dir.glob("*.md")):
            if f.name.startswith("_"):
                continue
            if f.name.endswith(_ATTR_SUFFIXES):
                continue
            parts.append(f.read_text().strip())

    return "\n\n---\n\n".join(parts) if parts else ""
