# Channel Assignment — ASN-0111 review-5

**Date:** 2026-06-07 23:26

## Issue 1: RL6 (nesting fidelity) is never verified against a concrete instance
Reason: The fix only extends the existing worked example with a link-address span; RL6, the L13 canonical reflexive span, coverage semantics, and address-faithfulness are all already specified in the ASN, so the instance is constructible from its own content.

## Issue 2: RL2's formal statement is subsumed by RL1
Reason: The fix is to re-express RL2's independent content (slot-position/arity as a returned-value primitive via L6) or fold it into RL1; L6 is already cited and the distinction is internal to the ASN's own claims.
