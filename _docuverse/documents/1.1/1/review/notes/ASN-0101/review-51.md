# Review of ASN-0101

This ASN is mathematically mature: D0's effect, D1's gap-closure bijection, D8's three-group invariant discharge, and the D9/D11 projection-and-wp calculus are each carried through with explicit case analysis and boundary coverage (empty post-state, deletion at start/end, singleton, non-singleton interior). I found no rigor gap in the core proofs. The findings below are residual meta-prose accretion of the kind the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Redundant reassurance paragraph in D8's S8★ discharge
**ASN-0101, D8 Group (i) justification**: "The (a)-and-(b) obligation is *existential*: it requires the existence of some finite decomposition... Either way, the post-state's full S8★ obligation — (a) and (b) on the affected subspace, and (c) on the content subspace — is met."
**Problem**: The immediately preceding paragraph already discharges S8★ completely: singleton decomposition for (a)/(b), M12 (CanonicalUniqueness) for (c). This follow-on paragraph adds no proof step. It re-imagines the "merge indeterminacy" concern that the chosen singleton decomposition already sidesteps, then re-states that (a)/(b) hold "regardless of which I-adjacencies hold" and that (c) is "equally independent of the indeterminacy" — reassurance about a case the discharge already excluded. It also re-invokes M11/M12 a second time ("ASN-0058's M11... supplies that maximally merged decomposition and M12... certifies it is the only one"). A reader following the proof must skip this paragraph to reach the next claim.
**Required**: Delete the paragraph. If the link to the earlier "no reconciliation across the gap" remark is worth preserving, fold it into a single clause in the preceding paragraph rather than a standalone recap.

### Issue 2: Cross-document example closes with a duplicate of D5's motivation
**ASN-0101, cross-document transclusion example, final paragraph**: "The example concretely demonstrates the architectural commitment that transclusion is safe under deletion. The author of `d` deletes a paragraph that `d'` had transcluded... No invariant on `d'` is touched by the DELETE on `d` — exactly the autonomy guarantee that D5 was designed to provide."
**Problem**: This restates, in different words, the motivation already given at length in the D5 section ("This is the property that distinguishes Xanadu transclusion from copy-and-paste... deletion from one document's arrangement is structurally independent of the other only because of D5"). Two paragraphs in different sections deliver the same point; the example's own verification bullets (D2/D5/D9 cross-checks) already carry the demonstrative work.
**Required**: Trim to the verification result; drop the re-motivation, or cut it to one sentence that points back to D5 rather than re-arguing the autonomy guarantee.

### Issue 3: Notation-choice justification in the operation parameters
**ASN-0101, "The operation," Notational convention**: "...we write `ℓ_σ` for the span width of `σ` and reserve `ℓ` for link addresses (members of `dom(L)`); the subscript prevents confusion with the link-address variable `ℓ`."
**Problem**: The trailing clause "the subscript prevents confusion with the link-address variable `ℓ`" justifies *why* the notation was chosen rather than stating what it denotes — meta-prose in a structural slot.
**Required**: Drop the justifying clause; "we write `ℓ_σ` for span width and `ℓ` for link addresses" suffices.

## OUT_OF_SCOPE

None. The Open Questions section correctly defers recoverability mechanics, INSERT-after-DELETE recovery, and causal ordering to future work rather than smuggling them in as claims, and the implementation-boundary section is appropriately scoped as non-normative.

VERDICT: REVISE
