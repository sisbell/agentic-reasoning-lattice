# Review of ASN-0075

I checked the proofs (D-WIT, D-EXH, D-DISCR, D-NEED, D-DISJ), the wp analysis, the worked example, and the observational claims. The formal content is sound: D-WIT correctly conditions on composite-boundary state to invoke P4★; D-EXH's cross-product exclusion is valid; the D-DISCR two-history construction genuinely agrees on (C,L,E,M) and differs only on R; the worked example classifies all six pairs correctly and the SHOWDELETIONS output ({b},{c}) checks out. Edge cases (self-comparison, empty arrangements, disjoint provenance) are covered. Cross-references stay within the foundation set.

The findings below are anti-bloat: redundant restatement of the same property across sections.

## REVISE

### Issue 1: The "witness makes the deletion recoverable" theme is stated three times
**ASN-0075, output-set intro / wp Q1 / worked-example closing paragraph**:
- intro: "the still-current copy in the partner document is the *witness* that makes the deletion observable as recoverable."
- wp Q1: "The last conjunct (presence in `d_B`) is what makes the report *recoverable* — every reported deletion has a concrete witness in the partner document."
- worked example: "the example also illustrates the structural significance of the witness: `b` is reported as deleted from `d_A` only because `d_B` still holds it…"

**Problem**: The abstract claim (the partner's surviving copy is the witness that makes a deletion recoverable) is asserted three times in nearly identical terms. The worked-example version adds the concrete "if `d_B` had also deleted `b`" elaboration, which is illustrative; the two abstract restatements (intro + wp Q1) carry no additional content. A precise reader meets the same sentence three times.
**Required**: Keep the witness framing at one site (the output-set intro is the natural home) and the concrete elaboration in the worked example; drop the duplicate abstract sentence in the wp Q1 paragraph, leaving only the operational reading of the existential.

### Issue 2: D-RECONS restates a consequence already drawn under D-OBS
**ASN-0075, D-OBS consequences vs. D-RECONS**: D-OBS lists as a consequence "a later invocation after intervening state changes correctly reflects the new state," and D-RECONS then claims "The output depends only on the current state `Σ`. It does not depend on the particular sequence of transitions by which `Σ` was reached."
**Problem**: "Reflects the new state" and "depends only on the current state" are the same state-functional property phrased twice — once as an unlabeled D-OBS consequence, once as a standalone claim. The two sit in adjacent sections and force the reader to confirm they are not distinct guarantees.
**Required**: Drop the overlapping D-OBS consequence (or the D-RECONS prose) so the state-functional/history-independence property is asserted once. The genuinely distinct D-OBS consequences (repeatability, commutation with other queries) can stay.

## OUT_OF_SCOPE

The Open Questions correctly defer restoration, multi-document families, concurrent-transition consistency, and span-presentation — these are future operations, not gaps in this ASN. No action needed.

VERDICT: REVISE
