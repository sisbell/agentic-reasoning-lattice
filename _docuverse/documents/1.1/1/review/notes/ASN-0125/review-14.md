# Review of ASN-0125

The formal spine verifies. I checked EL0's wp argument (LP13 read as a weakest precondition), EL4's antichain reduction (PrefixSpanCoverage + R0a), the EL6(iv)/EL7(iv) two-level frame split (wp Case 2 with freshness + R0a discharging the third conjunct), EL-DM's induction, the EL11(a) projection biconditional (the "no content address extends a link address" step via L0/C1/SC-NEQ holds), the EL10 position-reuse construction, the EL13 cross-home commutation, and the EL14(c) standoff (`current = ∅`). The worked example is arithmetically consistent throughout. No correctness defects found, and the ASN stays in-territory — it specifies state-level operations and invariants abstractly, with implementation notes clearly marked as evidence.

The findings below are all meta-prose accretion, flagged under the `review-mode.anti-bloat` mandate.

## REVISE

### Issue 1: EL0 contribution-framing meta-prose
**ASN-0125, "The mutation postcondition is unachievable" (EL0)**: "What this note contributes is the reading of that invariant as a weakest precondition — the consequence for *editing* that LP13's persistence form leaves implicit."
**Problem**: The immediately preceding sentence already states the provenance ("it is L12 ... closed under →* — exactly LP13 ... — instantiated at `a`"). This sentence then editorializes about the note's contribution rather than advancing the proof; the reader skips it to reach the actual derivation ("Since `[J ⟹ ¬R_mut]` ..."). It is positioning prose, not reasoning.
**Required**: Delete the contribution-framing sentence. The wp reading *is* EL0's statement and needs no preface announcing its novelty.

### Issue 2: EL3 remark recapitulates content already in the intro and EL2/EL3
**ASN-0125, EL3 remark "The menu was shorter than it looked"**: "The genuinely distinct candidates were three: carry the claim in the **value space** ... **address space** ... or **relation space** ... The first two are already closed and need no re-derivation here: the value-space slot is fixed at the successor's birth (EL2(b)), the address-space nesting is an address the substrate never reaches (EL2(c)), and EL3 records the named RQs each violates."
**Problem**: The three-candidate framing already appears in "The problem" intro ("the genuinely distinct alternatives — a field in the successor's value, a nesting convention in the address space — are each eliminated by requirements we derive"). The "first two are already closed" sentence recaps EL2(b)/EL2(c) and the EL3 body while explicitly announcing it is "no re-derivation." The only load-bearing new content in this remark is its first sentence (the L8/TypedRelation collapse of "separate supersession link" ≡ "typed relation") and the Nelson grounding for refusing the structural reading even where nesting is available.
**Required**: Trim the remark to that new content; drop the three-candidate re-listing and the EL2/EL3 recap.

### Issue 3: The "supersession deactivates nothing" gloss is stated three times
**ASN-0125, EL6(iv) / EL7(iv) / EL9**: the same design moral recurs — EL6(iv): "Asserting supersession deactivates nothing. The original remains exactly as listed, exactly as active, exactly as readable as before; if its author also wants it retired ... that is a separate `Nullify(y)` — composable, never implied." EL7(iv): "In every case the edit *adds*; it touches nothing of the original." EL9: "superseding moves none of them ... The composite 'supersede and retire' is available; it is never implied."
**Problem**: The formal frame conclusions genuinely differ per operation (and are correct), but the design gloss — "the operation deactivates nothing; retirement is a separate, never-implied act" — is restated in different words across all three claims. This is the "two paragraphs say the same thing" pattern.
**Required**: State the moral once at its synthesis point (EL9, ThreeAxes) and let EL6(iv) and EL7(iv) carry only their formal frame conclusions (`nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)`, the conditional full-frame, etc.) without the repeated gloss.

## OUT_OF_SCOPE

None. The eight Open Questions (non-asserter retraction authority, supersession/retraction independence under arbitrary disciplines, meta-claims and currency stratification, non-empty-currency disciplines, temporal witnesses, span-level endset correspondence, edit/listing coupling, subtype-family observation closure) are all genuine future territory, correctly deferred rather than half-specified here.

VERDICT: REVISE
