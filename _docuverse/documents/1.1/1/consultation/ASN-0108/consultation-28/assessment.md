# Channel Assignment — ASN-0108 review-28

**Date:** 2026-06-13 02:02

## Issue 1: W9b's termination derivation assumes cursor-monotonicity that clause 1 alone does not supply — and the note's own W8 supplies the counterexample
Reason: Internal — this is proof repair using machinery already in the note. The gap (clause 1 from W5 transports ordering only across both-states links, while W8 admits orphaned cursors) and its remedies (add a value-totality hypothesis, or prove cursor-monotonicity at the resume state handling the orphaned-intermediate case) are entirely derivable from W5, the key-conditions ladder, and W8; no design intent or implementation evidence bears on the logic.

## Issue 2: "Orphaned (LP17)" over-states single-document Match-loss
Reason: Internal — a cross-ASN citation correction. The note's own definition of `Match` as single-document `findlinks_V`/F-FULL (`{a : discoverable_from(a, d_q, Σ)}`), together with the already-referenced formal statements of LP12/LP17 (ASN-0098) and D-NONMONO's K.μ⁻ (ASN-0127), determines that per-`d_q` loss is LP12/K.μ⁻ and that LP17 is the strictly stronger global ghosthood; the correct attribution is fixed by formal content already present.

## Issue 3: W5's claim statement buries its content under a four-way forward-reference tour
Reason: Internal — pure anti-bloat editorial trim. Reducing W5's statement to "clause 1 ranges over both-states links" and removing the deferral tour to W6/W7/W9b/D-ZERO is a prose-organization fix needing no external input.

## Issue 4: The "W6 blind spot" and the value-totality/state-stability point are each re-explained across multiple sections
Reason: Internal — pure anti-bloat deduplication. Stating each concept once at its home claim (W6, W8) and referencing by label elsewhere requires no design intent or implementation evidence.
