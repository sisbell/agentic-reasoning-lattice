# Channel Assignment — ASN-0102 review-50

**Date:** 2026-06-08 00:33

## Issue 1: J1'★ embedded discharge conflates the New/Old split (at COPY's pre-state) with the branch split (at the composite boundary)
Reason: Internal. The defect is a mismatch between two reference points both already defined in the ASN — `New`/`Old` at COPY's pre-state `Σ_i` and branch (a)/(b) at the boundary `Σ_0` — and the fix (argue the step-local extension against `Σ_i`, the boundary obligation against `Σ_0`) is derivable from the ASN's own definitions and the deferral to `ValidComposite★` it already states. No design intent or implementation evidence is at issue.

## Issue 2: Forward-reference / deferral accretion in the Amendment and X14
Reason: Internal. This is a purely expository restructuring — consolidating the standalone/embedded boundary reading into one named lemma, stating the step-local discharge once, and replacing the imagined `K.μ⁻` narration with a one-line pointer to `ValidComposite★` clause-2 — all reorganizing content already present in the ASN, requiring no external input.
