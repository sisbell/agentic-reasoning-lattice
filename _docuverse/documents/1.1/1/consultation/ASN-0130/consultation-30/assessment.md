# Channel Assignment — ASN-0130 review-30

**Date:** 2026-06-13 07:17

## Issue 1: (iii)'s decidability attributed to (iv), in tension with PR1
Reason: Internal — the fix realigns PR0's justification of (iii) with machinery already in the note: PR-SIG ("sig is defined exactly on the ever-registered addresses"), PR1's conjunct-division (treating (iii) as content/signature-intrinsic and (iv) as the lone active-membership conjunct), PR2's acyclic DAG (supplying the decidable down-the-DAG audit check), and PR3's "de-registered definition therefore still resolves, expands, and evaluates." No design intent or implementation evidence is at issue.

## Issue 2: PR5 states the ST⁺ parameter reading twice
Reason: Internal — pure redundancy collapse. The parameter reading and its soundness ("fixity across a step") are fully stated within PR5; the fix is to name it once in the opening, define it once in the Parameters qualification, and reduce the repeated "fixed" to a single sentence. Nothing turns on undocumented intent or code behavior.

## Issue 3: PR5's View qualification restates PR-VIEW
Reason: Internal — PR-VIEW already establishes denotation-invariance and the respelling-availability remark; the only new content is the rationale (PD0's classes are view-relative). The fix is to cite PR-VIEW and keep the rationale, derivable entirely from the note's own text.

## Issue 4: PS2 — meta-prose around the "entry-point seal below"
Reason: Internal — structural/prose fix. The enforcement claim is already delivered once by the *Entry points — the seal* paragraph; reducing PS2 to "Emitted only by certify_pd_stable (PR5a)" requires no external input.
