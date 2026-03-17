#!/usr/bin/env bash
# Remodel — re-run index → statements → dafny after an ASN revision.
#
# Usage:
#   ./run/remodel.sh 1
#   ./run/remodel.sh 1 --property TA3,TA3-strict
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 ASN [--property LABEL[,LABEL,...]]" >&2
    exit 1
fi

ASN="$1"
shift

python scripts/model.py index "$ASN" && \
python scripts/model.py statements "$ASN" && \
python scripts/model.py alloy "$ASN" "$@"
