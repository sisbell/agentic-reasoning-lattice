# Channel Assignment — ASN-0131 review-92

**Date:** 2026-06-14 19:05

## Issue 1: "Three further transition kinds" claims three, elaborates one
Reason: Internal. The note already cites the link-store frame for both K.α and K.ρ (`L' = L`, ASN-0047/ASN-0093) in the "Fresh emissions" section, and the parallel arrangement-frame facts the fix needs (K.α: `M' = M`; K.ρ: `M'(d) = M(d)` / LP14 projection-invariance) live in the same sibling ASNs the note already builds on — the reviewer has pinpointed every citation. Discharging the count is spec-internal bookkeeping requiring no design-intent or implementation evidence.

## Issue 2: Worked-example mischaracterizes a unit-depth span's coverage
Reason: Internal. The correct semantics — `coverage({(a₂, δ(1, #a₂))}) = {t : a₂ ≼ t}` (PrefixSpanCoverage, ASN-0043) — is invoked throughout the note and stated explicitly two paragraphs earlier for the structurally identical span `(a₄, δ(1, #a₄))` ("reaching only `a₄` and its descendants"); the fix is to make the one inconsistent phrase agree with the note's own coverage semantics.
