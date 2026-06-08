# ASN-0102 Claim Statements

*Source: ASN-0102-copy-operation.md (revised 2026-05-28) — Extracted: 2026-06-08*

## Definition — CopyOperation

**Preconditions PC1–PC4:**

- **(PC1)** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference with `d_i ∈ dom(Σ.M)`, `subspace(u_i) = s_C`, `V_{s_C}(d_i) ≠ ∅`, `resolve_Σ(R)` defined, every resolved address in `dom(Σ.C)`, and `W ≥ 1`.
- **(PC2)** `d ∈ E_doc`, equivalently `d ∈ dom(Σ.M)`.
- **(PC3)** `S = s_C`. Every source span is content-subspace-resident; resolved addresses carry `subspace_I(·) = s_C`; this pins `subspace(v) = s_C` for inserted positions.
- **(PC4)** Write `n_S = |V_{s_C}(d)|`.
  - *Non-empty* (`n_S ≥ 1`): positions are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S`; `v = [s_C,1,…,1,p]` with `1 ≤ p ≤ n_S + 1`.
  - *Empty* (`n_S = 0`): operation chooses depth `m ≥ 2` and takes `v = [s_C,1,…,1]` of depth `m`, with `p = 1`; this choice fixes `m` as the content-subspace depth of `d` for all subsequent positions.

**Resolution:**
`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,  `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

Run count: `k = (+ i : 1 ≤ i ≤ q : k_i)` where each `k_i` is the maximal-run count of reference `r_i` taken in isolation (C1a, M12 applied per reference).

**Cumulative offset:**
`c_j = (+ j' : 1 ≤ j' < j : n_{j'})`.

**Copied block set:**
`B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`.

**Effect — `COPY(R, d, v)` carries `Σ → Σ'`:**

- `Σ'.C = Σ.C`
- `Σ'.L = Σ.L`
- `Σ'.E = Σ.E`
- `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`
- `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ s_C`, or with `subspace(u) = s_C ∧ u < v`
- `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W`
- `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_{s_C}(d)` with `u ≥ v`
- `Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`

---

## COPY — CopyTransition (DEF, operation)

`COPY(R, d, v)` (single elementary transition; precond. PC1–PC4, target subspace `S = s_C`): `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; content subspace displaced forward by `W` and gap `[v, v+W)` bound to `resolve_Σ(R)` in order; `Σ'.R = Σ.R ∪ {(a_j+i, d)}`

---

## X1 — ContentStoreInvariance (INV, predicate)

`dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`

---

## X2 — NoFreshAllocation (LEMMA, lemma)

COPY consumes no previously-unallocated address; next content-allocation frontier of `d` unchanged.

*Derivation context:* A content-creating allocation extends `dom(Σ.C)`; by X1 that set is unchanged, so the frontier from which the next address is drawn is unchanged.

---

## X3 — SharedReference (LEMMA, lemma)

`ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`; placed addresses pre-exist (forced by X1 ∧ S3★).

*Derivation context:* The weakest precondition over all post-state mappings of `d` reduces to:
`wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`
(using `dom(Σ'.C) = dom(Σ.C)` by X1). Discharged at the pre-state by ASN-0058 C1.

---

## X4 — IdentityOfInstance (LEMMA, lemma)

Every appearance of a copied address resolves to the single value `Σ.C(a)` = `Σ'.C(a)`.

*Formal content:* If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`. The content store is a function (a key has one value).

---

## X5 — TransitiveIdentity (LEMMA, lemma)

The placed address is the content's original I-address through arbitrary copy chains.

*Derivation context:* Every address in `dom(Σ.C)` is produced by exactly one allocation event (S4, ASN-0036, via GlobalUniqueness, ASN-0034), and its `origin` is fixed once and for all by its own tumbler structure (S7). COPY allocates nothing (X1) and rewrites no I-coordinate (X3). Resolution reads the source arrangement to extract a *stored* I-address (`resolve` consults `Σ.M(d_s)`); because no COPY hop ever allocates a fresh address or alters an existing one, the tumbler resolution extracts is identically the one produced at that address's single allocation event, whether `d_s` authored the content or obtained it by any number of prior COPYs.

---

## X6 — OriginPreservation (LEMMA, lemma)

For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run).

---

## X7 — NonDestructivePlacement (LEMMA, lemma)

`(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`

*Derivation context:* The shift `· + W` restricted to `{u ∈ V_{s_C}(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4); its image lies at or above `v + W`. The copied `[v, v+W)` and displaced-image `[v+W, …)` ranges are disjoint by the X16 tiling.

---

## X8 — RunFragmentation (LEMMA, lemma)

The copied region is *constructed* as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per run of the resolution list `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`).

*(a) Within a single reference:* no two blocks coalesce. The copied blocks of one reference are target-V-adjacent by construction (`c_{j+1} = c_j + n_j`) and carry their source I-coordinates unchanged; source-V-adjacent-but-not-I-adjacent runs (by M7's conjunction ruling out source-V-adjacent pairs from being I-adjacent) become target-V-adjacent-but-not-I-adjacent blocks. Hence no within-reference pair is a merge candidate.

*(b) Across an inter-reference boundary:* the last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and may also be I-adjacent — precisely when they share an origin and abut in I-space (`a' = a + n`, M16/M16a). Such a boundary satisfies merge condition M7 and coalesces.

Merging the copied blocks among themselves yields `≤ k` blocks, with equality exactly when no inter-reference boundary is I-adjacent.

---

## X9 — ContiguousTargetRange (LEMMA, lemma)

Although the source may fragment into `k` runs and may draw from several source documents, the copied content occupies one *contiguous* V-range `[v, v + W)` in the target, in source order.

*Derivation context:* The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order.

---

## X10 — SourceHandling (LEMMA, lemma)

*(a) Non-interference for sources `d' ≠ d`:* No source document other than the target is altered: `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and `Σ'.C = Σ.C`. In particular, when a source `d_s ≠ d`, `Σ'.M(d_s) = Σ.M(d_s)` — its arrangement, its referenced content, and (by X6) the origins of its content are all untouched.

*(b) Snapshot resolution for `d_s = d`:* When the source *is* the target (self-transclusion), the source document is not unaltered — it is the target, and its content-subspace arrangement is displaced by `· + W`. The guarantee is *pre-state resolution*: `resolve_Σ(R)` reads `Σ.M(d)` before the displacement opens the gap. By the atomicity of COPY (X15), the precondition — including the resolution `resolve_Σ(R)` — is evaluated against the pre-state `Σ` in one indivisible step; thus `resolve_Σ(R)` reads `Σ.M(d)` *before* the displacement opens the gap.

---

## X11 — CrossOriginSeparation (LEMMA, lemma)

When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge.

*Derivation context:* The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce.

---

## X12 — BoundaryAbsorption (LEMMA, lemma)

The copied region meets the surrounding arrangement at two boundaries, each an independent merge candidate under M7 (V-adjacency given at both by construction; I-adjacency is the discriminating test):

- *Leading boundary* (present iff `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).
- *Trailing boundary* (present iff `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. A boundary across which origins differ cannot be absorbed (X11).

---

## X13 — Multiplicity (LEMMA, lemma)

After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance — and the model imposes no bound on such multiplicity (ASN-0036, S5, UnrestrictedSharing). A single I-address may be referenced from arbitrarily many documents and positions; COPY is the operation that increases this multiplicity without increasing the content store.

---

## X14 — ContainmentRecording (LEMMA, lemma)

At completion, `d` contains each copied address: `(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so `Contains_C(Σ') ⊇ {(a_j + i, d)}`, and COPY's effect has written the corresponding pairs into `Σ.R` (Definition: `Σ'.R = Σ.R ∪ {(a_j + i, d)}`).

Write the copied address set `A = {a_j + i : 1 ≤ j ≤ k, 0 ≤ i < n_j}` and split at pre-state `Σ`: `New = A ∖ ran(Σ.M(d))`, `Old = A ∩ ran(Σ.M(d))`.

**Coupling discharges (step-local recording fact SL):** The sole `s_C`-range growth COPY's own step contributes is `New`; COPY records `(a, d)` for every `a ∈ A ⊇ New`.

- *J0 (AllocationPlacementCoupling):* Vacuous — by X1, `dom(Σ'.C) = dom(Σ.C)`, so the antecedent `a ∈ dom(Σ'.C) ∖ dom(Σ.C)` is never satisfied.
- *J1★ (ExtensionRecordsProvenance), composite-wide:* COPY's own step's sole `s_C`-range growth is `New`; every member of `A ⊇ New` recorded into `Σ'.R`; by provenance permanence (P2) each pair persists into `R_clo`.
- *J1'★ (ProvenanceRequiresExtension), composite-wide:* Split `A` at opening boundary `B`.
  - `a ∉ ran_{s_C}(B.M(d))`: COPY maps `a` at a content-subspace position `v + c` (P3, PC3), so `a ∈ ran_{s_C}(Σ'.M(d))`; J1'★'s consequent is met.
  - `a ∈ ran_{s_C}(B.M(d))`: then `(a, d) ∈ Contains_C(B)` and P4★ at boundary `B` gives `(a, d) ∈ R_B`; hence `(a, d) ∉ R_clo ∖ R_B`, antecedent vacuous.
- *P7 (ProvenanceGrounding):* Every pair COPY adds is `(a_j + i, d)` with `a_j + i ∈ A`; by C1 every such address lies in `dom(Σ.C) = dom(Σ'.C)` (X1).
- *P4★ (`Contains_C ⊆ R`), composite boundary:* Base case `Σ₀`: `Contains_C(Σ₀) = ∅ ⊆ R₀`. Step case from P4★ at boundary `B` plus composite-wide J1★: for any `(a, d) ∈ Contains_C(Σ_clo)`, either `a ∈ ran_{s_C}(B.M(d))` (P4★ at `B` yields `(a, d) ∈ R_B ⊆ R_clo`) or `a` is range-new across the composite (J1★ yields `(a, d) ∈ R_clo`).
- *P3 (ExtendedTransitionInvariants):* `dom(C) ⊆ dom(C')` and value-fixity from `Σ'.C = Σ.C`; `dom(L) ⊆ dom(L')` and value-fixity from `Σ'.L = Σ.L`; `E ⊆ E'` from `Σ'.E = Σ.E`; `R ⊆ R'` from `Σ'.R = Σ.R ∪ {…} ⊇ Σ.R`.
- *Link/entity invariants (L0, L1, L1a–c, L3, L14, L-fin, CL-OWN, CL-UNIQ, P8, NodeLineage, ActivatedEmission):* Preserved because `Σ'.L = Σ.L` and `Σ'.E = Σ.E`.

---

## X15 — Atomicity (LEMMA, lemma)

COPY either applies in full — establishing X1, X3, X7, S2, S3★, and the subspace's density discipline D-SEQ (X16) together — or not at all; no intermediate state is observable in which the displacement has been applied but the copied region not yet laid down, or vice versa.

*Derivation context:* COPY is a *single* elementary transition (Definition), not a composite of K.μ steps, so SequentialTransitionAxiom (ASN-0047/0093) applies directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step. A partial application would leave `Σ'.M(d)` either non-dense (a V-gap, contradicting X16) or double-bound (two I-addresses at one position), violating arrangement well-formedness.

---

## X16 — PostStateDensity (INV, predicate)

The post-state content subspace `V_{s_C}(d)` in `Σ'` is exactly `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN).

*Derivation:* The three classes of post-state `s_C`-positions occupy disjoint last-component ranges:

- *unmoved* (`u < v`): last component `c ∈ [1, p)`
- *copied* (`v + c`, `0 ≤ c < W`): last component `c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`

These three ranges tile `[1, n_S + W]` exactly:
`[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap and no gap (every integer in `[1, n_S + W]` lies in exactly one range, using `1 ≤ p ≤ n_S + 1`).

The minimum is `[s_C,1,…,1]`: when `p ≥ 2` it is the unmoved `c = 1` position; when `p = 1` the unmoved range is empty and `c = 1` is the first copied position.

*(Empty-subspace specialisation `n_S = 0`, `p = 1`, `W ≥ 1`:)* result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at the chosen depth `m`, with minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.

**S2 (functionality) discharge:** The tiling establishes pairwise disjointness within `s_C`; link-subspace V-positions and content-subspace V-positions have distinct first components (`s_L ≠ s_C`), so they disagree at position 1 and are distinct tumblers by T3 (CanonicalRepresentation, ASN-0034) — disjointness across the subspace boundary. Together: all post-state V-positions are pairwise distinct, so `Σ'.M(d)` is a well-defined partial function.
