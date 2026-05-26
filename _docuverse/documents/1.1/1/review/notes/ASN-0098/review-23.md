# Review of ASN-0098

## REVISE

### Issue 1: LP4 listed twice in working reference frame paragraph
**ASN-0098, "State Components", working reference frame paragraph**: "the projection function, LP4, and the per-document frame lemmas LP4–LP8 hold structurally identically"
**Problem**: LP4 appears both individually and within the range "LP4–LP8". The redundancy creates ambiguity: is LP4 being highlighted for some separate reason, or is the second occurrence (as part of the range) a typo? The text below names two exceptions (LP9's K.μ⁺_L sub-case, LP20's per-subspace refinement) but the positive enumeration is left genuinely unclear.
**Required**: Either narrow the range — "the projection function, LP4, and the per-document frame lemmas LP5–LP8" — or fold LP4 into the range alone — "the projection function and the per-document frame lemmas LP4–LP8".

### Issue 2: Trace example leaves i₀ structurally unspecified
**ASN-0098, "A Worked Trace" section**: "A link `a` with endset `e₁ = {(i₀, ℓ)}`... `i₁, i₂, i₃, i₄` are pairwise sibling chain elements of a single content sub-allocator `A_C(d_alloc)`... They satisfy `i₀ ≤ i₁ < i₂ < i₃ < i₄ < i₀ ⊕ ℓ`"
**Problem**: The trace constrains `i₀` only by `i₀ ≤ i₁` and `i₀ ⊕ ℓ > i₄`. It is not stated whether `i₀` is itself a chain element, an anchor, a tumbler ahead of the chain — and the structural identity matters for verifying that `coverage(e₁)` actually contains `i₁..i₄` (the coverage being a half-open T1-interval). A reader cannot mechanically check the projection equation `project(a, 1, d₁, Σ) = {v₁, v₂, v₃, v₄}` without choosing some specific `i₀`.
**Required**: Pin `i₀` to a concrete structural choice (e.g., `i₀ = i₁` with `ℓ` chosen so that `s ⊕ ℓ > i₄`, or `i₀ = b_C(d_alloc)` if the trace intends an anchor-rooted span) so that the example is mechanically reproducible.

## OUT_OF_SCOPE

None identified — the open-questions section at the end of the ASN appropriately defers the future-ASN material (reverse-discovery primitive, V-order reflection, link-to-link discovery, cross-document fork invariants).

META: not applicable — the ASN stays squarely within abstract spec territory (deriving consequences from foundation invariants) and does not drift toward implementation mechanics.

VERDICT: REVISE
