# Channel Assignment — ASN-0086 review-170

**Date:** 2026-06-01 07:18

## Issue 1: R7a motivation is an essay justifying the lemma's retention, not its content
Reason: Purely editorial — the fix is to delete retention-justification prose and keep the lemma statement plus one scope sentence. The udanax-green fact is already stated in the ASN; no design-intent or fresh implementation evidence is needed to trim framing.

## Issue 2: The "not exercised, retained for closure value" claim is duplicated across two sections that defer to each other
Reason: Internal deduplication — consolidate the `m = 1` instantiation fact to one site and drop the cross-reference. Derivable from the ASN's own structure.

## Issue 3: Reduction-corollary proof re-litigates R7a's role instead of citing it
Reason: Internal — end the corollary at the reduction and replace the narration with a one-clause citation of R7a. No external channel required.
