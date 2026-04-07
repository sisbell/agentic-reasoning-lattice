# Review of ASN-0047

## REVISE

### Issue 1: J4 fork precondition is insufficient in the extended state

**ASN-0047, J4 (Fork composite):** "precondition d_src ∈ E_doc ∧ M(d_src) ≠ ∅"

**Problem:** The K.μ⁺ amendment restricts arrangement extension to content-subspace V-positions. A document can have `M(d_src) ≠ ∅` while `dom_C(M(d_src)) = ∅` — a document with only link-subspace positions, which is reachable via K.δ + K.λ + K.μ⁺_L with no intervening K.μ⁺. In this state J4's precondition is satisfied, but J4's K.μ⁺ step is ill-formed: `ran(M(d_src)) ⊆ dom(L)` (all mappings are link-subspace, so S3★ gives targets in dom(L)), and `dom(L) ∩ dom(C) = ∅` by L14, so no I-address in the source's range can satisfy S3★'s content clause for a content-subspace V-position in d_new. The only option is `ran(M'(d_new)) = ∅`, making `dom(M'(d_new)) = ∅ = dom(M(d_new))` and violating K.μ⁺'s strict domain extension `dom(M'(d)) ⊃ dom(M(d))`.

The "Consequence for J4" section verifies J1★, J1'★, and D-CTG/D-MIN under the amended transitions but does not update the fork precondition to exclude this case. The sentence "with at least one I-address to transclude, the strict domain extension... is satisfiable" assumes the non-empty I-addresses are content addresses, which does not follow from `M(d_src) ≠ ∅` alone.

**Required:** Strengthen J4's precondition to `d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅`. Extend the existing clause "When the source arrangement is empty, the fork definition does not apply" to cover the content-subspace-empty case: when `V_{s_C}(d_src) = ∅`, creation from such a source is K.δ alone (ex nihilo), not a fork.

## OUT_OF_SCOPE

None. The open questions list is comprehensive; no additional gaps fall outside the ASN's stated scope.

VERDICT: REVISE
