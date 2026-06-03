# Review of ASN-0069

## REVISE

### Issue 1: §"Identity by Sub-Allocation" closing paragraph is roadmap meta-prose
**ASN-0069, §"Identity by Sub-Allocation", final paragraph**: "The identity argument is structurally independent of content inheritance, correspondence, and isolation. K.δ creates an empty-arrangement document; the fork's arrangement starts empty (the `Document(e)` effect clause of K.δ sets `M'(d_new) = ∅`). K.δ alone is exactly the empty fork (V7); §"Sharing, Not Duplication" derives the content-inheritance phase that turns the empty entity into a *version of* `d_src`."

**Problem**: The paragraph advances no part of the identity derivation. Its first sentence is a modularity claim *about* the argument ("structurally independent of…"); its last clause is a forward pointer to §"Sharing, Not Duplication." The only object-level fact — that K.δ initialises `M'(d_new) = ∅` — is already stated in V6's derivation, V7's section, and V0's empty-case effects. This is essay/roadmap content in a structural slot, the accretion pattern the anti-bloat pass targets.

**Required**: Delete the paragraph. The identity section's conclusion (V1) stands on its own, and V7 / §"Sharing, Not Duplication" carry their own claims without needing this signpost.

### Issue 2: §"Structural Correspondence" perpetuity sentence only signposts V12
**ASN-0069, §"Structural Correspondence"**: "The intercomparison guarantee is *perpetual*: V8 holds in the post-fork state, and its consequences propagate to every subsequent state in which neither side has overwritten the relevant V-positions. The permanence facts that underwrite this propagation are collected once in V12."

**Problem**: The second sentence carries no content — it announces that the supporting facts appear later (V12) rather than supplying or summarising them. The propagation argument is wholly in V12; this is a bare forward pointer that the precise reader must skip past to reach the actual claim.

**Required**: Either fold the perpetuity statement into V12 (where the permanence facts live) or drop the trailing signpost sentence, keeping only the qualified first sentence as the perpetuity claim.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork vs. source modification beyond atomic sequencing
**Why out of scope**: Listed in the ASN's own Open Questions and not in this ASN's territory; the sequential atomic-transition model is the only guarantee the substrate currently supplies.

### Topic 2: Snapshot vs. living forks, transcludent sources, version-space coherence
**Why out of scope**: These are correctly deferred to future ASNs; V9a's clarification that `R` records containment (not derivation edges) keeps this ASN clear of version-DAG territory, which is explicitly out of scope.

VERDICT: REVISE
