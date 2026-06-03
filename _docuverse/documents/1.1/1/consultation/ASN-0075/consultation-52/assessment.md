# Channel Assignment — ASN-0075 review-52

**Date:** 2026-06-03 09:05

## Issue 1: Version-fork shorthand carries reviser-drift and a forward reference into the proof
Reason: Pure editorial trim. The load-bearing fact `d' = inc(d, 1)` (K.δ case (ii), `k = 1`, needing only `d ∈ E_doc`) is already present in the ASN; the fix removes the re-mint refutation and the forward pointer. No external input needed.

## Issue 2: The "Supplementary lemma (R-disjointness implies Q0)" is untracked and scatters the emptiness analysis
Reason: Internal reorganization. The lemma is fully proved within the ASN; both options (promote to a tracked claim or fold into the `wp(Q0)` derivation) only move and label existing content. No design intent or implementation evidence is required.

## Issue 3: Defensive axiom-non-use commentary in D-NEED
Reason: Pure editorial trim. The substantive content — that R-membership distinguishes DELETED from NEVER_INCLUDED definitionally, hence at any reachable state — is already complete in the preceding sentence; only the "does not invoke P4★" narration is dropped.
