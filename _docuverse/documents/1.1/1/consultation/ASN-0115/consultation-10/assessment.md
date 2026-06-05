# Channel Assignment — ASN-0115 review-10

**Date:** 2026-06-05 06:43

## Issue 1: `item` is applied to all of `act` without establishing its two cases are exhaustive there
Reason: The fix is internal — the substrate section already states S3★-aux (SubspaceExhaustiveness, ASN-0047: every active V-position has subspace `s_C` or `s_L`); the revision merely cites it at the `item` definition to discharge case exhaustiveness. No design intent or implementation evidence is at stake.
