# Channel Assignment — ASN-0134 review-25

**Date:** 2026-06-14 04:28

## Issue 1: V2's "no `Q`-affecting step" condition is unsound for `stale` verdicts, because §8 defines `Q`-affecting only over `Observe_{K_i}` constituents
Reason: The fix is a definitional generalization internal to the note — broadening §8's realization formula and `Q`-affecting definition from per-type `Observe_{K_i}` constituents to all bounded-access constituents (the active-view read *and* each frontier descent). Every fact the repair and its witness need is already established in the ASN: A1 fixes `stale`'s realization as `g'(Observe_K(oper), f_{d₁}, …, f_{d_N})`, and A1/BH4 already state that a home's link frontier `f_d` interleaves every type homed at `d` (so a `K′ ≠ K` emit advances `f_d` while leaving the type-scoped `A_K` untouched); the banking argument is present in §8 and transfers verbatim over the widened constituent space, so no design-intent (Nelson) or implementation evidence (Gregory) is required.
