# Channel Assignment — ASN-0110 review-2

**Date:** 2026-06-08 00:18

## Issue 1: Result multiplicity — RE-exact contradicts the latitude granted in the RE-anon discussion
Reason: Internal. The ASN's own RE-anon reasoning establishes that count/multiplicity is withheld by design (counting is the separate FINDNUMOFLINKS operation), so the consistent fix is to fix the per-role object as the *set* `Eᵢ`, making RE-exact literal and deleting the "preserve multiplicities" latitude. No design intent or implementation evidence beyond what the note already cites is needed to choose set semantics.

## Issue 2: The operation is defined over arbitrary `I ⊆ T` but never shown to be realizable/decidable
Reason: The decidability argument (finite store via L-fin, finite endsets, per-span overlap decidable by T2) is internally derivable, but the *representation* the query region must be constrained to should match what the actual operation accepts — evidence the implementation supplies — so the realizability claim is grounded rather than invented.
Gregory question: What representation does RETRIEVEENDSETS take for its query region — a single span, a finite span-set, or something else — and does the search iterate the finite link store performing per-span overlap tests?

## Issue 3: Empty query region (`I = ∅`) not addressed on the I-side
Reason: Internal. RE-touch gives `touches(e, ∅) = false` for all `e`, and RE-arity fixes the tuple length at `N_max(Σ)` independent of the region, so the `I = ∅` result is `⟨∅, …, ∅⟩` of length `N_max(Σ)` — fully determined by the ASN's existing definitions.
