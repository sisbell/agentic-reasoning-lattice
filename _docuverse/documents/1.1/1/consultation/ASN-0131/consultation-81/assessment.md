# Channel Assignment — ASN-0131 review-81

**Date:** 2026-06-14 14:45

## Issue 1: Cross-model-transport defense accretes around a load-bearing derivation
Reason: Purely internal/editorial — the required fix is to state the ASN-0086 standing assumption flatly and strip the methodology-defense sentences ("no cross-model transport," "source and consistency witness," etc.) while keeping the existing ASN-0093 antichain derivation. The review itself confirms the argument survives intact; all load-bearing content is already present in the note, so no design intent (Nelson) or implementation evidence (Gregory) is required.

## Issue 2: Parenthetical imagines a precondition-excluded case, then defers it
Reason: Purely internal/editorial — drop the `W ⊆ s_L` clause (a case the operation's own `W ⊆ s_C` precondition excludes) while keeping the disjointness-to-obligation connection. OQ7 already records the deferred case, so the fix is derivable from the ASN alone.
