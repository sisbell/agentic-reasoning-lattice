# Channel Assignment — ASN-0130 review-3

**Date:** 2026-06-12 09:18

## Issue 1: `sig` and "valid encoding" are circularly grounded for reference-bearing runs
Reason: The fix is a formal stratification the note already contains the pieces for — PR0's (ii)/(iii) split gives the syntactic/type-level separation, and PR2's first-registration induction grounds `sig` on ever-registered addresses. No design intent or implementation evidence bears on a well-foundedness repair.

## Issue 2: PR3a's variable hygiene is asserted, not arranged — and the note's own worked example violates it
Reason: This is standard substitution metatheory — extend the renaming to parameters, state the weakening lemma, redo the PC2 applications — all derivable from WT/WT-ref as the note states them. Neither Nelson's intent nor the C implementation has anything to say about α-conversion discipline.

## Issue 3: `expand` is not a function as defined, but PR3 and PR5 treat it as one
Reason: The fix is a formal choice the review itself narrows (canonical content-determined renaming composes with Issue 2's fix and makes PR3/PR5's claims literally true), and the ASN's S0/identity commitments already favor a canonical spelling. Internal.

## Issue 4: the certification operation has no contract
Reason: The fix instantiates the note's own PR0 template at the `pd_stable` class — signature, validation order, I1 branch behavior, and a PR1-analogue all follow the patterns already in the ASN, and the remaining choices (separate call vs. flag, target must be actively registered for the lint's active-view reading to cohere) are constrained by the note's own text and worked example. Internal.

## Issue 5: the worked composition uses an operation and an atom that don't exist in the system
Reason: Spelling `under_cap` in genuine PL is internal (the PC2a count-comparison route is already named), but rewriting "INSERT" as K.α steps requires knowing what contiguity the real allocator actually guarantees for a single insertion — exactly the evidence the review says "INSERT" papers over.
Gregory question: When udanax-green stores newly inserted text, does a single insertion mint consecutive I-addresses on the document's origin chain as one uninterrupted run, or can interleaved operations (on the same or other documents) leave one insertion's addresses non-contiguous?
