# Channel Assignment — ASN-0126 review-9

**Date:** 2026-06-08 22:02

## Issue 1: Registry-entry count mismatch in the worked illustration
Reason: Pure internal bookkeeping fix — the prose says "four" but five bullets follow; correcting the count (or relocating `retract`) requires only the ASN's own text, no design intent or implementation evidence.

## Issue 2: The singleton-coverage characterization names an empty class
Reason: The correction follows from PrefixSpanCoverage (ASN-0043), already cited in the note: `coverage({(a, δ(1, #a))}) = {t : a ≼ t}` is always infinite over `T` and no tumbler is childless, so the empty-class characterization is derivable and fixable from the ASN's own definitional inheritance — no channel needed.
