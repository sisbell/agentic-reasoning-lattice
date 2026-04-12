## V-position ordinal decomposition

S8a establishes V-positions as element-field tumblers whose first component is the subspace identifier (subspace(v) = v₁), and the ordinal-only formulation of TA7a (ASN-0034) establishes that within-subspace arithmetic passes only the ordinal to the operations while holding the subspace identifier as structural context. We now formalize this decomposition with concrete extraction and reconstruction functions: separating a V-position into its subspace identifier and its within-subspace ordinal, reconstructing a V-position from these components, and projecting a displacement onto its ordinal component. We then establish the central property: tumbler addition commutes with the decomposition, and derive from this that TA7a's closure guarantees on S govern the S-membership of the result.

**ord(v)** — *OrdinalExtraction* (DEF, function). For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier. When v satisfies S8a, every component of v is positive, so every component of [v₂, ..., vₘ] is positive — placing ord(v) in TA7a's domain S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v ≥ 2`.
- *Definition:* `ord(v) = [v₂, ..., vₘ]` where `m = #v`.
- *Postconditions:* `ord(v) ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#ord(v) = #v - 1`. When `v` satisfies S8a (`zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0`), `ord(v) ∈ S` — every component of `[v₂, ..., vₘ]` is positive since every component of `v` is positive by S8a.
- *Frame:* Pure function on the component sequence of `v` — no state is read or modified.

**vpos(S, o)** — *VPositionReconstruction* (DEF, function). For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with #vpos(S, o) = k + 1. These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

*Formal Contract:*
- *Preconditions:* `S ∈ ℕ`, `o ∈ T`, `#o ≥ 1`.
- *Definition:* `vpos(S, o) = [S, o₁, ..., oₖ]` where `k = #o`.
- *Postconditions:* `vpos(S, o) ∈ T`, `#vpos(S, o) = #o + 1`, `vpos(S, o)₁ = S`. (a) `ord(vpos(S, o)) = o` — since `vpos(S, o) = [S, o₁, ..., oₖ]`, stripping the first component recovers `[o₁, ..., oₖ] = o`. (b) For any `v ∈ T` with `#v ≥ 2`: `vpos(subspace(v), ord(v)) = v` — since `subspace(v) = v₁` and `ord(v) = [v₂, ..., vₘ]`, reconstruction gives `[v₁, v₂, ..., vₘ] = v`. Both inverse properties are pure sequence identities that hold unconditionally on T. When `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`, the result satisfies S8a: `zeros(vpos(S, o)) = 0` (S ≥ 1 and each oᵢ > 0, so no component is zero) and `vpos(S, o) > 0`.
- *Frame:* Pure function on `S` and the component sequence of `o` — no state is read or modified.

**w_ord** — *OrdinalDisplacementProjection* (DEF, function). For a displacement w with `w₁ = 0` and `#w = m ≥ 2`, the *ordinal projection* is:

`w_ord = [w₂, ..., wₘ]`

of length m − 1. The condition `w₁ = 0` is structurally necessary: it ensures `actionPoint(w) ≥ 2`, so by TumblerAdd all positions before the action point are copied from the operand — position 1 (the subspace identifier) is preserved by any addition `v ⊕ w`. This is the mechanism by which arithmetic stays within a subspace. At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c].

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `#w ≥ 2`, `w₁ = 0`.
- *Definition:* `w_ord = [w₂, ..., wₘ]` where `m = #w`.
- *Postconditions:* `w_ord ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#w_ord = #w - 1`. When `w > 0`, `w_ord > 0` — since `w₁ = 0`, positivity of `w` requires some `wᵢ > 0` with `i ≥ 2`, which appears in `w_ord`. When `w > 0`: `actionPoint(w_ord) = actionPoint(w) - 1`.
- *Frame:* Pure function on the component sequence of `w` — no state is read or modified.

The definitions above decompose V-positions into subspace context and ordinal operand. We now establish that the decomposition is structure-preserving: tumbler addition commutes with extraction. This is the property that makes the definitions more than naming conventions — it connects V-position arithmetic to TA7a's closure guarantees on S.

**OrdAddHom** — *OrdinalAdditionHomomorphism* (LEMMA). For a V-position `v` with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `w > 0`, and `actionPoint(w) ≤ m`:

`ord(v ⊕ w) = ord(v) ⊕ w_ord`

*Proof.* Let `k = actionPoint(w)`. Since `w₁ = 0`, we have `k ≥ 2`. By TumblerAdd, the result `r = v ⊕ w` is built component-wise in three regions:

- For `1 ≤ i < k`: `rᵢ = vᵢ` (copy from start).
- At `i = k`: `rₖ = vₖ + wₖ` (single-component advance).
- For `k < i ≤ m`: `rᵢ = wᵢ` (copy from displacement).

So `ord(v ⊕ w) = [r₂, ..., rₘ] = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`.

For the right-hand side, `w_ord = [w₂, ..., wₘ]` has `actionPoint(w_ord) = k - 1`, since `(w_ord)ⱼ = w_{j+1}` and the first nonzero `w_{j+1}` occurs at `j + 1 = k`, i.e. `j = k - 1`. The application is well-defined: `actionPoint(w_ord) = k − 1 ≤ m − 1 = #ord(v)`, since `k ≤ m` by precondition. By TumblerAdd for `ord(v) ⊕ w_ord`:

- For `1 ≤ j < k-1`: `(ord(v) ⊕ w_ord)ⱼ = ord(v)ⱼ = v_{j+1}`.
- At `j = k-1`: `(ord(v) ⊕ w_ord)_{k-1} = ord(v)_{k-1} + (w_ord)_{k-1} = vₖ + wₖ`.
- For `k-1 < j ≤ m-1`: `(ord(v) ⊕ w_ord)ⱼ = (w_ord)ⱼ = w_{j+1}`.

So `ord(v) ⊕ w_ord = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`.

The two sequences are identical component by component. ∎

*Instance (a).* Let `v = [1, 3, 5]`, `w = [0, 0, 2]` (action point 3). Then `v ⊕ w = [1, 3, 7]` and `ord([1, 3, 7]) = [3, 7]`. On the right, `ord(v) = [3, 5]` and `w_ord = [0, 2]`, giving `[3, 5] ⊕ [0, 2] = [3, 7]`. Both sides agree.

*Instance (b).* Let `v = [1, 3, 5]`, `w = [0, 4, 0]` (action point 2). Then `v ⊕ w = [1, 7, 0]` and `ord([1, 7, 0]) = [7, 0]`. On the right, `ord(v) = [3, 5]` and `w_ord = [4, 0]`, giving `[3, 5] ⊕ [4, 0] = [7, 0]`. Both sides agree. Note that `[7, 0] ∉ S` — the zero in the tail component after the action point places the result outside TA7a's domain S, illustrating the S-membership boundary.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`; `w ∈ T`, `w > 0`, `#w = m`, `w₁ = 0`, `actionPoint(w) ≤ m`.
- *Postconditions:* (a) `ord(v ⊕ w) = ord(v) ⊕ w_ord`. (b) `subspace(v ⊕ w) = subspace(v)` — since `k ≥ 2`, TumblerAdd copies `r₁ = v₁` from the start, preserving the subspace identifier. (c) Full decomposition: `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)` — let `r = v ⊕ w`; by TA0 `#r = #w = m ≥ 2`, so the generalized inverse (vpos contract (b)) applies to `r`: `vpos(subspace(r), ord(r)) = r`; substituting `subspace(r) = subspace(v)` from (b) and `ord(r) = ord(v) ⊕ w_ord` from (a) yields the result. Note that `ord(v) ⊕ w_ord` need not lie in S — the definition and inverse properties of vpos are pure sequence operations that hold for any `o ∈ T`.
- *Frame:* Both sides are computed from `v` and `w` alone — no state is consulted.

**OrdAddS8a** — *AdditionPreservesS8a* (LEMMA). For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `w > 0`, and `actionPoint(w) ≤ m`: `v ⊕ w` satisfies S8a if and only if all components of `w_ord` after its action point are positive.

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

**OrdShiftHom** — *OrdinalShiftHomomorphism* (COROLLARY). For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

`ord(shift(v, n)) = shift(ord(v), n)`

Since `shift(v, n) = v ⊕ δ(n, m)` and `δ(n, m) = [0, ..., 0, n]` has `δ(n, m)₁ = 0`, OrdAddHom applies. The ordinal projection `(δ(n, m))_ord = [0, ..., 0, n]` of length `m - 1` is `δ(n, m-1)`. So `ord(v ⊕ δ(n, m)) = ord(v) ⊕ δ(n, m-1) = shift(ord(v), n)`. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.
- *Postconditions:* `ord(shift(v, n)) = shift(ord(v), n)`. When `v` satisfies S8a, OrdAddS8a applies; since `δ(n, m) = [0, ..., 0, n]` has action point `m`, there are no tail components after the action point — the OrdAddS8a condition is vacuously satisfied. Therefore `shift(v, n)` unconditionally satisfies S8a when `v` does.
