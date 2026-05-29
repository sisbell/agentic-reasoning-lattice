# Review of ASN-0040

## REVISE

### Issue 1: s.B-frame dispatch carries forward-looking proof-method prose
**ASN-0040, B0a**: "This partition fixes the shape of every inductive step over reachable states. We call it the *s.B-frame dispatch*: ... any predicate on s.B carried by the inductive hypothesis transfers to the successor unchanged, leaving only the baptismal case to argue."
**Problem**: This is use-site rationale, not content of the partition. It explains how B0a will be consumed by downstream inductions rather than what B0a asserts — exactly the `review-mode.anti-bloat` pattern of "prose around an axiom explaining why it is needed." Worse, the explanation is then re-stated verbatim in every consumer: B1, B10, and B_fin each open their step with "By the s.B-frame dispatch (§B0a) the frame case carries [X] to s' unchanged." The generic method-description thus appears four times.
**Required**: Keep the *name* (the shorthand earns its place across four proofs) but cut the explanatory sentence "any predicate on s.B carried by the inductive hypothesis transfers... leaving only the baptismal case to argue" — the proofs already say this where it is load-bearing.

### Issue 2: B8 silently weakens the foundation's global uniqueness without motivating the restriction
**ASN-0040, B8**: "two acts are co-reachable iff both lie on a single transition path s_init →* s for some reachable state s."
**Problem**: The foundation (GlobalUniqueness, ASN-0034) establishes *unconditional* address distinctness across all allocation events. B8 delivers only single-path distinctness, and the proof genuinely needs it ("Along that one path the edges are linearly ordered, so β₁ and β₂ are comparable" — Case 1 collapses for non-co-reachable acts). A precise reader arriving from the foundation's strong claim will ask why this ASN retreats to co-reachable, and the text gives no answer. The gap is not the missing proof (branching/replication is properly out of scope) — it is the absent one-sentence acknowledgment that co-reachability coincides with global uniqueness only under a linear history, with the divergent-state case deferred.
**Required**: Add a sentence after the B8 definition stating why the restriction suffices here (single-history reachability) and pointing to the existing cross-replica open question for the general (branching) case.

### Issue 3: forward reference to B₀ conf. in the registry definition
**ASN-0040, s.B (BaptismalRegistry)**: "subject to the conformance requirement stated at B₀ conf. below."
**Problem**: A forward pointer "below" to a property defined several sections later, the kind of accretion the review mode flags at source. The s.B definition does not need the conformance requirement to be understood; the dependency is consumed only in the B1/B10/B_fin base cases, which cite B₀ conf. directly.
**Required**: Drop the forward clause from the s.B definition. State seed conformance once, at B₀ conf., where the base-case proofs cite it.

## OUT_OF_SCOPE

### Topic 1: content-storage precondition in B3
**ASN-0040, B3**: "Content presupposes baptism: any content-storage layer built atop this model may store content at an address only after that address is baptized."
**Why out of scope**: The ghost-element framing itself (a baptized position holding nothing) is squarely a baptism concept and belongs here. But the final clause imposes an ordering constraint on a *content-storage layer*, which the scope list defers ("content storage and retrieval"). Recast it as a downstream obligation for that future ASN rather than a claim asserted here, or drop it.

VERDICT: REVISE
