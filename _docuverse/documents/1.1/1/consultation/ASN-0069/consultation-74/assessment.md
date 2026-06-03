# Channel Assignment — ASN-0069 review-74

**Date:** 2026-06-02 23:54

## Issue 1: V12(d) — defensive prose explaining why lemmas are needed
Reason: Internal — the fix removes role-narration and keeps the operative derivation chain (V4+V4b range equality, P4★ at boundary Σ, P2 forward), all of which are already present in the ASN.

## Issue 2: V8c — tautological derivation at length
Reason: Internal — collapsing the proof to a one-line observation about commutativity of ∩ and symmetry of = requires no design intent or implementation evidence.

## Issue 3: V8b — derivation is tautological; "state-relative" not substantiated
Reason: Internal — deciding between dropping V8b or proving monotone non-increase is a self-contained structural choice; the shrinkage mechanism (edits) is explicitly out of this ASN's scope.

## Issue 4: Worked example — duplicated K.δ-alone walkthrough
Reason: Internal — collapsing two redundant vignettes into one with a single CL-OWN/V5 link-preservation sentence is pure exposition cleanup derivable from V5/V6/V7 already stated.

## Issue 5: Dependency Audit — use-site inventory
Reason: Internal — dropping the mechanism catalog while retaining the ASN-0040 removal recommendation and the single re-derivation note is an editorial trim with no external dependency.
