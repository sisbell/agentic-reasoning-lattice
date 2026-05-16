# Review of ASN-0051

## REVISE

### Issue 1: SV6 worked example uses inconsistent subspace conventions
**ASN-0051, "Cross-origin exclusion (SV6)" worked example**: The example uses `s = 1.0.1.0.1.0.1.2.3` where `s_7 = 1` is the first element-field component, calling this the subspace identifier.
**Problem**: The "Subspace note" preceding the example states "The example below uses tumblers with first component 1; this aligns with the content subspace s_C = 1 used in the SV10 witness for consistency across worked examples". But the first element-field component (position p₃+1 = 7) is `s_C` per the K.α amendment of ASN-0047, not the *first* component of the whole tumbler. The SV10 witness uses element field `E(i_k) = [1, k]` where `1 = s_C` at position E₁. The two uses of "first component" — first of the whole tumbler vs first of the element field — are conflated.
**Required**: Clarify that the relevant "first component" is the first element-field component (s_C in the element-field's E₁ slot), and verify the worked example's tumblers respect this. As written, the element-field of `s` is `[1, 2, 3]` so E₁(s) = 1 = s_C, which is correct, but the prose comment about "first component" is ambiguous.

### Issue 2: SV13(e) link-subspace extension classification
**ASN-0051, SV13(e) M-frame list**: "K.α, K.δ, K.ρ, and K.λ all preserve M-values in their frame... (K.μ⁺_L is *not* M-frame — it adds a V↦I mapping in the link subspace — and is covered by the extension bullet above)"
**Problem**: The parenthetical correctly distinguishes K.μ⁺_L as M-modifying. However, the "K.δ caveat" treats K.δ's seeding of `M(d_new) = ∅` as "M-frame in the sense that M-values at every pre-existing d ∈ dom(Σ.M) are unchanged". By the same argument, K.μ⁺_L is also "M-frame in the sense that values at pre-existing v ∈ dom(M(d)) are unchanged" — it just extends dom(M(d)) by one new V-position. The classification is inconsistent: K.δ extending dom(M) by one document with empty arrangement is called M-frame (with caveat), while K.μ⁺_L extending dom(M(d)) by one V-position is called not M-frame. Both extend dom; neither modifies existing values.
**Required**: Either include K.μ⁺_L in the M-frame list with parallel caveat (treating both as "preserve M-values at pre-existing entries"), or treat K.δ's seeding as M-modifying alongside K.μ⁺/K.μ⁺_L. The current asymmetric treatment confuses the M-frame concept.

### Issue 3: OrdinalShiftBase description wording
**ASN-0051, Notation section**: "TumblerAdd applied at the position of a's last nonzero component (position #a for T4-valid a)"
**Problem**: The OrdinalShift definition (ASN-0034) operates at position `#a` regardless of T4-validity — `shift(v, n) = v ⊕ δ(n, #v)` always uses #v as the action point. For T4-valid `a`, position #a happens to coincide with the last nonzero component (since T4(iv) gives `a_#a ≠ 0`). The description leads with "last nonzero component" then clarifies via parenthetical, but the lead phrasing is structurally misleading: the operation is "at position #a", and the "last nonzero" reading is a consequence of T4-validity, not the operation's specification.
**Required**: Lead with the structural definition: "TumblerAdd applied at the trailing position #a (which for T4-valid a coincides with the last nonzero component)".

### Issue 4: dom_C terminology used without local definition
**ASN-0051, SV5 composite-level note**: "when dom_C(M(d)) ≠ ∅ it expands into two consecutive elementary steps"
**Problem**: `dom_C(M(d))` appears in ASN-0047's K.μ~ definition as a shorthand but is not given an explicit definition in either ASN-0047 or ASN-0051. From context it appears to mean `V_{s_C}(d)` (content-subspace V-positions per ASN-0036), but readers must infer this. The shared vocabulary list defines V_S(d) explicitly; dom_C is a different notation that aliases it.
**Required**: At first use in this ASN, gloss `dom_C(M(d))` as `V_{s_C}(d) = {v ∈ dom(M(d)) : subspace(v) = s_C}`, or replace with the explicit V_{s_C}(d) notation throughout.

### Issue 5: SV14(d) witness — F' coverage interval boundary
**ASN-0051, SV14(d) witness**: "carrying `F' = {(a₃, ℓ_a')}` for `ℓ_a' = a₄ ⊖ a₃` — well-defined by D0 (a₃ < a₄, equal lengths)"
**Problem**: D0 requires `a < b ∧ divergence(a, b) ≤ #a`. The witness invokes "a₃ < a₄, equal lengths" but doesn't address the divergence condition. For T4-valid sibling tumblers of equal length, divergence is at the last position (≤ #a), so D0 is satisfied — but the witness skips this step. Similarly, T12-well-formedness of (a₃, ℓ_a') requires `Pos(ℓ_a')` and `actionPoint(ℓ_a') ≤ #a₃`, also not explicitly addressed.
**Required**: Expand the discharge to: "well-defined by D0 since a₃ < a₄ with equal lengths places divergence at the last position ≤ #a₃; (a₃, ℓ_a') is T12-well-formed since Pos(ℓ_a') from a₃ < a₄ and actionPoint at #a₃". This pattern recurs in the SV10 witness with adequate detail; SV14(d) should follow suit.

### Issue 6: SV11 multi-block attainment witness — p ≥ 3 case only gestured
**ASN-0051, SV11 multi-block attainment**: "The same construction generalises: a single sufficiently-long block β₁ overlapped by a second block β₂ at a tail subset, paired with m spans whose coverages each puncture both blocks' offsets at non-adjacent positions, witnesses attainment at higher (m, p)..."
**Problem**: The witness explicitly exhibits (m = 2, p = 2). For (m ≥ 2, p ≥ 3), all (p choose 2) pairs must overlap and every block must satisfy `n_k ≥ 2m − 1`. The "construction generalises" gesture leaves the reader to verify that such a configuration is actually realizable at p ≥ 3 (does requiring all three pairs of three blocks to pairwise overlap force constraints that prevent attainment?). The biconditional itself is fully proven, but the existence claim for the (m ≥ 2, p ≥ 3) regime relies on an unconstructed witness.
**Required**: Exhibit a concrete p = 3 witness (e.g., three nested blocks β₁ ⊇ β₂ ⊇ β₃ with sufficient sizes, plus m spans puncturing each at non-adjacent positions), or explicitly state that p ≥ 3 attainment is conjectural pending further construction.

### Issue 7: Empty-arrangement boundary for SV11
**ASN-0051, SV11**: The claim "every arrangement M(d) admits a block decomposition" via C1a covers the M(d) = ∅ case (where p = 0 and B = ∅).
**Problem**: SV11's formula `π_text(e, d) = ⋃_{j,k}` with k ranging over an empty index set yields an empty union (correctly π_text(e, d) = ∅), and the bound m · p = 0 is also empty. But this boundary case is not explicitly noted, and the attainment biconditional ("every (j, k) yields a non-empty term") is vacuously satisfied when no (j, k) pairs exist. A reader checking edge cases against the biconditional will wonder whether m · p = 0 counts as attained.
**Required**: Add a brief boundary note clarifying the p = 0 case: π_text(e, d) = ∅, m · p = 0, and the bound is trivially attained.

## OUT_OF_SCOPE

None. The ASN appropriately defers same-origin coverage growth to ASN-0034's allocator discipline, link-subspace endset projection to a future Link Subspace ASN, and broader-level span survivability to ASN-0034 — these scope deferrals are clearly marked.

VERDICT: REVISE
