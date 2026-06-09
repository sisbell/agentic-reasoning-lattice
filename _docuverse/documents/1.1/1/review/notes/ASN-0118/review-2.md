# Review of ASN-0118

## REVISE

### Issue 1: CP1 is stipulated, not derived — the "necessity" claim is unsupported
**ASN-0118, "The transclusion frame"**: "The single claim that makes COPY *transclusion* and not *copying* is CP1 ... We derive it as a necessity, not a stipulation, by reasoning backward from the placement." And: "No allocation step is reachable from a state where resolution already names existing addresses, and so CP1 holds."
**Problem**: The argument shows only that referential integrity (S3) *can* be discharged without store growth — that finding `cᵢ` already present is *sufficient*. It does not show growth is *prohibited*. Store monotonicity S1 *permits* `dom(C)` to grow; nothing in S3 or the placement obligation forbids an operation from also allocating fresh content alongside the references. The sentence "no allocation step is reachable" is a non-sequitur: an operation does not allocate because its *definition* says so, not because allocation is unreachable. CP1 is precisely the frame condition that *defines* COPY as transclusion rather than REPLICATE — it is the design stipulation, and the ASN's own REPLICATE contrast confirms that an allocating operation is perfectly well-formed. Claiming CP1 is "derived as a necessity" is false.
**Required**: State CP1 as the defining frame condition of COPY (a stipulation), and recast the surrounding argument as: *given* CP1, referential integrity is dischargeable with no growth via CP0(a)+S1; *without* CP1 the operation would be REPLICATE. Drop the "necessity, not stipulation" and "no allocation step is reachable" framing.

### Issue 2: Empty-destination boundary case omitted from the contiguity/tiling derivation
**ASN-0118, "The destination's prior arrangement is preserved"**: "Before COPY, `V_{s_C}(d)` is the contiguous run `{min + i : 0 ≤ i < N}` with `min = [s_C, 1, …, 1]` (D-MIN) and `N = |V_{s_C}(d)|` ... so its top is `max = min + (N−1)`."
**Problem**: The operation precondition explicitly admits `V_{s_C}(d) = ∅` via ValidFirstInsertionPosition, but the no-holes / D-MIN / D-SEQ preservation derivation assumes `N ≥ 1`. With `N = 0`, `max = min + (N−1) = min + (−1)` is undefined, D-MIN does not apply pre-state, and the three-interval tiling argument has no left or shifted region. The empty-destination case — where COPY establishes the *first* content of a document — is exactly where D-MIN/D-SEQ must be *established* rather than *preserved*, and it is never shown.
**Required**: Add the `V_{s_C}(d) = ∅` case: `p = [s_C, 1, …, 1]`, CP3a/CP3b vacuous, placement lays `W` positions from `p`, and the post-state run `{p + i : 0 ≤ i < W}` satisfies D-MIN (`min = p`) and D-SEQ directly.

### Issue 3: Missing precondition that the spec-set's active positions lie in the content subspace
**ASN-0118, "What a spec-set names"**: "We restrict attention to *content* spec-sets: every active position is in the text subspace, `subspace(vⱼ) = s_C`, so by referential integrity (S3★) each resolves to a content address `Σ.M(d_s)(vⱼ) ∈ dom(Σ.C)`."
**Problem**: This is asserted as a scoping remark, but nothing in the V-spec definition or the COPY precondition enforces it. A V-spec's start `s` satisfies S8a but is unconstrained in `subspace(s)`, so a well-formed spec-set could have active positions with `subspace(vⱼ) = s_L`; resolution would then read link addresses (S3★ gives `dom(Σ.L)`, not `dom(Σ.C)`), and CP0(a) would fail. Worse, CP2 binds those addresses to content-subspace destination positions `p + i`, which would violate S3★ in the post-state (a content V-position imaging a link address). The guarantee CP1/CP0(a) depend on a precondition that is never stated.
**Required**: Add an explicit COPY precondition that every active position of `R` is in the content subspace (equivalently, the spec-set is content-resident), so that CP0(a) and the S3★ obligation of CP2 are actually discharged.

### Issue 4: CP8 provenance — J1★ cited as if it produces the record, and self-transclusion "already held" relies on an uncited invariant
**ASN-0118, CP8 paragraph**: "the placement enters it into that range (CP2), and ASN-0047's coupling J1★ (ExtensionRecordsProvenance) fires, forcing `(cᵢ, d) ∈ Σ'.R`." And: "`(cᵢ, d) ∈ Σ.R` already held and persists by provenance permanence (P2)."
**Problem**: Two distinct gaps. (a) J1★ is a *coupling requirement* on a valid composite — it constrains COPY to *include* a provenance-recording (K.ρ) step; it does not itself "fire" and add a record. COPY is never decomposed into its atomic K.μ⁺ + K.ρ steps, so the postcondition CP8 is justified circularly (J1★ requires the record that CP8 asserts). The record is produced by a K.ρ step that COPY must perform — that step should be named. (b) In the self-transclusion branch, the addresses `cᵢ` are bound by `d`'s own pre-state content positions, so they are not range-new and J1★ does not fire; the ASN then asserts `(cᵢ, d) ∈ Σ.R` "already held." But that membership follows from P4★ (`Contains_C(Σ) ⊆ R`), which is never cited here — P2 supplies only *persistence*, not prior *existence*.
**Required**: Either decompose COPY into its constituent K.μ⁺/K.ρ atomic steps and state that the K.ρ steps discharge CP8 (with J1★/J1'★ as the obligation/uniqueness constraints), or otherwise show the record is *produced*, not merely *required*. For the self-transclusion branch, cite P4★ to establish `(cᵢ, d) ∈ Σ.R` before invoking P2.

## OUT_OF_SCOPE

### Topic 1: Partially-bound spans (some named positions unbound)
**Why out of scope**: Listed as an Open Question; resolving the semantics of partial binding is new territory for a future ASN, not a defect here.

### Topic 2: Differing element-field depths assembled into one region; correspondence relation; link-subspace transclusion
**Why out of scope**: Each is raised as an Open Question and concerns machinery (level-uniformity reconciliation, correspondence, link placement) beyond COPY's content-placement contract.

VERDICT: REVISE
