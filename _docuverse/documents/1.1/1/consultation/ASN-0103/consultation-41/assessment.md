# Channel Assignment — ASN-0103 review-41

**Date:** 2026-06-08 10:10

## Issue 1: Cross-chain distinctness re-derives a foundation guarantee
Reason: Internal. The fix swaps a long exhaustiveness walk for a citation to GlobalUniqueness (ASN-0034), a foundation result the ASN already references via B8 in CND.monotone; no design intent or implementation evidence is involved.

## Issue 2: Prefix transitivity invoked without grounding
Reason: Internal. Either ASN-0042's Prefix contract supplies transitivity (a foundation-citation check) or the one-line derivation from the prefix definition (`#p ≤ #q ≤ #r` with component agreement) goes inline — both resolvable from existing material without Nelson or Gregory.
