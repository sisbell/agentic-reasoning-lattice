#!/usr/bin/env bash
# Merge a worktree branch back into current branch.
#
# Usage:
#   ./run/worktree-merge.sh alloy-asn2
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME" >&2
    exit 1
fi

name="$1"
branch="wt/$name"

if ! git rev-parse --verify "$branch" >/dev/null 2>&1; then
    echo "Branch not found: $branch" >&2
    exit 1
fi

git merge --no-edit "$branch"
