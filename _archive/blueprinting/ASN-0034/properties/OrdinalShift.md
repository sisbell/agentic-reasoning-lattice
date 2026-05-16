**Definition (OrdinalShift).** For a tumbler v of length m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

TA0 is satisfied: the action point of δ(n, m) is m = #v, so k ≤ #v holds trivially. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the deepest component by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n] changes the first component. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves tumbler depth, and — since n ≥ 1 — component positivity: shift(v, n)ₘ = vₘ + n ≥ 1 unconditionally for all vₘ ≥ 0.
