# Channel Assignment — ASN-0108 review-49

**Date:** 2026-06-13 10:23

## Issue 1: κ-section refutes a key that is not a candidate
Reason: Internal. The definition already fixes the designated slice *a priori*, so the "currently-matched-endpoint key" is a construct the definition excludes; the load-bearing invariance fact ("the least I-address of a fixed slice is invariant") is already stated in the ASN and stands once the strawman is dropped. No design intent or implementation evidence is needed to delete a refutation of a non-candidate.

## Issue 2: definition justified by downstream use rather than its own meaning
Reason: Internal. The definitional content ("the slice is a function of the immutable link value, not of whichever endpoint matches") is already present in the ASN; the fix only removes the downstream-justification and defensive scaffolding around it, an editorial subtraction that consults neither channel.

## Issue 3: over-generalization in the key definition
Reason: Internal. The review itself notes no W-claim needs the "any such designation" generality — each needs only that the chosen key is permanent, which the ASN already establishes — so cutting the decorative generalization leaves the existing key definition (designated slice, least-covered I-address) intact without new evidence.

## Issue 4: foil bullet pre-announces the per-claim verdicts
Reason: Internal. The fix removes a forward-reference that previews conclusions W5/W6/W8/W9 prove on their own; the retained definition and the "the link search emphatically does not" fact are already in the ASN, so this is a pure editorial cut.

## Issue 5: summary essay sentence in W6
Reason: Internal. Deleting an exhaustiveness/summary sentence that does not advance W6's append-at-tail argument is a self-contained editorial cut; the append-at-tail reasoning is fully present without it.
