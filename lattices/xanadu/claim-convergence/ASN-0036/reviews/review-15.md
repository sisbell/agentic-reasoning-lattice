# Formalize — ASN-0036 / D-CTG

*2026-04-12 14:48*

- `INACCURATE: The postcondition formula quantifies over v₂ ∈ V_S(d) without requiring #v₂ = #v₁. The inner quantifier accesses (v₂)ⱼ for j up to #v₁ − 1; if v₂ were shorter than v₁, those components would be undefined. The proof relies on S8-depth to guarantee all positions in V_S(d) share the same depth m, so the antecedent must include #v₂ = #v₁ (or equivalently #v₂ ≥ 3) to make the formula self-contained. The condition #v₁ ≥ 3 alone is insufficient. Should be: (A d, S, v₁, v₂ : v₁ ∈ V_S(d) ∧ v₂ ∈ V_S(d) ∧ #v₁ ≥ 3 ∧ #v₂ = #v₁ : (A j : 2 ≤ j ≤ #v₁ − 1 : (v₁)ⱼ = (v₂)ⱼ))`
