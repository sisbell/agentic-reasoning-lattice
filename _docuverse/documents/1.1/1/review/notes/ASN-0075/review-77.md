# Review of ASN-0075

The mathematics is sound. D-WIT, D-EXH, D-DISCR, and D-DISJ are correctly proved with proper boundary scoping (P4★ at composite boundaries), the wp analysis is non-trivial (distinguishing computability-precondition from meaning-precondition), the worked example verifies the key classification postconditions, and edge cases (self-comparison, empty arrangements, disjoint provenance, asymmetric population) are covered. Cross-references are all to foundation ASNs (0034, 0036, 0047). The remaining issues are anti-bloat, consistent with this note's `review-mode.anti-bloat` classifier and the prior REVISE cycles on observationality and use-site padding.

## REVISE

### Issue 1: Observationality "reads/computes/returns" stated twice
**ASN-0075, SHOWDELETIONS Definition section and D-OBS section**: Definition section closes with "The definition reads `M(d_A)`, `M(d_B)`, and `R` to compute the two output sets and returns them." D-OBS restates: "The operation reads `M(d_A)`, `M(d_B)`, and `R`; it computes the output sets; it returns them."
**Problem**: Two paragraphs say the same thing in different words — exactly the duplication pattern this note flags. The reads/computes/returns content is the observationality claim and belongs solely in D-OBS; the Definition section only needs to fix the operation as the comprehension pair.
**Required**: Drop the trailing sentence from the Definition section; let D-OBS carry the reads/computes/returns statement.

### Issue 2: D-ORIG justification carries a redundant illustration
**ASN-0075, "Origin Traceability" → Justification (second paragraph)**: "The user-facing meaning: any returned address self-identifies its home document. When `d_A` and `d_B` were derived from a common ancestor `d_C`, content inherited from `d_C` and later deleted from `d_A` carries `origin(a) = d_C`..."
**Problem**: The actual justification is the first paragraph (S7 gives `origin` on `dom(C)`). The second paragraph is illustrative example content whose home is the worked example, which already exercises `origin(b) = origin(c) = d_A`. Per the placement rule, example prose in a claim-justification slot should be flagged for placement.
**Required**: Remove the second paragraph (or fold any unique point into the worked example); the S7 sentence discharges D-ORIG.

## OUT_OF_SCOPE

### Topic 1: Restoration, concurrency, multi-document witnesses, span-presentation
These appear in Open Questions and are correctly deferred — restoration consuming SHOWDELETIONS output, concurrent-transition consistency, >2-document generalization, and finite span presentation of deletion sets are future-ASN territory, not gaps in this one.

VERDICT: REVISE
