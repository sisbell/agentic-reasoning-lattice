#!/usr/bin/env bash
# Regenerate vault/project-model/index.md from ASN yaml files.
#
# Groups by topic, sorts by ASN number within each group.
# Reads status, title, depends from each yaml.
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

    line="| $label | $title | $status | $deps |"

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

| ASN | Title | Status | Depends |
|-----|-------|--------|---------|
HEADER

for line in "${foundations[@]}"; do
    echo "$line" >> "$INDEX"
done

cat >> "$INDEX" << 'HEADER'

## Operations

| ASN | Title | Status | Depends |
|-----|-------|--------|---------|
HEADER

for line in "${operations[@]}"; do
    echo "$line" >> "$INDEX"
done

echo "" >> "$INDEX"

# Summary
total=$(( ${#foundations[@]} + ${#operations[@]} ))
echo "Generated: $total ASNs (${#foundations[@]} foundation, ${#operations[@]} operations)"
