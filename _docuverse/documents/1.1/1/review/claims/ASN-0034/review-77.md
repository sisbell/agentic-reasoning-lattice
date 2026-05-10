# Cone Review — ASN-0034/TA3 (cycle 5)

*2026-04-16 09:07*

### TA3 directly invokes ZPD's exports but omits ZPD from Depends
**Foundation**: (internal — ZPD, referenced by TumblerSub but not shown)
**ASN**: TA3 (OrderPreservationUnderSubtractionWeak), Case B and its sub-cases
**Issue**: TA3's proof operates extensively on `zpd(a, w)` and `zpd(b, w)` as first-class objects — defining `dₐ = zpd(a, w)`, establishing `d_b = zpd(b, w)` is well-defined (via the biconditional "zpd defined iff not zero-padded-equal"), comparing zpd positions (`dₐ = d_b`, `dₐ < d_b`, `dₐ > d_b`), and reasoning about agreement at positions before the zpd. These are all properties of zpd that come from ZPD's definition, not from TumblerSub's contract. TumblerSub's Definition field uses zpd with a parenthetical "(ZPD)" citation but does not re-export zpd's fundamental properties (existence condition, first-position semantics, pre-zpd agreement). TumblerSub's postconditions export the operation's result membership, length, positivity, and action-point identity — none of which define what zpd *is*. The ASN's convention requires direct citation of every property whose exports a proof invokes: TA2 cites T0 directly even though T0 is reachable transitively through TumblerSub; T1 cites T3 directly even though T3 is a simple consequence of T0. By the same convention, TA3's direct use of zpd's definition and properties requires citing ZPD.

Specific uses: (1) the B1 bridge argument uses "not zero-padded-equal → zpd defined" (ZPD's existence biconditional); (2) the B1–B2 bridge proves `d_b` is well-defined via the same biconditional; (3) Sub-cases B2–B4 compare zpd positions, relying on zpd being the *first* position of zero-padded disagreement; (4) throughout Case B, pre-zpd agreement (`aᵢ = wᵢ` for `i < dₐ`) is invoked as a property of zpd, not derived from TumblerSub's three-phase formula.

**What needs resolving**: TA3's formal contract must include ZPD in its Depends field, with a role statement identifying the specific ZPD exports the proof invokes: the existence biconditional (zpd defined iff not zero-padded-equal), the first-position characterisation, and the pre-zpd agreement guarantee.
