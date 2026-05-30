# Channel Assignment — ASN-0084 review-49

**Date:** 2026-05-30 10:57

## Issue 1: Foundation property S8 renamed "SpanDecomposition"
Reason: This is a notation-alignment problem against the foundation ASN-0036, which the author can consult directly. Neither design intent (Nelson) nor implementation evidence (Gregory) bears on what name and clause-lettering ASN-0036 uses; the fix is to match the foundation's own labels.

## Issue 2: Citations to ASN-0036 properties not present in the foundation
Reason: Whether ASN-0036 exports "ShiftPreservation," an "S8 corollary," and "OrdinalExtraction" is verifiable against the foundation spec, and the field-preservation step (subspace_I, zeros, #E under shift) is derivable from the ASN-0034 tumbler/shift axioms already cited. The fix is internal cross-reference correction plus a local proof.

## Issue 3: Meta-prose justifying proof ordering and reading conventions
Reason: Pure editorial deletion of non-circularity narration and reader instructions; the lemma's dependencies are already recorded in its Depends-on clause. No external channel involved.

## Issue 4: The same invariant-transport argument is repeated three times
Reason: Consolidating the C'=C transport and S5/multiplicity argument into one cited location is an internal de-duplication; the arguments themselves are already proven in the ASN.

## Issue 5: Use-site inventories and "we do not repeat" forward-management prose
Reason: Trimming the consumer roster and repetition-management sentence down to the single substantive identity-convention fact is editorial; the fact and its proof are already present in the ASN.
