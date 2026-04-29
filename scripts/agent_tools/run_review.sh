#!/usr/bin/env bash
# Reviewer participant — run one review pass on the named ASN.
# Files comment.revise and comment.out-of-scope links to the substrate.
#
# Usage: run_review.sh <asn>
set -euo pipefail
ASN="${1:?usage: run_review.sh <asn>}"
exec python3 scripts/note-review.py "$ASN"
