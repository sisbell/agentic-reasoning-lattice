"""
Produce Interface — mechanically assemble formal-statements.md.

Reads YAML summaries + .md formal contracts for each claim.
No LLM calls. Requires summaries to exist — run summarize.py first.
"""

import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.shared.paths import WORKSPACE, CLAIM_CONVERGENCE_DIR, formal_stmts, note_dir
from lib.shared.common import find_asn, build_label_index, load_claim_metadata
from lib.shared.foundation import _extract_formal_contract


def assemble_formal_statements(asn_num):
    """Mechanically assemble formal-statements.md from YAML summaries + .md contracts.

    Reads summary from each claim's YAML and formal contract from its .md.
    Errors if any claim is missing a summary.

    Returns the output path, or None on failure.
    """
    asn_path, asn_label = find_asn(str(asn_num))
    if asn_path is None:
        print(f"  [ASSEMBLE] ASN-{asn_num:04d} not found", file=sys.stderr)
        return None

    claim_dir = CLAIM_CONVERGENCE_DIR / asn_label
    if not claim_dir.exists():
        print(f"  [ASSEMBLE] No claim-convergence directory for {asn_label}",
              file=sys.stderr)
        return None

    all_meta = load_claim_metadata(claim_dir)
    if not all_meta:
        print(f"  [ASSEMBLE] No claim metadata for {asn_label}",
              file=sys.stderr)
        return None

    label_index = build_label_index(claim_dir)

    # Check summaries exist
    missing = [l for l, m in all_meta.items() if not m.get("summary")]
    if missing:
        print(f"  [ASSEMBLE] {len(missing)} claims missing summaries — "
              f"run: python scripts/summarize.py {asn_num}",
              file=sys.stderr)
        for l in missing[:10]:
            print(f"    {l}", file=sys.stderr)
        return None

    # Get source date
    source_text = asn_path.read_text()
    date_match = re.search(r"\*.*?(\d{4}-\d{2}-\d{2}).*?\*", source_text)
    all_dates = re.findall(r"\d{4}-\d{2}-\d{2}",
                           date_match.group(0) if date_match else "")
    asn_date = all_dates[-1] if all_dates else "unknown"

    # Assemble
    parts = [
        f"# {asn_label} Formal Statements\n",
        f"*Source: {asn_path.name} (revised {asn_date}) — "
        f"Extracted: {time.strftime('%Y-%m-%d')}*\n",
    ]

    for label, meta in all_meta.items():
        name = meta.get("name", label)
        summary = meta["summary"]

        stem = label_index.get(label, label)
        md_path = claim_dir / f"{stem}.md"

        parts.append(f"## {label} — {name}\n")
        parts.append(f"{summary}\n")

        if md_path.exists():
            contract = _extract_formal_contract(md_path.read_text())
            if contract:
                parts.append(f"{contract}\n")

        parts.append("---\n")

    output = "\n".join(parts) + "\n"

    # Write
    out_dir = note_dir(asn_num)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = formal_stmts(asn_num)
    out_path.write_text(output)

    prop_count = len(all_meta)
    print(f"  [ASSEMBLE] {out_path.relative_to(WORKSPACE)} "
          f"({prop_count} claims, {len(output) // 1024}KB)",
          file=sys.stderr)

    return out_path
