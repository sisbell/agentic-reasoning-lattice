# Channel Assignment — ASN-0133 review-50

**Date:** 2026-06-14 17:30

## Issue 1: The worked registry's "type isolation" claim is false
Reason: The asymmetric structure the fix requires is already stated in the note — ρ_P's `Emit_cmt` grows `L_cmt` (= ρ_R's domain), and "a `res` lands in `L_res`, which `T_P` never reads"; the fix reconciles the note's internal contradiction using facts already present.

## Issue 2: "H-FAIR satisfiable against an arbitrary environment" contradicts "no turn-fairness is stated"
Reason: The fix corrects an overreaching satisfiability claim using the note's own definitions (H-FAIR's three discharges, the consecutive-environment-step interleaving model) and the standard weak-vs-joint turn-fairness distinction the note already gestures at by deferring scheduler construction to the implementation layer.

## Issue 3: Regime (i) and its content-deposit subsumption are stated three times
Reason: Pure de-duplication of the note's own prose — define regime (i) once in the Q6 bullet and back-reference it from the proof and H-SFAIR; no external input needed.

## Issue 4: Residual defensive meta-prose
Reason: Pure editorial cut of defensive codas and one Q3/OQ5 duplication; OQ5 already carries the sufficiency-not-necessity point, so the fix is internal.
