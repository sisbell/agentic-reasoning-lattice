# Review of ASN-0122

This is a mature, mathematically solid note. I checked the proofs case by case and verified the worked example pair-by-pair; the substance is converged. The address-vs-value derivation (X1/X2), the locality factoring (X5), the maximal-run canonical form (X11), the transport lemma and its four edit instantiations (X-T/X7), the chain-invisibility composition (X6), and the interval-clipping bound (X4c) all hold, with preconditions correctly tracked (the explicit injectivity discharge for the shifting contraction in X7(iii) and the S8-depth/TS2 pairing in X11 are exactly the spots that are usually hand-waved, and they are not). The six-element worked example genuinely exercises fan-out, the tie-break, clipping, and the self-comparison boundary; every count is forced. The two implementation deficiencies are adjudicated against the abstract claims rather than excused.

The remaining findings are prose-level, surfaced under the note's `review-mode.anti-bloat` mandate.

## REVISE

### Issue 1: X12's closing sentence restates the R4 bullet
**ASN-0122, "The Operation" (X12)**: The R4 bullet already says "a conforming implementation may emit any presentation satisfying R1–R3 — finer-than-maximal pairs, a different packing of the record — since report equivalence is denotational." The sentence following the Frame bullet then re-says it: "Conformance is thus denotational, exactly as for span-sets: granularity and packing are free (R4 is the reference, not an obligation), while soundness, completeness, confinement, and the determinism of the chosen presentation (R1–R3) are non-negotiable."
**Problem**: Two passages in the same contract assert the same binding/non-binding split — "denotational equivalence," "any presentation satisfying R1–R3," "R4 is the reference not an obligation." The closing sentence's only non-duplicated content is the five-word analogy "exactly as for span-sets." This is the "two paragraphs say the same thing in different words" pattern the anti-bloat mode names, sitting in the one slot (the operation contract) where each clause should carry distinct weight.
**Required**: Cut the closing sentence, or reduce it to the new connection alone (e.g., fold "exactly as for span-sets" into the R4 bullet's existing "report equivalence is denotational" clause and drop the rest).

### Issue 2: Residual self-referential / defensive framing
**ASN-0122, "The Pair" (the n-remark) and "Stability" (X6 (b))**: Two phrases narrate the writing or defend against a foundation doctrine rather than advancing the claim:
- "A remark on `n`. Tumbler differences are not counts (ASN-0034), **and we have not violated that doctrine**: `n` counts lockstep steps…"
- "Steps compose, under two premises **we state rather than leave implicit**."
**Problem**: "and we have not violated that doctrine" is a defensive justification; "we state rather than leave implicit" is process narration. In both cases the surrounding content is substantive (the D-SEQ★-density argument that legitimizes the count; the two genuinely-needed premises for X6(b)), but the framing is the residue the recent strip pass is targeting, and a reader skips past it to reach the claim.
**Required**: Lead each with the positive content. For the n-remark: "`n` counts lockstep steps, not an address-space difference; the count is well-defined because D-SEQ★ makes content positions dense." For X6(b): "Steps compose under two premises:" — drop "we state rather than leave implicit."

## OUT_OF_SCOPE

The future-facing topics (a derived/cached correspondence index and its consistency contract, n-way alignment composed from pairwise reports, multiplicity-annotated matching reports, interoperable pair granularity) are already and correctly held in the Open Questions section rather than claimed. No additional out-of-scope material needs raising.

VERDICT: REVISE
