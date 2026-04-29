# Cone Review — ASN-0034/T10 (cycle 2)

*2026-04-25 18:10*

### Case 1 dispatched without walking De Morgan
**Class**: REVISE
**Foundation**: Prefix (PrefixRelation), NAT-order
**ASN**: T10 proof — "*Case 1: `m ≤ n`.* From `p₁ ⋠ p₂` and `p₁` having length `m ≤ n`, the definition of ≼ fails: there exists `j` with `1 ≤ j ≤ m` and `p₁ⱼ ≠ p₂ⱼ`. Since `m ≤ n`, `j ≤ m = ℓ`."
**Issue**: Case 1 compresses exactly the step that the prior cycle's REVISE forced Case 2 to walk: De Morgan over `¬(p₁ ≼ p₂)` against the conjunction `#p₁ ≤ #p₂ ∧ (∀i : 1 ≤ i ≤ #p₁ : (p₂)ᵢ = (p₁)ᵢ)`, with `m ≤ n` ruling out the length disjunct so the component disjunct holds. After Case 2 was rewritten to walk the derivation, the asymmetry now runs the other way: Case 2 is explicit, Case 1 is dispatched in one sentence ("the definition of ≼ fails"). The two cases should be at the same level of granularity.
**What needs resolving**: Walk Case 1 in the same form as Case 2 — note that `m ≤ n` is `#p₁ ≤ #p₂`, expand `¬(p₁ ≼ p₂)` by De Morgan to the two-disjunct form, observe that the length disjunct contradicts `m ≤ n`, conclude that the component disjunct holds, yielding the existence of `j` with `1 ≤ j ≤ m` and `(p₂)ⱼ ≠ (p₁)ⱼ`.

### `min(m, n) ≤ m` and `min(m, n) ≤ n` not derived
**Class**: OBSERVE
**Foundation**: NAT-wellorder (NatWellOrdering)
**ASN**: T10 proof — "with `k ≤ m` and NAT-order's `≤`-transitivity Consequence, `k ≤ #a`. Symmetrically, `p₂ ≼ b` gives `n ≤ #b`; with `k ≤ n` and `≤`-transitivity again, `k ≤ #b`"
**Issue**: After the case split closes, the proof uses both `k ≤ m` and `k ≤ n` but only `k ≤ ℓ = min(m, n)` was established. The bridge — `min(m, n) ≤ m` and `min(m, n) ≤ n` — is the least-element clause of NAT-wellorder applied to the two-element set `{m, n}`, but the proof does not invoke it. Mechanical, but the citation to NAT-wellorder in Depends is currently scoped to "well-definedness of `min`," which covers existence but not the order properties of the witness. A precise reader has to fill in the step.

VERDICT: REVISE
