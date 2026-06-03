# Channel Assignment — ASN-0071 review-60

**Date:** 2026-06-03 11:22

## Issue 1: `vspec`/`iaddrs` reinvent ASN-0058's content-reference machinery without acknowledging the relaxation
Reason: Internal fix — the relaxation rationale (search-direction needs partial coverage and coarse/cross-depth anchors) is already grounded in the ASN's own framing and its cited LM 4/63 and 4/38 quotes, and the relation to ASN-0058's `ContentReference`/`resolve` is a cross-referencing task against an already-cited foundation. No design-intent or implementation evidence is needed.

## Issue 2: Currency deferral duplicates Open Question 1 (anti-bloat)
Reason: Internal fix — purely removing the duplicated trailing deferral sentence; the Open Question already carries it. No external channel needed.
