# Review of ASN-0059

## REVISE

### Issue 1: I10 B2 verification — within-group disjointness omitted

**ASN-0059, Block Decomposition Effect, B2 verification**: "Within subspace S: B_left blocks have V-extents ending before p; the new block occupies [p, p + n − 1]; shifted blocks start at or beyond p + n. No overlap."

**Problem**: This argument establishes between-group disjointness (B_left vs new block vs shifted blocks) but does not address within-group disjointness. Two B_left blocks could in principle overlap (β_L from the split plus case-(a) blocks); two shifted blocks could in principle overlap. The within-group argument is straightforward but must be stated — "No overlap" without it is incomplete.

**Required**: Add two sentences: (a) B_left blocks are pairwise disjoint because they are drawn from B (inheriting B2), with β_L's V-extent a strict subset of the original β's V-extent, which was disjoint from every other block in B by B2. (b) Shifted blocks are pairwise disjoint because V(shift\_block(β, n)) = shift(V(β), n), shift is injective (I7), and the original V-extents are pairwise disjoint by B2 on B.

### Issue 2: TA-strict cited for ordinal increment

**ASN-0059, INSERT as Composite Transition**: "I0(ii) gives aⱼ₊₁ = aⱼ + 1 > aⱼ by TA-strict (ASN-0034), so a₁ < a₂ < ... < aₙ — all distinct."

**Problem**: TA-strict is the lemma `(A a, w > 0 : a ⊕ w > a)` for tumbler addition ⊕. I0(ii) defines `+` as ordinal increment via TA5(c), not tumbler addition. Applying TA-strict requires the unstated equivalence `inc(a, 0) = a ⊕ δ(1, #a)` when `sig(a) = #a`. TA5(a) directly states `t' > t` for ordinal increment with no intermediate step needed.

**Required**: Cite TA5(a) instead of TA-strict, or explicitly state the equivalence between ordinal increment and tumbler addition with δ(1, m).

### Issue 3: VContiguity quantifies over invalid and unbounded intermediate positions

**ASN-0059, Contiguity, VContiguity definition**: "(A v : subspace(v) = S ∧ #v = #u ∧ u < v < w : v ∈ V_S)"

**Problem**: The inner quantification ranges over all tumblers of the given depth and subspace between u and w — including tumblers with zero components (violating S8a) and, more critically, infinitely many valid tumblers across ordinal-group boundaries. At depth m ≥ 3, if u and w differ at any position j < m, the lexicographic interval contains infinitely many depth-m tumblers. For example, between [1, 2, 1] and [1, 3, 1], every [1, 2, k] for k ≥ 2 is an intermediate — infinitely many, all S8a-valid. Combined with S8-fin, VContiguity is unsatisfiable for depth ≥ 3 V_S spanning multiple ordinal groups. At depth 2, the issue does not arise: between [S, a] and [S, b], the intermediates are the finitely many [S, i] with a < i < b. The definition is correct but this scope limitation is non-obvious and affects how readers interpret I9's applicability.

**Required**: Add a note after the definition observing that at depth ≥ 3, VContiguity constrains V_S to positions sharing a common prefix at positions 1..m−1 (a single ordinal group), because lexicographic ordering creates infinite intervals across ordinal groups. This makes the definition's scope transparent. For the typical text-subspace case (m = 2), the constraint is vacuously satisfied and VContiguity behaves as expected.

## OUT_OF_SCOPE

### Topic 1: VContiguity as a system-wide invariant
**Why out of scope**: The ASN explicitly lists this as an open question. Whether contiguity is an invariant enforced by the system or a precondition the caller must satisfy is an architectural decision, not an error in the INSERT specification.

### Topic 2: Depth ≥ 3 V-position structures
**Why out of scope**: The typical text V-position has depth 2 (subspace + ordinal). Multi-level ordinal structures for V-positions would arise from hierarchical document models and belong in a future ASN on document structure. INSERT's postconditions (I1–I5) are correct at any depth; only VContiguity has surprising depth ≥ 3 behavior (addressed in REVISE Issue 3).

VERDICT: REVISE
