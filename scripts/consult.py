#!/usr/bin/env python3
"""Consult — ad-hoc channel consultation.

Resolves the target channel (via --asn → campaign, or explicit --channel),
loads the channel plugin at channels/<name>/consultations/consult.py, and
invokes its consult(). Wraps the call with transcript-dir creation and
answer-file writing — one place, not per-channel.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.shared.paths import CONSULTATIONS_DIR
from lib.shared.campaign import resolve_campaign
from lib.consultation.consult import load_channel_plugin, next_session_dir


def main():
    parser = argparse.ArgumentParser(description="Ad-hoc channel consultation")
    parser.add_argument("role", choices=["theory", "evidence"])
    parser.add_argument("question", nargs="?")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--model", "-m", default="opus")
    parser.add_argument("--effort", default="max")
    parser.add_argument("--asn", default=None)
    parser.add_argument("--channel", default=None)
    # Channel-specific flags — passed through to plugins that recognize them.
    parser.add_argument("--with-png", action="store_true",
                        help="Nelson-specific: enable page-image tool access")
    parser.add_argument("--kb-only", action="store_true",
                        help="Gregory-specific: KB agent only")
    parser.add_argument("--code-only", action="store_true",
                        help="Gregory-specific: code agent only")
    args = parser.parse_args()

    if args.stdin:
        question = sys.stdin.read().strip()
    elif args.question:
        question = args.question
    else:
        parser.error("Provide a question or use --stdin")
    if not question:
        parser.error("Empty question")

    if args.channel:
        channel = args.channel
    elif args.asn:
        ctx = resolve_campaign(args.asn)
        channel = ctx.theory_channel if args.role == "theory" else ctx.evidence_channel
    else:
        parser.error("Provide --asn (to resolve via campaign) or --channel (explicit)")

    plugin = load_channel_plugin(channel)

    prefix = f"ASN-{args.asn}" if args.asn else "adhoc"
    consult_dir = next_session_dir(CONSULTATIONS_DIR / prefix / "sessions", channel)
    (consult_dir / "question.md").write_text(question + "\n")
    answer_file = consult_dir / "answer.md"

    extra = {}
    if args.with_png:
        extra["with_png"] = True
    if args.kb_only:
        extra["kb_only"] = True
    if args.code_only:
        extra["code_only"] = True

    print(f"  [{channel.upper()}] consulting...", file=sys.stderr)
    answer = plugin.consult(
        question, model=args.model, effort=args.effort, **extra)
    answer_file.write_text(answer)
    print(str(answer_file))
    print(f"  [LOG] {consult_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
