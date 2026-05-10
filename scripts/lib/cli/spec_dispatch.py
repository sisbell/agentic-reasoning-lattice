"""Spec-dispatch CLI helpers — collapse two recurring CLI shapes.

Two operator-gated agent dispatch shapes recur across top-level
scripts:

  Lattice-scope spec dispatch (extract, clone, absorb)
    Operator drops one spec md into a workspace inbox dir; agent
    consumes it via `spec_filename=`. Target is the lattice itself.
    Helper: `run_spec_cli`.

  ASN-scope patch dispatch (note-patch, claim-patch)
    Operator passes an ASN number positional + `--patch <filename>`;
    the patch lives in a per-ASN subdir under a kind-rooted inbox.
    Agent consumes it via `patch_filename=` and is dispatched on
    the resolved note address.
    Helper: `run_patch_cli`.

Each helper handles the boilerplate (argparse, inbox existence
check, dry-run output, session open, agent dispatch, status print,
exit code). Each consuming script collapses to a docstring + one
config call.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Type

from lib.agents.base import Agent
from lib.lattice.labels import format_label
from lib.protocols.febe.session import open_session
from lib.shared.common import find_asn
from lib.shared.paths import LATTICE, WORKSPACE


# ─── Lattice-scope spec dispatch ───────────────────────────────────


def run_spec_cli(
    *,
    name: str,
    agent_cls: Type[Agent],
    inbox: Path,
    description: str,
    dry_run_steps: str,
    accepts_model: bool = True,
    next_hint: Optional[str] = None,
) -> int:
    """Operator-gated dispatcher for a lattice-scope spec doc.

    The operator drops a spec md into `inbox`; this helper:
      1. Parses argv (`--spec`, optional `--model`/`--effort`, `--dry-run`)
      2. Verifies the spec exists; prints `dry_run_steps` if dry-run
      3. Opens a session, instantiates `agent_cls`, dispatches it
         against the lattice account address with `spec_filename=`
      4. Prints `[DONE]` + the result detail; optionally prints
         `[NEXT] <next_hint>` on success
      5. Returns 0 on success, 1 on failure

    Args:
      name: Short tag printed in [NAME] (uppercased).
      agent_cls: Agent subclass to instantiate.
      inbox: Workspace inbox directory; the spec is at `inbox / <filename>`.
      description: argparse description.
      dry_run_steps: One-line phase summary printed in --dry-run mode.
      accepts_model: When True, expose `--model` / `--effort` flags
        and pass them as kwargs to the agent constructor.
      next_hint: Optional "[NEXT] ..." hint printed after a successful
        fire to suggest follow-up commands.
    """
    parser = argparse.ArgumentParser(prog=name, description=description)
    parser.add_argument(
        "--spec", required=True,
        help=(
            f"Spec filename in {inbox.relative_to(WORKSPACE) if inbox.is_relative_to(WORKSPACE) else inbox}/. "
            "Operator drops the spec md there before running."
        ),
    )
    if accepts_model:
        parser.add_argument(
            "--model", "-m", default="opus", choices=["opus", "sonnet"],
        )
        parser.add_argument(
            "--effort", default="max", help="Thinking effort level",
        )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = inbox / args.spec
    if not spec_path.exists():
        print(
            f"  [ERROR] Spec not found in workspace: {spec_path}",
            file=sys.stderr,
        )
        print(
            f"  Drop the spec md at {spec_path} and re-run.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print(f"  [DRY RUN] Steps: {dry_run_steps}", file=sys.stderr)
        print(f"  Spec: {spec_path}", file=sys.stderr)
        print(f"  Content:\n{spec_path.read_text()}", file=sys.stderr)
        return 0

    print(f"  [{name.upper()}] {args.spec}", file=sys.stderr)

    with open_session(LATTICE) as session:
        kwargs = (
            {"model": args.model, "effort": args.effort}
            if accepts_model else {}
        )
        agent = agent_cls(**kwargs)
        # Operator-gated agents take target context from the spec
        # doc; the addr argument is unused but required by the
        # Agent dispatch surface — pass the lattice account as a
        # stand-in.
        lattice_addr = session.store.account
        result = agent(session, lattice_addr, spec_filename=args.spec)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    if next_hint and result.success:
        print(f"  [NEXT] {next_hint}", file=sys.stderr)
    return 0 if result.success else 1


# ─── ASN-scope patch dispatch ──────────────────────────────────────


def run_patch_cli(
    *,
    name: str,
    agent_cls: Type[Agent],
    inbox_root: Path,
    description: str,
    dry_run_steps: str,
    next_hint_template: Optional[str] = None,
) -> int:
    """Operator-gated patch dispatcher scoped to a single ASN.

    The operator passes the ASN positional and `--patch <filename>`;
    the patch lives at `inbox_root / <ASN-NNNN> / <filename>`. This
    helper resolves the note address (via find_asn) and dispatches
    `agent_cls` with `patch_filename=`.

    Args:
      name: Short tag printed in [NAME] (uppercased).
      agent_cls: Agent subclass (e.g. NotePatchAgent, ClaimPatchAgent).
      inbox_root: Workspace inbox root for this kind of patch.
      description: argparse description.
      dry_run_steps: One-line phase summary printed in --dry-run mode.
      next_hint_template: Optional [NEXT] hint format string with one
        `{asn}` placeholder, e.g.
        "Drive convergence: python scripts/run-trigger.py note_review {asn}".
    """
    parser = argparse.ArgumentParser(prog=name, description=description)
    parser.add_argument("asn", type=int, help="ASN number to patch")
    parser.add_argument(
        "--patch", required=True,
        help=(
            f"Patch filename in "
            f"{inbox_root.relative_to(WORKSPACE) if inbox_root.is_relative_to(WORKSPACE) else inbox_root}/<ASN-NNNN>/. "
            "Operator drops the patch md there before running."
        ),
    )
    parser.add_argument(
        "--model", "-m", default="opus", choices=["opus", "sonnet"],
    )
    parser.add_argument(
        "--effort", default="max", help="Thinking effort level",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    asn_path, asn_label = find_asn(str(args.asn))
    if asn_path is None:
        print(f"  [ERROR] {format_label(args.asn)} not found", file=sys.stderr)
        return 1

    patch_path = inbox_root / asn_label / args.patch
    if not patch_path.exists():
        print(
            f"  [ERROR] Patch not found in workspace: {patch_path}",
            file=sys.stderr,
        )
        print(
            f"  Drop the patch md at {patch_path} and re-run.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print(f"  [DRY RUN] Steps: {dry_run_steps}", file=sys.stderr)
        print(f"  Patch: {patch_path}", file=sys.stderr)
        print(f"  Content:\n{patch_path.read_text()}", file=sys.stderr)
        return 0

    print(f"  [{name.upper()}] {asn_label} ← {args.patch}", file=sys.stderr)

    with open_session(LATTICE) as session:
        note_rel = str(asn_path.resolve().relative_to(LATTICE.resolve()))
        note_addr = session.get_addr_for_path(note_rel)
        if note_addr is None:
            note_addr = session.register_path(note_rel)

        agent = agent_cls(model=args.model, effort=args.effort)
        result = agent(session, note_addr, patch_filename=args.patch)

    print(f"\n  [DONE] {result.detail}", file=sys.stderr)
    if next_hint_template and result.success:
        print(
            f"  [NEXT] {next_hint_template.format(asn=args.asn)}",
            file=sys.stderr,
        )
    return 0 if result.success else 1
