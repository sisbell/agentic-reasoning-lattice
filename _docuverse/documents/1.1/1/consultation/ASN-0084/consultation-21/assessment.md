# Channel Assignment — ASN-0084 review-21

**Date:** 2026-05-15 09:54

## Issue 1: Imprecise citation of OrdinalShift's domain
Reason: Fix is internal — the ASN already establishes its own identity convention (`c₀ + 0 = c₀`) and cites ASN-0034's OrdinalShift. The repair is to split the citation so that j ≥ 1 falls under ASN-0034's contract and j = 0 falls under the ASN's identity convention, with the same care applied at every boundary-offset TS3 invocation.

## Issue 2: Subspace confinement omits the OrdShiftHom (b) citation
Reason: Fix is internal — OrdShiftHom (b) is an exported property of ASN-0036 that the ASN may cite directly. The repair is to replace the S8a citation with OrdShiftHom (b) as the load-bearing fact for subspace preservation under ordinal shift; CS3 remains the source of the cuts' subspace.

## Issue 3: R-PRE omits w_μ ≥ 1 for the 4-cut case
Reason: Fix is internal — the derivation (CS2 + R-PRE(iv)) is already present inline in R-SWP. The repair is a structural choice (add a clause or hoist to Consequences of R-PRE) that the author can make without external input.

## Issue 4: Compressed bounds in canonical decomposition step (b)
Reason: Fix is internal — the missing inequality chain (`p ≤ k₂ < n₂`, `ord(v₁) − 1 ≥ 1`) is derivable from the ASN's own setup. The repair is to expand the proof, with no design-intent or implementation-evidence question.

## Issue 5: Signed-magnitude carrier arithmetic undefined
Reason: Fix is internal — the review identifies that the main lemmas (R-DISP, R-PPERM, R-SPERM) do not depend on the carrier arithmetic. The repair is the lighter option of demoting the closing-paragraph discussion to informal commentary.

## Issue 6: R-BLK Phase 1 "later cut in right-hand piece" claim not derived
Reason: Fix is internal — the inequality chain (`ord(c_j) > ord(c_i) = ord(v_k) + c`) uses only CS2 and the offset computation already present in Phase 1. The repair is proof expansion.

## Issue 7: R-RI labeled LEMMA but presented inline
Reason: Fix is internal — the derivation is already correct and present in prose; the repair is structural (lift to a labeled lemma header parallel to R-PIV, R-SWP, etc.).

## Issue 8: Identification paragraph's NAT-sub claim incomplete at j = 0
Reason: Fix is internal — the ASN's own identity convention covers j = 0, and ASN-0034's NAT-sub contract is already cited. The repair is to clarify that the correspondence is with the shift-or-identity composition (OrdinalShift for j ≥ 1, identity for j = 0).
