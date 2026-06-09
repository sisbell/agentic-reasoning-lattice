# Review of ASN-0116

## REVISE

### Issue 1: Post-state appeal to ExtendedReachableStateInvariants rests on a premise the precondition does not assert

**ASN-0116, "The document remains one coherent sequence" (S8★) and end of "INSERT as a valid composite":** "S8★ ... holds at the filled post-state directly by ExtendedReachableStateInvariants (ASN-0047), INSERT being a valid composite — it is a post-state invariant" and "the appeal to ExtendedReachableStateInvariants for its post-state is licensed."

**Problem**: ExtendedReachableStateInvariants (ASN-0047) yields the per-state invariants (including S8★) only for states *reachable from Σ₀ by valid composites*. Showing "INSERT is a valid composite" gives Σ' reachable **only if Σ is itself reachable from Σ₀**. The precondition does not assert this. It asserts the weaker "Σ is a composite boundary — ... so the composite-boundary properties ... hold at the pre-state." Asserting that the *consequences* (P4★, P4a, P7a) hold is not the same as asserting reachability: a state can satisfy those properties without lying on any valid trace, and for such a Σ the theorem does not transfer to Σ'. The note went to the trouble of proving D-SEQ/D-MIN/D-CTG and the content-store invariants for the post-state *directly* precisely because the relevant ASN-0082 lemmas do not transfer — yet S8★ is deferred to a theorem whose hypothesis (reachability of the pre-state) the precondition supplies only obliquely.

**Required**: Either (a) state the precondition as "Σ is reachable from Σ₀ by a valid transition trace" (from which the composite-boundary properties follow), so the post-state appeal to ExtendedReachableStateInvariants is licensed; or (b) discharge S8★ for INSERT's post-state directly (the inserted block is one run by P1, the shifted-suffix runs are carried by I-SHIFT, and S8 applies per-subspace), as is already done for contiguity.

### Issue 2: RAN's introduction is a use-site inventory of downstream consumers

**ASN-0116, after the Frame clauses:** "We derive once, from these clauses, the range identity that both the provenance discharge and the discoverability weakest precondition consume:" and, in the Effect preamble, "One arithmetic fact, consumed by the value clauses below, we record first — the block-disjointness fact".

**Problem**: This is forward-reference accretion of the kind this review mode is asked to surface — a definition/lemma introduced by enumerating its downstream consumers rather than by advancing its own content. RAN is true and self-contained; naming "the provenance discharge and the discoverability weakest precondition" as its consumers adds no reasoning, and the inventory rots as consumers move. The "consumed by the value clauses below" tag on the block-disjointness fact is the same pattern in miniature.

**Required**: State RAN and the block-disjointness fact on their own terms; drop the consumer enumerations.

### Issue 3: The freshness-vs-immutability caution is stated defensively twice

**ASN-0116, P4 and P5:** P4 — "We stress what does *not* underwrite this: it is *not* that A_new is fresh against dom(C). Foundation L4 ... and L9 ... let an endset reference *any* tumbler ... Coverage-invariance rests on endset immutability, not on freshness." P5 — "(This step turns on *arrangements*, not endsets: it is valid here precisely because ran(M(d')) ⊆ dom(C), whereas the analogous 'fresh ⇒ not in any endset' inference fails — endsets may name ghost addresses, L4/L9. ...)"

**Problem**: The underlying *substantive* point (an endset may already name an address INSERT mints into A_new, so freshness is not the ground) is worth one statement and is genuinely load-bearing for the new-block-witness/ghost cases. But it appears as a defensive justification in two places, the second largely re-explaining the first against a different misreading. The recurring "here is the wrong inference and why we don't use it" framing is the noise; the ghost-reference fact itself should be retained.

**Required**: Keep the ghost-reference fact once (it is needed for P4's new-block witnesses and P6's containment wp); reduce the P5 parenthetical to the actual proof step (`A_new ∩ ran(M(d')) = ∅` because `ran(M(d')) ⊆ dom(C)` by S3 and `A_new ∩ dom(C) = ∅` by P0) without re-litigating the rejected inference.

## OUT_OF_SCOPE

### Topic 1: Insertion at a transcluded/shared position; concurrent insertions; transclusion-sourced provenance; post-fragmentation contiguity
**Why out of scope**: These are the note's own Open Questions and concern transclusion (ASN-0118), concurrency/serialization, and later editing — new territory, not defects in INSERT's fresh-allocation specification.

VERDICT: REVISE
