# Channel Assignment — ASN-0107 review-23

**Date:** 2026-06-08 12:01

## Issue 1: R2's decrement bound silently assumes a single consulted slot
Reason: This is a formalization-consistency defect entirely internal to the ASN — the fix either adds an explicit single-slot precondition mirroring R1's (P-slot) or redefines `k` as "links losing their last reach in *some* consulted slot" and re-derives the bound. Both the multi-slot semantics and the corrected derivation follow from `sat`'s own conjunctive-across-slots definition already present in the note.

## Issue 2: Deferral paragraph adds no claim
Reason: Pure editorial deletion/fold; the substantive observation (conservation is anchoring-conditional) is already proved by E4 and D2 within the ASN. No external design intent or implementation evidence is required.

## Issue 3: Cross-ASN reference by number to a non-foundation ASN
Reason: Mechanical self-containment fix — replace "the separate FINDLINKS retrieval operation (ASN-0099)" with the operation name alone, matching the Open Questions' existing phrasing. Nothing external needed.
