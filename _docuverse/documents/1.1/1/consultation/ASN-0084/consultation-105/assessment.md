# Channel Assignment — ASN-0084 review-105

**Date:** 2026-05-30 21:18

## Issue 1: Cut ordinals are used as positive naturals, but CS1–CS4 permit a zero second component
Reason: Internal fix. The ASN already supplies everything needed: S8a (ASN-0036) makes V-positions zero-free, R-PRE(iv) forces c₀…c_{n−2} into V_S(d), and the last cut c_{n−1} is handled by EXT-VAC — so cut positivity is derivable from the ASN's own definitions and the singleton-tumbler identification it already establishes. No design intent or implementation evidence is required to add the positivity clause or derive it.

## Issue 2: "Subspace confinement" in Consequences of R-PRE restates SUBCONF (anti-bloat)
Reason: Internal editorial fix. This is purely a prose-compression decision (delete or inline the SUBCONF instantiation); it requires no design intent or implementation evidence, only the ASN's own SUBCONF and CS4.
