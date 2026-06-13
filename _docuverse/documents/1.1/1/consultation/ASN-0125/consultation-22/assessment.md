# Channel Assignment — ASN-0125 review-22

**Date:** 2026-06-13 15:24

## Issue 1: The currency query can return retracted versions, and EL14(d)'s disclosure does not surface this
Reason: The fix is internal — the independence consequence follows directly from Df-SUCC (succ_o filters on the claim address `addr(e)`, never on `old(e)`/`new(e)`) combined with EL9(3)'s already-established axis independence, and the (a)/(b) framing choice is settled by the ASN's own "disclosure, not decision" stance in EL14(d). No design intent beyond EL9's three-axes commitment and no implementation evidence is required, since the review already establishes the reachability of the Nullify-the-successor sequence from EL-DM.
