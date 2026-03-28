#!/usr/bin/env bash
# Converge — review then revise until converged.
#
# Usage:
#   ./run/asn-converge.sh 2
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 ASN" >&2
    exit 1
fi

python scripts/discover.py "$1"
python scripts/discover.py "$1" --converge
