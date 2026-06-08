# Channel Assignment — ASN-0111 review-34

**Date:** 2026-06-08 13:24

## Issue 1: Worked-example RL5 bullet restates the claim verbatim instead of verifying
Reason: Purely editorial — delete the restated conclusion and end at the coverage computation. The fix is internal to the ASN's own RL5 claim and worked-example text; no design intent or implementation evidence bears on a redundant sentence.

## Issue 2: "they are what readlink will exploit" misattributes the structural screen to the operation
Reason: The correction follows directly from the ASN's own RL0 framing (definedness is a fact about `dom(Σ.L)`, not address syntax) and the bare definition `readlink(a, Σ) ≡ Σ.L(a)`. Reassigning the clause to the reader's RL0 pre-test is derivable internally.

## Issue 3: "Ownership lives in the read key" is a top-level section for a one-sentence non-guarantee
Reason: Placement-only fix — fold the L2 `home(a)` boundary note into RL1 or the scope framing. The content and its justification (L2, ASN-0043) are already present; no external channel needed.
