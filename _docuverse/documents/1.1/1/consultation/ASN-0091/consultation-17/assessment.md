# Channel Assignment — ASN-0091 review-17

**Date:** 2026-05-26 18:54

## Issue 1: "by π's injectivity" in S2 derivation requires bijectivity, not injectivity
Reason: Pure logical correction — the existence half requires surjectivity and `π⁻¹` requires bijectivity, both of which RA-π already supplies. Fix is a one-phrase substitution internal to the ASN.

## Issue 2: "The set is preserved (RE-proj)" in Run Decomposition section is imprecise
Reason: Wording precision against RE-proj as already stated. The accurate characterisation (cardinality and underlying I-addresses, not literal V-positions) is fully derivable from RA-π and the existing RE-proj statement.

## Issue 3: P4a transition-history derivation repeated verbatim in three places
Reason: Refactoring/DRY cleanup. The derivation already lives in the main text; the worked examples just need to cite it. No design-intent or implementation evidence in play.

## Issue 4: Foundation invariants S8a, S8-fin, S8-depth not enumerated in the "trivially preserved" list
Reason: Enumeration gap. The discharge mechanism (RA-dom plus state-independence of `subspace`, `#v`, `zeros`) is fully derivable from the ASN's own premises; ASN-0084's R-SP provides the alternative pointer. Internal.

## Issue 5: Claim table omits the ★ (multi-step composed) forms
Reason: Documentation completeness. The ★ forms and their restrictions are already derived in the composition section; promoting them into the table is a structural edit with no external dependency.
