# Review of ASN-0051

## REVISE

### Issue 1: SV1 and SV12 numbering gaps
**ASN-0051, Properties Introduced table and throughout**: The survivability labels run SV0, SV2, SV3, SV4, SV5, SV6, SV7, SV8, SV9, SV10, SV11, SV13. Labels SV1 and SV12 appear nowhere in the document or table.
**Problem**: Numbering gaps confuse downstream consumers — a reader citing SV13 may search for SV12 and find nothing. The commit log entry "promote SV7 to DiscoveryInvarianceUnderLFrame, demote coupling absence to corollary" suggests prior revisions reorganized labels, but the final document doesn't explain the gaps. Future ASNs that cite "SV-N" must be able to find each N.
**Required**: Either renumber the labels consecutively (SV0–SV12 with the synthesis taking the last slot), or add a note at the head of the Properties Introduced table recording which labels were withdrawn during revision and why.

### Issue 2: Confused empty-endset and empty-query collapse
**ASN-0051, Asymmetric empty endsets paragraph (Bilateral Vitality section)**: "For any endset e with coverage(e) = ∅ and any address set A ⊆ dom(Σ.C): π(∅, d) = ∅, locate(∅, d) = ∅, and discover_s(∅) = ∅ — projection, location, and discovery degenerate by the empty-intersection rule."
**Problem**: The notation ∅ is used inconsistently in a single sentence. In `π(∅, d)` and `locate(∅, d)`, the ∅ argument denotes the empty *endset* (so coverage(e) = ∅). In `discover_s(∅)`, the ∅ argument denotes the empty *query set* — discover_s's signature takes an I-address set, not an endset. The substantive claim the narrative needs is "a link with empty endset is not discoverable through any query A," which is `a ∉ discover_s(A) for all A` when coverage(Σ.L(a).s) = ∅. The actual statement `discover_s(∅) = ∅` is the trivially-true claim that an empty query returns nothing — unrelated to empty endsets.
**Required**: Distinguish the two ∅ uses. For the empty-endset discoverability claim, state explicitly: "for a link a with coverage(Σ.L(a).s) = ∅, a ∉ discover_s(A) for any A, since coverage(Σ.L(a).s) ∩ A = ∅ ∩ A = ∅."

### Issue 3: Loose biconditional on locate–π relation
**ASN-0051, Endset Projection section**: "The two are related by M(d)'s function property (S2, ArrangementFunctionality): v ∈ locate(e, d) iff M(d)(v) ∈ π(e, d)."
**Problem**: The reverse direction requires v ∈ dom(M(d)) for M(d)(v) to be defined; without that the biconditional is ill-formed when v ∉ dom(M(d)). The forward direction supplies v ∈ dom(M(d)) from locate's defining set, but the reverse direction doesn't.
**Required**: Restrict the quantifier: "For all v ∈ dom(M(d)), v ∈ locate(e, d) iff M(d)(v) ∈ π(e, d)." Or note that v ranges over dom(M(d)) when reading the biconditional.

## OUT_OF_SCOPE

### Topic 1: Full projection including link-subspace contributions
**Why out of scope**: SV11 restricts to π_text (content-subspace projection) and the ASN explicitly defers the link-subspace contribution to a future "Link Subspace ASN." L13's reflexive-addressing case is similarly deferred. This is a deliberate scope decision, not a gap.

### Topic 2: Cross-origin exclusion for non-element-level span starts
**Why out of scope**: SV6 restricts to element-level span starts. L4 permits broader-level starts, but Nelson's design treats coverage growth at account/node/document levels as a feature, not a constraint. A formal claim about broader-level survivability would belong in a hierarchy-discipline ASN, not here.

### Topic 3: Formal characterization of same-origin coverage growth
**Why out of scope**: The ASN identifies sequential-overshoot and child-depth-entry mechanisms in prose and provides a concrete counterexample. The architectural framing ("byte level closed, broader levels open by design") is level-dependent — its formalization belongs in an allocation-discipline ASN that distinguishes text vs. document allocation regimes, not in survivability.

### Topic 4: Bilateral vitality preservation across forks
**Why out of scope**: J4 (ForkComposite) appears in the foundation extracts but the ASN does not address vitality preservation under forks. This is reasonable — fork-specific survivability properties build on this ASN's machinery and belong in a versioning ASN.

VERDICT: REVISE
