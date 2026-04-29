# Revision Categorization — ASN-0051 review-5

**Date:** 2026-03-20 21:25

## Issue 1: SV6 implicit element-level precondition on span start
Category: INTERNAL
Reason: The precondition `zeros(s) = 3` is already implicit in the proof's use of `origin(s)` and "action point within the element field." The fix is adding an explicit statement of what the proof already requires.

## Issue 2: SV3 asymmetric resolution treatment
Category: INTERNAL
Reason: The resolution argument for contraction is already sketched in the review itself and follows directly from the contraction frame condition and existing definitions. It mirrors the SV2 resolution paragraph already present.

## Issue 3: SV7 is a definitional tautology
Category: INTERNAL
Reason: The fix is either reframing as a design remark or strengthening the formal statement using definitions already in the ASN (e.g., the transclusion discovery consequence follows from the existing definitions of `discover_s` and `K.μ⁺`). No external evidence needed.

## Issue 4: SV13(e) imprecise about reordering and resolution
Category: INTERNAL
Reason: The correction ("changes" → "may change") is directly derivable from SV5's own "in general" qualifier and the worked example already in the ASN, which demonstrates a reordering that preserves the resolution set.

## Issue 5: SV13(f) blends proved and architectural claims
Category: INTERNAL
Reason: The ASN body already correctly distinguishes proved claims from architectural observations ("architectural, not definitional"). The fix is carrying that same distinction into the SV13 summary, which is an editorial adjustment within existing content.
