# ASN-0057: Displacement Identities

*2026-03-19*

ASN-0034 defined the tumbler space T with its total order (T1) and its arithmetic — the addition ⊕ that advances along the tumbler line (TumblerAdd), the subtraction ⊖ that recovers displacements (TumblerSub). Given two positions a and b on the tumbler line, a natural question is whether b ⊖ a yields a displacement w such that a ⊕ w faithfully recovers b. This ASN establishes the well-definedness condition for such displacement recovery and the round-trip identity that guarantees faithfulness.


## Displacement recovery

From TumblerAdd, a ⊕ w acts at the action point k of w: it copies a₁..aₖ₋₁, advances aₖ by wₖ, and replaces the tail with w's tail. So if a ⊕ w = b, then a and b agree on components 1..k−1 and diverge at k, with bₖ = aₖ + wₖ and bᵢ = wᵢ for i > k. Reading off the width:

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

where k = divergence(a, b). This is exactly the formula for b ⊖ a from ASN-0034's TumblerSub. We write w = b ⊖ a and call it the *displacement from a to b*. The displacement is well-defined when:

**D0** — *DisplacementWellDefined* (precondition). a < b, and the divergence k of a and b satisfies k ≤ #a.

D0 ensures the displacement b ⊖ a is a well-defined positive tumbler, and that a ⊕ (b ⊖ a) is defined (TA0 satisfied, since the displacement is positive and its action point k ≤ #a). Round-trip faithfulness additionally requires #a ≤ #b. The displacement w = b ⊖ a has length max(#a, #b), and the result a ⊕ w has length #w (by the result-length identity from TumblerAdd). When #a > #b, #w = #a > #b, so the result cannot equal b (by T3). When #a ≤ #b, #w = #b, giving the correct result length; combined with the component-by-component argument at the action point (k ≤ #a for arithmetic, #w = #b for length), this establishes a ⊕ w = b (D1 below).

When a is a proper prefix of b (divergence type (ii) from ASN-0034), the divergence is #a + 1, exceeding #a, and D0 is not satisfied — no valid displacement exists.


## Round-trip identity

**D1** — *DisplacementRoundTrip* (lemma). For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

*Proof.* Let k = divergence(a, b). By hypothesis k ≤ #a ≤ #b, so this is type (i) divergence with aₖ < bₖ. Define w = b ⊖ a by TumblerSub: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k. The result has length max(#a, #b) = #b. Now w > 0 since wₖ > 0, and the action point of w is k ≤ #a, so TA0 is satisfied. Applying TumblerAdd: (a ⊕ w)ᵢ = aᵢ = bᵢ for i < k (before divergence), (a ⊕ w)ₖ = aₖ + (bₖ − aₖ) = bₖ, and (a ⊕ w)ᵢ = wᵢ = bᵢ for i > k. The result has length #w = #b; every component matches b, so a ⊕ w = b by T3.  ∎

When a = b, no displacement is needed; the degenerate case is handled separately since b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed (TA0 requires w > 0). D0 ensures the displacement is well-defined; D1 ensures the round-trip is faithful when additionally #a ≤ #b.


## Worked example

Consider a = [1, 2, 3] and b = [1, 5, 1]. We have #a = #b = 3.

*D0 check.* divergence(a, b) = 2, since a₁ = b₁ = 1 and a₂ = 2 ≠ 5 = b₂. The condition k = 2 ≤ #a = 3 is satisfied.

*Displacement.* By TumblerSub, w = b ⊖ a: w₁ = 0 (i < k), w₂ = 5 − 2 = 3 (i = k), w₃ = 1 (i > k, from b). So w = [0, 3, 1].

*Round-trip.* The action point of w is 2. By TumblerAdd, a ⊕ [0, 3, 1]: position 1 copies a₁ = 1, position 2 computes 2 + 3 = 5, position 3 copies w₃ = 1. Result: [1, 5, 1] = b.  ✓

The generalization to #a < #b can be seen with a' = [1, 2] and the same b = [1, 5, 1]. Here #a' = 2 < 3 = #b, the divergence is still 2 (a'₂ = 2 ≠ 5 = b₂), and k = 2 ≤ #a' = 2 satisfies D0. TumblerSub (zero-padding a' to length 3) gives the same w = [0, 3, 1] of length 3. The round-trip a' ⊕ [0, 3, 1] produces [1, 5, 1] = b — the result has length #w = 3 = #b, matching the target.


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| D0 | precondition | Displacement well-definedness: a < b and divergence(a, b) ≤ #a ensures positive displacement with TA0 satisfied | introduced |
| D1 | lemma | Displacement round-trip: for a < b with divergence(a, b) ≤ #a and #a ≤ #b, a ⊕ (b ⊖ a) = b | introduced |
