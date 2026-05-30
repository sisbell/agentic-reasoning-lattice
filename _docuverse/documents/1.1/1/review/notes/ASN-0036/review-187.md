# Review of ASN-0036

## REVISE

### Issue 1: OrdShiftHom cites a nonexistent proof part

**ASN-0036, OrdShiftHom (Depends)**: "S8a (V-position well-formedness) — supplies `vᵢ ≥ 1` for part (c)."

**Problem**: OrdShiftHom has exactly two postconditions, (a) and (b); its proof has only "Part (a)" and "Part (b)"; its Instance exercises only (a) and (b). There is no part (c). This is a dangling reference left over from an earlier three-part version of the lemma — precisely the reviser-drift pattern the anti-bloat classifier asks to surface. S8a is in fact consumed in part (b) (the `rₘ = vₘ + n ≥ 1 + 1 > 0` step), not in any "(c)."

**Required**: Change "for part (c)" to "for part (b)."

### Issue 2: The shift-successor fact is restated three times before OrdShiftHom states it

**ASN-0036, end of "Fixed-depth V-positions" through start of "Shift preservation for V-positions"**: three consecutive passages assert the same content before the lemma that formalizes it:

1. After the S8-depth contract: "*Within a subspace, consecutive positions differ only at the ordinal (last) component: a position v is followed by shift(v, 1) … the next ordinal at the same depth.*"
2. Immediately following: "*The successor shift(v, 1) = v ⊕ δ(1, #v) … agrees with v on positions 1 ≤ i < m and sets shift(v, 1)_m = v_m + 1, so it preserves the subspace identifier v₁ while incrementing only the ordinal component.*"
3. Subsection intro: "*We need exactly two facts about this advance: it preserves the subspace identifier, and it preserves S8a well-formedness. Both follow directly from TumblerAdd's component formula applied to δ(n, m)…*"

**Problem**: Passage 2's "preserves the subspace identifier v₁" is exactly OrdShiftHom (a); passage 3 previews and pre-proves both OrdShiftHom (a) and (b) ("Both follow directly from…"), and re-states `subspace(v) = v₁` (already fixed by the `subspace` contract) and `shift = v ⊕ δ` (already stated in passage 1). This is "two paragraphs … say the same thing in different words" plus a use-site preview that pre-proves the lemma — accreted meta-prose the precise reader must skip past to reach the actual claim.

**Required**: Keep one statement of the shift-successor fact (the OrdShiftHom lemma itself), delete the duplicating prose. At most one lead-in sentence is needed before the lemma; the component-level "agrees on 1 ≤ i < m, increments position m" belongs in the proof, not restated twice ahead of it.

## OUT_OF_SCOPE

None. Operation-layer preservation of D-CTG/D-MIN/S2 and the canonical depth choice are already correctly deferred to the Open Questions and excluded by Scope.

VERDICT: REVISE
