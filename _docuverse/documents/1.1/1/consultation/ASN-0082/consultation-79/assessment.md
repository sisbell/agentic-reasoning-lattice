# Channel Assignment — ASN-0082 review-79

**Date:** 2026-05-30 14:38

## Issue 1: Scoping axioms duplicated and re-cited at every use site
Reason: Pure editorial deduplication — remove the standalone paragraph and the parenthetical tags, keeping S = 1 and #p = 2 as ordinary contract preconditions. No external intent or implementation evidence is involved; the fix is internal.

## Issue 2: D-BJ part (c) is proof-by-restatement
Reason: A proof-structure cleanup. Surjectivity onto a set defined as the image is vacuous; retitle to "order-preserving injection" or state the image-definition once. Fully derivable from the ASN's own definitions.

## Issue 3: Triplicated frame-note prose in the cross-subspace worked example
Reason: Editorial deduplication — verify D-CTG/D-MIN/D-SEQ-post for V_1 only and state the V_2 exemption once, which D-CS already supplies. No external channel needed.

## Issue 4: The S ≠ 1 "active" insertion case is asserted but never exercised
Reason: I3 and the preservation lemmas (I3-VP, I3-S2, I3-S3, I3-CS/CX) are already proven for general S ≥ 1, so a concrete S = 2 worked example is a mechanical instantiation of existing machinery, and the tombstone-reuse permission is already grounded in ASN-0036's D-CTG frame note cited here. The fix is internal — the math is present; only the verification trace is missing.
