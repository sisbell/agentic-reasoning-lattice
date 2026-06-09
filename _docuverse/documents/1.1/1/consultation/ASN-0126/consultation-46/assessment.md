# Channel Assignment — ASN-0126 review-46

**Date:** 2026-06-09 11:28

## Issue 1: R's registration status is asserted in one section and re-opened in another
Reason: The internal contradiction is plain, but choosing the resolution — make R a framework axiom in `Σ_init.registry` versus leave it app-declared — turns on whether retraction was designed as a substrate-universal primitive. ASN-0086 puts Nullify in the core vocabulary, which hints internally, but the intent question is Nelson's.
Nelson question: Was retraction (Nullify/R) intended to be a substrate-shipped primitive that every framework-governed substrate guarantees, or an app-level type each app must register for itself?

## Issue 2: P6's induction step names L12 but needs P1/P4 to carry the hypothesis
Reason: The fix is fully derivable from the ASN — P1, P4 (and P2) are already proved in the note, and the required change is simply to name the P1/P4 chain alongside L12 in P6's induction step. No external channel needed.

## Issue 3: Duplicate and defensive meta-prose (anti-bloat)
Reason: Pure editorial deletion of duplicate and defensive sentences identified by line; no design intent or implementation evidence is involved. Internal.
