### Right cancellation and the many-to-one property

The converse — right cancellation — does not hold.

**TA-RC (RightCancellationFailure).** There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

*Proof.* We exhibit three specific tumblers and verify the claim by direct computation.

Let `a = [1, 3, 5]`, `b = [1, 3, 7]`, and `w = [0, 2, 4]`. Each is a length-3 nonempty finite sequence over ℕ; T0's comprehension clause, instantiated at `p = 3` and the component maps `r_a(1)=1, r_a(2)=3, r_a(3)=5`, `r_b(1)=1, r_b(2)=3, r_b(3)=7`, and `r_w(1)=0, r_w(2)=2, r_w(3)=4`, supplies witness tumblers in `T` with these lengths and components, establishing `a, b, w ∈ T`. The third components differ (`5 ≠ 7`), so `a ≠ b` by T3.

The displacement `w` has action point `k = 2`, since `w₁ = 0` and `w₂ = 2 > 0`. TA0 requires `actionPoint(w) ≤ #a` and `actionPoint(w) ≤ #b`; both reduce to `2 ≤ 3`, which holds.

We compute `a ⊕ w` by TumblerAdd with action point `k = 2`:

- Position `i = 1` (`i < k`): prefix copy gives `(a ⊕ w)₁ = a₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(a ⊕ w)₂ = a₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(a ⊕ w)₃ = w₃ = 4`.

So `a ⊕ w = [1, 5, 4]`.

We compute `b ⊕ w` by the same three rules:

- Position `i = 1` (`i < k`): prefix copy gives `(b ⊕ w)₁ = b₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(b ⊕ w)₂ = b₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(b ⊕ w)₃ = w₃ = 4`.

So `b ⊕ w = [1, 5, 4]`.

Both results are `[1, 5, 4]`, hence `a ⊕ w = b ⊕ w`. The tail-copy rule discards components of the start after position `k`, so the difference between `a₃ = 5` and `b₃ = 7` is erased.

We have exhibited `a ≠ b` with `a ⊕ w = b ⊕ w`, both sides well-defined: right cancellation fails.  ∎

*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — comprehension clause, instantiated at length `p = 3` with the component maps for `a = [1,3,5]`, `b = [1,3,7]`, and `w = [0,2,4]` respectively, establishes `a, b, w ∈ T` — the carrier-set membership presupposed by every condition cited below.
  - T3 (CanonicalRepresentation) — inequality from a single component disagreement.
  - TA0 (WellDefinedAddition) — action-point bound for well-definedness.
  - TA-Pos (PositiveTumbler) — positivity of `w` licensing the action point.
  - ActionPoint (ActionPoint) — minimum-position formula fixing `k = 2`.
  - TumblerAdd (TumblerAdd) — three-region rule computing each side.
- *Postconditions:* ∃ a, b, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w
