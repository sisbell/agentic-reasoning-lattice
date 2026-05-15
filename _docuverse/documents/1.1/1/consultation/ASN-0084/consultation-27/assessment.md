# Channel Assignment — ASN-0084 review-27

**Date:** 2026-05-15 12:07

## Issue 1: w_μ ≥ 1 derivation lacks explicit V-position witness
Reason: Internal proof gap. The witness (c₁) and all justifications (CS2, CS3, CS4, R-PRE(iv)) are already present in the ASN; only the explicit bridge step is missing.

## Issue 2: R-BLK Phase 1 closing uses interval notation for a discrete set
Reason: Notational clarity issue. The fix is a pure rephrasing using vocabulary already established in the ASN.

## Issue 3: Forward/backward extent maxima existence asserted without bound
Reason: Internal proof gap. The bound (N − ord(v) from D-SEQ) and the well-ordering principle are both already cited or available within the ASN's existing dependency set (ASN-0036, ASN-0034).
