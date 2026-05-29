# Channel Assignment — ASN-0045 review-13

**Date:** 2026-05-28 19:45

## Issue 1: Z0 is an unnecessary stipulated premise — T4c already constrains the range
Reason: The fix is internal — it turns on whether T4c's bijection (cited as ASN-0034) already delivers `zeros(t) ∈ {0,1,2,3}`, which is verifiable against the cited T4c contract within the spec corpus. No design intent or implementation evidence is required; the resolution is to replace Z0 with a citation to T4c's already-established domain.

## Issue 2: at-most-one is also a redundant reconstruction of T4c injectivity
Reason: Internal — the choice between citing T4c's injectivity (already in the cited ASN-0034) plus functionality of `zeros`, versus the numeral-distinctness reconstruction, is a presentation/citation decision derivable from the ASN's own dependencies. Neither Nelson's intent nor Gregory's code bears on it.

## Issue 3: citation to a nonexistent "Definition slot" of T4c
Reason: Internal — this is a pure citation-target correction checkable against T4c's actual contract structure (Preconditions/Postconditions) in the cited ASN-0034. The rename derivation is otherwise sound; only the slot name must be fixed, which needs no design or implementation channel.
