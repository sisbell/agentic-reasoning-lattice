# Channel Assignment — ASN-0134 review-20

**Date:** 2026-06-14 02:23

## Issue 1: single-home `stale` is classified as a single bounded access, but active-membership requires a cross-home retraction read
Reason: Internal inconsistency, no channel needed. A1's claim that one descent of `d`'s link subspace "enumerates `d`'s active type-`K` members" contradicts the note's own §4 (the target-residence race fixes `d_retr ≠ home(target)`, grounded in ASN-0128 P0's `d_retr ∈ dom(M)`-only constraint) and the `nullified` definition (ASN-0086, coverage by `L_R` tuples homed at any retractor) — both already load-bearing elsewhere in the note. The descent yields `L_K|_d` and `f_d` but not active-ness, which needs the separate global retraction read; reclassifying single-home `stale` as a multi-read (governed by clause 7, not clause 4) follows directly from the note's own access-count discriminator, and option (b)'s "fused access" is undercut by the note's existing `findpreviousisagr` evidence, which recovers only the frontier.
