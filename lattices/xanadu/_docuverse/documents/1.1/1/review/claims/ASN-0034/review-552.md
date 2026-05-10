# Cone Review — ASN-0034/T10 (cycle 1)

*2026-04-25 18:03*

### Undefined symbol `⋠`
**Class**: REVISE
**Foundation**: Prefix (PrefixRelation)
**ASN**: T10 (PartitionIndependence) — "let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`)" and "*Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`"
**Issue**: The `⋠` symbol appears in T10's statement, prose, formal preconditions, and proof, but Prefix introduces only `≼` and `≺`. The intended reading is `¬(· ≼ ·)`, but this is never stated. A downstream consumer (oracle generator, formal model) cannot resolve the symbol.
**What needs resolving**: Either define `⋠` in Prefix as the negation of `≼` (e.g., `p ⋠ q ⟺ ¬(p ≼ q)`), or replace every occurrence in T10 with `¬(p₁ ≼ p₂)` etc.

### T10 Case 2 dispatched by "symmetric argument"
**Class**: REVISE
**Foundation**: Prefix, NAT-order
**ASN**: T10 proof — "*Case 2: `m > n`.* By the symmetric argument from `p₂ ⋠ p₁`: there exists `j` with `1 ≤ j ≤ n` and `p₂ⱼ ≠ p₁ⱼ`, with `j ≤ n = ℓ`."
**Issue**: Case 2 invokes "the symmetric argument" without walking it. The asymmetry that needs explicit handling: Case 1 used the hypothesis `m ≤ n` directly to satisfy `#p₁ ≤ #p₂` and trigger De Morgan on `¬(p₁ ≼ p₂)`. Case 2's hypothesis is `m > n`, which is `n < m`; deriving `n ≤ m` (so that the length condition for `p₂ ≼ p₁` holds and the failure of `p₂ ⋠ p₁` reduces to component-disagreement) requires the `≤`-definition `n ≤ m ⟺ n < m ∨ n = m` from NAT-order. The walk is short but it is precisely the kind of case the prompt's discipline forbids dispatching by analogy.
**What needs resolving**: Spell out Case 2: from `m > n` derive `n ≤ m` via NAT-order's `≤`-definition, note the length clause of `p₂ ≼ p₁` is satisfied, then apply De Morgan to `¬(p₂ ≼ p₁)` to obtain the existence of `j` with `1 ≤ j ≤ n` and `(p₁)ⱼ ≠ (p₂)ⱼ`.

### "Distinct" is redundant with non-nesting in T10 prose
**Class**: OBSERVE
**Foundation**: Prefix (reflexivity Consequence)
**ASN**: T10 prose — "Two allocators with distinct, non-nesting prefixes can allocate simultaneously"
**Issue**: Mutual non-nesting (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`) already excludes `p₁ = p₂`, since Prefix's reflexivity Consequence gives `p₁ ≼ p₁`, hence `p₁ = p₂` would yield `p₁ ≼ p₂`, contradicting `p₁ ⋠ p₂`. The "distinct" qualifier is informational redundancy, not an additional precondition. Minor framing.

### Index domain attributed to T3 in T10 proof
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: T10 proof — "Since `k ≤ #a`, `k` lies in T3's index domain `{1, …, #a}`."
**Issue**: The index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}` is introduced and committed to by T0's component-projection axiom, not by T3. T3 only consumes it through extensionality. A downstream reader chasing the citation will land in T3 and find no domain definition.

VERDICT: REVISE
