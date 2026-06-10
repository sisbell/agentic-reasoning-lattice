# Channel Assignment — ASN-0119 review-24

**Date:** 2026-06-10 02:42

## Issue 1: General invariant-discharge paragraph buried in the Links section
Reason: Pure reorganization — the J/P/E/C invariant discharge is already fully written and verified in the note; the fix only relocates it from "Links" into "What is preserved." No design intent or implementation evidence is at stake, only placement.

## Issue 2: The same non-citation justification, stated twice with a forward cross-reference
Reason: Internal de-duplication. The methodological principle (ASN-0098's LP3/LP11 are proved over a transition vocabulary excluding REARRANGE_K) is already stated in the note, and the required new location ("The two streams," where REARRANGE is first distinguished from K.μ~) is specified by the review itself — nothing external is needed.

## Issue 3: "wp = true" is imprecise for a partial operation
Reason: Internal consistency fix. The note's own "Well-definedness" section already establishes REARRANGE as partial, defined exactly where R-PRE holds, so the corrected shorthand `wp = R-PRE` is derivable directly from the ASN's existing content.
