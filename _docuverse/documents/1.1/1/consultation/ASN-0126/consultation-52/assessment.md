# Channel Assignment — ASN-0126 review-52

**Date:** 2026-06-09 13:12

## Issue 1: the wp failure-mode prose claims only one landing conjunct can fail; in fact two can
Reason: Internal. Both failure conditions are already stated in the note's own wp — C2 (`K ≁ R ∨ a_emit ∉ coverage(G)`) is false exactly for a self-nullifying retraction, which the note's P5 realizes via its own unit-depth wrapper `{(a_emit, δ(1,#a_emit))}` (Binary-conformant, self-covering), and C3's failure is witnessed by the note's own Born-nullified example. The C2-inherited / C3-newly-live distinction is grounded in the worked example's own Step-1 remark that the C3 witness's range "could not [be] suppl[ied by] the unit-depth wrapper," so no design-intent or implementation evidence is required.

## Issue 2: the third conjunct's meaning is restated three times before the substantive point
Reason: Internal. Pure prose consolidation of the note's own three restatements of C3 into a single statement-then-argument, folding in the Issue 1 correction — nothing turns on design intent or implementation behavior.

## Issue 3: the "K registered ⟹ K ∈ T_admissible" derivation is written out twice
Reason: Internal. The four-step chain is already proved (twice) within the note from its own C0 and coverage definitions; extracting it as one cited lemma is a refactor of existing content, derivable without external evidence.
