# Review of ASN-0053

## REVISE

### Issue 1: S10 missing level-compatibility preconditions
**ASN-0053, S10 (UnionOrderIndependence)**: "The normalized form of a span-set union is independent of the order in which spans are combined: normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)"
**Problem**: Every other span operation in the ASN explicitly states its level-uniformity and level-compatibility requirements — S1, S3, S4, S8, S11 all do this. S10 states no preconditions despite depending on S8 and S9, which require level-uniform and mutually level-compatible spans. The proof invokes `normalize`, which is defined by S8 only for level-compatible span-sets. For the union Σ₁ ∪ Σ₂, the precondition is non-trivial: spans across the two sets must be mutually level-compatible, not just within each set. The omission breaks the ASN's own pattern of self-contained property statements.
**Required**: Add explicit precondition: "For span-sets Σ₁, Σ₂, Σ₃ whose component spans are level-uniform and mutually level-compatible across all sets." The associativity clause involves three sets — state that all spans across all three must be mutually level-compatible.

## OUT_OF_SCOPE

### Topic 1: LeftCancellation as a foundation property
**Why out of scope**: The ASN correctly derives LeftCancellation from ASN-0034's definitions and acknowledges it "is properly a tumbler arithmetic fact, belonging with ASN-0034." Promoting it to the foundation is a future consolidation task, not a defect in this ASN.

### Topic 2: General span difference beyond containment
**Why out of scope**: S11 handles the containment case (⟦β⟧ ⊆ ⟦α⟧). The general difference for arbitrary overlap is derivable — compute the intersection via S1, then apply S11 to the containing span and the intersection — yielding the same bound of 2. Stating this composed result explicitly would be useful but is new territory, not an error.

VERDICT: REVISE
