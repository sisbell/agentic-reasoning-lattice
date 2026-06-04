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

**Notational convention** (used throughout this ASN). We adopt `shift(t, 0) := t` as a notational extension of OrdinalShift (ASN-0034), which is defined only for `n ≥ 1`. This convention is consistent with OrdinalShiftBase (ASN-0058), whose definition `t + 0 = t` establishes the identity behaviour at offset zero under the `+` notation; we lift the same identity to the `shift(·, ·)` notation for uniform exposition. With this convention, the `j = 0` admissible position above resolves to `shift(min, 0) = min(V_{s_C}(d))` — insertion at the very beginning.

This yields `N + 1` admissible positions: `j = 0` inserts before the first character, `j = N` after the last, and `j ∈ {1, …, N−1}` in the interior.

For empty `V_{s_C}(d)`, the precondition is the ternary predicate `ValidFirstInsertionPosition(d, p, m)` (ASN-0036): the caller chooses a depth `m ≥ 2` and the single admissible position is `[s_C, 1, …, 1]` of length `m`. The post-state has `V_{s_C}(d') ≠ ∅`, at which point S8-depth fixes `m_C = m` for `d` at every state in which `V_{s_C}(d)` remains non-empty — every subsequent text-subspace position in `d` must have depth `m` as long as that condition holds, since S8-depth is a per-state invariant under ValidComposite★ (ASN-0047).

The condition `n ≥ 1` rules out a degenerate empty-insertion case. The values `v_k` must be elements of the content type `Val`; the abstract specification places no further constraint on their structure.

These preconditions are necessary; we shall verify they are jointly sufficient.

## Discovering the Three Effects

We reason from the intent backward to the formal specification. INSERT splices `n` new content units into `d`'s arrangement at V-position `p`. Three effects must obtain together.

### Effect One: Allocation

The new content units do not exist in `dom(C)` before the operation. Nelson is unambiguous (Q1, Q5, Q8): INSERT creates *new* content with *fresh* I-addresses. The operation does not reuse, alias, or identify with any pre-existing I-address.

The freshness comes from `d`'s content sub-allocator `A_C(d)`, by the substrate's allocation discipline (ASN-0093). We require `n` addresses, produced by `n` successive K.α firings under the substrate's transition vocabulary:

  `a_k = A_C(d)`'s `k`-th emission across the composite, for `0 ≤ k < n`

The freshness of each `a_k` is established against the state immediately preceding its K.α firing — not against the operation's pre-state Σ. If Σ_k denotes the substrate state after K.α has fired for `a_0, …, a_{k−1}`, then K.α's precondition requires `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)`. This conjunction is exactly the conclusion of SubsequentEmissionFreshness (ASN-0093): the subsequent emission `a_k = inc(a_prev, 0)` of `A_C(d)` is fresh against `dom(C) ∪ dom(L)`, with the three-way split — within-document, cross-document, cross-subspace — discharged there. The boundary case `m_d = 0`, where `a_0` is `A_C(d)`'s first emission `[d.0.s_C.1]`, is covered by FirstEmissionFreshness (ASN-0093). These two lemmas discharge K.α's freshness precondition at each of the `n` firings.

By the chain discipline (ChainPrefixExtension, ChainEnumerationInjectivity; ASN-0093), every `a_k` has `origin(a_k) = d`, satisfies `b_C(d) ≼ a_k` (extending the content sub-allocator anchor), and is structurally produced by the sub-allocator's `inc(·, 0)` chain. The addresses `a_0, a_1, …, a_{n−1}` form a contiguous initial-segment extension of the chain: `a_{k+1} = inc(a_k, 0)` for `0 ≤ k < n − 1`, and `a_0` is either `[d.0.s_C.1]` (if `d` had no prior content emissions, per K.α's first-emission predicate in ASN-0093) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(Σ.C) : origin(a) = d}` (per K.α's subsequent-emission predicate in ASN-0093).

**Chain emissions in ordinal-shift form (INS.chain-shift).** The allocation recurrence `a_{k+1} = inc(a_k, 0)` admits an equivalent ordinal-shift reading. We claim that for any contiguous chain segment of `A_C(d)`, successive emissions are ordinal shifts: if `a_i` and `a_{i+j}` are chain elements with `a_{i+1} = inc(a_i, 0)` at each step, then `a_{i+j} = shift(a_i, j)`. In particular `a_k = shift(a_0, k)` for the Insertion chain (`0 ≤ k < n`).

The single-step identity `inc(a_i, 0) = shift(a_i, 1)` is not definitional — it holds because each `a_i` is a T4-valid address. Each `a_i` is a chain element of `A_C(d)`, hence T4-valid by ChainElementT4Validity (ASN-0093). By TA5-SigValid (ASN-0034), a T4-valid address has `sig(a_i) = #a_i` — its rightmost nonzero component sits at its last position. Applying TA5 (HierarchicalIncrement, the `k = 0` case; ASN-0034) to `a_{i+1} = inc(a_i, 0)`: the increment modifies position `sig(a_i) = #a_i` to `(a_i)_{#a_i} + 1`, preserves the length (`#a_{i+1} = #a_i`), and leaves every other component fixed. This is precisely the action of `shift(a_i, 1) = a_i ⊕ δ(1, #a_i)` (OrdinalShift; ASN-0034), which advances the last component by 1 and copies the prefix. Hence `a_{i+1} = shift(a_i, 1)`.

The identity iterates because `inc(·, 0)` preserves T4 (TA5a; ASN-0034) and preserves length (TA5(c); ASN-0034): every successor `a_{i+1}` is again a T4-valid same-length address, so `sig = #` holds at every index and the inc/shift equivalence applies at each step. Composing by TS3 (ShiftComposition; ASN-0034) — `shift(shift(a_i, j), 1) = shift(a_i, j + 1)` — and unfolding from the base `a_i = shift(a_i, 0)` yields `a_{i+j} = shift(a_i, j)` by induction on `j`. Specialising to `i = 0` gives `a_k = shift(a_0, k)`.

Consequently the Insertion region `{(shift(p, k), a_k) : 0 ≤ k < n}` coincides with `{(shift(p, k), shift(a_0, k)) : 0 ≤ k < n}`, which is exactly the denotation `⟦(p, a_0, n)⟧` of the mapping block `(p, a_0, n)` under OrdinalShiftBase (ASN-0058) — there the run's I-address `a_0 + k` reads as `shift(a_0, k)`.

The post-state content store:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `C'(a_k) = v_k` for `0 ≤ k < n`
  `C'(a) = C(a)` for `a ∈ dom(C)`

The third clause is the most important. The pre-existing content is *not touched*. Its values are preserved bit-for-bit; its addresses persist in the post-state. This is the foundational permanence guarantee S0.

### Effect Two: Placement

The new I-addresses must appear at V-positions `p, shift(p, 1), …, shift(p, n−1)`. With `shift(p, 0) = p`, the mapping is exact:

  `(A k : 0 ≤ k < n : M'(d)(shift(p, k)) = a_k)`

By OrdAddHom clause (b) (ASN-0082) applied to `w = δ(k, m_C)`, every `shift(p, k)` for `k ≥ 1` lies in the same subspace as `p`: `subspace(shift(p, k)) = s_C`. The result-length identity of TumblerAdd (ASN-0034) gives `#shift(p, k) = m_C`. For `k = 0`, `shift(p, 0) = p` shares subspace and depth with `p` trivially. Each `shift(p, k)` satisfies S8a (VPositionWellFormedness, ASN-0036): zero-free, depth `≥ 2`, all components positive. The justification routes through `p`'s own S8a, which is supplied by the insertion-position precondition directly — `ValidInsertionPosition` postcondition (b) (ASN-0036) in the non-empty case, or `ValidFirstInsertionPosition` postcondition (b) (ASN-0036) in the empty case. Both predicates assert S8a as their (b) postcondition unconditionally. The shift's tail component `p_{m_C} + k ≥ 1` then transfers S8a to `shift(p, k)`: zeros remain zero (the leading components of `p` are `1` by ValidInsertionPosition/ValidFirstInsertionPosition postcondition (d), and the tail is positive), depth is preserved at `m_C ≥ 2`, all components remain strictly positive. The new V-positions are well-formed inhabitants of `V_{s_C}(d')`.

### Effect Three: Shift

Every existing V-position `v ∈ V_{s_C}(d)` with `v ≥ p` must remap. The content there does not change — it keeps its I-address — but its V-position advances by `n`:

  `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

This clause is the specified effect of INSERT's step-3 K.μ⁺ (§The Operation: Formal Contract), which by construction adds exactly the mappings `shift(v, n) ↦ M(d)(v)` for each `v ∈ V_{s_C}(d)` with `v ≥ p`. The right region is the source of the shift; the shifted-right region is its image. The two are related by the order-preserving (TS1, ShiftOrderPreservation; ASN-0034) and injective (TS2, ShiftInjectivity; ASN-0034) shift map. The image of the shift map is exactly `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N}` when we write `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`. The Insertion positions `shift(p, k)` for `0 ≤ k < n` are disjoint from these shift-images (by the pairwise-disjointness argument below for S2).

For positions `v ∈ V_{s_C}(d)` with `v < p` (the left region), the arrangement is unchanged (I3-L, PostInsertionLeftFrame; ASN-0082).

For positions in subspaces other than `s_C` — including the link subspace — the arrangement is unchanged (I3-X, PostInsertionCrossSubspaceFrame; ASN-0082).

For other documents `d' ≠ d`, the arrangement is unchanged (I3-D, PostInsertionCrossDocumentFrame; ASN-0082).

Pre-existing content store entries are preserved pointwise — every `a ∈ dom(C)` has `a ∈ dom(C')` with `C'(a) = C(a)` (S0, ContentImmutability; ASN-0036, and P0, ContentPermanence; ASN-0047) — discharged by INS.C's third clause. INSERT extends `dom(C)` by the freshly allocated addresses (Effect One), so the store itself is *not* unchanged.

These exhaust the cases.

## The Operation: Formal Contract

INSERT is a **substrate composite** in the sense of ValidComposite★ (ASN-0047) — a finite sequence of elementary transitions drawn from the substrate's K-vocabulary, governed at the composite boundary by the coupling constraints J0, J1★, J1'★. It is *not* a new elementary primitive; the substrate transition vocabulary is not amended.

The operative substrate is ValidComposite★ (ASN-0047), whose vocabulary is `{K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, K.ρ}`. Document registration in this framework is K.δ in its IsDocument sub-case.

We state INSERT as a composite `Σ →* Σ'`.

**Operation:** `INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)`

**Substrate Decomposition.** INSERT realises as the following sequence of elementary transitions, in order:

1. **`n` successive K.α firings** allocating fresh content addresses `a_0, a_1, …, a_{n−1}` from `A_C(d)`. Each K.α firing satisfies its freshness precondition against the intermediate state immediately preceding it (justified by ChainEnumerationInjectivity; ASN-0093 — see Effect One above).
2. **One K.μ⁻ on `d`** — fired iff the pre-state content-subspace Right region `{v ∈ V_{s_C}(d) : v ≥ p}` is non-empty — retaining the Left prefix of `V_{s_C}(d)` (with `n'_{s_C} = p_m − 1`) and retaining all of `V_{s_L}(d)` (with `n'_{s_L} = n_{s_L}`). The operative condition is single: K.μ⁻ appears in the canonical decomposition exactly when strict `s_C` contraction is both needed (the Right region must be removed before K.μ⁺ can reintroduce it shifted) and admissible while preserving `s_L`. When the Right region is empty — the append case (`p_m = N + 1`) and both empty-content-subspace cases (`V_{s_C}(d) = ∅`) — K.μ⁻ is omitted, and step 3's K.μ⁺ alone adds the Insertion region, leaving `V_{s_L}(d)` untouched.
3. **One K.μ⁺ on `d`** adding the Insertion V-positions (mapping `shift(p, k) ↦ a_k` for `0 ≤ k < n`) and the Shifted-right V-positions (mapping `shift(v, n) ↦ M(d)(v)` for each `v ∈ V_{s_C}(d)` with `v ≥ p`). All additions in step 3 lie in subspace `s_C`, as required by K.μ⁺'s content-subspace restriction (ASN-0047).
4. **`n` successive K.ρ firings** recording provenance pairs `(a_k, d)` for `0 ≤ k < n`.

Each intermediate state in this sequence satisfies the per-state invariants (Class (a) of ASN-0047); the composite-boundary properties (Class (b): P4★, P4a, P7a) are discharged at the boundary `Σ →* Σ'` by the constraints J0, J1★, J1'★.

**State Preconditions** (evaluated against the operation's pre-state Σ):
- `d ∈ dom(M)`
- `subspace(p) = s_C`
- `#p = m_C` (the common depth of `V_{s_C}(d)` if non-empty per S8-depth, ASN-0036; the caller's chosen depth `m ≥ 2` if empty)
- `p` is a valid insertion position: either `ValidInsertionPosition(d, p)` (ASN-0036) for non-empty `V_{s_C}(d)` — equivalently `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ |V_{s_C}(d)|}` (with `shift(t, 0) = t`) — or `ValidFirstInsertionPosition(d, p, m)` (ASN-0036) for empty `V_{s_C}(d)`, equivalently `p = [s_C, 1, …, 1]` of depth `m`
- `n ≥ 1`
- `v_k ∈ Val` for each `0 ≤ k < n`

**Composite atomicity.** Composite-level atomicity is definitional under ValidComposite★ (§Atomicity). Its consequence here is determinacy of Σ': because the chain index `m_d` consulted by K.α cannot advance via a foreign K.α mid-composite, and the text subspace `V_{s_C}(d)` cannot be modified mid-composite, the freshness and placement arguments above determine Σ' from the pre-state. An implementation that realizes the sequential transition model (for instance, multiple threads serialised onto the abstract total order) inherits this determinacy; the concurrency-control mechanism it uses is below this ASN's abstraction level.

**Effect — Content Store:**
Let `a_0, a_1, …, a_{n−1}` denote the `n` successive emissions of `A_C(d)` produced by the K.α firings of step 1. Then:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `(A k : 0 ≤ k < n : C'(a_k) = v_k)`
  `(A a : a ∈ dom(C) : C'(a) = C(a))`

**Effect — Arrangement of `d`, text subspace:**
Three disjoint regions:

  *Left* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

  *Insertion* — `(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)` — with `shift(p, 0) = p`.

  *Shifted right* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

  *Exhaustiveness* (INS.M-exhaustive) — `(A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right)`, where Left, Insertion, and Shifted-right denote the three V-position sets defined by the per-region clauses above. Equivalently, `V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions, with no additional `s_C` positions in the post-state.

The exhaustiveness clause is a property of the post-state `V_{s_C}(d')`, and it follows directly from the composite construction. Steps 1 and 4 (the K.α and K.ρ firings) frame `M` (`M' = M`; ASN-0047), so they introduce no `s_C` position. Step 2's K.μ⁻ (when fired) only *removes* positions. Step 3's K.μ⁺ adds *exactly* the Insertion positions `{shift(p, k) : 0 ≤ k < n}` and the Shifted-right positions `{shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p}` (its specified effect). Hence every `s_C` position in `dom(M'(d))` is either a surviving pre-state position with `v < p` (Left), an Insertion position, or a Shifted-right position — no fourth region exists.

**Effect — Provenance:**

  `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`

realised by step 4's `n` K.ρ firings.

**Frame Conditions:**
- `L' = L`. The link store is unchanged: no K.λ fires in the decomposition, so `dom(L)` and every link value persist by L12 (LinkImmutability; ASN-0093).
- `E' = E`. The entity set is unchanged: no K.δ fires in the decomposition (`dom(M)` is governed via K.δ-IsDocument under ValidComposite★; INSERT registers no new document and creates no new node, account, or non-document entity).
- `dom(M') = dom(M)`. As a specialisation of `E' = E` for the document subset: no new document is registered.
- `(A d' : d' ∈ dom(M) ∧ d' ≠ d : M'(d') = M(d'))`. Other documents' arrangements are unchanged (K.α, K.μ⁻, K.μ⁺, K.ρ all carry `(A d' : d' ≠ d :: M'(d') = M(d'))` as their explicit per-step frame in ASN-0047).
- `{v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C} ∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : M'(d)(v) = M(d)(v))`. Other subspaces of `d` — in particular `V_{s_L}(d)` — are unchanged both as sets (no new non-`s_C` positions appear in `dom(M'(d))`, and no existing ones are removed) and pointwise (existing mappings preserve their images). Step 2's K.μ⁻ (when fired) preserves the link subspace by `n'_{s_L} = n_{s_L}`; step 3's K.μ⁺ adds only content-subspace V-positions (per the K.μ⁺ amendment in ASN-0047), so the set-equality direction holds in both directions.

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
- *Insertion:* `{[1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}}` — matches `shift(p, k) ↦ a_k` for `k ∈ {0, 1}` via INS.M-insert; note `shift([1,3], 0) = [1,3]`.
- *Shifted right:* `{[1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}` — matches `shift(v, 2) ↦ M(d)(v)` for `v ∈ {[1,3], [1,4], [1,5]}` via INS.M-shift.

The last-component values in `V_{s_C}(d')` are `{1, 2, 3, 4, 5, 6, 7}` — sequential, contiguous, starting at 1, satisfying INS.inv.seq with new cardinality `N + n = 7`.

*Projection-shift correspondence (INS.proj).* Suppose a link `ℓ ∈ dom(L)` has a slot with endset `e_1` delivered by the canonical span `(a_2, δ(3, #a_2))`, whose coverage is the half-open tumbler interval `coverage(e_1) = [a_2, a_5)` (since `a_5 = a_2 ⊕ δ(3, #a_2) = shift(a_2, 3)` — INS.chain-shift applied to the pre-state chain segment `a_2, a_3, a_4, a_5`, all T4-valid same-length emissions of `A_C(d)`; ASN-0098). This interval strictly contains `{a₂, a₃, a₄}` — by T5 (ASN-0034) it also holds every descendant of `a₂, a₃, a₄`. The quantity that equals the three-element set is the *intersection with the range*: `coverage(e_1) ∩ ran(M(d)) = {a₂, a₃, a₄}`, the three I-addresses of the pre-state range that fall in the interval. **Tightness precondition of the trace below, grounded in the example's substrate state.** We construct `Σ_{e_1}` — the state at which `e_1` was incorporated into `ℓ` via K.λ — concretely. Let `Σ_{e_1}` be the substrate state of `d` immediately after `M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃, [1,4] ↦ a₄, [1,5] ↦ a₅}` had been established (the pre-state of our INSERT) and *before* any subsequent K.α firing of INSERT advances `A_C(d)`'s chain. At `Σ_{e_1}`, the content addresses `a₁, a₂, a₃, a₄, a₅ ∈ dom(Σ_{e_1}.C)` are all present — they were placed there by prior K.α firings constituting the chain of `A_C(d)` (per ChainMembershipForOrigin; ASN-0093), with structural form `aᵢ = [d.0.s_C.i]` for `1 ≤ i ≤ 5`. The endset `e_1`'s delivering span `(a_2, δ(3, #a_2))` has start `a_2 ∈ dom(Σ_{e_1}.C)`, width `δ(3, #a_2)` of length `#a_2 = #d + 3` (so the action point equals the length — canonical), and reach `a_2 ⊕ δ(3, #a_2) = a_5`. By LP-Fin Corollary (CanonicalIntervalCharacterisation; ASN-0098), the F-candidates in the half-open interval `[a_2, a_2 ⊕ δ(3, #a_2))` are exactly `{[d.0.s_C.2], [d.0.s_C.3], [d.0.s_C.4]} = {a_2, a_3, a_4}`. All three are members of `dom(Σ_{e_1}.C)` by construction. Therefore the tightness conditions of ASN-0098 hold: the span is canonical (width is `δ(3, #a_2)`), the start lies in `dom(Σ_{e_1}.C) ∪ dom(Σ_{e_1}.L)`, and every F-candidate in the interval lies in `dom(Σ_{e_1}.C) ∪ dom(Σ_{e_1}.L)`. We conclude `tight(e_1, Σ_{e_1})` (ASN-0098). This is the load-bearing assumption that makes `N_I = ∅` concrete via LP19a (TightFreshness; ASN-0098); we trace the non-tight alternative at the end of this example. We trace the projection through the composite.

Pre-state `project(ℓ, 1, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e_1)} = {[1,2], [1,3], [1,4]}`, since the I-addresses of `ran(M(d))` lying in `coverage(e_1) = [a_2, a_5)` are exactly `coverage(e_1) ∩ ran(M(d)) = {a₂, a₃, a₄}`. Partition into regions relative to `p = [1,3]`: `P_0^L = {[1,2]}` (the single position with `v < p`); `P_0^R = {[1,3], [1,4]}` (positions with `v ≥ p`); `P_0^{s_L} = ∅` (the link subspace is empty for this example).

Step 1 (K.α firings): `Σ.M(d)` unchanged, projection unchanged at `{[1,2], [1,3], [1,4]}` by LP6.

Step 2 (K.μ⁻): `V_{s_C}(d_intermediate) = {[1,1], [1,2]}`. The projection contracts to `P_0 ∩ R_kept = {[1,2]}` by LP10 — the Right contributions `[1,3]` and `[1,4]` temporarily disappear.

Step 3 (K.μ⁺): adds Insertion positions `{[1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}}` and Shifted-right positions `{[1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}`. By LP9, the new projection contributions are exactly those new V-positions whose image lies in `coverage(e_1) = [a_2, a_5)`. Among Insertion: by LP19a (TightFreshness; ASN-0098) applied to the tightness assumption `tight(e_1, Σ_{e_1})`, the freshly allocated `a_{new0}, a_{new1}` cannot lie in `coverage(e_1)` — so `a_{new0}, a_{new1} ∉ coverage(e_1)` and `N_I = ∅`. Among Shifted-right: `a₃, a₄ ∈ coverage(e_1)` (both lie in `[a_2, a_5)`) but `a₅ ∉ coverage(e_1)` (it is the exclusive upper bound), so `N_S = {[1,5], [1,6]}`.

The projection grows to `{[1,2]} ∪ ∅ ∪ {[1,5], [1,6]} = {[1,2], [1,5], [1,6]}`.

Step 4 (K.ρ firings): projection unchanged by LP14.

Post-state `project(ℓ, 1, d, Σ') = {[1,2], [1,5], [1,6]}`. Apply the region-aware shift map `π`: π is identity on `P_0^L = {[1,2]}`, giving `{[1,2]}`; π is `shift(·, 2)` on `P_0^R = {[1,3], [1,4]}`, giving `{[1,5], [1,6]}`. The combined image `π(project(ℓ, 1, d, Σ)) = {[1,2], [1,5], [1,6]}` matches `project(ℓ, 1, d, Σ')` exactly. Since `N_{ℓ,1} = N_I = ∅` in this tight-endset case, INS.proj's general form `π(project) ∪ N_{ℓ,i}` resolves to `π(project)`. The projection has shifted with the content; the link has tracked it.

*Non-tight alternative.* For the tight `e_1` above, `N_I = ∅` holds for a structural reason that outlives tightness: K.α's subsequent-emission rule advances the chain frontier, so `a_{new0} = inc([d.0.s_C.5], 0) = [d.0.s_C.6]` and `a_{new1} = [d.0.s_C.7]` both lie strictly above `coverage(e_1)`'s ceiling `a_5 = [d.0.s_C.5]` under T1 (last components 6, 7 > 5), regardless of any tightness assumption. To exhibit `N_I ≠ ∅` we need an endset whose declared coverage reaches *past* the chain frontier. Take `e_1'` delivered by the canonical span `(a_2, δ(10, #a_2))`, with `coverage(e_1') = [a_2, [d.0.s_C.12])` (since `a_2 ⊕ δ(10, #a_2) = shift(a_2, 10) = [d.0.s_C.12]`). This endset is non-tight at the INSERT pre-state `Σ_{e_1'}`: the F-candidates `[d.0.s_C.6], …, [d.0.s_C.11]` lie in the interval but are absent from `dom(Σ_{e_1'}.C) ∪ dom(Σ_{e_1'}.L)` — the chain frontier is only at `[d.0.s_C.5]` — so the tightness condition of ASN-0098 fails and LP19a is inapplicable. Now both fresh addresses fall inside coverage: `a_{new0} = [d.0.s_C.6]` and `a_{new1} = [d.0.s_C.7]` satisfy `a_2 ≤ a_{new k} < [d.0.s_C.12]`, so the Insertion positions `[1,3]` and `[1,4]` both contribute and `N_I = {[1,3], [1,4]}`. The INS.proj general form `π(project) ∪ N_{ℓ,i}` captures both regimes; the tight case is the special simplification with `N_I = ∅`. Non-tight endsets are designed to capture later-allocated content within their declared range, and INSERT's freshly placed I-addresses are exactly such content.

*Discoverability (INS.inv.discov).* Pre-state `discoverable_from(ℓ, d, Σ)` holds because the projection was non-empty. Post-state `project(ℓ, 1, d, Σ') = {[1,2], [1,5], [1,6]} ≠ ∅`, so `discoverable_from(ℓ, d, Σ')` also holds. The link is preserved across the operation; the coverage targets `{a₂, a₃, a₄}` are still in `ran(M'(d)) = {a₁, a₂, a_{new0}, a_{new1}, a₃, a₄, a₅}`.

*Provenance discharge (J0, J1★, J1'★).* Step 4's two K.ρ firings add exactly `(a_{new0}, d)` and `(a_{new1}, d)` to R, giving `R' = R ∪ {(a_{new0}, d), (a_{new1}, d)}`. These are the two freshly allocated Insertion images, placed at `[1,3]` and `[1,4]`. The Shifted-right images `a₃, a₄, a₅` (placed at `[1,5], [1,6], [1,7]`) were already arranged pre-state at `[1,3], [1,4], [1,5]`, so they are already in R by pre-state P4★ and impose no new obligation. Here the coupling logic instantiates to the two pairs above: J0 pairs each fresh `dom(C') \ dom(C)` address with its K.μ⁺ placement, J1★ records each newly-arranged content-subspace image, and J1'★ matches each new R'-entry back to a placement — all satisfied when step 4's K.ρ firings commit.

**Append case (`j = N = 5`).** With the same pre-state, `INSERT(d, [1,6], ⟨v₀⟩)` (where `[1,6] = shift([1,1], 5)` is one past the last position). The Right region is empty; no K.μ⁻ fires (Left = entire `V_{s_C}(d)`). Composite: one K.α + one K.μ⁺ adding `[1,6] ↦ a_{new0}` only + one K.ρ. Post-state `V_{s_C}(d') = {[1,1], …, [1,6]}` with `a₁, …, a₅, a_{new0}` as images.

**Empty-document first insertion.** Let `d` have `V_{s_C}(d) = ∅` and additionally `V_{s_L}(d) = ∅` (so the document's arrangement is entirely empty). Invoke `INSERT(d, [1,1], ⟨v₀, v₁, v₂⟩)` with `m = 2` (caller-chosen depth) and `n = 3`. The position `p = [1,1]` is the unique value admitted by `ValidFirstInsertionPosition(d, p, 2)` (ASN-0036). K.μ⁻ is omitted because the content-subspace Right region is empty (`V_{s_C}(d) = ∅`, so no `v ≥ p`). The variant where `V_{s_C}(d) = ∅` but `V_{s_L}(d) ≠ ∅` produces the same INSERT post-state shape on the content subspace: the operation's text-subspace effect (Insertion at `shift(p, k) ↦ a_{new k}`, empty Left, empty Shifted-right) depends only on `V_{s_C}(d) = ∅`, not on whether `V_{s_L}(d)` is empty; the link subspace is preserved verbatim by the cross-subspace frame in either variant. The composite reduces to:

1. **Three K.α firings.** `A_C(d)` emits `a_{new0} = [d.0.s_C.1]` (first-emission predicate fires since `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`), then `a_{new1} = inc(a_{new0}, 0)`, then `a_{new2} = inc(a_{new1}, 0)`. Each freshly satisfies K.α's freshness precondition by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093).
2. **One K.μ⁺ on `d`** adding three V-positions: `[1,1] ↦ a_{new0}`, `[1,2] ↦ a_{new1}`, `[1,3] ↦ a_{new2}`. All in subspace `s_C` per the K.μ⁺ amendment.
3. **Three K.ρ firings** recording `(a_{new0}, d)`, `(a_{new1}, d)`, `(a_{new2}, d)` in R.

The post-state arrangement:

  `M'(d) = {[1,1] ↦ a_{new0}, [1,2] ↦ a_{new1}, [1,3] ↦ a_{new2}}`

with `V_{s_C}(d') = {[1,1], [1,2], [1,3]}`; this first insertion fixes `m_C = 2` for `d`. Verifying the three regions: *Left* is empty (no pre-state position with `v < p`); *Insertion* is `{[1,1] ↦ a_{new0}, [1,2] ↦ a_{new1}, [1,3] ↦ a_{new2}}` matching `shift(p, k) ↦ a_k` for `k ∈ {0, 1, 2}` (with `shift([1,1], 0) = [1,1]`); *Shifted right* is empty (no pre-state position with `v ≥ p`).

*Cross-subspace and cross-document frames (empty case).* `V_{s_L}(d) = ∅` is preserved trivially: K.μ⁺'s content-subspace restriction adds no `s_L` positions, so `V_{s_L}(d') = ∅` matches. Other subspaces are vacuous. Other documents `d' ≠ d` have `M'(d') = M(d')` by each elementary step's cross-document frame.

*Discharge of J0, J1★, J1'★ (empty case).* Step 3's three K.ρ firings add `(a_{new0}, d), (a_{new1}, d), (a_{new2}, d)` to R. Since pre-state `ran(M(d)) = ∅`, all three Insertion images are newly-arranged, placed by step 2's K.μ⁺ at `[1,1], [1,2], [1,3]` respectively. Here the coupling logic instantiates to these three pairs — each fresh `a_{new k}` is placed at `[1,1+k]` (J0), is a newly-arranged content-subspace image (J1★), and matches its new R'-entry (J1'★) — satisfied when step 3's K.ρ firings commit.

*Empty-arrangement vs. fresh-allocator-state sub-case.* The example above has both `V_{s_C}(d) = ∅` (empty arrangement) and `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅` (fresh allocator state). These two conditions are independent and select different aspects of the operation: *empty arrangement* (`V_{s_C}(d) = ∅`) is the precondition that selects `ValidFirstInsertionPosition(d, p, m)` over `ValidInsertionPosition(d, p)` and forces the V-position `p = [1, 1]`; *fresh allocator state* (`{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`) is the K.α first-emission predicate that determines `a_{new0} = [d.0.s_C.1]` exactly. Consider the alternative sub-case where `d` has prior content emissions in `dom(C)` that are not currently arranged — for example, content allocated by an earlier INSERT and later removed from `M(d)` by a K.μ⁻, leaving the addresses permanent in `C` (by P0) but the arrangement empty. Concretely, suppose `dom(C)` contains `[d.0.s_C.1], [d.0.s_C.2]` from a prior INSERT both subsequently dropped from `M(d)`. Then the empty-arrangement precondition still holds (selecting `ValidFirstInsertionPosition`), but K.α's first-emission predicate is false; instead the subsequent-emission predicate fires `a_{new0} = inc(max{a' ∈ dom(C) : origin(a') = d}, 0) = inc([d.0.s_C.2], 0) = [d.0.s_C.3]`, continuing the existing chain rather than producing `[d.0.s_C.1]` (which is already taken). The generic notation `a_{new k}` covers both sub-cases; the V-position assignments `[1, 1] ↦ a_{new0}`, `[1, 2] ↦ a_{new1}`, `[1, 3] ↦ a_{new2}` are determined by the empty-arrangement condition, while the actual address values are determined by the chain state. The post-state predicates (D-CTG★, D-MIN★, D-SEQ★, S8a, S8-depth) hold uniformly in either sub-case; J0, J1★, J1'★ discharge identically (the fresh `a_{new k}` are by definition outside `ran(M(d)) = ∅` regardless of whether they are first emissions or chain continuations).

## Verifying the Invariants

The post-state Σ' must satisfy every system invariant. We verify the principal ones.

### Permanence of existing content (S0, P0)

The content-store effect's third clause asserts `(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`. This is S0 (ContentImmutability; ASN-0036), equivalently P0 (ContentPermanence; ASN-0047), which subsumes S0 ∧ S1. The first clause `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` adds new addresses without removing any; the new addresses are fresh by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093), so no overwrite occurs. Store monotonicity `dom(C) ⊆ dom(C')` follows.

Each per-step K.α firing preserves S0 by its own frame (its effect adds a new binding without modifying existing ones); K.μ⁻, K.μ⁺, K.ρ have frame `C' = C` and so preserve S0 trivially. The composite preserves S0 by composition.

The consequence Nelson emphasises (Q5): a reader holding any pre-state I-address `a ∈ dom(C)` retrieves the same value `C'(a) = C(a)` from the post-state. The reader needs no knowledge of where in any document's Vstream that content now lies.

### Cross-document independence (Q3)

The frame `(A d' : d' ≠ d : M'(d') = M(d'))` directly enforces independence: no document other than `d` has its arrangement altered. Coupled with `L' = L` and content-store preservation, this means that any document `d'` that transcludes content from `d` continues to map the same V-positions to the same I-addresses, and those I-addresses continue to resolve to the same values.

The two documents may share I-addresses through transclusion, but the cross-document frame and content preservation together ensure that the shared I-addresses' values and the *other* document's mappings are unaffected.

Cross-document independence extends to link projection: for any link `ℓ ∈ dom(L)` and any document `d' ≠ d`, the projection from `d'` is unchanged, `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`. This is established with the `d' ≠ d` case of INS.proj in §Coverage and link discoverability.

### Arrangement functionality (S2)

We verify that `M'(d)` is a function (S2, ArrangementFunctionality; ASN-0036): no V-position has two distinct image I-addresses.

The Left, Insertion, and Shifted-right regions are pairwise disjoint as sets of V-positions. Writing `p = [s_C, 1, …, 1, p_m]`:

- *Left ∩ Insertion = ∅.* Left positions have last component `< p_m`; Insertion positions have last component in `{p_m, p_m + 1, …, p_m + n − 1}`. The component arithmetic splits on `k`, since `δ(k, m_C)` is defined only for `k ≥ 1` (OrdinalDisplacement, ASN-0034). For `k = 0`, `shift(p, 0) = p`, so the final component is `(shift(p, 0))_{m_C} = p_m`. For `1 ≤ k < n`, the OrdinalShift definition `shift(p, k) = p ⊕ δ(k, m_C)` (ASN-0034) and TumblerAdd's piecewise rule (ASN-0034) at action point `m_C` apply: positions `1, …, m_C − 1` are inherited from `p`, and the final component is `(shift(p, k))_{m_C} = p_{m_C} + δ(k, m_C)_{m_C} = p_m + k`. Across both cases the last component ranges over `{p_m, p_m + 1, …, p_m + n − 1}` for `0 ≤ k < n`.

- *Insertion ∩ Shifted-right = ∅.* Insertion positions have last component in `{p_m, …, p_m + n − 1}`. Shifted-right positions image `v` with last component `v_m ≥ p_m` to `shift(v, n) = v ⊕ δ(n, m_C)`; by the same TumblerAdd rule (ASN-0034), the last component of `shift(v, n)` is `v_m + n`. Since `v_m ≥ p_m` and `n ≥ 1`, every Shifted-right last component satisfies `v_m + n ≥ p_m + n`, strictly greater than every Insertion last component.

- *Left ∩ Shifted-right = ∅.* Left last components are `< p_m`; Shifted-right last components are `≥ p_m + n ≥ p_m + 1`.

Within each region the mapping is uniquely defined: Left and Shifted-right by `M(d)` applied to a unique source position — for Shifted-right, source uniqueness follows from TS2 (ShiftInjectivity; ASN-0034) once its equal-length precondition is met: by S8-depth (FixedDepthVPositions; ASN-0036) all pre-state `s_C` positions share the common depth `m_C`, so for any pair of pre-state Right sources `v₁, v₂ ∈ V_{s_C}(d)` with `v₁ ≥ p` and `v₂ ≥ p`, `#v₁ = #v₂ = m_C` satisfies TS2's precondition; TS2 then yields injectivity — distinct sources `v₁ ≠ v₂` yield `shift(v₁, n) ≠ shift(v₂, n)`. Insertion images are uniquely indexed by `k`. The pairwise-disjoint and uniquely-defined regions together exhaust `V_{s_C}(d')` by INS.M-exhaustive — no fourth region of `s_C` positions exists in the post-state to violate functionality. So `M'(d)` is a well-defined function.

The pairwise-disjoint, uniquely-defined regions just given establish that `M'(d)` is a function directly. For other subspaces and other documents, `M'` equals `M`, which is already a function by the pre-state S2.

### Referential integrity (S3★)

We verify the generalised content-and-link form S3★ (GeneralizedReferentialIntegrity; ASN-0047): `(A v ∈ dom(M'(d)) : (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`.

For Left and Shifted-right content-subspace positions: the image is `M(d)(v')` for some pre-state position `v' ∈ dom(M(d))` with `subspace(v') = s_C`, so by pre-state S3★ the image lies in `dom(C)`, and by P0 (ContentPermanence; ASN-0047) `dom(C) ⊆ dom(C')`.

For Insertion positions: the image is `a_k ∈ dom(C')` by the content-store effect.

For positions in subspaces other than `s_C` of `d` (notably `s_L`), and for positions in other documents: unchanged by frame; S3★ follows from the pre-state combined with link-store immutability `L' = L`.

These three cases exhaust `dom(M'(d))` (by INS.M-exhaustive plus the cross-subspace frame), so S3★ holds on the whole post-state arrangement.

### Sequential text-subspace structure (D-CTG★, D-MIN★, D-SEQ★)

We verify the per-subspace forms D-CTG★ (PerSubspaceContiguity), D-MIN★ (PerSubspaceMinimumPosition), and D-SEQ★ (PerSubspaceSequentialPositions) from ASN-0047 for the text subspace `s_C` of `d` post-state.

**Closed-interval reduction (used in both cases below).** For any depth `m ≥ 2` and any `K ≥ 1`, the set `Pref(m, K) := {[s_C, 1, …, 1, k] : 1 ≤ k ≤ K}` (depth-`m` positions) satisfies D-CTG★ over the full depth-`m`, subspace-`s_C`, all-positive slice between its extremes `min = [s_C, 1, …, 1]` and `max = [s_C, 1, …, 1, K]` under T1. The slice ranges over *every* such tuple, not only those sharing the prefix `[s_C, 1, …, 1]`; for `m ≥ 3` it contains off-prefix tuples such as `[s_C, 2, 1, …, 1]` that must be shown to fall outside `[min, max]`. By D-CTG-depth (SharedPrefixReduction; ASN-0036), for `m ≥ 3` contiguity reduces to the last component once all positions share components `2` through `m − 1`. Write `z = [s_C, z_2, …, z_m]` with every `z_j ≥ 1` and `min ≤ z ≤ max`. If some `z_j > 1` for a least `j` with `2 ≤ j ≤ m − 1`, then `z` agrees with `max` on components `1, …, j − 1` and has `z_j > 1 = max_j` at the first divergence, so `z > max` by T1 case (i) — contradicting `z ≤ max`. Hence `z_j = 1` for `2 ≤ j ≤ m − 1`, so `z = [s_C, 1, …, 1, z_m]`; with `1 ≤ z_m ≤ K` forced at the last component, `z ∈ Pref(m, K)`. (For `m = 2` there are no interior positions and the reduction is immediate.) The last-component range `{1, …, K}` being contiguous closes D-CTG★. The two cases below apply this with `m = m_C, K = N + n` and with `m, K = n` respectively.

Suppose `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` with `N ≥ 1` (by pre-state D-SEQ★), and `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`. Then:

- Left positions: `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}` — empty if `p_m = 1`.
- Insertion positions: `{[s_C, 1, …, 1, p_m + j] : 0 ≤ j < n} = {[s_C, 1, …, 1, k] : p_m ≤ k < p_m + n}`.
- Shifted-right positions: `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N} = {[s_C, 1, …, 1, k] : p_m + n ≤ k ≤ N + n}` — empty if `p_m = N + 1`.

Their union is `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, which is exactly the sequential structure required by D-SEQ★ with new cardinality `N + n`. The minimum `[s_C, 1, …, 1]` is in the union, so D-MIN★ holds.

For D-CTG★, the union `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` is exactly `Pref(m_C, N + n)`, so the closed-interval reduction (instantiated with `m = m_C`, `K = N + n`) closes D-CTG★.

For the empty pre-state case (`V_{s_C}(d) = ∅`) with `p = [s_C, 1, …, 1]` of caller-chosen depth `m ≥ 2` (via ValidFirstInsertionPosition; ASN-0036): the post-state has only the Insertion region (Left and Shifted-right are empty). The Insertion positions are `shift(p, k) = [s_C, 1, …, 1, 1 + k]` for `0 ≤ k < n`, by OrdAddHom (ASN-0082) for `k ≥ 1` (where `shift(p, k) = p ⊕ δ(k, m)` agrees with `p` on positions `1, …, m − 1` and adds `k` to position `m`) and for `k = 0` (where `shift(p, 0) = p` resolves the position to `p` itself, which is `[s_C, 1, …, 1, 1] = [s_C, 1, …, 1]` since `p_m = 1`). Since `p_m = 1` (the unique valid first position has last component 1), the last components of the Insertion positions are `{1 + 0, 1 + 1, …, 1 + (n − 1)} = {1, 2, …, n}` and the leading `m − 1` components are all `1` throughout.

Post-state `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}`. We verify each predicate:

- *D-MIN★:* the minimum of `V_{s_C}(d')` under T1 is the position with the smallest last component, namely `[s_C, 1, …, 1, 1] = [s_C, 1, …, 1]` of depth `m`. This matches D-MIN★'s required form `[s_C, 1, …, 1]`.
- *D-CTG★:* the post-state `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}` is exactly `Pref(m, n)`, so the closed-interval reduction (instantiated with `K = n`) closes D-CTG★.
- *D-SEQ★:* the explicit form `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}` matches D-SEQ★ with `n_{s_C} = n` and depth `m_{s_C} = m`.
- *S8-depth:* every position in `V_{s_C}(d')` has length `m`. Pre-state `V_{s_C}(d) = ∅` imposes no depth constraint, so this first insertion fixes `m_C = m` for `d`.
- *S8a:* each Insertion position `[s_C, 1, …, 1, k]` is zero-free (subspace identifier `s_C ≥ 1` and all other components `1`), has length `m ≥ 2`, and has all components strictly positive.

The empty case differs from the non-empty case in that no Left or Shifted-right regions appear and no K.μ⁻ fires in the composite (the content-subspace Right region is empty when `V_{s_C}(d) = ∅`), but the post-state invariants are verified by the same predicate checks on the post-state's exhibited form.

### Post-state V-position well-formedness (S8-depth, S8a, S8-fin) and S7 invariants

We verify the post-state V-position predicates (S8-depth, S8a, S8-fin) and the S7 invariants directly. The S7 invariants range over `dom(C)` and the document set: S7a/S7b/S7d on pre-existing addresses follow from pointwise S0/P0 preservation, and the fresh `a_k` are discharged by the explicit C1/C1b/C1c argument below.

- *S8-depth (FixedDepthVPositions, ASN-0036).* Split the verification by `k`. At `k = 0`: `shift(p, 0) = p`, so `#shift(p, 0) = #p = m_C` directly from `p`'s precondition (`#p = m_C` from INSERT's preconditions, supplied either by S8-depth on the non-empty pre-state or by the caller's `ValidFirstInsertionPosition` depth choice). At `k ≥ 1`: by the OrdinalShift definition (ASN-0034), `shift(p, k) = p ⊕ δ(k, m_C)`; TumblerAdd's result-length identity (ASN-0034) gives `#shift(p, k) = #δ(k, m_C) = m_C`. In both cases, every Insertion position has depth `m_C`; Left and Shifted-right positions have depth `m_C` by §Effect Three's shift clause and the pre-state S8-depth. S8-depth holds across all subspaces of the post-state.

- *S8a (VPositionWellFormedness, ASN-0036).* Split the verification by `k`. At `k = 0`: `shift(p, 0) = p`, so S8a transfers directly from `p`'s S8a — `p` itself satisfies S8a (zero-free, depth `≥ 2`, all components strictly positive) by ValidInsertionPosition postcondition (b) (ASN-0036) in the non-empty case, or by ValidFirstInsertionPosition postcondition (b) (ASN-0036) in the empty case. At `k ≥ 1`: TumblerAdd's piecewise rule (ASN-0034) applied to `shift(p, k) = p ⊕ δ(k, m_C)` at action point `m_C` copies the leading `m_C − 1` components from `p`, which are all `1` (since `p` is a valid insertion position of the form `[s_C, 1, …, 1, p_m]` per ValidInsertionPosition's postcondition (d), ASN-0036, or `[s_C, 1, …, 1]` per ValidFirstInsertionPosition's postcondition (d), ASN-0036); the final component is `p_m + k ≥ p_m ≥ 1`. So `zeros(shift(p, k)) = 0`, `#shift(p, k) = m_C ≥ 2`, and every component is strictly positive. In both cases S8a holds on Insertion positions; Left positions inherit S8a from the pre-state (unchanged), and Shifted-right positions satisfy S8a because `shift(v, n)` preserves zero-freedom, depth, and positivity (§Atomicity, step 3). So S8a holds across the post-state.

- *S8-fin (FiniteArrangement, ASN-0036).* The Insertion region contributes exactly `n` new V-positions to `dom(M'(d))`. The pre-state `dom(M(d))` is finite by pre-state S8-fin; the post-state `dom(M'(d))` is the union of finite Left + finite Shifted-right + finite Insertion (cardinality `n`) + finite cross-subspace contributions, hence finite.

- *S7 invariants (S7a, S7b, S7d, and the derived theorem S7, ASN-0036), together with the content element-field invariants C1b and C1c (ASN-0093, also carried in ASN-0047's ExtendedReachableStateInvariants).* The predicates range over `dom(C)` and the document set, not over the V-position regions. Every pre-state `a ∈ dom(C)` inherits S7a, S7b, S7d, C1b, and C1c at the post-state by the pointwise S0/P0 preservation already established under §Permanence and the unchanged document set. For each freshly allocated `a_k ∈ dom(C') ∖ dom(C)`: `origin(a_k) = d ∈ dom(M')` discharges S7a (DocumentScopedAllocation) by K.α's emission discipline (ASN-0093); `zeros(a_k) = 3` discharges S7b (ElementLevelIAddresses) by C1 (ContentElementLevel, ASN-0093) — every content address has `zeros = 3`; `#E(a_k) ≥ 2` discharges C1b (ContentElementFieldDepth, ASN-0093) since `A_C(d)`'s first emission has `#E = 2` (FirstEmission, ASN-0093) and every subsequent emission via `inc(·, 0)` preserves length (TA5(c), ASN-0034); C1c (ContentAllocatorConformance, ASN-0093/ASN-0047) is discharged for `a_k` because `a_k` is an element of `A_C(d)` reached from `origin(a_k) = d` by `A_C(d)`'s T10a-conforming inc-chain (ChainMembershipForOrigin and ChainDiscipline, ASN-0093), which is exactly the conforming step sequence C1c requires; S7d (DocumentAllocationDiscipline) holds at `d` by pre-state inheritance — `d ∈ dom(M)` was a document-allocation event under T10a with `zeros(d) = 2` and T4-validity (M0, ASN-0093). The derived theorem S7 (StructuralAttribution) follows by composition.

- *P6 (ExistentialCoherence, ASN-0047).* `(A a ∈ dom(C') :: origin(a) ∈ E'_doc)` (where `E_doc` is the document subset of `E`). The argument uses the ValidComposite★ invariant `E_doc = dom(M)` (every document is allocated with `M(d) = ∅` by K.δ-IsDocument, the sole extender of `dom(M)`; ASN-0047), holding at both Σ and Σ'. Every pre-state `a ∈ dom(C)` inherits P6 because `dom(C) ⊆ dom(C')` and `origin(a)` is a property of the address `a` itself (an invariant of the addressing scheme, by S7 / StructuralAttribution), unchanged across the composite; meanwhile `E' = E` by INS.frame.E (no K.δ fires), so `E'_doc = E_doc`, and pre-state `origin(a) ∈ E_doc` lifts to `origin(a) ∈ E'_doc`. For each freshly allocated `a_k ∈ dom(C') ∖ dom(C)`: `origin(a_k) = d` by K.α's emission discipline (ASN-0093); INSERT's precondition gives `d ∈ dom(M) = E_doc`; INS.frame.E gives `E_doc = E'_doc`; hence `d ∈ E'_doc`, so `origin(a_k) ∈ E'_doc`. P6 is preserved across the composite.

### Per-subspace span decomposition (S8★)

S8★ (PerSubspaceSpanDecomposition; ASN-0047) requires that each per-subspace arrangement `M'(d)|_{V_S(d')}` admit a finite block decomposition satisfying ASN-0036's S8 conditions. The content-subspace arrangement `M'(d)|_{V_{s_C}(d')}` is a *restriction* of the whole arrangement `M'(d)` to a single subspace, so existence is supplied not by M2 (DecompositionExistence; ASN-0058) — which is stated for whole arrangements — but by C1a (RestrictionDecomposition; ASN-0058), the lemma that lifts M11/M12 to restrictions whose induced domain lies within a single subspace. We discharge C1a's three preconditions for `f = M'(d)|_{V_{s_C}(d')}`: (i) `f` is functional, being a restriction of the function `M'(d)` (S2, verified above under §Arrangement functionality, here in its extended form S3★/S2); (ii) `dom(f)` is finite, being a subset of the finite `dom(M'(d))` (S8-fin, verified under §Post-state V-position well-formedness); (iii) every position in `dom(f)` has first component `s_C`, so `dom(f) ⊆ V_{s_C}(d')` lies in a single subspace, and S8-depth (verified above) gives it a single common depth `m_C ≥ 2`. With these preconditions met, C1a yields a (unique maximally merged) block decomposition for `M'(d)|_{V_{s_C}(d')}`, discharging existence. The link-subspace branch S8★ requires for `M'(d)|_{V_{s_L}(d')}` is discharged by the trivial length-1 decomposition (per ASN-0047), inherited unchanged from the pre-state by the cross-subspace frame `V_{s_L}(d') = V_{s_L}(d)`.

The text-subspace decomposition has a particularly simple form: the Insertion region `{(shift(p, k), a_k) : 0 ≤ k < n}` forms a single correspondence run `(p, a_0, n)`. We discharge this collapse through the M7 merge condition (ASN-0058), which requires both V-adjacency and I-adjacency between successive length-1 blocks `(shift(p, k), a_k, 1)` and `(shift(p, k+1), a_{k+1}, 1)`.

For V-adjacency, M7 requires `shift(p, k+1) = shift(p, k) + 1`, reading the mapping-block `+ 1` as `shift(·, 1)`: this is `shift(shift(p, k), 1) = shift(p, k+1)`, an instance of TS3 (ShiftComposition; ASN-0034).

For I-adjacency, M7 requires `a_{k+1} = a_k + 1`, again reading `+ 1` as `shift(·, 1)`. By INS.chain-shift, `a_{k+1} = shift(a_k, 1)`, which is the I-adjacency M7 demands.

Both adjacencies holding, the `n` Insertion blocks merge into a single length-`n` block `(p, a_0, n)`, whose denotation `{(shift(p, k), shift(a_0, k)) : 0 ≤ k < n}` equals `{(shift(p, k), a_k) : 0 ≤ k < n}` by INS.chain-shift's `a_k = shift(a_0, k)`. The Left and Shifted-right portions are derived from the pre-state decomposition as follows. A pre-state block `(v', a', m')` whose V-extent straddles `p` — i.e., `v' < p` and `p ≤ shift(v', m' − 1)` — is first split at the interior offset `c := p_m − v'_m ∈ {1, …, m' − 1}` via M4 (ASN-0058), yielding a Left piece `(v', a', c)` and a Right piece `(shift(v', c), a' + c, m' − c)`. After all straddling pre-state blocks are split, every remaining pre-state block lies entirely below `p` (a Left block) or entirely at or above `p` (a Right block). The Left blocks transfer unchanged to the post-state; each Right block `(v', a', m')` becomes a Shifted-right block `(shift(v', n), a', m')` — V-start advanced by `n`, with I-start and width unchanged (shift acts only on V-positions, not on I-addresses; the width is the count of mapped positions, which is the same as in the source block). The post-state content-subspace decomposition is finite and well-defined, its existence guaranteed by C1a applied to the restriction `M'(d)|_{V_{s_C}(d')}` (preconditions discharged above). Restricting to the content subspace is essential here: M2 carries the precondition S3 (ReferentialIntegrity, ASN-0036), `ran(M(d)) ⊆ dom(C)`, which the whole extended-state arrangement fails whenever `V_{s_L}(d') ≠ ∅` — link-subspace positions map into `dom(L)`, so the whole arrangement satisfies only S3★ (GeneralizedReferentialIntegrity, ASN-0047), not S3. C1a ranges over the single content subspace, whose range is `⊆ dom(C)`; the link subspace is handled separately by S8★'s trivial length-1 decomposition.

This discharges S8★ conditions (a) (lockstep displacement, established by the run construction above) and (b) (label well-definedness, from each block being a well-formed mapping block over `dom(C')`), together with *existence* via C1a (the same restriction lemma, with preconditions discharged above). It remains to discharge condition (c) — uniqueness of the maximal-run decomposition, which S8★ requires only on the content subspace. C1a lifts M12 to the restriction — factoring through M12a (maximal runs partition the domain) and M12b (every block of a maximally merged decomposition is a maximal run) — and asserts that the restriction "admits a *unique* maximally merged block decomposition," closing condition (c) on the content subspace. (Condition (c) is not required on the link subspace, where S8★ asks only for the trivial length-1 decomposition.)

S8★ is preserved.

### Cross-subspace isolation

The frame `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` directly preserves all subspaces of `d` other than the text subspace. In particular, `V_{s_L}(d') = V_{s_L}(d)`, and link-subspace mappings are unchanged.

INSERT's shift is scoped strictly to `s_C`; non-text positions are never in the shift's carrier. The frame `INS.frame.subspace` (`V_{s_L}(d') = V_{s_L}(d)` with mappings unchanged) establishes the isolation directly.

Gregory's implementation realises this isolation via a two-blade "knife" whose blades bracket the text subspace; link-subspace crums are classified as outside the shift region and are uniformly left untouched. The structural property is what we verify abstractly; the knife is one (efficient) implementation.

### Link store unchanged (L12, L0, L1, L3)

`L' = L` directly preserves every link's address and value. Every `ℓ ∈ dom(L)` has `L'(ℓ) = L(ℓ)` — endsets are pointwise preserved. The element-level structure L1 and the N-endset structure L3 range over `dom(L)` alone, which is unchanged, so they hold of `L'` trivially.

The subspace partition L0 requires more care, because it has two conjuncts: `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)` and `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`. The first conjunct ranges over `dom(L)`, unchanged, and so is discharged trivially. The second conjunct ranges over `dom(C)`, which INSERT *extends* by the fresh content addresses `a_0, …, a_{n−1}` (INS.C) — it is therefore not a property of `L` alone. For each freshly allocated `a_k`, `subspace_I(a_k) = s_C` holds by DisjointSubAllocatorChains (ASN-0093): every address `a_k` is produced by `d`'s content sub-allocator `A_C(d)`, and every output of `A_C(d)` carries subspace identifier `s_C`. The pre-existing entries of `dom(C)` satisfy the conjunct by the pre-state invariant. Hence L0's content clause is preserved.

### Coverage and link discoverability

For every link `ℓ ∈ dom(L)` and every slot `i`, the endset `Σ.L(ℓ).e_i` is a set of spans. Each span `(s, ℓ_w)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ_w}` — a purely combinatorial property of the span representation, consulting no state component (definition of `coverage` in ASN-0098). Since `L' = L`, every link value is unchanged at every slot, so coverage is unchanged: by LP3★ (MultiStepCoverageInvariance; ASN-0098), `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` for every link and every slot. (LP3★ extends to multi-step compositions, so it discharges the property across the substrate composite, not just per-step.)

**Projection-shift correspondence (postcondition).** For every link `ℓ ∈ dom(L)`, slot `i`, and document `d' ∈ dom(M)`:

  `project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}`

where:
- *For `d' ≠ d`:* `π` is the identity and `N_{ℓ,i} = ∅`, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`. LP4 (ArrangementSpecificity; ASN-0098) and LP5 (CrossDocumentIndependence; ASN-0098) are single-step lemmas ("for every transition `Σ → Σ'`"), and INSERT is a composite of `2n+1`/`2n+2` elementary steps, so we must chain them rather than cite them once. Each elementary step of the substrate decomposition (every K.α, the optional K.μ⁻, K.μ⁺, every K.ρ) carries the explicit cross-document frame `(A d'' : d'' ≠ d : M'(d'') = M(d''))`, so `M(d')` is unmodified at every step. LP4 applied at each step (its hypothesis `M_{j+1}(d') = M_j(d')` is met by that step's frame) gives `project(ℓ, i, d', Σ_{j+1}) = project(ℓ, i, d', Σ_j)`; composing across the finite step sequence `Σ = Σ_0 → … → Σ_m = Σ'` yields `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`.
- *For `d' = d`, link subspace:* the link-subspace contribution is unchanged (frame), so `π` is the identity on link-subspace contributions and `N_{ℓ,i}` contributes none.
- *For `d' = d`, text subspace:* `π` is the *region-aware shift map* — identity on the Left region (`v < p`) and `shift(·, n)` on the Right region (`v ≥ p`). The Right branch of `π` closes within subspace `s_C`: for every `v ∈ V_{s_C}(d)` with `v ≥ p`, by OrdAddHom (b clause, ASN-0082) applied to `shift(v, n) = v ⊕ δ(n, m_C)` (a displacement with `δ(n, m_C)_1 = 0`), `subspace(shift(v, n)) = subspace(v) = s_C`, so `shift(v, n) ∈ V_{s_C}(d')`. `N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n}` is the set of newly placed V-positions in `V_{s_C}(d')` whose image `a_k` happens to lie in `coverage(Σ'.L(ℓ).e_i)`.

The derivation tracks `project(ℓ, i, d, ·)` through each intermediate state of the substrate decomposition. Let `e_i := Σ.L(ℓ).e_i` denote the slot's endset; LP3★ (MultiStepCoverageInvariance; ASN-0098) gives `coverage(Σ_j.L(ℓ).e_i) = coverage(e_i)` at every intermediate `Σ_j`, so we write `coverage(e_i)` unambiguously throughout.

Step 0 — pre-state:

  `P_0 := project(ℓ, i, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e_i)}`

Partition `P_0` into:
- `P_0^L := {v ∈ P_0 : subspace(v) = s_C ∧ v < p}` (Left contributions)
- `P_0^R := {v ∈ P_0 : subspace(v) = s_C ∧ v ≥ p}` (Right contributions)
- `P_0^{s_L} := {v ∈ P_0 : subspace(v) = s_L}` (link-subspace contributions)

By S3★-aux (SubspaceExhaustiveness; ASN-0047), `dom(M(d)) ⊆ V_{s_C}(d) ∪ V_{s_L}(d)`, so `P_0 = P_0^L ∪ P_0^R ∪ P_0^{s_L}` is exact.

Step 1 — after each K.α firing:

  `project(ℓ, i, d, Σ_α_k) = project(ℓ, i, d, Σ_α_{k−1}) = … = P_0`

by LP6 (ContentAllocationInvariance; ASN-0098): K.α modifies only C and has frame `(A d :: M'(d) = M(d))`, so the projection is unchanged at every K.α intermediate.

Step 2 — after K.μ⁻ (when fired). K.μ⁻ retains `R_kept := L ∪ V_{s_L}(d)` where `L := {v ∈ V_{s_C}(d) : v < p}`; the Right region is removed from `dom(M(d))`. By LP10 (ContractionMonotonicity; ASN-0098), the projection contracts to its intersection with the kept domain:

  `project(ℓ, i, d, Σ_μ⁻) = P_0 ∩ R_kept = P_0^L ∪ P_0^{s_L}`

— the Right contributions are temporarily removed; Left and link-subspace contributions are preserved.

When K.μ⁻ does *not* fire (the content-subspace Right region is empty), `Σ_μ⁻` does not exist as a distinct state and the flow passes from `Σ_α_n` directly to `Σ_μ⁺`. In every K.μ⁻-omitted case `P_0^R = ∅`: the empty-content-subspace cases have `V_{s_C}(d) = ∅`, so no V-position satisfies `v ∈ V_{s_C}(d) ∧ v ≥ p`; the append case has `p_m = N + 1`, so no `v ∈ V_{s_C}(d)` (with last components in `{1, …, N}`) satisfies `v ≥ p`. The projection at the post-Step-1 state is therefore `P_0 = P_0^L ∪ P_0^R ∪ P_0^{s_L} = P_0^L ∪ P_0^{s_L}` — identical in form to the K.μ⁻-fired formula above. Steps 3 and 4 below proceed uniformly from this expression regardless of whether Step 2 fired.

Step 3 — after K.μ⁺. K.μ⁺ adds two disjoint sets of new V-positions:
- *Insertion positions* `I := {shift(p, k) : 0 ≤ k < n}`, each mapping `shift(p, k) ↦ a_k`
- *Shifted-right positions* `S := {shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p}`, each mapping `shift(v, n) ↦ M(d)(v)`

By LP9 (ExtensionMonotonicity; ASN-0098), the projection grows by exactly those new V-positions whose image lies in `coverage(e_i)`:

  `project(ℓ, i, d, Σ_μ⁺) = project(ℓ, i, d, Σ_μ⁻) ∪ N_I ∪ N_S`

where:
- `N_I := {shift(p, k) : 0 ≤ k < n ∧ a_k ∈ coverage(e_i)}` — Insertion contributions
- `N_S := {shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p ∧ M(d)(v) ∈ coverage(e_i)} = {shift(v, n) : v ∈ P_0^R}` — Shifted-right contributions

Substituting:

  `project(ℓ, i, d, Σ_μ⁺) = P_0^L ∪ P_0^{s_L} ∪ N_I ∪ {shift(v, n) : v ∈ P_0^R}`

Step 4 — after each K.ρ firing:

  `project(ℓ, i, d, Σ_ρ_k) = project(ℓ, i, d, Σ_μ⁺) = … = project(ℓ, i, d, Σ')`

by LP14 (ProvenanceRecordingInvariance; ASN-0098): K.ρ modifies only R and has frame `(A d :: M'(d) = M(d))`, so the projection is unchanged.

Combining:

  `project(ℓ, i, d, Σ') = P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L} ∪ N_I`

Identifying π as the region-aware shift map (identity on Left and link-subspace contributions, `shift(·, n)` on Right contributions) and setting `N_{ℓ,i} := N_I`:

  `π(P_0) := P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L}`

  `project(ℓ, i, d, Σ') = π(project(ℓ, i, d, Σ)) ∪ N_{ℓ,i}`

The K.μ⁻ step's "temporary retraction" of `P_0^R` from the intermediate projection is *cancelled* by K.μ⁺'s reintroduction of those V-positions at shifted addresses: the Right contributions disappear at `Σ_μ⁻` (because their V-positions are removed from `dom(M(d))`) and reappear at `Σ_μ⁺` at the V-positions `shift(v, n)` (with the same I-addresses `M(d)(v)`). The cancellation is exact because K.μ⁺ adds *exactly* the shifted V-positions `{shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p}` with the same image mapping, so every Right contribution to the projection is recovered at its shifted V-position.

*Consequence — preservation of pre-state discoverability:*

  `discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ')`

Every pre-state V-position contributing to projection is mapped (by π or identity) to a post-state V-position with the same I-address, so the non-emptiness of any pre-state projection slot transfers to the post-state.

*Consequence — fresh-address discoverability (the `N_{ℓ,i}` term):* A fresh `a_k` lies in `coverage(Σ'.L(ℓ).e_i)` only if the endset includes `a_k` in its span coverage. For *tight* endsets — those bounded to address ranges already populated at the time the endset was incorporated — this cannot happen: by LP19a (TightFreshness; ASN-0098), the freshness of `a_k` against the endset's incorporation state places it outside the tight coverage, so `N_{ℓ,i} = ∅`. For non-tight endsets, a fresh `a_k` may indeed land in coverage, and this is by intent: non-tight endsets are designed to capture later-allocated content within their declared range. LP19 (TightEndsetBoundaryExclusion; ASN-0098) specialises this to K.μ⁺ steps of the composite: V-positions newly added by K.μ⁺ whose image was freshly allocated by a prior K.α step of the composite are excluded from any pre-existing tight endset's projection.

### Provenance (R, P4★, P4a, P7a)

The provenance relation `R ⊆ T_elem × E_doc` (ASN-0047) records which documents have ever contained which I-addresses. INSERT's effect on R is `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`, realised by `n` K.ρ firings in step 4 of the substrate composite.

The composite-boundary coupling J1★ (ExtensionRecordsProvenanceContentSubspace; ASN-0047) requires every newly-arranged content-subspace I-address with no pre-state arrangement under `d` to have its provenance pair in `R'`. For Insertion positions, the freshly allocated `a_k` was not in any `ran(M(d))` pre-state. At the moment of `a_k`'s K.α firing, the freshness precondition `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)` holds by SubsequentEmissionFreshness (ASN-0093), with FirstEmissionFreshness covering the boundary case `m_d = 0`; by P0 (ContentPermanence; ASN-0047) applied along `Σ →* Σ_k`, this lifts to `a_k ∉ dom(Σ.C)`; and by pre-state S3★ (GeneralizedReferentialIntegrity; ASN-0047), `ran(M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`, whence `a_k ∉ ran(M(d))`. So J1★ requires `(a_k, d) ∈ R'` — discharged by step 4. For Shifted-right positions, `M(d)(v) = a` was already arranged at some content-subspace V-position `v ∈ dom(M(d))`, so J1★'s requirement of "not previously arranged in d's content subspace" is false, and no new R entry is required for these. The pair `(a, d)` was already in R via the historical state (preserved by P2, ProvenancePermanence; ASN-0047).

J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047) requires every new R' entry to correspond to a newly-arranged content-subspace I-address. Each `(a_k, d)` added in step 4 corresponds to the placement `shift(p, k) ↦ a_k` introduced by step 3's K.μ⁺ — satisfied.

P4★ (ProvenanceBoundsContentSubspace; ASN-0047): `Contains_C(Σ') ⊆ R'`. Pre-state P4★ gives `Contains_C(Σ) ⊆ R`. The post-state's content-subspace arrangement adds n new pairs (one per Insertion position with image `a_k`); each is in R' via step 4. So P4★ holds.

P4a (TraceWitnessing; ASN-0047): every `(a, d) ∈ R'` admits a witness state — a *composite boundary* in the trace `Σ₀ →* … →* Σ_n = Σ'` — at which `a` was in d's content-subspace range. The witness is quantified over boundary states `{Σ₀, …, Σ_n}`, not over states interior to a composite. For pre-state `(a, d) ∈ R`, P4a inherits. For each new `(a_k, d)` added in step 4, the witness is the composite boundary `Σ'` itself (`= Σ_n`): step 4's K.ρ firings frame M (`(A d :: M'(d) = M(d))`), so the Insertion placement `shift(p, k) ↦ a_k` introduced by step 3's K.μ⁺ survives to `Σ'`, keeping `a_k ∈ ran(M'(d))` at that boundary.

P7 (ProvenanceGrounding; ASN-0047): `(A (a, d') ∈ R' :: a ∈ dom(C'))` — every R' entry's first component is in the post-state content store. For pre-state pairs `(a, d') ∈ R`, P7 inherits: pre-state P7 gives `a ∈ dom(C)`, and `dom(C) ⊆ dom(C')` by P0 (ContentPermanence; ASN-0047). For each new R' entry `(a_k, d)` added by step 4's K.ρ firings: K.ρ's own precondition requires `a_k ∈ dom(C)`, so the K.ρ(a_k, d) firing follows step 1's K.α(a_k), which committed `a_k` to `dom(C)`; since `a_k` is never removed thereafter, `a_k ∈ dom(C')` at the post-state. P7 holds.

P7a (ProvenanceCoverage; ASN-0047): every `a ∈ dom(C')` has some `d` with `(a, d) ∈ R'`. Pre-state P7a covers `dom(C)`; each new `a_k ∈ dom(C') \ dom(C)` is paired with `d` in step 4.

### What is *not* allocated

INSERT does *not* allocate new documents (`dom(M') = dom(M)`), does *not* allocate new links (`L' = L`), and does *not* allocate I-addresses outside `dom(C)`'s content subspace (every `a_k` has `subspace_I(a_k) = s_C`). The allocation footprint is precisely `n` content-subspace I-addresses scoped to `d`.

## Atomicity and Canonical Order

Nelson requires that after INSERT, the system is in "canonical order" — every structural invariant holds simultaneously. INSERT is a substrate composite governed by ValidComposite★ (ASN-0047), and its atomicity is the *composite-boundary* form: per-state invariants (Class (a) of ASN-0047 — S2, S3★, S8-depth, S8a, D-CTG★, D-MIN★, D-SEQ★, L0, L12, L14, …) hold at *every* state including each intermediate within the composite; composite-boundary properties (Class (b) — P4★, P4a, P7a) and the coupling constraints (J0, J1★, J1'★) hold at the boundary between Σ and Σ'.

Composite-level atomicity is *definitional* — not an extra property the substrate must separately supply. By ValidComposite★, INSERT's elementary transitions form a *contiguous* finite sequence `Σ = Σ₀ → Σ₁ → … → Σₙ = Σ'`; transitions are totally ordered (SequentialTransitionAxiom; ASN-0093), so no foreign elementary transition interleaves between INSERT's steps, and Σ' is determined by the contract.

We verify that each intermediate state in INSERT's substrate decomposition satisfies the per-state invariants.

Several per-state invariants of ASN-0047's ExtendedReachableStateInvariants are preserved by frame at every intermediate of INSERT's decomposition, because the state components they constrain are never modified. By the state component they range over:

- *Entity-set invariants* — P8 (EntityHierarchy), NodeLineage (NodeDescentFromBootstrap), ActivatedEmission (every non-node entity is an emission of an activated entity-level sub-allocator), M0 (DocumentTumblerWellFormed; ASN-0093). The entity set E (equivalently `dom(M)` for documents under ValidComposite★) is unchanged at every intermediate: no K.δ fires. Each invariant is a predicate over E (or `dom(M)`) and so holds at every intermediate by inheritance from the pre-state. ActivatedEmission in particular is preserved by the frame `E' = E` (INS.frame.E): INSERT fires no K.δ, so no new entity enters E, and the pre-state witness — an activated entity-level sub-allocator `A` with `e ∈ dom(A)` — survives unchanged for every `e ∈ E`.
- *Content-allocation invariants* — S4 (OriginBasedIdentity; ASN-0036). S4 ranges over `dom(C)`, not over E or `dom(M)`, so the "no K.δ fires" frame reasoning above does not apply — INSERT extends `dom(C)` by `n` fresh addresses via K.α firings, and S4 must be discharged against the changed `dom(C)` at every intermediate. The discharge proceeds in three parts at the `k`-th K.α intermediate state Σ_{α,k}. (i) *Pre-state pairs remain distinct.* For `a₁, a₂ ∈ dom(Σ.C)`, pre-state S4 gives `a₁ ≠ a₂`; P0 (ContentPermanence; ASN-0047) keeps both in `dom(Σ_{α,k}.C)` with the same identities, so distinctness transfers unchanged. (ii) *New addresses are distinct from pre-state addresses.* Each freshly emitted `a_j` (for `0 ≤ j ≤ k`) satisfies K.α's freshness precondition `a_j ∉ dom(Σ_{α,j−1}.C) ∪ dom(Σ_{α,j−1}.L)` at its own emission state (by SubsequentEmissionFreshness, with FirstEmissionFreshness for the boundary case `m_d = 0`; ASN-0093), so `a_j ∉ dom(Σ.C)` by P0 along `Σ →* Σ_{α,j−1}`. (iii) *The freshly emitted addresses are pairwise distinct.* For any pair `0 ≤ i < j ≤ k`, ChainEnumerationInjectivity (ASN-0093) supplies `a_i = t_{m_d + i + 1} < t_{m_d + j + 1} = a_j` under the tumbler order T1 (strict monotonicity of the chain enumeration), so `a_i ≠ a_j` by T1 irreflexivity. Together (i)–(iii) discharge S4 at every K.α intermediate. The subsequent K.μ⁻, K.μ⁺, and K.ρ firings have frame `C' = C` and so inherit S4 trivially.
- *Link-store invariants* — L0 (SubspacePartition), L1 (LinkElementLevel), L1a (LinkScopedAllocation), L1b (LinkElementFieldDepth), L1c (LinkAllocatorConformance), L3 (NEndsetStructure), L-fin (LinkStoreFiniteness), L12 (LinkImmutability), CL-OWN (LinkSubspaceOwnership), CL-UNIQ (LinkSubspacePositionUniqueness). The link store L is unchanged at every intermediate: no K.λ fires. L1, L1a, L1b, L1c, L3, L-fin, and L12 range over `dom(L)` alone and inherit from the pre-state. L0 is the exception: its first conjunct `(A a ∈ dom(L) :: subspace_I(a) = s_L)` ranges over the unchanged `dom(L)` and inherits trivially, but its second conjunct `(A a ∈ dom(C) :: subspace_I(a) = s_C)` ranges over `dom(C)`, which the K.α firings extend. For each freshly emitted `a_k`, `subspace_I(a_k) = s_C` by DisjointSubAllocatorChains (ASN-0093) — `a_k` is an output of `d`'s content sub-allocator `A_C(d)`; pre-existing entries inherit from the pre-state. So L0's content clause holds at every K.α intermediate, and the subsequent K.μ⁻, K.μ⁺, K.ρ firings leave `dom(C)` unchanged (`C' = C`) and inherit it. CL-OWN and CL-UNIQ constrain link-subspace V-position mappings; the link subspace `V_{s_L}(d)` is preserved by every step (K.α and K.ρ leave M untouched; K.μ⁻ retains `V_{s_L}(d)` with `n'_{s_L} = n_{s_L}`; K.μ⁺ adds only content-subspace positions per the ASN-0047 amendment). The link-subspace mappings are therefore unchanged across the composite, and CL-OWN, CL-UNIQ inherit from the pre-state.
- *Content-store finiteness* — C-fin (ContentStoreFiniteness). The pre-state has `|dom(C)| < ∞`; each K.α firing adds exactly one address; n is finite. So `|dom(C')| ≤ |dom(C)| + n < ∞` at every intermediate.
- *Subspace exhaustiveness* — S3★-aux (SubspaceExhaustiveness). At every intermediate, `V_{s_C}(d)` and `V_{s_L}(d)` together cover `dom(M(d))` because the K.μ⁻ and K.μ⁺ steps add and remove only positions with subspace ∈ {s_C, s_L} (the K.μ⁺ amendment restricts new V-positions to `subspace = s_C`; K.μ⁻'s per-subspace retention preserves the same partition). Other documents' arrangements are unchanged. So S3★-aux holds.

- *After each of the `n` K.α firings of step 1.* `dom(C)` extends by one fresh `a_k` with `origin(a_k) = d`; `M(d)` is unchanged. Per-state invariants on M (S2, S3★, S8a, S8-depth, S8-fin, S8★, D-CTG★, D-MIN★, D-SEQ★) hold trivially because M is unchanged. S8a in particular continues to hold of every pre-existing V-position by hypothesis on the pre-state; S8-depth continues to fix the same `m_C` (resp. `m_L`) per subspace because `dom(M(d))` is unchanged. S8★ (PerSubspaceSpanDecomposition; ASN-0047) inherits from the pre-state because `M` is unchanged by K.α: the per-subspace restrictions and their maximal-run decompositions are identical to the pre-state's, which held S8★ by hypothesis. Per-state invariants on C (C-fin, S7a, S7b, C1b, C1c) hold because each `a_k` is a well-formed content-subspace address with `zeros(a_k) = 3` and `#E(a_k) ≥ 2` reached by `A_C(d)`'s T10a-conforming inc-chain, satisfying the per-address conditions. P6 (ExistentialCoherence; ASN-0047) holds at this intermediate because `origin(a_k) = d ∈ dom(M)` by INSERT's precondition, and `E` (equivalently `dom(M)` for documents) is unchanged at every intermediate by INS.frame.E. P7 (ProvenanceGrounding; ASN-0047) holds at this intermediate because R is unchanged by K.α; for each pre-state pair `(a, d') ∈ R`, `a ∈ dom(C)` by pre-state P7 and `dom(C)` only grows. L14 holds because `a_k ∉ dom(L)` (K.α's freshness precondition). L0's content clause holds because `subspace_I(a_k) = s_C` (DisjointSubAllocatorChains, ASN-0093 — `a_k` is an output of `A_C(d)`), so every entry of the extended `dom(C)` still carries subspace identifier `s_C`. The composite-boundary properties (J0, J1★, P4★) are not yet required to hold at this intermediate — `a_k` is in `dom(C)` but not yet placed, which J0 would forbid at a composite boundary, but the intermediate is interior to the composite.

- *After step 2's K.μ⁻ (when fired).* `V_{s_C}(d_intermediate)` reduces to the Left prefix `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}`, which is sequential, contiguous, and starts at the minimum — D-SEQ★, D-CTG★, D-MIN★ all hold on the content subspace. Each retained position is a subset of the pre-state's `V_{s_C}(d)`; S8a (zero-free, depth `≥ 2`, all components positive) inherits unchanged from the pre-state, and every retained position has length exactly `m_C`, so S8-depth holds in subspace `s_C` with `m_C` unchanged. The link subspace is retained verbatim (`n'_{s_L} = n_{s_L}`): `V_{s_L}(d_intermediate) = V_{s_L}(d)` pointwise (positions and images alike). Per-state invariants on the link subspace at the intermediate are inherited bit-for-bit from the pre-state: S8a and S8-depth (with `m_L` unchanged) follow from the unchanged set; D-CTG★, D-MIN★, and D-SEQ★ on `V_{s_L}(d_intermediate)` each follow from their pre-state forms applied to the unchanged set — D-CTG★ because the same positions retain the same contiguity structure under the V-ordering, D-MIN★ because `min(V_{s_L}(d_intermediate)) = min(V_{s_L}(d))` is preserved, and D-SEQ★ because the enumeration `V_{s_L}(d) = {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n_{s_L}}` carries over unchanged. CL-OWN and CL-UNIQ on the link-subspace mappings also inherit verbatim. S8-fin holds because `dom(M(d_intermediate))` is a subset of the finite pre-state `dom(M(d))`. S3★ holds because retained images are unchanged and S3★ held of the pre-state. S8★ (PerSubspaceSpanDecomposition; ASN-0047) holds at this intermediate: the content subspace `V_{s_C}(d_intermediate)` is the contiguous prefix `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}` (empty when `p_m = 1`), and its single-subspace restriction `M(d_intermediate)|_{V_{s_C}(d_intermediate)}` admits a finite maximally-merged decomposition by C1a (RestrictionDecomposition; ASN-0058) — whose preconditions hold here (functionality from S2, finiteness from S8-fin, single-subspace induced domain of common depth `m_C` from S8-depth), lifting M11/M12 to the restriction; the link subspace is retained verbatim and inherits its trivial length-1 decomposition from the pre-state. P4★ (composite-boundary) would not hold at this intermediate if it required all post-state ran(M(d)) entries to be in R — but R has not yet been extended; the obligation is delegated to the composite boundary.

- *After step 3's K.μ⁺.* `V_{s_C}(d_intermediate)` extends to the full post-state `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, satisfying D-SEQ★, D-CTG★, D-MIN★. Every newly added V-position is one of the Insertion positions `shift(p, k) = [s_C, 1, …, 1, p_m + k]` for `0 ≤ k < n` or one of the Shifted-right positions `shift(v, n) = [s_C, 1, …, 1, v_m + n]` for `v ∈ V_{s_C}(d)` with `v ≥ p`. For each, we verify S8a and S8-depth explicitly:
   - *Insertion positions.* S8a and S8-depth on `shift(p, k)` for `0 ≤ k < n` are established by the `shift(p, k)` argument in §Post-state V-position well-formedness (the S8a and S8-depth bullets); since `M(d_intermediate)` coincides with the post-state `M'(d)`, that derivation applies verbatim here.
   - *Shifted-right positions.* For `v = [s_C, 1, …, 1, v_m] ∈ V_{s_C}(d)` with `v ≥ p`, the pre-state S8a ensures `v_m ≥ 1`. `shift(v, n) = v ⊕ δ(n, m_C)` has length `m_C` (S8-depth preserved), subspace `s_C` (OrdAddHom (b), ASN-0082), leading components all `1`, and final component `v_m + n ≥ 1 + 1 = 2 > 0`. So `zeros(shift(v, n)) = 0` and S8a holds.

  S2 (ArrangementFunctionality) holds at this intermediate: since `M(d_intermediate)` coincides with the post-state `M'(d)`, the pairwise region-disjointness argument of §Arrangement functionality (Left, Insertion, Shifted-right have disjoint last-component ranges, with Shifted-right source uniqueness by TS2; ASN-0034) shows no V-position receives two distinct images. Every newly arranged content-subspace I-address is in `dom(C)` already (the freshly allocated `a_k` from step 1, or the pre-existing M(d)(v) for Shifted-right) — S3★ holds. S8-fin holds because `dom(M(d_intermediate))` is finite — it grows by at most `n + |R|` positions where `R` is the pre-state Right region, both finite. S8★ (PerSubspaceSpanDecomposition; ASN-0047) holds at this intermediate because the K.μ⁺ step is the last substrate step that modifies `M`: the intermediate arrangement `M(d_intermediate)` coincides with the post-state `M'(d)`, so S8★ here is exactly the post-state S8★ discharged in §Per-subspace span decomposition (S8★) via C1a on the content subspace plus the trivial length-1 decomposition on the link subspace. J0 (composite-boundary) is now satisfied: each `a_k ∈ dom(C')` has a placement at `shift(p, k)`.

- *After each of the `n` K.ρ firings of step 4.* R extends by one `(a_k, d)` pair; the final K.ρ intermediate *is* the composite boundary `Σ'`, the state at which the provenance obligations come due. The composite-boundary couplings and properties J1★, P4★, P4a, P7a — together with the per-state P7 across each K.ρ commit — are evaluated at exactly this boundary state, where the provenance discharge applies. S8★ (PerSubspaceSpanDecomposition; ASN-0047) holds at each K.ρ intermediate because K.ρ frames `M` (`M' = M`): the arrangement and hence its per-subspace decompositions are identical to the end-of-step-3 (= post-state) arrangement, where S8★ was already discharged.

The decomposition is admissible under ValidComposite★ because (i) every elementary transition's per-step precondition is met at its intermediate state, and (ii) the composite-boundary coupling constraints J0, J1★, J1'★ hold at the boundary `Σ →* Σ'`.

This also discharges P3 (ExtendedTransitionInvariants; ASN-0047), the sole *composite-transition* obligation, which ASN-0047 states as the synthesis `P0 ∧ P1 ∧ P2 ∧ L12`. Each conjunct holds between the initial state Σ and the final state Σ': P0 (ContentPermanence — `dom(C) ⊆ dom(C')` with value preservation) follows from step 1's K.α firings extending `dom(C)` by fresh addresses while the K.μ⁻/K.μ⁺/K.ρ frames leave existing entries untouched; P1 (EntityPermanence — `E ⊆ E'`) follows from INS.frame.E (`E' = E`, no K.δ); P2 (ProvenancePermanence — `R ⊆ R'`) follows from step 4's K.ρ firings being purely additive on R; and L12 (LinkImmutability — `dom(L) ⊆ dom(L')` with value preservation) follows from INSERT firing no K.λ, so `L' = L`. Their conjunction is exactly P3, so the composite transition `Σ →* Σ'` satisfies ExtendedTransitionInvariants.

The composite is *not* admissible in alternative decompositions that would break a per-state invariant at an intermediate:

- *K.μ⁺ before K.α* (place `a_k` before allocating it). K.μ⁺'s precondition requires `a ∈ dom(C)` for every new mapping. The intermediate before K.α has `a_k ∉ dom(C)`, so K.μ⁺ cannot fire — the decomposition is ill-typed.

- *K.μ⁺ without prior K.μ⁻ in an interior insertion.* K.μ⁺ extends `dom(M(d))`; it preserves existing mappings. To map both `[s_C, 1, …, 1, p_m]` to `M(d)([s_C, 1, …, 1, p_m])` (the original content) and to `a_0` (the new content) would violate S2 — per-state functionality. So shift via K.μ⁻ + K.μ⁺ is *required*, not an implementation choice.

- *K.μ⁻ retaining strictly less than the Left prefix.* Both retention parameters of K.μ⁻ are admissible across `{0, 1, …, n_S}` per K.μ⁻'s precondition. A decomposition with `n'_{s_C} = 0` (full content-subspace shrinkage) is well-typed: the intermediate has `V_{s_C}(d_intermediate) = ∅` and satisfies D-CTG★, D-MIN★, D-SEQ★ vacuously. The subsequent K.μ⁺ may re-add the full sequential run `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` starting from the minimum, mapping each position to the appropriate I-address. The K.μ⁺ precondition requires only that the resulting M'(d) satisfies D-CTG★ and D-MIN★ — it does not require new positions to be added only at the high end. Such alternative decompositions are admissible and reach the same Σ'.

The post-state Σ' is *uniquely determined* by the operation contract; the substrate decomposition that realises it is not. We verify uniqueness component by component.

  *Content store.* Every admissible decomposition fires exactly `n` K.α steps in their forced order (per the K.α strict-order argument below — the `k`-th firing must produce the determined chain element `t_{m_d + k + 1}` of `A_C(d)`). So `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` with each `a_k` determined uniquely by the pre-state's chain index `m_d` (read from `Σ.C`) and the inputs; the value `C'(a_k) = v_k` is set by the K.α firing's value parameter `v_k` from INSERT's input sequence. The frame of every other elementary step (K.μ⁻, K.μ⁺, K.ρ) leaves C unchanged, so `C'(a) = C(a)` for `a ∈ dom(C)` is preserved by composition.

  *Arrangement of `d`.* At the boundary, `V_{s_C}(d')` equals Left ∪ Insertion ∪ Shifted-right, with no fourth region — this is the exhaustiveness clause INS.M-exhaustive, established at the effect specification (§The Operation: Formal Contract) from the composite construction. When K.μ⁻ fires it retains exactly the Left prefix and removes the Right region, and step 3's K.μ⁺ adds exactly the Insertion and Shifted-right positions (in subspace `s_C`, per the K.μ⁺ amendment); when K.μ⁻ is omitted the Right region of the pre-state `V_{s_C}(d)` — the set `{v ∈ V_{s_C}(d) : v ≥ p}` — is empty (the empty-content-subspace cases have `V_{s_C}(d) = ∅`, so no V-position satisfies `v ≥ p`; the append case has `p_m = N + 1`, so no `v ∈ V_{s_C}(d)` with last components in `{1, …, N}` satisfies `v ≥ p`), so the preserved pre-state positions are exactly Left, the Shifted-right region is empty, and K.μ⁺ adds exactly Insertion. No other elementary step can introduce an `s_C` position, since K.α and K.ρ frame `M` (`M' = M`, ASN-0047) and K.μ⁻ only removes. These three regions and the mapping on each are fully determined by `p`, `n`, the determined `a_k`, and the pre-state `V_{s_C}(d)`. Any admissible decomposition reaches this M'(d) at the boundary because the K.μ⁻ + K.μ⁺ pair must (i) remove every pre-state position with `v ≥ p` and reintroduce it at `shift(v, n)` (forced by INS.M-shift), (ii) introduce each Insertion position `shift(p, k) ↦ a_k` (forced by INS.M-insert), and (iii) leave the Left region intact (forced by INS.M-left). Whether the K.μ⁻ retention parameter is `n'_{s_C} = p_m − 1` (retain Left) or `n'_{s_C} = 0` (retain nothing), the K.μ⁺ step (or steps) must re-add exactly the missing positions to satisfy the boundary, so the final M'(d) is identical in either decomposition.

  *Arrangement of other documents.* `M'(d') = M(d')` for `d' ≠ d` by every elementary step's frame, regardless of decomposition.

  *Other components.* `L' = L`, `E' = E`, `dom(M') = dom(M)` by the frame of every elementary step in the composite (no K.λ, no K.δ fires); `R' = R ∪ {(a_k, d) : 0 ≤ k < n}` because step 4 adds exactly these `n` pairs in some order — set union being order-independent, R' is identical across decompositions.

Two representative comparisons confirm: a decomposition with `n'_{s_C} = p_m − 1` (the canonical choice) and one with `n'_{s_C} = 0` (full shrinkage) reach different intermediate states (the latter has empty V_{s_C} at the intermediate, the former retains the Left prefix), but both arrive at the same Σ'. K.μ⁻ retention parameters may range over `{0, 1, …, p_m − 1}` for the content subspace, K.μ⁺ may be split across multiple firings, and K.α + K.ρ firings may be reordered to a degree (described below), provided each intermediate satisfies the per-state invariants.

Among the elementary firings, three forced orderings arise from K.α firings and a fourth arises from K.μ⁻'s relationship to K.μ⁺ when K.μ⁻ fires. Every remaining pair commutes at the per-state level.

The three K.α-induced forced orderings:

- *K.α(a_k) before K.α(a_{k+1}).* K.α's subsequent-emission predicate (ASN-0093) computes its output as `inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`, consulting `dom(C)`. The `(k+1)`-th firing therefore depends on the `k`-th firing's commit to `dom(C)` (sequenced by SequentialTransitionAxiom; ASN-0093) — a side-effect dependency that forces their order.

- *K.α(a_k) before K.μ⁺ placing `a_k`.* K.μ⁺'s precondition requires each new mapping's image to be in `dom(C)`. If K.μ⁺ attempted to add `shift(p, k) ↦ a_k` before the K.α firing that produces `a_k`, the intermediate would have `a_k ∉ dom(C)` and the per-step precondition would fail.

- *K.α(a_k) before K.ρ(a_k, d).* K.ρ's precondition requires `a ∈ dom(C)`. K.ρ(a_k, d) firing before K.α(a_k) would find `a_k ∉ dom(C)` and the per-step precondition would fail.

The fourth, conditional on K.μ⁻ firing:

- *K.μ⁻ before K.μ⁺* (whenever K.μ⁻ fires in the composite — that is, for interior insertions and for `j = 0` insertions, where the Right region is non-empty and `n'_{s_C} < n_{s_C}` is required). K.μ⁺'s extension precondition requires `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))` — that is, K.μ⁺ preserves the image of every V-position already in the document's arrangement. Consider firing K.μ⁺ before K.μ⁻ for any interior insertion: at least one position `v ∈ V_{s_C}(d)` with `v ≥ p` is in the pre-K.μ⁺ domain `dom(M(d))` and would need to receive a new image under K.μ⁺. Concretely, at `j ∈ {0, …, N−1}` the position `shift(p, 0) = p` (when `j = 0`) or `p` itself (interior) is in pre-state `dom(M(d))` with `M(d)(p) ≠ a_0`, so K.μ⁺ attempting to add `p ↦ a_0` would violate its functional-extension precondition. K.μ⁻ must fire first to remove the Right region from `dom(M(d))`, so that K.μ⁺'s subsequent additions extend a domain disjoint from the Right region. The forced ordering is conditional: when K.μ⁻ is omitted (the `j = N` append case and the empty pre-state case), there is no fourth ordering, because K.μ⁺ adds positions only outside the existing domain.

These forced orderings determine INSERT's boundary obligations; every other interleaving of the elementary steps reaches the same Σ'. No per-state invariant is sensitive to the relative order of the remaining steps, and the coupling constraints J0, J1★, J1'★ are obligations on INSERT's own boundary `(Σ, Σ')` — discharged there, where every `a_k` is both placed by K.μ⁺ and recorded by K.ρ, regardless of internal order — so the canonical placement of the K.ρ firings at the end of steps 1–4 is expository, not mandatory.

This is what Nelson calls "all changes, once made, leave the file remaining in canonical order, which was an internal mandate of the system." Implementations realise the composite via transactional sequencing, locking, copy-on-write, or log-and-commit — but the choice of decomposition is below the level of abstraction at which INSERT is specified. External observers see the composite boundary; the intermediate states are not externally observable.

## Weakest-Precondition Analysis

The verification above proceeds forward — from preconditions and substrate effects to the post-state. We can also reason backward from a desired postcondition to the pre-state condition that secures it. This is Dijkstra's `wp` calculus, and we apply it to two non-trivial postconditions.

**Discoverability preservation.** Consider the postcondition `discoverable_from(ℓ, d, ·)` for a fixed link `ℓ ∈ dom(L)` and the operation's target document `d`. We compute:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), discoverable_from(ℓ, d, ·))`

By LP12 (DiscoverabilityCharacterisation; ASN-0098), `discoverable_from(ℓ, d, Σ')` is equivalent to `(E i : coverage(Σ'.L(ℓ).e_i) ∩ ran(Σ'.M(d)) ≠ ∅)`. By LP3★ (MultiStepCoverageInvariance; ASN-0098), `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` since INSERT does not alter `L`. By the post-state's M-effect, `ran(M'(d)) = ran(M(d)) ∪ {a_k : 0 ≤ k < n}` — the pre-existing range augmented by the freshly allocated I-addresses. The wp expands to:

  `(E i : coverage(Σ.L(ℓ).e_i) ∩ (ran(Σ.M(d)) ∪ {a_k : 0 ≤ k < n}) ≠ ∅)`

which distributes to:

  `discoverable_from(ℓ, d, Σ) ∨ (E i, k : 0 ≤ k < n : a_k ∈ coverage(Σ.L(ℓ).e_i))`

The second disjunct — fresh-address capture — collapses to `false` for any *tight* endset `e_i` (with `tight(e_i, Σ_{e_i})` evaluated at the state of `e_i`'s incorporation). LP19a (TightFreshness; ASN-0098) establishes that a freshly allocated `a_k` cannot lie in a tight endset's coverage, because `a_k ∉ dom(Σ_{e_i}.C) ∪ dom(Σ_{e_i}.L)` by Store Monotonicity★ and the freshness of K.α's emission against the operation's pre-state. Thus, when every slot of `Σ.L(ℓ)` is tight at its incorporation state, the wp simplifies to:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), discoverable_from(ℓ, d, ·)) ≡ discoverable_from(ℓ, d, Σ)`

— a non-trivial conclusion: discoverability of a tight-endset link from `d` is preserved exactly when it held at the pre-state. INSERT neither creates nor destroys discoverability for tight links; it is transparent to them.

**Provenance membership for a specific I-address.** Consider the postcondition `(a, d) ∈ R'` for a fixed I-address `a` and target document `d`. We compute:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), (a, d) ∈ R')`

By the post-state's R-effect, `R' = R ∪ {(a_k, d) : 0 ≤ k < n}` where `a_0, …, a_{n−1}` are the freshly allocated content addresses. Thus `(a, d) ∈ R'` holds iff `(a, d) ∈ R` or `a ∈ {a_0, …, a_{n−1}}`. The second disjunct depends on the K.α emission discipline: `a = a_k` for some `k` iff `a` is the `(m_d + k + 1)`-th element of the chain `A_C(d)` (where `m_d` is the chain index of the last emission already in `dom(Σ.C)` for origin `d`). For a fixed `a`, this is a structural predicate on the pre-state: either `a` lies in `dom(C)` already (and is *not* a freshly allocated address — the second disjunct fails) or `a` is one of the next `n` chain elements of `A_C(d)` that K.α will produce. The wp is therefore:

  `(a, d) ∈ R  ∨  a ∈ {next n chain elements of A_C(d) starting from chain index m_d + 1}`

where the second-disjunct chain elements are determined by `Σ.C` and the chain enumeration of `A_C(d)`. The pre-state condition is operationally decidable: the chain index `m_d` is recoverable from `Σ.C` via the chain enumeration, and the next `n` chain elements are then determined.

This wp captures both the substrate's effect on R and the structural determinism of the K.α firings — the pre-state condition is a Boolean combination of a pre-state predicate (`(a, d) ∈ R`) and a substrate-derivable property (chain membership), reflecting INSERT's combined provenance-recording and fresh-allocation behaviour.

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

*Corollary (cross-document allocation independence).* If two distinct documents `d_1 ≠ d_2` each invoke INSERT with the same value sequence `⟨v_0, …, v_{n−1}⟩` at any positions, they produce two disjoint sequences of fresh I-addresses `⟨a_0^{(1)}, …, a_{n−1}^{(1)}⟩` and `⟨a_0^{(2)}, …, a_{n−1}^{(2)}⟩` with `origin(a_k^{(1)}) = d_1 ≠ d_2 = origin(a_k^{(2)})`. The two address sets are disjoint by SubAllocatorBundle (ASN-0047): `dom(A_C(d_1)) ∩ dom(A_C(d_2)) = ∅` for `d_1 ≠ d_2`. Value coincidence at `Σ.C(a_k^{(1)}) = Σ.C(a_k^{(2)})` is observable but does not produce identity — the system observes it as two unrelated allocations.

*Corollary (version chain independence).* When a version `d_v = inc(d_src, 1)` is derived from `d_src` (out of scope here, but a substrate operation under K.δ-IsDocument) and subsequently INSERT is invoked on `d_v`, the freshly allocated `a_k` come from `A_C(d_v)` with `origin(a_k) = d_v ≠ d_src`. The original `d_src` retains its allocated content unchanged; the version's new content has its own attribution. This corollary depends on the per-document sub-allocator existence guaranteed by SubAllocatorBundle for each `d_v ∈ E_doc` (ASN-0047).

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
| INS.chain-shift | For contiguous emissions of A_C(d), a_{i+j} = shift(a_i, j); in particular a_k = shift(a_0, k). Each inc(·,0) step equals shift(·,1) because chain elements are T4-valid (ChainElementT4Validity, ASN-0093), so sig = # (TA5-SigValid) and inc(·,0) bumps only the last component (TA5); the identification iterates under T4 preservation (TA5a) and uniform length under `inc(·, 0)` (TA5(c), ASN-0034) and composes by TS3 (ShiftComposition) | introduced |
| INS.C | dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}; C'(a_k) = v_k; ∀a ∈ dom(C): C'(a) = C(a) | introduced |
| INS.M-left | Text-subspace positions v < p in dom(M(d)) appear unchanged in M'(d) | introduced |
| INS.M-insert | M'(d)(shift(p, k)) = a_k for 0 ≤ k < n, with shift(p, 0) = p | introduced |
| INS.M-shift | For v ∈ V_{s_C}(d) with v ≥ p: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v); established directly by step-3 K.μ⁺'s specified effect, with shift order-preservation/injectivity by TS1/TS2 (ASN-0034) | introduced |
| INS.M-exhaustive | (A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right); the post-state's text-subspace domain contains no s_C positions beyond the three regions — established at the effect specification from the composite construction (K.α/K.ρ frame M, K.μ⁻ only removes, K.μ⁺ adds exactly Insertion ∪ Shifted-right) | introduced |
| INS.R | R' = R ∪ {(a_k, d) : 0 ≤ k < n}; discharges composite-boundary couplings J0, J1★, J1'★ (ASN-0047) | introduced |
| INS.frame.subspace | Non-content subspaces of d are unchanged (bidirectionally): {v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C}, and M'(d) agrees with M(d) pointwise on that set. No new non-s_C positions appear; no existing ones are removed | introduced |
| INS.frame.doc | Other documents' arrangements are unchanged: ∀d' ≠ d: M'(d') = M(d') | introduced |
| INS.frame.L | L' = L: link store entirely unchanged | introduced |
| INS.frame.E | E' = E: entity set unchanged (no K.δ in the decomposition); specialises to dom(M') = dom(M) for documents | introduced |
| INS.frame.dom | dom(M') = dom(M): no new documents registered | introduced |
| INS.inv.immut | Content immutability S0 (ASN-0036) / P0 (ASN-0047) preserved: dom(C) ⊆ dom(C') and pointwise values preserved | introduced |
| INS.inv.identity | Permanent I-address identity preserved: ∀a ∈ dom(C): a ∈ dom(C'), C'(a) = C(a), origin(a) unchanged | introduced |
| INS.inv.func | M'(d) is a function (S2 preserved); Left, Insertion, Shifted-right regions are pairwise disjoint by TumblerAdd component arithmetic, with Shifted-right source uniqueness by TS2 (ASN-0034) | introduced |
| INS.inv.refint | Referential integrity S3★ (ASN-0047) preserved: ran(M'(d)) ⊆ dom(C') ∪ dom(L') per-subspace, re-derived directly | introduced |
| INS.inv.seq | D-CTG★, D-MIN★, D-SEQ★ (ASN-0047) preserved in text subspace: V_{s_C}(d') is sequential with cardinality \|V_{s_C}(d)\| + n | introduced |
| INS.inv.depth | S8-depth (ASN-0036) preserved: non-empty case leaves m_C unchanged; empty case fixes m_C = m on first insertion. A later K.μ⁻ emptying V_{s_C}(d) makes S8-depth vacuous and permits a different depth on the next first-insertion | introduced |
| INS.inv.cross-subspace | Cross-subspace isolation: V_{s_L}(d') = V_{s_L}(d) with mappings unchanged | introduced |
| INS.inv.cross-doc | Cross-document isolation: arrangements of all d' ≠ d unchanged | introduced |
| INS.inv.coverage | Endset coverage unchanged for every link by LP3★ (ASN-0098): coverage depends only on L, which is preserved | introduced |
| INS.inv.discov | Pre-state discoverability preserved: every link discoverable from any document at Σ remains discoverable at Σ' | introduced |
| INS.proj | Projection-shift correspondence: project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i} where π is region-aware (identity on Left, shift-by-n on Right, identity for d' ≠ d and link subspace) and N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n} captures Insertion images whose fresh a_k lies in coverage; N_{ℓ,i} = ∅ for tight endsets by LP19a (ASN-0098) | introduced |
| INS.atomicity | INSERT's substrate composite preserves per-state invariants (Class (a) of ASN-0047) at every intermediate state; composite-boundary properties (Class (b) — P4★, P4a, P7a) and coupling constraints (J0, J1★, J1'★) hold at the boundary Σ →* Σ'. Elementary-level atomicity is supplied by SequentialTransitionAxiom (ASN-0093); composite-level atomicity is definitional under ValidComposite★ (ASN-0047) — INSERT's elementaries form a contiguous transition sequence, so Σ' is determined by the contract | introduced |
| INS.position | INSERT permitted at any valid position: N+1 valid positions under ValidInsertionPosition for non-empty V_{s_C}(d), plus single first-insertion position under ValidFirstInsertionPosition(d, p, m) with caller-chosen m ≥ 2 for empty case | introduced |
| INS.identity | INSERT creates fresh content identity: each a_k is a new allocation with origin(a_k) = d; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence | introduced |
| INS.identity.crossdoc | Cross-document allocation independence: two distinct documents inserting identical values produce disjoint fresh I-address sequences with distinct origins (by SubAllocatorBundle, ASN-0047) | introduced |
| INS.identity.version | Version chain independence: INSERT on a derived version d_v allocates from A_C(d_v) with origin = d_v ≠ origin of d_v's source document | introduced |
| INS.identity.tightsurv | Link survivability through value coincidence: tight endsets cannot accidentally capture freshly allocated content by LP19a (ASN-0098) | introduced |

## Open Questions

- An implementation must realize the abstract sequential transition model. What must it guarantee to recover canonical order after a partial failure during the substrate composite?
- What invariants must an analogous insertion operation preserve when the target is the link subspace rather than the text subspace?
- Is INSERT closed under composition with itself — i.e., if `Σ →INSERT→ Σ_1 →INSERT→ Σ_2`, is there always a single INSERT from `Σ` to `Σ_2`, or do the intermediate effects accumulate in ways that no single INSERT can reproduce?
- What does the abstract specification say about concurrent INSERTs targeting the same V-position from independent agents — must the system serialise them, and if so, on what basis is the order chosen?
- What derived properties of a document — current size, last-modified marker, total I-address footprint — does INSERT update, and which of these are part of the abstract state versus derivable from it?
