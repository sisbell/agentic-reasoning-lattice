# Channel Assignment — ASN-0047 review-363

**Date:** 2026-06-02 12:05

## Issue 1: SubAllocatorBundle is miscategorized as inherited
Reason: Pure document-organization fix — relocating a row between two tables based on labels already present in the ASN. No design-intent or implementation evidence is needed; the split between inherited chain facts and the cross-subspace delta is already stated in-document.

## Issue 2: P7a is stated without a derivation at its definition site
Reason: The derivation already exists in the Class (b) proof (J0 + S3★ + L14 + S3★-aux + J1★); the fix only adds a pointer or inline restatement matching P6/P7. Entirely internal to the ASN.

## Issue 3: The "New properties introduced" table reproduces full operation definitions verbatim
Reason: De-duplication of content already present normatively in the Elementary transitions box; reducing rows to one-line characterizations needs no external input, only the ASN's own definitions.
