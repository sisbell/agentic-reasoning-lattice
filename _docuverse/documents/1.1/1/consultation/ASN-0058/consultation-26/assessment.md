# Channel Assignment — ASN-0058 review-26

**Date:** 2026-05-14 20:29

## Issue 1: M2's proof under-specifies the vocabulary translation
Reason: The fix is purely expositional — spell out the B1/B2/B3 ↔ S8(a)/S8(b) correspondence and cite S8-depth/S8a for the range coincidence. All facts are already present in the ASN and its citations to ASN-0036; no design intent or implementation evidence required.

## Issue 2: M7's overlap case proof is overly dense
Reason: The fix is internal restructuring — extract the overlap-impossibility argument as a named sub-lemma with numbered steps. The proof content is already correct; only the presentation needs to be reorganized, which is derivable from the existing ASN material.

## Issue 3: M12 canonical uniqueness proof packs multiple intricate sub-arguments
Reason: The fix is internal abstraction — extract M12a and M12b as named sub-lemmas to factor the recurring "depth-m V-positions cannot V-overlap" skeleton out of M7 and M12. This is pure proof refactoring derivable from existing content; no external input needed.
