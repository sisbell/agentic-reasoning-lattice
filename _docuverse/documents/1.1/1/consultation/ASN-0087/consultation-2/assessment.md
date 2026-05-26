# Channel Assignment — ASN-0087 review-2

**Date:** 2026-05-26 12:06

## Issue 1: Invariant table omits S2 (functionality)
Reason: The fix is fully specified by the reviewer using D-SEQ★ at Σ and K.μ⁺_L's positioning rule, both already cited in the ASN. Derivable from existing content.

## Issue 2: Invariant table omits trivially-preserved per-state invariants
Reason: The required enumeration relies on frame conditions (`C`, `E`, `R` unchanged) and K.λ's freshness, all already established in the ASN. The reviewer has supplied the justifications.

## Issue 3: LP3★ citation in Reflexive Endsets is needlessly indirect
Reason: A direct derivation using K.λ's effect and K.μ⁺_L's frame on `L` — both already in the Effect and Frame sections. The reviewer has provided exact replacement text.

## Issue 4: "Reassign" terminology in Permanence is imprecise
Reason: The fix uses K.μ~-FIX (substrate spec already referenced via ASN-0093/ASN-0047). The reviewer has supplied the precise semantics needed to rephrase.

## Issue 5: Intermediate state Σ_mid invariant preservation not verified
Reason: The verification follows from K.λ's frame on `M` and the fact that `dom(L)` only grows — both already established in Preconditions. Reviewer has provided the justification.

## Issue 6: M-PriorLinkDisc scope is under-specified
Reason: The `d_target ≠ d` case follows directly from K.μ⁺_L's frame `(A d' ≠ d :: M'(d') = M(d'))`, already stated in M-Frame. Pure scope extension of an existing argument.
