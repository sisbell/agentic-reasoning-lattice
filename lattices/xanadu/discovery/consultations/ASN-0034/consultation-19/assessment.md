# Revision Categorization — ASN-0034 review-19

**Date:** 2026-03-26 02:13



## Issue 1: Three circular dependencies in the YAML graph
Category: INTERNAL
Reason: The fix involves removing reverse edges in the dependency graph to match the derivation order already established in the ASN text. All necessary information is present in the ASN itself.

## Issue 2: Spurious dependencies — YAML contradicts the ASN property table
Category: INTERNAL
Reason: The ASN's own property table specifies the correct dependency sets for each property. The fix is mechanical: trim each YAML `follows_from` to match the table already written in the ASN.

## Issue 3: Spurious transitive dependencies in TS5 and D2
Category: INTERNAL
Reason: The derivation sections explicitly cite only the direct dependencies (TS3/TS4 for TS5, D1/TA-LC for D2). Removing transitive entries is a mechanical correction derivable from the ASN text.

## Issue 4: Name mismatches in YAML
Category: INTERNAL
Reason: The ASN parentheticals provide the canonical names. The fix is mechanical string replacement to align YAML `name` fields with the ASN's own naming.
