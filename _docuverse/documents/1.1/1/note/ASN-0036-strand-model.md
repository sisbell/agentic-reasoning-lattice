# ASN-0036: Strand Model

*2026-03-14; revised 2026-03-21, 2026-03-22, 2026-03-22, 2026-03-28, 2026-04-09, 2026-04-11*

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
- *Axiom (design requirement):* For every state transition `Σ → Σ'`, `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`.
- *Postconditions:* (a) Domain persistence — `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)`. (b) Value preservation — `a ∈ dom(Σ.C) ⟹ Σ'.C(a) = Σ.C(a)`.
- *Frame:* No condition on arrangements — the postcondition holds for arbitrary `Σ'.M(d)` and arbitrary changes to any document's arrangement.

**S1 (Store monotonicity).** `[dom(Σ.C) ⊆ dom(Σ'.C)]`

S1 is a corollary of S0, stated separately for emphasis.

S0 and S1 together establish `C` as an *append-only log*. New entries may be added — each at a fresh address guaranteed unique by T9 and T10 (ASN-0034) — but no existing entry may be modified or removed.

Nelson states this as an explicit design commitment: "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." Gregory's implementation confirms the commitment. Of the seventeen FEBE commands Nelson specifies, none modifies existing Istream content. There is no MODIFY, UPDATE, or REPLACE operation. The absence is structural — the protocol provides no mechanism for mutating stored content.

Gregory's evidence reveals an instructive footnote. The implementation carries a `refcount` field annotated "for subtree sharing, disk garbage collecting." Functions for reference-counted deletion exist: `deletefullcrumandgarbageddescendents()` and `deletewithgarbageddescendents()`. But the actual reclamation call was commented out on a specific date: `/*subtreefree(ptr);*/ /*12/04/86*/`. The machinery was built, dated December 4, 1986, and deliberately deactivated. S0 and S1 are upheld not by architectural impossibility but by a design choice so consistent that four decades of continuous operation have never violated it.

*Proof.* We wish to show that for every state transition `Σ → Σ'`, `dom(Σ.C) ⊆ dom(Σ'.C)`.

Let `a ∈ dom(Σ.C)` be arbitrary. By S0 (content immutability), `a ∈ dom(Σ.C)` implies the conjunction `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The first conjunct yields `a ∈ dom(Σ'.C)` directly. Since `a` was chosen arbitrarily from `dom(Σ.C)`, we have established `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C))`, which is `dom(Σ.C) ⊆ dom(Σ'.C)` by definition of subset inclusion.

S1 is strictly weaker than S0: it asserts domain persistence without value preservation. It is the domain conjunct of S0, restated for emphasis, and it specialises T8 (allocation permanence, ASN-0034) to the content store. T8 guarantees `allocated(s) ⊆ allocated(s')` for the address space as a whole; S1 guarantees `dom(Σ.C) ⊆ dom(Σ'.C)` for the content store specifically. The two properties have different scopes: T8 covers addresses that have been allocated but may carry no content, while S1 covers addresses at which content has actually been stored. ∎

*Formal Contract:*
- *Preconditions:* State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Postconditions:* `dom(Σ.C) ⊆ dom(Σ'.C)`.


## The arrangement and referential integrity

Vstream is where mutability lives. Each document's arrangement `M(d)` maps V-positions to I-addresses, presenting stored content as a readable sequence. Unlike `C`, arrangements change freely — content can be added, removed, and reordered.

**S2 (Arrangement functionality).** For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

This is inherent in the concept of a "virtual byte stream." Nelson: "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." Each position in the stream shows exactly one piece of content. A V-position cannot simultaneously contain two different things.

We note the phrase "regardless of their native origin." A document's Vstream presents content as a seamless sequence even when the I-addresses are scattered across multiple documents' Istreams. The arrangement function is what makes heterogeneous Istream origins appear as a uniform Vstream stream.

*Formal Contract:*
- *Axiom (definitional):* `Σ.M(d) : T ⇀ T` is a (partial) function — `(A d, v, a₁, a₂ : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a₁ ∧ Σ.M(d)(v) = a₂ : a₁ = a₂)`.
- *Postconditions:* For each `v ∈ dom(Σ.M(d))`, the image `Σ.M(d)(v)` is uniquely determined.
- *Frame:* Distinct V-positions may map to the same I-address (sharing — S5); injectivity is *not* asserted.

The bridge between the two state components is a well-formedness condition:

**S3 (Referential integrity).** `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Every V-reference resolves. If a document's arrangement says "at position `v`, display the content at I-address `a`," then `a` must be in `dom(C)`. There are no dangling references.

The maintenance of S3 across state transitions reveals a temporal ordering constraint. The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

For an operation that only adds a V-mapping without creating content, the target I-address must already be in `dom(C)`. An operation that atomically creates content at `a` and adds the mapping `M(d)(v) = a` satisfies S3 in the post-state without sequential precedence — `a ∈ dom(Σ'.C)` and `Σ'.M(d)(v) = a` are established simultaneously. The dependency is logical, not temporal: a reference presupposes the existence of its target, but existence need not precede reference in a prior transition. What matters for persistence is that S1 guarantees once `a` enters `dom(C)`, it remains — so a valid reference cannot become dangling through any subsequent state transition.

We observe a deliberate asymmetry. S3 says arrangement implies existence: `ran(M(d)) ⊆ dom(C)`. It does NOT say existence implies arrangement. Content can exist in Istream without being arranged in any current document. Nelson calls such content "deleted bytes — not currently addressable, awaiting historical backtrack functions, may remain included in other versions." The asymmetry is the space in which persistence independence lives.

*Formal Contract (S3):*
- *Axiom (well-formedness invariant):* In every state `Σ`, `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — equivalently, `ran(Σ.M(d)) ⊆ dom(Σ.C)`. Nelson asserts the canonical-order mandate of completed changes: "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34] Changes are "instantaneous" [LM 1/34] and the system is defined by the commands to which it responds [LM 4/61], so the invariant is asserted of the quiescent states between operations, not of any mid-operation interior — which lies outside Nelson's observable model.
- *Preservation across transitions:* For an operation that adds a V-mapping `M(d)(v) = a`, `wp(op, S3) ⟹ a ∈ dom(Σ'.C)` — the I-address must exist in the post-state.
- *Frame:* S3 is one-directional — content may exist in `dom(C)` without being referenced (orphaned content; S0 forbids reclamation, so orphaned content persists); existence does not entail arrangement.
- *Depends:* S1 (store monotonicity) — once a reference is valid, S1 prevents the target from being removed.


## Content identity

What distinguishes transclusion from coincidence? In conventional systems, identity is by value — two files with identical bytes are "the same." In Xanadu, identity is by address.

**S4 (Origin-based identity).** For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`. Two independent writings of the word "hello" produce distinct I-addresses. A transclusion of existing content shares the original I-address.

S4 follows directly from GlobalUniqueness (ASN-0034), which establishes that no two distinct allocation events — whether from the same allocator or different allocators, whether simultaneous or separated by years — produce the same address. The two-stream architecture exploits this guarantee: when `Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂)` for documents `d₁ ≠ d₂`, the system knows this is transclusion — shared content with a common origin — not coincidental value equality. The structural test for shared identity is address equality, decidable from the addresses alone (T3, ASN-0034) without value comparison.

S4 creates a fundamental asymmetry in the system. The content store `C` is oblivious to values — it does not care whether `C(a₁) = C(a₂)`. But the arrangement family `M` is sensitive to addresses — two arrangements that map to the same I-address share content structurally, while two arrangements that map to different I-addresses with equal values do not. Nelson captures the distinction:

> "Remember the analogy between text and water. Water flows freely, ice does not. The free-flowing, live documents on the network are subject to constant new use and linkage... Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." [LM 2/48]

Live content shares I-addresses. Dead copies create new ones. The difference is structural — computable from the state alone.

*Proof.* We are given I-addresses `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034). We wish to show `a₁ ≠ a₂`.

GlobalUniqueness (ASN-0034) establishes the following invariant: for every pair of addresses `a, b` produced by distinct allocation events in any reachable system state, `a ≠ b`. The invariant's precondition requires only that `a₁` and `a₂` arise from distinct allocation events under T10a — it places no condition on the values `Σ.C(a₁)` and `Σ.C(a₂)`. Since `a₁` and `a₂` are produced by distinct allocation events by hypothesis, GlobalUniqueness yields `a₁ ≠ a₂` directly.

The independence from content values deserves emphasis. GlobalUniqueness is a property of the tumbler addressing scheme: it derives from the structural interaction of T9 (forward allocation), T10 (partition independence), T10a (allocator discipline), and TA5 (hierarchical increment) — none of which reference the content store `C` or the value domain `Val`. The conclusion `a₁ ≠ a₂` is therefore invariant under any assignment of values to addresses. Whether `Σ.C(a₁) = Σ.C(a₂)` or `Σ.C(a₁) ≠ Σ.C(a₂)`, the addresses remain distinct.

Finally, the distinctness `a₁ ≠ a₂` is decidable from the addresses alone by T3 (CanonicalRepresentation, ASN-0034): two tumblers are equal if and only if they have the same length and agree at every component. No value comparison is required — the structural test for shared identity is address equality, computable in time proportional to the shorter address. ∎

*Formal Contract:*
- *Preconditions:* `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034).
- *Postconditions:* `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.
- *Frame:* The content store `C` and value domain `Val` play no role in the proof — distinctness is a property of the addressing scheme alone.


## Sharing

The arrangement function `M(d)` need not be injective. This is not a deficiency but a design requirement — it is what makes transclusion work.

**S5 (Unrestricted sharing).** The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

To see this, fix any `N`. Construct state `Σ_N` with one I-address `a` where `C(a) = w` for some value `w`, and `N + 1` documents `d₁, ..., d_{N+1}`, each with `M(dᵢ) = {v ↦ a}` for a single shared V-position `v` — the pairs `(dᵢ, v)` are distinct because the documents are. S0 is vacuous — single state, no transition to check. S2 holds: each `M(dᵢ)` is a function with a single entry. S3 holds: `a ∈ dom(C)`. The sharing multiplicity of `a` is `N + 1 > N`. Since `N` was arbitrary, no finite bound is entailed. The same holds within a single document: for any `N`, construct `Σ'_N` with one I-address `a` where `C(a) = w`, and one document `d` with `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}` for `N + 1` distinct V-positions. S0 and S1 are vacuous as above (single state, no transition to check). S2 holds — each `vᵢ` maps to exactly one I-address (namely `a`). S3 holds — `a ∈ dom(C)`. The within-document sharing multiplicity is `N + 1 > N`.

In any particular state, the sharing multiplicity of each address is a definite finite number — possibly zero for orphaned content. The property is an architectural anti-constraint: the invariants place no finite cap on how many references may accumulate.

Nelson: "The virtual byte stream of a document may include bytes from any other document." And: "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely." Transclusion is recursive and unlimited.

Gregory confirms the unbounded nature at the implementation level. The global index that records which documents reference which I-addresses accumulates entries without cap — "no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism anywhere in the code path." Each referential inclusion adds one entry. The only constraints are physical resources (memory and disk), not architectural limits.

The combination of S4 and S5 gives the system its distinctive character. S4 says identity is structural — determined by I-address, not by value. S5 says sharing is unlimited — any number of documents can reference the same content. Together they establish a regime in which quotation is a first-class structural relationship: any number of documents can quote the same passage, and the system knows they are all quoting — not independently writing — because they share I-addresses.

We observe that the state `Σ = (C, M)` makes the sharing relation computable: given any `a ∈ dom(C)`, the set `{d : (E v :: M(d)(v) = a)}` is determined by the state. Nelson requires this to be queryable: "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." The state model supports this — the information is present; only the efficiency of its extraction is an implementation concern.

*Proof.* We wish to show that for every `N ∈ ℕ`, there exists a state `Σ` satisfying S0–S3 in which some I-address has sharing multiplicity exceeding `N`. We give two constructions — one for cross-document sharing, one for within-document sharing — each succeeding for arbitrary `N`.

**Cross-document construction.** Fix `N ∈ ℕ`. Define state `Σ_N = (C_N, M_N)` by:

- `C_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`.
- `N + 1` documents `d₁, …, d_{N+1}` with explicit witnesses `dᵢ = [1, 0, 1, 0, i]` for `i = 1, …, N + 1` (the natural numbers `1, …, N + 1` exist in ℕ by NAT-closure, ASN-0034 — `1 ∈ ℕ` from the same axiom's base case, and `i + 1 ∈ ℕ` for any `i ∈ ℕ` by closure under addition; the index range `i ∈ {1, …, N + 1}` is required so that the `D(dᵢ) = [i]` field has a strictly positive component, satisfying T4's positive-component constraint on present fields — at `i = 0` the trailing component would be a zero, which T4 reads as a field separator rather than a content component). Each `dᵢ` is a valid document-level tumbler: `zeros(dᵢ) = 2` with no adjacent zeros, positive endpoint components, and the three fields `N(dᵢ) = [1]`, `U(dᵢ) = [1]`, `D(dᵢ) = [i]` populated by strictly positive natural numbers (T4, HierarchicalParsing, ASN-0034). The `dᵢ` are pairwise distinct by T3 (CanonicalRepresentation, ASN-0034) since they have distinct last components. Fix a single V-position `v = [1, 1]` shared across all `N + 1` documents, and define each arrangement as `M_N(dᵢ) = {v ↦ a}`. The pairs `(dᵢ, v)` are pairwise distinct because the first coordinates `dᵢ` are pairwise distinct, which suffices for distinctness of pairs.

We verify each invariant. S0 (content immutability) and S1 (store monotonicity) quantify over state transitions `Σ → Σ'`; we consider `Σ_N` as a single state with no transition, so both hold vacuously. S2 (arrangement functionality): each `M_N(dᵢ)` contains a single entry `{v ↦ a}` — the domain has one element, so uniqueness of the image is immediate; `M_N(dᵢ)` is a function. S3 (referential integrity): the sole I-address referenced by any arrangement is `a`, and `a ∈ dom(C_N)` by construction.

The sharing multiplicity of `a` in `Σ_N` is `|{(d, v) : v ∈ dom(M_N(d)) ∧ M_N(d)(v) = a}| = N + 1`, since each of the `N + 1` documents contributes exactly one pair `(dᵢ, v)` (with the same fixed `v = [1, 1]` across all `i`). Thus the multiplicity exceeds `N`.

**Within-document construction.** Fix `N ∈ ℕ`. Define state `Σ'_N = (C'_N, M'_N)` by:

- `C'_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`.
- One document `d` with `M'_N(d) = {v₁ ↦ a, v₂ ↦ a, …, v_{N+1} ↦ a}` where `vₖ = [1, k]` for `k = 1, …, N + 1` — pairwise distinct V-positions (distinctness follows from distinct last components by T3, ASN-0034).

S0 and S1 are vacuous as above — single state, no transition to check. S2 (arrangement functionality): the `vᵢ` are pairwise distinct by construction (distinct last components, T3 — CanonicalRepresentation, ASN-0034), so each V-position maps to exactly one I-address (namely `a`); `M'_N(d)` is a well-defined function. S3 (referential integrity): the sole referenced I-address `a` satisfies `a ∈ dom(C'_N)` by construction.

The within-document sharing multiplicity is `|{v : v ∈ dom(M'_N(d)) ∧ M'_N(d)(v) = a}| = N + 1 > N`.

**Conclusion.** Since both constructions succeed for arbitrary `N ∈ ℕ`, the conjunction S0 ∧ S1 ∧ S2 ∧ S3 is consistent with sharing multiplicity exceeding any given finite bound. No finite cap on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|` is entailed by these invariants — neither across documents nor within a single document. ∎

*Formal Contract:*
- *Preconditions:* `N ∈ ℕ` arbitrary.
- *Postconditions:* There exists a state `Σ` satisfying S0 (content immutability), S1 (store monotonicity), S2 (arrangement functionality), and S3 (referential integrity) such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).
- *Frame:* S5 ranges over S0–S3 only; the witnesses are not claimed to satisfy later invariants.
- *Depends:* S0 (content immutability) — preserved vacuously by the single-state construction; S1 (store monotonicity) — preserved vacuously; S2 (arrangement functionality) — required to establish that the constructed `M(d)` is a well-defined function (pairwise-distinct keys map to single images); S3 (referential integrity) — established by construction since `ran(M(d)) = {a} ⊆ dom(C)`; T0 (ASN-0034) — supplies the ℕ-valued component carrier from which the explicit witness enumerations `dᵢ = [1, 0, 1, 0, i]` and `vₖ = [1, k]` are drawn; T4 (HierarchicalParsing, ASN-0034) — certifies the explicit document witnesses `dᵢ = [1, 0, 1, 0, i]` as well-formed document-level tumblers (`zeros = 2`, no adjacent zeros, positive endpoint components, each present field a non-empty sequence of strictly positive natural numbers); T3 (CanonicalRepresentation, ASN-0034) — used in the cross-document construction to establish distinctness of the explicit document witnesses `dᵢ` from distinct last components (the V-positions are identical `[1, 1]` across all documents); and in the within-document construction to establish distinctness of V-positions `[1, k]` for `k = 1, …, N + 1` from distinct last components (a single document is used).


## Persistence independence

Content persists in Istream regardless of whether any arrangement references it. The formal property — `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)` across every state transition — is already supplied by S0 (and equivalently by its S1 specialization to the domain). What remains to be stated is the *design commitment* that S0's formulation does not emphasize on its surface: the decision NOT to garbage-collect unreferenced content. This is a remark on what S0 forbids, not a separately-axiomatized property.

S0's antecedent is `a ∈ dom(Σ.C)` alone: it does not condition on whether `a` appears in `ran(M(d))` for any document `d`. The guarantee makes no reference to the arrangement functions whatsoever — the content function `C` and the arrangement functions `M` are distinct components of the system state, and S0 constrains `C` without mentioning `M`. The persistence of `a` in `dom(C)` is a property of the content store alone, insulated from the arrangement layer by the two-stream separation. A system could satisfy a weakened variant of S0 — one that permits removal of `a` from `dom(C)` when `(A d :: a ∉ ran(M(d)))` — while preserving a conditional form of content immutability; S0's unconditional form is precisely what rules this out. By the same argument, S0 forbids every reclamation rule that conditions removal of `a` on some predicate about `a`'s referenceability: reference-counted reclamation when the count drops to zero; mark-and-sweep from the current document roots; mark-and-sweep from all roots reachable at any time; link-orphan reclamation; cross-document orphan reclamation; address invalidation. Each such rule is a transition predicate that would remove some `a ∈ dom(Σ.C)` from `dom(Σ'.C)`, contradicting S0's unconditional universal.

Nelson explicitly rejects reclamation in any form. "Deleted bytes" are described as "not currently addressable, awaiting historical backtrack functions." The content remains because history requires it. Version reconstruction depends on the availability of Istream fragments from prior arrangements. If content were reclaimed when its last current reference vanished, the system could not fulfill: "When you ask for a given part of a given version at a given time, it comes to your screen."

The no-reclamation commitment creates what Gregory calls an "orphan" phenomenon. Content in `dom(C)` that is not in `ran(M(d))` for any current document `d` is *unreachable through any query that starts from Vstream*. Gregory's evidence is definitive: "There is no mechanism to discover them, and the architecture makes no provision for it." The system provides no Istream iterator, no allocation registry queryable for "all content ever stored." To retrieve orphaned content, you must already know its I-address.

This is not a deficiency but a structural consequence of the two-stream model. The system's query interface is Vstream-primary: you start from a document (a Vstream entity), look up content (through the arrangement), and follow references (through Istream addresses). There is no path that begins in Istream and discovers content without a Vstream entry point. Orphaned content is permanent but practically invisible — a kind of information-theoretic dark matter, present by guarantee but unobservable through the system's own instruments.


## Structural attribution

Every V-position can be traced to the document that originally created its content.

We first restrict S7's domain. The projection `D(a)` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: `zeros = 0` is node-only, `zeros = 1` is node+user, `zeros ≥ 2` has a document field). Since Istream addresses designate content elements within documents, we require:

**S7b (Element-level I-addresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This is a design requirement: content resides at the element level — the finest level of the four-level tumbler hierarchy. Node, user, and document-level tumblers identify containers, not content. By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

*Formal Contract (S7b):*
- *Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.
- *Postconditions:* By T4's field correspondence, all four identifying fields — node, user, document, element — are present and the element field exists. The projections `N(a)`, `U(a)`, `D(a)`, `E(a)` supplied by T4b are all well-defined.
- *Depends:* T4 (HierarchicalParsing, ASN-0034) — field correspondence; T4b (UniqueParse, ASN-0034) — projection definitions; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — supplies the surrounding T4-validity (no adjacent zeros, positive endpoint components `a₁ ≠ 0 ∧ a_{#a} ≠ 0`) on which T4b's projections in the postcondition rely; T10a.4 bounds `zeros ≤ 3`, and this axiom is the strict-equality strengthening that pins down `zeros(a) = 3` for content-bearing addresses; S0 (content immutability) — fixes `a`'s components, so allocation-time structure persists.

With the domain pinned to element-level addresses, S7 requires a further architectural premise that T4 alone does not supply. T4 tells us HOW to parse a tumbler into fields; it does not tell us that Istream addresses are allocated under the originating document's tumbler prefix. We state this premise explicitly:

**S7a (Document-scoped allocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N(a).0.U(a).0.D(a)` obtained by truncating the element field, where `N(a)`, `U(a)`, `D(a)` are the partial projections supplied by T4b (UniqueParse, ASN-0034) — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

This is a design requirement, not a convention. Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. The address IS the provenance: "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents.

*Formal Contract (S7a):*
- *Axiom (design requirement):* `(A a : a ∈ dom(Σ.C) :: the document-level prefix N(a).0.U(a).0.D(a) is the tumbler of the document whose owner performed the allocation that placed a into dom(C))`. By S7b (stated above), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are everywhere defined on the domain over which the axiom quantifies.
- *Depends:* T4 (HierarchicalParsing, ASN-0034) — defines the prefix structure; T4b (UniqueParse, ASN-0034) — defines projections `N`, `U`, `D` (the projection `D` is well-defined once `zeros(a) ≥ 2`, supplied here by S7b's `zeros(a) = 3`); S7b (Element-level I-addresses) — supplies `zeros(a) = 3` for every `a ∈ dom(Σ.C)`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are defined throughout the domain over which S7a is stated; T10a (AllocatorDiscipline, ASN-0034) — establishes the baptism principle; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — supplies the *surrounding* T4-validity (no adjacent zeros, positive endpoint components `a₁ ≠ 0 ∧ a_{#a} ≠ 0`) that T4b's projections require beyond the zero-count condition, so `N(a)`, `U(a)`, `D(a)` are well-defined on `dom(Σ.C)`; S0 (content immutability) — fixes `a`'s components, so allocation-time structure persists.

**S7c (Element-field depth).** Every content address has an element field of depth at least 2:

`(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)`

where `E(a)` is the element-field projection supplied by T4b (UniqueParse, ASN-0034). When S7c holds, we name the first component of the element field as the *I-address subspace identifier*:

`subspace_I(a) = E(a)₁`

This parallels `subspace(v) = v₁` for V-positions: both extract the subspace context from a tumbler whose first element-field component carries the subspace identifier. S7c is a design requirement ensuring that `subspace_I(a)` and the content ordinal `[E(a)₂, ..., E(a)_δ]` occupy distinct components. Without it, `δ = 1` is formally permitted by T4 and S7b — `inc(document_address, 2)` under T10a produces an element-level address with a single-component element field `[subspace_I(a)]`. At `δ = 1`, the subspace identifier IS the content ordinal: ordinal shifts change the subspace, and TA7a's ordinal-only formulation cannot be applied (removing the subspace identifier leaves an empty sequence, not a valid tumbler). At `δ ≥ 2`, `subspace_I(a)` is structural context outside the ordinal, and shifts act only within the subspace. Gregory's evidence confirms `δ = 2` as the standard allocation pattern: the element field is `[S, x]` where `S = subspace_I(a)` is the subspace identifier and `x` is the content ordinal.

*Formal Contract (S7c):*
- *Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)`.
- *Consequence (a) — subspace-ordinal separation:* `subspace_I(a) = E(a)₁` and the content ordinal `[E(a)₂, ..., E(a)_δ]` occupy distinct components of `E(a)`. *Derivation:* By S7b, `zeros(a) = 3`, so T4b's element-field projection `E(a)` is well-defined as a finite sequence of components. The axiom `#E(a) ≥ 2` gives the element field at least two components — `E(a)₁` and `E(a)₂` are therefore distinct positions. The content ordinal `[E(a)₂, ..., E(a)_δ]` begins at position 2 within `E(a)` and so does not overlap `E(a)₁` at position 1.
- *Consequence (b) — shift action-point separation:* For any `k ≥ 1`, the displacement `δ(k, #a)` has action point `#a`, which falls strictly after the position of `subspace_I(a)` in the full address — so `shift(a, k)` preserves `subspace_I(a)` by TumblerAdd's prefix rule: `subspace_I(shift(a, k)) = subspace_I(a)`. *Derivation:* ShiftPreservation conclusion (iv) below.
- *Consequence (c) — TA7a operand membership:* The within-subspace ordinal `[E(a)₂, ..., E(a)_δ]` is a non-empty tumbler in `S` — non-empty by S7c's own axiom `#E(a) ≥ 2`, and componentwise positive by T4's positive-component constraint on present fields — satisfying TA7a's operand precondition `o ∈ S` so that `⊕` and `⊖` are directly applicable. *Derivation:* Non-emptiness: by S7c, `#E(a) ≥ 2`, so the element field has at least a second component `E(a)₂`, and the suffix `[E(a)₂, …, E(a)_δ]` beginning at position 2 is therefore non-empty. Componentwise positivity: T4's positive-component constraint on present fields combined with T10a.4's componentwise positivity within `E(a)` gives `E(a)ᵢ ≥ 1` for every `i ∈ {1, …, δ}`, hence for every component of the suffix. The two facts together place the within-subspace ordinal in `S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}` (TA7a, ASN-0034).
- *Depends:* S7b (element-level I-addresses) — provides `E(a)`; T4b (UniqueParse, ASN-0034) — defines element-field projection; T4 (HierarchicalParsing, ASN-0034) — positive-component constraint on present fields, underwriting Consequence (c)'s positivity; ShiftPreservation (below) — supplies the subspace identity of Consequence (b); OrdinalShift (ASN-0034) — action point of `δ(k, #a)` at `#a` in Consequence (b); TumblerAdd (ASN-0034) — prefix rule, underwriting Consequence (b); TA7a (ASN-0034) — operand precondition `o ∈ S` for `⊕` and `⊖` on the within-subspace ordinal; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — componentwise positivity of `E(a)`, and the surrounding T4-validity used by T4b in Consequence (b); S0 (content immutability) — fixes `a`'s components, so allocation-time structure persists.

**subspace_I (I-address subspace identifier).** With S7c in hand, the projection `subspace_I(a) = E(a)₁` named in the prose above receives a standalone Formal Contract, paralleling the `subspace` block below for V-positions.

*Formal Contract:*
- *Signature:* `subspace_I : T → ℕ` — projects the first component of the element field of an I-address.
- *Preconditions:* `a ∈ dom(Σ.C)` (so S7b's `zeros(a) = 3` holds, making T4b's element-field projection `E(a)` well-defined); S7c's `#E(a) ≥ 2` (so that `E(a)₁` is well-defined as the first component of a non-empty element field).
- *Definition:* `subspace_I(a) = E(a)₁`.
- *Postconditions:* (a) `subspace_I(a) ∈ ℕ` — the projected component inherits T0's ℕ-valued carrier (ASN-0034). (b) `subspace_I(a) ≥ 1` — T4's positive-component constraint on present fields, refined by T10a.4's componentwise positivity within `E(a)`, delivers `E(a)₁ ≥ 1`.
- *Depends:* T0 (ASN-0034) — ℕ-valued component carrier underwriting postcondition (a); T4b (UniqueParse, ASN-0034) — supplies `E(a)` once S7b holds; T4 (HierarchicalParsing, ASN-0034) — positive-component constraint underwriting postcondition (b); T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — componentwise positivity within the element field, reinforcing postcondition (b); S7b — provides `E(a)` via `zeros(a) = 3`; S7c — provides `#E(a) ≥ 2`. The function depends only on S7b and S7c; subspace preservation under shift is established by ShiftPreservation conclusion (iv) below.

**ShiftPreservation** — *Element-level shift preserves structure* (LEMMA). For any `a ∈ dom(Σ.C)` and any `k ≥ 1`, the shift `shift(a, k) = a ⊕ δ(k, #a)` preserves the structural properties of `a`:

(i) `zeros(shift(a, k)) = 3` — S7b inherited;
(ii) `shift(a, k)` is T4-valid — all four T4 conjuncts (zero-count bound, no adjacent zeros, positive endpoint components) hold;
(iii) `#E(shift(a, k)) = #E(a)` — element-field depth inherited (S7c bound preserved);
(iv) `subspace_I(shift(a, k)) = subspace_I(a)` — subspace identifier inherited.

This lemma decouples the structural-preservation argument from S8's correspondence-run framing. The argument is generic in `a ∈ dom(Σ.C)` and `k ≥ 1`; it does not depend on whether `a` arises within a correspondence run, and it has its own Formal Contract independent of S8's existence proof (which exhibits only singleton witnesses where `k = 0` and the shift is the identity).

*Proof.* Let `δ = #E(a)`. By S7b, `zeros(a) = 3`, so T4 partitions `a` as `N(a).0.U(a).0.D(a).0.E(a)` with the three field-separator zeros at positions strictly less than `#a`, and the element field `E(a)` occupies positions `#a − δ + 1` through `#a`. By S7c, `δ ≥ 2`. The displacement `δ(k, #a) = [0, …, 0, k]` of length `#a` has `actionPoint(δ(k, #a)) = #a` (OrdinalShift, ASN-0034). By TumblerAdd's three-region component formula (ASN-0034), every component of `a` at a position strictly before `#a` is copied unchanged into `shift(a, k) = a ⊕ δ(k, #a)`, and TumblerAdd's length postcondition gives `#shift(a, k) = #a`. The only position whose value may differ from `a` is the last one, `#a`, which is overwritten by TumblerAdd's action-point clause: `shift(a, k)_{#a} = a_{#a} + k`.

*Conclusion (i): preserved zero-count.* By T4's field-segment constraint (ASN-0034) applied to `a`, `a_{#a} ≠ 0`, so `a_{#a} ∈ ℕ` with `a_{#a} ≥ 1`: since `0` is the least element of T0's carrier ℕ (ASN-0034) we have `0 ≤ a_{#a}`, and NAT-discrete at `m = 0` (`0 ≤ n < 0 + 1 ⟹ n = 0`) contrapositively excludes `a_{#a} < 1`, so NAT-order's trichotomy on `(a_{#a}, 1)` leaves `a_{#a} ≥ 1`; combined with `k ≥ 1`, NAT-addcompat (left and right order compatibility) together with NAT-order's ≤-transitivity Consequence yields the chain `1 + 1 ≤ a_{#a} + 1 ≤ a_{#a} + k`: right order compatibility at `(m, n, p) = (1, a_{#a}, 1)` lifts `1 ≤ a_{#a}` to `1 + 1 ≤ a_{#a} + 1`, then left order compatibility at `(m, n, p) = (a_{#a}, k, 1)` lifts `1 ≤ k` to `a_{#a} + 1 ≤ a_{#a} + k`, and ≤-transitivity chains the two into `a_{#a} + k ≥ 1 + 1 > 0`. By TumblerAdd's prefix rule, every position `i < #a` of `shift(a, k)` is copied unchanged from `a`, preserving the zero/nonzero status at every such position: the three field-separator zeros of `a` (between `N`, `U`, `D`, and `E`, all at positions `< #a`) remain zero in `shift(a, k)` at the same positions, and every non-separator position `i < #a` (each of which is nonzero in `a` since the three field separators account for all of `zeros(a) = 3` per S7b) remains nonzero in `shift(a, k)`. Combined with `a_{#a} + k > 0` at position `#a` from the chain above, `shift(a, k)` has exactly the three field-separator zeros at the same positions as `a` and no other zeros, so `zeros(shift(a, k)) = zeros(a) = 3` — establishing conclusion (i).

*Conclusion (ii): T4-validity of `shift(a, k)`.* All four T4-validity conjuncts hold for `shift(a, k)`. (1) *Zero-count bound:* conclusion (i) establishes `zeros(shift(a, k)) = 3 ≤ 3`. (2) *No adjacent zeros:* the three zeros of `shift(a, k)` sit at exactly the same positions as in `a` (all strictly less than `#a`, copied unchanged by TumblerAdd's prefix rule), and `a` is T4-valid (S7b's `zeros(a) = 3` together with T10a.4's preservation of T4-validity under T10a allocation), so `a`'s no-adjacent-zeros property carries over component-by-component to `shift(a, k)`. (3) *Positive first component:* `shift(a, k)₁ = a₁` since position 1 is strictly less than `#a` (because `#a ≥ 7` — three field-separator zeros plus at least one non-separator component in each of the four fields, summing to 3 + 4 = 7; invoking S7c's `#E(a) ≥ 2` tightens this to `#a ≥ 8`, and either bound suffices for `#a > 1`) and TumblerAdd's prefix rule copies position 1 unchanged; T4-validity of `a` then gives `a₁ ≠ 0`. (4) *Positive last component:* `shift(a, k)_{#a} = a_{#a} + k ≥ 1 + 1 > 0` from the chain established in conclusion (i).

*Conclusion (iii): preserved element-field depth.* With T4-validity of `shift(a, k)` in hand from conclusion (ii), T4b applies. Since `#shift(a, k) = #a` and the three field-separator zeros sit at exactly the same positions in `shift(a, k)` as in `a` (all strictly less than `#a`, copied by the prefix rule), T4's partition `N(shift(a, k)).0.U(shift(a, k)).0.D(shift(a, k)).0.E(shift(a, k))` has the same element-field boundary as `a`'s partition. The element field of `shift(a, k)` occupies exactly the last `δ` positions, so `#E(shift(a, k)) = #E(a) = δ ≥ 2`, preserving S7c's depth bound — establishing conclusion (iii).

*Conclusion (iv): preserved subspace identifier.* With conclusions (i) and (iii) in hand, the element field `E(shift(a, k))` is well-defined and occupies exactly the same positions in `shift(a, k)` as `E(a)` occupies in `a`: by (i) the three field-separator zeros sit at identical positions in both tumblers, so T4's partition draws its element-field boundary at the same position, and by (iii) the element field has the same length `δ` in both, while TumblerAdd's length postcondition gave `#shift(a, k) = #a`. Let `q` be the first position of the element field — the position at which the subspace identifier `E(a)₁` sits. The element field occupies the contiguous block of positions `q, q + 1, …, #a`. By S7c, `δ = #E(a) ≥ 2`, so this block contains at least two positions; in particular position `q + 1` belongs to the field and is therefore `≤ #a`, the field's last position. By NAT-addcompat's strict successor clause `q < q + 1`, and by NAT-order's transitivity composing `q < q + 1` with `q + 1 ≤ #a`, we obtain `q < #a`. Hence the subspace-identifier position `q` lies strictly before the action point `#a`, and TumblerAdd's prefix rule copies this component unchanged from `a`: `shift(a, k)_q = a_q`. Re-expressing via T4b's element-field projection on each side (licensed by conclusion (ii) for `shift(a, k)`, and by S7b + T10a.4 for `a`): `E(shift(a, k))₁ = E(a)₁`, i.e. `subspace_I(shift(a, k)) = subspace_I(a)` — establishing conclusion (iv). ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` (so S7b's `zeros(a) = 3` and S7c's `#E(a) ≥ 2` hold; T10a.4 supplies T4-validity of `a`); `k ∈ ℕ` with `k ≥ 1`.
- *Postconditions:* (i) `zeros(shift(a, k)) = 3`. (ii) `shift(a, k)` is T4-valid. (iii) `#E(shift(a, k)) = #E(a)`. (iv) `subspace_I(shift(a, k)) = subspace_I(a)`.
- *Depends:* S7b (element-level I-addresses) — `zeros(a) = 3` partitions `a` into N/U/D/E fields; S7c (element-field depth) — `#E(a) ≥ 2`, used in conclusion (iv)'s position-arithmetic step; T4 (HierarchicalParsing, ASN-0034) — field-segment constraint `a_{#a} ≠ 0`, partition of `a`, numeral convention `2 := 1 + 1`, positive-component constraint on present fields; T4b (UniqueParse, ASN-0034) — element-field projection applied to both `a` and `shift(a, k)`, with `shift(a, k)`'s T4-validity discharged by conclusion (ii) before T4b is invoked in conclusion (iii); T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4-validity of `a`, supplying the no-adjacent-zeros and positive-first-component facts inherited by `shift(a, k)` via TumblerAdd's prefix rule; OrdinalShift (ASN-0034) — action point of `δ(k, #a)` at `#a`; TumblerAdd (ASN-0034) — three-region component formula, prefix rule, length postcondition, action-point identity `shift(a, k)_{#a} = a_{#a} + k`; NAT-discrete (NatDiscreteness, ASN-0034) — excludes `a_{#a} < 1`, fixing `a_{#a} ≥ 1` in conclusion (i); NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034) — closure of ℕ under addition for `a_{#a} + k`; NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034) — order compatibility and the strict successor clause for the chains in conclusions (i) and (iv); NAT-order (NatStrictTotalOrder, ASN-0034) — transitivity and trichotomy closing those chains; S0 (content immutability) — fixes `a`'s components, so allocation-time structure persists.
- *Frame:* The lemma operates on `a` and `k` alone — no state is consulted beyond the membership `a ∈ dom(Σ.C)` used to discharge S7b and S7c.

S7's uniqueness argument additionally requires that document tumblers themselves be products of the same allocation discipline that governs I-addresses. We make this commitment explicit:

**S7d (Document allocation discipline).** Every document is addressed by a document-level tumbler (`zeros = 2`) allocated via T10a's allocator discipline (ASN-0034) under the owning user's prefix. Distinct documents arise from distinct allocation events.

This is a design requirement parallel to S7a. Nelson's baptism principle covers it directly: the user-level allocator baptises documents under the user's prefix in the same way each document's allocator baptises elements under the document's prefix. Without S7d, "documents" could in principle share document-level tumblers, and the cross-document uniqueness step in S7's proof would have no premise on which to instantiate GlobalUniqueness (ASN-0034) — S7a alone speaks only of how I-addresses sit beneath their owning document's prefix, not of how the document tumblers themselves are produced.

*Formal Contract (S7d):*
- *Axiom (design requirement):* Every document tumbler `d` satisfies `zeros(d) = 2` and is the result of an allocation event under T10a; distinct documents arise from distinct allocation events.
- *Postconditions:* By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers — the cross-document uniqueness premise for S7's identification argument.
- *Depends:* T10a (AllocatorDiscipline, ASN-0034) — allocation events; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — guarantees that every T10a allocation event produces a T4-valid tumbler, so document-level outputs satisfy T4's structural constraints (no adjacent zeros, positive endpoint components) that T4's field correspondence at `zeros = 2` presupposes; T4 (HierarchicalParsing, ASN-0034) — field correspondence at `zeros = 2`; GlobalUniqueness (ASN-0034) — uniqueness across allocation events.

With S7a, S7b, and S7d established, we can state structural attribution.

**S7 (Structural attribution).** For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = N(a).0.U(a).0.D(a)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system. Since document creation is an allocation event within a system conforming to T10a, GlobalUniqueness (ASN-0034) directly guarantees that distinct documents have distinct tumblers, and therefore distinct document-level prefixes. It is not metadata that can be stripped or forged — it IS the address. To retrieve the content, the system must know its I-address; to know its I-address is to know its origin.

S7 follows from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), S7d (document tumblers are themselves products of T10a allocation events, supplying the precondition for GlobalUniqueness), T4 (HierarchicalParsing, ASN-0034), and GlobalUniqueness (ASN-0034) (distinct document allocation events produce distinct document tumblers). Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

We note a subtlety. S7 identifies the document that ALLOCATED the I-address — the document where the content was first created. This is distinct from the document where the content currently appears. When content is transcluded from document B into document A, the reader viewing A sees the content, but S7 traces it to B. The distinction between "where I am reading" (Vstream context, document A) and "where this came from" (Istream structure, document B) is precisely the two-stream separation made visible.

Gregory's implementation reveals two mechanisms for origin lookup. The I-address prefix itself encodes the originating document (used during address allocation to scope the search range). Separately, each arrangement entry carries an explicit `homedoc` field recording the allocating document (used during retrieval). At the abstract level, S7 says only that the information is present in the address — it does not prescribe how an implementation extracts it.

*Proof.* We wish to show that for every `a ∈ dom(Σ.C)`, the function `origin(a) = N(a).0.U(a).0.D(a)` is well-defined, uniquely identifies the document that allocated `a`, and that this identification is permanent and unseverable.

**Well-definedness.** Two distinct contributions establish that `a` is a well-formed T4 tumbler on which the field-decomposition machinery applies. *First,* by S7b (element-level I-addresses), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3` — this strict equality is supplied axiomatically as a design requirement on element-level I-addresses, fixing the zero-count exactly. *Second,* by T10a.4 (T4PreservationUnderDiscipline, ASN-0034), every address produced by an allocation event under T10a's discipline is a well-formed T4 tumbler — T10a.4 preserves T4-validity (`zeros ≤ 3`, no adjacent zeros, positive endpoint components `a₁ ≠ 0 ∧ a_{#a} ≠ 0`) as a structural invariant under allocation, but does *not* itself fix the exact value `zeros = 3`. Combining the two: S7b pins the zero-count at exactly 3, T10a.4 supplies the structural well-formedness, and together they guarantee that T4's field-decomposition machinery applies to `a`. By T4 (HierarchicalParsing, ASN-0034), `zeros(a) = 3` means `a` contains exactly three zero-valued field separators, and the partial projections supplied by T4b (UniqueParse, ASN-0034) — `N(a)`, `U(a)`, `D(a)`, `E(a)` — extract the node, user, document, and element fields respectively, each as a finite sequence of strictly positive natural numbers. T4's positive-component constraint guarantees every non-separator component is strictly positive, and T4's non-empty field constraint guarantees each present field has at least one component. The projections `N(a)`, `U(a)`, and `D(a)` are therefore all well-defined with at least one strictly positive component each. The truncation `origin(a)` — formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field — is a well-defined tumbler satisfying `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy.

**Identification.** By S7a (document-scoped allocation), every I-address is allocated under the tumbler prefix of the document that created it. The document-level prefix of `a` — precisely `origin(a)`, the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`. This is not a lookup or annotation: the address structurally encodes its provenance. S7a ensures that `origin(a)` IS the allocating document's tumbler.

**Uniqueness across documents.** By S7d (document allocation discipline), every document tumbler is itself the product of an allocation event under T10a's discipline: a document is created by allocating a document-level address under the owning user's prefix, and distinct documents arise from distinct allocation events. For documents `d₁ ≠ d₂`, S7d supplies the required premise — distinct allocation events — and GlobalUniqueness (ASN-0034) then guarantees that the resulting document-level tumblers are distinct. By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison. Therefore, for any `a₁, a₂ ∈ dom(Σ.C)` allocated under distinct documents: `origin(a₁) ≠ origin(a₂)`. The origin function discriminates allocating documents without ambiguity.

**Permanence.** By S0 (content immutability), once `a ∈ dom(Σ.C)`, then `a ∈ dom(Σ'.C)` for all successor states `Σ'` — the address persists. Since `a` is a tumbler — a fixed sequence of components, not a mutable reference — and `origin(a)` is computed from the components of `a` alone via T4's deterministic field decomposition, `origin(a)` yields the same result in every state in which `a` exists. By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused. The attribution cannot be severed because it is not a separate datum attached to the content — it is a structural property of the address itself. To retrieve content at `a`, a system must know `a`; to know `a` is to know `origin(a)`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), S7d (document allocation discipline), T4 (HierarchicalParsing, ASN-0034), T4b (UniqueParse, ASN-0034) — supplies the projections `N(a)`, `U(a)`, `D(a)`, `E(a)` from which `origin(a)` is computed, T10a (allocator discipline, ASN-0034), and T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — guarantees that T4-validity (`zeros ≤ 3`, no adjacent zeros, positive endpoint components) is preserved by every T10a allocation event, so the structural prerequisites of T4's field decomposition hold for `a`. The strict equality `zeros(a) = 3` itself comes from S7b axiomatically; T10a.4 supplies the surrounding T4 well-formedness needed for T4/T4b projections to be well-defined on `a`.
- *Postconditions:* (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.


## Span decomposition

The arrangement `M(d)` maps individual V-positions to I-addresses. But the mapping has internal structure: contiguous V-ranges often correspond to contiguous I-ranges. This is what makes finite representation possible.

Before defining correspondence runs, we must establish the structure of `dom(M(d))` more carefully.

**S8-fin (Finite arrangement).** For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

S8-fin follows from the operational reality: each V-position enters `dom(M(d))` through a specific operation (INSERT, COPY, etc.), and the system has performed only finitely many operations. No operation introduces infinitely many V-positions.

*Formal Contract:*
- *Axiom (design requirement):* For every state `Σ` and document `d`, `dom(Σ.M(d))` is a finite set.
- *Postconditions:* `|dom(Σ.M(d))| < ∞` — the arrangement has finite cardinality. Consequently `ran(Σ.M(d))` is finite (image of a finite set under a function).
- *Frame:* No constraint on the unbounded growth of `dom(C)`; only individual arrangements are required to be finite at any given state.

**S8a (V-position well-formedness).** A V-position is, by definition, an element-field tumbler of depth at least 2. From this structural commitment the zero-count and componentwise-positivity conjuncts follow:

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

A V-position represents the element field of a full document-scoped address — the fourth field in the T4 field structure. Its first component `v₁` is the subspace identifier. The depth constraint `#v ≥ 2` parallels S7c for I-address element fields: it ensures the subspace identifier `v₁` and the within-subspace ordinal `[v₂, ..., v_m]` occupy distinct components. Without it, `#v = 1` is formally permitted by T4, and the subspace identifier would coincide with the entire V-position — ordinal shifts would change the subspace, and the ordinal-extraction machinery (`ord(v)`, OrdAddHom, OrdShiftHom) below would be undefined. With `#v ≥ 2`, the subspace identifier is structural context outside the ordinal, and shifts act only within the subspace. The domain and range of `M(d)` live in structurally different tumbler subsets: `dom(M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2 ∧ (A i : tᵢ > 0)}` (element-field tumblers of depth at least 2), while `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b). Since all V-positions in subspace `s` extend the single-component prefix `[s]`, T5 (ContiguousSubtrees, ASN-0034) guarantees they form a contiguous interval under T1 — grounding the application of tumbler ordering properties to V-positions and justifying S8-depth's reference to "within a subspace."

*Remark.* The shared vocabulary identifies a second subspace for links (v₁ = 2, per T4 and LM 4/30). Link-subspace V-positions satisfy the same `zeros(v) = 0`, `#v ≥ 2`, and componentwise positivity constraints as text-subspace positions — both are element-field tumblers of depth ≥ 2 with strictly positive components. The subspace identifier (1 for text, 2 for links) is the first component of the element field; the `0` in tumbler notation (e.g., `N.0.U.0.D.0.2.1`) is a field separator, not a subspace identifier. S8a holds uniformly across both subspaces. (Subspace *alignment* — the requirement that each V-position resolve to an I-address in the matching subspace, `subspace(v) = subspace_I(M(d)(v))` — is deliberately not a strand-level invariant; it is an operations-layer obligation, posed as an Open Question below.)

*Proof.* S8a is a design requirement: V-positions are element-field tumblers of depth at least 2, paralleling S7c for I-address element fields. T4 (HierarchicalParsing, ASN-0034) constrains the structure of every field, and S7c-analog reasoning fixes the depth lower bound. We show each conjunct follows from this structural commitment.

A full element-level I-address has the form `N.0.U.0.D.0.E` where `N`, `U`, `D`, `E` are the node, user, document, and element fields respectively, separated by zero-valued components (the projections supplied by T4b, ASN-0034). The arrangement `M(d)` maps V-positions to such I-addresses (S3, S7b). A V-position `v` is structurally an element-field tumbler — the same shape as `E(a)` extracted from a document-scoped address. As an isolated field, `v` contains no field separators: the zeros in the full address are inter-field boundaries, not intra-field components. Therefore `zeros(v) = 0`.

The conjunct `#v ≥ 2` parallels S7c's `#E(a) ≥ 2` for I-addresses: the subspace identifier `v₁` and the within-subspace ordinal `[v₂, ..., v_m]` must occupy distinct components, otherwise ordinal-only arithmetic (TA7a, ASN-0034) cannot be applied. This is a design commitment for V-positions, justified architecturally by Nelson's text and link subspaces (LM 4/20, 4/30) where V-positions have the form `S.x` with `S` the subspace and `x` the ordinal — depth exactly 2.

The conjunct `(A i : 1 ≤ i ≤ #v : vᵢ > 0)` — every component of `v` is strictly positive — follows directly from `zeros(v) = 0` together with T0's ℕ-valued carrier. Every component of `v` is in ℕ, and `zeros(v) = 0` means no component equals 0; therefore every component is strictly positive. As a specialisation, `v₁ ≥ 1` holds — the subspace identifier is always a positive natural number. ∎

*Formal Contract:*
- *Definition:* A V-position is an element-field tumbler of depth at least 2 — paralleling S7c for I-address element fields. The `zeros(v) = 0` and componentwise-positivity conjuncts of the postcondition are derived from this structural commitment (proof above), not independently posited.
- *Preconditions:* T4 (HierarchicalParsing, ASN-0034) — every non-separator component is strictly positive, every present field has at least one component; T0 — components are natural numbers. (Note: S7c's `#E(a) ≥ 2` for I-address element fields is the architectural parallel that motivates the depth-≥-2 definition for V-positions; the definition is an independent commitment about V-positions, not derived from S7b or S7c.)
- *Postconditions:* `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`, where `#v ≥ 2` is *definitional* (the depth commitment for V-positions) and `zeros(v) = 0` together with componentwise positivity `(A i : 1 ≤ i ≤ #v : vᵢ > 0)` are *derived* from the element-field structural commitment (proof above).
- *Depends:* T0 (ASN-0034) — supplies the ℕ-valued component carrier on which `vᵢ ∈ ℕ` for every component; T4 (HierarchicalParsing, ASN-0034) — fixes the field-structural premises (non-separator components are strictly positive, each present field has at least one component); NAT-discrete (NatDiscreteness, ASN-0034) — discharges the positivity step: from `vᵢ ∈ ℕ` and `vᵢ ≠ 0` (the latter delivered by `zeros(v) = 0`), with `0` the least element of T0's carrier ℕ, NAT-discrete at `m = 0` excludes `vᵢ < 1`, yielding `vᵢ ≥ 1` and hence `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.

**subspace (V-position subspace identifier).** For any tumbler `v` of depth `#v ≥ 1`, define:

`subspace(v) = v₁`

extracting the subspace identifier as the first component. This is the definitional shorthand named in the prose under S7c (`subspace_I(a) = E(a)₁`), here given a standalone Formal Contract for V-positions.

*Formal Contract:*
- *Signature:* `subspace : T → ℕ` — projects the first component of a tumbler.
- *Preconditions:* `v ∈ T`, `#v ≥ 1` (so that `v₁` is well-defined as the first component of a non-empty tumbler).
- *Definition:* `subspace(v) = v₁`.
- *Postconditions:* (a) `subspace(v) ∈ ℕ` — the projected component inherits T0's ℕ-valued carrier (ASN-0034). (b) When `v` satisfies S8a, `subspace(v) ≥ 1` — S8a's componentwise positivity conjunct `(A i : 1 ≤ i ≤ #v : vᵢ > 0)` at `i = 1` delivers `v₁ ≥ 1`.
- *Depends:* T0 (ASN-0034) — ℕ-valued component carrier underwriting postcondition (a); S8a — componentwise positivity at `i = 1` underwriting postcondition (b). The function depends only on `#v ≥ 1`; subspace preservation under shift is established by OrdShiftHom (b) below.

**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

This is a design requirement, not a convention — parallel to S7a. Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth. Any correct implementation must satisfy this constraint.

*Formal Contract:*
- *Axiom (design requirement):* `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ subspace(v₁) = subspace(v₂) : #v₁ = #v₂)`.
- *Postconditions:* Within a subspace `s` of document `d`, there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`. Distinct subspaces may have distinct depths.
- *Depends:* S8a — for the lower bound `m_s ≥ 2`.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: position `s.x` is followed by `s.(x+1)` (where the `+1` is NAT addition on the ordinal component). A parallel uniformity holds for I-addresses within a correspondence run: all I-addresses in a run share the same tumbler depth and prefix, differing only at the element ordinal. This follows directly from TumblerAdd (PositionAdvance, ASN-0034): ordinal displacement `δ(k, m) = [0, ..., 0, k]` of length `m` has its action point at the last component, so TumblerAdd copies all earlier components from the start address unchanged (preserving the prefix) and produces a result of length `m` (preserving depth). The uniformity is definitional — a correspondence run `(v, a, n)` specifies `M(d)(shift(v, k)) = shift(a, k)`, and both `shift(v, k)` and `shift(a, k)` are ordinal displacements whose depth and prefix preservation follow from TumblerAdd's component-wise definition. Subspace preservation follows separately: for V-positions, the subspace identifier `v₁` is before the action point and is copied unchanged by TumblerAdd's prefix rule; for I-addresses, S7c guarantees element-field depth `δ ≥ 2`, so the subspace identifier `subspace_I(a)` is structural context outside the ordinal, and the shift acts on `[E(a)₂, ..., E(a)_δ]` without altering `subspace_I(a)`. We reserve the symbol `+` for NAT addition on components and indices throughout this ASN; tumbler ordinal displacement is always written as `shift(v, k)` (equivalently `v ⊕ δ(k, m)` per ASN-0034) — never as `v + k`.

(Why non-trivial runs arise in practice is a separate question. Allocator discipline — T10a, ASN-0034 — establishes that each allocator produces sibling outputs exclusively by `inc(·, 0)`, and TA5(c) guarantees the successor has the same depth as the predecessor. Consecutive allocations therefore produce consecutive I-addresses, which is why sequential content creation naturally yields correspondence runs of length greater than one. But this operational fact is motivation for the definition of correspondence runs, not a dependency of the decomposition proof.)

We extend `shift` to `k = 0` by convention: define `shift(v, 0) = v` (identity); for `k ≥ 1`, `shift(v, k) = v ⊕ δ(k, #v)` per OrdinalShift (ASN-0034). OrdinalShift's precondition is `n ≥ 1`; the extension to `k = 0` is purely notational — no arithmetic is performed. For I-addresses, `shift(a, 0) = a` and `shift(a, k) = a ⊕ δ(k, #a)` for `k ≥ 1`. This is well-defined: the action point of `δ(k, #a)` is `#a`, which falls at the element field's last component — S7c guarantees element-field depth `δ ≥ 2`, so the last component of the full address *is* the element ordinal's deepest position — and TumblerAdd's prefix rule copies all earlier components (node, user, document fields, their separators, and the subspace identifier) unchanged, producing a result of length `#a`.

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(shift(v, k)) = shift(a, k))`

At `k = 0` this is the base case `M(d)(v) = a`. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount. Within a correspondence run, each step forward in Vstream corresponds to the same step forward in Istream.

**S8 (Finite span decomposition).** For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the V-positions: every V-position in `dom(Σ.M(d))` falls in exactly one run — `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ)))`

(b) Within each run: `Σ.M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for all `k` with `0 ≤ k < nⱼ`

Each run represents a contiguous block of content that entered the arrangement as a unit — characters typed sequentially, or a span transcluded whole.

*Proof.* We construct a finite decomposition satisfying both conjuncts and prove it partitions `dom(M(d))`.

**Existence.** By S8-fin, `dom(M(d))` is finite. By S2 (ArrangementFunctionality), `M(d)` is a function, so each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)`. By S3 (referential integrity), `a ∈ dom(Σ.C)`. For each such `v`, form the singleton run `(v, a, 1)`. Conjunct (b) requires `M(d)(shift(v, k)) = shift(a, k)` for all `k` with `0 ≤ k < 1` — the only such `k` is `0`, where `shift(v, 0) = v` and `shift(a, 0) = a` by convention, so the identity reduces to `M(d)(v) = a`, which holds by construction. Since `dom(M(d))` is finite, the collection of singletons is finite.

**Corollary (subspace and field-structure preservation across a correspondence run).** This is not part of the existence argument and constructs no new run; it is a generic property of any correspondence run `(vⱼ, aⱼ, nⱼ)` satisfying S8's conjunct (b), recorded here so that decompositions arising from S8 or its operational refinements inherit it. Claim: for every `k` with `0 ≤ k < nⱼ`, the image `shift(aⱼ, k)` preserves three structural properties of `aⱼ` — (i) the I-address subspace identifier `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)`; (ii) the element-level zero-count `zeros(shift(aⱼ, k)) = zeros(aⱼ) = 3` (so `shift(aⱼ, k)` remains an element-level I-address, S7b); and (iii) the element-field depth `#E(shift(aⱼ, k)) = #E(aⱼ) = δⱼ ≥ 2` (so the depth bound of S7c is preserved).

*Proof.* By S3 (referential integrity) applied to `vⱼ ∈ dom(M(d))`, the image `aⱼ = M(d)(vⱼ) ∈ dom(Σ.C)`, so S7b and S7c apply to `aⱼ`. At `k = 0`, `shift(aⱼ, 0) = aⱼ` by convention and all three conclusions are immediate. For `k ≥ 1`, ShiftPreservation (above) applied pointwise to `aⱼ` and `k` yields (i) `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)`, (ii) `zeros(shift(aⱼ, k)) = 3`, and (iii) `#E(shift(aⱼ, k)) = #E(aⱼ) = δⱼ`. The conclusions are independent of the value of `k`, so they hold for every `k` with `1 ≤ k < nⱼ` regardless of run length. ∎

*Non-canonicality.* This is the *trivial decomposition*: every arrangement admits it, since singletons satisfy (a) and (b) by construction. S8 asserts existence of *some* finite decomposition, not minimum cardinality — coarser decompositions exist whenever consecutive `(vⱼ, aⱼ)` pairs admit the index-arithmetic identity `M(d)(shift(v, k)) = shift(a, k)` for `k > 0`, but their occurrence and preservation are determined by operations-layer behavior (whether allocations are consecutive, whether operations coalesce adjacent runs). The architectural discussion of `#runs(d)` below addresses typical operational regimes; the invariant itself does not commit to a canonical run count.

**Coverage.** Each `v ∈ dom(M(d))` lies in its own singleton's interval: `v ≤ v < shift(v, 1)`, where the right inequality holds because `shift(v, 1) > v` by TS4 (ShiftStrictIncrease, ASN-0034). So every V-position falls in at least one run.

**Uniqueness within a subspace.** Let `v, w ∈ dom(M(d))` be distinct V-positions with `v₁ = w₁ = S`. By S8-depth, `#v = #w = m` for some common depth `m`. We show `w ∉ [v, shift(v, 1))` via a clean lemma that abstracts away from the specific pair `(v, w)`.

*Setup for the lemma.* By S8a, `zeros(v) = 0`, so every component of `v` is nonzero. By definition, `shift(v, 1) = v ⊕ δ(1, m)`, where `δ(1, m)` is the unit displacement of depth `m` with action point at position `m` (OrdinalShift, ASN-0034). By TumblerAdd's length postcondition, `#shift(v, 1) = m`. By TumblerAdd's three-region component formula, components before the action point are copied from `v`: `shift(v, 1)ᵢ = vᵢ` for all `i < m`; at the action point, `shift(v, 1)_m = v_m + 1` (NAT addition on the last component, with `v_m + 1 ∈ ℕ` by NAT-closure; no carry, since tumbler addition is component-wise and the addition at position `m` does not propagate to other positions of the result).

By S8a, every V-position has depth `#v ≥ 2`, so `m ≥ 2`. (The depth-1 case `m = 1` is excluded by S8a: at `m = 1`, the only depth-1 tumbler with first component `S` is `[S]` itself by T3, so within-subspace uniqueness would hold vacuously — but S8a forbids depth 1 from occurring at all.)

**Within-subspace incompatibility lemma.** Let `v` be as above (a V-position with `v₁ = S`, `#v = m ≥ 2`, satisfying S8a). For any tumbler `t` with `t₁ = S`, `#t = m`, and `t ≠ v`: `t ∉ [v, shift(v, 1))`.

*Proof of lemma.* Suppose for contradiction that `t ∈ [v, shift(v, 1))`, i.e. `v ≤ t < shift(v, 1)`. Since `#t = #v = m`, the sequences diverge at some first position `j ≤ m`. The shared first component `t₁ = v₁ = S` forces `j ≥ 2`. At `m = 2` this further forces `j = m = 2`, leaving only Case j = m below; for `m ≥ 3`, both branches `2 ≤ j < m` and `j = m` are possible. Both branches yield contradictions.

*Case j < m.* Then `tᵢ = vᵢ` for `i < j`. The lemma's hypothesis `t ≠ v` combined with `v ≤ t` (from `t ∈ [v, shift(v, 1))`) strengthens to `v < t` — the non-strict relation `v ≤ t` resolves to strict `<` once equality is ruled out. T1(i) applied to `v < t` with first divergence at component `j` (valid since `j ≤ m = min(m, m)`) then yields `tⱼ > vⱼ`. Since `shift(v, 1)ⱼ = vⱼ` (as `j < m`), and `tᵢ = vᵢ = shift(v, 1)ᵢ` for `i < j`, the first divergence between `t` and `shift(v, 1)` is at position `j` with `tⱼ > shift(v, 1)ⱼ`, giving `t > shift(v, 1)` by T1(i) — contradicting `t < shift(v, 1)`.

*Case j = m.* Then `tᵢ = vᵢ` for `i < m`. Since `shift(v, 1)ᵢ = vᵢ` for `i < m` by TumblerAdd's prefix rule (the action point of `δ(1, m)` is `m`, so all components at positions `i < m` are copied from `v` unchanged), we get `tᵢ = shift(v, 1)ᵢ` for `i < m`, so the first divergence between `t` and `shift(v, 1)` is at position `m`. Since `tᵢ = vᵢ` for `i < m` and `t ≠ v` (with `#t = #v = m`), the divergence at `j = m` between `t` and `v` is also real: `t_m ≠ v_m`. Combined with `v ≤ t`, this gives `v < t`, and T1(i) applied to `v < t` with first divergence at `m` yields strict `t_m > v_m`; NAT-discrete (ASN-0034) at `(m, n) := (v_m, t_m)` promotes the strict inequality `v_m < t_m` to `v_m + 1 ≤ t_m`, i.e., `t_m ≥ v_m + 1`. From `t < shift(v, 1)` with first divergence at `m`: T1(i) gives `t_m < shift(v, 1)_m`, and the setup identity `shift(v, 1)_m = v_m + 1` (TumblerAdd at the action point; `v_m + 1 ∈ ℕ` by NAT-closure, ASN-0034) rewrites this to `t_m < v_m + 1`. But `t_m ≥ v_m + 1` and `t_m < v_m + 1` are incompatible by NAT-order's exactly-one trichotomy (ASN-0034), instantiated at `(t_m, v_m + 1)` — the clause `¬(a < b ∧ b ≤ a)` excludes the conjunction of the two inequalities. Contradiction. ∎ *(lemma)*

*Application to w.* The hypotheses `w₁ = v₁ = S`, `#w = m` (S8-depth), and `w ≠ v` are exactly the lemma's antecedents, so `w ∉ [v, shift(v, 1))`. Since all V-positions in subspace `S` share depth `m` (S8-depth) and the lemma applies to every such position distinct from `v`, no distinct V-position in the same subspace falls in `v`'s singleton interval.

*Remark.* S8-depth is essential. Without it, `dom(M(d))` could contain `s.3` (depth 2) and `s.3.1` (depth 3). By T1(ii), `s.3 < s.3.1` (prefix extension), and by T1(i) at position 2, `s.3.1 < s.4`. The position `s.3.1` would fall in the singleton interval of both `s.3` and `s.3.1` — violating unique partition.

**Uniqueness across subspaces.** Let `v ∈ dom(M(d))` with `v₁ = S₁` and `w ∈ dom(M(d))` with `w₁ = S₂`, where `S₁ ≠ S₂`. By S8a, `v` and `w` extend the single-component prefixes `[S₁]` and `[S₂]` respectively, and both have depth `≥ 2`. These prefixes are non-nesting: `[S₁] ≼ [S₂]` would require `S₁ = S₂` (both length-1 tumblers, so equality requires componentwise agreement by T3), contradicting `S₁ ≠ S₂`; symmetrically `[S₂] ⋠ [S₁]`.

(The depth-1 case `m = 1` is excluded by S8a — V-positions of depth 1 do not occur. Were they permitted, each subspace would contain at most one depth-1 V-position `[S]`, with cross-subspace uniqueness following from T1(i): tumblers extending `[S₁]` cannot equal tumblers extending the distinct prefix `[S₂]`.)

For `m ≥ 2` (the only case under S8a), the successor `shift(v, 1)` also extends `[S₁]`: by OrdinalShift (ASN-0034), `shift(v, 1) = v ⊕ δ(1, m)`, and since `δ(1, m)` has action point `m`, TumblerAdd's prefix rule (ASN-0034) copies every component at positions `i < m` from `v` unchanged. Since `m ≥ 2`, this includes position 1, giving `shift(v, 1)₁ = v₁ = S₁`.

Since `[S₁] ≼ v` and `[S₁] ≼ shift(v, 1)` and `v ≤ shift(v, 1)` by TS4 (ShiftStrictIncrease, ASN-0034), T5 (ContiguousSubtrees, ASN-0034) gives: for any `t` with `v ≤ t ≤ shift(v, 1)`, `[S₁] ≼ t`. Every element of `[v, shift(v, 1))` therefore extends `[S₁]`. By T10 (ASN-0034), since `[S₁]` and `[S₂]` are non-nesting prefixes, any tumbler extending `[S₁]` is distinct from any tumbler extending `[S₂]`. In particular, `w` (which extends `[S₂]`) cannot belong to `[v, shift(v, 1))`.

**Conclusion.** The singleton runs cover every V-position in `dom(M(d))` (coverage) and no V-position falls in two distinct singleton intervals (uniqueness within and across subspaces). The singletons partition `dom(M(d))`. Since `dom(M(d))` is finite (S8-fin), the decomposition is finite, establishing both conjuncts (a) and (b). ∎

*Formal Contract:*
- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); referential integrity (S3); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` (S8a); within each subspace, all V-positions share a common depth (S8-depth); I-addresses are element-level with `zeros(a) = 3` (S7b) and have element-field depth `#E(a) ≥ 2` (S7c); S7b and S7c are preconditions of the run-corollary (via ShiftPreservation), not of the existence claim.
- *Postconditions:* (*Existence.*) There exists a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` satisfying (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ)))` and (b) `(A j, k : 0 ≤ k < nⱼ : M(d)(shift(vⱼ, k)) = shift(aⱼ, k))`. The proof exhibits the singleton decomposition (every `nⱼ = 1`), for which conjunct (b) reduces to the base case `M(d)(vⱼ) = aⱼ` at `k = 0`. (*Corollary (subspace and field-structure preservation across a run).*) For any correspondence run `(vⱼ, aⱼ, nⱼ)` satisfying conjunct (b), every image `shift(aⱼ, k)` with `0 ≤ k < nⱼ` preserves three structural properties of `aⱼ`: (i) `subspace_I(shift(aⱼ, k)) = subspace_I(aⱼ)`; (ii) `zeros(shift(aⱼ, k)) = zeros(aⱼ) = 3` (S7b inherited); (iii) `#E(shift(aⱼ, k)) = #E(aⱼ) = δⱼ ≥ 2` (S7c bound preserved). At `k = 0` all three conclusions are immediate (the shift is the identity); for `k ≥ 1` the conclusions follow from ShiftPreservation (above) applied pointwise to `aⱼ ∈ dom(Σ.C)` (S3 supplies this membership) and each such `k`.
- *Depends:* (*Local properties*) S2 (ArrangementFunctionality) — each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)` for the singleton-run construction; S3 (referential integrity) — places `M(d)(v) ∈ dom(Σ.C)`, supplying ShiftPreservation's precondition for the run-corollary; S7b (Element-level I-addresses) and S7c (Element-field depth) — required by ShiftPreservation, which the run-corollary cites pointwise; ShiftPreservation (above) — supplies, for each `aⱼ ∈ dom(Σ.C)` and each `k ≥ 1`, the three structural-preservation conclusions that the run-corollary aggregates across `k ∈ {0, …, nⱼ − 1}` of any correspondence run; S8a — supplies `zeros(v) = 0` and `#v ≥ 2` for the within-subspace incompatibility lemma (the lemma's two-case analysis on the first divergence position needs `m ≥ 2` and `v_m > 0`); S8-depth — gives a common depth `m` to every V-position in a fixed subspace, enabling the uniqueness-within-a-subspace argument; S8-fin — finite `dom(M(d))` gives a finite singleton family. (*Foundation claims, ASN-0034*) T1 (TumblerOrdering) case (i) — first-divergence comparison powering the within- and across-subspace incompatibility lemmas; T3 (CanonicalRepresentation) — equates tumblers with their canonical component sequences; T4 (HierarchicalParsing) — partitions tumblers into N/U/D/E fields; T5 (ContiguousSubtrees) — shows that every element of `[v, shift(v, 1))` extends `[v₁]`, sealing the cross-subspace uniqueness step; T10 — non-nesting prefixes generate disjoint tumbler subtrees, ruling out cross-subspace overlap; TS4 (ShiftStrictIncrease) — `v < shift(v, 1)`, witnessing both the singleton-interval inclusion and the existence of a proper successor; TumblerAdd, OrdinalShift, OrdinalDisplacement — supply the action-point semantics of `δ(k, m)` and the three-region component formula; the action-point identity `shift(v, 1)_m = v_m + 1` underwrites the divergence step in the Case `j = m` branch of the within-subspace incompatibility lemma. NAT-discrete (NatDiscreteness) — supplies the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n`, instantiated at `(v_m, t_m)` in the Case `j = m` branch of the within-subspace incompatibility lemma to convert `v_m < t_m` (from T1(i)) to `t_m ≥ v_m + 1`. NAT-closure (NatArithmeticClosureAndIdentity) — closure of ℕ under addition places `v_m + 1` in ℕ, so the strict comparison `t_m < v_m + 1` is between two ℕ-elements. NAT-order (NatStrictTotalOrder) — supplies the exactly-one trichotomy clause `¬(a < b ∧ b ≤ a)` instantiated at `(t_m, v_m + 1)` that delivers the contradiction in the Case `j = m` branch of the within-subspace incompatibility lemma from the conjunction `t_m < v_m + 1 ∧ t_m ≥ v_m + 1`. (The NAT-discrete, NAT-closure, NAT-addcompat, and NAT-order roles that underwrite the run-corollary's `k ≥ 1` content are charged to ShiftPreservation, not duplicated here.)

What matters architecturally is that the number of runs `#runs(d)` is typically far smaller than `|dom(M(d))|` — the representation cost is proportional to the number of editing events, not the document size. Non-trivial runs arise when consecutive allocations produce consecutive I-addresses (as T10a and TA5(c) ensure operationally). Editing can both split and remove runs — inserting content in the middle of a run splits it into two, while deleting an entire run's V-span removes it. The number of distinct Istream allocation events underlying a document's history is monotonically non-decreasing (by S1), but the current arrangement's run count fluctuates with editing.

The run count drives V↔I translation cost — each correspondence run requires an independent tree traversal — so any implementation of the two-stream architecture must either consolidate adjacent runs or accept translation cost proportional to the fragmentation level.


## V-position ordinal decomposition

S8a establishes V-positions as element-field tumblers whose first component is the subspace identifier (subspace(v) = v₁), and the ordinal-only formulation of TA7a (ASN-0034) establishes that within-subspace arithmetic passes only the ordinal to the operations while holding the subspace identifier as structural context. We now formalize this decomposition with concrete extraction and reconstruction functions: separating a V-position into its subspace identifier and its within-subspace ordinal, reconstructing a V-position from these components, and projecting a displacement onto its ordinal component. We then establish the central property: tumbler addition commutes with the decomposition, and derive from this that TA7a's closure guarantees on S govern the S-membership of the result.

**ord(v)** — *OrdinalExtraction* (DEF, function). For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier. When v satisfies S8a, every component of v is positive, so every component of [v₂, ..., vₘ] is positive — placing ord(v) in TA7a's domain S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.

*Instance.* For `v = [1, 3, 5]` (text-subspace identifier `v₁ = 1`, depth `m = 3`, satisfying S8a), `ord(v) = [3, 5]`. The leading subspace identifier 1 is stripped; the remaining length-2 tumbler `[3, 5]` has both components positive, so `ord(v) ∈ S`.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v ≥ 2`.
- *Definition:* `ord(v) = [v₂, ..., vₘ]` where `m = #v`.
- *Postconditions:* `ord(v) ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#ord(v) = #v - 1`. When `v` satisfies S8a, `ord(v) ∈ S` — every component of `[v₂, ..., vₘ]` is positive since every component of `v` is positive by S8a's componentwise positivity conjunct `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.
- *Depends:* T0 (ℕ-valued carrier, ASN-0034); TA7a (ordinal-only formulation, ASN-0034) — defines the codomain S; S8a (V-position well-formedness) — for the S-membership postcondition.
- *Frame:* Pure function on the component sequence of `v` — no state is read or modified.

**vpos(S, o)** — *VPositionReconstruction* (DEF, function). For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with #vpos(S, o) = k + 1. These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

*Instance.* Continuing the example above with `v = [1, 3, 5]`, `ord(v) = [3, 5]`. Reconstructing with the text-subspace identifier: `vpos(subspace(v), ord(v)) = vpos(1, [3, 5]) = [1, 3, 5] = v`. The inverse property (b) is exhibited concretely on this instance.

*Formal Contract:*
- *Preconditions:* `S ∈ ℕ`, `o ∈ T`, `#o ≥ 1`.
- *Definition:* `vpos(S, o) = [S, o₁, ..., oₖ]` where `k = #o`.
- *Postconditions:* `vpos(S, o) ∈ T`, `#vpos(S, o) = #o + 1`, `vpos(S, o)₁ = S`. (a) `ord(vpos(S, o)) = o` — since `vpos(S, o) = [S, o₁, ..., oₖ]`, stripping the first component recovers `[o₁, ..., oₖ] = o`. (b) For any `v ∈ T` with `#v ≥ 2`: `vpos(subspace(v), ord(v)) = v` — since `subspace(v) = v₁` and `ord(v) = [v₂, ..., vₘ]`, reconstruction gives `[v₁, v₂, ..., vₘ] = v`. Both inverse properties are pure sequence identities that hold unconditionally on T. When `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)`, the result satisfies S8a: `zeros(vpos(S, o)) = 0` (no component is zero — `S ≥ 1` covers component 1 and each `oᵢ > 0` covers components 2 through `k + 1`), `#vpos(S, o) = k + 1 ≥ 2` (since `k = #o ≥ 1`), and `(A i : 1 ≤ i ≤ #vpos(S, o) : vpos(S, o)ᵢ > 0)` (componentwise positivity, by the same component-by-component argument).
- *Depends:* T0 (ℕ-valued carrier, ASN-0034); ord (definition above) — for the inverse property (a); S8a — for the satisfies-S8a postcondition.
- *Frame:* Pure function on `S` and the component sequence of `o` — no state is read or modified.

**w_ord** — *OrdinalDisplacementProjection* (DEF, function). For a displacement w with `w₁ = 0` and `#w = m ≥ 2`, the *ordinal projection* is:

`w_ord = [w₂, ..., wₘ]`

of length m − 1. The condition `w₁ = 0` is structurally necessary: it ensures `actionPoint(w) ≥ 2`, so by TumblerAdd all positions before the action point are copied from the operand — position 1 (the subspace identifier) is preserved by any addition `v ⊕ w`. This is the mechanism by which arithmetic stays within a subspace. At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c].

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `#w ≥ 2`, `w₁ = 0`.
- *Definition:* `w_ord = [w₂, ..., wₘ]` where `m = #w`.
- *Postconditions:* `w_ord ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#w_ord = #w - 1`. When `Pos(w)` (TA-Pos, ASN-0034), `Pos(w_ord)` — since `w₁ = 0`, the witness `wᵢ ≠ 0` required by `Pos(w)` must have `i ≥ 2`, and this component appears in `w_ord`. When `Pos(w)`: `actionPoint(w_ord) = actionPoint(w) - 1`.
- *Depends:* T0 (ℕ-valued carrier, ASN-0034); TumblerAdd (ASN-0034) — for the `actionPoint` relationship.
- *Frame:* Pure function on the component sequence of `w` — no state is read or modified.

The definitions above decompose V-positions into subspace context and ordinal operand. We now establish that the decomposition is structure-preserving: tumbler addition commutes with extraction. This is the property that makes the definitions more than naming conventions — it connects V-position arithmetic to TA7a's closure guarantees on S.

**OrdAddHom** — *OrdinalAdditionHomomorphism* (LEMMA). For a V-position `v` with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, and `Pos(w)` (TA-Pos, ASN-0034):

`ord(v ⊕ w) = ord(v) ⊕ w_ord`

*Proof.* Let `k = actionPoint(w)`. Since `w₁ = 0`, we have `k ≥ 2`. By TumblerAdd, the result `r = v ⊕ w` is built component-wise in three regions:

- For `1 ≤ i < k`: `rᵢ = vᵢ` (copy from start).
- At `i = k`: `rₖ = vₖ + wₖ` (single-component advance).
- For `k < i ≤ m`: `rᵢ = wᵢ` (copy from displacement).

*Part (a) — ordinal homomorphism.* So `ord(v ⊕ w) = [r₂, ..., rₘ] = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`.

For the right-hand side, `w_ord = [w₂, ..., wₘ]` has `actionPoint(w_ord) = k - 1`, since `(w_ord)ⱼ = w_{j+1}` and the first nonzero `w_{j+1}` occurs at `j + 1 = k`, i.e. `j = k - 1`. The application is well-defined: `actionPoint(w_ord) = k − 1 ≤ m − 1 = #ord(v)`, since `k ≤ m` by precondition. By TumblerAdd for `ord(v) ⊕ w_ord`:

- For `1 ≤ j < k-1`: `(ord(v) ⊕ w_ord)ⱼ = ord(v)ⱼ = v_{j+1}`.
- At `j = k-1`: `(ord(v) ⊕ w_ord)_{k-1} = ord(v)_{k-1} + (w_ord)_{k-1} = vₖ + wₖ`.
- For `k-1 < j ≤ m-1`: `(ord(v) ⊕ w_ord)ⱼ = (w_ord)ⱼ = w_{j+1}`.

The boundary regimes of `k` collapse one or both copy regions to the empty range: at `k = 2`, the first range `1 ≤ j < k-1` reduces to `1 ≤ j < 1` and is empty (no prefix copy); at `k = m`, the third range `k-1 < j ≤ m-1` reduces to `m-1 < j ≤ m-1` and is empty (no tail copy). The two-sided enumeration above is vacuously correct in either boundary case — the non-empty regions still match component by component, and the empty range contributes nothing on either side.

So `ord(v) ⊕ w_ord = [v₂, ..., v_{k-1}, vₖ + wₖ, w_{k+1}, ..., wₘ]`. The two sequences are identical component by component, establishing `ord(v ⊕ w) = ord(v) ⊕ w_ord`.

*Part (b) — subspace preservation.* Since `k ≥ 2`, the copy-from-start region `1 ≤ i < k` includes position `i = 1`, giving `r₁ = v₁`. By definition `subspace(r) = r₁` and `subspace(v) = v₁`, so `subspace(v ⊕ w) = r₁ = v₁ = subspace(v)`.

*Part (c) — full decomposition.* By TA0 (ASN-0034), `#r = #w = m ≥ 2`, so the generalized inverse property of vpos (vpos contract (b)) applies to `r`: `vpos(subspace(r), ord(r)) = r`. Substituting `subspace(r) = subspace(v)` from part (b) and `ord(r) = ord(v) ⊕ w_ord` from part (a) gives `r = vpos(subspace(v), ord(v) ⊕ w_ord)`, i.e. `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`. Note that `ord(v) ⊕ w_ord` need not lie in S — the definition and inverse properties of vpos are pure sequence operations holding for any `o ∈ T`. ∎

*Instance (a).* Let `v = [1, 3, 5]`, `w = [0, 0, 2]` (action point 3). Then `v ⊕ w = [1, 3, 7]` and `ord([1, 3, 7]) = [3, 7]`. On the right, `ord(v) = [3, 5]` and `w_ord = [0, 2]`, giving `[3, 5] ⊕ [0, 2] = [3, 7]`. Both sides agree.

*Instance (b).* Let `v = [1, 3, 5]`, `w = [0, 4, 0]` (action point 2). Then `v ⊕ w = [1, 7, 0]` and `ord([1, 7, 0]) = [7, 0]`. On the right, `ord(v) = [3, 5]` and `w_ord = [4, 0]`, giving `[3, 5] ⊕ [4, 0] = [7, 0]`. Both sides agree. Note that `[7, 0] ∉ S` — the zero in the tail component after the action point places the result outside TA7a's domain S, illustrating the S-membership boundary.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`. (The bound `actionPoint(w) ≤ m` is not stated separately: ActionPoint's contract in ASN-0034 already gives `1 ≤ actionPoint(w) ≤ #w`, and `#w = m` then forces `actionPoint(w) ≤ m`.)
- *Postconditions:* (a) `ord(v ⊕ w) = ord(v) ⊕ w_ord`. (b) `subspace(v ⊕ w) = subspace(v)`. (c) `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`. (Derivations of (b) and (c) are given in the proof body above.)
- *Depends:* ord, w_ord, vpos (definitions above); TumblerAdd (PositionAdvance, ASN-0034) — the three-region component formula; TA0 (length preservation, ASN-0034) — for part (c); ActionPoint (ASN-0034) — for the implicit `actionPoint(w) ≤ m` bound.
- *Frame:* Both sides are computed from `v` and `w` alone — no state is consulted.

**OrdAddS8a** — *AdditionPreservesS8a* (LEMMA). For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `Pos(w)` (TA-Pos, ASN-0034): `v ⊕ w` satisfies S8a if and only if all components of `w_ord` after its action point are positive.

*Proof.* Let `r = v ⊕ w` with `k = actionPoint(w) ≥ 2`. By TumblerAdd, the components of `r` partition into three regions:

- `r₁ = v₁ ≥ 1` (by S8a on `v`, and `w₁ = 0` so `1 < k` and TumblerAdd copies from `v`).
- For `2 ≤ i < k`: `rᵢ = vᵢ ≥ 1` (by S8a on `v`).
- At `i = k`: `rₖ = vₖ + wₖ ≥ 1 + 1 = 2`. From `vₖ ≥ 1` (S8a on `v`) and `wₖ ≥ 1` (ActionPoint's minimum-nonzero clause for the action-point component, ASN-0034), NAT-addcompat (left and right order compatibility) and NAT-order's ≤-transitivity Consequence give the chain `1 + 1 ≤ vₖ + 1 ≤ vₖ + wₖ`: right compatibility at `(m, n, p) = (1, vₖ, 1)` lifts `1 ≤ vₖ` to `1 + 1 ≤ vₖ + 1`, then left compatibility at `(m, n, p) = (vₖ, wₖ, 1)` lifts `1 ≤ wₖ` to `vₖ + 1 ≤ vₖ + wₖ`, and ≤-transitivity closes the chain into `vₖ + wₖ ≥ 1 + 1 = 2`.
- For `k < i ≤ m`: `rᵢ = wᵢ` (copied from the displacement).

The boundary regimes of `k` collapse one or both side regions to the empty range: at `k = 2`, the middle range `2 ≤ i < k` reduces to `2 ≤ i < 2` and is empty (no interior prefix-copy components beyond `r₁`); at `k = m`, the trailing range `k < i ≤ m` reduces to `m < i ≤ m` and is empty (no tail components past the action point). The case analysis remains correct under these collapses — empty ranges contribute nothing, and the unconditionally positive components stay unconditionally positive.

Components `r₁` through `rₖ` are unconditionally positive. S8a requires `zeros(r) = 0` and `(A i : 1 ≤ i ≤ #r : rᵢ > 0)`, which reduces to: every component is positive. The only components that can fail are `r_{k+1}, ..., r_m = w_{k+1}, ..., w_m` — exactly the tail components of `w`, which are the tail components of `w_ord` (since `(w_ord)_j = w_{j+1}` and the action point of `w_ord` is `k - 1`). Therefore:

`v ⊕ w satisfies S8a ⟺ (A i : k < i ≤ m : wᵢ > 0) ⟺ all tail components of w_ord are positive`

We now establish the second equivalence `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a` directly, in three explicit steps.

(a) *S8a on `v ⊕ w` reduces to componentwise positivity.* By TumblerAdd's length postcondition (TA0, ASN-0034), `#(v ⊕ w) = m ≥ 2`. With the depth lower bound satisfied, the remaining S8a conjuncts `zeros(v ⊕ w) = 0` and `(A i : 1 ≤ i ≤ m : (v ⊕ w)ᵢ > 0)` collapse to a single requirement: every component of `v ⊕ w` is strictly positive.

(b) *Position 1 is positive unconditionally.* The hypothesis `w₁ = 0` excludes `actionPoint(w) = 1` (the action point is the first nonzero position of `w`), forcing `actionPoint(w) ≥ 2`. Position 1 therefore lies strictly before the action point, and TumblerAdd's prefix-copy region copies it from `v`: `(v ⊕ w)₁ = v₁`. By S8a on `v`, `v₁ > 0`. Hence `(v ⊕ w)₁ > 0` independently of `w`.

(c) *Equivalence chain.* Combining (a) and (b), S8a on `v ⊕ w` collapses to positivity of positions 2 through `m`:

`v ⊕ w satisfies S8a ⟺ (A i : 2 ≤ i ≤ m : (v ⊕ w)ᵢ > 0) ⟺ (A j : 1 ≤ j ≤ m − 1 : ord(v ⊕ w)ⱼ > 0) ⟺ ord(v ⊕ w) ∈ S`

The middle equivalence is the reindexing `j = i − 1` together with the definition `ord(v ⊕ w) = [(v ⊕ w)₂, …, (v ⊕ w)_m]`; the final equivalence is the definition of `S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}`, where the length condition `#ord(v ⊕ w) = m − 1 ≥ 1` follows from `m ≥ 2`.

The displacement-tail characterization derived earlier is the same constraint viewed through OrdAddHom: `ord(v ⊕ w) = ord(v) ⊕ w_ord`, and since `ord(v) ∈ S` (componentwise positive by S8a on `v`), `ord(v ⊕ w) ∈ S` reduces to whether `w_ord`'s tail past its action point is positive — exactly the condition on `(A i : k < i ≤ m : wᵢ > 0)` derived above. Instance (b) above confirms the boundary: `w_ord = [4, 0]` has a zero after the action point, and `v ⊕ w = [1, 7, 0]` fails S8a. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`. (The bound `actionPoint(w) ≤ m` is not stated separately: ActionPoint's contract in ASN-0034 already gives `1 ≤ actionPoint(w) ≤ #w`, and `#w = m` then forces `actionPoint(w) ≤ m`.)
- *Postconditions:* `v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`.
- *Depends:* OrdAddHom (lemma above); TumblerAdd (PositionAdvance, ASN-0034) — three-region component formula; ActionPoint (ASN-0034) — for the implicit `actionPoint(w) ≤ m` bound and the minimum-nonzero clause `w_{actionPoint(w)} ≥ 1` that supplies `wₖ ≥ 1` at the action-point component; S8a (V-position well-formedness) — supplies `vₖ ≥ 1` at the action-point component; NAT-addcompat (NatAdditionOrderAndSuccessor, ASN-0034) — left and right order compatibility, instantiated at `(m, n, p) = (1, vₖ, 1)` (right) and `(m, n, p) = (vₖ, wₖ, 1)` (left) to combine `vₖ ≥ 1` and `wₖ ≥ 1` into the chain `1 + 1 ≤ vₖ + 1 ≤ vₖ + wₖ` underwriting `rₖ ≥ 2`; NAT-order (NatStrictTotalOrder, ASN-0034) — supplies the ≤-transitivity Consequence that closes this chain into `rₖ = vₖ + wₖ ≥ 1 + 1 = 2`.

**OrdShiftHom** — *OrdinalShiftHomomorphism* (COROLLARY). For a V-position `v` with `#v = m ≥ 2` and `n ≥ 1`:

`ord(shift(v, n)) = shift(ord(v), n)`

Since `shift(v, n) = v ⊕ δ(n, m)` and `δ(n, m) = [0, ..., 0, n]` has `δ(n, m)₁ = 0` (well-defined since `#δ(n, m) = m ≥ 2`), OrdAddHom applies. Its part (a) gives the ordinal identity: the ordinal projection `(δ(n, m))_ord = [0, ..., 0, n]` of length `m - 1` is `δ(n, m-1)`, so `ord(v ⊕ δ(n, m)) = ord(v) ⊕ δ(n, m-1) = shift(ord(v), n)`. Its part (b), instantiated at `w = δ(n, m)`, gives `subspace(v ⊕ δ(n, m)) = subspace(v)`, i.e. `subspace(shift(v, n)) = subspace(v)` — the shift operation preserves the subspace identifier. ∎

*Instance.* Let `v = [1, 3, 5]` (satisfying S8a, depth `m = 3`) and `n = 2`. The shift is computed left-to-right: `shift(v, 2) = v ⊕ δ(2, 3) = [1, 3, 5] ⊕ [0, 0, 2] = [1, 3, 7]` (TumblerAdd's action point is 3, so components 1 and 2 are copied from `v`, and component 3 receives `5 + 2 = 7`). All three postconditions exhibit on this instance:
- *(a) Ordinal homomorphism.* `ord(shift(v, 2)) = ord([1, 3, 7]) = [3, 7]`; on the right, `ord(v) = [3, 5]` and `shift(ord(v), 2) = [3, 5] ⊕ δ(2, 2) = [3, 5] ⊕ [0, 2] = [3, 7]` (action point 2, component 1 copied, component 2 receives `5 + 2 = 7`). Both sides equal `[3, 7]`.
- *(b) Subspace preservation.* `subspace(shift(v, 2)) = [1, 3, 7]₁ = 1 = v₁ = subspace(v)`.
- *(c) S8a preservation.* `[1, 3, 7]` has `zeros = 0` and every component positive (`1, 3, 7 ≥ 1`), with depth `3 ≥ 2`, so S8a holds on `shift(v, 2)` — unconditionally, since `δ(2, 3)` has its only nonzero component at the last position with no tail beyond.

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`, `n ≥ 1`.
- *Postconditions:* (a) `ord(shift(v, n)) = shift(ord(v), n)`. (b) `subspace(shift(v, n)) = subspace(v)` — derived from OrdAddHom (b) at `w = δ(n, m)`, whose `w₁ = 0` holds because `#δ(n, m) = m ≥ 2`. (c) When `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally — since `δ(n, m) = [0, ..., 0, n]` has action point `m` with no tail components beyond, the OrdAddS8a condition is vacuously satisfied.
- *Depends:* OrdAddHom (lemma above), OrdAddS8a (lemma above), OrdinalShift (ASN-0034), OrdinalDisplacement (ASN-0034).


## Arrangement contiguity

Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." This statement is specific to the text subspace (S = 1), where Nelson's "addresses 1 through 100" describes character positions. The link subspace (S = 2) has different structural semantics — link addresses are sparse and append-only, with deleted links marked by tombstones rather than ordinal renumbering. We formalize the text-subspace contiguity properties below as constraints on V-position sets within the text subspace; link-subspace contiguity semantics are deferred to a future ASN.

Write `S = subspace(v) = v₁` for the subspace identifier (the first component of the element-field V-position), and `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` for the set of V-positions in subspace S of document d. The specialization to the text subspace is `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}`. All V-positions in a given subspace share the same tumbler depth (S8-depth). The properties D-CTG, D-MIN, D-CTG-depth, and D-SEQ below bind `S = 1` directly in their formal statements — the architectural design constraint imposed by this ASN applies only to the text subspace; they are not claimed to hold for the link subspace `S = 2` or any other subspace. The underlying reasoning is parametric in S — should the constraints be extended to another subspace in future work, the proofs would apply with the obvious substitution `1 ↦ S` — but the formal contracts here are written for `S = 1`.

**D-CTG (VContiguity).** For each document d, V_1(d) (the text subspace) is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`

In words: within the text subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

*Formal Contract:*
- *Axiom (design requirement, text-subspace only):* `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`.
- *Preconditions:* `subspace(v) = 1` (text subspace); V-positions share a common depth (S8-depth).
- *Postconditions:* V_1(d) is either empty or occupies every position strictly between its extremes (at the fixed text-subspace depth).
- *Frame:* D-CTG is a constraint on well-formed text-subspace arrangements; preservation across editing operations is each operation's verification obligation.
- *Depends:* S8a (V-position well-formedness); S8-depth (common depth within subspace); T1 (TumblerOrdering, ASN-0034) — defines the order.

For the text subspace at depth m = 2, this is a finite condition: the intermediates between [1, a] and [1, b] are the finitely many [1, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_1(d) occupies a single unbroken block of ordinals.

At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction: all positions in V_1(d) must share components 2 through m − 1. The intuition — formalized as D-CTG-depth and proved below — is that if two positions diverged before the last component, then any choice of natural number n could be slotted into the next component to yield an intermediate; D-CTG would force all such intermediates into V_1(d), producing infinitely many positions and contradicting S8-fin.

**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_1(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_1(d) be non-empty with common depth `m` (S8-depth) and `m ≥ 3` (the lemma's non-triviality bound, supplied as an additional precondition rather than by S8-depth — S8-depth on its own guarantees only `m ≥ 2`, inherited from S8a). Suppose for contradiction that V_1(d) contains two positions v₁ and v₂ with v₁ < v₂ (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j, and (v₁)ⱼ < (v₂)ⱼ (the inequality follows from v₁ < v₂ by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

We construct infinitely many intermediates. For any natural number n > (v₁)ⱼ₊₁, define w of length m by:

- wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j (agreeing with v₁ on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (an empty range when j = m − 1, in which case wⱼ₊₁ = w_m is already the last component; otherwise this clause fills components j + 2 through m).

Then w has depth m (it has m components by construction), and subspace(w) = w₁ = (v₁)₁ = 1 (since j ≥ 2, the first component is copied from v₁). We verify v₁ < w < v₂:

- **w > v₁**: w agrees with v₁ on components 1 through j. At component j + 1, wⱼ₊₁ = n > (v₁)ⱼ₊₁. Since j + 1 ≤ m = min(m, m), by T1(i), w > v₁.
- **w < v₂**: w agrees with v₂ on components 1 through j − 1 (since v₁ and v₂ agree on these components by the definition of j). At component j, wⱼ = (v₁)ⱼ < (v₂)ⱼ. Since j ≤ m − 1 ≤ min(m, m), by T1(i), w < v₂.

We also verify that w satisfies S8a — necessary because D-CTG ranges over V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a. By construction, every component of w is at least 1: wᵢ = (v₁)ᵢ ≥ 1 for i ≤ j by S8a applied to v₁; wⱼ₊₁ = n > (v₁)ⱼ₊₁ ≥ 1 (again by S8a on v₁); and wᵢ = 1 for j + 2 ≤ i ≤ m. Hence zeros(w) = 0 and `(A i : 1 ≤ i ≤ #w : wᵢ > 0)`. Combined with #w = m ≥ 3 ≥ 2, w satisfies S8a — so the candidate w qualifies for D-CTG's consequent.

Since v₁ < w < v₂, subspace(w) = 1, #w = m = #v₁, and w satisfies S8a, D-CTG requires w ∈ V_1(d). We now exhibit infinitely many admissible values of n. T0(a) (UnboundedComponentValues, ASN-0034) supplies, for any natural-number bound M, one witness n ∈ ℕ with n > M. Iterating: starting from M₀ = (v₁)ⱼ₊₁, T0(a) supplies n₁ > M₀; setting M₁ = n₁, T0(a) supplies n₂ > M₁ ≥ n₁; continuing, we obtain a strictly increasing sequence n₁ < n₂ < n₃ < … of natural numbers, all exceeding (v₁)ⱼ₊₁. The sequence is infinite and pairwise distinct. Distinct values of n yield distinct tumblers w (they differ at component j + 1, so by T3, CanonicalRepresentation, ASN-0034, they are unequal). This produces infinitely many distinct positions in V_1(d), contradicting S8-fin (dom(M(d)) is finite).

Therefore no two positions in V_1(d) can disagree at any component j with 2 ≤ j ≤ m − 1. All positions share components 2 through m − 1, and contiguity reduces to contiguity of the last component (component m) alone. ∎

*Formal Contract:*
- *Preconditions:* V_1(d) non-empty; common depth `m` within the text subspace (S8-depth); `m ≥ 3` (the lemma's non-triviality bound, additional to S8-depth — at `m = 2` the conclusion holds vacuously since the range of shared components 2 through `m − 1` is empty).
- *Postconditions:* `(A v₁, v₂ ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of V_1(d) reduces to contiguity of the m-th (last) component.
- *Depends:* (*Local properties*) D-CTG (VContiguity) — supplies the contradiction step: the constructed intermediate `w` is strictly between `v₁` and `v₂` in subspace 1 at depth `m`, and D-CTG forces `w ∈ V_1(d)`; S8a — gives `m ≥ 2` and the positivity that makes the construction of `w` (with components copied from `v₁` and a free choice at position `j + 1`) yield a tumbler with `subspace(w) = 1` and `zeros(w) = 0`; S8-depth — guarantees `#w = #v₁ = m`, the precondition for T1's first-divergence comparison to operate at a common depth; S8-fin — the finiteness obligation that the infinitely many intermediates would contradict, closing the proof. (*Foundation claims, ASN-0034*) T0(a) (UnboundedComponentValues) — supplies, for any bound `M`, a natural-number witness `n > M`, generating the strictly increasing sequence of admissible intermediates; T1 case (i) (TumblerOrdering) — first-divergence comparison certifying `v₁ < w < v₂` at the chosen divergence position; T3 (CanonicalRepresentation) — distinct component sequences yield distinct tumblers, so the strictly increasing sequence of `n` values yields pairwise distinct `w`'s in `V_1(d)`.

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

**D-MIN (VMinimumPosition).** For each document d with V_1(d) non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in the text subspace per S8-depth), and every component is 1.

At depth 2 this gives min(V_1(d)) = [1, 1]. Combined with D-CTG and S8-fin, a document with n text elements occupies V-positions [1, 1] through [1, n] — matching Nelson's "addresses 1 through 100."

*Formal Contract:*
- *Axiom (design requirement, text-subspace only):* `V_1(d) ≠ ∅ ⟹ min(V_1(d)) = [1, 1, ..., 1]` of length `m_1` (the common depth of the text subspace per S8-depth).
- *Preconditions:* V_1(d) non-empty; common text-subspace depth `m_1` (S8-depth) with `m_1 ≥ 2` (S8a).
- *Postconditions:* Every component of `min(V_1(d))` equals 1; in particular the text subspace identifier `min(V_1(d))₁ = 1` and the within-subspace ordinal starts at the minimum positive value.
- *Depends:* S8a, S8-depth, T1 (TumblerOrdering, ASN-0034) — defines `min`.

We now derive the general form. By D-CTG-depth (when m ≥ 3) or trivially (when m = 2, there is only one post-subspace component), all positions in V_1(d) share components 2 through m − 1. By D-MIN, min(V_1(d)) = [1, 1, …, 1], so those shared components have value 1. Every position is therefore [1, 1, …, 1, k] for varying k. D-CTG restricted to the last component forbids gaps among the k values; D-MIN gives the minimum k = 1; S8-fin bounds the maximum at some finite n. Thus:

**D-SEQ (SequentialPositions).** For each document d, if V_1(d) is non-empty, then there exists n ≥ 1 such that:

`V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m, the common V-position depth in the text subspace (S8-depth). By S8a, every V-position has depth `≥ 2`, so `m ≥ 2`; the derivation below relies on this lower bound. At depth 2 this gives V_1(d) = {[1, k] : 1 ≤ k ≤ n}, matching Nelson's "addresses 1 through n."

*Proof.* Let V_1(d) be non-empty and let m be the common depth of all V-positions in the text subspace (S8-depth guarantees a common depth exists). By S8a, every V-position has `#v ≥ 2`, so `m ≥ 2`.

**Step 1: shared prefix.** We show that every position in V_1(d) has the form [1, 1, …, 1, k] — that is, components 2 through m − 1 are all equal to 1, with only the last component varying.

*Case m = 2.* Every position has exactly two components. By the definition `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}` together with `subspace(v) = v₁`, every position in V_1(d) has `v₁ = 1` — the subspace identifier sits at component 1. The second component is a single ordinal. There are no intermediate components (components 2 through m − 1 is the empty range 2 through 1), so the shared-prefix condition holds vacuously. Every position is [1, k] for some k, which is [1, 1, …, 1, k] with zero intervening 1s.

*Case m ≥ 3.* By D-CTG-depth (SharedPrefixReduction), all positions in V_1(d) share components 2 through m − 1. By D-MIN (VMinimumPosition), the minimum element of V_1(d) is [1, 1, …, 1] — a tuple of length m with every component equal to 1. Since the minimum shares components 2 through m − 1 with every other position, and those components of the minimum are all 1, every position in V_1(d) has components 2 through m − 1 equal to 1. Every position is therefore [1, 1, …, 1, k] for some value k at the m-th component.

**Step 2: minimum k.** By D-MIN, min(V_1(d)) = [1, 1, …, 1] of length m. In the representation [1, 1, …, 1, k], the minimum has k = 1 at the last component. Since the minimum is in V_1(d), the set of k-values attained by positions in V_1(d) includes 1.

**Step 3: contiguity of k-values.** Let k₁ < k₂ be two values attained by positions v₁ = [1, 1, …, 1, k₁] and v₂ = [1, 1, …, 1, k₂] in V_1(d). Both have subspace 1 and depth m. By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂ since they agree on components 1 through m − 1 and differ first at component m where k₁ < k₂. For any k ∈ ℕ with k₁ < k < k₂, the tuple w = [1, 1, …, 1, k] satisfies subspace(w) = 1, #w = m, and v₁ < w < v₂ (again by T1(i), since w agrees with both on components 1 through m − 1 and k₁ < k < k₂ at component m). Moreover w satisfies S8a: every component is strictly positive — the leading m − 1 components are all 1, and the last component k satisfies k > k₁ ≥ 1 — so zeros(w) = 0; and #w = m ≥ 2 inherits the depth bound S8a places on v₁. By D-CTG (VContiguity), w ∈ V_1(d). Therefore every k ∈ ℕ between any two attained k-values is itself attained — the k-values form a contiguous range.

**Step 4: finiteness.** By S8-fin (Finite arrangement), dom(M(d)) is finite, so V_1(d) ⊆ dom(M(d)) is finite. The k-values form a finite contiguous range.

**Assembly.** The k-values form a finite contiguous set of positive integers (Step 3, Step 4) that contains 1 (Step 2). Let n = max(k-values); this maximum is well-defined since the set is finite and non-empty (1 ∈ k-values). Then n ≥ 1. By Step 3 applied between 1 and n, every integer with 1 ≤ k ≤ n is attained, so {1, …, n} ⊆ k-values. By definition of n as the maximum, k-values ⊆ {1, …, n}. Hence the k-values are exactly {1, 2, …, n}. By Step 1, V_1(d) = {[1, 1, …, 1, k] : 1 ≤ k ≤ n}. ∎

*Formal Contract:*
- *Preconditions:* V_1(d) non-empty; common V-position depth m (S8-depth), with `m ≥ 2` inherited from S8a.
- *Postconditions:* `(E n : n ≥ 1 : V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length m.
- *Depends:* (*Local properties*) D-CTG (VContiguity) — supplies Step 3's contiguity-of-k-values argument: for any intermediate `k` with `k₁ < k < k₂`, the tuple `w = [1, …, 1, k]` is strictly between attained positions in subspace 1 at depth `m`, so D-CTG forces `w ∈ V_1(d)`; D-CTG-depth (SharedPrefixReduction) — supplies Step 1's `m ≥ 3` branch: all positions in `V_1(d)` share components 2 through `m − 1`; D-MIN (VMinimumPosition) — supplies Step 1's identification of the shared prefix values (all 1) and Step 2's `k = 1` base case; S8a — supplies the lower bound `m ≥ 2`, which both eliminates the depth-1 case and validates the empty-range branch of Step 1 (`m = 2`); S8-depth — guarantees the common depth `m` exists so Step 1 can speak of positions as length-`m` tuples; S8-fin — finiteness of `dom(M(d))` yields finiteness of `V_1(d)`, hence finiteness of the set of attained k-values (Step 4) and well-definedness of `n = max(k-values)`. (*Foundation claims, ASN-0034*) T1 case (i) (TumblerOrdering) — first-divergence comparison powering both Step 3's strict ordering `v₁ < w < v₂` (with the divergence at the last component) and the comparisons internal to D-CTG's application.

D-CTG is a design constraint on well-formed document states. It constrains which arrangement modifications constitute well-formed editing operations. We verify the base case: before any operations, dom(M(d)) = ∅ for all d (the arrangement is a partial function; no content has been allocated, so no V-mapping exists), so V_1(d) = ∅. D-CTG holds vacuously (no u, q exist to trigger its antecedent), and D-MIN holds vacuously (its antecedent requires V_1(d) non-empty). Observe that not all arrangement modifications preserve D-CTG: removing a single interior V-position from dom(M(d)) leaves the positions on either side no longer contiguous. D-CTG is therefore preserved only by those modifications that constitute well-formed editing operations — operations that restore contiguity after structural changes (e.g., by shifting subsequent positions).

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

We work with the arrangement M(d) and the contiguity constraint D-CTG from above, restricted to the text subspace `S = 1`. Write V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1} for the text-subspace V-positions of document d.

When V_1(d) is contiguous with |V_1(d)| = N positions, we write its elements as v₀, v₁, ..., v_{N−1} where v₀ is the minimum (D-MIN) and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ).

We split the valid-insertion-position predicate by document state. The non-empty case has its depth determined by state via S8-depth, so the predicate is binary; the empty case takes the depth as an operational input subject only to the strand-level bound `m ≥ 2`, so the predicate is genuinely ternary. Splitting eliminates the ambiguous third argument from the non-empty case while keeping the empty case's depth input explicit.

**Definition (ValidInsertionPosition, non-empty case).** For a document `d` with `V_1(d) ≠ ∅`, the *binary* predicate `ValidInsertionPosition(d, v)` is satisfied when:

- The common V-position depth `m` of V_1(d) is fixed by S8-depth and read from state — it is *not* a parameter of the predicate. By S8a, `m ≥ 2`.
- Setting `N = |V_1(d)|`, the predicate holds iff `v = shift(min(V_1(d)), j)` for some `j ∈ {0, 1, ..., N}` (taking `shift(·, 0)` as the identity, so the `j = 0` case is `v = min(V_1(d))`).

There are exactly `N + 1` valid insertion positions: the `N` positions coinciding with existing V-positions `v₀` through `v_{N−1}`, plus the append position `shift(min(V_1(d)), N)`.

**Definition (ValidFirstInsertionPosition, empty case).** For a document `d` with `V_1(d) = ∅`, the *ternary* predicate `ValidFirstInsertionPosition(d, v, m)` is satisfied when `m ∈ ℕ` with `m ≥ 2` and `v = [1, 1, ..., 1]` of depth `m`. Here `m` is an operational input chosen by the placing operation — distinct values of `m` identify distinct valid positions. The strand model fixes only the lower bound `m ≥ 2`; the specific value is an allocation convention.

The lower bound `m ≥ 2` is necessary: at `m = 1`, `v = [1]` and `shift([1], 1) = [1] ⊕ δ(1, 1) = [1] ⊕ [1]`; the action point of `[1]` is `k = 1`, so TumblerAdd gives `r₁ = 1 + 1 = 2`, producing `[2]` — a position in subspace 2, not 1. For `m ≥ 2`, `δ(n, m)` has action point `m`, and since `m > 1`, TumblerAdd copies component 1 unchanged — OrdinalShift preserves the subspace identifier. This is the canonical minimum position required by D-MIN. **The specific value of `m` beyond the bound `m ≥ 2` is not fixed by the strand model.** Nelson explicitly leaves "subdivision by further digits" open as "a distinct possibility" for which "several possible uses have been discussed" (LM 4/31). Basic INSERT typically commits to `m = 2`, but the architecture does not require this. Once any position is placed, S8-depth fixes the depth at the chosen `m` for all subsequent positions in the text subspace — transitioning the document into the non-empty regime governed by the binary `ValidInsertionPosition(d, v)`.

In both predicates, `v₁ = 1` is the text subspace identifier.

We verify the structural claims, which apply to both predicates. By D-MIN, `min(V_1(d)) = [1, 1, ..., 1]` of depth `m` (where `m` is the state-fixed common depth in the non-empty case, or the chosen depth in the empty case). By OrdinalShift and TumblerAdd, `shift([1, 1, ..., 1], j) = [1, 1, ..., 1] ⊕ δ(j, m)`; since `δ(j, m)` has action point `m` and `m ≥ 2`, TumblerAdd copies components 1 through `m − 1` unchanged and sets the last component to `1 + j`. The explicit form for the non-empty case is `shift(min(V_1(d)), j) = [1, 1, ..., 1 + j]`.

*Distinctness.* In the non-empty case, the `N + 1` positions have last components `1` (for `j = 0`, where `v = min(V_1(d))`), `2`, `3`, ..., `N + 1` (for `j = 1, ..., N`). These are pairwise distinct natural numbers, so by T3 (CanonicalRepresentation, ASN-0034) the `N + 1` tumblers are pairwise distinct.

*Depth preservation.* For `j ≥ 1` in the non-empty case, `#shift(v, j) = #v = m` by the result-length identity of OrdinalShift (ASN-0034). For `j = 0`, `#v = #min(V_1(d)) = m` by D-MIN. In the empty case, `#v = m` by construction. All valid positions have the common V-position depth required by S8-depth.

*Subspace identity.* Since `δ(j, m)` has action point `m ≥ 2`, TumblerAdd copies component 1 unchanged: `shift(min, j)₁ = min₁ = 1` for all `j ≥ 1`. For `j = 0` in the non-empty case and for the empty case, `v₁ = 1` directly by construction.

*S8a consistency.* Every valid position `[1, 1, ..., 1 + j]` (in the non-empty case) and `[1, 1, ..., 1]` (in the empty case) has all components strictly positive (subspace identifier is 1, intermediate components are 1, last component is `1 + j ≥ 1`), so `zeros(v) = 0` and `(A i : 1 ≤ i ≤ #v : vᵢ > 0)` — satisfying S8a.

*Formal Contract (ValidInsertionPosition, non-empty case).*
- *Signature:* `ValidInsertionPosition(d, v)` — a *binary* predicate on document `d` and V-position `v`. The common V-position depth `m` is determined by `d` via S8-depth and read from state.
- *Preconditions:* Document `d` with `V_1(d) ⊆ dom(M(d))` non-empty; D-CTG holds on V_1(d); `m ≥ 2` is the common depth of V_1(d) by S8-depth and S8a.
- *Definition:* `ValidInsertionPosition(d, v)` holds iff, writing `N = |V_1(d)|`, `v = shift(min(V_1(d)), j)` for some `j ∈ {0, 1, ..., N}` (with `shift(·, 0) = identity`).
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m` (the state-fixed common depth). (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d`, exactly `N + 1` values of `v` satisfy the predicate. (d) The explicit form is `v = [1, 1, ..., 1 + j]` with last component `1 + j` and all preceding components equal to 1.
- *Depends:* D-MIN, D-CTG, D-CTG-depth, D-SEQ; S8a, S8-fin, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

*Formal Contract (ValidFirstInsertionPosition, empty case).*
- *Signature:* `ValidFirstInsertionPosition(d, v, m)` — a *ternary* predicate on document `d`, V-position `v`, and depth `m`. The depth `m` is an operational input chosen by the placing operation; the strand model fixes only the lower bound `m ≥ 2`.
- *Preconditions:* Document `d` with `V_1(d) = ∅`; `m ∈ ℕ` with `m ≥ 2`.
- *Definition:* `ValidFirstInsertionPosition(d, v, m)` holds iff `v = [1, 1, ..., 1]` of depth `m`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m`. (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d` and `m`, exactly one value of `v` satisfies the predicate. (d) Once the position is placed, S8-depth fixes the depth at `m` for all subsequent positions in the text subspace, after which validity of further insertion positions is governed by `ValidInsertionPosition(d, v)`.
- *Frame:* The specific value of `m` is set by the placing operation, *not* by the strand model — Nelson's "subdivision by further digits" (LM 4/31) leaves the choice to operation-layer convention.
- *Depends:* D-MIN; S8a, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

### Valid insertion position examples

**Non-empty case (binary predicate).** Let subspace S = 1 and suppose V₁(d) = {[1, 1], [1, 2], [1, 3]}, so N = 3 and min(V₁(d)) = [1, 1]. The depth `m = 2` is read from state via S8-depth. The values of `v` satisfying `ValidInsertionPosition(d, v)` are:

- j = 0: v = min(V₁(d)) = [1, 1]
- j = 1: v = shift([1, 1], 1) = [1, 2]
- j = 2: v = shift([1, 1], 2) = [1, 3]
- j = 3: v = shift([1, 1], 3) = [1, 4]

That gives N + 1 = 4 positions. After an operation places new content at, say, [1, 2] — with whatever displacement mechanism the operation defines — the resulting V₁(d) must satisfy D-CTG and D-MIN. Verifying this is the operation's obligation, not the predicate's.

**Empty case (ternary predicate).** V₁(d) = ∅. Choosing depth m = 2, the unique `v` satisfying `ValidFirstInsertionPosition(d, v, 2)` is `[1, 1]`. D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands. Choosing m = 3 instead, `ValidFirstInsertionPosition(d, v, 3)` is satisfied uniquely by `v = [1, 1, 1]`; by T3, this is a different tumbler — once chosen, S8-depth locks the subspace to depth 3 for all future positions, and subsequent validity is governed by `ValidInsertionPosition(d, v)` with `m = 3` read from state.


## The separation theorem

We can now state the property that Nelson calls "the architectural foundation of everything" as a theorem rather than an axiom.

**S9 (Two-stream separation).** No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S9 carries no formal content beyond S0: its consequent is verbatim S0's, and its antecedent `Σ'.M(d) ≠ Σ.M(d)` merely restricts S0's universal quantification over transitions to the arrangement-modifying ones. Since S0 holds for *every* transition `Σ → Σ'` unconditionally, it holds a fortiori for arrangement-modifying ones, discharging the consequent. We retain S9 as a named theorem not because it strengthens S0 but because it names the architecturally salient *direction* of the dependency — that arrangement edits, the only transitions that touch `M`, cannot reach across into `C`. ∎

*Formal Contract:*
- *Preconditions:* State transition `Σ → Σ'` such that `Σ'.M(d) ≠ Σ.M(d)` for some document `d` (an arrangement-modifying transition); system satisfies S0 (content immutability).
- *Postconditions:* `(A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))` — every content entry persists with its value across the transition.
- *Frame:* The arrangement modification may be arbitrary (insertion, deletion, rearrangement, or any combination); S9 holds regardless of the specific transformation applied to `Σ.M(d)`.
- *Depends:* S0 (content immutability) — supplies the universal guarantee that S9 specialises to arrangement-modifying transitions.

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

*Check S0*: no prior content existed, so the implication holds vacuously. *Check S3*: every V-reference resolves — `ran(M(d₁)) ⊆ dom(C)`. *Check S7*: for `a = 1.0.1.0.1.0.1.3`, `origin(a) = 1.0.1.0.1 = d₁` — the document-level prefix directly identifies the allocating document. *Check S8*: the arrangement admits a single correspondence run `(v₁, a₁, n₁) = (1.1, 1.0.1.0.1.0.1.1, 5)`, exhibiting the index-arithmetic identity at every `k ∈ {0, 1, 2, 3, 4}`. We verify the identity explicitly at `k = 3`:

- *Left side: `M(d₁)(shift(1.1, 3))`.* The V-position `v = 1.1 = [1, 1]` has depth `m = 2`, so `shift(v, 3) = v ⊕ δ(3, 2) = [1, 1] ⊕ [0, 3] = [1, 4]` (action point 2; component 1 copied unchanged, component 2 receives `1 + 3 = 4`). Reading `M(d₁)([1, 4])` from the arrangement table: `M(d₁)(1.4) = 1.0.1.0.1.0.1.4`.

- *Right side: `shift(1.0.1.0.1.0.1.1, 3)`.* The I-address `a = 1.0.1.0.1.0.1.1` has depth `#a = 8` (three field-separator zeros plus five non-separator components), so `shift(a, 3) = a ⊕ δ(3, 8) = [1, 0, 1, 0, 1, 0, 1, 1] ⊕ [0, 0, 0, 0, 0, 0, 0, 3]` (action point 8 — the element ordinal's last component). TumblerAdd copies components 1 through 7 from `a` unchanged — including the three separator zeros at positions 2, 4, 6 (so `zeros(shift(a, 3)) = zeros(a) = 3`, the field-structure preservation supplied by ShiftPreservation, conclusion (i)) and the subspace identifier `subspace_I(a) = E(a)₁ = 1` at position 7 — and sets component 8 to `1 + 3 = 4`, yielding `[1, 0, 1, 0, 1, 0, 1, 4] = 1.0.1.0.1.0.1.4`.

- *Both sides equal `1.0.1.0.1.0.1.4`.* The same component-by-component computation works at every `k ∈ {0, 1, 2, 3, 4}`: `M(d₁)(shift(1.1, k)) = M(d₁)(1.(1+k)) = 1.0.1.0.1.0.1.(1+k) = shift(1.0.1.0.1.0.1.1, k)`.

*Check D-SEQ*: V₁(d₁) = {[1, k] : 1 ≤ k ≤ 5}, satisfying D-SEQ with n = 5. D-CTG holds (no gaps in the ordinal range 1..5) and D-MIN holds (min = [1, 1]).

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

*Check S0*: all 7 entries in `dom(C)` remain. The I-addresses `1.0.1.0.1.0.1.3`–`.5` are no longer in `ran(M(d₁))` but persist in `dom(C)`; these three addresses are now "orphaned" from `d₁`'s perspective, but still referenced by `M(d₂)` — persistence is unconditional (S0). *Check S9*: the deletion modified `M(d₁)` but `C` is unchanged — separation holds. *Check S8*: `M(d₁)` is now a single run `(1.1, 1.0.1.0.1.0.1.1, 2)`. The prior 1-run decomposition became a 1-run decomposition (the deletion removed an entire suffix, not a middle segment). `M(d₂)` is unchanged — still two runs. *Check D-SEQ*: V₁(d₁) = {[1, k] : 1 ≤ k ≤ 2}, D-SEQ with n = 2. D-CTG holds (no gaps in 1..2) and D-MIN holds (min = [1, 1]). V₁(d₂) is unchanged — D-SEQ with n = 5.


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
| S3 | Referential integrity: `(A d, v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C))` | design; uses S1 |
| S4 | Origin-based identity: distinct allocations produce distinct I-addresses regardless of value equality | from GlobalUniqueness, T3 (ASN-0034) |
| S5 | Unrestricted sharing: S0–S3 do not entail any finite bound on sharing multiplicity | consistent with S0, S1, S2, S3 |
| S7a | Document-scoped allocation: every I-address is allocated under the originating document's prefix | design; uses T4, T4b, T10a, T10a.4, S0 (ASN-0034) |
| S7b | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | design; uses T4, T4b, T10a.4, S0 (ASN-0034) |
| S7c | Element-field depth: `(A a ∈ dom(C) :: #E(a) ≥ 2)` — subspace identifier and content ordinal occupy distinct components | design; uses S7b, T4, T4b, TA7a, T10a.4, S0 (ASN-0034) |
| S7d | Document allocation discipline: every document is addressed by a document-level tumbler (`zeros = 2`) allocated via T10a under the owning user's prefix; distinct documents arise from distinct allocation events | design; uses T10a, T10a.4, T4 (ASN-0034) |
| subspace_I(a) | I-address subspace identifier: `subspace_I(a) = E(a)₁`; well-defined when S7c holds. Parallels `subspace(v) = v₁` for V-positions | introduced |
| ShiftPreservation | For any `a ∈ dom(Σ.C)` and `k ≥ 1`: (i) `zeros(shift(a, k)) = 3`; (ii) `shift(a, k)` is T4-valid; (iii) `#E(shift(a, k)) = #E(a)`; (iv) `subspace_I(shift(a, k)) = subspace_I(a)` | lemma from S7b, S7c, T0, T4, T4b, T10a.4, OrdinalShift, TumblerAdd, NAT-discrete, NAT-closure, NAT-addcompat, NAT-order (ASN-0034) |
| S7 | Structural attribution: `origin(a) = N(a).0.U(a).0.D(a)` — full document prefix | from S7a, S7b, S7d, S0, S4, T4, T4b, T3, T10a.4, GlobalUniqueness (ASN-0034) |
| S8-fin | Finite arrangement: `dom(M(d))` is finite for every document `d` | design requirement |
| S8a | V-position well-formedness: `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` — element-field tumblers of depth ≥ 2 with componentwise positive entries | definition (V-positions are element-field tumblers of depth ≥ 2, paralleling S7c); zero-count and positivity derived from T4, T0 (ASN-0034) |
| subspace(v) | V-position subspace identifier: `subspace(v) = v₁`; well-defined when `#v ≥ 1`. Parallels `subspace_I(a) = E(a)₁` for I-addresses | introduced; uses T0 (ASN-0034), S8a |
| S8-depth | Fixed-depth V-positions: `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` | design; uses S8a |
| S8 | Span decomposition: `dom(M(d))` decomposes into finitely many correspondence runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for `0 ≤ k < nⱼ`; corollary (via ShiftPreservation applied pointwise) preserves subspace identifier, zero-count (= 3, S7b), and element-field depth (= δⱼ ≥ 2, S7c) across each run | theorem from S2, S3, S7b, S7c, S8-fin, S8a, S8-depth, ShiftPreservation, T1, T3, T4, T5, T10, TumblerAdd, OrdinalShift, OrdinalDisplacement, TS4, NAT-discrete, NAT-closure, NAT-order (ASN-0034) |
| ord(v) | Ordinal extraction: ord(v) = [v₂, ..., vₘ]; when v satisfies S8a, ord(v) ∈ S | introduced |
| vpos(S, o) | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord for any o ∈ T; satisfies S8a when S ≥ 1 and all oᵢ > 0 | introduced |
| w_ord | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for displacement w with w₁ = 0 | introduced |
| OrdAddHom | (a) ord(v ⊕ w) = ord(v) ⊕ w_ord; (b) subspace(v ⊕ w) = subspace(v); (c) v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord) | lemma from ord, w_ord, TumblerAdd, TA0 (ASN-0034) |
| OrdAddS8a | v ⊕ w satisfies S8a ⟺ all tail components of w after the action point are positive; equivalently ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a | lemma from OrdAddHom, S8a, TumblerAdd (ASN-0034) |
| OrdShiftHom | ord(shift(v, n)) = shift(ord(v), n); shift(v, n) unconditionally satisfies S8a when v does | corollary from OrdAddHom, OrdAddS8a, OrdinalShift, OrdinalDisplacement (ASN-0034) |
| D-CTG | V-position contiguity (bound to text subspace `S = 1`): V_1(d) forms a contiguous ordinal range with no gaps — design constraint on well-formed document states; link subspace `S = 2` is exempt (sparse with tombstones) | design (text subspace); uses S8a, S8-depth, T1 (ASN-0034) |
| D-MIN | V-position minimum (bound to text subspace `S = 1`): non-empty V_1(d) has minimum [1, 1, ..., 1] with every component equal to 1 — design constraint | design requirement (text subspace) |
| D-CTG-depth | Shared prefix reduction (bound to text subspace `S = 1`, applies wherever D-CTG holds): at depth m ≥ 3, all positions in V_1(d) share components 2 through m − 1, so contiguity reduces to the last component | corollary of D-CTG, S8a, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034) |
| D-SEQ | Sequential positions (bound to text subspace `S = 1`): non-empty V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 | from D-CTG, D-CTG-depth, D-MIN, S8a, S8-fin, S8-depth, T1 (ASN-0034) |
| ValidInsertionPosition | Binary predicate `ValidInsertionPosition(d, v)` (non-empty case; bound to text subspace `S = 1`): when V_1(d) ≠ ∅, m is the common depth of V_1(d) (state-determined via S8-depth), and v = shift(min(V_1(d)), j) for j ∈ {0, ..., N} where N = |V_1(d)| | introduced |
| ValidFirstInsertionPosition | Ternary predicate `ValidFirstInsertionPosition(d, v, m)` (empty case; bound to text subspace `S = 1`): when V_1(d) = ∅, m ≥ 2 is an operational input chosen by the placing operation, and v = [1, 1, ..., 1] of depth m | introduced |
| S9 | Two-stream separation: arrangement changes cannot alter stored content | named directional reading of S0 (no formal content beyond S0) |


## Open Questions

What constraints must the content store's value domain `Val` satisfy — must all entries be uniform in type, or must `Val` support heterogeneous content (text, links, media) as first-class distinctions?

Must the span decomposition of an arrangement have a unique maximal form (fewest possible runs), or can multiple valid decompositions of different cardinality coexist for the same arrangement?

What must the system guarantee about the computability of the sharing inverse — given an I-address, what is the cost bound for determining which documents currently reference it?

Under what conditions, if any, may the referential integrity invariant S3 be temporarily violated — must it hold at every observable state, or only at quiescent states between operations?

What abstract property distinguishes content that exists but is unreachable from all current arrangements from content that exists and is reachable — and must the system maintain this distinction as queryable state?

Under what conditions do operations guarantee non-trivial correspondence runs (length > 1) — must sequential content creation produce a single run, or is the singleton decomposition the only structure guaranteed without operation-level constraints?

Does each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) preserve D-CTG and D-MIN?

What invariants must the displacement mechanism satisfy so that insertion at a ValidInsertionPosition preserves D-CTG, D-MIN, and S2?

The strand model fixes only the lower bound m ≥ 2 for V-position depth in an empty subspace; the specific value is a one-time allocation convention chosen by the first-placing operation, not a strand-level commitment. What operation-layer constraints determine the canonical choice of m (e.g., m = 2 for basic INSERT/DELETE versus deeper subdivisions Nelson contemplated)? What downstream capabilities — nested hierarchies, link subdivision, future extensibility — does each depth choice unlock or foreclose?

What must an operation guarantee about existing V-to-I mappings when it inserts at a position that coincides with an occupied V-position?

The strand model treats subspace alignment — `subspace(v) = subspace_I(M(d)(v))` for every V-position — as an operations-layer preservation obligation rather than a state-level invariant on arrangements. Which editing operations must establish this alignment for the V-positions they produce, and under what allocation conventions is preservation automatic versus requiring explicit operation-level enforcement?

Under what conditions on w does the subtraction homomorphism ord(v ⊖ w) = ord(v) ⊖ w_ord hold, given TA7a's conditional S-membership results for subtraction?

What are the precise conditions for the round-trip property (ord(v) ⊕ w_ord) ⊖ w_ord = ord(v)?
