#!/usr/bin/env bash
# Continuous note-cycle driver.
#
# Loops note-scheduler.py --dag (auto topo-sorted walk of all active
# notes) with git pull/push around each pass.
#
# With --workers N, spawns N parallel schedulers per outer cycle,
# each processing a round-robin partition of the DAG. Workers share
# the same working directory; the substrate's register_path file
# lock + commit_paths declarations + index.lock retry coordinate
# them safely.
#
# Stops only on Ctrl-C.
#
# Requires CLAUDE_CONFIG_DIRS in env for multi-account round-robin +
# quota failover. Example:
#
#   export CLAUDE_CONFIG_DIRS=~/.claude-acct-A,~/.claude-acct-B
#   bash scripts/run-notes-continuous.sh              # single worker
#   bash scripts/run-notes-continuous.sh --workers 4  # 4 parallel partitions
#
# Runtime config — _workspace/runner.env (optional)
#
# To adjust WORKERS or CLAUDE_CONFIG_DIRS without restarting the
# runner, create or edit `_workspace/runner.env`. The file is sourced
# at the top of each outer cycle; changes take effect on the next
# worker spawn (cycle boundary, not mid-scheduler).
#
# Example contents:
#
#   WORKERS=4
#   CLAUDE_CONFIG_DIRS=~/.claude-acct-A,~/.claude-acct-B,~/.claude-acct-C
#
# When the file is absent, the runner uses the CLI args and the
# parent shell's env. Invalid values (non-positive WORKERS, source
# errors) keep the previous values and log a warning.

set -u

cd "$(dirname "$0")/.."

CONFIG_FILE="_workspace/runner.env"

WORKERS=1
while [[ $# -gt 0 ]]; do
    case "$1" in
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        --workers=*)
            WORKERS="${1#*=}"
            shift
            ;;
        *)
            echo "  [run-notes-continuous] unknown arg: $1" >&2
            exit 2
            ;;
    esac
done

if ! [[ "$WORKERS" =~ ^[0-9]+$ ]] || [ "$WORKERS" -lt 1 ]; then
    echo "  [run-notes-continuous] --workers must be a positive integer" >&2
    exit 2
fi

# Load runtime config from `$CONFIG_FILE` if present. Sourced at the
# top of each outer cycle so operators can edit WORKERS /
# CLAUDE_CONFIG_DIRS mid-run; changes take effect on the next spawn.
# Invalid values keep previous values.
_load_runtime_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        return 0
    fi
    local prev_workers="$WORKERS"
    local prev_dirs="${CLAUDE_CONFIG_DIRS:-}"
    # shellcheck disable=SC1090
    if ! source "$CONFIG_FILE" 2>/dev/null; then
        echo "  [runner.env] source failed; keeping WORKERS=$prev_workers, CLAUDE_CONFIG_DIRS=$prev_dirs" >&2
        WORKERS="$prev_workers"
        export CLAUDE_CONFIG_DIRS="$prev_dirs"
        return 0
    fi
    if ! [[ "$WORKERS" =~ ^[0-9]+$ ]] || [ "$WORKERS" -lt 1 ]; then
        echo "  [runner.env] WORKERS=$WORKERS invalid; reverting to $prev_workers" >&2
        WORKERS="$prev_workers"
    fi
    export CLAUDE_CONFIG_DIRS
}

echo "  [run-notes-continuous] startup: WORKERS=$WORKERS CLAUDE_CONFIG_DIRS=${CLAUDE_CONFIG_DIRS:-(unset)}" >&2
if [[ -f "$CONFIG_FILE" ]]; then
    echo "  [run-notes-continuous] runtime config at $CONFIG_FILE will be sourced each cycle" >&2
fi

# Background pusher (one, shared) — pushes any commit landed in the
# working tree every 30s so the remote stays close to laptop's state.
start_pusher() {
    (
        while true; do
            sleep 30
            git push 2>/dev/null || true
        done
    ) &
    PUSHER_PID=$!
}
stop_pusher() {
    if [[ -n "${PUSHER_PID:-}" ]]; then
        kill "$PUSHER_PID" 2>/dev/null || true
        wait "$PUSHER_PID" 2>/dev/null || true
    fi
}

# Clean shutdown — kill the pusher and any in-flight workers when
# Ctrl-C lands.
cleanup() {
    stop_pusher
    # Place the shutdown sentinel so any still-running workers exit
    # gracefully on their next note-review check. No pkill of children
    # — the bash wrapper's `python | tee | sed` pipeline makes signal
    # forwarding unreliable; file-based coordination is the contract.
    touch _workspace/runner.shutdown 2>/dev/null || true
}
trap cleanup EXIT INT TERM

mkdir -p _workspace/logs

# Per-worker substrate-emission buffers. If a prior runner died with
# emissions still in these files (unflushed), discard them — pre-death
# emissions that already made it to canonical are kept (death-cleanup
# tools handle those); pre-death emissions still in pending are
# suspect (failed fire) and we start fresh.
rm -f _workspace/links.worker-*.jsonl

while true; do
    # Honor the file-based shutdown sentinel. If the operator placed
    # `_workspace/runner.shutdown` (e.g., via `scripts/runner-stop.sh`),
    # exit without respawning workers. To resume: run
    # `scripts/runner-resume.sh` to clear the sentinel, then restart
    # this wrapper.
    if [ -f "_workspace/runner.shutdown" ]; then
        echo "  [run-notes-continuous] shutdown sentinel present at" \
             "_workspace/runner.shutdown — exiting without respawn" >&2
        echo "  [run-notes-continuous] to resume: scripts/runner-resume.sh" \
             "then re-run this wrapper" >&2
        exit 0
    fi
    stop_pusher
    git pull --rebase --autostash 2>&1 | grep -v '^$' || true
    _load_runtime_config
    echo "  [run-notes-continuous] cycle: WORKERS=$WORKERS CLAUDE_CONFIG_DIRS=${CLAUDE_CONFIG_DIRS:-(unset)}" >&2

    # Surface orphan holdings before spawning workers. Silent when
    # clean; loud banner + retract commands when stuck. Threshold
    # default (135m) is safely above the 120m subprocess timeout, so
    # a healthy slow revise does not trigger.
    python scripts/diagnostics/stale_holdings.py --quiet || true

    start_pusher

    # Per-cycle timestamp for worker log filenames; keeps history
    # without ever-growing single files.
    ts=$(date +%Y%m%d-%H%M%S)

    # Build optional --exclude arg from EXCLUDE_CLASSES env var (set
    # in runner.env). Empty / unset means no exclusion.
    exclude_args=()
    if [[ -n "${EXCLUDE_CLASSES:-}" ]]; then
        exclude_args=(--exclude "$EXCLUDE_CLASSES")
        echo "  [run-notes-continuous] EXCLUDE_CLASSES=$EXCLUDE_CLASSES" >&2
    fi

    # Spawn workers in parallel. Each runs to outer-fixed-point
    # quiescence on its partition, then exits.
    if [ "$WORKERS" -eq 1 ]; then
        log_file="_workspace/logs/worker-0.$ts.log"
        echo "  [run-notes-continuous] worker 0 → $log_file" >&2
        python scripts/note-scheduler.py --dag "${exclude_args[@]}" 2>&1 \
            | tee -a "$log_file"
        worker_rc=${PIPESTATUS[0]}
        if [ "$worker_rc" -ne 0 ]; then
            echo "" >&2
            echo "  ╔════════════════════════════════════════════════════════════════╗" >&2
            echo "  ║  WORKER 0 CRASHED — exit code $worker_rc" >&2
            echo "  ║  Log: $log_file" >&2
            echo "  ╚════════════════════════════════════════════════════════════════╝" >&2
            echo "" >&2
        fi
    else
        WORKER_PIDS=()
        WORKER_LOGS=()
        for i in $(seq 0 $((WORKERS - 1))); do
            log_file="_workspace/logs/worker-$i.$ts.log"
            WORKER_LOGS+=("$log_file")
            echo "  [run-notes-continuous] worker $i → $log_file" >&2
            CLAUDE_WORKER_INDEX=$i python scripts/note-scheduler.py --dag \
                --partition "$i/$WORKERS" "${exclude_args[@]}" 2>&1 \
                | tee -a "$log_file" \
                | sed "s/^/[w$i] /" &
            WORKER_PIDS+=($!)
        done
        for i in "${!WORKER_PIDS[@]}"; do
            pid="${WORKER_PIDS[$i]}"
            if ! wait "$pid"; then
                rc=$?
                echo "" >&2
                echo "  ╔════════════════════════════════════════════════════════════════╗" >&2
                echo "  ║  WORKER $i CRASHED — exit code $rc" >&2
                echo "  ║  Log: ${WORKER_LOGS[$i]}" >&2
                echo "  ╚════════════════════════════════════════════════════════════════╝" >&2
                echo "" >&2
            fi
        done
    fi

    stop_pusher
    git push 2>&1 | grep -v '^$' || true
    echo "  [LOOP] sleeping 30s before next pass..."
    sleep 30
done
