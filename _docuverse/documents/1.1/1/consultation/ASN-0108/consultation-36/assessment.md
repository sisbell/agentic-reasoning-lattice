# Channel Assignment — ASN-0108 review-36

**Date:** 2026-06-13 05:16

## Issue 1: "matched-content key" and "content-position key" conflated in W6
Reason: The fix is a naming-scheme decision (declare "matched-content key" a family with two variants, or keep three flat names and reword W6 to "either content-drawn key") among constructs the note itself defines and already characterizes; no design intent or implementation evidence bears on the choice.

## Issue 2: "sole abstract respect in which the two identity keys differ" overstates, and is duplicated
Reason: "Sole" is contradicted by the note's own composite-key caution (the matched-content key needs an appended address tiebreaker to satisfy W0/W1) — a second divergence already stated in the body; narrowing the claim, stating it once, and dropping "(the comparison's home)" draws entirely on content already present.

## Issue 3: accreted "allocation is orthogonal" defensive prose (W5/W8)
Reason: Collapsing the allocation-rebuttal passages to a single positive statement (the address key is a state-independent function of the held value, hence frozen and computable) is pure prose editing; the load-bearing computability-vs-value-totality distinction it must preserve is already in W8.

## Issue 4: "No per-cursor local condition characterizes coherence" asserted beyond its support
Reason: Both offered remedies — supplying the meta-argument (a per-transition predicate cannot witness cross-cursor cancellation, so a whole-pass outcome is not per-cursor characterizable) or softening to "clause 1, the natural per-cursor condition, is not necessary" — are internal to the note's existing cancellation-walk logic; no external fact is needed.

## Issue 5: Open Question 4 is substantially answered in the body
Reason: W8 and W9 already establish that both permanent keys (Nelson's address key and Gregory's matched-content I-address key, each shown permanent in the note) keep `κ(c)` computable through orphaning, so an empty window certifies genuine exhaustion and only the rejected content-position key conflates the two; deciding to remove OQ4 or restate it as resolved follows from the note's own content.
