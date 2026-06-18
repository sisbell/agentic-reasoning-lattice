#!/usr/bin/env python3
"""Module interface extraction — the condensed, consumer-facing contract.

To a module design what claim-statements are to a note: a one-shot LLM
extraction of the converged `design.md` down to the interface a *dependent*
builds against (public signatures + caller contracts + downstream seams +
boundary), with the producing module's internal reasoning stripped out.

`module-design.py` feeds a dependent module its upstreams' `interface.md` (this
output) instead of their full `design.md` — far less context, no quality loss,
since a dependent never needed the internals (smaller high-signal context =
higher-quality output; same reason notes feed downstream as statements).

    python scripts/extract-interface.py M1          # one module
    python scripts/extract-interface.py M1 M2        # several
    python scripts/extract-interface.py --all        # every converged design
    python scripts/extract-interface.py M1 --no-commit
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.invoke_claude import invoke_claude

OUT_ROOT = ROOT / "_design" / "module-designs"
PROMPT = ROOT / "prompts/shared/module-design/interface.md"


def _git(args):
    subprocess.run(["git", *args], cwd=ROOT, check=True,
                   capture_output=True, text=True)


def _commit(path: Path, message: str, enabled: bool) -> None:
    if not enabled:
        return
    rel = str(path.relative_to(ROOT))
    _git(["add", rel])
    if subprocess.run(["git", "diff", "--cached", "--quiet", "--", rel],
                      cwd=ROOT).returncode == 0:
        return
    _git(["commit", "-q", "-m", message, "--", rel])
    print(f"  [commit] {message}", file=sys.stderr)


def extract(mid: str, model: str, effort: str, commit: bool) -> bool:
    design_md = OUT_ROOT / mid / "design.md"
    if not design_md.exists():
        print(f"[interface] {mid}: no design.md — skip (design it first).",
              file=sys.stderr)
        return False
    tmpl = PROMPT.read_text()
    tmpl = tmpl.replace("{{design}}", design_md.read_text())
    tmpl = tmpl.replace("{{module_id}}", mid)

    for attempt in range(1, 4):
        r = invoke_claude(tmpl, model=model, effort=effort, output_format="json")
        if r.ok and r.text.strip():
            iface = OUT_ROOT / mid / "interface.md"
            iface.write_text(r.text.strip() + "\n")
            src_kb = len(design_md.read_text()) // 1024
            out_kb = len(r.text) // 1024
            print(f"  [interface] {mid} [{r.elapsed:.0f}s] "
                  f"design ~{src_kb}KB → interface ~{out_kb}KB "
                  f"(in:{r.usage['input_tokens']} out:{r.usage['output_tokens']} "
                  f"${r.cost:.4f})", file=sys.stderr)
            _commit(iface, f"interface({mid}): extract consumer-facing contract",
                    commit)
            return True
        print(f"  [interface] {mid} attempt {attempt}/3 failed "
              f"(ok={r.ok}, {len(r.text)} chars)", file=sys.stderr)
    print(f"[interface] {mid}: FAILED after 3 attempts.", file=sys.stderr)
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("modules", nargs="*", help="module ids (M1 M2 ...)")
    ap.add_argument("--all", action="store_true",
                    help="extract for every module-designs/*/design.md")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="medium",
                    help="extraction is projection, not deep reasoning — medium is plenty")
    ap.add_argument("--no-commit", action="store_true")
    args = ap.parse_args()

    if args.all:
        mids = sorted(p.parent.name for p in OUT_ROOT.glob("*/design.md"))
    else:
        mids = [m.upper() if m.lower().startswith("m") else f"M{m}"
                for m in args.modules]
    if not mids:
        ap.error("give module ids (e.g. M1 M2) or --all")

    ok = 0
    for mid in mids:
        if extract(mid, args.model, args.effort, not args.no_commit):
            ok += 1
    print(f"[interface] extracted {ok}/{len(mids)}.", file=sys.stderr)
    return 0 if ok == len(mids) else 1


if __name__ == "__main__":
    raise SystemExit(main())
