# Channel Assignment — ASN-0126 review-96

**Date:** 2026-06-10 06:43

## Issue 1: "Tension with type identity" is an editorial overstatement, and imprecise
Reason: Internal. The fix is to drop the editorializing coda and reframe a false "tension" as the deliberate independence of two checks reading different slots — coverage-keyed type identity (slot 3) vs. span-count conformance (slots 1–2). Both checks are fully defined in the note (The registry, Shape-conformance), so the corrected framing is derivable from the ASN's own definitions; no design-intent or implementation evidence is required.

## Issue 2: Transfer-machinery scoping is forward-pointed and partly duplicated
Reason: Internal. The fix removes the forward-pointing "P6 makes that transfer inline" clause from B2 and de-duplicates the "no successors" rationale, having P6 and Gate realizability cite B2 rather than re-derive it. This is a pure reorganization of expository structure already present in the note (B2, P6, Gate realizability all exist with the relevant content), requiring neither Nelson nor Gregory.
