# Review of ASN-0093

I worked through the structural argument (anchor construction, sub-allocator chains, the ChainMembershipForOrigin contiguous-prefix induction, the freshness lemmas, the simultaneous-induction discharge matrix, and the nine-step worked example) and found the mathematical content sound: the chains are well-grounded ASN-0040 sibling streams, cross-document and cross-subspace freshness are correctly routed through T10 and T7, and `origin`-preservation under `inc(·,0)` is properly derived from TA5-SigValid. The discharge section cites the FirstEmission admissibility result rather than re-deriving it, which is the right move. My only finding is an anti-bloat residue.

## REVISE

### Issue 1: Orthogonal redirect closes the cross-document section
**ASN-0093, "Cross-document disjointness chain", final sentence**: "Cross-subspace collisions between `dom(C)` and `dom(L)` are prevented by SD (StoreDisjointness, above)."
**Problem**: This section's lemma establishes cross-*document* (same-subspace) disjointness via T10, and the claim is already complete at the lemma's `∎`. The trailing sentence does not advance that argument — it redirects to SD for the orthogonal cross-*subspace* concern. This is the flagged "handled by Y elsewhere" pattern occupying a structural slot (the tail of a lemma section). A reader following the cross-document argument has to skip past a pointer to a different mechanism that the section is not about.
**Required**: Drop the sentence. SD is already stated as its own invariant with a full inline derivation, and the freshness lemmas already invoke it where the cross-subspace case actually arises; the cross-document section needs no reminder of it.

## OUT_OF_SCOPE

None. The deferred topics (arrangement mutation, entity stratification, provenance, coupling, withdrawal) are explicitly scoped out and correctly handled — M2 fixing `M(d) = ∅` and the absence of any arrangement-mutation transition is the right substrate-level commitment.

VERDICT: REVISE
