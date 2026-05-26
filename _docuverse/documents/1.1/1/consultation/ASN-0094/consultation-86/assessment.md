# Channel Assignment — ASN-0094 review-86

**Date:** 2026-05-25 19:54

```
## Issue 1: T5 citation does not justify the prefix-closure / half-open interval identification
Reason: This is a proof-citation choice among three options the review enumerates (T12/PrefixSpanCoverage equivalence, explicit T1 case analysis, or sidestepping via T12's bounded reading) — all using foundational axioms already cited from ASN-0034 and ASN-0043. The fix is derivable from the ASN's existing axiomatic content; no design intent or implementation evidence is needed.
```

```
## Issue 2: Sh4 suppression probe absent from three idempotent walkthroughs
Reason: The Sh4 suppression probe pattern is already exhibited in the BundledDirectedPair and Resolution walkthroughs; the fix is to add parallel demonstrations at Classifier, Tuple-Classifier, and Provenance using the established Sh4 idempotency contract. Purely mechanical extension of existing ASN content.
```
