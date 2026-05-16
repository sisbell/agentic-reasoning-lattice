# Revision Categorization — ASN-0063 review-2

**Date:** 2026-03-21 18:27

## Issue 1: P4 (ProvenanceBounds) violated — omitted from CL11
Category: INTERNAL
Reason: The ASN already identifies and resolves the structurally identical J1/P7 conflict by introducing J1★. The same content-subspace scoping pattern applies mechanically to P4 and Contains.

## Issue 2: S3 supersession not stated
Category: INTERNAL
Reason: S3★ is already defined in the ASN and its relationship to S3 is implicit. The fix is adding explicit supersession statements — all necessary definitions and reasoning are present.

## Issue 3: CL0 proof uses undefined shift(a_β, 0)
Category: INTERNAL
Reason: The M-aux convention (v + 0 = v) from ASN-0058 and the OrdinalShift definition from ASN-0034 provide everything needed to handle the c=0 case. Notational fix only.

## Issue 4: CL0 statement conflates image with span denotation
Category: INTERNAL
Reason: The ASN itself notes the containment is strict three paragraphs after CL0. The fix is restating CL0 to say "representable by" rather than "is" — a precision correction derivable from existing content.

## Issue 5: K.μ⁺_L freshness of v_ℓ unstated
Category: INTERNAL
Reason: The review itself notes the freshness property IS derivable from the existing preconditions via TS4 and T7. The fix is making the implicit derivation explicit.

## Issue 6: Direct I-span endset path not formalized
Category: INTERNAL
Reason: The ASN already describes the direct I-span path in prose ("endsets are taken as-is") and states that L3/L4 place no requirement on endset I-addresses being currently arranged. The fix is extending resolve with a trivial identity clause to match the existing prose.
