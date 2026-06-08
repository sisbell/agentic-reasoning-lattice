# Channel Assignment — ASN-0114 review-2

**Date:** 2026-06-08 02:12

## Issue 1: Worked example misstates coverage as a finite address set
Reason: Internal fix. The error is a notational/mathematical one — `coverage` is defined over `T` (ASN-0098), already cited in the note; correcting the enumeration to interval form or adding the `∩ F` qualifier is derivable from definitions already present.

## Issue 2: F5 applies a single-step invariant to a multi-step sequence without the closure
Reason: Internal fix. The required lemma LP13 and the Closure schema (★) are both in ASN-0098, already part of the note's cited substrate; either invoking them or writing the one-line induction is derivable from material the note already references.
