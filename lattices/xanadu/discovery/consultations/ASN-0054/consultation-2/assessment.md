# Revision Categorization — ASN-0054 review-2

**Date:** 2026-03-20 00:04

## Issue 1: Decomposition effect paragraph misplaced under COPY
Category: INTERNAL
Reason: The paragraph's content (regions, cuts, `rearrangend`) is clearly REARRANGE material, and COPY's decomposition effect follows from INSERT's, which is already described in the ASN. Pure editorial reorganization.

## Issue 2: A0 invariant status not formally declared
Category: INTERNAL
Reason: The ASN already establishes A0 as fundamental and proves preservation for all four operations. Declaring it as a per-state invariant and extending K.μ⁺/K.μ~ postconditions is a formal integration step derivable from the existing argument and ASN-0047's transition system.

## Issue 3: No concrete worked example
Category: INTERNAL
Reason: All definitions needed to construct and verify a numerical example (TumblerAdd, break predicate, run construction, A3–A7) are present in the ASN and its dependencies. The review even suggests a specific example. Purely mechanical.

## Issue 4: DELETE decomposition omits single-run-spanning-both-boundaries case
Category: INTERNAL
Reason: The missing case (one run producing two I-non-adjacent survivors) is derivable from the existing definitions of runs, breaks, and the deletion postcondition already stated in the ASN. No external evidence needed.

## Issue 5: "FEBE operations" undefined
Category: INTERNAL
Reason: The ASN already enumerates exactly four operations (INSERT, DELETE, REARRANGE, COPY) in its preservation section. Replacing the undefined term with this explicit list, as the review suggests, requires no external input.
