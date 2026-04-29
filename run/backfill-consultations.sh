#!/usr/bin/env bash
# Backfill consultation substrate classifiers for the active lattice.
#
# Usage:
#   LATTICE=xanadu    ./run/backfill-consultations.sh             # default --min-asn 34
#   LATTICE=materials ./run/backfill-consultations.sh --min-asn 1
#   LATTICE=xanadu    ./run/backfill-consultations.sh --dry-run
set -euo pipefail
exec python3 scripts/migration_tools/backfill-consultations.py "$@"
