#!/usr/bin/env bash
# Continuous claim-cycle driver.
#
# Sibling of run-notes-continuous.sh — same wrapper shape, different
# scheduler. Loops claim-scheduler.py --dag (auto topo-sorted walk of
# all decomposed ASNs) with git pull/push around each pass.
#
# With --workers N, spawns N parallel schedulers per outer cycle, each
# processing a round-robin partition of the DAG. Workers share the
# same working directory; the substrate's register_path file lock +
# commit_paths declarations + index.lock retry coordinate them safely.
# Runs concurrently with run-notes-continuous.sh on the same checkout
# — claim-side and note-side scope_paths don't overlap (different
# document-type subdirs), and substrate writes share the same flock.
#
# Stops only on Ctrl-C or when _workspace/runner.shutdown is touched.
#
# Requires CLAUDE_CONFIG_DIRS in env for multi-account round-robin +
# quota failover. Example:
#
#   export CLAUDE_CONFIG_DIRS=~/.claude-acct-A,~/.claude-acct-B
#   bash scripts/run-claims-continuous.sh              # single worker
#   bash scripts/run-claims-continuous.sh --workers 4  # 4 parallel partitions
#
# Runtime config — _workspace/runner.env (optional). Same file the
# note runner reads. WORKERS / CLAUDE_CONFIG_DIRS / EXCLUDE_CLASSES
# apply uniformly to both runners.

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
            echo "  [run-claims-continuous] unknown arg: $1" >&2
            exit 2
            ;;
    esac
done

if ! [[ "$WORKERS" =~ ^[0-9]+$ ]] || [ "$WORKERS" -lt 1 ]; then
    echo "  [run-claims-continuous] --workers must be a positive integer" >&2
    exit 2
fi

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
    [[ -n "${MAX_REVIEWS:-}" ]] && export MAX_REVIEWS
}

echo "  [run-claims-continuous] startup: WORKERS=$WORKERS CLAUDE_CONFIG_DIRS=${CLAUDE_CONFIG_DIRS:-(unset)} MAX_REVIEWS=${MAX_REVIEWS:-(unset)}" >&2
if [[ -f "$CONFIG_FILE" ]]; then
    echo "  [run-claims-continuous] runtime config at $CONFIG_FILE will be sourced each cycle" >&2
fi

# Background pusher — independent from the note runner's pusher; both
# can run safely (each git push is idempotent if the remote is current).
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

# Clean shutdown — same file-based sentinel the note runner uses, so
# a single `runner-stop.sh` invocation stops both.
cleanup() {
    stop_pusher
    touch _workspace/runner.shutdown 2>/dev/null || true
}
trap cleanup EXIT INT TERM

mkdir -p _workspace/logs

# Worker-index offset for claims. Notes runner uses CLAUDE_WORKER_INDEX
# starting from 0; claims uses 100+ so the per-worker substrate-emission
# pending files (_workspace/links.worker-N.jsonl) don't collide. Without
# the offset, claims worker 0 and notes worker 0 would both append to
# links.worker-0.jsonl, and commit_after_fire's _flush_pending_jsonl
# would commit one runner's in-flight emissions under the other
# runner's fire — silent data loss for the loser.
CLAIM_WORKER_INDEX_OFFSET=100

# Per-worker substrate-emission buffers from prior CLAIM runs only —
# discard any unflushed pending in the claims index range. Notes' files
# (links.worker-0..N) are left intact in case the notes runner is
# concurrently active. Range 100-199 supports up to 100 claim workers.
for f in _workspace/links.worker-1[0-9][0-9].jsonl; do
    [ -e "$f" ] && rm -f "$f"
done

# One-time startup cleanup: retract stale holdings from prior runner
# sessions of either runner (notes or claims). Both runners emit
# holdings of the same shape; one cleanup serves both.
echo "  [run-claims-continuous] cleaning stale holdings from prior runs..." >&2
python scripts/diagnostics/stale_holdings.py --retract-all || true

while true; do
    if [ -f "_workspace/runner.shutdown" ]; then
        echo "  [run-claims-continuous] shutdown sentinel present at" \
             "_workspace/runner.shutdown — exiting without respawn" >&2
        echo "  [run-claims-continuous] to resume: scripts/runner-resume.sh" \
             "then re-run this wrapper" >&2
        exit 0
    fi
    stop_pusher
    git pull --rebase --autostash 2>&1 | grep -v '^$' || true
    _load_runtime_config
    echo "  [run-claims-continuous] cycle: WORKERS=$WORKERS CLAUDE_CONFIG_DIRS=${CLAUDE_CONFIG_DIRS:-(unset)} MAX_REVIEWS=${MAX_REVIEWS:-(unset)}" >&2

    python scripts/diagnostics/stale_holdings.py --quiet || true

    start_pusher

    ts=$(date +%Y%m%d-%H%M%S)

    exclude_args=()
    if [[ -n "${EXCLUDE_CLASSES:-}" ]]; then
        exclude_args=(--exclude "$EXCLUDE_CLASSES")
        echo "  [run-claims-continuous] EXCLUDE_CLASSES=$EXCLUDE_CLASSES" >&2
    fi

    if [ "$WORKERS" -eq 1 ]; then
        log_file="_workspace/logs/claim-worker-0.$ts.log"
        widx=$((CLAIM_WORKER_INDEX_OFFSET))
        echo "  [run-claims-continuous] worker 0 (idx=$widx) → $log_file" >&2
        CLAUDE_WORKER_INDEX=$widx python scripts/claim-scheduler.py --dag \
            ${exclude_args[@]+"${exclude_args[@]}"} 2>&1 \
            | tee -a "$log_file"
        worker_rc=${PIPESTATUS[0]}
        if [ "$worker_rc" -ne 0 ]; then
            echo "" >&2
            echo "  ╔════════════════════════════════════════════════════════════════╗" >&2
            echo "  ║  CLAIM WORKER 0 CRASHED — exit code $worker_rc" >&2
            echo "  ║  Log: $log_file" >&2
            echo "  ╚════════════════════════════════════════════════════════════════╝" >&2
            echo "" >&2
        fi
    else
        WORKER_PIDS=()
        WORKER_LOGS=()
        for i in $(seq 0 $((WORKERS - 1))); do
            log_file="_workspace/logs/claim-worker-$i.$ts.log"
            WORKER_LOGS+=("$log_file")
            widx=$((CLAIM_WORKER_INDEX_OFFSET + i))
            echo "  [run-claims-continuous] worker $i (idx=$widx) → $log_file" >&2
            CLAUDE_WORKER_INDEX=$widx python scripts/claim-scheduler.py --dag \
                --partition "$i/$WORKERS" ${exclude_args[@]+"${exclude_args[@]}"} 2>&1 \
                | tee -a "$log_file" \
                | sed "s/^/[cw$i] /" &
            WORKER_PIDS+=($!)
        done
        for i in "${!WORKER_PIDS[@]}"; do
            pid="${WORKER_PIDS[$i]}"
            if ! wait "$pid"; then
                rc=$?
                echo "" >&2
                echo "  ╔════════════════════════════════════════════════════════════════╗" >&2
                echo "  ║  CLAIM WORKER $i CRASHED — exit code $rc" >&2
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
