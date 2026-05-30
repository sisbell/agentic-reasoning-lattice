# Channel Assignment — ASN-0042 review-91

**Date:** 2026-05-30 01:25

## Issue 1: O15 condition (viii) carries an axiom-justification essay, not the axiom
Reason: Pure restructuring — the formal clause `pfx(π') = next(Σ.B, p, d)` and the necessity argument both already exist in the ASN; the fix relocates prose without needing design intent or new implementation evidence.

## Issue 2: The `delegated` definition enumerates downstream consumers instead of advancing meaning
Reason: Editorial — the signature and conjuncts are already present in the definition; removing the O18/O17b consumer commentary is internal to the ASN.

## Issue 3: The next-reachability caveat is restated in five places in different words
Reason: Deduplication of existing prose — consolidating five paraphrases into one canonical statement with cross-references requires only the ASN's own content.

## Issue 4: O17b axiom buried under implementation-corroboration essay
Reason: The formal coupling and transfer consequence are already stated; demoting the funnel narrative to one sentence is editorial trimming of content already in the ASN, requiring no fresh evidence from Gregory.

## Issue 5: Redundant precondition on O1
Reason: Internal logical fact — the `pfx` axiom's postcondition (b) already guarantees `T4(pfx(π))` unconditionally, so dropping it from O1's preconditions is derivable from the ASN alone.
