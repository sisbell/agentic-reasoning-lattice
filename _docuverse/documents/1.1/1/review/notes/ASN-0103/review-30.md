# Review of ASN-0103

The allocation argument is sound: the length-restricted frontier `D_A = E ∩ S(A,2)` correctly excludes versions, freshness/distinctness close cleanly via S0 + B7, and the single-`K.δ` decomposition genuinely yields atomicity. The math holds. The findings below are the anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface — accreted meta-prose and duplication that the precise reader must work around.

## REVISE

### Issue 1: The invariant verification is stated twice, in full
**ASN-0103, "Invariants Maintained" + table entry CND.inv**: The prose section walks every invariant ("Vacuous for the empty arrangement…", "Frame-inherited — no content, link, or provenance change…", "Concerning `d` directly…"), and the CND.inv table cell then reproduces the *same* categorized walk verbatim ("the empty-arrangement family … vacuous for d via dom(M'(d))=∅; the content/link/provenance families … frame-inherited; P3 holds since only M gains…").
**Problem**: Two passages in the same document say the same thing. A table entry should summarize a claim, not re-run the section's argument. The reader verifies the same categorization twice.
**Required**: Collapse CND.inv to a one-line statement ("Σ' satisfies ExtendedReachableStateInvariants and P3; verified directly for {P0,P1,M0,S2,S3★,P6,P8,S7d,ActivatedEmission,T8}, vacuous on dom(M'(d))=∅ for the arrangement family, frame-inherited otherwise") and keep the prose section as the single site of the argument.

### Issue 2: Roadmap and editorial meta-prose that advances no reasoning
**ASN-0103, "Background" and "Discovering the Effects"**: "We shall see that every claim about the operation flows from this single asymmetry: **an address is allocated; no content is.**"; "Three effects must obtain together; the third is the largest, because it is a frame."; "This is the largest effect and the heart of the user's guarantee."
**Problem**: These are previews and editorial rankings of the argument, not steps in it. "The third effect is the largest" tells the reader nothing they need to verify the frame; it is essay framing in a structural slot.
**Required**: Delete the preview sentence and the "largest effect / heart of the guarantee" editorializing; state the frame clauses directly.

### Issue 3: Defensive justification of a proof strategy not taken
**ASN-0103, Effect One**: "We do not assert that `D_A` is a contiguous initial prefix of the stream — that would make `d` *the* next unallocated emission, a stronger claim than freshness, monotonicity, and uniqueness need."
**Problem**: This is prose explaining what the author *declined* to prove and why, rather than advancing the proof. The freshness argument (`d ∈ S(A,2) \ D_A ⊆ S(A,2) \ E`) stands on its own and does not reference contiguity; the disclaimer is meta-commentary on proof scope.
**Required**: Remove the sentence. The freshness derivation already does not invoke contiguity, so nothing depends on disclaiming it.

### Issue 4: Out-of-scope forking mechanics described at paragraph length
**ASN-0103, "What Distinguishes Creation From Forking"**: "Such a document begins as a complete inclusion of its source: its arrangement is *populated* at creation, mapping V-positions onto the *same* I-addresses the source references. That shared Istream origin is exactly what makes refractive link-following and version intercomparison possible…"
**Problem**: CREATENEWVERSION is out of scope. The contrast that *this* ASN needs is `ran(M'(d)) = ∅` (fresh document shares nothing), which is one clause. The surrounding paragraph specifies the forking operation's populated-arrangement mechanics and downstream capabilities — content owed to a future ASN, not this one.
**Required**: Reduce to the single contrastive clause ("a forked document begins with a populated arrangement; a created one with `ran(M'(d)) = ∅`") and drop the elaboration of forking's mechanics and consequences.

## OUT_OF_SCOPE

### Topic 1: Effective-owner / baptismal-registry coupling
The note correctly defers `ω_{Σ'}(d) = ω_Σ(A)` and O5 grounding to a future ASN (the registry `B` is absent from this state), recording it in the final Open Question. This deferral is appropriately scoped — not an error here.

META: (none — the ASN defines state effects and invariants of CREATENEWDOCUMENT abstractly; it has not drifted into implementation mechanics, it has accreted meta-prose.)

VERDICT: REVISE
