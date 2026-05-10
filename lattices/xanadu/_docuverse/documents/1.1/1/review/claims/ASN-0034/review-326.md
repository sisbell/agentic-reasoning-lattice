# Cone Review — ASN-0034/ReverseInverse (cycle 6)

*2026-04-18 20:23*

### TA3-strict invocation in Step 3 undercounts its preconditions

**Foundation**: TA3-strict (OrderPreservationUnderSubtractionStrict) — Formal Contract Preconditions list `a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b` (seven preconditions).

**ASN**: ReverseInverse, Step 3: "We verify the preconditions of TA3-strict (Order preservation under subtraction, strict), which requires strict ordering between two tumblers, both `≥ w`, and equal length." And the two cases: "*Case `y ⊕ w > a`:* We have `a < y ⊕ w`, `a ≥ w`, `y ⊕ w ≥ w` (established above, in fact strict), and `#a = #(y ⊕ w)`. TA3-strict gives …" (and symmetrically in the `y ⊕ w < a` case).

**Issue**: TA3-strict's published contract has seven preconditions; the narrative names and discharges only four (strict order, two dominance relations, length equality). The three carrier-membership preconditions `a ∈ T`, `y ⊕ w ∈ T`, `w ∈ T` (under the operand renamings in each case) are never enumerated. `a ∈ T` and `w ∈ T` are ReverseInverse's outer preconditions, but `y ⊕ w ∈ T` is the cross-Step link — it requires TumblerAdd's carrier-membership postcondition, which in turn requires TumblerAdd's own preconditions at the `y ⊕ w` formation (`y ∈ T`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #y`) to be satisfied. None of these — neither the preconditions of the TumblerAdd invocation that forms `y ⊕ w` nor the postcondition `y ⊕ w ∈ T` that TA3-strict's `∈ T` precondition consumes — are named in Step 3. This parallels the TA4 precondition-count gap already captured in the prior findings, but it is a distinct invocation site (TA3-strict rather than TA4, invoked twice rather than once, and with the additional upstream obligation of discharging TumblerAdd's own preconditions to form `y ⊕ w`), and its carrier-membership chain for `y ⊕ w` is the only cross-Step thread that has no explicit link in the narrative.

**What needs resolving**: Either expand Step 3's TA3-strict precondition check to enumerate all seven preconditions in each case (naming `y ⊕ w ∈ T` via TumblerAdd's carrier-membership postcondition, and discharging TumblerAdd's own four preconditions at the `y ⊕ w` formation — `y ∈ T` via TumblerSub, `w ∈ T` outer, `Pos(w)` outer, `actionPoint(w) ≤ #y` via ActionPoint + Y1), or articulate why carrier-membership preconditions of TA3-strict and TumblerAdd can be elided at these invocations while the four ordering/length preconditions cannot.
