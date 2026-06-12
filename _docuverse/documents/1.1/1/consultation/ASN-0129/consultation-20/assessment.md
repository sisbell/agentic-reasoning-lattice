# Channel Assignment — ASN-0129 review-20

**Date:** 2026-06-11 22:04

## Issue 1: "A composite cannot convert between regimes" is asserted as fact, and the note's own constructions contradict it
Reason: The replacement statement is derivable from the note's own constructions, but recasting AM keying and BH3's opt-in reverse lookup as "atom-level conventions" touches design intent (was D4's opt-in a deliberate capability fence?) and needs implementation evidence on whether the read path itself already performs coverage-keyed matching for every type — both channels bear on whether any genuine residual non-conversion claim should be stated.
Nelson question: Was BH3's typed-reverse-lookup intended as a genuine capability fence — reverse access deliberately withheld from types that don't opt in — or as an indexed/efficient affordance over a query the system was always understood to answer by per-tuple filtering?
Gregory question: Does udanax-green's link query (findlinks/findlinksfromto) match the from-set by coverage/intersection rather than exact endset value, and does it answer reverse-direction (to-set-keyed) queries for every link type without any per-type opt-in?

## Issue 2: Five sites defer to Open Question 6, with the parity assessment stated twice
Reason: The fix is pure consolidation — choosing one statement site per conjecture and reducing the others to bare pointers — entirely determined by the note's own text; no design intent or implementation evidence bears on where prose lives.

## Issue 3: Defensive, reviewer-facing prose and within-section duplication
Reason: All five instances are deletions or single-site consolidations of content the note already states elsewhere; the fix is internal editing with no semantic question for either channel.
