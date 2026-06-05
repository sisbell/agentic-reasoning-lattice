# Review of ASN-0100

## REVISE

### Issue 1: Per-address content invariant discharge is duplicated across two sections
**ASN-0100, §Post-state V-position well-formedness (S7 bullet) and §Atomicity (the "K.α and K.ρ frame M" paragraph)**: Both sections discharge S7a, S7b, C1b, and C1c for the freshly allocated `a_k`, with the C1b justification appearing verbatim in both:

> "C1b (#E(a_k) ≥ 2, since A_C(d)'s first emission has #E = 2 (FirstEmission, ASN-0093) and every subsequent inc(·, 0) emission preserves length (TA5(c), ASN-0034))"

and the C1c, S7a, S7b justifications appearing in near-identical form (`zeros(a_k)=3 by C1`; `origin(a_k)=d by A_C(d)'s emission discipline`; the ChainMembershipForOrigin/ChainDiscipline chain).

**Problem**: This is accreted duplication — the same per-address discharge stated twice. Because §Atomicity already establishes the invariants hold "the moment its K.α firing commits a_k to dom(C), and persists unchanged to Σ' by P0," the §Post-state discharge of the *same* per-address invariants is redundant: the post-state assertion follows from the per-firing assertion plus P0. The precise reader must verify the two copies agree rather than reading one argument once.

**Required**: Discharge the per-address content invariants (S7a, S7b, C1b, C1c, plus P6/P7/L14/L0-content) in one place — the §Atomicity per-firing paragraph is the stronger location, since it covers every intermediate and Σ' follows by P0. In §Post-state V-position well-formedness, replace the per-address re-derivation with a one-line pointer, or move the post-state S7-invariant content there and drop the §Atomicity copy. Do not state both.

### Issue 2: Step 1 cites the wrong lemma for the freshness precondition
**ASN-0100, §Substrate Decomposition, step 1**: "Each K.α firing satisfies its freshness precondition against the intermediate state immediately preceding it (justified by ChainEnumerationInjectivity; ASN-0093 — see Effect One above)."

**Problem**: K.α's freshness precondition is `a_k ∉ dom(C) ∪ dom(L)`. ChainEnumerationInjectivity establishes only that the chain enumeration is injective (distinctness *within* the chain) — it does not discharge freshness against the existing store. The lemma that discharges the precondition is SubsequentEmissionFreshness (with FirstEmissionFreshness for the boundary), as §Effect One correctly states. The inline citation names a lemma that proves a different fact.

**Required**: Cite SubsequentEmissionFreshness / FirstEmissionFreshness for the freshness precondition (these already subsume the within-composite distinctness via ChainEnumerationInjectivity). Reserve the ChainEnumerationInjectivity citation for the S4/distinctness argument where it is actually load-bearing.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L)
**Why out of scope**: The ASN correctly bounds itself to the content subspace and names link-subspace insertion as a structurally distinct future operation. Not an error here.

### Topic 2: COPY, DELETE, REARRANGE, version derivation, replication
**Why out of scope**: Explicitly bounded in §Bounding the Scope; governed by other transitions.

VERDICT: REVISE
