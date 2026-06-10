# Review of ASN-0116

This is a careful, mature note. The valid-composite construction is sound, the boundary cases (front `J=1`, append `J=N+1`, empty subspace with its two emission sub-cases) are all walked concretely, the four-part witness decomposition in IP4 is complete and disjoint, and the IP6 weakest-precondition correctly lands on a *containment* rather than emptiness. The block-disjointness interval argument, the I3-V/I3-CS attribution of the vacated block, and the J0/J1★/J1'★ discharge against the range identity are all rigorous. My findings are precision-level.

## REVISE

### Issue 1: `coverage` carries a state subscript that the foundation forbids
**ASN-0116, IP4 (LinkSurvival)**: "For every endset `e` existing in `Σ`, `coverage_{Σ'}(e) = coverage_{Σ}(e)` (by L12 + LP3★ across the composite) — no link's designated content changes." (also the IP6 footnote: "`coverage_{Σ'}(eᵢ) = coverage_{Σ}(eᵢ)`")
**Problem**: The foundation is explicit that coverage does not consult state — ASN-0098: "Coverage is a purely combinatorial property of the endset's span representation — it does not consult any state component," and LP3★ is stated as `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` with the state inside the *argument*, never as a subscript on `coverage`. As written, `coverage_{Σ'}(e) = coverage_{Σ}(e)` is either trivial (if `e` is a fixed endset value, both sides are literally `coverage(e)` and L12+LP3★ are not needed) or under-specified (if `e` denotes a link slot, the precise object is `coverage(Σ.L(a).eᵢ)`). The L12+LP3★ citation only makes sense under the second reading, which is exactly LP3★'s native form. Standard 7: the ASN should use the foundation's notation, not re-annotate `coverage` with a state index.
**Required**: Replace `coverage_{Σ}(e)`/`coverage_{Σ'}(e)` with the foundation form `coverage(Σ.L(a).eᵢ)` / `coverage(Σ'.L(a).eᵢ)`, stating the invariance directly as LP3★. The body's unsubscripted `coverage(e)` is already correct and needs no change.

### Issue 2: the block-disjointness intervals are re-derived after being cited
**ASN-0116, "## The document remains one coherent sequence"**: "by the block-disjointness fact (Effect), the three index intervals `{1, …, J-1}` (prefix), `{J, …, J+n-1}` (new), `{J+n, …, N+n}` (shifted suffix) are consecutive, pairwise disjoint, and union to `{1, …, N+n}`."
**Problem**: This paragraph cites the block-disjointness fact "(Effect)" and then re-lists the same three intervals and re-asserts consecutiveness/disjointness/union — the content already established verbatim in the Effect section's "We record first the block-disjointness fact" sentence. The re-listing adds nothing after the citation; the note carries the anti-bloat classifier and this is precisely the "restates rather than cites" pattern. The genuinely new content here is the Nelson-Q10 connection and the reduction of the starred invariants to unstarred D-CTG/D-MIN/D-SEQ on the content subspace.
**Required**: Cite the block-disjointness fact and I-DOM, drop the interval re-listing, and keep only the new material (the reading-order conclusion and the starred→unstarred reduction).

### Issue 3: IP1's "within the S8★ partition" can mislead — the inserted block need not be a maximal-run element
**ASN-0116, "## The document remains one coherent sequence"**: "IP1 records the narrower fact that the inserted material forms one correspondence run within the S8★ partition."
**Problem**: The block's start `a` is fresh, so the block never I-merges *forward* with the shifted suffix (whose addresses are all strictly below `a`). But it can I-merge *backward*: if position `q_{J-1}` holds the current maximum origin-`d` address `a_prev` — a reachable configuration once arrangements can be reordered (K.μ~, ASN-0047) so that V-order ≠ I-order — then `a = a_prev + 1 = shift(M(d)(q_{J-1}), 1)`, making the block I-adjacent to the left run and hence part of the *same* maximal run. S8★'s partition is into *maximal* runs, so "forms one correspondence run within the S8★ partition" reads as claiming partition-element status the block need not have. IP1's formal statement ("the block is a correspondence run," lockstep) is correct and unaffected; only this gloss is imprecise.
**Required**: Soften the gloss to state that the inserted material is a correspondence run (S8's sense, not necessarily maximal), noting it may I-merge backward with the adjacent left run and thus need not be a standalone element of the maximal-run partition.

## OUT_OF_SCOPE

The Open Questions (transclusion at the insertion point, concurrent insertion freshness, transcluded-content provenance, post-edit fragmentation) correctly defer the genuinely new territory; no claims in this note stray into COPY/DELETE/REARRANGE/MAKELINK. Nothing to add.

VERDICT: REVISE
