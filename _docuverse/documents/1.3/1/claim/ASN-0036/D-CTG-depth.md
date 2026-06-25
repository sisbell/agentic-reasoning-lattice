**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_1(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_1(d) be non-empty with common depth `m` (S8-depth) and `m ≥ 3` (non-triviality bound, per the Preconditions). Suppose for contradiction that V_1(d) contains two positions u and x with u < x (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, uᵢ = xᵢ for all i < j, and uⱼ < xⱼ (the inequality follows from u < x by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

We construct infinitely many intermediates. For any natural number n > uⱼ₊₁, define w of length m by:

- wᵢ = uᵢ for 1 ≤ i ≤ j (agreeing with u on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (an empty range when j = m − 1, in which case wⱼ₊₁ = w_m is already the last component; otherwise this clause fills components j + 2 through m).

Then w has depth m (it has m components by construction), and subspace(w) = w₁ = u₁ = 1 (since j ≥ 2, the first component is copied from u). We verify u < w < x:

- **w > u**: w agrees with u on components 1 through j. At component j + 1, wⱼ₊₁ = n > uⱼ₊₁. Since j + 1 ≤ m = min(m, m), by T1(i), w > u.
- **w < x**: w agrees with x on components 1 through j − 1 (since u and x agree on these components by the definition of j). At component j, wⱼ = uⱼ < xⱼ. Since j ≤ m − 1 ≤ min(m, m), by T1(i), w < x.

We also verify that w satisfies S8a — necessary because D-CTG ranges over V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a. By construction, every component of w is at least 1: wᵢ = uᵢ ≥ 1 for i ≤ j by S8a applied to u; wⱼ₊₁ = n > uⱼ₊₁ ≥ 1 (again by S8a on u); and wᵢ = 1 for j + 2 ≤ i ≤ m. Hence zeros(w) = 0 and `(A i : 1 ≤ i ≤ #w : wᵢ > 0)`. Combined with #w = m ≥ 3 ≥ 2, w satisfies S8a — so the candidate w qualifies for D-CTG's consequent.

Since u < w < x, subspace(w) = 1, #w = m = #u, and w satisfies S8a, D-CTG requires w ∈ V_1(d). We now exhibit infinitely many admissible values of n. T0(a) (UnboundedComponentValues, ASN-0034) supplies, for any natural-number bound M, one witness n ∈ ℕ with n > M. Iterating: starting from M₀ = uⱼ₊₁, T0(a) supplies n₁ > M₀; setting M₁ = n₁, T0(a) supplies n₂ > M₁ ≥ n₁; continuing, we obtain a strictly increasing sequence n₁ < n₂ < n₃ < … of natural numbers, all exceeding uⱼ₊₁. The sequence is infinite and pairwise distinct. Distinct values of n yield distinct tumblers w (they differ at component j + 1, so by T3, CanonicalRepresentation, ASN-0034, they are unequal). This produces infinitely many distinct positions in V_1(d), contradicting S8-fin (dom(M(d)) is finite).

Therefore no two positions in V_1(d) can disagree at any component j with 2 ≤ j ≤ m − 1. All positions share components 2 through m − 1, and contiguity reduces to contiguity of the last component (component m) alone. ∎

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

*Formal Contract:*

- *Preconditions:*
  - V_1(d) ≠ ∅ (non-empty).
  - All positions in V_1(d) share a common depth m (S8-depth), with m ≥ 3 (non-triviality bound, per the Preconditions).
  - Every position p ∈ V_1(d) has subspace(p) = p₁ = 1.
  - V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a: `#p ≥ 2 ∧ (A i : 1 ≤ i ≤ #p : pᵢ > 0)`.
  - V_1(d) is contiguous in the position order (D-CTG): if u, x ∈ V_1(d), u < w < x, subspace(w) = 1, #w = #u, and w satisfies S8a, then w ∈ V_1(d).
  - dom(M(d)) is finite (S8-fin).
  - Component values are unbounded: for any bound M ∈ ℕ there exists n ∈ ℕ with n > M (T0(a), ASN-0034).

- *Postconditions:*
  - `(A u, x : u ∈ V_1(d) ∧ x ∈ V_1(d) : (A i : 2 ≤ i ≤ m − 1 : uᵢ = xᵢ))` — every pair of positions in V_1(d) agrees on components 2 through m − 1.
  - Contiguity of V_1(d) is determined by component m alone, structurally identical to the depth-2 case.

- *Definition:* For positions u, x ∈ V_1(d) (u < x, both depth m) whose first disagreement is at component j with 2 ≤ j ≤ m − 1, and for any n > uⱼ₊₁, the intermediate witness w of depth m is constructed by: wᵢ = uᵢ for 1 ≤ i ≤ j; wⱼ₊₁ = n; wᵢ = 1 for j + 2 ≤ i ≤ m (an empty clause when j = m − 1).
