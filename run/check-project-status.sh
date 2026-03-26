#!/usr/bin/env bash
# Check ASN health: stale exports and stale dependencies.
#
# For each active ASN shows:
#   - When the ASN was last updated
#   - When the export was last generated
#   - Whether the export is current
#   - Whether the ASN is current with its dependencies
#
# Usage:
#   ./run/check-project-status.sh

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
MODEL_DIR="$WORKSPACE/vault/project-model"

# Format unix timestamp to "Mar 22, 18:30"
fmt_date() {
    local ts="$1"
    if [ "$ts" = "0" ] || [ -z "$ts" ]; then
        echo "—"
    else
        date -r "$ts" "+%b %d, %H:%M" 2>/dev/null || echo "—"
    fi
}

printf "\n  %-12s %-24s %-16s %-16s %-14s %-18s\n" \
    "ASN" "Title" "ASN Updated" "Exported" "Needs Export" "Needs Rebase"
printf "  %-12s %-24s %-16s %-16s %-14s %-18s\n" \
    "---" "-----" "-----------" "--------" "------------" "------------"

export_issues=0
dep_issues=0

for yaml in "$MODEL_DIR"/ASN-*/project.yaml; do
    [ -f "$yaml" ] || continue

    asn_dir=$(dirname "$yaml")
    label=$(basename "$asn_dir")

    # Find reasoning doc
    asn_file=$(find "$WORKSPACE/vault/1-reasoning-docs" -name "${label}-*.md" -maxdepth 1 2>/dev/null | head -1 || true)
    if [ -z "$asn_file" ]; then
        continue
    fi

    # Get title from yaml
    title=$(grep '^title:' "$yaml" 2>/dev/null | sed 's/title: *"//;s/"//' | cut -c1-22 || true)

    # Reasoning doc timestamp
    asn_ts=$(git -C "$WORKSPACE" log -1 --format="%ct" -- "$asn_file" 2>/dev/null || echo "0")
    asn_date=$(fmt_date "$asn_ts")

    # Export status
    export_file="$asn_dir/formal-statements.md"
    export_date="—"
    export_status=""
    if [ ! -f "$export_file" ]; then
        export_status="MISSING!"
        export_issues=$((export_issues + 1))
    else
        export_ts=$(git -C "$WORKSPACE" log -1 --format="%ct" -- "$export_file" 2>/dev/null || echo "0")
        export_date=$(fmt_date "$export_ts")
        if [ "$export_ts" -lt "$asn_ts" ]; then
            export_status="YES"
            export_issues=$((export_issues + 1))
        else
            export_status="no"
        fi
    fi

    # Dep status — use last_rebase_check from yaml if available, else reasoning doc timestamp
    rebase_check_ts=$(grep '^last_rebase_check:' "$yaml" 2>/dev/null \
        | sed 's/last_rebase_check: *"//;s/"//' | xargs || true)
    if [ -n "$rebase_check_ts" ]; then
        # Convert ISO timestamp to unix
        check_ts=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$rebase_check_ts" "+%s" 2>/dev/null || echo "$asn_ts")
    else
        check_ts=$asn_ts
    fi

    deps=$(grep '^depends:' "$yaml" 2>/dev/null | sed 's/depends: *\[//;s/\]//;s/,/ /g' | xargs || true)
    dep_status="no"

    if [ -n "$deps" ]; then
        stale_dep=""
        for dep in $deps; do
            dep_label=$(printf "ASN-%04d" "$dep")
            dep_export="$MODEL_DIR/${dep_label}/formal-statements.md"
            [ -f "$dep_export" ] || continue

            dep_ts=$(git -C "$WORKSPACE" log -1 --format="%ct" -- "$dep_export" 2>/dev/null || echo "0")
            if [ "$dep_ts" -gt "$check_ts" ]; then
                stale_dep="$dep_label"
            fi
        done

        if [ -n "$stale_dep" ]; then
            dep_status="YES ($stale_dep)"
            dep_issues=$((dep_issues + 1))
        fi
    else
        dep_status="—"
    fi

    printf "  %-12s %-24s %-16s %-16s %-14s %-18s\n" \
        "$label" "$title" "$asn_date" "$export_date" "$export_status" "$dep_status"
done

printf "\n  Export issues: %d    Dep issues: %d\n" "$export_issues" "$dep_issues"

if [ $export_issues -gt 0 ]; then
    echo "  Fix exports: python scripts/normalize.py <N>"
fi
if [ $dep_issues -gt 0 ]; then
    echo "  Fix deps:    python scripts/rebase.py <N>"
fi
echo ""
if [ $dep_issues -gt 0 ]; then
    echo "  Note: Needs Rebase compares dependency export timestamps against the"
    echo "  ASN's last rebase check (or last update if never rebased). False positives:"
    echo "    - The dependency export changed in ways that don't affect this ASN"
    echo "    - The ASN predates the current pipeline (pre-Mar 20 foundations)"
    echo ""
fi
