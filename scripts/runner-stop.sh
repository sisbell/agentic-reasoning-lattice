#!/usr/bin/env bash
# Request graceful runner shutdown via the file-based sentinel.
#
# Runners check `_workspace/runner.shutdown` before each CHAIN-STARTING
# fire — note-review, inquiry-consult, note-draft (note side) and
# cone-review, full-review (claim side, claim-scheduler.py). If present,
# the runner finishes the in-flight fire, commits it, and exits without
# starting a new review/consult/draft chain. Committed work is fully
# resumable; downstream findings/revise from an already-emitted review
# are picked up on the next run.
#
# The bash wrapper (`run-notes-continuous.sh`) also checks the sentinel
# at the top of its outer loop and exits without respawning workers.
#
# NOTE: the sentinel persists until removed. Always run
# `scripts/runner-resume.sh` before starting a new run, or it will shut
# down immediately.
#
# Usage:
#   bash scripts/runner-stop.sh
#
# To resume:
#   bash scripts/runner-resume.sh
#   bash scripts/run-notes-continuous.sh --workers N
#
# No signals, no pkill, no shell tricks. Just a file.

mkdir -p _workspace
touch _workspace/runner.shutdown
echo "  [runner-stop] sentinel placed at _workspace/runner.shutdown" >&2
echo "  [runner-stop] workers will finish the current review→consult→revise" >&2
echo "  [runner-stop] chain, then exit. The bash wrapper exits when its" >&2
echo "  [runner-stop] outer loop sees the sentinel." >&2
echo "  [runner-stop] to resume: bash scripts/runner-resume.sh" >&2
