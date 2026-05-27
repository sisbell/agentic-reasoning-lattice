# Review of ASN-0099

This is a careful, dense specification of FINDLINKS. The two-phase factoring is clean; the conformance contracts (F2 ∧ F3 and variants) are well-articulated; the worked example is thorough; the A1a/A1b partition makes the interpretive commitments visible at the citation surface. The realizability discharge in F4 is rigorous, and the F9 family handles the survivability question carefully. I found no proofs by "similarly" or by checkmark, and the boundary cases (empty I, empty link store, empty constraint set, empty scope, empty V-region, K.δ-IsDocument sub-case) are all addressed.

That said, two issues warrant revision before the spec is built upon.

## REVISE

### Issue 1: F10's ordering property is not extended to filtered or scoped variants
**ASN-0099, "Result Ordering"**: F10 (OrderedResult) states that "the result set admits a unique presentation as a sequence ⟨a₁, a₂, ..., aₙ⟩ with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ)".

**Problem**: F10 is specifically tied to the unfiltered match predicate. The ASN explicitly extends determinism (F8 → F15, F16), survivability (F9 → F17, F18), and monotonicity (F19 → F19-filt, F19-sco) to the filtered and scoped forms, but does not extend F10. Pagination is named as the load-bearing reader-facing concern ("pagination demands that the order be stable across requests"); filtered queries from a UI are at least as common as unfiltered ones, and the spec's pattern of explicitly stating derivative claims for filtered/scoped variants makes the F10 omission a genuine asymmetry. An implementer reading F10 has no warrant from the spec that `findlinks_filtered(C, Σ)` or `findlinks_scoped(I, S, Σ)` admits a unique canonical ordering, even though the structural argument is identical.

**Required**: Add F10-filt and F10-sco stating that the filtered and scoped result sets respectively admit unique T1-sorted presentations. Each follows from the same structural argument (finite subset of dom(Σ.L) under T1's restriction is uniquely orderable), but explicit statement closes the asymmetry with F15–F19's treatment.

### Issue 2: State name `Σ''` is reused with different referents across queries in the worked example
**ASN-0099, Worked Example, Query 7 vs Query 11**: Query 7 introduces "the post-state Σ'' has `Σ''.M(d_a) = {v_a^1 ↦ α₃, v_a^2 ↦ α₁, v_a^3 ↦ α₂}`" (K.μ~ reordering from Σ). Query 11 reuses the same name: "yielding state `Σ''`" (K.μ⁻ then K.μ⁺_L from Σ via Σ').

**Problem**: The two Σ'' states are structurally different — Query 7's has all three content positions intact (just reordered), while Query 11's has two positions contracted out and a link-subspace position added. A reader cross-referencing claims that mention "Σ''" will conflate them. The worked example then verifies F15 against Σ'' citing Query 7's K.μ~ reasoning, but reasoning that would apply to Query 11's Σ'' would be different (different K.μ-family step composition). Symbol overloading in worked examples that are meant to anchor abstract claims is genuinely confusing.

**Required**: Rename one of the two Σ'' (e.g., Σ_perm for the reordering result and Σ_edit_link for the contraction+link-extension composite), or use a consistent indexing scheme across all queries (Σ_1, Σ_2, ... as Query 10 already does for its five-step chain).

## OUT_OF_SCOPE

The ASN's own "What We Have Not Specified" and "Open Questions" sections list the genuinely future-scope items: phantom addresses in the query I-set, multi-instance partition tolerance and consistency models, caching, access-control composition beyond scope filtering, the inverse direction (FOLLOWLINK/RETRIEVEENDSETS), the combined filtered-and-scoped operation, and timing bounds for K.λ→FINDLINKS commit visibility. These are appropriately deferred and not gaps in this ASN.

VERDICT: REVISE
