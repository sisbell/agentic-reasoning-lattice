# Review of ASN-0063

## REVISE

### Issue 1: ExtendedReachableStateInvariants — D-CTG and D-MIN unverified for K.μ⁺, K.μ⁻, K.μ~
**ASN-0063, ExtendedReachableStateInvariants proof**: "For K.μ⁺ (amended), K.μ⁻, K.μ~: hold L in frame; arrangement invariants verified in the S3★ and P4★ analyses above"
**Problem**: The theorem lists D-CTG and D-MIN among the invariants preserved in every reachable state, but the cited S3★ and P4★ analyses verified only S3★ and P4★ — not D-CTG or D-MIN. These three transitions modify M(d) and can violate contiguity/minimum constraints: K.μ⁺ can add a non-contiguous V-position (e.g., `[s_C, n+3]` when the current range ends at `n`); K.μ⁻ can remove an interior position; K.μ~ with an arbitrary bijection π can rearrange V-positions to violate D-MIN. ASN-0047's K.μ⁺ precondition requires S8a, S8-depth, and S8-fin but not D-CTG or D-MIN. ASN-0047's ReachableStateInvariants similarly omits D-CTG and D-MIN. Since this ASN claims the extended theorem, the proof must cover these invariants for all transitions — including the pre-existing ones.
**Required**: Verify D-CTG/D-MIN preservation for K.μ⁺ (amended), K.μ⁻, K.μ~. For K.μ~, the argument is available: D-SEQ uniquely determines the V-position set from D-CTG + D-MIN + S8-fin + S8-depth, so any bijection π satisfying these constraints maps dom_C(M(d)) to itself — forcing π to be the identity on content-subspace V-positions. For K.μ⁺ and K.μ⁻, either amend their postconditions with D-CTG/D-MIN requirements (as was done for K.μ⁺_L), or prove preservation from existing constraints at the composite level. S8 (SpanDecomposition) depends on D-CTG via D-SEQ, so its preservation is also unverified for these transitions.

### Issue 2: CL11 S8 verification — link-subspace runs omitted
**ASN-0063, CL11**: "existing text-subspace runs are unchanged since no text-subspace V-position is added, removed, or remapped. ✓"
**Problem**: S8's formal quantifier is `v₁ ≥ 1`, which captures link-subspace positions (the ASN correctly establishes s_L ≥ 1 from L0+L1+T4). When `V_{s_L}(d) ≠ ∅` before CREATELINK, the pre-existing link-subspace correspondence runs also fall under S8's quantifier. The verification addresses only "existing text-subspace runs," leaving existing link-subspace runs unmentioned.
**Required**: State that all existing runs — both text-subspace and link-subspace — are unchanged, since K.μ⁺_L preserves existing mappings (frame) and adds one position that either extends the last link-subspace run (if I-adjacent) or forms a new width-1 run. The new position `v_ℓ ∉ dom(M(d))` falls in no existing run, so no existing run is split or modified.

### Issue 3: CL2 derivation gap
**ASN-0063, CL2**: "Immediate from CL1"
**Problem**: CL1 is existential — "there exists E ∈ Endset with image(d, Ψ) ⊆ coverage(E)." CL2 asserts containment for the specific endset `resolve(d, Ψ)`. The derivation depends on CL1's *construction* (which builds exactly `resolve(d, Ψ)` from CL0 I-spans over the canonical decomposition), not on CL1's existential statement. As stated, the reader must re-inspect CL1's proof to confirm that the witness is `resolve`.
**Required**: Change "Immediate from CL1" to "Immediate from CL1's construction" or reference that CL1 constructs exactly `resolve(d, Ψ)`.

### Issue 4: Link-subspace withdrawal — singleton imprecision
**ASN-0063, Extending the Transition Framework (orphan link analysis)**: "Only the maximum V-position can be removed without violating D-CTG (removing the minimum would violate D-MIN)."
**Problem**: When `|V_{s_L}(d)| = 1`, the sole position is both minimum and maximum. Removing it leaves `V_{s_L}(d) = ∅`, and D-MIN is vacuously satisfied. The claim "removing the minimum would violate D-MIN" is false in this case.
**Required**: Qualify: "When `|V_{s_L}(d)| ≥ 2`, only the maximum can be removed without violating D-CTG or D-MIN. When `|V_{s_L}(d)| = 1`, the sole position can be removed (D-MIN holds vacuously for the empty set)."

### Issue 5: CREATELINK valid composite not explicitly verified
**ASN-0063, The CREATELINK Composite**: The composite is defined as K.λ + K.μ⁺_L, postconditions are stated (CL3), and invariant preservation is proved (CL11), but the ValidComposite requirements are not verified at the composite definition site.
**Problem**: ValidComposite (ASN-0047) requires (1) elementary preconditions at each intermediate state and (2) coupling constraints J0, J1★, J1'★ for the composite. K.μ⁺_L's precondition `ℓ ∈ dom(L)` must hold at the intermediate state (after K.λ), and coupling constraints must be checked. The necessary pieces are scattered: K.λ's frame leaves M unchanged (so K.μ⁺_L's V-position preconditions are evaluated against the pre-state); coupling constraints are analyzed in the orphan link discussion and CL11. But the verification is never consolidated into an explicit "CREATELINK is a valid composite" statement.
**Required**: Add explicit ValidComposite verification at the composite definition — confirm K.μ⁺_L's preconditions hold at the intermediate state (citing K.λ's frame), and confirm J0/J1★/J1'★ hold for the composite.

## OUT_OF_SCOPE

### Topic 1: S8a commentary inconsistency with s_L ≥ 1
**Why out of scope**: ASN-0036 S8a's parenthetical "(where v₁ = 0)" for link-subspace V-positions contradicts L0+L1+T4 (which establish s_L ≥ 1). This is a foundation error — the formal predicate `v₁ ≥ 1` is correct and the commentary is wrong. ASN-0063 correctly uses the formal predicate; the commentary correction belongs in ASN-0036.

### Topic 2: Link withdrawal mechanism
**Why out of scope**: The ASN identifies the constraints (D-CTG fixity, link-subspace fixity under K.μ~) and explicitly defers the withdrawal mechanism to open questions. This is new design territory, not an error.

### Topic 3: D-CTG/D-MIN in K.μ⁺, K.μ⁻, K.μ~ definitions
**Why out of scope**: The root cause is ASN-0047's transition definitions, which omit D-CTG/D-MIN from preconditions/postconditions. Amending those definitions is ASN-0047's scope. ASN-0063 must verify preservation (Issue 1 above) but need not redefine the elementary transitions.

VERDICT: REVISE
