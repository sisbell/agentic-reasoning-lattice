# Channel Assignment — ASN-0115 review-43

**Date:** 2026-06-10 03:20

## Issue 1: Forward-reference deferral pointer in the V-spec definition
Reason: Pure prose-organization fix internal to the ASN — drop a forward-pointing signpost and keep the substantive observation (the depth conjunct is re-evaluated per state because `m_S(d)` is mutable, already grounded in the cited ASN-0047 re-pinning) once. No design intent or implementation evidence bears on whether a deferral clause is removed.

## Issue 2: Non-advancing provenance enumeration in the `act` definition
Reason: Editorial trim derivable from the ASN alone — the override condition `V_S(d) ≠ ∅ ∧ #s ≠ m_S(d)` is already the full content of the branch, so cutting the redundant provenance parenthetical needs no external input.

## Issue 3: R2's justification imports a temporal invariant the single-state claim does not use
Reason: Internal attribution fix — the ASN already distinguishes single-state denotational equality (R2, from S2 + `item` + S3★) from cross-state permanence (R7/R11, from S0); rescoping R2's credit and dropping "(+ S0)" is settled by the ASN's own claim structure, requiring neither Nelson nor Gregory.
