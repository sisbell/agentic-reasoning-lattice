# Channel Assignment — ASN-0116 review-56

**Date:** 2026-06-09 21:00

## Issue 1: IP1's forward-merge justification fails in states with transcluded content
Reason: Internal. The conclusion ("forward I-merge never happens") already holds and the review hands the complete replacement argument; every fact it rests on is present in the ASN — `M(d)(q_J) ∈ dom(C)` by the already-cited S3★, and `shift(a,n) ∉ dom(C')` follows from the K.α mechanism the note already states (`a = inc(a_prev,0)`, `a_prev = max{a' ∈ dom(C) : origin(a') = d}`, run `A_new` stopping at `shift(a,n−1)`), so `M(d)(q_J) = shift(a,n)` is impossible. No design intent or implementation evidence is at issue.
