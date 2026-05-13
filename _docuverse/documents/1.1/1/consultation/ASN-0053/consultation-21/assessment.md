# Channel Assignment — ASN-0053 review-21

**Date:** 2026-05-13 14:15

## Issue 1: S5 action-point computation is asserted but not fully proven
Reason: Internal proof completion. The fix requires explicit zero-below-min verification in each case using TumblerAdd's defined behavior (already cited from ASN-0034). No design intent or implementation evidence needed.

## Issue 2: S11c Case 2 has no worked example
Reason: Internal construction. The proof gives the construction γ' = (reach(β), reach(α) ⊖ reach(β)); a worked example just instantiates it with concrete tumblers and verifies via D1. Derivable from the ASN alone.

## Issue 3: "Mutually level-compatible" is used in claim conditions but never defined
Reason: Internal definition addition. S6 already defines level_compat between two tumblers; extending to collections is a straightforward predicate over pairs. No external channels needed.

## Issue 4: S6 phrasing "for all endpoint pairs" suggests multiple pairs per span
Reason: Internal rephrasing. The reviewer supplies the corrected wording, which follows directly from D0's stated preconditions and TA-strict in ASN-0034. Derivable from the ASN.

## Issue 5: Interior-point definition's S0 citation is gratuitous
Reason: Internal citation fix. Membership follows directly from the definition of ⟦σ⟧ given earlier in the ASN. No external channels needed.

## Issue 6: S5 proof of part (a) under-specifies the k_d = k_{d'} case
Reason: Internal citation. The reviewer names the relevant foundation facts (NAT-zero, NAT-addbound) which live in the NAT/arithmetic foundation already underpinning ASN-0034. Fix is to cite them.
