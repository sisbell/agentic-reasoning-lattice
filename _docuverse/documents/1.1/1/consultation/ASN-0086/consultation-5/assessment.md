# Channel Assignment — ASN-0086 review-5

**Date:** 2026-05-16 16:53

## Issue 1: R3 proof conflates K with its representative
Reason: Internal fix. The TypedRelation definition already established membership by coverage-equivalence; the proof simply needs to use `K''` with `coverage(K'') = coverage(K)` and invoke R2 plus that equivalence. No external evidence or design intent is required.

## Issue 2: R6a proof has the parallel imprecision
Reason: Internal fix, parallel to Issue 1. R2 preserves the literal stored value, and the argument only needs `G'` preserved literally; restating the third entry as `R''` with `coverage(R'') = coverage(R)` is a textual correction derivable from the ASN's own definitions.

## Issue 3: R0 Step 4 lumps L14a under "orthogonal" without citing the setup hypothesis
Reason: Internal fix. The required argument chain (Step 2 fixes `subspace_I(a) = s_L`; setup hypothesis pins content to `s_C`; S3 from ASN-0036 makes arrangement values content addresses; therefore `a ∉ ran(Σ.M)`) is fully assembled in the review itself, and all cited invariants are already in the ASN's frame. The fix is to move L14a to its own bullet with this citation.

## Issue 4: Intro count mismatches the table
Reason: Purely editorial framing issue. The intro's six-property count omits R7; the fix is to either add a clause acknowledging R7 as a derived fact about the operations (not a sixth foundational property) or to relabel the framing. No external consultation needed.

## Issue 5: Case A's subspace-sweep wording is loose
Reason: Internal rephrasing. The review correctly identifies that the sweep is over `A_d`'s enumeration index from `d.0.1` to `d.0.s_L`, independent of where `s_C` sits — and proposes the exact replacement wording. The underlying substrate behavior (sibling `inc(·, 0)` advancing the enumeration index, TA5a/TA5c from ASN-0034) is already cited in the surrounding proof.
