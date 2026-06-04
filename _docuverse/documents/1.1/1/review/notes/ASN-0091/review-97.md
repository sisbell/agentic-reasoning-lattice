# Review of ASN-0091

I reviewed this against the foundation claim statements, checked each RE-* derivation, traced all six worked examples at the value level, and ran the anti-bloat scan flagged for this note.

## Verification performed (no defects found)

- **Realisation argument.** Clause-by-clause discharge of K.μ~ admissibility (i)–(v) is sound. Clause (i) correctly rests on the V-position *set* being fixed by RA-dom; the net-effect split routes the collapse branch (π ≠ id, M'(d) = M(d)) to the empty-sequence realiser with Σ' = Σ.
- **RE-ran / RE-μ.** π-substitution and finite-set injectivity steps verified; the target/non-target case split is complete.
- **RE-disc / RE-proj.** Set-equality lift of the pointwise biconditional valid both directions; LP12 applied where its preconditions hold by RA-frame.
- **L-chain + run-decomposition witnesses.** The disjoint-domain successor argument is correct, and the fragmentation/coalescence/equality witnesses each check arithmetically (cardinality 2→3, 3→2, 2→2 respectively).
- **Hard invariants.** Tiling/contiguity (D-CTG★) and referential integrity (S3★) are correctly reduced to domain-fixity + RA-adm.
- **Worked examples.** Each (3-cut pivot, 4-cut swap, interior cuts, shared-image non-uniqueness, net-effect collapse) demonstrates a distinct mechanism and verifies its postconditions concretely.

## REVISE

(none)

## OUT_OF_SCOPE

The five Open Questions (link-subspace rearrangement semantics, fragmentation cardinality bound, observational equivalence under discoverability, realisability of arbitrary well-formed bijections, same-source split reconstitution) are correctly placed as future work, not gaps in this ASN.

## Anti-bloat scan

No actionable accumulation found. No "Scope/Why-the-axiom-is-needed" sub-paragraphs, no document-ordering justifications, no repeated defer-to-downstream chains, no consumer-enumeration in definitions. The "State-Component-Only Invariants" enumeration (S0, S1, P0–P2, L12, M1, C0) reads as a use-site inventory but provides genuine exhaustiveness-verification value over the bare universal principle. The six worked examples are concrete (explicitly protected from the meta-prose category) and each non-redundant. The only meta-prose is isolated preview sentences ("The clause-by-clause argument below establishes…") too minor to warrant revision.

VERDICT: CONVERGED
