# Structural Violation: declaration-label-mismatch

**Claim:** ASN-0036/S8
**File:** S8.md
**Line:** 15

## Detail

declaration of '`succ` is injective and acyclic.** Suppose `succ(u) = succ(u')`. Then `shift(u, 1) = shift(u', 1)`. Since `shift` preserves depth, `#u = #shift(u, 1) = #shift(u', 1) = #u'`; TS2 (ShiftInjectivity, ASN-0034) applied at this common depth gives `u = u'`. So `succ` is injective on its domain — each V-position has at most one lockstep successor and at most one lockstep predecessor. There are no cycles: TS4 (ShiftStrictIncrease, ASN-0034) gives `shift(v, 1) > v`, so each `succ`-step strictly increases under T1; a cycle would yield `v < v`, contradicting T1 irreflexivity' matches neither own label 'S8' nor any existing file's label
