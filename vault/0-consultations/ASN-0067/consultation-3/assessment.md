# Revision Categorization — ASN-0067 review-3

**Date:** 2026-03-21 16:50

## Issue 1: Variable name collision — "m" used for both V-position depth and content reference count
Category: INTERNAL
Reason: This is a notation inconsistency within the ASN. The fix is a variable rename — no external evidence about design intent or implementation behavior is needed.

## Issue 2: Wrong citation for S8a preservation in C3
Category: INTERNAL
Reason: The reviewer already identifies the correct justification (OrdinalShift definition from ASN-0034). The fix is replacing a misattributed citation with the correct one, derivable entirely from existing definitions.

## Issue 3: Elementary decomposition does not handle B_post = ∅
Category: INTERNAL
Reason: The boundary cases and their correct decompositions are derivable from the elementary transition vocabulary (ASN-0047) and block decomposition (ASN-0058). The reviewer has already identified the correct two-step composite for B_post = ∅ and the needed D-CTG clarification.

## Issue 4: "Injectivity" where "functionality" is meant
Category: INTERNAL
Reason: This is a terminology error — S2 defines functionality, not injectivity, and S5 explicitly permits non-injectivity. The fix is a word replacement derivable from existing definitions.

## Issue 5: No concrete worked example
Category: INTERNAL
Reason: All ingredients for the worked example — tumbler arithmetic (ASN-0034), block decomposition (ASN-0058), and the COPY definition itself — are already present in the ASN and its dependencies. No external design intent or implementation evidence is needed.
