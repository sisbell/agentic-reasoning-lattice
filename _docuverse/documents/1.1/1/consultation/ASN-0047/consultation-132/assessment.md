# Channel Assignment — ASN-0047 review-132

**Date:** 2026-05-19 21:09

## Issue 1: K.μ⁺'s functionality precondition leaves pairwise distinctness of new positions implicit
Reason: The fix is a formalization tightening — making the implicit partial-function typing explicit by adding a pairwise-distinctness clause to K.μ⁺'s precondition. Derivable from the ASN's own functional-typing convention; no design or implementation question is at stake.

## Issue 2: Cross-document disjointness lemma Case A relies on zeros(e₁) = zeros(e₂) without citation
Reason: The fix is to cite an already-stated precondition (zeros(e₁) = zeros(e₂) = z) at the step where it is load-bearing. Pure proof-exposition tightening derivable from the lemma's existing statement.

## Issue 3: The "Class (b) properties may transiently fail" matrix entry for P4a is operationally misleading
Reason: The ASN's existing ValidComposite★ already commits to initial-to-final coupling evaluation, which makes option (b) — K.ρ-first ordering admissible, with Σ' itself serving as the P4a witnessing state — consistent with the established framework. The fix is to rewrite the matrix entry to make this concrete; no design intent question requires resolution beyond what is already in the ASN.

## Issue 4: The "necessary and sufficient" claim for K.μ~'s existence condition mixes axiom-tight necessity with operation-side sufficiency
Reason: The fix is to reorganize the existing arguments — either split the existence condition into necessity/sufficiency statements with forward references, or front-load the full-clearance form's universal admissibility. Pure exposition restructuring within the ASN's existing content.

## Issue 5: The Class (b) introduction's distinction between "per-state" and "composite-boundary" deserves a concrete example at the point of definition
Reason: The required trace material (P7a failing at post-K.α and restored at post-K.ρ) already appears in the ASN's worked examples; the fix is to extract a summary paragraph at the definition site. Pure exposition; no external input needed.
