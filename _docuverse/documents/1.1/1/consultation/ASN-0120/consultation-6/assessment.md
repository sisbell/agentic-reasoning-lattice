# Channel Assignment — ASN-0120 review-6

**Date:** 2026-06-09 00:52

## Issue 1: `subspace_I` asserted where it is undefined
Reason: Internal fix. The correction re-routes the conclusion through store membership using ML2 and the link-inheritance fact `E(ℓ)₁ = E(aₖ)₁ = s_C ≠ s_L`, both already established in the ASN and its foundation citations (ASN-0043/0093). No design intent or implementation evidence is at issue — only the misuse of a partial function.

## Issue 2: K.μ⁺_L preconditions not discharged
Reason: Internal fix. Discharging `a ∈ dom(L)`, `origin(a) = d`, `a ∉ ran(M(d))`, and the well-formed V-position uses ML0, freshness, S3★/CL-OWN, and K.μ⁺_L's own `ValidFirstLinkPosition` clause — all substrate facts already cited in the ASN. The review itself supplies the one-line discharge.

## Issue 3: Open Question 3 is already answered by the ASN
Reason: Internal fix. ML0 freshness plus SubsequentEmissionFreshness (ASN-0093) and the R2 consequence (ASN-0086) already close the question; converting it to a stated consequence draws only on claims the ASN already cites. No external channel needed.
