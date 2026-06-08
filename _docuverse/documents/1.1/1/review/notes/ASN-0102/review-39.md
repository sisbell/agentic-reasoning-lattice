# Review of ASN-0102

## REVISE

### Issue 1: X8 retains defensive prose litigating a previously-rejected argument

**ASN-0102, X8 (RunFragmentation)**: "Hence no within-reference pair is a merge candidate — directly, without the stronger (and false) claim of pairwise non-I-adjacency. (Were the stronger fact wanted, it would follow from V-contiguity of `dom(M(d_s)|⟦σ⟧)` within the subspace (D-SEQ): consecutive blocks are V-adjacent, so maximality forces them non-I-adjacent, while non-consecutive blocks are not V-adjacent at all. But the conclusion here needs only the conjunction.)"

**Problem**: This passage does not advance the proof — it argues about a claim the proof deliberately does *not* make. The correct argument is the single preceding sentence: `resolve` returns the maximally-merged decomposition (C1a/M12), which by definition contains no pair satisfying M7's conjunction of V- and I-adjacency, so no within-reference pair is a merge candidate. That suffices. The clause "without the stronger (and false) claim" and the entire parenthetical reconstruct a rejected alternative and then explain why it is not needed. This is exactly the reviser-drift pattern: a fix to the X8 merge argument left behind the corpse of the old argument rather than removing it. The precise reader must skip past it to follow the actual chain.

**Required**: Delete the "without the stronger (and false) claim" clause and the parenthetical. State only the conjunction argument that the conclusion uses. While editing, also remove the dangling forward signpost "The new content is the inter-reference boundary below." — let the next bullet speak for itself.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of already-copied content and continued discoverability
The first open question (origin/discoverability after a copied address is itself later displaced) is genuine future territory — it depends on operations and discoverability machinery beyond a single COPY's contract.

### Topic 2: Transitive containment when a reference-holder becomes a source
The second open question (containment-record obligations when a document that obtained content by reference is itself referenced) belongs to a later ASN coordinating COPY across documents, not to this operation's definition.

VERDICT: REVISE
