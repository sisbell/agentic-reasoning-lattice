# Channel Assignment — ASN-0053 review-30

**Date:** 2026-05-28 19:34

## Issue 1: S7 title overclaims — covering is not representation
Reason: Internal. The proof already establishes that the constructed span covers a half-open interval (containing deeper points by the span denotation already defined), so the cover-vs-representation distinction and subtree-convexity are derivable from S0 and the ASN's own definitions; renaming and noting the impossibility is editorial.

## Issue 2: Restated prose in "The reach function"
Reason: Internal. Deleting the redundant restatement and reducing the `a = b` case to a single clause requires only the content already present in the section.

## Issue 3: "Observations from the implementation" is implementation-mechanics essay
Reason: Internal. The fix is to cut defensive framing and implementation-mechanics prose; the encoding example to potentially retain (Q13) is already in the ASN, so no new evidence is needed to decide what to remove.

## Issue 4: S6 carries motivational essay in a definition slot
Reason: Internal. Reducing S6 to its definition plus the load-bearing fact (same length ⇒ type-(i) divergence, D0 satisfied) and tightening the analogy uses only material already in the section; no design-intent or implementation evidence is required.

## Issue 5: Label collision on "D2"
Reason: Internal. Renaming the locally-derived span-level consequence to avoid colliding with ASN-0034's D2 label is a purely editorial fix derivable from the ASN's own structure.
