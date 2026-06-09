# Channel Assignment — ASN-0126 review-42

**Date:** 2026-06-09 10:58

## Issue 1: "R must be Binary" is a non-sequitur
Reason: Internal. The note already states the load-bearing justification ("Only *discontiguous* multi-target retraction falls to the front end") — Binary forbids gated `|G| ≥ 2` retraction that Multi would admit. The fix reorders existing reasoning to present Binary as the framework's chosen registration, not a span-count necessity; no external intent or implementation evidence is required.

## Issue 2: "Sh-conf consults no state-indexed set" is restated ~5 times
Reason: Internal. Pure deduplication — state the rule once at Shape-conformance, reference by label from P5, and have the Worked illustration assert only the verdict. No design-intent or implementation question bears on which copy to keep.

## Issue 3: Duplicate forward-deferrals to "Worked illustration"
Reason: Internal. Editorial removal of one of two adjacent forward pointers to the same downstream example; nothing about intent or the udanax-green code is at issue.

## Issue 4: domain-discharge ordering explained, then re-pointed redundantly
Reason: Internal. Collapsing two parenthetical back-references to a single reference where the wp first relies on the ordering — a self-contained restructuring of the note's own derivation.
