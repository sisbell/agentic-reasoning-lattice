# ASN-0102 Claim Statements

*Source: ASN-0102-copy-operation.md (revised 2026-05-28) — Extracted: 2026-06-08*

## Definition — CopyResolution

Source designation: `R = ⟨r₁, …, r_q⟩`, each `rᵢ = (d_i, σ_i)` a well-formed content reference. Resolution pinned to pre-state `Σ`:

`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

## Definition — CopiedBlockSet

Cumulative offset: `c_j = (+ j' : 1 ≤ j' < j : n_{j'})`.

Copied block set: `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`.

## Definition — CopyOperation

**Preconditions:**

- **(PC1)** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference (ASN-0058) with `d_i ∈ dom(Σ.M)` and, writing `σ_i = (u_i, ℓ_i)` for its V-span, `subspace(u_i) = s_C`, so `V_{s_C}(d_i) ≠ ∅`, `resolve_Σ(R)` is defined, and by C1 (ResolutionIntegrity, ASN-0058) every resolved address lies in `dom(Σ.C)`. Since `q ≥ 1` and each reference has positive resolved width (C2 gives `w(resolve_Σ(r_i)) = ℓ_{i,m} ≥ 1`), the total width satisfies `W ≥ 1`.
- **(PC2)** `d ∈ E_doc`, equivalently `d ∈ dom(Σ.M)`.
- **(PC3)** `S = s_C`.
- **(PC4)** Write `n_S = |V_{s_C}(d)|`. *Non-empty* (`n_S ≥ 1`): positions of `V_{s_C}(d)` are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S` at common depth `m`, and `v = [s_C,1,…,1,p]` is a valid insertion position with `1 ≤ p ≤ n_S + 1`. *Empty* (`n_S = 0`): depth `m ≥ 2` chosen, `v = [s_C,1,…,1]` of depth `m`, `p = 1`.

**Effect** (`Σ → Σ'`):

- `Σ'.C = Σ.C`
- `Σ'.L = Σ.L`
- `Σ'.E = Σ.E`
- `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`
- `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ s_C`, or with `subspace(u) = s_C ∧ u < v`
- `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W`
- `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_{s_C}(d)` with `u ≥ v`
- `Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`

---

## COPY — CopyTransition (DEF, function)

`COPY(R, d, v)` (single elementary transition; precond. PC1–PC4, target subspace `S = s_C`): `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; content subspace displaced forward by `W` and gap `[v, v+W)` bound to `resolve_Σ(R)` in order; `Σ'.R = Σ.R ∪ {(a_j+i, d)}`

## X1 — ContentStoreInvariance (LEMMA, lemma)

`dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`

Immediate from `Σ'.C = Σ.C`.

## X2 — SharedReference (LEMMA, lemma)

`ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`

Forced by X1 together with S3★, discharged at the pre-state by C1 (PC1).

Weakest-precondition form:

`wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`

(using `dom(Σ'.C) = dom(Σ.C)` by X1, with PC3 fixing the inserted subspace to `s_C`).

## X3 — IdentityOfInstance (LEMMA, lemma)

If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`.

## X4 — TransitiveIdentity (LEMMA, lemma)

The address placed by COPY is the content's original I-address, irrespective of how many copy hops separate source from origin.

Formal basis: Every address in `dom(Σ.C)` is produced by exactly one allocation event (S4) and its `origin` is fixed once and for all by its own tumbler structure (S7). COPY allocates nothing (X1) and rewrites no I-coordinate (X2). Resolution reads `Σ.M(d_s)` to extract a stored I-address; because no COPY hop ever allocates a fresh address or alters an existing one, the tumbler resolution extracts is identically the one produced at that address's single allocation event. Hence `a` is the same tumbler at the end of any chain `… → d_s → d`.

## X5 — OriginPreservation (LEMMA, lemma)

For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run).

## X6 — NonDestructivePlacement (LEMMA, lemma)

`(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`

The shift `· + W` restricted to `{u ∈ V_{s_C}(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4), and its image lies at or above `v + W`. The copied range `[v, v+W)` and the displaced-image range `[v+W, n_S+W]` are disjoint (the tiling of X15), so no copied mapping collides with a displaced one.

## X7 — RunFragmentation (LEMMA, lemma)

The copied region is constructed as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per run of the resolution list `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`). This constructed count `k` tracks the resolution-run count of the source, independent of `W`.

- *Within a single reference*: no two blocks coalesce. Source-V-adjacent consecutive maximal runs are not I-adjacent (M7 conjunction, ASN-0058, C1a/M12); copy alters no I-coordinate; so target-V-adjacent-but-not-I-adjacent blocks cannot merge.
- *Across an inter-reference boundary*: the last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and coalesce exactly when they share an origin and abut in I-space (`a' = a + n`, M16/M16a), satisfying merge condition M7.

Merging the copied blocks among themselves yields `≤ k` blocks, with equality exactly when no inter-reference boundary is I-adjacent.

## X8 — ContiguousTargetRange (LEMMA, lemma)

The copied content occupies one contiguous V-range `[v, v + W)` in the target, in source order.

The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order.

## X9 — SourceHandling (LEMMA, lemma)

**(a) Non-interference for sources `d_s ≠ d`.**
`Σ'.M(d_s) = Σ.M(d_s)` (instantiating the "other documents" clause at `d' = d_s ≠ d`), so its arrangement, its referenced content, and the origins of its content (by X5) are all unchanged.

**(b) Snapshot resolution for `d_s = d`.**
When the source is the target (self-transclusion), the target-as-source is read at the pre-state `Σ` and is itself displaced by `· + W` (not unaltered). `resolve_Σ(R)` consults `Σ.M(d)`, not `Σ'.M(d)`.

## X10 — CrossOriginSeparation (LEMMA, lemma)

When the copied content draws from two or more origins, blocks with different origins cannot merge.

The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce.

## X11 — BoundaryAbsorption (LEMMA, lemma)

The copied region meets the surrounding arrangement at two boundaries, each an independent merge candidate under M7:

- *Leading boundary* (present iff `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).
- *Trailing boundary* (present iff `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged; each may absorb, both may, or neither; the conditions are independent. A boundary across which origins differ cannot be absorbed (X10).

## X12 — Multiplicity (LEMMA, lemma)

After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance.

Each copied address `a` is at the post-state the image of a copied target position `v + c` (COPY effect clause), and also retains a source appearance `v_s` with `Σ.M(d_s)(v_s) = a` (PC1). When `d_s ≠ d`: source arrangement untouched (X9(a)), `v_s ∈ dom(Σ'.M(d_s))`, different document from `v + c`. When `d_s = d`: source is displaced but survives (X6) to `v_s + W` (if `v_s ≥ v`) or held fixed (if `v_s < v`); the surviving source position is either below `v` or at-or-above `v + W` (X15 tiling), hence `≠ v + c ∈ [v, v+W)`. Hence at least two distinct `(document, V-position)` pairs reference `a` in `Σ'`.

The model imposes no upper bound: a single I-address may be referenced from arbitrarily many documents and positions (ASN-0036, S5, UnrestrictedSharing).

## X13 — ContainmentRecording (LEMMA, lemma)

`(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so `Contains_C(Σ') ⊇ {(a_j + i, d)}`, and `Σ'.R = Σ.R ∪ {(a_j+i, d)}`.

Copied address set: `A = {a_j + i : 1 ≤ j ≤ k, 0 ≤ i < n_j}`. Every member of `A` is the image of a copied position `v + c` (`0 ≤ c < W`) in `Σ'.M(d)` (COPY effect clause, PC3), so `A ⊆ ran_{s_C}(Σ'.M(d))`.

**Step-local recording fact (SL):** COPY records `(a, d)` for every `a ∈ A` (Definition), and each such `a` is content-subspace-range-resident — `a ∈ ran_{s_C}(Σ'.M(d))` — at COPY's post-state `Σ'`; by provenance permanence (P2) every recorded pair persists.

## X14 — Atomicity (INV, predicate)

COPY is a single elementary transition (Definition) in all cases — not a composite of K.μ steps — so SequentialTransitionAxiom (ASN-0047/0093) applies to it directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step, with no observable intermediate state.

## X15 — PostStateDensity (LEMMA, lemma)

The post-state content subspace `V_{s_C}(d)` in `Σ'` is exactly `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN).

The three classes of post-state `s_C`-positions occupy disjoint last-component ranges:

- *unmoved* (`u < v`): last component `c ∈ [1, p)`
- *copied* (`v + c`, `0 ≤ c < W`): last component `p + c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`

These tile `[1, n_S + W]` exactly: `[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap and no gap (every integer in `[1, n_S + W]` lies in exactly one range, using `1 ≤ p ≤ n_S + 1`). The minimum `[s_C,1,…,1]`: when `p ≥ 2` it is the unmoved `c = 1` position; when `p = 1` the unmoved range is empty and `c = 1` is the first copied position; D-MIN holds in either case.

*(Empty-subspace specialisation `n_S = 0`):* `p = 1`, `W ≥ 1`; result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at the depth `m` chosen in PC4, minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.

## X16 — InvariantPreservation (LEMMA, lemma)

COPY maintains every invariant `ValidComposite★` (ASN-0047) binds at its post-state: the per-state `ExtendedReachableStateInvariants` conjunction (including P7), the composite-boundary properties P4★/P4a/P7a, and the transition theorem P3.

**Range routing (RR):**

`ran_{s_C}(Σ'.M(d)) = ran_{s_C}(Σ.M(d)) ∪ A`

Each member of the post-state range reaches `R'` by one of two routes:
- *(carried)* `a ∈ ran_{s_C}(Σ.M(d))`: by P4★ at `Σ_0`, `(a, d) ∈ R_{Σ_0}`, carried into `R'` by P2.
- *(recorded)* `a ∈ A`: COPY's unconditional write (SL) records `(a, d) ∈ R'` directly.

**J1★/J1'★:** For a recorded pair `(a, d)` with `a ∈ A`: if `a ∈ ran_{s_C}(M_{Σ_0}(d))`, RR's carried route gives `(a, d) ∈ R_{Σ_0}`, pair not `R`-new, J1'★ vacuous; otherwise `a` is range-new, COPY's write meets J1★ and satisfies J1'★'s consequent.

**P7 (ProvenanceGrounding):** Every pair COPY adds is `(a_j + i, d)` with `a_j + i ∈ A`; by C1 (via PC1, X2) every such address lies in `dom(Σ.C) = dom(Σ'.C)` (X1). The pair is well-typed: `d ∈ E_doc` (PC2); `Element(a_j + i)` holds since `a_j + i ∈ dom(Σ.C)` and by S7b every content address has `zeros = 3`.

**P3 (ExtendedTransitionInvariants):** `dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`. Discharged directly from COPY's frame: `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.R = Σ.R ∪ {(a_j+i, d)} ⊇ Σ.R`.

**P4★ (`Contains_C(Σ') ⊆ R'`):** For `(a, d') ∈ Contains_C(Σ')`: if `d' ≠ d`, frame gives `(a, d') ∈ Contains_C(Σ)`, pre-state P4★ places it in `R`, P2 in `R'`; if `d' = d`, `a ∈ ran_{s_C}(Σ'.M(d))`, RR routes `(a, d)` into `R'`.

**P7a (`(A a ∈ dom(Σ'.C) :: (E d' :: (a, d') ∈ R'))`):** By X1, `dom(Σ'.C) = dom(Σ.C)`; pre-state P7a furnishes each such `a` a record `(a, d') ∈ R`, carried into `R'` by P2.

**P4a (TraceWitnessing):** A pair already in `R` is witnessed at some state of the reaching prefix by the inductive hypothesis; a pair in `R' ∖ R` is one COPY recorded (X13), so `d' = d`, `a ∈ A`, and `a` is content-subspace-resident at `Σ'` by SL, witnessed by `Σ'` itself.
