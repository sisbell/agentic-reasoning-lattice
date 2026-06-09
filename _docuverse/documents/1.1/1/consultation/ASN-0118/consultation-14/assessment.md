# Channel Assignment — ASN-0118 review-14

**Date:** 2026-06-09 00:20

## Issue 1: Non-text subspace domain is underdetermined by the postconditions
Reason: Internal. The ASN already exhibits the composite (step (i)'s K.μ⁻ retains `s_L` in full, step (ii)'s K.μ⁺ adds only `s_C` positions), which establishes that no non-text positions are added or removed; the fix merely lifts that already-proven fact into an explicit CP3c-style domain-closure postcondition. No design intent or implementation evidence is required — the closure is derivable from the operation's own decomposition.
