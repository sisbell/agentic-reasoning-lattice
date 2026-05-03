#!/usr/bin/env python3
"""
Extract claims from a source ASN into a new extension ASN.

Usage:
    python scripts/note-extend.py -s 53 -t 57 -b 34 --claims D0,D1
    python scripts/note-extend.py --source 53 --target 57 --base 34 --claims D0,D1
"""

import re
import sys
import time

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.shared.paths import (WORKSPACE, LATTICE, NOTE_DIR, MANIFESTS_DIR,
                   prompt_path, load_inquiry, inquiry_doc_path,
                   note_yaml, claim_statements)
from lib.shared.common import read_file, find_asn, invoke_claude, log_usage, step_commit
from lib.shared.foundation import find_extensions


EXTEND_TEMPLATE = prompt_path("discovery/manage/extend.md")


def parse_registry_labels(asn_content):
    """Extract claim labels from the statement registry table."""
    labels = []
    in_table = False
    for line in asn_content.splitlines():
        lower = line.lower()
        if "statement registry" in lower or "claims introduced" in lower:
            in_table = False  # reset -- next table is the one
            continue
        if line.startswith("| ") and ("Label" in line or "label" in line):
            in_table = True
            continue
        if in_table and re.match(r"\|[-\s|]+\|", line):
            continue  # separator row
        if in_table and line.startswith("|"):
            parts = [c.strip() for c in line.split("|")]
            # parts[0] is empty (before first |), parts[1] is label
            if len(parts) >= 3 and parts[1]:
                for sub in parts[1].split(","):
                    sub = sub.strip()
                    if sub:
                        labels.append(sub)
        elif in_table and not line.startswith("|") and line.strip():
            break  # end of table
    return labels


def validate(source_num, target_num, base_num, claim_labels):
    """Validate inputs. Returns (source_path, source_content) or exits."""
    # Source != base
    if source_num == base_num:
        print(f"  [ERROR] Source and base cannot be the same ASN",
              file=sys.stderr)
        sys.exit(1)

    # Source ASN exists
    source_path, source_label = find_asn(str(source_num))
    if source_path is None:
        print(f"  [ERROR] Source ASN-{source_num:04d} not found in "
              f"{NOTE_DIR.relative_to(WORKSPACE)}/", file=sys.stderr)
        sys.exit(1)

    # Base inquiry exists
    base_manifest = load_inquiry(base_num)
    if not base_manifest:
        print(f"  [ERROR] Base ASN-{base_num:04d} has no inquiry doc",
              file=sys.stderr)
        sys.exit(1)

    # Target does not exist
    target_label = f"ASN-{target_num:04d}"
    target_yaml = note_yaml(target_num)
    target_asns = list(NOTE_DIR.glob(f"{target_label}-*.md"))
    if target_yaml.exists():
        print(f"  [ERROR] {target_label} already exists in project model",
              file=sys.stderr)
        sys.exit(1)
    if target_asns:
        print(f"  [ERROR] {target_label} already exists in reasoning docs",
              file=sys.stderr)
        sys.exit(1)

    # Claim labels exist in source registry
    source_content = source_path.read_text()
    registry_labels = parse_registry_labels(source_content)
    missing = [p for p in claim_labels if p not in registry_labels]
    if missing:
        print(f"  [ERROR] Claims not found in source registry: "
              f"{', '.join(missing)}", file=sys.stderr)
        print(f"  Available labels: {', '.join(registry_labels)}",
              file=sys.stderr)
        sys.exit(1)

    return source_path, source_content, base_manifest


def derive_names(base_title, base_num):
    """Compute slug and title for the new extension."""
    existing = find_extensions(base_num)
    n = len(existing)
    base_slug = base_title.lower().replace(" ", "-")
    slug = f"{base_slug}-{n}"
    title = f"{base_title} {n}"
    return slug, title


def compute_depends(base_num):
    """Compute depends list: base's own deps (from substrate) + base itself."""
    import re
    from lib.backend.predicates import active_links
    from lib.febe.session import open_session
    base_inq = inquiry_doc_path(base_num)
    base_rel = str(base_inq.resolve().relative_to(LATTICE.resolve()))
    deps = {base_num}
    session = open_session(LATTICE)
    store = session.store  # for emit_* (Pass 2 will migrate)
    if base_rel in store.path_to_addr:
        base_addr = store.path_to_addr[base_rel]
        for link in active_links(store.state, "citation.depends",
                                 from_set=[base_addr]):
            for cited_addr in link.to_set:
                cited_path = store.path_for_addr(cited_addr)
                if cited_path is None:
                    continue
                m = re.search(r"ASN-(\d+)", cited_path)
                if m:
                    deps.add(int(m.group(1)))
    return sorted(deps)


def build_prompt(source_content, claim_labels, target_num, base_num,
                 source_num, base_title, ext_title, base_statements,
                 foundation_stmts):
    """Build the extraction prompt from the template."""
    template = read_file(EXTEND_TEMPLATE)
    if not template:
        print("  [ERROR] Prompt template not found", file=sys.stderr)
        sys.exit(1)

    target_label = f"ASN-{target_num:04d}"
    base_label = f"ASN-{base_num:04d}"
    source_label = f"ASN-{source_num:04d}"
    date = time.strftime("%Y-%m-%d")

    return (template
            .replace("{{source_content}}", source_content)
            .replace("{{foundation_statements}}", foundation_stmts)
            .replace("{{base_statements}}", base_statements)
            .replace("{{claims}}", ", ".join(claim_labels))
            .replace("{{target_label}}", target_label)
            .replace("{{base_label}}", base_label)
            .replace("{{base_title}}", base_title)
            .replace("{{source_label}}", source_label)
            .replace("{{ext_title}}", ext_title)
            .replace("{{date}}", date))


def strip_preamble(text):
    """Strip any preamble before the ASN header."""
    marker = re.search(r"^# ASN-\d+", text, re.MULTILINE)
    if marker:
        return text[marker.start():]
    return text


def write_manifest(target_num, title, base_num, source_num, depends,
                   claims):
    """Write the project model YAML for the new extension."""
    target_label = f"ASN-{target_num:04d}"
    base_label = f"ASN-{base_num:04d}"
    source_label = f"ASN-{source_num:04d}"
    dep_list = ", ".join(str(d) for d in depends)

    content = (
        f"# {target_label} — {title}\n"
        f'title: "{title}"\n'
        f"extends: {base_num}\n"
        f"source: {source_num}\n"
        f"depends: [{dep_list}]\n"
        f"\n"
        f"consultations:\n"
        f'  question: "Extension of {base_label}: '
        f'claims {", ".join(claims)} from {source_label}."\n'
    )

    path = note_yaml(target_num)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path
