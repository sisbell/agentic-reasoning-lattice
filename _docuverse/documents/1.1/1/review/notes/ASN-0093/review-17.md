# Review of ASN-0093

I conducted a thorough review of this ASN, checking each operation, invariant, lemma, and the worked example against the rubric criteria.

## Examination Summary

**Proofs checked in detail:**
- All six chain lemmas (ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension) — each has explicit base/step induction, citing only earlier lemmas in the documented dependency order.
- ChainMembershipForOrigin's transition induction covers all three transitions (K.σ, K.α, K.λ) with first-emit and subsequent-emit branches.
- FirstEmissionFreshness exhibits all four cases explicitly (content × link × dom(C) × dom(L)) — none deferred via "by similarly."
- Cross-document disjointness Case A (prefix-comparable) uses M0 at *both* `d₁` and `d₂` to discharge `d₂[#d₁+1] ≠ 0`. Case B (prefix-incomparable) handles all three structural sub-cases (B.i at equality, B.i at strict `<`, B.ii at strict `>`), each exercised against a concrete document pair in the worked example (including the hypothetical `d_alt' = [3, 0, 7, 0, 11, 13]` to exercise B.i at strict `<`).

**Boundary cases verified:**
- Base case at `Σ₀ = (∅, ∅, ∅)` — explicitly stated for L14, L-fin, C-fin and vacuous for the rest.
- First emission (empty store branch) and subsequent emission (non-empty branch) both exercised at K.α (Steps 2, 4, 6) and K.λ (Steps 3, 7, 8).
- Empty arrangement: `M(d) = ∅` invariant pinned at K.σ; ASN-0036's S2/S3/S8a/D-CTG correctly identified as vacuously satisfied.

**Invariant conjuncts:**
- L3's three conjuncts (`|L(a)| ≥ 3`, each `eᵢ ∈ Endset`, `e₃ ≠ ∅`) all pinned in K.λ's precondition.
- M0's two conjuncts (`ValidAddress(d)` and `zeros(d) = 2`) pinned in K.σ's precondition.
- C1c/L1c's strengthened clauses (`k₁ = 2`, length monotonicity `#tᵢ > #origin(·)`) explicitly discharged in both first-emit and subsequent-emit chain exhibitions.

**Concrete example depth:**
The 9-step worked example exercises all three operations across three documents, verifies all 17 invariants at each successor state, and explicitly traces Cross-document disjointness for Case A (`d ≼ d'` at Step 5), Case B.i at equality (`d, d_alt` at Step 9), Case B.ii (`d_alt, d'` at Step 9), and Case B.i at strict `<` (hypothetical `d_alt'`).

**Simultaneous-induction discipline:**
The framing paragraph correctly identifies which properties are chain-indexed (state-independent) versus transition-indexed (state-dependent), and the discharge matrix together with the lemma-preservation rows handle the mutual entanglement between ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, and C2/L1a.

**Cross-ASN references:** All references are to foundation ASNs (0034, 0036, 0040, 0043) per the allowed list.

**No "by similarly" hand-waves:** Every "symmetric" appeal is accompanied by an explicit content↔link substitution rule and the parallel case is shown.

## REVISE

No REVISE items.

## OUT_OF_SCOPE

The ASN's "Open Questions" section already correctly defers link withdrawal/tombstoning (per LM 4/9), arrangement mutation primitives, entity stratification, provenance recording, document baptism discipline, concurrency, and additional subspace identifiers. The Scope section explicitly lists these. No further OUT_OF_SCOPE topics to flag.

VERDICT: CONVERGED
