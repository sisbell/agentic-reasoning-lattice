# Channel Assignment — ASN-0094 review-78

**Date:** 2026-05-25 16:33

## Issue 1: FDD preservation Case A enumeration is incomplete
Reason: Internal fix. Sh4's Case A enumeration already exhibits the correct structure (item 3 covers the K.λ at K' ~ R no-intersection sub-case); FDD's enumeration should either mirror Sh4 or drop to the case-equation alone. No design intent or implementation evidence needed.

## Issue 2: d_retr unspecified in worked example edge case
Reason: Internal fix. The Nullify precondition P0 (already cited from ASN-0086) requires only d_retr ∈ dom(Σ_5.M); the walkthrough's existing setup conventions (home_K, home_R) provide the template for either pre-allocating d_retr or noting that any document container suffices. No design intent or implementation evidence needed.
