#!/usr/bin/env bash
# Scaffold a new lattice directory.
#
# Usage:
#   ./run/new-lattice.sh --name NAME
#
# Example:
#   ./run/new-lattice.sh --name materials
set -euo pipefail

python3 scripts/new-lattice.py "$@"
