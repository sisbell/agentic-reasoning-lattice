# Claim Formal Contract — ASN-0036/OrdShiftHom — run 1

*2026-06-25T18:31:25Z*
*Model: opus*
*Cycles: 1*
*Validation: MATCH*

## Validation detail

(no detail)

## Review-rewrite detail

(passed)

## Final LLM response

**OrdShiftHom (OrdinalShiftPreservation).** For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

(a) `subspace(shift(v, n)) = subspace(v)`.

(b) When `v` satisfies S8a, `shift(v, n)` satisfies S8a.

*Proof.* Write `shift(v, n) = v ⊕ δ(n, m)` with `δ(n, m) = [0, ..., 0, n]` of length `m` (OrdinalShift, OrdinalDisplacement, ASN-0034). By OrdinalDisplacement, `actionPoint(δ(n, m)) = m`, so the addition is well-defined since `actionPoint(δ(n, m)) = m ≤ #v`. By TumblerAdd, the result `r = v ⊕ δ(n, m)` is built component-wise: for `1 ≤ i < m`, `rᵢ = vᵢ` (these positions precede the action point and are copied from `v`); at `i = m`, `rₘ = vₘ + n`. There are no positions beyond the action point, and `#r = m` (TA0, ASN-0034).

*Part (a).* Since `m ≥ 2`, position 1 lies in the copy-from-`v` region, so `r₁ = v₁`. By definition `subspace(r) = r₁ = v₁ = subspace(v)`.

*Part (b).* Assume `v` satisfies S8a: `zeros(v) = 0`, `#v = m ≥ 2`, and `vᵢ ≥ 1` for every `i`. For `1 ≤ i < m`, `rᵢ = vᵢ ≥ 1`; at `i = m`, `rₘ = vₘ + n ≥ 1 + 1 > 0`. Every component of `r` is positive, so `zeros(r) = 0` and `(A i : 1 ≤ i ≤ #r : rᵢ > 0)`, with `#r = m ≥ 2`. Hence `shift(v, n)` satisfies S8a. ∎

*Instance.* Let `v = [1, 3, 5]` (text subspace `v₁ = 1`, depth `m = 3`, satisfying S8a) and `n = 2`. Then `shift(v, 2) = v ⊕ δ(2, 3) = [1, 3, 5] ⊕ [0, 0, 2] = [1, 3, 7]` (action point 3; components 1 and 2 copied from `v`, component 3 receives `5 + 2 = 7`). (a) `subspace(shift(v, 2)) = [1, 3, 7]₁ = 1 = v₁ = subspace(v)`. (b) `[1, 3, 7]` has `zeros = 0`, every component positive (`1, 3, 7 ≥ 1`), and depth `3 ≥ 2`, so S8a holds on `shift(v, 2)`.

*Formal Contract:*

- *Preconditions:* `v` is a V-position with `#v = m ≥ 2`; `n ≥ 1`. For part (b), additionally `v` satisfies S8a (`zeros(v) = 0` and `vᵢ ≥ 1` for every `i`).
- *Postconditions:* (a) `subspace(shift(v, n)) = subspace(v)`. (b) If `v` satisfies S8a, then `shift(v, n)` satisfies S8a.
- *Frame:* `#shift(v, n) = #v = m` (depth preserved); for every `1 ≤ i < m` the component is copied unchanged (`rᵢ = vᵢ`), in particular the text subspace `r₁ = v₁` is preserved; only the action-point component changes (`rₘ = vₘ + n`).
- *Definition:* `shift(v, n) = v ⊕ δ(n, m)`, where `δ(n, m) = [0, ..., 0, n]` is the ordinal displacement of length `m` with `actionPoint(δ(n, m)) = m` (OrdinalShift, OrdinalDisplacement).
