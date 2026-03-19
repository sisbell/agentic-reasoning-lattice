# Review of ASN-0053

## REVISE

### Issue 1: S3 merge proof — converse direction skips a critical sub-case

**ASN-0053, S3 (MergeEquivalence)**: "Conversely, any t with s ≤ t < r falls in ⟦α⟧ if t < reach(α), or in ⟦β⟧ if t ≥ start(β) — and the overlap/adjacency condition reach(α) ≥ start(β) ensures no position is missed."

**Problem**: The claim "in ⟦β⟧ if t ≥ start(β)" is necessary but not sufficient — membership in ⟦β⟧ also requires t < reach(β), which is not shown. The actual argument requires multiple steps that are compressed into the em-dash clause:

1. The second case applies when t ≥ reach(α).
2. Combined with t < r, this gives r > reach(α).
3. Since r = max(reach(α), reach(β)) and r > reach(α), it follows that r = reach(β).
4. Then t < r = reach(β).
5. Combined with t ≥ reach(α) ≥ start(β) (overlap condition), we get t ∈ ⟦β⟧.

The phrase "ensures no position is missed" states the conclusion without showing the mechanism. The forward direction (⟦α⟧ ∪ ⟦β⟧ ⊆ [s, r)) is explicit; the converse should be equally so.

**Required**: Expand the converse to show both cases explicitly. In particular, show that when t ≥ reach(α), the constraint t < r forces r = reach(β), giving t < reach(β).

## OUT_OF_SCOPE

### Topic 1: Cross-level span operations
**Why out of scope**: The ASN correctly restricts to level-uniform, level-compatible spans (S6) and identifies cross-level interactions as an open question. The conditions under which spans at different hierarchical depths can be intersected, merged, or split are genuinely new territory requiring analysis of when valid displacements exist across depth boundaries.

### Topic 2: LeftCancellation promotion to foundation
**Why out of scope**: The ASN introduces LeftCancellation as a tumbler arithmetic property and acknowledges it "properly belongs with ASN-0034." This is a correct structural observation — the property is about ⊕ injectivity in its second argument, independent of spans — but promoting it to the foundation is a separate editorial action, not an error in this ASN.

### Topic 3: S7-to-S8 composability gap
**Why out of scope**: S7 (FiniteRepresentability) produces a span-set with ⟦Σ⟧ ⊇ P, but individual spans may be at different tumbler lengths, making the result non-level-compatible and hence not normalizable by S8. Characterizing when a point set admits a level-compatible covering span-set is a separate question about the interaction between hierarchical depth and representability.

### Topic 4: General span-set difference
**Why out of scope**: S11 handles the containment case (⟦β⟧ ⊆ ⟦α⟧). The general case ⟦α⟧ \ ⟦β⟧ for arbitrary α, β also yields at most 2 spans (by case analysis on SC), but stating and proving the general bound belongs in a future ASN that addresses span-set difference as a first-class operation.

VERDICT: REVISE
