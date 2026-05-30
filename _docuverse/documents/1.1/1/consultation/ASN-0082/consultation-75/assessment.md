# Channel Assignment — ASN-0082 review-75

**Date:** 2026-05-30 14:12

## Issue 1: Use-site inventory in OrdinalExceedsDisplacement
Reason: Purely editorial — the fix removes a consumer enumeration and structural-rationale sentence while keeping the `v = r` result-length justification, all derivable from the ASN's own text. No design intent or implementation evidence bears on whether redundant prose is cut.

## Issue 2: D-SEP(a) restates the upstream proof rather than citing it
Reason: Internal citation hygiene — the identity already lives in OrdinalExceedsDisplacement (i) within this ASN; reducing the parenthetical to a direct citation needs only the ASN's own cross-reference structure.

## Issue 3: Redundant re-derivation inside D-BJ proof of (a)
Reason: Internal collapse — OrdinalExceedsDisplacement (ii) already supplies `ord(v) ≥ w_ord`; removing the depth-2 restatement and embedded ∎ tag is fully determined by the ASN's existing lemma chain.
