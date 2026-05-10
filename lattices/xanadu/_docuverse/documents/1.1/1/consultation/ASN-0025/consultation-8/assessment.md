# Revision Categorization — ASN-0025 review-8

**Date:** 2026-03-07 12:49

## Issue 1: J1/J2 preservation asserted without per-operation proof
Category: INTERNAL
Reason: The set algebra follows directly from the V-space postconditions already stated for each operation. The review even sketches the argument — it just needs to be written out per-operation alongside existing P0∧P1 and J0 verifications.

## Issue 2: VPos type undefined; "text position" and "link position" predicates informal
Category: INTERNAL
Reason: The ASN already describes V-positions as carrying a subspace identifier (text=1, link=2) and an ordinal component. Formalizing VPos as a typed pair and adding the missing "q is a text position" guard to the `q < p` clauses is derivable from definitions already present in the ASN and TA7a/TA7b from ASN-0001.

## Issue 3: CREATE DOCUMENT precondition informal
Category: INTERNAL
Reason: For the permanence argument, the only needed precondition is freshness of the allocated orgl, which follows from GlobalUniqueness. The fix is to note that user account modeling is deferred and reduce the precondition to what the permanence argument actually requires — no design intent or implementation evidence needed.
