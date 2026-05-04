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
from lib.shared.paths import (
    NOTE_DIR, USAGE_LOG, CLAIM_CONVERGENCE_DIR, CLAIM_DIR,
)


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


def assemble_readonly(asn_label):
    """Concatenate the source-note structural sections + per-claim files
    for read-only whole-ASN consumption.

    Returns assembled text (structural sections first, then claim bodies).
    Used by cross-cutting scripts that need the whole-ASN view.
    """
    from lib.shared.paths import CLAIM_DERIVATION_DIR

    cc_dir = CLAIM_CONVERGENCE_DIR / asn_label
    structural_dir = CLAIM_DERIVATION_DIR / asn_label / "structural"
    docs_dir = CLAIM_DIR / asn_label

    parts = []

    if structural_dir.exists():
        for f in sorted(structural_dir.glob("*.md")):
            parts.append(f.read_text().strip())
    elif cc_dir.exists():
        for f in sorted(cc_dir.glob("_*.md")):
            parts.append(f.read_text().strip())

    if docs_dir.exists():
        for f in sorted(docs_dir.glob("*.md")):
            if f.name.startswith("_"):
                continue
            if f.name.endswith(_ATTR_SUFFIXES):
                continue
            parts.append(f.read_text().strip())

    return "\n\n---\n\n".join(parts) if parts else ""
