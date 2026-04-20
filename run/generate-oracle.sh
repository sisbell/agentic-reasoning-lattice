#!/usr/bin/env bash
# Generate Rust oracle from verified Dafny proofs.
#
# Copies proof files to a temp directory, substitutes abstract types
# with concrete ones, runs dafny translate rs, and outputs to lattices/xanadu/implementation/translation/.
#
# Usage: ./scripts/generate-oracle.sh

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
PROOFS="$WORKSPACE/lattices/xanadu/verification/proofs"
ORACLE="$WORKSPACE/lattices/xanadu/implementation/translation"
TMPDIR="$(mktemp -d)"
STAGING="$TMPDIR/lattices/xanadu/verification/proofs"

trap 'rm -rf "$TMPDIR"' EXIT

echo "[ORACLE] Copying proof files..."
mkdir -p "$STAGING"
for dir in TumblerAlgebra TwoSpace TumblerBaptism TumblerOwnership; do
    cp -r "$PROOFS/$dir" "$STAGING/"
done

echo "[ORACLE] Substituting abstract types..."
# type Val(==) → type Val = seq<nat>
sed -i.bak 's/type Val(==)/type Val = seq<nat>/' "$STAGING/TwoSpace/TwoSpace.dfy"
rm -f "$STAGING"/TwoSpace/*.bak

echo "[ORACLE] Collecting source files..."
SOURCES=$(find "$STAGING" -name '*.dfy' | sort)
echo "  $(echo "$SOURCES" | wc -l | tr -d ' ') files"

echo "[ORACLE] Translating to Rust..."
dafny translate rs $SOURCES \
    --output "$ORACLE/xanadu-oracle" \
    --no-verify \
    --enforce-determinism \
    --allow-warnings

echo "[ORACLE] Cleaning source references..."
# Replace messy temp/relative paths with clean lattices/xanadu/verification/proofs/ references
sed -i.bak 's|/// .*/lattices/xanadu/verification/proofs/|/// lattices/xanadu/verification/proofs/|g' "$ORACLE/xanadu-oracle-rust/src/xanadu_oracle.rs"
rm -f "$ORACLE/xanadu-oracle-rust/src/"*.bak

echo "[ORACLE] Generated files:"
find "$ORACLE" -type f | sort

echo "[ORACLE] Done."
