# Channel Assignment — ASN-0108 review-25

**Date:** 2026-06-13 01:06

## Issue 1: W5's iff is not tight — clause 1 permits resurrection re-delivery
Reason: Internal. The defect is a scoping mismatch within the note's own logic — clause 1's "for every `a` matching in both states" cannot constrain re-entry after an orphan gap, and the note already states the resurrection-re-delivery outcome abstractly in W9b and the address-key resurrection-at-permanent-low-key behavior. The fix (re-scope the re-delivery half to match the skip half, or restrict the iff to the address-key class) is derivable from claims already present.

## Issue 2: W8/W9 ground cursor-key survival in T8, contradicting W5's own (regrounded) orthogonality finding
Reason: Internal. W5 already establishes the regrounding — that `κ`'s value-freezing is definitional and T8/GlobalUniqueness are orthogonal — and the fix is only to carry that same attribution into W8/W9 and rescope the T8 citation to its actual role. No design intent or implementation fact is in question; the reasoning is fully present in the note.

## Issue 3: W9's "single cursor's cut-point is all W9 needs" is neither necessary nor sufficient for what W9 asserts
Reason: Internal. The note already contains every notion the fix needs — computability of `κ(c)` (the W8 counterexample), clause 1 at every cursor (W9b's condition (i)), and the W5 cut-point walk — so splitting the conflated proviso into the cardinality fact (under computability) and the everything-delivered guarantee (under clause 1 at every cursor) is pure internal disentangling.
