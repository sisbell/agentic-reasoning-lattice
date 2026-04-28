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
from lib.shared.common import write_frontmatter
from lib.shared.paths import (
    LATTICE_NAME, CAMPAIGNS_DIR, CHANNELS_DIR, WORKSPACE,
    campaign_dir, campaign_doc_path, campaign_vocab, load_channel_meta,
)
from lib.store.emit import emit_campaign
from lib.store.store import default_store


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

    # Validate channels exist and have a description in meta.yaml.
    for role, channel_name in (("theory", args.theory), ("evidence", args.evidence)):
        try:
            meta = load_channel_meta(channel_name)
        except FileNotFoundError as e:
            print(f"  [ERROR] {role} channel: {e}", file=sys.stderr)
            print(f"          Create the channel first: add resources/, "
                  f"consultations/, and meta.yaml (with a `description:` "
                  f"field) under {CHANNELS_DIR / channel_name}.",
                  file=sys.stderr)
            sys.exit(1)
        if not (meta.get("description") or "").strip():
            print(f"  [ERROR] {role} channel {channel_name} is missing "
                  f"`description:` in meta.yaml — the assign-channels prompt "
                  f"requires it.", file=sys.stderr)
            sys.exit(1)

    # Validate campaign name is not taken
    doc_path = campaign_doc_path(args.name)
    if doc_path.exists():
        print(f"  [ERROR] Campaign already exists: {doc_path}",
              file=sys.stderr)
        sys.exit(1)

    # Substrate-managed campaign descriptor + vocabulary in same dir
    cdir = campaign_dir(args.name)
    cdir.mkdir(parents=True, exist_ok=True)
    fm = {
        "name": args.name,
        "theory": args.theory,
        "evidence": args.evidence,
        "target": args.target,
    }
    title = args.name.replace("-", " ").title()
    body = f"# Campaign: {title}\n"
    doc_path.write_text(write_frontmatter(fm, body))

    with default_store() as store:
        emit_campaign(store, doc_path)

    vocab_path = campaign_vocab(args.name)
    vocab_path.write_text("")

    print(f"  [OK] Campaign scaffolded:")
    print(f"       {doc_path.relative_to(WORKSPACE)}  — descriptor (theory: {args.theory}, evidence: {args.evidence})")
    print(f"       {vocab_path.relative_to(WORKSPACE)}  — bridge vocabulary stub")
    print()
    print(f"  Next steps:")
    print(f"    1. Curate {vocab_path.relative_to(WORKSPACE)}")
    print(f"       (read both corpora; coin unified names for bridge terms)")
    print(f"    2. Author an inquiry with `campaign: {args.name}` in its frontmatter")
    print(f"    3. Run discovery: ./run/run-discovery.sh <N> --lattice {LATTICE_NAME}")


if __name__ == "__main__":
    main()
