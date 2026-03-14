#!/usr/bin/env bash
# Remove a worktree and its branch.
#
# Usage:
#   ./run/worktree-remove.sh alloy-asn2
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME" >&2
    exit 1
fi

name="$1"
branch="wt/$name"
wt="worktrees/$name"

if [ -d "$wt" ]; then
    git worktree remove "$wt" --force
fi

if git rev-parse --verify "$branch" >/dev/null 2>&1; then
    git branch -d "$branch"
fi
