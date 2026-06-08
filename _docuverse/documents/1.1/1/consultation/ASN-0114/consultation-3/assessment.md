# Channel Assignment — ASN-0114 review-3

**Date:** 2026-06-08 02:17

## Issue 1: Disclosure derivation assumes all covered addresses are T4-valid and document-bearing
Reason: Internal fix. The correction is derivable from substrate the ASN already cites — ASN-0043 L4/L9 (endsets may target any tumbler, including ghost/non-document addresses) and ASN-0034 T4b (field projections undefined on non-conforming addresses). Restricting the disclosure claim to `zeros ≥ 2` addresses is a logical qualification, requiring no design intent or implementation evidence.

## Issue 2: Undefined/inconsistent term "spec-set"
Reason: Internal fix. Pure terminology consistency — the body uses "span-set" (ASN-0053) throughout; "spec-set" is a stray typo with no distinct meaning, replaceable directly from the ASN's own vocabulary.
