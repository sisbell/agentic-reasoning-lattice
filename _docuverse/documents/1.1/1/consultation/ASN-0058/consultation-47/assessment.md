# Channel Assignment — ASN-0058 review-47

**Date:** 2026-05-30 07:49

## Issue 1: Nonexistent foundation citation in C0
Reason: The review already names the correct foundation axioms (NAT-closure + NAT-addcompat); this is a mechanical citation correction internal to the ASN and its foundation, needing no design intent or implementation evidence.

## Issue 2: Undefined `subspace_I` and missing foundation `ShiftPreservation`
Reason: The fix is to define `subspace_I` and supply the I-side shift-invariance argument inline — M16a already proves the analogous prefix-preservation result for `origin`, so the same action-point/prefix-copy reasoning is available within this ASN. Internal.

## Issue 3: S7c cited but absent from foundation
Reason: The review identifies that the core conclusion needs only `#E(a) ≥ 1` (available from T4a field non-emptiness), so the fix is recasting the citation using already-present foundation claims. Internal.

## Issue 4: Forward-reference deferral prose in M6
Reason: Pure prose deletion — restate M6 as its four proved properties and let M16b carry origin traceability. Derivable from the ASN's own structure.

## Issue 5: Use-site inventory in M16a
Reason: Pure prose deletion of a downstream-consumer inventory; the precondition stands on its own and is discharged at each call site already. Internal.

## Issue 6: Downstream-dependency and non-circularity justifications in M2
Reason: Pure prose deletion of two meta-justification sentences; the inclusion argument and precondition inheritance remain intact without them. Internal.

## Issue 7: "Why a precondition isn't needed" prose
Reason: Pure prose deletion of defensive justification; clause (b)'s proof depends only on the `a ∈ dom(C)` hypothesis and the I-side shift-invariance lemma. Internal.
