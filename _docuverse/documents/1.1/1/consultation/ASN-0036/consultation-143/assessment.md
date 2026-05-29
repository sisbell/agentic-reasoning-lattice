# Channel Assignment — ASN-0036 review-143

**Date:** 2026-05-29 01:27

## Issue 1: D-CTG's consequent admits tumblers that S8a forbids
Reason: Internal fix — the consequent's guard need only gain `zeros(v) = 0` (or "satisfies S8a"), a constraint already defined within the ASN; no design intent or implementation evidence bears on this purely formal tightening.

## Issue 2: "Ordinal-shift prefix lemma" restates a foundation property under a local name
Reason: Internal fix — the lemma duplicates OrdinalShift's postconditions (ASN-0034, already cited throughout); replacing the named local lemma with a direct citation is derivable from existing references.

## Issue 3: Duplicated "to know `a` is to know `origin(a)`"
Reason: Internal fix — deleting the S7 intro restatement and keeping the load-bearing Permanence-step version is an editorial deduplication requiring no external input.
