# Cone Review — ASN-0034/T2 (cycle 1)

*2026-04-17 12:46*

### NAT-* axioms cited but not stated
**Foundation**: T0 (CarrierSetDefinition) — "The standard properties of ℕ that downstream proofs cite … are stated as separate axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder, NAT-sub, NAT-cancel, NAT-addassoc). This list is exhaustive: the ASN states no NAT-* axiom outside it."
**ASN**: Only NAT-order (NatStrictTotalOrder) appears as a stated axiom in the ASN. T1's Depends list invokes NAT-addcompat (strict successor inequality), NAT-discrete (forward direction `m < n ⟹ m + 1 ≤ n`), NAT-cancel (right cancellation at fixed summand `1`), and NAT-wellorder (least element of the divergence set) at dozens of concrete sites, and the narrative text refers to them by name.
**Issue**: T0 asserts the NAT-* list is stated in the ASN as separate axioms, but the document shown contains only NAT-order. The other six NAT-* axioms — NAT-closure, NAT-discrete, NAT-addcompat, NAT-wellorder, NAT-sub, NAT-cancel, NAT-addassoc — are cited as ground truth without any formal Axiom contract, so every T1 site that depends on them rests on an unstated premise despite T0's exhaustiveness claim. If instead these are meant to live outside the ASN, T0's "this list is exhaustive; the ASN states no NAT-* axiom outside it" is false (the ASN states none *inside* it either).
**What needs resolving**: Either add the six missing NAT-* axiom contracts in the same shape as NAT-order, or rewrite T0 to reflect that the NAT-* properties are imported from an external foundation (and record that foundation as a Depends entry on T1 and on any other property that cites them).

### T2 Depends omits NAT-order
**Foundation**: NAT-order (NatStrictTotalOrder) — trichotomy: "(A m, n ∈ ℕ :: exactly one of m < n, m = n, n < m)".
**ASN**: T2 proof — Case 1: "The scan finds `aₖ ≠ bₖ` … The ordering is decided by whether `aₖ < bₖ` or `bₖ < aₖ`"; Case 2: "if `m < n` … if `n < m` … if `m = n`". T2 *Depends* lists T0, T1, T3.
**Issue**: Both case dispatches are trichotomy on ℕ. In Case 1, the step from `aₖ ≠ bₖ` to the two-way split `aₖ < bₖ ∨ bₖ < aₖ` is exactly NAT-order's trichotomy at the component pair `(aₖ, bₖ)`. In Case 2, partitioning `(m, n)` into `m < n`, `n < m`, `m = n` is NAT-order's trichotomy at the length pair — and exhaustiveness of the case split (postcondition (a), that the ordering is always decided) depends on this trichotomy being exhaustive. Neither invocation is discharged by T0, T1, or T3.
**What needs resolving**: T2 must either add NAT-order to its Depends list with the two trichotomy sites called out, or rework the proof so that the case splits follow from properties already in its Depends closure.
