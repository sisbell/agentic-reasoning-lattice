# Channel Assignment — ASN-0108 review-10

**Date:** 2026-06-05 05:04

## Issue 1: Direction of the "stronger than" relation between frozen-prefix and membership-identity is reversed
Reason: The fix is derivable from the ASN alone — the worked example (a frozen-prefix model violating membership-identity) and the nesting line "membership-identity ⊃ frozen-prefix ⊃ genuine weakest" already establish the correct direction, so only the introductory sentence's wording must be reversed. No design intent or implementation evidence is at stake.
