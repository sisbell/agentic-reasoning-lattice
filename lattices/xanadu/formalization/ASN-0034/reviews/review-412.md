# Regional Review — ASN-0034/TA0 (cycle 1)

*2026-04-23 01:45*

Reading ASN-0034 as a system, checking claim chains, definition stability, and proof coverage.

### TA0 contract omits Postconditions field
**Class**: OBSERVE
**Foundation**: N/A (internal)
**ASN**: TA0 (WellDefinedAddition). The claim line states `a ⊕ w ∈ T ∧ #(a ⊕ w) = #w`, and the prose calls TA0 a "labelled well-definedness fact," but the *Formal Contract* lists only `Preconditions` and `Depends` — no `Postconditions`.
**Issue**: TumblerAdd and ActionPoint both carry explicit `Postconditions` in their contracts; TA0's whole purpose is to *re-export* two of TumblerAdd's postconditions under a single label, yet those exported facts are absent from the slot that downstream ASNs will cite. A reader reconstructing the dependency graph from contract fields alone would see TA0 as a bare precondition-plus-depends entry with nothing asserted.

### Minimality step in dominance proof elides a ℕ-trichotomy appeal
**Class**: OBSERVE
**Foundation**: N/A (internal)
**ASN**: TumblerAdd, dominance proof, subcase "some `aⱼ > 0` for `j < k`": "For `1 ≤ i < j`: `aᵢ = 0` by minimality of `j`".
**Issue**: Minimality of `j` in `{j : 1 ≤ j < k ∧ aⱼ > 0}` yields `¬(aᵢ > 0)` for `i < j` with `1 ≤ i < k`; converting that to `aᵢ = 0` uses NAT-zero's disjunction `0 < n ∨ 0 = n` to collapse the `¬(0 < aᵢ)` branch. The chain is sound but the step is unnamed here, whereas the parallel move `0 < w_{actionPoint(w)} ⟹ 1 ≤ w_{actionPoint(w)}` in ActionPoint is spelled out with every axiom cited. Inconsistency in granularity, not a gap.

No correctness issues found. Definitions are stable across sections; precondition chain from TA0 → TumblerAdd → ActionPoint is unbroken; all four uniqueness subcases in ActionPoint are walked; both dominance case splits (existential and its complement) are discharged; the `k = 1` edge of dominance is handled by vacuity in the universal branch; `≥` is delivered by the disjunction of T1 case (i) and T3 as the contract advertises.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 186s*
