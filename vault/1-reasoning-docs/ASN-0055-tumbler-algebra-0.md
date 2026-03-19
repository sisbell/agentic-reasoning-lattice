# ASN-0055: Tumbler Algebra 0

*2026-03-19*

This ASN extends the tumbler algebra foundation (ASN-0034) with two properties of TumblerAdd that follow directly from the constructive definition but were not stated in ASN-0034. Both are pure tumbler arithmetic facts.


## Left cancellation

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

**TA-LC** (*LeftCancellation*). If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

*Proof.* Let k₁ and k₂ be the action points of x and y. If k₁ < k₂, then (a ⊕ x)_{k₁} = a_{k₁} + x_{k₁} while (a ⊕ y)_{k₁} = a_{k₁} (position k₁ falls in the "copy from start" range of y). Equality gives x_{k₁} = 0, contradicting k₁ being the action point of x. Symmetrically k₂ < k₁ is impossible. So k₁ = k₂ = k.

At position k: a_k + x_k = a_k + y_k gives x_k = y_k. For i > k: x_i = (a ⊕ x)_i = (a ⊕ y)_i = y_i. For i < k: x_i = 0 = y_i. It remains to establish #x = #y. By T3, a ⊕ x = a ⊕ y implies #(a ⊕ x) = #(a ⊕ y). From TumblerAdd's result-length formula, #(a ⊕ w) = max(k − 1, 0) + (#w − k + 1) for any w with action point k. Since both x and y share the same action point k, we get #x = #y. By T3 (same length, same components), x = y.  ∎

TumblerAdd is *left-cancellative*: the start position can be "divided out" from equal results, recovering the displacement uniquely. This is a direct consequence of TumblerAdd's constructive definition — each component of the result is determined by exactly one input, so equality of results propagates back to equality of inputs.


## Right cancellation fails

The converse — right cancellation — does not hold. TumblerAdd's many-to-one property (noted informally in ASN-0034's definition of TumblerAdd) means distinct starts can produce the same result under the same displacement.

**TA-RC** (*RightCancellationFailure*). There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

*Proof by example.* Let a = [1, 3, 5], b = [1, 3, 7], and w = [0, 2, 4] (action point k = 2). Then:

  a ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]
  b ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]  (component 3 of b is discarded — tail replacement)

Wait — b₂ = 3 as well, so b ⊕ w = [1, 5, 4] also. But a₃ = 5 ≠ 7 = b₃, and both are discarded by the tail replacement at k = 2. So a ⊕ w = b ⊕ w = [1, 5, 4] despite a ≠ b.  ∎

The mechanism is TumblerAdd's tail replacement: components of the start position after the action point are discarded and replaced by the displacement's tail. Any two starts that agree on components 1..k and differ only on components after k will produce the same result under any displacement with action point k. Formally:

**TA-MTO** (*ManyToOne*). For any displacement w with action point k and any tumblers a, b with #a ≥ k, #b ≥ k, and a_i = b_i for all 1 ≤ i ≤ k: a ⊕ w = b ⊕ w.

*Proof.* From TumblerAdd's definition: for i < k, (a ⊕ w)_i = a_i = b_i = (b ⊕ w)_i. At i = k, (a ⊕ w)_k = a_k + w_k = b_k + w_k = (b ⊕ w)_k. For i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i. The results have the same length (max(k − 1, 0) + (#w − k + 1) depends only on k and #w). By T3, a ⊕ w = b ⊕ w.  ∎

The converse also holds: if a ⊕ w = b ⊕ w, then a and b must agree on components 1..k (from the "copy from start" region of TumblerAdd), though they may differ freely on components after k. This gives a precise characterization of the equivalence classes: *a and b produce the same result under w if and only if they agree on the first k components, where k is the action point of w.*


## Statement registry

| Label | Statement | Status |
|-------|-----------|--------|
| TA-LC | a ⊕ x = a ⊕ y ⟹ x = y (left cancellation) | introduced |
| TA-RC | Right cancellation fails: ∃ a ≠ b with a ⊕ w = b ⊕ w | introduced |
| TA-MTO | a agrees with b on components 1..k ⟺ a ⊕ w = b ⊕ w for displacement w with action point k | introduced |


## Open Questions

- Does left cancellation extend to a ⊕ x ≤ a ⊕ y ⟹ x ≤ y (left cancellation for the order)? This would strengthen TA1-strict.
- The equivalence-class characterization (TA-MTO converse) suggests that TumblerAdd at action point k is a projection that discards information below level k. Does this projection have useful algebraic properties (idempotence, composition)?
