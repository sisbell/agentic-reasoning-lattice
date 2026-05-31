# Channel Assignment — ASN-0043 review-173

**Date:** 2026-05-31 03:13

## Issue 1: Meta-prose around the L1c chain condition explains why the guard is encoded rather than what it says
Reason: Purely editorial — the fix collapses a justification of an encoding choice into one clause about the `k = 1` guard's automatic discharge by T10a.4, all of which is already established in the ASN. No design intent or implementation evidence is at stake.

## Issue 2: The Coverage definition note states its single point twice
Reason: Internal prose deduplication — deleting a restatement of the lossy-projection fact, which is already demonstrated in the worked example (Step 6). No external channel needed.
