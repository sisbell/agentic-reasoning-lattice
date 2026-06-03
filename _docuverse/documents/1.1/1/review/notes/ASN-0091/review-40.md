# Review of ASN-0091

I checked the abstract Vstream-only class definition, the REARRANGE_K realisation argument, every per-invariant discharge, the four worked examples, and the multi-step composition section. I focused on the places these specifications usually fail: hidden circularity in the admissibility discharge, boundary cases, the bijection-non-uniqueness handling, and foundation-citation discipline.

## REVISE

None.

The areas most likely to harbor a defect all hold up under scrutiny:

- **No circularity in the RA-adm discharge.** S2 at Σ' is proven from RA-dom + RA-π bijectivity + pre-state S2 alone; S3★ at Σ' is proven constructively from fact (b) (R-PPERM/R-SPERM subspace-confinement), not from RA-adm; clause (iii) length-preservation is anchored on CS4 + ordinal-shift length identity independent of RA-dom. The ASN explicitly flags and avoids the K.μ~-FIX cycle by sourcing RA-dom directly from the ASN-0084 postcondition. The dependency chains terminate at structural facts.

- **π ≠ id vs M'(d) ≠ M(d) is handled correctly.** The rotation/swap-invariance criteria (period gcd(w_α,w_β) for the pivot; positional α/β equality for the swap), the period-2 worked counterexample, and the collapse-case routing to the identity composite are all sound. The collapse case correctly yields Σ' = Σ via RA-π + RA-dom + RA-frame.

- **Boundary cases covered.** Empty arrangement (vacuous abstract / excluded by R-PRE(iv)∧CS2 for REARRANGE_K), interior cuts exercising R-EXT (third example), and shared I-addresses with multiple valid π (fourth example) are each concretely traced. RE-proj uniformity across witnesses is correctly established as a state-determined identity.

- **Worked examples verified numerically.** I recomputed the 3-cut pivot, 4-cut swap, interior-cut, and two-step (+,−) composition run cardinalities and coverage/projection witnesses; each matches. ChainDisjointAdjacency's structural argument (via TA5(c) chain-successor identity + T3, with the T10a.6 alternative) holds uniformly including the proper-prefix length case.

- **Citation discipline clean.** Every external reference is to a foundation ASN (0034, 0036, 0047, 0058, 0084, 0093, 0098); no non-foundation cross-reference and no reinvented foundation notation.

## OUT_OF_SCOPE

The Open Questions (link-subspace rearrangement semantics, same-source span-split transclusion guarantees, observational equivalence at discoverability level, run-cardinality increase bounds, completeness of cut-sequence rearrangements) are correctly deferred to future ASNs rather than treated as gaps here.

VERDICT: CONVERGED
