# Channel Assignment — ASN-0071 review-62

**Date:** 2026-06-03 11:32

## Issue 1: PC-RANGE proof omits the equal-depth (#v = #u) sub-case — the primary case
Reason: Pure proof-completeness fix. The missing sub-case is discharged entirely from machinery already in the ASN — T1 case (i)/(ii), reach exclusivity, and S8-depth — so no design intent or implementation evidence is needed.

## Issue 2: "What we do not specify" (ii) and (iii) are out-of-scope deferrals, not non-specifications
Reason: Editorial removal of meta-prose; the one load-bearing point (single-state evaluation) already lives in *Currency*. Derivable from the ASN alone.

## Issue 3: vspec relaxation paragraph is a use-site inventory plus defensive design rationale
Reason: Prose trimming to the operative precondition (T12 on `ℓ`); the vspec definition and its contrast with ASN-0058 are already present in the ASN. No external channel needed.

## Issue 4: duplicated reachability deferrals
Reason: Editorial merge of two identical ASN-0047 deferrals into one reference. Fully internal.
