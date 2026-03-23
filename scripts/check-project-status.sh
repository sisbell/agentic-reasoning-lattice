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
#   ./scripts/check-asns.sh

set -euo pipefail

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
MODEL_DIR="$WORKSPACE/vault/project-model"
INDEX="$WORKSPACE/vault/project-model/index.md"

# Build set of deprecated/absorbed/dormant ASNs from index
deprecated=$(grep -E '~~ASN-|dormant' "$INDEX" 2>/dev/null \
    | sed -E 's/.*\| ~~?(ASN-[0-9]+)~~?.*/\1/' \
    | sort || true)

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

for yaml in "$MODEL_DIR"/ASN-*.yaml; do
    [ -f "$yaml" ] || continue

    label=$(basename "$yaml" .yaml)

    # Skip deprecated/absorbed/dormant
    if echo "$deprecated" | grep -q "^${label}$" 2>/dev/null; then
        continue
    fi

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
    export_file="$WORKSPACE/vault/3-export/${label}-statements.md"
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

    # Dep status
    deps=$(grep '^depends:' "$yaml" 2>/dev/null | sed 's/depends: *\[//;s/\]//;s/,/ /g' | xargs || true)
    dep_status="no"

    if [ -n "$deps" ]; then
        stale_dep=""
        for dep in $deps; do
            dep_label=$(printf "ASN-%04d" "$dep")
            dep_export="$WORKSPACE/vault/3-export/${dep_label}-statements.md"
            [ -f "$dep_export" ] || continue

            dep_ts=$(git -C "$WORKSPACE" log -1 --format="%ct" -- "$dep_export" 2>/dev/null || echo "0")
            if [ "$dep_ts" -gt "$asn_ts" ]; then
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
    echo "  Fix exports: python scripts/export.py <N>"
fi
if [ $dep_issues -gt 0 ]; then
    echo "  Fix deps:    python scripts/rebase.py <N>"
fi
echo ""
if [ $dep_issues -gt 0 ]; then
    echo "  Note: Needs Rebase is based on timestamps only — a dependency's export"
    echo "  was regenerated after this ASN was last updated. This does NOT always"
    echo "  mean real changes are needed. False positives occur when:"
    echo "    - The ASN was already rebased but the rebase was a no-op"
    echo "    - The dependency export changed in ways that don't affect this ASN"
    echo "    - The ASN predates the current pipeline (pre-Mar 20 foundations)"
    echo ""
fi
