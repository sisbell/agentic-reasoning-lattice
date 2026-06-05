# Channel Assignment — ASN-0109 review-1

**Date:** 2026-06-04 19:08

## Issue 1: No concrete worked example
Reason: Constructing a worked instance and checking E1, E3, E4, E5, E7, E9 against concrete endset values is purely an exercise in applying the ASN's own definitions; no design intent or implementation evidence is required.

## Issue 2: E6 invokes single-step immutability for the transitive closure without induction
Reason: The induction over `→*` uses foundation claims L12 (value fixity) and L12a (membership persistence) already cited in the model; assembling the base/step argument is internal to the spec.

## Issue 3: `home` is broadened beyond its foundation definition
Reason: The fix is reconciling E7's use of `home`/`participants` with the foundation's T4-validity domain (zeros = 3) and L4 EndsetGenerality — both already present; restricting the projection domain or proving totality is derivable from existing definitions.

## Issue 4: Weakest-precondition analysis is only the trivial case
Reason: The non-trivial wp for empty resolution of a non-empty endset follows directly from the `res`/`resolved` definitions stated in the ASN; the computation is internal.

## Issue 5: Operation name inconsistent with title and Nelson's term
Reason: The verbatim Nelson definition (LM 4/70) and term RETRIEVEENDSETS are already quoted; choosing one name and stating READENDSETS is this ASN's name for Nelson's operation is editorial and derivable from content present.

## Issue 6: E8 asserts properties of traversal, which is undefined and out of scope
Reason: The fix is to drop the comparative negative claims or relocate them to non-normative prose, retaining the positive read-establishes content (E2/E3/E5); this is an internal scoping decision needing no external channel.
