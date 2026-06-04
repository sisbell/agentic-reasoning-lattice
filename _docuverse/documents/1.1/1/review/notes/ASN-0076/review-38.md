# Review of ASN-0076

I checked the composite construction (E0), the preservation/distinctness/freedom claims (E1–E3), the supersession structure (E4–E7), and the persistence/frame claims (E8–E10), plus the worked example. The formal machinery is sound: K.λ preconditions are discharged step-by-step at each intermediate state, the ValidComposite★ couplings (J0/J1★/J1'★) are correctly shown vacuous, boundary cases (k=0 in E5, first-vs-subsequent emission in E0) are handled, and the worked example verifies every claim against concrete tumblers. I found no correctness gap.

The findings below are prose accretion of exactly the kind this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: E9 speculates about an unspecified "counter-claim" operation
**ASN-0076, E9 (Lineage Permanence), trailing prose**: "A user who later wishes to 'retract' the supersession cannot do so by mutating `ℓ_sup`. They can, however, allocate a *counter-claim* — a new link asserting that the supersession is not in force... The system accumulates the full history of claims and counter-claims, leaving the resolution policy to the reader."
**Problem**: E9's claim is permanence of `ℓ_sup` (a one-line corollary of L12/LP13). This paragraph does not advance that claim; it speculates about a future operation ("counter-claim") and system behavior the ASN does not define, and it directly pre-answers the Open Question "What does it mean abstractly for a supersession claim to be *retracted* or *contradicted*...". The same topic now lives in two places.
**Required**: Delete the counter-claim/resolution-policy speculation; the retraction question is already (and properly) deferred to Open Questions.

### Issue 2: E5 closes with essay comparison to an out-of-scope architecture
**ASN-0076, E5 (Divergent Successors), final two paragraphs**: "This stands in sharp contrast to an in-place edit model, in which 'the' successor is a singular state component and successive edits must be reconciled into a single result. Such reconciliation either forces consensus (centralizing the system) or discards information..."
**Problem**: This is motivational essay about an alternative (non-specified, non-existent) edit model. It establishes nothing about E5's claim, which is fully discharged by the preceding induction. Essay content in a claim slot.
**Required**: Cut to at most one sentence stating the operative fact ("the model imposes no exclusivity among supersession claims; resolution is reader-side policy"), which the construction already proves.

### Issue 3: E8's prose largely restates E1
**ASN-0076, E8 (Original Resolution Unaffected)**: the claim's body reduces ("The claim reduces to E1") and its trailing prose ("A reader who held a reference to `ℓ_old` before EDITLINK still holds a valid reference after; the link's endsets are still readable...") repeats E1's trailing prose ("The original link's I-address remains valid; its endsets are bit-for-bit identical...").
**Problem**: Two paragraphs in adjacent claims saying the same thing in different words. E8 *as a derived consequence* (resolution operations see no change) is worth keeping, but its restatement of E1's permanence narrative is redundant.
**Required**: Keep E8's claim; trim the trailing prose so it states only the resolution-specific consequence, without re-narrating E1.

## OUT_OF_SCOPE

### Topic 1: Conventions for recognizing/traversing supersession chains
The Open Questions correctly defer chain-cycle invariants, type-endset recognizability conventions, successor-span identification, and "current successor" computation. These are genuine future territory, not defects here.

VERDICT: REVISE
