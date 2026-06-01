# Channel Assignment — ASN-0086 review-193

**Date:** 2026-06-01 13:47

## Issue 1: "Unit-depth retraction discipline" states a false equivalence — the ASN's own Worked Sketch is a counterexample
Reason: Internal fix. The counterexample is the ASN's own Worked Sketch Step 4, and the correction (demote "equivalently" to one-directional, or pin characterization (1) to the producing call's pre-state) is a purely logical edit derivable from the document's existing content.

## Issue 2: K-Step Conformance Preservation discharges clauses (b)/(c) only for K.λ
Reason: Internal fix. That K.σ/K.α emit zero link keys (and hence satisfy the link-key clauses (b)/(c) vacuously) is already established by the ASN's own State transition relation and ASN-0093 frame conditions; only the proof's case-split prose needs completing.

## Issue 3: Forward-reference / meta-prose accretion (anti-bloat classifier)
Reason: Internal fix. This is a de-duplication edit — collapse the re-narrated NestedLinkWitness construction to a single site and bare citations elsewhere — requiring no design intent or implementation evidence.
