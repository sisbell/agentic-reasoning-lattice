# Review of ASN-0107

I checked the definitions for totality, the monotonicity proofs, the non-monotonicity (reordering) analysis, the weakest-precondition derivation, and verified the worked example component-by-component.

**Definitions and well-definedness.** `sat`, `match`, `num` are well-formed; `match ⊆ dom(Σ.L)` with L-fin gives totality and finiteness, and the degenerate requests (`Qᵢ = ∅`, no overlap, empty store) all yield a clean `0`. The interpretive commitments (overlap-not-containment satisfaction; conjunctive-across-slots, disjunctive-within; standard-triple scoping with `Q=(T,T,T)` admitted) are stated explicitly rather than smuggled.

**Existence laws (E1–E4).** E1 correctly grounds satisfaction-permanence in LP3★ + L12; E2/E4 correctly use store monotonicity + address freshness (matching creations land at fresh addresses disjoint from the prior match set, so the cardinality delta is exactly the matching-creation count, with no subtractive term since L12 forbids removal). E3's claim that only K.λ moves the existence count is correct against the ASN-0047/0093 transition vocabulary.

**Discovery laws (D1–D3, R-laws).** The reordering clause in D2 is the place most likely to be hand-waved, and it is not: it reasons about the *forward image* `Qᵢ(Σ)` directly, explicitly declines to transfer LP9–LP11 (which govern the *preimage* `project`), correctly computes `Qᵢ(Σ') = {M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom}`, and gives the exact (not merely sufficient) preservation condition, with the content-sharing counterexample showing setwise fixity is sufficient-not-necessary. R1's three load-bearing provisos (P-last, P-slot, P-sole) are each justified by a concrete way the decrement would otherwise fail, and R1 is correctly positioned as the `k=1` specialisation of R2.

**R6 (wp).** The pullback is mechanically correct (coverage permanence via L12/E1; resolved-part substitution via `Σ'.M(d_q) = M(d_q) ↾ R`), the "weakest" justification rests on determinism + logical equivalence rather than a one-sided implication, and the `R ⊆ dom` monotone-specialisation correctly explains the drop-but-never-add asymmetry.

**Worked example.** Verified: `d` has zeros=2; `a₁,a₂,τ` have zeros=3 with `E₁=s_C`; `ℓ₁–ℓ₃` have `E₁=s_L`; the multi-span `ℓ₃` contributes 1 (P1); value-identical `ℓ₁,ℓ₂` contribute 2 (P2); the contraction drop 3→1 is R2 with `k=3, Δ=−2`; the K.μ~ swap 3→0 satisfies admissibility (length/subspace-preserving, link-fixing vacuous) and exhibits D2's reordering clause exactly. The E4 two-step creation check (one matching, one not) correctly nets `+1`.

No cross-ASN references outside the foundation set; Nelson/udanax citations are evidence, not claim dependencies. The ASN stays at the level of system guarantees (the deduplication point is flagged as an implementation *observation*, not promoted to mechanism), so no drift.

I found no missing boundary case, no proof-by-"similarly", and no overclaim. The deferred topics (independent per-slot document anchoring, discovery/existence coincidence, count-vs-retrieval consistency) are appropriately held in Open Questions rather than asserted.

VERDICT: CONVERGED
