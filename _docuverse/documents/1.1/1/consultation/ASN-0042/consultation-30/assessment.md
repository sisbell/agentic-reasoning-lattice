# Channel Assignment — ASN-0042 review-30

**Date:** 2026-05-14 00:56

## Issue 1: FirstDelegatorIsπ unnecessarily invokes AccountLevelPermanence with insufficient preconditions
Reason: Internal proof fix. The reviewer has supplied the exact replacement derivation using delegation condition (ii) and the covering-chain lemma already cited from O2's proof — all material is internal to the ASN.

## Issue 2: O10 Form B coverage analysis overstates necessity as sufficient
Reason: Internal proof clarification. The precise characterization follows from T4 positivity and the prefix relation already in use; the conclusion (`u ∉ S`) is unchanged. No design intent or implementation evidence is needed.

## Issue 3: O15 axiomatized before `delegated` relation is defined
Reason: Internal exposition/ordering issue. The reviewer offers two structural remedies (reorder or inline the six conditions); both are editorial choices about presentation within the ASN, not questions of design intent or implementation behavior.
