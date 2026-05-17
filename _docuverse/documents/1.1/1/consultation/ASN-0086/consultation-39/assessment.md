# Channel Assignment — ASN-0086 review-39

**Date:** 2026-05-17 16:02

## Issue 1: Class (iii) Frame condition leaves value-preservation at existing keys implicit, undermining R7a's "Frame-alone" derivation
Reason: The fix is a choice between two presentations internal to ASN-0086 — either tighten the Frame's class-(iii) clause to include explicit value-preservation at existing keys (e.g., `Σ'.L = Σ.L ⊕ {a ↦ (F, G, K)}`), or acknowledge L12 as load-bearing for R7a's Case (a) and revise the "consistency consequence" framing. Both options are derivable from material already present in the ASN (the Frame definitions, R7a's proof, and the L12/L12a citations); no design-intent or implementation evidence is required to choose between them.
