# Channel Assignment — ASN-0102 review-49

**Date:** 2026-06-08 00:25

## Issue 1: T7 misapplied to V-positions in X16
Reason: Internal — the fix is a citation correction, replacing T7 (element-level I-addresses) with T1/T3 (component-wise tumbler distinctness) from ASN-0034, which are already available foundations. No design intent or implementation evidence is needed.

## Issue 2: standalone/embedded two-readings exposition is duplicated
Reason: Internal — purely an editorial deduplication, consolidating the boundary-reading argument into X14 and leaving operational facts in the Definition. No external content is involved.

## Issue 3: protocol-rationale bloat justifying free composability
Reason: Internal — the fix removes defensive justification prose (the docopy-call-pattern and K.μ⁻/K.μ~ appeals), reducing to the structural statement. Trimming existing prose requires no new evidence; the load-bearing facts already cite Q1/ASN-0047.

## Issue 4: embedded J1'★ discharge is circular
Reason: Internal — the fix is a logical correction about what ValidComposite★ (ASN-0047) requires: either show COPY's per-step witness survives to Σ_n under the frame, or scope boundary J1'★ as a composite-level obligation COPY cannot discharge alone. This is derivable from the coupling definitions already in the ASN and ASN-0047.
