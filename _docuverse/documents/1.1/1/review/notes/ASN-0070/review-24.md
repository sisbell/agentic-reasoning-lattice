# Review of ASN-0070

I reviewed this against the inverse-image core (F0/F1), the canonical-uniqueness theorem (F-canonical), the subspace correspondence (F-subspace), and all derived properties, with attention to the proofs that are easiest to hand-wave: the consecutivity characterisation, the V-restricted↔full bridge, and the existence half of canonicalisation.

## REVISE

(none)

The proofs that usually fail in resolution specifications are discharged here with explicit work:

- **Canonical existence is proved, not asserted.** Step 2a constructs the per-run span set, partitions `X` into maximal runs (with a real acyclicity argument for the partition, not a bare "single-valued ⟹ chains"), and verifies N1/N2 against run-maximality. The shape (F-canon-form) and the existence/uniqueness obligation (F-canonical) are correctly separated rather than conflated.
- **The consecutivity Characterisation** is proved in both directions, with the reverse direction carried by an induction on prefix positions that correctly closes the final component via T0 discreteness (`t_m < t''_m < t_m + 1`).
- **The V-restricted vs. full denotation gap** is handled honestly: the positivity clause is flagged as a canonical-form *convention* (with the `([1,0], δ(3,2))` vs `([1,1], δ(2,2))` witness showing the postcondition alone underdetermines `(s,c)`), and the bridge lifting S9 to `⟦·⟧_V`-equivalence is given via run reconstruction.
- **Edge cases are exercised concretely.** Seven configurations cover partial reach (a₁ unreached in Config 1), no reach, within-document multiplicity, fragmentation across a non-adjacent block of unrelated origin (F-contig instantiated at `j>0, c<n`), link-subspace resolution, cross-subspace straddle with *both* result components populated, and state-dependence via K.μ⁻ — including the F-subspace reverse direction (S3★-aux + L14) that the single-component cases never test jointly.
- **No cross-ASN violations:** every referenced ASN (0034, 0036, 0043, 0047, 0053, 0058) is a foundation; `coverage` is restated under its foundation name, not reinvented.
- **F-sound/F-complete** are correctly identified as the two halves of the postcondition equality rather than independent obligations, and the case-analysis biconditional in F-subspace's consequence (forward via S3★, reverse via S3★-aux + L14) is the non-trivial step it needs to be.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting, concurrency semantics, transclusion-lineage relations, citation-grade canonical-form mandates
**Why out of scope**: These are the ASN's own Open Questions. They concern downstream system-level contracts (what a citation artifact must guarantee, concurrency under concurrent modification, cross-document resolution relationships under shared lineage) that belong to future ASNs, not to the FOLLOWLINK query definition itself. The ASN correctly defers rather than half-specifying them.

VERDICT: CONVERGED
