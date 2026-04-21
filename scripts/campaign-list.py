#!/usr/bin/env python3
"""
List campaigns in a lattice with their configs and ASN counts.

Walks lattices/<lattice>/campaigns/, reads each campaign's config.yaml,
walks lattices/<lattice>/manifests/*/note.yaml to count ASNs per campaign
(including ASNs that inherit the default_campaign), and reports.

Usage:
    LATTICE=materials python scripts/campaign-list.py
"""

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    LATTICE_NAME, CAMPAIGNS_DIR, MANIFESTS_DIR,
    load_lattice_config, campaign_config, campaign_vocab,
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


def asn_campaign(manifest_path):
    """Read an ASN manifest and return its `campaign:` value, or None."""
    try:
        data = yaml.safe_load(manifest_path.read_text()) or {}
    except (FileNotFoundError, OSError):
        return None
    return data.get("campaign")


def _asn_label_from_dir(d):
    m = re.match(r"(ASN-\d+)", d.name)
    return m.group(1) if m else None


def main():
    lattice_config = load_lattice_config()
    default_campaign = lattice_config.get("default_campaign")

    if not CAMPAIGNS_DIR.exists():
        print(f"No campaigns directory at {CAMPAIGNS_DIR}", file=sys.stderr)
        sys.exit(1)

    campaigns = sorted(
        d for d in CAMPAIGNS_DIR.iterdir()
        if d.is_dir() and (d / "config.yaml").exists()
    )

    if not campaigns:
        print(f"No campaigns found in {CAMPAIGNS_DIR}", file=sys.stderr)
        sys.exit(1)

    # Build ASN-to-campaign mapping from manifests
    asn_by_campaign = {c.name: [] for c in campaigns}
    if MANIFESTS_DIR.exists():
        for asn_dir in sorted(MANIFESTS_DIR.iterdir()):
            if not asn_dir.is_dir():
                continue
            label = _asn_label_from_dir(asn_dir)
            if label is None:
                continue
            manifest = asn_dir / "note.yaml"
            if not manifest.exists():
                continue
            bound = asn_campaign(manifest) or default_campaign
            if bound and bound in asn_by_campaign:
                asn_by_campaign[bound].append(label)

    print(f"Lattice: {LATTICE_NAME} (default_campaign: {default_campaign or '—'})")
    print()

    for cdir in campaigns:
        name = cdir.name
        try:
            cfg = yaml.safe_load(campaign_config(name).read_text()) or {}
        except (FileNotFoundError, yaml.YAMLError):
            cfg = {}

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
