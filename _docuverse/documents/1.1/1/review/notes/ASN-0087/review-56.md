# Review of ASN-0087

## REVISE

### Issue 1: S8★ verification omits the content-subspace half

**ASN-0087, Per-State Invariants at Σ' (S8★ row and its "see below" discharge)**: "S8★: per-subspace span decomposition — link subspace admits trivial length-1 decomposition (see below)" and the body text discharges only `M'(d)|_{V_{s_L}^{Σ'}(d)}`.

**Problem**: ASN-0047's S8★ is a conjunction over *both* subspaces `S ∈ {s_C, s_L}`, and it retains the uniqueness condition (c) specifically on the content subspace. The verification discharges only the link-subspace decomposition and never addresses the content-subspace half — including condition (c) — at the home document `d`. Every other invariant conjunct in this ASN is addressed explicitly; this one is half-discharged, which is exactly the "skip the hard one" gap.

**Required**: State that the content-subspace decomposition `M'(d)|_{V_{s_C}^{Σ'}(d)}` (with its uniqueness condition (c)) is preserved by inheritance, because K.μ⁺_L touches only the link subspace, so `M(d)|_{V_{s_C}(d)}` is frame-fixed and the pre-state S8★ content decomposition carries to `Σ'` unchanged.

### Issue 2: M-Effect claim states "depth per M-DepthConv" for the subsequent-link case, where it does not apply

**ASN-0087, Claims Introduced (M-Effect)**: "...else `v_ℓ = shift(max(V_{s_L}(d)), 1)` (with `n_L = |V_{s_L}(d)|`); depth per M-DepthConv."

**Problem**: M-DepthConv fixes the canonical depth `m = 2` only for the *first* link MAKELINK places, and its own scope clause restricts the `m_L(d) = 2` conclusion to documents "whose link V-positions were all placed by MAKELINK." For the non-empty (subsequent) case, the depth is whatever `m_L(d)` the existing link subspace already carries — which need not be 2 if some prior link V-position at `d` was placed by another K.μ⁺_L caller at depth `m ≥ 2`. The body's Effect section correctly states "depth `m_L(d)`, the existing link-subspace depth" for this case; the table claim collapses both cases to "depth per M-DepthConv," which is imprecise for the subsequent-link branch.

**Required**: In M-Effect, attribute the empty-case depth to M-DepthConv (`m = 2`) and the non-empty-case depth to the existing `m_L(d)` (read from state), matching the body's Effect section.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets

The first and fourth Open Questions (constraints on endsets covering not-yet-allocated I-addresses; discoverability once that content is later created) concern endset authoring discipline beyond `e₃ ≠ ∅`. This is legitimately deferred — StandardAuthoring is introduced as a *discipline*, not enforced, and a full well-formedness regime belongs to a future ASN.

### Topic 2: Protocol-level atomicity of the composite

The visibility bound on the intermediate state `Σ_mid` (fifth Open Question) is correctly identified as belonging to a protocol layer above the substrate; M-CompAtomicity scopes it out rather than over-specifying.

VERDICT: REVISE
