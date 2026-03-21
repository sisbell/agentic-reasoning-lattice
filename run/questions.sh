#!/usr/bin/env bash
# Generate consultation questions for an ASN.
#
# Usage:
#   ./run/questions.sh 58
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 ASN" >&2
    exit 1
fi

ASN="$1"

python scripts/draft.py questions --inquiries "$ASN"
