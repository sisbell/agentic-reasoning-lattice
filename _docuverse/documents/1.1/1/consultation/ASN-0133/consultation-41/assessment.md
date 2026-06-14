# Channel Assignment — ASN-0133 review-41

**Date:** 2026-06-14 13:10

## Issue 1: The heterogeneous-rewrite rationale is stated three times
Reason: Pure deduplication — the required fix names exactly which statement to keep (Q0's abstract rewrite, the worked numeric computation) and which prose restatements to drop. All content is already present in the ASN; nothing turns on design intent or implementation behavior.

## Issue 2: Extended meta-commentary on hypothesis roles ("why/whether used") rather than what they say
Reason: The operative role-facts (H-W ⟹ H-RF via Q5; H-W implies quiescence directly; H-SFAIR's regime form excludes case (3) but needs turn-fairness equivalent to regime (i)) are all theorems the note already derives, and the required fix supplies the one-line condensations verbatim. Collapsing the repeated re-derivations is internal editorial work.

## Issue 3: Q6 conflates its statement with its proof
Reason: Reorganization only — lead with the unconditional registry-side result, tabulate the per-package reached-and-held conclusions, then give the proof. The hypothesis-attribution correction ("weak H-FAIR alone" → "weak H-FAIR + bounded growth") is supplied by Q6's own proof text ("With bounded growth each of the finitely many arguments…"), so the fix is derivable from the ASN alone.
