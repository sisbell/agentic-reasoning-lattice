# Channel Assignment — ASN-0036 review-175

**Date:** 2026-05-29 05:46

## Issue 1: Forward-reference justification prose in S5
Reason: Pure editorial deletion of meta-commentary about document ordering; the load-bearing content (which invariants are state-level vs. transition-level) is already present in the ASN. No design intent or implementation evidence is needed.

## Issue 2: Duplicate full-invariant verification across the two S5 constructions
Reason: Deduplication of identical verification prose for the shared address `a`; both constructions already appear in full in the ASN, so factoring the common facts is purely internal restructuring.

## Issue 3: ValidInsertionPosition postcondition (d) form versus subspace claim
Reason: Notational disambiguation to match the D-SEQ form `[1, 1, ..., 1, 1+j]` already used elsewhere in the ASN; the correct depth-`m` shape is fully determined by OrdinalShift and D-MIN as stated in the document.
