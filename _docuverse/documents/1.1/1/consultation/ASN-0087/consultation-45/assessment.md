# Channel Assignment — ASN-0087 review-45

**Date:** 2026-06-04 00:32

## Issue 1: Navigation-only deferral sentence in *Freshness of the Allocation*
Reason: Pure deletion of a forward-pointer sentence; the S2 verification is self-contained within the ASN. No design intent or implementation evidence is required.

## Issue 2: Defensive meta-characterization trailing M-DepthConv
Reason: The fix restates M-DepthConv's existing rule and scope (already fully specified in the ASN) and drops a classificatory gloss. Internal to the document.

## Issue 3: Presentation-justification framing in *Side Effects on Prior Links' Discoverability*
Reason: The confinement result and its justification (frame-preservation for `d_target ≠ d`) are already derived inline in the section; the fix only removes the meta-wrapper. Derivable from the ASN alone.
