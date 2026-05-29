# Channel Assignment — ASN-0040 review-55

**Date:** 2026-05-28 22:08

## Issue 1: Duplicated downstream deferrals in Bop
Reason: Internal — the fix is to delete one of two redundant passages stating the same deferral. No design intent or implementation evidence is needed; both passages already exist in the ASN and the redundancy is verifiable from the text alone.

## Issue 2: The "next evaluated against precondition state" claim is restated in five places
Reason: Internal — consolidating a fact that is already the sole content of B4 and replacing restatements with "by B4" citations. The atomicity-read-exactness fact is fully established within the ASN; this is pure deduplication.

## Issue 3: Frame clause carries a downstream-component inventory
Reason: Internal — trimming an enumeration of components owned by other ASNs that adds no constraint. The frame "only s.B is modified" is self-contained; no external channel informs the deletion.

## Issue 4: B3 partition enumerates a configuration its own requirement excludes
Reason: Internal — the forbidden fourth row is the logical negation of the ASN's own stated implication `Occupied(t,s) ⟹ t ∈ s.B`. Removing or folding it follows directly from the requirement already present.

## Issue 5: B6 condition (iii) is not independently necessary at d = 1
Reason: Internal — the scoping correction follows from the ASN's own arithmetic (at d = 1, `zeros(p) > 3` already violates T4 via condition (i)), and the sufficiency proof already admits this. No design intent or implementation evidence is required to restrict the necessity claim to d = 2.
