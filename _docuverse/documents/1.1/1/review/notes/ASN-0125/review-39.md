# Review of ASN-0125

I checked every EL claim and the worked example against the foundations. The substance is rigorous: EL0 (wp = false via LP13), EL1 (transition-instance identity), EL2(a–d), the EL3 derivation, EL-DM's induction, EL4 (PrefixSpanCoverage + R0a), EL6/EL7 contracts (including the disciplined-vs-unconditional `nullified` split and the wp Case 2 application), EL9–EL16, and the six-step worked example all hold up under scrutiny. The disciplined-hypothesis scoping on "active at birth" is correct (non-unit-depth retractions could otherwise catch a fresh address), boundary cases are covered (Σ₀ empty store, `current = ∅` standoff, position re-binding, fork), and foundation usage is clean with no reinvention. The findings below are prose-level.

## REVISE

### Issue 1: EL9 gloss upgrades status-preservation to status-assertion
**ASN-0125, EL9 (ThreeAxes)**: "An edit, as such, leaves the original resolvable, listed, and active."
**Problem**: The preceding sentence — "superseding moves none of them" — is the precise claim, and EL6(iv)/EL7(iv) support it: resolution is unconditional (EL9(1)), but listing (EL9(2), `Σ'.M = Σ.M`) and activity (EL9(3), `nullified` frame) are *preserved*, not *asserted*. An edit of an unlisted original (one never seated by K.μ⁺_L, or de-listed per the EL9(2) construction) leaves it unlisted; an edit of an already-nullified link leaves it inactive. So the literal reading "the original is left ... listed and active" is false in exactly the cases EL9(2)/EL9(3) and EL14(e) take pains to admit. The gloss is both less precise than and redundant with the sentence before it.
**Required**: Align the gloss with status-preservation, e.g., "leaves the original resolvable, and its listing and activity exactly as they were."

### Issue 2: Clause-level rhetorical accretion (anti-bloat)
**ASN-0125, EL8(b)**: "... not a function of Σ — an overlay the attribution guarantee neither needs nor invokes."
**ASN-0125, EL15(d)**: "... holding exactly when the chain was fully asserted and no hop demoted — and any specification that promised it unconditionally would be promising what no implementation of this substrate can keep."
**Problem**: Both trailing clauses restate the claim just made (EL8(b): "not a function of Σ"; EL15(d): "member-to-ends operative traversability is a derived property"/"(a)–(c) are the invariants ... warns against more"). They are defensive/rhetorical tails that do not advance the argument — the anti-bloat patterns this note is classified for. A precise reader skips them to reach the next claim.
**Required**: Delete the redundant clauses; the substantive content in each item survives intact in the surrounding sentences.

## OUT_OF_SCOPE

None. The Open Questions section correctly defers future territory (cross-asserter retraction authority, supersession of retractions, claims-targeting-claims meta-stratification, endset span-level correspondence) without making claims about it, and the layer's bare-K.λ for original-link creation is used only to prove discipline preservation (EL-DM), not to specify MAKELINK.

VERDICT: REVISE
