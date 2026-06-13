# Channel Assignment — ASN-0130 review-28

**Date:** 2026-06-13 06:27

## Issue 1: PR5's threshold extension is phrased to over-reach, then walled off by a digression
Reason: Internal. The fix narrows the phrasing to the two cases ("ℕ literal or environment-bound parameter") that PR5 itself already names as the only reachable ones, and deletes the digression. Both the two-case enumeration and the soundness ground it leans on (fixity across a step is the only property PD0's argument consumes) are already present in the note; no design intent or implementation evidence is needed.

## Issue 2: PR3a's capture-freeness justification is false for the sequential intermediates it invokes
Reason: Internal. The repair re-articulates capture-freeness from facts PR3a already establishes — `u`'s binders are all expansion names, each `yⱼ` occurs only within `u` at parameter positions, the `Eⱼ` sit in disjoint subtrees, and `yⱼ ∉ Eᵢ`. Both suggested options are pure substitution mechanics over in-note facts; no external channel required.

## Issue 3: PR5a restates the idem-⊤ hit/miss dynamics PR0 already spells
Reason: Internal. Pure deduplication — replace the restated hit/miss block with a deferral to I1's idem-⊤ contract (ASN-0128, already cited) exactly as PR0 invokes it, keeping only the Unary `G = ∅` note. Entirely editorial.
