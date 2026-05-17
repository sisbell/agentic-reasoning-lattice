#!/usr/bin/env bash
# Request graceful runner shutdown via the file-based sentinel.
#
# Workers check `_workspace/runner.shutdown` before each note-review
# fire. If present, they exit without starting a new review cycle —
# in-flight consult/revise fires complete naturally (their predicates
# remain True while their work exists), so the worker finishes the
# current review→consult→revise chain cleanly before exiting.
#
# The bash wrapper (`run-notes-continuous.sh`) also checks the sentinel
# at the top of its outer loop and exits without respawning workers.
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
