# Review of ASN-0070

I worked through the load-bearing proofs: F-canonical (both existence via the maximal-run construction in Step 2a and uniqueness via the consecutivity Characterisation and the ⟦·⟧_V→⟦·⟧ bridge), F-subspace's biconditional (forward via S3★, reverse via S3★-aux + L14), F-contig (M1 monotonicity + T12 order-convexity), and the six worked configurations.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN confines itself to the FOLLOWLINK query and correctly defers concurrency, partial-reach reporting, transclusion-lineage relationships, and content-retrieval coupling to its Open Questions rather than asserting claims about them.)

Notes from the verification, none rising to a revision:

- **Step 1, case `k = m_S(d)`, both inclusions** are fully discharged (forward by explicit witness construction, reverse by least-divergence contradiction against the prefix-copy region) — no "by symmetry" gap. The `k < m` exclusion correctly invokes T0(a) unboundedness to force infinite `⟦σ⟧_V`, ruling out non-terminal action points by the finiteness criterion.
- **The Characterisation's reverse induction** (`t < t'' < t'` ⟹ contradiction) exhausts all four `(q, q')` divergence cases and closes the position-`m` step via T0 discreteness — sound.
- **Maximal-run partition** is justified by single-valued successor/predecessor + acyclicity from T1 irreflexivity/transitivity, not assumed.
- **M-int citation** in "Computation via Decomposition" applies only to `v+k ∈ V(β) ⊆ dom(M(d))` (with `v+k < v+n` by TS5), satisfying M-int's domain hypothesis; the per-subspace block partition follows.
- **F-multi** correctly separates the implication (F0+F1+F-subspace) from reachability (K.μ⁺ content-side non-injectivity), and confines S5 to the abstract-cardinality point — the distinction the prior reviews demanded is honored.
- **Existence** of an admissible representation (Step 2a) is proved, not merely shape-constrained, so F1's postcondition is dischargeable and F-det/F-empty rest on a real result.

One minor prose imprecision worth the author's eye (not a revision): in "Multi-Document Reach," "links that resolved against `d` will resolve … against `d'`" when `ran(M(d'))` overlaps `ran(M(d))` is an overstatement — overlap of ranges does not guarantee the overlap includes a given link's coverage. The surrounding hedges ("possibly," "significantly") keep it informal, but the sentence reads stronger than the inverse-image relation supports.

VERDICT: CONVERGED
