# Channel Assignment — ASN-0086 review-15

**Date:** 2026-05-16 21:38

## Issue 1: R0a antichain corollary terminology inconsistent with worked example
Reason: Pure internal consistency fix — the worked example and R0 proof already use the "depth-2 link allocator" terminology; R0a's corollary simply needs to align with it. No external evidence required.

## Issue 2: R0 Step 2 Case A freshness justification conflates spawn with deposit
Reason: The distinction between allocator enumeration and `dom(Σ.L)` is already established in the note's own substrate-primitive framing ("intermediate addresses along the chain are not required to be in `dom(Σ.L)`"). The fix follows directly from Case A's hypothesis and L1a, both internal to the ASN.

## Issue 3: Nullify's choice of home(a) is a convention without justification
Reason: This is a design-intent and implementation question — whether retractions are meant to be sited at the target's home (Nelson) and how the udanax-green code actually homes retraction-like structures (Gregory). Both inform whether `home(a)` should be canonical or caller-supplied.
Nelson question: In Nelson's link/retraction design, does a retraction belong to the same document as the link it retracts, or is the retraction's ownership independent of its target?
Gregory question: In udanax-green, when a link is retracted or its analogous lifecycle operation invoked, where is the retracting structure homed — at the target link's home document, at a caller-specified document, or at a system-wide location?

## Issue 4: R5's "no opposing invariant" enumeration omits ASN-0036 and ASN-0034 invariants
Reason: The reviewer's proposed fix is a single scope-acknowledgment sentence; ASN-0036 and ASN-0034 invariant scopes are matters of those ASNs' own definitions, derivable without external consultation.
