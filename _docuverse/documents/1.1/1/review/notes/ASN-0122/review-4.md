# Review of ASN-0122

I checked the derivations against the foundations, re-ran the worked example's arithmetic, and stress-tested the partition, transport, and vacuity theorems for skipped cases. Summary of the load-bearing verifications:

- **Region clip / subspace-crossing (`State, Instances, and Spec-Sets`):** The counterexample `σ = ([1,5],[3])` is genuinely T12-well-formed with a content-subspace *start* yet denotes `[2,7]` (a link position) — I confirmed `reach = [1,5] ⊕ [3] = [4]` and `[1,5] ≤ [2,7] < [4]`. So the `∩ V_{s_C}` clip, not `subspace(start)=s_C`, is what delivers content-only regions. The operand-hygiene-vs-guarantee distinction is correct and load-bearing.
- **X9 (SubspaceVacuity):** Verified all three link-foot cases (cross-doc via CL-OWN+S7 single-valued origin; content↔link via SD; same-doc via CL-UNIQ) collapse `res p = res q` to `p = q`, so the decomposition `corr = (content–content) ⊔ (link diagonal on P∩Q)` is exhaustive and disjoint, with the diagonal determined without consulting `res`. Losslessness-for-correspondence holds.
- **X11 (CanonicalReport):** Out-degree ≤ 1 (functionality of `succ`), in-degree ≤ 1 (TS2 per coordinate), acyclicity (TS4) ⟹ finite functional graph is a disjoint union of simple paths. Sort key `(first foot, second foot)` is injective on maximal pairs (shared key ⟹ shared first element ⟹ coincide), so the canonical order is well-defined. Fan-out and the tie-break necessity are correctly exhibited.
- **Worked example:** Recomputed `corr` (3 elements), the chain partition (`γ₁` width 2, `γ₂` width 1), the swap transpose (first feet tie, second-foot separation), the window clip (`γ₁` clips to one pair, X4c), and the disjoint-window detector (`{a,b}∩{c,b}={b}`). Every count is forced by the definitions.
- **X-T / X6 / X7:** Confirmed the transport lemma's res-preservation telescopes across the chain composite `φ_k∘…∘π_i∘…∘φ₁` under the two stated premises, that all five arrangement-edit kinds (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, ASN-0082 shifting contraction) are covered (injectivity of `τ=id∪σ` on `L∪R` rests on D-DP's `L∩Q₃=∅`), and that non-arrangement transitions fall to X5.
- **X2 composite validity:** The lone-K.δ and the K.α+K.μ⁺+K.ρ composites discharge J0/J1★/J1'★ as claimed; S4 gives `a₁≠a₂`.

The cross-ASN references are all to foundation ASNs (0034/0036/0045/0047/0053/0058/0082/0086/0093/0098); no foundation notation is reinvented (correspondence pairs are a new object, not a restatement of ASN-0058 mapping blocks). The boundary cases — empty spec-set, clip-to-nothing, `V_{s_C}(d)=∅`, both regions empty, full contraction, differing per-side depths — are each addressed explicitly. The two implementation deficiencies are correctly reported as deviations from the binding postconditions, not as spec defects.

## REVISE

None.

## OUT_OF_SCOPE

The deferred extensions (n-way alignment composed from pairwise reports, derived-index consistency contracts, matching-with-multiplicity equivalence, and whether arrangement-presence is the right basis vs. stored-span reference) are correctly placed in Open Questions rather than asserted as claims. The stability theorems (X7) cite the foundation edit operations (K.μ family, ASN-0082 contraction) to prove `corr` stable under them without redefining the out-of-scope content operations themselves — the right boundary. No in-scope coverage is missing and no out-of-scope operation is improperly specified.

VERDICT: CONVERGED
