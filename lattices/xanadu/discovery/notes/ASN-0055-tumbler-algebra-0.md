# ASN-0055: Tumbler Algebra 0

*2026-03-19*

This ASN extends the tumbler algebra foundation (ASN-0034) with two properties of TumblerAdd that follow directly from the constructive definition but were not stated in ASN-0034. Both are pure tumbler arithmetic facts.


## Left cancellation

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

**TA-LC** — *LeftCancellation* (LEMMA, lemma). If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

*Proof.* Let k₁ and k₂ be the action points of x and y. If k₁ < k₂, then (a ⊕ x)_{k₁} = a_{k₁} + x_{k₁} while (a ⊕ y)_{k₁} = a_{k₁} (position k₁ falls in the "copy from start" range of y). Equality gives x_{k₁} = 0, contradicting k₁ being the action point of x. Symmetrically k₂ < k₁ is impossible. So k₁ = k₂ = k.

At position k: a_k + x_k = a_k + y_k gives x_k = y_k. For i > k: x_i = (a ⊕ x)_i = (a ⊕ y)_i = y_i. For i < k: x_i = 0 = y_i. It remains to establish #x = #y. By T3, a ⊕ x = a ⊕ y implies #(a ⊕ x) = #(a ⊕ y). From TumblerAdd's result-length formula, #(a ⊕ w) = max(k − 1, 0) + (#w − k + 1) for any w with action point k. Since both x and y share the same action point k, we get #x = #y. By T3 (same length, same components), x = y.  ∎

TumblerAdd is *left-cancellative*: the start position can be "divided out" from equal results, recovering the displacement uniquely. This is a direct consequence of TumblerAdd's constructive definition — each component of the result is determined by exactly one input, so equality of results propagates back to equality of inputs.

*Worked example.* Let a = [2, 5] and suppose a ⊕ x = a ⊕ y = [2, 8]. We recover x and y uniquely. First, the action points must agree: if k_x = 1, then (a ⊕ x)₁ = a₁ + x₁ = 2 + x₁ = 2, giving x₁ = 0, which contradicts k_x = 1. So k_x = 2, and by the same argument k_y = 2. At position k = 2: a₂ + x₂ = 5 + x₂ = 8 gives x₂ = 3, and a₂ + y₂ = 5 + y₂ = 8 gives y₂ = 3. For i < k: x₁ = 0 = y₁. From the result-length formula with k = 2: #(a ⊕ x) = max(1, 0) + (#x − 1) = #x, so #x = 2 = #y. By T3, x = y = [0, 3].


## Right cancellation fails

The converse — right cancellation — does not hold. TumblerAdd's many-to-one property (noted informally in ASN-0034's definition of TumblerAdd) means distinct starts can produce the same result under the same displacement.

**TA-RC** — *RightCancellationFailure* (LEMMA, lemma). There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

*Proof by example.* Let a = [1, 3, 5], b = [1, 3, 7], and w = [0, 2, 4] (action point k = 2). Then:

  a ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]
  b ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]  (component 3 of b is discarded — tail replacement)

So a ⊕ w = b ⊕ w = [1, 5, 4] despite a ≠ b — the difference at position 3 is erased by tail replacement.  ∎

The mechanism is TumblerAdd's tail replacement: components of the start position after the action point are discarded and replaced by the displacement's tail. Any two starts that agree on components 1..k and differ only on components after k will produce the same result under any displacement with action point k. Formally:

**TA-MTO** — *ManyToOne* (LEMMA, lemma). For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

*Proof (forward).* Assume a_i = b_i for all 1 ≤ i ≤ k. From TumblerAdd's definition: for i < k, (a ⊕ w)_i = a_i = b_i = (b ⊕ w)_i. At i = k, (a ⊕ w)_k = a_k + w_k = b_k + w_k = (b ⊕ w)_k. For i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i. The results have the same length (max(k − 1, 0) + (#w − k + 1) depends only on k and #w). By T3, a ⊕ w = b ⊕ w.  ∎

*Proof (converse).* Suppose a ⊕ w = b ⊕ w. Let k be the action point of w. We must show a_i = b_i for all 1 ≤ i ≤ k.

(a) For i < k: position i falls in the "copy from start" region of TumblerAdd, so (a ⊕ w)_i = a_i and (b ⊕ w)_i = b_i. From a ⊕ w = b ⊕ w we get a_i = b_i.

(b) At i = k: (a ⊕ w)_k = a_k + w_k and (b ⊕ w)_k = b_k + w_k. Equality gives a_k + w_k = b_k + w_k, hence a_k = b_k by cancellation in ℕ.

Components after k are unconstrained: for i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i regardless of a_i and b_i.  ∎

This gives a precise characterization of the equivalence classes: *a and b produce the same result under w if and only if they agree on the first k components, where k is the action point of w.*


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| TA-LC | LEMMA, lemma | a ⊕ x = a ⊕ y ⟹ x = y (left cancellation) | introduced |
| TA-RC | LEMMA, lemma | Right cancellation fails: ∃ a ≠ b with a ⊕ w = b ⊕ w | introduced |
| TA-MTO | LEMMA, lemma | a agrees with b on components 1..k ⟺ a ⊕ w = b ⊕ w for displacement w with action point k | introduced |


## Open Questions

- Does left cancellation extend to a ⊕ x ≤ a ⊕ y ⟹ x ≤ y (left cancellation for the order)? This would strengthen TA1-strict.
- The equivalence-class characterization (TA-MTO converse) suggests that TumblerAdd at action point k is a projection that discards information below level k. Does this projection have useful algebraic properties (idempotence, composition)?
