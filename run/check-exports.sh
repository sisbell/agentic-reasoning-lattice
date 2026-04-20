#!/usr/bin/env bash
# Check which ASNs have stale or missing exports.
#
# Compares the last git commit timestamp of each active ASN's reasoning
# doc against its export file. Lists any where the export is older than
# the reasoning doc or missing entirely.
#
# Usage:
#   ./scripts/check-exports.sh

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
INDEX="$WORKSPACE/lattices/xanadu/project-model/index.md"

# Extract active ASN numbers from index (skip deprecated/absorbed/dormant)
active_asns=$(grep -E '^\| ASN-[0-9]+' "$INDEX" \
    | grep -v '~~' \
    | grep -v 'dormant' \
    | sed -E 's/^\| (ASN-[0-9]+).*/\1/' \
    | sort)

stale=0
missing=0
ok=0

printf "\n  %-12s %-30s %-20s %-20s %s\n" "ASN" "Title" "Reasoning Doc" "Export" "Status"
printf "  %-12s %-30s %-20s %-20s %s\n" "---" "-----" "-------------" "------" "------"

for label in $active_asns; do
    # Find reasoning doc
    asn_file=$(ls "$WORKSPACE/lattices/xanadu/discovery/notes/${label}-"*.md 2>/dev/null | head -1)
    if [ -z "$asn_file" ]; then
        continue
    fi

    # Get title from index
    title=$(grep "$label" "$INDEX" | head -1 | sed -E 's/.*\| ([^|]+) \|.*/\1/' | xargs)

    # Get last commit timestamp for reasoning doc
    asn_ts=$(git -C "$WORKSPACE" log -1 --format="%ct" -- "$asn_file" 2>/dev/null || echo "0")
    asn_date=$(git -C "$WORKSPACE" log -1 --format="%ci" -- "$asn_file" 2>/dev/null | cut -d' ' -f1,2 | cut -c1-16 || echo "none")

    # Find export file
    export_file="$WORKSPACE/lattices/xanadu/project-model/${label}/formal-statements.md"

    if [ ! -f "$export_file" ]; then
        printf "  %-12s %-30s %-20s %-20s %s\n" "$label" "$title" "$asn_date" "—" "MISSING"
        missing=$((missing + 1))
        continue
    fi

    # Get last commit timestamp for export
    export_ts=$(git -C "$WORKSPACE" log -1 --format="%ct" -- "$export_file" 2>/dev/null || echo "0")
    export_date=$(git -C "$WORKSPACE" log -1 --format="%ci" -- "$export_file" 2>/dev/null | cut -d' ' -f1,2 | cut -c1-16 || echo "none")

    if [ "$export_ts" -lt "$asn_ts" ]; then
        printf "  %-12s %-30s %-20s %-20s %s\n" "$label" "$title" "$asn_date" "$export_date" "STALE"
        stale=$((stale + 1))
    else
        printf "  %-12s %-30s %-20s %-20s %s\n" "$label" "$title" "$asn_date" "$export_date" "OK"
        ok=$((ok + 1))
    fi
done

printf "\n  Summary: %d OK, %d STALE, %d MISSING\n\n" "$ok" "$stale" "$missing"

if [ $stale -gt 0 ] || [ $missing -gt 0 ]; then
    echo "  To fix stale/missing exports:"
    echo "  python scripts/normalize.py <ASN_NUMBER> [<ASN_NUMBER> ...]"
    echo ""
fi
