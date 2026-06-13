# Review of ASN-0125

I checked the formal spine and it holds: EL0's `wp(S, R_mut) = false` reading of L12/LP13; the EL2/EL3 carrier-necessity derivation (exhaustive over the entity/store-writers `K.α, K.δ, K.λ, K.ρ`, with the `K.μ` family excluded as V→I bindings); the EL6/EL7 contracts (including the wp Case 2 active-at-birth argument, which correctly leans on R0a *at `Σ'`* to escape pre-existing unit-depth retraction coverage); EL-DM's induction; and the EL9–EL16 axes/discovery/currency results. The worked example traces correctly against the `a_emit` chain arithmetic, including the `current(ℓ₀) = ∅` standoff and the `[s_L,2]` position re-binding. The findings below are residual meta-prose of the kind the anti-bloat classifier flags — not correctness.

## REVISE

### Issue 1: Df-LAY pre-states the Remark's no-enforcement thesis behind a forward pointer
**ASN-0125, Df-LAY (EditingLayer)**: "A bare `Emit_{K_sup}`, a bare `Emit_R`, or a bare `K.λ` carrying either class is *not* an editing-layer operation — the substrate cannot enforce this (see EL1 and the Remark on no enforceable coupling below), but the layer does not issue them."
**Problem**: The clause "the substrate cannot enforce this (see … the Remark … below)" states, with a forward pointer, precisely the thesis the later "Remark (no enforceable coupling)" develops in full ("the substrate therefore *cannot* compel an editor to declare, and the completeness of the supersession record is a protocol property of the editing layer, not a substrate invariant"). The definitional content Df-LAY needs — that bare class-carrying operations are excluded and the layer does not issue them — is self-contained; the *why-it-cannot-be-enforced* is the Remark's subject and is duplicated here. This is the named accretion pattern exactly: rationale-bearing meta-prose around a forward reference, the same point asserted in two sections.
**Required**: Keep only the definitional fact in Df-LAY (bare class-carrying operations are not editing-layer operations; the layer does not issue them); drop the "(the substrate cannot enforce this, see … below)" rationale-and-pointer and let the Remark own the no-enforcement argument.

### Issue 2: EL8(e) is interpretive coda occupying a claim slot
**ASN-0125, EL8 (ClaimStanding), item (e)**: "it is a claim, not a verdict: the substrate records who said what and adjudicates nothing. Recognition of *standing* is structural; recognition of *truth* is the reader's."
**Problem**: Items (a)–(d) are properties grounded in cited results (permanence by EL5a; attribution by T4b/T6; openness by the schema; addressability by L4c). Item (e) grounds nothing — it is a design aphorism enumerated as a peer of the formal items. Essay content in a structural slot.
**Required**: Drop (e), or move the standing-vs-truth framing into surrounding prose if it is wanted as scope-setting, rather than carrying it as a sub-claim of EL8.

## OUT_OF_SCOPE

The eight Open Questions (non-asserter retraction authority, activity/replacement independence under arbitrary disciplines, meta-claim currency stratification, non-empty-currency discipline, temporal witnesses, span-level endset correspondence, edit↔listing coupling, subtype-family observation closure) are correctly deferred — each is new territory, not a gap in this note. In particular, editing a claim is admitted (EL8d) without the note owing meta-claim well-foundedness: `reach_o` always terminates within finite `dom(Σ.L)`, so `current` stays computable regardless, and the semantic stratification question is properly OQ3.

VERDICT: REVISE
