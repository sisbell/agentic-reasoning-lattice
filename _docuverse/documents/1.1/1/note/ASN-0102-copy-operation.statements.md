# ASN-0102 Claim Statements

*Source: ASN-0102-copy-operation.md (revised 2026-05-28) — Extracted: 2026-05-28*

## Definition — CopyResolution

`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`

Where `R = ⟨r₁, …, r_p⟩`, each `rᵢ = (d_i, σ_i)` a well-formed content reference. The cumulative offset `c_j = (+ j' : 1 ≤ j' < j : n_{j'})`. `k` is the number of maximal contiguous I-runs the source occupies (C1a, M12).

## Definition — CopyBlockSet

`B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`

A contiguous lay-down of the resolved I-sequence at consecutive target V-positions, with `c_{j+1} = c_j + n_j`.

## Definition — CopyOperation

**Preconditions:**

- **(P1) Source resolvable at `Σ`, into the content subspace.** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference (ASN-0058) with `d_i ∈ dom(Σ.M)` and, writing `σ_i = (u_i, ℓ_i)` for its V-span, **`subspace(u_i) = s_C`** — every source span resolves within its source document's *content* subspace, so `V_{s_C}(d_i) ≠ ∅` and `resolve_Σ(R)` is defined. Since `p ≥ 1` and each reference has positive resolved width (C2 gives `w(resolve_Σ(r_i)) = ℓ_{i,m} ≥ 1`), the total width satisfies **`W ≥ 1`**.
- **(P2) Target document.** `d ∈ E_doc`, equivalently `d ∈ dom(Σ.M)`.
- **(P3) Content subspace.** The target subspace is the content (byte) subspace: `S = s_C`. This pins `subspace(v) = s_C` for the inserted positions.
- **(P4) Valid insertion position.** Write `n_S = |V_{s_C}(d)|`.
  - *Non-empty subspace* (`n_S ≥ 1`): `v = [s_C,1,…,1,p]` with `1 ≤ p ≤ n_S + 1` (ASN-0036, ValidInsertionPosition).
  - *Empty subspace* (`n_S = 0`): operation chooses depth `m ≥ 2` and takes `v = [s_C,1,…,1]` of depth `m` (ASN-0036, ValidFirstInsertionPosition), with `p = 1`.

**Effect** of `COPY(R, d, v)` carrying `Σ → Σ'`:

- **Content store — untouched.** `Σ'.C = Σ.C`.
- **Link store — untouched.** `Σ'.L = Σ.L`.
- **Entity set — untouched.** `Σ'.E = Σ.E`.
- **Other documents — untouched.** `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`.
- **Target arrangement.** `Σ'.M(d)` is:
  - `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ s_C`, or with `subspace(u) = s_C ∧ u < v`;
  - `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W` (the copied region `B_copy`);
  - `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_{s_C}(d)` with `u ≥ v` (the displaced region).
- **Provenance.** `Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`.

---

## COPY — CopyTransition (DEF, operation)

`COPY(R, d, v)` (single elementary transition; precond. P1–P4, target subspace `S = s_C`): `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; content subspace displaced forward by `W` and gap `[v, v+W)` bound to `resolve_Σ(R)` in order; `Σ'.R = Σ.R ∪ {(a_j+i, d)}`

## X1 — ContentStoreInvariance (LEMMA, postcondition)

`dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`

## X2 — NoFreshAllocation (LEMMA, corollary)

COPY consumes no previously-unallocated address; next content-allocation frontier of `d` unchanged.

*Derivation:* A content-creating allocation extends `dom(Σ.C)`; by X1 that set is unchanged, so the frontier from which the next address is drawn is unchanged.

## X3 — SharedReference (LEMMA, postcondition)

`ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`

Placed addresses pre-exist (forced by X1 ∧ S3★). The whole of S3★ reduces to:

`wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`

(using `dom(Σ'.C) = dom(Σ.C)` by X1).

## X4 — IdentityOfInstance (LEMMA, postcondition)

If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`.

## X5 — TransitiveIdentity (LEMMA, property)

The address placed by COPY is the content's *original* I-address, irrespective of how many copy hops separate source from origin.

*Derivation:* Every address in `dom(Σ.C)` is produced by exactly one allocation event (S4, ASN-0036, via GlobalUniqueness, ASN-0034), and its `origin` is fixed once and for all by its own tumbler structure (S7). COPY allocates nothing (X1) and rewrites no I-coordinate (X3). Resolution reads the source arrangement to extract a *stored* I-address (ASN-0058 `resolve` consults `Σ.M(d_s)`); because no COPY hop ever allocates a fresh address or alters an existing one, the tumbler resolution extracts is identically the one produced at that address's single allocation event — whether `d_s` authored the content or itself obtained it by any number of prior COPYs.

## X6 — OriginPreservation (LEMMA, postcondition)

For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run).

## X7 — NonDestructivePlacement (LEMMA, postcondition)

`(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`

*Derivation notes:*
- The shift `· + W` restricted to `{u ∈ V_{s_C}(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4), and its image lies at or above `v + W`.
- The *freed* positions (displaced content's pre-state slots) are last-components `[p, n_S]`: every position at or after `v` in `V_{s_C}(d)`, all vacated by shift `· + W`.
- The *portion of the copy target region `[v, v+W)`* that was occupied pre-state is `[p, min(n_S, p+W−1)]` — a proper subset of freed slots when `W < n_S − p + 1`.
- The no-overwrite conclusion rests on disjointness: copied region (last-components `[p, p+W)`) and displaced image (last-components `[p+W, n_S+W]`) occupy disjoint ranges.

## X8 — RunFragmentation (LEMMA, structural)

The copied region is *constructed* as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per maximal contiguous I-run of `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`). Canonical count `≤ k`, with equality exactly when no inter-reference boundary is I-adjacent.

Sub-cases:
- *Within a single reference*: consecutive runs never coalesce. (a) The reference span `⟦σ⟧` is V-contiguous and fully populated; maximal runs of `f = M(d_s)|⟦σ⟧` are V-adjacent (`v_{j+1} = v_j + n_j`). (b) With V-adjacency, maximality of run `j` gives `f(v_j + n_j) ≠ a_j + n_j`, hence `a_{j+1} ≠ a_j + n_j` — M7's merge condition fails.
- *Across an inter-reference boundary*: the last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and coalesce iff I-adjacent (`a' = a + n`, M16/M16a).

## X9 — ContiguousTargetRange (LEMMA, postcondition)

The copied content occupies one *contiguous* V-range `[v, v + W)` in the target, in source order.

*Derivation:* Blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b).

## X10 — SourceNonInterference (LEMMA, postcondition)

`(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and `Σ'.C = Σ.C`.

*Self-transclusion case* (`d_s = d`): by SequentialTransitionAxiom (ASN-0047/0093) the precondition — including `resolve_Σ(R)` — is evaluated against the pre-state `Σ` and the effect is committed to `Σ'` in one indivisible step. Thus `resolve_Σ(R)` reads `Σ.M(d)` *before* the displacement opens the gap.

## X11 — CrossOriginSeparation (LEMMA, structural)

When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge (M7 ∧ M16); distinct portions stay distinguishable.

*Derivation:* The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce.

## X12 — BoundaryAbsorption (LEMMA, structural)

The copied region meets the surrounding arrangement at *two* boundaries, each an independent merge candidate under M7:

- *Leading boundary* (present iff `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).
- *Trailing boundary* (present iff `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. Origin carried intact by the addresses (X6); a boundary across which origins differ cannot be absorbed (X11).

## X13 — Multiplicity (LEMMA, postcondition)

After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance — and the model imposes no bound on such multiplicity (ASN-0036, S5, UnrestrictedSharing). A single I-address may be referenced from arbitrarily many documents and positions.

## X14 — ContainmentRecording (LEMMA, coupling discharge)

`(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so `Contains_C(Σ') ⊇ {(a_j + i, d)}`.

Provenance effect: `Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`.

Coupling discharges. Write `A = {a_j + i : 1 ≤ j ≤ k, 0 ≤ i < n_j}`, `New = A ∖ ran(Σ.M(d))`, `Old = A ∩ ran(Σ.M(d))`:

- *J0 (AllocationRequiresPlacement).* Vacuous: by X1, `dom(Σ'.C) = dom(Σ.C)`, so `a ∈ dom(Σ'.C) ∖ dom(Σ.C)` is never satisfied.
- *J1★ (ExtensionRecordsProvenanceContentSubspace).* For each `a ∈ New` the provenance effect records `(a, d) ∈ Σ'.R`. For `a ∈ Old`, J1★'s antecedent `a ∈ ran(Σ'.M(d)) ∖ ran(Σ.M(d))` is false.
- *J1'★ (ProvenanceRequiresExtension).* *(a) `a ∈ New`:* `a ∈ ran(Σ'.M(d)) ∖ ran(Σ.M(d))` at a copied position in subspace `s_C` (P3). *(b) `a ∈ Old`:* `(a, d) ∈ Contains_C(Σ)`, and by P4★ `(a, d) ∈ R` at pre-state, so `(a, d) ∉ R' ∖ R` — vacuously satisfied.
- *P7 (ProvenanceGrounding):* `(a, d) ∈ R ⟹ a ∈ dom(C)`. Every pair COPY adds: `a_j + i ∈ dom(Σ.C)` by C1 (via P1, X3) and X1.
- *P4★ at post-state:* `Contains_C(Σ') = Contains_C(Σ) ∪ {(a_j + i, d)} ⊆ R'`.

## X15 — Atomicity (LEMMA, property)

COPY either applies in full — establishing X1, X3, X7, S2, S3★, and the subspace's density discipline D-SEQ (X16) together — or not at all; no intermediate state is observable in which the displacement has been applied but the copied region not yet laid down, or vice versa.

*Derivation:* COPY is a *single* elementary transition (Definition), so SequentialTransitionAxiom (ASN-0047/0093) applies directly: precondition read against `Σ` and effect committed to `Σ'` in one indivisible step, with no intermediate state between. A partial application would leave `Σ'.M(d)` either non-dense (a V-gap, contradicting X16) or double-bound (two I-addresses at one position).

## X16 — PostStateDensity (LEMMA, postcondition)

Post-state `V_{s_C}(d) = {[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN).

*Derivation:* The three classes of post-state `s_C`-positions occupy disjoint last-component ranges:
- *unmoved* (`u < v`): last component `c ∈ [1, p)`;
- *copied* (`v + c`, `0 ≤ c < W`): last component `c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`;
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`.

These tile `[1, n_S + W]` exactly: `[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap and no gap, using `1 ≤ p ≤ n_S + 1`. The minimum `[s_C,1,…,1]` holds because `c = 1` is occupied (unmoved when `p ≥ 2`, first copied when `p = 1`).

*Empty-subspace case* (`n_S = 0`): specialisation `p = 1`, `W ≥ 1` — result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at depth `m` chosen in P4, minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.

*S8a for all post-state positions:*
- *Copied positions:* each `v + c = [s_C,1,…,1,p+c]` (`0 ≤ c < W`) has `zeros = 0`, depth `m ≥ 2`, all components positive.
- *Displaced positions:* each `u + W = shift(u, W)` for `u ∈ V_{s_C}(d)` with `u ≥ v` inherits S8a from `u` — shift preserves S8a and depth (`#shift(u, W) = #u = m`, OrdShiftHom (c)).
