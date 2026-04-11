# ASN-0085: V-Position Ordinal Decomposition

*2026-04-11*

The strand model (ASN-0036) defines V-positions as element-field tumblers whose first component is the subspace identifier (subspace(v) = v₁), and the ordinal-only formulation of TA7a (ASN-0034) establishes that within-subspace arithmetic passes only the ordinal to the operations while holding the subspace identifier as structural context. This ASN extends the strand model with the concrete extraction and reconstruction functions that formalize this decomposition: separating a V-position into its subspace identifier and its within-subspace ordinal, reconstructing a V-position from these components, and projecting a displacement onto its ordinal component. We then establish the central property: tumbler addition commutes with the decomposition, connecting these definitions to TA7a's closure guarantees on S.


## Ordinal Extraction

We frequently need to separate a V-position into its subspace identifier and its ordinal within that subspace. Per the ordinal-only formulation of TA7a (ASN-0034), we define the extraction and reconstruction functions.

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
- *Preconditions:* `S ≥ 1`, `o ∈ T`, `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`.
- *Definition:* `vpos(S, o) = [S, o₁, ..., oₖ]` where `k = #o`.
- *Postconditions:* `vpos(S, o) ∈ T`, `#vpos(S, o) = #o + 1`, `vpos(S, o)₁ = S`. The result satisfies S8a: `zeros(vpos(S, o)) = 0` (S ≥ 1 and each oᵢ > 0, so no component is zero) and `vpos(S, o) > 0`.
- *Frame:* Pure function on `S` and the component sequence of `o` — no state is read or modified.

**w_ord** — *OrdinalDisplacementProjection* (DEF, function). For a displacement w with `w₁ = 0` and `#w = m ≥ 2`, the *ordinal projection* is:

`w_ord = [w₂, ..., wₘ]`

of length m − 1. The condition `w₁ = 0` is structurally necessary: it ensures `actionPoint(w) ≥ 2`, so by TumblerAdd all positions before the action point are copied from the operand — position 1 (the subspace identifier) is preserved by any addition `v ⊕ w`. This is the mechanism by which arithmetic stays within a subspace. At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c].

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `#w ≥ 2`, `w₁ = 0`.
- *Definition:* `w_ord = [w₂, ..., wₘ]` where `m = #w`.
- *Postconditions:* `w_ord ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#w_ord = #w - 1`. When `w > 0`, `w_ord > 0` — since `w₁ = 0`, positivity of `w` requires some `wᵢ > 0` with `i ≥ 2`, which appears in `w_ord`. `actionPoint(w_ord) = actionPoint(w) - 1`.
- *Frame:* Pure function on the component sequence of `w` — no state is read or modified.


## Arithmetic Homomorphism

The definitions above decompose V-positions into subspace context and ordinal operand. We now establish that the decomposition is structure-preserving: tumbler addition commutes with extraction. This is the property that makes the definitions more than naming conventions — it connects V-position arithmetic to TA7a's closure guarantees on S.

**OrdAddHom** — *OrdinalAdditionHomomorphism* (LEMMA). For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `w > 0`, and `actionPoint(w) ≤ m`:

`ord(v ⊕ w) = ord(v) ⊕ w_ord`

*Proof.* Let `k = actionPoint(w)`. Since `w₁ = 0`, we have `k ≥ 2`. By TumblerAdd, the result `r = v ⊕ w` is built component-wise in three regions:

- For `1 ≤ i < k`: `rᵢ = vᵢ` (copy from start).
- At `i = k`: `rₖ = vₖ + wₖ` (single-component advance).
- For `k < i ≤ m`: `rᵢ = wᵢ` (copy from displacement).

So `ord(v ⊕ w) = [r₂, ..., rₘ] = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`.

For the right-hand side, `w_ord = [w₂, ..., wₘ]` has `actionPoint(w_ord) = k - 1`, since `(w_ord)ⱼ = w_{j+1}` and the first nonzero `w_{j+1}` occurs at `j + 1 = k`, i.e. `j = k - 1`. By TumblerAdd for `ord(v) ⊕ w_ord`:

- For `1 ≤ j < k-1`: `(ord(v) ⊕ w_ord)ⱼ = ord(v)ⱼ = v_{j+1}`.
- At `j = k-1`: `(ord(v) ⊕ w_ord)_{k-1} = ord(v)_{k-1} + (w_ord)_{k-1} = vₖ + wₖ`.
- For `k-1 < j ≤ m-1`: `(ord(v) ⊕ w_ord)ⱼ = (w_ord)ⱼ = w_{j+1}`.

So `ord(v) ⊕ w_ord = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`.

The two sequences are identical component by component. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `w > 0`, `#w = m`, `w₁ = 0`, `actionPoint(w) ≤ m`.
- *Postconditions:* `ord(v ⊕ w) = ord(v) ⊕ w_ord`.
- *Frame:* Both sides are computed from `v` and `w` alone — no state is consulted.

**OrdShiftHom** — *OrdinalShiftHomomorphism* (COROLLARY). For a V-position `v` satisfying S8a with `#v = m ≥ 2` and `n ≥ 1`:

`ord(shift(v, n)) = shift(ord(v), n)`

Since `shift(v, n) = v ⊕ δ(n, m)` and `δ(n, m) = [0, ..., 0, n]` has `δ(n, m)₁ = 0`, OrdAddHom applies. The ordinal projection `(δ(n, m))_ord = [0, ..., 0, n]` of length `m - 1` is `δ(n, m-1)`. So `ord(v ⊕ δ(n, m)) = ord(v) ⊕ δ(n, m-1) = shift(ord(v), n)`. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T` satisfying S8a, `#v = m ≥ 2`, `n ≥ 1`.
- *Postconditions:* `ord(shift(v, n)) = shift(ord(v), n)`.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ord(v) | Ordinal extraction: ord(v) = [v₂, ..., vₘ]; when v satisfies S8a, ord(v) ∈ S | introduced |
| vpos(S, o) | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord; result satisfies S8a | introduced |
| w_ord | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for displacement w with w₁ = 0 | introduced |
| OrdAddHom | ord(v ⊕ w) = ord(v) ⊕ w_ord for within-subspace displacements (w₁ = 0) | introduced |
| OrdShiftHom | ord(shift(v, n)) = shift(ord(v), n) | introduced |


## Open Questions

Under what conditions on w does the subtraction homomorphism ord(v ⊖ w) = ord(v) ⊖ w_ord hold, given TA7a's conditional S-membership results for subtraction?

What are the precise conditions for the round-trip property (ord(v) ⊕ w_ord) ⊖ w_ord = ord(v)?
