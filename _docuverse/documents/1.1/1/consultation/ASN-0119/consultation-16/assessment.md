# Channel Assignment — ASN-0119 review-16

**Date:** 2026-06-09 17:50

## Issue 1: Imprecise characterizations in the P7c (footprint run-structure) discussion
Reason: Internal — this is a terminology and logical-phrasing correction grounded entirely in the note's own content. The note already computes the negative per-region displacements (`−w_α`, `−(w_α+w_μ)`), already cites ASN-0034's shift (defined for `n ≥ 1`) and R-COMM (which licenses `π(v+k)=π(v)+k` regardless of sign), and already supplies both the correct term ("constant displacement") and the precise sub-case labels that the umbrella sentence is meant to be replaced by. No design intent or implementation evidence is required.

## Issue 2: Open Question 5 is answered within the note
Reason: Internal — the note already proves the property OQ5 asks about (π maps each subspace onto itself in the S3★ derivation; the middle displacement `w_β − w_α` is realized by R-S2 strictly within `V_S(d)`; the well-definedness section states the abstract operation admits no boundary-crossing collision). The retarget material — the green formula-based boundary-crossing defect — is already cited in that same section via Question 17, so dropping or retargeting the OQ draws only on content already present.
