# Channel Assignment — ASN-0126 review-12

**Date:** 2026-06-08 23:34

## Issue 1: Span-count-vs-coverage coalescing burden analyzed for F but skipped for Binary's G
Reason: The fix is internal. The note already discharges the F coalescing burden by citing Gregory's "no endset coalescing at all" (udanax-green stores spans per-emit, consolidation hook commented out) and Nelson's canonical single-span form — both apply to *any* endset, so they extend to Binary's G symmetrically without new evidence. The required edit is to state that the normalization burden attaches to every single-span slot (`|F|=1` for all shapes; `|G|=1` for Binary) and optionally add an abutting-G witness; all derivable from material already present.

## Issue 2: Projection base case does not anchor to ASN-0086's Σ_init
Reason: The fix is internal — a one-sentence formal assertion that `π(Σ_init) = Σ_init^{0086}` (the framework adds the registry without altering C/M/L), which the Registry-permanence section already implies. No design intent or implementation evidence is needed to close the base case.
