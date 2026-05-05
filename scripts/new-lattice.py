#!/usr/bin/env python3
"""
Scaffold a new lattice directory.

Creates `lattices/<name>/` with the minimal config (`config.yaml`).
Substrate directories (`_docuverse/`, `_workspace/`) are auto-created
on first use by the runtime — no need to pre-create them.

Idempotent on a missing target: refuses to overwrite an existing lattice
directory. Run once per new domain.

Usage:
    ./run/new-lattice.sh --name materials
    ./run/new-lattice.sh --name myproject

The lattice's `default_campaign` is left blank — set it after you
create your first campaign with `run/new-campaign.sh`.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LATTICES_DIR = REPO_ROOT / "lattices"

NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new lattice directory")
    parser.add_argument("--name", required=True,
                        help="Lattice name (lowercase, hyphenated; "
                             "becomes the directory name)")
    args = parser.parse_args()

    if not NAME_RE.match(args.name):
        print(f"  [ERROR] lattice name {args.name!r} must be lowercase, "
              f"start with a letter, and contain only letters, digits, "
              f"and hyphens.", file=sys.stderr)
        sys.exit(1)

    lattice_dir = LATTICES_DIR / args.name
    if lattice_dir.exists():
        print(f"  [ERROR] {lattice_dir.relative_to(REPO_ROOT)} already exists.",
              file=sys.stderr)
        sys.exit(1)

    lattice_dir.mkdir(parents=True)

    config_path = lattice_dir / "config.yaml"
    config_path.write_text(
        "# Lattice configuration.\n"
        "#\n"
        "# default_campaign: name of the campaign ASNs inherit by default.\n"
        "# Leave blank until you create your first campaign with\n"
        "# `run/new-campaign.sh`, then set it here.\n"
        "default_campaign:\n"
    )

    print(f"  Created {lattice_dir.relative_to(REPO_ROOT)}/", file=sys.stderr)
    print(f"    config.yaml", file=sys.stderr)
    print(f"\n  Next steps:", file=sys.stderr)
    print(f"    1. Create channels under channels/ "
          f"(see docs/getting-started/03-add-channels.md)", file=sys.stderr)
    print(f"    2. Create your first campaign with "
          f"`./run/new-campaign.sh --lattice {args.name} --name <campaign> "
          f"--theory <ch> --evidence <ch> --target '...'`",
          file=sys.stderr)
    print(f"    3. Set the campaign as default in "
          f"{config_path.relative_to(REPO_ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
