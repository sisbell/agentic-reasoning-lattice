**Definition (Divergence).** For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`. Mutual exclusivity is immediate: if case (i) holds, some `aₖ ≠ bₖ` within shared positions falsifies case (ii)'s universal agreement. For exhaustiveness, suppose neither case applies — all shared components agree and `#a = #b`. Then by T3, `a = b`, contradicting `a ≠ b`. In case (i), `a` and `b` differ at a component both possess. In case (ii), they agree on all shared positions but one is longer — the divergence lies "just past" the shorter tumbler's last component.

For prefix-related pairs, `divergence(a, b) = min(#a, #b) + 1 > min(#a, #b)`. TA1-strict requires both `actionPoint(w) ≤ min(#a, #b)` — combining TA0's single-operand precondition `actionPoint(w) ≤ #a` applied to each operand — and `actionPoint(w) ≥ divergence(a, b)`. For prefix-related operands these constraints are jointly unsatisfiable: the action point cannot simultaneously lie within both tumblers and reach past the shorter one's last component. TA1-strict therefore makes no claim about prefix-related pairs. TA1 covers them, showing that both results become equal and order is preserved as non-reversal.

*Formal Contract:*
- *Definition:* For `a, b ∈ T` with `a ≠ b`: (i) if `∃ k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`; (ii) if `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1`. Exactly one case applies (exhaustiveness by T3: if neither case holds, `a = b`).
- *Depends:* T3 (CanonicalRepresentation) — exhaustiveness: if neither case (i) nor case (ii) applies, all shared components agree and `#a = #b`, whence T3 yields `a = b`, contradicting `a ≠ b`.
