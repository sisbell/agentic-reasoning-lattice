# Channel Assignment — ASN-0100 review-135

**Date:** 2026-06-08 01:31

## Issue 1: The "re-derive S3/S7 because I3-C is violated" rationale is stated three times
Reason: Purely editorial deduplication — consolidate one rationale to its proof site and reduce the others to cross-references. The justification (I3-C violated by growing dom(C)) is already fully present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: The INS.M-exhaustive composite argument is duplicated, with an inconsistent attribution
Reason: Internal fix — the proof location is determinable from the ASN itself (§Arrangement functionality holds the discharge, §The Operation: Formal Contract only states it). Deduplicating and correcting the mis-pointer requires only the ASN's own structure.

## Issue 3: Claims-table rows carry justification/deferral prose instead of bare claim statements
Reason: Editorial trimming of the claims table to bare claim statements, with reasoning already relocated per Issue 1. Entirely derivable from the ASN's existing content.
