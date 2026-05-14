# Channel Assignment — ASN-0043 review-61

**Date:** 2026-05-14 15:25

## Issue 1: subspace_I extension to ghost addresses is not stated
Reason: Definitional scope clarification — extending `subspace_I = E(a)₁` to all T4-valid tumblers with `zeros(a) = 3` and `#E(a) ≥ 1` is internal bookkeeping. T4b's projection domain is already established in ASN-0034; no design intent or implementation evidence required.

## Issue 2: L11b proof uses operational "firing" language for a state-existence claim
Reason: Pure proof-reframing — rewrite the construction as a direct state extension (`Σ'.L = Σ.L ∪ {a' ↦ Σ.L(a)}`) and verify conformance. The witness construction is already present; the fix is presentational, not substantive.

## Issue 3: L9 proof's Case A chain implicitly requires structural-producibility reading of L1c
Reason: Clarifying whether L1c's chain is a structural witness or operational event log is a formalization choice within this ASN. The structural reading is already implicit in how T10a is stated in ASN-0034; promoting it from parenthetical to L1c proper is internal.

## Issue 4: PrefixSpanCoverage inclusion direction glosses the c = x case
Reason: Pure proof fix — split `x ≼ c` into `c = x` (reflexivity) and proper extension (T1(ii)). Both branches discharge from existing ASN-0034 definitions.

## Issue 5: L-fin labeled "across transitions" in worked example
Reason: Pure labeling fix — verify L-fin per-state, L12/L12a per-transition. The distinction is already encoded in the invariants' own statements; only the worked example's presentation needs adjustment.

## Issue 6: L8 (same_type) reflexivity not exercised at the basic worked-example state
Reason: Pure example extension — add `same_type(a, a)` verification using the already-proved PrefixSpanCoverage to compute `coverage({(g, δ(1, 8))}) = {t : g ≼ t}`. All machinery is in the ASN.

## Issue 7: L7 (DirectionalFlexibility) not illustrated in worked example
Reason: Pure example annotation — add an inline note observing that F/G labels are nominal. L7's META content (slot positions carry no structural directional weight) is already established; the fix is just illustrating it concretely.
