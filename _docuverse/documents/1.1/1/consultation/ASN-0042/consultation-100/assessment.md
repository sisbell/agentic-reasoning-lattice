# Channel Assignment — ASN-0042 review-100

**Date:** 2026-05-30 02:51

## Issue 1: O14 states its bootstrap-registry clause three times
Reason: Pure editorial deduplication — delete the standalone restatement sentence and trim the opening parenthetical, keeping the formula clause. No design intent or implementation evidence is at stake; the identical clause is already present and the fix only removes repetition.

## Issue 2: The `findpreviousisagr` / "single allocation point advancing past delegated slots" corroboration is repeated four times
Reason: The implementation fact is already stated identically in all four locations; consolidating it to O17b and back-referencing elsewhere needs no new evidence. The fix is internal reorganization of content already present and consistent in the ASN.

## Issue 3: The `delegated` predicate references `pfx(π')` for a principal not yet in `Π_Σ` without naming the state
Reason: The clarification — that `pfx(π')` in conditions (i)–(v) denotes `pfx_{Σ'}(π')`, well-defined by O15's membership clause and immutable by O13 — is fully derivable from the ASN's own axioms. The O8 proof already uses this reading; the fix only makes it explicit.

## Issue 4: The node-level fork branch (`zeros(pfx(π)) = 0 → zeros(a') = 1`) is never verified on a concrete address
Reason: The node-level fork construction follows mechanically from O10's own definition and the tumbler algebra (TA5(d), `next`/`hwm`), applied to the already-present principal `π_N`. Adding the concrete instance and Form-A exclusion is a self-contained derivation requiring no design intent or implementation evidence.
