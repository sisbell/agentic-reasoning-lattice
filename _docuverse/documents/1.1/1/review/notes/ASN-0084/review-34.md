# Review of ASN-0084

## REVISE

### Issue 1: R-WP citation error for V-position subspace preservation
**ASN-0084, R-WP non-S-subspace case**: "v_j + k has subspace S' ≠ S by the corollary 'subspace preservation across a correspondence run' of ASN-0036, applied to the original run"
**Problem**: ASN-0036's S8 corollary ("subspace and field-structure preservation across a run") concerns I-addresses (`subspace_I(shift(a_j, k)) = subspace_I(a_j)`), not V-positions. The fact needed here — that `subspace(v_j + k) = subspace(v_j)` for V-positions — comes from OrdShiftHom (b), which R-BLK's Scope note cites correctly. R-WP is inconsistent with R-BLK in its citation.
**Required**: Replace the citation with OrdShiftHom (b) of ASN-0036 (with the identity convention for k = 0), matching the R-BLK usage.

### Issue 2: R-WP title misrepresents what is proved
**ASN-0084, R-WP section title "Weakest-Precondition Computation" and lemma label "RearrangeWeakestPrecondition"**: The lemma statement uses `⇐` (sufficiency), and the proof only establishes that the RHS implies wp.
**Problem**: A wp computation must characterize the weakest precondition — equivalence, not one direction. The current text shows only that R-PRE ∧ pre-state invariants ∧ B is *sufficient*. Necessity is not argued. The Dijkstra-voice frame this ASN otherwise maintains makes this terminological gap visible.
**Required**: Either retitle to "Sufficient Precondition" (and rename the lemma), or prove necessity by showing that any state where REARRANGE_C establishes Q must satisfy the RHS.

### Issue 3: Undefined notation "subspace_V"
**ASN-0084, R-BLK Scope note**: "subspace_V(v) = subspace_V(v_b) = S' for every v ∈ V(b)"
**Problem**: ASN-0036 uses `subspace` for V-position projection and `subspace_I` for I-address projection. The `_V` subscript is introduced here without definition and isn't used elsewhere in the ASN. Reader must guess that `subspace_V = subspace`.
**Required**: Use `subspace` (matching ASN-0036), or introduce `subspace_V` explicitly at first use.

### Issue 4: Missing worked example for the w_α = w_β sub-case
**ASN-0084, R-DISP and the worked examples section**: The R-DISP μ-branch defines three sub-cases (w_β > w_α, w_β < w_α, w_β = w_α). The 4-cut worked example exhibits the first sub-case (w_α = 2, w_β = 3, so Δ_μ = +1).
**Problem**: The Δ_μ = 0 sub-case (w_α = w_β) is the degenerate one where μ is *fixed* and α and β swap around it. This is a structurally different rearrangement (genuine swap rather than asymmetric exchange) and warrants verification against the formulas. Without a concrete example, the reader has only the case analysis in R-SPERM and R-DISP.
**Required**: Add a short worked example with w_α = w_β to verify Δ_μ = 0 against the postcondition formulas and the run-partition transformation.

## OUT_OF_SCOPE

### Topic 1: Inverse rearrangement and undo
**Why out of scope**: REARRANGE invertibility is a useful property (for editing semantics) but constructing the inverse cut sequence from post-state structure is a separate analysis. Not required for specifying the operation itself.

### Topic 2: Characterizing which pre-state run pairs produce post-state mergeability
**Why out of scope**: The ASN explicitly defers this in the R-BLK closing remark. The 4-cut example shows a concrete instance (B-C merging with H), but the general characterization requires tying region assignment to I-address arithmetic — a refinement for a follow-on ASN.

### Topic 3: REARRANGE on text subspaces with depth m_1 > 2
**Why out of scope**: The ASN restricts to m_1 = 2 explicitly. Lifting the depth restriction requires generalizing the singleton-tumbler/natural identification to multi-component ordinals; this is a separate generalization, not a gap in this ASN.

### Topic 4: Cross-subspace REARRANGE
**Why out of scope**: Explicitly declared out of scope by CS3 and the introductory prose.

VERDICT: REVISE
