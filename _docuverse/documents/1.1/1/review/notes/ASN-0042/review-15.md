# Review of ASN-0042

## REVISE

### Issue 1: O14 permits bootstrap nesting that falsifies the Account-level permanence Corollary

**ASN-0042, Permanence and Refinement (Corollary)**: "Changes to ω within dom(π) arise only from π's own delegation choices, or recursively from sub-delegates' choices within their own sub-domains."

**Problem**: O14's formal statement allows bootstrap principals with nesting prefixes. Consider `Π₀ = {π₁, π₂}` where `pfx(π₁) = [1]` and `pfx(π₂) = [1, 0, 2]`. Both satisfy O14: `zeros ≤ 1`, distinct prefixes, T4-valid, and coverage holds. But `π₂` was not introduced by delegation from `π₁` — it was bootstrapped. Now `π₂` can delegate within `dom(π₂) ⊆ dom(π₁)`, changing `ω` for addresses in `dom(π₁)` without any act of `π₁` or any "sub-delegate" of `π₁`. The Corollary claims this cannot happen.

The prose discusses only non-nesting bootstrap configurations ("one initial principal per node, e.g., principals at [1] and [2]"), and Nelson's design supports this — accounts are created through delegation from the node operator, not bootstrapped. But O14's formal statement does not enforce non-nesting.

**Required**: Add a pairwise non-nesting constraint to O14:

`(A π₁, π₂ ∈ Π₀ : π₁ ≠ π₂ ⟹ pfx(π₁) ⋠ pfx(π₂) ∧ pfx(π₂) ⋠ pfx(π₁))`

This is consistent with the described scenarios and closes the gap in the Corollary's derivation. With non-nesting bootstrap, every principal whose prefix extends `pfx(π)` entered `Π` via delegation from `π` or a transitive sub-delegate of `π`, and the inductive argument for the Corollary goes through.

### Issue 2: O4's derivation assumes an unstated allocation-closure property

**ASN-0042, The Exclusivity Invariant**: "If `a` is newly allocated in a transition Σ → Σ', then by O5 the allocator is a principal `π` with `pfx(π) ≼ a`."

**Problem**: O5 constrains the *form* of allocation: `(A a ∈ T, π : a newly allocated by π ⟹ pfx(π) ≼ a ∧ ...)`. This says IF `π` allocated `a`, THEN `pfx(π) ≼ a`. It does not assert the existential — that every address entering `Σ.alloc` WAS allocated by some principal. The derivation of O4 needs: for every `a ∈ Σ'.alloc ∖ Σ.alloc`, there exists `π ∈ Π_Σ` such that `π` allocated `a`. O5 does not provide this.

The ASN has O15 as a closure axiom for principals ("Principals enter Π exclusively through bootstrap or delegation") but no corresponding closure axiom for addresses. The asymmetry leaves a gap in O4's derivation.

**Required**: Either (a) add an allocation-closure axiom — every address entering `Σ.alloc` in a transition was allocated by some principal in `Π_Σ` — or (b) strengthen O5 to include the closure property (addresses enter `Σ.alloc` only through allocation by the most-specific covering principal), or (c) restate O4 as an axiom rather than a derived property.

## OUT_OF_SCOPE

### Topic 1: Content-model invariants for the O10 fork
**Why out of scope**: O10 establishes that a fork creates a new address under the requesting principal's domain, with the original unchanged. But the invariants connecting the forked address to the original — transclusion identity, link survival, attribution chains, the "inclusion links" Nelson references — require the I-space, V-space, and link models that are explicitly out of scope. A future ASN on content operations will need to specify what "same content identity" means across an ownership boundary.

VERDICT: REVISE
