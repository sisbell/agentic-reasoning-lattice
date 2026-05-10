# Cone Review — ASN-0034/D2 (cycle 2)

*2026-04-18 18:35*

### D1's action-point derivation lacks a Depends source

**Foundation**: ActionPoint defines `actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})` — the action point is the first nonzero component. TumblerSub's conditional postcondition `actionPoint(a ⊖ w) = zpd(a, w)` provides an alternative route to identify the action point of a subtraction result.

**ASN**: D1 proof, step deriving the action point of w: "Third, the action point of w is k: every component before position k is zero, and wₖ > 0, so k is the first positive component. Since k ≤ #a by hypothesis, the precondition of TumblerAdd (TA0) is satisfied". This identification then feeds the TA0 citation in D1's Depends ("establishes a ⊕ w ∈ T from Pos(w) and actionPoint(w) = k ≤ #a").

**Issue**: D1's Depends list does not include ActionPoint, and the TumblerSub Depends entry enumerates only "component formulas… establishes w ∈ T from b ≥ a… length-pair dispatch" — it does not mention TumblerSub's conditional postcondition `actionPoint(a ⊖ w) = zpd(a, w)`. The proof's "first positive component" reasoning relies on ActionPoint's defining minimum-formula, but that property is not cited as a dependency. By contrast, D0 explicitly cites ActionPoint ("the postcondition `actionPoint(b ⊖ a) = divergence(a, b)` uses ActionPoint's definition (derived via TumblerSub's conditional postcondition and the ZPD–Divergence identification)") for the same role.

**What needs resolving**: Either add ActionPoint as a Depends entry in D1 (matching D0's treatment), or expand the TumblerSub Depends entry to enumerate the actionPoint conditional postcondition that supplies `actionPoint(b ⊖ a) = k` directly — and adjust the proof text accordingly so that the action-point identification routes through the chosen source.

---

### TumblerSub's no-divergence branch length argument relies on tumbler-typing of operands not made fully explicit

**Foundation**: T0 characterises T as finite sequences over ℕ with length ≥ 1. TumblerSub's Definition produces a result of length `L` selected by NAT-order trichotomy on `(#a, #w)`.

**ASN**: TumblerSub proof of `a ⊖ w ∈ T`: "The result is therefore a finite sequence over ℕ with length `L ≥ 1` — since `a, w ∈ T` requires both `#a ≥ 1` and `#w ≥ 1`, and `L` is named by the trichotomy dispatch as one of `#a` or `#w`, each of which is at least 1".

**Issue**: This argument is correct but the Depends does not enumerate that the `L ≥ 1` step consumes T0's length axiom (which supplies `#a ≥ 1` and `#w ≥ 1`) at this site. The T0 citation in TumblerSub's Depends discharges membership/projection but does not call out this additional load-bearing use of T0's length-≥-1 stipulation, which is what licenses the "result has length ≥ 1" conclusion needed to land back in T. Other properties (e.g., TumblerAdd) make the parallel use of `#w ≥ 1` from `w ∈ T` explicit when justifying `#(a ⊕ w) ≥ 1`.

**What needs resolving**: Extend TumblerSub's T0 Depends entry to enumerate the `L ≥ 1` step's consumption of T0's `#a ≥ 1 ∧ #w ≥ 1` stipulation, matching the per-step citation discipline TumblerAdd applies for the analogous result-length-≥-1 step.
