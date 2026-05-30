# Channel Assignment — ASN-0042 review-106

**Date:** 2026-05-30 03:36

## Issue 1: O17b labels delegation as registry-frame, contradicting O18 and the ASN's own worked example
Reason: Fully internal. O18, DelegatorAllocatesPrefix, condition (v) next-reachability, and the Worked Example ("`[1, 0, 2]`... is baptized at the delegation transition") all already establish that delegation lands in the `next(Σ.B, p, d)` branch; the fix is removing the contradictory parenthetical to align with content already present.

## Issue 2: `delegated_Σ*` is defined as the closure of `R_Σ`, not of `delegated_Σ`
Reason: Fully internal. The ASN already supplies the needed facts — condition (iv) plus O13 imply a newcomer's actual delegator is its most-specific cover at every later state — so either proving `delegated_Σ* = (delegated_Σ)*` or renaming the `R_Σ`-closure is a self-contained formal task requiring no design intent or implementation evidence.

## Issue 3: O17b carries use-site-inventory and implementation prose in an axiom slot
Reason: Fully internal. The fix is editorial — state the axiom as the two-branch disjunction, drop the op-by-op inventory, and compress the existing Gregory paragraph to a one-line provenance pointer; no new evidence or design intent is needed since the abstract coupling is already stated.
