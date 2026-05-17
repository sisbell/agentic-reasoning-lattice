#!/usr/bin/env bash
# Graceful runner shutdown — locates the continuous-runner wrapper and
# its worker children, sends SIGTERM, waits briefly for confirmation.
#
# After the runner's signal-handler upgrade, SIGTERM is graceful: each
# worker finishes its current fire (LLM call, substrate emissions,
# retraction in `finally`, commit-step flush), then exits cleanly.
# No worker-buffer cleanup or stale-holdings retraction is required.
#
# Usage:
#   bash scripts/runner-stop.sh
#
# Exit codes:
#   0 — signaled at least one process
#   1 — no runner found (already stopped, or never started)
#
# For mid-fire abort (skip graceful shutdown): kill -9 the wrapper or
# workers directly. That leaves the same cleanup mess as before this
# script existed.

set -u

# Find the bash wrapper (parent of the workers). Match the path to avoid
# pgrep collisions with other shells; bash continuous-runners run as
# `bash scripts/run-notes-continuous.sh ...`.
mapfile -t wrapper_pids < <(pgrep -f "scripts/run-notes-continuous.sh" || true)

if [[ ${#wrapper_pids[@]} -eq 0 ]]; then
    echo "  [runner-stop] no continuous runner found" >&2
    # Check for orphan workers (note-scheduler without wrapper)
    mapfile -t orphan_workers < <(pgrep -f "scripts/note-scheduler.py" || true)
    if [[ ${#orphan_workers[@]} -gt 0 ]]; then
        echo "  [runner-stop] orphan workers detected:" >&2
        ps -p "${orphan_workers[@]}" -o pid,etime,command >&2
        echo "  [runner-stop] signaling workers directly" >&2
        kill "${orphan_workers[@]}"
        echo "  [runner-stop] workers will finish current fire then exit" >&2
        exit 0
    fi
    exit 1
fi

echo "  [runner-stop] signaling wrapper(s): ${wrapper_pids[*]}" >&2

# SIGTERM the wrapper(s). The wrapper's existing trap forwards SIGTERM
# to its child workers via pkill -P $$. Workers' signal handler flips
# the runner's shutdown flag; current fire completes; workers exit.
kill "${wrapper_pids[@]}"

echo "  [runner-stop] workers will finish their current fire then exit" >&2
echo "  [runner-stop] (current LLM call can be 300-700s; use kill -9 to abort sooner)" >&2
