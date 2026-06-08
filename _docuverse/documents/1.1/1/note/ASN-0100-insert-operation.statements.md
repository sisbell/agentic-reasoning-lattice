# ASN-0100 Claim Statements

*Source: ASN-0100-insert-operation.md (revised 2026-05-27) — Extracted: 2026-06-08*

## Definition — InsertLeftRegion

Left positions: `{v ∈ dom(M(d)) : subspace(v) = s_C ∧ v < p}`

## Definition — InsertInsertionRegion

Insertion positions: `{shift(p, k) : 0 ≤ k < n}`, each mapping `shift(p, k) ↦ a_k`

## Definition — InsertRightRegion

Right region: `Right := {v ∈ V_{s_C}(d) : v ≥ p}`

## Definition — InsertShiftedRightRegion

Shifted-right positions: `{shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p}`, each mapping `shift(v, n) ↦ M(d)(v)`

## Definition — ValidInsertionPosition

For non-empty `V_{s_C}(d)` with cardinality `N = |V_{s_C}(d)|`:

`p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ N}`

Equivalently: `subspace(p) = s_C ∧ #p = m_C` where `m_C` is the common depth of `V_{s_C}(d)` fixed by S8-depth.

## Definition — ValidFirstInsertionPosition

For empty `V_{s_C}(d)`, the ternary predicate `ValidFirstInsertionPosition(d, p, m)`:

`p = [s_C, 1, …, 1]` of depth `m`, where `m := #p ≥ 2`.

The single admissible position is `[s_C, 1, …, 1]` of length `m = #p`.

## Definition — MuMinusFires

**(INS.μ⁻-fires):** K.μ⁻ fires iff `Right ≠ ∅`; it is omitted in exactly two cases — the append case (`p_m = N + 1`) and the empty-content-subspace case (`V_{s_C}(d) = ∅`) — in both of which `Right = ∅`.

## Definition — RegionAwareShiftMap

The region-aware shift map `π` on `project(ℓ, i, d, Σ)`:

- *Left contributions* (`subspace(v) = s_C ∧ v < p`): `π(v) = v`
- *Link-subspace contributions* (`subspace(v) = s_L`): `π(v) = v`
- *Right contributions* (`subspace(v) = s_C ∧ v ≥ p`): `π(v) = shift(v, n)`

By S3★-aux (SubspaceExhaustiveness; ASN-0047) these three classes exhaust `project(ℓ, i, d, Σ)`, so `π` is total on it.

---

## INS.def — InsertDef (DEF, DEFINITION)

`INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)` is a substrate composite `Σ →* Σ'` under ValidComposite★ (ASN-0047), realised as the following sequence of elementary transitions, in order:

1. **`n` successive K.α firings** allocating fresh content addresses `a_0, a_1, …, a_{n−1}` from `A_C(d)`, freshness per INS.alloc.
2. **One K.μ⁻ on `d`** — fired iff `Right ≠ ∅` (INS.μ⁻-fires) — retaining the Left prefix of `V_{s_C}(d)` (with `n'_{s_C} = p_m − 1`) and retaining all of `V_{s_L}(d)` (with `n'_{s_L} = n_{s_L}`).
3. **One K.μ⁺ on `d`** adding the Insertion V-positions (`shift(p, k) ↦ a_k` for `0 ≤ k < n`) and the Shifted-right V-positions (`shift(v, n) ↦ M(d)(v)` for each `v ∈ V_{s_C}(d)` with `v ≥ p`).
4. **`n` successive K.ρ firings** recording provenance pairs `(a_k, d)` for `0 ≤ k < n`.

## INS.pre — InsertPre (PRE, requires)

INSERT preconditions (evaluated against the operation's pre-state Σ):

- `d ∈ dom(M)`
- `subspace(p) = s_C`
- depth of `p`, split by case:
  - *Non-empty `V_{s_C}(d)`:* `#p = m_C`, where `m_C` is the common depth of `V_{s_C}(d)` fixed by S8-depth (ASN-0036)
  - *Empty `V_{s_C}(d)`:* `#p ≥ 2` is the genuine constraint; the operation then sets `m_C := #p`
- `p` is a valid insertion position: either `ValidInsertionPosition(d, p)` (ASN-0036) for non-empty `V_{s_C}(d)` — equivalently `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ |V_{s_C}(d)|}` — or `ValidFirstInsertionPosition(d, p, m)` (ASN-0036) for empty `V_{s_C}(d)`, equivalently `p = [s_C, 1, …, 1]` of depth `m`
- `n ≥ 1`
- `v_k ∈ Val` for each `0 ≤ k < n`
- *Composite-boundary premise.* The pre-state Σ is a composite boundary (ASN-0047), so the composite-boundary properties P4★, P4a, P7a of ExtendedReachableStateInvariants are available.

## INS.alloc — InsertAlloc (LEMMA, lemma)

INSERT allocates precisely `n` fresh I-addresses from `d`'s content sub-allocator `A_C(d)`, each with `subspace_I(a_k) = s_C` and `origin(a_k) = d`; freshness per ASN-0093:

- `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)` where Σ_k is the substrate state after K.α has fired for `a_0, …, a_{k−1}`.
- `a_{k+1} = inc(a_k, 0)` for `0 ≤ k < n − 1`
- `a_0` is either `[d.0.s_C.1]` (if `d` had no prior content emissions) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(Σ.C) : origin(a) = d}` (per K.α's subsequent-emission predicate in ASN-0093).
- `b_C(d) ≼ a_k` for all `0 ≤ k < n`
- By ChainEnumerationInjectivity (ASN-0093): `a_0, a_1, …, a_{n−1}` are pairwise distinct.

## INS.C — InsertContentStore (EFF, ensures)

`dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`

`(A k : 0 ≤ k < n : C'(a_k) = v_k)`

`(A a : a ∈ dom(C) : C'(a) = C(a))`

## INS.M-left — InsertMLeft (EFF, ensures)

Text-subspace positions `v < p` in `dom(M(d))` appear unchanged in `M'(d)`:

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

## INS.M-insert — InsertMInsert (EFF, ensures)

`M'(d)(shift(p, k)) = a_k` for `0 ≤ k < n`, with `shift(p, 0) = p`:

`(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)`

## INS.M-shift — InsertMShift (EFF, ensures)

For `v ∈ V_{s_C}(d)` with `v ≥ p`: `shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v)` — the `S = s_C` instance of I3 (PostInsertionShift; ASN-0082):

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

## INS.I3-coincide — InsertI3Coincide (LEMMA, lemma)

`M'(d) ↾ (Left ∪ Shifted-right)` is pointwise identical to the I3-specified arrangement `M_{I3}` (`S = s_C`, shift `n`, point `p`):

`(A v : v ∈ Left ∪ Shifted-right :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M_{I3}(v))`

The two differ only on the gap `[p, shift(p, n))`: I3 vacates that gap (I3-V, PostInsertionVacating), INSERT fills exactly that gap with the Insertion positions mapping to the fresh `a_k`.

## INS.M-exhaustive — InsertMExhaustive (EFF, ensures)

`(A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right)`

where Left, Insertion, and Shifted-right denote the three V-position sets defined by the per-region clauses. Equivalently:

`V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions, with no additional `s_C` positions in the post-state.

## INS.R — InsertProvenance (EFF, ensures)

`R' = R ∪ {(a_k, d) : 0 ≤ k < n}`

realised by step 4's `n` K.ρ firings; discharges composite-boundary couplings J0, J1★, J1'★ (ASN-0047).

## INS.frame.subspace — InsertFrameSubspace (FRAME, ensures)

Non-content subspaces of `d` are unchanged (bidirectionally):

`{v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C}`

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : M'(d)(v) = M(d)(v))`

No new non-`s_C` positions appear; no existing ones are removed. In particular, `V_{s_L}(d') = V_{s_L}(d)`.

## INS.frame.doc — InsertFrameDoc (FRAME, ensures)

Other documents' arrangements are unchanged:

`(A d' : d' ∈ dom(M) ∧ d' ≠ d : M'(d') = M(d'))`

## INS.frame.L — InsertFrameL (FRAME, ensures)

`L' = L`: link store entirely unchanged. No K.λ fires in the decomposition, so `dom(L)` and every link value persist.

## INS.frame.E — InsertFrameE (FRAME, ensures)

`E' = E`: entity set unchanged (no K.δ in the decomposition).

Specialises to `dom(M') = dom(M)` for documents: no new document is registered.

## INS.inv.immut — InsertInvImmut (INV, predicate)

Content immutability S0 (ASN-0036) / P0 (ASN-0047) preserved:

`dom(C) ⊆ dom(C')`

`(A a : a ∈ dom(C) : C'(a) = C(a))`

`(A a : a ∈ dom(C) : origin(a)` unchanged`)`

## INS.inv.func — InsertInvFunc (INV, predicate)

`M'(d)` is a function (S2 preserved): Left, Insertion, Shifted-right regions are pairwise disjoint.

Disjointness established by last-component arithmetic (all positions share common prefix `[s_C, 1, …, 1]` at depth `m_C`):

- *Left ∩ Insertion = ∅*: Left positions have last component `< p_m`; Insertion positions have last component in `{p_m, p_m + 1, …, p_m + n − 1}`.
- *Insertion ∩ Shifted-right = ∅*: every Shifted-right last component satisfies `v_m + n ≥ p_m + n`, strictly greater than every Insertion last component.
- *Left ∩ Shifted-right = ∅*: Left last components are `< p_m`; Shifted-right last components are `≥ p_m + n ≥ p_m + 1`.

## INS.inv.refint — InsertInvRefint (INV, predicate)

Referential integrity S3★ (ASN-0047) preserved:

`(A v ∈ dom(M'(d)) : (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`

- Left and Shifted-right: images are pre-state `M(d)(v') ∈ dom(C)` and `dom(C) ⊆ dom(C')` by P0.
- Insertion: image is `a_k ∈ dom(C')` by INS.C.
- Link-subspace and other documents: unchanged by frame; S3★ follows from pre-state combined with `L' = L`.

## INS.inv.seq — InsertInvSeq (INV, predicate)

D-CTG★, D-MIN★, D-SEQ★ (ASN-0047) preserved in text subspace:

`V_{s_C}(d')` is sequential with cardinality `|V_{s_C}(d)| + n`:

`V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` (non-empty pre-state case)

`V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}` (empty pre-state case)

In both cases:
- *D-MIN★*: minimum of `V_{s_C}(d')` under T1 is `[s_C, 1, …, 1]`.
- *D-SEQ★*: explicit form matches D-SEQ★ with depth `m_{s_C}` and the stated cardinality.
- *D-CTG★*: post-state equals `Pref(m_C, N + n)` (resp. `Pref(m, n)`), closed by the closed-interval reduction.

## INS.inv.depth — InsertInvDepth (INV, predicate)

S8-depth (ASN-0036) preserved:

- *Non-empty case*: every position in `V_{s_C}(d')` has length exactly `m_C`; the common depth is unchanged.
- *Empty case*: every position in `V_{s_C}(d')` has length `m = #p`, fixing `m_C := m` on first insertion.

For `k ≥ 1`, `#shift(p, k) = m_C` by the result-length identity of TumblerAdd (ASN-0034); for `k = 0`, the position is `p` with `#p = m_C`.

## INS.C1a-app — InsertC1aApp (LEMMA, lemma)

For any single-subspace restriction `f = M(d)|_{V_S(d)}`, C1a's (ASN-0058) three preconditions are discharged uniformly from S2, S8-fin, S8-depth, yielding a unique maximally-merged decomposition:

- (i) `f` is functional, being a restriction of the function `M(d)` (S2)
- (ii) `dom(f)` is finite, being a subset of the finite `dom(M(d))` (S8-fin)
- (iii) every position in `dom(f)` has first component `S`, so `dom(f) ⊆ V_S(d)` lies in a single subspace, and S8-depth gives it a single common depth `m_S ≥ 2`

Instantiated at `f = M'(d)|_{V_{s_C}(d')}` at S2, S8-fin, S8-depth holding at the post-state, C1a yields the unique maximally-merged block decomposition for `M'(d)|_{V_{s_C}(d')}`.

## INS.inv.coverage — InsertInvCoverage (INV, predicate)

Endset coverage unchanged for every link by LP3★ (ASN-0098): coverage depends only on `L`, which is preserved:

`(A ℓ ∈ dom(L), i : coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i))`

## INS.inv.discov — InsertInvDiscov (INV, predicate)

Pre-state discoverability preserved: every link discoverable from any document at Σ remains discoverable at Σ':

`(A ℓ ∈ dom(L), d' ∈ dom(M) : discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ'))`

Every pre-state V-position contributing to projection is mapped (by π or identity) to a post-state V-position with the same I-address, so non-emptiness of any pre-state projection slot transfers to the post-state.

## INS.proj — InsertProj (LEMMA, lemma)

Projection-shift correspondence: for every `ℓ ∈ dom(L)`, slot `i`, and document `d' ∈ dom(M)`:

`project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}`

where:

- *For `d' ≠ d`*: `π` is the identity and `N_{ℓ,i} = ∅`, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`.
- *For `d' = d`*: `π` is the region-aware shift map (identity on Left and link-subspace contributions, `shift(·, n)` on Right contributions):

  `π(P_0) := P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L}`

  `N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n}` is the set of newly placed Insertion V-positions whose image `a_k` lies in `coverage(Σ'.L(ℓ).e_i)`.

  For tight endsets: `N_{ℓ,i} = ∅` (by LP19, TightEndsetBoundaryExclusion; ASN-0098).

Derived from step-by-step tracking through the substrate decomposition:

`project(ℓ, i, d, Σ') = P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L} ∪ N_I`

where `P_0 = P_0^L ∪ P_0^R ∪ P_0^{s_L}` partitions `project(ℓ, i, d, Σ)` by region class.

## INS.atomicity — InsertAtomicity (INV, predicate)

INSERT's substrate composite preserves per-state invariants at every intermediate state, with composite-boundary properties (P4★, P4a, P7a) and couplings (J0, J1★, J1'★) holding at the boundary `Σ →* Σ'`:

- Per-state invariants (Class (a): S2, S3★, S8-depth, S8a, D-CTG★, D-MIN★, D-SEQ★, L0, L12, L14, …) hold at every state including each intermediate within the composite.
- Composite-boundary properties (Class (b): P4★, P4a, P7a) and coupling constraints (J0, J1★, J1'★) hold at the boundary between Σ and Σ'.
- The composite is admissible under ValidComposite★ (ASN-0047): every elementary transition's per-step precondition is met at its intermediate state; K.μ⁻'s strict-contraction requirement is discharged by `n'_{s_C} = p_m − 1 < n_{s_C}` (since `Right ≠ ∅` implies `p_m ≤ N`).
- P3 (ExtendedTransitionInvariants; ASN-0047) holds: `P0 ∧ P1 ∧ P2 ∧ L12` between Σ and Σ'.

## INS.identity — InsertIdentity (LEMMA, lemma)

INSERT creates fresh content identity: each `a_k` is a new allocation with `origin(a_k) = d`; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence.

Formally: the freshness condition `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)` at each K.α firing guarantees `{a_0, …, a_{n−1}} ∩ dom(Σ.C) = ∅` and `{a_0, …, a_{n−1}} ∩ dom(Σ.L) = ∅`.

If two allocations carry coinciding bytes (`C'(a_i) = C'(a_j)` for `i ≠ j`, or matching a pre-existing value), that coincidence is observable but produces no shared identity: `a_i ≠ a_j` (by ChainEnumerationInjectivity, ASN-0093) and each `a_k ∉ dom(Σ.C)`.

## INS.identity.crossdoc — InsertIdentityCrossDoc (COROLLARY, lemma)

Cross-document allocation independence: two distinct documents `d_1 ≠ d_2` each invoking INSERT with the same value sequence `⟨v_0, …, v_{n−1}⟩` at any positions produce two disjoint sequences of fresh I-addresses:

`⟨a_0^{(1)}, …, a_{n−1}^{(1)}⟩` and `⟨a_0^{(2)}, …, a_{n−1}^{(2)}⟩`

with `origin(a_k^{(1)}) = d_1 ≠ d_2 = origin(a_k^{(2)})`.

The two address sets are disjoint by SubAllocatorBundle (ASN-0047):

`dom(A_C(d_1)) ∩ dom(A_C(d_2)) = ∅` for `d_1 ≠ d_2`
