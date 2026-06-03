# Review of ASN-0068

## REVISE

### Issue 1: CV-SPAN-VIEW postcondition (c) is meta-prose, not a guarantee
**ASN-0068, CV-SPAN-VIEW, postcondition (c)**: "*Input parameterization.* `π_{m_a, m_b}` (and hence `π*_{m_a, m_b}`) depends on the input ... only through the induced depths `(m_a, m_b)`. ... This is an *input-dependent* presentational equivalence: the same triple `(v_a, v_b, n)` projects to different span-pairs at different depth pairs."
**Problem**: The "postcondition" restates the subscript notation — `π_{m_a,m_b}` consults `(m_a, m_b)` — and its verification concedes this is "Immediate from the definition." The closing sentence ("the same triple projects to different span-pairs at different depth pairs") is explanatory prose about the parameterization rather than a structural guarantee. This is the "new prose explaining why a construction is parameterized rather than what it claims" pattern. (a) Well-formedness and (b) Injectivity carry the content; (c) advances nothing.
**Required**: Delete postcondition (c) and its verification. If the depth-dependence needs noting, fold it into the signature line (`π_{m_a, m_b}`) where the subscripts already say it.

### Issue 2: CV-FIN bound-tightness aside in Example 3 is defensive justification
**ASN-0068, Example 3**: "This example also shows why CV-FIN's product bound, not the smaller `min(...)`, is the correct upper bound ... The product bound is itself not always tight — Example 1 achieves `|MaxRuns| = 1` against a product bound of `3·4 = 12` — but it is the smallest bound expressible from cardinalities of `dom(M)` alone."
**Problem**: This paragraph defends the *choice* of bound stated in CV-FIN against an imagined alternative (`min`) and litigates tightness. It does not verify a claim of the ASN; it argues for a drafting decision. The observation `|MaxRuns| = 3 > 2` that the example legitimately demonstrates is one sentence; the surrounding tightness/expressibility commentary is meta-prose about CV-FIN's formulation.
**Required**: Reduce to the single sentence establishing `|MaxRuns|` can exceed `min(|dom(M(d_a))|, |dom(M(d_b))|)`. Remove the "smallest bound expressible" defense and the Example-1 product-bound restatement.

### Issue 3: CV-SPAN-VIEW set-level lift restates a triviality
**ASN-0068, CV-SPAN-VIEW**: "Lifting per-run to set-level via the standard image construction ... `π*_{m_a, m_b}(M) = { π_{m_a, m_b}(r) : r ∈ M }`" and postcondition (b)'s "The set-level lift ... inherits injectivity, since an injection induces an injection on the powerset, so `π*_{m_a, m_b}` is a bijection between `Result` and its image."
**Problem**: The per-run map `π` plus its injectivity is the substantive content. The `π*` powerset-image apparatus and the "inherits injectivity ... bijection with its image" restatement add a textbook fact (an injection lifts to an injection on images) dressed as separate machinery. Nothing downstream in the ASN consumes `π*`; it is scaffolding around the real claim.
**Required**: State the per-run projection and its injectivity; drop the `π*` lift and the powerset-injectivity restatement, or compress to a half-sentence ("hence the run-set is recoverable from its span-pair image").

## OUT_OF_SCOPE

### Topic 1: Behavior under concurrent mid-comparison arrangement modification
The Open Questions raise invariants for concurrent modification during a comparison. CV-RO and CV-DETERM correctly fix the operation as a single-state snapshot; concurrency semantics belong to a later transition-interleaving ASN, not here. No action needed — correctly deferred.

### Topic 2: Multi-document / version-history composition
The Pairwise Scope section and several Open Questions name aggregation across version histories and multi-document correspondence composition. Keeping these out is correct; they would require a separate composition operator.

META: not applicable — the ASN specifies an abstract read-only operation (state-consultation only, no transition, depth-independent correspondence) and remains within system-guarantee territory; the findings are accreted prose, not drift.

VERDICT: REVISE
