# Review of ASN-0087

## REVISE

### Issue 1: L1c invariant verification is hand-waved
**ASN-0087, Invariant Preservation section**: "L1c: structural inc-chain conformance from SubAllocatorAxiom.ChainDiscipline"
**Problem**: L1c (foundation) requires an explicit chain `(t₀, t₁, …, tₙ)` from `t₀ = origin(ℓ) = d` to `tₙ = ℓ`, with each `kᵢ ∈ {0, 1, 2}`, `k₁ = 2`, and every intermediate length strictly exceeding `#d`. The ASN cites SubAllocatorAxiom.ChainDiscipline but never names the steps. The chain to `ℓ = [d, 0, s_L, k_s]` passes through `inc(d, 2) = [d, 0, s_C] = b_C(d)`, then `inc(b_C(d), 0) = b_L(d)`, then `inc(b_L(d), 1) = [d, 0, s_L, 1]`, then `inc(·, 0)` to reach `ℓ`. Each `kᵢ` and the `k₁ = 2` requirement need explicit verification.
**Required**: Construct the inc-chain step-by-step with each `kᵢ` identified, showing `k₁ = 2` and per-step length monotonicity.

### Issue 2: Missing S-invariant verifications in M-Inv
**ASN-0087, M-Inv claim**: lists "L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, S3★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★" plus unchanged-component invariants.
**Problem**: The list omits S-invariants relevant to introducing `v_ℓ`: S8a (V-position well-formedness — `zeros(v_ℓ) = 0`, `#v_ℓ ≥ 2`, components positive), S8-depth (common depth `m_L = 2` across link subspace), S8-fin (finiteness preserved), D-SEQ★ (the link-subspace V-positions remain a contiguous initial segment `{[s_L, 1, …, 1, k] : 1 ≤ k ≤ n_L + 1}`), and S8★ (per-subspace span decomposition for link subspace via trivial length-1 runs). D-SEQ★ in particular requires non-trivial argument that `v_ℓ` extends the existing sequence by exactly one position.
**Required**: Add explicit verification of S8a, S8-depth, S8-fin, D-SEQ★, S8★ in the Invariant Preservation section and the M-Inv claim.

### Issue 3: No concrete example
**ASN-0087, entire ASN**: No worked scenario verifies the postconditions against a specific state.
**Problem**: Standards require at least one concrete scenario. The ASN never picks a state — e.g., a document `d` with content addresses `a₁, a₂ ∈ dom(C)` and empty link subspace — and walks through MAKELINK with explicit endsets, showing the resulting `ℓ`, `v_ℓ`, post-state arrangement, and LP12 evaluation for a chosen target document.
**Required**: A worked example illustrating M-Alloc, M-Effect, M-Disc, with at least one non-trivial discoverability check.

### Issue 4: No weakest precondition analysis
**ASN-0087, Preconditions section**: Provides only forward preconditions.
**Problem**: Standards require non-trivial wp analysis. A natural target: `wp(MAKELINK, discoverable_from(ℓ, d_target, ·))`. For `d_target = d`, the wp reduces to "some `eᵢ` covers an element already in `ran(M(d))` OR some `eᵢ` covers `ℓ` itself." For `d_target ≠ d`, it reduces to "some `eᵢ` covers an element of `ran(M(d_target))`." Either case makes explicit how endset choice and target arrangement jointly determine the post-state property.
**Required**: At least one non-trivial wp computation for a post-condition of MAKELINK.

### Issue 5: v_ℓ construction not made explicit in Effect
**ASN-0087, Effect section**: "Σ'.M(d) = Σ.M(d) ∪ {v_ℓ ↦ ℓ}"
**Problem**: The Effect references `v_ℓ` without restating its construction. The formula (`v_ℓ = [s_L, 1]` of depth 2 if `V_{s_L}(d) = ∅`; `v_ℓ = shift(max(V_{s_L}(d)), 1)` otherwise) lives in K.μ⁺_L's foundation definition. Since MAKELINK is the operator-facing event, the formula belongs in MAKELINK's own specification — the reader should not need to chase K.μ⁺_L to discover what V-position is bound.
**Required**: State `v_ℓ`'s construction explicitly in the Effect section.

### Issue 6: Intermediate-state discoverability claim is imprecise
**ASN-0087, Atomicity section**: "discoverable_from(ℓ, d, Σ_mid)… its value at Σ_mid is the same as at the pre-state for every d, since Σ_mid.M = Σ.M."
**Problem**: At pre-state Σ, `discoverable_from(ℓ, d, Σ)` is undefined because the predicate's domain requires `ℓ ∈ dom(Σ.L)`, which fails. The phrase "same as at the pre-state" has no referent. The intended comparison is `Σ_mid` vs `Σ'`: at `Σ'`, `ran(M(d))` gains `ℓ`, so reflexive endsets (those covering `ℓ` itself) yield differing values at the two states; non-reflexive endsets yield the same values.
**Required**: Replace the pre-state comparison with the Σ_mid vs Σ' comparison; isolate the reflexive case.

### Issue 7: MAKELINK's side effect on other links' discoverability not analyzed
**ASN-0087, M-Frame, "What Does Not Change", and "Discoverability Is Symmetric"**: Frame asserts existing entries in `L` are unchanged; no claim addresses how the new `ℓ ∈ ran(Σ'.M(d))` changes discovery of *other* links.
**Problem**: While `L(ℓ')` for prior `ℓ'` is unchanged by L12, `ran(M(d))` is changed by adding `ℓ`. If some prior `ℓ'` has an endset whose coverage contains `ℓ`, then `discoverable_from(ℓ', d, Σ')` can become true while `discoverable_from(ℓ', d, Σ)` was false. This is a meaningful change in the discovery graph caused by MAKELINK, but the ASN's framing of "what does not change" misses it.
**Required**: Add a claim characterizing the change in discoverability of prior links from `d`, specifically the case where a prior link's endset coverage contains `ℓ`.

### Issue 8: Reflexive endset case not addressed
**ASN-0087, throughout**: No claim treats the case where one of MAKELINK's own endsets has coverage containing `ℓ` itself.
**Problem**: L13 (ASN-0043) permits link addresses as endset targets, and `coverage(eᵢ)` may include `ℓ`. After MAKELINK, `ℓ ∈ ran(Σ'.M(d))` and `ℓ ∈ coverage(eᵢ)`, so `v_ℓ ∈ project(ℓ, i, d, Σ')` — the home document immediately discovers `ℓ` via the reflexive endset. The "Discoverability Is Symmetric" section claims the home document has no privileged role in discovery, but a reflexive endset gives the home document guaranteed discovery the moment `v_ℓ` is placed. This boundary case affects M-Disc and M-DiscSymmetry.
**Required**: Add explicit treatment of the reflexive endset case, or scope it out explicitly.

### Issue 9: Verification that K.μ⁺_L's first-arrangement guard is satisfied is incomplete
**ASN-0087, Preconditions section**: "ℓ ∉ ran(M(d)) — from ℓ ∉ dom(L) at Σ and K.λ's frame (A d :: M'(d) = M(d))"
**Problem**: The derivation is missing a step. From `ℓ ∉ dom(Σ.L)` and S3★ (which constrains link-subspace V-position images to `dom(L)`), one can conclude `ℓ ∉ ran(Σ.M(d)|_{V_{s_L}(d)})`. To exclude `ℓ ∈ ran(Σ.M(d)|_{V_{s_C}(d)})`, one needs the L14 disjointness (`ℓ ∈ dom(L_mid)` and content-subspace images lie in `dom(C)`, with `dom(C) ∩ dom(L) = ∅`). The current one-line derivation conflates these.
**Required**: Make the S3★ + L14 chain explicit in deriving `ℓ ∉ ran(Σ_mid.M(d))`.

## OUT_OF_SCOPE

### Topic 1: Protocol-layer composite atomicity
**Why out of scope**: Already noted in Open Questions. Substrate provides no composite-level atomicity; protocol-layer atomicity is a separate concern.

### Topic 2: Well-formedness of endsets referencing addresses not in dom(C) ∪ dom(L)
**Why out of scope**: Already noted in Open Questions. This is endset semantics, settled by foundation L4 and LP18, not by MAKELINK specifically.

### Topic 3: V-position movement of links by subsequent operations
**Why out of scope**: Already noted in Open Questions; subsequent operations are outside this ASN's scope per the explicit operation list.

VERDICT: REVISE
