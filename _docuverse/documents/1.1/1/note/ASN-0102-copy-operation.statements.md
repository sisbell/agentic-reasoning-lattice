# ASN-0102 Claim Statements

*Source: ASN-0102-copy-operation.md (revised 2026-05-28) — Extracted: 2026-06-03*

## Definition — CopyPreconditions

**P1 (Source resolvable at Σ, into the content subspace).** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference (ASN-0058) with `d_i ∈ dom(Σ.M)` and, writing `σ_i = (u_i, ℓ_i)` for its V-span, `subspace(u_i) = s_C` — every source span resolves within its source document's content subspace, so `V_{s_C}(d_i) ≠ ∅` and `resolve_Σ(R)` is defined. Since `q ≥ 1` and each reference has positive resolved width (C2 gives `w(resolve_Σ(r_i)) = ℓ_{i,m} ≥ 1`), the total width satisfies `W ≥ 1` — the empty copy is excluded.

**P2 (Target document).** `d ∈ E_doc`, equivalently `d ∈ dom(Σ.M)`.

**P3 (Content subspace).** The target subspace is the content (byte) subspace: `S = s_C`. This pins `subspace(v) = s_C` for the inserted positions.

**P4 (Valid insertion position).** Write `n_S = |V_{s_C}(d)|`.
- *Non-empty subspace* (`n_S ≥ 1`): by D-SEQ the positions of `V_{s_C}(d)` are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S` at the common depth `m` (S8-depth), and `v = [s_C,1,…,1,p]` is a valid insertion position with `1 ≤ p ≤ n_S + 1` (ASN-0036, ValidInsertionPosition).
- *Empty subspace* (`n_S = 0`): there is no pre-existing common depth. The operation chooses a depth `m ≥ 2` and takes `v = [s_C,1,…,1]` of depth `m` (ASN-0036, ValidFirstInsertionPosition), with `p = 1`; this choice fixes `m` as the content-subspace depth of `d` for all subsequent positions.

## Definition — CopyResolution

`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

Every resolved address already exists: `(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C)))` (C1).

The run count `k = (+ i : 1 ≤ i ≤ q : k_i)`, where each `k_i` is the maximal-contiguous-I-run count of reference `r_i` taken in isolation.

## Definition — CopyOperation

The operation `COPY(R, d, v)` carries `Σ → Σ'` as follows.

**Content store — untouched.**
`Σ'.C = Σ.C`.

**Link store — untouched.**
`Σ'.L = Σ.L`.

**Entity set — untouched.**
`Σ'.E = Σ.E`.

**Other documents — untouched.**
`(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`.

**Target arrangement.** Write the cumulative offset `c_j = (+ j' : 1 ≤ j' < j : n_{j'})`, so the copied region is the block set

`B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`.

Formally `Σ'.M(d)` is the partial function:
- `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ s_C`, or with `subspace(u) = s_C ∧ u < v`;
- `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W` (the copied region `B_copy`);
- `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_{s_C}(d)` with `u ≥ v` (the displaced region).

**Provenance.**
`Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`.

## Definition — WeakestPreconditionS3Star

The weakest precondition of COPY with respect to S3★ reduces to a single membership obligation on the copied region:

`wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`

(using `dom(Σ'.C) = dom(Σ.C)` by X1; the relation is equality, not containment — these are exactly the new mappings S3★ constrains, and they are routed to `dom(Σ.C)` because P3 fixes their subspace to `s_C`).

---

## COPY — CopyTransition (DEF, operation)

`COPY(R, d, v)` (single elementary transition; precond. P1–P4, target subspace `S = s_C`): `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; content subspace displaced forward by `W` and gap `[v, v+W)` bound to `resolve_Σ(R)` in order; `Σ'.R = Σ.R ∪ {(a_j+i, d)}`

## X1 — ContentStoreInvariance (LEMMA, lemma)

`dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`

## X2 — NoFreshAllocation (LEMMA, lemma)

COPY consumes no previously-unallocated address: the set of addresses available to a subsequent content-creating allocation in `d` is identical before and after COPY.

*Derivation:* A content-creating allocation extends `dom(Σ.C)`; by X1 that set is unchanged, so the frontier from which the next address is drawn is unchanged.

## X3 — SharedReference (LEMMA, lemma)

`ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`

Every address introduced into `ran(Σ'.M(d))` by COPY already belonged to `dom(Σ.C)`. This is forced by X1 together with S3★, and is discharged at the pre-state by ASN-0058 C1 (resolution yields only existing addresses).

## X4 — IdentityOfInstance (LEMMA, lemma)

If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`.

## X5 — TransitiveIdentity (LEMMA, lemma)

The address placed by COPY is the content's original I-address, irrespective of how many copy hops separate source from origin.

*Structural fact:* Every address in `dom(Σ.C)` is produced by exactly one allocation event (S4, ASN-0036, via GlobalUniqueness, ASN-0034), and its `origin` is fixed once and for all by its own tumbler structure (S7). COPY allocates nothing (X1) and rewrites no I-coordinate (X3: the addresses it places already lie in `dom(Σ.C)`). The tumbler resolution extracts is identically the one produced at that address's single allocation event — whether `d_s` authored the content or itself obtained it by any number of prior COPYs.

## X6 — OriginPreservation (LEMMA, lemma)

For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run).

## X7 — NonDestructivePlacement (LEMMA, lemma)

`(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`

*Key structural facts used in derivation:*
- The shift `· + W` restricted to `{u ∈ V_{s_C}(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4), and its image lies at or above `v + W`, while the copied region occupies `[v, v+W)`; the two ranges are disjoint.
- The copied region (last-components `[p, p+W)`) and the displaced image (last-components `[p+W, n_S+W]`) occupy disjoint ranges.

## X8 — RunFragmentation (LEMMA, lemma)

The copied region is constructed as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per maximal contiguous I-run of `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`). The canonical block count is `≤ k`, with equality exactly when no inter-reference boundary is I-adjacent (in particular whenever consecutive references draw from distinct origins, X11).

*Sub-claims:*

*(a) Within a single reference:* Consecutive runs never coalesce. On a V-contiguous domain, the maximal runs of `f = M(d_s)|⟦σ⟧` (C1a, M12) are V-adjacent: the run after run `j` begins at `v_{j+1} = v_j + n_j`. With V-adjacency, maximality of run `j` — it cannot be right-extended, so `f(v_j + n_j) ≠ a_j + n_j` — gives `a_{j+1} ≠ a_j + n_j`, so M7's merge condition `a_{j+1} = a_j + n_j` fails.

*(b) Across an inter-reference boundary:* The last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and may also be I-adjacent — precisely when they share an origin and abut in I-space (`a' = a + n`, M16/M16a). Such a boundary satisfies merge condition M7 and coalesces in the canonical form.

## X9 — ContiguousTargetRange (LEMMA, lemma)

Although the source may fragment into `k` runs and may draw from several source documents, the copied content occupies one contiguous V-range `[v, v + W)` in the target, in source order.

*Derivation:* The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order.

## X10 — SourceHandling (LEMMA, lemma)

*(a) Non-interference for sources `d' ≠ d`.* No source document other than the target is altered: `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and `Σ'.C = Σ.C`.

*(b) Snapshot resolution for `d_s = d`.* When the source is the target (self-transclusion), the source document is not unaltered — it is the target, and its content-subspace arrangement is displaced by `· + W`. The guarantee that holds here is not non-alteration but pre-state resolution: the copied span is read against `Σ` before the displacement opens the gap. By SequentialTransitionAxiom (ASN-0047/0093) the precondition — including the resolution `resolve_Σ(R)` — is evaluated against the pre-state `Σ` and the effect is committed to `Σ'` in one indivisible step.

## X11 — CrossOriginSeparation (LEMMA, lemma)

When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge.

*Derivation:* The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce.

## X12 — BoundaryAbsorption (LEMMA, lemma)

The copied region meets the surrounding arrangement at two boundaries, each an independent merge candidate under M7:

- *Leading boundary* (present iff `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).
- *Trailing boundary* (present iff `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. After any absorption the merged block is indistinguishable from one never split (M8) — except that origin is carried intact by the addresses (X6). A boundary across which origins differ cannot be absorbed (X11).

## X13 — Multiplicity (LEMMA, lemma)

After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance — and the model imposes no bound on such multiplicity (ASN-0036, S5, UnrestrictedSharing). A single I-address may be referenced from arbitrarily many documents and positions; COPY is the operation that increases this multiplicity without increasing the content store.

## X14 — ContainmentRecording (LEMMA, lemma)

At completion, `d` contains each copied address: `(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so the derived content-containment relation records `Contains_C(Σ') ⊇ {(a_j + i, d)}`.

Provenance: `Σ'.R = Σ.R ∪ {(a_j + i, d)}`.

**Setup — `New` vs. `Old`:** Write copied address set `A = {a_j + i : 1 ≤ j ≤ k, 0 ≤ i < n_j}` and split: `New = A ∖ ran(Σ.M(d))` and `Old = A ∩ ran(Σ.M(d))`.

*Coupling discharges:*

- *J0 (AllocationRequiresPlacement).* Vacuous: by X1, `dom(Σ'.C) = dom(Σ.C)`, so the antecedent `a ∈ dom(Σ'.C) ∖ dom(Σ.C)` is never satisfied.

- *J1★ (ExtensionRecordsProvenanceContentSubspace).* The content-subspace range gains exactly `New`. For each `a ∈ New` the Definition's provenance effect records `(a, d) ∈ Σ'.R`. For `a ∈ Old`, J1★'s antecedent `a ∈ ran(Σ'.M(d)) ∖ ran(Σ.M(d))` is false.

- *J1'★ (ProvenanceRequiresExtension).* *(a) `a ∈ New`:* `a` is new to the content-subspace range, so `a ∈ ran(Σ'.M(d)) ∖ ran(Σ.M(d))` at a copied position in subspace `s_C` (P3). *(b) `a ∈ Old`:* `(a, d) ∈ Contains_C(Σ)`, and by P4★ (`Contains_C(Σ) ⊆ R`) the pair `(a, d)` is already in `R` at the pre-state. So `(a, d) ∉ R' ∖ R`, and J1'★'s antecedent is false — vacuously satisfied.

- *P7 (ProvenanceGrounding):* `(a, d) ∈ R ⟹ a ∈ dom(C)`. Every pair COPY adds is `(a_j + i, d)` with `a_j + i ∈ dom(Σ.C) = dom(Σ'.C)` (X1, C1).

- *P4★ at post-state:* `Contains_C(Σ') = Contains_C(Σ) ∪ {(a_j + i, d)}`. Each pre-state pair lies in `R ⊆ R'` by P4★ at `Σ`; each new pair `(a_j + i, d)` lies in `R'` by COPY's effect. Hence `Contains_C(Σ') ⊆ R'`.

## X15 — Atomicity (LEMMA, lemma)

COPY either applies in full — establishing X1, X3, X7, S2, S3★, and the subspace's density discipline D-SEQ (X16) together — or not at all; no intermediate state is observable in which the displacement has been applied but the copied region not yet laid down, or vice versa.

*Derivation:* COPY is a single elementary transition (Definition), not a composite of K.μ steps, so SequentialTransitionAxiom (ASN-0047/0093) applies to it directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step, with no intermediate state between. A partial application would leave `Σ'.M(d)` either non-dense (a V-gap, contradicting X16) or double-bound (two I-addresses at one position), violating arrangement well-formedness.

## X16 — PostStateDensity (LEMMA, lemma)

The post-state content subspace `V_{s_C}(d)` in `Σ'` is exactly `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN).

*Derivation:* By P4 the pre-state positions are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S`, and `v = [s_C,1,…,1,p]`. The three classes of post-state `s_C`-positions occupy disjoint last-component ranges:

- *unmoved* (`u < v`): last component `c ∈ [1, p)`;
- *copied* (`v + c`, `0 ≤ c < W`): last component `c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`;
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`.

These three ranges tile `[1, n_S + W]` exactly: `[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap and no gap (every integer in `[1, n_S + W]` lies in exactly one range, using `1 ≤ p ≤ n_S + 1`).

The minimum is `[s_C,1,…,1]`: when `p ≥ 2` it is the unmoved `c = 1` position; when `p = 1` the unmoved range is empty and `c = 1` is the first copied position.

(The empty-subspace case `n_S = 0` is the specialisation `p = 1`, `W ≥ 1`: the result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at the depth `m` chosen in P4, with minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.)
