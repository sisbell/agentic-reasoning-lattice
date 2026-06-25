# Claim Formal Contract — ASN-0036/D-SEQ — run 1

*2026-06-25T19:00:28Z*
*Model: opus*
*Cycles: 1*
*Validation: MISMATCH*

## Validation detail

`

- `MISSING_PRECONDITION: D-CTG-depth (SharedPrefixReduction) is invoked in the proof at Step 1, Case m ≥ 3 — "By D-CTG-depth (SharedPrefixReduction), all positions in V_1(d) share components 2 through m − 1" — but it does not appear in the contract's preconditions. The preconditions enumerate "D-CTG (VContiguity) and D-MIN (VMinimumPosition)" as the well-formedness conditions, silently omitting D-CTG-depth. For m ≥ 2 the shared-prefix step is the structural spine of the proof; without D-CTG-depth in the contract, a consumer verifying only the stated preconditions cannot reconstruct the argument for m ≥ 3. The invariant section repeats the same omission — it lists "D-CTG and D-MIN hold" as the well-formedness guarantees without mentioning D-CTG-depth.`

## Review-rewrite detail

(passed)

## Final LLM response

**D-SEQ (SequentialPositions).** For each document d, if V_1(d) is non-empty, then there exists n ≥ 1 such that:

`V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m, the common V-position depth in the text subspace (S8-depth). By S8a, every V-position has depth `≥ 2`, so `m ≥ 2`; the derivation below relies on this lower bound. At depth 2 this gives V_1(d) = {[1, k] : 1 ≤ k ≤ n}, matching Nelson's "addresses 1 through n."

*Proof.* Let V_1(d) be non-empty and let m be the common depth of all V-positions in the text subspace (S8-depth guarantees a common depth exists). By S8a, every V-position has `#v ≥ 2`, so `m ≥ 2`.

**Step 1: shared prefix.** We show that every position in V_1(d) has the form [1, 1, …, 1, k] — that is, components 2 through m − 1 are all equal to 1, with only the last component varying.

*Case m = 2.* Every position has exactly two components. By the definition `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}` together with `subspace(v) = v₁`, every position in V_1(d) has `v₁ = 1` — the subspace identifier sits at component 1. The second component is a single ordinal. There are no intermediate components (components 2 through m − 1 is the empty range 2 through 1), so the shared-prefix condition holds vacuously. Every position is [1, k] for some k, which is [1, 1, …, 1, k] with zero intervening 1s.

*Case m ≥ 3.* By the definition `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}` together with `subspace(v) = v₁`, every position has `v₁ = 1` — the subspace identifier sits at component 1. By D-CTG-depth (SharedPrefixReduction), all positions in V_1(d) share components 2 through m − 1. By D-MIN (VMinimumPosition), the minimum element of V_1(d) is [1, 1, …, 1] — a tuple of length m with every component equal to 1. Since the minimum shares components 2 through m − 1 with every other position, and those components of the minimum are all 1, every position in V_1(d) has components 2 through m − 1 equal to 1. Together with `v₁ = 1`, every position is therefore [1, 1, …, 1, k] for some value k at the m-th component.

**Step 2: minimum k.** By D-MIN, min(V_1(d)) = [1, 1, …, 1] of length m. In the representation [1, 1, …, 1, k], the minimum has k = 1 at the last component. Since the minimum is in V_1(d), the set of k-values attained by positions in V_1(d) includes 1.

**Step 3: contiguity of k-values.** Let k₁ < k₂ be two values attained by positions v₁ = [1, 1, …, 1, k₁] and v₂ = [1, 1, …, 1, k₂] in V_1(d). Both have subspace 1 and depth m. By T1(i) (LexicographicOrder, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂. For any k ∈ ℕ with k₁ < k < k₂, the tuple w = [1, 1, …, 1, k] satisfies subspace(w) = 1, #w = m, and v₁ < w < v₂ (again by T1(i), since w agrees with both on components 1 through m − 1 and k₁ < k < k₂ at component m). Moreover w satisfies S8a: every component is strictly positive — the leading m − 1 components are all 1, and the last component k satisfies k > k₁ ≥ 1 — so zeros(w) = 0; and #w = m ≥ 2 inherits the depth bound S8a places on v₁. By D-CTG (VContiguity), w ∈ V_1(d). Therefore every k ∈ ℕ between any two attained k-values is itself attained — the k-values form a contiguous range.

**Step 4: finiteness.** By S8-fin (Finite arrangement), dom(M(d)) is finite, so V_1(d) ⊆ dom(M(d)) is finite. The k-values form a finite contiguous range.

**Assembly.** The k-values form a finite contiguous set of positive integers (Step 3, Step 4) that contains 1 (Step 2). Let n = max(k-values); this maximum is well-defined since the set is finite and non-empty (1 ∈ k-values). Then n ≥ 1. By Step 3 applied between 1 and n, every integer with 1 ≤ k ≤ n is attained, so {1, …, n} ⊆ k-values. By definition of n as the maximum, k-values ⊆ {1, …, n}. Hence the k-values are exactly {1, 2, …, n}. By Step 1, V_1(d) = {[1, 1, …, 1, k] : 1 ≤ k ≤ n}. ∎

D-CTG is a design constraint on well-formed document states. We verify the base case: before any operations, dom(M(d)) = ∅ for all d (the arrangement is a partial function; no content has been allocated, so no V-mapping exists), so V_1(d) = ∅. D-CTG holds vacuously (no u, q exist to trigger its antecedent), and D-MIN holds vacuously (its antecedent requires V_1(d) non-empty).

*Formal Contract:*

- *Preconditions:* V_1(d) is non-empty. The document state is well-formed, so the contiguity constraint D-CTG (VContiguity) and the minimality property D-MIN (VMinimumPosition) hold. All V-positions in the text subspace share a common depth m (S8-depth), with `m ≥ 2` (S8a), and dom(M(d)) is finite (S8-fin).
- *Postconditions:* There exists n ≥ 1 such that V_1(d) = {[1, 1, …, 1, k] : 1 ≤ k ≤ n}, where each tuple has length m. Equivalently, the m-th-component values attained by the positions of V_1(d) are exactly the contiguous set {1, 2, …, n}.
- *Invariant:* In every well-formed state reachable from the empty base state (dom(M(d)) = ∅), D-CTG and D-MIN hold, and consequently V_1(d) is either empty or of the sequential form {[1, 1, …, 1, k] : 1 ≤ k ≤ n}. Across each transition s → s' that preserves well-formedness, this characterization is preserved; the base state satisfies it vacuously since V_1(d) = ∅.
