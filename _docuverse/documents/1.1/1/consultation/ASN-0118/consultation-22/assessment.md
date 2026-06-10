# Channel Assignment — ASN-0118 review-22

**Date:** 2026-06-10 07:35

## Issue 1: Use-site inventory and non-use note in the resolution section
Reason: Pure prose-trimming. The fix deletes a forward use-site inventory (CP0(a)/CP0(c)) and a C2-non-use sentence and states the partial-binding-by-restriction point once; both the two-premise identification and the C2-loss open question are already in the ASN, so nothing external is at issue.

## Issue 2: Duplicated domain-closure rationale (CP3c and CP6)
Reason: Editorial deduplication — keep the closure-principle justification at CP3c and let CP6's "non-text instance of CP3c's closure principle" back-reference stand alone. The justification is already present and uncontested; no design intent or implementation evidence is needed.

## Issue 3: Two forward-deferrals to the tiling argument
Reason: Editorial — collapse two forward pointers into one (CP3c carries it, the CP3 displacement gloss drops it). The tiling argument itself is internal and unchanged; no channel needed.

## Issue 4: Open Question 2 is already answered by CP0
Reason: Internal — CP0 totally orders the resolved sequence (spec-set order, then ascending V-start per C1b) and CP2 binds `p+i ↦ cᵢ` in that order, fixing placement order; the dedup/normalization reading the reviewer flags is settled by the ASN's own CP4/M14/S5 (permanently independent occurrences, no merging). Both readings resolve from the ASN's own content.
