# Formalize — ASN-0036 / OrdShiftHom

*2026-04-12 15:58*

**OrdShiftHom** — *OrdinalShiftHomomorphism* (COROLLARY). For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

`ord(shift(v, n)) = shift(ord(v), n)`

Since `shift(v, n) = v ⊕ δ(n, m)` and `δ(n, m) = [0, ..., 0, n]` is a tumbler of length `m` with zeros in positions `1` through `m - 1` and `n` in position `m`, we verify OrdAddHom's preconditions: `δ(n, m)₁ = 0`; `δ(n, m) > 0` because `n ≥ 1` makes the last component positive; `#δ(n, m) = m`; and `actionPoint(δ(n, m)) = m ≤ m`, since position `m` is the first nonzero component. OrdAddHom applies, giving `ord(v ⊕ δ(n, m)) = ord(v) ⊕ (δ(n, m))_ord`.

The ordinal projection `(δ(n, m))_ord = [δ(n, m)₂, ..., δ(n, m)_m] = [0, ..., 0, n]` of length `m - 1` is `δ(n, m-1)`. Since `#ord(v) = m - 1`, the definition of shift gives `shift(ord(v), n) = ord(v) ⊕ δ(n, m-1)`. So `ord(v ⊕ δ(n, m)) = ord(v) ⊕ δ(n, m-1) = shift(ord(v), n)`.

For S8a preservation: since `actionPoint(δ(n, m)) = m`, the tail region after the action point (positions `k < i ≤ m` with `k = m`) is empty. By OrdAddS8a, the condition for `v ⊕ δ(n, m)` to satisfy S8a reduces to a vacuously true universal quantification over this empty range. Therefore `shift(v, n)` unconditionally satisfies S8a when `v` does. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.
- *Postconditions:* (a) `ord(shift(v, n)) = shift(ord(v), n)`. (b) If `v` satisfies S8a, then `shift(v, n)` satisfies S8a — by OrdAddS8a with `w = δ(n, m)`, `actionPoint(w) = m`, so the tail region `(k, m]` is empty and the positivity condition holds vacuously.
