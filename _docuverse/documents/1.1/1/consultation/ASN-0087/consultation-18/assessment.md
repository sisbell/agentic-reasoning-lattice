# Channel Assignment — ASN-0087 review-18

**Date:** 2026-06-03 10:37

## Issue 1: m_L(d) = 2 asserted as universal, not derived
Reason: Fully internal. The justification depends only on the substrate operation set (ASN-0047/0093) and M-DepthConv — the review itself supplies the missing argument (J4/ForkComposite copies only the content subspace, so MAKELINK is the sole link-placement path) plus an induction over document history. No design intent or implementation evidence is needed.

## Issue 2: v_ℓ freshness justified only within-subspace at point of claim
Reason: Fully internal. The cross-subspace exclusion (SC-NEQ at position 1) is already proven in this ASN's own S2 verification; the fix is to complete the argument inline or forward-reference S2.
