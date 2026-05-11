# Channel Assignment — ASN-0036 review-78

**Date:** 2026-05-11 01:05

## Issue 1: S8 contract's S8a precondition is incompletely restated
Reason: The fix is internal to the ASN — S8a's three-conjunct definition is stated earlier in the same document, and the S8 proof's reliance on `#v ≥ 2` and componentwise positivity is visible in the proof body. Reconciling the inline summary with S8a's canonical form requires no design-intent or implementation evidence.

## Issue 2: S8 dependency listing includes TA5 but the proof does not use TA5
Reason: The fix is internal — the operators actually consumed by S8's proof are enumerated in the proof body (TumblerAdd, OrdinalShift, OrdinalDisplacement, TS4, T1, T3, T5, T10), and TA5 appears only in motivational prose. Correcting the dependency citation is a mechanical alignment with the existing proof.
