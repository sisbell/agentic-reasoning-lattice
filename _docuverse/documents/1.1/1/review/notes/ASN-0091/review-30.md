# Review of ASN-0091

## OUT_OF_SCOPE

### Topic 1: Link-subspace REARRANGE semantics
ASN-0084's CS3 fixes the cut subspace to s_C, so this ASN addresses only content-subspace rearrangement. What semantics rearrangement should carry on the link subspace — and what invariants such an operation would preserve — is appropriately raised as Open Question 2.

### Topic 2: Mixed sequences interleaving REARRANGE with other operations
The composition section addresses pure REARRANGE sequences. Interleaving with K.α, K.λ, K.μ⁺, K.μ⁻, K.δ, K.σ, K.ρ is noted briefly (deferring to ASN-0098's LP-Comp) but full mixed-sequence analysis belongs to a separate ASN.

### Topic 3: Quantitative bounds on run-decomposition cardinality change
RE-frag/RE-coal/RE-eq and their ★ forms establish existence and arbitrary direction sequences. Open Question 4 asks for tighter quantitative per-invocation bounds — appropriate for a future ASN.

### Topic 4: Universality of cut-sequence rearrangements
Open Question 5 asks whether every admissible π is realizable as a finite composition of cut-sequence rearrangements. This expressiveness question is out of scope.

### Topic 5: Cross-document transclusion split by cuts
Open Question 1 asks about specific guarantees when a cut splits a transcluded span into non-contiguous pieces. The general transclusion preservation (RE-trans) is established; finer-grained guarantees belong to a future ASN.

### Topic 6: Observational equivalence of distinct REARRANGEs
Open Question 3 asks when distinct REARRANGE transitions are equivalent at the discoverability level rather than arrangement-equality level. Refinement of equivalence belongs to a future ASN.

VERDICT: CONVERGED
