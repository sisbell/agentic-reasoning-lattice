# Channel Assignment — ASN-0036 review-132

**Date:** 2026-05-28 23:45

## Issue 1: Coalescing/maximal-run caveat stated three times
Reason: Pure editorial deduplication — the fix removes redundant restatements of a caveat already present in the ASN; no design intent or implementation evidence is required.

## Issue 2: S7 dependency list stated three times
Reason: Internal cleanup — the narrative recitation duplicates the proof structure and Depends clause already in the ASN; deletion needs no external channel.

## Issue 3: "not re-derived here" meta-prose in projection contracts
Reason: Editorial — removing meta-prose while retaining the source citation (S7b/S8a) is fully derivable from the ASN's existing text.

## Issue 4: Operation-layer references embedded in position predicates
Reason: Scope cleanup — restating the predicate in pure state terms and deferring the choice-of-m discussion to the existing Open Question is internal; the ASN already declares operation mechanics out of scope.

## Issue 5: S8's existence claim is discharged only by the degenerate witness
Reason: The fix is choosing between restricting the postcondition to the proven singleton partition or relabeling the worked example — both decisions are about aligning the contract with the proof already present, fully internal to the ASN.
