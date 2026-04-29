# Formalize — ASN-0036 / D-CTG

*2026-04-13 12:26*

- `INACCURATE: The postcondition formula guards with v₁ ∈ V_S(d) ∧ v₂ ∈ V_S(d) ∧ #v₁ ≥ 3, then accesses (v₂)ⱼ for 2 ≤ j ≤ #v₁ − 1, without requiring #v₂ = #v₁. The component access (v₂)ⱼ is only well-formed when #v₂ ≥ #v₁ − 1 + 1 = #v₁. The proof establishes this result only for positions of equal depth m (both v₁ and v₂ have depth m "by S8-depth"). The guard should include #v₁ = #v₂ to make the formula self-contained and faithful to the proof's assumption: v₁ ∈ V_S(d) ∧ v₂ ∈ V_S(d) ∧ #v₁ = #v₂ ∧ #v₁ ≥ 3.`
