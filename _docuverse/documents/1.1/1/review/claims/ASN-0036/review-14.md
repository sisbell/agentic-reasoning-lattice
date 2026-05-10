# Formalize — ASN-0036 / vpos(S, o)

*2026-04-12 14:43*

**vpos(S, o)** — *VPositionReconstruction* (DEF, function). For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with #vpos(S, o) = k + 1. These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

*Proof.* We verify that the definition is well-formed, then establish each stated property — the length, the inverse laws, and the connection to S8a.

The construction prepends the natural number S to the component sequence of tumbler o = [o₁, ..., oₖ]. Since o ∈ T with k = #o ≥ 1, the result [S, o₁, ..., oₖ] is a finite sequence of k + 1 natural numbers — hence an element of T with #vpos(S, o) = k + 1 = #o + 1. The first component vpos(S, o)₁ = S by construction.

*Inverse (a): ord(vpos(S, o)) = o.* By definition, vpos(S, o) = [S, o₁, ..., oₖ]. The function ord strips the first component (the subspace identifier), yielding [o₁, ..., oₖ]. This sequence is o itself, so ord(vpos(S, o)) = o. The identity holds unconditionally on T for any S ∈ ℕ and o ∈ T with #o ≥ 1.

*Inverse (b): vpos(subspace(v), ord(v)) = v for any v ∈ T with #v ≥ 2.* Let v = [v₁, v₂, ..., vₘ] with m = #v ≥ 2. Then subspace(v) = v₁ and ord(v) = [v₂, ..., vₘ]. The ordinal ord(v) has #ord(v) = m − 1 ≥ 1 components, satisfying the precondition #o ≥ 1 required by vpos. Applying the definition: vpos(v₁, [v₂, ..., vₘ]) = [v₁, v₂, ..., vₘ] = v. This identity holds unconditionally on T for any v with #v ≥ 2.

*S8a preservation.* When S ≥ 1 and every component of o is strictly positive — that is, (A i : 1 ≤ i ≤ k : oᵢ > 0) — the result vpos(S, o) = [S, o₁, ..., oₖ] has every component strictly positive. No component is zero, so zeros(vpos(S, o)) = 0. Since S ≥ 1 entails the first component is at least 1, and all remaining components exceed zero, vpos(S, o) > 0. Both conjuncts of S8a (V-position well-formedness) are therefore satisfied. ∎

*Formal Contract:*
- *Preconditions:* `S ∈ ℕ`, `o ∈ T`, `#o ≥ 1`.
- *Definition:* `vpos(S, o) = [S, o₁, ..., oₖ]` where `k = #o`.
- *Postconditions:* `vpos(S, o) ∈ T`, `#vpos(S, o) = #o + 1`, `vpos(S, o)₁ = S`. (a) `ord(vpos(S, o)) = o`. (b) For any `v ∈ T` with `#v ≥ 2`: `vpos(subspace(v), ord(v)) = v`. When `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`: `zeros(vpos(S, o)) = 0 ∧ vpos(S, o) > 0` (S8a, V-position well-formedness).
- *Frame:* Pure function on `S` and the component sequence of `o` — no state is read or modified.
