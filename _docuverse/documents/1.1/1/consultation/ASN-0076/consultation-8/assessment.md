# Channel Assignment — ASN-0076 review-8

**Date:** 2026-05-25 20:58

## Issue 1: E4's proof omits formal discharge of the membership conditions
Reason: The required derivation chain uses only primitives already invoked in the ASN — K.λ's effect from §E0, L12 for value persistence, and L6 for slot accessor semantics. All foundational pieces are cited; the fix is a mechanical rewriting of E4's proof to discharge the membership claims explicitly before invoking L13/L4/PrefixSpanCoverage as interpretation.

## Issue 2: Notational inconsistency in E7's proof
Reason: A pure notational correction — replacing `Σ.L(ℓ_sup)` with `Σ'.L(ℓ_sup)` and citing the (repaired) E4 instead of "the construction." No external evidence is needed; the fix follows directly from the post-state being the relevant evaluation point.

## Issue 3: "Step order" argument conflates definition and necessity
Reason: The reviewer's own argument cites L4 (already in the ASN's foundation recap) to show K.λ's preconditions do not require `ℓ_new ∈ dom(L)`; the fix is to rephrase the ordering as a definitional choice of the composite rather than a precondition-level necessity, while preserving the semantic remark as commentary. Fully derivable from the ASN's existing composite definition and L4.
