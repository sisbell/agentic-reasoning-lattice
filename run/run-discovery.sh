#!/usr/bin/env bash
# Run discovery convergence loop — review, then revise until converged.
#
# Usage:
#   ./run/run-discovery.sh ASN [--lattice NAME]
#
# Examples:
#   ./run/run-discovery.sh 2                          # default lattice (xanadu)
#   ./run/run-discovery.sh 2 --lattice materials      # run on the materials lattice
set -euo pipefail

usage() {
    echo "Usage: $0 ASN [--lattice NAME]" >&2
    exit 1
}

ASN=""
LATTICE_ARG=""

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
            echo "Usage: $0 ASN [--lattice NAME]"
            exit 0
            ;;
        --*)
            echo "Unknown option: $1" >&2
            usage
            ;;
        *)
            if [ -z "$ASN" ]; then
                ASN="$1"
            else
                echo "Unexpected argument: $1" >&2
                usage
            fi
            shift
            ;;
    esac
done

[ -n "$ASN" ] || usage

if [ -n "$LATTICE_ARG" ]; then
    export LATTICE="$LATTICE_ARG"
fi

python scripts/discovery-review.py "$ASN"
python scripts/discovery-revise.py "$ASN" --converge
