#!/usr/bin/env bash
# Converge — run the claim-convergence pipeline on an ASN.
#
# Runs each stage to internal convergence in sequence:
#   converge → contract-review → dependency-review → full-review → contract-review
#
# Usage:
#   ./run/converge.sh 40                       # full pipeline, 1 cycle
#   ./run/converge.sh 40 3                     # full pipeline, 3 cycles
#   ./run/converge.sh --from dependency-review 40      # start at dependency-check
#   ./run/converge.sh --from full-review 40 2  # start at full-review, 2 cycles

set -euo pipefail

FROM=""

while [[ "${1:-}" == --* ]]; do
    case "$1" in
        --from) FROM="$2"; shift 2 ;;
        *) echo "Unknown flag: $1" >&2; exit 1 ;;
    esac
done

if [ $# -lt 1 ]; then
    echo "Usage: $0 [--from STEP] ASN [CYCLES]" >&2
    echo "Steps: converge, contract-review, dependency-review, full-review" >&2
    exit 1
fi

ASN="$1"
CYCLES="${2:-1}"

for i in $(seq 1 "$CYCLES"); do
    if [ "$CYCLES" -gt 1 ]; then
        echo ""
        echo "  =================================================="
        echo "  Claim convergence cycle $i/$CYCLES — ASN $ASN"
        echo "  =================================================="
        echo ""
    fi

    case "${FROM:-converge}" in
        converge)
            python scripts/converge.py "$ASN" &&
            python scripts/contract-review.py "$ASN" &&
            python scripts/dependency-review.py "$ASN" &&
            python scripts/full-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        contract-review)
            python scripts/contract-review.py "$ASN" &&
            python scripts/dependency-review.py "$ASN" &&
            python scripts/full-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        dependency-review)
            python scripts/dependency-review.py "$ASN" &&
            python scripts/full-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        full-review)
            python scripts/full-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        contract-review-final)
            python scripts/contract-review.py "$ASN"
            ;;
        *)
            echo "Unknown step: $FROM" >&2
            echo "Valid: converge, contract-review, dependency-review, full-review" >&2
            exit 1
            ;;
    esac
done
