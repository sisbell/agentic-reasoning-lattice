# Channel Assignment — ASN-0100 review-83

**Date:** 2026-06-05 05:37

## Issue 1: Opening atomicity promise overstated against the note's own result
Reason: Internal — the Atomicity section already establishes the precise distinction (Class (a) per-state invariants hold at every intermediate; P4★/P4a/P7a hold only at the boundary). The fix merely realigns the opening framing with the body's own verified result; no design intent or implementation evidence is needed.

## Issue 2: Garbled, redundant phrasing in the K.μ⁻-before-K.μ⁺ forced-ordering argument
Reason: Internal — (INS.μ⁻-fires) already establishes that `Right ≠ ∅` iff `p ∈ dom(M(d))` (i.e. `p_m ≤ N`), and the spurious `j = 0`/interior split names the same tumbler twice. Collapsing to the single uniform statement is derivable entirely from the ASN's own content.

## Issue 3: Re-insertion sub-case re-derives a V-side checklist it simultaneously declares insensitive
Reason: Internal — this is a compression of redundant exposition the paragraph itself declares insensitive; the V-side discharges identically to the first-insertion example already in the note, and the distinct I-side content (K.α subsequent-emission branch, chain continuation past `a_prev`) is retained as-is. No channel input required.
