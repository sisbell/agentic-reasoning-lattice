# Channel Assignment — ASN-0102 review-15

**Date:** 2026-06-03 16:19

## Issue 1: ActivatedEmission is never discharged
Reason: Internal — the fix is fully determined by COPY's own frame (`Σ'.E = Σ.E`, no entity-level sub-allocation) and the existing vacuous-bucket reasoning pattern; no design intent or implementation evidence is in question.

## Issue 2: ExtendedTransitionInvariants (P3) is not discharged
Reason: Internal — P3 is trivially discharged by citing the COPY frame already stated in the Definition (`Σ'.C=Σ.C`, `Σ'.L=Σ.L`, `Σ'.E=Σ.E`, `Σ'.R ⊇ Σ.R`); the obligation and its discharge are both derivable from the note's own content.

## Issue 3: Worked example does not exercise the subtlest part of X14
Reason: Internal — extending the worked example to a self-transclusion (`d_s = d`) scenario only requires instantiating the existing COPY definition and the New/Old split already proven in X14; the J1★/J1'★ branches are settled in the note, so tracing a concrete `Σ'.R` needs no external input.
