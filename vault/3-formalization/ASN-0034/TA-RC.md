### Right cancellation and the many-to-one property

The converse — right cancellation — does not hold. TumblerAdd's many-to-one property (noted informally in the definition of TumblerAdd above) means distinct starts can produce the same result under the same displacement.

**TA-RC (RightCancellationFailure).** There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

*Proof.* We exhibit three specific tumblers and verify the claim by direct computation.

Let `a = [1, 3, 5]`, `b = [1, 3, 7]`, and `w = [0, 2, 4]`. We first establish that `a ≠ b`: the third components differ (`5 ≠ 7`), so `a ≠ b` by T3 (CanonicalRepresentation).

Next we verify that both additions are well-defined. The displacement `w` has action point `k = 2`, since `w₁ = 0` and `w₂ = 2 > 0`. For `a ⊕ w`, TA0 requires `actionPoint(w) ≤ #a`, i.e. `2 ≤ 3`, which holds. For `b ⊕ w`, TA0 requires `actionPoint(w) ≤ #b`, i.e. `2 ≤ 3`, which likewise holds.

We compute `a ⊕ w` by TumblerAdd's constructive definition with action point `k = 2`:

- Position `i = 1` (`i < k`): prefix copy gives `(a ⊕ w)₁ = a₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(a ⊕ w)₂ = a₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(a ⊕ w)₃ = w₃ = 4`.

So `a ⊕ w = [1, 5, 4]`.

We compute `b ⊕ w` by the same three rules:

- Position `i = 1` (`i < k`): prefix copy gives `(b ⊕ w)₁ = b₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(b ⊕ w)₂ = b₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(b ⊕ w)₃ = w₃ = 4`.

So `b ⊕ w = [1, 5, 4]`.

Both results are `[1, 5, 4]`, hence `a ⊕ w = b ⊕ w`. The critical observation is that `a` and `b` differ only at position 3, which lies after the action point `k = 2`. TumblerAdd's tail-copy rule discards all components of the start after position `k`, replacing them with the displacement's tail. The difference between `a₃ = 5` and `b₃ = 7` is therefore erased — neither value contributes to the result.

We have exhibited `a ≠ b` with `a ⊕ w = b ⊕ w`, both sides well-defined: right cancellation fails.  ∎

*Formal Contract:*
- *Axiom:* ∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w

The mechanism is TumblerAdd's tail replacement: components of the start position after the action point are discarded and replaced by the displacement's tail. Any two starts that agree on components 1..k and differ only on components after k will produce the same result under any displacement with action point k. Formally:
