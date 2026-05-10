# Revision Categorization — ASN-0004 review-3

**Date:** 2026-03-06 16:16

## Issue 1: INS1 contiguity is prose, not formal
Category: INTERNAL
Reason: The ASN's prose already asserts contiguity and defines a₀; the fix is purely mechanical — rewrite the formal INS1 to match what the prose and all downstream references already assume. No external evidence needed.

## Issue 2: Missing owner frame condition
Category: INTERNAL
Reason: The ASN itself argues (at INS-F5) that "silence is not a frame condition" and that omitted components must be explicitly preserved. Applying the ASN's own reasoning to `owner` yields the missing clause directly.

## Issue 3: S-DISJ preservation not verified
Category: INTERNAL
Reason: The ASN already contains INS1a (text allocation is subspace-local) and INS-F5 (link positions unchanged), which together imply S-DISJ preservation. The fix is to either classify S-DISJ as an axiom or add a short proof using properties already stated in the ASN.
