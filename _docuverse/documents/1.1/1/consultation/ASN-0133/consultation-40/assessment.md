# Channel Assignment — ASN-0133 review-40

**Date:** 2026-06-14 12:51

## Issue 1: Single-target removal cannot make the producer's half "unreached"
Reason: Fix is internal — it aligns the parenthetical with the note's own Q6 case taxonomy. The distinction (single oscillating argument = case (2) holding-failure via vacuously-true empty-domain conjunct; ≥2 out-of-phase arguments = case (3) reaching-failure) is fully established in Q6, so relabeling as case (2) or extending to ≥2 targets is derivable from the ASN alone.

## Issue 2: The stratification "repair" is asserted, not derived, and introduces undefined machinery
Reason: Fix is internal — the review supplies the missing route through Q5a ("resolver emissions never enlarge `[D_{ρ_P}]`" ⟹ producer-domain growth is external input ⟹ Q5a ⟹ H-RF), and Q5a and Open Question 4 are already in the note. Deriving the corollary or demoting the "stratum" framing to future work needs no design intent or implementation evidence.

## Issue 3: The S-monotonicity rationale is stated twice, SC forward-justifying Q9's content
Reason: Purely editorial deduplication within the note — move the anti-monotone rationale and `¬S(addr(x))` counterexample to Q9, leave only the constraint statement at SC. No external channel.

## Issue 4: The H-W critique buries a one-line fact under editorial framing
Reason: Purely editorial tightening — the circularity fact (`|W(σ)| < ∞` forces a maximal trigger-true index, so H-W ⟹ reaches-and-holds quiescence) and the H-RF < bounded-growth < conclusion ordering are already present; only the surrounding restatement needs cutting. No external channel.

## Issue 5: `is_in_chain` does not reach `chain`'s default-view value
Reason: Fix is internal — the corrective facts (UV never rewrites `is_in_chain`, it reads the unrewritten active walk and is view-stable; only `elems(chain(x))` needs the set-valued filter rebuild) are fixed by ASN-0129's UV and already restated in Q0. Separating the two quantities is a re-framing of content the note already carries, not a question of implementation behavior or design intent.
