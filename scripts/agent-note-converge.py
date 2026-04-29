#!/usr/bin/env python3
"""Build the system prompt for the note-convergence driver agent.

The agent's prompt is three layers:
  1. Role  — what the agent is responsible for
  2. Protocol — the verbatim Note Convergence Protocol document
  3. Tool surface — the five Bash-invocable tools the agent uses

Output: writes the assembled prompt to
`lattices/<lattice>/_workspace/agent-runs/note-converge-<asn>-<ts>.prompt`,
prints the path, and prints the suggested `claude` invocation.

The user runs the tool — this script does not invoke claude itself.

Usage:
    python3 scripts/agent-note-converge.py <asn>
"""

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, LATTICE_NAME

REPO = Path(__file__).resolve().parent.parent

# The protocol doc declares its module dependencies in §2 — substrate,
# agent module, and the parent convergence protocol. The agent gets all
# four verbatim so the property names cited in note-convergence
# (SUB1, A3, etc.) are grounded in their actual definitions.
SPEC_DOCS = [
    ("Note Convergence Protocol",
     REPO / "docs" / "protocols" / "note-convergence-protocol.md"),
    ("Convergence Protocol (parent — predicate, comment/resolution semantics)",
     REPO / "docs" / "protocols" / "convergence-protocol.md"),
    ("Substrate Module (link graph, SUB1–SUB6)",
     REPO / "docs" / "modules" / "substrate-module.md"),
    ("Agent Module (agent identity, manages, A1–A6)",
     REPO / "docs" / "modules" / "agent-module.md"),
]

ROLE = """You are the agent driving one note to convergence under the Note
Convergence Protocol.

Your job:
- Follow the protocol's algorithm (see Protocol section below).
- Preserve its safety properties (file only the link types the protocol
  defines; respect retraction semantics; honor finding classification).
- Pursue its liveness properties — drive the substrate's convergence
  predicate to true.
- Halt when the predicate holds AND a confirmation review files zero
  new revises.

You do not edit notes or substrate state directly. You invoke the tools
listed in the Tool surface section via Bash, read each tool's output,
and decide the next step based on the protocol.

The protocol's §6 algorithm describes a deterministic playbook. You
may follow it as written, or use the protocol's properties as your
contract and adapt within them. Either is in spec — see the protocol's
own framing of §6 as a reference algorithm.
"""

TOOL_SURFACE = """Five tools, all invoked via Bash from the repo root.

### `python3 scripts/agent_tools/predicate_status.py <asn>`

Substrate query. Prints one line:

    NOTE=<label> REVISES_TOTAL=<n> REVISES_OPEN=<n> RESOLUTIONS=<n> PREDICATE_HOLDS=<true|false>

`PREDICATE_HOLDS=true` ⇔ every active `comment.revise` on the note has
a matching active `resolution`. This is the protocol's convergence
predicate at the substrate level.

### `python3 scripts/agent_tools/open_revises.py <asn>`

Substrate query. Prints one line per unresolved revise comment:

    <comment_id>\\t<title>

Empty output means no open revises. Useful before deciding whether to
run a revise pass (RetryOpenRevises in §6.3).

### `bash scripts/agent_tools/run_review.sh <asn>`

Reviewer participant. Runs one review pass on the note. Files new
`comment.revise` and `comment.out-of-scope` links to the substrate.
Writes a review document to the lattice's reviews directory.

After this returns, query `predicate_status` and `open_revises` to see
what changed.

### `bash scripts/agent_tools/run_revise.sh <asn>`

Reviser participant. Addresses currently-open revises by editing the
note and filing `resolution.edit` links. Reads the substrate's open
revises queue at start; you don't pass them in.

After this returns, query `predicate_status` to see how many resolved.

### `bash scripts/agent_tools/commit.sh "<message>"`

Stages working-tree changes and commits. Prints `COMMITTED` on success
or `NOTHING_TO_COMMIT` if no changes are staged.

## Loop guidance

The protocol's §6.2 cycle is:

1. RetryOpenRevises — query open_revises; if any exist, run_revise first.
2. Review — run_review.
3. EmitFindings — handled inside run_review.
4. Revise — if the latest review filed REVISE findings, run_revise.
5. Commit — commit after each cycle's substrate writes.
6. Check predicate; if holds and the latest review was zero-revise,
   indicate convergence and halt.

Recommended halt conditions:

- PREDICATE_HOLDS=true AND the most recent review filed zero REVISE
  findings — converged.
- Predicate fails to advance for several cycles — file a diagnostic
  in the workspace and halt.
- Tool failure — halt and report.

## Substrate-state queries vs side-effecting tools

Treat predicate_status and open_revises as free observation. Run them
liberally. The two participant tools (run_review, run_revise) and
commit are the side-effecting ones — each takes time and changes
state.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asn")
    args = ap.parse_args()

    asn_path, asn_label = find_asn(args.asn)
    if asn_path is None:
        print(f"ERROR: ASN not found: {args.asn}", file=sys.stderr)
        sys.exit(1)

    spec_sections = []
    for label, doc_path in SPEC_DOCS:
        spec_sections.append(f"## {label}\n\n{doc_path.read_text()}")
    spec_text = "\n\n---\n\n".join(spec_sections)

    system_prompt = "\n\n---\n\n".join([
        "# Role\n\n" + ROLE,
        "# Specification\n\n"
        "Your role is governed by the four documents below. Note Convergence "
        "is the protocol you implement; the others define modules and "
        "properties Note Convergence's §2 declares as dependencies.\n\n"
        + spec_text,
        "# Tool surface\n\n" + TOOL_SURFACE,
    ])

    user_message = f"Drive {asn_label} to convergence."

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    runs_dir = LATTICE / "_workspace" / "agent-runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    base = runs_dir / f"note-converge-{asn_label}-{timestamp}"
    system_path = base.with_suffix(".system.txt")
    user_path = base.with_suffix(".user.txt")
    system_path.write_text(system_prompt)
    user_path.write_text(user_message)

    sys_rel = system_path.relative_to(REPO)
    user_rel = user_path.relative_to(REPO)

    print(f"Built prompt:", file=sys.stderr)
    print(f"  system: {sys_rel}  ({len(system_prompt):,} chars)",
          file=sys.stderr)
    print(f"  user:   {user_rel}", file=sys.stderr)
    print(f"", file=sys.stderr)
    lattice_env = f"LATTICE={LATTICE_NAME}"
    print(f"To run the driver agent headlessly on opus "
          f"(against the {LATTICE_NAME} lattice):", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"  {lattice_env} bash -c '\\", file=sys.stderr)
    print(f"    cat {user_rel} | \\", file=sys.stderr)
    print(f"    claude --print \\", file=sys.stderr)
    print(f"           --model opus \\", file=sys.stderr)
    print(f"           --append-system-prompt \"$(cat {sys_rel})\" \\",
          file=sys.stderr)
    print(f"           --allowed-tools Bash'", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(f"  (the bash -c wrapper carries LATTICE through to claude's tool "
          f"calls; without it claude inherits the parent shell's LATTICE, "
          f"which defaults to xanadu)", file=sys.stderr)
    print(f"", file=sys.stderr)
    print(str(system_path))


if __name__ == "__main__":
    main()
