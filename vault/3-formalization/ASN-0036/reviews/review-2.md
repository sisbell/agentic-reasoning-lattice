# Formalize — ASN-0036 / D-CTG

*2026-04-12 14:24*

`

- `INACCURATE: The postcondition's formal antecedent includes #v₁ ≥ 3 but not #v₂ = #v₁ (or #v₂ ≥ 3). The inner expression (v₁)ⱼ = (v₂)ⱼ for j ≤ #v₁ − 1 presupposes v₂ has at least depth #v₁ − 1; without this the expression is ill-formed when #v₂ < #v₁ − 1. The proof explicitly cites S8-depth ("both depth m by S8-depth") to guarantee equal depths before performing the component-wise comparison. The antecedent must include #v₁ = #v₂ (or equivalently #v₂ ≥ 3 given uniform-subspace depth from S8-depth) to make the formal statement self-contained, or the shared-depth constraint must appear explicitly rather than only in the surrounding prose.`
