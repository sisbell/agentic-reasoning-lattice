# Rebase Review of ASN-0036

## REVISE

(none)

All foundation citations were verified against the extracted ASN-0034 formal statements:

- **S4** cites T9, T10, T10a, TA5(d), T3 — labels and formal content match. The three-case argument (same-allocator via T9, non-nesting via T10, nesting via T10a+TA5(d)+T3) is complete and correctly attributed. Registry lists all five dependencies.
- **S7** cites T4, T9, T10 — labels match. T4 for field parsing, T9+T10 for document-prefix uniqueness. Registry includes local dependencies S7a, S7b alongside foundation ones.
- **S8** cites T1, T5, T10, TA5(c), TA7a — all labels correct. TA5(c) used for ordinal-successor depth preservation in the singleton partition proof; TA7a for subspace closure in correspondence-run well-definedness; T5+T10 for cross-subspace disjointness. Registry lists all dependencies including local ones (S8-fin, S8a, S2, S8-depth).
- **D-CTG-depth** cites T0(a) and T1 — labels match. T0(a) for unbounded component values in the contradiction argument; T1(i) for ordering at the divergence point. Registry is consistent.
- **S1** references T8 as an analogy, not a derivation source — registry correctly says "corollary of S0."
- **ValidInsertionPosition** cites T3 for distinctness, OrdinalShift/TumblerAdd for depth and subspace preservation — all match foundation definitions.

No broken references, no orphaned prose, no silent dependencies, no registry inconsistencies.

VERDICT: CONVERGED
