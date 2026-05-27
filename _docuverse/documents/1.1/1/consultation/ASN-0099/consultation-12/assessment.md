# Channel Assignment — ASN-0099 review-12

**Date:** 2026-05-26 19:45

## Issue 1: F4 (MatchFormulaUniqueness) witnesses reference unrealizable coverage shapes
Reason: The fix is derivable from the ASN's own references (T12 in ASN-0034, PrefixSpanCoverage in ASN-0043) and the review supplies concrete realizable witness shapes using canonical spans. No design-intent question and no implementation evidence is needed — the proof's logical structure is preserved and only the witness exhibits change to use coverage shapes the span machinery actually produces.
