# Review of ASN-0047

I checked the transition model's proofs against its invariants, focusing on the K.μ~ decomposition, the entity-allocation discharge, the per-subspace D-* derivations, and the foundation-inheritance bookkeeping. The mathematics is largely sound and heavily worked. The findings below are a notation reinvention, an internal table/body inconsistency, and several instances of the meta-prose the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: "tracked" reinvents the foundation term "activated"
**ASN-0047, Notation (Entity-level allocator)**: "Throughout this ASN *tracked* abbreviates ASN-0034's *activated* (AllocatedSet)... its *tracked domain* is the realized domain `domₛ(A)`... *Tracked-domain monotonicity* is ASN-0034's `domₛ(A) ⊆ dom_{s'}(A)`."

**Problem**: AllocatedSet (ASN-0034, foundation) already names this concept "activated," with "realized domain `domₛ(A)`" and the monotonicity `domₛ(A) ⊆ dom_{s'}(A)`. Introducing the synonyms *tracked*, *tracked domain*, *tracked-domain monotonicity* and then carrying them through FrontierEquivalence, TrackedEmission, ParentAllocatorDispatch, and the verification matrix is reinvented notation for a foundation primitive (Standard 7). It forces the reader to hold a private glossary mapping back to the foundation.

**Required**: Use the foundation term *activated* (and `domₛ(A)`) directly, or drop the rename and cite AllocatedSet at each use. If a one-word handle is genuinely needed, state it once and do not coin a new "…-monotonicity" label that duplicates the foundation's.

### Issue 2: SubAllocatorBundle table claims a five-sub-clause structure the body does not present
**ASN-0047, *Properties Introduced* → *Inherited from foundation*, SubAllocatorBundle row**: "...with the five sub-clauses (Subspace, FirstEmission, Namespace, T10aConformance, Disjointness) each proved from a named ASN-0093 lemma."

**Problem**: The body definition of SubAllocatorBundle (*Allocator hierarchy under documents*) does not present five named sub-clauses. It lists the standing chain properties as foundation facts in three running groupings and then states that "the one obligation the bundle must discharge beyond these foundation facts is the cross-subspace disjointness delta." The labels "Subspace / FirstEmission / Namespace / T10aConformance / Disjointness" appear nowhere in the prose. A reader directed by the table to a five-part proof finds a different structure.

**Required**: Reconcile the two. Either restructure the body to present the five named sub-clauses the table advertises, or correct the table row to describe the actual body structure (foundation-fact bundle + the cross-subspace disjointness delta).

### Issue 3: Document-routing meta-prose around the K.μ~ full-clearance steps
**ASN-0047, *Decomposition of K.μ~*, Full-clearance form**: "Steps (A)–(B) below establish this... and later appeals name these steps directly rather than re-deferring."

**Problem**: The trailing clause "and later appeals name these steps directly rather than re-deferring" describes how the document cross-references itself, not what the operation does. It advances no reasoning about K.μ~; it is bookkeeping about prior review cycles' deferral patterns. This is exactly the forward-reference accretion the anti-bloat classifier flags.

**Required**: Delete the self-referential clause. The Steps (A)/(B) labels are sufficient for later citation without narrating the citation policy.

### Issue 4: ParentAllocatorDispatch opens with an authority/use-site inventory
**ASN-0047, *Allocator hierarchy under documents*, ParentAllocatorDispatch (sub-lemma)**: "This sub-lemma is the authoritative site for owning-allocator identification and for the spawnPt-membership premise that identification supplies; the K.δ precondition box and the *K.δ case (ii) discharge* cite it rather than re-deriving the identification."

**Problem**: This sentence enumerates downstream consumers and asserts the lemma's "authoritative site" status rather than advancing the lemma's content. Per the accretion patterns, a definition's introduction that inventories its citing sites is noise the reader must skip past to reach the actual claim (the level-based allocator identification that follows).

**Required**: Remove the "authoritative site / cited by X and Y rather than re-deriving" framing. State the lemma's claim directly; the downstream sites already cite it where they need it.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
The ASN's K.μ⁻ contracts the link subspace by suffix removal only; interior withdrawal of an arranged link (the implementation's compact-and-renumber `DELETEVSPAN`) is correctly deferred. This is already named in the Open Questions and belongs to a future contraction-operation ASN, not this one. Link permanence itself is discharged on `dom(L)` by L12 independently of the arrangement, so the abstract guarantees here are complete.

### Topic 2: Concurrent allocation and serialization under a shared home document
The Open Questions raise whether concurrent link/content allocation must be serialized. Under SequentialTransitionAxiom this ASN models only totally-ordered atomic transitions, so concurrency is genuinely new territory rather than a gap in the present model.

META: not applicable — the ASN defines state, transitions on state, and invariants at the appropriate abstract level; it has not drifted into implementation mechanics.

VERDICT: REVISE
