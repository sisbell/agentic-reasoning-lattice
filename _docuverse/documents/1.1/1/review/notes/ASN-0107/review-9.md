# Review of ASN-0107

I worked through every claim against its cited foundations, re-derived the monotonicity laws, and checked the worked example line by line (tumbler structure, zero-counts, subspace identifiers, the contraction/extension/reorder arithmetic, and the wp specialisation). I also confirmed the transition coverage is exhaustive and the boundary cases (empty `Qᵢ`, `Q = (T,T,T)`, empty store, shared-endpoint deletion, partial survival) are handled.

## REVISE

(none)

Findings considered and discharged as sound:

- **`sat`/`num` well-definedness** — totality and finiteness follow correctly from L-fin; degenerate `Qᵢ = ∅` and `Q = (T,T,T)` are both treated, the latter correctly resolving to "links with non-empty from/to endsets" via L3 and `Endset = 𝒫_fin(Span)`.
- **E1–E4** — the existence-anchoring laws cite LP3★ (multi-step coverage invariance) and L12a correctly; E3's transition enumeration (K.α, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.σ/K.δ, K.ρ) is the complete non-K.λ vocabulary of ASN-0047, so "all operations" is genuinely covered, not just three.
- **D2 reordering clause** — the forward-image computation `Qᵢ(Σ') = {M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom}` is correct, and the sufficient-but-not-necessary analysis (setwise fixity vs. content-sharing preservation) is rigorous rather than hand-waved. The explicit refusal to transfer LP9–LP11 (which govern the *preimage* `project`, not the forward image) is the right call.
- **R1/R2/R6** — the three provisos (P-last), (P-slot), (P-sole) are each shown load-bearing with the exact counterexample they exclude; R6's wp derivation is a genuine mechanical pullback with a correct weakest-not-merely-sufficient argument and a clean specialisation back to R1's split.
- **Worked example** — internally consistent throughout: `d` has `zeros = 2`; `a₁,a₂,τ` are `zeros = 3`, `s_C` content addresses; `ℓ₁,ℓ₂,ℓ₃` are `s_L`; the contraction drops `[1,3]↦a₁` giving `Δ = −2` within R2's `{−3,…,0}` band with `ℓ₃` surviving per R3; the reorder swap correctly drives `num_disc 3→0` with `ran` preserved, illustrating D2's distinctly-imaged-boundary-crossing case.
- **A2** — the discoverability (existential, per-slot) vs. counting (conjunctive, all-slot) distinction is correctly drawn; the prior to/type-subspace error is resolved, with the clarification that `Wᵢ` are query V-regions over `d_new`'s positions, not document subspaces, and that `Q₂=Q₃=T` belongs to existence anchoring only.

Depth requirements are met: concrete example present and exercised against P1, P2, E4, R2, R3, D2; non-trivial wp present (R6); derived consequences explored under each of E, D, R; no proof-by-checkmark or proof-by-"similarly."

## OUT_OF_SCOPE

The five Open Questions (independent per-slot anchoring, discovery=existence coincidence, count-vs-retrieval cardinality, deduplication-as-mandate-vs-discipline, request representation invariance) are correctly deferred; none is an error in this ASN. The deduplication remark in P1 is framed as an implementation observation supporting the abstract set-cardinality claim, not as smuggled mechanics — it does not constitute drift.

VERDICT: CONVERGED
