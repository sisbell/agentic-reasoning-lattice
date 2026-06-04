# Review of ASN-0087

## REVISE

### Issue 1: D-CTG★ discharge rests on an unsupported global reachability claim
**ASN-0087, *Invariant Preservation* → "For D-CTG★":** "MAKELINK is the sole producer of link-subspace V-positions (M-Comp): it commits the canonical depth `m_L^{Σ'}(d) = 2` for every first link it places (M-DepthConv) ... Hence `m_L(d) > 2` is never reachable, and the slice is the depth-2, subspace-`s_L` slice ... a slice with *no* interior positions."

**Problem**: D-CTG★ is a per-state invariant that must hold at `Σ'` for an *arbitrary* reachable pre-state satisfying the invariant package. That package (S8a, S8-depth, D-SEQ★, …) does not pin `m_L(d) = 2`; the substrate's `K.μ⁺_L` explicitly admits `ValidFirstLinkPosition(d, v_ℓ, m)` for *any* `m ≥ 2` (ASN-0047). The proof closes this gap by asserting "MAKELINK is the sole producer of link-subspace V-positions," but:
- This is attributed to M-Comp, which states only that MAKELINK *equals* `K.λ ; K.μ⁺_L` — it says nothing about MAKELINK being the *only* invoker of `K.μ⁺_L`. The citation does not support the claim.
- A single ASN cannot establish a global reachability fact about every invocation of an independently-listed substrate atomic (`K.μ⁺_L` appears in ASN-0047's valid-composite vocabulary). "`m_L(d) > 2` is never reachable" is therefore unproven.

The conclusion (contiguity) does in fact hold at any depth, which makes the detour both unsound and unnecessary: within a fixed first-component slice, the only slice tuples `z` with `[s_L,1,…,1] ≤ z ≤ [s_L,1,…,1,K]` are exactly `{[s_L,1,…,1,k] : 1 ≤ k ≤ K}` (any tuple raising an interior component exceeds the upper extreme under T1).

**Required**: Prove D-CTG★ directly for arbitrary `m_L(d) ≥ 2` — the extension-by-one-at-the-top of a D-SEQ★ initial segment is contiguous at every depth — and delete the unsupported "sole producer / never reachable" reasoning (and its misattribution to M-Comp). The "no interior positions" shortcut and its dependence on a global reachability claim should go.

### Issue 2: Reviser-drift / accretion around the freshness derivation
**ASN-0087, *Freshness of the Allocation*** and **Side Effects, final paragraph**:

- The dedicated *Freshness of the Allocation* section, forward-referenced from *Preconditions* (`[*Freshness of the Allocation*, below]`), reduces to two bullets that each restate a foundation lemma already named (`FirstEmissionFreshness`, `SubsequentEmissionFreshness`, ASN-0093). It advances no reasoning beyond the citation the *Preconditions* bullet already carries; the forward reference plus a section-for-a-citation is accretion.
- *Side Effects*, final paragraph: "The new step here is the backward transfer of `ℓ`'s freshness from the K.λ allocation state `Σ_ℓ` to the earlier authoring state `Σ_{ℓ'}` …" — "The new step here is" is narration *about* the proof rather than the proof; fold the (valid) backward-transfer reasoning in without the meta-framing.

**Problem**: Both force the reader past meta-prose / restated foundation citations to follow the actual claim.
**Required**: Collapse *Freshness of the Allocation* into the existing *Preconditions* citation (one line), and strip the "The new step here is" framing from the side-effects derivation.

### Issue 3: Duplicated sentence in the claims table
**ASN-0087, Claims table, M-Comp**: "The semicolon denotes sequential composition of atomic transitions." is a verbatim repeat of the same sentence in *Decomposition*.
**Problem**: Same statement in two slots.
**Required**: Keep it in *Decomposition*; drop it from the table description (the table should carry the claim, not re-explain notation).

## OUT_OF_SCOPE

### Topic 1: Exclusivity of MAKELINK as the link-V-position producer
**Why out of scope**: Whether `K.μ⁺_L` is ever invoked outside MAKELINK is a global property of the operation vocabulary, settled by the composite-operation layer, not by this note. (Issue 1 only asks that the D-CTG★ proof not *depend* on it.)

VERDICT: REVISE
