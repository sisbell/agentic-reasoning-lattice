# Review of ASN-0047

I checked the elementary transitions, the K.δ case-split, the K.μ~ decomposition, the coupling calculus (J0/J1★/J1'★), the cross-layer derivations (P6/P7/P7a/GlobalLineage), and the four worked traces. The state model, transition frames, and invariant-preservation arguments are sound — the K.μ~ necessity/sufficiency equivalence, the K.μ⁻ constructive/post-state equivalence, FrontierEquivalence, and the Cross-document disjointness chain all hold up under step-by-step checking, and the worked examples discharge their stated postconditions correctly. The remaining issues are confined to the meta-prose accretion this note's `anti-bloat` classifier flags.

## REVISE

### Issue 1: "Single location / single source" organizational meta-prose
**ASN-0047, K.δ case (ii) and *Properties Introduced***: e.g. "discharged uniformly in §*K.δ case (ii) discharge and parent-allocator activation* — **the single location for the spawn/activation argument**"; and "The four structural identities ... are stated and derived inline at *Elementary transitions*, K.δ case (ii); **that catalogue is their single source**."
**Problem**: The cross-reference (where the argument lives) is useful; the appended commentary asserting that a section is "the single location" / "their single source" justifies document organization rather than advancing the claim. This is precisely the forward-reference accretion the note targets — prose a reader must skip to follow the argument. The phrase recurs (K.δ definition, the K.δ discharge section, and the worked examples all defer to the same "single location").
**Required**: Keep the section pointer; delete the "single location / single source" editorial framing. The pointer carries the navigation without the meta-commentary.

### Issue 2: Derivation-location justification appended to a label
**ASN-0047, *Decomposition of K.μ~* (K.μ~ range-invariance)**: "We label this conclusion **K.μ~ range-invariance**; **both premises sit in this section, so it is derived here and cited by reference elsewhere rather than re-derived**."
**Problem**: The substantive content ends at the label and the derivation. The trailing clause explains *why the derivation is placed here* — a defensive justification of document layout that does not advance the reasoning. Same shape appears in the Notation block ("both spellings appear in this ASN denotationally identically").
**Required**: Drop the "derived here ... rather than re-derived" justification; the label plus the in-section derivation suffice. Downstream citations of the label stand on their own.

## OUT_OF_SCOPE

### Topic 1: Interior link-withdrawal with renumbering (DELETEVSPAN-style compaction)
**Why out of scope**: The ASN's K.μ⁻ models link-subspace contraction by suffix removal only, faithful to a gap-free POOM for suffix deletions; interior withdrawal with compact-and-renumber is a distinct operation. The ASN already names this correctly in its Open Questions, and named operations (DELETEVSPAN) are explicitly out of scope. Not an error in this ASN.

### Topic 2: Type-only / one-sided links (`e₁ ∪ e₂` emptiness)
**Why out of scope**: Whether K.λ should exclude type-only links is genuine new territory the ASN flags as an open question; L3 only mandates a non-empty type slot, which is internally consistent. Resolving the semantics belongs in a future ASN.

VERDICT: REVISE
