# Channel Assignment — ASN-0124 review-1

**Date:** 2026-06-12 18:33

## Issue 1: FD-FRESH composes a transition the note's own state model cannot express
Reason: This is a modeling-consistency defect between the note's declared vocabulary and a borrowed ASN-0082 transition; the review's option (a) gives a complete in-vocabulary recomposition (K.α*, full-clear K.μ⁻, rebuild K.μ⁺, K.ρ) whose stepwise invariance derivation follows from FD-STEP and freshness already in the note. Neither design intent nor implementation evidence bears on which formal presentation to use — the fix is internal.

## Issue 2: FD-LOSSY's witness is a sketch, not a construction
Reason: The required fix is to exhibit two concrete reachable states with full composite sequences and boundary checks, at the rigor FD-NEUT(c) already demonstrates; the review even sketches a realizable pattern using only the note's own composites and J0/J1★ obligations. Purely internal proof completion.

## Issue 3: Two-phase dynamics for `finddocs_V` stop at a qualitative remark
Reason: The missing monotone inclusions follow directly from lemmas the note already holds (F-IMG-MONO/F-IMG-CONTR via FD-IMGC, FD-STEP, FD-IMONO), and the reorder-on-named-document case needs only a constructed example or stability lemma within the existing model; the present-tense resolution semantics it rests on is already settled by D-PRES and the Q8 consultation. Internal derivation work.

## Issue 4: The worked illustration fires a reorder whose precondition fails
Reason: The fix is mechanical — relocate the reorder step to a document where K.μ~'s enabling conditions hold (d_A or pre-contraction d_B), all within the illustration's existing construction. No external input needed.

## Issue 5: FD-COOC's full-containment identity breaks at `I = ∅`
Reason: An empty-boundary guard or an explicit empty-intersection convention over `dom(Σ.M)` resolves it, matching how the note already handles its other degenerate cases. Internal formal hygiene.
