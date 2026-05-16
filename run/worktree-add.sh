#!/usr/bin/env bash
# Create an isolated worktree for parallel work.
#
# Usage:
#   ./run/worktree-add.sh NAME [--with-harness]
#
# By default, just creates the worktree on branch wt/NAME and inits
# submodules. Use --with-harness when the worktree needs the
# udanax-green test harness built (alloy/dafny generation against
# live backend, golden-test work). Dafny verification of claim files
# does NOT need the harness — skip the flag for that.
set -euo pipefail

with_harness=0
positional=()
while [ $# -gt 0 ]; do
    case "$1" in
        --with-harness)
            with_harness=1
            shift
            ;;
        -h|--help)
            cat <<EOF
Usage: $0 NAME [--with-harness]

Creates worktrees/NAME on a fresh branch wt/NAME.

Options:
  --with-harness   also build the udanax-green test harness
                   (channels/gregory/resources/udanax-test-harness).
                   Slow; skip unless you need it for alloy/golden work.
EOF
            exit 0
            ;;
        *)
            positional+=("$1")
            shift
            ;;
    esac
done

if [ "${#positional[@]}" -lt 1 ]; then
    echo "Usage: $0 NAME [--with-harness]" >&2
    exit 1
fi

name="${positional[0]}"
branch="wt/$name"
wt="worktrees/$name"

if [ -d "$wt" ]; then
    echo "Worktree already exists: $wt" >&2
    exit 1
fi

git worktree add "$wt" -b "$branch" HEAD --quiet
git -C "$wt" submodule update --init --quiet

if [ "$with_harness" -eq 1 ]; then
    harness="$wt/channels/gregory/resources/udanax-test-harness"
    if [ ! -d "$harness" ]; then
        echo "  [WARN] harness dir not found in worktree: $harness" >&2
        echo "  [WARN] worktree created; skipping harness build" >&2
    else
        make -C "$harness" --quiet
        make -C "$harness" golden --quiet
    fi
fi

echo "$wt"
