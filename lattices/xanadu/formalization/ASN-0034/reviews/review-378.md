# Regional Review — ASN-0034/TA-Pos (cycle 4)

*2026-04-22 16:38*

### `≥` is used in T0's axiom without being introduced by any dependency
**Foundation**: T0 (CarrierSetDefinition); NAT-order (NatStrictTotalOrder)
**ASN**: T0 formal contract: "… and `(A a ∈ T :: #a ≥ 1)`." T0 Depends: "NAT-order … supplies `≤` on ℕ, whose converse `≥` appears in the nonemptiness clause `#a ≥ 1`." NAT-order formal contract: "The non-strict relation `≤` on ℕ is defined by `m ≤ n ⟺ m < n ∨ m = n`."
**Issue**: T0's axiom uses the relation symbol `≥`, but NAT-order's formal contract introduces only `<` and `≤` — `≥` is not defined in any cited dependency's contract. The T0 prose calls `≥` "the converse of `≤`", but that prose-level gloss does not enter NAT-order's contract, so `≥` is an ungrounded symbol inside T0's axiom. This parallels the resolved `≠` finding: either the symbol gets a formal introduction in its owning claim, or T0 rephrases without it.
**What needs resolving**: Either extend NAT-order's formal contract to define `≥` (e.g., `m ≥ n ⟺ n ≤ m`), or rewrite T0's nonemptiness clause as `(A a ∈ T :: 1 ≤ #a)` so every symbol in the axiom is grounded in a declared Depends.

### Complementarity bullet's justification doesn't match the claim it justifies
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos formal contract: "*Complementarity:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`, obtained from the defining clauses by the DeMorgan duality of bounded quantifiers, with T0's `(A a ∈ T :: #a ≥ 1)` keeping the index range nonempty so the partition is genuine."
**Issue**: The logical equivalence `Pos(t) ⟺ ¬Zero(t)` holds pointwise by DeMorgan regardless of `#t`; at `#t = 0` both sides collapse (Pos = False, Zero = True) and the biconditional still holds. So `(A a ∈ T :: #a ≥ 1)` is not what makes the complementarity axiom true. Its actual role is separate: it ensures that the class descriptions ("at least one nonzero component"; "at least one component, each equal to `0`") match membership — i.e., that the partition is non-vacuous. The bullet welds a true equivalence to a rationale it doesn't need, and the prose above it does the same weld. A precise reader cannot tell which fact depends on `#a ≥ 1`.
**What needs resolving**: Separate the two facts. State the complementarity equivalence as derivable from the definitions and DeMorgan alone; state the non-vacuity of the partition as a second, distinct consequence that rests on `#a ≥ 1`. The formal contract slot should carry the claim(s), not the derivation narrative.
