# Review of ASN-0040

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Parent prerequisite chain
**Why out of scope**: The ASN explicitly defers whether `p ∈ Σ.B` is required before baptizing children under p. This depends on the ownership/authorization model, which is a distinct specification concern. The formal development is sound regardless of how this question is resolved — B6(i) gates structural validity (T4), and the authorization gate is orthogonal.

### Topic 2: Distributed baptism coordination
**Why out of scope**: B4 serializes within a namespace; cross-namespace concurrency is permitted by B7. The coordination protocol for multi-replica systems (open question 5) and the minimal serialization grain (open question 7) are engineering/protocol concerns that build on the guarantees established here, not gaps in this ASN's claims.

### Topic 3: Bulk allocation
**Why out of scope**: Baptizing a contiguous range in a single operation is an optimization that must satisfy B4 and B1 — the constraints are established here, the optimization mechanism is future work.

---

**Verification notes on the formal development:**

**B0/B0a**: B0 (irrevocability) is the state-level reading of T8; B0a (baptismal closure) constrains the growth mechanism. Together they establish the only-through-the-gate property. The deferred parent prerequisite does not affect the soundness of either — B0a constrains structural validity (T4 via B6) and depth arithmetic, which is sufficient for the downstream proofs.

**S0/S1**: S0 follows from iterated TA5(a) with transitivity. S1 follows from TA5(b) for c₁ and TA5(c) for subsequent siblings (modification at sig > #p leaves the prefix invariant). Both are sound one-step derivations from foundation.

**B1 induction**: Base case (B₀ conformance) is explicitly required. Inductive step: a baptism in namespace (p, d) adds c_{hwm+1}, extending the contiguous prefix by one; a baptism in any other namespace (q, e) adds an element outside S(p, d) by B7, leaving children unchanged. B0 ensures no element is lost. B0a ensures no non-baptismal insertion. B4 ensures the state observation is current within the target namespace. The cross-namespace preservation argument (new element not in S(p', d') for (p', d') ≠ (p, d)) is explicitly stated. The induction is well-founded (over the count of baptisms from genesis).

**B₀ conformance**: Requires both contiguous prefix and T4 for all seeds. The traced example verifies [1] is conforming: it satisfies T4, and no sibling stream contains it (stream elements have length ≥ 2). The requirement that seeds satisfy T4 is essential — it grounds both B7 (Case 3 requires T4 for parents) and B10 (base case of the registry-wide T4 induction).

**B10 derivation**: Induction on the baptism sequence. Base: B₀ conformance (T4 for seeds). Step, hwm = 0: c₁ = inc(p, d), p satisfies T4 by B6(i), IncrementPreservesValidity gives T4 for c₁ when d ∈ {1, 2} and zeros(p) + (d−1) ≤ 3. Step, hwm > 0: c_{m+1} = inc(cₘ, 0), cₘ satisfies T4 by IH, IncrementPreservesValidity with k = 0 preserves T4 unconditionally. Both sub-cases shown. The chain closes: every element entering B satisfies T4, so B7's precondition (T4 for parents) is automatically satisfied when the parent is itself baptized.

**B5/B5a**: B5 follows from TA5(d) — d−1 new zeros are introduced, none destroyed. B5a follows from TA5(c) — sibling increment modifies only sig(t), advancing a positive value (precondition discharged for all stream elements by induction: c₁ has final component 1, each increment preserves positivity). The uniform zeros count across S(p, d) follows by combining B5 and iterated B5a.

**B7 case analysis**: Exhaustive under B6 constraints (d, d' ∈ {1, 2}). Case 1 (different element lengths): T3 gives disjointness. Case 2 (non-nesting prefixes, equal lengths): T10 gives disjointness. Case 3 (nesting prefixes, equal lengths): forces d = 2, d' = 1, #p' = #p + 1; position #p + 1 is invariantly 0 in S(p, 2) (zero separator from TA5(d)) and invariantly > 0 in S(p', 1) (T4 ensures p' doesn't end in zero; TA5(c) modifies only the last position, leaving #p + 1 unchanged). The reverse nesting direction (p' ≼ p) is symmetric. I verified that no other configuration arises: #p' − #p = d − d' is forced to 1 by d, d' ∈ {1, 2} with d > d'.

**B8 derivation**: Within a namespace, B4 + B1 + S0 give distinct stream indices mapped to distinct addresses. Across namespaces, B7 gives disjoint ranges. The ASN correctly notes the complementary relationship with ASN-0034's GlobalUniqueness — algebraic (per-stream monotonicity) vs. set-theoretic (per-stream contiguity + cross-stream disjointness).

**Weakest precondition analysis**: wp(baptize, B1) identifies state precondition B1, environmental assumptions B0a and B4, and supporting lemma B7. wp(baptize, freshness) partitions B into three disjoint cases: target namespace (B1 gives c_{hwm+1} is the first unbaptized sibling), other B6-valid namespaces (B7 gives disjointness), orphan seeds not in any stream (c_{hwm+1} ∈ S(p, d) while orphans ∉ S(p, d)). The trivial wp (hwm = N+1 requires hwm = N) is correctly identified as uninteresting. The non-trivial wp reveals the mutual support structure of B1, B0a, B4, B7 — each required for the others' preservation.

**Concrete example**: Steps 1–3 verified against B1, B5, B5a, B6, B7. B7 Case 3 verified with S([1], 2) vs. S([1, 1], 1) — position 2 is 0 vs. 1, invariant under sibling increments. The example exercises the first-child branch (children = ∅ → inc(p, d)) and the sibling branch (children ≠ ∅ → inc(max, 0)), and covers both same-level (d = 1) and level-crossing (d = 2) baptism.

**B9**: Follows from T0(a) — the child ordinal occupies a single unbounded component. Combined with B1, any namespace can grow to an arbitrary contiguous prefix. No architectural ceiling.

VERDICT: CONVERGED
