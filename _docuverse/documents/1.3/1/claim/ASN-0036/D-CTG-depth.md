**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_1(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_1(d) be non-empty with common depth `m` (S8-depth) and `m ≥ 3` — a scope restriction ensuring the interior index range `2 ≤ i ≤ m − 1` is non-empty, so the shared-prefix claim has content; the `m = 2` case, where that range is empty and the claim is vacuous, is handled separately in D-SEQ's `m = 2` case. Suppose for contradiction that V_1(d) contains two positions u and x with u < x (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, uᵢ = xᵢ for all i < j, and uⱼ < xⱼ (the inequality follows from u < x by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

We construct infinitely many intermediates. For any natural number n > uⱼ₊₁, define w of length m by:

- wᵢ = uᵢ for 1 ≤ i ≤ j (agreeing with u on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (an empty range when j = m − 1, in which case wⱼ₊₁ = w_m is already the last component; otherwise this clause fills components j + 2 through m).

Every component of w lies in ℕ — wᵢ = uᵢ ∈ ℕ for 1 ≤ i ≤ j since u ∈ T, wⱼ₊₁ = n ∈ ℕ, and wᵢ = 1 ∈ ℕ for j + 2 ≤ i ≤ m — and w has length m ≥ 3 ≥ 1, so by T0's comprehension clause (CarrierSetDefinition, ASN-0034), instantiated at length m and this component map, w ∈ T: the construction yields a genuine tumbler, which is what later lets us instantiate D-CTG's inner v ∈ T quantifier at the constructed w. Then w has depth m (it has m components by construction), and subspace(w) = w₁ = u₁ = 1 (since j ≥ 2, the first component is copied from u). We verify u < w < x:

- **w > u**: w agrees with u on components 1 through j. At component j + 1, wⱼ₊₁ = n > uⱼ₊₁. Since j + 1 ≤ m = min(m, m), by T1(i), w > u.
- **w < x**: w agrees with x on components 1 through j − 1 (since u and x agree on these components by the definition of j). At component j, wⱼ = uⱼ < xⱼ. Since j ≤ m − 1 ≤ min(m, m), by T1(i), w < x.

We also verify that w satisfies S8a — necessary because D-CTG ranges over V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a. By construction, every component of w is at least 1: wᵢ = uᵢ ≥ 1 for i ≤ j by S8a applied to u; wⱼ₊₁ = n > uⱼ₊₁ ≥ 1 (again by S8a on u); and wᵢ = 1 for j + 2 ≤ i ≤ m. Hence zeros(w) = 0 and `(A i : 1 ≤ i ≤ #w : wᵢ > 0)`. Combined with #w = m ≥ 3 ≥ 2, w satisfies S8a — so the candidate w qualifies for D-CTG's consequent.

Since u < w < x, subspace(w) = 1, #w = m = #u, and w satisfies S8a, D-CTG requires w ∈ V_1(d). We now exhibit infinitely many admissible values of n. T0(a) (UnboundedComponentValues, ASN-0034) supplies, for any natural-number bound M, one witness n ∈ ℕ with n > M. Iterating: starting from M₀ = uⱼ₊₁, T0(a) supplies n₁ > M₀; setting M₁ = n₁, T0(a) supplies n₂ > M₁ ≥ n₁; continuing, we obtain a strictly increasing sequence n₁ < n₂ < n₃ < … of natural numbers, all exceeding uⱼ₊₁. The sequence is infinite and pairwise distinct. Distinct values of n yield distinct tumblers w (they differ at component j + 1, so by T3, CanonicalRepresentation, ASN-0034, they are unequal). This produces infinitely many distinct positions in V_1(d), contradicting S8-fin (dom(M(d)) is finite).

Therefore no two positions in V_1(d) can disagree at any component j with 2 ≤ j ≤ m − 1. All positions share components 2 through m − 1, and contiguity reduces to contiguity of the last component (component m) alone. ∎

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

*Formal Contract:*

- *Preconditions:*
  - V_1(d) ≠ ∅ (non-empty).
  - All positions in V_1(d) share a common depth m (S8-depth), with m ≥ 3 — a scope restriction, not a derived bound: at m ≥ 3 the interior index range 2 ≤ i ≤ m − 1 is non-empty, so the shared-prefix claim has content, whereas the m = 2 case, where that range is empty and the claim is vacuous, is handled separately in D-SEQ's m = 2 case.
  - Every position p ∈ V_1(d) has subspace(p) = p₁ = 1.
  - V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a: `#p ≥ 2 ∧ (A i : 1 ≤ i ≤ #p : pᵢ > 0)`.
  - V_1(d) is contiguous in the position order (D-CTG): if u, x ∈ V_1(d), u < w < x, subspace(w) = 1, #w = #u, and w satisfies S8a, then w ∈ V_1(d).
  - dom(M(d)) is finite (S8-fin).
  - Component values are unbounded: for any bound M ∈ ℕ there exists n ∈ ℕ with n > M (T0(a), ASN-0034).

- *Postconditions:*
  - `(A u, x : u ∈ V_1(d) ∧ x ∈ V_1(d) : (A i : 2 ≤ i ≤ m − 1 : uᵢ = xᵢ))` — every pair of positions in V_1(d) agrees on components 2 through m − 1.
  - Contiguity of V_1(d) is determined by component m alone, structurally identical to the depth-2 case.

- *Definition:* For positions u, x ∈ V_1(d) (u < x, both depth m) whose first disagreement is at component j with 2 ≤ j ≤ m − 1, and for any n > uⱼ₊₁, the intermediate witness w of depth m is constructed by: wᵢ = uᵢ for 1 ≤ i ≤ j; wⱼ₊₁ = n; wᵢ = 1 for j + 2 ≤ i ≤ m (an empty clause when j = m − 1).

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the shared depth `m` for all positions in V_1(d), consumed as the proof's starting invariant that all elements have a common depth before the contradiction is constructed
  - T1 (LexicographicOrder, ASN-0034) — supplies the component-comparison clause of the lexicographic order; invoked at three points in the proof to derive u < w and w < x from the first differing component
  - S8a (ArrangementDomainRestriction) — supplies the well-formedness predicate (`#p ≥ 2 ∧ (A i : 1 ≤ i ≤ #p : pᵢ > 0)`) that the constructed intermediate w must satisfy before D-CTG can require w ∈ V_1(d)
  - D-CTG (VContiguity) — supplies the contiguity axiom applied to force w ∈ V_1(d) from u < w < x with matching subspace, depth, and S8a well-formedness; the claim's contradiction rests on producing infinitely many such w
  - T0 (CarrierSetDefinition, ASN-0034) — supplies the comprehension clause that grounds the carrier membership w ∈ T of the explicitly-constructed witness w (length m, every component ℕ-valued), the prerequisite for instantiating D-CTG's inner v ∈ T quantifier at w
  - T0(a) (UnboundedComponentValues, ASN-0034) — supplies, for any bound M, a witness n > M; consumed to construct the strictly increasing sequence n₁ < n₂ < … of admissible intermediates that contradicts S8-fin
  - T3 (CanonicalRepresentation, ASN-0034) — supplies tumbler equality as component-wise identity; used to conclude that distinct values of n yield distinct depth-m positions w (differing at component j + 1)
  - S8-fin (FiniteArrangement) — supplies finiteness of dom(M(d)); the proof is by contradiction, and the infinite sequence of distinct positions in V_1(d) contradicts this finiteness
- *Forward References:*
  - T4 (HierarchicalParsing, ASN-0034) — cited as the structural reason zero is unavailable as a V-position component (zero is a field separator), grounding the 1-based ordinal convention for V-positions stated after the main proof