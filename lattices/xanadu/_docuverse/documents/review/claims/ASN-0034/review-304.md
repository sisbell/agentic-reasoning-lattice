# Cone Review — ASN-0034/TA3 (cycle 5)

*2026-04-18 16:13*

### TA-Pos missing from TA3's Depends despite Pos/Zero predicate use at every TA6 invocation

**Foundation**: N/A — cross-cutting citation discipline: TA-Pos is the definitional source of the `Pos` and `Zero` predicate symbols throughout this ASN, as TA6's Depends entry establishes ("TA-Pos (PositiveTumbler) — Conjunct 2 uses both paired predicate symbols TA-Pos introduces: `Pos(t)` ... and `Zero(t)`").

**ASN**: TA3 Sub-case A1: "making `b ⊖ w` a positive tumbler; by TA6 the zero tumbler `a ⊖ w` is strictly less." Sub-case A3: "If `b ⊖ w` has any positive component, then `a ⊖ w` (all zeros) is strictly less by TA6." Sub-case B1: "The subtraction `a ⊖ w` is the zero tumbler of length `L_{a,w}`... the pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By TA6, `a ⊖ w < b ⊖ w`." TA3's Depends lists TA2, TumblerSub, ZPD, T1, T3, TA6, NAT-sub, NAT-order, NAT-zero, NAT-discrete — but not TA-Pos.

**Issue**: TA6's postcondition (b) — the clause TA3 cites at each of these sites — has literal form `(A s, t ∈ T : Zero(s) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`, with `Zero(s)` being TA-Pos's universal-zero predicate symbol. TumblerSub's conditional postcondition `Pos(a ⊖ w)` (used to certify `b ⊖ w` as "positive") similarly names TA-Pos's existential predicate. Applying TA6 requires discharging its `Zero(s)` hypothesis for `s = a ⊖ w`, and consuming TumblerSub's Pos postcondition requires the Pos symbol; both require TA-Pos as the definitional source. TA3's Depends omits TA-Pos, so the Pos/Zero predicates are consumed in the proof and the citation of TA6 without an axiomatic source — even though every sibling consumer of TA6 in this ASN (TA6 itself, TA-PosDom) cites TA-Pos.

**What needs resolving**: TA3 must either add TA-Pos to its Depends with per-site accounting of the Zero/Pos predicate uses (Sub-cases A1, A3, B1 at minimum, plus the "positive tumbler" / "zero tumbler" framings throughout), or reformulate so that every TA6 application and every "positive"/"zero" attribution of a result tumbler is stated via a symbol or postcondition already supplied by a cited property.
