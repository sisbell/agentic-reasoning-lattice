# ASN-0100 Claim Statements

*Source: ASN-0100-insert-operation.md (revised 2026-05-27) — Extracted: 2026-05-28*

## Definition — InsertLeftRegion

`Left := {v ∈ dom(M(d)) : subspace(v) = s_C ∧ v < p}`

## Definition — InsertInsertionRegion

`Insertion := {shift(p, k) : 0 ≤ k < n}`, mapping `shift(p, k) ↦ a_k` for `0 ≤ k < n`, reading `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058).

## Definition — InsertShiftedRightRegion

`Shifted-right := {shift(v, n) : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p}`, mapping `shift(v, n) ↦ M(d)(v)`.

## Definition — InsertRegionAwareShiftMap

`π(project(ℓ, i, d, Σ)) := P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L}`

where:
- `P_0^L := {v ∈ project(ℓ, i, d, Σ) : subspace(v) = s_C ∧ v < p}` (Left contributions, π = identity)
- `P_0^R := {v ∈ project(ℓ, i, d, Σ) : subspace(v) = s_C ∧ v ≥ p}` (Right contributions, π = shift(·, n))
- `P_0^{s_L} := {v ∈ project(ℓ, i, d, Σ) : subspace(v) = s_L}` (link-subspace contributions, π = identity)

---

## INS.def — InsertDef (DEF, definition)

`INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)` is a substrate composite `Σ →* Σ'` under ValidComposite★ (ASN-0047), realised as `n` K.α + (optional K.μ⁻) + K.μ⁺ + `n` K.ρ

---

## INS.pre — InsertPre (PRE, requires)

INSERT preconditions:
- `d ∈ dom(M)`
- `p` valid in text subspace of `d`: binary predicate `ValidInsertionPosition` for non-empty case, ternary predicate `ValidFirstInsertionPosition(d, p, m)` with caller-chosen `m ≥ 2` for empty case
- `n ≥ 1`
- `v_k ∈ Val`
- composite-atomicity assumption: no other composite's elementary transitions interleave between INSERT's elementaries on the affected document and its content sub-allocator chain

---

## INS.alloc — InsertAlloc (LEMMA, lemma)

INSERT allocates exactly `n` fresh I-addresses from `d`'s content sub-allocator `A_C(d)`; each `a_k` satisfies `origin(a_k) = d`; each K.α firing satisfies its freshness precondition against its own intermediate state by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093)

---

## INS.chain-shift — InsertChainShift (LEMMA, lemma)

For contiguous emissions of `A_C(d)`, `a_{i+j} = shift(a_i, j)`; in particular `a_k = shift(a_0, k)`. Each `inc(·,0)` step equals `shift(·,1)` because chain elements are T4-valid (ChainElementT4Validity, ASN-0093), so `sig = #` (TA5-SigValid) and `inc(·,0)` bumps only the last component (TA5); the identification iterates under T4 preservation (TA5a) and uniform length (ChainUniformLength, ASN-0093) and composes by TS3 (ShiftComposition)

---

## INS.C — InsertContentStore (POST, postcondition)

`dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`

`C'(a_k) = v_k`

`∀a ∈ dom(C): C'(a) = C(a)`

---

## INS.M-left — InsertArrangeLeft (POST, postcondition)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

Text-subspace positions `v < p` in `dom(M(d))` appear unchanged in `M'(d)`

---

## INS.M-insert — InsertArrangeInsert (POST, postcondition)

`(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)`

reading `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058)

---

## INS.M-shift — InsertArrangeShift (POST, postcondition)

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

discharged by I3 (ASN-0082)

---

## INS.M-exhaustive — InsertArrangeExhaustive (POST, postcondition)

`(A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right)`

Equivalently: `V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions, with no additional `s_C` positions in the post-state. The post-state's text-subspace domain contains no `s_C` positions beyond the three regions, discharged by the substrate decomposition's K.μ⁻ + K.μ⁺ steps adding precisely those positions

---

## INS.R — InsertProvenance (POST, postcondition)

`R' = R ∪ {(a_k, d) : 0 ≤ k < n}`

discharges composite-boundary couplings J0, J1★, J1'★ (ASN-0047)

---

## INS.frame.subspace — InsertFrameSubspace (FRAME, postcondition)

Non-content subspaces of `d` are unchanged (bidirectionally):

`{v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C}`

and `M'(d)` agrees with `M(d)` pointwise on that set. No new non-`s_C` positions appear; no existing ones are removed

---

## INS.frame.doc — InsertFrameDoc (FRAME, postcondition)

Other documents' arrangements are unchanged: `∀d' ≠ d: M'(d') = M(d')`

---

## INS.frame.L — InsertFrameLink (FRAME, postcondition)

`L' = L`: link store entirely unchanged

---

## INS.frame.E — InsertFrameEntity (FRAME, postcondition)

`E' = E`: entity set unchanged (no K.δ in the decomposition); specialises to `dom(M') = dom(M)` for documents

---

## INS.frame.dom — InsertFrameDom (FRAME, postcondition)

`dom(M') = dom(M)`: no new documents registered

---

## INS.inv.immut — InsertInvImmut (INV, predicate)

Content immutability S0 (ASN-0036) / P0 (ASN-0047) preserved:

`dom(C) ⊆ dom(C')` and `(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`

---

## INS.inv.identity — InsertInvIdentity (INV, predicate)

Permanent I-address identity preserved:

`∀a ∈ dom(C): a ∈ dom(C') ∧ C'(a) = C(a) ∧ origin(a)` unchanged

---

## INS.inv.func — InsertInvFunc (INV, predicate)

`M'(d)` is a function (S2 preserved); Left, Insertion, Shifted-right regions are pairwise disjoint by TumblerAdd component arithmetic, with Shifted-right source uniqueness by TS2 (ASN-0034):

- *Left ∩ Insertion = ∅*: Left last components `< p_m`; Insertion last components in `{p_m, p_m+1, …, p_m+n−1}`
- *Insertion ∩ Shifted-right = ∅*: Shifted-right last components `≥ p_m + n`
- *Left ∩ Shifted-right = ∅*: Left last components `< p_m`; Shifted-right last components `≥ p_m + n`

---

## INS.inv.refint — InsertInvRefint (INV, predicate)

Referential integrity S3★ (ASN-0047) preserved:

`(A v ∈ dom(M'(d)) : (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`

discharged also by I3-S3 (ASN-0082)

---

## INS.inv.seq — InsertInvSeq (INV, predicate)

D-CTG★, D-MIN★, D-SEQ★ (ASN-0047) preserved in text subspace:

`V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`

i.e., `V_{s_C}(d')` is sequential with cardinality `|V_{s_C}(d)| + n`

---

## INS.inv.depth — InsertInvDepth (INV, predicate)

S8-depth (ASN-0036) preserved:
- In non-empty case: `m_C` is unchanged
- In empty case: the first insertion fixes `m_C = m` for `d` at every subsequent state in which `V_{s_C}(d)` remains non-empty (a later K.μ⁻ emptying `V_{s_C}(d)` makes S8-depth vacuous and permits a different depth on the next first-insertion)

---

## INS.inv.cross-subspace — InsertInvCrossSubspace (INV, predicate)

Cross-subspace isolation:

`V_{s_L}(d') = V_{s_L}(d)` with mappings unchanged:

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_L :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

---

## INS.inv.cross-doc — InsertInvCrossDoc (INV, predicate)

Cross-document isolation: arrangements of all `d' ≠ d` unchanged

`(A d' : d' ∈ dom(M) ∧ d' ≠ d :: M'(d') = M(d'))`

---

## INS.inv.coverage — InsertInvCoverage (INV, predicate)

Endset coverage unchanged for every link by LP3★ (ASN-0098):

`(A ℓ ∈ dom(L), i :: coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i))`

coverage depends only on `L`, which is preserved

---

## INS.inv.discov — InsertInvDiscov (INV, predicate)

Pre-state discoverability preserved:

`(A ℓ ∈ dom(L), d' ∈ dom(M) :: discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ'))`

every link discoverable from any document at `Σ` remains discoverable at `Σ'`

---

## INS.proj — InsertProj (LEMMA, lemma)

Projection-shift correspondence: for every `ℓ ∈ dom(L)`, slot `i`, and document `d' ∈ dom(M)`:

`project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}`

where:
- For `d' ≠ d`: `π` is the identity and `N_{ℓ,i} = ∅`, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`
- For `d' = d`, text subspace: `π` is the region-aware shift map (identity on Left, `shift(·, n)` on Right, identity on link-subspace contributions)
- `N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n}` captures Insertion images whose fresh `a_k` lies in `coverage(e_i)`:

  `N_{ℓ,i} := {shift(p, k) : 0 ≤ k < n ∧ a_k ∈ coverage(Σ'.L(ℓ).e_i)}`

- `N_{ℓ,i} = ∅` for tight endsets by LP19a (ASN-0098)

---

## INS.atomicity — InsertAtomicity (LEMMA, lemma)

INSERT's substrate composite preserves per-state invariants (Class (a) of ASN-0047) at every intermediate state; composite-boundary properties (Class (b) — P4★, P4a, P7a) and coupling constraints (J0, J1★, J1'★) hold at the boundary `Σ →* Σ'`. Elementary-level atomicity is supplied by SequentialTransitionAxiom (ASN-0093); composite-level atomicity (no inter-composite interleaving) is required as a precondition (see INS.pre) and is a property of the substrate environment

---

## INS.position — InsertPosition (LEMMA, lemma)

INSERT permitted at any valid position:
- `N+1` valid positions under `ValidInsertionPosition` for non-empty `V_{s_C}(d)`:

  `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ N}`

- Single first-insertion position under `ValidFirstInsertionPosition(d, p, m)` with caller-chosen `m ≥ 2` for empty case:

  `p = [s_C, 1, …, 1]` of depth `m`

---

## INS.identity — InsertIdentity (LEMMA, lemma)

INSERT creates fresh content identity: each `a_k` is a new allocation with `origin(a_k) = d`; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence:

`∀a ∈ dom(C), 0 ≤ k < n : a_k ≠ a`

---

## INS.identity.crossdoc — InsertIdentityCrossDoc (COR, corollary)

Cross-document allocation independence: two distinct documents `d_1 ≠ d_2` inserting identical values produce disjoint fresh I-address sequences with distinct origins:

`dom(A_C(d_1)) ∩ dom(A_C(d_2)) = ∅` for `d_1 ≠ d_2`

so `⟨a_0^{(1)}, …, a_{n−1}^{(1)}⟩` and `⟨a_0^{(2)}, …, a_{n−1}^{(2)}⟩` are disjoint with `origin(a_k^{(1)}) = d_1 ≠ d_2 = origin(a_k^{(2)})` (by SubAllocatorAxiom.Disjointness, ASN-0047)

---

## INS.identity.version — InsertIdentityVersion (COR, corollary)

Version chain independence: INSERT on a derived version `d_v` allocates from `A_C(d_v)` with `origin = d_v ≠ origin` of `d_v`'s source document:

`origin(a_k) = d_v` for all `a_k` produced by INSERT on `d_v`, where `d_v ≠ d_src`

---

## INS.identity.tightsurv — InsertIdentityTightSurv (COR, corollary)

Link survivability through value coincidence: tight endsets cannot accidentally capture freshly allocated content by LP19a (ASN-0098):

`(A ℓ ∈ dom(L), i, k : tight(Σ.L(ℓ).e_i, Σ_{e_i}) ∧ 0 ≤ k < n :: a_k ∉ coverage(Σ.L(ℓ).e_i))`
