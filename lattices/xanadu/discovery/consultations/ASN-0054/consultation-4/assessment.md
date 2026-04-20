# Revision Categorization — ASN-0054 review-4

**Date:** 2026-03-20 06:49

## Issue 1: A0 enforcement mechanism contradicts INSERT decomposition
Category: INTERNAL
Reason: The ASN already contains both the correct framing ("composite-boundary invariant… may be temporarily violated at intermediate states") and the contradictory K.μ⁺/K.μ~ proposal. The fix — replacing the elementary postcondition with a composite coupling constraint — is derivable from the ASN's own composite-boundary invariant language and the ASN-0047 composite transition framework.

## Issue 2: Worked example uses malformed I-addresses
Category: INTERNAL
Reason: S7b (zeros(a) = 3) and T4's parsing rule are already stated foundations. Constructing correct element-level addresses and re-verifying the arithmetic is mechanical — no design intent or implementation evidence is needed.

## Issue 3: REARRANGE missing precondition bounds
Category: INTERNAL
Reason: INSERT and DELETE already state analogous bounds (0 ≤ j ≤ n, 0 ≤ j and j + w ≤ n) in the same ASN. Adding 0 ≤ c₁ and c₃ ≤ n is pattern-matching against the precondition style already established in the document.

## Issue 4: Open question about L(d) is answerable from foundations
Category: INTERNAL
Reason: The review finding itself derives the answer from S8-depth, which is a foundation invariant already referenced in the ASN. The corollary follows directly from existing definitions.
