# Review of ASN-0107

## REVISE

### Issue 1: R1's (P-last) precondition does not establish "a leaves Qᵢ(Σ')" under content sharing

**ASN-0107, R1 (MinimalDecrementNoStoreRetraction)**: "**(P-last)** *Last position.* The removed V-position is the last consulted one mapping to its resolved I-address `a`, so `a` leaves `Qᵢ(Σ')`."

**Problem**: The label ("Last position") and the text ("the last consulted one mapping to ... `a`") name two different conditions, and neither establishes the stated consequence:

1. For a `K.μ⁻` step to remove a *single* consulted entry `v ↦ a`, the retention scope must drop exactly one position, which by `K.μ⁻`'s canonical-prefix retention (`R = {[S,1,…,1,k] : 1 ≤ k ≤ n'_S}`, PerSubspaceContractionScope, ASN-0047) forces `v` to be the *arrangement-maximal* position `[S, n_S]` in its subspace. R1 never states this; "last consulted one mapping to `a`" is not the same as "arrangement-maximal."
2. The note itself admits content sharing (M13/S5: distinct V-positions may map the same I-address, invoked explicitly in D2 and the worked example). If `a` is mapped by `v` *and* by some earlier retained position `[S, j]` with `j < n_S`, then removing only `v` leaves `a ∈ Qᵢ(Σ')` via the surviving position. So "the last consulted one mapping to `a`" does **not** imply `a` leaves `Qᵢ(Σ')` — the case the precondition is supposed to guarantee.

The headline result `Δnum_disc ∈ {−1, 0}` survives (the unguaranteed sub-case merely lands in the `0` branch), but the derivation as written asserts a consequence that fails under the sharing the ASN elsewhere relies on.

**Required**: Either (a) add the condition that `v` is the unique consulted position mapping to `a` (so `a` genuinely leaves `Qᵢ(Σ')`), or fold the shared-`a`/retained-duplicate situation into the explicit `Δ = 0` branch; and (b) state the arrangement-maximality of `v` that single-entry `K.μ⁻` actually requires, rather than conflating it with the I-address-sharing notion under one "Last position" label.

### Issue 2: D2 carries defensive meta-prose explaining why downstream lemmas do *not* apply

**ASN-0107, D2 (DiscoveryNonMonotonicity)**: "We reason about `Qᵢ` directly: it is a forward image of a query region, not the preimage `project(e, d, Σ)` of an endset's coverage that ASN-0098's LP9–LP11 govern, so those lemmas about `project` do not transfer to it." and the parenthetical "(The two facts used — strict domain extension and prior-domain agreement — are the structural premises of LP9, common to both extension transitions, applied here to the forward image rather than the preimage.)"

**Problem**: This is meta-prose about methodology — it explains which foreign lemmas are *not* used and which premises of LP9 are *re-used*, rather than advancing the claim. The reader must skip past a disclaimer about `project`/LP9–LP11 to reach the actual reasoning, which stands on its own (the extension/contraction/reordering arguments are self-contained). Flagged per the anti-bloat mandate's "use-site inventory / methodology-provenance" pattern.

**Required**: State the forward-image argument directly. Drop the disclaimer about `project` and the LP9-premise inventory; if the structural facts (domain extension, prior-domain agreement) are needed, assert them, not their lineage.

### Issue 3: R6 derivation contains methodology-provenance prose

**ASN-0107, R6 (CountedLinkPreservationWP)**: "This is the conjunctive-`sat` analogue of ASN-0098's LP12a (ContractionDiscoverabilityWP), which pulls the *existential* `discoverable_from` postcondition back through the same `K.μ⁻` effect; the pullback method is taken from there unchanged, the only difference being the conjunction over all three slots that `sat` imposes where LP12a takes a disjunction."

**Problem**: This sentence narrates where the proof technique came from ("taken from there unchanged") rather than performing or advancing the derivation, which follows immediately and is self-contained. It is the "essay about methodology in a structural slot" pattern.

**Required**: Remove the provenance narration. The subsequent "*Derivation.*" paragraph already gives the complete wp pullback; the LP12a comparison adds no proof content.

### Issue 4: R1's opener duplicates the R-section introduction

**ASN-0107, R1 opener**: "The section opener already settled the store side: no link-removal transition exists, so the existence count never falls and only the discovery count moves, through arrangement contraction."

**Problem**: The R-section introduction already states this in full ("The substrate provides no link-removal transition (L12) ... the existence count (E2) therefore cannot fall ... Only the discovery count moves under withdrawal ... through one mechanism alone: arrangement contraction"). R1's opening sentence restates the same content in different words — the "two paragraphs say the same thing" pattern.

**Required**: Drop the restatement and have R1 proceed directly to the minimal-contraction analysis.

## OUT_OF_SCOPE

### Topic 1: Multi-document independent anchoring of the three request parts
The first Open Question (parts anchored to different documents' separately-evolving arrangements) is genuinely new territory — a richer request model than the single-querying-document discovery anchoring this ASN specifies. Correctly deferred.

### Topic 2: Coincidence of discovery and existence counts; count-vs-retrieval-cardinality relationship
The second and third Open Questions concern conditions under which the two anchorings agree and the relationship to the retrieval operation's returned set. The latter touches FINDLINKS/ASN-0099, which the scope section excludes. Correctly out of scope.

VERDICT: REVISE
