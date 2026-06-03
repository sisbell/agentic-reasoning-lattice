# ASN-0100 Claim Statements

*Source: ASN-0100-insert-operation.md (revised 2026-05-27) — Extracted: 2026-06-03*

## INS.def — InsertDefinition (DEF, definition)

`INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)` is a substrate composite `Σ →* Σ'` under ValidComposite★ (ASN-0047), realised as n K.α + (optional K.μ⁻) + K.μ⁺ + n K.ρ.

Substrate decomposition:
1. `n` successive K.α firings allocating fresh content addresses `a_0, a_1, …, a_{n−1}` from `A_C(d)`
2. One K.μ⁻ on `d` retaining the Left prefix of `V_{s_C}(d)` with `n'_{s_C} = p_m − 1` and retaining `V_{s_L}(d)` with `n'_{s_L} = n_{s_L}`; omitted in cases (i.a) `V_{s_C}(d) = ∅ ∧ V_{s_L}(d) = ∅`, (i.b) `V_{s_C}(d) = ∅ ∧ V_{s_L}(d) ≠ ∅`, (ii) `p_m = N + 1`
3. One K.μ⁺ on `d` adding exactly the Insertion V-positions (`shift(p, k) ↦ a_k` for `0 ≤ k < n`) and the Shifted-right V-positions (`shift(v, n) ↦ M(d)(v)` for `v ∈ V_{s_C}(d)` with `v ≥ p`)
4. `n` successive K.ρ firings recording provenance pairs `(a_k, d)` for `0 ≤ k < n`

---

## INS.pre — InsertPrecondition (PRE, requires)

**State preconditions** (evaluated against pre-state Σ):
- `d ∈ dom(M)`
- `subspace(p) = s_C`
- `#p = m_C` (common depth of `V_{s_C}(d)` if non-empty per S8-depth; caller-chosen depth `m ≥ 2` if empty)
- `p` is a valid insertion position: either `ValidInsertionPosition(d, p)` (ASN-0036) for non-empty `V_{s_C}(d)` — equivalently `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ |V_{s_C}(d)|}` reading `shift(t, 0) = t` per OrdinalShiftBase (ASN-0058) — or `ValidFirstInsertionPosition(d, p, m)` (ASN-0036) for empty `V_{s_C}(d)`, equivalently `p = [s_C, 1, …, 1]` of depth `m`
- `n ≥ 1`
- `v_k ∈ Val` for each `0 ≤ k < n`

**Environmental assumption (composite atomicity):** No elementary transition of any other composite interleaves between INSERT's elementaries on: (i) `A_C(d)`'s chain emission state — the set `{a ∈ dom(C) : origin(a) = d}` — and (ii) `M(d)`'s text subspace `V_{s_C}(d)`.

---

## INS.alloc — InsertAllocation (LEMMA, lemma)

INSERT allocates exactly `n` fresh I-addresses from `d`'s content sub-allocator `A_C(d)`; each `a_k` satisfies `origin(a_k) = d`; each K.α firing satisfies its freshness precondition against its own intermediate state:

`a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)`

where `Σ_k` denotes the substrate state after K.α has fired for `a_0, …, a_{k−1}`.

Freshness discharged by:
- `a_k ∉ dom(Σ_k.C)`: by ChainEnumerationInjectivity (ASN-0093): `a_k = t_{m_d + k + 1}` with index strictly greater than every prior index; by SubAllocatorBundle (ASN-0047): `dom(A_C(d)) ∩ dom(A_C(d')) = ∅` for `d ≠ d'`; by FirstEmissionFreshness (ASN-0093) for boundary case `m_d = 0`
- `a_k ∉ dom(Σ_k.L)`: by DisjointSubAllocatorChains (ASN-0093): `subspace_I(a_k) = s_C`; by L0 (SubspacePartition): every `ℓ ∈ dom(Σ_k.L)` has `subspace_I(ℓ) = s_L`; by SC-NEQ (ASN-0093): `s_C ≠ s_L`

Addresses `a_0, …, a_{n−1}` form a contiguous initial-segment extension of the chain: `a_{k+1} = inc(a_k, 0)` for `0 ≤ k < n − 1`.

---

## INS.chain-shift — InsertChainShift (LEMMA, lemma)

For contiguous emissions of `A_C(d)`, `a_{i+j} = shift(a_i, j)`; in particular `a_k = shift(a_0, k)` for the Insertion chain (`0 ≤ k < n`).

Proof steps:
1. Single-step: `inc(a_i, 0) = shift(a_i, 1)`. Each `a_i` is T4-valid by ChainElementT4Validity (ASN-0093), so `sig(a_i) = #a_i` by TA5-SigValid (ASN-0034). Applying TA5 (HierarchicalIncrement, `k = 0` case; ASN-0034): `inc(a_i, 0)` modifies position `sig(a_i) = #a_i` to `(a_i)_{#a_i} + 1`, preserves length, leaves other components fixed. This is `shift(a_i, 1) = a_i ⊕ δ(1, #a_i)` (OrdinalShift; ASN-0034).
2. The identification iterates because `inc(·, 0)` preserves T4 (TA5a; ASN-0034) and preserves length (TA5(c); ASN-0034).
3. Composing by TS3 (ShiftComposition; ASN-0034): `shift(shift(a_i, j), 1) = shift(a_i, j + 1)`; unfolding from base `a_i = shift(a_i, 0)` (OrdinalShiftBase; ASN-0058) yields `a_{i+j} = shift(a_i, j)` by induction on `j`.

Consequence: the Insertion region `{(shift(p, k), a_k) : 0 ≤ k < n}` equals `{(shift(p, k), shift(a_0, k)) : 0 ≤ k < n}` = denotation `⟦(p, a_0, n)⟧` of mapping block `(p, a_0, n)` under OrdinalShiftBase (ASN-0058).

---

## INS.C — InsertContentStore (POST, ensures)

Let `a_0, a_1, …, a_{n−1}` denote the `n` successive emissions of `A_C(d)` produced by the K.α firings of step 1. Then:

```
dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}
(A k : 0 ≤ k < n : C'(a_k) = v_k)
(A a : a ∈ dom(C) : C'(a) = C(a))
```

---

## INS.M-left — InsertArrangeLeft (POST, ensures)

```
(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))
```

---

## INS.M-insert — InsertArrangeInsert (POST, ensures)

```
(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)
```

reading `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058).

---

## INS.M-shift — InsertArrangeShift (POST, ensures)

```
(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))
```

Discharged by I3 (PostInsertionShift; ASN-0082). Preconditions of I3 discharged: (i) `d ∈ dom(M)` from INSERT's precondition; (ii) `M(d) : T ⇀ T` from substrate typing; (iii) `#p ≥ 2 ∧ subspace(p) = s_C ≥ 1`; (iv) depth-compatibility `V_{s_C}(d) ≠ ∅ ⟹ #p = #v` for any `v ∈ V_{s_C}(d)` from S8-depth; (v) `n ≥ 1`.

---

## INS.M-exhaustive — InsertArrangeExhaustive (POST, ensures)

```
(A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right)
```

where:
- Left = `{v ∈ dom(M(d)) : subspace(v) = s_C ∧ v < p}`
- Insertion = `{shift(p, k) : 0 ≤ k < n}`
- Shifted-right = `{shift(v, n) : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p}`

Equivalently: `V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions, with no additional `s_C` positions in the post-state.

---

## INS.R — InsertProvenance (POST, ensures)

```
R' = R ∪ {(a_k, d) : 0 ≤ k < n}
```

Discharges composite-boundary couplings:
- J0 (AllocationRequiresPlacement; ASN-0047): each `a_k ∈ dom(C') \ dom(C)` placed at `shift(p, k)` by step 3's K.μ⁺
- J1★ (ExtensionRecordsProvenanceContentSubspace; ASN-0047): each freshly allocated `a_k` not previously in `ran(M(d))` has `(a_k, d) ∈ R'`
- J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047): each new R' entry `(a_k, d)` corresponds to placement `shift(p, k) ↦ a_k` by step 3's K.μ⁺

---

## INS.frame.subspace — InsertFrameSubspace (POST, ensures)

Non-content subspaces of `d` are unchanged bidirectionally:

```
{v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C}
∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : M'(d)(v) = M(d)(v))
```

No new non-`s_C` positions appear; no existing ones are removed. Step 2's K.μ⁻ (when fired) preserves the link subspace by `n'_{s_L} = n_{s_L}`; step 3's K.μ⁺ adds only content-subspace V-positions per the K.μ⁺ amendment (ASN-0047).

---

## INS.frame.doc — InsertFrameDoc (POST, ensures)

```
(A d' : d' ∈ dom(M) ∧ d' ≠ d : M'(d') = M(d'))
```

---

## INS.frame.L — InsertFrameLinkStore (POST, ensures)

```
L' = L
```

Link store entirely unchanged: no K.λ fires in the decomposition, so `dom(L)` and every link value persist by L12 (LinkImmutability; ASN-0093).

---

## INS.frame.E — InsertFrameEntity (POST, ensures)

```
E' = E
```

Entity set unchanged (no K.δ in the decomposition); specialises to `dom(M') = dom(M)` for documents.

---

## INS.frame.dom — InsertFrameDomain (POST, ensures)

```
dom(M') = dom(M)
```

No new documents registered.

---

## INS.inv.immut — InsertInvImmutability (INV, predicate)

Content immutability S0 (ASN-0036) / P0 (ASN-0047) preserved:

```
dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))
```

---

## INS.inv.identity — InsertInvIdentity (INV, predicate)

Permanent I-address identity preserved:

```
(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a) ∧ origin(a) unchanged)
```

---

## INS.inv.func — InsertInvFunctionality (INV, predicate)

`M'(d)` is a function (S2, ArrangementFunctionality; ASN-0036 preserved). Left, Insertion, Shifted-right regions are pairwise disjoint:

Writing `p = [s_C, 1, …, 1, p_m]`:
- Left ∩ Insertion = ∅: Left positions have last component `< p_m`; Insertion positions have last component in `{p_m, …, p_m + n − 1}` (for `k = 0`, `shift(p, 0) = p` by OrdinalShiftBase so last component is `p_m`; for `k ≥ 1`, last component is `p_m + k` by TumblerAdd piecewise rule)
- Insertion ∩ Shifted-right = ∅: every Shifted-right last component is `v_m + n ≥ p_m + n`, strictly greater than every Insertion last component `p_m + k < p_m + n`
- Left ∩ Shifted-right = ∅: Left last components `< p_m`; Shifted-right last components `≥ p_m + n`

Shifted-right source uniqueness by TS2 (ShiftInjectivity; ASN-0034): for `v₁, v₂ ∈ V_{s_C}(d)` with `v₁ ≥ p` and `v₂ ≥ p`, `#v₁ = #v₂ = m_C` by S8-depth; TS2 then gives `v₁ ≠ v₂ ⟹ shift(v₁, n) ≠ shift(v₂, n)`.

---

## INS.inv.refint — InsertInvRefInt (INV, predicate)

Referential integrity S3★ (GeneralizedReferentialIntegrity; ASN-0047) preserved:

```
(A v ∈ dom(M'(d)) :
  (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C'))
  ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))
```

- Left and Shifted-right positions: image is `M(d)(v')` for pre-state `v'` with `subspace(v') = s_C`, so image `∈ dom(C)` by pre-state S3★; `dom(C) ⊆ dom(C')` by P0
- Insertion positions: image is `a_k ∈ dom(C')` by INS.C
- Non-`s_C` subspaces and other documents: unchanged by frame; S3★ from pre-state combined with `L' = L`

Discharged also by I3-S3 (PostInsertionReferentialIntegrity; ASN-0082) for the Left + Shifted-right + cross-subspace portion.

---

## INS.inv.seq — InsertInvSeq (INV, predicate)

D-CTG★ (PerSubspaceContiguity), D-MIN★ (PerSubspaceMinimumPosition), D-SEQ★ (PerSubspaceSequentialPositions) (ASN-0047) preserved in text subspace:

```
V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ |V_{s_C}(d)| + n}
```

For non-empty pre-state with `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` and `p = [s_C, 1, …, 1, p_m]`:
- Left: `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}`
- Insertion: `{[s_C, 1, …, 1, k] : p_m ≤ k < p_m + n}`
- Shifted-right: `{[s_C, 1, …, 1, k] : p_m + n ≤ k ≤ N + n}`
- Union: `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`

New cardinality: `|V_{s_C}(d)| + n`.

---

## INS.inv.depth — InsertInvDepth (INV, predicate)

S8-depth (FixedDepthVPositions; ASN-0036) preserved:

- Non-empty case: `m_C` is unchanged; every Insertion position `shift(p, k)` has `#shift(p, k) = m_C` (by OrdinalShiftBase for `k = 0`; by TumblerAdd result-length identity for `k ≥ 1`)
- Empty case: the first insertion fixes `m_C = m` (caller-chosen `m ≥ 2` from ValidFirstInsertionPosition) for `d` at every subsequent state in which `V_{s_C}(d)` remains non-empty; a later K.μ⁻ emptying `V_{s_C}(d)` makes S8-depth vacuous and permits a different depth `m'` on the next first-insertion

---

## INS.inv.cross-subspace — InsertInvCrossSubspace (INV, predicate)

Cross-subspace isolation:

```
V_{s_L}(d') = V_{s_L}(d)
∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : M'(d)(v) = M(d)(v))
```

---

## INS.inv.cross-doc — InsertInvCrossDoc (INV, predicate)

Cross-document isolation:

```
(A d' : d' ∈ dom(M) ∧ d' ≠ d : M'(d') = M(d'))
```

---

## INS.inv.coverage — InsertInvCoverage (INV, predicate)

Endset coverage unchanged for every link by LP3★ (MultiStepCoverageInvariance; ASN-0098):

```
(A ℓ ∈ dom(L), i : coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i))
```

Coverage depends only on `L`, which is preserved by `L' = L`.

---

## INS.inv.discov — InsertInvDiscov (INV, predicate)

Pre-state discoverability preserved:

```
(A ℓ ∈ dom(L), d' ∈ dom(M) :
  discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ'))
```

Every pre-state V-position contributing to projection is mapped (by π or identity) to a post-state V-position with the same I-address, preserving non-emptiness of any pre-state projection slot.

---

## INS.proj — InsertProj (LEMMA, lemma)

Projection-shift correspondence: for every link `ℓ ∈ dom(L)`, slot `i`, document `d' ∈ dom(M)`:

```
project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}
```

where:

**Region-aware shift map π**, with `P_0 = project(ℓ, i, d', Σ)` partitioned as:
- `P_0^L := {v ∈ P_0 : subspace(v) = s_C ∧ v < p}`
- `P_0^R := {v ∈ P_0 : subspace(v) = s_C ∧ v ≥ p}`
- `P_0^{s_L} := {v ∈ P_0 : subspace(v) = s_L}`

```
π(P_0) := P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L}
```

For `d' ≠ d`: `π` is identity, `N_{ℓ,i} = ∅`, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`.

**New-insertion term:**
```
N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n}
N_{ℓ,i} := {shift(p, k) : 0 ≤ k < n ∧ a_k ∈ coverage(Σ'.L(ℓ).e_i)}
```

For tight endsets: `N_{ℓ,i} = ∅` by LP19a (TightFreshness; ASN-0098).

**Step-by-step derivation:**
- After K.α firings: `project(ℓ, i, d, Σ_α) = P_0` by LP6 (ContentAllocationInvariance; ASN-0098)
- After K.μ⁻ (when fired): `project(ℓ, i, d, Σ_{μ⁻}) = P_0^L ∪ P_0^{s_L}` by LP10 (ContractionMonotonicity; ASN-0098)
- After K.μ⁺: `project(ℓ, i, d, Σ_{μ⁺}) = P_0^L ∪ P_0^{s_L} ∪ N_I ∪ {shift(v, n) : v ∈ P_0^R}` by LP9 (ExtensionMonotonicity; ASN-0098)
- After K.ρ firings: unchanged by LP14 (ProvenanceRecordingInvariance; ASN-0098)

---

## INS.atomicity — InsertAtomicity (LEMMA, lemma)

INSERT's substrate composite preserves per-state invariants (Class (a) of ASN-0047) at every intermediate state; composite-boundary properties (Class (b) — P4★, P4a, P7a) and coupling constraints (J0, J1★, J1'★) hold at the boundary `Σ →* Σ'`.

- Elementary-level atomicity supplied by SequentialTransitionAxiom (ASN-0093): each individual elementary transition is uninterruptible
- Composite-level atomicity (no inter-composite elementary interleaving on the affected document and its content sub-allocator chain `A_C(d)`) is required as a precondition (see INS.pre) and is a property of the substrate environment

Forced orderings in the decomposition:
1. K.α(a_k) before K.α(a_{k+1}): second firing's output depends on `dom(C)` state changed by first firing's commit
2. K.α(a_k) before K.μ⁺ placing `a_k`: K.μ⁺ precondition requires `a_k ∈ dom(C)`
3. K.α(a_k) before K.ρ(a_k, d): K.ρ precondition requires `a ∈ dom(C)`
4. K.μ⁻ before K.μ⁺ (when K.μ⁻ fires): K.μ⁺ extension precondition would be violated if `p ∈ dom(M(d))` with `M(d)(p) ≠ a_0`

The composite transition `Σ →* Σ'` satisfies P3 (ExtendedTransitionInvariants; ASN-0047): `P0 ∧ P1 ∧ P2 ∧ L12`.

---

## INS.position — InsertPosition (LEMMA, lemma)

INSERT permitted at any valid position:

Non-empty case (`ValidInsertionPosition(d, p)`; ASN-0036): `N + 1` valid positions `j ∈ {0, …, N}`:
```
p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ N}
```
- `j = 0`: Left empty, entire pre-state shifts; K.μ⁻ shrinks to ∅
- `j = N`: Shifted-right empty; K.μ⁻ omitted (append case)
- `j ∈ {1, …, N−1}`: both Left and Shifted-right non-empty; K.μ⁻ + K.μ⁺

Empty case (`ValidFirstInsertionPosition(d, p, m)`; ASN-0036): single valid position with caller-chosen `m ≥ 2`:
```
p = [s_C, 1, …, 1]  of depth m
```
K.μ⁻ omitted (cases i.a or i.b of substrate decomposition).

---

## INS.identity — InsertIdentity (INV, predicate)

INSERT creates fresh content identity: each `a_k` is a new allocation with `origin(a_k) = d`; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence:

```
(A k : 0 ≤ k < n : a_k ∉ dom(Σ.C) ∧ origin(a_k) = d)
∧ (A k₁, k₂ : 0 ≤ k₁ < k₂ < n : a_{k₁} ≠ a_{k₂})
∧ (A k : 0 ≤ k < n : (A a : a ∈ dom(Σ.C) : a_k ≠ a))
```

---

## INS.identity.crossdoc — InsertIdentityCrossDoc (LEMMA, lemma)

Cross-document allocation independence: two distinct documents `d_1 ≠ d_2` each invoking INSERT with the same value sequence `⟨v_0, …, v_{n−1}⟩` produce disjoint fresh I-address sequences:

```
⟨a_0^{(1)}, …, a_{n−1}^{(1)}⟩  and  ⟨a_0^{(2)}, …, a_{n−1}^{(2)}⟩
```

with:
```
origin(a_k^{(1)}) = d_1 ≠ d_2 = origin(a_k^{(2)})
∧ {a_0^{(1)}, …, a_{n−1}^{(1)}} ∩ {a_0^{(2)}, …, a_{n−1}^{(2)}} = ∅
```

by SubAllocatorBundle (ASN-0047): `dom(A_C(d_1)) ∩ dom(A_C(d_2)) = ∅` for `d_1 ≠ d_2`.

---

## INS.identity.version — InsertIdentityVersion (LEMMA, lemma)

Version chain independence: INSERT on a derived version `d_v = inc(d_src, 1)` allocates from `A_C(d_v)` with `origin = d_v ≠ origin of d_v`'s source document:

```
origin(a_k) = d_v ≠ d_src
∧ dom(A_C(d_v)) ∩ dom(A_C(d_src)) = ∅
```

by SubAllocatorBundle (ASN-0047) applied to `d_v ≠ d_src`, both in `E_doc`.

---

## INS.identity.tightsurv — InsertIdentityTightSurv (LEMMA, lemma)

Link survivability through value coincidence: tight endsets cannot accidentally capture freshly allocated content:

For any tight endset `e` with `tight(e, Σ_e)`, and any fresh `a_k` allocated by INSERT:

```
a_k ∉ dom(Σ_e.C) ∪ dom(Σ_e.L)  ⟹  a_k ∉ coverage(e)
```

by LP19a (TightFreshness; ASN-0098): `N_{ℓ,i} = ∅` for all tight endsets.

Specifically: if `tight(e, Σ_e)` and `a_k` is freshly allocated by INSERT (so `a_k ∉ dom(Σ.C)` where `Σ` is INSERT's pre-state), then by Store Monotonicity★ `dom(Σ_e.C) ⊆ dom(Σ.C)`, so `a_k ∉ dom(Σ_e.C) ∪ dom(Σ_e.L)`, placing `a_k` outside the tight coverage.

---

## Definition — InsertLeftRegion

The Left region of `d`'s text subspace with respect to insertion position `p`:

```
Left := {v ∈ dom(M(d)) : subspace(v) = s_C ∧ v < p}
```

---

## Definition — InsertInsertionRegion

The Insertion region for `n` values inserted at position `p` with allocated addresses `a_0, …, a_{n−1}`:

```
Insertion := {(shift(p, k), a_k) : 0 ≤ k < n}
```

where `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058), and `shift(p, k) = p ⊕ δ(k, m_C)` for `k ≥ 1` per OrdinalShift (ASN-0034).

---

## Definition — InsertShiftedRightRegion

The Shifted-right region of `d`'s text subspace with respect to insertion position `p` and count `n`:

```
Shifted-right := {(shift(v, n), M(d)(v)) : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p}
```

---

## Definition — InsertProjectionMap

The region-aware shift map `π` for INSERT, mapping pre-state projection contributions to post-state positions. For `P_0 = project(ℓ, i, d, Σ)` partitioned as `P_0^L ∪ P_0^R ∪ P_0^{s_L}`:

```
π(P_0) := P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L}
```

- Identity on Left: `v ∈ P_0^L ⟹ π(v) = v` (positions with `subspace(v) = s_C ∧ v < p`)
- Shift-by-n on Right: `v ∈ P_0^R ⟹ π(v) = shift(v, n)` (positions with `subspace(v) = s_C ∧ v ≥ p`)
- Identity on link subspace: `v ∈ P_0^{s_L} ⟹ π(v) = v`
- Identity for `d' ≠ d`: `π` is identity on all contributions from other documents
