# Channel Assignment — ASN-0098 review-27

**Date:** 2026-05-26 06:01

## Issue 1: Achievability section conflates state-relative tightness with future emissions
Reason: The fix is purely a rephrasing that separates two claims already established in the ASN — tightness-at-`Σ_e` (discharged by the construction choosing `n` such that all F-candidates have indices ≤ m at `Σ_e`) and LP19's downstream consequence (subsequent emissions at indices > m lie outside the half-open interval). Both facts are already proven; no design intent or implementation evidence is required.

## Issue 2: LP-Comp's mixed-chain composition is asserted without explicit proof
Reason: The choice between (a) providing explicit induction for the three same-operation cases or (b) reducing LP-Comp to a documentation note about the per-step lemmas forming a covering case-analysis is an internal proof-structure decision. The author can inspect LP18 and LP19's existing proofs to confirm whether the cumulative claim is load-bearing and choose accordingly.

## Issue 3: LP12b's scope omits the link-canonical class
Reason: The symmetric argument for `s = [d_s, 0, s_L, k_s]` follows mechanically from LP-Fin Corollary applied at `X = s_L` (yielding `coverage ∩ dom(C) = ∅` by the SubspaceConventionAxiom flip), and ASN-0043 L4(c) already admits link-subspace endsets. The decision to add LP12b' or declare OUT_OF_SCOPE is derivable from the ASN's own machinery; no external channel is needed.

## Issue 4: LP10's exact-difference set comprehension consumes K.μ⁻'s effect without citing its full force
Reason: The fix is a one-line citation chain combining K.μ⁻'s effect clause, its contracted-arrangement definition (`M'(d) = M(d) ↾ R`), and D-SEQ★ — all already-cited pieces of ASN-0047 and ASN-0093 referenced elsewhere in this ASN. The author can verify the exact wording in ASN-0047 directly without consulting Nelson or Gregory.
