The rest of the proof — T4-validity of `a` via S7a → T10a.4, construction of `origin(a) ∈ T` via T0 comprehension, zero-count = 2 via the position inventory and NAT-card, boundary components from T4b's strict-positivity postcondition, the Identification step via S7a, the Uniqueness step via S7d + GlobalUniqueness, and Permanence via S0 — is sound. Both findings below sit in the no-two-zeros-adjacent sub-argument inside S7's Well-definedness step.

### Missing case walk in the "matching the orderings" inference
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder) — irreflexivity `¬(n < n)`, exactly-one trichotomy `¬(m < n ∧ n < m)`
**ASN**: S7 (StructuralAttribution), Well-definedness, no-two-zeros-adjacent sub-proof — "matching the orderings i < i + 1 and #N(a) + 1 < ((#N(a) + 1) + #U(a)) + 1 forces i = #N(a) + 1 and i + 1 = ((#N(a) + 1) + #U(a)) + 1"
**Issue**: At this point the proof knows `i ∈ {#N(a)+1, X}` and `i+1 ∈ {#N(a)+1, X}` (where `X = ((#N(a)+1)+#U(a))+1`). That is a four-case domain; three must be eliminated before the conclusion follows. The proof says "forces" without naming what rules out each impossible case: (a) `i = #N(a)+1, i+1 = #N(a)+1` — ruled out by `i < i+1` implying `i ≠ i+1`, which requires NAT-order's irreflexivity; (b) `i = X, i+1 = X` — ruled out by the same irreflexivity argument; (c) `i = X, i+1 = #N(a)+1` — ruled out because `#N(a)+1 < X` makes `i+1 < i`, contradicting `i < i+1`, which requires NAT-order's exactly-one trichotomy `¬(i < i+1 ∧ i+1 < i)`. The word "forces" substitutes for this case walk without performing it.
**What needs resolving**: The proof must walk all four cases and cite, for each eliminated case, the specific NAT-order clause — irreflexivity for (a) and (b), exactly-one trichotomy for (c) — that makes the case impossible.

### "By transitivity of <" does not cover the 2 = 1 branch
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder) — ≤-definition `m ≤ n ⟺ m < n ∨ m = n`, `<`-transitivity, irreflexivity
**ASN**: S7 (StructuralAttribution), Well-definedness, no-two-zeros-adjacent sub-proof — "the chain 1 = #U(a) + 1 ≥ 2 > 1 forces 1 > 1 by transitivity of <. This contradicts NAT-order's irreflexivity ¬(1 < 1)"
**Issue**: The step derives `1 > 1` from `1 ≥ 2` (equivalently `2 ≤ 1`) and `2 > 1` (equivalently `1 < 2`) and cites only `<`-transitivity. But `2 ≤ 1` by the ≤-definition means `2 < 1 ∨ 2 = 1`, producing two branches: (a) `2 < 1` with `1 < 2` gives `1 < 1` by `<`-transitivity — the cited tool applies; (b) `2 = 1` substituted into `1 < 2` gives `1 < 1` by congruence of `<` under equality (Leibniz), not by `<`-transitivity. The citation does not cover branch (b), leaving the Leibniz step unjustified under the named tool.
**What needs resolving**: The proof must expand the step to name the ≤-definition case split on `2 ≤ 1` and supply the justification for each branch: `<`-transitivity for the `2 < 1` case; Leibniz substitution (equality of `2` and `1` imported into `1 < 2`) for the `2 = 1` case.

VERDICT: REVISE