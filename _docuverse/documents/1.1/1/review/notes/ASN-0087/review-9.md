# Review of ASN-0087

## REVISE

### Issue 1: L1c chain uniqueness claim has gaps in the argument
**ASN-0087, "Per-State Invariants at Σ'" (L1c verification)**: "the chain `(d, b_C(d), b_L(d), t_1^L(d), …, ℓ)` is the *unique* structural inc-derivation of any `ℓ ∈ dom(L)` from its home document"

**Problem**: The supporting argument relies on TA5a's zero-count saturation and length-target intuition, but it does not establish per-step uniqueness. From b_C(d) (zeros = 3), TA5a admits both k=0 and k=1 — only the destination structure of b_L(d) (subspace 2 at position #d+2) forces k_2 = 0. The bound-saturation argument addresses what happens after t_1 and t_3 but does not rule out alternative k_i at each transition. The conclusion "unique" needs a per-step enumeration showing no alternative k_i value produces a valid chain to ℓ.

**Required**: Either weaken the claim (drop "unique" and assert only existence, which is what L1c demands), or supply the per-step uniqueness argument:
- k_1 = 2 forced: k=0 violates #tᵢ > #d; k=1 produces [d, 1] from which no link-address structure with origin = d is reachable.
- k_2 = 0 forced: k=0 reaches subspace s_L by incrementing position #d+2 from 1 to 2; k=1 appends a new component, missing b_L(d).
- k_3 = 1 forced: k=1 produces t_1^L(d); k=0 produces [d, 0, 3], not in A_L(d).
- k_j = 0 for j ≥ 4: A_L(d) sibling steps determined uniquely by the chain index of ℓ.

### Issue 2: Σ_mid invariant preservation bundles 8 invariants under "same reasoning"
**ASN-0087, "Atomicity" section**: "The same reasoning preserves all link-store invariants (L0, L1, L1a, L1b, L1c, L3, L14, L-fin) at Σ_mid via K.λ's precondition discharge."

**Problem**: This single sentence covers 8 distinct invariants without per-invariant verification. The S3★ case is explicit (referential integrity under domain growth) but the L-invariants are bundled. While the underlying reasoning is genuinely uniform — K.λ's precondition discharges each clause for the new entry ℓ; the frame on L preserves prior entries — the bundling violates the convention of explicit case-by-case verification that the rest of the ASN follows.

**Required**: A short per-invariant breakdown at Σ_mid. Three to four lines suffice:
- L0, L1, L1a, L1b, L3 on ℓ: discharged directly by K.λ's precondition (E(ℓ)₁ = s_L, zeros(ℓ) = 3, origin(ℓ) = d ∈ dom(M), #E(ℓ) ≥ 2, link-value structural constraints).
- L1c at Σ_mid: the same chain (d, b_C(d), b_L(d), …, ℓ) constructed for Σ' applies at Σ_mid.
- L14: K.λ's freshness (ℓ ∉ dom(Σ.C)) combined with L14 at Σ gives dom(Σ_mid.C) ∩ dom(Σ_mid.L) = ∅.
- L-fin: |dom(Σ_mid.L)| = |dom(Σ.L)| + 1, finite by L-fin at Σ.
- For prior entries: K.λ's frame on L preserves every prior ℓ' ∈ dom(Σ.L) with Σ_mid.L(ℓ') = Σ.L(ℓ'), so all per-entry invariants on prior entries hold at Σ_mid by inheritance.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
