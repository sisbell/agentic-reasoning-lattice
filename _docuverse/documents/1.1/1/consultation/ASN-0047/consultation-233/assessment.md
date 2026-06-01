# Channel Assignment — ASN-0047 review-233

**Date:** 2026-06-01 10:23

## Issue 1: "Replacement rides the K.μ⁻ + K.μ⁺ skeleton of K.μ~" conflates two distinct composites
Reason: Internal fix. K.μ~'s own bijection equation forces range preservation (`ran(M'(d)) = ran(M(d))`), while the replacement worked examples already in this ASN change `ran(M(d)|_{s_C})` — the contradiction and its resolution are both fully present in the ASN's own definitions, so the rewrite (replacement is a separate range-changing K.μ⁻ + K.μ⁺ composite) needs no external channel.

## Issue 2: Dangling cross-reference for `max`-well-definedness in K.α / K.λ subsequent emission
Reason: Internal fix. The required discharge (nonempty by the subsequent-emission predicate, finite by C-fin/L-fin, totally ordered by T1) is assembled entirely from properties stated within this ASN; only the placement/wording of the cross-reference needs correcting.

## Issue 3: Forward-reference accretion — repeated deferrals to "V-position depth (operational)"
Reason: Internal/editorial fix. Consolidating three deferrals into one definition site plus bare name-references is purely a structural rewrite over existing ASN content; no design-intent or implementation evidence is at stake.
