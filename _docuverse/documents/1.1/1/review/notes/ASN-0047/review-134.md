# Review of ASN-0047

## REVISE

### Issue 1: Typo or unclear phrasing in version-chain discussion
**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation"**: "The allocator-tree relationship `A_v(d) ⊆ A_v(d)` (every version after v_1 lives in the same A_v(d) allocator) is orthogonal to the T4b parent projection that P8 quantifies over."

**Problem**: `A_v(d) ⊆ A_v(d)` is trivially true (any set is a subset of itself) and doesn't express the intended meaning. The parenthetical suggests the intent is "every version after v_1 inhabits `dom(A_v(d))`" — a containment relation between versions and the allocator's domain, not between the allocator and itself.

**Required**: Replace with the intended relation, e.g., `{v_i : i ≥ 1} ⊆ dom(A_v(d))` or "every v_i with i ≥ 1 has v_i ∈ dom(A_v(d))".

### Issue 2: T10a.7 citation in (t, 0) uniqueness derivation
**ASN-0047, "K.δ case (ii) discharge", FrontierEquivalence premise (i)**: "T10a chain-advancement uniqueness at `(t, 0)` (derived, not axiomatic): ... The derivation chains T10a.7 (EnumerationInjectivity, ASN-0034) — the chain map `n ↦ tₙ` is injective, so `inc(tₙ, 0)` deterministically advances the chain to `tₙ₊₁` (a determinate next address, not a choice) — with P1's E-monotonicity (premise (ii)) and the operational precondition `inc(t, 0) ∉ E`..."

**Problem**: The (t, 0)-fires-at-most-once property is actually delivered by: (a) TA5(c)'s functional determinism of inc(t, 0), (b) the precondition `inc(t, 0) ∉ E` enforced at each K.δ event, and (c) P1's preservation. T10a.7 (EnumerationInjectivity) says distinct chain *indices* map to distinct addresses; it does not establish that inc is a function. The determinism of `inc(tₙ, 0) = tₙ₊₁` is from TA5(c), not from T10a.7. The framing makes T10a.7 load-bearing when it is actually tangential.

**Required**: Restate the derivation chain as TA5(c) (functional determinism) + precondition + P1, with T10a.7 cited only where it actually does work (e.g., in framing the chain's enumeration structure for "frontier" identification).

### Issue 3: Sub-allocator names provenance labeling
**ASN-0047, "Allocator hierarchy under documents", Sub-allocator names**: "**Sub-allocator names** (per ASN-0093 for d-rooted sub-allocators; A_doc and A_account introduced here as the entity-hierarchy generalisations)."

**Problem**: The parenthetical implies all d-rooted sub-allocators are from ASN-0093, but A_v(d) (the version sub-allocator) is also d-rooted and is introduced in this ASN, not in ASN-0093. ASN-0093 defines only A_C(d) and A_L(d). Readers tracing provenance for A_v(d) to ASN-0093 will not find it there.

**Required**: Clarify the attribution: "A_C(d) and A_L(d) per ASN-0093; A_v(d), A_doc(A), A_account(N) introduced here." This matches the actual provenance.

### Issue 4: S8★ link-subspace decomposition relies on undefined operation
**ASN-0047, "S8★ (Per-subspace span decomposition)"**: "*Link subspace.* `M(d)|_{V_{s_L}(d)} : V_{s_L}(d) → dom(L)` ... S8★(s_L) is instead discharged by the *trivial length-1 decomposition* `{(v, M(d)(v), 1) : v ∈ V_{s_L}(d)}` — every link-subspace V-position constitutes its own length-1 correspondence run, satisfying S8's conditions (a) and (b) on singletons by construction."

**Problem**: ASN-0036's S8 condition (b) is `M(d)(shift(v_j, k)) = shift(a_j, k)` for `0 ≤ k < n_j`. At `n_j = 1`, the only check is at `k = 0`, requiring `M(d)(shift(v, 0)) = shift(a, 0)`. But OrdShift in ASN-0036 requires `n ≥ 1`, making `shift(v, 0)` undefined. The proof relies on a convention `shift(v, 0) = v` that is not stated. Without this convention, "satisfying S8's conditions ... on singletons by construction" is unverifiable.

**Required**: State the `shift(v, 0) := v` convention explicitly, or rework the trivial decomposition to avoid the undefined operation (e.g., by using the run definition `(A k : 0 ≤ k < 1 : ...)` which is vacuous at `n = 1` if shift at `k = 0` is excluded).

### Issue 5: J4 fork omits link-subspace clearance discharge
**ASN-0047, "J4 (Fork composite)"**: The fork definition lists only K.δ + K.μ⁺ + K.ρ "and no other elementary steps."

**Problem**: The ASN later states "Link-subspace mappings from the source document are not copied — the forked document's link subspace starts empty." But what about D-CTG★ / D-MIN★ on `V_{s_L}(d_new)` at the post-state? The proof states they hold "vacuously since V_{s_L}(d_new) is empty." However, the fork's K.μ⁺ step adds only content-subspace positions (by amendment), so V_{s_L}(d_new) remains empty — but K.δ alone establishes `M(d_new) = ∅` by the totality convention. The discharge for link-subspace invariants relies on this initialization, which should be cited explicitly. The current text moves through the discharge quickly without naming "K.δ initialises M(d_new) = ∅, so V_{s_L}(d_new) = ∅ at fork's intermediate state."

**Required**: Make the K.δ initialization explicit in the fork's invariant verification — name the route from K.δ's totality-convention effect on M(d_new) to the empty V_{s_L}(d_new) at the fork's post-state.

### Issue 6: Worked example "Step 5" verification gap
**ASN-0047, "Worked example: link allocation and arrangement", Step 5 (K.μ⁻ contracting links)**: The verification of D-SEQ★ at Σ' states `V_{s_L}(d') = {[s_L, 1]} matches {[s_L, k] : 1 ≤ k ≤ 1}` at n_{s_L} = 1.

**Problem**: D-CTG★ over the singleton V_{s_L}(d') = {[2, 1]} is asserted contiguous trivially. But the K.μ⁻ admissible contraction shape proof requires the post-state characterization (D-CTG★ + D-MIN★ + D-SEQ★) to match the constructive precondition (n'_{s_L} = 1). The example does not verify that the operation discharged its precondition (per-subspace retention count) before firing; it only verifies the post-state. The link between "user chose n'_{s_L} = 1" and "the per-subspace constructive shape was admissible" is not shown.

**Required**: In the K.μ⁻ verification step of the worked example, explicitly state the chosen (n'_{s_C}, n'_{s_L}) pair and confirm the constructive precondition is satisfied, then derive the post-state shape from it.

### Issue 7: K.μ⁺ pairwise-distinctness clause is overcomplicated
**ASN-0047, "K.μ⁺ (Arrangement extension)" precondition**: "*Pairwise V-position distinctness on new mappings:* the set of newly added V-positions `{v : v ∈ dom(M'(d)) ∖ dom(M(d))}` is in bijective correspondence with the set of new mappings — equivalently, K.μ⁺ does not specify two distinct mappings `(v₁ ↦ a₁), (v₂ ↦ a₂)` with `v₁ = v₂` and `a₁ ≠ a₂`."

**Problem**: This precondition expresses S2 (functionality) preservation indirectly. A reader must parse the bijective-correspondence statement and the contrapositive form to extract the underlying constraint (new mappings have pairwise distinct V-positions). The "equivalently" rephrasing is the contrapositive of distinctness, which is functionality. Since S2 is a per-state invariant the operation is required to preserve anyway, the verbose precondition statement adds little clarity.

**Required**: Either reformulate as the direct distinctness statement ("the new V-positions `{v_1, ..., v_k}` are pairwise distinct"), or note that this is just S2 preservation made explicit for the operation's multi-position semantics.

### Issue 8: K.μ~ matrix entry "via fixity" is imprecise
**ASN-0047, "ExtendedReachableStateInvariants", verification matrix, K.μ~ entry for D-CTG★/D-MIN★**: "K.μ⁻ (full-clearance) leaves link subspace contiguous via fixity and content subspace empty (vacuous); K.μ⁺ preconditions re-establish D-CTG★ / D-MIN★ on the rebuilt content arrangement..."

**Problem**: "Leaves link subspace contiguous via fixity" reads as invoking the K.μ~ link-subspace fixity theorem (Steps 1–4 of the Decomposition section). But the full-clearance form retains V_{s_L}(d) pointwise *by construction*, not by appeal to the fixity theorem. The fixity theorem is what justifies the convention; the full-clearance form's effect on link subspace is direct (it doesn't remove any link-subspace positions). The matrix entry conflates the convention's foundation with its mechanical application.

**Required**: Rephrase to "K.μ⁻ (full-clearance) by construction retains V_{s_L}(d) pointwise; D-CTG★/D-MIN★ on link subspace carry forward from Σ via the inductive hypothesis."

## OUT_OF_SCOPE

### Topic 1: Worked example for K.μ~ with content cardinality > 2
**Why out of scope**: The worked examples cover |dom_C| = 2 (simple swap). More complex bijections (3-cycles, multi-position permutations) are mechanically handled by the same framework but aren't worked. This is acceptable example coverage; demanding all cases be worked would be excessive.

### Topic 2: Concrete worked example for orphan link state
**Why out of scope**: Orphan links (K.λ without K.μ⁺_L) are discussed in prose under "Orphan links and coupling flexibility" but not given a worked trace. The single-operation case is simple enough that prose suffices.

### Topic 3: Behavior under concurrent transitions
**Why out of scope**: SequentialTransitionAxiom rules out concurrency by design; concurrent operation semantics belong to a future ASN (listed in Open Questions).

### Topic 4: Mechanism for interior link withdrawal
**Why out of scope**: Listed in Open Questions. D-CTG★ forces suffix-only link contraction; interior withdrawal requires a separate mechanism (status flag, tombstone) outside this ASN's scope.

VERDICT: REVISE
