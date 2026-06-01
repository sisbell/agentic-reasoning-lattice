# Channel Assignment — ASN-0086 review-130

**Date:** 2026-06-01 00:47

## Issue 1: L12/L12a miscited as members of ASN-0043's StateLocalInvariants
Reason: Internal fix. The review supplies ASN-0043's actual StateLocalInvariants catalog, and the ASN itself uses L12/L12a as predicates over `Σ → Σ'` (R2, R3), confirming they are transition-level — so dropping them from the single-state list and, if needed, restating as a transition clause is derivable from content already present.

## Issue 2: Citation-convention meta-prose in the substrate-conforming-state definition
Reason: Internal fix. Pure deletion of a citation-bookkeeping sentence; naming the consequence already suffices and no design-intent or implementation evidence bears on it.

## Issue 3: Duplicate downstream deferrals to WP Case 1
Reason: Internal fix. Removing the redundant forward pointer from the Properties table while keeping the one in the Definition is a purely editorial deduplication derivable from the ASN's own structure.
