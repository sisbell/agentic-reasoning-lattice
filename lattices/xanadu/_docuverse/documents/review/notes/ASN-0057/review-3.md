# Review of ASN-0057

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Reverse recovery (start from end and displacement)
Given `a ⊕ w = b`, the reverse `b ⊖ w` does not recover `a` in general — TumblerAdd's tail-replacement means information about `a` at positions `> k` is lost. A future ASN could characterize when reverse recovery is possible and what additional information is needed.
**Why out of scope**: D1 and D2 fully characterize the forward direction; the reverse is a distinct question with different structure.

### Topic 2: Displacement composition
If `w₁ = b ⊖ a` and `w₂ = c ⊖ b`, what is the relationship between `w₁`, `w₂`, and `c ⊖ a`? This matters for composing span shifts.
**Why out of scope**: The ASN establishes the single-step identity; composition is a separate algebraic question.

### Topic 3: Existence of displacements when #a > #b
When `#a > #b`, `b ⊖ a` does not round-trip (correctly identified), but a *shorter* displacement can still satisfy `a ⊕ w = b` — e.g., `a = [1, 2, 3]`, `b = [1, 5]`, `w = [0, 3]`. This case is outside D1/D2's scope but may be relevant for cross-depth arithmetic.
**Why out of scope**: The ASN correctly restricts to `#a ≤ #b`; alternative displacement constructions are a different topic.

VERDICT: CONVERGED
