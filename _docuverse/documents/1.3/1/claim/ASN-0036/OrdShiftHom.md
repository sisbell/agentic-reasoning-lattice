**OrdShiftHom** — *OrdinalShiftPreservation* (LEMMA). For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

(a) `subspace(shift(v, n)) = subspace(v)`.

(b) When `v` satisfies S8a, `shift(v, n)` satisfies S8a.

*Proof.* Write `shift(v, n) = v ⊕ δ(n, m)` with `δ(n, m) = [0, ..., 0, n]` of length `m` (OrdinalShift, OrdinalDisplacement, ASN-0034). By OrdinalDisplacement, `actionPoint(δ(n, m)) = m`, so the addition is well-defined since `actionPoint(δ(n, m)) = m ≤ #v`. By TumblerAdd, the result `r = v ⊕ δ(n, m)` is built component-wise: for `1 ≤ i < m`, `rᵢ = vᵢ` (these positions precede the action point and are copied from `v`); at `i = m`, `rₘ = vₘ + n`. There are no positions beyond the action point, and `#r = m` (TA0, ASN-0034).

*Part (a).* Since `m ≥ 2`, position 1 lies in the copy-from-`v` region, so `r₁ = v₁`. By definition `subspace(r) = r₁ = v₁ = subspace(v)`.

*Part (b).* Assume `v` satisfies S8a: `zeros(v) = 0`, `#v = m ≥ 2`, and `vᵢ ≥ 1` for every `i`. For `1 ≤ i < m`, `rᵢ = vᵢ ≥ 1`; at `i = m`, `rₘ = vₘ + n ≥ 1 + 1 > 0`. Every component of `r` is positive, so `zeros(r) = 0` and `(A i : 1 ≤ i ≤ #r : rᵢ > 0)`, with `#r = m ≥ 2`. Hence `shift(v, n)` satisfies S8a. ∎

*Instance.* Let `v = [1, 3, 5]` (text subspace `v₁ = 1`, depth `m = 3`, satisfying S8a) and `n = 2`. Then `shift(v, 2) = v ⊕ δ(2, 3) = [1, 3, 5] ⊕ [0, 0, 2] = [1, 3, 7]` (action point 3; components 1 and 2 copied from `v`, component 3 receives `5 + 2 = 7`). (a) `subspace(shift(v, 2)) = [1, 3, 7]₁ = 1 = v₁ = subspace(v)`. (b) `[1, 3, 7]` has `zeros = 0`, every component positive (`1, 3, 7 ≥ 1`), and depth `3 ≥ 2`, so S8a holds on `shift(v, 2)`.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.
- *Postconditions:* (a) `subspace(shift(v, n)) = subspace(v)`. (b) When `v` satisfies S8a, `shift(v, n)` satisfies S8a.
- *Depends:* OrdinalShift (ASN-0034) — `shift(v, n) = v ⊕ δ(n, m)`; OrdinalDisplacement (ASN-0034) — `δ(n, m) = [0, ..., 0, n]` with action point `m`; TumblerAdd (ASN-0034) — the component formula copying positions before the action point; TA0 (length preservation, ASN-0034) — `#shift(v, n) = m`; S8a (V-position well-formedness) — supplies `vᵢ ≥ 1` for part (b).

- *Depends:*
  - OrdinalShift (ASN-0034) — supplies the definition `shift(v, n) = v ⊕ δ(n, m)` that the proof writes out in its opening step
  - OrdinalDisplacement (ASN-0034) — supplies `δ(n, m) = [0, ..., 0, n]` with `actionPoint(δ(n, m)) = m`, used to establish well-definedness of the addition
  - TumblerAdd (ASN-0034) — supplies the component-wise addition formula that justifies the copy/increment split at the action point
  - TA0 (ASN-0034) — supplies length preservation `#shift(v, n) = m`, used in both parts of the proof
  - S8a (V-position well-formedness) — supplies `vᵢ ≥ 1` for every `i`, the premise that part (b) directly consumes