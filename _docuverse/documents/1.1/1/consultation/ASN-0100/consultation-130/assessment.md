# Channel Assignment — ASN-0100 review-130

**Date:** 2026-06-08 01:02

## Issue 1: Redundant restatement of the K.α emission branch in Effect One
Reason: Pure prose deduplication — drop a restated predicate and open at the nuance. No design intent or implementation evidence needed; the change is internal to the ASN's own text.

## Issue 2: Non-advancing forward-defer in Effect Three
Reason: Deleting a meta-prose sentence that announces a deferral already fulfilled in §Verifying the Invariants. Entirely internal.

## Issue 3: I3's preconditions never discharged before inheriting its consequences
Reason: The required discharge line cites I3's preconditions (`#p ≥ 2`, `subspace(p) = s_C`, depth-compatibility, `n ≥ 1`), all already established by INS.pre and the depth precondition within this ASN; the fix is to state the discharge, which is derivable internally.
