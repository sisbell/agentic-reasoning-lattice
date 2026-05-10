# Cone Review — ASN-0034/TA3 (cycle 1)

*2026-04-16 07:28*

### TA6 formal contract omits dependency declarations
**Foundation**: (internal — foundation ASN)
**ASN**: TA6 (ZeroTumblers), formal contract section — the contract lists only postconditions, no Depends field
**Issue**: The proof header states "Proof (from T1, T4)" and the body relies on both: T1 supplies the ordering witness in Conjunct 2, and T4 supplies the positive-first-component constraint that is the *sole* basis for Conjunct 1 ("T4 requires every valid address to satisfy `t₁ > 0`"). Neither dependency appears in the formal contract. T4 is particularly critical — it is not defined anywhere in the presented ASN content, so a reader or formalization tool cannot trace the precondition chain for Conjunct 1 at all.
**What needs resolving**: TA6's formal contract must include a Depends field listing T1 and T4, with the same citation style used by the other properties in this ASN.

---

### TA3 formal contract omits dependency declarations
**Foundation**: (internal — foundation ASN)
**ASN**: TA3 (OrderPreservationUnderSubtractionWeak), formal contract — lists only preconditions and postconditions
**Issue**: The proof invokes at least five other properties: TA2 (well-formedness of subtraction results), TumblerSub (subtraction definition and its precondition consequence that `aₖ > wₖ` at the zpd), T1 (ordering definition for every case split), T3 (equality from component agreement in Sub-case A2's length-equality branch), and TA6 (zero-tumbler ordering in Sub-cases A1, A3, B1). None are declared. This is the longest and most complex proof in the ASN; its dependency chain is the one most in need of explicit tracing.
**What needs resolving**: TA3's formal contract must include a Depends field enumerating every property the proof relies on, with the role of each dependency stated (as done in TumblerSub's contract).

---

### Inconsistent assumptions about whether T admits the empty sequence
**Foundation**: (internal — T0 CarrierSetDefinition, not shown)
**ASN**: TumblerSub vs TA6
**Issue**: TumblerSub's postcondition proof states as fact: "since `a, w ∈ T` requires `#a ≥ 1` and `#w ≥ 1`" — treating minimum length 1 as a consequence of T-membership. TA6's proof for Conjunct 1 branches on `#t = 0` for `t ∈ T`: "If `#t = 0`, then `t` has no first component…" — treating length 0 as a reachable case for T-members. These are contradictory beliefs about T0. If T0 guarantees `#t ≥ 1`, TumblerSub is correct but TA6 reasons about an impossible case (misleading about the domain). If T0 permits the empty sequence, TumblerSub's claim that `max(#a, #w) ≥ 1` is unfounded and TA2's membership proof breaks.
**What needs resolving**: The ASN must settle whether T includes the empty sequence, and both TumblerSub and TA6 must be consistent with that decision. If T0 already settles this, the inconsistent property should be corrected; if T0 is ambiguous, T0 itself needs tightening.

---

### Non-strict ordering relations ≤ and ≥ used without grounding
**Foundation**: T1 (LexicographicOrder) — defines `<` and proves it a strict total order
**ASN**: TA2 precondition `a ≥ w`; TA3 preconditions `a ≥ w`, `b ≥ w` and postcondition `a ⊖ w ≤ b ⊖ w`; TumblerSub precondition `a ≥ w (T1)`
**Issue**: T1 defines only the strict relation `<` and proves irreflexivity, trichotomy, and transitivity for it. The non-strict relations `≤` and `≥` appear in the preconditions or postconditions of three properties but are never formally introduced — no property's postcondition exports their definition, and no formal contract cites a definition for them. While `a ≤ b ⟺ a < b ∨ a = b` is standard, a specification targeting TLA+ formalization cannot leave a relation that appears in multiple contracts as an implicit derivation. The TumblerSub precondition annotation "`a ≥ w` (T1)" even cites T1 as the source, but T1's contract does not export `≥`.
**What needs resolving**: Either T1's postconditions must be extended to export the derived relations `≤` and `≥` with their definitions, or a separate property must define them. Every property that uses `≤` or `≥` must then cite that definition in its Depends.
