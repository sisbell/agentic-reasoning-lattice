# Review of ASN-0125

The architecture is sound and the core proofs hold under scrutiny. I checked EL0 (the wp reading of LP13), the EL6(iv)/EL7(iv) nullification-frame arguments (the R0a "fresh address escapes pre-existing unit-depth retraction coverage" step), the EL11(a) coverage trace ("no content address extends a link address"), the EL13 commutation (a_emit dependence on the per-home subset), and the entire worked example (chain addresses, `current` cardinalities 1/≥2/0) — all check out. EL-DM correctly closes the "at disciplined Σ" conditionals into a reachable, non-vacuous domain. The findings below are refinements, the first two of which the anti-bloat classifier specifically solicits.

## REVISE

### Issue 1: EL-DM's statement carries a use-site inventory and a non-circularity aside

**ASN-0125, EL-DM (statement)**: "Every editing-layer-reachable state is edit-disciplined — so the conditional claims that follow (EL6(iii), EL7(iii), the EL7(iv) full frame, EL14's active-at-birth, and EL8's disciplined-state hypothesis) are evaluated over a reachable, non-vacuous domain, not an assumed one. (EL11's contextual half rests instead on per-claim schema-conformance, which EL4 supplies without a whole-state hypothesis; at editing-layer-reachable states every claim conforms regardless, so it applies there too.)"

**Problem**: The theorem is the first clause; the Base/Step below is why it holds. Everything between is accretion of two flagged kinds. The em-dash clause is a use-site inventory — five downstream consumers enumerated — that does not advance EL-DM's meaning; the parenthetical is a non-circularity justification (EL11 depends on EL4, not EL-DM), which is precisely the "the forward pointer is non-circular by Y argument" pattern. The inventory is also loose: "EL14's active-at-birth" attributes to EL14 a property that is actually EL6(iii)'s conclusion (EL14(a) merely consumes it).

**Required**: Reduce the statement to the theorem. If motivation is wanted, a single clause ("so the 'at disciplined Σ' conditionals below are non-vacuous") suffices. Drop the five-item consumer list. If the EL11/EL4 scoping must be stated to forestall a circularity worry (EL-DM → EL7 → EL11), state it once, at EL11, not inside EL-DM's statement.

### Issue 2: "disciplined claim" is an undefined term in EL11

**ASN-0125, EL11(a)**: "For a disciplined claim `e` and any document `d`, the to-side of `e` projects into `d` iff `d` currently lists the original" (and the implied symmetric from-side statement).

**Problem**: "disciplined" is defined by Df-DISC for *states* and *layers*, never for individual claims, and it collides with "edit-disciplined." The property EL11(a)'s proof actually uses is schema-conformance of `e` alone — it invokes EL4, stated "for any *schema-conforming* claim," and the per-state invariants (S3★, R0a, C1, L0, L1b) hold at every reachable state without any whole-state discipline hypothesis. EL-DM itself confirms this: it says EL11's contextual half "rests instead on per-claim schema-conformance." So the statement names a property (whole-state discipline of `e`?) that is both undefined and stronger than what the proof needs.

**Required**: Replace "disciplined claim" with "schema-conforming claim" in EL11(a) and its symmetric from-side reading, matching the terminology EL4 and EL-DM already use.

### Issue 3 (minor): Df-LAY previews the Remark's conclusion

**ASN-0125, Df-LAY**: "...the substrate cannot forbid such emissions (discipline is a protocol property, not a substrate invariant; see the Remark on no enforceable coupling below) — but the layer does not issue them." **Remark (no enforceable coupling)**: "...the completeness of the supersession record is a protocol property of the editing layer, not a substrate invariant."

**Problem**: The "protocol property, not a substrate invariant" conclusion is asserted in Df-LAY (with a forward pointer) and then established at the Remark — the forward-pointer-plus-previewed-conclusion is the cross-section deferral the anti-bloat mode targets, and the conclusion phrase is duplicated near-verbatim.

**Required**: Let the Remark own the conclusion. Df-LAY can restrict the layer's operations and gesture minimally ("the substrate cannot enforce this; see EL1 / the Remark") without restating "protocol property, not a substrate invariant" inline.

## OUT_OF_SCOPE

No improperly included topics. The eight Open Questions correctly defer future territory (cross-asserter retraction authority, meta-claim stratification, span-level endset correspondence, edit↔listing coupling, prefix-rooted subtype observation closure) rather than claiming it, and the use of `Observe`/`project` to characterize claim discoverability (EL11) is intrinsic to the edit's observable semantics, not a re-specification of the out-of-scope FINDLINKS/RETRIEVEENDSETS operations.

VERDICT: REVISE
