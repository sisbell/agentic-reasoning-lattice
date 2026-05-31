# Channel Assignment — ASN-0043 review-133

**Date:** 2026-05-30 20:50

## Issue 1: L11b's non-injectivity witness writes the carried payload as a fixed triple, contradicting the arity-≥3 generality it quantifies over
Reason: Internal fix — the correction is purely notational, replacing `(F, G, Θ)` with the generic `N`-tuple `Σ.L(a)` to match L11b's own quantifier and L3's arity admission, all already present in the ASN.

## Issue 2: L11a closes with a defensive justification of what is *not* needed
Reason: Internal fix — deleting the redundant sentence requires no design intent or implementation evidence; the argument already closes at the GlobalUniqueness step within the ASN.
