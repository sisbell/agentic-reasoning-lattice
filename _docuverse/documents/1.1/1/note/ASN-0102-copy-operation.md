# ASN-0102: The COPY Operation

*2026-05-28*

We are asked what happens when *existing* content is placed at a position in a document. The word "placed" is treacherous: in ordinary computing it means *duplicated*, and the placement creates a second, independent occurrence of the bytes. The whole of this note is an argument that, for the operation we are specifying, placement means something else — placement by *reference* — and that this single decision dictates everything the operation may and may not do.

We work over the standing state. A system state `Σ` carries a content store `Σ.C : T ⇀ Val` and, for each document `d`, an arrangement `Σ.M(d) : T ⇀ T` mapping V-positions to I-addresses (ASN-0036). We write `dom(Σ.C)` for the set of allocated I-addresses and `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` for the I-addresses `d` currently references. The tumbler vocabulary — the order `<`, displacement `⊕`/`⊖`, the shift `shift(t, k)` (written `t + k` in its ordinal form, with `t + 0 = t`, after ASN-0058), the subspace projector `subspace(v)`, the home-document projector `origin(a) = N(a).0.U(a).0.D(a)` (ASN-0036, S7) — is taken from the foundations without restatement. Mapping blocks `(v, a, n)` with denotation `⟦(v,a,n)⟧ = {(v+k, a+k) : 0 ≤ k < n}`, their decomposition into maximal runs, the merge condition, and the resolution of content references are taken from ASN-0058.

---

## The cardinal question

There is exactly one operation in the foundational vocabulary that brings genuinely new content into existence: it allocates a fresh I-address and binds a value to it, enlarging `dom(Σ.C)`. COPY is *not* that operation. Nelson is explicit that the two are different acts over the same address machinery — one touches both streams, the other touches only the arrangement:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

So the question "what is the effect of placing existing content" resolves into three sub-questions, and we will answer each as a consequence of one decision. *What is preserved?* The content's permanent identity. *What shifts?* The arrangement, and only the arrangement. *What invariants must hold at completion?* Referential integrity, origin-traceability, and atomicity. We take these in turn, but first we must say what the operation *is*.

---

## The source designation and its resolution

COPY does not name bytes; it names *positions* that already hold bytes. Its source argument is a content reference sequence `R = ⟨r₁, …, r_p⟩` (ASN-0058), each `rᵢ = (d_i, σ_i)` a well-formed content reference into some source document's arrangement. Resolution flattens these into an I-address sequence. Because the source may include the target itself (`d_s = d`), the evaluation point matters: we resolve against the *pre-state* `Σ`, the state at which the operation's precondition is read, and write the result with that state pinned:

`resolve_Σ(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve_Σ(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

Two facts about resolution are load-bearing and both come from ASN-0058. First, *every resolved address already exists*: by C1, `(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C)))`. Second, *the run count `k` is the number of maximal contiguous I-runs the source occupies* (C1a, M12) — it is a property of how fragmented the source content is in I-space, not of its width `W`. We will return to both.

### Precondition

We collect the complete precondition under which `COPY(R, d, v)` is defined at `Σ`.

- **(P1) Source resolvable at `Σ`.** Each `rᵢ = (d_i, σ_i)` is a well-formed content reference (ASN-0058) with `d_i ∈ dom(Σ.M)` and `V_{S_i}(d_i) ≠ ∅`, so `resolve_Σ(R)` is defined. Since `p ≥ 1` and each reference has positive resolved width (C2 gives `w(resolve_Σ(r_i)) = ℓ_{i,m} ≥ 1`), the total width satisfies **`W ≥ 1`** — the empty copy is excluded.
- **(P2) Target document.** `d ∈ dom(Σ.M)`.
- **(P3) Content subspace.** The target subspace is the content (byte) subspace: `S = s_C`. COPY places transcluded *content*, whose resolved addresses lie in `dom(Σ.C)` and so carry `subspace_I(·) = s_C`; the link subspace `s_L` is populated only in creation order by MAKELINK and is not a legal target for COPY (Q1). This pins `subspace(v) = s_C` for the inserted positions and is the conjunct S3★ will require below.
- **(P4) Valid insertion position.** Write `n_S = |V_{s_C}(d)|`.
  - *Non-empty subspace* (`n_S ≥ 1`): by D-SEQ the positions of `V_{s_C}(d)` are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S` at the common depth `m` (S8-depth), and `v = [s_C,1,…,1,p]` is a valid insertion position with `1 ≤ p ≤ n_S + 1` (ASN-0036, ValidInsertionPosition).
  - *Empty subspace* (`n_S = 0`): there is no pre-existing common depth. The operation *chooses* a depth `m ≥ 2` and takes `v = [s_C,1,…,1]` of depth `m` (ASN-0036, ValidFirstInsertionPosition), with `p = 1`; this choice fixes `m` as the content-subspace depth of `d` for all subsequent positions.

---

## Definition of COPY

COPY is a *single elementary transition*: we add it to the system's transition vocabulary `Σ` (ASN-0047) as its own operation, with the complete frame stated below. It is deliberately *not* an instance of K.μ⁺ (ArrangementExtension, ASN-0047), which requires `M'(d)(v) = M(d)(v)` on every pre-existing V-position; COPY *relabels* the content-subspace positions at or after `v` by the forward shift `· + W`, so no extension transition describes it. Declaring COPY elementary — one indivisible event, precondition read against `Σ` and effect committed to `Σ'` in a single step under SequentialTransitionAxiom (ASN-0047/0093) — is what underwrites both the atomicity guarantee (X15) and the pre-state resolution that makes self-transclusion well-defined (X10). Because the standing state carries five components, `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)`, the contract must pin all five.

The operation `COPY(R, d, v)` carries `Σ → Σ'` as follows.

**Content store — untouched.**
`Σ'.C = Σ.C`.

**Link store — untouched.**
`Σ'.L = Σ.L`. COPY creates no link and alters none; this discharges the `s_L`-routing conjunct of S3★ below and preserves L12 (link immutability) vacuously.

**Entity set — untouched.**
`Σ'.E = Σ.E`. COPY allocates no node, account, or document.

**Other documents — untouched.**
`(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`.

**Target arrangement.** Write the cumulative offset `c_j = (+ j' : 1 ≤ j' < j : n_{j'})`, so the copied region is the block set

`B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`,

a contiguous lay-down of the resolved I-sequence at consecutive target V-positions. Positions of `d` in the content subspace `s_C` (P3) at or after `v` shift forward by `W`; positions below `v` and positions in the link subspace are unmoved. Formally `Σ'.M(d)` is the partial function

- `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ s_C`, or with `subspace(u) = s_C ∧ u < v`;
- `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W` (the copied region `B_copy`);
- `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_{s_C}(d)` with `u ≥ v` (the displaced region).

**Provenance.** COPY extends `d`'s content-subspace range by the copied addresses, so its effect records their containment in the provenance relation:

`Σ'.R = Σ.R ∪ {(a_j + i, d) : 1 ≤ j ≤ k, 0 ≤ i < n_j}`.

This is a state component distinct from the *derived* containment relation `Contains_C` (which reads off `Σ'.M` automatically): the provenance relation `Σ.R` records the fact persistently, and it is the effect that discharges the coupling invariant J1★ (ExtensionRecordsProvenanceContentSubspace, ASN-0047) — see X14. Folding the K.ρ-style recording into COPY's own effect is what lets a single elementary transition meet the coupling obligation that the foundation otherwise discharges at a composite boundary.

The displacement is the same forward shift that INSERT performs — Nelson treats COPY's positional effect as identical to INSERT's [LM 4/66–67] — and we specify it here only as far as needed to state COPY's invariants; its position-management mechanics are not the subject of this note. What *is* the subject is the half of the definition that distinguishes COPY from every content-creating operation: `Σ'.C = Σ.C`. We now derive its consequences.

---

## What is preserved: content immutability forces shared reference

We claim the operation cannot create content, and from that, that what it places must already exist.

**X1 (ContentStoreInvariance).** `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`. This is immediate from the definition `Σ'.C = Σ.C`. But it is not an arbitrary stipulation; it is *what the act of inclusion means*. Nelson:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

Gregory's trace confirms the abstract claim concretely: `docopy` calls `insertpm` (which writes the document's POOM, the arrangement) and `insertspanf` (which writes the containment index), but never `inserttextingranf`, the sole content-creating primitive. The I-address high-water mark queried before allocation is therefore unchanged by COPY (Q16). We record this as a corollary.

**X2 (NoFreshAllocation).** COPY consumes no previously-unallocated address: the set of addresses available to a subsequent content-creating allocation in `d` is identical before and after COPY. *Derivation.* A content-creating allocation extends `dom(Σ.C)`; by X1 that set is unchanged, so the frontier from which the next address is drawn is unchanged. The cost of copying fragmented content is borne entirely in the arrangement (in the number of blocks, X8), never in the content store.

Now the decisive step. In the extended state the governing invariant is the *generalised* referential integrity S3★ (ASN-0047): every V-position is routed to the store its subspace names — `subspace(v) = s_C ⟹ Σ'.M(d)(v) ∈ dom(Σ'.C)` and `subspace(v) = s_L ⟹ Σ'.M(d)(v) ∈ dom(Σ'.L)`. We must establish S3★ at the post-state, so we compute the weakest precondition over *all* post-state mappings of `d`, which the definition partitions into three classes:

- *Unmoved* (`subspace(u) ≠ s_C`, or `subspace(u) = s_C ∧ u < v`): `Σ'.M(d)(u) = Σ.M(d)(u)`. These images are unchanged, so S3★ holds for them in `Σ'` exactly as it did in `Σ`, since `dom(Σ'.C) = dom(Σ.C)` (X1) and `dom(Σ'.L) = dom(Σ.L)` (COPY's frame leaves `Σ.L` untouched). In particular the `s_L`-routing conjunct is discharged with no new obligation: COPY introduces no link-subspace position and alters no existing one.
- *Displaced* (`u ∈ V_{s_C}(d), u ≥ v`, image at `u + W`): `Σ'.M(d)(u + W) = Σ.M(d)(u)`, again an unchanged image in subspace `s_C`, so its target lies in `dom(Σ.C) = dom(Σ'.C)` as before.
- *Copied* (positions `v + c` for `0 ≤ c < W`, all in subspace `s_C` by P3): `Σ'.M(d)(v + c) = a_j + i`. These are the only genuinely new obligations, and they fall entirely under the `s_C` conjunct of S3★.

The two preserved classes are discharged by X1 and the link-frame. Hence the whole of S3★ reduces to a single biconditional obligation on the copied region:

`wp(COPY, S3★) ≡ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C))`

(using `dom(Σ'.C) = dom(Σ.C)` by X1; the relation is equality, not containment — these are exactly the new mappings S3★ constrains, and they are routed to `dom(Σ.C)` because P3 fixes their subspace to `s_C`). Therefore the placed addresses must *already* lie in `dom(Σ.C)` at the pre-state, and they do, by C1 (resolution yields only existing addresses). The operation has no freedom here: having renounced content creation, the only addresses it can legally place are ones that already exist — and P3 guarantees it places them where S3★ demands.

**X3 (SharedReference).** Every address introduced into `ran(Σ'.M(d))` by COPY already belonged to `dom(Σ.C)`: `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`. This is forced by X1 together with S3★, and is discharged at the pre-state by ASN-0058 C1 (resolution yields only existing addresses). The placed content is a reference, never a duplicate — not by convention, but because there is no other state-consistent possibility.

---

## What is preserved: identity of instance, and its transitivity

Because COPY places the original I-addresses themselves, every appearance of the content resolves through the *same* key into the *single* content store.

**X4 (IdentityOfInstance).** If `Σ'.M(d)(v') = a` (a copied appearance) and `Σ.M(d_s)(v_s) = a` (its source appearance), then both denote the one value `Σ.C(a) = Σ'.C(a)`. The content store is a function (a key has one value), so there is nothing for the two appearances to disagree about. Nelson's formulation is that there is no second copy from which to diverge:

> "The COPY operation does not duplicate content — it creates an additional Vstream reference to the same Istream content." (Q4)

Identity here is *of instance*, not of value: two independently authored occurrences of the same text hold distinct I-addresses and are not made equal by COPY; only addresses that share an origin share an I-address.

**X5 (TransitiveIdentity).** The address placed by COPY is the content's *original* I-address, irrespective of how many copy hops separate source from origin. *Derivation.* Resolution reads the source document's arrangement to extract the stored I-address (ASN-0058 `resolve` consults `Σ.M(d_s)`); the arrangement of `d_s` already holds the original address whether `d_s` authored the content or itself obtained it by an earlier COPY (by this same X3 applied to that earlier step). Hence `a` is the same tumbler at the end of any chain `… → d_s → d`, and Gregory's trace confirms no copy hop ever rewrites the I-coordinate of a crum (Q13). Identity is invariant under arbitrarily deep copy chains.

**X6 (OriginPreservation).** For every copied address `a`, `origin(a)` is unchanged by COPY and continues to identify the document that allocated `a` (ASN-0036, S7; ASN-0058, M16a gives invariance of origin under the ordinal shift used within a run). Because the I-address itself encodes the home document, the system can, after placement, reveal that the content originated elsewhere — Nelson's "you always know where you are" [LM 2/40] is a structural consequence of X3, not a separately maintained annotation. Attribution cannot be stripped, because there is no attribution metadata to strip: there is only the address.

---

## What shifts: the arrangement, and nothing is overwritten

The displacement clause moves existing content forward to make room; it must lose nothing.

**X7 (NonDestructivePlacement).** Every pre-existing binding of `d` survives COPY, relabelled by the forward shift on the content subspace `s_C`: `(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ s_C ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_{s_C}(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`. *Derivation.* The shift `· + W` restricted to `{u ∈ V_{s_C}(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4), and its image lies at or above `v + W`, while the copied region occupies `[v, v+W)`; the two ranges are disjoint, so no copied mapping collides with a displaced one. The gap `[v, v+W)` is V-space that held nothing of `d` before the relabelling. Hence no `(V, I)` binding is overwritten — there is no overwrite operation here, only displacement. Nelson:

> "users may create new published documents out of old ones indefinitely … without damaging the originals." [LM 2/45]

**X8 (RunFragmentation).** The copied region is *constructed* as `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` — `k` blocks, one per maximal contiguous I-run of `resolve_Σ(R)`, laid at consecutive V-starts (`c_{j+1} = c_j + n_j`). This constructed count `k` tracks the I-space fragmentation of the source, not the width `W`: copying heavily-edited (fragmented) source costs more blocks than copying pristine source of the same width. The *canonical* (maximally-merged, M12) count of the copied region need not equal `k`, however, and we must not conflate the two. Two cases separate:

- *Within a single reference*, consecutive runs are the maximal runs of that reference (C1a, M12), hence pairwise non-I-adjacent by definition of maximality; they never coalesce.
- *Across an inter-reference boundary*, the last block of `r_i` and the first of `r_{i+1}` are V-adjacent by construction and may also be I-adjacent — precisely when they share an origin and abut in I-space (`a' = a + n`, M16/M16a). Such a boundary satisfies the merge condition M7 and coalesces in the canonical form.

Hence the canonical block count is `≤ k`, with equality exactly when no inter-reference boundary is I-adjacent (in particular whenever consecutive references draw from distinct origins, X11). The constructed `k`-block form is what the contiguous lay-down produces directly; whether Gregory's implementation *coalesces* below `k` depends on which index one examines, and the two indices part company precisely at a same-origin, I-abutting boundary. The POOM side (`docopy` → `insertpm`) *does* coalesce such a boundary: `insertcbcnd` widens an existing crum in place exactly when `isanextensionnd`'s twin gates both pass — `homedoc` equality *and* I-adjacency (the incoming I-origin equals the existing crum's I-reach) — and because the references are laid down at consecutive V-positions, the second `insertpm` finds the first crum's reach at exactly the abutting position and extends it rather than emitting a second crum (Q8). The POOM therefore realises the *canonical* (`≤ k`) count. The spanfilade side (`insertspanf`) has no such extension mechanism: it issues one `insertnd` call per I-span entry and stores one DOCISPAN entry per reference, realising the constructed count `k`. The two counts agree exactly when no inter-reference boundary is same-origin and I-adjacent; where one is, the POOM crum count drops below `k` while the spanfilade entry count stays at `k`. The canonical count is the abstract lower bound, and the POOM attains it.

**X9 (ContiguousTargetRange).** Although the source may fragment into `k` runs and may draw from several source documents, the copied content occupies one *contiguous* V-range `[v, v + W)` in the target, in source order. *Derivation.* The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order (Gregory Q14/Q17). The 2-D rebalancing of any concrete index cannot perturb this, since V-order is recomputed from coordinates that COPY does not alter (Q14).

**X16 (PostStateDensity).** The post-state content subspace `V_{s_C}(d)` in `Σ'` is exactly `{[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}` at depth `m` — contiguous with no V-gap (D-SEQ) and with minimum `[s_C,1,…,1]` (D-MIN). *Derivation.* By P4 the pre-state positions are `[s_C,1,…,1,c]` for `1 ≤ c ≤ n_S`, and `v = [s_C,1,…,1,p]`. The shift `· + W` on subspace `s_C` increments only the last component (it is the ordinal shift `δ(W, m)`, OrdShiftHom, leaving the subspace identifier and the intermediate `1`-components fixed). The three classes of post-state `s_C`-positions therefore occupy disjoint last-component ranges:

- *unmoved* (`u < v`): last component `c ∈ [1, p)`;
- *copied* (`v + c`, `0 ≤ c < W`): last component `c ∈ [p, p + W)`, since `v + c = [s_C,1,…,1,p+c]`;
- *displaced* (`u ≥ v`, image `u + W`): original last component `c ∈ [p, n_S]` mapped to `c + W ∈ [p + W, n_S + W]`.

These three half-open/closed ranges tile `[1, n_S + W]` exactly: `[1, p) ∪ [p, p + W) ∪ [p + W, n_S + W] = [1, n_S + W]`, with no overlap (the boundaries `p` and `p + W` are shared endpoints of abutting intervals) and no gap (every integer in `[1, n_S + W]` lies in exactly one range, using `1 ≤ p ≤ n_S + 1`). Hence `V_{s_C}(d)` in `Σ'` is the contiguous run `1 ≤ c ≤ n_S + W` — D-SEQ holds with population `n_S + W`. The minimum is `[s_C,1,…,1]`: when `p ≥ 2` it is the unmoved `c = 1` position; when `p = 1` the unmoved range is empty and `c = 1` is the first copied position; either way `c = 1` is occupied, so D-MIN holds. (The empty-subspace case `n_S = 0` is the specialisation `p = 1`, `W ≥ 1`: the result is `{[s_C,1,…,1,c] : 1 ≤ c ≤ W}` at the depth `m` chosen in P4, with minimum `[s_C,1,…,1]` by ValidFirstInsertionPosition.)

---

## What invariants the completed operation must maintain

Three further obligations bind the post-state.

**X10 (SourceNonInterference).** No source document is altered: `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and `Σ'.C = Σ.C`. In particular, when a source `d_s ≠ d`, `Σ'.M(d_s) = Σ.M(d_s)` — its arrangement, its referenced content, and (by X6) the origins of its content are all untouched. *Self-transclusion.* When `d_s = d`, the snapshot property follows from the formal transition semantics, not from implementation detail: by SequentialTransitionAxiom (ASN-0047/0093) the precondition — including the resolution `resolve_Σ(R)` — is evaluated against the pre-state `Σ` and the effect is committed to `Σ'` in one indivisible step. Thus `resolve_Σ(R)` reads `Σ.M(d)` *before* the displacement opens the gap, and `R` resolves against the frozen pre-state image of the copied span even though `d` is simultaneously the target. Gregory's trace exhibits the same ordering concretely (`specset2ispanset` precedes `insertpm`, Q15), but the guarantee is already forced by the atomicity of the transition.

**X11 (CrossOriginSeparation).** When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge. *Derivation.* The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce. Each character's home document remains recoverable, as Nelson's royalty and attribution guarantees require (Q9).

**X12 (BoundaryAbsorption).** The copied region meets the surrounding arrangement at *two* boundaries, each an independent merge candidate under M7 (V-adjacency is given at both by construction; I-adjacency is the discriminating test):

- *Leading boundary* (present iff a position immediately precedes `v` in `V_{s_C}(d)`, i.e. `p ≥ 2`): the first copied block `(v, a_1, n_1)` absorbs into the unmoved predecessor block ending at `v` exactly when that predecessor's I-reach equals `a_1` (I-adjacency).
- *Trailing boundary* (present iff content is displaced, i.e. `p ≤ n_S`): the last copied block `(v + c_k, a_k, n_k)` and the first displaced block — V-start `v + W` (V-adjacent, since `c_k + n_k = W`), I-start `Σ.M(d)(v)` (the content formerly at `v`) — absorb exactly when `Σ.M(d)(v) = a_k + n_k` (I-adjacency).

Neither boundary is privileged: each may absorb, both may, or neither, and the conditions are independent. The earlier claim that the leading boundary is the *only* absorption site is false — the trailing boundary is an equal candidate whenever `p ≤ n_S`. After any absorption the merged block is indistinguishable from one never split (M8) — *except* that origin is carried intact by the addresses (X6). Absorption is therefore a representational economy that never erases identity: the homedoc that conditions it (Gregory Q12) is precisely `origin`, and a boundary across which origins differ cannot be absorbed (X11).

**X13 (Multiplicity).** After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance — and the model imposes no bound on such multiplicity (ASN-0036, S5, UnrestrictedSharing). A single I-address may be referenced from arbitrarily many documents and positions; COPY is the operation that increases this multiplicity without increasing the content store.

**X14 (ContainmentRecording and coupling discharge).** At completion, `d` contains each copied address: `(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so the *derived* content-containment relation records `Contains_C(Σ') ⊇ {(a_j + i, d)}`. Containment is read off `Σ'.M` and is therefore automatic; the *provenance* relation `Σ.R` is a separate state component, which COPY's effect populates explicitly (Definition): `Σ'.R = Σ.R ∪ {(a_j + i, d)}`. We must show this post-state is well-formed against the coupling invariants of ValidComposite★ (ASN-0047). Treating COPY as the length-1 composite it is, each is discharged:

- *J0 (AllocationRequiresPlacement).* Vacuous: by X1, `dom(Σ'.C) = dom(Σ.C)`, so the antecedent `a ∈ dom(Σ'.C) ∖ dom(Σ.C)` is never satisfied — COPY allocates no content.
- *J1★ (ExtensionRecordsProvenanceContentSubspace).* The content-subspace range gains exactly `{a_j + i}` (X3, restricted to subspace `s_C`), and the Definition's provenance effect records `(a_j + i, d) ∈ Σ'.R` for precisely these addresses. The obligation is met by COPY's own effect, not deferred.
- *J1'★ (ProvenanceRequiresExtension).* The only pairs added to `R` are `{(a_j + i, d)}`, and each `a_j + i` is a content address newly mapped in `d`'s content subspace at the copied position `v + c_j + i`. Every new provenance pair is therefore backed by a genuine content-subspace range extension, with no spurious record.

By content-containment permanence this record persists across subsequent states (the address remains discoverable as contained in `d` even if `d` later drops it from its arrangement). This is the abstract counterpart of the spanfilade entry that makes FINDDOCSCONTAINING return the target immediately after a copy, recorded against the *destination* document, not the original creator (Gregory Q18/Q19; Nelson Q6/Q8). Origin-traceability (X6) and containment-recording (X14) are independent facts: the former says *where the content was born*, the latter says *which documents now hold it* — COPY establishes both.

**X15 (Atomicity).** COPY either applies in full — establishing X1, X3, X7, S2, S3★, and the subspace's density discipline D-SEQ (X16) together — or not at all; no intermediate state is observable in which the displacement has been applied but the copied region not yet laid down, or vice versa. *Derivation.* COPY is a *single* elementary transition (Definition), not a composite of K.μ steps, so SequentialTransitionAxiom (ASN-0047/0093) applies to it directly: the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step, with no intermediate state between. (Were COPY instead a composite, ValidComposite★ would admit observable states between its atomic steps, and this clause would weaken to a composite-boundary guarantee; the elementary declaration is what licenses the strong "no intermediate state" form here.) This same axiom pins `resolve_Σ(R)` to the pre-state — the source is read *before* any displacement (cf. X10), so self-transclusion sees a frozen image. A partial application would leave `Σ'.M(d)` either non-dense (a V-gap, contradicting X16) or double-bound (two I-addresses at one position), violating the arrangement well-formedness that holds at every reachable state. Nelson reaches the same conclusion from the design side: the file is left "in canonical order, which was an internal mandate of the system" [LM 1/34] — there is no acknowledged state in which canonical order is suspended.

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
- **X7** — the displaced bindings `x_3, x_4, x_5` survive intact at `[1,7], [1,8], [1,9]`; nothing is overwritten (the copied region occupied the freed `[1,3]..[1,6]`).
- **X8** — the copied region is `k = 2` blocks, *independent of* `W = 4`. The two blocks are *not* I-adjacent (`a_2 ≠ a_1 + 2`, distinct origins), so the canonical count is also 2 — equality holds because the single inter-reference boundary is not I-adjacent.
- **X9** — the copy occupies the contiguous V-range `[1,3]..[1,6] = [v, v+W)`, in source order.
- **X11** — block `([1,3], a_1, 2)` (origin `d_1`) and block `([1,5], a_2, 2)` (origin `d_2`) cannot merge: I-adjacency would need `a_2 = a_1 + 2`, but M16 forbids it across distinct origins.
- **X16 (density)** — post-state `V_{s_C}(d) = {[1,c] : 1 ≤ c ≤ 9}`, contiguous, `n_S + W = 5 + 4 = 9`, minimum `[1,1]`. No gap.
- **X12** — leading boundary (`p = 3 ≥ 2`): the unmoved predecessor at `[1,2]` holds `x_2`; it absorbs block 1 iff `x_2`'s I-reach is `a_1`, i.e. `x_2 = a_1 - 1` with `origin(x_2) = d_1`. Trailing boundary (`p = 3 ≤ n_S = 5`): the first displaced block holds `x_3` at `[1,7]`; it absorbs block 2 iff `x_3 = a_2 + 2`. Both are genuine, independent candidates — generically neither fires.

---

## A remark on what COPY is

Strip the displacement away — which COPY shares with content creation — and what remains is the irreducible essence: COPY is the operation that *enlarges the arrangement's reach into the content store without enlarging the store*. It is the unique act that grows `ran(Σ.M(d))` while leaving `dom(Σ.C)` fixed (X1 ∧ X3). Content creation grows both; deletion shrinks reach without touching the store; rearrangement permutes within fixed reach. COPY alone imports existing identity. Every consequence in this note — shared instance, transitive origin, source non-interference, cross-origin separation, permanent containment — follows from that one positional fact about the two streams. The word "copy" is, as Nelson observed, a misnomer; the operation is inclusion, and inclusion is reference.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| COPY | `COPY(R, d, v)` (single elementary transition; precond. P1–P4, target subspace `S = s_C`): `Σ'.C = Σ.C`; `Σ'.L = Σ.L`; `Σ'.E = Σ.E`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; content subspace displaced forward by `W` and gap `[v, v+W)` bound to `resolve_Σ(R)` in order; `Σ'.R = Σ.R ∪ {(a_j+i, d)}` | introduced |
| X1 | ContentStoreInvariance — `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))` | introduced |
| X2 | NoFreshAllocation — COPY consumes no previously-unallocated address; next content-allocation frontier of `d` unchanged | introduced |
| X3 | SharedReference — `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`; placed addresses pre-exist (forced by X1 ∧ S3★) | introduced |
| X4 | IdentityOfInstance — every appearance of a copied address resolves to the single value `Σ.C(a)` | introduced |
| X5 | TransitiveIdentity — the placed address is the content's original I-address through arbitrary copy chains | introduced |
| X6 | OriginPreservation — `origin(a)` unchanged and recoverable for every copied `a`; attribution is structural | introduced |
| X7 | NonDestructivePlacement — every pre-existing binding of `d` survives, relabelled by the forward shift; nothing overwritten | introduced |
| X8 | RunFragmentation — copied region is *constructed* as `k` blocks (one per maximal contiguous I-run, independent of `W`); canonical count `≤ k`, equality iff no inter-reference boundary is I-adjacent | introduced |
| X9 | ContiguousTargetRange — copied content occupies one contiguous V-range `[v, v+W)` in source order | introduced |
| X10 | SourceNonInterference — no source document's arrangement, content, or origins are altered | introduced |
| X11 | CrossOriginSeparation — blocks of distinct origin cannot merge (M7 ∧ M16); distinct portions stay distinguishable | introduced |
| X12 | BoundaryAbsorption — leading boundary (`p ≥ 2`) and trailing boundary (`p ≤ n_S`) are independent merge candidates, each absorbing iff I-adjacent; origin still carried | introduced |
| X13 | Multiplicity — placed addresses gain reference multiplicity ≥ 2, with no model-imposed bound (S5) | introduced |
| X14 | ContainmentRecording and coupling discharge — `d` recorded as containing each copied address; provenance written to `Σ.R`; J0/J1★/J1'★ discharged; record permanent; against destination | introduced |
| X15 | Atomicity — COPY (single elementary transition) applies wholly or not at all; no partial/intermediate arrangement observable | introduced |
| X16 | PostStateDensity — post-state `V_{s_C}(d) = {[s_C,1,…,1,c] : 1 ≤ c ≤ n_S + W}`, contiguous (D-SEQ), min `[s_C,1,…,1]` (D-MIN) | introduced |

## Open Questions

When copied content is later displaced again by a subsequent operation, what invariant ties the original origin to the address's continued discoverability?

What must the system guarantee about containment records when a document that obtained content by reference is itself the source of a further reference?

Under what conditions, if any, may two references to the same content be required to resolve to differing views of it across time?

What must remain true of a copied address's identity when the document that allocated it is no longer reachable?
