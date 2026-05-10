# Review of ASN-0081

## REVISE

### Issue 1: D-CS frame condition is one-directional; invariant proofs require biconditional

**ASN-0081, Region Postconditions, D-CS**: "`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`"

**Problem**: D-CS guarantees every pre-state non-S position survives in the post-state but does not exclude new positions appearing in non-S subspaces. The proofs of D-CTG-post, D-MIN-post, S8-depth-post, and S8a-post all cite D-CS as establishing that non-S subspaces are "unchanged" — meaning their position sets are exactly the pre-state sets. D-CS only provides the `⊇` direction. An implementation satisfying the current specification could inject phantom positions into subspace `S' ≠ S` while remaining compliant, potentially violating D-CTG, D-MIN, S8-depth, or S8a for `S'`.

D-CD correctly uses equality (`M'(d') = M(d')`). D-DOM uses set equality for subspace S. D-CS is the only frame condition with this precision gap.

**Required**: Strengthen D-CS to a biconditional on domains:

```
(A S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'})
∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : M'(d)(v) = M(d)(v))
```

This closes the specification gap and validates the claims already made in the four invariant proofs.

### Issue 2: Statement registry missing key definitions

**ASN-0081, Statement Registry**: ThreeRegions (`L`, `X`, `R`) and `Q₃` are defined in the Contraction Setup section and referenced throughout (D-DOM, D-DP, D-CTG-post, all worked examples) but have no registry entries. The contraction operation itself — the ASN's central contribution — has no top-level registry entry aggregating its preconditions, postconditions, and frame conditions.

**Problem**: The registry is the ASN's quick-reference interface for downstream consumers. Omitting the three-region partition and the operation-level entry forces readers to parse prose to find these definitions.

**Required**: Add registry entries for ThreeRegions (`L`, `X`, `R`, `Q₃`) and for the contraction operation itself (with pointers to its component postconditions D-SHIFT, D-DOM, D-L, D-CS, D-CD, D-I).

### Issue 3: D-BJ label/registry mismatch

**ASN-0081, Shift Correctness, D-BJ**: The lemma text states "The map σ : R → Q₃ is an order-preserving bijection." The registry entry says "σ is order-preserving and injective on R."

**Problem**: The proof establishes order-preservation and injectivity; surjectivity holds trivially from `Q₃ = {σ(v) : v ∈ R}`. The label "ShiftBijectivity" matches the text but not the registry.

**Required**: Align the registry statement with the lemma text: "σ : R → Q₃ is an order-preserving bijection."

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinals of depth > 1

**Why out of scope**: The ASN correctly identifies this as an open question. At depth > 1, TA4's zero-prefix precondition fails for ordinals like `[1, ..., 1, pₘ]` (components before the action point are 1, not 0), breaking the D-SEP round-trip proof. A generalization requires either a different round-trip argument or a shift formulation that bypasses TA4. This is new algebraic territory, not an error in the depth-2 treatment.

VERDICT: REVISE
