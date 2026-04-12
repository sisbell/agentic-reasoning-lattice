**OrdShiftHom** — *OrdinalShiftHomomorphism* (COROLLARY). For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

`ord(shift(v, n)) = shift(ord(v), n)`

Since `shift(v, n) = v ⊕ δ(n, m)` and `δ(n, m) = [0, ..., 0, n]` has `δ(n, m)₁ = 0`, OrdAddHom applies. The ordinal projection `(δ(n, m))_ord = [0, ..., 0, n]` of length `m - 1` is `δ(n, m-1)`. So `ord(v ⊕ δ(n, m)) = ord(v) ⊕ δ(n, m-1) = shift(ord(v), n)`. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.
- *Postconditions:* `ord(shift(v, n)) = shift(ord(v), n)`. When `v` satisfies S8a, OrdAddS8a applies; since `δ(n, m) = [0, ..., 0, n]` has action point `m`, there are no tail components after the action point — the OrdAddS8a condition is vacuously satisfied. Therefore `shift(v, n)` unconditionally satisfies S8a when `v` does.
