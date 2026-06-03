# Review of ASN-0070

This is a careful note and the central mathematics — the inverse-image relation F0, the canonical-form uniqueness theorem F-canonical, and the contiguity argument F-contig — holds up under scrutiny. Step 1's exhaustiveness on `actionPoint(ℓ)`, the consecutivity Characterisation (both directions), Step 2a's existence construction, and the left/right-closure gap arguments are all genuinely worked, not hand-waved. The findings below are confined to the meta-prose accretion the anti-bloat classifier targets, plus one Depends-slot issue.

## REVISE

### Issue 1: Intra-lemma duplication in F-det
**ASN-0070, F-det (DenotationalDeterminism)**: The postcondition states "The representations `Σ_V` and `Σ_V'` may differ; after canonical-form derivation, they coincide." The derivation's closing sentence then restates: "The representations `Σ_V` and `Σ_V'` may differ at the representational level ... but their V-restricted denotations coincide."
**Problem**: Two sentences in the same lemma say the same thing. The closing line advances no reasoning past the postcondition it echoes.
**Required**: Drop the closing restatement; the five numbered steps already establish uniqueness.

### Issue 2: The "denotation determined, representation not" point is repeated across the note
**ASN-0070, Canonical Form section and F-det**: The same observation appears at least three times: the udanax note ("The denotation is determined; the representation is not."), the closing paragraph of Canonical Form ("We do not commit the operation's postcondition to canonical form ... An implementation may return any representationally equivalent form."), and inside F-det.
**Problem**: One load-bearing statement of the denotation/representation split suffices. Repeating it in three sections is prose the reader must recognize as redundant.
**Required**: State it once (the Canonical Form closing paragraph is the natural home) and remove the echoes.

### Issue 3: F-canonical Step 2 establishes uniqueness twice
**ASN-0070, F-canonical, Step 2**: The "Unique reconstruction" paragraph already proves that two Step-1-restricted normalised span-sets with the same `⟦·⟧_V` have identical component pairs `(s_j, c_j)` — i.e., uniqueness. The subsequent "S9 application" paragraph then re-derives the same uniqueness through the bridge plus S9.
**Problem**: Two consecutive paragraphs reach the same conclusion by different routes. The direct reconstruction argument is self-sufficient; the S9 invocation adds no force.
**Required**: Keep one. Either close on "Unique reconstruction" or, if S9 is the intended authority, fold the reconstruction argument into the bridge and drop the standalone paragraph.

### Issue 4: P-alloc carries a use-site inventory
**ASN-0070, A Worked Example, "Setup premise (P-alloc)"**: "Configurations 1, 4, and 5 below all rest on P-alloc; the per-block intersection steps reference it rather than re-stating it."
**Problem**: This enumerates which downstream configurations consume the premise — the "definition's introduction enumerates downstream consumers" pattern. The premise's content stands on its own; the inventory is bookkeeping prose.
**Required**: Delete the sentence. The configurations cite P-alloc at their use sites already.

### Issue 5: F-multi Depends lists non-load-bearing entries to justify hypothesis reachability
**ASN-0070, F-multi (MultiplicityPreservation), Depends**: Lists "K.μ⁺ (ArrangementExtension) — its lack of content-side injectivity makes the shared-I-address hypothesis reachable; S5 (UnrestrictedSharing) — supplies the abstract-cardinality witness."
**Problem**: The implication derivation (hypothesis → conclusion) uses only F0, F1, F-subspace, and S3★-aux. K.μ⁺ and S5 appear nowhere in that chain; they support only the separate "Structural admissibility" remark about whether the hypothesis is vacuous. Putting reachability-justification into the Depends slot of a derivation that does not depend on it is exactly the forward-reference accretion the classifier flags.
**Required**: Move K.μ⁺/S5 out of Depends into the "Structural admissibility" remark (where they belong), or excise the remark and the two entries together — the lemma's value is the implication, which the worked example (Config 2) already witnesses concretely.

## OUT_OF_SCOPE

### Topic 1: Multi-home resolution, concurrency semantics, transclusion-lineage relationships
**Why out of scope**: The three Open Questions correctly defer these to future ASNs; they are new territory, not gaps in the present query specification.

VERDICT: REVISE
