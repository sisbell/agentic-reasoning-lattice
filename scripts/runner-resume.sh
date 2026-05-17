#!/usr/bin/env bash
# Clear the shutdown sentinel so the runner can be (re)started.
#
# Removes `_workspace/runner.shutdown` if present. After running this,
# start the continuous runner normally:
#   bash scripts/run-notes-continuous.sh --workers N
#
# Companion to `scripts/runner-stop.sh`.

if [ -f "_workspace/runner.shutdown" ]; then
    rm -f _workspace/runner.shutdown
    echo "  [runner-resume] sentinel cleared" >&2
else
    echo "  [runner-resume] no sentinel present (already clear)" >&2
fi
echo "  [runner-resume] start the runner with:" >&2
echo "  [runner-resume]   bash scripts/run-notes-continuous.sh --workers N" >&2
