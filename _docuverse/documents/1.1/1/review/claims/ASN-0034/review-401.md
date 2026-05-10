# Regional Review — ASN-0034/T4a (cycle 3)

*2026-04-23 00:37*

### Exactly-one trichotomy used but not axiomatized
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder), T4 (HierarchicalParsing)
**ASN**: NAT-order's axiom slot states totality as pure disjunction: "`(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (totality)", and the accompanying prose explicitly phrases it as "Totality: for any `m, n ∈ ℕ`, **at least one** of `m < n`, `m = n`, `n < m` holds". T4's Exhaustion, however, asserts the stronger form and cites it by name: "Trichotomy at `(zeros(t), m)` asserts that **exactly one** of `zeros(t) < m`, `zeros(t) = m`, `m < zeros(t)` holds... **trichotomy's exactly-one clause then forbids the third**."
**Issue**: Exactly-one is strictly stronger than at-least-one. To derive it from NAT-order's axioms one must exclude `A ∧ B` for each pair `A, B ∈ {m < n, m = n, n < m}`. Transitivity+irreflexivity excludes `m < n ∧ n < m`, but excluding `m < n ∧ m = n` (and `n < m ∧ m = n`) requires substitution of equals under `<` — the very principle the Exhaustion explicitly disclaims: "substitution of equals under `<` is not among NAT-order's stated properties, so we avoid relying on it." The proof therefore both disclaims the principle and (one sentence later) relies on its consequence. In the concrete branches, e.g., at `m = 0` the case `0 = zeros(t) ∧ zeros(t) < 0` is ruled out only by substitution; at later steps, the `m = zeros(t) ∧ zeros(t) < m` case is the same pattern. At-least-one alone does not justify "forbids the third" once one of the other two holds.
**What needs resolving**: Either (a) NAT-order's axiom slot must export exactly-one (stating that `<` and `=` are mutually exclusive, or equivalently that `m < n ⟹ m ≠ n`, as an axiom or as a derivable Consequence with its licensing principle explicitly declared — e.g., treating Leibniz substitution as a logical primitive available to all ASNs), and the Exhaustion's disclaimer must be reconciled with that; or (b) T4's Exhaustion must re-route each `A ∧ B` exclusion using only properties NAT-order actually exports, which for the `A ∧ (m = zeros(t))` branches means either citing NAT-zero's Consequence `¬(n < 0)` at `m = 0` (available) and finding analogous lever at `m ∈ {1, 2, 3}` (not currently exported by any foundation), or accepting substitution as logical.

VERDICT: REVISE
