# Channel Assignment — ASN-0069 review-23

**Date:** 2026-05-25 19:20

## Issue 1: V8b's K.μ⁺_L argument elides the load-bearing step
Reason: The fix is purely expository — making explicit the two-step inference (modification locality + value invariance at v ∈ F) from K.μ⁺_L's definition in ASN-0047 and the subspace partition, both already cited in the ASN. No design intent or implementation evidence is needed.

## Issue 2: V8b's case analysis omits K.μ⁻/K.μ⁺/K.μ~ on non-chain documents
Reason: The fix invokes per-target frame conditions for K.μ⁻, K.μ⁺, K.μ~ already defined in ASN-0047. The required reasoning is a mechanical application of those frame conditions to the case d ≠ d_src, d ≠ d_new. Internal fix.

## Issue 3: V2's nested length-induction structure is implicit
Reason: The fix is a structural/expository reorganisation — either lifting a sub-lemma or marking inner vs outer induction. The proof content (TA5(c), TA5(d) on A_v(d_src)'s emission count) is unchanged. Internal fix.

## Issue 4: V11's premise convention at i=1 is unspecified
Reason: The fix is a notational convention clarification — spelling out that "step 0's post-state" at i=1 denotes the chain's initial pre-state Σ. The mathematical content of the premise and proof is unchanged. Internal fix.
