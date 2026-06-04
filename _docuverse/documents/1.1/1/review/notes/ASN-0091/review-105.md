# Review of ASN-0091

I checked the abstract Vstream-only class definition, the REARRANGE_K realisation argument (all five K.μ~ admissibility clauses, the net-effect split, frame discharge, reachability), every RE-* derivation, the L-chain lemma, all five worked examples (verifying the cut arithmetic and run cardinalities by hand), and the multi-step composition table.

The note holds up under scrutiny. Specific things I verified rather than assumed:

- **Net-effect split is sound.** The collapse case (π ≠ id yet `M'(d) = M(d)` under shared images) is real, correctly identified, and correctly routed to the empty-sequence realiser with `Σ' = Σ`. The K.μ~ precondition (`M(d)|_{dom_C}` ≥ 2 distinct values) is discharged by ASN-0047's stated necessary-and-sufficient equivalence with clause (ii), not left dangling.
- **Run-decomposition witnesses check arithmetically.** Coalescence (3→2), fragmentation (2→3), and equality (2→2, π ≠ id) each verify against the R-P1/R-P2 formulas and L-chain's exclusion of cross-chain adjacency. The cut ordinals, region widths, and resulting runs are all correct.
- **Boundary cases handled.** Empty arrangement (excluded by R-PRE(ii), admitted abstractly), identity, collapse, non-empty in-S exterior (Worked Example 3 via RE-ext), and 4-cut μ-displacement (Worked Example 2 via R-SPERM) are each exercised.
- **RE-proj witness-independence is proven, not just illustrated.** The biconditional derivation uses only RA-π, so it holds for every valid π; the non-uniqueness example confirms the set image is state-determined.
- **RE-trans (iii) link-subspace exclusion** correctly routes through CL-OWN + S3★-aux + S3★ to establish `a ∈ dom(C)` before invoking C2, and correctly carries the `origin(a) ≠ d` side condition.
- **Transition invariants** (S0, S1, P0–P2, L12, P3, M1, C0) are discharged separately via RA-frame — these are *not* covered by RA-adm (which is per-state only), so the enumeration is load-bearing rather than redundant.

No cross-ASN references outside the foundation set; no notation reinvention; no implementation drift (REARRANGE_K is the ASN-0084 foundation operation, and the contribution is the abstract invariant package — legitimate state-guarantee territory).

## OUT_OF_SCOPE

### Topic 1: Joint reconstitution of a same-source span split by a cut
**Why out of scope**: The note proves each fragment carries the correct `origin` (RE-trans + RE-origin) but explicitly declines to establish whether the fragments jointly reconstitute the source span. This is correctly deferred to the first Open Question, not an error.

### Topic 2: Link-subspace reordering semantics, observational equivalence, run-cardinality bounds, cut-sequence realizability completeness
**Why out of scope**: All four are framed as Open Questions for future ASNs. The current note's claims do not depend on them.

VERDICT: CONVERGED
