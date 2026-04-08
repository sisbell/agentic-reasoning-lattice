**Definition (Divergence).** For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`. In case (i), `a` and `b` differ at a component both possess. In case (ii), they agree on all shared positions but one is longer — the divergence lies "just past" the shorter tumbler's last component.

For prefix-related pairs, `divergence(a, b) = min(#a, #b) + 1 > min(#a, #b)`. Since TA0 requires `k ≤ min(#a, #b)`, the condition `k ≥ divergence(a, b)` in TA1-strict below is unsatisfiable for prefix-related operands. This is correct: when `a` is a proper prefix of `b` (or vice versa), Case 1 of the verification below shows that addition erases the divergence, producing equality rather than strict inequality. TA1-strict makes no claim about prefix-related pairs — TA1 (weak) covers them, guaranteeing non-reversal.

*Formal Contract:*
- *Definition:* For `a, b ∈ T` with `a ≠ b`: (i) if `∃ k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`; (ii) if `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`. Exactly one case applies.
