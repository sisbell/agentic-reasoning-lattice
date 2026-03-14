# Revision Categorization — ASN-0036 review-4

**Date:** 2026-03-14 16:42

## Issue 1: S5 uses derivability operator without model-theoretic support
Category: INTERNAL
Reason: The fix is either to sketch a trivial model family (for any N, construct N+1 documents each mapping one V-position to the same I-address — S0–S3 are verifiable from definitions already in the ASN) or to restate without `⊢` and "reachable." Both options use only material present in the ASN.

## Issue 2: S8 depends on I-address depth uniformity within runs, unstated and underived
Category: INTERNAL
Reason: The reviewer supplies the complete derivation chain: T9 → TA5(c) → same depth. All referenced properties (T9, TA5(c)) are from ASN-0034, already cited in this ASN. The fix is to state the property and write out the derivation — no external evidence needed.

## Issue 3: S8-depth has ambiguous status — property or design requirement
Category: INTERNAL
Reason: This is a classification decision parallel to S7a's existing classification. The reviewer identifies the exact pattern to follow. No external knowledge is required — only editorial reclassification using the ASN's own taxonomy.

## Issue 4: Open question 6 is answered by S8's own definition
Category: INTERNAL
Reason: The answer is already in the ASN: correspondence runs are *defined* by ordinal correspondence, and S8 proves any M(d) decomposes into runs. The fix is to resolve or rephrase the question using existing content.

## Issue 5: Properties table misclassifies S8
Category: INTERNAL
Reason: The ASN already contains the explicit singleton-run existence proof from S8-fin and S2. The fix is a one-cell edit in the properties table, following the precedent the ASN already sets for S1 and S9.
