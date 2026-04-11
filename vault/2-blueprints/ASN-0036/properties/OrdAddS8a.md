**OrdAddS8a (AdditionPreservesS8a).** For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `w > 0`, and `actionPoint(w) ≤ m`: `v ⊕ w` satisfies S8a if and only if all components of `w_ord` after its action point are positive.

*Proof.* Let `r = v ⊕ w` with `k = actionPoint(w) ≥ 2`. By TumblerAdd, the components of `r` partition into three regions:

- `r₁ = v₁ ≥ 1` (by S8a on `v`, and `w₁ = 0` so `1 < k` and TumblerAdd copies from `v`).
- For `2 ≤ i < k`: `rᵢ = vᵢ ≥ 1` (by S8a on `v`).
- At `i = k`: `rₖ = vₖ + wₖ ≥ 1 + 1 = 2` (since `vₖ ≥ 1` by S8a and `wₖ ≥ 1` as the action-point component).
- For `k < i ≤ m`: `rᵢ = wᵢ` (copied from the displacement).

Components `r₁` through `rₖ` are unconditionally positive. S8a requires `zeros(r) = 0` and `r > 0`, which reduces to: every component is positive. The only components that can fail are `r_{k+1}, ..., r_m = w_{k+1}, ..., w_m` — exactly the tail components of `w`, which are the tail components of `w_ord` (since `(w_ord)_j = w_{j+1}` and the action point of `w_ord` is `k - 1`). Therefore:

`v ⊕ w satisfies S8a ⟺ (A i : k < i ≤ m : wᵢ > 0) ⟺ all tail components of w_ord are positive`

By OrdAddHom, `ord(v ⊕ w) = ord(v) ⊕ w_ord`, so equivalently `ord(v ⊕ w) ∈ S` under the same condition — the ordinal-domain S-membership and the V-position S8a property are two views of the same constraint on the displacement's tail. Instance (b) above confirms the boundary: `w_ord = [4, 0]` has a zero after the action point, and `v ⊕ w = [1, 7, 0]` fails S8a. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `w > 0`, `#w = m`, `w₁ = 0`, `actionPoint(w) ≤ m`.
- *Postconditions:* `v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`.
