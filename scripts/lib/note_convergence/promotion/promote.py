"""
Promotion step functions — shared by open-questions and out-of-scope orchestrators.

- load_existing_inquiries: read title + question from all note.yaml files
- next_asn_number: find next available ASN number
- parse_promoted: parse LLM promotion output into structured items
- create_note_yaml: write a new ASN project manifest
- load_existing_promotion: read previous promotion report for an ASN
- save_promotion_report: write promotion report
"""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, MANIFESTS_DIR, note_dir


def load_existing_inquiries():
    """Read title + question from all note.yaml files.

    Returns formatted text for injection into the promotion prompt.
    """
    entries = []
    for yaml_path in sorted(MANIFESTS_DIR.glob("ASN-*/note.yaml")):
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except Exception:
            continue
        label = yaml_path.parent.name
        title = data.get("title", "")
        question = data.get("consultations", {}).get("question", "")
        if title:
            entries.append(f"- {label}: {title} — {question}")
    return "\n".join(entries) if entries else "(none)"


def next_asn_number():
    """Find the next available ASN number."""
    max_num = 0
    for d in MANIFESTS_DIR.iterdir():
        if d.is_dir():
            m = re.match(r"ASN-(\d+)", d.name)
            if m:
                num = int(m.group(1))
                if num > max_num:
                    max_num = num
    return max_num + 1


def parse_promoted(text):
    """Parse LLM promotion output into list of promoted items.

    Each item is a dict with keys: title, question, area, nelson, gregory.
    """
    items = []
    in_promoted = False
    current = None

    for line in text.split("\n"):
        stripped = line.strip()

        if stripped.startswith("## Promoted"):
            in_promoted = True
            continue
        if stripped.startswith("## Declined"):
            in_promoted = False
            if current:
                items.append(current)
                current = None
            continue

        if not in_promoted:
            continue

        # New promoted question
        if stripped.startswith("- **"):
            if current:
                items.append(current)
            current = {}
            continue

        if current is None:
            continue

        # Parse metadata lines
        if stripped.startswith("- Title:"):
            current["title"] = stripped[len("- Title:"):].strip()
        elif stripped.startswith("- Question:"):
            current["question"] = stripped[len("- Question:"):].strip()
        elif stripped.startswith("- Area:"):
            current["area"] = stripped[len("- Area:"):].strip()
        elif stripped.startswith("- Nelson:"):
            try:
                current["nelson"] = int(stripped[len("- Nelson:"):].strip())
            except ValueError:
                current["nelson"] = 10
        elif stripped.startswith("- Gregory:"):
            try:
                current["gregory"] = int(stripped[len("- Gregory:"):].strip())
            except ValueError:
                current["gregory"] = 10

    if current:
        items.append(current)

    return items


def create_note_yaml(asn_num, title, question, area, source_asn,
                        nelson=10, gregory=10):
    """Create a new note.yaml for a promoted ASN.

    Returns the path to the created file.
    """
    out_dir = note_dir(asn_num)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "note.yaml"

    content = f"""# ASN-{asn_num:04d} — {title}
title: "{title}"
stage: "inquiry"
topic: "{area}"
covers: ""
out_of_scope: ""
source: "promoted from ASN-{source_asn:04d}"

consultations:
  question: "{question}"
  nelson: {nelson}
  gregory: {gregory}
"""
    out_path.write_text(content)
    print(f"  [CREATED] {out_path.relative_to(WORKSPACE)}", file=sys.stderr)
    return out_path


def load_existing_promotion(asn_num, kind):
    """Load previous promotion report for an ASN.

    kind: "open-questions" or "out-of-scope"
    Returns content or empty string.
    """
    path = note_dir(asn_num) / f"promotion-{kind}.md"
    if path.exists():
        return path.read_text().strip()
    return ""


def save_promotion_report(asn_num, kind, text):
    """Save promotion report to the ASN's manifests directory.

    kind: "open-questions" or "out-of-scope"
    """
    out_dir = note_dir(asn_num)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"promotion-{kind}.md"
    path.write_text(text + "\n")
    print(f"  [WROTE] {path.relative_to(WORKSPACE)}", file=sys.stderr)
