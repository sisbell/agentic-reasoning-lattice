## Audit

Reading through the dependency graph from the NAT-* foundations upward, the core arithmetic machinery (NAT-induction, D-PRED, D-INJ) is internally sound. D-CTG-depth's contradiction is correctly structured. Three correctness gaps remain, plus one observation.

---

### D-SEQ Assembly — max(k-values) existence ungrounded
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder); NAT-wellorder (NatWellOrdering); NAT-induction (NatInduction)
**ASN**: D-SEQ Assembly step — "Let n = max(k-values); this maximum is well-defined since the set is a finite, non-empty (1 ∈ k-values) subset of ℕ, on which NAT-order's strict total order (NatStrictTotalOrder, ASN-0034) furnishes a greatest element."
**Issue**: NAT-order's formal contract posits irreflexivity, transitivity, and at-least-one trichotomy; none of these yield a greatest-element principle for finite sets. NAT-wellorder gives *least* elements of arbitrary non-empty subsets of ℕ — not greatest elements. The greatest element of a finite non-empty subset requires either an inductive argument on the cardinality (consuming NAT-induction and the cardinality machinery) or some transformation that reduces the maximum to a minimum. Neither is present, and NAT-wellorder and NAT-induction are absent from D-SEQ's Depends. Without a formal derivation that max(k-values) exists, n is undefined and the postcondition V_1(d) = {[1,…,1,k] : 1 ≤ k ≤ n} is unestablished.
**What needs resolving**: Provide a formal argument for why a finite non-empty subset of ℕ has a greatest element — for example, via induction on the set's cardinality using NAT-induction (with the cardinality accessed through the restriction of S8-fin's bijection to V_1(d)), or an alternative construction of n that avoids the maximum entirely (e.g., define n as the cardinality of k-values, then show k-values = {1,…,n} by the contiguity and lower-bound established in Steps 2–3). Add the consumed foundation(s) to D-SEQ's Depends.

---

### D-MIN and D-SEQ — V_1(d) ungrounded, V-sub absent from Depends
**Class**: REVISE
**Foundation**: V-sub (SubspaceProjection)
**ASN**: D-MIN Formal Contract — "For each document d with V_1(d) ≠ ∅, min(V_1(d)) = [1, 1, ..., 1]"; D-MIN Definition — "We apply min only to S = V_1(d), and V_1(d) ⊆ dom(Σ.M(d)) is finite by S8-fin." D-SEQ Step 1 proof — "By the definition V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1} together with subspace(v) = v₁, every position in V_1(d) has v₁ = 1."
**Issue**: V_1(d) is defined by V-sub (SubspaceProjection). Every other claim that uses V_1(d) in a formal statement — D-CTG, D-CTG-depth — lists V-sub in Depends explicitly and credits it as the source of the definition. D-MIN and D-SEQ both use V_1(d) in their formal contracts and proofs (D-SEQ Step 1 directly unfolds the definition V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}), yet neither lists V-sub. The symbol V_1(d) is therefore ungrounded in both formal contracts: a formalization tool consulting their Depends finds no defining source.
**What needs resolving**: Add V-sub (SubspaceProjection) to D-MIN's Depends and to D-SEQ's Depends, with entries that credit V-sub for the definition V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1} being invoked in each claim's formal statement or proof.

---

### D-SEQ Step 3 — zeros(w) = 0 ungrounded, T4 and NAT-card absent from Depends
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing); NAT-card (NatFiniteSetCardinality)
**ASN**: D-SEQ Step 3 — "Moreover w satisfies S8a: every component is strictly positive — the leading m − 1 components are all 1, and the last component k satisfies k > k₁ ≥ 1 — so zeros(w) = 0."
**Issue**: The step "so zeros(w) = 0" requires two things: (1) the zeros function, defined by T4 as zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|; (2) the empty-set characterization |S| = 0 ⟺ S = ∅ (NAT-card's k = 0 case), to conclude that all-positive components imply zeros = 0. D-CTG-depth performs the identical derivation and explicitly cites T4 and NAT-card for exactly this bridge. D-SEQ collapses it to a one-phrase assertion without citing either. Neither T4 nor NAT-card appears in D-SEQ's Depends. A formalization tool invoking D-CTG on the constructed w needs zeros(w) = 0 as a verified guard; the missing derivation leaves this guard unestablished.
**What needs resolving**: Add T4 (for the zeros symbol and its definition) and NAT-card (for the empty-set characterization |S| = 0 ⟺ S = ∅) to D-SEQ's Depends, and ground the zeros(w) = 0 step with the same bridge D-CTG-depth uses: the zero-filter {i : 1 ≤ i ≤ #w ∧ wᵢ = 0} is empty because every wᵢ > 0 (leading components equal 1 > 0 by NAT-closure's 0 < 1; last component > 0 from k > k₁ > 0 by NAT-order transitivity); NAT-card then reads the cardinality of the empty filter as 0.

---

### D-MIN — min existence for tumbler sets rests on informal fold argument
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder); NAT-induction (NatInduction)
**ASN**: D-MIN Definition — "A strict total order has a unique least element on every finite non-empty set — fold the binary minimum (well-defined by T1's totality, order-independent by T1's transitivity) across the finitely many elements — so min(V_1(d)) exists and is unique whenever V_1(d) ≠ ∅."
**Issue**: The "fold the binary minimum" argument is correct in principle but is not formally derived from the axioms. V_1(d) is a set of tumblers, not naturals, so NAT-wellorder does not apply directly; the minimum of a finite totally ordered set of tumblers requires induction on the set size (consuming NAT-induction applied to the set's cardinality under some enumeration). Since D-MIN is a design posit, the well-formedness of the statement "min(V_1(d)) = [1,…,1]" depends on min being well-defined, and the informal argument leaves that foundation implicit.
**What needs resolving**: N/A (the claim is sound; noting for the record that a formal treatment would invoke induction on the enumeration length from S8-fin's bijection restricted to V_1(d), or appeal to the tumbler ordering's lexicographic reduction to finitely many NAT-wellorder applications across the m component positions).

VERDICT: REVISE