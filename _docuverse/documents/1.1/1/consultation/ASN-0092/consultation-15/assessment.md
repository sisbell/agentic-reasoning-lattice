# Revision Categorization — ASN-0067 review-15

**Date:** 2026-03-22 23:34

## Issue 1: C3 claims completeness but omits S1 and S8
Category: INTERNAL
Reason: S1 follows trivially from C' = C (already stated as C0), and S8 follows from its prerequisites (S8-fin, S8a, S2, S8-depth, D-CTG, D-MIN), all already verified in C3. The fix is adding one-line derivations from existing content.

## Issue 2: State declaration omits L; effects block incomplete
Category: INTERNAL
Reason: COPY uses no K.λ or K.μ⁺_L transitions, so L is unchanged — this is already noted in the C3 extended-state section. The fix is moving that reasoning earlier (into the state declaration or effects block) and correcting the frame-condition justification to note these transitions simply have no L-modifying effect.

## Issue 3: Per-subspace verification gap at intermediate states
Category: INTERNAL
Reason: The K.μ⁻ step removes only B_post ⊆ B_S entries; the K.μ⁺ step adds only subspace-S entries. Non-target subspaces are unchanged by construction, which is already established (B_other is classified and carried through unchanged). The fix is adding one sentence per step stating this explicitly.

## Issue 4: J1★/J1'★ equivalence argument incomplete
Category: INTERNAL
Reason: L14 (dom(C) ∩ dom(L) = ∅) and S3★ (link-subspace maps to dom(L)) are already verified in C3's extended-state invariant block. The fix is citing them alongside P.7 in the equivalence sentence — all required properties are present in the ASN.

## Issue 5: V-ordering citation incorrect
Category: INTERNAL
Reason: B1 is a coverage property; the V-ordering comes from the Resolution definition in ASN-0058, which the ASN already cites correctly elsewhere in the same section. The fix is a one-word citation swap.
