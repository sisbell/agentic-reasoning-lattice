# Channel Assignment — ASN-0069 review-12

**Date:** 2026-05-25 16:20

## Issue 1: V0 Effects citation for "undefined elsewhere" cites the wrong claim
Reason: V4b already exists in the ASN and establishes `dom(M'(d_new)) = V_{s_C}(d_src)` exactly. The fix is purely a citation correction — swap/augment the V6 citation with V4b as the primary justification.

## Issue 2: V0 Effects citation for R' cites V9 alone, which gives only inclusion
Reason: The K.δ, K.μ⁺, and K.ρ frame conditions are all defined in ASN-0047 (already cited throughout the ASN), and the bound on the n K.ρ steps is verified in the ASN's own composite-verification walkthrough. Fix is internal to citation/proof expansion.

## Issue 3: V8a cites P0/S0 but the operative axiom is K.α's arrangement-preservation frame
Reason: K.α's frame condition `(A d :: M'(d) = M(d))` is part of the ASN-0047 foundation already invoked elsewhere in this ASN (e.g., for K.μ⁺/K.μ⁻/K.μ~ frames). The fix is a mechanical citation swap to the correct frame axiom.

## Issue 4: Notation convention for multiple forks introduced after first use
Reason: Editorial repositioning — the remark already exists in the ASN; it just needs to move earlier (before V10 or at the top of "Independence Among Forks"). No external knowledge required.

## Issue 5: V4 prose precondition is redundant with vacuity
Reason: The decision is a framing choice fully resolvable from the ASN's own structure — V7 already normatively admits empty-source forks, and the universal in V4 is vacuously true in that case, so unifying via vacuity is internally consistent. No external evidence needed.
