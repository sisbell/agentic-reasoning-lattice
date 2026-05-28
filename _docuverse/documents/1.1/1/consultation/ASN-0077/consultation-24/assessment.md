# Channel Assignment — ASN-0077 review-24

**Date:** 2026-05-27 20:11

## Issue 1: Closure argument scope in O0(b)
Reason: The fix is a scope clarification about which formal transition vocabulary the closure has been verified against — derivable from ASN-0047 and ASN-0093 specifications already cited. Neither design intent (Nelson) nor implementation evidence (Gregory) is needed to decide between option (a) restricting to ValidComposite★ or option (b) extending the enumeration.

## Issue 2: Multi-step versions of O5 and O6 not stated explicitly
Reason: The fix is a standard inductive extension from single-step to multi-step transition chains, following the pattern foundation ASN-0098 already establishes. The derivations follow mechanically from the single-step results — no design intent or implementation evidence required.

## Issue 3: Worked example omits direct verification of O8, O11, O11'
Reason: The fix extends the existing worked example with concrete computations of already-derived claims using the same scenario apparatus. No new design intent or implementation behaviour is being claimed — only illustration of established results.

## Issue 4: O0(c) totality claim under-justified
Reason: The fix is a proof-derivation correction routing the totality discharge through both (a) and (b) rather than (a) alone. It is internal to the ASN's existing argument structure and does not require external evidence.
