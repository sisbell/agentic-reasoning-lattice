**D-SEQ (SequentialPositions).** For each document d and subspace S, if V_S(d) is non-empty and the common V-position depth m ≥ 2 (S8-depth), then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m. The precondition m ≥ 2 is necessary: at m = 1 the tuple `[S, 1, ..., 1, k]` collapses to a single component where the subspace identifier S and the varying ordinal k occupy the same position, and the derivation step "D-MIN gives the minimum k = 1" fails because min(V_S(d)) = [S] has last component S, not 1. ValidInsertionPosition independently requires m ≥ 2 (the empty-subspace case establishes this lower bound), so the precondition is always satisfied in practice. At depth 2 this gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}, matching Nelson's "addresses 1 through n."

*Proof.* Let V_S(d) be non-empty and let m ≥ 2 be the common depth of all V-positions in subspace S (S8-depth guarantees a common depth exists).

**Step 1: shared prefix.** We show that every position in V_S(d) has the form [S, 1, …, 1, k] — that is, components 2 through m − 1 are all equal to 1, with only the last component varying.

*Case m = 2.* Every position has exactly two components: the subspace identifier S at component 1, and a single ordinal at component 2. There are no intermediate components (components 2 through m − 1 is the empty range 2 through 1), so the shared-prefix condition holds vacuously. Every position is [S, k] for some k, which is [S, 1, …, 1, k] with zero intervening 1s.

*Case m ≥ 3.* By D-CTG-depth (SharedPrefixReduction), all positions in V_S(d) share components 2 through m − 1. By D-MIN (VMinimumPosition), the minimum element of V_S(d) is [S, 1, …, 1] — a tuple of length m with every post-subspace component equal to 1. Since the minimum shares components 2 through m − 1 with every other position, and those components of the minimum are all 1, every position in V_S(d) has components 2 through m − 1 equal to 1. Every position is therefore [S, 1, …, 1, k] for some value k at the m-th component.

**Step 2: minimum k.** By D-MIN, min(V_S(d)) = [S, 1, …, 1] of length m. In the representation [S, 1, …, 1, k], the minimum has k = 1 at the last component. Since the minimum is in V_S(d), the set of k-values attained by positions in V_S(d) includes 1.

**Step 3: contiguity of k-values.** Let k₁ < k₂ be two values attained by positions v₁ = [S, 1, …, 1, k₁] and v₂ = [S, 1, …, 1, k₂] in V_S(d). Both have subspace S and depth m. By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂. For any integer k with k₁ < k < k₂, the tuple w = [S, 1, …, 1, k] satisfies subspace(w) = S, #w = m, and v₁ < w < v₂ (again by T1(i), since w agrees with both on components 1 through m − 1 and k₁ < k < k₂ at component m). By D-CTG (VContiguity), w ∈ V_S(d). Therefore every integer between any two attained k-values is itself attained — the k-values form a contiguous range.

**Step 4: finiteness.** By S8-fin (Finite arrangement), dom(M(d)) is finite, so V_S(d) ⊆ dom(M(d)) is finite. The k-values form a finite contiguous range.

**Assembly.** The k-values form a finite contiguous range of positive integers (Step 3, Step 4) beginning at 1 (Step 2). Therefore there exists n ≥ 1 such that the k-values are exactly {1, 2, …, n}. By Step 1, V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}. ∎

*Formal Contract:*
- *Preconditions:* V_S(d) non-empty; common V-position depth m ≥ 2 (S8-depth); D-CTG (VContiguity); D-MIN (VMinimumPosition); S8-fin (finite arrangement).
- *Postconditions:* `(E n : n ≥ 1 : V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length m.

D-CTG is a design constraint on well-formed document states. It constrains which arrangement modifications constitute well-formed editing operations. We verify the base case: before any operations, dom(M(d)) = ∅ for all d (the arrangement is a partial function; no content has been allocated, so no V-mapping exists), so V_S(d) = ∅ for every subspace S. D-CTG holds vacuously (no u, q exist to trigger its antecedent), and D-MIN holds vacuously (its antecedent requires V_S(d) non-empty). Observe that not all arrangement modifications preserve D-CTG: removing a single interior V-position from dom(M(d)) leaves the positions on either side no longer contiguous. D-CTG is therefore preserved only by those modifications that constitute well-formed editing operations — operations that restore contiguity after structural changes (e.g., by shifting subsequent positions).

Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN.

### Concrete example

Consider document d at depth 2 in the text subspace (S = 1), with arrangement:

M(d) = {[1,1] ↦ a₁,  [1,2] ↦ a₂,  [1,3] ↦ a₃}

Then V₁(d) = {[1,1], [1,2], [1,3]}.

**D-CTG check.** The extremes are [1,1] and [1,3]. The only intermediate with subspace 1 and depth 2 between them is [1,2], which is in V₁(d). For the adjacent pairs — ([1,1],[1,2]) and ([1,2],[1,3]) — there are no intermediates. D-CTG is satisfied. ✓

**D-MIN check.** min(V₁(d)) = [1,1], whose last component is 1. ✓

**Violation.** Suppose we removed [1,2], yielding V₁(d) = {[1,1], [1,3]}. Now [1,2] is an intermediate between [1,1] and [1,3] that is absent from V₁(d) — D-CTG is violated. This illustrates why removing a single interior V-position is not a well-formed editing operation on its own; a well-formed deletion must also shift subsequent positions to restore contiguity.

Now consider depth 3. Let document d' have arrangement:

M(d') = {[1,1,1] ↦ a₁,  [1,1,2] ↦ a₂,  [1,1,3] ↦ a₃}

Then V₁(d') = {[1,1,1], [1,1,2], [1,1,3]}.

**D-CTG check.** The extremes are [1,1,1] and [1,1,3]. The only intermediate at subspace 1 and depth 3 between them is [1,1,2], which is in V₁(d'). ✓

**D-MIN check.** min(V₁(d')) = [1,1,1] = [S, 1, 1], with all post-subspace components equal to 1. ✓

**Violation (depth ≥ 3).** Suppose instead V₁(d') = {[1,1,1], [1,2,1]}. D-CTG requires every intermediate with subspace 1 and depth 3 between [1,1,1] and [1,2,1] to be present. But [1,1,2], [1,1,3], [1,1,4], ... are all intermediates — infinitely many, contradicting S8-fin. This is D-CTG-depth in action: positions differing before the last component cannot coexist in a finite arrangement.
