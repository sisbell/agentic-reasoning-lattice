# Review of ASN-0053

## REVISE

### Issue 1: S8 (NormalizationExistence) has no concrete worked example

**ASN-0053, Normalization / S8**: The construction presents a sweep-line algorithm with a loop invariant proof but verifies it against no specific scenario.

**Problem**: S8 introduces the most complex algorithm in the ASN — sort, scan, conditionally merge or emit, finalize — yet no concrete span-set is walked through the procedure. Every other core property (S1, S3, S4/S5, S11) is verified against an explicit numerical instance. The normalization algorithm involves both merge steps (extending the current interval) and emit steps (flushing the current interval and starting a new one); only a multi-span example can exercise both branches.

**Required**: Add a worked example with at least 3–4 input spans that exercises both the merge branch (overlap/adjacency) and the emit branch (separation). For instance, a span-set like ⟨([1, 7], [0, 2]), ([1, 3], [0, 5]), ([1, 10], [0, 3])⟩ would, after sorting to ⟨([1, 3], [0, 5]), ([1, 7], [0, 2]), ([1, 10], [0, 3])⟩, demonstrate a merge (σ₂ overlaps the current interval) and then an emit (σ₃ is separated), yielding the normalized form ⟨([1, 3], [0, 6]), ([1, 10], [0, 3])⟩. Verify J at each step, and verify N1/N2 of the output.

### Issue 2: Merge-then-split inverse not stated (complement of S4a)

**ASN-0053, Split / S4a**: "splitting σ at p (S4) and merging the two parts (S3) recovers σ exactly."

**Problem**: S4a establishes the split→merge direction: decomposing a span and recomposing it is an identity. The converse — merging two adjacent level-uniform spans and then splitting the result at the original boundary recovers the two original spans — is an equally load-bearing algebraic law that follows directly from S3, S4, and D2, yet the ASN neither states nor derives it. The tools are all present: if α and β are adjacent with reach(α) = start(β), then merge gives γ = (start(α), reach(β) ⊖ start(α)), and splitting γ at start(β) yields λ = (start(α), start(β) ⊖ start(α)) = (start(α), width(α)) = α (by D2 applied to α) and ρ = (start(β), reach(β) ⊖ start(β)) = β (by D2 applied to β). The derivation is three lines and completes the picture: split and merge are exact inverses in both directions.

**Required**: State the merge→split direction as a companion property (e.g., S3b MergeSplitInverse) with explicit derivation using D2.

## OUT_OF_SCOPE

### Topic 1: General two-span set difference (beyond containment)

S11 proves the difference bound for the containment case (⟦β⟧ ⊆ ⟦α⟧). The proper-overlap case (SC (iii)) yields at most 1 span; the separated/adjacent cases yield ⟦α⟧ itself. A unified result — "the set difference of any two level-compatible spans is a span-set of at most 2 spans" — would follow from SC + S11 but is not stated. This is a natural extension, not an error in the current treatment.

**Why out of scope**: S11 covers the hardest and most operationally relevant case (DELETE removes a contained sub-range). The remaining SC cases are simpler and would be new territory.

### Topic 2: Cross-level span interaction

The ASN correctly restricts all binary operations to level-compatible operands (S6). The open questions ask about cross-level intersection and split. Defining what it means for spans at different depths to interact — and what well-formedness conditions govern the result — is future work.

**Why out of scope**: The single-level algebra is self-consistent and complete at its level of abstraction. Cross-level operations require new definitions beyond what this ASN establishes.

VERDICT: REVISE
