#!/usr/bin/env python3
"""Rebase a module's downstream cone (or the whole stack) in build order.

When an upstream module's interface changes, every module that builds against it
was designed against a now-stale contract. This walks the affected cone in
build_order and, for each module, runs:

    module-design.py MX --rebase      (re-review vs CURRENT upstream interfaces, re-converge)
    extract-interface.py MX           (publish the updated interface for its dependents)

It MUST be sequential: a downstream rebase has to see its upstreams' re-extracted
interfaces, so module N+1 only starts after module N's interface is republished.
Each step auto-commits (the underlying scripts do), so a cascade is a clean series
of per-module commits.

    python scripts/rebase-cone.py --all              # whole stack, build_order (skips M1, the gold root)
    python scripts/rebase-cone.py M2                 # M2 + every module that transitively depends on it
    python scripts/rebase-cone.py --all --from M3    # resume the cascade at M3 (after a failure/stop)
    python scripts/rebase-cone.py --all --include-m1 # include M1 too (normally skipped — oracle-backed)

Set CLAUDE_CONFIG_DIRS in the environment as usual; it is inherited by the children.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MODULES_YAML = ROOT / "_design/modules/modules.yaml"
OUT_ROOT = ROOT / "_design" / "module-designs"


def _load():
    data = yaml.safe_load(MODULES_YAML.read_text())
    mods = data["modules"]
    return mods, data.get("build_order", list(mods))


def _norm(m: str) -> str:
    m = m.strip()
    return m.upper() if m.lower().startswith("m") else f"M{m}"


def _transitive_dependents(targets: set[str], mods: dict) -> set[str]:
    """targets + every module that (transitively) depends on any target."""
    cone = set(targets)
    grew = True
    while grew:
        grew = False
        for y, m in mods.items():
            if y in cone:
                continue
            if set(m.get("depends_on", []) or []) & cone:
                cone.add(y)
                grew = True
    return cone


def _designed(mid: str) -> bool:
    return (OUT_ROOT / mid / "design.md").exists()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modules", nargs="*", help="seed module(s); their downstream cone is rebased")
    ap.add_argument("--all", action="store_true", help="rebase every designed module in build_order")
    ap.add_argument("--from", dest="start", help="resume the build_order cascade at this module")
    ap.add_argument("--include-m1", action="store_true",
                    help="include M1 (skipped by default — gold via the Dafny oracle, no upstream to realign)")
    ap.add_argument("--effort", default=None, help="override effort passed to module-design --rebase")
    ap.add_argument("--dry-run", action="store_true", help="print the cascade order and exit")
    args = ap.parse_args()

    mods, build_order = _load()

    if args.all:
        cone = {m for m in build_order if _designed(m)}
    elif args.modules:
        targets = {_norm(m) for m in args.modules}
        bad = [t for t in targets if t not in mods]
        if bad:
            ap.error(f"unknown module(s): {bad}")
        cone = _transitive_dependents(targets, mods)
    else:
        ap.error("give seed module(s) or --all")

    if not args.include_m1:
        cone.discard("M1")

    # Order by build_order; only modules that have a design to rebase.
    seq = [m for m in build_order if m in cone and _designed(m)]
    if args.start:
        start = _norm(args.start)
        if start not in seq:
            ap.error(f"--from {start} is not in the cascade {seq}")
        seq = seq[seq.index(start):]

    if not seq:
        sys.exit("[rebase-cone] nothing to rebase (no designed modules in scope).")

    print(f"[rebase-cone] cascade ({len(seq)}): {' → '.join(seq)}", file=sys.stderr)
    if args.dry_run:
        return 0

    for i, mid in enumerate(seq, 1):
        print(f"\n[rebase-cone] ===== {mid} ({i}/{len(seq)}): rebase =====", file=sys.stderr)
        rb = [sys.executable, "scripts/module-design.py", mid, "--rebase"]
        if args.effort:
            rb += ["--effort", args.effort]
        if subprocess.run(rb, cwd=ROOT).returncode != 0:
            sys.exit(f"[rebase-cone] {mid} rebase FAILED — fix, then resume: "
                     f"rebase-cone.py --all --from {mid}")
        print(f"[rebase-cone] ===== {mid} ({i}/{len(seq)}): re-extract interface =====",
              file=sys.stderr)
        ex = [sys.executable, "scripts/extract-interface.py", mid]
        if args.effort:
            ex += ["--effort", args.effort]
        if subprocess.run(ex, cwd=ROOT).returncode != 0:
            sys.exit(f"[rebase-cone] {mid} interface extract FAILED — resume: "
                     f"rebase-cone.py --all --from {mid}")

    print(f"\n[rebase-cone] DONE — rebased + re-extracted: {' → '.join(seq)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
