# Channel Assignment — ASN-0111 review-26

**Date:** 2026-06-08 12:30

## Issue 1: The same operation-contrast is delivered three times
Reason: Pure editorial deduplication — the read-vs-search/follow/count contrast is already stated in the ASN's intro; deciding which copies to cut requires no design intent or implementation evidence.

## Issue 2: Essay framing in "Deriving the read"
Reason: Deletion of a meta-prose sentence that advances no reasoning; derivable from the ASN alone.

## Issue 3: A full section devoted to a fact the operation does not deliver
Reason: The fix (compress to a one-line remark citing L2, or attach a labeled claim) is internal — L2 is already cited in the ASN and the home-from-key derivation is fully present. Whether ownership-from-key should be a guarantee this operation asserts is a design-intent question for Nelson.
Nelson question: Is recovering a link's owning home document from its address key intended to be a guaranteed part of the read interface, or merely an incidental consequence of the address layout?

## Issue 4: Defensive/exhaustiveness prose in RL2
Reason: Trimming defensive restatement of L3; the arity-N content is already carried by the formal statement, so the fix is derivable from the ASN alone.

## Issue 5: Recap sentence adds nothing
Reason: Cut or fold a recap of three adjacent claims; purely internal editorial choice.
