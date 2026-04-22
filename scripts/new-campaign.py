#!/usr/bin/env python3
"""
Scaffold a new campaign in a lattice.

Validates that the named theory and evidence channels exist under
channels/, and that the campaign name is not already
taken. Creates the campaign directory with config.yaml and a stub
vocabulary.md ready for upfront curation.

Does NOT curate the vocabulary (that is deliberate authoring work).
Does NOT modify the lattice's default_campaign.

Usage:
    ./run/new-campaign.sh --lattice materials \\
        --name dulong-petit-clausius \\
        --theory clausius-1857 \\
        --evidence dulong-petit-1819 \\
        --target "Rediscover DP via Clausius's 1857 kinetic theory"
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import (
    LATTICE_NAME, CAMPAIGNS_DIR, CHANNELS_DIR, WORKSPACE,
    campaign_dir, campaign_config, campaign_vocab,
)


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new campaign directory")
    parser.add_argument("--name", required=True,
                        help="Campaign name (used as the directory name)")
    parser.add_argument("--theory", required=True,
                        help="Theory channel name (must exist under channels/)")
    parser.add_argument("--evidence", required=True,
                        help="Evidence channel name (must exist under channels/)")
    parser.add_argument("--target", required=True,
                        help="One-line prose description of the campaign's target")
    args = parser.parse_args()

    # Validate channels exist
    for role, channel_name in (("theory", args.theory), ("evidence", args.evidence)):
        ch_dir = CHANNELS_DIR / channel_name
        if not ch_dir.exists():
            print(f"  [ERROR] {role} channel not found: {ch_dir}",
                  file=sys.stderr)
            print(f"         Create the channel first: add corpus files "
                  f"and meta.yaml under {ch_dir}.",
                  file=sys.stderr)
            sys.exit(1)
        meta_path = ch_dir / "meta.yaml"
        if not meta_path.exists():
            print(f"  [ERROR] {role} channel is missing meta.yaml at {meta_path}",
                  file=sys.stderr)
            print(f"          Add meta.yaml with a `description:` field before "
                  f"creating a campaign that binds this channel — the "
                  f"assign-channels prompt requires it.",
                  file=sys.stderr)
            sys.exit(1)

    # Validate campaign name is not taken
    cdir = campaign_dir(args.name)
    if cdir.exists():
        print(f"  [ERROR] Campaign already exists: {cdir}", file=sys.stderr)
        sys.exit(1)

    # Create campaign dir
    cdir.mkdir(parents=True)

    cfg_path = campaign_config(args.name)
    cfg_path.write_text(
        f"theory: {args.theory}\n"
        f"evidence: {args.evidence}\n"
        f"target: \"{args.target}\"\n"
    )

    vocab_path = campaign_vocab(args.name)
    vocab_path.write_text("")

    # Report
    print(f"  [OK] Campaign scaffolded: {cdir.relative_to(WORKSPACE)}/")
    print(f"       config.yaml     — theory: {args.theory}, evidence: {args.evidence}")
    print(f"       vocabulary.md   — stub header, awaiting curation")
    print()
    print(f"  Next steps:")
    print(f"    1. Curate {vocab_path.relative_to(WORKSPACE)}")
    print(f"       (read both corpora; coin unified names for bridge terms)")
    print(f"    2. Author an ASN with `campaign: {args.name}` in its manifest")
    print(f"    3. Run discovery: ./run/run-discovery.sh <N> --lattice {LATTICE_NAME}")


if __name__ == "__main__":
    main()
