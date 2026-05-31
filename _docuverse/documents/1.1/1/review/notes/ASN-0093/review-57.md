# Review of ASN-0093

## REVISE

### Issue 1: ChainUniformZeroCount is given two incompatible derivations
**ASN-0093, Per-chain disciplines vs. discharge matrix vs. worked example**:
- Disciplines block: "**ChainUniformZeroCount.** Every element of `A_C(d)` ... has `zeros = 3`. *Source: ASN-0040 SiblingStream postcondition*."
- Matrix (C1/C1b/L1, K.α/K.λ subsequent-emit): "`zeros(a) = zeros(a_prev) = 3` by B5a (ChainUniformZeroCount) and the IH on `a_prev`."
- Worked example Step 8: "`zeros(ℓ_new) = 3` (ChainUniformZeroCount — preserved under `inc(·, 0)` per ChainDiscipline, anchored at FirstEmission's `zeros = 3`)".

**Problem**: ChainUniformZeroCount and B5a (SiblingZerosPreservation, ASN-0040) are distinct foundation results — B5a is the *per-step* preservation `zeros(inc(t,0)) = zeros(t)`, while ChainUniformZeroCount is the *chain-level* "all elements `zeros = 3`" derived from the SiblingStream postcondition `cₙ = [p₁…p_{#p}, 0…0, n]` at depth 1. The matrix writes "B5a (ChainUniformZeroCount)" as if they were one citation, and Step 8 re-justifies ChainUniformZeroCount via "preserved under `inc(·,0)` per ChainDiscipline" (i.e., the B5a-per-step route), contradicting the disciplines block's stated source (the SiblingStream postcondition). A reader cannot tell which result is load-bearing where, and whether the parenthetical is a synonym or a second citation.

**Required**: Pick one route per use-site and label it consistently. Where the chain-level fact is wanted (`a ∈ A_C(d) ⟹ zeros(a) = 3`), cite ChainUniformZeroCount alone (sourced from the SiblingStream postcondition). Where the per-step fact is wanted (`zeros(inc(a_prev,0)) = zeros(a_prev)` with IH on `a_prev`), cite B5a alone. Drop the conflated "B5a (ChainUniformZeroCount)" form and the divergent Step-8 justification.

## OUT_OF_SCOPE

### Topic 1: Concrete verification of an `N > 3` link
The worked example exercises only StandardTriple `N = 3` instances; L3's distinctive claim ("admits arbitrary `N ≥ 3`", beyond Gregory's fixed 3) is never exercised concretely. The L3 discharge is arity-agnostic (precondition pins `|L(ℓ)| ≥ 3`), so this is not a correctness gap in the substrate — a worked `N = 4` instance would belong to a higher-arity-discipline note, not a revision here.

VERDICT: REVISE
