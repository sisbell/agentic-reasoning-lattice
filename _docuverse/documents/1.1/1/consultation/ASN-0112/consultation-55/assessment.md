# Channel Assignment — ASN-0112 review-55

**Date:** 2026-06-10 22:49

## Issue 1: V9's biconditional has an unproven direction
Reason: The fix is internal — the review itself sketches the complete proof route (TS2 shift injectivity, the D1 round-trip case, the TumblerSub componentwise case with S8a zero-freeness), all of which are lemmas the ASN already cites from ASN-0034. No design-intent or implementation question remains; the revision is either writing out that proof or weakening the claim, both derivable from existing content.

## Issue 2: V12 cites V8 for a fact V8 does not state
Reason: This is a citation correction — the permanence of `d` is already established as P1 (EntityPermanence, ASN-0047), and the review names the exact replacement. The fix requires no new evidence or intent clarification.
