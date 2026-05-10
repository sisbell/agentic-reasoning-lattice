# Cone Review — ASN-0034/PositiveTumbler (cycle 5)

*2026-04-16 22:10*

### TA0's *Depends* clause omits T0
**Foundation**: n/a (foundation ASN, internal dependency chain)
**ASN**: TA0 (WellDefinedAddition), *Depends* clause lists only "TA-Pos (PositiveTumbler, this ASN)", "TumblerAdd (TumblerAdd, this ASN)", and "ActionPoint (ActionPoint, this ASN)". T0 is not cited. Preconditions state "a ∈ T, w ∈ T". The proof concludes "each component of the result lies in ℕ and `#(a ⊕ w) = #w ≥ 1`, so `a ⊕ w ∈ T`", and the postcondition is "a ⊕ w ∈ T, #(a ⊕ w) = #w".
**Issue**: T0 is the property that defines the carrier set T, the length function `#·`, the component projection `·ᵢ`, and the axiom `#a ≥ 1 for all a ∈ T`. TA0 is load-bearing on T0 in three distinct places: (i) the preconditions `a ∈ T` and `w ∈ T` have no meaning without T0's definition of T; (ii) the proof's assertion `#w ≥ 1` is T0's length axiom applied to `w ∈ T`, not a consequence of TumblerAdd; (iii) the postcondition `a ⊕ w ∈ T` re-assembles the T0 membership condition (finite sequence over ℕ with length ≥ 1) from TumblerAdd's component-in-ℕ fact plus T0's length lower bound. Sister properties follow the convention (T1 and T3 both cite T0 in their *Depends* clauses); TA0 alone elides it. In a foundation ASN whose citation hygiene is otherwise explicit — TA0 even tags "Pos(w)" and "actionPoint(w) ≤ #a" with their defining properties — the omission of the foundational carrier-set citation is a gap in the dependency chain, not a stylistic shorthand.
**What needs resolving**: Add T0 (CarrierSetDefinition) to TA0's *Depends* clause with a note identifying which T0 facts are used (carrier-set definition for the preconditions, `#a ≥ 1` length axiom for the `#w ≥ 1` step in the proof, and the three-part membership characterisation assembled in the postcondition `a ⊕ w ∈ T`).

## Result

Cone converged after 6 cycles.

*Elapsed: 3223s*
