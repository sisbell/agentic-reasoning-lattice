# Channel Assignment — ASN-0108 review-48

**Date:** 2026-06-13 09:10

## Issue 1: The "relevant endset slot" is never defined, yet Gregory's key rests on it
Reason: The undefined slot sits inside Gregory's content-key reading — an abstraction of the spanfilade traversal — and the note's load-bearing claims (permanence, state-stability, computability through orphaning) all require the key to read a *fixed*, state-independent function of the link's immutable endsets; whether the udanax-green index actually keys on such a fixed slot (rather than the currently-matched endpoint, which the note itself rules out) is an implementation fact only Gregory can supply. Nelson's intended key is the address key, which has no slot ambiguity, so design intent is not at issue.
Gregory question: In udanax-green's link search, which endset slot(s) of a link does the spanfilade index it under — from, to, three, or some fixed union — and is that position a fixed function of the link's immutable endsets, independent of whichever endpoint a given query currently matches?

## Issue 2: Editorial value-assertions and cross-section re-announcement (anti-bloat)
Reason: Pure editorial/structural fix — excise the value-assertion asides and state the computability/state-stability/value-totality taxonomy once at W8 with W9/W9b referencing it. Every element involved is already present in the note; no design intent or implementation evidence is needed.

## Issue 3: LP18 cited for a case its precondition excludes
Reason: The review has already supplied the corrected citations (LP9 ExtensionMonotonicity for the general "becomes discoverable" event, LP18 as its orphan instance, L4/L9 for born ghosts) and confirmed the reasoning is sound; it is a mechanical citation swap verifiable against ASN-0098 and ASN-0043, which the note already cites extensively, so no channel consultation is required.
