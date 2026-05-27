# Channel Assignment — ASN-0099 review-18

**Date:** 2026-05-26 21:32

## Issue 1: A1 transient status creates a convergence-blocking dependency on ASN-0047
Reason: The fix is a cross-ASN amendment to ASN-0047's K.μ⁺, K.μ⁻, K.ρ frame clauses; validating that this amendment is correct requires both design intent (whether these operations were meant to be link-preserving) and implementation evidence (whether the actual code leaves L untouched).
Nelson question: Was the design intent that content-editing operations (K.μ⁺, K.μ⁻) and provenance recording (K.ρ) leave the link store completely unmodified, with link allocation reserved exclusively to K.λ?
Gregory question: In the udanax-green implementation, do the routines corresponding to content extension, content contraction, and provenance/redirect recording ever modify the link store, or is link mutation confined entirely to the link-allocation routine?

## Issue 2: F9★ scope is narrower than the natural multi-step lift of F9-cor
Reason: F9-cor already establishes single-step preservation across V ∖ {K.λ}, and transitivity supplies the multi-step lift directly; no external evidence or design-intent question is needed to broaden F9★ or add a companion claim.

## Issue 3: F12 conflates definition and claim
Reason: This is a presentation and labeling issue internal to ASN-0099 — the choice between treating F12 as a definition vs. a claim, and how to surface that in the claims table, is resolvable from the ASN's own structure without external input.

## Issue 4: F4's universality argument lacks realizability discharge for non-enumerated strengthening classes
Reason: The realizability material is already in the ASN (K.λ's precondition admits arbitrary endsets subject to well-formedness, and the canonical-span witness construction generalizes); sharpening F4's abstract claim to a reachability-based formulation or narrowing to the enumerated classes is an internal restructuring of the argument.
