# Channel Assignment — ASN-0087 review-39

**Date:** 2026-06-03 23:52

## Issue 1: Reconciliation prose in "What Is Indexed?" is reviser drift
Reason: Pure editorial reduction — the substantive claim (home document alone gets the reflexive route; content-reach route is symmetric) is already established in the body via M-DiscSymmetry and M-Reflexive. Removing the reconciliation framing requires no design intent or implementation evidence.

## Issue 2: Protocol-concurrency reasoning embedded in Inputs
Reason: The ASN's own Atomicity section already assigns composite-level/protocol concerns to the protocol layer; dropping or relocating the intervening-emission caveat is internally derivable from that existing deferral.

## Issue 3: D-SEQ★ verification ignores MAKELINK's own depth commitment
Reason: M-DepthConv and the Effect section already fix `m = 2`; aligning the D-SEQ★ verification to that committed depth is a formal consistency edit using content already present in the ASN.

## Issue 4: Open Question already answered in the body
Reason: The Atomicity section and M-CompAtomicity already characterize the `Σ_mid` vs `Σ'` distinction; removing or rephrasing the question is an internal consistency fix derivable from the ASN alone.
