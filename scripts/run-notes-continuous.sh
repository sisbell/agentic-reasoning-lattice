#!/usr/bin/env bash
# Continuous note-cycle driver.
#
# Loops note-scheduler.py --dag (auto topo-sorted walk of all active
# notes) with git pull/push around each pass. Designed for the
# "notes machine" in the two-machine split — runs continuously,
# picks up cross-machine substrate updates each pass via git pull,
# stops only on Ctrl-C.
#
# Requires CLAUDE_CONFIG_DIRS in env for 2-account round-robin +
# quota failover. Example:
#
#   export CLAUDE_CONFIG_DIRS=~/.claude-acct-A,~/.claude-acct-B
#   bash scripts/run-notes-continuous.sh

set -u

cd "$(dirname "$0")/.."

# Background pusher — runs every 30s while the scheduler is alive so
# each auto-commit (one per fire, ~5min cadence) is visible on the
# remote within 30s. Killed before each outer pull/pass and respawned.
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
trap stop_pusher EXIT

while true; do
    stop_pusher
    git pull --rebase --autostash 2>&1 | grep -v '^$' || true
    start_pusher
    python scripts/note-scheduler.py --dag
    stop_pusher
    git push 2>&1 | grep -v '^$' || true
    echo "  [LOOP] sleeping 30s before next pass..."
    sleep 30
done
