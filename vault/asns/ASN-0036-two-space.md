# ASN-0036: Two Space

*2026-03-14*

We wish to understand what formal invariants govern the relationship between permanent content storage and mutable document arrangement in Xanadu. Nelson separated these concerns into two address spaces — I-space for content identity and V-space for document positions — and asserted this separation as the architectural foundation on which permanence, transclusion, and attribution all rest. We seek the abstract properties that define this separation: what must hold in any correct implementation, regardless of the underlying data structures.

The approach is: model the system as two state components, derive what each must guarantee independently, then identify the invariants connecting them. Nelson provides architectural intent; Gregory's implementation reveals which properties are load-bearing.

Nelson conceived the two spaces as inseparable aspects of a single architecture. Gregory implemented them as distinct enfilade types with different stability characteristics. Between these two accounts we find the abstract structure: a content store that grows but never changes, and a family of arrangement functions that change freely but may reference only what the store contains.


## Two components of state

The observation that motivates the entire design is that content EXISTS independently of how it is ARRANGED. A paragraph does not cease to exist when removed from a document — it merely ceases to appear there. Nelson states this plainly:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

This observation forces the state into two components:

**Σ.C : T ⇀ Val** — the *content store*. A partial function mapping I-space addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

**Σ.M(d) : T ⇀ T** — the *arrangement* of document `d`. A partial function mapping V-space positions to I-space addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

A conventional system merges these — "the file" IS the content IS the arrangement. Editing overwrites. Saving destroys the prior state. Nelson rejected this explicitly: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." The two-component model is his alternative: editing modifies `M(d)` while `C` remains invariant. The separation is the premise; what follows are the invariants it must satisfy.


## The content store

We ask: what must `C` guarantee? Nelson requires that any historical version be reconstructable, that content transcluded across documents maintain its meaning, and that attribution be permanent. Working backward from these guarantees — what must `C` satisfy for them to hold?

Suppose `C(a)` could change from value `w` to `w'` in some state transition. Then every document whose arrangement maps a V-position to `a` would silently show different content — with no editing operation having touched any arrangement. Historical versions, which reconstruct their state by reassembling I-space fragments, would silently present altered text. Content transcluded from one document into another would mutate without the including document's knowledge or consent. Nelson: "Users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." Mutation of `C(a)` damages every original that contains `a`.

We therefore require:

**S0 (Content immutability).** For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

Once content is stored at address `a`, both the address and its value are fixed for all future states. This is the central invariant of the two-space architecture.

S0 is a strong property. It asserts two things simultaneously: that `a` remains in the domain (the address persists), and that the value at `a` is unchanged (the content is immutable). In weakest-precondition terms, for any operation producing successor state `Σ'`:

`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))`

must hold in every reachable state. This constrains every operation to either leave `C(a)` unchanged or to operate only on addresses not yet in `dom(C)` — that is, to create new content at fresh addresses.

**S1 (Store monotonicity).** `[dom(Σ.C) ⊆ dom(Σ'.C)]`

S1 is a corollary of S0, stated separately for emphasis. It is the content-store specialisation of T8 (allocation permanence, ASN-0034): T8 guarantees that allocated addresses persist in the abstract address space; S1 ensures that the content at those addresses persists as well.

S0 and S1 together establish `C` as an *append-only log*. New entries may be added — each at a fresh address guaranteed unique by GlobalUniqueness (ASN-0034) — but no existing entry may be modified or removed.

Nelson states this as an explicit design commitment: "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." Gregory's implementation confirms the commitment. Of the seventeen FEBE commands Nelson specifies, none modifies existing I-space content. There is no MODIFY, UPDATE, or REPLACE operation. The absence is structural — the protocol provides no mechanism for mutating stored content.

Gregory's evidence reveals an instructive footnote. The implementation carries a `refcount` field annotated "for subtree sharing, disk garbage collecting." Functions for reference-counted deletion exist: `deletefullcrumandgarbageddescendents()` and `deletewithgarbageddescendents()`. But the actual reclamation call was commented out on a specific date: `/*subtreefree(ptr);*/ /*12/04/86*/`. The machinery was built, dated December 4, 1986, and deliberately deactivated. S0 and S1 are upheld not by architectural impossibility but by a design choice so consistent that four decades of continuous operation have never violated it.


## The arrangement and referential integrity

V-space is where mutability lives. Each document's arrangement `M(d)` maps V-positions to I-addresses, presenting stored content as a readable sequence. Unlike `C`, arrangements change freely — content can be added, removed, and reordered.

**S2 (Arrangement functionality).** For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

This is inherent in the concept of a "virtual byte stream." Nelson: "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." Each position in the stream shows exactly one piece of content. A V-position cannot simultaneously contain two different things.

We note the phrase "regardless of their native origin." A document's V-space presents content as a seamless sequence even when the I-addresses are scattered across multiple documents' I-spaces. The arrangement function is what makes heterogeneous I-space origins appear as a uniform V-space stream.

The bridge between the two state components is a well-formedness condition:

**S3 (Referential integrity).** `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Every V-reference resolves. If a document's arrangement says "at position `v`, display the content at I-address `a`," then `a` must be in `dom(C)`. There are no dangling references.

The maintenance of S3 across state transitions reveals a temporal ordering constraint. The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

The target I-address must already be in `dom(C)` before the arrangement can reference it. S1 then guarantees that once `a` enters `dom(C)`, it remains — so a valid reference cannot become dangling through any subsequent state transition. The temporal order is: content enters `C` first, then `M(d)` may reference it.

We observe a deliberate asymmetry. S3 says arrangement implies existence: `ran(M(d)) ⊆ dom(C)`. It does NOT say existence implies arrangement. Content can exist in I-space without being arranged in any current document. Nelson calls such content "deleted bytes — not currently addressable, awaiting historical backtrack functions, may remain included in other versions." The asymmetry is the space in which persistence independence lives.


## Content identity

What distinguishes transclusion from coincidence? In conventional systems, identity is by value — two files with identical bytes are "the same." In Xanadu, identity is by address.

**S4 (Origin-based identity).** For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`. Two independent writings of the word "hello" produce distinct I-addresses. A transclusion of existing content shares the original I-address.

S4 follows from GlobalUniqueness (ASN-0034), which guarantees that no two distinct allocations — whether from the same allocator or different allocators, whether simultaneous or separated by years — produce the same address. The two-space architecture exploits this guarantee: when `Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂)` for documents `d₁ ≠ d₂`, the system knows this is transclusion — shared content with a common origin — not coincidental value equality. The structural test for shared identity is address equality, decidable from the addresses alone (T2, ASN-0034) without value comparison.

S4 creates a fundamental asymmetry in the system. The content store `C` is oblivious to values — it does not care whether `C(a₁) = C(a₂)`. But the arrangement family `M` is sensitive to addresses — two arrangements that map to the same I-address share content structurally, while two arrangements that map to different I-addresses with equal values do not. Nelson captures the distinction:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage... Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Live content shares I-addresses. Dead copies create new ones. The difference is structural — computable from the state alone.


## Sharing

The arrangement function `M(d)` need not be injective. This is not a deficiency but a design requirement — it is what makes transclusion work.

**S5 (Unrestricted sharing).** The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. The invariants S0–S3 impose no finite upper bound on sharing multiplicity — S0–S3 do not entail any finite bound on sharing:

`¬(E N ∈ ℕ :: S0–S3 ⊢ (A Σ reachable, a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| ≤ N))`

We note that in any particular state, the sharing multiplicity of each address is a definite finite number — possibly zero for orphaned content (S6). The property is an architectural anti-constraint: the invariants place no finite cap on how many references may accumulate.

Nelson: "The virtual byte stream of a document may include bytes from any other document." And: "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely." Transclusion is recursive and unlimited.

Gregory confirms the unbounded nature at the implementation level. The global index that records which documents reference which I-addresses accumulates entries without cap — "no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism anywhere in the code path." Each referential inclusion adds one entry. The only constraints are physical resources (memory and disk), not architectural limits.

The combination of S4 and S5 gives the system its distinctive character. S4 says identity is structural — determined by I-address, not by value. S5 says sharing is unlimited — any number of documents can reference the same content. Together they establish a regime in which quotation is a first-class structural relationship: any number of documents can quote the same passage, and the system knows they are all quoting — not independently writing — because they share I-addresses.

We observe that the state `Σ = (C, M)` makes the sharing relation computable: given any `a ∈ dom(C)`, the set `{d : (E v :: M(d)(v) = a)}` is determined by the state. Nelson requires this to be queryable: "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." The state model supports this — the information is present; only the efficiency of its extraction is an implementation concern.


## Persistence independence

Content persists in I-space regardless of whether any arrangement references it.

**S6 (Persistence independence).** The membership of `a` in `dom(Σ.C)` is independent of all arrangements:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

S6 is a consequence of S0, which guarantees domain persistence unconditionally — it does not condition on whether any arrangement references `a`. But we state S6 separately because it names a design commitment that S0's formulation does not emphasise: the decision NOT to garbage-collect unreferenced content.

A system could satisfy a weakened form of S0 that permits removal when `(A d :: a ∉ ran(M(d)))` — when no arrangement references the content. Nelson explicitly rejects this. "Deleted bytes" are described as "not currently addressable, awaiting historical backtrack functions." The content remains because history requires it. Version reconstruction depends on the availability of I-space fragments from prior arrangements. If content were reclaimed when its last current reference vanished, the system could not fulfill: "When you ask for a given part of a given version at a given time, it comes to your screen."

S6 creates what Gregory calls an "orphan" phenomenon. Content in `dom(C)` that is not in `ran(M(d))` for any current document `d` is *unreachable through any query that starts from V-space*. Gregory's evidence is definitive: "There is no mechanism to discover them, and the architecture makes no provision for it." The system provides no I-space iterator, no allocation registry queryable for "all content ever stored." To retrieve orphaned content, you must already know its I-address.

This is not a deficiency but a structural consequence of the two-space model. The system's query interface is V-space-primary: you start from a document (a V-space entity), look up content (through the arrangement), and follow references (through I-space addresses). There is no path that begins in I-space and discovers content without a V-space entry point. Orphaned content is permanent but practically invisible — a kind of information-theoretic dark matter, present by guarantee but unobservable through the system's own instruments.


## Structural attribution

Every V-position can be traced to the document that originally created its content.

S7 requires an architectural premise that T4 alone does not supply. T4 tells us HOW to parse a tumbler into fields; it does not tell us that I-space addresses are allocated under the originating document's tumbler prefix. We state this premise explicitly:

**S7a (Document-scoped allocation).** Every I-space address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

This is a design requirement, not a convention. Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. The address IS the provenance: "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents.

We must also restrict S7's domain. The function `fields(a).document` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: `zeros = 0` is node-only, `zeros = 1` is node+user, `zeros ≥ 2` has a document field). Since I-space addresses designate content elements within documents, we require:

**S7b (Element-level I-addresses).** Every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This follows from T4 and the tumbler hierarchy: content is stored at the element level (the fourth and finest level of the address hierarchy). Node, user, and document-level tumblers identify containers, not content.

With S7a and S7b established, we can state structural attribution:

**S7 (Structural attribution).** For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system (by GlobalUniqueness, ASN-0034, which covers all cases: same-allocator monotonicity, non-nesting prefixes, and nesting prefixes distinguished by length). It is not metadata that can be stripped or forged — it IS the address. To retrieve the content, the system must know its I-address; to know its I-address is to know its origin.

S7 follows from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), and T4 (field parsing, ASN-0034). Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

We note a subtlety. S7 identifies the document that ALLOCATED the I-address — the document where the content was first created. This is distinct from the document where the content currently appears. When content is transcluded from document B into document A, the reader viewing A sees the content, but S7 traces it to B. The distinction between "where I am reading" (V-space context, document A) and "where this came from" (I-space structure, document B) is precisely the two-space separation made visible.

Gregory's implementation reveals two mechanisms for origin lookup. The I-address prefix itself encodes the originating document (used during address allocation to scope the search range). Separately, each arrangement entry carries an explicit `homedoc` field recording the allocating document (used during retrieval). At the abstract level, S7 says only that the information is present in the address — it does not prescribe how an implementation extracts it.


## Span decomposition

The arrangement `M(d)` maps individual V-positions to I-addresses. But the mapping has internal structure: contiguous V-ranges often correspond to contiguous I-ranges. This is what makes finite representation possible.

Before defining correspondence runs, we must establish the structure of `dom(M(d))` more carefully.

**S8-fin (Finite arrangement).** For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

S8-fin follows from the operational reality: each V-position enters `dom(M(d))` through a specific operation (INSERT, COPY, etc.), and the system has performed only finitely many operations. No operation introduces infinitely many V-positions.

**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth. Gregory's evidence is conclusive: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: position `s.x` is followed by `s.(x+1)`. Similarly, I-addresses within a single document and subspace share a common prefix and differ only at the element ordinal (the last component of the element field). Per TA7a (ASN-0034), ordinal displacement within a fixed-depth subspace reduces to natural-number addition on the ordinal component, with the structural prefix held as context. We write `v + k` for this operation applied to V-positions, and `a + k` for the same applied to the element ordinal of I-addresses.

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a` — no displacement, no arithmetic. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount. Within a correspondence run, each step forward in V-space corresponds to the same step forward in I-space.

**S8 (Finite span decomposition).** For each document `d`, the arrangement `Σ.M(d)` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition `dom(M(d))`: every V-position in `dom(M(d))` falls in exactly one run — `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run: `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

Each run represents a contiguous block of content that entered the arrangement as a unit — characters typed sequentially, or a span transcluded whole.

The decomposition always exists. By S8-fin, `dom(M(d))` is finite. For the degenerate case: each V-position `v` with `M(d)(v) = a` forms a singleton run `(v, a, 1)`. At `k = 0`: `M(d)(v + 0) = M(d)(v) = a = a + 0` — the base case holds trivially. The singleton runs partition `dom(M(d))` — each position falls in exactly one run. Since `dom(M(d))` is finite, the set of singleton runs is finite.

What matters architecturally is that the number of runs `#runs(d)` is typically far smaller than `|dom(M(d))|` — the representation cost is proportional to the number of editing events, not the document size.

S8 follows from the finiteness of `dom(M(d))` (S8-fin) and the structure of tumbler arithmetic. Forward allocation (T9, ASN-0034) ensures that consecutively created content receives consecutive I-addresses, producing natural correspondence runs. Editing can both split and remove runs — inserting content in the middle of a run splits it into two, while deleting an entire run's V-span removes it. The number of distinct I-space allocation events underlying a document's history is monotonically non-decreasing (by S1), but the current arrangement's run count fluctuates with editing.

Gregory's evidence shows that `#runs(d)` has consequences beyond representation cost. Each correspondence run requires an independent tree traversal during V↔I translation. Gregory identifies the inner loop of this traversal as the documented CPU hotspot, responsible for 40% of processing time. For a document with `N` runs, a full V→I conversion requires `N` independent traversals — the cost is multiplicative in the fragmentation level, not merely additive. A consolidation function to merge adjacent runs was started in the implementation and abandoned mid-expression — the function body stops with an incomplete conditional: `if(`. Any implementation of the two-space architecture must either consolidate runs or accept performance proportional to fragmentation level.


## The separation theorem

We can now state the property that Nelson calls "the architectural foundation of everything" as a theorem rather than an axiom.

**S9 (Two-space separation).** No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S0 guarantees that `a ∈ dom(Σ.C)` implies `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every state transition `Σ → Σ'`, unconditionally. The consequent of S9 is a special case of S0's universal guarantee, restricted to transitions that modify some arrangement. ∎

S9 is the formal statement of Nelson's claim: "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." It says: the two state components are coupled only through S3 (referential integrity). Arrangements depend on the content store — S3 requires every V-reference to resolve — but the content store is independent of all arrangements. This is a one-way dependency:

```
C ← M(d₁), M(d₂), M(d₃), ...
```

Changes to any `M(d)` cannot break `C`. But changes to `C` could break `M` — which is precisely why `C` is immutable. S0 (content immutability) is the mechanism; S9 (two-space separation) is the consequence.

The asymmetry is deliberate and load-bearing. Nelson enumerates the guarantees that depend on it: link survivability (links point to I-addresses, which S0 preserves), version reconstruction (historical states are assembled from I-space fragments, which S0 preserves), transclusion integrity (transcluded content maintains its value because S0 prevents mutation), and origin traceability (I-addresses encode provenance permanently because S0 prevents reassignment).

Gregory's implementation confirms the separation operationally. Every editing command in the FEBE protocol works exclusively on arrangement state. Of the editing commands Nelson specifies, none modifies existing I-space content. Commands that create content (INSERT, APPEND) extend `dom(C)` with fresh addresses and simultaneously update some `M(d)`. Commands that modify arrangement (DELETE, REARRANGE, COPY) touch only `M(d)`, leaving `C` untouched. No command crosses the boundary in the dangerous direction — no arrangement operation can corrupt stored content.


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

*Check S0*: no prior content existed, so the implication holds vacuously. *Check S3*: every V-reference resolves — `ran(M(d₁)) ⊆ dom(C)`. *Check S7*: for `a = 1.0.1.0.1.0.1.3`, `origin(a) = 1.0.1.0.1 = d₁` — the document-level prefix directly identifies the allocating document. *Check S8*: the arrangement decomposes into a single correspondence run `(1.1, 1.0.1.0.1.0.1.1, 5)`. Verify: `M(d₁)(1.1 + k) = 1.0.1.0.1.0.1.1 + k` for `k = 0, 1, 2, 3, 4`. One run — the five characters were typed sequentially, receiving consecutive I-addresses by T9.

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

*Check S0*: all 5 prior entries in `dom(C)` remain with unchanged values. The transition added 2 new entries. *Check S3*: every V-reference in `M(d₂)` resolves — positions `1.1`–`1.3` reference I-addresses from `d₁` (which exist by S1), positions `1.4`–`1.5` reference the newly allocated addresses. *Check S7*: for `a = 1.0.1.0.1.0.1.4` (the second 'l' in `d₂`), `origin(a) = 1.0.1.0.1 = d₁` — attribution traces to the originating document, not to `d₂` where the content currently appears. *Check S5*: the I-address `1.0.1.0.1.0.1.3` now appears in both `ran(M(d₁))` and `ran(M(d₂))` — sharing multiplicity is 2. *Check S8*: `M(d₂)` decomposes into two correspondence runs: `(1.1, 1.0.1.0.1.0.1.3, 3)` for the transclusion, and `(1.4, 1.0.1.0.2.0.1.1, 2)` for the native content. Two runs partition the five V-positions exactly.

**After deleting "llo" from d₁** — state Σ₃. DELETE removes V-positions `1.3`–`1.5` from `M(d₁)`:

| V-position `v` | `M(d₁)(v)` |
|---|---|
| `1.1` | `1.0.1.0.1.0.1.1` |
| `1.2` | `1.0.1.0.1.0.1.2` |

*Check S0*: all 7 entries in `dom(C)` remain. The I-addresses `1.0.1.0.1.0.1.3`–`.5` are no longer in `ran(M(d₁))` but persist in `dom(C)`. *Check S6*: these three addresses are now "orphaned" from `d₁`'s perspective, but still referenced by `M(d₂)` — persistence is unconditional. *Check S9*: the deletion modified `M(d₁)` but `C` is unchanged — separation holds. *Check S8*: `M(d₁)` is now a single run `(1.1, 1.0.1.0.1.0.1.1, 2)`. The prior 1-run decomposition became a 1-run decomposition (the deletion removed an entire suffix, not a middle segment). `M(d₂)` is unchanged — still two runs.


## The document as arrangement

One consequence of the two-space model deserves explicit statement. A document is not its content — it is its arrangement of content.

Two documents `d₁ ≠ d₂` may render identically — displaying the same text in the same order — because their arrangements happen to map to the same I-addresses in the same sequence: `(A v ∈ dom(M(d₁)) :: M(d₁)(v) = M(d₂)(v))`. Yet they remain distinct documents with independent arrangements, independent ownership, and independent edit histories. Conversely, a single document's arrangement changes across versions while the underlying I-space content is unchanged — different mappings over the same stored material.

Nelson: "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." The document is, in his metaphor, "an evolving ongoing braid." The braid is the arrangement; the strands are the I-space content. The braid is re-twisted when parts are rearranged, added, or subtracted — but the strands remain intact.

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
| S4 | Origin-based identity: distinct allocations produce distinct I-addresses regardless of value equality | from GlobalUniqueness (ASN-0034) |
| S5 | Unrestricted sharing: S0–S3 do not entail any finite bound on sharing multiplicity | introduced |
| S6 | Persistence independence: `a ∈ dom(C)` is unconditional — independent of all arrangements | corollary of S0 |
| S7a | Document-scoped allocation: every I-address is allocated under the originating document's prefix | introduced |
| S7b | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | introduced |
| S7 | Structural attribution: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — full document prefix | from S7a, S7b, T4 (ASN-0034) |
| S8-fin | Finite arrangement: `dom(M(d))` is finite for every document `d` | introduced |
| S8-depth | Fixed-depth V-positions: within a subspace, all V-positions share the same tumbler depth | introduced |
| S8 | Span decomposition: `M(d)` decomposes into finitely many correspondence runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(vⱼ + k) = aⱼ + k` for `0 ≤ k < nⱼ` | introduced |
| S9 | Two-space separation: arrangement changes cannot alter stored content | theorem from S0 |


## Open Questions

What constraints must the content store's value domain `Val` satisfy — must all entries be uniform in type, or must `Val` support heterogeneous content (text, links, media) as first-class distinctions?

Must the span decomposition of an arrangement have a unique maximal form (fewest possible runs), or can multiple valid decompositions of different cardinality coexist for the same arrangement?

What must the system guarantee about the computability of the sharing inverse — given an I-address, what is the cost bound for determining which documents currently reference it?

Under what conditions, if any, may the referential integrity invariant S3 be temporarily violated — must it hold at every observable state, or only at quiescent states between operations?

What abstract property distinguishes content that exists but is unreachable from all current arrangements from content that exists and is reachable — and must the system maintain this distinction as queryable state?

Must the arrangement function `M(d)` preserve any relationship between V-space ordering and I-space ordering within a correspondence run, or can the mapping be arbitrarily permuted as long as each V-position maps to exactly one I-address?
