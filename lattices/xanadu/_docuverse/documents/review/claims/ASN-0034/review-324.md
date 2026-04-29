# Cone Review — ASN-0034/ReverseInverse (cycle 4)

*2026-04-18 20:08*

### TA4 invocation in ReverseInverse undercounts its preconditions

**Foundation**: TA4 (PartialInverse) — Formal Contract Preconditions list `a ∈ T`, `w ∈ T`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)` — six preconditions, not four.

**ASN**: ReverseInverse, Step 2: "TA4 (Partial inverse) requires four preconditions: `Pos(w)` (given), `k = #y` (by Y1), `#w = k` (given), and `(A i : 1 ≤ i < k : yᵢ = 0)` (by Y2). All four hold, so TA4 yields: `(y ⊕ w) ⊖ w = y` — (†)".

**Issue**: TA4's published contract has six preconditions; the narrative names and discharges only four. The carrier-membership preconditions `y ∈ T` and `w ∈ T` (TA4 applied at TA4's `a := y`) are never mentioned. Both can be discharged — `y ∈ T` through TumblerSub's carrier-membership postcondition on `a ⊖ w` (given `a, w ∈ T` and `a ≥ w`), and `w ∈ T` from ReverseInverse's outer precondition — but the narrative "All four hold" terminates the precondition check two items short of TA4's contract, so a reviser who tightens TA4's carrier-membership premises gets no Depends-backed or narrative-backed signal that this invocation site consumes them. The gap also omits the only precondition-chain step that transits through TumblerSub's postcondition (`y = a ⊖ w ∈ T`) rather than through outer preconditions or Y1/Y2, leaving the one cross-property link in the checklist unstated.

**What needs resolving**: Either rewrite the Step 2 precondition check to enumerate all six of TA4's preconditions (naming `y ∈ T` via TumblerSub's carrier-membership postcondition and `w ∈ T` from the outer precondition, alongside the four already listed), or articulate why the carrier-membership preconditions of TA4 can be elided at this invocation while the four listed ones cannot.
