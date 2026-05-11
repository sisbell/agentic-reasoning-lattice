# Channel Assignment — ASN-0040 review-28

**Date:** 2026-05-11 11:27

## Issue 1: Empty B₀ is inconsistent with ASN-0034's singleton-root genesis under Bridge2
Reason: The choice between tightening B₀ conf. to require B₀ ⊇ allocated(Σ_init) versus retaining the "possibly empty" license turns on Nelson's design intent — whether the system was meant to admit a genuinely empty genesis or whether at least one root address (Nelson's "Earth node" or analogous) is constitutive of the address space at startup.
Nelson question: Did Nelson's design require at least one root address (e.g. an "Earth node" or designated initial position) to exist at system genesis, or did the design admit a system that begins with an empty address space and grows entirely by baptism?

## Issue 2: B6(i) necessity argument cites "collapsing B7" where B8 is the property actually at risk
Reason: This is a labeling correction internal to the ASN — the reviewer identified B8 (global uniqueness) as the property actually at risk and provided exact replacement wording. The substantive argument is unchanged; only the cross-reference is wrong.

## Issue 3: B1 sub-case (C) collapses the stream-identity step at its cross-reference
Reason: The stream-identity result S(p, 1) = S(p', 2) is already proved earlier in the same sub-case; the fix is to re-invoke it explicitly at the cross-reference. Derivable from the ASN's own content with the exact insertion the reviewer specified.
