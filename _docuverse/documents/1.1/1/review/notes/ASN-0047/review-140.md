# Review of ASN-0047

I conducted a thorough review of this substantial ASN, focusing on the elementary transitions, coupling constraints, verification matrix, and worked examples.

**What I verified:**

- **State model**: Σ = (C, L, E, M, R) and Σ₀ are explicitly defined; initial-state verification covers every per-state invariant including vacuous link-store cases.
- **K.δ case (ii) discharge**: All four sub-cases (k = 0 via FrontierEquivalence; k = 1 with case (a')/(b') T10a.6 dispatch; k = 2 with sub-cases A/B/C terminating at NodeUniqueAllocation/NodeRegistryBootstrap) discharge `e ∉ E` cleanly.
- **K.μ~ dependency chain (A) → (E)**: The chain is non-circular. Step (A) derives subspace preservation from admissibility (i)'s stipulated S3★(Σ') + L14; Step (B) mechanically realises the stipulation; Steps (C)-(D) establish link-subspace fixity (Step C does not consume CL-UNIQ; Step D consumes CL-UNIQ at pre-state via outer induction's IH); Step (E) closes the existence condition `|dom_C(M(d))| ≥ 2`.
- **K.μ⁻ admissible contraction shape**: Forward and reverse directions both proved; equivalence of constructive precondition with post-state characterization is solid.
- **Cross-document disjointness chain lemma**: Case A (prefix-comparable) and Case B (prefix-incomparable) both fully proven; same-level hypothesis is load-bearing for Case A.
- **GlobalLineage**: Three-part derivation (entities, content, links) with explicit induction on L1c's structural inc-chain.
- **Composite-boundary properties**: P4★/P4a/P7a transient-failure-and-restoration discipline cleanly separated from per-state invariants under ValidComposite★.
- **Worked examples**: Five concrete traces verify central postconditions (fork, interior content replacement, two/three-step replacement variants, link allocation, entity hierarchy by K.δ).
- **Boundary cases handled**: empty arrangements, first allocations via SubAllocatorAxiom.FirstEmission, bootstrap node via NodeRegistryBootstrap, K.μ⁻ on singleton.
- **Verification matrix**: Comprehensive coverage of every (invariant, transition) pair with substantive load-bearing discharge in each cell.

## REVISE

(none)

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED
