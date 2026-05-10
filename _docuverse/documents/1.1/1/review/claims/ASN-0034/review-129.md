# Cross-cutting Review — ASN-0034 (cycle 2)

*2026-04-17 07:26*

Reading the ASN as a system, I found one new cross-cutting issue beyond those in Previous Findings.

### T7's quantification range exceeds where its notation is well-defined
**Foundation**: (foundation ASN)
**ASN**: T7 (SubspaceDisjointness). The statement quantifies as `(A a, b ∈ T : zeros(a) = zeros(b) = 3 : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`, while the Formal Contract *Preconditions* clause reads "a, b ∈ T with zeros(a) = zeros(b) = 3 (both are element-level addresses with well-formed field structure per T4)."
**Issue**: The notation `a.E₁` is supplied by T4b (UniqueParse): "The component-access notation `t.X₁` denotes the first component of `X(t)` and is defined exactly when `X(t) ≠ ε`", and T4b's own preconditions require `t` to satisfy T4 (at most three zeros, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`). The predicate `zeros(t) = 3` alone does not entail T4-validity — for example, `t = [0, 1, 0, 2, 0, 3]` has `zeros(t) = 3` but violates `t₁ ≠ 0`; `t = [1, 0, 0, 2, 0, 3]` has `zeros(t) = 3` but violates the no-adjacent-zeros clause. For such tumblers `fields(t)` is undefined (T4b has no postcondition about them), so `a.E₁` has no licensed meaning, and the statement `a.E₁ ≠ b.E₁` is ill-formed as a predicate. The proof itself tacitly uses T4-validity: it names field-length tuples `(α, β, γ, δ)` and places separators at positions `α + 1`, `α + β + 2`, `α + β + γ + 3` — a decomposition only underwritten by T4b, which requires T4-validity. The parenthetical "(...with well-formed field structure per T4)" in the Preconditions line signals the author's intent, but the statement's quantifier does not carry this restriction.

**What needs resolving**: Either the quantifier in T7's statement and the Preconditions clause must explicitly require T4-validity on `a` and `b` (matching T4b's preconditions that license `a.E₁`), or T7 must demonstrate that `a.E₁` is well-defined from `zeros(a) = 3` alone without appeal to T4's field-segment constraint. Downstream readers treating T7 as "zeros = 3 suffices" would misapply it to non-T4-valid tumblers where the conclusion may be vacuous (because `a.E₁` is undefined) rather than substantive.
