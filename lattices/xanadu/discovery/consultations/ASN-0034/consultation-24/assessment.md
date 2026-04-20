# Revision Categorization — ASN-0034 review-24

**Date:** 2026-03-26 08:48

## Issue 1: TA3 proof — missing case for zero-padded-equal operands
Category: INTERNAL
Reason: The missing case is fillable from existing definitions (TA6, Divergence, TumblerSub). The proof sketch is already provided in the review finding itself — zero-padded equality produces a zero tumbler, positivity of `b ⊖ w` follows from `bⱼ > aⱼ = wⱼ`, and TA6 closes it.

## Issue 2: Circular dependency — TumblerAdd ⟷ TA4
Category: INTERNAL
Reason: TumblerAdd is a constructive definition with no upstream dependencies. The error is a dependency graph annotation mistake correctable from the ASN's own presentation order.

## Issue 3: Circular dependency — Divergence ⟷ TA1-strict
Category: INTERNAL
Reason: Divergence is a pure definition depending only on T1. The spurious entries (TA0, TA1, TA1-strict) are downstream consumers, identifiable as such from the ASN text alone.

## Issue 4: Circular dependency — TA-strict ⟷ T12
Category: INTERNAL
Reason: The ASN's own verification paragraph and property table both confirm TA-strict depends only on TumblerAdd and T1. The fix is removing labels the derivation never references.

## Issue 5: Circular dependency — D0 ⟷ D1
Category: INTERNAL
Reason: The ASN states D0 before D1, and D1's proof explicitly cites D0 as a hypothesis. The reversed dependency is a graph annotation error.

## Issue 6: Spurious dependencies — TumblerSub
Category: INTERNAL
Reason: TumblerSub is a constructive definition; the property table already correctly states "from Divergence, T1." The fix removes labels the definition never uses.

## Issue 7: Spurious dependencies — TS5
Category: INTERNAL
Reason: TS5's two-line derivation in the ASN text references only TS3 and TS4. The property table confirms this. No external evidence needed.

## Issue 8: Spurious dependency — T12 on T5
Category: INTERNAL
Reason: The ASN explicitly distinguishes T12 from T5 ("We reserve T5 for the distinct claim..."). The property table agrees. The fix removes a label the derivation disavows.

## Issue 9: Spurious dependencies — additional corrections
Category: INTERNAL
Reason: Each sub-item (T0(b), T7, T9, PositiveTumbler) has its correct dependencies stated in the ASN prose or property table. The fixes remove labels not referenced in the respective derivations.

## Issue 10: TA1-strict name mismatch
Category: INTERNAL
Reason: The correct name appears in the property table ("Addition preserves the total order (strict)..."). The dependency graph name is a scanning artifact correctable by inspection.
