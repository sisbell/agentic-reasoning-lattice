# Channel Assignment — ASN-0123 review-54

**Date:** 2026-06-13 23:48

## Issue 1: V9w's witness claim is vacuous for content-empty cross-owner forks, and the consequence is never derived
Reason: Internal. The fix is a logical derivation over clauses the note already states — `A = ∅ ⟺ n = 0` (from the Abbreviations), the contract's admission of `n = 0` (scope note + V-WF), V9(a) severance, V13's empty delta, and V9w's vacuity. Scoping the claim to `A ≠ ∅` and recording the degenerate consequence (no state-level witness, only the off-state `derives` event under VD) requires no design intent and no implementation evidence; every premise is present in the ASN.

## Issue 2: V11(a) states immediacy twice — abstractly, then by re-enumeration
Reason: Internal. Pure anti-bloat prose surgery — dropping the redundant K.μ⁺/K.μ⁻/K.μ~ enumeration while keeping the abstract immediacy statement and the load-bearing "no allocation, registration, or unlock owed" point. No external facts are involved.
