# Channel Assignment — ASN-0036 review-155

**Date:** 2026-05-29 02:45

## Issue 1: Result/count asserted inside the ValidInsertionPosition Definition slot
Reason: Purely structural relocation — the `N + 1` count is already re-derived in the standalone derivation paragraph and recorded in postcondition (c). Removing it from the Definition slot is an editorial deduplication derivable from the ASN's own existing content.

## Issue 2: Commentary embedded in the ValidFirstInsertionPosition Definition
Reason: The commentary is meta-text that duplicates the existing Open Question on the canonical choice of `m`; striking it from the Definition slot requires no design intent or implementation evidence, only the ASN's own structure.

## Issue 3: S1 Remark is a scope inventory that does not advance the claim
Reason: The remark compares S1's scope against T8 (a foundation property already in ASN-0034); the distinguishing fact (S1 conditioned on `a ∈ dom(C)`) is already explicit in S1's statement and frame, so dropping or folding it is internal.
