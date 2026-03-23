#!/usr/bin/env bash
# Regenerate vault/project-model/index.md from ASN yaml files.
#
# Groups by topic, sorts by ASN number within each group.
# Reads status, title, depends from each yaml.
# Computes export freshness from file timestamps.
#
# Usage:
#   ./run/generate-index.sh

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
MODEL_DIR="$WORKSPACE/vault/project-model"
INDEX="$MODEL_DIR/index.md"

# Collect data from yamls
declare -a foundations=()
declare -a operations=()

for yaml in "$MODEL_DIR"/ASN-*.yaml; do
    [ -f "$yaml" ] || continue

    label=$(basename "$yaml" .yaml)
    title=$(grep '^title:' "$yaml" | sed 's/title: *"//;s/"//' || true)
    status=$(grep '^status:' "$yaml" | sed 's/status: *"//;s/"//' || true)
    topic=$(grep '^topic:' "$yaml" | sed 's/topic: *"//;s/"//' || true)
    deps=$(grep '^depends:' "$yaml" | sed 's/depends: *\[//;s/\]//;s/ //g' || true)

    [ -z "$status" ] && status="—"
    [ -z "$deps" ] && deps="—"

    # Compute export freshness from file timestamps
    asn_file=$(find "$WORKSPACE/vault/1-reasoning-docs" -name "${label}-*.md" -maxdepth 1 2>/dev/null | head -1 || true)
    export_file="$WORKSPACE/vault/3-export/${label}-statements.md"

    if [ -z "$asn_file" ]; then
        export_status="—"
    elif [ ! -f "$export_file" ]; then
        export_status="missing"
    else
        asn_ts=$(stat -f %m "$asn_file" 2>/dev/null || echo "0")
        export_ts=$(stat -f %m "$export_file" 2>/dev/null || echo "0")
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

Generated from vault/project-model/ASN-*.yaml — do not edit manually.
Regenerate with: `./run/generate-index.sh`

## Foundation

| ASN | Title | Status | Export | Depends |
|-----|-------|--------|--------|---------|
HEADER

for line in "${foundations[@]}"; do
    echo "$line" >> "$INDEX"
done

cat >> "$INDEX" << 'HEADER'

## Operations

| ASN | Title | Status | Export | Depends |
|-----|-------|--------|--------|---------|
HEADER

for line in "${operations[@]}"; do
    echo "$line" >> "$INDEX"
done

echo "" >> "$INDEX"

# Summary
total=$(( ${#foundations[@]} + ${#operations[@]} ))
echo "Generated: $total ASNs (${#foundations[@]} foundation, ${#operations[@]} operations)"
