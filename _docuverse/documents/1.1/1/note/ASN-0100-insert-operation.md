# ASN-0100: INSERT Operation

*2026-05-27*

## The Question

When new content is inserted at a position in a document's Vstream, what is the precise post-state? Three sub-questions structure the inquiry:

- *What is allocated* — what new state appears in the content store and in the document's arrangement?
- *What shifts* — which existing V→I mappings change position, and by how much?
- *What invariants must hold after completion* — and atomically, with no observable intermediate state in which a *per-state* invariant is violated?

The answer must be sharp enough that an implementation can be measured against it, and abstract enough that two implementations meeting the spec are externally indistinguishable.

## Background: The Two-Stream Asymmetry

The foundation distinguishes two address spaces. The content store `C : T ⇀ Val` assigns content values to I-addresses; once `a ∈ dom(C)`, the binding is permanently fixed (S0). The arrangement `M(d) : T ⇀ T` assigns I-addresses to V-positions within document `d`; arrangements are mutable, but only in a controlled way.

INSERT acts on both, but asymmetrically. It *grows* `C` by appending fresh entries; it never alters existing entries, never reassigns I-addresses, never identifies one I-address with another. It *grows and rearranges* `M(d)`: existing content keeps its permanent I-address — and the value stored there — while only its V-position within `d` may shift. Since links attach to I-addresses (not V-positions), insertion cannot break them.

## The Operation's Inputs

INSERT takes three arguments: a target document `d ∈ dom(M)`, a V-position `p` at which the insertion begins, and a sequence of new content values `⟨v₀, v₁, …, v_{n−1}⟩` with `n ≥ 1`.

We restrict attention to the *content subspace* `s_C` of `d` — Nelson's text content.

The position `p` must be a *valid insertion position* in `V_{s_C}(d)`. We unpack this:

  `subspace(p) = s_C ∧ #p = m_C`

where `m_C` is the common depth of `V_{s_C}(d)` enforced by S8-depth (FixedDepthVPositions, ASN-0036) on the text subspace. For non-empty `V_{s_C}(d)` with current cardinality `N = |V_{s_C}(d)|`, the precondition is the binary predicate `ValidInsertionPosition(d, p)` (ASN-0036), which unpacks to:

  `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ N}`

**Notational convention** (used throughout this ASN). The `k = 0` ordinal-shift identity `shift(t, 0) := t` is the foundation convention OrdinalShiftBase (ASN-0058), under which ASN-0036's S8 already operates. With it, the `j = 0` admissible position above resolves to `shift(min, 0) = min(V_{s_C}(d))` — insertion at the very beginning.

This yields `N + 1` admissible positions: `j = 0` inserts before the first character, `j = N` after the last, and `j ∈ {1, …, N−1}` in the interior. The *append* operation Nelson lists as a separate convenience (APPEND) is the `j = N` case of INSERT — distinct in name only, identical in semantic effect.

For empty `V_{s_C}(d)`, the precondition is the ternary predicate `ValidFirstInsertionPosition(d, p, m)` (ASN-0036). Its third argument is *not* a separate operation input: it is bound to `m := #p`, the depth of the supplied `p`. A caller who hands INSERT a position `p = [s_C, 1, …, 1]` has thereby fixed its length, and that length (constrained only by `#p ≥ 2`) is the `m` the predicate consumes. The single admissible position is `[s_C, 1, …, 1]` of length `m = #p`. The post-state has `V_{s_C}(d') ≠ ∅`.

The condition `n ≥ 1` rules out a degenerate empty-insertion case. The values `v_k` must be elements of the content type `Val`; the abstract specification places no further constraint on their structure.

## Discovering the Three Effects

INSERT splices `n` new content units into `d`'s arrangement at V-position `p`. Three effects must obtain together.

### Effect One: Allocation

The new content units do not exist in `dom(C)` before the operation. INSERT creates `n` new content units at *fresh* I-addresses drawn from never-reused locations: Xanadu storage is append-only, so each unit is laid down at a new address rather than reusing any existing one.

The freshness comes from `d`'s content sub-allocator `A_C(d)`, by the substrate's allocation discipline (ASN-0093). We require `n` addresses, produced by `n` successive K.α firings under the substrate's transition vocabulary:

  `a_k = A_C(d)`'s `k`-th emission across the composite, for `0 ≤ k < n`

The freshness of each `a_k` is established against the state immediately preceding its K.α firing — not against the operation's pre-state Σ. If Σ_k denotes the substrate state after K.α has fired for `a_0, …, a_{k−1}`, then K.α's precondition requires `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)`. This conjunction is exactly the conclusion of SubsequentEmissionFreshness (ASN-0093): the subsequent emission `a_k = inc(a_prev, 0)` of `A_C(d)` is fresh against `dom(C) ∪ dom(L)`. The boundary case `m_d = 0`, where `a_0` is `A_C(d)`'s first emission `[d.0.s_C.1]`, is covered by FirstEmissionFreshness (ASN-0093). These two lemmas discharge K.α's freshness precondition at each of the `n` firings.

By the chain discipline (ChainPrefixExtension, ChainEnumerationInjectivity; ASN-0093), every `a_k` has `origin(a_k) = d`, satisfies `b_C(d) ≼ a_k` (extending the content sub-allocator anchor), and is structurally produced by the sub-allocator's `inc(·, 0)` chain. The addresses `a_0, a_1, …, a_{n−1}` form a contiguous initial-segment extension of the chain: `a_{k+1} = inc(a_k, 0)` for `0 ≤ k < n − 1`, and `a_0` is either `[d.0.s_C.1]` (if `d` had no prior content emissions, per K.α's first-emission predicate in ASN-0093) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(Σ.C) : origin(a) = d}` (per K.α's subsequent-emission predicate in ASN-0093).

Branch selection keys on `dom(C)`, not the arrangement: when residual `origin = d` content persists in `dom(C)` (`{a' ∈ dom(Σ.C) : origin(a') = d} ≠ ∅`), the *subsequent*-emission branch fires off the persisted frontier `a_prev` — continuing `A_C(d)`'s chain rather than restarting it — even when `V_{s_C}(d) = ∅`.

The post-state content store grows by the fresh addresses `a_0, …, a_{n−1}` carrying the new values `v_0, …, v_{n−1}`, while every pre-existing binding is preserved unchanged (claim INS.C).

The pre-existing content is *not touched*: its values are preserved bit-for-bit, and its addresses persist in the post-state. This is the foundational permanence guarantee S0.

### Effect Two: Placement

The new I-addresses must appear at V-positions `p, shift(p, 1), …, shift(p, n−1)`. The mapping is exact:

  `(A k : 0 ≤ k < n : M'(d)(shift(p, k)) = a_k)`

By OrdAddHom clause (b) (ASN-0082) applied to `w = δ(k, m_C)`, every `shift(p, k)` for `k ≥ 1` lies in the same subspace as `p`: `subspace(shift(p, k)) = s_C`. The result-length identity of TumblerAdd (ASN-0034) gives `#shift(p, k) = m_C`. For `k = 0`, the position is `p`, sharing subspace and depth trivially. The placement effect is thus that each Insertion position is `shift(p, k)` for `0 ≤ k < n`, mapping to `a_k`; these positions constitute the *Insertion region*.

### Effect Three: Shift

Every existing V-position `v ∈ V_{s_C}(d)` with `v ≥ p` must remap. The content there does not change — it keeps its I-address — but its V-position advances by `n`. This is the *Shifted right* effect of INSERT's step-3 K.μ⁺ (claim INS.M-shift), which by construction adds exactly the mappings `shift(v, n) ↦ M(d)(v)` for each `v ∈ V_{s_C}(d)` with `v ≥ p`. The right region is the source of the shift; the shifted-right region is its image. The two are related by the order-preserving (TS1, ShiftOrderPreservation; ASN-0034) and injective (TS2, ShiftInjectivity; ASN-0034) shift map. The image of the shift map is exactly `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N}` when we write `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`. The Insertion positions `shift(p, k)` for `0 ≤ k < n` are disjoint from these shift-images (by the pairwise-disjointness argument below for S2).

**Identification with the foundation's post-insertion shift (INS.I3-coincide).** Let `M_{I3}` denote the arrangement that ASN-0082's I3 (PostInsertionShift) specifies at `S = s_C`, shift amount `n`, and insertion point `p`. I3's preconditions (`#p ≥ 2`, `subspace(p) = s_C`, depth-compatibility — `#p = m_C` for existing same-subspace positions — and `n ≥ 1`) are met by INS.pre, so invoking I3 and inheriting its per-state lemmas is licensed. The Shifted-right effect is the `S = s_C` instance of I3, and the Left region is I3's left-frame (I3-L). The one region I3 does *not* supply is the Insertion placement: I3 *vacates* the gap `[p, shift(p, n))` (I3-V, PostInsertionVacating) without filling it, whereas INSERT fills exactly that gap with the Insertion positions mapping to the fresh `a_k`. The precise relationship is therefore a *restriction equality*, not an equality of whole arrangements: I3's domain and INSERT's `M'(d)` differ on the gap (I3 holds no mapping there; INSERT holds the Insertion region), but on Left ∪ Shifted-right the two are pointwise identical —

  `(A v : v ∈ Left ∪ Shifted-right :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M_{I3}(v))`.

Because `M'(d)` coincides pointwise with the I3 arrangement on Left ∪ Shifted-right, the *content-frame-independent* arrangement lemmas I3 establishes of that arrangement transfer to `M'(d)` restricted to those two regions — specifically I3-S2 (functionality), I3-VP (S8a well-formedness), I3-VD (fixed depth), and I3-fin (finiteness), each a property of the arrangement alone. INSERT re-derives S3 (§Referential integrity) and S7 (§Post-state V-position well-formedness) independently rather than inheriting them.

## The Operation: Formal Contract

INSERT is a **substrate composite** in the sense of ValidComposite★ (ASN-0047) — a finite sequence of elementary transitions drawn from the substrate's K-vocabulary, governed at the composite boundary by the coupling constraints J0, J1★, J1'★.

We state INSERT as a composite `Σ →* Σ'`.

**Operation:** `INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)`

**Substrate Decomposition.** INSERT realises as the following sequence of elementary transitions, in order:

1. **`n` successive K.α firings** allocating fresh content addresses `a_0, a_1, …, a_{n−1}` from `A_C(d)`, freshness per INS.alloc.
2. **One K.μ⁻ on `d`** — fired iff the pre-state content-subspace Right region `Right := {v ∈ V_{s_C}(d) : v ≥ p}` is non-empty — retaining the Left prefix of `V_{s_C}(d)` (with `n'_{s_C} = p_m − 1`) and retaining all of `V_{s_L}(d)` (with `n'_{s_L} = n_{s_L}`). When the Right region is empty, K.μ⁻ is omitted, and step 3's K.μ⁺ alone adds the Insertion region, leaving `V_{s_L}(d)` untouched.

   **(INS.μ⁻-fires):** K.μ⁻ fires iff `Right ≠ ∅`; it is omitted in exactly two cases — the append case (`p_m = N + 1`) and the empty-content-subspace case (`V_{s_C}(d) = ∅`) — in both of which `Right = ∅` (the empty case has no V-position at all in `V_{s_C}(d)`; the append case has every `v ∈ V_{s_C}(d)` with last component in `{1, …, N}`, none satisfying `v ≥ p`).
3. **One K.μ⁺ on `d`** adding the Insertion V-positions (mapping `shift(p, k) ↦ a_k` for `0 ≤ k < n`) and the Shifted-right V-positions (mapping `shift(v, n) ↦ M(d)(v)` for each `v ∈ V_{s_C}(d)` with `v ≥ p`). All additions in step 3 lie in subspace `s_C`, as required by K.μ⁺'s content-subspace restriction (ASN-0047).
4. **`n` successive K.ρ firings** recording provenance pairs `(a_k, d)` for `0 ≤ k < n`.

**State Preconditions** (evaluated against the operation's pre-state Σ):
- `d ∈ dom(M)`
- `subspace(p) = s_C`
- depth of `p`, split by case:
  - *Non-empty `V_{s_C}(d)`:* `#p = m_C`, where `m_C` is the common depth of `V_{s_C}(d)` fixed by S8-depth (ASN-0036) — the caller cannot choose otherwise.
  - *Empty `V_{s_C}(d)`:* `#p ≥ 2` is the genuine constraint (there is no pre-existing depth to match); the operation then sets `m_C := #p`, binding the third argument of `ValidFirstInsertionPosition`.
- `p` is a valid insertion position: either `ValidInsertionPosition(d, p)` (ASN-0036) for non-empty `V_{s_C}(d)` — equivalently `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ |V_{s_C}(d)|}` — or `ValidFirstInsertionPosition(d, p, m)` (ASN-0036) for empty `V_{s_C}(d)`, equivalently `p = [s_C, 1, …, 1]` of depth `m`
- `n ≥ 1`
- `v_k ∈ Val` for each `0 ≤ k < n`
- *Composite-boundary premise.* The pre-state Σ is a composite boundary (ASN-0047), so the composite-boundary properties P4★, P4a, P7a of ExtendedReachableStateInvariants are available.

**Effect — Content Store:**
Let `a_0, a_1, …, a_{n−1}` denote the `n` successive emissions of `A_C(d)` produced by the K.α firings of step 1. Then:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `(A k : 0 ≤ k < n : C'(a_k) = v_k)`
  `(A a : a ∈ dom(C) : C'(a) = C(a))`

**Effect — Arrangement of `d`, text subspace:**
Three disjoint regions:

  *Left* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

  *Insertion* — `(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)`.

  *Shifted right* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

  *Exhaustiveness* (INS.M-exhaustive) — `(A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right)`, where Left, Insertion, and Shifted-right denote the three V-position sets defined by the per-region clauses above. Equivalently, `V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions, with no additional `s_C` positions in the post-state.

**Effect — Provenance:**

  `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`

realised by step 4's `n` K.ρ firings.

**Frame Conditions:**
- `L' = L`. The link store is unchanged: no K.λ fires in the decomposition, so `dom(L)` and every link value persist by L12 (LinkImmutability; ASN-0093).
- `E' = E`. The entity set is unchanged: no K.δ fires in the decomposition, hence `E'_doc = E_doc`.
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
- *Insertion:* `{[1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}}` — matches `shift(p, k) ↦ a_k` for `k ∈ {0, 1}` via INS.M-insert.
- *Shifted right:* `{[1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}` — matches `shift(v, 2) ↦ M(d)(v)` for `v ∈ {[1,3], [1,4], [1,5]}` via INS.M-shift.

The last-component values in `V_{s_C}(d')` are `{1, 2, 3, 4, 5, 6, 7}` — sequential, contiguous, starting at 1, satisfying INS.inv.seq with new cardinality `N + n = 7`.

*Provenance discharge (J0, J1★, J1'★).* Step 4's two K.ρ firings add exactly `(a_{new0}, d)` and `(a_{new1}, d)` to R, giving `R' = R ∪ {(a_{new0}, d), (a_{new1}, d)}`. These are the two freshly allocated Insertion images, placed at `[1,3]` and `[1,4]`. The Shifted-right images `a₃, a₄, a₅` (placed at `[1,5], [1,6], [1,7]`) were already arranged pre-state at `[1,3], [1,4], [1,5]`, so they are already in R by pre-state P4★ and impose no new obligation. Here the coupling logic instantiates to the two pairs above: J0 pairs each fresh `dom(C') \ dom(C)` address with its K.μ⁺ placement, J1★ records each newly-arranged content-subspace image, and J1'★ matches each new R'-entry back to a placement — all satisfied when step 4's K.ρ firings commit.

**Append case (`j = N = 5`).** With the same pre-state, `INSERT(d, [1,6], ⟨v₀⟩)` (where `[1,6] = shift([1,1], 5)` is one past the last position). The Right region is empty; no K.μ⁻ fires (Left = entire `V_{s_C}(d)`). Composite: one K.α + one K.μ⁺ adding `[1,6] ↦ a_{new0}` only + one K.ρ. Post-state `V_{s_C}(d') = {[1,1], …, [1,6]}` with `a₁, …, a₅, a_{new0}` as images.

**Prepend case (`j = 0` on a non-empty document).** The symmetric extreme — insert *before all* existing content — is the uniquely stressful K.μ⁻ scenario, because `Left = ∅` *forces* full content-subspace clearance. With the same pre-state `V_{s_C}(d) = {[1,1], …, [1,5]}` (`m_C = 2`, `N = 5`), invoke `INSERT(d, [1,1], ⟨v₀⟩)` with `n = 1`. The position `p = [1,1] = shift(min(V_{s_C}(d)), 0) = min(V_{s_C}(d))` corresponds to `j = 0`, with `p_m = 1`. The Right region `Right = {v ∈ V_{s_C}(d) : v ≥ p}` is the *entire* `V_{s_C}(d)` (since `p` is the minimum), so `Right ≠ ∅` and K.μ⁻ *fires*. The composite:

1. **One K.α firing.** `A_C(d)` emits `a_{new0}`, fresh.
2. **K.μ⁻ on `d`** retains the Left prefix with `n'_{s_C} = p_m − 1 = 0` — a *forced* full content-subspace clearance, since `Left = ∅` admits no smaller retention. Post-step the text-subspace is `V_{s_C}(d_intermediate) = ∅`, on which D-CTG★, D-MIN★, D-SEQ★ hold *vacuously*. Link subspace retained at `n'_{s_L} = n_{s_L}`.
3. **K.μ⁺ on `d`** re-adds the *entire* run from the minimum: `[1,1] ↦ a_{new0}` (Insertion), and `[1,2] ↦ a₁`, `[1,3] ↦ a₂`, `[1,4] ↦ a₃`, `[1,5] ↦ a₄`, `[1,6] ↦ a₅` (Shifted right — `shift([1,k], 1) = [1, k+1]` for each `k ∈ {1, …, 5}`). *Every* pre-state position is shifted; none survives in place.
4. **One K.ρ firing** records `(a_{new0}, d)`.

The post-state arrangement:

  `M'(d) = {[1,1] ↦ a_{new0}, [1,2] ↦ a₁, [1,3] ↦ a₂, [1,4] ↦ a₃, [1,5] ↦ a₄, [1,6] ↦ a₅}`

with `V_{s_C}(d') = {[1,1], …, [1,6]}`, cardinality `N + n = 6`. Verifying the post-state sequential invariants, with `min = [1,1]` and `max = [1,6]`:

- *D-MIN★:* the minimum under T1 is `[1,1] = [s_C, 1]` of depth 2 — the required form. The re-pin of the minimum survives the full clearance: K.μ⁺'s content-subspace restriction (ASN-0047) requires the re-added `V_{s_C}(d')` to start at `[s_C, 1, …, 1]`, which the Insertion position `shift(p, 0) = [1,1]` supplies.
- *D-SEQ★ (INS.inv.seq):* the last-component values are `{1, 2, 3, 4, 5, 6}` — sequential, contiguous, starting at 1 — matching `{[1, k] : 1 ≤ k ≤ 6}` with `n_{s_C} = 6`, depth `m_{s_C} = 2`.

**Empty-document first insertion.** Let `d` have `V_{s_C}(d) = ∅` and additionally `V_{s_L}(d) = ∅` (so the document's arrangement is entirely empty), and stipulate further that no content has ever been allocated under `d` — `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅` — so under this stipulation K.α's first-emission branch fires (the branch keys on `dom(C)`, per INS.alloc). Invoke `INSERT(d, [1,1], ⟨v₀, v₁, v₂⟩)` with `n = 3` (so the depth is `m = #p = #[1,1] = 2`). The position `p = [1,1]` is the unique value admitted by `ValidFirstInsertionPosition(d, p, 2)` (ASN-0036). K.μ⁻ is omitted — the empty-content-subspace case of (INS.μ⁻-fires). The composite reduces to:

1. **Three K.α firings.** `A_C(d)` emits `a_{new0} = [d.0.s_C.1]` (first-emission branch, per the setup stipulation), then `a_{new1} = inc(a_{new0}, 0)`, then `a_{new2} = inc(a_{new1}, 0)`. Each freshly satisfies K.α's freshness precondition by SubsequentEmissionFreshness, with FirstEmissionFreshness covering the first-emission boundary `a_{new0}` (ASN-0093).
2. **One K.μ⁺ on `d`** adding three V-positions: `[1,1] ↦ a_{new0}`, `[1,2] ↦ a_{new1}`, `[1,3] ↦ a_{new2}`. All in subspace `s_C` per the K.μ⁺ amendment.
3. **Three K.ρ firings** recording `(a_{new0}, d)`, `(a_{new1}, d)`, `(a_{new2}, d)` in R.

The post-state arrangement:

  `M'(d) = {[1,1] ↦ a_{new0}, [1,2] ↦ a_{new1}, [1,3] ↦ a_{new2}}`

with `V_{s_C}(d') = {[1,1], [1,2], [1,3]}` (depth pinned at `m_C = 2` per INS.inv.depth). Verifying the three regions: *Left* is empty (no pre-state position with `v < p`); *Insertion* is `{[1,1] ↦ a_{new0}, [1,2] ↦ a_{new1}, [1,3] ↦ a_{new2}}` matching `shift(p, k) ↦ a_k` for `k ∈ {0, 1, 2}`; *Shifted right* is empty (no pre-state position with `v ≥ p`).

*Cross-subspace and cross-document frames (empty case).* `V_{s_L}(d) = ∅` is preserved trivially: K.μ⁺'s content-subspace restriction adds no `s_L` positions, so `V_{s_L}(d') = ∅` matches. Other subspaces are vacuous. Other documents `d' ≠ d` have `M'(d') = M(d')` by each elementary step's cross-document frame.

*Provenance (empty case).* No K.μ⁻ fires and pre-state `ran(M(d)) = ∅`, so all three Insertion images are range-new — no already-arranged Shifted-right image is carried in by pre-state P4★ — and step 3's three K.ρ firings record `(a_{new0}, d), (a_{new1}, d), (a_{new2}, d)`.

**Re-insertion into a cleared content subspace (subsequent-emission branch).** The empty-document example above fired K.α's first-emission branch; we now exercise the complementary subsequent-emission branch, instantiating the residual-content nuance of §Effect One. Suppose `d` once held `V_{s_C}(d) = {[1,1], [1,2]}` with `M(d) = {[1,1] ↦ [d.0.s_C.1], [1,2] ↦ [d.0.s_C.2]}`, then a full content-subspace clearance (K.μ⁻ with `n'_{s_C} = 0`) removed both V-positions while `[d.0.s_C.1]`, `[d.0.s_C.2]` remain in `dom(Σ.C)`. So `V_{s_C}(d) = ∅` with residual set `{a' ∈ dom(Σ.C) : origin(a') = d} = {[d.0.s_C.1], [d.0.s_C.2]}` and frontier `a_prev = [d.0.s_C.2]`.

Invoke `INSERT(d, [1,1], ⟨v₀, v₁⟩)` with `n = 2` (depth `m = #p = 2`). Since `V_{s_C}(d) = ∅`, the precondition is `ValidFirstInsertionPosition(d, [1,1], 2)` (ASN-0036) and K.μ⁻ is omitted (empty-content-subspace case of (INS.μ⁻-fires)). The composite:

1. **Two K.α firings.** The residual set `{a' ∈ dom(Σ.C) : origin(a') = d} = {[d.0.s_C.1], [d.0.s_C.2]}` is non-empty, so the *subsequent-emission* branch fires (INS.alloc): `A_C(d)` emits `a_{new0} = inc(a_prev, 0) = inc([d.0.s_C.2], 0) = [d.0.s_C.3]`, continuing the chain off the persisted frontier rather than restarting it, then `a_{new1} = inc(a_{new0}, 0) = [d.0.s_C.4]`. Each is fresh against its emission state by SubsequentEmissionFreshness (ASN-0093).
2. **One K.μ⁺ on `d`** adding `[1,1] ↦ a_{new0}` and `[1,2] ↦ a_{new1}`, both in subspace `s_C`.
3. **Two K.ρ firings** recording `(a_{new0}, d)`, `(a_{new1}, d)` in R.

The post-state arrangement:

  `M'(d) = {[1,1] ↦ [d.0.s_C.3], [1,2] ↦ [d.0.s_C.4]}`

with `V_{s_C}(d') = {[1,1], [1,2]}`. The point of this example is the *decoupling* of the V-position index from the I-address chain index: the I-addresses resume the chain at indices 3 and 4 (the chain never restarts), yet the V-positions restart at `[s_C, 1]`. The sequential invariants are stated over `V_{s_C}(d')` alone and so are blind to the chain index:

- *D-MIN★:* the minimum under T1 is `[1,1] = [s_C, 1]` of depth 2 — the required form, independent of whether the images are `[d.0.s_C.1..2]` or `[d.0.s_C.3..4]`.
- *D-SEQ★:* the explicit form `{[1, k] : 1 ≤ k ≤ 2}` matches D-SEQ★ with `n_{s_C} = 2`, depth `m_{s_C} = 2` — determined by the count and depth of V-positions, not by the I-address chain frontier.

**Deep-subspace interior insertion (`m_C = 3`).** The examples above all run at depth `m_C = 2`, where the shared prefix `[s_C, 1, …, 1]` is empty and contiguity reduces to the last component trivially. We now exercise a multi-level content subspace, where the closed-interval reduction's hardest step — excluding off-prefix slice tuples — is actually live. Let `d` have `V_{s_C}(d) = {[1,1,1], [1,1,2], [1,1,3]}` (so `m_C = 3`, `N = 3`), with arrangement:

  `M(d) = {[1,1,1] ↦ a₁, [1,1,2] ↦ a₂, [1,1,3] ↦ a₃}`

Invoke `INSERT(d, [1,1,2], ⟨v₀⟩)` with `n = 1`. The position `p = [1,1,2]` corresponds to `j = 1` (since `shift([1,1,1], 1) = [1,1,2]`), interior; `p_m = 2`. The composite fires:

1. **One K.α firing.** `A_C(d)` emits `a_{new0}`, fresh.
2. **K.μ⁻ on `d`** retains the Left prefix with `n'_{s_C} = p_m − 1 = 1`: post-step the text-subspace is `{[1,1,1]}`. Link subspace retained at `n'_{s_L} = n_{s_L}`.
3. **K.μ⁺ on `d`** adds three V-positions: `[1,1,2] ↦ a_{new0}` (Insertion), and `[1,1,3] ↦ a₂`, `[1,1,4] ↦ a₃` (Shifted right — `shift([1,1,2], 1) = [1,1,3]` and `shift([1,1,3], 1) = [1,1,4]`, both advancing only the last component by `n = 1`).
4. **One K.ρ firing** records `(a_{new0}, d)`.

The post-state arrangement:

  `M'(d) = {[1,1,1] ↦ a₁, [1,1,2] ↦ a_{new0}, [1,1,3] ↦ a₂, [1,1,4] ↦ a₃}`

with `V_{s_C}(d') = {[1,1,1], [1,1,2], [1,1,3], [1,1,4]}`. We verify the three sequential invariants on this post-state, with `min = [1,1,1]` and `max = [1,1,4]`:

- *D-MIN★:* the minimum under T1 is `[1,1,1] = [s_C, 1, 1]` of depth 3 — the required form.
- *D-SEQ★:* the explicit form `{[1,1,k] : 1 ≤ k ≤ 4}` matches D-SEQ★ with `n_{s_C} = 4`, depth `m_{s_C} = 3`.
- *D-CTG★ (off-prefix exclusion, the live case at `m ≥ 3`).* D-CTG★ quantifies over the *full* depth-3, subspace-`s_C`, all-positive slice — every tuple `[1, z_2, z_3]` with `z_2, z_3 ≥ 1`, not only those sharing the prefix `[1,1,·]`. We must show every such `z` with `min ≤ z ≤ max` lies in `{[1,1,k] : 1 ≤ k ≤ 4}`. Take a candidate off-prefix tuple `z = [1, 2, 1]` (component 2 is off-prefix). Comparing `z` with `max = [1,1,4]` under T1: the first divergence is at position 2, where `z_2 = 2 > 1 = max_2`, so `z > max` by T1 case (i) — hence `z ∉ [min, max]`, excluded from the closed interval. The same argument excludes any tuple whose first off-prefix component exceeds 1. So the only slice tuples inside `[min, max]` are those of the form `[1, 1, z_3]` with `1 ≤ z_3 ≤ 4`, exactly `V_{s_C}(d')`. D-CTG★ holds.

## Verifying the Invariants

The post-state Σ' must satisfy every system invariant. We verify the principal ones.

### Permanence of existing content (S0, P0)

The content-store effect's third clause asserts `(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`. This is S0 (ContentImmutability; ASN-0036), equivalently P0 (ContentPermanence; ASN-0047), which subsumes S0 ∧ S1. The first clause `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` adds new addresses without removing any; the new addresses are fresh against `dom(C) ∪ dom(L)` (INS.alloc), so no overwrite occurs. Store monotonicity `dom(C) ⊆ dom(C')` follows.

Each per-step K.α firing preserves S0 by its own frame (its effect adds a new binding without modifying existing ones); K.μ⁻, K.μ⁺, K.ρ have frame `C' = C` and so preserve S0 trivially. The composite preserves S0 by composition.

The consequence: a reader holding any pre-state I-address `a ∈ dom(C)` retrieves the same value `C'(a) = C(a)` from the post-state. The reader needs no knowledge of where in any document's Vstream that content now lies.

### Cross-document independence

The frame `(A d' : d' ≠ d : M'(d') = M(d'))` directly enforces independence: no document other than `d` has its arrangement altered. Coupled with `L' = L` and content-store preservation, this means that any document `d'` that transcludes content from `d` continues to map the same V-positions to the same I-addresses, and those I-addresses continue to resolve to the same values.

Cross-document independence extends to link projection; the `d' ≠ d` case is derived in INS.proj (§Coverage and link discoverability).

### Arrangement functionality (S2)

We verify that `M'(d)` is a function (S2, ArrangementFunctionality; ASN-0036): no V-position has two distinct image I-addresses.

The Left, Insertion, and Shifted-right regions are pairwise disjoint as sets of V-positions. Writing `p = [s_C, 1, …, 1, p_m]`:

The disjointness arguments below compare *last components*, which is sound only because every pre-state content position shares the common prefix `[s_C, 1, …, 1]`. We establish this first. By pre-state D-SEQ★ (PerSubspaceSequentialPositions; ASN-0047), `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` at the common depth `m_C` (S8-depth; ASN-0036), so every pre-state content position agrees with every other on components `1, …, m_C − 1` (all equal to `1` for the leading subspace-and-prefix run; D-CTG-depth, SharedPrefixReduction, ASN-0036, supplies this prefix agreement directly for `m_C ≥ 3`, and it is immediate for `m_C = 2`). Under this shared prefix, T1 reduces the order to the last component: for any pre-state content position `v` and the insertion point `p`, `v < p ⟺ v_{m_C} < p_m`. Thus "Left positions have last component `< p_m`" is exactly the order condition `v < p` restated, not an unsupported claim.

- *Left ∩ Insertion = ∅.* Left positions have last component `< p_m`; Insertion positions have last component in `{p_m, p_m + 1, …, p_m + n − 1}`. The component arithmetic splits on `k`, since `δ(k, m_C)` is defined only for `k ≥ 1` (OrdinalDisplacement, ASN-0034). For `k = 0`, `shift(p, 0) = p`, so the final component is `(shift(p, 0))_{m_C} = p_m`. For `1 ≤ k < n`, the OrdinalShift definition `shift(p, k) = p ⊕ δ(k, m_C)` (ASN-0034) and TumblerAdd's piecewise rule (ASN-0034) at action point `m_C` apply: positions `1, …, m_C − 1` are inherited from `p`, and the final component is `(shift(p, k))_{m_C} = p_{m_C} + δ(k, m_C)_{m_C} = p_m + k`. Across both cases the last component ranges over `{p_m, p_m + 1, …, p_m + n − 1}` for `0 ≤ k < n`.

- *Insertion ∩ Shifted-right = ∅.* Insertion positions have last component in `{p_m, …, p_m + n − 1}`. Shifted-right positions image `v` with last component `v_m ≥ p_m` to `shift(v, n) = v ⊕ δ(n, m_C)`; by the same TumblerAdd rule (ASN-0034), the last component of `shift(v, n)` is `v_m + n`. Since `v_m ≥ p_m` and `n ≥ 1`, every Shifted-right last component satisfies `v_m + n ≥ p_m + n`, strictly greater than every Insertion last component.

- *Left ∩ Shifted-right = ∅.* Left last components are `< p_m`; Shifted-right last components are `≥ p_m + n ≥ p_m + 1`.

Within each region the mapping is uniquely defined. On Left ∪ Shifted-right, internal functionality is the inherited I3-S2 (§Effect Three). Insertion images are uniquely indexed by `k`. The cross-region disjointness above (which involves the Insertion region, outside I3's scope) combines these into functionality of the whole `M'(d)`.

We now establish INS.M-exhaustive — that these three regions exhaust `V_{s_C}(d')`, so no fourth region of `s_C` positions exists in the post-state to violate functionality. The clause is a property of the post-state `V_{s_C}(d')`, and it follows directly from the composite construction. Steps 1 and 4 (the K.α and K.ρ firings) frame `M` (`M' = M`; ASN-0047), so they introduce no `s_C` position. Step 2's K.μ⁻ (when fired) only *removes* positions. Step 3's K.μ⁺ adds *exactly* the Insertion positions `{shift(p, k) : 0 ≤ k < n}` and the Shifted-right positions `{shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p}` (its specified effect). Hence every `s_C` position in `dom(M'(d))` is either a surviving pre-state position with `v < p` (Left), an Insertion position, or a Shifted-right position — no fourth region exists.

The pairwise-disjoint and uniquely-defined regions together exhaust `V_{s_C}(d')` by INS.M-exhaustive, so `M'(d)` is a well-defined function.

For other subspaces and other documents, `M'` equals `M`, which is already a function by the pre-state S2.

### Referential integrity (S3★)

We verify the generalised content-and-link form S3★ (GeneralizedReferentialIntegrity; ASN-0047): `(A v ∈ dom(M'(d)) : (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`.

For Left and Shifted-right content-subspace positions: we re-derive referential integrity directly rather than inheriting I3-S3, because growing `dom(C)` (INS.C) violates I3's content frame I3-C, on which I3-S3's proof premise rests. Each image is `M(d)(v')` for some pre-state position `v' ∈ dom(M(d))` with `subspace(v') = s_C`, which pre-state S3★ places in `dom(C)`, and `dom(C) ⊆ dom(C')` by P0 (ContentPermanence; ASN-0047) — so `ran(M'(d)) ⊆ dom(C')` there.

For Insertion positions: the image is `a_k ∈ dom(C')` by the content-store effect.

For positions in subspaces other than `s_C` of `d` (notably `s_L`), and for positions in other documents: unchanged by frame; S3★ follows from the pre-state combined with link-store immutability `L' = L`.

These three cases exhaust `dom(M'(d))` (by INS.M-exhaustive plus the cross-subspace frame), so S3★ holds on the whole post-state arrangement.

### Sequential text-subspace structure (D-CTG★, D-MIN★, D-SEQ★)

We verify the per-subspace forms D-CTG★ (PerSubspaceContiguity), D-MIN★ (PerSubspaceMinimumPosition), and D-SEQ★ (PerSubspaceSequentialPositions) from ASN-0047 for the text subspace `s_C` of `d` post-state.

**Closed-interval reduction (used in both cases below).** For any depth `m ≥ 2` and any `K ≥ 1`, the set `Pref(m, K) := {[s_C, 1, …, 1, k] : 1 ≤ k ≤ K}` (depth-`m` positions) satisfies D-CTG★ over the full depth-`m`, subspace-`s_C`, all-positive slice between its extremes `min = [s_C, 1, …, 1]` and `max = [s_C, 1, …, 1, K]` under T1. The slice ranges over *every* such tuple, not only those sharing the prefix `[s_C, 1, …, 1]`; for `m ≥ 3` it contains off-prefix tuples such as `[s_C, 2, 1, …, 1]` that must be shown to fall outside `[min, max]`. By D-CTG-depth (SharedPrefixReduction; ASN-0036), for `m ≥ 3` contiguity reduces to the last component once all positions share components `2` through `m − 1`. Write `z = [s_C, z_2, …, z_m]` with every `z_j ≥ 1` and `min ≤ z ≤ max`. If some `z_j > 1` for a least `j` with `2 ≤ j ≤ m − 1`, then `z` agrees with `max` on components `1, …, j − 1` and has `z_j > 1 = max_j` at the first divergence, so `z > max` by T1 case (i) — contradicting `z ≤ max`. Hence `z_j = 1` for `2 ≤ j ≤ m − 1`, so `z = [s_C, 1, …, 1, z_m]`; with `1 ≤ z_m ≤ K` forced at the last component, `z ∈ Pref(m, K)`. (For `m = 2` there are no interior positions and the reduction is immediate.) This establishes convexity between the *global extremes* `min` and `max`. D-CTG★ (ASN-0047) quantifies over *every* pair `v_lo, v_hi ∈ Pref(m, K)`, not just the extremes; the arbitrary-pair case reduces to the extreme case in one step. For any such pair and any slice tuple `z` with `v_lo ≤ z ≤ v_hi`, transitivity with `min ≤ v_lo` and `v_hi ≤ max` (both holding because `min` and `max` are, respectively, the least and greatest elements of `Pref(m, K)` under T1) gives `min ≤ z ≤ max`, whence `z ∈ Pref(m, K)` by the extreme result just proved. The last-component range `{1, …, K}` being contiguous closes D-CTG★. The two cases below apply this with `m = m_C, K = N + n` and with `m, K = n` respectively.

Suppose `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` with `N ≥ 1` (by pre-state D-SEQ★), and `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`. Then:

- Left positions: `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}` — empty if `p_m = 1`.
- Insertion positions: `{[s_C, 1, …, 1, p_m + j] : 0 ≤ j < n} = {[s_C, 1, …, 1, k] : p_m ≤ k < p_m + n}`.
- Shifted-right positions: `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N} = {[s_C, 1, …, 1, k] : p_m + n ≤ k ≤ N + n}` — empty if `p_m = N + 1`.

Their union is `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, which is exactly the sequential structure required by D-SEQ★ with new cardinality `N + n`. The minimum `[s_C, 1, …, 1]` is in the union, so D-MIN★ holds.

For D-CTG★, the union `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` is exactly `Pref(m_C, N + n)`, so the closed-interval reduction (instantiated with `m = m_C`, `K = N + n`) closes D-CTG★.

For the empty pre-state case (`V_{s_C}(d) = ∅`) with `p = [s_C, 1, …, 1]` of depth `m = #p ≥ 2` (via ValidFirstInsertionPosition; ASN-0036): the post-state has only the Insertion region (Left and Shifted-right are empty). The Insertion positions are `shift(p, k) = [s_C, 1, …, 1, 1 + k]` for `0 ≤ k < n`, by OrdAddHom (ASN-0082) for `k ≥ 1` (where `shift(p, k) = p ⊕ δ(k, m)` agrees with `p` on positions `1, …, m − 1` and adds `k` to position `m`) and for `k = 0` (the position is `p = [s_C, 1, …, 1]` itself, since `p_m = 1`). Since `p_m = 1` (the unique valid first position has last component 1), the last components of the Insertion positions are `{1 + 0, 1 + 1, …, 1 + (n − 1)} = {1, 2, …, n}` and the leading `m − 1` components are all `1` throughout.

Post-state `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}`. We verify each predicate:

- *D-MIN★:* the minimum of `V_{s_C}(d')` under T1 is the position with the smallest last component, namely `[s_C, 1, …, 1, 1] = [s_C, 1, …, 1]` of depth `m`. This matches D-MIN★'s required form `[s_C, 1, …, 1]`.
- *D-CTG★:* the post-state `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}` is exactly `Pref(m, n)`, so the closed-interval reduction (instantiated with `K = n`) closes D-CTG★.
- *D-SEQ★:* the explicit form `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}` matches D-SEQ★ with `n_{s_C} = n` and depth `m_{s_C} = m`.
- *S8-depth:* every position in `V_{s_C}(d')` has length `m`, the depth bound to `m_C` at the precondition (§The Operation: Formal Contract); pre-state `V_{s_C}(d) = ∅` imposes no prior depth constraint to conflict with it.

The empty case differs from the non-empty case in that no Left or Shifted-right regions appear and no K.μ⁻ fires in the composite (the content-subspace Right region is empty when `V_{s_C}(d) = ∅`), but the post-state invariants are verified by the same predicate checks on the post-state's exhibited form.

### Post-state V-position well-formedness (S8-depth, S8a, S8-fin) and S7 invariants

We verify the post-state V-position predicates (S8-depth, S8a, S8-fin) and the S7 invariants directly. The S7 invariants range over `dom(C)` and the document set: S7a/S7b/S7d on pre-existing addresses follow from pointwise S0/P0 preservation.

- *S8a (VPositionWellFormedness, ASN-0036) and S8-depth (FixedDepthVPositions, ASN-0036).* We discharge well-formedness (claim **S8a**) and fixed depth `m_C` (claim **INS.inv.depth**) for all three regions here. Each Insertion position `shift(p, k)` is a well-formed inhabitant of `V_{s_C}(d')`. For `k = 0`, the position is `p`, which satisfies S8a directly — `p` is zero-free, of depth `m_C ≥ 2`, with all components strictly positive — by ValidInsertionPosition postcondition (b) (non-empty case) or ValidFirstInsertionPosition postcondition (b) (empty case) (ASN-0036). For `k ≥ 1`, TumblerAdd's piecewise rule at action point `m_C` copies the leading `m_C − 1` components of `p`, all strictly positive (position 1 is the subspace identifier `s_C ≥ 1`; the remaining `m_C − 2` are `1`, by ValidInsertionPosition postcondition (d) or, in the empty case, ValidFirstInsertionPosition's definition fixing `v = [s_C, 1, …, 1]` of depth `m`, ASN-0036), and sets the final component to `p_m + k ≥ p_m ≥ 1`; so `zeros(shift(p, k)) = 0`, `#shift(p, k) = m_C ≥ 2`, and every component is strictly positive. This establishes S8a and fixed depth `m_C` for every Insertion position. On Left ∪ Shifted-right, the inherited I3-VP gives S8a (zero-freedom, depth `≥ 2`, positivity) and the inherited I3-VD gives the common depth `m_C` (INS.inv.depth) (§Effect Three). So S8a and INS.inv.depth hold for all three regions of `V_{s_C}(d')`, hence across all subspaces of the post-state.

- *S8-fin (FiniteArrangement, ASN-0036).* The Left and Shifted-right regions are finite by the inherited I3-fin (§Effect Three). The Insertion region contributes exactly `n` new V-positions to `dom(M'(d))`. The post-state `dom(M'(d))` is the union of finite Left + finite Shifted-right + finite Insertion (cardinality `n`) + finite cross-subspace contributions, hence finite.

- *S7 invariants (S7a, S7b, S7d, and the derived theorem S7, ASN-0036), together with the content element-field invariants C1b and C1c (ASN-0093, also carried in ASN-0047's ExtendedReachableStateInvariants).* The predicates range over `dom(C)` and the document set, not over the V-position regions. Every pre-state `a ∈ dom(C)` inherits S7a, S7b, S7d, C1b, and C1c at the post-state by the pointwise S0/P0 preservation already established under §Permanence and the unchanged document set. **Per-address discharge for each freshly allocated `a_k`.** Each clause below holds the moment its K.α firing commits `a_k` to `dom(C)`, and therefore at every K.α intermediate state and at Σ', persisting unchanged by P0 (with `a_k ∉ dom(L)` persisting by L12): S7a — `origin(a_k) = d ∈ dom(M')` by `A_C(d)`'s emission discipline (ASN-0093); S7b — `zeros(a_k) = 3` by C1 (ContentElementLevel; ASN-0093); C1b — `#E(a_k) ≥ 2`, since `A_C(d)`'s first emission has `#E = 2` (FirstEmission, ASN-0093) and every subsequent `inc(·, 0)` emission preserves length (TA5(c), ASN-0034); C1c — `a_k` is an element of `A_C(d)` reached from `origin(a_k) = d` by `A_C(d)`'s T10a-conforming inc-chain (ChainMembershipForOrigin, ChainDiscipline, ASN-0093), exactly the conforming step sequence C1c requires; and L0's content clause — `subspace_I(a_k) = s_C` (DisjointSubAllocatorChains; ASN-0093). S7d (DocumentAllocationDiscipline) holds at `d` by pre-state inheritance — `d ∈ dom(M)` was a document-allocation event under T10a with `zeros(d) = 2` and T4-validity (M0, ASN-0093). The derived theorem S7 (StructuralAttribution) follows by composition.

- *P6 (ExistentialCoherence, ASN-0047).* `(A a ∈ dom(C') :: origin(a) ∈ E'_doc)` (where `E_doc` is the document subset of `E`). The argument uses the invariant `E_doc = dom(M)` (M1, ArrangementMonotonicity, ASN-0047), holding at both Σ and Σ'. Every pre-state `a ∈ dom(C)` inherits P6 because `dom(C) ⊆ dom(C')` and `origin(a)` is a property of the address `a` itself (an invariant of the addressing scheme, by S7 / StructuralAttribution), unchanged across the composite; meanwhile `E' = E` by INS.frame.E (no K.δ fires), so `E'_doc = E_doc`, and pre-state `origin(a) ∈ E_doc` lifts to `origin(a) ∈ E'_doc`. Each freshly allocated `a_k` satisfies P6 directly: `origin(a_k) = d` by `A_C(d)`'s emission discipline (ASN-0093), and `d ∈ dom(M) = E_doc = E'_doc`. P6 is preserved across the composite.

### Per-subspace span decomposition (S8★)

S8★ (PerSubspaceSpanDecomposition; ASN-0047) requires that each per-subspace arrangement `M'(d)|_{V_S(d')}` admit a finite block decomposition satisfying ASN-0036's S8 conditions. The content-subspace arrangement `M'(d)|_{V_{s_C}(d')}` is a *restriction* of the whole arrangement `M'(d)` to a single subspace, so existence is supplied by C1a (RestrictionDecomposition; ASN-0058), the lemma that lifts M11/M12 to restrictions whose induced domain lies within a single subspace.

**C1a applicability (INS.C1a-app).** For any single-subspace restriction `f = M(d)|_{V_S(d)}` — a document's arrangement restricted to one subspace `S` — C1a's three preconditions are discharged uniformly whenever the host state satisfies S2, S8-fin, and S8-depth: (i) `f` is functional, being a restriction of the function `M(d)` (S2); (ii) `dom(f)` is finite, being a subset of the finite `dom(M(d))` (S8-fin); (iii) every position in `dom(f)` has first component `S`, so `dom(f) ⊆ V_S(d)` lies in a single subspace, and S8-depth gives it a single common depth `m_S ≥ 2`. With these met, C1a yields a unique maximally-merged block decomposition for `f`.

Instantiating INS.C1a-app at `f = M'(d)|_{V_{s_C}(d')}` (S2 from §Arrangement functionality, in its extended S3★/S2 form; S8-fin from §Post-state V-position well-formedness; S8-depth from above, with `S = s_C` and `m_S = m_C ≥ 2`) yields the (unique maximally merged) block decomposition for `M'(d)|_{V_{s_C}(d')}`, discharging existence. The link-subspace branch S8★ requires for `M'(d)|_{V_{s_L}(d')}` is discharged by the trivial length-1 decomposition (per ASN-0047), inherited unchanged from the pre-state by the cross-subspace frame `V_{s_L}(d') = V_{s_L}(d)`.

The single C1a object discharges all of S8★'s conditions on the content subspace. Because C1a's decomposition is *maximally merged*, M12b (ASN-0058) makes every one of its blocks a maximal run of `M'(d)|_{V_{s_C}(d')}`. A maximal run `(v, a, n)` satisfies condition (a) — lockstep displacement, `M'(d)(shift(v, k)) = shift(a, k)` for `0 ≤ k < n` — by the definition of a correspondence run, and condition (b) — label well-definedness — because each block is a well-formed mapping block whose I-addresses lie in `dom(C')` (S2 for functionality, S3★ for referential integrity). Condition (c) — uniqueness of the maximal-run decomposition, which S8★ requires only on the content subspace — is exactly C1a's uniqueness assertion: C1a lifts M12 to the restriction, factoring through M12a (maximal runs partition the domain) and M12b (every block of a maximally merged decomposition is a maximal run). (Condition (c) is not required on the link subspace, where S8★ asks only for the trivial length-1 decomposition.)

S8★ is preserved.

### Cross-subspace isolation

INSERT's shift is scoped strictly to `s_C`; non-text positions are never in the shift's carrier. The frame `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` (`INS.frame.subspace`) directly preserves all subspaces of `d` other than the text subspace. In particular, `V_{s_L}(d') = V_{s_L}(d)`, and link-subspace mappings are unchanged.

### Link store unchanged (L12, L0, L1, L3)

`L' = L` directly preserves every link's address and value. Every `ℓ ∈ dom(L)` has `L'(ℓ) = L(ℓ)` — endsets are pointwise preserved. The element-level structure L1 and the N-endset structure L3 range over `dom(L)` alone, which is unchanged, so they hold of `L'` trivially.

The subspace partition L0 has two conjuncts. Its `dom(L)` conjunct `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)` ranges over the unchanged `dom(L)` and is discharged trivially. Its content conjunct `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)` ranges over the `dom(C)` that INSERT *extends* by the fresh `a_0, …, a_{n−1}` (INS.C); for each such `a_k`, `subspace_I(a_k) = s_C` by the S7 bullet (§Post-state V-position well-formedness).

### Coverage and link discoverability

For every link `ℓ ∈ dom(L)` and every slot `i`, the endset `Σ.L(ℓ).e_i` is a set of spans. Each span `(s, ℓ_w)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ_w}` — a purely combinatorial property of the span representation, consulting no state component (definition of `coverage` in ASN-0098). Since `L' = L`, every link value is unchanged at every slot, so coverage is unchanged: by LP3★ (MultiStepCoverageInvariance; ASN-0098), `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` for every link and every slot.

**Projection-shift correspondence (INS.proj).** For every link `ℓ ∈ dom(L)`, slot `i`, and document `d' ∈ dom(M)`:

  `project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}`

where:
- *For `d' ≠ d`:* `π` is the identity and `N_{ℓ,i} = ∅`, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`. Each elementary step of the substrate decomposition (every K.α, the optional K.μ⁻, K.μ⁺, every K.ρ) carries the explicit cross-document frame `(A d'' : d'' ≠ d : M'(d'') = M(d''))`, so `M(d')` is unmodified at every step. LP4 (ArrangementSpecificity; ASN-0098) applied at each step gives `project(ℓ, i, d', Σ_{j+1}) = project(ℓ, i, d', Σ_j)`; composing across the finite step sequence `Σ = Σ_0 → … → Σ_m = Σ'` yields `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`.
- *For `d' = d`:* `π` is the *region-aware shift map* on the whole of `project(ℓ, i, d, Σ)`, defined by each contributing V-position's class — covering all three classes a contribution may fall into:
  - *Left contributions* (`subspace(v) = s_C ∧ v < p`): `π(v) = v` (identity).
  - *Link-subspace contributions* (`subspace(v) = s_L`): `π(v) = v` (identity); these are unchanged by frame.
  - *Right contributions* (`subspace(v) = s_C ∧ v ≥ p`): `π(v) = shift(v, n)`. This branch closes within subspace `s_C`: for every `v ∈ V_{s_C}(d)` with `v ≥ p`, by OrdAddHom (b clause, ASN-0082) applied to `shift(v, n) = v ⊕ δ(n, m_C)` (a displacement with `δ(n, m_C)_1 = 0`), `subspace(shift(v, n)) = subspace(v) = s_C`, so `shift(v, n) ∈ V_{s_C}(d')`.

  By S3★-aux (SubspaceExhaustiveness; ASN-0047) these three classes exhaust `project(ℓ, i, d, Σ)`, so `π` is total on it. `N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n}` is the set of newly placed Insertion V-positions in `V_{s_C}(d')` whose image `a_k` happens to lie in `coverage(Σ'.L(ℓ).e_i)`.

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

When K.μ⁻ does *not* fire, `Σ_μ⁻` does not exist as a distinct state and the flow passes from `Σ_α_n` directly to `Σ_μ⁺`. By (INS.μ⁻-fires), the omitted cases have `Right = ∅`, and since `P_0^R ⊆ Right`, also `P_0^R = ∅`. The projection at the post-Step-1 state is therefore `P_0 = P_0^L ∪ P_0^R ∪ P_0^{s_L} = P_0^L ∪ P_0^{s_L}` — identical in form to the K.μ⁻-fired formula above. Steps 3 and 4 below proceed uniformly from this expression regardless of whether Step 2 fired.

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

Steps 2 and 3 make the retraction/reintroduction exact: K.μ⁻ removes `P_0^R` from the intermediate projection (Step 2) and K.μ⁺ recovers every Right contribution at its shifted V-position `shift(v, n)` with the same I-address (Step 3, the `{shift(v, n) : v ∈ P_0^R}` term).

*Consequence — preservation of pre-state discoverability:*

  `discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ')`

Every pre-state V-position contributing to projection is mapped (by π or identity) to a post-state V-position with the same I-address, so the non-emptiness of any pre-state projection slot transfers to the post-state.

*Consequence — fresh-address discoverability (the `N_{ℓ,i}` term):* A fresh `a_k` lies in `coverage(Σ'.L(ℓ).e_i)` only if the endset includes `a_k` in its span coverage. For *tight* endsets — those bounded to address ranges already populated at the time the endset was incorporated — this cannot happen: by LP19a (TightFreshness; ASN-0098), the freshness of `a_k` against the endset's incorporation state places it outside the tight coverage, so `N_{ℓ,i} = ∅`. For non-tight endsets, a fresh `a_k` may indeed land in coverage, and this is by intent: non-tight endsets are designed to capture later-allocated content within their declared range. LP19 (TightEndsetBoundaryExclusion; ASN-0098) specialises this to K.μ⁺ steps of the composite: V-positions newly added by K.μ⁺ whose image was freshly allocated by a prior K.α step of the composite are excluded from any pre-existing tight endset's projection.

### Provenance (R, P4★, P4a, P7a)

The provenance relation `R ⊆ T_elem × E_doc` (ASN-0047) records which documents have ever contained which I-addresses. INSERT's effect on R is `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`, realised by `n` K.ρ firings in step 4 of the substrate composite.

The composite-boundary coupling J1★ (ExtensionRecordsProvenance; ASN-0047), in its content-subspace instance, requires every newly-arranged content-subspace I-address with no pre-state arrangement under `d` to have its provenance pair in `R'`. For Insertion positions, the freshly allocated `a_k` was not in any `ran(M(d))` pre-state. At the moment of `a_k`'s K.α firing, `a_k` is fresh against its emission state by INS.alloc; by P0 (ContentPermanence; ASN-0047) applied along `Σ →* Σ_k`, this lifts to `a_k ∉ dom(Σ.C)`; and by pre-state S3★ (GeneralizedReferentialIntegrity; ASN-0047), `ran(M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`, whence `a_k ∉ ran(M(d))`. So J1★ requires `(a_k, d) ∈ R'` — discharged by step 4. For Shifted-right positions, `M(d)(v) = a` was already arranged at some content-subspace V-position `v ∈ dom(M(d))`, so J1★'s requirement of "not previously arranged in d's content subspace" is false, and no new R entry is required for these. The pair `(a, d)` is in R already: for a Shifted-right address, `a` was in `d`'s content-subspace range at the pre-state composite boundary Σ, so `(a, d) ∈ Contains_C(Σ) ⊆ R` by pre-state P4★ (ProvenanceBounds; ASN-0047) — available because Σ is a composite boundary (INS.pre's composite-boundary premise) — and P2 (ProvenancePermanence; ASN-0047) preserves it to R'.

J1'★ (ProvenanceRequiresExtension; ASN-0047) requires every new R' entry to correspond to a newly-arranged content-subspace I-address. Each `(a_k, d)` added in step 4 corresponds to the placement `shift(p, k) ↦ a_k` introduced by step 3's K.μ⁺ — satisfied.

P4★ (ProvenanceBounds; ASN-0047): `Contains_C(Σ') ⊆ R'`. Pre-state P4★ gives `Contains_C(Σ) ⊆ R`. The post-state's content-subspace arrangement adds n new pairs (one per Insertion position with image `a_k`); each is in R' via step 4. So P4★ holds.

P4a (TraceWitnessing; ASN-0047): every `(a, d) ∈ R'` admits a witness state — a *composite boundary* in the trace `Σ₀ →* … →* Σ_n = Σ'` — at which `a` was in d's content-subspace range. The witness is quantified over boundary states `{Σ₀, …, Σ_n}`, not over states interior to a composite. For pre-state `(a, d) ∈ R`, P4a inherits. For each new `(a_k, d)` added in step 4, the witness is the composite boundary `Σ'` itself (`= Σ_n`): step 4's K.ρ firings frame M (`(A d :: M'(d) = M(d))`), so the Insertion placement `shift(p, k) ↦ a_k` introduced by step 3's K.μ⁺ survives to `Σ'`, keeping `a_k ∈ ran(M'(d))` at that boundary.

P7 (ProvenanceGrounding; ASN-0047): `(A (a, d') ∈ R' :: a ∈ dom(C'))` — every R' entry's first component is in the post-state content store. For pre-state pairs `(a, d') ∈ R`, P7 inherits: pre-state P7 gives `a ∈ dom(C)`, and `dom(C) ⊆ dom(C')` by P0 (ContentPermanence; ASN-0047). For each new R' entry `(a_k, d)` added by step 4's K.ρ firings: K.ρ's own precondition requires `a_k ∈ dom(C)`, so the K.ρ(a_k, d) firing follows step 1's K.α(a_k), which committed `a_k` to `dom(C)`; since `a_k` is never removed thereafter, `a_k ∈ dom(C')` at the post-state. P7 holds.

P7a (ProvenanceCoverage; ASN-0047): every `a ∈ dom(C')` has some `d` with `(a, d) ∈ R'`. Pre-state P7a covers `dom(C)`; each new `a_k ∈ dom(C') \ dom(C)` is paired with `d` in step 4.

## Atomicity and Canonical Order

Nelson requires that after INSERT, the system is in "canonical order" — every structural invariant holds simultaneously. INSERT is a substrate composite governed by ValidComposite★ (ASN-0047), and its atomicity is the *composite-boundary* form: per-state invariants (Class (a) of ASN-0047 — S2, S3★, S8-depth, S8a, D-CTG★, D-MIN★, D-SEQ★, L0, L12, L14, …) hold at *every* state including each intermediate within the composite; composite-boundary properties (Class (b) — P4★, P4a, P7a) and the coupling constraints (J0, J1★, J1'★) hold at the boundary between Σ and Σ'.

We verify that each intermediate state in INSERT's substrate decomposition satisfies the per-state invariants.

Several per-state invariants of ASN-0047's ExtendedReachableStateInvariants are preserved by frame at every intermediate of INSERT's decomposition, because the state components they constrain are never modified. By the state component they range over:

- *Invariants ranging solely over the unmodified components E and L inherit from the pre-state at every intermediate.* No K.δ fires (`E' = E`, INS.frame.E) and no K.λ fires (`L' = L`), so every predicate over the entity set E or the link store L holds at each intermediate by pre-state inheritance — this covers P8, NodeLineage, ActivatedEmission, M0 (over E / `dom(M)`) and L1, L1a, L1b, L1c, L3, L-fin, L12 (over `dom(L)`). CL-OWN and CL-UNIQ constrain link-subspace V-position mappings, which every step leaves untouched (K.μ⁻ retains `V_{s_L}(d)` at `n'_{s_L} = n_{s_L}`; K.μ⁺ adds only content-subspace positions), so they inherit as well.
- *Content-allocation invariants* — S4 (OriginBasedIdentity; ASN-0036). S4 ranges over `dom(C)`, which INSERT extends by `n` fresh addresses via K.α firings, so S4 must be discharged against the changed `dom(C)` at every intermediate. The discharge proceeds in three parts at the `k`-th K.α intermediate state Σ_{α,k}. (i) *Pre-state pairs remain distinct.* For `a₁, a₂ ∈ dom(Σ.C)`, pre-state S4 gives `a₁ ≠ a₂`; P0 (ContentPermanence; ASN-0047) keeps both in `dom(Σ_{α,k}.C)` with the same identities, so distinctness transfers unchanged. (ii) *New addresses are distinct from pre-state addresses.* Each freshly emitted `a_j` (for `0 ≤ j ≤ k`) is fresh against its own emission state by INS.alloc, so `a_j ∉ dom(Σ.C)` by P0 along `Σ →* Σ_{α,j−1}`. (iii) *The freshly emitted addresses are pairwise distinct.* For any pair `0 ≤ i < j ≤ k`, ChainEnumerationInjectivity (ASN-0093) supplies `a_i = t_{m_d + i + 1} < t_{m_d + j + 1} = a_j` under the tumbler order T1 (strict monotonicity of the chain enumeration), so `a_i ≠ a_j` by T1 irreflexivity. Together (i)–(iii) discharge S4 at every K.α intermediate. The subsequent K.μ⁻, K.μ⁺, and K.ρ firings have frame `C' = C` and so inherit S4 trivially.
- *L0's content conjunct* — L0's `dom(L)` conjunct `(A a ∈ dom(L) :: subspace_I(a) = s_L)` inherits with the other link-store invariants above, but its content conjunct `(A a ∈ dom(C) :: subspace_I(a) = s_C)` ranges over the `dom(C)` that the K.α firings extend, holding per-address for each fresh `a_k` by the S7-bullet discharge (§Post-state V-position well-formedness).
- *Content-store finiteness* — C-fin (ContentStoreFiniteness). The pre-state has `|dom(C)| < ∞`; each K.α firing adds exactly one address; n is finite. So `|dom(C')| ≤ |dom(C)| + n < ∞` at every intermediate.
- *Subspace exhaustiveness* — S3★-aux (SubspaceExhaustiveness). At every intermediate, `V_{s_C}(d)` and `V_{s_L}(d)` together cover `dom(M(d))` because the K.μ⁻ and K.μ⁺ steps add and remove only positions with subspace ∈ {s_C, s_L} (the K.μ⁺ amendment restricts new V-positions to `subspace = s_C`; K.μ⁻'s per-subspace retention preserves the same partition). Other documents' arrangements are unchanged. So S3★-aux holds.

**K.α and K.ρ frame M; all M-invariants inherit unchanged at those intermediates.** Steps 1 and 4 leave the arrangement untouched (`M' = M`; ASN-0047), so every per-state invariant ranging over `M` — S2, S3★, S8a, S8-depth, S8-fin, S8★, D-CTG★, D-MIN★, D-SEQ★ — inherits unchanged at each K.α and K.ρ intermediate from the preceding state; in particular S8★'s per-subspace restrictions and their maximal-run decompositions are identical to the preceding state's. The only components those steps modify are `dom(C)` (K.α) and `R` (K.ρ). For the fresh `a_k` that K.α commits, the per-address content invariants (S7a, S7b, C1b, C1c, and L0's content clause) hold at each K.α intermediate by the S7 bullet (§Post-state V-position well-formedness). The remaining per-address obligations — genuinely new at the intermediate level — hold at the same K.α intermediates: P6 (`origin(a_k) = d ∈ dom(M) = E_doc = E'_doc`, the document set framed by INS.frame.E; established in the P6 bullet of §Post-state V-position well-formedness); P7 and L14 (`a_k ∈ dom(C)`, `a_k ∉ dom(L)` by K.α's freshness precondition); with S4, C-fin, and S3★-aux for these addresses supplied by the grouped per-component arguments above. K.ρ's additions to `R` are purely additive: P7 holds because each `(a_k, d)` follows the K.α that placed `a_k` in `dom(C)`, and pre-state pairs `(a, d') ∈ R` inherit `a ∈ dom(C) ⊆ dom(C')`.

Two M-modifying intermediates remain — **post-K.μ⁻** and **post-K.μ⁺**. K.μ⁺ is the composite's last M-modifying step, and the subsequent K.ρ firings frame `M`, so the post-K.μ⁺ arrangement equals the composite's final `M'(d)`. The post-K.μ⁺ intermediate inherits the I3-discharged post-state invariants directly (§Verifying the Invariants), but the post-K.μ⁻ intermediate — a contraction state retaining only the Left prefix, with no I3 counterpart — requires the independent argument given below.

- *After step 2's K.μ⁻ (when fired).* `V_{s_C}(d_intermediate)` reduces to the Left prefix `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}`, which is sequential, contiguous, and starts at the minimum — D-SEQ★, D-CTG★, D-MIN★ all hold on the content subspace. Each retained position is a subset of the pre-state's `V_{s_C}(d)`; S8a (zero-free, depth `≥ 2`, all components positive) inherits unchanged from the pre-state, and every retained position has length exactly `m_C`, so S8-depth holds in subspace `s_C` with `m_C` unchanged. The link subspace is retained pointwise (`n'_{s_L} = n_{s_L}`, so `V_{s_L}(d_intermediate) = V_{s_L}(d)` with positions and images alike), so every per-subspace invariant on `V_{s_L}` — S8a, S8-depth, D-CTG★, D-MIN★, D-SEQ★, CL-OWN, CL-UNIQ — inherits unchanged from the pre-state. S8-fin holds because `dom(M(d_intermediate))` is a subset of the finite pre-state `dom(M(d))`. S3★ holds because retained images are unchanged and S3★ held of the pre-state. S8★ (PerSubspaceSpanDecomposition; ASN-0047) holds at this intermediate: the content subspace `V_{s_C}(d_intermediate)` is the contiguous prefix `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}` (empty when `p_m = 1`), and its single-subspace restriction `M(d_intermediate)|_{V_{s_C}(d_intermediate)}` admits a finite maximally-merged decomposition by INS.C1a-app instantiated at this intermediate (S2, S8-fin, S8-depth all holding at `d_intermediate` as established above in this bullet); the link subspace is retained verbatim and inherits its trivial length-1 decomposition from the pre-state.

- *After step 3's K.μ⁺ — the arrangement at this intermediate equals the final `M'(d)`.* The post-K.μ⁺ arrangement equals the composite's final arrangement `M'(d)` even though the state itself is not yet `Σ'` (its provenance component `R` is extended only by the step-4 K.ρ firings). The arrangement invariants here — S2, S3★, S8a, S8-depth, S8-fin, S8★, D-CTG★, D-MIN★, D-SEQ★ on `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` — are the post-state assertions established in §Verifying the Invariants, which verified `Σ'` directly. J0 (composite-boundary) is first satisfied at this step: each `a_k ∈ dom(C')` has its placement at `shift(p, k)`.

- *After each of the `n` K.ρ firings of step 4.* R extends by one `(a_k, d)` pair; M is framed, so the arrangement invariants inherit by the collapsed K.α/K.ρ statement above. The final K.ρ intermediate *is* the composite boundary `Σ'`, where the composite-boundary couplings and properties J1★, P4★, P4a, P7a — together with the per-state P7 across each K.ρ commit — come due and are discharged.

The decomposition is admissible under ValidComposite★ because (i) every elementary transition's per-step precondition is met at its intermediate state, and (ii) the composite-boundary coupling constraints J0, J1★, J1'★ hold at the boundary `Σ →* Σ'`. The least-obvious per-step obligation in (i) is K.μ⁻'s strict-contraction requirement (PerSubspaceContractionScope, ASN-0047): at least one subspace `S` must admit strict contraction `n'_S < n_S`. The decomposition fixes `n'_{s_C} = p_m − 1` and `n'_{s_L} = n_{s_L}`. K.μ⁻ fires only when `Right ≠ ∅` (INS.μ⁻-fires), which gives `p_m ≤ N = n_{s_C}`, hence `n'_{s_C} = p_m − 1 < n_{s_C}` — discharging strict contraction on the content subspace; `n'_{s_L} = n_{s_L}` contracts nothing and needs no discharge.

This also discharges P3 (ExtendedTransitionInvariants; ASN-0047), the sole *composite-transition* obligation, which ASN-0047 states as the synthesis `P0 ∧ P1 ∧ P2 ∧ L12`. Each conjunct holds between the initial state Σ and the final state Σ': P0 (ContentPermanence — `dom(C) ⊆ dom(C')` with value preservation) follows from step 1's K.α firings extending `dom(C)` by fresh addresses while the K.μ⁻/K.μ⁺/K.ρ frames leave existing entries untouched; P1 (EntityPermanence — `E ⊆ E'`) follows from INS.frame.E (`E' = E`, no K.δ); P2 (ProvenancePermanence — `R ⊆ R'`) follows from step 4's K.ρ firings being purely additive on R; and L12 (LinkImmutability — `dom(L) ⊆ dom(L')` with value preservation) follows from INSERT firing no K.λ, so `L' = L`. Their conjunction is exactly P3, so the composite transition `Σ →* Σ'` satisfies ExtendedTransitionInvariants.

The post-state Σ' is *uniquely determined* by the operation contract; the substrate decomposition that realises it is not. We verify uniqueness component by component.

  *Content store.* Every admissible decomposition fires exactly `n` K.α steps in their forced order (per the K.α strict-order argument below — the `k`-th firing must produce the determined chain element `t_{m_d + k + 1}` of `A_C(d)`). So `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` with each `a_k` determined uniquely by the pre-state's chain index `m_d` (read from `Σ.C`) and the inputs; the value `C'(a_k) = v_k` is set by the K.α firing's value parameter `v_k` from INSERT's input sequence. The frame of every other elementary step (K.μ⁻, K.μ⁺, K.ρ) leaves C unchanged, so `C'(a) = C(a)` for `a ∈ dom(C)` is preserved by composition.

  *Arrangement of `d`.* At the boundary, `V_{s_C}(d')` equals Left ∪ Insertion ∪ Shifted-right, with no fourth region — this is the exhaustiveness clause INS.M-exhaustive, proved from the composite construction in §Arrangement functionality. When K.μ⁻ fires it retains exactly the Left prefix and removes the Right region, and step 3's K.μ⁺ adds exactly the Insertion and Shifted-right positions (in subspace `s_C`, per the K.μ⁺ amendment); when K.μ⁻ is omitted the Right region of the pre-state `V_{s_C}(d)` is empty by (INS.μ⁻-fires), so the preserved pre-state positions are exactly Left, the Shifted-right region is empty, and K.μ⁺ adds exactly Insertion. These three regions and the mapping on each are fully determined by `p`, `n`, the determined `a_k`, and the pre-state `V_{s_C}(d)`. Any admissible decomposition reaches this M'(d) at the boundary because the K.μ⁻ + K.μ⁺ pair must (i) remove every pre-state position with `v ≥ p` and reintroduce it at `shift(v, n)` (forced by INS.M-shift), (ii) introduce each Insertion position `shift(p, k) ↦ a_k` (forced by INS.M-insert), and (iii) leave the Left region intact (forced by INS.M-left). Whether the K.μ⁻ retention parameter is `n'_{s_C} = p_m − 1` (retain Left) or `n'_{s_C} = 0` (retain nothing), the K.μ⁺ step (or steps) must re-add exactly the missing positions to satisfy the boundary, so the final M'(d) is identical in either decomposition.

  *Arrangement of other documents.* `M'(d') = M(d')` for `d' ≠ d` by every elementary step's frame, regardless of decomposition.

  *Other components.* `L' = L`, `E' = E`, `dom(M') = dom(M)` by the frame of every elementary step in the composite (no K.λ, no K.δ fires); `R' = R ∪ {(a_k, d) : 0 ≤ k < n}` because step 4 adds exactly these `n` pairs in some order — set union being order-independent, R' is identical across decompositions.

Two representative comparisons confirm: a decomposition with `n'_{s_C} = p_m − 1` (the canonical choice) and one with `n'_{s_C} = 0` (full shrinkage) reach different intermediate states (the latter has empty V_{s_C} at the intermediate, the former retains the Left prefix), but both arrive at the same Σ'. Both are well-typed: the full-shrinkage intermediate has `V_{s_C}(d_intermediate) = ∅` and satisfies D-CTG★, D-MIN★, D-SEQ★ vacuously, and its subsequent K.μ⁺ re-adds the entire sequential run `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` from the minimum — admissible because the K.μ⁺ precondition requires only that the resulting M'(d) satisfy D-CTG★ and D-MIN★, not that new positions be added only at the high end. K.μ⁻ retention parameters may range over `{0, 1, …, p_m − 1}` for the content subspace, K.μ⁺ may be split across multiple firings — though intermediate D-CTG★/D-SEQ★ constrains rather than frees the split ordering: a split that adds the Shifted-right positions before the Insertion positions would leave a gap in `V_{s_C}` (e.g. `{[1,1], [1,2], [1,5], [1,6], [1,7]}`, missing `[1,3], [1,4]`), violating contiguity at that intermediate, so each split must add the Insertion positions before (or together with) the Shifted-right positions — and K.α + K.ρ firings may be reordered to a degree (described below), provided each intermediate satisfies the per-state invariants.

Among the elementary firings, three forced orderings arise from K.α firings and a fourth arises from K.μ⁻'s relationship to K.μ⁺ when K.μ⁻ fires. Every remaining pair commutes at the per-state level.

The three K.α-induced forced orderings:

- *K.α(a_k) before K.α(a_{k+1}).* K.α's subsequent-emission predicate (ASN-0093) computes its output as `inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`, consulting `dom(C)`. The `(k+1)`-th firing therefore depends on the `k`-th firing's commit to `dom(C)` (sequenced by SequentialTransitionAxiom; ASN-0093) — a side-effect dependency that forces their order.

- *K.α(a_k) before K.μ⁺ placing `a_k`.* K.μ⁺'s precondition requires each new mapping's image to be in `dom(C)`. If K.μ⁺ attempted to add `shift(p, k) ↦ a_k` before the K.α firing that produces `a_k`, the intermediate would have `a_k ∉ dom(C)` and the per-step precondition would fail.

- *K.α(a_k) before K.ρ(a_k, d).* K.ρ's precondition requires `a ∈ dom(C)`. K.ρ(a_k, d) firing before K.α(a_k) would find `a_k ∉ dom(C)` and the per-step precondition would fail.

The fourth, conditional on K.μ⁻ firing:

- *K.μ⁻ before K.μ⁺* (whenever K.μ⁻ fires in the composite — that is, for interior insertions and for `j = 0` insertions, where the Right region is non-empty and `n'_{s_C} < n_{s_C}` is required). K.μ⁺'s extension precondition requires `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))` — that is, K.μ⁺ preserves the image of every V-position already in the document's arrangement. Consider firing K.μ⁺ before K.μ⁻ for any interior insertion: at least one position `v ∈ V_{s_C}(d)` with `v ≥ p` is in the pre-K.μ⁺ domain `dom(M(d))` and would need to receive a new image under K.μ⁺. Concretely, whenever the Right region is non-empty (`p_m ≤ N`), the position `p` is in pre-state `dom(M(d))` with `M(d)(p) ≠ a_0`, so a K.μ⁺ firing before K.μ⁻ would violate its image-preserving precondition at `p` by attempting to rebind `p ↦ a_0`. K.μ⁻ must fire first to remove the Right region from `dom(M(d))`, so that K.μ⁺'s subsequent additions extend a domain disjoint from the Right region. The forced ordering is conditional: when K.μ⁻ is omitted (the `j = N` append case and the empty pre-state case), there is no fourth ordering, because K.μ⁺ adds positions only outside the existing domain.

Beyond these forced orderings, every other interleaving of the elementary steps reaches the same Σ': no per-state invariant is sensitive to the relative order of the remaining steps, each intermediate is itself a reachable state satisfying the per-state invariants, and the coupling constraints J0, J1★, J1'★ are obligations on INSERT's own boundary `(Σ, Σ')` — discharged there, where every `a_k` is both placed by K.μ⁺ and recorded by K.ρ. The abstract specification commits to none of the admissible interleavings.

## Weakest-Precondition Analysis

The verification above proceeds forward — from preconditions and substrate effects to the post-state. We can also reason backward from a desired postcondition to the pre-state condition that secures it. This is Dijkstra's `wp` calculus, and we apply it to two non-trivial postconditions.

**Discoverability preservation.** Consider the postcondition `discoverable_from(ℓ, d, ·)` for a fixed link `ℓ ∈ dom(L)` and the operation's target document `d`. We compute:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), discoverable_from(ℓ, d, ·))`

By LP12 (DiscoverabilityCharacterisation; ASN-0098), `discoverable_from(ℓ, d, Σ')` is equivalent to `(E i : coverage(Σ'.L(ℓ).e_i) ∩ ran(Σ'.M(d)) ≠ ∅)`. By LP3★ (MultiStepCoverageInvariance; ASN-0098), `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` since INSERT does not alter `L`. By the post-state's M-effect (available because INS.pre holds), `ran(M'(d)) = ran(M(d)) ∪ {a_k : 0 ≤ k < n}` — the pre-existing range augmented by the freshly allocated I-addresses. The wp expands to:

  `(E i : coverage(Σ.L(ℓ).e_i) ∩ (ran(Σ.M(d)) ∪ {a_k : 0 ≤ k < n}) ≠ ∅)`

which distributes to:

  `discoverable_from(ℓ, d, Σ) ∨ (E i, k : 0 ≤ k < n : a_k ∈ coverage(Σ.L(ℓ).e_i))`

The second disjunct — fresh-address capture — collapses to `false` for any *tight* endset `e_i` (with `tight(e_i, Σ_{e_i})` evaluated at the state of `e_i`'s incorporation), by INS.proj's tight-endset case (`N_{ℓ,i} = ∅`): a freshly allocated `a_k` cannot lie in a tight endset's coverage. Thus, when every slot of `Σ.L(ℓ)` is tight at its incorporation state, the wp simplifies to:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), discoverable_from(ℓ, d, ·)) ≡ INS.pre ∧ discoverable_from(ℓ, d, Σ)`

— a non-trivial conclusion: from an enabling pre-state, discoverability of a tight-endset link from `d` is preserved exactly when it held at the pre-state. INSERT neither creates nor destroys discoverability for tight links; it is transparent to them.

**Provenance membership for a specific I-address.** Consider the postcondition `(a, d) ∈ R'` for a fixed I-address `a` and target document `d`. We compute:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), (a, d) ∈ R')`

By the post-state's R-effect (available because INS.pre holds), `R' = R ∪ {(a_k, d) : 0 ≤ k < n}` where `a_0, …, a_{n−1}` are the freshly allocated content addresses. Thus, from an enabling pre-state, `(a, d) ∈ R'` holds iff `(a, d) ∈ R` or `a ∈ {a_0, …, a_{n−1}}`. The second disjunct depends on the K.α emission discipline: `a = a_k` for some `k` iff `a` is the `(m_d + k + 1)`-th element of the chain `A_C(d)` (where `m_d` is the chain index of the last emission already in `dom(Σ.C)` for origin `d`). For a fixed `a`, this is a structural predicate on the pre-state: either `a` lies in `dom(C)` already (and is *not* a freshly allocated address — the second disjunct fails) or `a` is one of the next `n` chain elements of `A_C(d)` that K.α will produce. Conjoining INSERT's precondition INS.pre, the wp is therefore:

  `INS.pre  ∧  ((a, d) ∈ R  ∨  a ∈ {next n chain elements of A_C(d) starting from chain index m_d + 1})`

where the second-disjunct chain elements are determined by `Σ.C` and the chain enumeration of `A_C(d)`. The pre-state condition is operationally decidable: the chain index `m_d` is recoverable from `Σ.C` via the chain enumeration, and the next `n` chain elements are then determined.

This wp captures both the substrate's effect on R and the structural determinism of the K.α firings — the pre-state condition is a Boolean combination of a pre-state predicate (`(a, d) ∈ R`) and a substrate-derivable property (chain membership), reflecting INSERT's combined provenance-recording and fresh-allocation behaviour.

## Identity Through Allocation

INSERT confers fresh content identity (claim INS.identity): its allocation is fresh (INS.C, INS.alloc), each `a_k` a new emission of `A_C(d)` with `origin(a_k) = d`. The system tracks identity by allocation event, not by value — if two allocations carry coinciding bytes, that coincidence is observable but produces no shared identity.

The identity-by-allocation property has an explicit cross-document consequence.

*Corollary (cross-document allocation independence, INS.identity.crossdoc).* If two distinct documents `d_1 ≠ d_2` each invoke INSERT with the same value sequence `⟨v_0, …, v_{n−1}⟩` at any positions, they produce two disjoint sequences of fresh I-addresses `⟨a_0^{(1)}, …, a_{n−1}^{(1)}⟩` and `⟨a_0^{(2)}, …, a_{n−1}^{(2)}⟩` with `origin(a_k^{(1)}) = d_1 ≠ d_2 = origin(a_k^{(2)})`. The two address sets are disjoint by SubAllocatorBundle (ASN-0047): `dom(A_C(d_1)) ∩ dom(A_C(d_2)) = ∅` for `d_1 ≠ d_2`. Value coincidence at `Σ.C(a_k^{(1)}) = Σ.C(a_k^{(2)})` is observable but does not produce identity — the system observes it as two unrelated allocations.

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
| INS.pre | INSERT preconditions: d ∈ dom(M); p a valid insertion position in the text subspace of d; n ≥ 1; v_k ∈ Val; pre-state Σ is a composite boundary (unpacked in §The Operation's Inputs) | introduced |
| INS.alloc | INSERT allocates precisely n fresh I-addresses from d's content sub-allocator A_C(d), each with subspace_I(a_k) = s_C and origin(a_k) = d; freshness per ASN-0093 (unpacked in §Effect One) | introduced |
| INS.C | dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}; C'(a_k) = v_k; ∀a ∈ dom(C): C'(a) = C(a) | introduced |
| INS.M-left | Text-subspace positions v < p in dom(M(d)) appear unchanged in M'(d) | introduced |
| INS.M-insert | M'(d)(shift(p, k)) = a_k for 0 ≤ k < n, with shift(p, 0) = p | introduced |
| INS.M-shift | For v ∈ V_{s_C}(d) with v ≥ p: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v) — the S = s_C instance of I3 (PostInsertionShift; ASN-0082) | introduced |
| INS.I3-coincide | M'(d) ↾ (Left ∪ Shifted-right) is pointwise identical to the I3-specified arrangement M_{I3} (S = s_C, shift n, point p): ∀v ∈ Left ∪ Shifted-right, M'(d)(v) = M_{I3}(v); the two differ only on the gap [p, shift(p,n)) (I3 vacates, INSERT fills) | introduced |
| INS.M-exhaustive | (A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right); the post-state's text-subspace domain contains no s_C positions beyond the three regions | introduced |
| INS.R | R' = R ∪ {(a_k, d) : 0 ≤ k < n}; discharges composite-boundary couplings J0, J1★, J1'★ (ASN-0047) | introduced |
| INS.frame.subspace | Non-content subspaces of d are unchanged (bidirectionally): {v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C}, and M'(d) agrees with M(d) pointwise on that set. No new non-s_C positions appear; no existing ones are removed | introduced |
| INS.frame.doc | Other documents' arrangements are unchanged: ∀d' ≠ d: M'(d') = M(d') | introduced |
| INS.frame.L | L' = L: link store entirely unchanged | introduced |
| INS.frame.E | E' = E: entity set unchanged (no K.δ in the decomposition); specialises to dom(M') = dom(M) for documents (no new documents registered) | introduced |
| INS.inv.immut | Content immutability S0 (ASN-0036) / P0 (ASN-0047) preserved: dom(C) ⊆ dom(C'), pointwise values preserved, and origin(a) unchanged for every a ∈ dom(C) | introduced |
| INS.inv.func | M'(d) is a function (S2 preserved): Left, Insertion, Shifted-right regions are pairwise disjoint | introduced |
| INS.inv.refint | Referential integrity S3★ (ASN-0047) preserved: ran(M'(d)) ⊆ dom(C') ∪ dom(L') per-subspace | introduced |
| INS.inv.seq | D-CTG★, D-MIN★, D-SEQ★ (ASN-0047) preserved in text subspace: V_{s_C}(d') is sequential with cardinality \|V_{s_C}(d)\| + n | introduced |
| INS.inv.depth | S8-depth (ASN-0036) preserved: non-empty case leaves m_C unchanged; empty case fixes m_C = m on first insertion | introduced |
| INS.C1a-app | For any single-subspace restriction f = M(d)\|_{V_S(d)}, C1a's (ASN-0058) three preconditions are discharged uniformly from S2, S8-fin, S8-depth, yielding a unique maximally-merged decomposition | introduced |
| INS.inv.coverage | Endset coverage unchanged for every link by LP3★ (ASN-0098): coverage depends only on L, which is preserved | introduced |
| INS.inv.discov | Pre-state discoverability preserved: every link discoverable from any document at Σ remains discoverable at Σ' | introduced |
| INS.proj | Projection-shift correspondence: project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}, with π the region-aware shift map and N_{ℓ,i} the fresh-Insertion captures (= ∅ for tight endsets) | introduced |
| INS.atomicity | INSERT's substrate composite preserves per-state invariants at every intermediate state, with composite-boundary properties (P4★, P4a, P7a) and couplings (J0, J1★, J1'★) holding at the boundary Σ →* Σ' | introduced |
| INS.identity | INSERT creates fresh content identity: each a_k is a new allocation with origin(a_k) = d; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence | introduced |
| INS.identity.crossdoc | Cross-document allocation independence: two distinct documents inserting identical values produce disjoint fresh I-address sequences with distinct origins (by SubAllocatorBundle, ASN-0047) | introduced |

## Open Questions

- An implementation must realize the abstract sequential transition model. What must it guarantee to recover canonical order after a partial failure during the substrate composite?
- What invariants must an analogous insertion operation preserve when the target is the link subspace rather than the text subspace?
- Is INSERT closed under composition with itself — i.e., if `Σ →INSERT→ Σ_1 →INSERT→ Σ_2`, is there always a single INSERT from `Σ` to `Σ_2`, or do the intermediate effects accumulate in ways that no single INSERT can reproduce?
- What does the abstract specification say about concurrent INSERTs targeting the same V-position from independent agents — must the system serialise them, and if so, on what basis is the order chosen?
- What derived properties of a document — current size, last-modified marker, total I-address footprint — does INSERT update, and which of these are part of the abstract state versus derivable from it?
