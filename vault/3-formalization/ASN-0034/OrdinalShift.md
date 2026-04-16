**OrdinalShift (OrdinalShift).** For a tumbler v ∈ T of length m = #v and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

We verify the four preconditions of TA0 for this application. First, v ∈ T by assumption. Second, by OrdinalDisplacement, δ(n, m) = [0, …, 0, n] is a finite sequence of length m ≥ 1 over ℕ, so by T0, δ(n, m) ∈ T. Third, since n ≥ 1 the m-th component of δ(n, m) is nonzero, whence by PositiveTumbler Pos(δ(n, m)). Fourth, the action point of δ(n, m) is m = #v by OrdinalDisplacement, so actionPoint(δ(n, m)) ≤ #v holds trivially.

With all TA0 preconditions satisfied, shift(v, n) = v ⊕ δ(n, m) ∈ T. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n, and #shift(v, n) = #δ(n, m) = m = #v. The shift advances the deepest component by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n] changes the first component. Since n ≥ 1, component positivity holds unconditionally: shift(v, n)ₘ = vₘ + n ≥ 1 for all vₘ ≥ 0. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
- *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v, shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n ≥ 1
