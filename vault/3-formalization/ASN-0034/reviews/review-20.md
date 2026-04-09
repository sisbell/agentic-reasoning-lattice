# Cross-cutting Review — ASN-0034 (cycle 3)

*2026-04-09 00:47*

I've read the entire ASN-0034 as a system — tracing every precondition chain, checking definition consistency across all 60+ properties, verifying case analysis exhaustiveness, and confirming that the duplicate proof sections (verification of TA1, TA3, TA4) are consistent with their main presentations.

### TA1-strict declares "from Divergence, TumblerAdd" but directly invokes T1
**Foundation**: T1 (LexicographicOrder), TA1-strict (StrictOrderPreservation)
**ASN**: TA1-strict property table entry declares `from Divergence, TumblerAdd`. The proof's Case 1 concludes: *"Position k witnesses T1 case (i): a ⊕ w < b ⊕ w."* Case 2 concludes identically: *"By T1 case (i), a ⊕ w < b ⊕ w."* Both conclusions invoke T1's definition to establish the ordering of the results.
**Issue**: T1 is available transitively through Divergence (which declares `from T1`), so the precondition chain is not logically broken. However, the convention elsewhere in the ASN is to list directly-invoked properties in the "from" clause — compare TA3, which declares `from TA2, T1, TA6, TumblerSub`, listing T1 alongside properties that also transitively provide it. TA1-strict's proof uses T1 as a direct inferential step (not mediated through Divergence), yet only Divergence and TumblerAdd appear in the declared chain. A dependency-checking tool or formalization following the declared "from" list would not see T1 in scope for TA1-strict unless it resolved the transitive path through Divergence — a path the proof text does not follow.
**What needs resolving**: TA1-strict's declared dependencies should include T1, consistent with the convention established by TA3, TA-strict (`from TumblerAdd, T1`), and other arithmetic properties that list T1 when their proofs invoke it directly.

No other cross-property logical issues found. The proofs are correct: case analyses are exhaustive over their domains, the formal Divergence and TumblerSub's zpd are never conflated, the allocation uniqueness argument correctly partitions all pairs through four exhaustive cases, and the PartitionMonotonicity induction correctly establishes that parent-level siblings leave the partition (inc(p, 0) does not extend p, since it modifies position sig(p)).

## Result

Not converged after 3 cycles.

*Elapsed: 4713s*
