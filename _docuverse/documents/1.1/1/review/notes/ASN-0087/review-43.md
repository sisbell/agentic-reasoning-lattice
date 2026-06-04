# Review of ASN-0087

The technical content here is strong. I checked the composite decomposition, the precondition reduction (`ℓ ∉ ran(Σ.M(d))` via S3★ + S3★-aux + freshness), the two-part S2 exclusion, the full per-state / boundary / transition invariant sweep against ASN-0047's `ExtendedReachableStateInvariants` list, the wp case split, the worked example arithmetic, and the LP9/LP18 side-effect specialization. I found no correctness gaps — boundary cases (empty non-type endsets, first link vs. subsequent, reflexive endset, forward-reaching prior endset) are all addressed. The findings below are the meta-prose / forward-reference accretion the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: Implementation-rationale tail on M-NoIndexState
**ASN-0087, "What Is Indexed?"**: "An implementation may maintain an auxiliary structure — a reverse lookup from I-addresses to link addresses, the *spanfilade* in Gregory's implementation — for efficient computation. Such structures are caches: any state where they are consistent with `L` and `M` produces the same `project` and `discoverable_from` results. The abstract claim is the discovery *property*; the index is a performance choice."
**Problem**: The spec claim is established by the preceding sentence (discoverability is computed from `L` and `M`, no separate component needed). The cache/spanfilade/"performance choice" elaboration is implementation-mechanics prose that does not advance the M-NoIndexState claim — it explains why an implementation *might* cache, which is outside the abstract specification's territory.
**Required**: Reduce to the spec statement: discoverability is a derived function of `L` and `M`, so no index state component is required. Drop the cache rationale.

### Issue 2: Reflexive route asserted-then-deferred across three sections
**ASN-0087, "Inputs" / "What Is Indexed?" / "A Worked Example"**: the reflexive route appears in *Inputs* ("a caller authoring a reflexive endset ... may predict `ℓ`"), in *What Is Indexed?* ("The home document alone gains an additional, arrangement-independent reflexive route, derived as route (ii) of *Weakest Precondition for Discoverability*, Case 2"), and again in the worked-example reflexive variant — but the actual derivation lives only in wp Case 2 (M-Reflexive).
**Problem**: This is the named accretion pattern — multiple paragraphs in different sections asserting a conclusion and deferring to the same downstream location before it is proved. *What Is Indexed?* states the home-document reflexive privilege as fact and forward-points; wp Case 2 then re-derives it. A reader must hold the unproved assertion across several sections.
**Required**: State the reflexive route once, at the point it is derived (wp Case 2 / M-Reflexive). Reduce the *Inputs* and *What Is Indexed?* mentions to bare cross-pointers without restating the conclusion, or remove the early assertions.

### Issue 3: Redundant restatement in wp Case 1
**ASN-0087, "Weakest Precondition for Discoverability," Case 1**: "The allocation of `ℓ` contributes nothing to discoverability from documents other than `d`; the predicate this case adds is the independent membership obligation `d_target ∈ dom(Σ.M)` that keeps `discoverable_from` defined at the post-state."
**Problem**: This sentence restates conclusions already established two paragraphs earlier (in *Membership precondition* and the case derivation itself). It advances no new reasoning.
**Required**: Delete the trailing sentence; the wp formula and its derivation already carry the content.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of endsets referencing never-allocated addresses
**Why out of scope**: The ASN's own Open Questions correctly defer this to a future ASN; L4 (EndsetGenerality) already permits such spans, and constraining them is new territory, not an error here.

VERDICT: REVISE
