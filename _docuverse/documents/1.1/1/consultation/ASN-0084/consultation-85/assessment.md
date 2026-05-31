# Channel Assignment — ASN-0084 review-85

**Date:** 2026-05-30 17:49

## Issue 1: Tiling of [c₀, c₃) is proved twice
Reason: This is a purely editorial deduplication — deleting the redundant coverage argument from the "Reduction of compound shifts" block and keeping only the left-associativity reading. Both the duplicated proof and its surviving home (R-SWP) are entirely within the ASN, so no design intent or implementation evidence is required.

## Issue 2: Front-loaded depth-invariance justification with downstream-consumer pointer
Reason: This is a relocation of an existing justification (the depth-invariance of TS3) from the section opener into Split and Merge where it is consumed. The fact, its citation (TS3/ASN-0034), and its consumers are all present in the ASN, so the fix is internal and needs neither channel.
