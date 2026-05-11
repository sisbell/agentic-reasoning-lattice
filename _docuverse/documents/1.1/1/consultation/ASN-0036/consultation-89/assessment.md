# Channel Assignment — ASN-0036 review-89

**Date:** 2026-05-11 03:51

## Issue 1: OrdShiftHom lacks a dedicated concrete example
Reason: Adding a worked instance is mechanical — the values and computations follow directly from existing definitions of `shift`, `ord`, OrdAddHom, and OrdShiftHom in this ASN. No external input needed.

## Issue 2: ord and vpos definitions lack worked instances
Reason: The inverse properties to be exhibited are pure sequence manipulations whose worked instances follow directly from the definitions of `ord`, `vpos`, and `subspace` in this ASN. No external input needed.

## Issue 3: S8 existence proof's invocation of S7c is misplaced
Reason: Editorial restructuring within the proof body to align with the existing formal contract. The contract is already correct; the body just needs to match. No external input needed.

## Issue 4: S8 never exhibits a non-singleton decomposition
Reason: The "hello" worked example already asserts a single run of length 5; exhibiting conjunct (b) at `k = 1, 2` and the auxiliary lemma's subspace preservation is mechanical tumbler arithmetic from TumblerAdd and OrdinalShift in ASN-0034. No external input needed.

## Issue 5: The "Auxiliary lemma" claim about subspace_I position lacks explicit verification of field-structure preservation
Reason: The gap is filled by TumblerAdd's three-region formula in ASN-0034, which is already cited in the lemma. Adding the explicit separator-preservation step is internal to the proof. No external input needed.

## Issue 6: ValidInsertionPosition's ternary signature is awkward and underspecified for the empty case
Reason: The strand-model commitment ("not fixed by the strand model... m ≥ 2") is already stated in prose; the fix is either splitting the predicate or hoisting that commitment into the formal contract. Both options are editorial choices derivable from existing ASN content. No external input needed.
