# Channel Assignment — ASN-0091 review-24

**Date:** 2026-05-26 20:41

## Issue 1: RE-disc proof quantifies over all documents but only handles the target
Reason: Fix is derivable from the ASN alone — split proof into target case (RE-ran) and non-target case (RE-other), both already established in this ASN. No design intent or implementation evidence required.

## Issue 2: RE-trans proof emphasises target d without addressing non-target d
Reason: Fix is internal — the non-target case follows trivially from RE-other (already proved in this ASN), and the target case from RE-ran/RE-μ. Pure proof-restructuring.

## Issue 3: Range equality for non-target documents is never stated as a lemma
Reason: Fix is derivable from the ASN alone — either generalize RE-ran's statement with a two-line case-split proof (target by π-bijection, non-target by RE-other) or add a uniform-range lemma. All premises already present.
