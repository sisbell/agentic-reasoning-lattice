# Channel Assignment — ASN-0102 review-36

**Date:** 2026-06-07 22:38

## Issue 1: Precondition labels P1–P4 collide with foundation invariant labels
Reason: Pure relabeling of COPY-local preconditions to a non-colliding scheme and updating internal references; no design intent or implementation evidence is involved.

## Issue 2: P4a referred to by a name the foundation does not use
Reason: The correct foundation name (TraceWitnessing) is already fixed by ASN-0047, which the ASN cites; substituting it is a mechanical naming correction internal to the text.

## Issue 3: S3★-aux discharge is folded into the S3★ wp computation without its own argument
Reason: The missing one-line discharge follows entirely from the ASN's own P3 (content-subspace precondition) and pre-state S3★-aux carried by unmoved/displaced positions; no external channel needed.
