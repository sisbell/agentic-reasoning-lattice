# Review of ASN-0086

## REVISE

### Issue 1: Use-site inventory in the off-chain-edge consequence is document bookkeeping, not argument

**ASN-0086, Remark — NestedLinkWitness**: "*Off-chain-edge consequence (stated here once).* ... R0 and the Emit_K partiality remark cite this consequence by name without restating it."

**Problem**: The parenthetical "(stated here once)" and the sentence enumerating downstream citers ("R0 and the Emit_K partiality remark cite this consequence by name without restating it") are pure organizational bookkeeping. They tell the reader how the document is laid out rather than advancing the consequence's content. This is the flagged anti-bloat pattern "a definition's introduction enumerates downstream consumers." The consequence stands on its own; citing sites can reference it without the source announcing who references it.

**Required**: Delete the "(stated here once)" tag and the use-site-inventory sentence. State the off-chain-edge consequence as a plain claim. The downstream sites already cite it by name — that suffices.

### Issue 2: Verbatim-repeated forward deferral to NestedLinkWitness

**ASN-0086, R0 (intro)** and **Definition — Emit_K**: both carry the identical clause "by the off-chain-edge consequence stated once in Remark — NestedLinkWitness."

**Problem**: The same deferral phrase appears verbatim in two sections (R0's load-bearing-domain paragraph and the Emit_K partiality remark), matching the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." Paired with the source remark's own "stated here once," the phrase "stated once" now occurs three times across the note, which is self-referential meta-prose rather than reasoning.

**Required**: Each site needs only the bare cross-reference (the consequence's name). Drop the "stated once" qualifier at all three occurrences; the consequence is a named claim and the reader does not need to be reminded it appears only once.

### Issue 3: Proof-narration meta-prose in R5 Steps 3–4

**ASN-0086, R5, Step 3**: "so R0's emission argument is uniform over *any* L3-conforming triple regardless of `coverage(F)`, `coverage(G)`, or `coverage(K)`; the only content-dependent check, L3, is met here." **Step 4**: "The Step 3 uniformity does not inspect which slot the self-targeting endset occupies, so the slot-symmetric discharge is immediate."

**Problem**: These sentences describe a *property of the proof* ("the emission argument is uniform," "the uniformity does not inspect which slot") rather than executing the argument. Step 4's from-set case is already symmetric by the explicit L3-conformance checks restated in that step; the appeal to "Step 3 uniformity" is redundant narration that the reader must skip to reach the actual discharge.

**Required**: For Step 4, retain the concrete checks (arity 3, `G_self ∈ Endset`, `∅ ∈ Endset`, `K` non-empty) and the R0 invocation; remove the "Step 3 uniformity does not inspect..." sentence. In Step 3, the "uniform over any L3-conforming triple regardless of coverage" clause can be cut — R0's statement already quantifies over arbitrary `F, G ∈ Endset` and `K ∈ T_admissible`, so the genericity is carried by R0's own quantifiers.

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity model for Emit vs Observe
The Open Questions raise atomicity of Emit relative to concurrent Observe and the consistency model for observed `A_K` transitions. These belong in a future ASN layering a concurrency semantics over the relational vocabulary; they are not defects in this note's single-writer, sequential-transition treatment.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The handling of `|Σ.L(a)| > 3` links as elements of higher-arity relations (vs binary projections) is correctly deferred. This note's restriction to standard triples is stated explicitly and consistently; the generalization is new territory.

VERDICT: REVISE

The rigor content is sound — I checked R0a (both home cases), R-Scope, the wp Case 2 derivation (both directions and the two-restriction necessity argument), L-ContiguousPrefix's non-circular dependency on ChainMembershipForOrigin, and the worked sketch's concrete tumbler arithmetic, and found no correctness gaps. The remaining findings are residual forward-reference meta-prose flagged by the anti-bloat classifier.
