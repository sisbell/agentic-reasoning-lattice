# Channel Assignment — ASN-0071 review-56

**Date:** 2026-06-03 10:55

## Issue 1: F-DEEP introduced by forward-reference to an undefined label
Reason: Pure expository ordering. The mechanism (S8-depth forcing `#v = m_C < #u`, hence empty intersection via the `#v < #u` case) is already fully derived in the ASN; restating F-DEEP on its own terms or moving the F-FILT introduction earlier requires only the ASN's own content.

## Issue 2: `wp-defined` used in *Resolution* before it is defined in *The operation*
Reason: Pure expository ordering. The definition `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` and its justification (M1, P1 of ASN-0047) are already present; relocating it to the first `iaddrs_one` use is internal.

## Issue 3: PC-RANGE prose gloss overstates the captured set
Reason: The set equation is already proven correct in the ASN; the fix only weakens the gloss to "lies within" and notes membership is determined by `∩ dom(M(d_s))`. D-SEQ★'s prefix-pinning is a prior-ASN structural property the author can apply directly, so no channel is needed.
