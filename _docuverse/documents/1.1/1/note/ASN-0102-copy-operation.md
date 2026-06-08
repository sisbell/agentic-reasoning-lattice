# ASN-0102: The COPY Operation

*2026-05-28*

We are asked what happens when *existing* content is placed at a position in a document. Placement here is by *reference*, not duplication: COPY allocates no content (X1), and this single fact dictates what the operation may and may not do.

We work over the standing state. A system state `Σ` carries a content store `Σ.C : T ⇀ Val` and, for each document `d`, an arrangement `Σ.M(d) : T ⇀ T` mapping V-positions to I-addresses (ASN-0036). We write `dom(Σ.C)` for the set of allocated I-addresses and `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` for the I-addresses `d` currently references. The tumbler vocabulary — the order `<`, displacement `⊕`/`⊖`, the shift `shift(t, k)` (written `t + k` in its ordinal form, with `t + 0 = t`, after ASN-0058), the subspace projector `subspace(v)`, the home-document projector `origin(a) = N(a).0.U(a).0.D(a)` (ASN-0036, S7) — is taken from the foundations without restatement. Mapping blocks `(v, a, n)` with denotation `⟦(v,a,n)⟧ = {(v+k, a+k) : 0 ≤ k < n}`, their decomposition into maximal runs, the merge condition, and the resolution of content references are taken from ASN-0058.

---

## The source designation and its resolution

COPY does not name bytes; it names *positions* that already hold bytes. Its source argument is a content reference sequence `R = ⟨r₁, …, r_q⟩` (ASN-0058), each `rᵢ = (d_i, σ_i)` a well-formed content reference into some source document's arrangement. Resolution flattens these into an I-address sequence. Because the source may include the target itself (`d_s = d`), the evaluation point matters: we resolve against the *pre-state* `Σ`, the state at which the operation's precondition is read, and write the result with that state pinned:

`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

Resolution supplies two facts from ASN-0058. First, *every resolved address already exists*: by C1, `(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C)))`. Second, *the run count `k` is the total number of runs of the concatenated resolution* — the sum over references `k = (+ i : 1 ≤ i ≤ q : k_i)`, where each `k_i` is the maximal-contiguous-I-run count of reference `r_i` taken in isolation (C1a, M12 applied per reference).

### Precondition

We collect the complete precondition under which `COPY(R, d, v)` is defined at `Σ`.

- **(PC1) Source resolvable at `Σ`, into the content subspace.** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference (ASN-0058) with `d_i ∈ dom(Σ.M)` and, writing `σ_i = (u_i, ℓ_i)` for its V-span, **`subspace(u_i) = s_C`**, so `V_{s_C}(d_i) ≠ ∅`, `resolve_Σ(R)` is defined, and by C1 (ResolutionIntegrity, ASN-0058) every resolved address lies in `dom(Σ.C)`. Since `q ≥ 1` and each reference has positive resolved width (C2 gives `w(resolve_Σ(r_i)) = ℓ_{i,m} ≥ 1`), the total width satisfies **`W ≥ 1`** — the empty copy is excluded.
- **(PC2) Target document.** `d ∈ E_doc`, equivalently `d ∈ dom(Σ.M)` (`dom(Σ.M) = E_doc`, ASN-0047).
- **(PC3) Content subspace.** The target subspace is the content (byte) subspace: `S = s_C`. COPY places transcluded *content*: by PC1 every source span is content-subspace-resident, so C1 yields resolved addresses in `dom(Σ.C)`, carrying `subspace_I(·) = s_C`; the link subspace `s_L` is populated only in creation order by MAKELINK and is not a legal target for COPY (Q1). This pins `subspace(v) = s_C` for the inserted positions and is the conjunct S3★ will require below.
- **(PC4) Valid insertion position.** Write `n_S = |V_{s_C}(d)|`.
  - *Non-empty subspace* (`n_S ≥ 1`): by D-SEQ the positions of `V_{s_C}(d)` are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S` at the common depth `m` (S8-depth), and `v = [s_C,1,…,1,p]` is a valid insertion position with `1 ≤ p ≤ n_S + 1` (ASN-0036, ValidInsertionPosition).
  - *Empty subspace* (`n_S = 0`): there is no pre-existing common depth. The operation *chooses* a depth `m ≥ 2` and takes `v = [s_C,1,…,1]` of depth `m` (ASN-0036, ValidFirstInsertionPosition), with `p = 1`; this choice fixes `m` as the content-subspace depth of `d` for all subsequent positions.

---

## Definition of COPY

COPY is added to the system's transition vocabulary `𝒦` (ASN-0047) as an elementary transition in its own right, with the complete frame stated below. Its effect *relabels* the content-subspace positions at or after `v` by the forward shift `· + W` (the effect clause below). Because the standing state carries five components, `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)`, the contract must pin all five.

**Amendment to `ValidComposite★`.** COPY is added to `ValidComposite★`'s atomic vocabulary (ASN-0047) as a new transition kind, admissible only as a length-1 (standalone) composite. A standalone COPY `Σ → Σ'` is then a valid composite — its clause-1 transition precondition is PC1–PC4 (read at `Σ`) and its clause-2 couplings J0/J1★/J1'★ are evaluated between `Σ` and `Σ'` — so its endpoints `Σ` and `Σ'` are **composite boundaries**, at which the composite-boundary properties of ASN-0047, in particular P4★ (`Contains_C(Σ) ⊆ R`), hold.

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

**Provenance.** COPY extends `d`'s content-subspace range by the copied addresses, so its effect records their containment in the provenance relation:

`Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`.

The displacement is the same forward shift that INSERT performs — Nelson treats COPY's positional effect as identical to INSERT's [LM 4/66–67]. The half of the definition that distinguishes COPY from every content-creating operation is `Σ'.C = Σ.C`. We now derive its consequences.

---

## What is preserved: content immutability forces shared reference

We claim the operation cannot create content, and from that, that what it places must already exist.

**X1 (ContentStoreInvariance).** `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`. This is immediate from the definition `Σ'.C = Σ.C`. Nelson:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

Gregory's trace confirms the abstract claim concretely: `docopy` calls `insertpm` (which writes the document's POOM, the arrangement) and `insertspanf` (which writes the containment index), but never `inserttextingranf`, the sole content-creating primitive. The I-address high-water mark queried before allocation is therefore unchanged by COPY (Q16). We record this as a corollary.

**X2 (NoFreshAllocation).** COPY consumes no previously-unallocated address: the set of addresses available to a subsequent content-creating allocation in `d` is identical before and after COPY. *Derivation.* A content-creating allocation extends `dom(Σ.C)`; by X1 that set is unchanged, so the frontier from which the next address is drawn is unchanged. The cost of copying fragmented content is borne entirely in the arrangement (in the number of blocks, X8), never in the content store.

Now the decisive step. In the extended state the governing invariant is the *generalised* referential integrity S3★ (ASN-0047): every V-position is routed to the store its subspace names — `subspace(v) = s_C ⟹ Σ'.M(d)(v) ∈ dom(Σ'.C)` and `subspace(v) = s_L ⟹ Σ'.M(d)(v) ∈ dom(Σ'.L)`. We must establish S3★ at the post-state, so we compute the weakest precondition over *all* post-state mappings of `d`, which the definition partitions into three classes:

- *Unmoved* (`subspace(u) ≠ s_C`, or `subspace(u) = s_C ∧ u < v`): `Σ'.M(d)(u) = Σ.M(d)(u)`. These images are unchanged, so S3★ holds for them in `Σ'` exactly as it did in `Σ`, since `dom(Σ'.C) = dom(Σ.C)` (X1) and `dom(Σ'.L) = dom(Σ.L)` (COPY's frame leaves `Σ.L` untouched). In particular the `s_L`-routing conjunct is discharged with no new obligation: COPY introduces no link-subspace position and alters no existing one.
- *Displaced* (`u ∈ V_{s_C}(d), u ≥ v`, image at `u + W`): `Σ'.M(d)(u + W) = Σ.M(d)(u)`, again an unchanged image in subspace `s_C`, so its target lies in `dom(Σ.C) = dom(Σ'.C)` as before.
- *Copied* (positions `v + c` for `0 ≤ c < W`, all in subspace `s_C` by PC3): `Σ'.M(d)(v + c) = a_j + i`. These are the only genuinely new obligations, and they fall entirely under the `s_C` conjunct of S3★.

The two preserved classes are discharged by X1 and the link-frame. Hence the whole of S3★ reduces to a single membership obligation on the copied region:

`wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`

(using `dom(Σ'.C) = dom(Σ.C)` by X1; the relation is equality, not containment — these are exactly the new mappings S3★ constrains, and they are routed to `dom(Σ.C)` because PC3 fixes their subspace to `s_C`). Therefore the placed addresses must *already* lie in `dom(Σ.C)` at the pre-state, and they do, by C1 (resolution yields only existing addresses). The operation has no freedom here: having renounced content creation, the only addresses it can legally place are ones that already exist — and PC3 guarantees it places them where S3★ demands.

**X3 (SharedReference).** Every address introduced into `ran(Σ'.M(d))` by COPY already belonged to `dom(Σ.C)`: `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`. This is forced by X1 together with S3★, and is discharged at the pre-state by ASN-0058 C1 (resolution yields only existing addresses). The placed content is a reference, never a duplicate — not by convention, but because there is no other state-consistent possibility.

---

## What is preserved: identity of instance, and its transitivity

Because COPY places the original I-addresses themselves, every appearance of the content resolves through the *same* key into the *single* content store.

**X4 (IdentityOfInstance).** If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`. The content store is a function (a key has one value), so there is nothing for the two appearances to disagree about. There is no second copy from which to diverge: Nelson's primary text specifies that non-native bytes are never duplicated but remain at their home locations, fetched by request —

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Identity here is *of instance*, not of value: two independently authored occurrences of the same text hold distinct I-addresses and are not made equal by COPY; only addresses that share an origin share an I-address.

**X5 (TransitiveIdentity).** The address placed by COPY is the content's *original* I-address, irrespective of how many copy hops separate source from origin. *Derivation.* The claim needs no induction on chain length; one structural fact closes it. Every address in `dom(Σ.C)` is produced by exactly one allocation event (S4, ASN-0036, via GlobalUniqueness, ASN-0034), and its `origin` is fixed once and for all by its own tumbler structure (S7) — neither is a property of how the address came to be referenced. COPY allocates nothing (X1) and rewrites no I-coordinate (X3: the addresses it places already lie in `dom(Σ.C)`). Resolution reads the source arrangement to extract a *stored* I-address (ASN-0058 `resolve` consults `Σ.M(d_s)`); because no COPY hop ever allocates a fresh address or alters an existing one, the tumbler resolution extracts is identically the one produced at that address's single allocation event — whether `d_s` authored the content or itself obtained it by any number of prior COPYs. Hence `a` is the same tumbler at the end of any chain `… → d_s → d`, and Gregory's trace confirms no copy hop ever rewrites the I-coordinate of a crum (Q13). Identity is invariant under arbitrarily deep copy chains.

**X6 (OriginPreservation).** For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run). Because the I-address itself encodes the home document, the system can, after placement, reveal that the content originated elsewhere — Nelson's "you always know where you are" [LM 2/40] is a structural consequence of X3, not a separately maintained annotation. Attribution cannot be stripped, because there is no attribution metadata to strip: there is only the address.

---

## What shifts: the arrangement, and nothing is overwritten

The displacement clause moves existing content forward to make room; it must lose nothing.

**X7 (NonDestructivePlacement).** Every pre-existing binding of `d` survives COPY, relabelled by the forward shift on the content subspace `s_C`: `(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`. *Derivation.* The shift `· + W` restricted to `{u ∈ V_{s_C}(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4), and its image lies at or above `v + W`, while the copied region occupies `[v, v+W)`; the two ranges are disjoint, so no copied mapping collides with a displaced one. The relabelling moves the displaced bindings (those `u ∈ V_{s_C}(d)` with `u ≥ v`) up to `[v+W, …)`, after which the copied region fills `[v, v+W)`. In last-component terms, the copied region occupies `[p, p+W)` and the displaced image occupies `[p+W, n_S+W]` — the shift carries every displaced slot to a last-component `≥ p+W`, while every copied last-component is `< p+W`, so no copied mapping can land on a surviving displaced one. Hence no `(V, I)` binding is destroyed or overwritten: each displaced binding survives with its I-address intact and only its V-label changes — there is no overwrite operation here, only displacement. Nelson:

> "users may create new published documents out of old ones indefinitely … without damaging the originals." [LM 2/45]

**X8 (RunFragmentation).** The copied region is *constructed* as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per run of the resolution *list* `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`). This constructed count `k` tracks the I-space fragmentation of the source, not the width `W`: copying heavily-edited (fragmented) source costs more blocks than copying pristine source of the same width. The *canonical* (maximally-merged, M12) count of the copied region need not equal `k`, however, and we must not conflate the two. Two cases separate:

- *Within a single reference*, no two blocks coalesce. Here the inference needs the source's V-contiguity to close, so we spell it out. The copied blocks of one reference are *target*-V-adjacent by construction (`c_{j+1} = c_j + n_j`) and carry their source I-coordinates unchanged, so a within-reference target merge candidate would require the consecutive resolved runs to be I-adjacent *in the source*. But `resolve(d_s, σ)` restricts `M(d_s)` to the span's V-range `f = M(d_s)|⟦σ⟧`, and the source content subspace is gap-free (D-SEQ, ASN-0036), so `f` has a contiguous V-domain and its consecutive maximal runs are *source*-V-adjacent. Maximal-merge (ASN-0058, C1a/M12) then forbids any source-V-adjacent pair from also being I-adjacent — that is exactly M7's conjunction it rules out. Since copy alters no I-coordinate, the source-V-adjacent-but-not-I-adjacent runs become target-V-adjacent-but-not-I-adjacent blocks. Hence no within-reference pair is a merge candidate.
- *Across an inter-reference boundary*, the last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and may also be I-adjacent — precisely when they share an origin and abut in I-space (`a' = a + n`, M16/M16a). Such a boundary satisfies the merge condition M7 and coalesces in the canonical form.

Hence the canonical block count is `≤ k`, with equality exactly when no inter-reference boundary is I-adjacent (in particular whenever consecutive references draw from distinct origins, X11). The abstract state commits only to the *arrangement* — the V→I mapping `Σ'.M(d)` — and not to any particular block count: the constructed `k`-block form and the canonical `≤ k` form denote the *same* arrangement, differing only as representations of it. An alternative implementation is free to store either (Q8).

**X9 (ContiguousTargetRange).** Although the source may fragment into `k` runs and may draw from several source documents, the copied content occupies one *contiguous* V-range `[v, v + W)` in the target, in source order. *Derivation.* The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order (Gregory Q14/Q17). The 2-D rebalancing of any concrete index cannot perturb this, since V-order is recomputed from coordinates that COPY does not alter (Q14).

**X16 (PostStateDensity).** The post-state content subspace `V_{s_C}(d)` in `Σ'` is exactly `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN). *Derivation.* By PC4 the pre-state positions are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S`, and `v = [s_C,1,…,1,p]`. The shift `· + W` on subspace `s_C` increments only the last component (it is the ordinal shift by `δ(W, m)`, OrdinalShift, ASN-0034: `shift(u, W)ᵢ = uᵢ` for `i < m` and `shift(u, W)_m = u_m + W`, leaving the subspace identifier and the intermediate `1`-components fixed; the subspace identifier `s_C = u₁` is preserved a fortiori by OrdShiftHom (a)). The three classes of post-state `s_C`-positions therefore occupy disjoint last-component ranges:

- *unmoved* (`u < v`): last component `c ∈ [1, p)`;
- *copied* (`v + c`, `0 ≤ c < W`): last component `c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`;
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`.

These three half-open/closed ranges tile `[1, n_S + W]` exactly: `[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap (the boundaries `p` and `p + W` are shared endpoints of abutting intervals) and no gap (every integer in `[1, n_S + W]` lies in exactly one range, using `1 ≤ p ≤ n_S + 1`). Hence `V_{s_C}(d)` in `Σ'` is the contiguous run `1 ≤ c ≤ n_S + W` — D-SEQ holds with population `n_S + W`. The minimum is `[s_C,1,…,1]`: when `p ≥ 2` it is the unmoved `c = 1` position; when `p = 1` the unmoved range is empty and `c = 1` is the first copied position; either way `c = 1` is occupied, so D-MIN holds. (The empty-subspace case `n_S = 0` is the specialisation `p = 1`, `W ≥ 1`: the result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at the depth `m` chosen in PC4, with minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.)

Finally, every post-state `s_C`-position — not only the insertion anchor `v` — is well-formed in the sense of S8a. ValidInsertionPosition (PC4) discharges S8a for `v = [s_C,1,…,1,p]` itself, but the interior copied positions `v + 1, …, v + (W−1)` and the displaced positions `u + W` are new entries in `dom(Σ'.M(d))` and must satisfy S8a independently. *Copied positions:* each `v + c = [s_C,1,…,1,p+c]` (`0 ≤ c < W`) has `zeros = 0`, depth `m ≥ 2`, and all components positive (`s_C ≥ 1`, the interior components are `1`, the last component `p + c ≥ 1`). *Displaced positions:* each `u + W = shift(u, W)` for `u ∈ V_{s_C}(d)` with `u ≥ v` inherits S8a from `u` — shift preserves S8a unconditionally (OrdShiftHom (b)) and preserves depth (`#shift(u, W) = #u = m`, OrdinalShift, ASN-0034) — so the displaced image is again a depth-`m`, zero-free, all-positive `s_C`-position. With S8a holding for all three classes, all post-state `s_C`-positions sharing depth `m` (S8-depth), and the copied, displaced, and unmoved `s_C`-classes occupying pairwise-disjoint V-positions (the tiling above), the modified subspace is internally collision-free. The remaining post-state positions — the unmoved link-subspace entries (`subspace(u) = s_L`) — are disjoint from *every* `s_C`-position by subspace-identifier distinctness: any `s_L`-position and any `s_C`-position are element-level tumblers differing in their first component (`s_L ≠ s_C`), so T7 (SubspaceDisjointness, ASN-0034) gives them distinct addresses with no possibility of collision. The tiling thus establishes disjointness *within* `s_C`, and T7 establishes disjointness *across* the subspace boundary, together yielding full pairwise disjointness of all post-state V-positions. Hence the post-state arrangement `Σ'.M(d)` is a well-defined partial function — S2 (functionality) is fully discharged for the post-state.

---

## What invariants the completed operation must maintain

Three further obligations bind the post-state.

**X10 (SourceHandling).** The guarantee splits by whether the source is the target, and the two halves are *different properties* — non-alteration in one case, pre-state resolution in the other.

*(a) Non-interference for sources `d' ≠ d`.* No source document *other than the target* is altered: `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and `Σ'.C = Σ.C`. In particular, when a source `d_s ≠ d`, `Σ'.M(d_s) = Σ.M(d_s)` — its arrangement, its referenced content, and (by X6) the origins of its content are all untouched.

*(b) Snapshot resolution for `d_s = d`.* When the source *is* the target (self-transclusion), the source document is not unaltered — it is the target, and its content-subspace arrangement is displaced by `· + W`. The guarantee that holds here is not non-alteration but *pre-state resolution*: the copied span is read against `Σ` before the displacement opens the gap. By the atomicity of COPY (X15), the precondition — including the resolution `resolve_Σ(R)` — is evaluated against the pre-state `Σ` in one indivisible step; thus `resolve_Σ(R)` reads `Σ.M(d)` *before* the displacement opens the gap, and `R` resolves against the frozen pre-state image of the copied span even though `d` is simultaneously the target. Gregory's trace exhibits the same ordering concretely (`specset2ispanset` precedes `insertpm`, Q15).

**X11 (CrossOriginSeparation).** When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge. *Derivation.* The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce. Each character's home document remains recoverable, as Nelson's royalty and attribution guarantees require (Q9).

**X12 (BoundaryAbsorption).** The copied region meets the surrounding arrangement at *two* boundaries, each an independent merge candidate under M7 (V-adjacency is given at both by construction; I-adjacency is the discriminating test):

- *Leading boundary* (present iff a position immediately precedes `v` in `V_{s_C}(d)`, i.e. `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).
- *Trailing boundary* (present iff content is displaced, i.e. `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` (the content formerly at `v`) — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. After any absorption the merged block is indistinguishable from one never split (M8) — *except* that origin is carried intact by the addresses (X6). Absorption is therefore a representational economy that never erases identity: the homedoc that conditions it (Gregory Q12) is precisely `origin`, and a boundary across which origins differ cannot be absorbed (X11).

**X13 (Multiplicity).** After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance — and the model imposes no bound on such multiplicity (ASN-0036, S5, UnrestrictedSharing). A single I-address may be referenced from arbitrarily many documents and positions; COPY is the operation that increases this multiplicity without increasing the content store.

**X14 (ContainmentRecording and coupling discharge).** At completion, `d` contains each copied address: `(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so `Contains_C(Σ') ⊇ {(a_j + i, d)}`, and COPY's effect has written the corresponding pairs into `Σ.R` (Definition: `Σ'.R = Σ.R ∪ {(a_j + i, d)}`). We must show this post-state is well-formed against the coupling invariants of ValidComposite★ (ASN-0047). By the composite-boundary consequence established in the Definition, the coupling clauses J0/J1★/J1'★ apply between `Σ` and `Σ'` and the composite-boundary property P4★ holds at `Σ`. Each clause is discharged:

- *J0 (AllocationPlacementCoupling, ASN-0047).* Vacuous: by X1, `dom(Σ'.C) = dom(Σ.C)`, so the antecedent `a ∈ dom(Σ'.C) ∖ dom(Σ.C)` is never satisfied — COPY allocates no content.

**Setup for the J1★/J1'★ discharges — `New` vs. `Old`.** Both provenance-coupling obligations turn on a distinction the J0 case did not need: *newly mapped at a position* versus *new to the range*. Write the copied address set `A = {a_j + i : 1 ≤ j ≤ k, 0 ≤ i < n_j}` and split it by prior membership in `d`'s range: `New = A ∖ ran(Σ.M(d))` (addresses `d` did not already reference) and `Old = A ∩ ran(Σ.M(d))` (addresses `d` already referenced). `Old` is non-empty exactly when `d` already holds some copied content — in particular under self-transclusion (`d_s = d`) or when a prior COPY already placed the same content in `d`. Every copied address is *mapped at a fresh copied position* `v + c` regardless of class; only those in `New` actually enlarge `ran(Σ.M(d))`. The two bullets below use this split directly.

- *J1★ (ExtensionRecordsProvenance, ASN-0047).* The content-subspace range gains exactly `New` (X3, restricted to subspace `s_C`) — a subset of `A`, possibly empty. For each `a ∈ New` the Definition's provenance effect records `(a, d) ∈ Σ'.R`, so every genuine range extension is recorded; the obligation is met by COPY's own effect, not deferred. For `a ∈ Old`, J1★'s antecedent `a ∈ ran(Σ'.M(d)) ∖ ran(Σ.M(d))` is false (the address was already in range), so J1★ imposes no obligation on it.
- *J1'★ (ProvenanceRequiresExtension).* The only pairs COPY adds to `R` are `{(a, d) : a ∈ A}`; we show each pair in `R' ∖ R` corresponds to a genuine range extension. *(a) `a ∈ New`:* `a` is new to the content-subspace range, so `a ∈ ran(Σ'.M(d)) ∖ ran(Σ.M(d))` at a copied position in subspace `s_C` (P3) — both conjuncts of J1'★ hold, and `(a, d)` lies in `R' ∖ R` legitimately. *(b) `a ∈ Old`:* `a` is already referenced by `d` at a content-subspace position before COPY (it is a content address, so by L14 (ASN-0043) it cannot be the image of any `s_L` V-position, and by S3★ its referencing position lies in `s_C`); hence `(a, d) ∈ Contains_C(Σ)`, and by P4★ (`Contains_C(Σ) ⊆ R`, ASN-0047) the pair `(a, d)` is *already* in `R` at the pre-state. So `(a, d) ∉ R' ∖ R`, and J1'★'s antecedent is false for it — vacuously satisfied. No pair in `R' ∖ R` fails to back a genuine range extension, so J1'★ holds.

Because COPY writes new pairs into `Σ.R`, it incurs two further provenance obligations that the foundation otherwise carries implicitly, and both are discharged at the point of the `Σ.R` extension. *P7 (ProvenanceGrounding: `(a, d) ∈ R ⟹ a ∈ dom(C)`).* Every pair COPY adds is `(a_j + i, d)` with `a_j + i ∈ A`; by C1 (via PC1, X3) every such address lies in `dom(Σ.C) = dom(Σ'.C)` (X1), so each newly recorded pair is grounded in the content store and P7 is preserved. The same pair is well-typed against `Σ.R ⊆ T_elem × E_doc` (ASN-0047) on both factors: the `E_doc` side by `d ∈ E_doc` (PC2), and the `T_elem` side because `Element(a_j + i)` holds — `a_j + i ∈ dom(Σ.C)` (just shown) and by S7b (ASN-0036) every content address is element-level (`zeros = 3`). *P4★ (`Contains_C(Σ') ⊆ R'`) at the post-state.* The post-state content-containment relation is `Contains_C(Σ') = Contains_C(Σ) ∪ {(a_j + i, d)}` (X14's first sentence gives the `⊇`; the displaced and unmoved classes carry their pre-state pairs forward unchanged, and no `s_C` image leaves the range, giving the `⊆`). Each pre-state pair lies in `R ⊆ R'` by P4★ at `Σ`; each new pair `(a_j + i, d)` lies in `R'` by COPY's effect. Hence `Contains_C(Σ') ⊆ R'`, and P4★ is preserved.

The remaining invariants of ExtendedReachableStateInvariants (ASN-0047) are discharged below, one conjunct or group per clause:

- *L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ, P8, NodeLineage, ActivatedEmission (link/entity Class (a)).* Preserved because COPY's frame leaves `Σ.L` and `Σ.E` untouched (`Σ'.L = Σ.L`, `Σ'.E = Σ.E`) and adds no `s_L`-subspace V-position, so every clause quantifying over `dom(Σ.L)`, `E`, or link-subspace positions holds at `Σ'` exactly as at `Σ`.
- *P6 (ExistentialCoherence).* `(A a ∈ dom(Σ.C) :: origin(a) ∈ E_doc)` carries forward: `dom(Σ.C)` and its origins are frozen (X1, X6) and `E_doc` is unchanged (`Σ'.E = Σ.E`).
- *S2, S8a.* Established at X16 (well-formed, pairwise-disjoint, single-depth post-state positions).
- *S3★.* The wp computation above.
- *S3★-aux.* Every post-state V-position has subspace `s_C` or `s_L`: copied positions are `s_C` by PC3; unmoved and displaced positions carry their pre-state subspace (`s_C` or `s_L` by pre-state S3★-aux) unchanged.
- *D-CTG★, D-MIN★, D-SEQ★.* Established at X16, restricted to the only modified subspace `s_C`; the others are unmoved.
- *S8-depth.* Established at X16, which fixes the common content-subspace depth `m` for every post-state `s_C`-position — the inherited `m` when `n_S ≥ 1`, the chosen-and-pinned `m` when `n_S = 0`.
- *S7a–S7d, C-fin.* Content store unchanged by X1.
- *S8-fin.* `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {copied positions}` adds exactly `W = (+ j : 1 ≤ j ≤ k : n_j) < ∞` positions to the finite pre-state domain (S8-fin at `Σ`), hence remains finite.
- *C1b (`#E(a) ≥ 2`), C1c (ContentAllocatorConformance).* Both quantify only over `dom(Σ.C)` and the tumbler structure of its members, which X1 freezes (`dom(Σ'.C) = dom(Σ.C)`, values fixed), so both hold at `Σ'` exactly as at `Σ`.
- *S8★ (PerSubspaceSpanDecomposition).* Re-established for the modified subspace: `Σ'.M(d)|_{V_{s_C}(d)}` is functional (S2, X16), finite-domain (S8-fin), and contiguous at the single common depth `m` (D-CTG★/D-SEQ★, X16) mapping into `dom(Σ'.C)` (S3★) — precisely ASN-0036's S8 hypotheses — so it decomposes, with `B_copy` plus the displaced and unmoved runs as witnessing runs; the link-subspace projection `Σ'.M(d)|_{V_{s_L}(d)}` is unmoved and carries its pre-state length-1 decomposition forward.
- *S4 (OriginBasedIdentity).* COPY allocates nothing (`dom(Σ'.C) = dom(Σ.C)`, X1), so the set of allocation events — and the pairwise distinctness S4 asserts — is identical at `Σ'` and `Σ`.
- *P4a, P7a (composite-boundary Class (b) beyond P4★).* P4a: each new pair `(a_j + i, d)` is witnessed by the post-state arrangement itself (`a_j + i ∈ ran(Σ'.M(d))` at a content-subspace position, X14). P7a: the copied addresses already enjoyed coverage at the pre-state (in `dom(Σ.C)`, hence recorded against some document by P7a at `Σ`), and COPY only adds pairs.

Finally, COPY is a transition, so it must also discharge the separate transition theorem **ExtendedTransitionInvariants** (ASN-0047), whose sole conjunct is **P3** (`dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ (A a ∈ dom(C) :: C'(a) = C(a)) ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))`). It is discharged directly from COPY's frame: `Σ'.C = Σ.C` gives both `dom(C) ⊆ dom(C')` and content value-fixity; `Σ'.L = Σ.L` gives both `dom(L) ⊆ dom(L')` and link value-fixity; `Σ'.E = Σ.E` gives `E ⊆ E'`; and `Σ'.R = Σ.R ∪ {(a_j+i, d)} ⊇ Σ.R` gives `R ⊆ R'`. Every conjunct of P3 holds, with M the only component that changes.

By content-containment permanence this record persists across subsequent states (the address remains discoverable as contained in `d` even if `d` later drops it from its arrangement). This is the abstract counterpart of the spanfilade entry that makes FINDDOCSCONTAINING return the target immediately after a copy, recorded against the *destination* document, not the original creator (Gregory Q18/Q19; Nelson Q6/Q8).

**X15 (Atomicity).** COPY either applies in full — establishing X1, X3, X7, S2, S3★, and the subspace's density discipline D-SEQ (X16) together — or not at all; no intermediate state is observable in which the displacement has been applied but the copied region not yet laid down, or vice versa. *Derivation.* COPY is a *single* elementary transition (Definition), not a composite of K.μ steps, so SequentialTransitionAxiom (ASN-0047/0093) applies to it directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step, with no intermediate state between. A partial application would leave `Σ'.M(d)` either non-dense (a V-gap, contradicting X16) or double-bound (two I-addresses at one position), violating the arrangement well-formedness that holds at every reachable state. Nelson reaches the same conclusion from the design side: the file is left "in canonical order, which was an internal mandate of the system" [LM 1/34] — there is no acknowledged state in which canonical order is suspended.

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
- **X3** — every newly referenced address (`a_1, a_1+1, a_2, a_2+1`) lies in `dom(Σ.C)`. Discharged by C1; required by `wp(COPY, S3★)`.
- **X7** — the displaced bindings `x_3, x_4, x_5` survive intact at `[1,7], [1,8], [1,9]`; nothing is overwritten. Here `W = 4 > n_S − p + 1 = 3`, so the freed positions are only `[1,3]..[1,5]` (the pre-state slots of `x_3, x_4, x_5`); the copied region fills `[1,3]..[1,6]`, of which `[1,6]` was unoccupied pre-state. The no-overwrite conclusion holds by the disjointness of copied (`[1,3]..[1,6]`) and displaced-image (`[1,7]..[1,9]`) ranges (X16), not by `[1,3]..[1,6]` having been fully populated.
- **X8** — the copied region is `k = 2` blocks, *independent of* `W = 4`. The two blocks are *not* I-adjacent (`a_2 ≠ a_1 + 2`, distinct origins), so the canonical count is also 2 — equality holds because the single inter-reference boundary is not I-adjacent.
- **X9** — the copy occupies the contiguous V-range `[1,3]..[1,6] = [v, v+W)`, in source order.
- **X11** — block `([1,3], a_1, 2)` (origin `d_1`) and block `([1,5], a_2, 2)` (origin `d_2`) cannot merge: I-adjacency would need `a_2 = a_1 + 2`, but M16 forbids it across distinct origins.
- **X16 (density)** — post-state `V_{s_C}(d) = {[1,c] : 1 ≤ c ≤ 9}`, contiguous, `n_S + W = 5 + 4 = 9`, minimum `[1,1]`. No gap.
- **X12** — leading boundary (`p = 3 ≥ 2`): the unmoved predecessor at `[1,2]` holds `x_2`; it absorbs block 1 iff `x_2`'s I-reach is `a_1`, i.e. `x_2 = a_1 - 1` with `origin(x_2) = d_1`. Trailing boundary (`p = 3 ≤ n_S = 5`): the first displaced block holds `x_3` at `[1,7]`; it absorbs block 2 iff `x_3 = a_2 + 2`. Both are genuine, independent candidates — generically neither fires.

### A self-transclusion scenario (`Old ≠ ∅`, source overlaps the displaced region)

The first example was cross-origin with a distinct source, so `Old = A ∩ ran(Σ.M(d))` was empty and the J1'★ branch for already-referenced addresses never fired. We now exercise exactly that branch — a *self-transclusion*, where the target is its own source — and we deliberately position the source span *at or after* `v`, so the copied span overlaps the region the displacement will move.

Fix `s_C = 1`. Let `d` have content subspace of common depth `m = 2` and population `n_S = 3`, so `V_{s_C}(d) = {[1,1], [1,2], [1,3]}` with pre-state bindings `Σ.M(d)([1,1]) = x_1`, `Σ.M(d)([1,2]) = x_2`, `Σ.M(d)([1,3]) = x_3`, where `x_1, x_2, x_3 ∈ dom(Σ.C)` are distinct. The source is the single self-reference `R = ⟨(d, σ)⟩` whose V-span covers `d`'s own *third* content position `[1,3]` — and crucially `[1,3] ≥ v` for the `v = [1,2]` we copy at, so the source lies squarely in the region the copy will displace. Resolved against the *pre-state* `Σ`: `resolve_Σ(R) = ⟨(x_3, 1)⟩` — one run of width `W = 1`, since `Σ.M(d)([1,3]) = x_3`. We copy at `v = [1,2]`, so `p = 2`, `k = 1`, `B_copy = {([1,2], x_3, 1)}`. The displaced region is `{u ∈ V_{s_C}(d) : u ≥ [1,2]} = {[1,2], [1,3]}`, which shifts by `W = 1` to `[1,3], [1,4]`.

The post-state arrangement `Σ'.M(d)`:

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `x_1` | unmoved |
| 2 | `[1,2]` | `x_3` | copied (blk 1) |
| 3 | `[1,3]` | `x_2` | displaced (from `[1,2]`) |
| 4 | `[1,4]` | `x_3` | displaced (from `[1,3]`) |

**Why X10(b)/X15 are load-bearing here.** The source span names V-position `[1,3]`, which satisfies `[1,3] ≥ v`. Resolution against the pre-state `Σ` reads `Σ.M(d)([1,3]) = x_3` — the correct content — and lays it down at the copied slot `[1,2] ∈ [v, v+W)`, while the original `x_3` shifts to `[1,4] ∈ [v+W, …)`. Had resolution instead read the *post-state* `Σ'`, position `[1,3]` would hold `x_2` — the content the displacement had just shoved up from `[1,2]` — so the copy would transclude `x_2` rather than `x_3`: a *different, circular* result, in which the operation feeds on its own displacement. X15's atomicity (the precondition, including `resolve_Σ(R)`, is read against `Σ` in one indivisible step) is precisely what forecloses this, and X10(b)'s pre-state pinning is the only thing that makes a self-transclusion overlapping the displaced region well-defined. Gregory's ordering (`specset2ispanset` precedes `insertpm`, Q15) exhibits the same discipline: the source is snapshotted *before* the arrangement is rewritten.

Now the provenance trace. The copied address set is `A = {x_3}`. The pre-state range is `ran(Σ.M(d)) = {x_1, x_2, x_3}`, so:

- `New = A ∖ ran(Σ.M(d)) = ∅` — the copied address was *already* referenced by `d`;
- `Old = A ∩ ran(Σ.M(d)) = {x_3} = A`.

COPY's effect still writes `Σ'.R = Σ.R ∪ {(x_3, d)}`. With `New = ∅` and `Old = A`, the couplings fire as X14's split dictates:

- **J1★** is vacuous: `New = ∅`, so there is no genuine range extension to record.
- **J1'★** is discharged on its `Old`-branch: `(x_3, d) ∈ Contains_C(Σ)` (x_3 is referenced by `d` at `[1,3]` in the pre-state, content subspace), so by P4★ it is already in `Σ.R`; hence `Σ'.R = Σ.R`, `R' ∖ R = ∅`, and the antecedent is false for every pair.

The reference multiplicity rises (X13): `x_3` is now referenced from `[1,2]` (copied) *and* `[1,4]` (its displaced original) — yet `dom(Σ'.C) = dom(Σ.C)` (X1) and `R' = R`, so neither store grows. And X7 is exercised non-trivially: the displaced bindings `x_2, x_3` survive intact at `[1,3], [1,4]`, the copied region `[1,2]` and the displaced-image range `[1,3], [1,4]` being disjoint (X16), so nothing is overwritten despite the source and the displaced content overlapping.

### The empty-subspace first insertion (`n_S = 0`, `p = 1`)

Both scenarios above are *interior* — a non-empty subspace with `1 < p ≤ n_S`, inheriting a pre-state D-SEQ run. The genuinely different configuration is the first insertion into an *empty* content subspace, where there is no pre-state common depth to inherit: the operation must *choose* a depth `m` and pin it (PC4, ValidFirstInsertionPosition), `New = A` with `Old = ∅`, and there are neither unmoved nor displaced positions.

Fix `s_C = 1`. Let `d` be freshly registered with `V_{s_C}(d) = ∅`, so `n_S = 0`. The source is a single same-origin reference of width `W = 2`: `R = ⟨(d_1, σ)⟩` with `resolve_Σ(R) = ⟨(a_1, 2)⟩`, `origin(a_1) = d_1`, and `a_1, a_1+1 ∈ dom(Σ.C)`. By PC4 the operation chooses depth `m = 2` and takes `v = [1,1]` of depth 2 (ValidFirstInsertionPosition), so `p = 1`, `k = 1`, `c_1 = 0`, `B_copy = {([1,1], a_1, 2)}`. The choice fixes `m = 2` as `d`'s content-subspace depth for all future positions.

The post-state arrangement `Σ'.M(d)`:

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `a_1` | copied (blk 1) |
| 2 | `[1,2]` | `a_1+1` | copied (blk 1) |

Now check the boundary-specific claims:

- **X1** — `dom(Σ'.C) = dom(Σ.C)`: `a_1, a_1+1` were already allocated; the empty subspace gains references, not content.
- **X16 (density, min)** — both the unmoved range (`p = 1`, empty) and the displaced range (no `u ≥ v`, since `V_{s_C}(d) = ∅`) are empty, so the tiling degenerates to the single copied range `[p, p+W) = [1, 3)`. Post-state `V_{s_C}(d) = {[1,c] : 1 ≤ c ≤ 2}` at the chosen depth `m = 2` — contiguous with `n_S + W = 0 + 2 = 2`, minimum `[1,1]` (the first copied position, not an unmoved one), discharged here by ValidFirstInsertionPosition rather than by an inherited D-SEQ. S8a holds for both copied positions: each `[1, 1+c]` (`0 ≤ c < 2`) has `zeros = 0`, depth `2 ≥ 2`, all components positive.
- **X14 (coupling split)** — `A = {a_1, a_1+1}`; the pre-state content-subspace range is empty, so `New = A` and `Old = ∅`. **J1★** fires on every copied address (each a genuine range extension, recorded by COPY's effect as `(a_1, d), (a_1+1, d) ∈ Σ'.R`); **J1'★** is discharged entirely on its `(a)`-branch (`New`); the `Old`-branch is vacuous. J0 is vacuous by X1.

### The append boundary (`p = n_S + 1`, trailing boundary absent)

A second boundary configuration the interior examples do not exercise is the *append*: inserting at `p = n_S + 1`, past the last occupied position. No content is displaced (there is no `u ∈ V_{s_C}(d)` with `u ≥ v`), so the trailing boundary of X12 is *absent* and only the leading boundary is a merge candidate.

Fix `s_C = 1`, `m = 2`, `n_S = 3`, so `V_{s_C}(d) = {[1,1], [1,2], [1,3]}` with bindings `x_1, x_2, x_3 ∈ dom(Σ.C)`. We copy at `v = [1,4]`, so `p = 4 = n_S + 1`. The source is a single same-origin reference of width `W = 2`: `resolve_Σ(R) = ⟨(a_1, 2)⟩`, `B_copy = {([1,4], a_1, 2)}`.

| `c` | post-state position | image | class |
|----|----|----|----|
| 1 | `[1,1]` | `x_1` | unmoved |
| 2 | `[1,2]` | `x_2` | unmoved |
| 3 | `[1,3]` | `x_3` | unmoved |
| 4 | `[1,4]` | `a_1` | copied (blk 1) |
| 5 | `[1,5]` | `a_1+1` | copied (blk 1) |

- **X16 (density)** — the displaced range is empty (`p = 4 > n_S = 3`), so the tiling is unmoved `[1, p) = [1, 4)` followed by copied `[p, p+W) = [4, 6)`, with no displaced tail. Post-state `V_{s_C}(d) = {[1,c] : 1 ≤ c ≤ 5}`, contiguous, `n_S + W = 5`, minimum `[1,1]` (unmoved).
- **X12 (trailing boundary absent)** — the leading boundary is present (`p = 4 ≥ 2`): the unmoved predecessor at `[1,3]` holds `x_3`, absorbing block 1 iff `x_3`'s I-reach is `a_1` (i.e. `x_3 = a_1 - 1` with `origin(x_3) = d_1`). The trailing boundary is *absent*: the condition `p ≤ n_S` fails (`4 ≤ 3` is false), there is no first displaced block, so no trailing merge candidate exists.

### A coalescing copy (`canonical < k`, leading boundary fires)

Every scenario above lands on the *non*-merging side of X8 and X12: distinct origins, or single runs, with each boundary failing I-adjacency. We now construct the discriminating case — a same-origin source whose two references abut in I-space (so the inter-reference boundary *coalesces*, `canonical = k − 1`), placed against a predecessor it I-abuts (so the *leading* boundary *absorbs*). One instance exercises the non-trivial half of both claims.

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

- **X8 (inter-reference coalescence, `canonical < k`)** — the two copied blocks are V-adjacent (`[1,5] = [1,3] + 2`, since `c_2 = n_1 = 2`) and I-adjacent (`a_1+2 = a_1 + n_1` with `n_1 = 2`, M7), and they share origin `d_1` (so M16 does not block them). The merge condition holds, and the copied region's canonical count is `k − 1 = 1`: the single block `([1,3], a_1, 4)`. This is the `canonical < k` half of X8, witnessed against a concrete instance rather than only argued in prose.
- **X12 (leading boundary absorbs)** — the leading boundary is present (`p = 3 ≥ 2`). The unmoved predecessor run `([1,1], a_1−2, 2)` ends with I-reach `(a_1−2) + 2 = a_1`, which equals the first copied I-start `a_1`; V-adjacency holds (`[1,3] = [1,1] + 2`) and origins agree (`d_1`). The predecessor *absorbs* the copied region — the firing case of X12, the half the append example left failing.
- **Whole-arrangement canonical form** — composing both merges, the entire post-state content subspace collapses to the single canonical block `([1,1], a_1−2, 6)`: six V-positions, one maximal I-run of width `n_S + W = 6`, all origin `d_1`. The constructed `k = 2`-block copied region (plus the unmoved run) and this one-block canonical form denote the *same* arrangement `Σ'.M(d)`, differing only as representations (X8) — no I-coordinate or V-order is altered by the choice between them.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| COPY | `COPY(R, d, v)` (single elementary transition; precond. PC1–PC4, target subspace `S = s_C`): `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; content subspace displaced forward by `W` and gap `[v, v+W)` bound to `resolve_Σ(R)` in order; `Σ'.R = Σ.R ∪ {(a_j+i, d)}` | introduced |
| X1 | ContentStoreInvariance — `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))` | introduced |
| X2 | NoFreshAllocation — COPY consumes no previously-unallocated address; next content-allocation frontier of `d` unchanged | introduced |
| X3 | SharedReference — `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`; placed addresses pre-exist (forced by X1 ∧ S3★) | introduced |
| X4 | IdentityOfInstance — every appearance of a copied address resolves to the single value `Σ.C(a)` | introduced |
| X5 | TransitiveIdentity — the placed address is the content's original I-address through arbitrary copy chains | introduced |
| X6 | OriginPreservation — `origin(a)` unchanged and recoverable for every copied `a`; attribution is structural | introduced |
| X7 | NonDestructivePlacement — every pre-existing binding of `d` survives, relabelled by the forward shift; nothing overwritten | introduced |
| X8 | RunFragmentation — copied region is *constructed* as `k` blocks (one per run of the resolution *list* `resolve_Σ(R)`, each per-reference maximally merged but not merged across reference boundaries, independent of `W`); canonical count `≤ k`, equality iff no inter-reference boundary is I-adjacent | introduced |
| X9 | ContiguousTargetRange — copied content occupies one contiguous V-range `[v, v+W)` in source order | introduced |
| X10 | SourceHandling — (a) non-interference: no source document *other than the target* (`d' ≠ d`) is altered; (b) snapshot resolution: when `d_s = d` the target-as-source is read at the pre-state (it *is* displaced, not unaltered) | introduced |
| X11 | CrossOriginSeparation — blocks of distinct origin cannot merge (M7 ∧ M16); distinct portions stay distinguishable | introduced |
| X12 | BoundaryAbsorption — leading boundary (`p ≥ 2`) and trailing boundary (`p ≤ n_S`) are independent merge candidates, each absorbing iff I-adjacent; origin still carried | introduced |
| X13 | Multiplicity — placed addresses gain reference multiplicity ≥ 2, with no model-imposed bound (S5) | introduced |
| X14 | ContainmentRecording and coupling discharge — `d` recorded as containing each copied address; provenance written to `Σ.R`; J0/J1★/J1'★ discharged, P7/P4★/P4a/P7a preserved, link/entity Class (a) invariants (incl. ActivatedEmission) vacuous, P3 (ExtendedTransitionInvariants) discharged from frame; record permanent; against destination | introduced |
| X15 | Atomicity — COPY (single elementary transition) applies wholly or not at all; no partial/intermediate arrangement observable | introduced |
| X16 | PostStateDensity — post-state `V_{s_C}(d) = {[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}`, contiguous (D-SEQ), min `[s_C,1,…,1]` (D-MIN) | introduced |

## Open Questions

When copied content is later displaced again by a subsequent operation, what invariant ties the original origin to the address's continued discoverability?

What must the system guarantee about containment records when a document that obtained content by reference is itself the source of a further reference?

Under what conditions, if any, may two references to the same content be required to resolve to differing views of it across time?

What must remain true of a copied address's identity when the document that allocated it is no longer reachable?
