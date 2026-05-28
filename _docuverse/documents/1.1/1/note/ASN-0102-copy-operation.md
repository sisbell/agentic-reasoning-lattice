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

COPY does not name bytes; it names *positions* that already hold bytes. Its source argument is a content reference sequence `R = ⟨r₁, …, r_p⟩` (ASN-0058), each `rᵢ = (d_i, σ_i)` a well-formed content reference into some source document's arrangement. Resolution flattens these into an I-address sequence

`resolve(R) = ⟨(a₁, n₁), …, (a_k, n_k)⟩`,    `W = w(resolve(R)) = (+ j : 1 ≤ j ≤ k : n_j)`.

Two facts about resolution are load-bearing and both come from ASN-0058. First, *every resolved address already exists*: by C1, `(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ.C)))`. Second, *the run count `k` is the number of maximal contiguous I-runs the source occupies* (C1a, M12) — it is a property of how fragmented the source content is in I-space, not of its width `W`. We will return to both.

The target argument is a document `d ∈ dom(Σ.M)` and a V-position `v` with `subspace(v) = S` that is a valid insertion position of `d`'s subspace `S` at the common depth `m` (ASN-0036, S8-depth). Let `n_S = |V_S(d)|` be the current population of that subspace, so the positions in `V_S(d)` are `[S,1,…,1,c]` for `1 ≤ c ≤ n_S` (D-SEQ), and `v = [S,1,…,1,p]` with `1 ≤ p ≤ n_S + 1`.

---

## Definition of COPY

The operation `COPY(R, d, v)` carries `Σ → Σ'` as follows.

**Content store — untouched.**
`Σ'.C = Σ.C`.

**Other documents — untouched.**
`(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`.

**Target arrangement.** Write the cumulative offset `c_j = (+ j' : 1 ≤ j' < j : n_{j'})`, so the copied region is the block set

`B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}`,

a contiguous lay-down of the resolved I-sequence at consecutive target V-positions. Positions of `d` in subspace `S` at or after `v` shift forward by `W`; positions below `v` and positions in other subspaces are unmoved. Formally `Σ'.M(d)` is the partial function

- `Σ'.M(d)(u) = Σ.M(d)(u)` for `u ∈ dom(Σ.M(d))` with `subspace(u) ≠ S`, or with `subspace(u) = S ∧ u < v`;
- `Σ'.M(d)(v + c) = a_j + i` where `c = c_j + i`, `0 ≤ i < n_j`, for each `0 ≤ c < W` (the copied region `B_copy`);
- `Σ'.M(d)(u + W) = Σ.M(d)(u)` for `u ∈ V_S(d)` with `u ≥ v` (the displaced region).

The displacement is the same forward shift that INSERT performs — Nelson treats COPY's positional effect as identical to INSERT's [LM 4/66–67] — and we specify it here only as far as needed to state COPY's invariants; its position-management mechanics are not the subject of this note. What *is* the subject is the half of the definition that distinguishes COPY from every content-creating operation: `Σ'.C = Σ.C`. We now derive its consequences.

---

## What is preserved: content immutability forces shared reference

We claim the operation cannot create content, and from that, that what it places must already exist.

**X1 (ContentStoreInvariance).** `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))`. This is immediate from the definition `Σ'.C = Σ.C`. But it is not an arbitrary stipulation; it is *what the act of inclusion means*. Nelson:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

Gregory's trace confirms the abstract claim concretely: `docopy` calls `insertpm` (which writes the document's POOM, the arrangement) and `insertspanf` (which writes the containment index), but never `inserttextingranf`, the sole content-creating primitive. The I-address high-water mark queried before allocation is therefore unchanged by COPY (Q16). We record this as a corollary.

**X2 (NoFreshAllocation).** COPY consumes no previously-unallocated address: the set of addresses available to a subsequent content-creating allocation in `d` is identical before and after COPY. *Derivation.* A content-creating allocation extends `dom(Σ.C)`; by X1 that set is unchanged, so the frontier from which the next address is drawn is unchanged. The cost of copying fragmented content is borne entirely in the arrangement (in the number of blocks, X8), never in the content store.

Now the decisive step. The arrangement must satisfy referential integrity: every V-position maps to an existing I-address (ASN-0036, S3). Apply this to the new mappings introduced by `B_copy` in the post-state. By construction the copied region binds positions to the addresses `a_j + i`. We compute the weakest precondition:

`wp(COPY, S3) ⊇ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ'.C))`.

By X1, `dom(Σ'.C) = dom(Σ.C)`. Therefore the placed addresses must *already* lie in `dom(Σ.C)` at the pre-state. The operation has no freedom here: having renounced content creation, the only addresses it can legally place are ones that already exist.

**X3 (SharedReference).** Every address introduced into `ran(Σ'.M(d))` by COPY already belonged to `dom(Σ.C)`: `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`. This is forced by X1 together with S3, and is discharged at the pre-state by ASN-0058 C1 (resolution yields only existing addresses). The placed content is a reference, never a duplicate — not by convention, but because there is no other state-consistent possibility.

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

**X7 (NonDestructivePlacement).** Every pre-existing binding of `d` survives COPY, relabelled by the forward shift on subspace `S`: `(A u ∈ dom(Σ.M(d)) : (subspace(u) ≠ S ∨ u < v) ⟹ Σ'.M(d)(u) = Σ.M(d)(u)) ∧ (A u ∈ V_S(d) : u ≥ v ⟹ Σ'.M(d)(u + W) = Σ.M(d)(u))`. *Derivation.* The shift `· + W` restricted to `{u ∈ V_S(d) : u ≥ v}` is strictly order-preserving and injective (ASN-0034, TS1/TS2/TS4), and its image lies at or above `v + W`, while the copied region occupies `[v, v+W)`; the two ranges are disjoint, so no copied mapping collides with a displaced one. The gap `[v, v+W)` is V-space that held nothing of `d` before the relabelling. Hence no `(V, I)` binding is overwritten — there is no overwrite operation here, only displacement. Nelson:

> "users may create new published documents out of old ones indefinitely … without damaging the originals." [LM 2/45]

**X8 (RunFragmentation).** The copied region admits a block decomposition with exactly `k` blocks — one per maximal contiguous I-run of `resolve(R)` — laid at consecutive V-starts: `B_copy = {(v + c_j, a_j, n_j) : 1 ≤ j ≤ k}` with `c_{j+1} = c_j + n_j`. The block count `k` tracks the I-space fragmentation of the source, not the width `W` (Gregory: one DOCISPAN per sporgl, `|new entries| = |ispanset(source)|`, Q11/Q18). Copying heavily-edited (fragmented) source costs more blocks than copying pristine source of the same width.

**X9 (ContiguousTargetRange).** Although the source may fragment into `k` runs and may draw from several source documents, the copied content occupies one *contiguous* V-range `[v, v + W)` in the target, in source order. *Derivation.* The blocks of `B_copy` are pairwise V-adjacent by construction (`c_{j+1} = c_j + n_j`); resolution concatenates references in their listed order and preserves intra-reference V-order (ASN-0058 C1b), so the target V-order is exactly the source order (Gregory Q14/Q17). The 2-D rebalancing of any concrete index cannot perturb this, since V-order is recomputed from coordinates that COPY does not alter (Q14).

---

## What invariants the completed operation must maintain

Three further obligations bind the post-state.

**X10 (SourceNonInterference).** No source document is altered: `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and `Σ'.C = Σ.C`. In particular, when a source `d_s ≠ d`, `Σ'.M(d_s) = Σ.M(d_s)` — its arrangement, its referenced content, and (by X6) the origins of its content are all untouched. The source is read, never written (Nelson Q7; Gregory Q15: resolution snapshots the source before any displacement, so even self-transclusion with `d_s = d` reads a frozen image of the copied span before the gap is opened).

**X11 (CrossOriginSeparation).** When the copied content draws from two or more origins, the distinct portions remain structurally distinguishable: blocks with different origins cannot merge. *Derivation.* The merge condition requires I-adjacency `a₂ = a₁ + n₁` (ASN-0058, M7); but addresses from distinct origins cannot be I-adjacent (M16), since `a₁ + n₁` shares `origin(a₁)` (M16a) while `a₂` does not. Hence a copied region spanning `r` distinct origins decomposes into at least `r` blocks that no canonicalisation can coalesce. Each character's home document remains recoverable, as Nelson's royalty and attribution guarantees require (Q9).

**X12 (BoundaryAbsorption).** The first copied block may absorb into the block immediately preceding `v`, and only then, exactly when they are both V-adjacent and I-adjacent (ASN-0058, M7); after absorption the merged block is indistinguishable from one never split (M8) — *except* that origin is carried intact by the addresses (X6). Absorption is therefore a representational economy that never erases identity: the homedoc that conditions it (Gregory Q12) is precisely `origin`, and a boundary across which origins differ cannot be absorbed (X11).

**X13 (Multiplicity).** After COPY the placed addresses are referenced from at least two V-positions — their source appearance and their target appearance — and the model imposes no bound on such multiplicity (ASN-0036, S5, UnrestrictedSharing). A single I-address may be referenced from arbitrarily many documents and positions; COPY is the operation that increases this multiplicity without increasing the content store.

**X14 (ContainmentRecording).** At completion, `d` contains each copied address: `(A j, i : 0 ≤ i < n_j : a_j + i ∈ ran(Σ'.M(d)))`, so the content-containment relation `Contains_C(Σ')` records `(a_j + i, d)`. By content-containment permanence this record persists across subsequent states (the address remains discoverable as contained in `d` even if `d` later drops it from its arrangement). This is the abstract counterpart of the spanfilade entry that makes FINDDOCSCONTAINING return the target immediately after a copy, recorded against the *destination* document, not the original creator (Gregory Q18/Q19; Nelson Q6/Q8). Origin-traceability (X6) and containment-recording (X14) are independent facts: the former says *where the content was born*, the latter says *which documents now hold it* — COPY establishes both.

**X15 (Atomicity).** COPY either applies in full — establishing X1, X3, X7, S2, S3, and the subspace's density discipline D-SEQ together — or not at all; no intermediate state is observable in which the displacement has been applied but the copied region not yet laid down, or vice versa. *Derivation.* Transitions are atomic and totally ordered (ASN-0047/0093, SequentialTransitionAxiom): the precondition is read against `Σ` and the effect committed to `Σ'` in one indivisible step. A partial application would leave `Σ'.M(d)` either non-dense (a V-gap) or double-bound (two I-addresses at one position), violating the arrangement well-formedness that holds at every reachable state. Nelson reaches the same conclusion from the design side: the file is left "in canonical order, which was an internal mandate of the system" [LM 1/34] — there is no acknowledged state in which canonical order is suspended.

---

## A remark on what COPY is

Strip the displacement away — which COPY shares with content creation — and what remains is the irreducible essence: COPY is the operation that *enlarges the arrangement's reach into the content store without enlarging the store*. It is the unique act that grows `ran(Σ.M(d))` while leaving `dom(Σ.C)` fixed (X1 ∧ X3). Content creation grows both; deletion shrinks reach without touching the store; rearrangement permutes within fixed reach. COPY alone imports existing identity. Every consequence in this note — shared instance, transitive origin, source non-interference, cross-origin separation, permanent containment — follows from that one positional fact about the two streams. The word "copy" is, as Nelson observed, a misnomer; the operation is inclusion, and inclusion is reference.

---

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| COPY | `COPY(R, d, v)`: `Σ'.C = Σ.C`; `Σ'.M(d') = Σ.M(d')` for `d' ≠ d`; target subspace `S` displaced forward by `W` and gap `[v, v+W)` bound to `resolve(R)` in order | introduced |
| X1 | ContentStoreInvariance — `dom(Σ'.C) = dom(Σ.C) ∧ (A a ∈ dom(Σ.C) : Σ'.C(a) = Σ.C(a))` | introduced |
| X2 | NoFreshAllocation — COPY consumes no previously-unallocated address; next content-allocation frontier of `d` unchanged | introduced |
| X3 | SharedReference — `ran(Σ'.M(d)) ∖ ran(Σ.M(d)) ⊆ dom(Σ.C)`; placed addresses pre-exist (forced by X1 ∧ S3) | introduced |
| X4 | IdentityOfInstance — every appearance of a copied address resolves to the single value `Σ.C(a)` | introduced |
| X5 | TransitiveIdentity — the placed address is the content's original I-address through arbitrary copy chains | introduced |
| X6 | OriginPreservation — `origin(a)` unchanged and recoverable for every copied `a`; attribution is structural | introduced |
| X7 | NonDestructivePlacement — every pre-existing binding of `d` survives, relabelled by the forward shift; nothing overwritten | introduced |
| X8 | RunFragmentation — copied region is `k` blocks, one per maximal contiguous I-run; `k` independent of `W` | introduced |
| X9 | ContiguousTargetRange — copied content occupies one contiguous V-range `[v, v+W)` in source order | introduced |
| X10 | SourceNonInterference — no source document's arrangement, content, or origins are altered | introduced |
| X11 | CrossOriginSeparation — blocks of distinct origin cannot merge (M7 ∧ M16); distinct portions stay distinguishable | introduced |
| X12 | BoundaryAbsorption — first copied block absorbs the predecessor iff V- and I-adjacent; origin still carried | introduced |
| X13 | Multiplicity — placed addresses gain reference multiplicity ≥ 2, with no model-imposed bound (S5) | introduced |
| X14 | ContainmentRecording — `d` recorded as containing each copied address; record permanent; against destination | introduced |
| X15 | Atomicity — COPY applies wholly or not at all; no partial arrangement observable | introduced |

## Open Questions

What must a placement operation guarantee about the consistency of a self-transclusion when the target position lies strictly inside the source span?

When copied content is later displaced again by a subsequent operation, what invariant ties the original origin to the address's continued discoverability?

What must the system guarantee about containment records when a document that obtained content by reference is itself the source of a further reference?

Under what conditions, if any, may two references to the same content be required to resolve to differing views of it across time?

What must remain true of a copied address's identity when the document that allocated it is no longer reachable?
