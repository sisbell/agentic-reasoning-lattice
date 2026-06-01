# Channel Assignment — ASN-0047 review-183

**Date:** 2026-05-31 23:17

## Issue 1: J1'★ derivation is step-local but the stated obligation is composite-scoped
Reason: The fix is internal — it concerns the ASN's own proof machinery (wp calculus, J0, P2, ValidComposite★). Either extending the derivation to the composite level via J0/P2, or reframing J1'★ as an imposed coupling, is fully determined by content already present in the ASN.

## Issue 2: Inaccurate use claim in the Contains(Σ) definition
Reason: The fix is internal — correcting a forward reference from `Contains(Σ)` to `Contains_C(Σ)` and dropping "as a state invariant" is settled by the ASN's own definitions (P4★ is stated over `Contains_C`, and the ASN itself proves `Contains(Σ) ⊆ R` unsatisfiable in the extended state).

## Issue 3: Cross-section deferral stubs to a single downstream location
Reason: The fix is internal and purely organizational — consolidating three stub-plus-deferral introductions of P4★/P4a/P7a into single statements requires no design intent or implementation evidence, only relocation of existing prose.

## Issue 4: Structural-navigation prose in place of reasoning
Reason: The fix is internal and editorial — replacing "is/isn't in the matrix" filing commentary with the one-line pointer (TrackedEmission) and the corollary statements with their one-step discharge (distinctness corollaries) uses content already present in the ASN.
