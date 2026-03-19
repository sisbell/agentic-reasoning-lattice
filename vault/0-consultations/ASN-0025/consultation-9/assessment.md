# Revision Categorization — ASN-0025 review-9

**Date:** 2026-03-07 17:26

## Issue 1: DocId type undefined; fresh document identity not established
Category: INTERNAL
Reason: The ASN already has orgl(d) ∈ Σ.A and GlobalUniqueness; stating DocId = IAddr (identified by orgl) and deriving freshness from o ∉ Σ.A is purely a matter of making implicit definitions explicit from existing machinery.

## Issue 2: Orgl injectivity invariant missing
Category: INTERNAL
Reason: Follows directly from the resolution of Issue 1 — if DocId = IAddr via orgl, injectivity is automatic from the function definition. If DocId is independent, the invariant is a straightforward formal addition using existing GlobalUniqueness.

## Issue 3: Content at new addresses unspecified for three operations
Category: INTERNAL
Reason: The ASN already defines Value as covering "structural entries (document and version orgls), and link data." The fix is adding postconditions like Σ'.ι(o) = v for an appropriate value type — the review itself notes the permanence argument does not depend on the specific value, only on completeness.

## Issue 4: COPY self-copy reasoning incomplete for P5
Category: INTERNAL
Reason: The V-space postconditions already show that shifted entries retain their I-addresses. The fix is a case split (d = d_s vs. d ≠ d_s) using reasoning already present in the COPY section's shift postconditions.

## Issue 5: REARRANGE claims "three properties" but lists four
Category: INTERNAL
Reason: Counting error — four properties are listed and later correctly referenced as "all four." Change "Three" to "Four."

## Issue 6: J1/J2 preservation unverified in four operation sections
Category: INTERNAL
Reason: Each verification uses only the ASN's own definitions (domain preservation for REARRANGE, position-for-position copy for CREATE VERSION, append-at-next for CREATE LINK, empty domain for CREATE DOCUMENT). The review provides the exact derivations needed.
