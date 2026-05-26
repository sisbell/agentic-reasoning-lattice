# Channel Assignment — ASN-0098 review-23

**Date:** 2026-05-26 04:35

## Issue 1: LP4 listed twice in working reference frame paragraph
Reason: Purely editorial redundancy. The fix is a textual choice between two enumerations both already present in the paragraph; no design intent or implementation evidence is needed.

## Issue 2: Trace example leaves i₀ structurally unspecified
Reason: The ASN already establishes all structural machinery (chain elements, anchors, half-open T1 intervals, PrefixSpanCoverage) needed to pin i₀ to a concrete choice. Selecting one that makes coverage(e₁) ⊇ {i₁..i₄} mechanically verifiable is internal to the ASN.
