#!/usr/bin/env bash
# Stage all working-tree changes and commit with the given message.
#
# Usage: commit.sh "<message>"
set -euo pipefail
MSG="${1:?usage: commit.sh \"<message>\"}"
git add -A
if git diff --cached --quiet; then
    echo "NOTHING_TO_COMMIT"
    exit 0
fi
git commit -m "$MSG"
echo "COMMITTED"
