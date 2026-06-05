# Channel Assignment — ASN-0100 review-79

**Date:** 2026-06-05 05:00

## Issue 1: Empty worked example conflates empty arrangement with empty allocation history
Reason: The fix is derivable from the ASN itself — it already invokes S0/P0 (content persists in `dom(C)` after removal from the arrangement) and ASN-0093's first-vs-subsequent emission predicates. Adding the stipulation or the history-dependence note requires no external intent or implementation evidence.

## Issue 2: L0 content-clause argument duplicated verbatim across two sections
Reason: Pure deduplication of an argument already present and correct in the ASN; stating it once and citing from the other site needs no channel.

## Issue 3: Hub-and-spoke deferral to §Atomicity for the fresh-address discharge
Reason: Editorial restructuring of where a discharge lives; the proof content is unchanged and fully internal to the ASN.

## Issue 4: C1a precondition discharge repeated near-verbatim
Reason: Factoring a duplicated precondition-discharge into one reusable statement is internal restructuring, derivable from the ASN's own S2/S8-fin/S8-depth citations.
