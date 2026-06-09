# Channel Assignment — ASN-0116 review-10

**Date:** 2026-06-08 21:24

## Issue 1: LP9 is cited for a transition that does not satisfy its preconditions
Reason: Internal. The ASN already derives `ran(M'(d)) = ran(M(d)) ∪ A_new` directly from I-LEFT/I-SHIFT/I-NEW, and the review supplies LP9's stated preconditions (E2, K.μ⁺/K.μ⁺_L) showing they fail; dropping or annotating the citation needs no design intent or implementation evidence.

## Issue 2: LP3 (single-step) cited where the composite needs LP3★
Reason: Internal. INSERT is defined in-ASN as an `n+1`-step composite, and the correct multi-step lemma LP3★ is named by the review; swapping the citation is a foundation-lemma granularity fix requiring neither Nelson nor Gregory.

## Issue 3: S8★ (per-subspace run decomposition) not addressed for the post-state
Reason: Internal. The post-state's S8★ existence-and-uniqueness follows from S8 (ASN-0036) plus I3-fin, both already in the ASN's foundation set; adding the sentence is derivable from the ASN's own content.
