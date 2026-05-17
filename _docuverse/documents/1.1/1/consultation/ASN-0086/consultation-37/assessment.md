# Channel Assignment — ASN-0086 review-37

**Date:** 2026-05-17 14:16

## Issue 1: Worked Sketch's ghost addresses violate T4
Reason: The fix is derivable from the ASN's own content. Option (a) — replacing the ghosts with `k = 3` and `r = 4` — is verifiable directly: each is a single-component tumbler with `zeros = 0`, trivially T4-valid, and the disjointness `{t : 3 ≼ t} ∩ {t : 4 ≼ t} = ∅` follows from the tumbler-prefix algebra. The author can also consult L9 in ASN-0043 to decide whether option (b) is admissible.

## Issue 2: Arrangement-modification frame citation imprecise
Reason: Pure citation-chain precision fix. The relationship between ASN-0036's transition class definitions and ASN-0043's L12/L12a is already documented in those foundation ASNs (cited throughout ASN-0086); the correction is mechanical — rewrite the inline citation to thread through both ASNs in the right order.

## Issue 3: Setup's "Maintenance protocol" paragraph length and placement
Reason: Pure presentation/reorganization fix. The content of the paragraph is already correct; only its length and position need to change. No external input needed.

## Issue 4: R7 row in "Properties Introduced" table — typology
Reason: Pure table-notation consistency fix. The R7a and R7b rows above already carry the substantive typing; the author chooses between omitting R7's composite row or coining a single category. No external input needed.

## Issue 5: "Allocator-state commitment" paragraph density
Reason: Pure presentation fix — add a signalling sentence flagging that the sparse-allocator interpretation is a load-bearing design commitment relied on by R0 Step 2 Case A. The substantive content is already in the main body and Appendix A.1; only the signposting needs strengthening.
