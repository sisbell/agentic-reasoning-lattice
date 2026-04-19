#!/usr/bin/env bash
# Formalize — run the full formalization pipeline on an ASN.
#
# Runs each stage to internal convergence in sequence:
#   formalize → contract-review → dependency-review → full-review → local-review → contract-review
#
# Usage:
#   ./run/formalize.sh 40                       # full pipeline, 1 cycle
#   ./run/formalize.sh 40 3                     # full pipeline, 3 cycles
#   ./run/formalize.sh --from dependency-review 40      # start at dependency-check
#   ./run/formalize.sh --from full-review 40 2  # start at full-review, 2 cycles

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
    echo "Steps: formalize, dependency-review, full-review, local-review" >&2
    exit 1
fi

ASN="$1"
CYCLES="${2:-1}"

for i in $(seq 1 "$CYCLES"); do
    if [ "$CYCLES" -gt 1 ]; then
        echo ""
        echo "  =================================================="
        echo "  Formalization cycle $i/$CYCLES — ASN $ASN"
        echo "  =================================================="
        echo ""
    fi

    case "${FROM:-formalize}" in
        formalize)
            python scripts/formalize.py "$ASN" &&
            python scripts/contract-review.py "$ASN" &&
            python scripts/dependency-review.py "$ASN" &&
            python scripts/full-review.py "$ASN" &&
            python scripts/local-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        contract-review)
            python scripts/contract-review.py "$ASN" &&
            python scripts/dependency-review.py "$ASN" &&
            python scripts/full-review.py "$ASN" &&
            python scripts/local-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        dependency-review)
            python scripts/dependency-review.py "$ASN" &&
            python scripts/full-review.py "$ASN" &&
            python scripts/local-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        full-review)
            python scripts/full-review.py "$ASN" &&
            python scripts/local-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        local-review)
            python scripts/local-review.py "$ASN" &&
            python scripts/contract-review.py "$ASN"
            ;;
        contract-review-final)
            python scripts/contract-review.py "$ASN"
            ;;
        *)
            echo "Unknown step: $FROM" >&2
            echo "Valid: formalize, contract-review, dependency-review, full-review, local-review" >&2
            exit 1
            ;;
    esac
done
