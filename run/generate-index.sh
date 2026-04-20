#!/usr/bin/env bash
# Regenerate lattices/xanadu/manifests/index.md from ASN project yamls.
#
# Groups by topic, sorts by ASN number within each group.
# Reads stage, title, depends from each yaml.
# Computes export freshness from file timestamps.
#
# Usage:
#   ./run/generate-index.sh

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
MANIFESTS_DIR="$WORKSPACE/lattices/xanadu/manifests"
INDEX="$MANIFESTS_DIR/index.md"

# Collect data from yamls
declare -a foundations=()
declare -a operations=()

for yaml in "$MANIFESTS_DIR"/ASN-*/note.yaml; do
    [ -f "$yaml" ] || continue

    asn_dir=$(dirname "$yaml")
    label=$(basename "$asn_dir")
    title=$(grep '^title:' "$yaml" | sed 's/title: *"//;s/"//' || true)
    status=$(grep '^stage:' "$yaml" | sed 's/stage: *"//;s/"//' || true)
    topic=$(grep '^topic:' "$yaml" | sed 's/topic: *"//;s/"//' || true)
    deps=$(grep '^depends:' "$yaml" | sed 's/depends: *\[//;s/\]//;s/ //g' || true)

    [ -z "$status" ] && status="—"
    [ -z "$deps" ] && deps="—"

    # Compute export freshness from file timestamps
    asn_file=$(find "$WORKSPACE/lattices/xanadu/discovery/notes" -name "${label}-*.md" -maxdepth 1 2>/dev/null | head -1 || true)
    export_file="$asn_dir/formal-statements.md"

    if [ -z "$asn_file" ]; then
        export_status="—"
    elif [ ! -f "$export_file" ]; then
        export_status="missing"
    else
        asn_ts=$(git log -1 --format=%ct -- "$asn_file" 2>/dev/null || echo "0")
        export_ts=$(git log -1 --format=%ct -- "$export_file" 2>/dev/null || echo "0")
        if [ "$export_ts" -ge "$asn_ts" ]; then
            export_status="current"
        else
            export_status="stale"
        fi
    fi

    line="| $label | $title | $status | $export_status | $deps |"

    if [ "$topic" = "foundation" ]; then
        foundations+=("$line")
    else
        operations+=("$line")
    fi
done

# Write index
cat > "$INDEX" << 'HEADER'
# ASN Index

Generated from lattices/xanadu/manifests/ASN-*/note.yaml — do not edit manually.
Regenerate with: `./run/generate-index.sh`

## Foundation

| ASN | Title | Stage | Export | Depends |
|-----|-------|-------|--------|---------|
HEADER

for line in "${foundations[@]}"; do
    echo "$line" >> "$INDEX"
done

cat >> "$INDEX" << 'HEADER'

## Operations

| ASN | Title | Stage | Export | Depends |
|-----|-------|-------|--------|---------|
HEADER

for line in "${operations[@]}"; do
    echo "$line" >> "$INDEX"
done

echo "" >> "$INDEX"

# Summary
total=$(( ${#foundations[@]} + ${#operations[@]} ))
echo "Generated: $total ASNs (${#foundations[@]} foundation, ${#operations[@]} operations)"
