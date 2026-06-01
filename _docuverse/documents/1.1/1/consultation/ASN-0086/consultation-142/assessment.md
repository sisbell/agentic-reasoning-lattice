# Channel Assignment — ASN-0086 review-142

**Date:** 2026-06-01 02:44

## Issue 1: R0 first-emission L1c chain — per-step zero-count bound misattributed to the seed
Reason: The fix is internal — the ASN already supplies every needed fact: TA5a's two tight bounds (`k=2 ∧ zeros≤2`, `k=1 ∧ zeros≤3`), B5 giving `zeros(inc(d,2))=3`, and `zeros(d)=2`. Reattributing each `k>0` step to its own input's zero-count is mechanical rewriting against material already present.

## Issue 2: Duplicated T12-well-formedness argument in the Nullify definition
Reason: Pure editorial deduplication of two consecutive paragraphs stating the identical T12-well-formedness claim; no design intent or implementation evidence is in question.

## Issue 3: Arity-3 scope rationale stated twice
Reason: Editorial deduplication within one definition; the scoping rationale is fully derivable from the ASN's own `A_K`/`L_K` definitions, which already fix arity-3 as the relation domain.

## Issue 4: "(b) disambiguates (c)" explanation duplicated between definition and proof
Reason: Editorial — move the load-bearing rationale to the definition and have the proof cite the clauses; the interplay is already stated in the ASN and needs no external confirmation.

## Issue 5: Roadmap inventory in the introduction
Reason: Editorial trim of a forward-pointing label inventory; the thesis and all labels are defined in place below, so no design or implementation input is needed.
