**S7c (Element-field depth).** Every content address has an element field of depth at least 2:

`(A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)`

This is a design requirement ensuring that the subspace identifier `E₁` and the content ordinal `[E₂, ..., E_δ]` occupy distinct components. Without it, `δ = 1` is formally permitted by T4 and S7b — `inc(document_address, 2)` under T10a produces an element-level address with a single-component element field `[E₁]`. At `δ = 1`, the subspace identifier IS the content ordinal: ordinal shifts change the subspace, and TA7a's ordinal-only formulation cannot be applied (removing the subspace identifier leaves an empty sequence, not a valid tumbler). At `δ ≥ 2`, the subspace identifier is structural context outside the ordinal, and shifts act only within the subspace. Gregory's evidence confirms `δ = 2` as the standard allocation pattern: the element field is `[S, x]` where `S` is the subspace identifier and `x` is the content ordinal.

With S7a and S7b established, we can state structural attribution. (S7c, stated here for architectural completeness, is load-bearing for S8-depth's ordinal shift analysis below, not for S7 itself.)

*Formal Contract:*
- *Axiom:* (A a ∈ dom(Σ.C) :: #fields(a).element ≥ 2)
- *Preconditions:* `zeros(a) = 3` for all `a ∈ dom(Σ.C)` — T4's field correspondence requires `zeros(a) = 3` for the element field to exist and `#fields(a).element` to be well-defined. (Entailed by S7b.)
