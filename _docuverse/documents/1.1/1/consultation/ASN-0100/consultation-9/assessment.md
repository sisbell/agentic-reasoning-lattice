# Channel Assignment — ASN-0100 review-9

**Date:** 2026-05-27 15:07

## Issue 1: "Shifting both V-start and width by n" misdescribes the Shifted-right blocks
Reason: Pure wording correction derivable from the ASN's own per-region clauses (INS.M-shift maps `shift(v, n) ↦ M(d)(v)` — same image, same position count) and block semantics in ASN-0058. No design intent or implementation evidence required.

## Issue 2: Pre-state decomposition need not transfer "unchanged" across the insertion boundary
Reason: The fix follows directly from M2/M7 block decomposition semantics in ASN-0058 and INSERT's own Left/Insertion/Shifted-right partition by V-position relative to `p`. Either splitting pre-state blocks at `p` or relying on M2's existence applied to the post-state is internal restructuring.
