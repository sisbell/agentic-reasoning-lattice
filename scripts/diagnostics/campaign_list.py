#!/usr/bin/env python3
"""
List campaigns in a lattice with their configs and ASN counts.

Walks lattices/<lattice>/campaigns/, reads each campaign's frontmatter,
and counts ASNs per campaign by reading inquiry doc frontmatter (each
inquiry's `campaign:` field; inquiries without one inherit the
lattice's default_campaign).

Usage:
    LATTICE=materials python scripts/diagnostics/campaign_list.py
"""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.lattice.config import lattice_config as cfg
from lib.lattice.labels import label_pattern
from lib.shared.paths import (
    LATTICE_NAME, CAMPAIGN_DIR, INQUIRY_DIR,
    campaign_doc_path, campaign_vocab,
)


def count_vocab_terms(vocab_path):
    """Count curated terms in a vocabulary file.

    A term is identified by a markdown bold at line start: **Term**: …
    This matches xanadu's vocabulary convention (Istream, Vstream, Tumbler, …).
    """
    try:
        text = vocab_path.read_text()
    except FileNotFoundError:
        return 0
    return sum(1 for line in text.splitlines() if line.startswith("**"))


def asn_campaign(inquiry_path):
    """Read an inquiry md and return its `campaign:` frontmatter value,
    or None. Inquiries can opt out of the lattice default by setting
    a campaign explicitly in their frontmatter."""
    from lib.shared.frontmatter import read_doc_frontmatter
    return read_doc_frontmatter(inquiry_path).get("campaign")


def _asn_label_from_dir(d):
    m = label_pattern().match(d.name)
    return m.group(0) if m else None


def main():
    default_campaign = cfg().default_campaign

    if not CAMPAIGN_DIR.exists():
        print(f"No campaigns directory at {CAMPAIGN_DIR}", file=sys.stderr)
        sys.exit(1)

    campaigns = sorted(
        d for d in CAMPAIGN_DIR.iterdir()
        if d.is_dir() and (d / "campaign.md").exists()
    )

    if not campaigns:
        print(f"No campaigns found in {CAMPAIGN_DIR}", file=sys.stderr)
        sys.exit(1)

    # Build ASN-to-campaign mapping from inquiry mds
    asn_by_campaign = {c.name: [] for c in campaigns}
    if INQUIRY_DIR.exists():
        for path in sorted(INQUIRY_DIR.glob(f"{cfg().label_prefix}-*.md")):
            m = label_pattern().match(path.stem)
            if m is None:
                continue
            label = m.group(0)
            bound = asn_campaign(path) or default_campaign
            if bound and bound in asn_by_campaign:
                asn_by_campaign[bound].append(label)

    print(f"Lattice: {LATTICE_NAME} (default_campaign: {default_campaign or '—'})")
    print()

    for cdir in campaigns:
        name = cdir.name
        from lib.shared.frontmatter import read_doc_frontmatter
        cfg = read_doc_frontmatter(campaign_doc_path(name))

        is_default = " [default]" if name == default_campaign else ""
        asns = asn_by_campaign.get(name, [])
        vocab_terms = count_vocab_terms(campaign_vocab(name))

        print(f"{name}{is_default}")
        print(f"  theory: {cfg.get('theory', '—')}")
        print(f"  evidence: {cfg.get('evidence', '—')}")
        target = cfg.get("target", "")
        if target:
            print(f"  target: {target}")
        if asns:
            asn_list = ", ".join(asns)
            print(f"  ASNs: {len(asns)} ({asn_list})")
        else:
            print(f"  ASNs: 0")
        print(f"  vocabulary: {vocab_terms} terms curated")
        print()


if __name__ == "__main__":
    main()
