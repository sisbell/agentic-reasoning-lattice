# ASN-0036: Istream and Vstream

*2026-03-14; revised 2026-03-21, 2026-03-22, 2026-03-22*

We wish to understand what formal invariants govern the relationship between permanent content storage and mutable document arrangement in Xanadu. Nelson separated these concerns into two address spaces — Istream for content identity and Vstream for document positions — and asserted this separation as the architectural foundation on which permanence, transclusion, and attribution all rest. We seek the abstract properties that define this separation: what must hold in any correct implementation, regardless of the underlying data structures.

The approach is: model the system as two state components, derive what each must guarantee independently, then identify the invariants connecting them. Nelson provides architectural intent; Gregory's implementation reveals which properties are load-bearing.

Nelson conceived the two streams as inseparable aspects of a single architecture. Gregory implemented them as distinct enfilade types with different stability characteristics. Between these two accounts we find the abstract structure: a content store that grows but never changes, and a family of arrangement functions that change freely but may reference only what the store contains.


## Two components of state

The observation that motivates the entire design is that content EXISTS independently of how it is ARRANGED. A paragraph does not cease to exist when removed from a document — it merely ceases to appear there. Nelson states this plainly:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

This observation forces the state into two components:

**Σ.C : T ⇀ Val** — the *content store*. A partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

**Σ.M(d) : T ⇀ T** — the *arrangement* of document `d`. A partial function mapping Vstream positions to Istream addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

A conventional system merges these — "the file" IS the content IS the arrangement. Editing overwrites. Saving destroys the prior state. Nelson rejected this explicitly: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." The two-component model is his alternative: editing modifies `M(d)` while `C` remains invariant. The separation is the premise; what follows are the invariants it must satisfy.


## The content store

We ask: what must `C` guarantee? Nelson requires that any historical version be reconstructable, that content transcluded across documents maintain its meaning, and that attribution be permanent. Working backward from these guarantees — what must `C` satisfy for them to hold?

Suppose `C(a)` could change from value `w` to `w'` in some state transition. Then every document whose arrangement maps a V-position to `a` would silently show different content — with no editing operation having touched any arrangement. Historical versions, which reconstruct their state by reassembling Istream fragments, would silently present altered text. Content transcluded from one document into another would mutate without the including document's knowledge or consent. Nelson: "Users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." Mutation of `C(a)` damages every original that contains `a`.

We therefore require:

**S0 (Content immutability).** For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

Once content is stored at address `a`, both the address and its value are fixed for all future states. This is the central invariant of the two-stream architecture.

S0 is a strong property. It asserts two things simultaneously: that `a` remains in the domain (the address persists), and that the value at `a` is unchanged (the content is immutable). In weakest-precondition terms, for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state. This constrains every operation to either leave `C(a)` unchanged or to operate only on addresses not yet in `dom(C)` — that is, to create new content at fresh addresses.

**S1 (Store monotonicity).** `[dom(Σ.C) ⊆ dom(Σ'.C)]`

S1 is a corollary of S0, stated separately for emphasis. It is the content-store specialisation of T8 (allocation permanence, ASN-0034): T8 guarantees that allocated addresses persist in the abstract address space; S1 ensures that the content at those addresses persists as well.

S0 and S1 together establish `C` as an *append-only log*. New entries may be added — each at a fresh address guaranteed unique by T9 and T10 (ASN-0034) — but no existing entry may be modified or removed.

Nelson states this as an explicit design commitment: "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." Gregory's implementation confirms the commitment. Of the seventeen FEBE commands Nelson specifies, none modifies existing Istream content. There is no MODIFY, UPDATE, or REPLACE operation. The absence is structural — the protocol provides no mechanism for mutating stored content.

Gregory's evidence reveals an instructive footnote. The implementation carries a `refcount` field annotated "for subtree sharing, disk garbage collecting." Functions for reference-counted deletion exist: `deletefullcrumandgarbageddescendents()` and `deletewithgarbageddescendents()`. But the actual reclamation call was commented out on a specific date: `/*subtreefree(ptr);*/ /*12/04/86*/`. The machinery was built, dated December 4, 1986, and deliberately deactivated. S0 and S1 are upheld not by architectural impossibility but by a design choice so consistent that four decades of continuous operation have never violated it.


## The arrangement and referential integrity

Vstream is where mutability lives. Each document's arrangement `M(d)` maps V-positions to I-addresses, presenting stored content as a readable sequence. Unlike `C`, arrangements change freely — content can be added, removed, and reordered.

**S2 (Arrangement functionality).** For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

This is inherent in the concept of a "virtual byte stream." Nelson: "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." Each position in the stream shows exactly one piece of content. A V-position cannot simultaneously contain two different things.

We note the phrase "regardless of their native origin." A document's Vstream presents content as a seamless sequence even when the I-addresses are scattered across multiple documents' Istreams. The arrangement function is what makes heterogeneous Istream origins appear as a uniform Vstream stream.

The bridge between the two state components is a well-formedness condition:

**S3 (Referential integrity).** `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Every V-reference resolves. If a document's arrangement says "at position `v`, display the content at I-address `a`," then `a` must be in `dom(C)`. There are no dangling references.

The maintenance of S3 across state transitions reveals a temporal ordering constraint. The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

For an operation that only adds a V-mapping without creating content, the target I-address must already be in `dom(C)`. An operation that atomically creates content at `a` and adds the mapping `M(d)(v) = a` satisfies S3 in the post-state without sequential precedence — `a ∈ dom(Σ'.C)` and `Σ'.M(d)(v) = a` are established simultaneously. The dependency is logical, not temporal: a reference presupposes the existence of its target, but existence need not precede reference in a prior transition. What matters for persistence is that S1 guarantees once `a` enters `dom(C)`, it remains — so a valid reference cannot become dangling through any subsequent state transition.

We observe a deliberate asymmetry. S3 says arrangement implies existence: `ran(M(d)) ⊆ dom(C)`. It does NOT say existence implies arrangement. Content can exist in Istream without being arranged in any current document. Nelson calls such content "deleted bytes — not currently addressable, awaiting historical backtrack functions, may remain included in other versions." The asymmetry is the space in which persistence independence lives.


## Content identity

What distinguishes transclusion from coincidence? In conventional systems, identity is by value — two files with identical bytes are "the same." In Xanadu, identity is by address.

**S4 (Origin-based identity).** For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`. Two independent writings of the word "hello" produce distinct I-addresses. A transclusion of existing content shares the original I-address.

S4 follows from foundation properties. T9 (ForwardAllocation, ASN-0034) covers same-allocator distinctness: later allocations are strictly greater, hence distinct from all earlier ones. T10 (PartitionIndependence, ASN-0034) covers cross-allocator distinctness for non-nesting prefixes: disjoint subtree populations mean allocations from independent allocators cannot collide. For allocators with nesting prefixes (parent-child), T10a (AllocatorDiscipline, ASN-0034) guarantees the child's outputs are deeper than the parent's — by TA5(d), `#inc(t, k') = #t + k'` — so T3 (CanonicalRepresentation, ASN-0034) ensures their outputs are distinct. Together they guarantee that no two distinct allocations — whether from the same allocator or different allocators, whether simultaneous or separated by years — produce the same address. The two-stream architecture exploits this guarantee: when `Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂)` for documents `d₁ ≠ d₂`, the system knows this is transclusion — shared content with a common origin — not coincidental value equality. The structural test for shared identity is address equality, decidable from the addresses alone (T3, ASN-0034) without value comparison.

S4 creates a fundamental asymmetry in the system. The content store `C` is oblivious to values — it does not care whether `C(a₁) = C(a₂)`. But the arrangement family `M` is sensitive to addresses — two arrangements that map to the same I-address share content structurally, while two arrangements that map to different I-addresses with equal values do not. Nelson captures the distinction:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage... Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Live content shares I-addresses. Dead copies create new ones. The difference is structural — computable from the state alone.


## Sharing

The arrangement function `M(d)` need not be injective. This is not a deficiency but a design requirement — it is what makes transclusion work.

**S5 (Unrestricted sharing).** The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

To see this, fix any `N`. Construct state `Σ_N` with one I-address `a` where `C(a) = w` for some value `w`, and `N + 1` documents `d₁, ..., d_{N+1}`, each with `M(dᵢ) = {vᵢ ↦ a}` for distinct V-positions `vᵢ`. S0 is vacuous — single state, no transition to check. S2 holds: each `M(dᵢ)` is a function with a single entry. S3 holds: `a ∈ dom(C)`. The sharing multiplicity of `a` is `N + 1 > N`. Since `N` was arbitrary, no finite bound is entailed. The same holds within a single document: for any `N`, construct `Σ'_N` with one I-address `a` where `C(a) = w`, and one document `d` with `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}` for `N + 1` distinct V-positions. S0 and S1 are vacuous as above (single state, no transition to check). S2 holds — each `vᵢ` maps to exactly one I-address (namely `a`). S3 holds — `a ∈ dom(C)`. The within-document sharing multiplicity is `N + 1 > N`.

In any particular state, the sharing multiplicity of each address is a definite finite number — possibly zero for orphaned content (S6). The property is an architectural anti-constraint: the invariants place no finite cap on how many references may accumulate.

Nelson: "The virtual byte stream of a document may include bytes from any other document." And: "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely." Transclusion is recursive and unlimited.

Gregory confirms the unbounded nature at the implementation level. The global index that records which documents reference which I-addresses accumulates entries without cap — "no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism anywhere in the code path." Each referential inclusion adds one entry. The only constraints are physical resources (memory and disk), not architectural limits.

The combination of S4 and S5 gives the system its distinctive character. S4 says identity is structural — determined by I-address, not by value. S5 says sharing is unlimited — any number of documents can reference the same content. Together they establish a regime in which quotation is a first-class structural relationship: any number of documents can quote the same passage, and the system knows they are all quoting — not independently writing — because they share I-addresses.

We observe that the state `Σ = (C, M)` makes the sharing relation computable: given any `a ∈ dom(C)`, the set `{d : (E v :: M(d)(v) = a)}` is determined by the state. Nelson requires this to be queryable: "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." The state model supports this — the information is present; only the efficiency of its extraction is an implementation concern.


## Persistence independence

Content persists in Istream regardless of whether any arrangement references it.

**S6 (Persistence independence).** The membership of `a` in `dom(Σ.C)` is independent of all arrangements:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

S6 is a consequence of S0, which guarantees domain persistence unconditionally — it does not condition on whether any arrangement references `a`. But we state S6 separately because it names a design commitment that S0's formulation does not emphasise: the decision NOT to garbage-collect unreferenced content.

A system could satisfy a weakened form of S0 that permits removal when `(A d :: a ∉ ran(M(d)))` — when no arrangement references the content. Nelson explicitly rejects this. "Deleted bytes" are described as "not currently addressable, awaiting historical backtrack functions." The content remains because history requires it. Version reconstruction depends on the availability of Istream fragments from prior arrangements. If content were reclaimed when its last current reference vanished, the system could not fulfill: "When you ask for a given part of a given version at a given time, it comes to your screen."

S6 creates what Gregory calls an "orphan" phenomenon. Content in `dom(C)` that is not in `ran(M(d))` for any current document `d` is *unreachable through any query that starts from Vstream*. Gregory's evidence is definitive: "There is no mechanism to discover them, and the architecture makes no provision for it." The system provides no Istream iterator, no allocation registry queryable for "all content ever stored." To retrieve orphaned content, you must already know its I-address.

This is not a deficiency but a structural consequence of the two-stream model. The system's query interface is Vstream-primary: you start from a document (a Vstream entity), look up content (through the arrangement), and follow references (through Istream addresses). There is no path that begins in Istream and discovers content without a Vstream entry point. Orphaned content is permanent but practically invisible — a kind of information-theoretic dark matter, present by guarantee but unobservable through the system's own instruments.


## Structural attribution

Every V-position can be traced to the document that originally created its content.

S7 requires an architectural premise that T4 alone does not supply. T4 tells us HOW to parse a tumbler into fields; it does not tell us that Istream addresses are allocated under the originating document's tumbler prefix. We state this premise explicitly:

**S7a (Document-scoped allocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

This is a design requirement, not a convention. Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. The address IS the provenance: "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents.

We must also restrict S7's domain. The function `fields(a).document` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: `zeros = 0` is node-only, `zeros = 1` is node+user, `zeros ≥ 2` has a document field). Since Istream addresses designate content elements within documents, we require:

**S7b (Element-level I-addresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This is a design requirement: content resides at the element level — the finest level of the four-level tumbler hierarchy. Node, user, and document-level tumblers identify containers, not content. By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

With S7a and S7b established, we can state structural attribution:

**S7 (Structural attribution).** For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system. Three cases establish that distinct documents produce distinct prefixes. T9 (ForwardAllocation, ASN-0034) covers same-allocator distinctness: later allocations are strictly greater, so distinct documents within an allocator have distinct prefixes. T10 (PartitionIndependence, ASN-0034) covers cross-allocator distinctness for non-nesting prefixes: disjoint subtree populations mean documents from independent allocators cannot share a prefix. For allocators with nesting prefixes (parent-child, where a parent spawns a child via `inc(·, k')` per T10a), AllocatorDiscipline (T10a, ASN-0034) guarantees the child's outputs are deeper than the parent's — by TA5(d), `#inc(t, k') = #t + k'` — so T3 (CanonicalRepresentation, ASN-0034) ensures their document prefixes are distinct. It is not metadata that can be stripped or forged — it IS the address. To retrieve the content, the system must know its I-address; to know its I-address is to know its origin.

S7 follows from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), and T4 (FieldSeparatorConstraint, ASN-0034). Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

We note a subtlety. S7 identifies the document that ALLOCATED the I-address — the document where the content was first created. This is distinct from the document where the content currently appears. When content is transcluded from document B into document A, the reader viewing A sees the content, but S7 traces it to B. The distinction between "where I am reading" (Vstream context, document A) and "where this came from" (Istream structure, document B) is precisely the two-stream separation made visible.

Gregory's implementation reveals two mechanisms for origin lookup. The I-address prefix itself encodes the originating document (used during address allocation to scope the search range). Separately, each arrangement entry carries an explicit `homedoc` field recording the allocating document (used during retrieval). At the abstract level, S7 says only that the information is present in the address — it does not prescribe how an implementation extracts it.


## Span decomposition

The arrangement `M(d)` maps individual V-positions to I-addresses. But the mapping has internal structure: contiguous V-ranges often correspond to contiguous I-ranges. This is what makes finite representation possible.

Before defining correspondence runs, we must establish the structure of `dom(M(d))` more carefully.

**S8-fin (Finite arrangement).** For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

S8-fin follows from the operational reality: each V-position enters `dom(M(d))` through a specific operation (INSERT, COPY, etc.), and the system has performed only finitely many operations. No operation introduces infinitely many V-positions.

**S8a (V-position well-formedness).** Every text-subspace V-position is an element-field tumbler with all components strictly positive:

`(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`

A V-position represents the element field of a full document-scoped address — the fourth field in the T4 field structure. Its first component `v₁` is the subspace identifier; this ASN treats only the text subspace, where `v₁ ≥ 1`. The range guard `v₁ ≥ 1` captures both text-subspace (v₁ = 1) and link-subspace (v₁ = 2) V-positions. This ASN treats only the text subspace; the link subspace is deferred to a future ASN. The domain and range of `M(d)` live in structurally different tumbler subsets: within the text subspace, `{v ∈ dom(M(d)) : v₁ ≥ 1} ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}` (element-field tumblers), while `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b). Since all V-positions in subspace `s` extend the single-component prefix `[s]`, T5 (PrefixContiguity, ASN-0034) guarantees they form a contiguous interval under T1 — grounding the application of tumbler ordering properties to V-positions and justifying S8-depth's reference to "within a subspace."

*Remark.* The shared vocabulary identifies a second subspace for links (v₁ = 2, per T4 and LM 4/30). Link-subspace V-positions satisfy the same `zeros(v) = 0` and `v > 0` constraints as text-subspace positions — both are element-field tumblers with strictly positive components. The subspace identifier (1 for text, 2 for links) is the first component of the element field; the `0` in tumbler notation (e.g., `N.0.U.0.D.V.0.2.1`) is a field separator, not a subspace identifier. Link-subspace arrangement semantics are deferred to a future ASN.

**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

This is a design requirement, not a convention — parallel to S7a. Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth. Any correct implementation must satisfy this constraint.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: position `s.x` is followed by `s.(x+1)`. A parallel uniformity holds for I-addresses within a correspondence run: all I-addresses in a run share the same tumbler depth and prefix, differing only at the element ordinal. This follows from TA7a (ASN-0034): ordinal displacement `[x] ⊕ [k] = [x + k]` preserves the component count by construction, so the full I-address preserves depth and prefix when the structural context is held fixed. The uniformity is definitional — a correspondence run `(v, a, n)` specifies `M(d)(v + k) = a + k`, and both `v + k` and `a + k` are ordinal displacements that TA7a guarantees remain within their respective subspaces at the same depth. We write `v + k` for ordinal displacement applied to V-positions, and `a + k` for the same applied to the element ordinal of I-addresses.

(Why non-trivial runs arise in practice is a separate question. Allocator discipline — T10a, ASN-0034 — establishes that each allocator produces sibling outputs exclusively by `inc(·, 0)`, and TA5(c) guarantees the successor has the same depth as the predecessor. Consecutive allocations therefore produce consecutive I-addresses, which is why sequential content creation naturally yields correspondence runs of length greater than one. But this operational fact is motivation for the definition of correspondence runs, not a dependency of the decomposition proof.)

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a` — no displacement, no arithmetic. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount. Within a correspondence run, each step forward in Vstream corresponds to the same step forward in Istream.

**S8 (Finite span decomposition).** For each document `d`, the text-subspace portion of the arrangement — `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d)) ∧ v₁ ≥ 1}` — can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the text-subspace V-positions: every text-subspace V-position in `dom(Σ.M(d))` falls in exactly one run — `(A v ∈ dom(Σ.M(d)) : v₁ ≥ 1 : (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run: `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

Each run represents a contiguous block of content that entered the arrangement as a unit — characters typed sequentially, or a span transcluded whole.

The decomposition always exists. By S8-fin, `dom(M(d))` is finite, hence so is its text-subspace subset `{v ∈ dom(M(d)) : v₁ ≥ 1}`. For the degenerate case: each V-position `v` with `M(d)(v) = a` forms a singleton run `(v, a, 1)`. At `k = 0`: `M(d)(v + 0) = M(d)(v) = a = a + 0` — the base case holds trivially. Since `dom(M(d))` is finite, the set of singleton runs is finite.

It remains to show uniqueness: each text-subspace `v ∈ dom(M(d))` (with `v₁ ≥ 1`) falls in exactly one singleton's interval. A singleton `(v, a, 1)` claims the interval `[v, v + 1)` — that is, `{t : v ≤ t < v + 1}` where `v + 1` is the ordinal successor within the subspace. Two cases. *Same subspace*: by S8-depth, all V-positions in a subspace share the same tumbler depth `d`. For a depth-`d` V-position `v`, the singleton claims interval `[v, v + 1)`, where `v + 1` is the ordinal successor. Since `zeros(v) = 0` (S8a), every component of `v` is nonzero, so `sig(v) = max({i : 1 ≤ i ≤ d ∧ vᵢ ≠ 0}) = max({1, …, d}) = d` — and TA5(c) with `k = 0` therefore changes only position `d`, with `#(v+1) = #v = d`. We show this interval contains no depth-`d` tumbler other than `v` itself. Suppose `t` has depth `d` and `v ≤ t < v + 1`. If `t = v`, done. Otherwise `t ≠ v`, and since `#t = #v = d`, divergence occurs at some component position `j ≤ d`. If `j < d`: then `t_i = v_i` for `i < j` and `t_j > v_j` (from `v ≤ t`). Since `v + 1` agrees with `v` at all positions before `d`, `(v+1)_j = v_j < t_j`, giving `t > v + 1` by T1 — contradicting `t < v + 1`. If `j = d`: then `t_i = v_i` for `i < d`. From `v ≤ t`, `t_d ≥ v_d`; from `t < v + 1` (with `(v+1)_d = v_d + 1`), `t_d < v_d + 1`, so `t_d = v_d` — contradicting `t_d ≠ v_d`. Therefore `t = v`. Since distinct V-positions produce disjoint singleton intervals, the singletons partition each subspace's V-positions. Without S8-depth this fails: if `dom(M(d))` contained both `s.3` (depth 2) and `s.3.1` (depth 3), then `s.3 < s.3.1 < s.4` by T1 prefix extension, and `s.3.1` would fall in the interval of both singletons. *Different subspaces*: by S8a, V-positions in subspace `s` share the prefix `[s]`. By T5 (PrefixContiguity, ASN-0034), the set of tumblers extending `[s]` forms a contiguous interval under T1. By T10 (PartitionIndependence, ASN-0034), if `s₁ ≠ s₂` then `[s₁]` and `[s₂]` are non-nesting prefixes (both are single-component tumblers differing at position 1, so neither is a prefix of the other), and all tumblers with prefix `[s₁]` are distinct from all tumblers with prefix `[s₂]`. T5 gives contiguity of each prefix's extensions; T10 gives disjointness; together they give separation — no singleton interval in one subspace contains any tumbler from another. The singleton runs therefore partition `{v ∈ dom(M(d)) : v₁ ≥ 1}`.

What matters architecturally is that the number of runs `#runs(d)` is typically far smaller than `|dom(M(d))|` — the representation cost is proportional to the number of editing events, not the document size.

S8 follows from the finiteness of the text-subspace portion of `dom(M(d))` (S8-fin) and the structure of tumbler arithmetic — S8-depth and TA7a ensure ordinal displacement preserves depth within each subspace, T5 and T10 guarantee cross-subspace disjointness (T5 gives contiguity, T10 gives separation), and TA5(c) ensures ordinal successors preserve tumbler length. The singleton decomposition always exists; non-trivial runs arise when consecutive allocations produce consecutive I-addresses (as T10a and TA5(c) ensure operationally). Editing can both split and remove runs — inserting content in the middle of a run splits it into two, while deleting an entire run's V-span removes it. The number of distinct Istream allocation events underlying a document's history is monotonically non-decreasing (by S1), but the current arrangement's run count fluctuates with editing.

Gregory's evidence shows that `#runs(d)` has consequences beyond representation cost. Each correspondence run requires an independent tree traversal during V↔I translation. Gregory identifies the inner loop of this traversal as the documented CPU hotspot, responsible for 40% of processing time. For a document with `N` runs, a full V→I conversion requires `N` independent traversals — the cost is multiplicative in the fragmentation level, not merely additive. A consolidation function to merge adjacent runs was started in the implementation and abandoned mid-expression — the function body stops with an incomplete conditional: `if(`. Any implementation of the two-stream architecture must either consolidate runs or accept performance proportional to fragmentation level.


## Arrangement contiguity

Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." We formalize these structural properties as constraints on V-position sets within each subspace, extending the arrangement invariants established above.

Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**D-CTG — VContiguity (DESIGN).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are the finitely many [S, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction: all positions in V_S(d) must share components 2 through m − 1.

*Proof.* Suppose for contradiction that V_S(d) contains two positions v₁ < v₂ (both depth m by S8-depth) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j, and (v₁)ⱼ < (v₂)ⱼ (since v₁ < v₂ by T1(i)). For any natural number n > (v₁)ⱼ₊₁, define w of length m by:

- wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j (agreeing with v₁ on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (if any such positions exist).

Then w has subspace S (since w₁ = (v₁)₁ = S) and depth m. We verify v₁ < w < v₂:

- **w > v₁**: w agrees with v₁ on components 1 through j. At component j + 1, n > (v₁)ⱼ₊₁. By T1(i), w > v₁.
- **w < v₂**: w agrees with v₂ on components 1 through j − 1 (since v₁ and v₂ agree there). At component j, wⱼ = (v₁)ⱼ < (v₂)ⱼ. By T1(i), w < v₂.

By D-CTG, every such w belongs to V_S(d). By T0(a), unboundedly many values of n exist, yielding infinitely many distinct positions in V_S(d) — contradicting S8-fin. ∎

This applies uniformly to all depths m ≥ 3 and all divergence points j ∈ {2, …, m − 1}. At depth m = 3, the only possible pre-last divergence is j = 2. For illustration: suppose V_S(d) contained [S, 1, 5] and [S, 2, 1]. Setting j = 2, for any n > 5, w = [S, 1, n] satisfies [S, 1, 5] < [S, 1, n] < [S, 2, 1], so D-CTG forces [S, 1, 6], [S, 1, 7], ... into V_S(d) — infinitely many, contradicting S8-fin. At depth m = 4, divergence could occur at j = 2 or j = 3; the same construction applies in each case.

**D-CTG-depth — SharedPrefixReduction (COROLLARY; from D-CTG, S8-fin, S8-depth, T0(a), T1 (ASN-0034)).** For depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

**D-MIN — VMinimumPosition (DESIGN).** For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

At depth 2 this gives min(V_S(d)) = [S, 1]. Combined with D-CTG and S8-fin, a document with n elements in subspace S occupies V-positions [S, 1] through [S, n] — matching Nelson's "addresses 1 through 100."

We now derive the general form. By D-CTG-depth (when m ≥ 3) or trivially (when m = 2, there is only one post-subspace component), all positions in V_S(d) share components 2 through m − 1. By D-MIN, min(V_S(d)) = [S, 1, …, 1], so those shared components have value 1. Every position is therefore [S, 1, …, 1, k] for varying k. D-CTG restricted to the last component forbids gaps among the k values; D-MIN gives the minimum k = 1; S8-fin bounds the maximum at some finite n. Thus:

**D-SEQ — SequentialPositions (COROLLARY; from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth).** For each document d and subspace S, if V_S(d) is non-empty then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m (the common V-position depth in subspace S). At depth 2 this gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}, matching Nelson's "addresses 1 through n."

D-CTG is a design constraint on well-formed document states. It constrains which arrangement modifications constitute well-formed editing operations. We verify the base case: before any operations, dom(M(d)) = ∅ for all d (the arrangement is a partial function; no content has been allocated, so no V-mapping exists), so V_S(d) = ∅ for every subspace S. D-CTG holds vacuously (no u, q exist to trigger its antecedent), and D-MIN holds vacuously (its antecedent requires V_S(d) non-empty). Observe that not all arrangement modifications preserve D-CTG: removing a single interior V-position from dom(M(d)) leaves the positions on either side no longer contiguous. D-CTG is therefore preserved only by those modifications that constitute well-formed editing operations — operations that restore contiguity after structural changes (e.g., by shifting subsequent positions).

Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN.

### Concrete example

Consider document d at depth 2 in the text subspace (S = 1), with arrangement:

M(d) = {[1,1] ↦ a₁,  [1,2] ↦ a₂,  [1,3] ↦ a₃}

Then V₁(d) = {[1,1], [1,2], [1,3]}.

**D-CTG check.** The extremes are [1,1] and [1,3]. The only intermediate with subspace 1 and depth 2 between them is [1,2], which is in V₁(d). For the adjacent pairs — ([1,1],[1,2]) and ([1,2],[1,3]) — there are no intermediates. D-CTG is satisfied. ✓

**D-MIN check.** min(V₁(d)) = [1,1], whose last component is 1. ✓

**Violation.** Suppose we removed [1,2], yielding V₁(d) = {[1,1], [1,3]}. Now [1,2] is an intermediate between [1,1] and [1,3] that is absent from V₁(d) — D-CTG is violated. This illustrates why removing a single interior V-position is not a well-formed editing operation on its own; a well-formed deletion must also shift subsequent positions to restore contiguity.

Now consider depth 3. Let document d' have arrangement:

M(d') = {[1,1,1] ↦ a₁,  [1,1,2] ↦ a₂,  [1,1,3] ↦ a₃}

Then V₁(d') = {[1,1,1], [1,1,2], [1,1,3]}.

**D-CTG check.** The extremes are [1,1,1] and [1,1,3]. The only intermediate at subspace 1 and depth 3 between them is [1,1,2], which is in V₁(d'). ✓

**D-MIN check.** min(V₁(d')) = [1,1,1] = [S, 1, 1], with all post-subspace components equal to 1. ✓

**Violation (depth ≥ 3).** Suppose instead V₁(d') = {[1,1,1], [1,2,1]}. D-CTG requires every intermediate with subspace 1 and depth 3 between [1,1,1] and [1,2,1] to be present. But [1,1,2], [1,1,3], [1,1,4], ... are all intermediates — infinitely many, contradicting S8-fin. This is D-CTG-depth in action: positions differing before the last component cannot coexist in a finite arrangement.


## Valid insertion position

We work with the arrangement M(d) and the contiguity constraint D-CTG from above. Write V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the V-positions in subspace S of document d.

When V_S(d) is contiguous with |V_S(d)| = N positions, we write its elements as v₀, v₁, ..., v_{N−1} where v₀ is the minimum (D-MIN) and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ).

**ValidInsertionPosition** — *ValidInsertionPosition* (DEF, predicate). A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2, since the first position placed in any subspace is established by the empty case, which requires m ≥ 2, and S8-depth preserves depth thereafter. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. The lower bound m ≥ 2 is necessary: at m = 1, v = [S] and shift([S], 1) = [S] ⊕ δ(1, 1) = [S] ⊕ [1]; the action point of [1] is k = 1, so TumblerAdd gives r₁ = S + 1, producing [S + 1] — a position in subspace S + 1, not S. For m ≥ 2, δ(n, m) has action point m, and since m > 1, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier. This is the canonical minimum position required by D-MIN. The choice of m is a one-time structural commitment: once any position is placed, S8-depth fixes the depth for all subsequent positions in the subspace.

In both cases, S = v₁ is the subspace identifier.

In the non-empty case, there are exactly N + 1 valid insertion positions: the N positions coinciding with existing V-positions v₀ through v_{N−1}, plus the append position shift(min(V_S(d)), N). In the empty case, there is one valid position per choice of depth m — but since m is chosen once and then held fixed by S8-depth, exactly one position is valid for any given depth.

We verify the structural claims. By D-MIN, min(V_S(d)) = [S, 1, ..., 1] of depth m. By OrdinalShift and TumblerAdd, shift([S, 1, ..., 1], j) = [S, 1, ..., 1] ⊕ δ(j, m); since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1 unchanged and sets the last component to 1 + j. The explicit form is shift(min(V_S(d)), j) = [S, 1, ..., 1 + j].

*Distinctness.* The N + 1 positions have last components 1 (for j = 0, where v = min(V_S(d))), 2, 3, ..., N + 1 (for j = 1, ..., N). These are pairwise distinct natural numbers, so by T3 (CanonicalRepresentation, ASN-0034) the N + 1 tumblers are pairwise distinct.

*Depth preservation.* For j ≥ 1, #shift(v, j) = #v = m by the result-length identity of OrdinalShift (ASN-0034). For j = 0, #v = #min(V_S(d)) = m by D-MIN. In the empty case, #v = m by construction. All valid positions have the common V-position depth required by S8-depth.

*Subspace identity.* Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged: shift(min, j)₁ = min₁ = S for all j ≥ 1. For j = 0, v₁ = min₁ = S directly.

*S8a consistency.* For text-subspace positions (S ≥ 1), every valid position [S, 1, ..., 1 + j] has all components strictly positive (S ≥ 1, intermediate components are 1, last component is 1 + j ≥ 1), so zeros(v) = 0 and v > 0 — satisfying S8a.

### Valid insertion position examples

**Non-empty case.** Let subspace S = 1 and suppose V₁(d) = {[1, 1], [1, 2], [1, 3]}, so N = 3 and min(V₁(d)) = [1, 1]. The valid insertion positions are:

- j = 0: v = min(V₁(d)) = [1, 1]
- j = 1: v = shift([1, 1], 1) = [1, 2]
- j = 2: v = shift([1, 1], 2) = [1, 3]
- j = 3: v = shift([1, 1], 3) = [1, 4]

That gives N + 1 = 4 positions. After an operation places new content at, say, [1, 2] — with whatever displacement mechanism the operation defines — the resulting V₁(d) must satisfy D-CTG and D-MIN. Verifying this is the operation's obligation, not the predicate's.

**Empty case.** V₁(d) = ∅. Choosing depth m = 2, the valid insertion position is [1, 1]. D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands. Choosing m = 3 instead would give [1, 1, 1]; by T3, this is a different tumbler — once chosen, S8-depth locks the subspace to depth 3 for all future positions.


## The separation theorem

We can now state the property that Nelson calls "the architectural foundation of everything" as a theorem rather than an axiom.

**S9 (Two-stream separation).** No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S0 guarantees that `a ∈ dom(Σ.C)` implies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every state transition `Σ → Σ'`, unconditionally. The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement. ∎

S9 is the formal statement of Nelson's claim: "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." It says: the two state components are coupled only through S3 (referential integrity). Arrangements depend on the content store — S3 requires every V-reference to resolve — but the content store is independent of all arrangements. This is a one-way dependency:

```
C ← M(d₁), M(d₂), M(d₃), ...
```

Changes to any `M(d)` cannot break `C`. But changes to `C` could break `M` — which is precisely why `C` is immutable. S0 (content immutability) is the mechanism; S9 (two-stream separation) is the consequence.

The asymmetry is deliberate and load-bearing. Nelson enumerates the guarantees that depend on it: link survivability (links point to I-addresses, which S0 preserves), version reconstruction (historical states are assembled from Istream fragments, which S0 preserves), transclusion integrity (transcluded content maintains its value because S0 prevents mutation), and origin traceability (I-addresses encode provenance permanently because S0 prevents reassignment).

Gregory's implementation confirms the separation operationally. Every editing command in the FEBE protocol works exclusively on arrangement state. Of the editing commands Nelson specifies, none modifies existing Istream content. Commands that create content (INSERT, APPEND) extend `dom(C)` with fresh addresses and simultaneously update some `M(d)`. Commands that modify arrangement (DELETE, REARRANGE, COPY) touch only `M(d)`, leaving `C` untouched. No command crosses the boundary in the dangerous direction — no arrangement operation can corrupt stored content.


## Worked example

We instantiate the state model with specific tumblers to ground the abstractions. Consider two documents: document `d₁` at tumbler `1.0.1.0.1` and document `d₂` at tumbler `1.0.1.0.2`. The user creates `d₁` with the text "hello" (five characters), then creates `d₂` which transcludes three characters ("llo") from `d₁` and appends two new characters ("ws").

**Initial state Σ₀**: empty. `dom(C) = ∅`, `dom(M(d₁)) = dom(M(d₂)) = ∅`.

**After creating d₁ with "hello"** — state Σ₁. Five I-addresses are allocated under `d₁`'s prefix, with element-level tumblers (`zeros = 3`):

| I-address `a` | `C(a)` |
|---|---|
| `1.0.1.0.1.0.1.1` | 'h' |
| `1.0.1.0.1.0.1.2` | 'e' |
| `1.0.1.0.1.0.1.3` | 'l' |
| `1.0.1.0.1.0.1.4` | 'l' |
| `1.0.1.0.1.0.1.5` | 'o' |

The arrangement `M(d₁)` maps V-positions (in subspace 1, text) to these I-addresses:

| V-position `v` | `M(d₁)(v)` |
|---|---|
| `1.1` | `1.0.1.0.1.0.1.1` |
| `1.2` | `1.0.1.0.1.0.1.2` |
| `1.3` | `1.0.1.0.1.0.1.3` |
| `1.4` | `1.0.1.0.1.0.1.4` |
| `1.5` | `1.0.1.0.1.0.1.5` |

*Check S0*: no prior content existed, so the implication holds vacuously. *Check S3*: every V-reference resolves — `ran(M(d₁)) ⊆ dom(C)`. *Check S7*: for `a = 1.0.1.0.1.0.1.3`, `origin(a) = 1.0.1.0.1 = d₁` — the document-level prefix directly identifies the allocating document. *Check S8*: the arrangement decomposes into a single correspondence run `(1.1, 1.0.1.0.1.0.1.1, 5)`. Verify: `M(d₁)(1.1 + k) = 1.0.1.0.1.0.1.1 + k` for `k = 0, 1, 2, 3, 4`. One run — the five characters were typed sequentially, receiving consecutive I-addresses by T10a (allocator discipline). *Check D-SEQ*: V₁(d₁) = {[1, k] : 1 ≤ k ≤ 5}, satisfying D-SEQ with n = 5. D-CTG holds (no gaps in the ordinal range 1..5) and D-MIN holds (min = [1, 1]).

**After creating d₂ with transclusion + append** — state Σ₂. The transclusion of "llo" from `d₁` shares the original I-addresses. The append of "ws" allocates two new I-addresses under `d₂`'s prefix:

| I-address `a` | `C(a)` |
|---|---|
| `1.0.1.0.2.0.1.1` | 'w' |
| `1.0.1.0.2.0.1.2` | 's' |

The content store now has 7 entries (5 from `d₁`, 2 new from `d₂`).

The arrangement `M(d₂)`:

| V-position `v` | `M(d₂)(v)` | origin |
|---|---|---|
| `1.1` | `1.0.1.0.1.0.1.3` | `d₁` (transcluded 'l') |
| `1.2` | `1.0.1.0.1.0.1.4` | `d₁` (transcluded 'l') |
| `1.3` | `1.0.1.0.1.0.1.5` | `d₁` (transcluded 'o') |
| `1.4` | `1.0.1.0.2.0.1.1` | `d₂` (native 'w') |
| `1.5` | `1.0.1.0.2.0.1.2` | `d₂` (native 's') |

*Check S0*: all 5 prior entries in `dom(C)` remain with unchanged values. The transition added 2 new entries. *Check S3*: every V-reference in `M(d₂)` resolves — positions `1.1`–`1.3` reference I-addresses from `d₁` (which exist by S1), positions `1.4`–`1.5` reference the newly allocated addresses. *Check S7*: for `a = 1.0.1.0.1.0.1.4` (the second 'l' in `d₂`), `origin(a) = 1.0.1.0.1 = d₁` — attribution traces to the originating document, not to `d₂` where the content currently appears. *Check S5*: the I-address `1.0.1.0.1.0.1.3` now appears in both `ran(M(d₁))` and `ran(M(d₂))` — sharing multiplicity is 2. *Check S8*: `M(d₂)` decomposes into two correspondence runs: `(1.1, 1.0.1.0.1.0.1.3, 3)` for the transclusion, and `(1.4, 1.0.1.0.2.0.1.1, 2)` for the native content. Two runs partition the five V-positions exactly. *Check D-SEQ*: V₁(d₁) is unchanged — {[1, k] : 1 ≤ k ≤ 5}, D-SEQ with n = 5. V₁(d₂) = {[1, k] : 1 ≤ k ≤ 5}, D-SEQ with n = 5. Both satisfy D-CTG and D-MIN.

**After deleting "llo" from d₁** — state Σ₃. DELETE removes V-positions `1.3`–`1.5` from `M(d₁)`:

| V-position `v` | `M(d₁)(v)` |
|---|---|
| `1.1` | `1.0.1.0.1.0.1.1` |
| `1.2` | `1.0.1.0.1.0.1.2` |

*Check S0*: all 7 entries in `dom(C)` remain. The I-addresses `1.0.1.0.1.0.1.3`–`.5` are no longer in `ran(M(d₁))` but persist in `dom(C)`. *Check S6*: these three addresses are now "orphaned" from `d₁`'s perspective, but still referenced by `M(d₂)` — persistence is unconditional. *Check S9*: the deletion modified `M(d₁)` but `C` is unchanged — separation holds. *Check S8*: `M(d₁)` is now a single run `(1.1, 1.0.1.0.1.0.1.1, 2)`. The prior 1-run decomposition became a 1-run decomposition (the deletion removed an entire suffix, not a middle segment). `M(d₂)` is unchanged — still two runs. *Check D-SEQ*: V₁(d₁) = {[1, k] : 1 ≤ k ≤ 2}, D-SEQ with n = 2. D-CTG holds (no gaps in 1..2) and D-MIN holds (min = [1, 1]). V₁(d₂) is unchanged — D-SEQ with n = 5.


## The document as arrangement

One consequence of the two-stream model deserves explicit statement. A document is not its content — it is its arrangement of content.

Two documents `d₁ ≠ d₂` may render identically — displaying the same text in the same order — because their arrangements happen to map to the same I-addresses in the same sequence: `(A v ∈ dom(M(d₁)) :: M(d₁)(v) = M(d₂)(v))`. Yet they remain distinct documents with independent arrangements, independent ownership, and independent edit histories. Conversely, a single document's arrangement changes across versions while the underlying Istream content is unchanged — different mappings over the same stored material.

Nelson: "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." The document is, in his metaphor, "an evolving ongoing braid." The braid is the arrangement; the strands are the Istream content. The braid is re-twisted when parts are rearranged, added, or subtracted — but the strands remain intact.

This has a formal consequence: document equality is not decidable by content comparison. You cannot determine whether two documents are "the same" by comparing their rendered output — the same output can arise from different arrangements of different I-addresses that happen to carry identical values. Identity requires comparing document identifiers (tumblers, per T3) or arrangement functions, not rendered content.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.C | Content store: `T ⇀ Val`, mapping I-addresses to content values | introduced |
| Σ.M(d) | Arrangement for document `d`: `T ⇀ T`, mapping V-positions to I-addresses | introduced |
| S0 | Content immutability: `a ∈ dom(C) ⟹ a ∈ dom(C') ∧ C'(a) = C(a)` for all transitions | introduced |
| S1 | Store monotonicity: `dom(C) ⊆ dom(C')` for all transitions | corollary of S0 |
| S2 | Arrangement functionality: `M(d)` is a function — each V-position maps to exactly one I-address | introduced |
| S3 | Referential integrity: `(A d, v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C))` | introduced |
| S4 | Origin-based identity: distinct allocations produce distinct I-addresses regardless of value equality | from T9, T10, T10a, TA5, T3 (ASN-0034) |
| S5 | Unrestricted sharing: S0–S3 do not entail any finite bound on sharing multiplicity | consistent with S0–S3 (witness construction) |
| S6 | Persistence independence: `a ∈ dom(C)` is unconditional — independent of all arrangements | corollary of S0 |
| S7a | Document-scoped allocation: every I-address is allocated under the originating document's prefix | introduced |
| S7b | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | introduced |
| S7 | Structural attribution: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — full document prefix | from S7a, S7b, T4, T9, T10, T10a, TA5, T3 (ASN-0034) |
| S8-fin | Finite arrangement: `dom(M(d))` is finite for every document `d` | introduced |
| S8a | V-position well-formedness: `(A v ∈ dom(M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)`; link subspace deferred | introduced |
| S8-depth | Fixed-depth V-positions: `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` | design requirement |
| S8 | Span decomposition (text subspace): `{(v, M(d)(v)) : v₁ ≥ 1}` decomposes into finitely many correspondence runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(vⱼ + k) = aⱼ + k` for `0 ≤ k < nⱼ` | theorem from S8-fin, S8a, S2, S8-depth, T1, T5, T10, TA5(c), TA7a (ASN-0034) |
| D-CTG | V-position contiguity: within each subspace, V-positions form a contiguous ordinal range with no gaps — design constraint on well-formed document states | introduced |
| D-MIN | V-position minimum: minimum V-position in each non-empty subspace has all post-subspace components equal to 1 — design constraint | introduced |
| D-CTG-depth | Shared prefix reduction: at depth m ≥ 3, contiguity reduces to the last component (all positions share components 2 through m − 1) | corollary from D-CTG, S8-fin, S8-depth, T0(a), T1 (ASN-0034) |
| D-SEQ | Sequential positions: non-empty V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 | corollary from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth |
| ValidInsertionPosition | if V_S(d) ≠ ∅: v = min(V_S(d)) or v = shift(min(V_S(d)), j) with 1 ≤ j ≤ N, common depth m ≥ 2; if V_S(d) = ∅: v = [S, 1, ..., 1] of depth m ≥ 2 | introduced |
| S9 | Two-stream separation: arrangement changes cannot alter stored content | theorem from S0 |


## Open Questions

What constraints must the content store's value domain `Val` satisfy — must all entries be uniform in type, or must `Val` support heterogeneous content (text, links, media) as first-class distinctions?

Must the span decomposition of an arrangement have a unique maximal form (fewest possible runs), or can multiple valid decompositions of different cardinality coexist for the same arrangement?

What must the system guarantee about the computability of the sharing inverse — given an I-address, what is the cost bound for determining which documents currently reference it?

Under what conditions, if any, may the referential integrity invariant S3 be temporarily violated — must it hold at every observable state, or only at quiescent states between operations?

What abstract property distinguishes content that exists but is unreachable from all current arrangements from content that exists and is reachable — and must the system maintain this distinction as queryable state?

Under what conditions do operations guarantee non-trivial correspondence runs (length > 1) — must sequential content creation produce a single run, or is the singleton decomposition the only structure guaranteed without operation-level constraints?

Does each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) preserve D-CTG and D-MIN?

What invariants must the displacement mechanism satisfy so that insertion at a ValidInsertionPosition preserves D-CTG, D-MIN, and S2?

Under what conditions does the choice of initial depth m for an empty subspace affect the expressiveness of subsequent arrangements?

What must an operation guarantee about existing V-to-I mappings when it inserts at a position that coincides with an occupied V-position?
