# Channel Assignment — ASN-0112 review-50

**Date:** 2026-06-08 12:55

## Issue 1: V11 closing sentence recaps the paragraph; "freshly created or fully emptied" duplicated
Reason: Pure editorial deduplication — removing a recapping clause and a doubled phrase within one paragraph. No design intent or implementation evidence is at stake; the empty-case semantics (`⟨⟩`, undefined `min`, sentinel-not-address) are already fully established in the ASN.

## Issue 2: equidepth-from-S8-depth re-derived across adjacent V-ReachTight and V-LevelUniform paragraphs
Reason: Internal restructuring — establish the single-subspace equidepth fact (from S8-depth, already in the ASN) once and have the second paragraph cite it. No external input needed; the shared premise is wholly derivable from foundation facts the note already cites.
