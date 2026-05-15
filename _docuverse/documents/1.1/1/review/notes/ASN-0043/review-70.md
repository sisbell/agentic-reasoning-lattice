# Review of ASN-0043

## Summary

This is a substantial, rigorous specification of the link layer. The proof structure is exhaustive — the L9 ghost-type construction, the L11b non-injectivity construction, and the five-state worked example each verify state-local invariants comprehensively, with explicit case discrimination (Cases A/B in L9's L1c verification) and careful boundary handling. The `s_C`-residence scoping in L0a is honest about where the ASN's disjointness guarantee holds and where it depends on a future ASN-0036 revision. The arity-4 link in the worked example (Σ_3) exercises L3, L6, and L8 in the higher-arity regime non-vacuously. The L8 discrimination at Σ_4 (with `g` vs `g'` sibling ghosts) demonstrates a non-trivial `same_type = false` case via disjoint coverage cones — not just the reflexive equality case. The L1c "k₁ = 2 is the only k = 2 step" derivation correctly identifies that TA5a's `zeros ≤ 2` precondition fires exactly once, at the chain's first step. The chain-prefix-preservation argument in Home and Ownership is fully spelled out at each step (TA5(b)/(c), TA5-SigValid, T10a.4 each cited at the point of use), and the L11a corollary from GlobalUniqueness is properly decomposed into the `home ≠` and `home =` cases.

The PrefixSpanCoverage axiom is acknowledged as pending relocation to a span-algebra ASN; this is tracked in the Open Questions and matches the memory note on span-algebra-gap. The L9 dom(Σ.M) ≠ ∅ precondition (with its explanation of the empty-state carrier-root question) and the L1a membership clause (vs. mere structural T4-validity) reflect careful state-invariant discipline.

## REVISE

None.

## OUT_OF_SCOPE

None — the ASN's explicit scope section properly delimits operations, V-space mechanics, indexing, and policy as future-ASN material, and the open questions enumerate the right next-layer issues (transclusion interaction, compound link well-formedness, coverage-vs-decomposition query semantics, allocation ordering, type hierarchy semantics, store consistency with arrangements).

VERDICT: CONVERGED
