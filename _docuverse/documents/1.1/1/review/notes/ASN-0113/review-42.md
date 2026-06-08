# Review of ASN-0113

The mathematics is sound. I checked the load-bearing derivations — W3 (T12 well-formedness of `ext(d,S)`), W4 (T5 prefix-confinement giving exact coverage, including the genuinely non-vacuous depth-3 instance), W10/W11 (first-component confinement and disjointness), W19 (the wp partition by emptiness bits, correctly conjoining `d ∈ dom(M)` so a failed precondition is not conflated with `⟨⟩`), and W20 (the careful arranged-vs-homed distinction via CL-OWN/CL-UNIQ). All hold. The worked instances earn their place: the depth-3 case in particular exercises the off-prefix, admissible-last-component tumbler `[S,2,1]` that the last-component bound alone would not exclude — exactly the case the `m_S = 2` instances leave vacuous.

The findings below are the meta-prose patterns the `review-mode.anti-bloat` classifier asks for.

## REVISE

### Issue 1: W17 closes by imagining an invariant-excluded failure
**ASN-0113, "Invariants across the members" (W17)**: "The reader who later asks for the region the member bounds finds neither more nor fewer items than the extent claims; what must never happen is a mismatch where the extent designates a region but the region's population differs from it."
**Problem**: W17 *is* the one-step-beyond-W4 consequence of S3★ — every V-slice position within `ext(d,S)` carries content. The trailing "what must never happen is a mismatch..." restates the claim as a danger that S3★ already excludes. This is the reviser-drift pattern: prose imagining a case the carrier invariant forbids, added after the actual content.
**Required**: End W17 at the S3★ statement. Drop the "what must never happen" sentence.

### Issue 2: W7 states "one per kind" three times
**ASN-0113, "The operation: one span per occupied subspace" (W7)**: "one per kind, *never one per contiguous fragment and never one per individual item*" … "The report is at the granularity of *kind*, not of position" … "a thousand characters and three links yields two members, not a thousand-and-three."
**Problem**: Three successive restatements of a single fact (`|result| = |occupied(d)|`). The concrete "thousand characters / three links" example is worth keeping; the abstract "never per fragment, never per item" and "granularity of kind not position" are the same statement twice over, around the example.
**Required**: Keep the concrete example and the Nelson/Gregory citations; cut one of the two abstract restatements.

### Issue 3: Opening paragraph is rhetorical framing, not reasoning
**ASN-0113, intro paragraph 1**: "We are trying to understand a question that looks like the bounding query of its sibling but is not: *given only your name, how much of each kind of thing do you hold?* … and the difference between one span and several is the whole subject of this note."
**Problem**: Essay-style scene-setting that advances no claim. The substantive setup (Nelson's "span-set indicating both the number of characters of text and the number of links," two distinct subspaces) is fully carried by paragraph 2.
**Required**: Compress to the operational framing in paragraph 2; the contrast with the single-span sibling is already made precisely in W0 and the Open Questions.

## OUT_OF_SCOPE

### Topic 1: Behavior under relaxed D-CTG★ (fragmented subspaces)
**Why out of scope**: The first Open Question correctly defers this. W4's single-span exactness rests on D-CTG★ contiguity at every reachable state; a foundation extension that relaxed it would require fragmented-span reporting semantics that belong in that future work, not here.

### Topic 2: Permanence of reported extent across version fork and under transclusion
**Why out of scope**: Raised as Open Questions; these concern cross-version/cross-document content sharing, new territory beyond a pure single-document query.

VERDICT: REVISE
