#!/usr/bin/env bash
# One-time migration: flatten vault/project-model/ and vault/3-export/ into
# per-ASN directories under vault/project-model/ASN-NNNN/.
#
# Uses git mv for history preservation.
#
# Moves:
#   vault/project-model/ASN-NNNN.yaml          → ASN-NNNN/project.yaml
#   vault/project-model/ASN-NNNN-open-issues.md → ASN-NNNN/open-issues.md
#   vault/3-export/ASN-NNNN-statements.md       → ASN-NNNN/formal-statements.md
#   vault/3-export/ASN-NNNN-deps.yaml           → ASN-NNNN/dependency-graph.yaml
#
# Then removes vault/3-export/ and vault/2a-audit/.

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
MODEL_DIR="$WORKSPACE/vault/project-model"
EXPORT_DIR="$WORKSPACE/vault/3-export"
AUDIT_DIR="$WORKSPACE/vault/2a-audit"

cd "$WORKSPACE"

echo "=== Migrating project model to per-ASN directories ==="

# 1. Move project model YAMLs
for yaml in "$MODEL_DIR"/ASN-*.yaml; do
    [ -f "$yaml" ] || continue
    label=$(basename "$yaml" .yaml)
    target_dir="$MODEL_DIR/$label"
    mkdir -p "$target_dir"
    echo "  $label.yaml → $label/project.yaml"
    git mv "$yaml" "$target_dir/project.yaml"
done

# 2. Move open-issues files
for issues in "$MODEL_DIR"/ASN-*-open-issues.md; do
    [ -f "$issues" ] || continue
    label=$(basename "$issues" -open-issues.md)
    target_dir="$MODEL_DIR/$label"
    mkdir -p "$target_dir"
    echo "  $label-open-issues.md → $label/open-issues.md"
    git mv "$issues" "$target_dir/open-issues.md"
done

# 3. Move statement exports
if [ -d "$EXPORT_DIR" ]; then
    for stmt in "$EXPORT_DIR"/ASN-*-statements.md; do
        [ -f "$stmt" ] || continue
        label=$(basename "$stmt" -statements.md)
        target_dir="$MODEL_DIR/$label"
        mkdir -p "$target_dir"
        echo "  3-export/$label-statements.md → $label/formal-statements.md"
        git mv "$stmt" "$target_dir/formal-statements.md"
    done

    # 4. Move deps YAMLs
    for deps in "$EXPORT_DIR"/ASN-*-deps.yaml; do
        [ -f "$deps" ] || continue
        label=$(basename "$deps" -deps.yaml)
        target_dir="$MODEL_DIR/$label"
        mkdir -p "$target_dir"
        echo "  3-export/$label-deps.yaml → $label/dependency-graph.yaml"
        git mv "$deps" "$target_dir/dependency-graph.yaml"
    done

    # 5. Remove vault/3-export/ (should be empty now, maybe .gitkeep left)
    rm -f "$EXPORT_DIR/.gitkeep" 2>/dev/null || true
    if [ -d "$EXPORT_DIR" ]; then
        remaining=$(ls -A "$EXPORT_DIR" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$remaining" = "0" ]; then
            rmdir "$EXPORT_DIR"
            echo "  Removed vault/3-export/"
        else
            echo "  WARNING: vault/3-export/ not empty, skipping removal"
            ls -la "$EXPORT_DIR"
        fi
    fi
fi

# 6. Remove vault/2a-audit/ (empty)
if [ -d "$AUDIT_DIR" ]; then
    git rm -r "$AUDIT_DIR" 2>/dev/null || rm -rf "$AUDIT_DIR"
    echo "  Removed vault/2a-audit/"
fi

echo ""
echo "=== Migration complete ==="
echo ""
echo "Verify with: git status"
echo "Then commit: git commit -m 'refactor(vault): migrate to per-ASN project model directories'"
