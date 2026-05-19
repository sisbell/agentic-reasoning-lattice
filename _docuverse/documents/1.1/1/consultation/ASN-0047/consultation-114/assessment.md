# Channel Assignment — ASN-0047 review-114

**Date:** 2026-05-19 10:41

## Issue 1: S8★ citation imprecision for link-subspace projection
Reason: Internal — the ASN already states the link-subspace case is covered by "the trivial length-1 decomposition" which requires no S8 machinery; the fix is to align the citation with this self-contained discharge.

## Issue 2: NodeUniqueAllocation does not explicitly state registry-tracking closure
Reason: Internal — the closure clause is what the K.δ k = 2 sub-case B discharge already relies on; adding an explicit clause (c) to NodeUniqueAllocation formalizes the implicit chain without requiring external evidence about the registry mechanism itself.

## Issue 3: K.δ case (ii) k = 0 prose elides the strict relation between freshness and frontier identification
Reason: Internal — T10a GlobalUniqueness is already cited elsewhere in the ASN as the cross-allocator collision premise; the fix is to surface it explicitly at this site.

## Issue 4: Dual initial-state definition
Reason: Internal — purely a presentational consolidation of two existing definitions; no design or implementation evidence is at issue.

## Issue 5: K.α "amendment" terminology contradicts its own disclaimer
Reason: Internal — the ASN's own disclaimer states there is no local amendment; the fix is either deletion or renaming of the shorthand, derivable from the existing inheritance relationship with ASN-0093.

## Issue 6: Verification matrix "frame" entries hide a non-trivial discharge for L-related rows
Reason: Internal — the discharge mechanism (amended frame with `L' = L`) is already documented in the prose below the matrix; the fix is to surface this annotation at the cells.
