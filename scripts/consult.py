#!/usr/bin/env python3
"""Consult — ad-hoc expert consultation.

Dispatches to a channel plugin if one exists at channels/<name>/; otherwise
falls back to the per-lattice scripts under domains/<lattice>/scripts/.
The fallback is temporary — removed once all channels are migrated to plugins.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import DOMAIN, CONSULTATIONS_DIR, WORKSPACE
from lib.shared.campaign import resolve_campaign
from lib.consult import load_channel_plugin, next_session_dir


def _peek_channel(role, args_list):
    """Peek at argv to determine which channel this invocation targets.
    Returns the channel name, or None if it can't be determined up front
    (in which case we fall through to the lattice-script subprocess path,
    which handles its own arg parsing).
    """
    peek = argparse.ArgumentParser(add_help=False)
    peek.add_argument("--asn", default=None)
    peek.add_argument("--channel", default=None)
    known, _ = peek.parse_known_args(args_list)
    if known.channel:
        return known.channel
    if known.asn:
        ctx = resolve_campaign(known.asn)
        return ctx.theory_channel if role == "theory" else ctx.evidence_channel
    return None


def _run_plugin(plugin, role, args_list):
    """Handle the plugin path: parse our minimal flags, create a session dir,
    invoke the plugin's consult(), write transcript, print the answer path."""
    p = argparse.ArgumentParser()
    p.add_argument("question", nargs="?")
    p.add_argument("--stdin", action="store_true")
    p.add_argument("--model", "-m", default="opus")
    p.add_argument("--effort", default="max")
    p.add_argument("--asn", default=None)
    p.add_argument("--channel", default=None)
    args = p.parse_args(args_list)

    if args.stdin:
        question = sys.stdin.read().strip()
    elif args.question:
        question = args.question
    else:
        p.error("Provide a question or use --stdin")
    if not question:
        p.error("Empty question")

    # Resolve channel (may have already been peeked, but this is the authoritative read)
    if args.channel:
        channel = args.channel
    else:
        ctx = resolve_campaign(args.asn)
        channel = ctx.theory_channel if role == "theory" else ctx.evidence_channel

    prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    consult_dir = next_session_dir(CONSULTATIONS_DIR / prefix / "sessions", channel)
    (consult_dir / "question.md").write_text(question + "\n")
    answer_file = consult_dir / "answer.md"

    print(f"  [{channel.upper()}] consulting...", file=sys.stderr)
    answer = plugin.consult(question, model=args.model, effort=args.effort)
    answer_file.write_text(answer)
    print(str(answer_file))
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("theory", "evidence"):
        print(f"Usage: consult.py <theory|evidence> [args...]", file=sys.stderr)
        sys.exit(1)
    role = sys.argv[1]
    rest = sys.argv[2:]

    channel = _peek_channel(role, rest)
    if channel:
        try:
            plugin = load_channel_plugin(channel)
            _run_plugin(plugin, role, rest)
            return
        except FileNotFoundError:
            pass  # fall through to lattice-script path

    # Fallback: subprocess to the lattice script (removed in commit 5)
    script = DOMAIN / "scripts" / f"{role}.py"
    if not script.exists():
        print(f"consult.py: no plugin for channel {channel!r} and no {script}",
              file=sys.stderr)
        sys.exit(1)
    sys.exit(subprocess.run([sys.executable, str(script)] + rest).returncode)


if __name__ == "__main__":
    main()
