# ASN-0036: Istream and Vstream

*2026-03-14; revised 2026-03-21, 2026-03-22, 2026-03-22, 2026-03-28*

We wish to understand what formal invariants govern the relationship between permanent content storage and mutable document arrangement in Xanadu. Nelson separated these concerns into two address spaces — Istream for content identity and Vstream for document positions — and asserted this separation as the architectural foundation on which permanence, transclusion, and attribution all rest. We seek the abstract properties that define this separation: what must hold in any correct implementation, regardless of the underlying data structures.

The approach is: model the system as two state components, derive what each must guarantee independently, then identify the invariants connecting them. Nelson provides architectural intent; Gregory's implementation reveals which properties are load-bearing.

Nelson conceived the two streams as inseparable aspects of a single architecture. Gregory implemented them as distinct enfilade types with different stability characteristics. Between these two accounts we find the abstract structure: a content store that grows but never changes, and a family of arrangement functions that change freely but may reference only what the store contains.


## Two components of state

The observation that motivates the entire design is that content EXISTS independently of how it is ARRANGED. A paragraph does not cease to exist when removed from a document — it merely ceases to appear there. Nelson states this plainly:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

This observation forces the state into two components:

**Σ.C (ContentStore).** The *content store*: a partial function mapping Istream addresses to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values, opaque at this level of abstraction. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

Σ.C is a definition, not a derived property. We justify the modelling choice. Nelson's architecture requires a mechanism that associates content values with permanent addresses — the Istream. The natural mathematical object is a partial function `C : T ⇀ Val`. It is partial because not every tumbler carries content: only those addresses at which content has been stored belong to `dom(C)`. It maps to `Val` rather than to a specific type because the content store is indifferent to what it stores — text, links, media — at this level of abstraction. The domain `dom(Σ.C)` names the set of addresses at which content exists; all subsequent properties (S0 through S9) constrain how this domain and these values evolve under state transitions. The content store is the first of two state components; the second is the arrangement family Σ.M(d). Together they constitute the complete system state `Σ = (C, M)`. ∎

*Formal Contract:*
- *Axiom:* `Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.
- *Definition:* `dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

**Σ.M(d) (Arrangement).** The *arrangement* of document `d`: a partial function mapping Vstream positions to Istream addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

A conventional system merges these — "the file" IS the content IS the arrangement. Editing overwrites. Saving destroys the prior state. Nelson rejected this explicitly: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." The two-component model is his alternative: editing modifies `M(d)` while `C` remains invariant. The separation is the premise; what follows are the invariants it must satisfy.

Σ.M(d) is a definition, not a derived property. We justify the modelling choice. A document in Nelson's architecture is not a contiguous block of stored content but a structure that *selects from* the content store — specifying which content appears, in what order. The natural mathematical object for this selection is a partial function `M(d) : T ⇀ T`. It maps from V-positions (tumblers addressing locations within the document's virtual stream) to I-addresses (tumblers addressing locations in the content store). It is partial because not every tumbler is an active V-position: only those positions at which `d` currently presents content belong to `dom(M(d))`. The codomain is `T` rather than `Val` because an arrangement does not contain content values directly — it refers to I-addresses where content resides. The content itself is retrieved via `Σ.C`. This indirection is the structural mechanism by which Nelson's two requirements — immutable content and mutable presentation — coexist: editing a document changes which I-addresses its V-positions reference (modifying `M(d)`) without altering what any I-address stores (preserving `Σ.C`). The arrangement is the second of two state components; together with the content store Σ.C, they constitute the complete system state `Σ = (C, M)`. ∎

*Formal Contract:*
- *Axiom:* `Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.
- *Definition:* `dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.
- *Definition:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.

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

*Formal Contract:*
- *Invariant:* `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every transition `Σ → Σ'`
- *Axiom:* imposed as a design constraint on all content-store operations

**S1 (Store monotonicity).** `[dom(Σ.C) ⊆ dom(Σ'.C)]`

S1 is a corollary of S0, stated separately for emphasis. It is the content-store specialisation of T8 (allocation permanence, ASN-0034): T8 guarantees that allocated addresses persist in the abstract address space; S1 ensures that the content at those addresses persists as well.

S0 and S1 together establish `C` as an *append-only log*. New entries may be added — each at a fresh address guaranteed unique by T9 and T10 (ASN-0034) — but no existing entry may be modified or removed.

Nelson states this as an explicit design commitment: "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." Gregory's implementation confirms the commitment. Of the seventeen FEBE commands Nelson specifies, none modifies existing Istream content. There is no MODIFY, UPDATE, or REPLACE operation. The absence is structural — the protocol provides no mechanism for mutating stored content.

Gregory's evidence reveals an instructive footnote. The implementation carries a `refcount` field annotated "for subtree sharing, disk garbage collecting." Functions for reference-counted deletion exist: `deletefullcrumandgarbageddescendents()` and `deletewithgarbageddescendents()`. But the actual reclamation call was commented out on a specific date: `/*subtreefree(ptr);*/ /*12/04/86*/`. The machinery was built, dated December 4, 1986, and deliberately deactivated. S0 and S1 are upheld not by architectural impossibility but by a design choice so consistent that four decades of continuous operation have never violated it.

*Proof.* We wish to show that for every state transition `Σ → Σ'`, `dom(Σ.C) ⊆ dom(Σ'.C)`.

Let `a ∈ dom(Σ.C)` be arbitrary. By S0 (content immutability), `a ∈ dom(Σ.C)` implies the conjunction `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The first conjunct yields `a ∈ dom(Σ'.C)` directly. Since `a` was chosen arbitrarily from `dom(Σ.C)`, we have established `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C))`, which is `dom(Σ.C) ⊆ dom(Σ'.C)` by definition of subset inclusion.

S1 is strictly weaker than S0: it asserts domain persistence without value preservation. We state it separately because it names a distinct architectural commitment — the content store grows monotonically — and because it specialises T8 (allocation permanence, ASN-0034) from the abstract address space to the content store. T8 guarantees `allocated(s) ⊆ allocated(s')` for the address space as a whole; S1 guarantees `dom(Σ.C) ⊆ dom(Σ'.C)` for the content store specifically. The two properties have different scopes: T8 covers addresses that have been allocated but may carry no content, while S1 covers addresses at which content has actually been stored. That `dom(Σ.C)` is a subset of the allocated set means S1 could in principle follow from T8 together with an axiom linking allocation to content storage — but the derivation from S0 is more direct and reveals the logical relationship: domain monotonicity is a consequence of content immutability, not an independent commitment. ∎

*Formal Contract:*
- *Preconditions:* State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Invariant:* `dom(Σ.C) ⊆ dom(Σ'.C)`.


## The arrangement and referential integrity

Vstream is where mutability lives. Each document's arrangement `M(d)` maps V-positions to I-addresses, presenting stored content as a readable sequence. Unlike `C`, arrangements change freely — content can be added, removed, and reordered.

**S2 (Arrangement functionality).** For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

This is inherent in the concept of a "virtual byte stream." Nelson: "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." Each position in the stream shows exactly one piece of content. A V-position cannot simultaneously contain two different things.

We note the phrase "regardless of their native origin." A document's Vstream presents content as a seamless sequence even when the I-addresses are scattered across multiple documents' Istreams. The arrangement function is what makes heterogeneous Istream origins appear as a uniform Vstream stream.

*Formal Contract:*
- *Axiom:* For each document `d`, `Σ.M(d)` is a function — every `v ∈ dom(Σ.M(d))` maps to exactly one I-address.

The bridge between the two state components is a well-formedness condition:

**S3 (Referential integrity).** `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Every V-reference resolves. If a document's arrangement says "at position `v`, display the content at I-address `a`," then `a` must be in `dom(C)`. There are no dangling references.

The maintenance of S3 across state transitions reveals a temporal ordering constraint. The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

For an operation that only adds a V-mapping without creating content, the target I-address must already be in `dom(C)`. An operation that atomically creates content at `a` and adds the mapping `M(d)(v) = a` satisfies S3 in the post-state without sequential precedence — `a ∈ dom(Σ'.C)` and `Σ'.M(d)(v) = a` are established simultaneously. The dependency is logical, not temporal: a reference presupposes the existence of its target, but existence need not precede reference in a prior transition. What matters for persistence is that S1 guarantees once `a` enters `dom(C)`, it remains — so a valid reference cannot become dangling through any subsequent state transition.

We observe a deliberate asymmetry. S3 says arrangement implies existence: `ran(M(d)) ⊆ dom(C)`. It does NOT say existence implies arrangement. Content can exist in Istream without being arranged in any current document. Nelson calls such content "deleted bytes — not currently addressable, awaiting historical backtrack functions, may remain included in other versions." The asymmetry is the space in which persistence independence lives.

*Proof.* We establish S3 as a state invariant by induction over the reachable states of the system.

**Base case.** In the initial state `Σ₀`, no document has yet acquired any arrangement entries: `dom(Σ₀.M(d)) = ∅` for every document `d`. The universal quantification `(A d, v : v ∈ dom(Σ₀.M(d)) : Σ₀.M(d)(v) ∈ dom(Σ₀.C))` holds vacuously over the empty domain.

**Inductive step.** Assume S3 holds in state `Σ` and consider an arbitrary transition `Σ → Σ'`. We must show `(A d, v : v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ dom(Σ'.C))`. Take an arbitrary document `d` and `v ∈ dom(Σ'.M(d))`. Two cases arise.

*Case 1: Preserved mapping.* Suppose `v ∈ dom(Σ.M(d))` and the mapping is retained: `Σ'.M(d)(v) = Σ.M(d)(v)`. By the inductive hypothesis, `Σ.M(d)(v) ∈ dom(Σ.C)`. By S1 (store monotonicity), `dom(Σ.C) ⊆ dom(Σ'.C)`. Combining: `Σ'.M(d)(v) = Σ.M(d)(v) ∈ dom(Σ.C) ⊆ dom(Σ'.C)`, so `Σ'.M(d)(v) ∈ dom(Σ'.C)`.

*Case 2: New or modified mapping.* Suppose either `v ∉ dom(Σ.M(d))` or `Σ'.M(d)(v) ≠ Σ.M(d)(v)`. Let `a = Σ'.M(d)(v)`. The weakest-precondition analysis above requires `a ∈ dom(Σ'.C)` for every such mapping. We take this as an axiom: every arrangement-modifying operation that introduces a mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state — either because `a` already existed in `dom(Σ.C)` (and persists by S1), or because the operation atomically creates content at `a`. This is a design constraint on all arrangement-modifying operations, parallel to S0's constraint on content-store operations. Under this axiom, `Σ'.M(d)(v) ∈ dom(Σ'.C)`.

Since both cases yield `Σ'.M(d)(v) ∈ dom(Σ'.C)`, and `d` and `v` were arbitrary, S3 holds in `Σ'`. By induction, S3 holds in every reachable state. ∎

*Formal Contract:*
- *Preconditions:* State transitions satisfy S1 (store monotonicity).
- *Axiom:* Every arrangement-modifying operation introducing a mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state.
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`


## Content identity

What distinguishes transclusion from coincidence? In conventional systems, identity is by value — two files with identical bytes are "the same." In Xanadu, identity is by address.

**S4 (Origin-based identity).** For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`. Two independent writings of the word "hello" produce distinct I-addresses. A transclusion of existing content shares the original I-address.

S4 follows directly from GlobalUniqueness (ASN-0034), which establishes that no two distinct allocation events — whether from the same allocator or different allocators, whether simultaneous or separated by years — produce the same address. The two-stream architecture exploits this guarantee: when `Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂)` for documents `d₁ ≠ d₂`, the system knows this is transclusion — shared content with a common origin — not coincidental value equality. The structural test for shared identity is address equality, decidable from the addresses alone (T3, ASN-0034) without value comparison.

S4 creates a fundamental asymmetry in the system. The content store `C` is oblivious to values — it does not care whether `C(a₁) = C(a₂)`. But the arrangement family `M` is sensitive to addresses — two arrangements that map to the same I-address share content structurally, while two arrangements that map to different I-addresses with equal values do not. Nelson captures the distinction:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage... Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Live content shares I-addresses. Dead copies create new ones. The difference is structural — computable from the state alone.

*Proof.* We are given I-addresses `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to the tumbler axioms of ASN-0034 (T9, T10, T10a, TA5). We wish to show `a₁ ≠ a₂`.

GlobalUniqueness (ASN-0034) establishes the following invariant: for every pair of addresses `a, b` produced by distinct allocation events in any reachable system state, `a ≠ b`. The invariant's precondition requires only that `a₁` and `a₂` arise from distinct allocation events under the tumbler axioms — it places no condition on the values `Σ.C(a₁)` and `Σ.C(a₂)`. Since `a₁` and `a₂` are produced by distinct allocation events by hypothesis, GlobalUniqueness yields `a₁ ≠ a₂` directly.

The independence from content values deserves emphasis. GlobalUniqueness is a property of the tumbler addressing scheme: it derives from the structural interaction of T9 (forward allocation), T10 (partition independence), T10a (allocator discipline), and TA5 (hierarchical increment) — none of which reference the content store `C` or the value domain `Val`. The conclusion `a₁ ≠ a₂` is therefore invariant under any assignment of values to addresses. Whether `Σ.C(a₁) = Σ.C(a₂)` or `Σ.C(a₁) ≠ Σ.C(a₂)`, the addresses remain distinct.

Finally, the distinctness `a₁ ≠ a₂` is decidable from the addresses alone by T3 (CanonicalRepresentation, ASN-0034): two tumblers are equal if and only if they have the same length and agree at every component. No value comparison is required — the structural test for shared identity is address equality, computable in time proportional to the shorter address. ∎

*Formal Contract:*
- *Preconditions:* `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to the tumbler axioms of ASN-0034 (T9, T10, T10a, TA5).
- *Postconditions:* `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.
- *Frame:* The content store `C` and value domain `Val` play no role in the proof — distinctness is a property of the addressing scheme alone.


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

*Proof.* We wish to show that for every `N ∈ ℕ`, there exists a state `Σ` satisfying S0–S3 in which some I-address has sharing multiplicity exceeding `N`. We give two constructions — one for cross-document sharing, one for within-document sharing — each succeeding for arbitrary `N`.

**Cross-document construction.** Fix `N ∈ ℕ`. Define state `Σ_N = (C_N, M_N)` by:

- `C_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`.
- `N + 1` documents `d₁, …, d_{N+1}`, with `M_N(dᵢ) = {vᵢ ↦ a}` for pairwise distinct V-positions `vᵢ`.

We verify each invariant. S0 (content immutability) and S1 (store monotonicity) quantify over state transitions `Σ → Σ'`; we consider `Σ_N` as a single state with no transition, so both hold vacuously. S2 (arrangement functionality): each `M_N(dᵢ)` contains a single entry `{vᵢ ↦ a}` — the domain has one element, so uniqueness of the image is immediate; `M_N(dᵢ)` is a function. S3 (referential integrity): the sole I-address referenced by any arrangement is `a`, and `a ∈ dom(C_N)` by construction.

The sharing multiplicity of `a` in `Σ_N` is `|{(d, v) : v ∈ dom(M_N(d)) ∧ M_N(d)(v) = a}| = N + 1`, since each of the `N + 1` documents contributes exactly one pair `(dᵢ, vᵢ)`. Thus the multiplicity exceeds `N`.

**Within-document construction.** Fix `N ∈ ℕ`. Define state `Σ'_N = (C'_N, M'_N)` by:

- `C'_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`.
- One document `d` with `M'_N(d) = {v₁ ↦ a, v₂ ↦ a, …, v_{N+1} ↦ a}` for `N + 1` pairwise distinct V-positions `v₁, …, v_{N+1}`.

S0 and S1 are vacuous as above — single state, no transition to check. S2 (arrangement functionality): the `vᵢ` are pairwise distinct by hypothesis, so each V-position maps to exactly one I-address (namely `a`); `M'_N(d)` is a well-defined function. S3 (referential integrity): the sole referenced I-address `a` satisfies `a ∈ dom(C'_N)` by construction.

The within-document sharing multiplicity is `|{v : v ∈ dom(M'_N(d)) ∧ M'_N(d)(v) = a}| = N + 1 > N`.

**Conclusion.** Since both constructions succeed for arbitrary `N ∈ ℕ`, the conjunction S0 ∧ S1 ∧ S2 ∧ S3 is consistent with sharing multiplicity exceeding any given finite bound. No finite cap on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|` is entailed by these invariants — neither across documents nor within a single document. ∎

*Formal Contract:*
- *Preconditions:* `N ∈ ℕ` arbitrary.
- *Postconditions:* There exists a state `Σ` satisfying S0 (content immutability), S1 (store monotonicity), S2 (arrangement functionality), and S3 (referential integrity) such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).
- *Frame:* S0–S3 are the only invariants checked. The constructions are minimal — single I-address, trivial arrangements — to isolate the consistency claim from other architectural properties.


## Persistence independence

Content persists in Istream regardless of whether any arrangement references it.

**S6 (Persistence independence).** The membership of `a` in `dom(Σ.C)` is independent of all arrangements:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

S6 is a consequence of S0, which guarantees domain persistence unconditionally — it does not condition on whether any arrangement references `a`. But we state S6 separately because it names a design commitment that S0's formulation does not emphasise: the decision NOT to garbage-collect unreferenced content.

A system could satisfy a weakened form of S0 that permits removal when `(A d :: a ∉ ran(M(d)))` — when no arrangement references the content. Nelson explicitly rejects this. "Deleted bytes" are described as "not currently addressable, awaiting historical backtrack functions." The content remains because history requires it. Version reconstruction depends on the availability of Istream fragments from prior arrangements. If content were reclaimed when its last current reference vanished, the system could not fulfill: "When you ask for a given part of a given version at a given time, it comes to your screen."

S6 creates what Gregory calls an "orphan" phenomenon. Content in `dom(C)` that is not in `ran(M(d))` for any current document `d` is *unreachable through any query that starts from Vstream*. Gregory's evidence is definitive: "There is no mechanism to discover them, and the architecture makes no provision for it." The system provides no Istream iterator, no allocation registry queryable for "all content ever stored." To retrieve orphaned content, you must already know its I-address.

This is not a deficiency but a structural consequence of the two-stream model. The system's query interface is Vstream-primary: you start from a document (a Vstream entity), look up content (through the arrangement), and follow references (through Istream addresses). There is no path that begins in Istream and discovers content without a Vstream entry point. Orphaned content is permanent but practically invisible — a kind of information-theoretic dark matter, present by guarantee but unobservable through the system's own instruments.

*Proof.* We wish to show that for every `a ∈ dom(Σ.C)` and every state transition `Σ → Σ'`, the implication `a ∈ dom(Σ'.C)` holds regardless of any changes to any arrangement function `Σ.M(d)`.

The argument has two parts: first that domain persistence holds, then that it holds independently of arrangements.

**Domain persistence.** Let `a ∈ dom(Σ.C)` be arbitrary and let `Σ → Σ'` be any state transition. By S0 (content immutability), `a ∈ dom(Σ.C)` implies the conjunction `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The first conjunct yields `a ∈ dom(Σ'.C)` directly. Since `a` was arbitrary, `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C))`.

**Independence from arrangements.** S0's guarantee is quantified over ALL state transitions `Σ → Σ'` — including transitions that add, remove, or reassign entries in any arrangement `M(d)`. Crucially, S0's antecedent is `a ∈ dom(Σ.C)` alone: it does not condition on whether `a` appears in `ran(M(d))` for any document `d`. The guarantee makes no reference to the arrangement functions whatsoever — the content function `C` and the arrangement functions `M` are distinct components of the system state, and S0 constrains `C` without mentioning `M`. Therefore, the conclusion `a ∈ dom(Σ'.C)` holds whether zero, one, or all arrangements reference `a`, and whether the transition modifies any arrangement or not. The persistence of `a` in `dom(C)` is a property of the content store alone, insulated from the arrangement layer by the two-stream separation.

We note what S6 excludes. A system satisfying a weakened variant of S0 — one that permits removal of `a` from `dom(C)` when `(A d :: a ∉ ran(M(d)))` — would violate S6 while potentially preserving a conditional form of content immutability. S6's independence follows precisely because S0 is unconditional: it does not carve out an exception for unreferenced content. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` and state transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Postconditions:* `a ∈ dom(Σ'.C)`, with no condition on the arrangement functions `Σ.M(d)` or `Σ'.M(d)` for any document `d`.
- *Frame:* The arrangement functions `M(d)` are unconstrained — S6 holds for all possible values of `Σ'.M(d)`, including `Σ'.M(d) = ∅`.


## Structural attribution

Every V-position can be traced to the document that originally created its content.

S7 requires an architectural premise that T4 alone does not supply. T4 tells us HOW to parse a tumbler into fields; it does not tell us that Istream addresses are allocated under the originating document's tumbler prefix. We state this premise explicitly:

**S7a (Document-scoped allocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

This is a design requirement, not a convention. Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. The address IS the provenance: "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents.

*Formal Contract:*
- *Preconditions:* S7b (element-level I-addresses) ensures `zeros(a) = 3` for all `a ∈ dom(Σ.C)`, so that T4's `fields(a)` yields node, user, document, and element fields.
- *Axiom:* For every `a ∈ dom(Σ.C)`, the document-level prefix `(fields(a).node).0.(fields(a).user).0.(fields(a).document)` identifies the document whose owner allocated `a`.

A further design requirement constrains which tumblers may serve as content addresses. By T4's field correspondence (ASN-0034), the zero count determines a tumbler's hierarchical level: `zeros(t) = 0` gives node-level, `zeros(t) = 1` gives user-level, `zeros(t) = 2` gives document-level, and `zeros(t) = 3` gives element-level — the finest granularity. Since Istream addresses designate content elements within documents, every content address must reside at element level.

**S7b (Element-level I-addresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This is a design requirement: content resides at the element level — the finest level of the four-level tumbler hierarchy. Node, user, and document-level tumblers identify containers, not content. By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

*Formal Contract:*
- *Axiom:* `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

With S7a and S7b established, we can state structural attribution:

**S7 (Structural attribution).** For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system. Since document creation is an allocation event within a system conforming to T10a, GlobalUniqueness (ASN-0034) directly guarantees that distinct documents have distinct tumblers, and therefore distinct document-level prefixes. It is not metadata that can be stripped or forged — it IS the address. To retrieve the content, the system must know its I-address; to know its I-address is to know its origin.

S7 follows from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), T4 (FieldSeparatorConstraint, ASN-0034), and GlobalUniqueness (ASN-0034) (distinct document creations produce distinct prefixes). Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

We note a subtlety. S7 identifies the document that ALLOCATED the I-address — the document where the content was first created. This is distinct from the document where the content currently appears. When content is transcluded from document B into document A, the reader viewing A sees the content, but S7 traces it to B. The distinction between "where I am reading" (Vstream context, document A) and "where this came from" (Istream structure, document B) is precisely the two-stream separation made visible.

Gregory's implementation reveals two mechanisms for origin lookup. The I-address prefix itself encodes the originating document (used during address allocation to scope the search range). Separately, each arrangement entry carries an explicit `homedoc` field recording the allocating document (used during retrieval). At the abstract level, S7 says only that the information is present in the address — it does not prescribe how an implementation extracts it.

*Proof.* We wish to show that for every `a ∈ dom(Σ.C)`, the function `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` is well-defined, uniquely identifies the document that allocated `a`, and that this identification is permanent and unseverable.

**Well-definedness.** By S7b (element-level I-addresses), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`. By T4 (FieldSeparatorConstraint, ASN-0034), `zeros(a) = 3` means `a` contains exactly three zero-valued field separators, and `fields(a)` decomposes `a` into four fields: node, user, document, and element. T4's positive-component constraint guarantees every non-separator component is strictly positive, and T4's non-empty field constraint guarantees each present field has at least one component. The expressions `fields(a).node`, `fields(a).user`, and `fields(a).document` are therefore all well-defined with at least one strictly positive component each. The truncation `origin(a)` — formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field — is a well-defined tumbler satisfying `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy.

**Identification.** By S7a (document-scoped allocation), every I-address is allocated under the tumbler prefix of the document that created it. The document-level prefix of `a` — precisely `origin(a)`, the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`. This is not a lookup or annotation: the address structurally encodes its provenance. S7a ensures that `origin(a)` IS the allocating document's tumbler.

**Uniqueness across documents.** Document tumblers are themselves products of the tumbler allocation scheme: a document is created by allocating a document-level address under the owning user's prefix. For documents `d₁ ≠ d₂` created by distinct allocation events, GlobalUniqueness (ASN-0034) guarantees their document-level tumblers are distinct. By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison. Therefore, for any `a₁, a₂ ∈ dom(Σ.C)` allocated under distinct documents: `origin(a₁) ≠ origin(a₂)`. The origin function discriminates allocating documents without ambiguity.

**Permanence.** By S0 (content immutability), once `a ∈ dom(Σ.C)`, then `a ∈ dom(Σ'.C)` for all successor states `Σ'` — the address persists. Since `a` is a tumbler — a fixed sequence of components, not a mutable reference — and `origin(a)` is computed from the components of `a` alone via T4's deterministic field decomposition, `origin(a)` yields the same result in every state in which `a` exists. By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused. The attribution cannot be severed because it is not a separate datum attached to the content — it is a structural property of the address itself. To retrieve content at `a`, a system must know `a`; to know `a` is to know `origin(a)`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), T4 (FieldSeparatorConstraint, ASN-0034), and T10a (allocator discipline, ASN-0034).
- *Definition:* `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — the document-level prefix of `a`, obtained by truncating the element field.
- *Postconditions:* (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.


## Span decomposition

The arrangement `M(d)` maps individual V-positions to I-addresses. But the mapping has internal structure: contiguous V-ranges often correspond to contiguous I-ranges. This is what makes finite representation possible.

Before defining correspondence runs, we must establish the structure of `dom(M(d))` more carefully.

**S8-fin (Finite arrangement).** For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

S8-fin is a design invariant whose enforcement is a constraint on every operation that modifies the arrangement. We justify it by induction over the sequence of operations that produce a reachable state.

In the initial state Σ₀, every document `d` has `dom(Σ₀.M(d)) = ∅` — the empty set is finite. This is our base case.

For the inductive step, suppose `dom(Σ.M(d))` is finite in state Σ, and let Σ → Σ' be a transition produced by a single operation. By design, every arrangement-modifying operation — INSERT, DELETE, COPY, REARRANGE, APPEND — accepts a finite specification and modifies `dom(M(d))` by adding or removing only finitely many V-positions. No operation is permitted to introduce infinitely many V-positions; this is not derived from other properties but is a constraint imposed on every operation definition. A finite set altered by finitely many additions and removals remains finite, so `dom(Σ'.M(d))` is finite.

Since every reachable state is obtained from Σ₀ by a finite sequence of such transitions, and each transition preserves finiteness of the domain, `dom(Σ.M(d))` is finite for every document `d` in every reachable state Σ. ∎

*Formal Contract:*
- *Invariant:* `dom(Σ.M(d))` is finite for every document `d` and every reachable state Σ.
- *Axiom:* Every arrangement-modifying operation adds or removes only finitely many V-positions — finiteness of each operation's effect is a design constraint enforced by construction.

**S8a (V-position well-formedness).** Every V-position is an element-field tumbler with all components strictly positive:

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`

A V-position represents the element field of a full document-scoped address — the fourth field in the T4 field structure. Its first component `v₁` is the subspace identifier. The conjunct `v₁ ≥ 1` is not a guard but a universally true consequence: V-positions are element-field tumblers, and T4's positive-component constraint requires every component of every field to be strictly positive — so `v₁ ≥ 1` holds for all V-positions without exception. This universality is load-bearing: S8's partition proof requires every V-position to belong to some subspace `S` with `v₁ = S ≥ 1` to invoke T5 and T10 for cross-subspace disjointness. The domain and range of `M(d)` live in structurally different tumbler subsets: `dom(M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}` (element-field tumblers), while `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b). Since all V-positions in subspace `s` extend the single-component prefix `[s]`, T5 (PrefixContiguity, ASN-0034) guarantees they form a contiguous interval under T1 — grounding the application of tumbler ordering properties to V-positions and justifying S8-depth's reference to "within a subspace."

*Remark.* The shared vocabulary identifies a second subspace for links (v₁ = 2, per T4 and LM 4/30). Link-subspace V-positions satisfy the same `zeros(v) = 0` and `v > 0` constraints as text-subspace positions — both are element-field tumblers with strictly positive components. The subspace identifier (1 for text, 2 for links) is the first component of the element field; the `0` in tumbler notation (e.g., `N.0.U.0.D.V.0.2.1`) is a field separator, not a subspace identifier. Link-subspace arrangement semantics are deferred to a future ASN.

*Proof.* S8a is a design requirement: V-positions are element-field tumblers, and T4 (FieldSeparatorConstraint, ASN-0034) constrains the structure of every field. We show each conjunct follows from this structural commitment.

A full element-level I-address has the form `N.0.U.0.D.0.E` where `N`, `U`, `D`, `E` are the node, user, document, and element fields respectively, separated by zero-valued components. The arrangement `M(d)` maps V-positions to such I-addresses (S3, S7b). A V-position `v` is the element field `E` extracted from the document-scoped address — the fourth field in T4's decomposition. As an isolated field, `v` contains no field separators: the zeros in the full address are inter-field boundaries, not intra-field components. Therefore `zeros(v) = 0`.

The conjunct `v > 0` — every component of `v` is strictly positive — follows directly from T4's positive-component constraint. T4 requires that every non-separator component of every field satisfy `Eₗ > 0` for `1 ≤ l ≤ δ`, where `δ = #v` is the number of components in the element field. Since `zeros(v) = 0`, every component of `v` is a non-separator component, so every component is strictly positive: `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.

The conjunct `v₁ ≥ 1` is a specialisation of `v > 0` to the first component. T4's non-empty field constraint requires `δ ≥ 1` — the element field has at least one component. Since `v₁` is a component of the element field with `v₁ > 0` (from the positive-component constraint), we obtain `v₁ ≥ 1`. This is not an independent condition but a universally true consequence that we state explicitly because it is load-bearing: `v₁` serves as the subspace identifier, and S8's partition proof requires every V-position to belong to some subspace `S = v₁ ≥ 1` to invoke T5 and T10 for cross-subspace disjointness. ∎

*Formal Contract:*
- *Axiom:* V-positions are element-field tumblers — the fourth field in T4's decomposition of element-level addresses.
- *Preconditions:* S3 (Referential integrity) — `ran(M(d)) ⊆ dom(Σ.C)`, so S7b applies to the images of `M(d)`; T4 (FieldSeparatorConstraint, ASN-0034) — every non-separator component is strictly positive, every present field has at least one component; S7b — addresses in `dom(Σ.C)` are element-level tumblers with `zeros(a) = 3`.
- *Postconditions:* `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`.

**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

This is a design requirement, not a convention — parallel to S7a. Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth. Any correct implementation must satisfy this constraint.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: position `s.x` is followed by `s.(x+1)`. A parallel uniformity holds for I-addresses within a correspondence run: all I-addresses in a run share the same tumbler depth and prefix, differing only at the element ordinal. This follows from TA7a (ASN-0034): ordinal displacement `[x] ⊕ [k] = [x + k]` preserves the component count by construction, so the full I-address preserves depth and prefix when the structural context is held fixed. The uniformity is definitional — a correspondence run `(v, a, n)` specifies `M(d)(v + k) = a + k`, and both `v + k` and `a + k` are ordinal displacements that TA7a guarantees remain within their respective subspaces at the same depth. We write `v + k` for ordinal displacement applied to V-positions, and `a + k` for the same applied to the element ordinal of I-addresses.

(Why non-trivial runs arise in practice is a separate question. Allocator discipline — T10a, ASN-0034 — establishes that each allocator produces sibling outputs exclusively by `inc(·, 0)`, and TA5(c) guarantees the successor has the same depth as the predecessor. Consecutive allocations therefore produce consecutive I-addresses, which is why sequential content creation naturally yields correspondence runs of length greater than one. But this operational fact is motivation for the definition of correspondence runs, not a dependency of the decomposition proof.)

*Formal Contract:*
- *Axiom:* `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`
- *Definition:* A *correspondence run* is a triple `(v, a, n)` with `n ≥ 1` such that `(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`, where `v + k` and `a + k` denote ordinal displacement (TA7a) applied to V-positions and I-address element ordinals respectively.

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)`

At `k = 0` this is the base case `M(d)(v) = a` — no displacement, no arithmetic. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount. Within a correspondence run, each step forward in Vstream corresponds to the same step forward in Istream.

**S8 (Finite span decomposition).** For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the V-positions: every V-position in `dom(Σ.M(d))` falls in exactly one run — `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run: `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

Each run represents a contiguous block of content that entered the arrangement as a unit — characters typed sequentially, or a span transcluded whole.

*Proof.* We construct a finite decomposition satisfying both conjuncts and prove it partitions `dom(M(d))`.

**Existence.** By S8-fin, `dom(M(d))` is finite. By S2 (ArrangementFunctionality), `M(d)` is a function, so each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)`. For each such `v`, form the singleton run `(v, a, 1)`. Conjunct (b) requires `M(d)(v + k) = a + k` for all `k` with `0 ≤ k < 1` — the only such `k` is `0`, giving `M(d)(v) = a`, which holds by construction. Since `dom(M(d))` is finite, the collection of singletons is finite.

**Coverage.** Each `v ∈ dom(M(d))` lies in its own singleton's interval: `v ≤ v < v + 1`, where the right inequality holds because `v + 1 = inc(v, 0) > v` by TA5(a). So every V-position falls in at least one run.

**Uniqueness within a subspace.** Let `v, w ∈ dom(M(d))` be distinct V-positions with `v₁ = w₁ = S`. By S8-depth, `#v = #w = m` for some common depth `m`. We show `w ∉ [v, v + 1)`.

By S8a, `zeros(v) = 0`, so every component of `v` is nonzero and `sig(v) = max({i : 1 ≤ i ≤ m ∧ vᵢ ≠ 0}) = m`. By TA5(c), `v + 1 = inc(v, 0)` satisfies `#(v + 1) = m` and differs from `v` only at position `m`, with `(v + 1)_m = v_m + 1`. In particular, `(v + 1)ᵢ = vᵢ` for all `i < m`.

Suppose for contradiction that `t ≠ v` satisfies `#t = m` and `v ≤ t < v + 1`. Since `#t = #v = m`, the sequences diverge at some first position `j ≤ m`.

*Case j < m.* Then `tᵢ = vᵢ` for `i < j` and `tⱼ > vⱼ` (from `v ≤ t` by T1(i), since `j ≤ m = min(m, m)`). Since `(v + 1)ⱼ = vⱼ` (as `j < m`), and `tᵢ = vᵢ = (v + 1)ᵢ` for `i < j`, the first divergence between `t` and `v + 1` is at position `j` with `tⱼ > (v + 1)ⱼ`, giving `t > v + 1` by T1(i) — contradicting `t < v + 1`.

*Case j = m.* Then `tᵢ = vᵢ` for `i < m`, so `tᵢ = (v + 1)ᵢ` for `i < m` as well. The first divergence between `t` and `v + 1` is at position `m`. From `v ≤ t` with first divergence at `m`: `t_m ≥ v_m` by T1(i). From `t < v + 1` with first divergence at `m`: `t_m < (v + 1)_m = v_m + 1` by T1(i). Since components are natural numbers, `v_m ≤ t_m < v_m + 1` forces `t_m = v_m`. But then `t` agrees with `v` at all `m` components with `#t = #v = m`, so `t = v` by T3 (CanonicalRepresentation, ASN-0034) — contradicting `t ≠ v`.

Both cases yield contradictions. Since all V-positions in subspace `S` have depth `m` (S8-depth), no distinct V-position in the same subspace falls in `v`'s singleton interval.

*Remark.* S8-depth is essential. Without it, `dom(M(d))` could contain `s.3` (depth 2) and `s.3.1` (depth 3). By T1(ii), `s.3 < s.3.1` (prefix extension), and by T1(i) at position 2, `s.3.1 < s.4`. The position `s.3.1` would fall in the singleton interval of both `s.3` and `s.3.1` — violating unique partition.

**Uniqueness across subspaces.** Let `v ∈ dom(M(d))` with `v₁ = S₁` and `w ∈ dom(M(d))` with `w₁ = S₂`, where `S₁ ≠ S₂`. By S8a, `v` extends the single-component prefix `[S₁]` and `w` extends `[S₂]`. These prefixes are non-nesting: `[S₁] ≼ [S₂]` would require `S₁ = S₂` (both length-1 tumblers, so equality requires componentwise agreement by T3), contradicting `S₁ ≠ S₂`; symmetrically `[S₂] ⋠ [S₁]`.

*Case m ≥ 2.* The successor `v + 1` also extends `[S₁]`: since `sig(v) = m ≥ 2`, TA5(b) gives `(v + 1)ᵢ = vᵢ` for all `i < sig(v)`, so in particular `(v + 1)₁ = v₁ = S₁`. Since `[S₁] ≼ v` and `[S₁] ≼ (v + 1)` and `v ≤ v + 1` by TA5(a), T5 (PrefixContiguity, ASN-0034) gives: for any `t` with `v ≤ t ≤ v + 1`, `[S₁] ≼ t`. Every element of `[v, v + 1)` therefore extends `[S₁]`. By T10 (ASN-0034), since `[S₁]` and `[S₂]` are non-nesting prefixes, any tumbler extending `[S₁]` is distinct from any tumbler extending `[S₂]`. In particular, `w` (which extends `[S₂]`) cannot belong to `[v, v + 1)`.

*Case m = 1.* Then `v = [S₁]` and `v + 1 = [S₁ + 1]` (TA5(c) with `sig(v) = 1`). For any `t ∈ [v, v + 1)`: if `t₁ < S₁`, T1(i) gives `t < [S₁] = v`, contradicting `t ≥ v`; if `t₁ > S₁`, then `t₁ ≥ S₁ + 1` (components are natural numbers) and T1 gives `t ≥ [S₁ + 1] = v + 1`, contradicting `t < v + 1`. So `t₁ = S₁` for every `t ∈ [v, v + 1)`. Since `w₁ = S₂ ≠ S₁`, `w ∉ [v, v + 1)`. (Operationally, `m = 1` does not arise: ValidInsertionPosition requires `m ≥ 2`, since at `m = 1` ordinal succession changes the subspace identifier. But the partition holds regardless.)

**Conclusion.** The singleton runs cover every V-position in `dom(M(d))` (coverage) and no V-position falls in two distinct singleton intervals (uniqueness within and across subspaces). The singletons partition `dom(M(d))`. Since `dom(M(d))` is finite (S8-fin), the decomposition is finite, establishing both conjuncts (a) and (b). ∎

*Formal Contract:*
- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1)` (S8a); within each subspace, all V-positions share a common depth (S8-depth).
- *Postconditions:* There exists a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` satisfying (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))` and (b) `(A j, k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k)`.

What matters architecturally is that the number of runs `#runs(d)` is typically far smaller than `|dom(M(d))|` — the representation cost is proportional to the number of editing events, not the document size. Non-trivial runs arise when consecutive allocations produce consecutive I-addresses (as T10a and TA5(c) ensure operationally). Editing can both split and remove runs — inserting content in the middle of a run splits it into two, while deleting an entire run's V-span removes it. The number of distinct Istream allocation events underlying a document's history is monotonically non-decreasing (by S1), but the current arrangement's run count fluctuates with editing.

Gregory's evidence shows that `#runs(d)` has consequences beyond representation cost. Each correspondence run requires an independent tree traversal during V↔I translation. Gregory identifies the inner loop of this traversal as the documented CPU hotspot, responsible for 40% of processing time. For a document with `N` runs, a full V→I conversion requires `N` independent traversals — the cost is multiplicative in the fragmentation level, not merely additive. A consolidation function to merge adjacent runs was started in the implementation and abandoned mid-expression — the function body stops with an incomplete conditional: `if(`. Any implementation of the two-stream architecture must either consolidate runs or accept performance proportional to fragmentation level.


## Arrangement contiguity

Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." We formalize these structural properties as constraints on V-position sets within each subspace, extending the arrangement invariants established above.

Write S = subspace(v) = v₁ for the subspace identifier (the first component of the element-field V-position), and V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**D-CTG (VContiguity).** For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

In words: within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the standard text subspace at depth m = 2, this is a finite condition: the intermediates between [S, a] and [S, b] are the finitely many [S, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_S(d) occupies a single unbroken block of ordinals.

At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction: all positions in V_S(d) must share components 2 through m − 1.

*Proof.* Suppose for contradiction that V_S(d) contains two positions v₁ < v₂ (both depth m by S8-depth) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j, and (v₁)ⱼ < (v₂)ⱼ. The strict inequality at component j follows from v₁ < v₂ by T1(i) (LexicographicOrdering, ASN-0034): the first component at which two equal-length tumblers disagree determines their order. For any natural number n > (v₁)ⱼ₊₁, define w of length m by:

- wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j (agreeing with v₁ on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (if any such positions exist).

Then w has subspace S (since w₁ = (v₁)₁ = S) and depth m. We verify v₁ < w < v₂:

- **w > v₁**: w agrees with v₁ on components 1 through j. At component j + 1, n > (v₁)ⱼ₊₁. By T1(i), w > v₁.
- **w < v₂**: w agrees with v₂ on components 1 through j − 1 (since v₁ and v₂ agree there). At component j, wⱼ = (v₁)ⱼ < (v₂)ⱼ. By T1(i), w < v₂.

By D-CTG, every such w belongs to V_S(d). By T0(a), unboundedly many values of n exist; distinct values of n produce tumblers that differ at component j + 1, hence are distinct by T3 (CanonicalRepresentation, ASN-0034) — yielding infinitely many distinct positions in V_S(d), contradicting S8-fin. ∎

This applies uniformly to all depths m ≥ 3 and all divergence points j ∈ {2, …, m − 1}. At depth m = 3, the only possible pre-last divergence is j = 2. For illustration: suppose V_S(d) contained [S, 1, 5] and [S, 2, 1]. Setting j = 2, for any n > 5, w = [S, 1, n] satisfies [S, 1, 5] < [S, 1, n] < [S, 2, 1], so D-CTG forces [S, 1, 6], [S, 1, 7], ... into V_S(d) — infinitely many, contradicting S8-fin. At depth m = 4, divergence could occur at j = 2 or j = 3; the same construction applies in each case.

*Formal Contract:*
- *Invariant:* `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`
- *Axiom:* Every arrangement-modifying operation preserves V-contiguity within each subspace — this is a design constraint enforced by construction, parallel to S8-fin.

**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_S(d) be non-empty with common depth m ≥ 3 (S8-depth). Suppose for contradiction that V_S(d) contains two positions v₁ and v₂ with v₁ < v₂ (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j, and (v₁)ⱼ < (v₂)ⱼ (the inequality follows from v₁ < v₂ by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

We construct infinitely many intermediates. For any natural number n > (v₁)ⱼ₊₁, define w of length m by:

- wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j (agreeing with v₁ on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (if any such positions exist; since j ≤ m − 1, at least the m-th component exists at position j + 1 or beyond).

Then w has depth m (it has m components by construction), and subspace(w) = w₁ = (v₁)₁ = S (since j ≥ 2, the first component is copied from v₁). We verify v₁ < w < v₂:

- **w > v₁**: w agrees with v₁ on components 1 through j. At component j + 1, wⱼ₊₁ = n > (v₁)ⱼ₊₁. Since j + 1 ≤ m = min(m, m), by T1(i), w > v₁.
- **w < v₂**: w agrees with v₂ on components 1 through j − 1 (since v₁ and v₂ agree on these components by the definition of j). At component j, wⱼ = (v₁)ⱼ < (v₂)ⱼ. Since j ≤ m − 1 ≤ min(m, m), by T1(i), w < v₂.

Since v₁ < w < v₂, subspace(w) = S, and #w = m = #v₁, D-CTG requires w ∈ V_S(d). By T0(a) (UnboundedComponentValues, ASN-0034), unboundedly many values of n > (v₁)ⱼ₊₁ exist. Distinct values of n yield distinct tumblers w (they differ at component j + 1, so by T3, CanonicalRepresentation, ASN-0034, they are unequal). This produces infinitely many distinct positions in V_S(d), contradicting S8-fin (dom(M(d)) is finite).

Therefore no two positions in V_S(d) can disagree at any component j with 2 ≤ j ≤ m − 1. All positions share components 2 through m − 1, and contiguity reduces to contiguity of the last component (component m) alone. ∎

*Formal Contract:*
- *Preconditions:* V_S(d) non-empty; common depth m ≥ 3 (S8-depth); D-CTG (VContiguity); dom(M(d)) finite (S8-fin).
- *Postconditions:* `(A v₁, v₂ ∈ V_S(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of V_S(d) reduces to contiguity of the m-th (last) component.

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141."

**D-MIN (VMinimumPosition).** For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

D-MIN is a design constraint, not a derived property. D-CTG and S8-fin together establish that V_S(d) is a finite contiguous block, and D-CTG-depth establishes that positions share components 2 through m − 1, but none of these determine *where* the block starts: a set V_S(d) = {[S, 5, 3, k] : 1 ≤ k ≤ n} satisfies D-CTG, D-CTG-depth, S8-depth, and S8-fin equally well. What pins the starting ordinal is a convention of the tumbler system itself. All ordinal numbering starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). D-MIN asserts that V-positions follow this same convention, giving each subspace the canonical starting point [S, 1, …, 1].

At depth 2 this gives min(V_S(d)) = [S, 1]. Combined with D-CTG and S8-fin, a document with n elements in subspace S occupies V-positions [S, 1] through [S, n] — matching Nelson's "addresses 1 through 100."

*Formal Contract:*
- *Axiom:* `min(V_S(d)) = [S, 1, ..., 1]` for every document d and subspace S with V_S(d) non-empty, where the tuple has length m (S8-depth) and every post-subspace component is 1.

*Corollary (general form).* We derive from D-MIN the structure of V_S(d). By D-CTG-depth (when m ≥ 3) or vacuously (when m = 2, there is only one post-subspace component), all positions in V_S(d) share components 2 through m − 1. By D-MIN, min(V_S(d)) = [S, 1, …, 1], so those shared components have value 1. Every position is therefore [S, 1, …, 1, k] for varying k. D-CTG restricted to the last component forbids gaps among the k values; D-MIN gives the minimum k = 1; S8-fin bounds the maximum at some finite n. Thus:

**D-SEQ (SequentialPositions).** For each document d and subspace S, if V_S(d) is non-empty and the common V-position depth m ≥ 2 (S8-depth), then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m. The precondition m ≥ 2 is necessary: at m = 1 the tuple `[S, 1, ..., 1, k]` collapses to a single component where the subspace identifier S and the varying ordinal k occupy the same position, and the derivation step "D-MIN gives the minimum k = 1" fails because min(V_S(d)) = [S] has last component S, not 1. ValidInsertionPosition independently requires m ≥ 2 (the empty-subspace case establishes this lower bound), so the precondition is always satisfied in practice. At depth 2 this gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}, matching Nelson's "addresses 1 through n."

*Proof.* Let V_S(d) be non-empty and let m ≥ 2 be the common depth of all V-positions in subspace S (S8-depth guarantees a common depth exists).

**Step 1: shared prefix.** We show that every position in V_S(d) has the form [S, 1, …, 1, k] — that is, components 2 through m − 1 are all equal to 1, with only the last component varying.

*Case m = 2.* Every position has exactly two components: the subspace identifier S at component 1, and a single ordinal at component 2. There are no intermediate components (components 2 through m − 1 is the empty range 2 through 1), so the shared-prefix condition holds vacuously. Every position is [S, k] for some k, which is [S, 1, …, 1, k] with zero intervening 1s.

*Case m ≥ 3.* By D-CTG-depth (SharedPrefixReduction), all positions in V_S(d) share components 2 through m − 1. By D-MIN (VMinimumPosition), the minimum element of V_S(d) is [S, 1, …, 1] — a tuple of length m with every post-subspace component equal to 1. Since the minimum shares components 2 through m − 1 with every other position, and those components of the minimum are all 1, every position in V_S(d) has components 2 through m − 1 equal to 1. Every position is therefore [S, 1, …, 1, k] for some value k at the m-th component.

**Step 2: minimum k.** By D-MIN, min(V_S(d)) = [S, 1, …, 1] of length m. In the representation [S, 1, …, 1, k], the minimum has k = 1 at the last component. Since this is the minimum of V_S(d) and all positions share components 1 through m − 1 (Step 1), every other position [S, 1, …, 1, k] satisfies k ≥ 1 by T1(i). Therefore 1 is both attained and minimum among the k-values.

**Step 3: contiguity of k-values.** Let k₁ < k₂ be two values attained by positions v₁ = [S, 1, …, 1, k₁] and v₂ = [S, 1, …, 1, k₂] in V_S(d). Both have subspace S and depth m. By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂. For any integer k with k₁ < k < k₂, the tuple w = [S, 1, …, 1, k] satisfies subspace(w) = S, #w = m, and v₁ < w < v₂ (again by T1(i), since w agrees with both on components 1 through m − 1 and k₁ < k < k₂ at component m). By D-CTG (VContiguity), w ∈ V_S(d). Therefore every integer between any two attained k-values is itself attained — the k-values form a contiguous range.

**Step 4: finiteness.** By S8-fin (Finite arrangement), dom(M(d)) is finite, so V_S(d) ⊆ dom(M(d)) is finite. The k-values form a finite contiguous range.

**Assembly.** The k-values form a finite contiguous range of positive integers (Step 3, Step 4) beginning at 1 (Step 2). Therefore there exists n ≥ 1 such that the k-values are exactly {1, 2, …, n}. By Step 1, V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}. ∎

*Formal Contract:*
- *Preconditions:* V_S(d) non-empty; common V-position depth m ≥ 2 (S8-depth); D-CTG (VContiguity); D-CTG-depth (SharedPrefixReduction, for m ≥ 3); D-MIN (VMinimumPosition); dom(M(d)) finite (S8-fin).
- *Postconditions:* `(E n : n ≥ 1 : V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length m.

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

**Definition (ValidInsertionPosition).** A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2, since the first position placed in any subspace is established by the empty case, which requires m ≥ 2, and S8-depth preserves depth thereafter. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. The lower bound m ≥ 2 is necessary: at m = 1, v = [S] and shift([S], 1) = [S] ⊕ δ(1, 1) = [S] ⊕ [1]; the action point of [1] is k = 1, so TumblerAdd gives r₁ = S + 1, producing [S + 1] — a position in subspace S + 1, not S. For m ≥ 2, δ(n, m) has action point m, and since m > 1, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier. This is the canonical minimum position required by D-MIN. The choice of m is a one-time structural commitment: once any position is placed, S8-depth fixes the depth for all subsequent positions in the subspace.

In both cases, S = v₁ is the subspace identifier.

In the non-empty case, there are exactly N + 1 valid insertion positions: the N positions coinciding with existing V-positions v₀ through v_{N−1}, plus the append position shift(min(V_S(d)), N). In the empty case, there is one valid position per choice of depth m — but since m is chosen once and then held fixed by S8-depth, exactly one position is valid for any given depth.

We verify the structural claims. By D-MIN, min(V_S(d)) = [S, 1, ..., 1] of depth m. By OrdinalShift and TumblerAdd, shift([S, 1, ..., 1], j) = [S, 1, ..., 1] ⊕ δ(j, m); since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1 unchanged and sets the last component to 1 + j. The explicit form is shift(min(V_S(d)), j) = [S, 1, ..., 1 + j].

*Distinctness.* The N + 1 positions have last components 1 (for j = 0, where v = min(V_S(d))), 2, 3, ..., N + 1 (for j = 1, ..., N). These are pairwise distinct natural numbers, so by T3 (CanonicalRepresentation, ASN-0034) the N + 1 tumblers are pairwise distinct.

*Depth preservation.* For j ≥ 1, #shift(v, j) = #v = m by the result-length identity of OrdinalShift (ASN-0034). For j = 0, #v = #min(V_S(d)) = m by D-MIN. In the empty case, #v = m by construction. All valid positions have the common V-position depth required by S8-depth.

*Subspace identity.* Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged: shift(min, j)₁ = min₁ = S for all j ≥ 1. For j = 0, v₁ = min₁ = S directly.

*S8a consistency.* For text-subspace positions (S ≥ 1), every valid position [S, 1, ..., 1 + j] has all components strictly positive (S ≥ 1, intermediate components are 1, last component is 1 + j ≥ 1), so zeros(v) = 0 and v > 0 — satisfying S8a. ∎

*Formal Contract:*
- *Preconditions:* d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1 (subspace identifier).
- *Definition:* v is a valid insertion position in subspace S of d when: (1) V_S(d) ≠ ∅ with |V_S(d)| = N: v = min(V_S(d)) or v = shift(min(V_S(d)), j) for 1 ≤ j ≤ N; (2) V_S(d) = ∅: v = [S, 1, …, 1] of depth m ≥ 2.
- *Postconditions:* #v = m (depth preservation); v₁ = S (subspace identity); zeros(v) = 0 ∧ v > 0 (S8a consistency); in the non-empty case, exactly N + 1 valid positions, pairwise distinct by T3.

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

*Formal Contract:*
- *Preconditions:* State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Invariant:* `[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`.


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
| S0 | Content immutability: `a ∈ dom(C) ⟹ a ∈ dom(C') ∧ C'(a) = C(a)` for all transitions | design requirement |
| S1 | Store monotonicity: `dom(C) ⊆ dom(C')` for all transitions | from S0 |
| S2 | Arrangement functionality: `M(d)` is a function — each V-position maps to exactly one I-address | axiom |
| S3 | Referential integrity: `(A d, v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C))` | design requirement |
| S4 | Origin-based identity: distinct allocations produce distinct I-addresses regardless of value equality | from GlobalUniqueness, T3 (ASN-0034) |
| S5 | Unrestricted sharing: S0–S3 do not entail any finite bound on sharing multiplicity | consistent with S0, S1, S2, S3 |
| S6 | Persistence independence: `a ∈ dom(C)` is unconditional — independent of all arrangements | from S0 |
| S7a | Document-scoped allocation: every I-address is allocated under the originating document's prefix | design requirement |
| S7b | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | design requirement |
| S7 | Structural attribution: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — full document prefix | from S7a, S7b, S0, S4, T4, T3, GlobalUniqueness (ASN-0034) |
| S8-fin | Finite arrangement: `dom(M(d))` is finite for every document `d` | design requirement |
| S8a | V-position well-formedness: `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)` — universal, from T4 positive-component constraint | from T4, S7b (ASN-0034) |
| S8-depth | Fixed-depth V-positions: `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` | design requirement |
| S8 | Span decomposition: `dom(M(d))` decomposes into finitely many correspondence runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(vⱼ + k) = aⱼ + k` for `0 ≤ k < nⱼ` | theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5 (ASN-0034) |
| D-CTG | V-position contiguity: within each subspace, V-positions form a contiguous ordinal range with no gaps — design constraint on well-formed document states | design requirement |
| D-MIN | V-position minimum: minimum V-position in each non-empty subspace has all post-subspace components equal to 1 — design constraint | design requirement |
| D-CTG-depth | Shared prefix reduction: at depth m ≥ 3, contiguity reduces to the last component (all positions share components 2 through m − 1) | corollary of D-CTG, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034) |
| D-SEQ | Sequential positions (m ≥ 2): non-empty V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 | from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth, T1 (ASN-0034) |
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
