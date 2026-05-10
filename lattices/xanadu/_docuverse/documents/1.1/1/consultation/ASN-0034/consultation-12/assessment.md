# Revision Categorization — ASN-0034 review-12

**Date:** 2026-03-13 21:50

## Issue 1: TA5 commentary makes false claim about immediate successor
Category: INTERNAL
Reason: The fix is derivable from the ASN's own definitions — TA5(d) specifies what inc(t,k) produces, and the "Order structure" section already correctly identifies t.0 as the immediate successor. The incorrect commentary contradicts the ASN's own content.

## Issue 2: Global uniqueness proof — Case 4 does not cover parent's child-spawning output vs child's sibling outputs
Category: INTERNAL
Reason: The missing argument uses only properties already stated in the ASN: the child-spawning output IS the child's base address (by T10a's definition), and TA5(a) guarantees every subsequent child sibling is strictly greater. No external evidence needed.

## Issue 3: Subtraction definition — "When a = w" conflates T3 equality with zero-padded agreement
Category: INTERNAL
Reason: This is a notational precision issue — the correct condition is already stated in the parenthetical ("no divergence exists after padding"), and the fix is rewording to avoid the overloaded "a = w" notation. No design intent or implementation evidence required.
