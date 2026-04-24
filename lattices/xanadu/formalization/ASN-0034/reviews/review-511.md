# Regional Review — ASN-0034/OrdinalShift (cycle 1)

*2026-04-24 09:50*

### "Constant time" mis-states operation complexity
**Class**: OBSERVE
**Foundation**: —
**ASN**: TumblerAdd, "No carry propagation" paragraph: "This is why the operation is fast — constant time regardless of tumbler length."
**Issue**: The operation copies components `1..k−1` from `a` and `k+1..n` from `w`, which is linear in `n`. The contrast with carry-propagating arithmetic (no recursive upward cascade from position `k`) is valid, but "constant time regardless of tumbler length" mis-states the complexity class. The precise statement is: a single ℕ-addition at position `k`, with no propagation to positions `< k`.

### "NAT-order's disjointness clause" cited as named export
**Class**: OBSERVE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: OrdinalDisplacement, promotion proof: "By NAT-order's disjointness clause `(A m, n ∈ ℕ : m < n : m ≠ n)` instantiated at `(0, n)` ..."
**Issue**: NAT-order's Formal Contract exports exactly-one-trichotomy as a Consequence with conjunct `¬(m < n ∧ m = n)`; the form `m < n ⟹ m ≠ n` is a one-step contrapositive, not a named clause. NAT-sub's body explicitly notes this, calling it "a derivable contrapositive ... left ... as a derivable contrapositive of the exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct." The OrdinalDisplacement citation invents a "disjointness clause" that isn't in the contract; routing via the conjunct + contrapositive would be consistent with how NAT-sub itself cites the same fact.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 741s*
