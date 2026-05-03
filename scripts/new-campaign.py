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
    LATTICE_NAME, CAMPAIGN_DIR, CHANNELS_DIR, WORKSPACE,
    campaign_dir, campaign_doc_path, campaign_vocab, load_channel_meta,
)
from lib.backend.emit import emit_campaign
from lib.backend.store import default_store


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

    # Validate channels exist and are well-formed.
    for role, channel_name in (("theory", args.theory), ("evidence", args.evidence)):
        try:
            meta = load_channel_meta(channel_name)
        except FileNotFoundError as e:
            print(f"  [ERROR] {role} channel: {e}", file=sys.stderr)
            print(f"          Create the channel first: add resources/, "
                  f"consultations/, and meta.yaml (with a `description:` "
                  f"and `shape:` field) under "
                  f"{CHANNELS_DIR / channel_name}.", file=sys.stderr)
            sys.exit(1)
        if not (meta.get("description") or "").strip():
            print(f"  [ERROR] {role} channel {channel_name} is missing "
                  f"`description:` in meta.yaml — the assign-channels prompt "
                  f"requires it.", file=sys.stderr)
            sys.exit(1)
        shape = meta.get("shape")
        if not shape:
            print(f"  [ERROR] {role} channel {channel_name} is missing "
                  f"`shape:` in meta.yaml — set it to `flat-corpus` (single "
                  f"directory of .md sources) or `custom` (channel supplies "
                  f"its own consultations/consult.py).", file=sys.stderr)
            sys.exit(1)
        ch_dir = CHANNELS_DIR / channel_name
        if shape == "custom":
            consult_py = ch_dir / "consultations" / "consult.py"
            if not consult_py.exists():
                print(f"  [ERROR] {role} channel {channel_name} declares "
                      f"`shape: custom` but {consult_py.relative_to(ch_dir.parent.parent)} "
                      f"does not exist.", file=sys.stderr)
                sys.exit(1)
        else:
            for prompt_name in ("answer.md", "generate-questions.md"):
                prompt_path = ch_dir / "consultations" / prompt_name
                if not prompt_path.exists():
                    print(f"  [ERROR] {role} channel {channel_name} "
                          f"(shape: {shape}) is missing "
                          f"{prompt_path.relative_to(ch_dir.parent.parent)}.",
                          file=sys.stderr)
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

    from lib.shared.paths import LATTICE
    store = default_store(LATTICE)
    doc_rel = str(doc_path.resolve().relative_to(LATTICE.resolve()))
    doc_addr = store.register_path(doc_rel)
    emit_campaign(store, doc_addr)

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
