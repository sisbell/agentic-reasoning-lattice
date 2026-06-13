# Channel Assignment — ASN-0108 review-38

**Date:** 2026-06-13 05:37

## Issue 1: The stated import boundary is contradicted by W6a
Reason: Internal fix — the bridge facts W6a relies on (F-V, F-IMG, F-LAMBDA) are already cited in the body and the review itself enumerates them; correcting the false "exactly two... and use nothing more" exhaustiveness claim is a matter of reconciling the import list with what the note already uses, requiring no design intent or implementation evidence.

## Issue 2: W5 states clause-1 sufficiency-not-necessity three times
Reason: Internal fix — the mathematical content (clause 1 sufficient, not necessary; per-cursor failures cancel) is present and correct, proven by the cancellation walk; collapsing the redundant prose restatements is pure anti-bloat compression derivable from the ASN alone.

## Issue 3: The three-key computability breakdown is re-derived in W8, W9, and W9b
Reason: Internal fix — the three-key breakdown (address: value-total; matched-content: endset persistence; position: fails) is already established correctly at W8; replacing the W9/W9b re-derivations with citations and resolving the computability/value-totality definition to one site is a cross-reference cleanup with no new design or implementation question.
