# Integration Review of ASN-0036

## REVISE

(none)

The four integrated properties and their proofs are sound:

**D-CTG**: Quantifier structure is correct — restricting intermediates to same-depth, same-subspace tumblers is necessary for consistency with S8-depth. The `#v = #u` guard prevents forcing different-depth tumblers into V_S(d), which would violate S8-depth.

**D-CTG-depth**: The proof by contradiction is complete. The construction of w with wⱼ₊₁ = n correctly establishes v₁ < w < v₂ for all cases (j ranging over {2, …, m−1}), including the boundary cases j = 2 and j = m−1. The appeal to infinitely many valid n (via T0(a)) to contradict S8-fin is valid. The proof handles all depths m ≥ 3 uniformly — at m = 3, only j = 2 applies; at m = 4, j ∈ {2, 3}; the same construction covers each. The singleton and empty-set boundary cases are handled (vacuously satisfied).

**D-MIN**: Correctly stated as a design requirement, not derived. The minimum's existence follows from V_S(d) being non-empty and finite under a total order.

**D-SEQ**: The derivation chain is complete: D-CTG-depth fixes the shared prefix, D-MIN pins those shared values to 1, D-CTG forbids gaps in the last component, D-MIN gives minimum k = 1, S8-fin bounds the maximum. The depth-2 case (where D-CTG-depth is vacuous) is handled correctly. Registry dependencies (D-CTG, D-MIN, S8-fin, S8-depth) transitively cover D-CTG-depth.

Integration quality: placement after S8/S8-depth (dependencies) and before S9 (independent) is correct. Notation (V_S(d), M(d), subspace(v)) is consistent with the rest of the document. Registry entries have correct labels, types, statuses, and dependency lists. No dangling or broken references. The concrete examples correctly illustrate both valid states and violations.

VERDICT: CONVERGED
