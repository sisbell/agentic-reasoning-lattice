# Review of ASN-0093

I checked each invariant's discharge in the per-(invariant, transition) matrix, the freshness/uniqueness lemmas (the hardest and most often hand-waved), the cross-document disjointness boundary cases, the simultaneous-induction structure for circularity, and the base case at Σ₀.

## Verification notes (no defects found)

**Cross-document disjointness, proper-prefix branch.** The argument that `p₂[#d₁+1] = d₂[#d₁+1] ≠ 0` is sound: since `d₁ ≺ d₂` and `zeros(d₁) = zeros(d₂) = 2` (M0), `d₂` carries `d₁`'s two zeros within positions `1..#d₁`, leaving no zero at `#d₁+1 ≤ #d₂`. First divergence is correctly located at the separator. T10's preconditions are met on both anchors.

**Freshness without circularity.** FirstEmissionFreshness/SubsequentEmissionFreshness invoke only pre-state (Σ) properties (ChainMembershipForOrigin, ChainPrefixExtension, C2/L1a, StoreT4Validity at Σ). ChainMembershipForOrigin's own step uses the state-independent FirstEmission lemma plus Σ-IH, not the freshness lemmas. The simultaneous-induction ordering (freshness → store invariants at Σ′ → ChainMembershipForOrigin at Σ′) is consistent.

**SD across allocation transitions.** The matrix's "standing consequence of L0/C1/L1/StoreT4Validity at Σ′" is valid: with the L0 C-clause holding at the new key, T7 covers the freshly added address; the derivation does not depend on the freshness argument and is sound either way.

**Subsequent-emit chain bookkeeping.** C1c/L1c clauses (`k₁ = 2`, `#tᵢ > #origin`) are correctly inherited unchanged from the IH chain and extended for the new `inc(·,0)` step via TA5(c). B5a's precondition `a_prev_{sig} > 0` is properly discharged through ChainElementT4Validity → TA5-SigValid → T4's `t_{#t} ≠ 0`.

**Base case and worked example.** Σ₀ vacuity/triviality is correct for all conjuncts. The nine-step example exercises first-emit, subsequent-emit, prefix-nested documents (d ≺ d′), and prefix-incomparable documents (d, d_alt), checking concrete addresses and origins against each invariant.

## REVISE

None.

## OUT_OF_SCOPE

The deferred topics (K.μ arrangement mutation, entity stratification, provenance, coupling, link withdrawal) are correctly identified in the Scope section and not specified here; no drift.

VERDICT: CONVERGED
