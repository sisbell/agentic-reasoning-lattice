# Channel Assignment — ASN-0093 review-45

**Date:** 2026-05-31 08:49

## Issue 1: Freshness lemmas' premises records omit load-bearing dependencies
Reason: The fix is internal — the proof bodies already cite the missing premises (FirstEmission, L1, ChainPrefixExtension, ChainUniformZeroCount, ChainElementT4Validity/StoreT4Validity), so reconciling the table columns with the existing arguments is pure bookkeeping derivable from the ASN itself.

## Issue 2: Duplicate StandardTriple/arity-N note (anti-bloat)
Reason: The fix is internal — trimming the redundant worked-example restatement to a one-line back-reference to L3 is an editorial deduplication requiring no design intent or implementation evidence.
