#!/usr/bin/env python3
"""Scout-callable CLI to spawn a new lattice in the docuverse.

    python scripts/agent_tools/create-lattice.py \\
        --name <new-lattice-name> \\
        [--label-prefix ASN] \\
        [--default-campaign <campaign-name>] \\
        [--no-bootstrap]

Invoked from within a scout/bridge agent's prompt session when the
scout decides a new lattice should exist. The new lattice inherits
its (node, user) from the calling scout's authorial space — same
space as the scout, at least initially. Cross-(node, user) lattice
spawning is not supported by this tool.

What the tool does:

  1. Resolve the calling scout's (node, user) from XANADU_AGENT_DOC
     (set by the scout-attribution layer; falls back to LATTICE env
     var for manual operator runs).
  2. Validate that no lattice doc with the requested name exists in
     the scout's (node, user) subtree.
  3. Write the lattice doc body at
     `_docuverse/documents/<node>/<user>/lattice/<name>.md` with
     frontmatter holding `label_prefix` and (optional)
     `default_campaign`.
  4. `register_path()` — account-aware allocator gives a tumbler in
     the scout's user-space.
  5. Optionally invoke `LatticeBootstrapAgent` to provision the
     canonical agent corpus into the new lattice's authorial subtree
     (skipped with `--no-bootstrap`).
  6. Print the new lattice doc's tumbler address on stdout for the
     calling prompt to capture.

What it does NOT do:

  - Update `_NODE_USER_PREFIX` in `lib/shared/paths.py`. The new
    lattice is a substrate citizen but NOT immediately accessible
    via `--lattice <new-name>` until that mapping is updated. The
    scout can still address the new lattice by tumbler.
  - Emit a `lattice` classifier on the lattice doc — there's no
    separate classifier for "this doc IS a lattice"; membership is
    expressed by other docs linking TO this one. Future substrate-
    query of "all lattice docs" would need a classifier; deferred.
  - Cross-(node, user) creation. Use a separate workflow if a lattice
    needs to be spawned in a different organization's space.

Exits 0 on success, prints the new lattice doc's address. Exits
non-zero with a message on conflict or env misconfiguration.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.agents.producers.lattice_bootstrap import (
    LatticeBootstrapAgent,
    is_lattice_bootstrapped,
)
from lib.protocols.febe.session import open_session
from lib.shared.paths import LATTICE, LATTICE_NODE, LATTICE_USER


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BOOTSTRAP_AGENTS = REPO_ROOT / "lattice-bootstrap" / "agents"


def _resolve_node_user() -> tuple[str, str]:
    """Resolve the calling scout's (node, user).

    Priority:
      1. XANADU_AGENT_DOC env var — parse `(node, user)` from the
         scout's doc path.
      2. LATTICE env var → _NODE_USER_PREFIX mapping (operator runs).
      3. Defaults from lib.shared.paths (current active lattice).
    """
    agent_doc = os.environ.get("XANADU_AGENT_DOC")
    if agent_doc:
        m = re.match(
            r"_docuverse/documents/([^/]+)/([^/]+)/agent/", agent_doc,
        )
        if m:
            return m.group(1), m.group(2)
    return LATTICE_NODE, LATTICE_USER


def _validate_name(name: str) -> bool:
    """Lattice name must be a single filesystem-safe path segment."""
    if not name:
        return False
    if "/" in name or "\\" in name or name.startswith("."):
        return False
    if not re.match(r"^[A-Za-z0-9_-]+$", name):
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--name", required=True,
        help="New lattice name (single path segment, no slashes).",
    )
    parser.add_argument(
        "--label-prefix", default="ASN",
        help="Prefix for the new lattice's labels (default: ASN).",
    )
    parser.add_argument(
        "--default-campaign", default=None,
        help="Default campaign for the new lattice (optional).",
    )
    parser.add_argument(
        "--no-bootstrap", action="store_true",
        help=(
            "Skip provisioning the canonical agent corpus into the new "
            "lattice. Default: bootstrap immediately after creation."
        ),
    )
    args = parser.parse_args()

    if not _validate_name(args.name):
        print(
            f"error: invalid lattice name {args.name!r} — must be a "
            f"single path segment matching [A-Za-z0-9_-]+",
            file=sys.stderr,
        )
        return 1

    node, user = _resolve_node_user()
    rel = f"_docuverse/documents/{node}/{user}/lattice/{args.name}.md"
    abs_path = REPO_ROOT / rel

    if abs_path.exists():
        print(
            f"error: lattice doc already exists at {rel}",
            file=sys.stderr,
        )
        return 1

    # Compose the lattice doc body.
    fm_lines = [f"label_prefix: {args.label_prefix}"]
    if args.default_campaign:
        fm_lines.append(f"default_campaign: {args.default_campaign}")
    body = (
        "---\n"
        + "\n".join(fm_lines) + "\n"
        + "---\n"
        + "\n"
        + f"# {args.name}\n"
        + "\n"
        + f"Lattice authored under (node, user) = ({node}, {user}). "
        + "Configuration in this doc's frontmatter is read by "
        + "`lib/lattice/config.py`.\n"
    )

    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(body)

    with open_session(LATTICE) as session:
        if session.get_addr_for_path(rel) is not None:
            print(
                f"error: path {rel} already registered in substrate "
                f"(stale on-disk file?)",
                file=sys.stderr,
            )
            return 1

        addr = session.register_path(rel)
        print(
            f"  [CREATE-LATTICE] {args.name} at {rel} → {addr}",
            file=sys.stderr,
        )

        if not args.no_bootstrap:
            agent = LatticeBootstrapAgent(
                corpus_dir=BOOTSTRAP_AGENTS,
                repo_root=REPO_ROOT,
                node_user=(node, user),
            )
            fires = 0
            max_fires = len(agent.specs) + 1
            while not is_lattice_bootstrapped(
                session, agent.specs, node, user,
            ):
                if fires >= max_fires:
                    print(
                        f"  [CREATE-LATTICE] runaway: {fires} fires "
                        f"without quiescence",
                        file=sys.stderr,
                    )
                    return 1
                result = agent(session=session, addr=addr)
                if not result.success:
                    print(
                        f"  [CREATE-LATTICE] bootstrap failed: "
                        f"{result.detail}",
                        file=sys.stderr,
                    )
                    return 1
                fires += 1
            print(
                f"  [CREATE-LATTICE] bootstrap: {fires} fire(s) "
                f"(0 = canonical corpus already shared with sibling "
                f"lattice in same (node, user))",
                file=sys.stderr,
            )

    # Print the new lattice doc's address on stdout for the prompt
    # session to capture.
    print(addr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
