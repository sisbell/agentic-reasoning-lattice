# Channel Assignment — ASN-0093 review-55

**Date:** 2026-05-31 10:12

## Issue 1: SubspaceConventionAxiom statement and provenance duplicated verbatim
Reason: Purely editorial deduplication — the canonical statement and provenance already live in the State model; reducing the table row to a pointer requires no design intent or implementation evidence.

## Issue 2: M2 enumerates which foundation invariants it makes vacuous
Reason: Dropping a downstream-consumer enumeration is internal to the note; the fix removes text without needing any external constraint or evidence.

## Issue 3: Worked-example Step 8 re-narrates the abstract freshness lemma instead of checking concrete tumblers
Reason: The concrete tumbler values (`ℓ_new = [1,0,2,0,5,0,2,2]`, `ℓ`, `ℓ''`, and the content addresses) are all present in the ASN, so the position-wise distinctness check is derivable internally.
