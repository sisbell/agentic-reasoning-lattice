# Channel Assignment — ASN-0058 review-37

**Date:** 2026-05-15 04:11

## Issue 1: M-int's subspace agreement step compresses the case analysis
Reason: The fix is a local proof rewrite — making the T1 case-elimination explicit using T1 (ASN-0034), which is already cited. No design intent or implementation evidence is needed; the required intermediate steps follow from T1's case structure already in scope.

## Issue 2: C0's invocation of T0(a) is indirect
Reason: The fix is a citation correction within ASN-0034's primitives — replacing T0(a) with T0's comprehension clause plus NAT-carrier. No design intent or implementation evidence is needed; the correct primitives are already available in ASN-0034 and the proof's construction is unchanged.
