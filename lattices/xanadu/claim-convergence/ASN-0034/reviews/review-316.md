# Cone Review — ASN-0034/D2 (cycle 3)

*2026-04-18 18:43*

### D2 Step 2 elides Divergence's symmetry in the ZPD identification
**Foundation**: ZPD's Relationship-to-Divergence postcondition at operand pair `(a, w)` gives `zpd(a, w) = divergence(a, w)`, so applied to pair `(b, a)` it yields `zpd(b, a) = divergence(b, a)`. Bridging `divergence(b, a)` to `divergence(a, b) = k` requires Divergence's symmetry postcondition `divergence(a, b) = divergence(b, a)`. D1 handles this explicitly: "Divergence's symmetry postcondition `divergence(a, b) = divergence(b, a)` bridges… yielding `zpd(b, a) = divergence(b, a) = divergence(a, b) = k`."
**ASN**: D2 Step 2 — "The ZPD–Divergence relationship (ZPD), applied to the pair (b, a) in case (i), gives `zpd(b, a) = divergence(a, b) = k`." Subsequent steps read off `actionPoint(b ⊖ a) = zpd(b, a) = k` from this identification.
**Issue**: The quoted line conflates two distinct facts: ZPD's identification of `zpd(b, a)` with `divergence(b, a)`, and Divergence's symmetry identifying `divergence(b, a)` with `divergence(a, b) = k`. The intermediate `divergence(b, a)` is never named. D2's Divergence Depends entry enumerates case-(ii) elimination, case-(i) shared-bound conjunction, and the agreement predicate `aᵢ = bᵢ`, but does not list symmetry as a consumed postcondition — unlike D1, whose Divergence Depends entry explicitly cites symmetry for exactly this operand-pair bridge. The same applies to the Pos/action-point derivation for `b ⊖ a`, which relies on this identification.
**What needs resolving**: Either rewrite D2's ZPD identification to route through `divergence(b, a)` explicitly (matching D1's chain) and add Divergence's symmetry postcondition to D2's Divergence Depends entry, or justify why symmetry is not consumed here.
