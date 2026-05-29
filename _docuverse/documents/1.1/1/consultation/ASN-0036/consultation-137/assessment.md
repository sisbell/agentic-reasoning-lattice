# Channel Assignment — ASN-0036 review-137

**Date:** 2026-05-29 00:20

## Issue 1: Maximal-run deferral repeated across three sites
Reason: Purely editorial deduplication of a hedge that already appears in Open Questions; the scope of S8 (singleton decomposition only) is fully stated in the ASN itself, so the fix is derivable from existing content with no design-intent or implementation evidence needed.

## Issue 2: Meta-prose occupying the S8 postcondition slot, and slightly misdescribing the claim
Reason: The correction is a logical one — for `nⱼ = 1` the quantifier `(A k : 0 ≤ k < nⱼ)` ranges over `{0}`, so conjunct (b) is fully satisfied — and follows directly from the ASN's own definitions; restating the postcondition plainly requires no external channel.

## Issue 3: Roadmap/tool-inventory paragraph before the S8 proof
Reason: Deleting a redundant preview that the proof body already covers is internal to the document; the proof already names the lemma, T5, and T10 at their use sites, so no design or implementation input is required.
