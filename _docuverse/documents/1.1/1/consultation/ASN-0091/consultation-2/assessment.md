# Channel Assignment — ASN-0091 review-2

**Date:** 2026-05-26 14:05

## Issue 1: Abstract class frame is too weak for RE-R
Reason: Internal structural choice — either widen RA-frame to include R (and E) or relabel RE-R as REARRANGE_K-specific. The ASN already names J3 as the derivation source; the fix is a consistency edit between the abstract definition and the claims partition, no external input required.

## Issue 2: RE-sub is not derivable from the abstract class
Reason: Internal — same shape as Issue 1. Either add a designated cut-subspace fixity clause to the abstract RA-π, or mark RE-sub as REARRANGE_K-specific. The ASN already cites R-FRAME-P/S correctly in the derivation; only the framing-vs-table split needs reconciling.

## Issue 3: Claims Introduced table conflates abstract and REARRANGE_K-specific claims
Reason: Internal — the prose already distinguishes which claims flow from RA-dom/RA-π/RA-frame versus which need ASN-0084 cut-sequence structure or ASN-0047 K.μ~ frame. Adding a provenance column is a mechanical annotation derivable from the existing derivation text.

## Issue 4: `→_R` notation undefined
Reason: Internal notation fix — add a one-line definition tying `→_R` to either the abstract Vstream-only class (RA-dom/π/frame) or to K.μ~, consistent with the section's intended scope. The ASN's existing vocabulary suffices.

## Issue 5: Multi-step run-decomposition claim under-stated
Reason: Internal — either construct a two-step witness by chaining the existing fragmentation and coalescence singletons (whose post-states are concrete, T4-valid arrangements), or weaken the prose to "no per-step monotonicity." Both options sit inside the ASN's worked-example apparatus.
