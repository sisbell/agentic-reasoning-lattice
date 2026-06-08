# ASN-0102 Claim Statements

*Source: ASN-0102-copy-operation.md (revised 2026-05-28) — Extracted: 2026-06-08*

## Definition — CopyOperation

Preconditions PC1–PC4. The operation `COPY(R, d, v)` carries `Σ → Σ'` as follows.

**Inputs:** Content reference sequence `R = ⟨r₁, …, r_q⟩`, target document `d ∈ E_doc`, insertion position `v`. Resolution: `resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`, `W = (+ j : 1 ≤ j ≤ k : n_j)`. Cumulative offset `c_j = (+ j' : 1 ≤ j' < j : n_{j'})`. Copied block set `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`.

**Effect:**

- `Σ'.C = Σ.C`
- `Σ'.L = Σ.L`
- `Σ'.E = Σ.E`
- `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`
- `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ s_C`, or with `subspace(u) = s_C ∧ u < v`
- `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W`
- `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_{s_C}(d)` with `u ≥ v`
- `Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`

---

## Definition — CopyPreconditions

- **(PC1)** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference (ASN-0058) with `d_i ∈ dom(Σ.M)` and, writing `σ_i = (u_i, ℓ_i)` for its V-span, `subspace(u_i) = s_C`, so `V_{s_C}(d_i) ≠ ∅`, `resolve_Σ(R)` is defined, and by C1 (ResolutionIntegrity, ASN-0058) every resolved address lies in `dom(Σ.C)`. Since `q ≥ 1` and each reference has positive resolved width, `W ≥ 1`.
- **(PC2)** `d ∈ E_doc`, equivalently `d ∈ dom(Σ.M)`.
- **(PC3)** COPY targets the content subspace: `S = s_C`.
- **(PC4)** Write `n_S = |V_{s_C}(d)|`.
  - *Non-empty subspace* (`n_S ≥ 1`): `v = [s_C,1,…,1,p]` is a valid insertion position with `1 ≤ p ≤ n_S + 1`.
  - *Empty subspace* (`n_S = 0`): the operation chooses a depth `m ≥ 2` and takes `v = [s_C,1,…,1]` of depth `m`, with `p = 1`.

---

## Definition — Resolve

`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

Resolution is pinned to the pre-state `Σ` — `resolve_Σ(R)` consults `Σ.M(d)` at the pre-state.

---

## X1 — ContentStoreInvariance (INV, predicate)

`dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`

---

## X2 — SharedReference (LEMMA, lemma)

`ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`

Every address introduced into `ran(Σ'.M(d))` by COPY already belonged to `dom(Σ.C)`. Forced by X1 together with S3★, discharged at the pre-state by C1 (PC1).

---

## X3 — IdentityOfInstance (LEMMA, lemma)

If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`.

---

## X4 — TransitiveIdentity (LEMMA, lemma)

The address placed by COPY is the content's original I-address, irrespective of how many copy hops separate source from origin.

Every address in `dom(Σ.C)` is produced by exactly one allocation event (S4, ASN-0036), and its `origin` is fixed once and for all by its own tumbler structure (S7). COPY allocates nothing (X1) and rewrites no I-coordinate (X2). Resolution reads the source arrangement to extract a stored I-address (`resolve` consults `Σ.M(d_s)`); because no COPY hop ever allocates a fresh address or alters an existing one, the tumbler resolution extracts is identically the one produced at that address's single allocation event — whether `d_s` authored the content or itself obtained it by any number of prior COPYs. Hence `a` is the same tumbler at the end of any chain `… → d_s → d`.

---

## X5 — OriginPreservation (LEMMA, lemma)

For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run).

---

## X6 — NonDestructivePlacement (LEMMA, lemma)

`(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`

Every pre-existing binding of `d` survives COPY, relabelled by the forward shift on the content subspace `s_C`.

---

## X7 — RunFragmentation (LEMMA, lemma)

The copied region is constructed as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per run of the resolution list `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`). This constructed count `k` tracks the resolution-run count of the source, independent of the width `W`.

Within-region merge yields `≤ k` blocks, with equality exactly when no inter-reference boundary is I-adjacent (in particular whenever consecutive references draw from distinct origins, X10).

Sub-cases:

**(a) Within a single reference:** no two blocks coalesce. The copied blocks are target-V-adjacent by construction and carry source I-coordinates unchanged; a within-reference target merge candidate would require consecutive resolved runs to be I-adjacent in the source, but maximal-merge (ASN-0058, C1a/M12) forbids any source-V-adjacent pair from also being I-adjacent (M7's conjunction). Since copy alters no I-coordinate, source-V-adjacent-but-not-I-adjacent runs become target-V-adjacent-but-not-I-adjacent blocks. Hence no within-reference pair is a merge candidate.

**(b) Across an inter-reference boundary:** the last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and may be I-adjacent — precisely when they share an origin and abut in I-space (`a' = a + n`, M16/M16a). Such a boundary satisfies M7 and coalesces.

---

## X8 — ContiguousTargetRange (LEMMA, lemma)

The copied content occupies one contiguous V-range `[v, v + W)` in the target, in source order.

The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order.

---

## X9 — SourceHandling (LEMMA, lemma)

**(a) Non-interference for sources `d_s ≠ d`.**
`Σ'.M(d_s) = Σ.M(d_s)`

A source document other than the target is left untouched by COPY's frame — instantiating the definition's "other documents" clause at `d' = d_s ≠ d`. Its arrangement, its referenced content, and the origins of its content (by X5) are all unchanged.

**(b) Snapshot resolution for `d_s = d`.**
When the source is the target (self-transclusion), the guarantee is pre-state pinning, not non-alteration: the target-as-source is read at the pre-state `Σ` and is itself displaced by `· + W` (not unaltered).

---

## X10 — CrossOriginSeparation (LEMMA, lemma)

When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge.

The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce.

---

## X11 — BoundaryAbsorption (LEMMA, lemma)

The copied region meets the surrounding arrangement at two boundaries, each an independent merge candidate under M7:

**(a) Leading boundary** (present iff `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).

**(b) Trailing boundary** (present iff `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. After any absorption the merged block is indistinguishable from one never split (M8), except that origin is carried intact by the addresses (X5), so a boundary across which origins differ cannot be absorbed (X10).

---

## X12 — Multiplicity (LEMMA, lemma)

After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance.

Each copied address `a` is, at the post-state, the image of a copied target position `v + c` (COPY effect clause). It also retains a source appearance: `a` was resolved from some source position `v_s` with `Σ.M(d_s)(v_s) = a` (PC1, resolution). That source appearance survives the operation at a V-position distinct from the copied one:

- When `d_s ≠ d`: the source arrangement is untouched (X9(a)), so `v_s ∈ dom(Σ'.M(d_s))` with `Σ'.M(d_s)(v_s) = a`.
- When `d_s = d`: the source is displaced but survives (X6), relabelled to `v_s + W` (if `v_s ≥ v`) or held fixed (if `v_s < v`) — in either case a V-position `≠ v + c` since the copied positions occupy exactly `[v, v + W)` and the surviving source position is either below `v` or at-or-above `v + W` (X15 tiling).

Hence at least two distinct `(document, V-position)` pairs reference `a` in `Σ'`. The model imposes no upper bound on this multiplicity (ASN-0036, S5, UnrestrictedSharing).

---

## X13 — ContainmentRecording (LEMMA, lemma)

`(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so `Contains_C(Σ') ⊇ {(a_j + i, d)}`, and COPY's effect has written the corresponding pairs into `Σ.R` (Definition: `Σ'.R = Σ.R ∪ {(a_j + i, d)}`).

Write the copied address set `A = {a_j + i : 1 ≤ j ≤ k, 0 ≤ i < n_j}`. Every member of `A` is the image of a copied position `v + c` (`0 ≤ c < W`) in `Σ'.M(d)` (COPY effect clause, PC3), so `A ⊆ ran_{s_C}(Σ'.M(d))` at COPY's post-state.

**Step-local recording fact (SL):** COPY records `(a, d)` for every `a ∈ A` (Definition), and each such `a` is content-subspace-range-resident — `a ∈ ran_{s_C}(Σ'.M(d))` — at COPY's post-state `Σ'`; by provenance permanence (P2) every recorded pair persists.

---

## X14 — Atomicity (LEMMA, lemma)

COPY is a single elementary transition (Definition) in all cases — not a composite of K.μ steps — so SequentialTransitionAxiom (ASN-0047/0093) applies to it directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step, with no observable intermediate state.

---

## X15 — PostStateDensity (INV, predicate)

The post-state content subspace `V_{s_C}(d)` in `Σ'` is exactly `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN).

The three classes of post-state `s_C`-positions occupy disjoint last-component ranges:

- *unmoved* (`u < v`): last component `c ∈ [1, p)`;
- *copied* (`v + c`, `0 ≤ c < W`): last component `p + c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`;
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`.

These three half-open/closed ranges tile `[1, n_S + W]` exactly: `[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap and no gap, using `1 ≤ p ≤ n_S + 1`.

The minimum is `[s_C,1,…,1]`: when `p ≥ 2` it is the unmoved `c = 1` position; when `p = 1` the unmoved range is empty and `c = 1` is the first copied position; either way `c = 1` is occupied, so D-MIN holds.

*(Empty-subspace case `n_S = 0`:* specialisation `p = 1`, `W ≥ 1`: result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at the depth `m` chosen in PC4, with minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.)

---

## X16 — InvariantPreservation (LEMMA, lemma)

COPY maintains every invariant `ValidComposite★` (ASN-0047) binds at its post-state: the per-state `ExtendedReachableStateInvariants` conjunction (including P7), the composite-boundary properties P4★/P4a/P7a, and the transition theorem P3. Provenance couplings (RR routing, J1★/J1'★) are discharged via X13's unconditional write.

Sub-claims:

**(a) Range routing (RR):**
`ran_{s_C}(Σ'.M(d)) = ran_{s_C}(Σ.M(d)) ∪ A`

Each member of the post-state range reaches `R'` by one of two routes:
- *(carried)* `a ∈ ran_{s_C}(Σ.M(d))`: by P4★ at boundary `Σ_0`, `(a, d) ∈ Contains_C(Σ_0) ⊆ R_{Σ_0}`, carried into `R'` by P2.
- *(recorded)* `a ∈ A`: COPY's unconditional write (SL) records `(a, d) ∈ R'` directly.

**(b) J1★/J1'★:** For a recorded pair `(a, d)` with `a ∈ A`: if `a ∈ ran_{s_C}(M_{Σ_0}(d))`, RR's carried route gives `(a, d) ∈ R_{Σ_0}`, so J1'★ is vacuous; otherwise `a` is range-new relative to `Σ_0`, COPY's write meets J1★ and satisfies J1'★'s consequent.

**(c) P7 (ProvenanceGrounding):** Every pair COPY adds is `(a_j + i, d)` with `a_j + i ∈ A`; by C1 (via PC1, X2) every such address lies in `dom(Σ.C) = dom(Σ'.C)` (X1).

**(d) P4★ (`Contains_C(Σ') ⊆ R'`):** Take `(a, d') ∈ Contains_C(Σ')`. If `d' ≠ d`, the frame gives `(a, d') ∈ Contains_C(Σ)`, whence pre-state P4★ places it in `R` and P2 in `R'`. If `d' = d`, then `a ∈ ran_{s_C}(Σ'.M(d))`, and RR routes `(a, d)` into `R'`.

**(e) P7a (`(A a ∈ dom(Σ'.C) :: (E d' :: (a, d') ∈ R'))`):** By X1, `dom(Σ'.C) = dom(Σ.C)`; pre-state P7a furnishes each such `a` a record `(a, d') ∈ R`, carried into `R'` by P2.

**(f) P3 (ExtendedTransitionInvariants):**
`dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`

Discharged directly from COPY's frame: `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R ∪ {(a_j+i, d)} ⊇ Σ.R`.
