# ASN-0100: INSERT Operation

*2026-05-27*

## The Question

When new content is inserted at a position in a document's Vstream, what is the precise post-state? Three sub-questions structure the inquiry:

- *What is allocated* — what new state appears in the content store and in the document's arrangement?
- *What shifts* — which existing V→I mappings change position, and by how much?
- *What invariants must hold after completion* — and atomically, with no observable intermediate state in which some invariant is violated?

The answer must be sharp enough that an implementation can be measured against it, and abstract enough that two implementations meeting the spec are externally indistinguishable.

## Background: The Two-Stream Asymmetry

The foundation distinguishes two address spaces. The content store `C : T ⇀ Val` assigns content values to I-addresses; once `a ∈ dom(C)`, the binding is permanently fixed (S0). The arrangement `M(d) : T ⇀ T` assigns I-addresses to V-positions within document `d`; arrangements are mutable, but only in a controlled way.

INSERT acts on both, but asymmetrically. It *grows* `C` by appending fresh entries; it never alters existing entries, never reassigns I-addresses, never identifies one I-address with another. It *grows and rearranges* `M(d)`; it never alters the underlying I-addresses, only the V-positions at which they are observed.

This asymmetry is the architectural pivot. Existing content keeps its permanent I-address across INSERT. Its V-position within `d` may shift, but the I-address — and the value stored there — is invariant. Since links attach to I-addresses (not V-positions), insertion cannot break them. The I-address is the *identity* of a piece of content; the V-position is the *current location* of that identity within an arrangement.

We shall see that every constraint on INSERT — what may shift, what must be preserved, what counts as atomic — flows from this single asymmetry.

## The Operation's Inputs

INSERT takes three arguments: a target document `d ∈ dom(M)`, a V-position `p` at which the insertion begins, and a sequence of new content values `⟨v₀, v₁, …, v_{n−1}⟩` with `n ≥ 1`.

We restrict attention to the *content subspace* `s_C` of `d` — Nelson's text content. (The link subspace `s_L` is governed by a structurally similar but distinct extension operation; the present analysis does not cover it.)

The position `p` must be a *valid insertion position* in `V_{s_C}(d)`. We unpack this:

  `subspace(p) = s_C ∧ #p = m_C`

where `m_C` is the common depth of `V_{s_C}(d)` enforced by S8-depth (FixedDepthVPositions, ASN-0036) on the text subspace. For non-empty `V_{s_C}(d)` with current cardinality `N = |V_{s_C}(d)|`, the precondition is the binary predicate `ValidInsertionPosition(d, p)` (ASN-0036), which unpacks to:

  `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ N}`

reading `shift(t, 0) = t` per the OrdinalShiftBase convention of ASN-0058. This yields `N + 1` admissible positions: `j = 0` inserts before the first character, `j = N` after the last, and `j ∈ {1, …, N−1}` in the interior.

For empty `V_{s_C}(d)`, the precondition is the ternary predicate `ValidFirstInsertionPosition(d, p, m)` (ASN-0036): the caller chooses a depth `m ≥ 2` and the single admissible position is `[s_C, 1, …, 1]` of length `m`. The post-state has `V_{s_C}(d') ≠ ∅`, at which point S8-depth fixes `m_C = m` permanently for that document — every subsequent text-subspace position in `d` must have depth `m`, since S8-depth is a per-state invariant under ValidComposite★ (ASN-0047).

The condition `n ≥ 1` rules out a degenerate empty-insertion case. The values `v_k` must be elements of the content type `Val`; the abstract specification places no further constraint on their structure.

These preconditions are necessary; we shall verify they are jointly sufficient.

## Discovering the Three Effects

We reason from the intent backward to the formal specification. INSERT splices `n` new content units into `d`'s arrangement at V-position `p`. Three effects must obtain together.

### Effect One: Allocation

The new content units do not exist in `dom(C)` before the operation. Nelson is unambiguous (Q1, Q5, Q8): INSERT creates *new* content with *fresh* I-addresses. The operation does not reuse, alias, or identify with any pre-existing I-address.

The freshness comes from `d`'s content sub-allocator `A_C(d)`, by the substrate's allocation discipline (ASN-0093). We require `n` addresses, produced by `n` successive K.α firings under the substrate's transition vocabulary:

  `a_k = A_C(d)`'s `k`-th emission across the composite, for `0 ≤ k < n`

The freshness of each `a_k` is established against the state immediately preceding its K.α firing — not against the operation's pre-state Σ. Concretely, if Σ_k denotes the substrate state after K.α has fired for `a_0, …, a_{k−1}`, then K.α's precondition requires `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)`. This holds by ChainEnumerationInjectivity (ASN-0093), which makes the chain enumeration `n ↦ t_n` injective: `a_k = t_{m_d + k + 1}` (where `m_d` is the chain index of the last emission already in `dom(Σ.C)` for origin `d`, or 0 if none), and the new index `m_d + k + 1` is strictly greater than every prior index, so `a_k` is distinct from `a_0, …, a_{k−1}` and from every pre-existing chain emission. Combined with FirstEmissionFreshness (ASN-0093) for the boundary case `m_d = 0`, each K.α firing satisfies its own freshness precondition.

By the chain discipline (ChainPrefixExtension, ChainEnumerationInjectivity; ASN-0093), every `a_k` has `origin(a_k) = d`, satisfies `b_C(d) ≼ a_k` (extending the content sub-allocator anchor), and is structurally produced by the sub-allocator's `inc(·, 0)` chain. The addresses `a_0, a_1, …, a_{n−1}` form a contiguous initial-segment extension of the chain: `a_{k+1} = inc(a_k, 0)` for `0 ≤ k < n − 1`, and `a_0` is either `[d.0.s_C.1]` (if `d` had no prior content emissions, per K.α's first-emission predicate in ASN-0093) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(Σ.C) : origin(a) = d}` (per K.α's subsequent-emission predicate in ASN-0093).

The post-state content store:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `C'(a_k) = v_k` for `0 ≤ k < n`
  `C'(a) = C(a)` for `a ∈ dom(C)`

The third clause is the most important. The pre-existing content is *not touched*. Its values are preserved bit-for-bit; its addresses persist in the post-state. This is the foundational permanence guarantee S0.

### Effect Two: Placement

The new I-addresses must appear at V-positions `p, shift(p, 1), …, shift(p, n−1)`. Reading `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058), the mapping is exact:

  `(A k : 0 ≤ k < n : M'(d)(shift(p, k)) = a_k)`

By OrdAddHom clause (b) (ASN-0036) applied to `w = δ(k, m_C)`, every `shift(p, k)` for `k ≥ 1` lies in the same subspace as `p`: `subspace(shift(p, k)) = s_C`. The result-length identity of TumblerAdd (ASN-0034) gives `#shift(p, k) = m_C`. For `k = 0`, `shift(p, 0) = p` shares subspace and depth with `p` trivially. Each `shift(p, k)` satisfies S8a (VPositionWellFormedness, ASN-0036): zero-free, depth `≥ 2`, all components positive (since `p` satisfies S8a by virtue of `p ∈ V_{s_C}(d) ∪ {[s_C, 1, …, 1]}` and the shift's tail component `p_{m_C} + k ≥ 1`). The new V-positions are well-formed inhabitants of `V_{s_C}(d')`.

### Effect Three: Shift

Every existing V-position `v ∈ V_{s_C}(d)` with `v ≥ p` must remap. The content there does not change — it keeps its I-address — but its V-position advances by `n`:

  `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

This clause is exactly the I3 postcondition (PostInsertionShift) of ASN-0082, instantiated for the text subspace `S = s_C` of `d`. The right region is the source of the shift; the shifted-right region is its image. The two are related by the order-preserving (TS1, ShiftOrderPreservation; ASN-0034) and injective (TS2, ShiftInjectivity; ASN-0034) shift map. The image of the shift map is exactly `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N}` when we write `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`.

For positions `v ∈ V_{s_C}(d)` with `v < p` (the left region), the arrangement is unchanged (I3-L, PostInsertionLeftFrame; ASN-0082).

For positions in subspaces other than `s_C` — including the link subspace — the arrangement is unchanged (I3-X, PostInsertionCrossSubspaceFrame; ASN-0082).

For other documents `d' ≠ d`, the arrangement is unchanged (I3-D, PostInsertionCrossDocumentFrame; ASN-0082).

The content store is unchanged outside the freshly allocated addresses (I3-C, PostInsertionContentFrame; ASN-0082).

These exhaust the cases.

## The Operation: Formal Contract

INSERT is a **substrate composite** in the sense of ValidComposite★ (ASN-0047) — a finite sequence of elementary transitions drawn from the substrate's K-vocabulary, governed at the composite boundary by the coupling constraints J0, J1★, J1'★. It is *not* a new elementary primitive; the substrate transition vocabulary is not amended.

We state INSERT as a composite `Σ →* Σ'`.

**Operation:** `INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)`

**Substrate Decomposition.** INSERT realises as the following sequence of elementary transitions, in order:

1. **`n` successive K.α firings** allocating fresh content addresses `a_0, a_1, …, a_{n−1}` from `A_C(d)`. Each K.α firing satisfies its freshness precondition against the intermediate state immediately preceding it (justified by ChainEnumerationInjectivity; ASN-0093 — see Effect One above).
2. **One K.μ⁻ on `d`** retaining the Left prefix of `V_{s_C}(d)` (with `n'_{s_C} = p_m − 1`) and retaining all of `V_{s_L}(d)` (with `n'_{s_L} = n_{s_L}`). *Omitted in two cases:* (i) when the pre-state `V_{s_C}(d) = ∅` (nothing to retain or shrink); (ii) when `p_m = N + 1` (append case — Left = entire pre-state `V_{s_C}(d)`, so no strict shrinkage of `V_{s_C}(d)` is required, and K.μ⁻'s precondition `(E S :: n'_S < n_S)` cannot be satisfied without affecting `V_{s_L}(d)`).
3. **One K.μ⁺ on `d`** adding the Insertion V-positions (mapping `shift(p, k) ↦ a_k` for `0 ≤ k < n`) and the Shifted-right V-positions (mapping `shift(v, n) ↦ M(d)(v)` for each `v ∈ V_{s_C}(d)` with `v ≥ p`). All additions are in subspace `s_C`, as required by K.μ⁺'s content-subspace restriction (ASN-0047).
4. **`n` successive K.ρ firings** recording provenance pairs `(a_k, d)` for `0 ≤ k < n`.

Each intermediate state in this sequence satisfies the per-state invariants (Class (a) of ASN-0047); the composite-boundary properties (Class (b): P4★, P4a, P7a) are discharged at the boundary `Σ →* Σ'` by the constraints J0, J1★, J1'★.

**Preconditions** (evaluated against the operation's pre-state Σ):
- `d ∈ dom(M)` (so K.α, K.μ⁺, K.ρ all have their `d ∈ E_doc` precondition met; K.μ⁻ when fired further requires `dom(M(d)) ≠ ∅`, satisfied in cases that invoke it)
- `subspace(p) = s_C`
- `#p = m_C` (the common depth of `V_{s_C}(d)` if non-empty per S8-depth, ASN-0036; the caller's chosen depth `m ≥ 2` if empty)
- `p` is a valid insertion position: either `ValidInsertionPosition(d, p)` (ASN-0036) for non-empty `V_{s_C}(d)` — equivalently `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ |V_{s_C}(d)|}` reading `shift(t, 0) = t` per OrdinalShiftBase (ASN-0058) — or `ValidFirstInsertionPosition(d, p, m)` (ASN-0036) for empty `V_{s_C}(d)`, equivalently `p = [s_C, 1, …, 1]` of depth `m`
- `n ≥ 1`
- `v_k ∈ Val` for each `0 ≤ k < n`

**Effect — Content Store:**
Let `a_0, a_1, …, a_{n−1}` denote the `n` successive emissions of `A_C(d)` produced by the K.α firings of step 1. Then:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `(A k : 0 ≤ k < n : C'(a_k) = v_k)`
  `(A a : a ∈ dom(C) : C'(a) = C(a))`

**Effect — Arrangement of `d`, text subspace:**
Three disjoint regions:

  *Left* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

  *Insertion* — `(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)` — reading `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058).

  *Shifted right* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

The post-state's text-subspace domain is exactly the union: `V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions.

**Effect — Provenance:**

  `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`

The composite-boundary coupling J1★ (ExtensionRecordsProvenanceContentSubspace; ASN-0047) requires every newly-arranged content-subspace I-address to have its provenance pair in `R'`. For Insertion positions, the K.α-allocated `a_k` is freshly placed and was not previously in `ran(M(d))`, so J1★ requires `(a_k, d) ∈ R'` — discharged by step 4. For Shifted-right positions, `M(d)(v) = a` was already in `ran(M(d))` at the pre-state, so J1★ imposes no obligation. Conversely, J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047) requires every new `R'` entry to correspond to a newly-arranged content-subspace I-address — discharged because each `(a_k, d)` is added in step 4 precisely as `a_k` is placed by step 3's K.μ⁺ at a content-subspace V-position. J0 (AllocationRequiresPlacement; ASN-0047) requires every newly allocated `a_k ∈ dom(C') \ dom(C)` to be placed in some `M'(d')`'s range — discharged by step 3's K.μ⁺ placing each `a_k` at `shift(p, k)`.

**Frame Conditions:**
- `L' = L`. The link store is unchanged: no K.λ fires in the decomposition, so `dom(L)` and every link value persist by L12 (LinkImmutability; ASN-0093).
- `E' = E`. The entity set is unchanged: no K.δ or K.σ fires in the decomposition (`dom(M)` is governed via K.δ-IsDocument or K.σ for document registration; INSERT registers no new document and creates no new node, account, or non-document entity).
- `dom(M') = dom(M)`. As a specialisation of `E' = E` for the document subset: no new document is registered.
- `(A d' : d' ∈ dom(M) ∧ d' ≠ d : M'(d') = M(d'))`. Other documents' arrangements are unchanged (K.α, K.μ⁻, K.μ⁺, K.ρ all carry `(A d' : d' ≠ d :: M'(d') = M(d'))` as their explicit per-step frame in ASN-0047).
- `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`. Other subspaces of `d` — in particular `V_{s_L}(d)` — are unchanged. Step 2's K.μ⁻ (when fired) preserves the link subspace by `n'_{s_L} = n_{s_L}`; step 3's K.μ⁺ adds only content-subspace V-positions (per the K.μ⁺ amendment in ASN-0047).

## A Worked Example

We instantiate INSERT to make the three regions concrete.

**Interior insertion.** Let `d` be a document with `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4], [1,5]}` (so `m_C = 2`, `N = 5`), with arrangement:

  `M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃, [1,4] ↦ a₄, [1,5] ↦ a₅}`

Invoke `INSERT(d, [1,3], ⟨v₀, v₁⟩)` with `n = 2`. The position `p = [1,3]` corresponds to `j = 2` (since `shift([1,1], 2) = [1,3]`), interior to the `N + 1 = 6` valid positions. The substrate composite fires:

1. **Two K.α firings.** A_C(d) emits `a_{new0}` and `a_{new1} = inc(a_{new0}, 0)`, both fresh.
2. **K.μ⁻ on `d`** retains the Left prefix `V_{s_C}(d)` with `n'_{s_C} = 2`: post-step the text-subspace is `{[1,1], [1,2]}`. Link subspace retained at `n'_{s_L} = n_{s_L}`.
3. **K.μ⁺ on `d`** adds five V-positions: `[1,3] ↦ a_{new0}` and `[1,4] ↦ a_{new1}` (Insertion), and `[1,5] ↦ a₃`, `[1,6] ↦ a₄`, `[1,7] ↦ a₅` (Shifted right).
4. **Two K.ρ firings** record `(a_{new0}, d)` and `(a_{new1}, d)` in R.

The post-state arrangement:

  `M'(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}, [1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}`

Verifying the three regions:
- *Left:* `{[1,1] ↦ a₁, [1,2] ↦ a₂}` — matches `{v < p}` via INS.M-left.
- *Insertion:* `{[1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}}` — matches `shift(p, k) ↦ a_k` for `k ∈ {0, 1}` via INS.M-insert; note `shift([1,3], 0) = [1,3]` by OrdinalShiftBase.
- *Shifted right:* `{[1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}` — matches `shift(v, 2) ↦ M(d)(v)` for `v ∈ {[1,3], [1,4], [1,5]}` via INS.M-shift.

The last-component values in `V_{s_C}(d')` are `{1, 2, 3, 4, 5, 6, 7}` — sequential, contiguous, starting at 1, satisfying INS.inv.seq with new cardinality `N + n = 7`.

**Append case (`j = N = 5`).** With the same pre-state, `INSERT(d, [1,6], ⟨v₀⟩)` (where `[1,6] = shift([1,1], 5)` is one past the last position). The Right region is empty; no K.μ⁻ fires (Left = entire `V_{s_C}(d)`). Composite: one K.α + one K.μ⁺ adding `[1,6] ↦ a_{new0}` only + one K.ρ. Post-state `V_{s_C}(d') = {[1,1], …, [1,6]}` with `a₁, …, a₅, a_{new0}` as images.

**Empty-document first insertion.** Let `d` have `V_{s_C}(d) = ∅`. Invoke `INSERT(d, [1,1], ⟨v₀, v₁, v₂⟩)` with `m = 2` (caller-chosen depth). No K.μ⁻ fires (nothing to retain). Composite: three K.α + one K.μ⁺ adding `[1,1] ↦ a_{new0}, [1,2] ↦ a_{new1}, [1,3] ↦ a_{new2}` + three K.ρ. Post-state `V_{s_C}(d') = {[1,1], [1,2], [1,3]}` with `m_C = 2` fixed permanently for `d` by S8-depth (ASN-0036).

## Verifying the Invariants

The post-state Σ' must satisfy every system invariant. We verify the principal ones.

### Permanence of existing content (S0, P0)

The content-store effect's third clause asserts `(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`. This is S0 (ContentImmutability; ASN-0036), strengthened by P0 (ContentPermanence; ASN-0047), verbatim. The first clause `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` adds new addresses without removing any; the new addresses are fresh by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093), so no overwrite occurs. Store monotonicity `dom(C) ⊆ dom(C')` follows.

Each per-step K.α firing preserves S0 by its own frame (its effect adds a new binding without modifying existing ones); K.μ⁻, K.μ⁺, K.ρ have frame `C' = C` and so preserve S0 trivially. The composite preserves S0 by composition.

The consequence Nelson emphasises (Q5): a reader holding any pre-state I-address `a ∈ dom(C)` retrieves the same value `C'(a) = C(a)` from the post-state. The reader needs no knowledge of where in any document's Vstream that content now lies.

### Cross-document independence (Q3)

The frame `(A d' : d' ≠ d : M'(d') = M(d'))` directly enforces independence: no document other than `d` has its arrangement altered. Coupled with `L' = L` and content-store preservation, this means that any document `d'` that transcludes content from `d` continues to map the same V-positions to the same I-addresses, and those I-addresses continue to resolve to the same values.

The two documents may share I-addresses through transclusion, but the cross-document frame and content preservation together ensure that the shared I-addresses' values and the *other* document's mappings are unaffected.

### Arrangement functionality (S2)

We verify that `M'(d)` is a function (S2, ArrangementFunctionality; ASN-0036): no V-position has two distinct image I-addresses.

The Left, Insertion, and Shifted-right regions are pairwise disjoint as sets of V-positions. Writing `p = [s_C, 1, …, 1, p_m]`:

- *Left ∩ Insertion = ∅.* Left positions have last component `< p_m`; Insertion positions have last component in `{p_m, p_m + 1, …, p_m + n − 1}` (by shift's last-component arithmetic per OrdAddHom and ShiftPreservation, ASN-0036).

- *Insertion ∩ Shifted-right = ∅.* Insertion positions have last component in `{p_m, …, p_m + n − 1}`. Shifted-right positions image `v` with last component `≥ p_m` to a position with last component `≥ p_m + n` (by TS4, ShiftStrictIncrease; ASN-0034). Hence Shifted-right positions have last component `≥ p_m + n`, strictly greater than Insertion positions.

- *Left ∩ Shifted-right = ∅.* Left last components are `< p_m`; Shifted-right last components are `≥ p_m + n ≥ p_m + 1`.

Within each region the mapping is uniquely defined: Left and Shifted-right by `M(d)` applied to a unique source position — for Shifted-right, source uniqueness follows from TS2 (ShiftInjectivity; ASN-0034): distinct sources `v₁ ≠ v₂` yield `shift(v₁, n) ≠ shift(v₂, n)`. Insertion images are uniquely indexed by `k`. So `M'(d)` is a well-defined function.

This conclusion is also discharged transitively by I3-S2 (PostInsertionFunctionality; ASN-0082), which establishes functionality of the post-state arrangement under the same shift discipline. For other subspaces and other documents, `M'` equals `M`, which is already a function by the pre-state S2.

### Referential integrity (S3★)

We verify the generalised content-and-link form S3★ (GeneralizedReferentialIntegrity; ASN-0047): `(A v ∈ dom(M'(d)) : (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`.

For Left and Shifted-right content-subspace positions: the image is `M(d)(v')` for some pre-state position `v' ∈ dom(M(d))` with `subspace(v') = s_C`, so by pre-state S3★ the image lies in `dom(C)`, and by P0 (ContentPermanence; ASN-0047) `dom(C) ⊆ dom(C')`.

For Insertion positions: the image is `a_k ∈ dom(C')` by the content-store effect.

For positions in subspaces other than `s_C` of `d` (notably `s_L`), and for positions in other documents: unchanged by frame; S3★ follows from the pre-state combined with link-store immutability `L' = L`.

This conclusion is also discharged by I3-S3 (PostInsertionReferentialIntegrity; ASN-0082).

### Sequential text-subspace structure (D-CTG★, D-MIN★, D-SEQ★)

We verify the per-subspace forms D-CTG★ (PerSubspaceContiguity), D-MIN★ (PerSubspaceMinimumPosition), and D-SEQ★ (PerSubspaceSequentialPositions) from ASN-0047 for the text subspace `s_C` of `d` post-state.

Suppose `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` with `N ≥ 1` (by pre-state D-SEQ★), and `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`. Then:

- Left positions: `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}` — empty if `p_m = 1`.
- Insertion positions: `{[s_C, 1, …, 1, p_m + j] : 0 ≤ j < n} = {[s_C, 1, …, 1, k] : p_m ≤ k < p_m + n}`.
- Shifted-right positions: `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N} = {[s_C, 1, …, 1, k] : p_m + n ≤ k ≤ N + n}` — empty if `p_m = N + 1`.

Their union is `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, which is exactly the sequential structure required by D-SEQ★ with new cardinality `N + n`. The minimum `[s_C, 1, …, 1]` is in the union, so D-MIN★ holds. The integer range `{1, …, N + n}` of last-component values is contiguous, so D-CTG★ holds.

For the empty pre-state case (`V_{s_C}(d) = ∅`) with `p = [s_C, 1, …, 1]` of depth `m`: post-state `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}`, satisfying all three predicates with `m_C := m`. From this point onward, S8-depth (FixedDepthVPositions; ASN-0036) — a per-state invariant — fixes the text-subspace depth at `m` for all subsequent transitions on `d`.

### Cross-subspace isolation

The frame `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` directly preserves all subspaces of `d` other than the text subspace. In particular, `V_{s_L}(d') = V_{s_L}(d)`, and link-subspace mappings are unchanged.

The isolation has a structural foundation independent of the explicit frame. The shift operation `shift(v, n) = v ⊕ δ(n, #v)` modifies only the last component of `v` at depth `m_C`. Even if it were applied to a position in `V_{s_L}(d)`, by OrdAddHom (b clause) the subspace identifier — the first component — would be preserved; the position would not migrate to the text subspace. But INSERT never applies shift to non-text positions in the first place. The subspace identifier is part of the V-position's structure, and INSERT's shift is scoped strictly to `s_C`.

Gregory's implementation realises this isolation via a two-blade "knife" whose blades bracket the text subspace; link-subspace crums are classified as outside the shift region and are uniformly left untouched. The structural property is what we verify abstractly; the knife is one (efficient) implementation.

### Link store unchanged (L12, L0, L1, L3)

`L' = L` directly preserves every link's address and value. Every `ℓ ∈ dom(L)` has `L'(ℓ) = L(ℓ)` — endsets are pointwise preserved. The subspace partition L0, the element-level structure L1, and the N-endset structure L3 are all properties of `L` alone and so hold of `L'` trivially.

### Coverage and link discoverability

For every link `ℓ ∈ dom(L)` and every slot `i`, the endset `Σ.L(ℓ).e_i` is a set of spans. Each span `(s, ℓ_w)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ_w}` — a purely combinatorial property of the span representation, consulting no state component (definition of `coverage` in ASN-0098). Since `L' = L`, every link value is unchanged at every slot, so coverage is unchanged: by LP3★ (MultiStepCoverageInvariance; ASN-0098), `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` for every link and every slot. (LP3★ extends to multi-step compositions, so it discharges the property across the substrate composite, not just per-step.)

**Projection-shift correspondence (postcondition).** For every link `ℓ ∈ dom(L)`, slot `i`, and document `d' ∈ dom(M)`:

  `project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}`

where:
- *For `d' ≠ d`:* `π` is the identity and `N_{ℓ,i} = ∅`, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)` — by frame `M'(d') = M(d')` together with LP4 (ArrangementSpecificity; ASN-0098) and LP5 (CrossDocumentIndependence; ASN-0098).
- *For `d' = d`, link subspace:* the link-subspace contribution is unchanged (frame), so `π` is the identity on link-subspace contributions and `N_{ℓ,i}` contributes none.
- *For `d' = d`, text subspace:* `π` is the *region-aware shift map* — identity on the Left region (`v < p`) and `shift(·, n)` on the Right region (`v ≥ p`); `N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n}` is the set of newly placed V-positions in `V_{s_C}(d')` whose image `a_k` happens to lie in `coverage(Σ'.L(ℓ).e_i)`.

The derivation: by INS.M-left every Left pre-state mapping `v → M(d)(v)` re-appears at the same V-position with the same I-address, so `v ∈ project(·, ·, d, Σ) ⟺ v ∈ project(·, ·, d, Σ')` for Left positions. By INS.M-shift every Right pre-state mapping `v → M(d)(v)` re-appears at `shift(v, n) → M(d)(v)`, so `v ∈ project(·, ·, d, Σ) ⟺ shift(v, n) ∈ project(·, ·, d, Σ')` for Right positions. By INS.M-insert the new Insertion V-positions map to fresh `a_k`, which contribute to the projection precisely when `a_k ∈ coverage(Σ'.L(ℓ).e_i)`. The three contributions partition the post-state projection.

LP9 (ExtensionMonotonicity; ASN-0098) gives the per-step characterisation of K.μ⁺'s contribution to projection growth; the composite's projection-shift correspondence is the combined Left-fixed + Right-shifted form, accounting also for K.μ⁻'s temporary retraction of the Right region within the composite's interior (which LP10, ContractionMonotonicity; ASN-0098, governs per-step but cancels against K.μ⁺'s re-introduction at the composite boundary).

*Consequence — preservation of pre-state discoverability:*

  `discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ')`

Every pre-state V-position contributing to projection is mapped (by π or identity) to a post-state V-position with the same I-address, so the non-emptiness of any pre-state projection slot transfers to the post-state.

*Consequence — fresh-address discoverability (the `N_{ℓ,i}` term):* A fresh `a_k` lies in `coverage(Σ'.L(ℓ).e_i)` only if the endset includes `a_k` in its span coverage. For *tight* endsets — those bounded to address ranges already populated at the time the endset was incorporated — this cannot happen: by LP19a (TightFreshness; ASN-0098), the freshness of `a_k` against the endset's incorporation state places it outside the tight coverage, so `N_{ℓ,i} = ∅`. For non-tight endsets, a fresh `a_k` may indeed land in coverage, and this is by intent: non-tight endsets are designed to capture later-allocated content within their declared range. LP19 (TightEndsetBoundaryExclusion; ASN-0098) specialises this to K.μ⁺ steps of the composite: V-positions newly added by K.μ⁺ whose image was freshly allocated by a prior K.α step of the composite are excluded from any pre-existing tight endset's projection.

### Provenance (R, P4★, P4a, P7a)

The provenance relation `R ⊆ T_elem × E_doc` (ASN-0047) records which documents have ever contained which I-addresses. INSERT's effect on R is `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`, realised by `n` K.ρ firings in step 4 of the substrate composite.

The composite-boundary coupling J1★ (ExtensionRecordsProvenanceContentSubspace; ASN-0047) requires every newly-arranged content-subspace I-address with no pre-state arrangement under `d` to have its provenance pair in `R'`. For Insertion positions, the freshly allocated `a_k` was not in any `ran(M(d))` pre-state (by FirstEmissionFreshness; ASN-0093), so J1★ requires `(a_k, d) ∈ R'` — discharged by step 4. For Shifted-right positions, `M(d)(v) = a` was already arranged at some content-subspace V-position `v ∈ dom(M(d))`, so J1★'s requirement of "not previously arranged in d's content subspace" is false, and no new R entry is required for these. The pair `(a, d)` was already in R via the historical state (preserved by P2, ProvenancePermanence; ASN-0047).

J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047) requires every new R' entry to correspond to a newly-arranged content-subspace I-address. Each `(a_k, d)` added in step 4 corresponds to the placement `shift(p, k) ↦ a_k` introduced by step 3's K.μ⁺ — satisfied.

P4★ (ProvenanceBoundsContentSubspace; ASN-0047): `Contains_C(Σ') ⊆ R'`. Pre-state P4★ gives `Contains_C(Σ) ⊆ R`. The post-state's content-subspace arrangement adds n new pairs (one per Insertion position with image `a_k`); each is in R' via step 4. So P4★ holds.

P4a (HistoricalFidelity; ASN-0047): every `(a, d) ∈ R'` has a historical state in which `a` was in d's content-subspace range. For pre-state `(a, d) ∈ R`, P4a inherits. For each new `(a_k, d)` added in step 4, the historical state is the substrate state at the end of step 3, in which `a_k ∈ ran(M'(d))` at the Insertion position.

P7a (ProvenanceCoverage; ASN-0047): every `a ∈ dom(C')` has some `d` with `(a, d) ∈ R'`. Pre-state P7a covers `dom(C)`; each new `a_k ∈ dom(C') \ dom(C)` is paired with `d` in step 4.

### What is *not* allocated

INSERT does *not* allocate new documents (`dom(M') = dom(M)`), does *not* allocate new links (`L' = L`), and does *not* allocate I-addresses outside `dom(C)`'s content subspace (every `a_k` has `subspace_I(a_k) = s_C`). The allocation footprint is precisely `n` content-subspace I-addresses scoped to `d`.

## Atomicity and Canonical Order

Nelson requires that after INSERT, the system is in "canonical order" — every structural invariant holds simultaneously. INSERT is a substrate composite governed by ValidComposite★ (ASN-0047), and its atomicity is the *composite-boundary* form: per-state invariants (Class (a) of ASN-0047 — S2, S3★, S8-depth, S8a, D-CTG★, D-MIN★, D-SEQ★, L0, L12, L14, …) hold at *every* state including each intermediate within the composite; composite-boundary properties (Class (b) — P4★, P4a, P7a) and the coupling constraints (J0, J1★, J1'★) hold at the boundary between Σ and Σ'.

We verify that each intermediate state in INSERT's substrate decomposition satisfies the per-state invariants.

- *After each of the `n` K.α firings of step 1.* `dom(C)` extends by one fresh `a_k` with `origin(a_k) = d`; `M(d)` is unchanged. Per-state invariants on M (S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, D-SEQ★) hold trivially because M is unchanged; per-state invariants on C (C-fin, S7a, S7b, S7c) hold because each `a_k` is a well-formed content-subspace address with `zeros(a_k) = 3` and `#E(a_k) ≥ 2`, satisfying the per-address conditions. L14 holds because `a_k ∉ dom(L)` (K.α's freshness precondition). The composite-boundary properties (J0, J1★, P4★) are not yet required to hold at this intermediate — `a_k` is in `dom(C)` but not yet placed, which J0 would forbid at a composite boundary, but the intermediate is interior to the composite.

- *After step 2's K.μ⁻ (when fired).* `V_{s_C}(d_intermediate)` reduces to the Left prefix `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}`, which is sequential, contiguous, and starts at the minimum — D-SEQ★, D-CTG★, D-MIN★ all hold. S3★ holds because retained images are unchanged. The link subspace is unchanged. P4★ (composite-boundary) would not hold at this intermediate if it required all post-state ran(M(d)) entries to be in R — but R has not yet been extended; the obligation is delegated to the composite boundary.

- *After step 3's K.μ⁺.* `V_{s_C}(d_intermediate)` extends to the full post-state `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, satisfying D-SEQ★, D-CTG★, D-MIN★. Every newly arranged content-subspace I-address is in `dom(C)` already (the freshly allocated `a_k` from step 1, or the pre-existing M(d)(v) for Shifted-right) — S3★ holds. J0 (composite-boundary) is now satisfied: each `a_k ∈ dom(C')` has a placement at `shift(p, k)`.

- *After each of the `n` K.ρ firings of step 4.* R extends by one `(a_k, d)` pair. The composite-boundary coupling J1★ requires every newly-arranged content-subspace I-address to be in R'; after all `n` firings, J1★ holds. P4★ (`Contains_C(Σ') ⊆ R'`) holds because every content-subspace range entry of M'(d) is either a pre-state entry (already in R via pre-state P4★) or an Insertion-region freshly allocated `a_k` (now in R via step 4). P4a (HistoricalFidelity) holds because each `(a_k, d) ∈ R'` corresponds to the substrate state at the end of step 3 where `a_k ∈ ran(M'(d))`.

The decomposition is admissible under ValidComposite★ because (i) every elementary transition's per-step precondition is met at its intermediate state, and (ii) the composite-boundary coupling constraints J0, J1★, J1'★ hold at the boundary `Σ →* Σ'`.

The composite is *not* admissible in alternative decompositions that would break a per-state invariant at an intermediate:

- *K.μ⁺ before K.α* (place `a_k` before allocating it). K.μ⁺'s precondition requires `a ∈ dom(C)` for every new mapping. The intermediate before K.α has `a_k ∉ dom(C)`, so K.μ⁺ cannot fire — the decomposition is ill-typed.

- *K.μ⁺ without prior K.μ⁻ in an interior insertion.* K.μ⁺ extends `dom(M(d))`; it preserves existing mappings. To map both `[s_C, 1, …, 1, p_m]` to `M(d)([s_C, 1, …, 1, p_m])` (the original content) and to `a_0` (the new content) would violate S2 — per-state functionality. So shift via K.μ⁻ + K.μ⁺ is *required*, not an implementation choice.

- *K.μ⁻ retaining strictly less than the Left prefix.* This would shrink `V_{s_C}(d_intermediate)` further than needed; the subsequent K.μ⁺ would have to re-add positions in the middle of the Left region (between `[s_C, 1, …, 1, k]` and `[s_C, 1, …, 1, k+1]`), but K.μ⁺'s constraints D-CTG★, D-MIN★ force any new V-position in `V_{s_C}(d)` to extend the existing sequential run at its high end. The interior gap cannot be filled by K.μ⁺.

Each ruled-out decomposition is either ill-typed (precondition violated) or per-state-invariant-violating. The substrate decomposition above is the unique well-typed sequence, modulo the ordering of independent K.α and K.ρ firings (which commute among themselves but not with K.μ⁺ and K.μ⁻).

This is what Nelson calls "all changes, once made, leave the file remaining in canonical order, which was an internal mandate of the system." Implementations realise the composite via transactional sequencing, locking, copy-on-write, or log-and-commit — but the choice is below the level of abstraction at which INSERT is specified. External observers see the composite boundary; the intermediate states are not externally observable. By the SequentialTransitionAxiom of ASN-0093, no other composite can interleave between Σ and Σ'.

## Position Constraints

We claim INSERT is permitted at any valid insertion position — beginning, middle, end, and on the first insertion into an empty document. The empty and non-empty cases use *different* precondition predicates with different operational characters.

**Non-empty case (predicate `ValidInsertionPosition(d, p)`, ASN-0036).** For non-empty `V_{s_C}(d)` with cardinality `N`, the `N + 1` valid positions correspond to:

- `j = 0`: insertion at the very beginning. Left is empty (no `v < p`); the entire pre-state text subspace shifts by `n`. K.μ⁻ in the composite shrinks `V_{s_C}(d)` to `∅` (`n'_{s_C} = 0`); K.μ⁺ re-adds Insertion + Shifted-right at the original positions advanced by `n`.
- `j = N`: insertion at the end (append). Shifted-right is empty (no `v ≥ p`, since `p = shift(min, N)` and `max(V_{s_C}(d)) = shift(min, N−1) < p`); no shift occurs. K.μ⁻ is *omitted* from the composite (no strict shrinkage required); K.μ⁺ adds only the Insertion positions at the high end of the existing sequence.
- `j ∈ {1, …, N−1}`: interior insertion. Both Left and Shifted-right are non-empty; both are realised through K.μ⁻ (retaining Left) + K.μ⁺ (adding Insertion + Shifted-right).

The non-empty case's depth parameter is fixed by S8-depth (ASN-0036): `m_C` is the common depth of the pre-state `V_{s_C}(d)`, and the caller cannot choose otherwise.

**Empty case (predicate `ValidFirstInsertionPosition(d, p, m)`, ASN-0036).** For empty `V_{s_C}(d)`, the unique valid position is `[s_C, 1, …, 1]` of caller-chosen depth `m ≥ 2`. This case has operationally distinct features from the non-empty case:

- The precondition is the *ternary* predicate `ValidFirstInsertionPosition(d, p, m)`, which takes `m` as a third argument (the chosen depth), versus the *binary* `ValidInsertionPosition(d, p)`.
- The depth `m` is an operational input chosen by the caller; the strand model fixes only the lower bound `m ≥ 2`.
- K.μ⁻ is *omitted* from the composite (pre-state has nothing to retain — `dom(M(d))` may still contain link-subspace positions, but `V_{s_C}(d) = ∅` means K.μ⁻ cannot strictly shrink the content subspace while preserving the link subspace).
- The post-state, with `V_{s_C}(d') ≠ ∅` for the first time, triggers S8-depth's enforcement of `m_C = m` for all subsequent text-subspace operations on `d`.

The two cases share the post-condition shape (Left ∪ Insertion ∪ Shifted-right partition with appropriate emptiness), but their precondition predicates and composite structures differ.

The edge cases within each case (Left empty, Shifted-right empty) require no special handling in the post-condition specification: the universal forms of the three regions handle them uniformly, with quantifier-bounded clauses vacuously satisfied when a region is empty.

The "no positional constraint" intent (Q6) is borne out: the operation is uniformly defined across the position space. The specific *append* operation Nelson lists as a separate convenience (APPEND) is the `j = N` case of INSERT — distinct in name only, since the caller does not need to know `N` if a separate API offers append directly, but identical in semantic effect.

## INSERT vs. COPY: Identity Through Allocation

Nelson (Q8) distinguishes INSERT from COPY — two operations that may produce visually identical Vstream effects but completely different Istream consequences. We address the distinction only to fix the identity character of INSERT; COPY's full operation specification is out of scope for this ASN.

INSERT allocates *fresh* I-addresses for new content. The defining clause of the content-store effect — `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` with each `a_k` fresh — is the structural guarantee that the new content is new. Each `a_k` has `origin(a_k) = d`: attribution accrues to `d`'s owner, royalties (if priced) flow to `d`'s account.

Two independent users who INSERT the word "the" into their respective documents produce two distinct addresses, two distinct origins; neither is a copy or transclusion of the other. The system tracks identity by allocation event, not by value. If their bytes happen to coincide — both authors wrote "the" — the system observes this as two unrelated allocations, not one shared content.

COPY (out of scope here) creates V→I mappings to *existing* I-addresses without allocating new content. The original document remains the home of the bytes; attribution stays with the original author. The Vstream effect can be made indistinguishable from an INSERT — the same V-positions populated with the same visible content — but the underlying Istream identity is fundamentally different.

### Derived corollaries of INS.identity

The identity-by-allocation property has explicit consequences for the system. We derive three.

*Corollary (cross-document allocation independence).* If two distinct documents `d_1 ≠ d_2` each invoke INSERT with the same value sequence `⟨v_0, …, v_{n−1}⟩` at any positions, they produce two disjoint sequences of fresh I-addresses `⟨a_0^{(1)}, …, a_{n−1}^{(1)}⟩` and `⟨a_0^{(2)}, …, a_{n−1}^{(2)}⟩` with `origin(a_k^{(1)}) = d_1 ≠ d_2 = origin(a_k^{(2)})`. The two address sets are disjoint by SubAllocatorAxiom.Disjointness (ASN-0047): `dom(A_C(d_1)) ∩ dom(A_C(d_2)) = ∅` for `d_1 ≠ d_2`. Value coincidence at `Σ.C(a_k^{(1)}) = Σ.C(a_k^{(2)})` is observable but does not produce identity — the system observes it as two unrelated allocations.

*Corollary (version chain independence).* When a version `d_v = inc(d_src, 1)` is derived from `d_src` (out of scope here, but a substrate operation under K.δ-IsDocument) and subsequently INSERT is invoked on `d_v`, the freshly allocated `a_k` come from `A_C(d_v)` with `origin(a_k) = d_v ≠ d_src`. The original `d_src` retains its allocated content unchanged; the version's new content has its own attribution. This corollary depends on the per-document sub-allocator existence guaranteed by SubAllocatorAxiom for each `d_v ∈ E_doc` (ASN-0047).

*Corollary (link survivability through value coincidence).* If a tight endset `e` was incorporated at state `Σ_e` (with `tight(e, Σ_e)`), and a subsequent INSERT in any document produces a fresh `a_new` whose value `Σ'.C(a_new) = Σ_e.C(a')` for some `a' ∈ coverage(e)`, then `a_new ∉ coverage(e)`. By LP19a (TightFreshness; ASN-0098), tight endsets cannot accidentally capture freshly allocated content — the endset's coverage is a set of I-addresses, not a set of values, and a fresh `a_new` is by construction outside `dom(Σ_e.C) ∪ dom(Σ_e.L)` and therefore outside the tight coverage. The link does not silently expand to capture the new (coincidentally identical) content.

The identity-by-allocation property of INSERT is foundational. All higher-level properties of the system — traceability of content to its author, royalty accounting, link survivability, version comparison via shared identity — depend on it. An implementation that silently de-duplicated content during INSERT (identifying identical bytes from independent allocations) would violate this property and corrupt every dependent guarantee. The specification therefore forbids it: each `a_k` is a *fresh* address, produced by `A_C(d)`'s allocator chain, with no negotiation of equivalence.

## Bounding the Scope

The specification given here is INSERT for the content subspace. It does not cover:

- Insertion into the link subspace; the foundation's `K.μ⁺_L` is a structurally different operation with its own semantics, and link allocation through `K.λ` differs from content allocation through `K.α` in the requirement of an N-endset value structure.
- COPY, which creates V→I references without content allocation. Out of scope.
- DELETE and REARRANGE; these are governed by other transitions in the substrate's vocabulary.
- Version derivation. INSERT does not create versions; a separate K.δ-style entity-creation operation handles that.
- Inter-server replication. The specification describes INSERT within a single local state; cross-server propagation is the BEBE protocol's concern.

What the specification *does* cover is the precise per-state effect of one INSERT on one document at one position, including every invariant that must continue to hold after the operation.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| INS.def | INSERT(d, p, ⟨v_0, …, v_{n−1}⟩) is a substrate composite Σ →* Σ' under ValidComposite★ (ASN-0047), realised as n K.α + (optional K.μ⁻) + K.μ⁺ + n K.ρ | introduced |
| INS.pre | INSERT preconditions: d ∈ dom(M); p valid in text subspace of d (binary predicate ValidInsertionPosition for non-empty case, ternary predicate ValidFirstInsertionPosition(d, p, m) with caller-chosen m ≥ 2 for empty case); n ≥ 1; v_k ∈ Val | introduced |
| INS.alloc | INSERT allocates exactly n fresh I-addresses from d's content sub-allocator A_C(d); each a_k satisfies origin(a_k) = d; each K.α firing satisfies its freshness precondition against its own intermediate state by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093) | introduced |
| INS.C | dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}; C'(a_k) = v_k; ∀a ∈ dom(C): C'(a) = C(a) | introduced |
| INS.M-left | Text-subspace positions v < p in dom(M(d)) appear unchanged in M'(d) | introduced |
| INS.M-insert | M'(d)(shift(p, k)) = a_k for 0 ≤ k < n, reading shift(p, 0) = p per OrdinalShiftBase (ASN-0058) | introduced |
| INS.M-shift | For v ∈ V_{s_C}(d) with v ≥ p: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v); discharged by I3 (ASN-0082) | introduced |
| INS.R | R' = R ∪ {(a_k, d) : 0 ≤ k < n}; discharges composite-boundary couplings J0, J1★, J1'★ (ASN-0047) | introduced |
| INS.frame.subspace | Non-content subspaces of d are unchanged: M'(d) agrees with M(d) on positions with subspace ≠ s_C | introduced |
| INS.frame.doc | Other documents' arrangements are unchanged: ∀d' ≠ d: M'(d') = M(d') | introduced |
| INS.frame.L | L' = L: link store entirely unchanged | introduced |
| INS.frame.E | E' = E: entity set unchanged (no K.δ or K.σ in the decomposition); specialises to dom(M') = dom(M) for documents | introduced |
| INS.frame.dom | dom(M') = dom(M): no new documents registered | introduced |
| INS.inv.immut | Content immutability S0 (ASN-0036) / P0 (ASN-0047) preserved: dom(C) ⊆ dom(C') and pointwise values preserved | introduced |
| INS.inv.identity | Permanent I-address identity preserved: ∀a ∈ dom(C): a ∈ dom(C'), C'(a) = C(a), origin(a) unchanged | introduced |
| INS.inv.func | M'(d) is a function (S2 preserved); Left, Insertion, Shifted-right regions are pairwise disjoint by TS2 and TS4 (ASN-0034) | introduced |
| INS.inv.refint | Referential integrity S3★ (ASN-0047) preserved: ran(M'(d)) ⊆ dom(C') ∪ dom(L') per-subspace; discharged also by I3-S3 (ASN-0082) | introduced |
| INS.inv.seq | D-CTG★, D-MIN★, D-SEQ★ (ASN-0047) preserved in text subspace: V_{s_C}(d') is sequential with cardinality \|V_{s_C}(d)\| + n | introduced |
| INS.inv.depth | S8-depth (ASN-0036) preserved: in non-empty case m_C is unchanged; in empty case the first insertion fixes m_C = m for all subsequent text-subspace operations on d | introduced |
| INS.inv.cross-subspace | Cross-subspace isolation: V_{s_L}(d') = V_{s_L}(d) with mappings unchanged | introduced |
| INS.inv.cross-doc | Cross-document isolation: arrangements of all d' ≠ d unchanged | introduced |
| INS.inv.coverage | Endset coverage unchanged for every link by LP3★ (ASN-0098): coverage depends only on L, which is preserved | introduced |
| INS.inv.discov | Pre-state discoverability preserved: every link discoverable from any document at Σ remains discoverable at Σ' | introduced |
| INS.proj | Projection-shift correspondence: project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i} where π is region-aware (identity on Left, shift-by-n on Right, identity for d' ≠ d and link subspace) and N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n} captures Insertion images whose fresh a_k lies in coverage; N_{ℓ,i} = ∅ for tight endsets by LP19a (ASN-0098) | introduced |
| INS.atomicity | INSERT's substrate composite preserves per-state invariants (Class (a) of ASN-0047) at every intermediate state; composite-boundary properties (Class (b) — P4★, P4a, P7a) and coupling constraints (J0, J1★, J1'★) hold at the boundary Σ →* Σ' | introduced |
| INS.position | INSERT permitted at any valid position: N+1 valid positions under ValidInsertionPosition for non-empty V_{s_C}(d), plus single first-insertion position under ValidFirstInsertionPosition(d, p, m) with caller-chosen m ≥ 2 for empty case | introduced |
| INS.identity | INSERT creates fresh content identity: each a_k is a new allocation with origin(a_k) = d; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence | introduced |
| INS.identity.crossdoc | Cross-document allocation independence: two distinct documents inserting identical values produce disjoint fresh I-address sequences with distinct origins (by SubAllocatorAxiom.Disjointness, ASN-0047) | introduced |
| INS.identity.version | Version chain independence: INSERT on a derived version d_v allocates from A_C(d_v) with origin = d_v ≠ origin of d_v's source document | introduced |
| INS.identity.tightsurv | Link survivability through value coincidence: tight endsets cannot accidentally capture freshly allocated content by LP19a (ASN-0098) | introduced |

## Open Questions

- Under what abstract conditions can an environment satisfy the composite-boundary atomicity guarantee, and what must an implementation provide to recover canonical order after a partial failure during the substrate composite?
- What invariants must an analogous insertion operation preserve when the target is the link subspace rather than the text subspace?
- Is INSERT closed under composition with itself — i.e., if `Σ →INSERT→ Σ_1 →INSERT→ Σ_2`, is there always a single INSERT from `Σ` to `Σ_2`, or do the intermediate effects accumulate in ways that no single INSERT can reproduce?
- What does the abstract specification say about concurrent INSERTs targeting the same V-position from independent agents — must the system serialise them, and if so, on what basis is the order chosen?
- Must INSERT operate on values atomically as a sequence, or may an implementation chunk a long insertion into smaller pieces while preserving observable equivalence at the abstract level?
- What derived properties of a document — current size, last-modified marker, total I-address footprint — does INSERT update, and which of these are part of the abstract state versus derivable from it?
- What abstract guarantee constrains the order in which the K.α firings of step 1 of the substrate composite may be interleaved with the K.ρ firings of step 4, and does any such reordering produce an externally observable difference?
