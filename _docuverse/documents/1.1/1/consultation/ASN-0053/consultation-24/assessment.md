# Channel Assignment — ASN-0053 review-24

**Date:** 2026-05-13 14:56

```
## Issue 1: Foundation reference name inconsistency
Reason: Pure naming fix to match foundation ASN-0034's canonical name `TumblerSub`. Derivable from the foundation reference itself.
```

```
## Issue 2: SC exhaustiveness uses WLOG without spelling out symmetric branches
Reason: Proof structure issue. The SC definition is explicitly symmetric in α, β via "or symmetrically" clauses, so the WLOG justification is internal to the ASN.
```

```
## Issue 3: S9 Case 2 handles only one inequality direction
Reason: Proof completeness fix. The symmetric branch follows by swapping Σ̂₁ and Σ̂₂ — a structural symmetry already present in the proof setup.
```

```
## Issue 4: S11 elides the decomposition derivation
Reason: Element-chasing derivation from the definitions of ⟦α⟧, ⟦β⟧, and set difference. S11c performs this style explicitly; the same pattern applies internally.
```

```
## Issue 5: S3b handles only one direction of adjacency
Reason: The second adjacency direction follows from S3a's commutativity result, which is already established in the ASN. Internal fix.
```

```
## Issue 6: Width recovery cites D2 without checking preconditions
Reason: D2's preconditions (divergence bound, length ordering) are discharged by level-uniformity (S6) and T12 (ASN-0034) — both already present in the ASN and its cited foundation.
```
