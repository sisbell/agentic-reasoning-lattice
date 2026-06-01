# Channel Assignment — ASN-0086 review-190

**Date:** 2026-06-01 13:18

## Issue 1: CoverageEqualityDecidable — gap-nonemptiness discharge is invalid for tight successor gaps
Reason: The fix is internal. The corrected fact — `(c_k, c_{k+1})` is empty iff `c_{k+1} = c_k.0`, since `c_k.0` is the immediate T1-successor — follows from ASN-0034's already-cited tumbler-order definitions (T1, TA5 successor note); identifying and excluding empty gaps from the indicator comparison is a proof-internal repair requiring no design intent or implementation evidence.

## Issue 2: Nullify's execution precondition is overstated; the wp Case 1 parenthetical mislabels a P0-satisfied failure as "dropping P0"
Reason: The fix is internal. The contradiction is between the note's own *Definition — Emit_K* (partiality over the state-local-conforming domain when the frontier is ill-formed) and *Definition — Nullify*'s "Whenever P0 holds, Nullify executes"; reconciling them — by restricting Nullify's domain to substrate-conforming Σ or adding a well-formed-frontier execution gate, and relabeling the parenthetical — is derivable from the note's existing definitions.

## Issue 3: Forward-reference ordering justification (anti-bloat)
Reason: The fix is internal and purely editorial — delete the placement-justification clause and collapse R6d's redundant opening framing. No design or implementation input is needed to remove meta-prose.
