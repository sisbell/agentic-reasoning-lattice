#!/usr/bin/env bash
# Build the prompt for the note-convergence driver agent.
# Prints the prompt path; user runs claude themselves with the prompt.
#
# Usage:
#   LATTICE=materials ./run/agent-note-converge.sh 1
set -euo pipefail
exec python3 scripts/agent-note-converge.py "$@"
