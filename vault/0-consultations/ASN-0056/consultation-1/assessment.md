# Revision Categorization — ASN-0056 review-1

**Date:** 2026-03-19 20:25

## Issue 1: S11d proof incomplete for containment case (iv)
Category: INTERNAL
Reason: Both subcases are derivable from existing content. When α ⊆ β, the difference is trivially ∅ (0 spans) by the same reasoning as S11b. S11 from ASN-0053 covers the converse. No external evidence needed.

## Issue 2: S11c symmetric overlap case — preconditions unverified
Category: INTERNAL
Reason: The required precondition chain (#reach(β) = #start(β) = #start(α) = #reach(α)) follows from level-uniformity of both spans plus the given level_compat on starts — all properties already defined and available in ASN-0053. The verification is mechanical.

## Issue 3: Registry type mismatch for SC
Category: INTERNAL
Reason: ASN-0053 defines SC as "LEMMA, lemma". The fix is correcting the registry entry to match — no design intent or implementation evidence needed.
