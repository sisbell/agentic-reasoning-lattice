# Review of ASN-0034

## REVISE

### Issue 1: TA7a verification contains a false intermediate claim and S is undefined

**ASN-0034, TA7a Verification**: "For ⊖: the divergence between o and w falls at position k or later (since wᵢ = 0 for i < k, and ordinal components are non-negative — the zero-padded values agree before k)."

**Problem**: The claim that divergence falls at k or later is false for multi-component ordinals. Valid address ordinals have all positive components (T4's positive-component constraint). When k ≥ 2, the displacement has wᵢ = 0 for i < k, but the ordinal has oᵢ > 0 for all i. The divergence falls at position 1 (where o₁ > 0 = w₁), not at k. The subtraction is a no-op: it produces o itself.

For k = 1, a different failure mode arises. Counterexample: o = [5, 3], w = [5, 1] (action point k = 1, 1 ≤ k ≤ m = 2). Preconditions satisfied: o ≥ w (agree at position 1, diverge at position 2 with 3 > 1). Subtraction: divergence at position 2, result [0, 3 − 1] = [0, 2]. This tumbler has a zero first component, violating T4's positive-component constraint for element fields. It is neither all-positive (not in S, if S means valid ordinals) nor all-zero (not in Z).

The deeper issue: S is never formally defined. The property uses `o ∈ S` and claims `o ⊖ w ∈ S ∪ Z` without specifying what membership in S requires. If S means ordinals with all positive components (matching T4), the subtraction claim has the counterexample above. If S means all tumblers, the claim is trivially true and provides no useful guarantee.

**Required**: (a) Define S precisely. (b) Fix the verification — for k ≥ 2, acknowledge the subtraction is a no-op (divergence at position 1, result is o ∈ S trivially). For k = 1, either restrict the displacement to ensure the result stays in S (e.g., require divergence at position k, which needs w to agree with o on all positions before k), or state the closure in terms that accommodate the zero-component result (e.g., "the result is a valid tumbler in T and the subspace identifier is preserved").

### Issue 2: Dependency graph has circular and reversed dependencies

**Problem**: Two circular dependencies make the graph unusable for topological ordering:

| Cycle | Direction in graph | Actual direction |
|---|---|---|
| TA-strict ↔ T12 | TA-strict lists T12 | T12 depends on TA-strict (for span non-emptiness). TA-strict's proof uses only TumblerAdd and T1 — T12 is mentioned as motivation, not as a premise. |
| D0 ↔ D1 | D0 lists D1 | D0 is a precondition *for* D1. D1's proof cites D0 as a prerequisite. D0's definition does not reference D1. |

Additionally, TumblerAdd lists TA4 in its `follows_from`, but TumblerAdd is a definition introduced before TA4. TA4's proof uses TumblerAdd, not the reverse.

**Required**: Remove T12 from TA-strict's `follows_from`. Remove D1 from D0's `follows_from`. Reverse TumblerAdd → TA4 to TA4 → TumblerAdd.

### Issue 3: Dependency graph has spurious dependencies

**Problem**: Multiple properties list `follows_from` entries that are only mentioned in passing (motivation, context, or contrast) but not used in the derivation. The most impactful:

| Property | Spurious entries | Reason |
|---|---|---|
| T0(b) | T0(a) | T0(b) follows from T's definition ("the constant sequence [1,...,1] of length n"), not from T0(a) |
| T7 | T1 | T7 is "corollary of T3 + T4" (property table). T1 is mentioned for the ordering consequence, not the derivation |
| T9 | T10, T8 | T9 derives from T10a + TA5(a) only. T10 (cross-allocator) and T8 (permanence) are mentioned in surrounding prose but not in the derivation |
| TA-strict | TA1, TA4 | The proof uses TumblerAdd definition + T1. TA1 and TA4 appear in the paragraph explaining why TA-strict is needed (degenerate model exclusion), not in the proof |
| Divergence | TA0, TA1, TA1-strict | Pure definition based on tumbler components and T1. TA0/TA1/TA1-strict appear in surrounding text about TA1-strict, not in the definition |
| T12 | T5 | T12 explicitly says "We reserve T5 for the distinct claim that prefix-defined sets are contiguous" |
| TA-MTO | TumblerSub | Both forward and converse proofs use TumblerAdd only |
| TS5 | T4, TA0, TS1, TumblerAdd | Proof uses TS3 + TS4 only |
| TumblerSub | TA1, TA1-strict, TA3 | TumblerSub is a definition; TA1/TA1-strict/TA3 are properties proved *about* TumblerSub, not premises for defining it |

**Required**: Remove the spurious entries listed above from each property's `follows_from`.

### Issue 4: Dependency graph has missing dependencies and name mismatches

**Problem (missing dependencies)**: Several derivations use properties not listed in their `follows_from`:

| Property | Undeclared dependency | Used in |
|---|---|---|
| TA1-strict | Divergence | Statement uses `divergence(a, b)`; proof's case analysis hinges on the divergence definition |
| TA-strict | TumblerAdd | Proof says "By the constructive definition (below)" and uses TumblerAdd's component formula |
| PartitionMonotonicity | TA5, T3 | Proof uses TA5(c) for length preservation of `inc(·, 0)` and T3 to conclude non-nesting from same-length-but-different |

**Problem (non-existent reference)**: T9 lists `TA5(a)` in its `follows_from`, but no property named `TA5(a)` exists in the graph. The intended reference is `TA5`.

**Problem (name mismatches)**:

| Property | Graph name | Actual name (from property table) |
|---|---|---|
| TA7a | `For ordinals \`o = [o₁,` (truncated) | "For ordinals o = [o₁, ..., oₘ] (m ≥ 1) in ordinal-only formulation, shift operations preserve all components before the action point and remain within the same subspace" |
| TA1-strict | `strict (Strict order preservation)` (parsing artifact) | "Addition preserves the total order (strict) when k ≤ min(#a, #b) ∧ k ≥ divergence(a, b)" |
| Divergence | `For a ≠ b` (truncated) | "For a ≠ b: first position k where aₖ ≠ bₖ (component divergence), or min(#a, #b) + 1 if one is a proper prefix of the other (prefix divergence)" |

**Required**: Add the missing dependencies. Change `TA5(a)` to `TA5` in T9. Fix the three truncated/malformed names.

## OUT_OF_SCOPE

### Topic 1: Left cancellation for the order
The open question "Does left cancellation extend to a ⊕ x ≤ a ⊕ y ⟹ x ≤ y?" can be resolved affirmatively using only properties already in this ASN. When action points differ (k_x ≠ k_y), the premise a ⊕ x ≤ a ⊕ y forces k_x > k_y (since k_x < k_y leads to a ⊕ x > a ⊕ y), and x < y follows from their action-point positions. When k_x = k_y, component-wise analysis at and after the action point gives x ≤ y. This would strengthen the cancellation characterization but introduces no new concepts.
**Why out of scope**: The ASN's existing properties are sufficient; this is an enhancement, not an error.

VERDICT: REVISE
