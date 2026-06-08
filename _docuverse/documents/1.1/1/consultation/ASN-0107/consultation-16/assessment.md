# Channel Assignment — ASN-0107 review-16

**Date:** 2026-06-08 11:06

## Issue 1: R1's (P-last) precondition does not establish "a leaves Qᵢ(Σ')" under content sharing
Reason: Internal fix. The correction is purely formal — strengthen (P-last) to require `v` be the unique consulted position mapping to `a` (or route the shared-duplicate case to the Δ=0 branch) and state the arrangement-maximality that single-entry K.μ⁻ forces. All inputs (M13/S5 sharing, PerSubspaceContractionScope from ASN-0047) are already cited in the note; no design intent or implementation evidence is at stake.

## Issue 2: D2 carries defensive meta-prose explaining why downstream lemmas do *not* apply
Reason: Internal fix. Anti-bloat removal of methodology-provenance prose; the extension/contraction/reordering arguments are self-contained in the note and need only be restated directly.

## Issue 3: R6 derivation contains methodology-provenance prose
Reason: Internal fix. The LP12a-lineage sentence is narration; the self-contained "Derivation." paragraph already performs the wp pullback. Pure deletion, no channel input needed.

## Issue 4: R1's opener duplicates the R-section introduction
Reason: Internal fix. The R-section intro already states the store-side result; dropping R1's restatement is a mechanical de-duplication derivable from the note alone.
