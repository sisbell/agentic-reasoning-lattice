# Channel Assignment — ASN-0119 review-21

**Date:** 2026-06-10 01:55

## Issue 1: The "cuts resolve against one arrangement" claim is stated twice, the first as a self-described preview of the second
Reason: Purely editorial deduplication — both passages already exist in the ASN, and the fix (drop the preview framing in "Cuts and regions," let "Atomicity" carry the claim and its consequence) is a rearrangement of present text. No design-intent or implementation evidence bears on it.

## Issue 2: Reading-process narration in structural slots
Reason: Internal — the underlying claims (the address-vs-position/value-vs-key distinction and RA1's `ran(M'(d)) = ran(M(d))`) are already stated in the ASN; the fix only strips the "we will be watching"/"we will lean on" meta-narration wrapping them, requiring no external input.

## Issue 3: The "fully accounted for" invariant census omits S3★-aux
Reason: Derivable from the ASN's own content — RA2 fixes the key set `dom(M'(d)) = dom(M(d))`, the body already states `subspace(·)` is intrinsic to `v`, and the universal principle "every reachable-state invariant constraining this set alone is inherited verbatim" is already established; adding S3★-aux (and optionally naming the E-family) applies that existing argument to one more named conjunct the reviewer has already identified.
