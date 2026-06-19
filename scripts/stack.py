#!/usr/bin/env python3
"""Level-parallel design/rebase across the module DAG.

The module DAG (modules.yaml depends_on) is not a chain — modules at the same
topological level are independent and can run concurrently. This groups the scope
by `topological_levels` (the same lib the method-dag uses) and runs each level's
modules in parallel, barriering between levels so a level-N+1 module only starts
after every level-N design is converged AND its interface re-extracted.

Concurrency is pinned to ACCOUNTS: each parallel worker grabs one config dir from
CLAUDE_CONFIG_DIRS and runs under it alone, so two workers never contend on one
account's cost/quota state. With two live accounts you get true 2-way parallelism
(and every parallel level in this DAG has exactly two modules).

Per module, a worker runs:  module-design.py MX [--rebase]  →  extract-interface.py MX

    # fresh design of the whole stack (no-ops already-converged modules, designs the rest):
    CLAUDE_CONFIG_DIRS="$HOME/.claude,$HOME/.claude-account2" python scripts/stack.py --all
    # rebase the whole stack into alignment, level-parallel:
    CLAUDE_CONFIG_DIRS="...,..." python scripts/stack.py --all --rebase
    python scripts/stack.py M3 --rebase            # M3 + its dependent cone, level-parallel
    python scripts/stack.py --all --rebase --from M3   # resume from M3's level onward
    python scripts/stack.py --all --rebase --dry-run   # print the parallel level plan
"""

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from queue import Queue

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.shared.topological_sort import topological_levels  # noqa: E402

MODULES_YAML = ROOT / "_design/modules/modules.yaml"
OUT_ROOT = ROOT / "_design" / "module-designs"


def _load():
    data = yaml.safe_load(MODULES_YAML.read_text())
    return data["modules"], data.get("build_order", list(data["modules"]))


def _norm(m: str) -> str:
    m = m.strip()
    return m.upper() if m.lower().startswith("m") else f"M{m}"


def _dependents(targets: set[str], mods: dict) -> set[str]:
    cone = set(targets)
    grew = True
    while grew:
        grew = False
        for y, m in mods.items():
            if y not in cone and (set(m.get("depends_on", []) or []) & cone):
                cone.add(y)
                grew = True
    return cone


def _designed(mid: str) -> bool:
    return (OUT_ROOT / mid / "design.md").exists()


def _accounts() -> list[str]:
    raw = os.environ.get("CLAUDE_CONFIG_DIRS", "").strip()
    if raw:
        return [a.strip() for a in raw.split(",") if a.strip()]
    home = os.environ["HOME"]
    return [f"{home}/.claude", f"{home}/.claude-account2"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modules", nargs="*", help="seed module(s); their dependent cone is processed")
    ap.add_argument("--all", action="store_true", help="process the whole stack")
    ap.add_argument("--rebase", action="store_true", help="rebase (re-review) instead of fresh design")
    ap.add_argument("--from", dest="start", help="start at this module's level (drop earlier modules)")
    ap.add_argument("--jobs", type=int, default=None, help="max parallel workers (default: #accounts)")
    ap.add_argument("--effort", default=None, help="override effort for module-design")
    ap.add_argument("--dry-run", action="store_true", help="print the level plan and exit")
    args = ap.parse_args()

    mods, build_order = _load()

    if args.all:
        scope = {m for m in build_order if (_designed(m) or not args.rebase)}
    elif args.modules:
        targets = {_norm(m) for m in args.modules}
        bad = [t for t in targets if t not in mods]
        if bad:
            ap.error(f"unknown module(s): {bad}")
        scope = _dependents(targets, mods)
    else:
        ap.error("give seed module(s) or --all")

    # For rebase, only modules that already have a design can be rebased.
    if args.rebase:
        scope = {m for m in scope if _designed(m)}

    if args.start:
        start = _norm(args.start)
        if start not in build_order:
            ap.error(f"--from {start} unknown")
        keep = set(build_order[build_order.index(start):])
        scope &= keep

    if not scope:
        sys.exit("[stack] nothing to do (empty scope).")

    # Topological levels over the SCOPED subgraph (deps outside scope are ignored for layering).
    deps_data = {"claims": {m: {"follows_from": [d for d in (mods[m].get("depends_on") or []) if d in scope]}
                            for m in scope}}
    levels = [lvl for lvl in topological_levels(deps_data) if lvl]

    accounts = _accounts()
    jobs = args.jobs or len(accounts)
    jobs = max(1, min(jobs, len(accounts)))

    print(f"[stack] mode={'rebase' if args.rebase else 'design'}  jobs={jobs}  "
          f"accounts={len(accounts)}", file=sys.stderr)
    for i, lvl in enumerate(levels):
        print(f"[stack]   level {i}: {sorted(lvl)}", file=sys.stderr)
    if args.dry_run:
        return 0

    acct_q: Queue = Queue()
    for a in accounts[:jobs]:
        acct_q.put(a)

    def run_module(mid: str):
        acct = acct_q.get()
        try:
            env = {**os.environ, "CLAUDE_CONFIG_DIRS": acct}
            dz = [sys.executable, "scripts/module-design.py", mid]
            if args.rebase:
                dz.append("--rebase")
            if args.effort:
                dz += ["--effort", args.effort]
            print(f"[stack] >>> {mid} (account {Path(acct).name}): module-design", file=sys.stderr)
            if subprocess.run(dz, cwd=ROOT, env=env).returncode != 0:
                return mid, "module-design FAILED"
            print(f"[stack] >>> {mid} (account {Path(acct).name}): extract-interface", file=sys.stderr)
            if subprocess.run([sys.executable, "scripts/extract-interface.py", mid],
                              cwd=ROOT, env=env).returncode != 0:
                return mid, "extract-interface FAILED"
            return mid, "ok"
        finally:
            acct_q.put(acct)

    for i, lvl in enumerate(levels):
        ordered = [m for m in build_order if m in lvl]
        print(f"\n[stack] ===== level {i}/{len(levels)-1}: {ordered} (parallel) =====", file=sys.stderr)
        failures = []
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            futs = {ex.submit(run_module, m): m for m in ordered}
            for fut in as_completed(futs):
                mid, status = fut.result()
                print(f"[stack] <<< {mid}: {status}", file=sys.stderr)
                if status != "ok":
                    failures.append((mid, status))
        if failures:
            sys.exit(f"[stack] level {i} had failures {failures} — fix, then resume: "
                     f"stack.py --all {'--rebase ' if args.rebase else ''}--from {ordered[0]}")

    print(f"\n[stack] DONE — {len(levels)} levels processed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
