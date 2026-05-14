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

set -u

cd "$(dirname "$0")/.."

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

echo "  [run-notes-continuous] WORKERS=$WORKERS CLAUDE_CONFIG_DIRS=${CLAUDE_CONFIG_DIRS:-(unset)}" >&2

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
    # SIGTERM all children of this shell
    pkill -P $$ 2>/dev/null || true
}
trap cleanup EXIT INT TERM

while true; do
    stop_pusher
    git pull --rebase --autostash 2>&1 | grep -v '^$' || true
    start_pusher

    # Spawn workers in parallel. Each runs to outer-fixed-point
    # quiescence on its partition, then exits.
    if [ "$WORKERS" -eq 1 ]; then
        python scripts/note-scheduler.py --dag
    else
        WORKER_PIDS=()
        for i in $(seq 0 $((WORKERS - 1))); do
            python scripts/note-scheduler.py --dag \
                --partition "$i/$WORKERS" 2>&1 \
                | sed "s/^/[w$i] /" &
            WORKER_PIDS+=($!)
        done
        for pid in "${WORKER_PIDS[@]}"; do
            wait "$pid"
        done
    fi

    stop_pusher
    git push 2>&1 | grep -v '^$' || true
    echo "  [LOOP] sleeping 30s before next pass..."
    sleep 30
done
