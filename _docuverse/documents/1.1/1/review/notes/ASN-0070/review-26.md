# Review of ASN-0070

I read this as a query specification built on a single relation — the inverse image `R(d,e) = M(d)⁻¹(coverage(e))` partitioned by subspace — with every operation property read off from it. I checked the proofs, the boundary behaviour, and the central uniqueness theorem.

## REVISE

(none)

The deep proof obligation — F-canonical (CanonicalUniqueness) — is discharged in full, not by appeal to "similarly." I verified:

- **Step 1 (width forcing)** is genuinely exhaustive: T12 + ActionPoint bound the action point `k` to `1 ≤ k ≤ m_S(d)`, so the two cases `k < m` and `k = m` cover all of it. The `k < m` exclusion correctly invokes T0(a) for the unbounded `t_m` that makes `⟦σ⟧_V` infinite, and the `k = m` case proves both inclusions of `⟦σ⟧_V = E` rather than asserting one and waving the other.
- **The consecutivity Characterisation** proves both directions, and the reverse direction's induction terminates correctly at position `m` via T0 discreteness (`t_m < t''_m < t_m + 1 ⟹` contradiction). The partition-into-chains argument correctly rules out cycles via strict-order acyclicity rather than assuming it.
- **The V-restricted ↔ full bridge** is the load-bearing step (S9 governs `⟦·⟧`, the postcondition fixes `⟦·⟧_V`), and it is established, not skipped — left- and right-closure of inter-component gaps are both proved, including the `s_j.m = 1` positivity sub-case.

Boundary behaviour is complete: empty document (undefined `m_S(d)` convention → `⟨⟩`), empty endset (`coverage(∅) = ∅` via F-slot), non-type empty slots, no-reach, partial-reach, within-document multiplicity (Config 2, with reachability grounded in K.μ⁺'s content-side non-injectivity, correctly distinguished from S5's abstract-cardinality claim), fragmentation across non-adjacent blocks (Config 6, exercising F-contig at `j>0`), cross-subspace straddle with both components non-empty (Config 7), and state-dependence (Config 4). F-sound/F-complete are correctly framed as the two inclusions of the postcondition rather than independent obligations. The wp analysis unpacks each precondition conjunct and the frame, concluding minimality.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting, concurrency semantics, transclusion-lineage relationships
**Why out of scope**: These are raised in the ASN's own Open Questions and concern system-level contracts that consume `follow` results (citation artifacts, concurrent-modification guarantees, derivation-preserving resolution). They are future territory, not defects in this query specification, which correctly promises only same-state denotational determinism and leaves canonical form an optional downstream projection.

VERDICT: CONVERGED
