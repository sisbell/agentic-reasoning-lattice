# Channel Assignment — ASN-0084 review-83

**Date:** 2026-05-30 17:37

## Issue 1: The `+` operator is defined only for depth-2 V-positions but used on I-addresses
Reason: The fix is internal — it restates ASN-0036's S8 `shift` convention (already cited) and notes TS3's depth-agnosticism (ASN-0034, already cited). No design intent or implementation evidence is required; the math holds for any tumbler and the cited foundations supply everything.
