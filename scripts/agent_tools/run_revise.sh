#!/usr/bin/env bash
# Reviser participant — address currently-open revises for the named ASN.
# Files resolution.edit links to the substrate.
#
# Usage: run_revise.sh <asn>
set -euo pipefail
ASN="${1:?usage: run_revise.sh <asn>}"
exec python3 scripts/note-revise.py "$ASN"
