# Channel Assignment — ASN-0100 review-74

**Date:** 2026-06-05 04:12

## Issue 1: Position Constraints section restates already-established precondition material
Reason: Purely editorial deduplication — the precondition predicates, `m := #p` binding, and K.μ⁻-omission are all already fixed in §The Operation's Inputs and §Formal Contract; the only new content (j → region-emptiness mapping) is present in the ASN. Internal trim, no channel needed.

## Issue 2: INS.proj is deferred to from multiple sections to the same downstream location
Reason: Restructuring task — the `d' ≠ d` branch is already derived in §Coverage as a one-line LP4 composition; consolidating the deferrals requires only moving existing ASN content, no design intent or implementation evidence.

## Issue 3: ActivatedEmission preservation is stated twice in the same breath
Reason: The group sentence and the trailing "ActivatedEmission in particular…" sentence give the identical `E' = E` frame argument, both already in the ASN; deciding whether to drop the repetition or single out a distinguishing fact is internal editorial judgment.
