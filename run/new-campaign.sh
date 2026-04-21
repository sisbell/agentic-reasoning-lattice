#!/usr/bin/env bash
# Scaffold a new campaign in a lattice.
#
# Usage:
#   ./run/new-campaign.sh --lattice NAME --name CAMPAIGN \
#       --theory CHANNEL --evidence CHANNEL \
#       --target "target description"
#
# Example:
#   ./run/new-campaign.sh --lattice materials \
#       --name dulong-petit-clausius \
#       --theory clausius-1857 \
#       --evidence dulong-petit-1819 \
#       --target "Rediscover DP via Clausius's 1857 kinetic theory"
set -euo pipefail

usage() {
    echo "Usage: $0 --lattice NAME --name CAMPAIGN --theory CHANNEL --evidence CHANNEL --target TEXT" >&2
    exit 1
}

LATTICE_ARG=""
PASSTHROUGH=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --lattice)
            [[ $# -ge 2 ]] || usage
            LATTICE_ARG="$2"
            shift 2
            ;;
        --lattice=*)
            LATTICE_ARG="${1#--lattice=}"
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            PASSTHROUGH+=("$1")
            shift
            ;;
    esac
done

if [ -n "$LATTICE_ARG" ]; then
    export LATTICE="$LATTICE_ARG"
fi

python scripts/new-campaign.py "${PASSTHROUGH[@]}"
