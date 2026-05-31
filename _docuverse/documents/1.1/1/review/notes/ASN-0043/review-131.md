# Review of ASN-0043

## REVISE

### Issue 1: L11a opens with a proof-obligation narration that the case analysis then re-establishes
**ASN-0043, L11a — LinkUniqueness**: "L1c (LinkAllocatorConformance) gives, for each `a ∈ dom(Σ.L)`, a T10a-conforming chain seeded at its document-level prefix... What L1c supplies, however, is only the *existence* of some conforming chain per link; GlobalUniqueness needs the stronger fact that `a₁` and `a₂` are genuine allocation events of the *one* tree 𝒯, respecting T10a's at-most-once-per-`(t, k')` child-spawning constraint."
**Problem**: This paragraph re-derives the S7d/DocVal fact that every `home(a)` is a node of 𝒯, then narrates *what GlobalUniqueness needs* before any work is done. The two cases that follow (distinct homes / shared home) each independently establish tree-membership via the at-most-once constraint — they do not consume this preamble, they reprove its content. The reader must skip the "what L1c supplies, however..." narration to reach the actual argument. This is the "explains why the stronger fact is needed" accretion pattern flagged for this note.
**Required**: Collapse the preamble to a single bridging sentence ("GlobalUniqueness requires both events to lie in the one tree 𝒯; the two cases establish this") and let the case analysis carry the derivation.

### Issue 2: The "Properties Introduced" summary table embeds derivation prose in index slots
**ASN-0043, Properties Introduced (table)**: e.g. L0b row — "T4-validity postcondition of L1c, derived there; with L0 + T7 yields the scoped disjointness `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` (the *L0a discharge*)"; L11a row — "single-system precondition discharged by embedding the L1c link chains in the one tree 𝒯"; L0 row — "together with L0a yields the scoped disjointness... via T7"; L6 row — "standard-triple consequence: `F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ)`".
**Problem**: A summary index should carry label + statement + status. These rows instead carry the proof mechanism ("via T7," "by embedding the L1c chains in 𝒯," "derived there; with L0 + T7 yields...") — essay content in a structural slot, duplicating arguments already fully stated in the body (L0b paragraph, L11a cases). This is exactly the kind of meta-prose that compounds across cycles in the table rather than the proof.
**Required**: Strip derivation clauses from the table rows, leaving the statement and a bare cross-reference (e.g., L0b → "every link address is T4-valid; see L1c"). Keep the mechanism in the body only.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace residence
The disjointness in L0b/L14 is scoped to the `s_C`-resident slice. Extending content-side disjointness to all of `dom(Σ.C)` requires a content-side invariant fixing a global content-subspace constant — this is correctly deferred to the first Open Question and belongs in a content-model revision, not here.

### Topic 2: Link↔arrangement consistency under transclusion
The interaction between `Σ.L` and transcluded I-addresses (Open Questions 2, 7, 8) concerns operation semantics and arrangement consistency, which are outside a static link-ontology note.

VERDICT: REVISE
