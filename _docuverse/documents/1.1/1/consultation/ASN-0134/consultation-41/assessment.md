# Channel Assignment — ASN-0134 review-41

**Date:** 2026-06-14 12:08

## Issue 1: The target-residence race is developed in three places with mutual deferrals
Reason: Internal. The race is already fully developed in §4 (the `A;B`/`B;A` scenario, rejection-to-zero, emit-before-retract remedy); the fix only relocates W5's re-derivation to a one-clause cite and lets OQ9 stand. No new design intent or implementation evidence is in play — the content stays in §4 unchanged.

## Issue 2: "Design intent" asides explain why a claim matters rather than advance it
Reason: Internal. The fix is deletion of asides that re-quote Nelson to restate significance; the design-intent framing and the three quotes already live in the epigraph/intro. Nothing new about Nelson's intent is being asserted, so no theory-channel verification is needed.

## Issue 3: Defensive justifications for roads not taken
Reason: Internal. The scope commitments (𝔼 = the ASN-0093→0128 stack; `K.σ` freshness and register-before-allocate assumed from the entity layer) are already load-bearing and stated; the fix only trims the defense of the excluded alternative. This is an argument-structure edit, not a question about what the design or implementation does.

## Issue 4: Clause 6 is a self-admitted redundant contract clause defended by surrounding prose
Reason: Internal. The note already proves via W6 that no runtime step writes the registry; demoting clause 6 to a remark and dropping the "minimal modulo" hedge uses only content already established. No external confirmation of registry behavior is needed beyond what W6 already cites.

## Issue 5: A6 enumerates its downstream consumers
Reason: Internal. Dropping A6's forward pointers to W0/W3 (which already cite A6 where stated) and merging OQ4/OQ5 (both ask for A5's batch-atomicity-to-a-reader contract) is purely editorial cross-referencing cleanup, derivable from the ASN's own structure.
