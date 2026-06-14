#!/usr/bin/env python3
"""Batch runner for design-digest over the asn-classes.yaml note set.

Runs design-digest.py per ASN — independent, resumable, parallel across
N workers, with account rotation (CLAUDE_CONFIG_DIRS, same as the note
runner). One note's failure never stops the batch.

    python scripts/design-digest-run.py --dry-run
    python scripts/design-digest-run.py --workers 4 --max-reviews 2
    python scripts/design-digest-run.py --classes operations --workers 3 --max-reviews 3

Parallel safety: each worker is a separate design-digest.py process;
their git commits serialize through a shared file lock, while the LLM
calls run fully in parallel. Account rotation is read from
_workspace/runner.env (CLAUDE_CONFIG_DIRS) unless already in the env,
and invoke_claude load-balances calls across those accounts.

Run standalone — keep the substrate note runner off (both commit).
"""

import argparse
import os
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

_print_lock = threading.Lock()  # keep parallel-worker lines from garbling

ROOT = Path(__file__).resolve().parent.parent
CLASSES_YAML = ROOT / "_workspace/design-classes.yaml"      # design pipeline's own list
FALLBACK_CLASSES = ROOT / "_workspace/asn-classes.yaml"     # if design list absent
DESIGN_ENV = ROOT / "_workspace/design-runner.env"
RUNNER_ENV = ROOT / "_workspace/runner.env"
DIGEST = ROOT / "scripts/design-digest.py"
LOGS = ROOT / "_workspace/logs"
STOP_FLAG = ROOT / "_workspace/design-digest.stop"


def _load_env(path):
    """Parse a KEY=VALUE env file (# comments, blank lines ignored)."""
    cfg = {}
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    return cfg


def _config_dirs(cfg):
    """CLAUDE_CONFIG_DIRS: design-runner.env, else runner.env, expanded."""
    val = cfg.get("CLAUDE_CONFIG_DIRS") or _load_env(RUNNER_ENV).get("CLAUDE_CONFIG_DIRS")
    return os.path.expandvars(val) if val else None


def _quiescent_subset(asns):
    """Partition into (ready, skipped). ready = the note has been reviewed
    AND has no pending revise work (is_doc_quiescent) — i.e. settled, not
    something the note runner is mid-cycle on. Read-only substrate query;
    safe to run while the runner is active (paths.json writes are atomic,
    links.jsonl is append-only, so a read sees a consistent snapshot)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from lib.protocols.febe.session import open_session
    from lib.predicates import has_been_reviewed, is_doc_quiescent
    from lib.shared.paths import LATTICE
    ready, skipped = [], []
    with open_session(LATTICE) as s:
        by_asn = {}
        for p, a in s.store.path_to_addr.items():
            m = re.search(r"/note/ASN-(\d+)-", p)
            if m and ".statements." not in p:
                by_asn.setdefault(int(m.group(1)), a)
        for n in asns:
            a = by_asn.get(n)
            if a is None:
                skipped.append((n, "no note"))
            elif has_been_reviewed(s, a) and is_doc_quiescent(s, a):
                ready.append(n)
            else:
                skipped.append((n, "not quiescent (runner working / unreviewed)"))
    return ready, skipped


def main():
    cfg = _load_env(DESIGN_ENV)  # defaults from _workspace/design-runner.env
    ap = argparse.ArgumentParser(
        description="Run design-digest over asn-classes.yaml "
                    "(defaults from _workspace/design-runner.env; CLI overrides).")
    ap.add_argument("--classes", default=cfg.get("CLASSES") or None,
                    help="comma-list of classes to include (default: all)")
    ap.add_argument("--exclude", default=cfg.get("EXCLUDE") or None,
                    help="comma-list of classes to skip")
    ap.add_argument("--workers", type=int, default=int(cfg.get("WORKERS", 3)),
                    help="parallel ASNs")
    ap.add_argument("--max-reviews", type=int, default=int(cfg.get("MAX_REVIEWS", 8)),
                    help="hard cap per note (backstop); the loop stops earlier at "
                         "2 consecutive CONVERGED reviews")
    ap.add_argument("--effort", default=cfg.get("EFFORT", "max"))
    ap.add_argument("--force", action="store_true",
                    help="skip the quiescence filter — digest every listed note "
                         "even if the runner is mid-cycle on it")
    ap.add_argument("--no-commit", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="print the ASN list and exit")
    ap.add_argument("--stop", action="store_true",
                    help="signal a graceful shutdown of a running batch: in-flight "
                         "notes finish their current review/revise cycle and commit, "
                         "queued notes never launch, then the batch drains. Sets the "
                         "stop flag and exits; the next normal run clears it.")
    args = ap.parse_args()

    if args.stop:
        STOP_FLAG.parent.mkdir(parents=True, exist_ok=True)
        STOP_FLAG.touch()
        print(f"[run] stop requested — wrote {STOP_FLAG.relative_to(ROOT)}. "
              f"In-flight notes finish their current cycle and commit, then exit; "
              f"queued notes drain without launching. Re-run normally to resume "
              f"(a fresh run clears the flag and continues from committed state).",
              file=sys.stderr)
        return

    classes_file = CLASSES_YAML if CLASSES_YAML.exists() else FALLBACK_CLASSES
    data = yaml.safe_load(classes_file.read_text())
    include = set(args.classes.split(",")) if args.classes else set(data)
    exclude = set(args.exclude.split(",")) if args.exclude else set()
    asns = sorted({int(n) for cls, members in data.items()
                   if cls in include and cls not in exclude
                   for n in members})

    # Digest only settled notes (skip whatever the note runner is still
    # working on); --force overrides. Coexists with the runner — design
    # commits retry through its index.lock.
    if args.force:
        skipped = []
    else:
        asns, skipped = _quiescent_subset(asns)
    for n, why in skipped:
        print(f"[run] skip ASN-{n:04d} — {why}", file=sys.stderr)

    env = os.environ.copy()
    dirs = _config_dirs(cfg)
    if dirs and not env.get("CLAUDE_CONFIG_DIRS"):
        env["CLAUDE_CONFIG_DIRS"] = dirs
    n_accounts = len(env.get("CLAUDE_CONFIG_DIRS", "").split(",")) if env.get("CLAUDE_CONFIG_DIRS") else 1

    print(f"[run] classes {sorted(include - exclude)} → {len(asns)} ready "
          f"({len(skipped)} skipped): {asns}", file=sys.stderr)
    print(f"[run] workers={args.workers} accounts={n_accounts} effort={args.effort} "
          f"max-reviews={args.max_reviews} commit={not args.no_commit}", file=sys.stderr)
    print(f"[run] graceful stop: `python scripts/design-digest-run.py --stop` "
          f"— in-flight notes finish their cycle and commit, the rest drain",
          file=sys.stderr)
    if args.dry_run:
        return

    # A fresh batch starts clean: clear any stale stop flag left by a prior
    # drain so this run isn't aborted by a leftover sentinel.
    STOP_FLAG.unlink(missing_ok=True)

    LOGS.mkdir(parents=True, exist_ok=True)

    def run_one(n):
        if STOP_FLAG.exists():
            return n, 0, None  # drained: stop signalled before this note launched
        log = LOGS / f"design-digest-ASN-{n:04d}.log"
        cmd = [sys.executable, str(DIGEST), "--asn", str(n),
               "--max-reviews", str(args.max_reviews), "--effort", args.effort]
        if args.no_commit:
            cmd.append("--no-commit")
        # Tee the subprocess output to stdout (live) AND the per-ASN log.
        # Prefix with the ASN only when running parallel, so a single-worker
        # run reads as a clean stream.
        prefix = f"[{n:04d}] " if args.workers > 1 else ""
        p = subprocess.Popen(cmd, cwd=ROOT, env=env, text=True, bufsize=1,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(log, "w") as lf:
            for line in p.stdout:
                lf.write(line)
                with _print_lock:
                    sys.stdout.write(prefix + line)
                    sys.stdout.flush()
        rc = p.wait()
        return n, rc, log

    ok, failed, drained = [], [], []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_one, n): n for n in asns}
        for i, fut in enumerate(as_completed(futs), 1):
            n, rc, log = fut.result()
            if log is None:
                drained.append(n)
                print(f"[run] ({i}/{len(asns)}) ASN-{n:04d} drained "
                      f"(stop signalled — not launched)", file=sys.stderr)
                continue
            (ok if rc == 0 else failed).append(n)
            print(f"[run] ({i}/{len(asns)}) ASN-{n:04d} {'ok' if rc == 0 else 'FAILED'} "
                  f"(rc={rc}) — {log.relative_to(ROOT)}", file=sys.stderr)

    print(f"\n[run] done. ok={len(ok)} failed={len(failed)} drained={len(drained)}",
          file=sys.stderr)
    if failed:
        print(f"[run] failed (no note yet / error): {sorted(failed)}", file=sys.stderr)
    if STOP_FLAG.exists():
        print(f"[run] stopped early by --stop (flag still set). Re-run normally to "
              f"resume — it clears the flag and continues from committed state.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
