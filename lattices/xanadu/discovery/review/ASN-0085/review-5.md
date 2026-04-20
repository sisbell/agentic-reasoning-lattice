# Review of ASN-0085

## REVISE

### Issue 1: OrdAddHom postcondition (c) invokes vpos outside its declared domain
**ASN-0085, OrdAddHom postconditions**: "(c) Full decomposition: v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord) — by (b) and (a), v ⊕ w has subspace subspace(v) and ordinal ord(v) ⊕ w_ord; by the inverse property vpos(subspace(v), ord(v)) = v (vpos contract (b)), reconstruction from these components recovers the result."

**Problem**: vpos is defined with the precondition `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`, restricting its domain to ordinals in S. Postcondition (c) applies vpos to `ord(v) ⊕ w_ord`, which may lie outside S — Instance (b) demonstrates exactly this: `ord(v) ⊕ w_ord = [7, 0]`, and `vpos(1, [7, 0])` is ill-formed under the declared contract since `o₂ = 0`. The justification compounds the error by citing "the inverse property vpos(subspace(v), ord(v)) = v (vpos contract (b))" — that inverse is for `v`, which satisfies S8a, but the claim needs the inverse for `v ⊕ w`, which may not.

The underlying sequence identity — prepending `x₁` to `[x₂, ..., xₘ]` recovers `x` — is trivially true for any `x ∈ T` with `#x ≥ 2`, regardless of S8a. But neither vpos's contract nor any other stated result establishes this general fact.

**Required**: Generalize vpos's precondition to accept any `o ∈ T` with `#o ≥ 1`, and make the S8a guarantee a conditional postcondition: "When `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`, the result satisfies S8a." The definition `vpos(S, o) = [S, o₁, ..., oₖ]` and the inverse properties are pure sequence operations that do not depend on component positivity. Then postcondition (c) follows from the generalized inverse, and Instance (b) becomes a well-typed demonstration of a result outside S8a — which is exactly the pedagogical role it plays.

VERDICT: REVISE
