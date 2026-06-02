# Review of ASN-0047

## REVISE

### Issue 1: SSGU cross-node distinctness cites T10, whose precondition fails for nested baptised nodes

**ASN-0047, *NodeRootedForest* / *Subtree-scoped GlobalUniqueness (SSGU)***: "For any inc-output `a` with `N ≼ a` for a baptised node `N`, GlobalUniqueness scoped to `N`'s subtree ... assigns `a` to exactly one allocation event within that subtree; cross-node distinctness (T10, ASN-0034, via CrossNodeAccountBase) excludes every event under a distinct baptised node `N' ≠ N`."

**Problem**: NodeLineage forces `n₀ = [1] ≼ e` for every node, and the ASN itself affirms in CrossNodeAccountBase that nodes may *nest* ("if one node nests in the other — say `N₁ ≼ N₂` ... the case NodeBaptism does not forbid, since multi-component node tumblers are T4-legal"). When `N ≼ N'`, the prefix cones overlap: any inc-output `a'` under `N'` satisfies `N ≼ N' ≼ a'`, so `a'` lies in both `N`'s and `N'`'s "subtree" under the prefix test. T10 (PartitionIndependence) requires `N ⋠ N' ∧ N' ⋠ N` — exactly the hypothesis that fails for a nested-node pair. So the blanket "cross-node distinctness (T10)" claim is unsound for the nesting case the ASN explicitly permits. The actual distinctness for nested nodes comes from the zero-separator divergence argument (every non-node inc-output introduces a zero where the deeper node has a nonzero component), which is what CrossNodeAccountBase in fact uses — not T10.

**Required**: Restate SSGU's cross-node clause to case-split on prefix-comparability: incomparable baptised nodes are separated by T10; nested baptised nodes are separated by the zero-separator divergence (the CrossNodeAccountBase mechanism generalised from account bases to arbitrary inc-outputs). Either way the citation "T10" alone is wrong for nested nodes and must name the correct premise.

### Issue 2: K.μ⁻ precondition carries defensive forward-deferring meta-prose

**ASN-0047, *Elementary transitions*, K.μ⁻ precondition**: "they are established in *K.μ⁻ admissible contraction shape* below. ... The constructive precondition is *equivalent* to the post-state characterization ...; the equivalence ... is proved in *K.μ⁻ admissible contraction shape* below. The effect clause ... and the strict-contraction clause ... carry the proper-subset requirement on their own. The value-preservation clause ... is satisfied automatically by the restriction definition ..."

**Problem**: This passage defers twice to the same downstream subsection (*K.μ⁻ admissible contraction shape*) and then re-litigates clause-by-clause which conjunct "carries" which requirement — defensive justification that does not advance the precondition's content. It matches the flagged accretion patterns (multiple deferrals to one downstream location; defensive justification in a structural slot). The precise reader must skip past the bookkeeping to recover what K.μ⁻ actually requires.

**Required**: Reduce to the load-bearing precondition (caller chooses per-subspace retention counts `n'_S ∈ {0,…,n_S}` with at least one strict `n'_S < n_S`; `M'(d) = M(d) ↾ R`) and a single pointer that the derived per-state invariants and the equivalence are proved below. Drop the per-clause "carries the requirement on its own" commentary.

### Issue 3: Triple-stated J1★ derivation rationale

**ASN-0047, *Scoped coupling constraints* (J1★ derivation) and *Extended reachable-state invariants* (P4★, P7a cells/prose)**: the "range-based, scoped to the content subspace because the K.μ⁺ amendment introduces only content-subspace V-positions" rationale, and the `ran(M'(d)|_{s_C}) ⊆ dom(C)` chain from S3★'s content clause, are restated in (a) the J1★ derivation, (b) the P7a composite-boundary argument, and (c) the J1★/J1'★ rows of the Properties-Introduced tables.

**Problem**: The same wp-from-P4★ reasoning and the same `a ∉ dom(C) ⟹ a ∉ ran(M(d)|_{s_C})` step appear in different sections in different words — the "two paragraphs say the same thing" accretion pattern. The P7a argument re-derives the range-new conjuncts that the J1★ section already established.

**Required**: State the range-based content-subspace scoping once (at the J1★ derivation) and have P7a cite it rather than re-deriving the `ran ⊆ dom(C)` chain.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
The Open Question on a "renumbering-aware link-arrangement contraction" (modelling the implementation's interior `DELETEVSPAN` compaction) is correctly deferred — K.μ⁻'s suffix-only contraction is sufficient for this ASN, and interior-compaction operations belong to the operations layer, which is out of scope.

### Topic 2: Concurrency of link allocation under a shared home document
The Open Question on serialization of concurrent same-document allocation is genuinely future territory; SequentialTransitionAxiom totally orders transitions here, so concurrency is not an error in this ASN.

VERDICT: REVISE
