Reading the full ASN against the foundation statements now.

Tracing through each claim: S0's lower-bound and upper-bound derivations both explicitly walk the ≤-abbreviation cases before composing with T1's strict transitivity. S11d's inline containment derivation for the SC(iv)-reverse case does the same — it spells out the four-case split for the lower bound and the two-case split for the upper bound, citing T1(c) and substitution of equals explicitly. The pattern is established twice in this ASN. SC and S11c then use the same compositional steps, but abbreviate them.

### SC case (iv) containment: mixed transitivity chain not walked
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) — exports strict transitivity postcondition (c) and the abbreviation `a ≤ b ≡ a < b ∨ a = b`; ≤-transitivity and the mixed `< + ≤ → <` composition are not T1 exports and must be derived.
**ASN**: SC (SpanClassification), overlap-and-disjointness proof, case (iv) with α the larger span: "every q ∈ ⟦β⟧ satisfies `start(α) ≤ start(β) ≤ q < reach(β) ≤ reach(α)`, so `⟦β⟧ ⊆ ⟦α⟧`"
**Issue**: Placing q ∈ ⟦α⟧ requires (a) `start(α) ≤ q` from `start(α) ≤ start(β)` and `start(β) ≤ q` (≤ + ≤ → ≤), and (b) `q < reach(α)` from `q < reach(β)` and `reach(β) ≤ reach(α)` (< + ≤ → <). Neither composition is a T1 export; each requires unfolding the ≤ abbreviation and case analysis — exactly what S0's lower-bound and upper-bound derivations do explicitly and what S11d's inline SC(iv)-reverse proof reproduces in full. SC asserts the chain in one line without walking either case split.
**What needs resolving**: The proof must derive `start(α) ≤ q` and `q < reach(α)` by case analysis on the ≤ abbreviation before concluding `⟦β⟧ ⊆ ⟦α⟧`, using the same four-case / two-case structure S0 and S11d's inline derivation exhibit.

---

### S11c Case 2 ⊆ direction: ⟦β⟧-membership asserted without deriving the lower bound
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) — same as above; `< + ≤ → ≤` composition requires case analysis, not a direct citation of T1.
**ASN**: S11c (DifferenceOverlap), Case 2 element-chase, ⊆ direction: "if `t < reach(β)`, then `start(β) < start(α) ≤ t < reach(β)`, so `t ∈ ⟦β⟧`"
**Issue**: Membership `t ∈ ⟦β⟧` requires `start(β) ≤ t` (lower bound) and `t < reach(β)` (given in this branch). The proof writes the chain `start(β) < start(α) ≤ t` and asserts `start(β) ≤ t` without deriving it. The step needs: unfold `start(α) ≤ t` as `(start(α) < t) ∨ (start(α) = t)`; in the strict sub-case apply T1(c) to `start(β) < start(α) < t` to get `start(β) < t`; in the equality sub-case substitute `start(α) = t` into `start(β) < start(α)` to get `start(β) < t`; fold back via the ≤ abbreviation. The ⊇ direction of the same Case 2 at least acknowledges T1 for the analogous step ("composes transitively (T1)"), though it too stops short of the full case walk; the ⊆ direction provides neither citation nor derivation.
**What needs resolving**: The ⊆ direction must derive `start(β) ≤ t` from `start(β) < start(α) ≤ t` by case-splitting on the ≤ abbreviation and applying T1(c) or substitution of equals in each branch before asserting `t ∈ ⟦β⟧`.

VERDICT: REVISE