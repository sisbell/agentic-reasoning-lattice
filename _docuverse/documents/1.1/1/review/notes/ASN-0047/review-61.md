# Review of ASN-0047

## REVISE

### Issue 1: Undefined "case (d)" in worked example

**ASN-0047, Worked example: link allocation and arrangement, Step 3 (K.μ⁻ admissibility at M_int)**: 
> "*Content-subspace pattern.* `V_{s_C}(d) = {[1,1], [1,2]}`, `V_{s_C}(d_int) = ∅` — full removal with `n'_{s_C} = 0`. This is the case-(d) admissible pattern of K.μ⁻ (subspace emptied; D-MIN★/D-CTG★/D-SEQ★ become vacuous on the cleared subspace)."

**Problem**: The K.μ⁻ case analysis (Elementary transitions, K.μ⁻ section) defines only three cases: (a) suffix removal, (b) interior removal, (c) prefix removal. Case (a) explicitly subsumes the n'_S = 0 full-clearance sub-case: "When n'_S = 0 (full-subspace clearance), V_S(d') = ∅ and D-CTG★ and D-MIN★ hold vacuously." There is no "case (d)". The Decomposition of K.μ~ section correctly cites case (a) for the same n'_S = 0 pattern.

**Required**: Replace "case-(d) admissible pattern" with "case (a) with n'_{s_C} = 0" (or equivalent), matching the case-analysis terminology used elsewhere in the ASN.

## OUT_OF_SCOPE

None — the ASN's explicit scope (Open Questions + Structural sufficiency and known gaps + Scope section) properly defers tombstoning, version-management semantics, account-level k=1, non-T10a allocators, and concurrent allocation to future work.

VERDICT: REVISE
