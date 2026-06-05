# Channel Assignment — ASN-0113 review-1

**Date:** 2026-06-04 22:46

## Issue 1: W12 existential is asserted "immediate," never constructed
Reason: Internal. The fix is a formal reachability construction over the ASN-0047 kernel constructors (K.δ/K.μ⁺/K.μ⁺_L) or citation of an existing foundation existence lemma, plus correcting the cross-reference (W14→W15) and typing the quantifiers `∈ ℕ` — all derivable from already-cited foundation content without new evidence or design intent.

## Issue 2: W5 biconditional has only one direction proved
Reason: Internal. The converse direction is discharged by a concrete counterexample (e.g. `V_S(d) = {[S,1],[S,3]}`, `[S,2]` inactive) showing the min-to-max span necessarily includes `[S,2] ∈ VSlice` — a pure derivation from the ASN's own span and V-slice definitions. The Gregory appeal is exactly what the review says to replace with a proof.

## Issue 3: W9 is trivial as formalized; the substantive claim is grounded in implementation, not the foundation
Reason: Internal. The review identifies the exact foundation ground (S3★-aux / SubspaceExhaustiveness, ASN-0047) and asks to restate W9 as `O(d) = V_{s_C}(d) ⊔ V_{s_L}(d)` and derive it from that already-existing claim, dropping the implementation appeal. No new consultation is needed.

## Issue 4: No concrete worked example
Reason: Internal. Instantiating the operation on a specific document (5 text positions, 2 links) and checking W3, W4, W11, W13, W16 is a mechanical computation against the ASN's own definitions, requiring neither design intent nor implementation evidence.
