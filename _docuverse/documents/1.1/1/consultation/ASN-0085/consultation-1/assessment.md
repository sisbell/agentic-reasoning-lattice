# Revision Categorization — ASN-0085 review-1

**Date:** 2026-04-11 01:12

## Issue 1: All three definitions lack formal contracts
Category: INTERNAL
Reason: The review specifies exactly which preconditions, postconditions, and frame conditions are needed, all derivable from S8a, T0, and TA7a already present in ASN-0034 and ASN-0036.

## Issue 2: The central property is missing — arithmetic does not factor through the decomposition
Category: INTERNAL
Reason: The review provides the full property statement, proof sketch via TumblerAdd/actionPoint, and the shift corollary — all from definitions already in ASN-0034. The ASN's own open question identifies this gap.

## Issue 3: No connection to TA7a's domain S
Category: INTERNAL
Reason: The argument is immediate from S8a (positive components) and TA7a's definition of S, both in existing foundation ASNs. The review spells out the one-line proof.

## Issue 4: "V-depth displacement" is undefined
Category: INTERNAL
Reason: The condition `w₁ = 0` and its justification via actionPoint are fully derivable from TumblerAdd in ASN-0034. The fix is either a local definition or inlining the conditions — no external design intent or implementation evidence needed.
