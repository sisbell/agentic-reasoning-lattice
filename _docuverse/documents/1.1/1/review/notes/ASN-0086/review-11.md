# Review of ASN-0086

## REVISE

### Issue 1: R0a's induction uses an implicit stronger invariant than the stated antichain
**ASN-0086, R0a Proof, Case 1 sub-case B**: "Every `a' ∈ dom(Σ.L)` with `home(a') = d` was itself emitted at an earlier step under the discipline, so by induction on the chain leading to Σ each such a' lies at `incʲ(d.0.s_L.1, 0)` for some j ≥ 0 — i.e., every existing link under d is a sibling of d.0.s_L.1 in the link-element-field allocator's enumeration."

**Problem**: The main induction's stated hypothesis is "antichain holds at Σ". But sub-case B's argument requires the structural property "every prior link with `home = d` lies in the sibling stream from `d.0.s_L.1`". This is strictly stronger than antichain — antichain alone permits same-home links from disjoint allocators, which sub-case B's argument cannot dispatch. The parenthetical at the end of sub-case B acknowledges the gap ("the discipline on prior steps is what places every prior link under d into the sibling stream"), but the auxiliary invariant remains unstated as a formal claim. The proof intertwines a main induction on antichain with an implicit sub-induction on the discipline's structural trace, and a Dijkstra-style induction should expose both.

**Required**: Either (a) introduce the auxiliary invariant explicitly — e.g., "Sibling-stream invariant: for every reachable Σ under the discipline, every `a ∈ dom(Σ.L)` with `home(a) = d` lies at `incʲ(d.0.s_L.1, 0)` for some `j ≥ 0`" — prove it by induction on chain length, then derive antichain as a corollary via T10a.2 (same-home) and zero-count additivity (different-home); or (b) rephrase sub-case B to derive its conclusion from the stated antichain hypothesis alone without appealing to "the chain leading to Σ".

### Issue 2: Open Questions cross-reference is unfulfilled
**ASN-0086, Setup hypothesis paragraph**: "Under L14's native scoped form (without globally `s_C`-resident content), R0, R4, and R5 would hold slice-wise on the `s_C`-resident content slice; the Open Questions section traces the further implications."

**Problem**: No Open Question actually traces what happens when Setup is relaxed. The seven Open Questions cover concurrency, multi-arity, ordering, atomicity, cardinality bounds, discipline elevation, and type-catalog evolution — none address the slice-wise behavior of R0, R4, and R5 in the absence of globally `s_C`-resident content. The cross-reference makes a specific claim ("traces the further implications") that the destination does not deliver.

**Required**: Either add a specific Open Question tracing what R0/R4/R5 say slice-wise when Setup is relaxed (e.g., "What is the precise statement of R0/R4/R5 in their slice-wise forms, and which substrate consumers can operate under those weaker forms?"), or remove the "traces the further implications" cross-reference and replace with a neutral observation.

### Issue 3: R6c's reach excludes arrangement-modifying transitions
**ASN-0086, R6c statement**: "Once retracted, a tuple stays out of every future active subset: `(A Σ, K, (a, F, G) ∈ L_K^Σ : a ∈ nullified(Σ) : (A Σ' : Σ ⊑ Σ' :: (a, F, G) ∉ A_K^{Σ'}))`"

**Problem**: `Σ ⊑ Σ'` is defined as the reflexive-transitive closure of `→`, which excludes arrangement-modifying transitions (per the Scoping note under the State Transition Relation definition). The user-facing claim "every future active subset" naturally reads as covering all reachable states, including those reached via arrangement modifications interleaved with `→` steps. The Scoping note acknowledges that arrangement modifications preserve every L-invariant trivially, but R6c's statement, read in isolation, leaves the parallel-vocabulary case implicit.

**Required**: Either extend `Σ ⊑ Σ'` to include arrangement-modifying transitions (and verify R6a's proof still goes through, which it does, since `Σ'.L = Σ.L` for such transitions makes R6a's `L_R^Σ ⊆ L_R^{Σ'}` step an equality), or add a parenthetical to R6c noting "and to all states reached from Σ by a mixed sequence of `→`-steps and arrangement-modifying transitions, since the latter leave `Σ.L` untouched and so preserve `nullified` and `A_K` trivially."

## OUT_OF_SCOPE

None. The ASN's Open Questions adequately delineate the future work; Issues 1–3 above are within-ASN clarity issues, not future-ASN topics.

VERDICT: REVISE
