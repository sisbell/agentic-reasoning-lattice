# ASN-0057: Displacement Identities

*2026-03-19*

ASN-0034 defined the tumbler space T with its total order (T1) and its arithmetic — the addition ⊕ that advances along the tumbler line (TumblerAdd), the subtraction ⊖ that recovers displacements (TumblerSub). Given two positions a and b on the tumbler line, a natural question is whether b ⊖ a yields a displacement w such that a ⊕ w faithfully recovers b. This ASN establishes the well-definedness condition for such displacement recovery and the round-trip identity that guarantees faithfulness when the operands share the same tumbler length.


## Displacement recovery

From TumblerAdd, a ⊕ w acts at the action point k of w: it copies a₁..aₖ₋₁, advances aₖ by wₖ, and replaces the tail with w's tail. So if a ⊕ w = b, then a and b agree on components 1..k−1 and diverge at k, with bₖ = aₖ + wₖ and bᵢ = wᵢ for i > k. Reading off the width:

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

where k = divergence(a, b). This is exactly the formula for b ⊖ a from ASN-0034's TumblerSubtract. We write w = b ⊖ a and call it the *displacement from a to b*. The displacement is well-defined when:

**D0** — *DisplacementWellDefined* (precondition). a < b, and the divergence k of a and b satisfies k ≤ #a.

D0 ensures the displacement b ⊖ a is a well-defined positive tumbler, and that a ⊕ (b ⊖ a) is defined (TA0 satisfied, since the displacement is positive and its action point k ≤ #a). It does not guarantee round-trip faithfulness — the identity a ⊕ (b ⊖ a) = b additionally requires #a = #b. When #a > #b, TumblerSubtract produces a displacement of length max(#a, #b) = #a, and the round-trip a ⊕ (b ⊖ a) yields a tumbler of length #a; since #a > #b, this result cannot equal b (by T3). (The case #a < #b with type (i) divergence — where a and b differ at a shared position, so k ≤ #a — also admits a faithful round-trip, since the D1 proof depends only on k ≤ #a, not on #a = #b. But when #a < #b and a is a proper prefix of b, the divergence is k = #a + 1 > #a, violating TA0 — no valid displacement exists.)

When a is a proper prefix of b (divergence type (ii) from ASN-0034), the divergence is #a + 1, exceeding #a, and no valid displacement exists.


## Round-trip identity

**D1** — *DisplacementRoundTrip* (lemma). For tumblers a, b ∈ T with a < b and #a = #b:

  a ⊕ (b ⊖ a) = b

*Proof.* Let k = divergence(a, b). Since #a = #b, this is type (i) divergence with k ≤ #a and aₖ < bₖ. Define w = b ⊖ a by TumblerSubtract: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k. The result has length #a. Now w > 0 since wₖ > 0, and the action point of w is k ≤ #a, so TA0 is satisfied. Applying TumblerAdd: (a ⊕ w)ᵢ = aᵢ = bᵢ for i < k (before divergence), (a ⊕ w)ₖ = aₖ + (bₖ − aₖ) = bₖ, and (a ⊕ w)ᵢ = wᵢ = bᵢ for i > k. Every component matches: a ⊕ w = b.  ∎

When a = b, no displacement is needed; the degenerate case is handled separately since b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed (TA0 requires w > 0). D0 ensures the displacement is well-defined; D1 ensures the round-trip is faithful for a < b.


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| D0 | precondition | Displacement well-definedness: a < b and divergence(a, b) ≤ #a ensures positive displacement with TA0 satisfied | introduced |
| D1 | lemma | Displacement round-trip: for a < b with #a = #b, a ⊕ (b ⊖ a) = b | introduced |
