# Revision Categorization — ASN-0082 review-7

**Date:** 2026-04-09 16:22

## Issue 1: I3 formalizes arrival but not departure — shift semantics incomplete
Category: INTERNAL
Reason: The fix — adding a vacating postcondition I3-V — is fully derivable from the ASN's own definitions. The review provides the exact formal statement needed, and the reasoning uses only M(d)'s partial-function semantics, the shift definition, and the existing region analysis already present in the ASN.

## Issue 2: Cited foundations missing from Statement Registry
Category: INTERNAL
Reason: T12 and T4 are already cited by label and ASN number in the document text. Adding them to the registry table is a mechanical bookkeeping fix requiring no external evidence.
