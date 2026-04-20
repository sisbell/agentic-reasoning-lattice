# Revision Categorization — ASN-0066 review-2

**Date:** 2026-03-21 13:12

## Issue 1: D-MIN base case not verified
Category: INTERNAL
Reason: The fix is adding one sentence applying the same vacuous-truth argument already used for D-CTG. The reasoning is identical and fully present in the ASN.

## Issue 2: Depth ≥ 3 structural consequence derived but not formalized
Category: INTERNAL
Reason: The derivation already exists inline in the ASN. The fix is labeling it, stating the combined consequence explicitly, and adding registry entries — all derivable from existing content.

## Issue 3: No depth ≥ 3 concrete example
Category: INTERNAL
Reason: The abstract argument already appears in the ASN with [S, 1, 5] and [S, 2, 1]. Constructing a positive example and violation at depth 3 is mechanical application of the definitions already present.

## Issue 4: Depth ≥ 3 argument overstates premises
Category: INTERNAL
Reason: The fix is restructuring the logical dependencies of an argument already fully present in the ASN — specifically, showing S8-fin alone suffices for the contradiction, and demoting S8a to a supplementary note. No external evidence needed.
