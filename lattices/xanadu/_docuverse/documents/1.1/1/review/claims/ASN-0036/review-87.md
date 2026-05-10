# Cone Review — ASN-0036/S8-crun (cycle 1)

*2026-04-15 07:57*

Now I have the full picture. Let me trace the specific gap.

From the file reads:

- **S7a** (AllPositiveElement): axiomatizes that every I-address field component is strictly positive — `(A a ∈ dom(Σ.C), i : 1 ≤ i ≤ #a ∧ aᵢ ≠ 0 : aᵢ ≥ 1)`. This establishes the positive-component constraint for dom(Σ.C).
- **S7b**: axiomatizes zeros(a) = 3 for dom(Σ.C).
- **T4b** preconditions: T3, T4 constraints (zeros ≤ 3, positive-component, non-empty field).
- **E₁(a)** preconditions: "a ∈ T with zeros(a) = 3 — T4b requires this for fields(a) to be well-defined."
- **E₁(a)** YAML depends: `[T4, T4b, S7b]` — does NOT include S7a.
- **S7c** preconditions: "zeros(a) = 3 for all a ∈ dom(Σ.C)" — does NOT cite S7a.
- **T4a** (SyntacticEquivalence): non-empty field constraint ⟺ (no adjacent zeros, first component > 0, last component > 0).

The chain I'm checking: for any `a ∈ dom(Σ.C)`, can we invoke T4b to establish `fields(a)` well-definedness?

T4b requires the non-empty field constraint. The non-empty field constraint (by T4a) requires: no adjacent zeros, first component > 0, last component > 0. S7a gives positive non-zero components; S7b gives zeros = 3. Together these give: the 3 zeros are separators, all other components are ≥ 1, hence first component is ≥ 1 (or is a zero separator), last component is ≥ 1 (or is a zero separator).

But wait — can the first or last component of a dom(Σ.C) address be zero? If the first component is zero, it would be one of the three separators. S7a says "aᵢ ≠ 0 ⟹ aᵢ ≥ 1", which is trivially true and doesn't prevent aᵢ = 0. S7b says exactly 3 zeros. So we could have a = [0, 1, 0, 1, 0, 1] with zeros = 3 and all non-zero components ≥ 1. This satisfies S7a and S7b but has an empty first field.

S7a as stated doesn't prevent the counterexample. And neither E₁(a) nor S7c cites S7a anyway. The gap persists.

---

### E₁(a) and S7c invoke T4b with incomplete preconditions — zeros(a) = 3 does not cover T4b's non-empty field requirement, and S7a does not fill the gap

**Foundation**: T4b (UniqueParse, ASN-0034) — Preconditions: `t` satisfies T3 (CanonicalRepresentation); `t` satisfies the T4 constraints (at most three zero-valued components, positive-component constraint, non-empty field constraint). T4a (SyntacticEquivalence, ASN-0034) — non-empty field constraint is equivalent to three syntactic conditions: no adjacent zeros, first component > 0, last component > 0.
**ASN**: E₁(a) body text: "For `a` with `zeros(a) = 3`, T4b (UniqueParse, ASN-0034) establishes that `fields(a)` is well-defined." E₁(a) formal contract preconditions: "`a ∈ T` with `zeros(a) = 3` — T4b requires this for `fields(a)` to be well-defined." E₁(a) body text: "T4a's non-adjacency constraint (invoked by T4b) ensures every field segment is non-empty." E₁(a) YAML depends: `[T4, T4b, S7b]`. S7c formal contract preconditions: "`zeros(a) = 3` for all `a ∈ dom(Σ.C)` — T4's field correspondence requires `zeros(a) = 3` for the element field to exist and `#fields(a).element` to be well-defined."
**Issue**: T4b requires four preconditions; E₁(a) and S7c cite only `zeros(a) = 3`, covering just the at-most-three-zeros condition. The non-empty field constraint is not established. The counterexample `[0, 1, 0, 1, 0, 1] ∈ T` has `zeros = 3` but its first field (before the first zero-valued separator) is empty — T4b cannot be invoked, `fields` as defined by T4b is not established as well-defined, and `fields(a).element₁` may not exist. E₁(a) specifically cites "T4a's non-adjacency constraint" as ensuring non-empty fields, but T4a's equivalence requires *all three* syntactic conditions (non-adjacency, first component > 0, last component > 0), not non-adjacency alone — non-adjacency without the boundary conditions still permits empty first or last fields. S7a (AllPositiveElement) does not fill the gap: it constrains non-zero components to be ≥ 1 (`aᵢ ≠ 0 ⟹ aᵢ ≥ 1`), but this is trivially true in ℕ and does not prevent the first or last component from being zero. Neither E₁(a) nor S7c cites S7a in any case. The gap propagates to S8-crun postcondition 3 (I-address subspace preservation), which invokes both `E₁(a + k)` well-definedness and S7c's element-field depth bound.
**What needs resolving**: The precondition chain from `dom(Σ.C)` addresses to T4b's non-empty field requirement must be established. Either (a) a property must axiomatize or derive that `dom(Σ.C)` addresses satisfy T4's non-empty field constraint — equivalently, by T4a, that the first and last components are positive and no two zeros are adjacent — or (b) E₁(a)'s definition scope must be restricted to addresses satisfying full T4 compliance, with a cited property establishing that `dom(Σ.C) ⊆ T4\text{-valid}`. E₁(a)'s body text must not present `zeros(a) = 3` as sufficient for T4b, and must not cite T4a's non-adjacency condition alone as ensuring non-empty fields.

## Result

Cone not converged after 1 cycles.

*Elapsed: 1145s*
