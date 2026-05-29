# Channel Assignment — ASN-0040 review-61

**Date:** 2026-05-28 22:57

## Issue 1: Excess-zero parent not covered by necessity sub-case (a)'s mechanism
Reason: Internal. The fix adds a count-violation configuration whose conclusion (`zeros(c₁) ≥ zeros(p) > 3`) follows from TA5(b) zero-preservation, already cited in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Trailing-zero d=1 exception restated four to five times
Reason: Internal. Purely an editorial deduplication — consolidate five restatements of an exception already fully argued within B6; no external channel bears on where the prose sits.

## Issue 3: "Disjointness motivation" paragraph justifies its own placement
Reason: Internal. Deleting meta-prose about document ordering while keeping the substantive S2/namespace-collision content requires no design or implementation input.

## Issue 4: B6 statement preamble duplicates the necessity proof with same-document forward pointers
Reason: Internal. Trimming the preamble to table plus interpretive reading and removing same-document forward pointers is a presentation edit; the necessity argument already lives in the proof.

## Issue 5: Misattributed citation in Bop freshness proof
Reason: Internal. The ASN's own freshness argument shows the conclusion rests on B1 and S0, not B4; correcting the citation is derivable from the surrounding proof text.

## Issue 6: B0b enumerates its downstream consumers
Reason: Internal. Dropping the consumer-inventory sentence while retaining B0b's statement and reduction is a self-contained editorial cut; each downstream proof already cites B0b at use.
