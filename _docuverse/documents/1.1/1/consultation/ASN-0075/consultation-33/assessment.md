# Channel Assignment — ASN-0075 review-33

**Date:** 2026-06-03 00:56

## Issue 1: Link-survival justification (D-IDENT) restricts to span start tumblers and omits interior references
Reason: The fix is derivable from the ASN's own foundation citations — Span/T12 (ASN-0034) defines reference as `start ≤ a < reach`, and P3 (ASN-0047) preserves `L` in its entirety. Resting the guarantee on P3 alone (every referencing link survives, independent of how it reaches `a`) requires no design intent or implementation evidence, only the span semantics already in scope.
