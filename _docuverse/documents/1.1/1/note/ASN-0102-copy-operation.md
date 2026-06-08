# ASN-0102: The COPY Operation

*2026-05-28*

We are asked what happens when *existing* content is placed at a position in a document. Placement here is by *reference*, not duplication: COPY allocates no content (X1).

We work over the standing state. A system state `Σ` carries a content store `Σ.C : T ⇀ Val` and, for each document `d`, an arrangement `Σ.M(d) : T ⇀ T` mapping V-positions to I-addresses (ASN-0036). We write `dom(Σ.C)` for the set of allocated I-addresses and `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` for the I-addresses `d` currently references. We use the tumbler vocabulary of the foundations and the mapping-block machinery of ASN-0058 (blocks `(v, a, n)`, their maximal-run decomposition, the merge condition, and content-reference resolution) directly, writing the ordinal shift `shift(t, k)` as `t + k`, with `t + 0 = t` (ASN-0058).

---

## The source designation and its resolution

COPY does not name bytes; it names *positions* that already hold bytes. Its source argument is a content reference sequence `R = ⟨r₁, …, r_q⟩` (ASN-0058), each `rᵢ = (d_i, σ_i)` a well-formed content reference into some source document's arrangement. Resolution flattens these into an I-address sequence. Because the source may include the target itself (`d_s = d`), **resolution is pinned to the pre-state `Σ`** — the state at which the operation's precondition is read — so `resolve_Σ(R)` consults `Σ.M(d)` at the pre-state. We write the result with that state pinned:

`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

### Precondition

We collect the complete precondition under which `COPY(R, d, v)` is defined at `Σ`.

- **(PC1) Source resolvable at `Σ`, into the content subspace.** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference (ASN-0058) with `d_i ∈ dom(Σ.M)` and, writing `σ_i = (u_i, ℓ_i)` for its V-span, **`subspace(u_i) = s_C`**, so `V_{s_C}(d_i) ≠ ∅`, `resolve_Σ(R)` is defined, and by C1 (ResolutionIntegrity, ASN-0058) every resolved address lies in `dom(Σ.C)`. Since `q ≥ 1` and each reference has positive resolved width (C2 gives `w(resolve_Σ(r_i)) = ℓ_{i,m} ≥ 1`), the total width satisfies **`W ≥ 1`** — the empty copy is excluded.
- **(PC2) Target document.** `d ∈ E_doc`, equivalently `d ∈ dom(Σ.M)` (`dom(Σ.M) = E_doc`, ASN-0047).
- **(PC3) Content subspace.** COPY targets the content subspace: `S = s_C`.
- **(PC4) Valid insertion position.** Write `n_S = |V_{s_C}(d)|`.
  - *Non-empty subspace* (`n_S ≥ 1`): by D-SEQ the positions of `V_{s_C}(d)` are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S` at the common depth `m` (S8-depth), and `v = [s_C,1,…,1,p]` is a valid insertion position with `1 ≤ p ≤ n_S + 1` (ASN-0036, ValidInsertionPosition).
  - *Empty subspace* (`n_S = 0`): there is no pre-existing common depth. The operation *chooses* a depth `m ≥ 2` and takes `v = [s_C,1,…,1]` of depth `m` (ASN-0036, ValidFirstInsertionPosition), with `p = 1`; this choice fixes `m` as the content-subspace depth of `d` for all subsequent positions.

---

## Definition of COPY

COPY's effect *relabels* the content-subspace positions at or after `v` by the forward shift `· + W` (the effect clause below), over the standing state `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)`.

**Amendment to `ValidComposite★`.** COPY is added to `ValidComposite★`'s atomic vocabulary (ASN-0047) as a new elementary transition kind, changing two state components — the arrangement `M` and the provenance relation `R`.

The operation `COPY(R, d, v)` carries `Σ → Σ'` as follows.

**Content store — untouched.**
`Σ'.C = Σ.C`.

**Link store — untouched.**
`Σ'.L = Σ.L`.

**Entity set — untouched.**
`Σ'.E = Σ.E`. COPY allocates no node, account, or document.

**Other documents — untouched.**
`(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`.

**Target arrangement.** Write the cumulative offset `c_j = (+ j' : 1 ≤ j' < j : n_{j'})`, so the copied region is the block set

`B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`,

a contiguous lay-down of the resolved I-sequence at consecutive target V-positions. Positions of `d` in the content subspace `s_C` (PC3) at or after `v` shift forward by `W`; positions below `v` and positions in the link subspace are unmoved. Formally `Σ'.M(d)` is the partial function

- `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ s_C`, or with `subspace(u) = s_C ∧ u < v`;
- `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W` (the copied region `B_copy`);
- `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_{s_C}(d)` with `u ≥ v` (the displaced region).

**Provenance.** COPY extends `d`'s content-subspace range by the copied addresses, so its effect records their containment in the provenance relation, against the *destination* document `d` (not the content's original creator):

`Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`.

---

## What is preserved: content immutability forces shared reference

We claim the operation cannot create content, and from that, that what it places must already exist.

**X1 (ContentStoreInvariance).** `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`. This is immediate from the definition `Σ'.C = Σ.C`. Gregory's trace confirms the abstract claim concretely: `docopy` calls `insertpm` (which writes the document's POOM, the arrangement) and `insertspanf` (which writes the containment index), but never `inserttextingranf`, the sole content-creating primitive. The I-address high-water mark queried before allocation is therefore unchanged by COPY (Q16).

In the extended state the governing invariant is the *generalised* referential integrity S3★ (ASN-0047): every V-position is routed to the store its subspace names — `subspace(v) = s_C ⟹ Σ'.M(d)(v) ∈ dom(Σ'.C)` and `subspace(v) = s_L ⟹ Σ'.M(d)(v) ∈ dom(Σ'.L)`. We must establish S3★ at the post-state, so we compute the weakest precondition over *all* post-state mappings of `d`, which the definition partitions into three classes:

- *Unmoved* (`subspace(u) ≠ s_C`, or `subspace(u) = s_C ∧ u < v`): `Σ'.M(d)(u) = Σ.M(d)(u)`. These images are unchanged, so S3★ holds for them in `Σ'` exactly as it did in `Σ`, since `dom(Σ'.C) = dom(Σ.C)` (X1) and `dom(Σ'.L) = dom(Σ.L)` (COPY's frame leaves `Σ.L` untouched). In particular the `s_L`-routing conjunct is discharged with no new obligation: COPY introduces no link-subspace position and alters no existing one.
- *Displaced* (`u ∈ V_{s_C}(d), u ≥ v`, image at `u + W`): `Σ'.M(d)(u + W) = Σ.M(d)(u)`, again an unchanged image in subspace `s_C`, so its target lies in `dom(Σ.C) = dom(Σ'.C)` as before.
- *Copied* (positions `v + c` for `0 ≤ c < W`, all in subspace `s_C` by PC3): `Σ'.M(d)(v + c) = a_j + i`. These are the only genuinely new obligations, and they fall entirely under the `s_C` conjunct of S3★.

The two preserved classes are discharged by X1 and the link-frame. Hence the whole of S3★ reduces to a single membership obligation on the copied region:

`wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`

(using `dom(Σ'.C) = dom(Σ.C)` by X1, with PC3 fixing the inserted subspace to `s_C` so these mappings fall under S3★'s `s_C` conjunct). Therefore the placed addresses must *already* lie in `dom(Σ.C)` at the pre-state, and they do, by C1 (PC1).

**X2 (SharedReference).** Every address introduced into `ran(Σ'.M(d))` by COPY already belonged to `dom(Σ.C)`: `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`. This is forced by X1 together with S3★, and is discharged at the pre-state by C1 (PC1). The placed content is a reference, never a duplicate — not by convention, but because there is no other state-consistent possibility.

---

## What is preserved: identity of instance, and its transitivity

Because COPY places the original I-addresses themselves, every appearance of the content resolves through the *same* key into the *single* content store.

**X3 (IdentityOfInstance).** If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`. The content store is a function (a key has one value), so there is nothing for the two appearances to disagree about. There is no second copy from which to diverge. Identity here is *of instance*, not of value: two independently authored occurrences of the same text hold distinct I-addresses and are not made equal by COPY; only addresses that share an origin share an I-address.

**X4 (TransitiveIdentity).** The address placed by COPY is the content's *original* I-address, irrespective of how many copy hops separate source from origin. *Derivation.* Every address in `dom(Σ.C)` is produced by exactly one allocation event (S4, ASN-0036, via GlobalUniqueness, ASN-0034), and its `origin` is fixed once and for all by its own tumbler structure (S7) — neither is a property of how the address came to be referenced. COPY allocates nothing (X1) and rewrites no I-coordinate (X2). Resolution reads the source arrangement to extract a *stored* I-address (ASN-0058 `resolve` consults `Σ.M(d_s)`); because no COPY hop ever allocates a fresh address or alters an existing one, the tumbler resolution extracts is identically the one produced at that address's single allocation event — whether `d_s` authored the content or itself obtained it by any number of prior COPYs. Hence `a` is the same tumbler at the end of any chain `… → d_s → d`, and Gregory's trace confirms no copy hop ever rewrites the I-coordinate of a crum (Q13). Identity is invariant under arbitrarily deep copy chains.

**X5 (OriginPreservation).** For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run). Because the I-address itself encodes the home document, the system can, after placement, reveal that the content originated elsewhere: the recoverability of attribution is a structural consequence of X2, not a separately maintained annotation.

---

## What shifts: the arrangement, and nothing is overwritten

The displacement clause moves existing content forward to make room; it must lose nothing.

**X6 (NonDestructivePlacement).** Every pre-existing binding of `d` survives COPY, relabelled by the forward shift on the content subspace `s_C`: `(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`. *Derivation.* The shift `· + W` restricted to `{u ∈ V_{s_C}(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4), and its image lies at or above `v + W`. The copied range `[v, v+W)` and the displaced-image range `[v+W, n_S+W]` are disjoint — they abut at `v+W` with no overlap (`[v, v+W) ∩ [v+W, n_S+W] = ∅`) — so no copied mapping collides with a displaced one. The relabelling moves the displaced bindings (those `u ∈ V_{s_C}(d)` with `u ≥ v`) up to `[v+W, …)`, after which the copied region fills `[v, v+W)`. Hence no `(V, I)` binding is destroyed or overwritten: each displaced binding survives with its I-address intact and only its V-label changes — there is no overwrite operation here, only displacement.

**X7 (RunFragmentation).** The copied region is *constructed* as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per run of the resolution *list* `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`). This constructed count `k` tracks the resolution-run count of the source, independent of the width `W`. Two cases separate the within-region merge behaviour:

- *Within a single reference*, no two blocks coalesce. The copied blocks of one reference are *target*-V-adjacent by construction (`c_{j+1} = c_j + n_j`) and carry their source I-coordinates unchanged, so a within-reference target merge candidate would require the consecutive resolved runs to be I-adjacent *in the source*. But `resolve(d_s, σ)` restricts `M(d_s)` to the span's V-range `f = M(d_s)|⟦σ⟧`, and the source content subspace is gap-free (D-SEQ, ASN-0036), so `f` has a contiguous V-domain and its consecutive maximal runs are *source*-V-adjacent. Maximal-merge (ASN-0058, C1a/M12) then forbids any source-V-adjacent pair from also being I-adjacent — that is exactly M7's conjunction it rules out. Since copy alters no I-coordinate, the source-V-adjacent-but-not-I-adjacent runs become target-V-adjacent-but-not-I-adjacent blocks. Hence no within-reference pair is a merge candidate.
- *Across an inter-reference boundary*, the last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and may also be I-adjacent — precisely when they share an origin and abut in I-space (`a' = a + n`, M16/M16a). Such a boundary satisfies the merge condition M7 and coalesces.

Merging the copied blocks among themselves thus yields `≤ k` blocks, with equality exactly when no inter-reference boundary is I-adjacent (in particular whenever consecutive references draw from distinct origins, X10). The abstract state commits only to the *arrangement* — the V→I mapping `Σ'.M(d)` — and not to any particular block count: the constructed `k`-block form and every merged form denote the *same* arrangement, differing only as representations of it (Q8).

**X8 (ContiguousTargetRange).** Although the source may fragment into `k` runs and may draw from several source documents, the copied content occupies one *contiguous* V-range `[v, v + W)` in the target, in source order. *Derivation.* The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order (Gregory Q14/Q17).

**X15 (PostStateDensity).** The post-state content subspace `V_{s_C}(d)` in `Σ'` is exactly `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN). *Derivation.* By PC4 the pre-state positions are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S`, and `v = [s_C,1,…,1,p]`. The shift `· + W` on subspace `s_C` increments only the last component (it is the ordinal shift by `δ(W, m)`, OrdinalShift, ASN-0034: `shift(u, W)ᵢ = uᵢ` for `i < m` and `shift(u, W)_m = u_m + W`, leaving the subspace identifier and the intermediate `1`-components fixed; the subspace identifier `s_C = u₁` is preserved a fortiori by OrdShiftHom (a)). The three classes of post-state `s_C`-positions therefore occupy disjoint last-component ranges:

- *unmoved* (`u < v`): last component `c ∈ [1, p)`;
- *copied* (`v + c`, `0 ≤ c < W`): last component `p + c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`;
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`.

These three half-open/closed ranges tile `[1, n_S + W]` exactly: `[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap (the boundaries `p` and `p + W` are shared endpoints of abutting intervals) and no gap (every integer in `[1, n_S + W]` lies in exactly one range, using `1 ≤ p ≤ n_S + 1`). Hence `V_{s_C}(d)` in `Σ'` is the contiguous run `1 ≤ c ≤ n_S + W` — D-SEQ holds with population `n_S + W`. The minimum is `[s_C,1,…,1]`: when `p ≥ 2` it is the unmoved `c = 1` position; when `p = 1` the unmoved range is empty and `c = 1` is the first copied position; either way `c = 1` is occupied, so D-MIN holds. (The empty-subspace case `n_S = 0` is the specialisation `p = 1`, `W ≥ 1`: the result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at the depth `m` chosen in PC4, with minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.)

Finally, every post-state `s_C`-position — not only the insertion anchor `v` — is well-formed in the sense of S8a. ValidInsertionPosition (PC4) discharges S8a for `v = [s_C,1,…,1,p]` itself, but the interior copied positions `v + 1, …, v + (W−1)` and the displaced positions `u + W` are new entries in `dom(Σ'.M(d))` and must satisfy S8a independently. *Copied positions:* each `v + c = [s_C,1,…,1,p+c]` (`0 ≤ c < W`) has `zeros = 0`, depth `m ≥ 2`, and all components positive (`s_C ≥ 1`, the interior components are `1`, the last component `p + c ≥ 1`). *Displaced positions:* each `u + W = shift(u, W)` for `u ∈ V_{s_C}(d)` with `u ≥ v` inherits S8a from `u` — shift preserves S8a unconditionally (OrdShiftHom (b)) and preserves depth (`#shift(u, W) = #u = m`, OrdinalShift, ASN-0034) — so the displaced image is again a depth-`m`, zero-free, all-positive `s_C`-position. With S8a holding for all three classes, all post-state `s_C`-positions sharing depth `m` (S8-depth), and the copied, displaced, and unmoved `s_C`-classes occupying pairwise-disjoint V-positions (the tiling above), the modified subspace is internally collision-free. The remaining post-state positions — the unmoved link-subspace entries (`subspace(u) = s_L`) — are disjoint from *every* `s_C`-position by subspace-identifier distinctness: a link-subspace V-position and a content-subspace V-position are zero-free, depth-`≥2` tumblers (S8a, ASN-0036 — **not** element-level addresses) whose first components differ (`subspace(·) = ·₁`, and `s_L ≠ s_C`), so they disagree at position 1 and are distinct tumblers by T3 (CanonicalRepresentation, ASN-0034). The tiling thus establishes disjointness *within* `s_C`, and this component-1 distinctness establishes disjointness *across* the subspace boundary, together yielding full pairwise disjointness of all post-state V-positions. Hence the post-state arrangement `Σ'.M(d)` is a well-defined partial function — S2 (functionality) is fully discharged for the post-state.

---

## What invariants the completed operation must maintain

Further obligations bind the post-state.

**X9 (SourceHandling).** The guarantee splits by whether the source is the target, and the two halves are *different properties* — non-alteration in one case, pre-state resolution in the other.

*(a) Non-interference for sources `d_s ≠ d`.* A source document other than the target is left untouched by COPY's frame — instantiating the definition's "other documents" clause at `d' = d_s ≠ d` gives `Σ'.M(d_s) = Σ.M(d_s)`, so its arrangement, its referenced content, and (by X5) the origins of its content are all unchanged.

*(b) Snapshot resolution for `d_s = d`.* When the source *is* the target (self-transclusion), the source document is not unaltered — it is the target, and its content-subspace arrangement is displaced by `· + W`. The guarantee here is not non-alteration but the pre-state pinning fixed by the source-resolution convention: the target-as-source is read at the pre-state `Σ` and is itself displaced by `· + W`. Gregory's trace exhibits the same ordering concretely (`specset2ispanset` precedes `insertpm`, Q15).

**X10 (CrossOriginSeparation).** When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge. *Derivation.* The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce. Each character's home document remains recoverable, as Nelson's royalty and attribution guarantees require (Q9).

**X11 (BoundaryAbsorption).** The copied region meets the surrounding arrangement at *two* boundaries, each an independent merge candidate under M7 (V-adjacency is given at both by construction; I-adjacency is the discriminating test):

- *Leading boundary* (present iff a position immediately precedes `v` in `V_{s_C}(d)`, i.e. `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).
- *Trailing boundary* (present iff content is displaced, i.e. `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` (the content formerly at `v`) — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. After any absorption the merged block is indistinguishable from one never split (M8) — *except* that origin is carried intact by the addresses (X5). Absorption is therefore a representational economy that never erases identity: the homedoc that conditions it (Gregory Q12) is precisely `origin`, and a boundary across which origins differ cannot be absorbed (X10).

**X12 (Multiplicity).** After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance. *Derivation of the lower bound.* Each copied address `a` is, at the post-state, the image of a copied target position `v + c` (COPY effect clause). It also retains a *source* appearance: `a` was resolved from some source position `v_s` with `Σ.M(d_s)(v_s) = a` (PC1, resolution). That source appearance survives the operation at a V-position distinct from the copied one. When `d_s ≠ d`, the source arrangement is untouched (X9(a)), so `v_s ∈ dom(Σ'.M(d_s))` with `Σ'.M(d_s)(v_s) = a` and the appearance lives in a different document. When `d_s = d`, the source is displaced but survives (X6): its image is relabelled to `v_s + W` (if `v_s ≥ v`) or held fixed (if `v_s < v`), in either case a V-position `≠ v + c` since the copied positions occupy exactly `[v, v + W)` and the surviving source position is either below `v` or at-or-above `v + W` (X15 tiling). Hence at least two distinct `(document, V-position)` pairs reference `a` in `Σ'`. The model imposes *no upper bound* on this multiplicity: a single I-address may be referenced from arbitrarily many documents and positions (ASN-0036, S5, UnrestrictedSharing). COPY is the operation that increases this multiplicity without increasing the content store.

**X13 (ContainmentRecording).** At completion, `d` contains each copied address: `(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so `Contains_C(Σ') ⊇ {(a_j + i, d)}`, and COPY's effect has written the corresponding pairs into `Σ.R` (Definition: `Σ'.R = Σ.R ∪ {(a_j + i, d)}`).

Write the copied address set `A = {a_j + i : 1 ≤ j ≤ k, 0 ≤ i < n_j}`. Every member of `A` is the image of a copied position `v + c` (`0 ≤ c < W`) in `Σ'.M(d)` (COPY effect clause, PC3), so `A ⊆ ran_{s_C}(Σ'.M(d))` at COPY's post-state. This yields COPY's **step-local recording fact (SL)**: COPY records `(a, d)` for every `a ∈ A` (Definition), and each such `a` is content-subspace-range-resident — `a ∈ ran_{s_C}(Σ'.M(d))` — at COPY's post-state `Σ'`; by provenance permanence (P2) every recorded pair persists.

**X16 (InvariantPreservation).** COPY maintains every invariant `ValidComposite★` (ASN-0047) binds at its post-state: the per-state `ExtendedReachableStateInvariants` conjunction (including P7), the composite-boundary properties P4★/P4a/P7a, and the transition theorem P3. We discharge them below.

*Composite-boundary reading.* Although COPY is a single elementary transition (X14), the singleton sequence consisting of that one transition is a valid composite by `ValidComposite★`'s definition (a finite sequence of atomic transitions). We therefore read COPY's pre-state as the composite's initial boundary `Σ_0 = Σ` and its post-state `Σ'` as the final composite boundary.

By (SL), COPY's provenance write is *unconditional* — it records `(a, d)` for every `a ∈ A`, whether or not `a` was already content-subspace-range-resident in `d`. The remaining coupling J0 is vacuous by X1 (COPY allocates nothing), so only J1★/J1'★ require routing.

**Range routing (RR).** The post-state content-subspace range partitions as

`ran_{s_C}(Σ'.M(d)) = ran_{s_C}(Σ.M(d)) ∪ A`,

because the unmoved and displaced classes together carry exactly the pre-state images `{Σ.M(d)(u) : u ∈ V_{s_C}(d)} = ran_{s_C}(Σ.M(d))`, while the copied class contributes `A` (`A ⊆ ran_{s_C}(Σ'.M(d))` by SL). Each member of the post-state range reaches `R'` by one of two routes:

- *(carried)* `a ∈ ran_{s_C}(Σ.M(d))`: by P4★ at the boundary `Σ_0`, `(a, d) ∈ Contains_C(Σ_0) ⊆ R_{Σ_0}`, and by P2 the pair persists to `R'`; such `a` is not `R`-new relative to `Σ_0`.
- *(recorded)* `a ∈ A`: COPY's unconditional write (SL) records `(a, d) ∈ R'` directly, with `a` content-subspace-resident at `Σ'`.

The two routes coincide on a copied address that is already resident (self-transclusion); both then apply and agree.

**J1★/J1'★.** Both couplings are range-based, evaluated only between `Σ_0` and `Σ'`. For a recorded pair `(a, d)` with `a ∈ A`: if `a ∈ ran_{s_C}(M_{Σ_0}(d))`, RR's carried route gives `(a, d) ∈ R_{Σ_0}`, so the pair is not `R`-new relative to `Σ_0` and J1'★ is vacuous for it; otherwise `a` is range-new relative to `Σ_0`, COPY's write meets J1★ (range-new ⟹ recorded) and satisfies J1'★'s consequent. COPY's unconditional write thus never violates J1'★.

COPY writes new pairs into `Σ.R`, so it discharges the per-state invariant **P7 (ProvenanceGrounding: `(a, d) ∈ R ⟹ a ∈ dom(C)`)** at the point of the extension. Every pair COPY adds is `(a_j + i, d)` with `a_j + i ∈ A`; by C1 (via PC1, X2) every such address lies in `dom(Σ.C) = dom(Σ'.C)` (X1), so each newly recorded pair is grounded in the content store. The same pair is well-typed against `Σ.R ⊆ T_elem × E_doc` (ASN-0047) on both factors: the `E_doc` side by `d ∈ E_doc` (PC2), and the `T_elem` side because `Element(a_j + i)` holds — `a_j + i ∈ dom(Σ.C)` (just shown) and by S7b (ASN-0036) every content address is element-level (`zeros = 3`).

`ExtendedReachableStateInvariants` (ASN-0047) has two halves: the *per-state* conjunction, required of every reachable state, and the *composite-boundary properties* P4★, P4a, P7a, required additionally at every composite boundary. The remaining *per-state* invariants are discharged below, one conjunct or group per clause:

- *Frame-trivial invariants over `C`, `L`, `E`.* COPY's frame freezes the content, link, and entity components — `Σ'.C = Σ.C` with values fixed (X1), `Σ'.L = Σ.L`, `Σ'.E = Σ.E` — and introduces no `s_L`-subspace V-position. Every invariant quantifying solely over these frozen components or their tumbler structure therefore holds at `Σ'` exactly as at `Σ`: **L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ, P8, NodeLineage, ActivatedEmission** (over `dom(Σ.L)`, `E`, and link-subspace positions); **S7a, S7b, S7, C-fin, C1b, C1c** (over `dom(Σ.C)` and its members' tumbler structure); **S7d** (document tumblers and their allocation events in `E`); **S4** (the allocation-event set and its pairwise distinctness); and **P6** (`origin(a) ∈ E_doc` for `a ∈ dom(Σ.C)`, with origins frozen by X5 and `E_doc` unchanged).
- *S2, S8a.* Established at X15 (well-formed, pairwise-disjoint, single-depth post-state positions).
- *S3★.* The wp computation above.
- *S3★-aux.* Every post-state V-position has subspace `s_C` or `s_L`: copied positions are `s_C` by PC3; unmoved and displaced positions carry their pre-state subspace (`s_C` or `s_L` by pre-state S3★-aux) unchanged.
- *D-CTG★, D-MIN★, D-SEQ★.* Established at X15, restricted to the only modified subspace `s_C`; the others are unmoved.
- *S8-depth.* Established at X15, which fixes the common content-subspace depth `m` for every post-state `s_C`-position — the inherited `m` when `n_S ≥ 1`, the chosen-and-pinned `m` when `n_S = 0`.
- *S8-fin.* By X15's tiling the post-state content subspace is `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}`, so the domain delta is `dom(Σ'.M(d)) ∖ dom(Σ.M(d)) = {[s_C,1,…,1,c] : n_S+1 ≤ c ≤ n_S+W}` — exactly `W = (+ j : 1 ≤ j ≤ k : n_j) < ∞` new positions. (Within `[1, n_S]` the displacement only relabels which I-address each key carries; the keys themselves persist.) Adding `W` positions to the finite pre-state domain (S8-fin at `Σ`) leaves it finite.
- *S8★ (PerSubspaceSpanDecomposition).* Re-established for the modified subspace: `Σ'.M(d)|_{V_{s_C}(d)}` is functional (S2, X15), finite-domain (S8-fin), and contiguous at the single common depth `m` (D-CTG★/D-SEQ★, X15) mapping into `dom(Σ'.C)` (S3★) — precisely ASN-0036's S8 hypotheses — so it decomposes, with `B_copy` plus the displaced and unmoved runs as witnessing runs; the link-subspace projection `Σ'.M(d)|_{V_{s_L}(d)}` is unmoved and carries its pre-state length-1 decomposition forward.

`ExtendedReachableStateInvariants` further demands the **composite-boundary properties P4★, P4a, P7a** at the composite boundary `Σ'`.

- *P4★ (`Contains_C(Σ') ⊆ R'`).* Take `(a, d') ∈ Contains_C(Σ')`. If `d' ≠ d`, the frame `Σ'.M(d') = Σ.M(d')` gives `(a, d') ∈ Contains_C(Σ)`, whence pre-state P4★ places it in `R` and P2 (`R ⊆ R'`) in `R'`. If `d' = d`, then `a ∈ ran_{s_C}(Σ'.M(d))`, and RR routes `(a, d)` into `R'` by its carried or recorded route. Either way `(a, d') ∈ R'`.
- *P7a (`(A a ∈ dom(Σ'.C) :: (E d' :: (a, d') ∈ R'))`).* By X1, `dom(Σ'.C) = dom(Σ.C)`; pre-state P7a furnishes each such `a` a record `(a, d') ∈ R`, carried into `R'` by P2. COPY's new records only enlarge the coverage, so every content address retains at least one provenance entry.
- *P4a (TraceWitnessing).* We discharge P4a parametrically, as one operation-preservation step in the reachability induction. Fix any invariant-satisfying pre-state `Σ` and any COPY carrying it to `Σ'`, and take P4a at `Σ` as the inductive hypothesis (it holds because `Σ` is a composite boundary reached by a shorter trace). The COPY-terminated trace — a witnessing trace reaching `Σ`, extended by this COPY composite, with trace states `{Σ_init, …, Σ, Σ'}` — witnesses every pair in `R'`: a pair already in `R` is witnessed at some state of the reaching prefix by the inductive hypothesis, and a pair in `R' ∖ R` is one COPY recorded (X13), so `d' = d` and `a ∈ A`, and RR's recorded route makes `a` content-subspace-resident at `Σ'` (some `v` with `Σ'.M(d)(v) = a`), so `Σ'` itself witnesses it.

Finally, COPY is a transition, so it must also discharge the separate transition theorem **ExtendedTransitionInvariants** (ASN-0047), whose sole conjunct is **P3** (`dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`). It is discharged directly from COPY's frame: `Σ'.C = Σ.C` gives both `dom(C) ⊆ dom(C')` and content value-fixity; `Σ'.L = Σ.L` gives both `dom(L) ⊆ dom(L')` and link value-fixity; `Σ'.E = Σ.E` gives `E ⊆ E'`; and `Σ'.R = Σ.R ∪ {(a_j+i, d)} ⊇ Σ.R` gives `R ⊆ R'`. Every conjunct of P3 holds.

**X14 (Atomicity).** COPY is a *single* elementary transition (Definition), not a composite of K.μ steps, so SequentialTransitionAxiom (ASN-0047/0093) applies to it directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step, with no observable intermediate state. In the displacing case this atomicity is forced; the non-displacing cases (`p = n_S+1` append, `n_S = 0` empty subspace) displace nothing and are also expressible as a valid composite.

*The displacing case (`p ≤ n_S ∧ W ≥ 1`): atomicity is forced.* When the insertion position precedes some occupied position, COPY's effect both displaces the content-subspace tail forward by `W` (X6) and fills the freed range `[v, v+W)` with the copied region (X15 tiling), and these two acts cannot be sequenced. Any decomposition into two or more elementary transitions must separate the displacement (any step that relabels `{u ∈ V_{s_C}(d) : u ≥ v}` upward by `· + W`) from the fill (a K.μ⁺ extension that binds the copied positions). Consider the state after the displacement but before the fill. The displaced positions now occupy last-component range `[p+W, n_S+W]` while the unmoved positions occupy `[1, p)`, so the content subspace `V_{s_C}(d)` is `{[s_C,1,…,1,c] : 1 ≤ c < p ∨ p+W ≤ c ≤ n_S+W}` — a set with a hole at `[p, p+W)`, since `p ≤ n_S` and `W ≥ 1` make that interval non-empty. That hole violates D-CTG★ (per-subspace contiguity) and D-SEQ★ (sequential positions from the minimum), both of which `ExtendedReachableStateInvariants` (ASN-0047) demands of *every* state reachable by elementary transitions drawn from a valid composite — not merely at composite boundaries. The reverse order (fill before displace) fares no better: in the displacing case the freed range `[v, v+W)` overlaps the still-occupied displaced-source positions `[v, n_S]` (non-empty since `p ≤ n_S`), so binding a copied position at any key `u ∈ [v, v+W) ∩ [v, n_S]` before that key's displaced binding has vacated *overwrites and loses* the displaced binding at that single key — `M(d)(u)` cannot hold both the copied image and the surviving displaced image. That is not a shared-component collision but a destruction of a pre-existing binding, which X6 (NonDestructivePlacement) forbids and which no intermediate state can repair, since the lost binding is gone. Either ordering thus exposes an intermediate state that fails a per-state invariant (D-CTG★/D-SEQ★ forward, X6's non-destruction reverse), so `ValidComposite★`'s clause (1) — each step's elementary precondition must hold at the *intermediate* state — cannot be met by any decomposition. Hence in the displacing case COPY is irreducibly atomic: the displacement and the fill must commit together, in the one indivisible step that carries `Σ` directly to the gap-free post-state `Σ'` (X15). The non-displacing cases displace nothing, so the freed range is empty and COPY coincides with a contiguous tail extension that `ValidComposite★` clause (1) admits as a decomposition; only the displacing case compels the elementary-transition model.

---

## A worked example

We instantiate the operation to see the claims bite. Fix `s_C = 1`. Let the target `d` have a content subspace of common depth `m = 2` and population `n_S = 5`, so `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4], [1,5]}` (D-SEQ), with pre-state bindings `Σ.M(d)([1,c]) = x_c` for some I-addresses `x_1, …, x_5 ∈ dom(Σ.C)`. We copy at `v = [1,3]`, so `p = 3`.

The source is a two-reference sequence resolving to a *cross-origin*, fragmented I-sequence of total width `W = 4`:

`resolve_Σ(R) = ⟨(a_1, 2), (a_2, 2)⟩`,  with `origin(a_1) = d_1`, `origin(a_2) = d_2`, `d_1 ≠ d_2`, and `a_1, a_1+1, a_2, a_2+1 ∈ dom(Σ.C)`.

So `k = 2`, `c_1 = 0`, `c_2 = 2`, `W = 4`. The copied block set is `B_copy = {([1,3], a_1, 2), ([1,5], a_2, 2)}`.

The post-state arrangement `Σ'.M(d)`:

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `x_1` | unmoved |
| 2 | `[1,2]` | `x_2` | unmoved |
| 3 | `[1,3]` | `a_1` | copied (blk 1) |
| 4 | `[1,4]` | `a_1+1` | copied (blk 1) |
| 5 | `[1,5]` | `a_2` | copied (blk 2) |
| 6 | `[1,6]` | `a_2+1` | copied (blk 2) |
| 7 | `[1,7]` | `x_3` | displaced |
| 8 | `[1,8]` | `x_4` | displaced |
| 9 | `[1,9]` | `x_5` | displaced |

Now check the claims:

- **X1** — `dom(Σ'.C) = dom(Σ.C)`: no new I-address appears; `a_1, a_1+1, a_2, a_2+1` were all already allocated.
- **X2** — every newly referenced address (`a_1, a_1+1, a_2, a_2+1`) lies in `dom(Σ.C)`. Discharged by C1; required by `wp(COPY, S3★)`.
- **X6** — the displaced bindings `x_3, x_4, x_5` survive intact at `[1,7], [1,8], [1,9]`; nothing is overwritten. Here `W = 4 > n_S − p + 1 = 3`, so the freed positions are only `[1,3]..[1,5]` (the pre-state slots of `x_3, x_4, x_5`); the copied region fills `[1,3]..[1,6]`, of which `[1,6]` was unoccupied pre-state. The no-overwrite conclusion holds by the disjointness of copied (`[1,3]..[1,6]`) and displaced-image (`[1,7]..[1,9]`) ranges (X15), not by `[1,3]..[1,6]` having been fully populated.
- **X7** — the copied region is `k = 2` blocks, *independent of* `W = 4`. The two blocks are *not* I-adjacent (`a_2 ≠ a_1 + 2`, distinct origins), so the in-isolation canonical count is also 2 — equality holds because the single inter-reference boundary is not I-adjacent.
- **X8** — the copy occupies the contiguous V-range `[1,3]..[1,6] = [v, v+W)`, in source order.
- **X10** — block `([1,3], a_1, 2)` (origin `d_1`) and block `([1,5], a_2, 2)` (origin `d_2`) cannot merge: I-adjacency would need `a_2 = a_1 + 2`, but M16 forbids it across distinct origins.
- **X15 (density)** — post-state `V_{s_C}(d) = {[1,c] : 1 ≤ c ≤ 9}`, contiguous, `n_S + W = 5 + 4 = 9`, minimum `[1,1]`. No gap.
- **X11** — leading boundary (`p = 3 ≥ 2`): the unmoved predecessor at `[1,2]` holds `x_2`; it absorbs block 1 iff `x_2`'s I-reach is `a_1`, i.e. `x_2 = a_1 - 1` with `origin(x_2) = d_1`. Trailing boundary (`p = 3 ≤ n_S = 5`): the first displaced block holds `x_3` at `[1,7]`; it absorbs block 2 iff `x_3 = a_2 + 2`. Both are genuine, independent candidates — generically neither fires.

### A self-transclusion scenario (copied address already referenced, source overlaps the displaced region)

This scenario is a *self-transclusion* — the target is its own source — with the source span positioned *at or after* `v`, so the copied span overlaps the region the displacement will move. It exercises the case where the copied address is *already referenced* by `d` (`A ∩ ran(Σ.M(d)) ≠ ∅`), so COPY's provenance write records nothing new.

Fix `s_C = 1`. Let `d` have content subspace of common depth `m = 2` and population `n_S = 3`, so `V_{s_C}(d) = {[1,1], [1,2], [1,3]}` with pre-state bindings `Σ.M(d)([1,1]) = x_1`, `Σ.M(d)([1,2]) = x_2`, `Σ.M(d)([1,3]) = x_3`, where `x_1, x_2, x_3 ∈ dom(Σ.C)` are distinct. The source is the single self-reference `R = ⟨(d, σ)⟩` whose V-span covers `d`'s own *third* content position `[1,3]` — and crucially `[1,3] ≥ v` for the `v = [1,2]` we copy at, so the source lies squarely in the region the copy will displace. Resolved against the *pre-state* `Σ`: `resolve_Σ(R) = ⟨(x_3, 1)⟩` — one run of width `W = 1`, since `Σ.M(d)([1,3]) = x_3`. We copy at `v = [1,2]`, so `p = 2`, `k = 1`, `B_copy = {([1,2], x_3, 1)}`. The displaced region is `{u ∈ V_{s_C}(d) : u ≥ [1,2]} = {[1,2], [1,3]}`, which shifts by `W = 1` to `[1,3], [1,4]`.

The post-state arrangement `Σ'.M(d)`:

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `x_1` | unmoved |
| 2 | `[1,2]` | `x_3` | copied (blk 1) |
| 3 | `[1,3]` | `x_2` | displaced (from `[1,2]`) |
| 4 | `[1,4]` | `x_3` | displaced (from `[1,3]`) |

The source span names V-position `[1,3]`, which satisfies `[1,3] ≥ v`. Resolution against the pre-state `Σ` reads `Σ.M(d)([1,3]) = x_3` and lays it down at the copied slot `[1,2] ∈ [v, v+W)`, while the original `x_3` shifts to `[1,4] ∈ [v+W, …)`. Had resolution instead read the *post-state* `Σ'`, position `[1,3]` would hold `x_2` — the content the displacement had just shoved up from `[1,2]` — so the copy would transclude `x_2` rather than `x_3`: a different, circular result. Pre-state resolution (X9(b)) is what makes this self-transclusion well-defined.

Now the recording (SL). The copied address set is `A = {x_3}`, and `x_3` is already referenced by `d` at `[1,3]` in the pre-state content subspace (`x_3 ∈ ran_{s_C}(Σ.M(d))`). By (SL), COPY records `(x_3, d)` and `x_3` is content-subspace-resident at `Σ'`. Taking this COPY as the whole embedding composite (pre-state `Σ = Σ_0`), `x_3` is resident at `Σ_0`, so it follows RR's carried route: by P4★ at `Σ_0`, `(x_3, d) ∈ R_{Σ_0}`, and COPY's write `Σ'.R = Σ.R ∪ {(x_3, d)}` adds nothing — `R' ∖ R = ∅`, so J1'★ is vacuous for `x_3`.

The reference multiplicity rises (X12): `x_3` is now referenced from `[1,2]` (copied) *and* `[1,4]` (its displaced original) — yet `dom(Σ'.C) = dom(Σ.C)` (X1) and `R' = R`, so neither store grows. And X6 is exercised non-trivially: the displaced bindings `x_2, x_3` survive intact at `[1,3], [1,4]`, the copied region `[1,2]` and the displaced-image range `[1,3], [1,4]` being disjoint (X15), so nothing is overwritten despite the source and the displaced content overlapping.

### The empty-subspace first insertion (`n_S = 0`, `p = 1`)

This is the first insertion into an *empty* content subspace, where there is no pre-state common depth to inherit: the operation must *choose* a depth `m` and pin it (PC4, ValidFirstInsertionPosition), every copied address is genuinely range-new, and there are neither unmoved nor displaced positions.

Fix `s_C = 1`. Let `d` be freshly registered with `V_{s_C}(d) = ∅`, so `n_S = 0`. The source is a single same-origin reference of width `W = 2`: `R = ⟨(d_1, σ)⟩` with `resolve_Σ(R) = ⟨(a_1, 2)⟩`, `origin(a_1) = d_1`, and `a_1, a_1+1 ∈ dom(Σ.C)`. By PC4 the operation chooses depth `m = 2` and takes `v = [1,1]` of depth 2 (ValidFirstInsertionPosition), so `p = 1`, `k = 1`, `c_1 = 0`, `B_copy = {([1,1], a_1, 2)}`. The choice fixes `m = 2` as `d`'s content-subspace depth for all future positions.

The post-state arrangement `Σ'.M(d)`:

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `a_1` | copied (blk 1) |
| 2 | `[1,2]` | `a_1+1` | copied (blk 1) |

Now check the boundary-specific claims:

- **X1** — `dom(Σ'.C) = dom(Σ.C)`: `a_1, a_1+1` were already allocated; the empty subspace gains references, not content.
- **X15 (density, min)** — both the unmoved range (`p = 1`, empty) and the displaced range (no `u ≥ v`, since `V_{s_C}(d) = ∅`) are empty, so the tiling degenerates to the single copied range `[p, p+W) = [1, 3)`. Post-state `V_{s_C}(d) = {[1,c] : 1 ≤ c ≤ 2}` at the chosen depth `m = 2` — contiguous with `n_S + W = 0 + 2 = 2`, minimum `[1,1]` (the first copied position, not an unmoved one), discharged here by ValidFirstInsertionPosition rather than by an inherited D-SEQ. S8a holds for both copied positions: each `[1, 1+c]` (`0 ≤ c < 2`) has `zeros = 0`, depth `2 ≥ 2`, all components positive.
- **X13 (recording)** — `A = {a_1, a_1+1}`; the pre-state content-subspace range is empty, so both copied addresses are genuinely range-new. By (SL), COPY records `(a_1, d)` and `(a_1+1, d)` into `Σ'.R`, each resident at `Σ'` — the record-with-residency the composite's J1★/J1'★ consume for these new range entries. J0 is vacuous by X1.

### The append boundary (`p = n_S + 1`, trailing boundary absent)

This is the *append*: inserting at `p = n_S + 1`, past the last occupied position. No content is displaced (there is no `u ∈ V_{s_C}(d)` with `u ≥ v`), so the trailing boundary of X11 is *absent* and only the leading boundary is a merge candidate.

Fix `s_C = 1`, `m = 2`, `n_S = 3`, so `V_{s_C}(d) = {[1,1], [1,2], [1,3]}` with bindings `x_1, x_2, x_3 ∈ dom(Σ.C)`. We copy at `v = [1,4]`, so `p = 4 = n_S + 1`. The source is a single same-origin reference of width `W = 2`: `resolve_Σ(R) = ⟨(a_1, 2)⟩`, `B_copy = {([1,4], a_1, 2)}`.

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `x_1` | unmoved |
| 2 | `[1,2]` | `x_2` | unmoved |
| 3 | `[1,3]` | `x_3` | unmoved |
| 4 | `[1,4]` | `a_1` | copied (blk 1) |
| 5 | `[1,5]` | `a_1+1` | copied (blk 1) |

- **X15 (density)** — the displaced range is empty (`p = 4 > n_S = 3`), so the tiling is unmoved `[1, p) = [1, 4)` followed by copied `[p, p+W) = [4, 6)`, with no displaced tail. Post-state `V_{s_C}(d) = {[1,c] : 1 ≤ c ≤ 5}`, contiguous, `n_S + W = 5`, minimum `[1,1]` (unmoved).
- **X11 (trailing boundary absent)** — the leading boundary is present (`p = 4 ≥ 2`): the unmoved predecessor at `[1,3]` holds `x_3`, absorbing block 1 iff `x_3`'s I-reach is `a_1` (i.e. `x_3 = a_1 - 1` with `origin(x_3) = d_1`). The trailing boundary is *absent*: the condition `p ≤ n_S` fails (`4 ≤ 3` is false), there is no first displaced block, so no trailing merge candidate exists.

### A coalescing copy (`canonical < k`, leading boundary fires)

This is the discriminating case for the *merging* side of X7 and X11 — a same-origin source whose two references abut in I-space (so the inter-reference boundary *coalesces*, `canonical = k − 1`), placed against a predecessor it I-abuts (so the *leading* boundary *absorbs*).

Fix `s_C = 1`, `m = 2`. Let `d` have content-subspace population `n_S = 2`, with pre-state bindings `Σ.M(d)([1,1]) = a_1 − 2` and `Σ.M(d)([1,2]) = a_1 − 1`, both of origin `d_1` and I-abutting (`(a_1−2)+1 = a_1−1`), so they form a single pre-state run of width 2 whose I-reach is `a_1`. We append at `v = [1,3]`, so `p = 3 = n_S + 1` — no content is displaced, so the trailing boundary is absent and only the leading boundary is in play.

The source is a two-reference sequence, *both references drawn from `d_1`*, resolving to two width-2 runs that abut in I-space:

`resolve_Σ(R) = ⟨(a_1, 2), (a_1 + 2, 2)⟩`,  with `origin(a_1) = origin(a_1+2) = d_1` and `a_1, …, a_1+3 ∈ dom(Σ.C)`.

So `k = 2`, `c_1 = 0`, `c_2 = 2`, `W = 4`, and `B_copy = {([1,3], a_1, 2), ([1,5], a_1+2, 2)}`.

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `a_1−2` | unmoved |
| 2 | `[1,2]` | `a_1−1` | unmoved |
| 3 | `[1,3]` | `a_1` | copied (blk 1) |
| 4 | `[1,4]` | `a_1+1` | copied (blk 1) |
| 5 | `[1,5]` | `a_1+2` | copied (blk 2) |
| 6 | `[1,6]` | `a_1+3` | copied (blk 2) |

Now the merge predicates *fire*:

- **X7 (inter-reference coalescence, `canonical < k`)** — the two copied blocks are V-adjacent (`[1,5] = [1,3] + 2`, since `c_2 = n_1 = 2`) and I-adjacent (`a_1+2 = a_1 + n_1` with `n_1 = 2`, M7), and they share origin `d_1` (so M16 does not block them). The merge condition holds, and the copied region's in-isolation canonical count is `k − 1 = 1`: the single block `([1,3], a_1, 4)`. This is the `canonical < k` half of X7, witnessed against a concrete instance rather than only argued in prose.
- **X11 (leading boundary absorbs)** — the leading boundary is present (`p = 3 ≥ 2`). The unmoved predecessor run `([1,1], a_1−2, 2)` ends with I-reach `(a_1−2) + 2 = a_1`, which equals the first copied I-start `a_1`; V-adjacency holds (`[1,3] = [1,1] + 2`) and origins agree (`d_1`). The predecessor *absorbs* the copied region — the firing case of X11, the half the append example left failing.
- **Whole-arrangement canonical form** — composing both merges, the entire post-state content subspace collapses to the single canonical block `([1,1], a_1−2, 6)`: six V-positions, one maximal I-run of width `n_S + W = 6`, all origin `d_1`. The constructed `k = 2`-block copied region (plus the unmoved run) and this one-block canonical form denote the *same* arrangement `Σ'.M(d)`, differing only as representations (X7) — no I-coordinate or V-order is altered by the choice between them.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| COPY | `COPY(R, d, v)` (single elementary transition; precond. PC1–PC4, target subspace `S = s_C`): `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; content subspace displaced forward by `W` and gap `[v, v+W)` bound to `resolve_Σ(R)` in order; `Σ'.R = Σ.R ∪ {(a_j+i, d)}` | introduced |
| X1 | ContentStoreInvariance — `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))` | introduced |
| X2 | SharedReference — `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`; placed addresses pre-exist (forced by X1 ∧ S3★) | introduced |
| X3 | IdentityOfInstance — every appearance of a copied address resolves to the single value `Σ.C(a)` | introduced |
| X4 | TransitiveIdentity — the placed address is the content's original I-address through arbitrary copy chains | introduced |
| X5 | OriginPreservation — `origin(a)` unchanged and recoverable for every copied `a`; attribution is structural | introduced |
| X6 | NonDestructivePlacement — every pre-existing binding of `d` survives, relabelled by the forward shift; nothing overwritten | introduced |
| X7 | RunFragmentation — copied region constructed as `k` blocks (one per resolution run, independent of `W`); within-region merge yields `≤ k`, with equality when no inter-reference boundary is I-adjacent | introduced |
| X8 | ContiguousTargetRange — copied content occupies one contiguous V-range `[v, v+W)` in source order | introduced |
| X9 | SourceHandling — (a) non-interference: no source document *other than the target* (`d' ≠ d`) is altered; (b) snapshot resolution: when `d_s = d` the target-as-source is read at the pre-state (it *is* displaced, not unaltered) | introduced |
| X10 | CrossOriginSeparation — blocks of distinct origin cannot merge (M7 ∧ M16); distinct portions stay distinguishable | introduced |
| X11 | BoundaryAbsorption — leading boundary (`p ≥ 2`) and trailing boundary (`p ≤ n_S`) are independent merge candidates, each absorbing iff I-adjacent; origin still carried | introduced |
| X12 | Multiplicity — placed addresses gain reference multiplicity ≥ 2, with no model-imposed bound (S5) | introduced |
| X13 | ContainmentRecording — `d` recorded as containing each copied address, provenance written to `Σ.R`; step-local recording fact (SL) | introduced |
| X14 | Atomicity — COPY is a single elementary transition (SequentialTransitionAxiom). In the displacing case (`p ≤ n_S ∧ W ≥ 1`) atomicity is *forced*: any displace-then-fill decomposition exposes an intermediate `s_C` V-gap violating D-CTG★/D-SEQ★ (forward) or destroys a displaced binding violating X6 (reverse). In the append (`p = n_S+1`) and empty-subspace (`n_S = 0`) cases COPY displaces nothing and is also expressible as a valid composite | introduced |
| X15 | PostStateDensity — post-state `V_{s_C}(d) = {[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}`, contiguous (D-SEQ), min `[s_C,1,…,1]` (D-MIN) | introduced |
| X16 | InvariantPreservation — COPY maintains the per-state `ExtendedReachableStateInvariants` (incl. P7), the composite-boundary properties (P4★, P4a, P7a), and the transition invariant P3; provenance couplings (RR routing, J1★/J1'★) discharged via X13's unconditional write | introduced |

## Open Questions

When copied content is later displaced again by a subsequent operation, what invariant ties the original origin to the address's continued discoverability?

What must the system guarantee about containment records when a document that obtained content by reference is itself the source of a further reference?

Under what conditions, if any, may two references to the same content be required to resolve to differing views of it across time?

What must remain true of a copied address's identity when the document that allocated it is no longer reachable?
