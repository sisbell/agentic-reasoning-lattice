# Channel Assignment — ASN-0051 review-38

**Date:** 2026-05-16 02:32

## Issue 1: SV6 informal statement says "newly allocated" but formal precondition is purely structural
Reason: The fix is an editorial alignment between the informal statement and the formal precondition list, both of which are present in the ASN. The proof's independence from allocation status is already established in the body.

## Issue 2: SV6 proof asserts "p₃ ≥ 6" without derivation
Reason: The derivation chains T4 constraints (t₁ ≠ 0, no adjacent zeros) that are already cited in the ASN and ASN-0034. The fix is purely arithmetic from properties already in scope.

## Issue 3: Properties table omits corollaries stated in the body
Reason: The omitted corollaries are already stated and proved in the body of the ASN; the fix is purely editorial — adding table rows that reference existing content.

## Issue 4: Cross-document decoupling witness — V-position naming collision left implicit
Reason: V-position document-locality follows from the foundation schema (M(d) is per-document, V-positions are tagged by subspace within d) already cited in the ASN. The fix is a one-clause clarification using concepts already in scope.
