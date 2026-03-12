# Revision Categorization — ASN-0030 review-4

**Date:** 2026-03-12 00:37

## Issue 1: A3 note contradicts the qualification for transition (c)
Category: INTERNAL
Reason: The contradiction is between two statements within the same section of the ASN. The fix — excluding (c) from the single-step list — is directly derivable from the ASN's own later analysis of transition (c).

## Issue 2: A4a missing frame condition
Category: INTERNAL
Reason: P7 (CrossDocVIndependent, ASN-0026) already provides the basis, and the parallel frame conditions in A4(f) and A5(f)-(g) provide the template. Pure completeness fix.

## Issue 3: A5(f) contradicts postconditions when d_s = d_t
Category: INTERNAL
Reason: The contradiction is a logical error within A5's own postconditions. P5 (ASN-0026) establishes self-transclusion is valid; the fix is to condition (f) on d_s ≠ d_t, derivable entirely from the existing definitions.

## Issue 4: A8 ghost analysis cites wrong inc invocation
Category: INTERNAL
Reason: Arithmetic error in applying TA5(d) from ASN-0001. The correct invocation is inc([1], 2), checkable directly from the definition.

## Issue 5: A8 ghost permanence argument has a vacuous premise
Category: INTERNAL
Reason: T10a's sequential discipline and T10's partition independence (both ASN-0001) jointly prevent same-level ghosts between siblings. The reframing to frontier ghosts follows from T9 (ForwardAllocation), all within existing ASN definitions.
