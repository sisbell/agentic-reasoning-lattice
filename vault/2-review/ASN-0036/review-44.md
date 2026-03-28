# Proof Verification: S8-depth

RESULT: FOUND

**Problem**: Missing formal contract. The property is explicitly described as "a design requirement, not a convention — parallel to S7a," yet S7a has a formal contract with an `*Axiom:*` field and S8-depth has none. The checklist requires: "If the formal contract is missing or incomplete, flag as FOUND."

Additionally, the property section embeds a definition (correspondence run) that should be formalized in the contract. The formal expression for the correspondence run is given inline:

> `(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

but is never promoted to a `*Definition:*` field.

**Required**: Add a `*Formal Contract:*` section at the end of the property, parallel to S7a's structure. It should include at minimum:

```
*Formal Contract:*
- *Axiom:* (A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)
- *Definition:* A *correspondence run* is a triple (v, a, n) with n ≥ 1 such that (A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k), where v + k and a + k denote ordinal displacement (TA7a) applied to V-positions and I-address element ordinals respectively.
```
