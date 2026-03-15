# Revision Categorization — ASN-0040 review-2

**Date:** 2026-03-15 12:54

## Issue 1: WP analysis conflates sequential and concurrent reasoning, omits B4
Category: INTERNAL
Reason: All relevant properties (B0a, B4, B1, B7, B8) are defined within the ASN. The fix is restructuring the prose and wp derivations to correctly attribute the serialization role to B4 instead of B0a — a logical consistency correction using the ASN's own definitions.

## Issue 2: B7 Case 3 has no concrete verification
Category: INTERNAL
Reason: The review even supplies the concrete instance ([1] at d=2 vs [1,1] at d=1). Tracing inc through TA5 for specific inputs is mechanical application of already-defined operations from ASN-0034. No design intent or implementation evidence needed.

## Issue 3: S0 cites TA-strict; should cite TA5(a)
Category: INTERNAL
Reason: This is a citation accuracy issue within the existing formal framework. TA5(a) directly establishes `t' > t` for inc; TA-strict applies to ⊕. The correct property is already present in ASN-0034 — the fix is changing which one is cited.
