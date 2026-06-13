# Channel Assignment — ASN-0133 review-10

**Date:** 2026-06-13 15:16

## Issue 1: H-FAIR's discharge condition omits in-domain trigger falsification
Reason: Internal. The correction — adding "T_ρ(x,·) becomes ⊥" as a third discharge, pinning "fired" to *real* fire, re-splitting Q6's post-N cases, and repairing the H-SFAIR ordering — is built entirely from machinery the note already owns: SF ⊥-stability (Q-EXT/PD0), the falsifier inventory (Q-FLIP), environment steps emitting through the same surface (RG), and the worked example's own "environment comments t" scenario. Fairness is the corpus's own stated hypothesis, not a design-intent or implementation question, and the reviewer confirms the termination conclusions are untouched.

## Issue 2: marker-pattern extinction for idem=⊤ classes skips the dedup-miss step
Reason: Gregory. The fix turns on two operation-surface facts inherited from ASN-0128, not stated in ASN-0133: what an idem=⊤ `Emit_K` deduplicates against (so a ⊤ audit-slice trigger precludes a hit and the emit actually grows `L_K`), and whether a born-nullified deposit still enters the audit slice. Both are implementation semantics of `Emit_K`/nullification, which is Gregory's evidence domain.
Gregory question: For an idem=⊤ Binary K, does `Emit_K`'s deduplication test against a slice contained in the audit slice (so a fire whose audit-slice trigger is ⊤ cannot hit dedup and the emit deposits into `L_K`), and does a born-nullified `Emit_K` deposit still enter the audit slice `L_K`?

## Issue 3: regime (ii) calls a still-assumed bound "structure not assumption"
Reason: Internal. The note already states in Q5a and H-RF that Q5a's route requires bounded domain growth and that this bound is "reachability-quantified … as meta-level as H-W"; the fix is just to make regime (ii)'s wording consistent with the note's own classification, using the reviewer-supplied replacement text.
