#!/usr/bin/env bash
# Create an isolated worktree for parallel work.
#
# Usage:
#   ./run/worktree-add.sh alloy-asn2
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME" >&2
    exit 1
fi

name="$1"
branch="wt/$name"
wt="worktrees/$name"

if [ -d "$wt" ]; then
    echo "Worktree already exists: $wt" >&2
    exit 1
fi

git worktree add "$wt" -b "$branch" HEAD --quiet
echo "$wt"
