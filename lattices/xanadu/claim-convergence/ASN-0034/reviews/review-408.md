# Regional Review — ASN-0034/TA5 (cycle 2)

*2026-04-23 01:17*

### NAT-discrete instantiation at m=0 silently relies on NAT-closure's left identity
**Class**: REVISE
**Foundation**: NAT-discrete axiom — `m + 1 ≤ n` in the consequent; NAT-closure's left-identity clause `0 + n = n`.
**ASN**: TA5 proof, Case `k > 0`: *"NAT-discrete (instantiated at `m = 0`, `n = k`) discharges its strict antecedent against the case hypothesis `0 < k` and yields `1 ≤ k`."*
**Issue**: Literal instantiation of NAT-discrete at `m = 0` yields `0 + 1 ≤ k`, not `1 ≤ k`. The rewrite to `1 ≤ k` requires NAT-closure's left identity `0 + n = n` at `n = 1`. That clause is a stated axiom of NAT-closure, but TA5's Depends cites NAT-closure only for addition closure (producing `0 + 1 ∈ ℕ` and `t_{sig(t)} + 1 ∈ ℕ`), not for left identity. The step is used and uncredited.
**What needs resolving**: Either cite NAT-closure's left-identity clause in TA5's Depends slot for the `0 + 1 = 1` rewrite, or reroute the derivation to avoid the instantiation `m = 0` (e.g., supply `1 ≤ k` via a different path).

### NAT-wellorder invoked as greatest-element principle in TA5-SIG
**Class**: REVISE
**Foundation**: NAT-wellorder — least-element principle on nonempty ℕ-subsets (as cited in T1 Depends).
**ASN**: TA5-SIG Depends: *"NAT-wellorder (NatWellOrdering) — greatest-element principle (dual of least-element) gives `max` on the nonempty subset `{i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}` of ℕ bounded above by `#t`."* T1 Depends, in contrast, cites NAT-wellorder as *"least-element principle."*
**Issue**: Least-element wellordering is not self-dual on ℕ. ℕ has no greatest element, so the "dual" statement is not an unconditional wellordering claim — it applies only to nonempty subsets that are *bounded above*. Existence of `max` on a bounded nonempty ℕ-subset is derivable from least-element wellordering (take the least upper bound), but that derivation is suppressed. The two Depends entries use NAT-wellorder as if it exported both primitives, while framing the second as a mere dual.
**What needs resolving**: Either establish (within NAT-wellorder) that the axiom exports a greatest-element clause for bounded nonempty subsets, or have TA5-SIG derive `max` from least-element wellordering with the boundedness witness `#t` made explicit.

VERDICT: REVISE
