# Channel Assignment — ASN-0086 review-206

**Date:** 2026-06-01 15:51

## Issue 1: "Higher-arity addresses are in A_rel but in no L_K" stated four times
Reason: Internal — this is a prose-deduplication fix; the fact (higher-arity links occupy `dom(Σ.L)` but are no `L_K` tuple) is already established by L3/the arity-3 restriction in the ASN, so consolidating its four restatements to the Partition note needs no external channel.

## Issue 2: Codomain choice justified with "for uniformity" meta-prose
Reason: Internal — dropping the "for uniformity" rationale and keeping only the map, image, and "into but not onto" is a pure editing operation derivable from the definition itself; no design-intent or implementation evidence is involved.

## Issue 3: Defensive deferral + scope-disclaimer prose around AdmissibleTypes
Reason: Internal — removing the stacked "(below)" deferrals and the L8-disclaimer parenthetical, letting CoverageEqualityDecidable carry its own decidability claim, is a reorganization of material already present in the ASN; no external channel needed.
