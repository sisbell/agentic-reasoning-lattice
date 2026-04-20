# Review of ASN-0085

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism and round-trip conditions
**Why out of scope**: The ASN explicitly lists these as open questions. TA7a's subtraction results involve conditional S-membership with multiple edge cases (e.g., the `[5,3] ⊖ [5,1] = [0,2]` counterexample), making the subtraction homomorphism genuinely harder than addition. This is future work, not an omission in the current ASN.

---

**Verification notes.** I traced OrdAddHom's proof component-by-component across three action-point positions (k = 2, k interior, k = m) and confirmed identical sequences on both sides in every case. Both instances verify: (a) `[3,7] = [3,7]`, (b) `[7,0] = [7,0]`. The well-definedness of the right-hand side (`actionPoint(w_ord) = k−1 ≤ m−1 = #ord(v)`) is established in the proof body. OrdAddS8a's iff condition is correct — components r₁ through rₖ are unconditionally positive (S8a on v gives rᵢ = vᵢ ≥ 1 for i < k; rₖ = vₖ + wₖ ≥ 2), so S8a reduces exactly to the tail condition on w_{k+1},...,wₘ. OrdShiftHom correctly verifies OrdAddHom's preconditions for δ(n,m) and correctly identifies the vacuous satisfaction of OrdAddS8a's tail condition when the action point equals m. The inverse properties of ord/vpos are pure sequence identities requiring no predicates beyond T membership. The `#w = m` restriction is a design choice consistent with the shift use case, not an error.

VERDICT: CONVERGED
