**OrdinalShift (OrdinalShift).** For a tumbler v ∈ T of length m = #v and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

We verify the four preconditions of TA0 for this application. First, v ∈ T by assumption. Second, by OrdinalDisplacement, δ(n, m) = [0, …, 0, n] is a finite sequence of length m ≥ 1 over ℕ, so by T0, δ(n, m) ∈ T. Third, since n ≥ 1 the m-th component of δ(n, m) is nonzero, whence by TA-Pos Pos(δ(n, m)). Fourth, the action point of δ(n, m) is m = #v by OrdinalDisplacement, so actionPoint(δ(n, m)) ≤ #v holds trivially.

With all TA0 preconditions satisfied, shift(v, n) = v ⊕ δ(n, m) ∈ T. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n, and #shift(v, n) = #δ(n, m) = m = #v. The shift advances the deepest component by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, letting c denote the sole component so that v = [c] with c ∈ ℕ, shift([c], n) = [c + n] changes the first component. Since n ≥ 1, component positivity holds unconditionally: shift(v, n)ₘ = vₘ + n ≥ 1 for all vₘ ≥ 0. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
- *Depends:* OrdinalDisplacement (OrdinalDisplacement) — invoked to construct `δ(n, m)` and supply its three structural facts: that `δ(n, m)` is a finite sequence of length `m ≥ 1` over ℕ, that its `m`-th component is `n ≥ 1`, and that its action point equals `m` ("by OrdinalDisplacement, δ(n, m) = [0, …, 0, n] is a finite sequence of length m ≥ 1 over ℕ … the action point of δ(n, m) is m = #v by OrdinalDisplacement"); each of these is consumed by a separate TA0 precondition check. T0 (CarrierSetDefinition) — invoked to discharge `δ(n, m) ∈ T` from its sequence form and length ("by T0, δ(n, m) ∈ T"). TA-Pos (PositiveTumbler) — invoked to discharge `Pos(δ(n, m))` from the m-th component being nonzero ("whence by TA-Pos Pos(δ(n, m))"). TA0 (WellDefinedAddition) — invoked to discharge `shift(v, n) = v ⊕ δ(n, m) ∈ T` ("With all TA0 preconditions satisfied, shift(v, n) = v ⊕ δ(n, m) ∈ T"); TA0 also supplies the result-length identity used to conclude `#shift(v, n) = #v`. TumblerAdd (TumblerAdd) — invoked to compute the components of the result via the piecewise prefix-copy / advance / tail-copy rule ("By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n, and #shift(v, n) = #δ(n, m) = m = #v"), which yields the postcondition that all components below position `m` are unchanged and position `m` is advanced by `n`.
- *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v, shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n ≥ 1
