# Channel Assignment — ASN-0119 review-38

**Date:** 2026-06-10 06:34

## Issue 1: The P4a discharge invokes an induction whose measure, base, and hypothesis are never stated
Reason: The fix is a proof-structuring exercise — making explicit the induction the argument already leans on (measure = number of composites, base = Σ₀ with R₀ = ∅ rendering P4a vacuous, step = case on the final composite). Both cases are already in the text and the base/measure are standard properties of the ASN-0047 reachable-state framework the note already builds on, so no design intent or implementation evidence is required.

## Issue 2: The RA1/RA2 citation cross-annotations do not line up and add parse overhead without advancing the argument
Reason: Pure citation bookkeeping against ASN-0084, a peer specification the author already cites — not a question of design intent (Nelson) or implementation behavior (Gregory). The reviewer has already enumerated which ASN-0084 lemma proves each result (ArrangementRearrangement + R-PPERM/R-SPERM → bijection equation; R-PPERM/R-SPERM → bijectivity; R-PIV/R-SWP → domain identity; R-RI → range equality), so the fix is to align the table and body to that enumeration and drop the cross-annotations.
