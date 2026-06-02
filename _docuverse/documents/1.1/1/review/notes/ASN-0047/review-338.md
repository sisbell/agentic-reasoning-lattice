# Review of ASN-0047

I checked the state model, the seven elementary transitions, the named composites (K.μ~, J4 fork), the coupling constraints, the per-state/composite-boundary invariant split, and the seven worked examples. The mathematics is sound: I found no failed preservation argument, no missing boundary case (empty document, full clearance, first insertion, orphan link, duplicate-I-address source, and interior replacement are all handled), no cross-ASN reference violation (ASN-0034/0036/0043/0045/0093 are all listed foundations), and no implementation drift (transitions are abstract; Gregory/Nelson appear as motivation, consistent with the foundation style). The findings below are the anti-bloat / forward-reference items the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: K.μ⁻ precondition forward-references the same lemma twice for the same equivalence
**ASN-0047, K.μ⁻ definition (constructive precondition)**: "...the strict-subset ⟺ strict-contraction correspondence is proved in *K.μ⁻ admissible contraction shape* below." and, two paragraphs later, "...this equivalence is proved in *K.μ⁻ admissible contraction shape* below."
**Problem**: Two forward pointers in one definition box deferring to the same lemma for facets of one equivalence (strict-subset ⟺ strict-contraction; constructive ⟺ post-state). This matches the flagged pattern "multiple paragraphs defer to the same downstream location" — the reader hits the pointer, skips, hits it again. The strict-subset/strict-contraction correspondence and the constructive/post-state equivalence are the *same* lemma's two directions.
**Required**: Consolidate into a single deferral ("the equivalence of the constructive precondition with the post-state characterization — including the strict-subset ⟺ strict-contraction match — is proved in *K.μ⁻ admissible contraction shape* below"), removing the second pointer.

### Issue 2: J4's φ-copy-vs-range-equality point is argued twice within the J4 section
**ASN-0047, J4 step (ii)**: step (ii) states the φ characterization with "**Order preservation**... **Multiplicity preservation**... Range equality is now a *derived consequence*, not the characterization"; a later paragraph in the same step re-argues it: "The position- and multiplicity-preserving copy — not mere range equality — is what 'copies the contents' demands..."
**Problem**: The same claim (φ-bijection is the characterization; range equality is merely derived) is stated in two paragraphs of one section in different words — the flagged "two paragraphs in the same document say the same thing." The dedicated worked example *Fork of a duplicate-I-address source* is the legitimate concrete test of the distinction and should stay; the in-section second statement is the redundant one.
**Required**: State the φ-vs-range principle once in step (ii) and let the duplicate-source worked example carry the demonstration; drop the second restatement.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link contraction
Already correctly deferred in the open questions (K.μ⁻ models suffix-only link removal, not the implementation's compact-and-renumber `DELETEVSPAN`). Not an error in this ASN.

### Topic 2: Link provenance and transitive-transclusion provenance
The absence of provenance for links (J-LV) and for transclusion chains is intentional and flagged in the open questions; belongs to a future ASN.

VERDICT: REVISE
