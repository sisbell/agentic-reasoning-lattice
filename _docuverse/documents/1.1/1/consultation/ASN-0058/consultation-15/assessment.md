# Channel Assignment — ASN-0058 review-15

**Date:** 2026-05-13 18:35

## Issue 1: M5(b) disjointness skips an injectivity step
Reason: Fix is internal — cite M0's injectivity argument (or directly TS4/TS5 from ASN-0034) already present in this ASN.

## Issue 2: M12 "immediate successor in the linear order" is false as stated
Reason: Fix is internal — replace the universal claim with the depth-m restricted statement, justified by T1 (ASN-0034) and S8-depth (ASN-0036), both already in scope.

## Issue 3: M12 condition 3 sub-case omits depth justification for v'
Reason: Fix is internal — the OrdShiftHom + S8-depth chain (both ASN-0036, already cited elsewhere in M12) supplies #v' = m without external input.

## Issue 4: M12 condition 2 sub-case skips the "v' is the last position" derivation
Reason: Fix is internal — the missing step uses M-aux (this ASN) and B2 disjointness (this ASN); no external evidence or design intent required.

## Issue 5: M7 overlap case omits the prefix-agreement step for v₂
Reason: Fix is internal — the case-elimination uses T1(i) and TumblerAdd prefix-preservation from ASN-0034, already invoked elsewhere in this passage.

## Issue 6: M13 (SharedContent) lacks a derivation
Reason: Fix is internal — the reviewer's two options (concrete witness via the block algebra; explicit S5 instantiation at N=1) are both derivable from definitions already in this ASN and ASN-0036.

## Issue 7: M7 overlap case — V_{v₁}(d) notation conflates membership and label
Reason: Fix is internal — rephrasing uses the existing distinction between `subspace(·)` (OrdShiftHom) and the set `V_s(d)` (S8-depth), both from ASN-0036.
