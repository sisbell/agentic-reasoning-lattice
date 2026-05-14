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

while true; do
    git pull --rebase --autostash 2>&1 | grep -v '^$' || true
    python scripts/note-scheduler.py --dag
    git push 2>&1 | grep -v '^$' || true
    echo "  [LOOP] sleeping 30s before next pass..."
    sleep 30
done
