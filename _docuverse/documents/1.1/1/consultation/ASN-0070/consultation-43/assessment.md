# Channel Assignment — ASN-0070 review-43

**Date:** 2026-06-03 00:06

## Issue 1: Speculative concurrency claim in F-frame's slot
Reason: The fix is a deletion fully justified by the ASN's own content — the note explicitly defers concurrency semantics in its Open Questions, and the frame invariant (`C'=C, M'=M, L'=L, E'=E, R'=R`) is stated verbatim already; no design intent or implementation evidence is needed to remove an unsupported aside the note itself disowns.
