# Review of ASN-0075

I worked through the proofs (D-EXH, D-DISCR, the R-disjointness supplementary lemma, D-SUBSP), re-derived the worked example end-to-end, and checked the operational edge cases. The ASN holds up.

Key checks performed:

- **D-EXH (Three-State Exhaustion).** The "impossible row" (`a ∈ ran(M(d)) ∧ (a,d) ∉ R`) is excluded rigorously via the L14 + S3★-aux + S3★-link-contrapositive + P4★ chain, not hand-waved. Mutual exclusion is genuine: CURRENT/DELETED split on `a ∈ ran(M(d))`, and DELETED/NEVER_INCLUDED split on `(a,d) ∈ R`. The composite-boundary hypothesis is correctly identified as load-bearing (P4★ is a boundary property) and discharged structurally by D-BOUND rather than dumped on the caller.
- **D-DISCR.** The two histories pin every component of `(C,L,E,M)` identically (content value synchronized via shared `v_a`, depth fixed at `m_C = 2`, entities equal by identical K.δ prefixes) while diverging only in `R`. J0 is correctly satisfied in History 2 by placing `a` in *some* arrangement (`d'`), not its origin; P6/P7a impose no constraint forcing `a` into `d`. The one-witness-pair refutation correctly suffices to defeat a universal discriminator.
- **Worked example.** Re-ran the composite: `M(d_A) = {[1,1]↦a, [1,2]↦c}`, `M(d_B) = {[1,1]↦a, [1,2]↦b}`, classification table and output `({b},{c})` all check. K.μ~ admissibility (swap [1,2]/[1,3]) and standalone K.μ⁻/K.μ~ composites (J2/J3 self-sufficiency) are valid.
- **D-SUBSP.** Witness-impossibility for link material is fully derived (L0, L14, S3★, CL-OWN exclude both content and link V-positions), not asserted.
- **wp analysis** is non-trivial (Q0 with the three-group R-partition proof, Q1 unpacking the recoverability witness).
- **Disjointness of the two halves** is correctly shown unconditional (contradictory `ran(M(d_B))` membership), independent of D-EXH.
- **Cross-ASN references** all target foundations (0034/0036/0047); no direct ASN-0093 citation appears in the body.

No skipped operational case found: `d_A = d_B`, empty arrangements, empty R-projections, asymmetric population, deleted-from-both (no witness), and current-in-both are all handled or appropriately deferred.

## OUT_OF_SCOPE

### Topic 1: >2-document families and third-document witnesses
Open Questions 3 and 5 (content deleted from both compared documents but current in a third; generalization beyond binary pairs) are correctly deferred — they require a witness-structure not present in the binary operation.

### Topic 2: Span/run presentation of the output
Open Questions 6–7 (finite span presentation of the deletion set, witness V-order semantics) belong to a span/bundle-algebra treatment, as D-ACT already notes.

### Topic 3: Restoration operation
Open Question 8 (consuming a SHOWDELETIONS subset to reintroduce content while preserving origin/link-resolvability) is a separate operation ASN.

VERDICT: CONVERGED
