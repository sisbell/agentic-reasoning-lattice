# Review of ASN-0070

## REVISE

### Issue 1: F-subspace consequence derivation hand-waves the biconditional
**ASN-0070, F-subspace Consequence derivation**: "By F-subspace, `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)` for `v ∈ dom(M(d))`."
**Problem**: F-subspace's postcondition is `subspace(v) = subspace_I(M(d)(v))`. To reach the biconditional `subspace(v) = s_C ⟺ M(d)(v) ∈ dom(C)`, the reverse direction (`M(d)(v) ∈ dom(C) ⟹ subspace(v) = s_C`) needs S3★-aux (exhaustiveness, ruling out subspace(v) = s_L) and L14 (`dom(C) ∩ dom(L) = ∅`, ruling out S3★'s alternative target). L0 provides only `a ∈ dom(C) ⟹ subspace_I(a) = s_C`, not the reverse.
**Required**: Make the case analysis explicit: forward via F-subspace + L0; reverse via S3★ + S3★-aux + L14 (a tumbler in subspace `s_C` that's in `ran(M(d))` must be in `dom(C)` because if it were in `dom(L)`, L14 would force `subspace_I` = `s_L`, contradicting F-subspace).

### Issue 2: V-restricted denotation undefined for empty content subspace
**ASN-0070, V-Restricted Denotation definition**: "`⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) }`"
**Problem**: For `S = s_L`, `m_L = 2` is fixed by LinkVPositionDepthAxiom. For `S = s_C`, `m_{s_C}(d)` is defined only when `V_{s_C}(d) ≠ ∅` (S8-depth, ASN-0036; first depth fixed by ValidFirstInsertionPosition). For a freshly created document `d` (where K.δ gives `M'(d) = ∅`), or any document with empty content subspace, `m_{s_C}(d)` is undefined and the formula is ill-formed. The wp analysis does not address this gap; F1's postcondition presumes well-formedness; F-canonical and F-empty inherit the issue.
**Required**: Adopt a convention (e.g., `⟦Σ_V^S⟧_V := ∅` when `m_S(d)` is undefined, or `m_S(d) := ⊥` with the formula yielding `∅`), or refine F1's precondition to ensure non-empty subspace, or argue that the only admissible `Σ_V^S` for empty subspace is `⟨⟩` and the equation holds trivially.

### Issue 3: F-canonical Step 1 over-restricts canonical form widths
**ASN-0070, Canonical Form, Derivation of uniqueness, Step 1**: "Spans constructed with these V-positions as starts and ordinal displacements as widths (per F-contig below) have start, width, and reach all of length `m_S(d)`..."
**Problem**: The restriction to "ordinal displacements as widths" is asserted but not justified. F-contig describes one computation path (via mapping-block intersection); it does not establish that canonical-form components must use ordinal-displacement widths. A level-uniform span `([S, x], [c, ...])` with `c ≥ 1` at action point 1 produces reach outside subspace `S` and either an infinite V-restricted denotation or one that cannot match a finite target. The derivation should make this exclusion argument explicit, not cite F-contig as if it discharged the obligation.
**Required**: Argue that for the V-restricted denotation to be finite and confined to subspace `S` at depth `m_S(d)`, the width's action point must be ≥ 2 (so the first component is zero, preserving subspace), forcing widths of the ordinal-displacement form `[0, ..., w_m]`. Or characterize canonical form abstractly without restricting widths and rely on S9 alone.

### Issue 4: F-canonical Step 2 conflates `⟦·⟧` and `⟦·⟧_V`
**ASN-0070, Canonical Form, Derivation of uniqueness, Step 2**: "S9 (NormalizationUniqueness, ASN-0053) gives, among span-sets denoting the same V-restricted set of positions, a unique normalised form."
**Problem**: S9 governs equality under `⟦·⟧` (full denotation), not `⟦·⟧_V` (V-restricted denotation). Two normalized span-sets with the same `⟦·⟧_V` need not have the same `⟦·⟧` in general. The bridge — for level-uniform spans at depth `m_S(d)` in subspace `S`, the V-restricted denotation determines the starts and reaches, hence the full denotation — must be argued, not assumed. This is what justifies invoking S9 on the V-restricted equivalence class.
**Required**: Show that under the level-uniformity hypothesis, two normalized span-sets with `⟦Σ̂₁⟧_V = ⟦Σ̂₂⟧_V` also satisfy `⟦Σ̂₁⟧ = ⟦Σ̂₂⟧`, then apply S9.

### Issue 5: F-empty's canonical form argument has the same `⟦·⟧` vs `⟦·⟧_V` gap
**ASN-0070, F-empty derivation**: "any non-empty normalised span-set has non-empty V-restricted denotation by S2 of ASN-0053"
**Problem**: S2 of ASN-0053 says every well-formed span has non-empty `⟦σ⟧`, not non-empty `⟦σ⟧_V`. The argument needs to invoke the fact that canonical-form components are constructed as level-uniform spans at depth `m_S(d)` in subspace `S`, so the start `s` satisfies `subspace(s) = S ∧ #s = m_S(d)`, placing `s ∈ ⟦σ⟧_V` (since `s ∈ ⟦σ⟧` by TA-strict).
**Required**: Make the bridge from S2 to V-restricted non-emptiness explicit — the start of any canonical-form span is, by construction, a depth-`m_S(d)` subspace-`S` tumbler in the span's denotation.

### Issue 6: `m_S(d)` notation used without formal introduction
**ASN-0070, F1 postcondition and throughout**: "each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)`"
**Problem**: The notation `m_S(d)` appears in F1, V-Restricted Denotation, F-canonical, F-empty, and the wp analysis, but is never formally introduced. The Setting section uses the distinct notations `m_{s_C}` (citing S8-depth) and `m_L = 2` (citing LinkVPositionDepthAxiom). The unified `m_S(d)` notation appears without a definition tying it back to these foundations.
**Required**: Introduce `m_S(d)` formally — e.g., "Write `m_S(d)` for the common V-position depth in subspace `S` of document `d`: `m_{s_C}(d)` is the common content depth from S8-depth (when defined); `m_{s_L}(d) = 2` by LinkVPositionDepthAxiom" — and acknowledge the empty-subspace case (Issue 2).

### Issue 7: Worked example does not exercise F-state
**ASN-0070, A Worked Example**: The example presents three configurations (Configuration 1, Second configuration, Third configuration) that differ in the link's endset, not in the system state.
**Problem**: F-state's claim — across different states, `R` may differ for the same link — is asserted without a witness. The "different configurations" in the worked example vary the endset (different `L(ℓ).e₁`), which exercises F0's dependence on coverage but not F-state's dependence on state. A more thorough example would fix the link and show how a K.μ⁺ or K.μ⁻ transition changes the result.
**Required**: Add a fourth configuration showing the same link evaluated against `d` before and after an arrangement-changing transition (e.g., K.μ⁻ that removes a V-position whose I-address is in the coverage), with the resolution differing across states.

## OUT_OF_SCOPE

The Open Questions section properly flags 8 topics that belong to future ASNs (partial reach reporting, cross-document reach relationships, concurrency semantics, transclusion lineage effects on resolution, ordering requirements, compactness guarantees, resolution-vs-retrieval relationship, canonicalisation exposure). No additional out-of-scope topics observed.

VERDICT: REVISE
