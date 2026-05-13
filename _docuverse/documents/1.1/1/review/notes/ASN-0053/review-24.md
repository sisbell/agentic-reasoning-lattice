# Review of ASN-0053

## REVISE

### Issue 1: Foundation reference name inconsistency

**ASN-0053, "The reach function" section**: "This is exactly the formula for b ⊖ a from ASN-0034's TumblerSubtract." Also: "When #start > #width, the round-trip fails: ... TumblerSubtract zero-pads reach to length #start..."

**Problem**: The foundation defines this operator as `TumblerSub`, not `TumblerSubtract`. Two occurrences of the incorrect name.

**Required**: Replace `TumblerSubtract` with `TumblerSub` throughout to match the foundation.

### Issue 2: SC exhaustiveness uses WLOG without spelling out symmetric branches

**ASN-0053, SC (SpanClassification), Exhaustiveness paragraph**: "Assume without loss of generality that start(α) ≤ start(β) (the symmetric cases are covered by the 'or symmetrically' clauses)."

**Problem**: The proof traces only the `start(α) ≤ start(β)` branch. The reader must independently verify that the symmetric branch (where `start(α) > start(β)`) produces the same five cases via the "or symmetrically" clauses in the SC definition. Given that the proof is the only justification for "every ordering ... falls into exactly one case," the WLOG step shifts work onto the reader.

**Required**: Either show the symmetric branch explicitly, or argue why WLOG is justified here (e.g., the SC definition is symmetric in α, β, so the classification is invariant under swapping).

### Issue 3: S9 Case 2 handles only one inequality direction

**ASN-0053, S9 proof, Case 2**: "say reach(αᵢ) < reach(βᵢ). Set p = reach(αᵢ)..."

**Problem**: Only the `reach(αᵢ) < reach(βᵢ)` branch is derived. The symmetric branch `reach(αᵢ) > reach(βᵢ)` (which is part of the case hypothesis `reach(αᵢ) ≠ reach(βᵢ)`) is left implicit.

**Required**: Explicitly state that the symmetric case follows by swapping the roles of Σ̂₁ and Σ̂₂ (or trace the second branch).

### Issue 4: S11 elides the decomposition derivation

**ASN-0053, S11 proof**: "Containment means start(α) ≤ start(β) and reach(β) ≤ reach(α). The difference decomposes into two intervals: Left: {t : start(α) ≤ t < start(β)} ... Right: {t : reach(β) ≤ t < reach(α)} ..."

**Problem**: "The difference decomposes into two intervals" is asserted, not derived. The element-chasing argument — for t ∈ ⟦α⟧, splitting on whether t < start(β), start(β) ≤ t < reach(β), or t ≥ reach(β), and showing the first and third cases are exactly the left and right intervals — is the load-bearing work and is omitted. S11c performs this style of derivation explicitly; S11 should follow the same pattern.

**Required**: Add element-chasing showing `⟦α⟧ \ ⟦β⟧ = left ∪ right` from the definitions, with explicit handling of the three sub-ranges of ⟦α⟧.

### Issue 5: S3b handles only one direction of adjacency

**ASN-0053, S3b preconditions**: "For adjacent level-uniform spans α and β with reach(α) = start(β) and level_compat(start(α), start(β))..."

**Problem**: Adjacency (as defined before S3) is `reach(α) = start(β) ∨ reach(β) = start(α)`. S3b's proof handles only the first disjunct. The second case (reach(β) = start(α)) is not addressed and would require either a separate proof or an explicit appeal to S3a.

**Required**: Either generalize the proof to both adjacency directions, or note that the second case follows by relabeling and S3a's commutativity result.

### Issue 6: Width recovery cites D2 without checking preconditions

**ASN-0053, "The reach function" section**: "Width recovery follows from displacement uniqueness in the foundation: since s ⊕ ℓ = reach(σ), for a level-uniform span σ, reach(σ) ⊖ start(σ) = width(σ) (D2, ASN-0034)."

**Problem**: D2 (DisplacementUnique) has eight preconditions including `divergence(a, b) ≤ #a` and `#a ≤ #b`. The application here (`a = start(σ)`, `b = reach(σ)`, `w = width(σ)`) requires verifying each. Level-uniformity discharges `#a ≤ #b` and the divergence bound (type (i), k ≤ #start), but this verification is not shown. For a foundational arithmetic identity that downstream proofs rely on, the derivation should be explicit.

**Required**: Add a one-paragraph derivation discharging D2's preconditions from level-uniformity and T12.

## OUT_OF_SCOPE

### Topic 1: Span operations across hierarchical levels

The ASN restricts to level-compatible operands throughout. Cross-depth intersection, merge, split, and difference are open questions for future work. The ASN appropriately defers these.

### Topic 2: Span-set difference and its tight bound

S11d bounds two-span difference at 2. The general span-set difference bound (normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)) is identified as an open question. Appropriately deferred.

### Topic 3: Behavior under address allocation

The Nelson caveat that normalized form depends on the ambient population, and the open question about updating normalized forms under allocation, are properly identified as future work.

VERDICT: REVISE
