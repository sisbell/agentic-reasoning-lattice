# Channel Assignment — ASN-0036 review-72

**Date:** 2026-05-10 23:02

## Issue 1: T4 cited as "FieldSeparatorConstraint" — foundation canonical name is "HierarchicalParsing"
Reason: This is a citation rename derivable from the foundation ASN-0034's canonical Name for T4. No design intent or implementation evidence needed — the fix is a mechanical substitution at every cite site.

## Issue 2: S8 proof uses inc(v, 0) for "v + 1" but the ASN defines v + 1 = shift(v, 1)
Reason: This is an internal proof-consistency issue. The ASN already defines `v + k = shift(v, k)` and the equivalence with `inc` (or the direct shift-only argument via TumblerAdd's postconditions) is derivable from ASN-0034's TA5 and TumblerAdd contracts already cited in the proof.

## Issue 3: S8 proof Case j = m uses t_m ≥ v_m where T1(i) delivers t_m > v_m
Reason: This is a proof-tightening fix derivable from T1(i) (TumblerOrdering, ASN-0034) which is already cited. The strict inequality follows directly from `v < t` (since `t ≠ v` and `v ≤ t`).

## Issue 4: "Treats j generically for any 1 ≤ j ≤ m" overstates the j range
Reason: Editorial correction of a range bound to match the shared-subspace reduction established two sentences earlier within the same proof. Purely internal.
