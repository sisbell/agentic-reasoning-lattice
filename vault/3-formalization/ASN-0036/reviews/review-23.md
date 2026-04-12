# Formalize — ASN-0036 / OrdAddS8a

*2026-04-12 15:10*

**OrdAddS8a** — *AdditionPreservesS8a* (LEMMA). For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `w > 0`, and `actionPoint(w) ≤ m`: `v ⊕ w` satisfies S8a if and only if all components of `w_ord` after its action point are positive.

*Proof.* Let `r = v ⊕ w` with `k = actionPoint(w)`. Since `w₁ = 0` and `w > 0`, the first nonzero component of `w` occurs at some position `k ≥ 2`. By TumblerAdd's result-length identity, `#r = #w = m`, so `r` has the same number of components as `v` and `w`. By TumblerAdd, the components of `r` partition into three regions:

- `r₁ = v₁ ≥ 1` (by S8a on `v`, and `1 < k` so TumblerAdd copies from `v`).
- For `2 ≤ i < k`: `rᵢ = vᵢ ≥ 1` (by S8a on `v`).
- At `i = k`: `rₖ = vₖ + wₖ ≥ 1 + 1 = 2` (since `vₖ ≥ 1` by S8a and `wₖ ≥ 1` as the action-point component).
- For `k < i ≤ m`: `rᵢ = wᵢ` (copied from the displacement).

Components `r₁` through `rₖ` are unconditionally positive. S8a requires `zeros(r) = 0`, `r₁ ≥ 1`, and `r > 0`, which together reduce to: every component of `r` is strictly positive. Since the prefix `r₁, ..., rₖ` is established positive, the only components that can fail are `r_{k+1}, ..., r_m = w_{k+1}, ..., w_m` — exactly the tail components of `w`, which are the tail components of `w_ord` (since `(w_ord)_j = w_{j+1}` and the action point of `w_ord` is `k - 1`). When `k = m`, the tail region is empty and the condition holds vacuously. Therefore:

`v ⊕ w satisfies S8a ⟺ (A i : k < i ≤ m : wᵢ > 0) ⟺ all tail components of w_ord are positive`

By OrdAddHom, `ord(v ⊕ w) = ord(v) ⊕ w_ord`, so checking S8a on `v ⊕ w` reduces to checking whether all components of `ord(v) ⊕ w_ord` are positive — the V-position S8a property and the ordinal-domain positivity condition are two views of the same constraint on the displacement's tail. OrdAddHom instance (b) confirms the boundary: `w_ord = [4, 0]` has a zero after the action point, and `v ⊕ w = [1, 7, 0]` fails S8a. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `w > 0`, `#w = m`, `w₁ = 0`, `actionPoint(w) ≤ m`.
- *Postconditions:* `v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, since `r₁ = v₁ ≥ 1` unconditionally and `ord(v ⊕ w) = ord(v) ⊕ w_ord` (OrdAddHom), `v ⊕ w` satisfies S8a if and only if all components of `ord(v) ⊕ w_ord` are positive.
