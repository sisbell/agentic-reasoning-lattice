# Review of ASN-0075

I checked D-EXH (exhaustion/exclusion), D-DISCR (necessity), the worked example, the wp derivations (Q0/Q1 and the R-disjointness lemma), and the subspace/identity/origin claims. Each holds up under the standards I apply.

## Verification notes

- **D-EXH** correctly isolates the "impossible" row (`a ∈ ran(M(d)) ∧ (a,d) ∉ R`) via the L14 + S3★-aux + S3★-contrapositive + P4★ chain, and the boundary hypothesis that activates P4★ is discharged structurally by D-BOUND rather than hand-waved. Mutual exclusion and exhaustiveness are both shown row-by-row, not by "similarly."
- **D-DISCR** is sharp: Histories 1 and 2 pin every component of `(C, L, E, M)` identically (synchronised content value `v_a`, identical K.δ entity sequence with E permanence, both `M(d) = ∅`, both `M(d') = {v'↦a}`) and differ only in `R`. Composite bundling correctly respects J0/J1★. One counterexample suffices to refute a universal discriminating function.
- **Worked example** concretely verifies D-EXH, D-IDENT, D-ORIG, D-SYM against a divergent-fork state, including the K.μ~-then-K.μ⁻ reordering needed to delete `b` from a non-trailing position. The classification table is internally consistent with the resulting `M`/`R`.
- **wp analysis** is non-trivial: Q0's vacuity is backed by the R-disjointness supplementary lemma with a genuine three-group case split, each group falsifying both conjuncts (and correctly distinguishing the P4★-dependent CURRENT-exclusion from the direct DELETED-first-conjunct failure).
- **Disjointness of the two report halves** is established unconditionally (contradictory range-membership on `M(d_B)`), correctly noted as needing neither D-EXH nor boundary.
- **D-SUBSP** derives witness-impossibility for link material from L0/L14/S3★/CL-OWN rather than asserting it; the content/link V-position subcases are both excluded.
- **Cross-ASN references** are confined to foundation ASNs (0034, 0036, 0047) — no Standard 7 violation. No notation is reinvented.
- **Boundary cases** (empty arrangements, self-comparison, asymmetric population) are addressed, and DELETED is semantically faithful to "was present, now absent" via P4a + J1★ + K.μ~ range-invariance.

No hand-waves, no proof-by-checkmark, no skipped invariant conjuncts, and a concrete example is present.

## OUT_OF_SCOPE

### Topic 1: Link-subspace and multi-document deletion analysis
The Open Questions defer per-document link deletion, three-document witnesses, and >2-document families. These are correctly deferred — new territory, not errors here.

### Topic 2: Span/run presentation of the output set
The decomposition of the I-address output into contiguous same-origin spans is explicitly handed to a span/bundle-algebra treatment (D-ACT). Appropriate deferral.

VERDICT: CONVERGED
