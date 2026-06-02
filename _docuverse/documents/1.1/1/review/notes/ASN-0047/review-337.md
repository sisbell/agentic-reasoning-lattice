# Review of ASN-0047

## REVISE

### Issue 1: Forest-scoping rationale for GlobalUniqueness is stated twice
**ASN-0047, NodeRootedForest / SSGU**: NodeRootedForest says "Cross-node distinctness — addresses under distinct baptised nodes `N₁ ≠ N₂`, including prefix-nested ones — is not a within-subtree GlobalUniqueness consequence; it is discharged by SSGU below." SSGU then re-states the same caveat: "because the `inc`-allocator structure is a forest, GlobalUniqueness cannot be applied unscoped — cross-node distinctness ... first excludes every event under a distinct baptised node `N' ≠ N` ...".

**Problem**: The load-bearing fact (the allocator structure is a forest, so foundation GlobalUniqueness applies only within a node-rooted subtree) is established in NodeRootedForest and then re-explained inside SSGU. This is the "two paragraphs say the same thing in different words" / forward-reference-with-rationale pattern the anti-bloat pass targets. The reader must read the same non-circularity argument twice before reaching the operative statement.

**Required**: State the forest caveat once (in NodeRootedForest), and let SSGU state only its operative conclusion ("scoped to the node-rooted subtree at `N`, GlobalUniqueness assigns `a` to exactly one event") without re-deriving why the unscoped application fails.

### Issue 2: Essay prose in the K.μ⁺ precondition restates S2 "made explicit"
**ASN-0047, K.μ⁺ precondition (*Pairwise V-position distinctness on new mappings*)**: "the newly added V-positions ... are pairwise distinct — this is S2 (ArrangementFunctionality, ASN-0036) preservation made explicit for K.μ⁺'s multi-position semantics ... making `M'(d)` a partial function (S2) by construction rather than by accident."

**Problem**: The precondition already requires new mappings disjoint from `dom(M(d))` with single-valued images; the S2 matrix cell discharges functionality. The "made explicit ... by construction rather than by accident" gloss is meta-prose explaining the relationship to S2 rather than adding a precondition. It is essay content in a structural (precondition) slot.

**Required**: Drop the explanatory gloss; if a distinctness clause is genuinely needed beyond the disjointness already stated, state it as a bare conjunct and let the S2 row carry the discharge.

### Issue 3: K.δ case (ii) sub-case discharge overlaps the dedicated discharge section
**ASN-0047, K.δ box vs *K.δ case (ii) discharge and parent-allocator activation***: The K.δ box already walks k = 0 / k = 1 / k = 2 with each sub-case's freshness reading (FrontierEquivalence vs ChildSpawnFreshness) and admissibility. The later dedicated section re-narrates the same k-labels and freshness mechanisms ("spawn-admissibility conjuncts ... are stated once at the K.δ box and are not repeated here") while the genuinely new content is only the parent-allocator dispatch and spawnPt-premise table.

**Problem**: The section straddles "new content (parent-allocator activation)" and "relocated restatement of the box's sub-case discharge." The relocated half is the pattern flagged: prose that re-says what the carrier already states.

**Required**: Restrict the dedicated section to the parent-allocator activation / spawnPt-premise table that the box omits, and reference the box for the freshness/admissibility discharge instead of re-narrating each k-label.

## OUT_OF_SCOPE

None — the candidate gaps I checked (interior link withdrawal with renumbering, type-only links, transclusion-chain provenance, concurrent allocation) are already captured as Open Questions.

VERDICT: REVISE
