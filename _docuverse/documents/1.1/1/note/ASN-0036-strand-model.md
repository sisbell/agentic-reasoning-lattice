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

*Formal Contract:*
- *Axiom:* `Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.
- *Definition:* `dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.

**Σ.M(d) (Arrangement).** The *arrangement* of document `d`: a partial function mapping Vstream positions to Istream addresses. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

A conventional system merges these — "the file" IS the content IS the arrangement. Editing overwrites. Saving destroys the prior state. Nelson rejected this explicitly: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." The two-component model is his alternative: editing modifies `M(d)` while `C` remains invariant. The separation is the premise; what follows are the invariants it must satisfy.

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

S0 and S1 together establish `C` as an *append-only log*. New entries may be added — each at a fresh address guaranteed unique by T9 and T10 (ASN-0034) — but no existing entry may be modified or removed.

Nelson states this as an explicit design commitment: "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." Gregory's implementation confirms the commitment. Of the seventeen FEBE commands Nelson specifies, none modifies existing Istream content. There is no MODIFY, UPDATE, or REPLACE operation. The absence is structural — the protocol provides no mechanism for mutating stored content.

Gregory's evidence shows the reclamation machinery was built but deliberately deactivated — the reference-counted deletion call is commented out (`/*subtreefree(ptr);*/`) — so S0 and S1 are upheld by design choice rather than architectural impossibility.

*Proof.* We wish to show that for every state transition `Σ → Σ'`, `dom(Σ.C) ⊆ dom(Σ'.C)`.

Let `a ∈ dom(Σ.C)` be arbitrary. By S0 (content immutability), `a ∈ dom(Σ.C)` implies the conjunction `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The first conjunct yields `a ∈ dom(Σ'.C)` directly. Since `a` was chosen arbitrarily from `dom(Σ.C)`, we have established `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C))`, which is `dom(Σ.C) ⊆ dom(Σ'.C)` by definition of subset inclusion.

S1 is the domain conjunct of S0, and it specialises T8 (allocation permanence, ASN-0034) to the content store. T8 guarantees `allocated(s) ⊆ allocated(s')` for the address space as a whole; S1 guarantees `dom(Σ.C) ⊆ dom(Σ'.C)` for the content store specifically. The two properties have different scopes: T8 covers addresses that have been allocated but may carry no content, while S1 covers addresses at which content has actually been stored. ∎

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
- *Postconditions:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` is a well-defined set — single-valuedness makes the image of `M(d)` depend only on its domain, so the range is determined.
- *Frame:* Distinct V-positions may map to the same I-address (sharing — S5); injectivity is *not* asserted.

The bridge between the two state components is a well-formedness condition:

**S3 (Referential integrity).** `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Every V-reference resolves. If a document's arrangement says "at position `v`, display the content at I-address `a`," then `a` must be in `dom(C)`. There are no dangling references.

The maintenance of S3 across state transitions reveals a temporal ordering constraint. The weakest precondition for S3 under an operation that adds a V-mapping `M(d)(v) = a` is:

`wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)`

For an operation that only adds a V-mapping without creating content, the target I-address must already be in `dom(C)`. An operation that atomically creates content at `a` and adds the mapping `M(d)(v) = a` satisfies S3 in the post-state without sequential precedence — `a ∈ dom(Σ'.C)` and `Σ'.M(d)(v) = a` are established simultaneously. The dependency is logical, not temporal: a reference presupposes the existence of its target, but existence need not precede reference in a prior transition. What matters for persistence is that S1 guarantees once `a` enters `dom(C)`, it remains — so a valid reference cannot become dangling through any subsequent state transition.

We observe a deliberate asymmetry. S3 says arrangement implies existence: `ran(M(d)) ⊆ dom(C)`. It does NOT say existence implies arrangement. Content can exist in Istream without being arranged in any current document — and since S0's antecedent is `a ∈ dom(Σ.C)` alone, not conditioned on whether `a` appears in any `ran(M(d))`, such unreferenced content is never reclaimed and persists. Nelson requires this for history — he calls such content "deleted bytes — not currently addressable, awaiting historical backtrack functions, may remain included in other versions," and version reconstruction depends on the availability of Istream fragments from prior arrangements. This persistence independence is the space the asymmetry opens.

*Formal Contract (S3):*
- *Axiom (well-formedness invariant):* In every state `Σ`, `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — equivalently, `ran(Σ.M(d)) ⊆ dom(Σ.C)`.
- *Preservation across transitions:* For an operation that adds a V-mapping `M(d)(v) = a`, `wp(op, S3) ⟹ a ∈ dom(Σ'.C)` — the I-address must exist in the post-state.
- *Frame:* S3 is one-directional — content may exist in `dom(C)` without being referenced (orphaned content); existence does not entail arrangement.
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

In any particular state, the sharing multiplicity of each address is a definite finite number — possibly zero for orphaned content. The property is an architectural anti-constraint: the invariants place no finite cap on how many references may accumulate.

Nelson: "The virtual byte stream of a document may include bytes from any other document." And: "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely." Transclusion is recursive and unlimited.

Gregory confirms the unbounded nature at the implementation level. The global index that records which documents reference which I-addresses accumulates entries without cap — "no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism anywhere in the code path." Each referential inclusion adds one entry. The only constraints are physical resources (memory and disk), not architectural limits.

The combination of S4 and S5 gives the system its distinctive character. S4 says identity is structural — determined by I-address, not by value. S5 says sharing is unlimited — any number of documents can reference the same content. Together they establish a regime in which quotation is a first-class structural relationship: any number of documents can quote the same passage, and the system knows they are all quoting — not independently writing — because they share I-addresses.

We observe that the state `Σ = (C, M)` makes the sharing relation computable: given any `a ∈ dom(C)`, the set `{d : (E v :: M(d)(v) = a)}` is determined by the state. Nelson requires this to be queryable: "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." The state model supports this — the information is present; only the efficiency of its extraction is an implementation concern.

*Proof.* We wish to show that for every `N ∈ ℕ`, there exists a state `Σ` satisfying S0–S3 in which some I-address has sharing multiplicity exceeding `N`. We give two constructions — one for cross-document sharing, one for within-document sharing — each succeeding for arbitrary `N`.

**Cross-document construction.** Fix `N ∈ ℕ`. Define state `Σ_N = (C_N, M_N)` by:

- `C_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`.
- `N + 1` documents `d₁, …, d_{N+1}` with explicit witnesses `dᵢ = [1, 0, 1, 0, i]` for `i = 1, …, N + 1` (the natural numbers `1, …, N + 1` exist in ℕ by NAT-closure, ASN-0034 — `1 ∈ ℕ` from the same axiom's base case, and `i + 1 ∈ ℕ` for any `i ∈ ℕ` by closure under addition; the index range `i ∈ {1, …, N + 1}` gives each `D(dᵢ) = [i]` field a strictly positive component, satisfying T4's positive-component constraint on present fields). Each `dᵢ` is a valid document-level tumbler: `zeros(dᵢ) = 2` with no adjacent zeros, positive endpoint components, and the three fields `N(dᵢ) = [1]`, `U(dᵢ) = [1]`, `D(dᵢ) = [i]` populated by strictly positive natural numbers (T4, HierarchicalParsing, ASN-0034). The `dᵢ` are pairwise distinct by T3 (CanonicalRepresentation, ASN-0034) since they have distinct last components. Fix a single V-position `v = [1, 1]` shared across all `N + 1` documents, and define each arrangement as `M_N(dᵢ) = {v ↦ a}`. The pairs `(dᵢ, v)` are pairwise distinct because the first coordinates `dᵢ` are pairwise distinct, which suffices for distinctness of pairs.

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


## Structural attribution

Every V-position can be traced to the document that originally created its content.

We first restrict S7's domain. The projection `D(a)` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: `zeros = 0` is node-only, `zeros = 1` is node+user, `zeros ≥ 2` has a document field). Since Istream addresses designate content elements within documents, we require:

**S7b (Element-level I-addresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This is a design requirement: content resides at the element level — the finest level of the four-level tumbler hierarchy. Node, user, and document-level tumblers identify containers, not content. By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

*Formal Contract (S7b):*
- *Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.
- *Postconditions:* By T4's field correspondence, all four identifying fields — node, user, document, element — are present and the element field exists. The projections `N(a)`, `U(a)`, `D(a)`, `E(a)` supplied by T4b are all well-defined.
- *Depends:* T4 (HierarchicalParsing, ASN-0034) — field correspondence; T4b (UniqueParse, ASN-0034) — projection definitions; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — supplies the surrounding T4-validity (no adjacent zeros, positive endpoint components `a₁ ≠ 0 ∧ a_{#a} ≠ 0`) on which T4b's projections in the postcondition rely, and supplies the bound `zeros ≤ 3` that S7b strengthens to the equality `zeros(a) = 3`; S0 (content immutability) — keeps `a ∈ dom(C')` across transitions, so the zero-count condition continues to hold on the same address.

**S7a (Document-scoped allocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N(a).0.U(a).0.D(a)` obtained by truncating the element field, where `N(a)`, `U(a)`, `D(a)` are the partial projections supplied by T4b (UniqueParse, ASN-0034) — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. The address IS the provenance: "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents.

*Formal Contract (S7a):*
- *Axiom (design requirement):* `(A a : a ∈ dom(Σ.C) :: the document-level prefix N(a).0.U(a).0.D(a) is the tumbler of the document whose owner performed the allocation that placed a into dom(C))`. By S7b (stated above), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are everywhere defined on the domain over which the axiom quantifies.
- *Depends:* T4 (HierarchicalParsing, ASN-0034) — defines the prefix structure; T4b (UniqueParse, ASN-0034) — defines projections `N`, `U`, `D`; S7b (Element-level I-addresses) — supplies `zeros(a) = 3` for every `a ∈ dom(Σ.C)`; T10a (AllocatorDiscipline, ASN-0034) — establishes the baptism principle; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation.

**S7c (Element-field depth).** Every content address has an element field of depth at least 2:

`(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)`

where `E(a)` is the element-field projection supplied by T4b (UniqueParse, ASN-0034). This parallels `subspace(v) = v₁` for V-positions: both extract the subspace context from a tumbler whose first element-field component carries the subspace identifier. S7c is a design requirement that the element field have depth at least 2, so that `subspace_I(a) = E(a)₁` and the content ordinal `[E(a)₂, ..., E(a)_{#E(a)}]` occupy distinct components. Gregory's evidence confirms `#E(a) = 2` as the standard allocation pattern: the element field is `[S, x]` where `S = subspace_I(a)` is the subspace identifier and `x` is the content ordinal.

*Formal Contract (S7c):*
- *Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)` — the element field has at least two components, so the subspace identifier `E(a)₁` and the content ordinal `[E(a)₂, ..., E(a)_{#E(a)}]` occupy distinct positions.
- *Depends:* S7b (element-level I-addresses) — provides `E(a)`; T4b (UniqueParse, ASN-0034) — defines element-field projection.

**subspace_I (I-address subspace identifier).** For any `a` with `zeros(a) = 3` and `#E(a) ≥ 2`, the subspace identifier of an I-address is the first component of its element field: `subspace_I(a) = E(a)₁`.

*Formal Contract:*
- *Signature:* `subspace_I : T → ℕ` — projects the first component of the element field of an I-address.
- *Preconditions:* `a ∈ dom(Σ.C)` (so S7b's `zeros(a) = 3` holds, making T4b's element-field projection `E(a)` well-defined); S7c's `#E(a) ≥ 2` (so that `E(a)₁` is well-defined as the first component of a non-empty element field).
- *Definition:* `subspace_I(a) = E(a)₁`.
- *Postconditions:* (a) `subspace_I(a) ∈ ℕ` — the projected component inherits T0's ℕ-valued carrier (ASN-0034). (b) `subspace_I(a) ≥ 1` — T4's positive-component constraint on present fields delivers `E(a)₁ ≥ 1`.
- *Depends:* T0 (ASN-0034) — ℕ-valued component carrier underwriting postcondition (a); T4b (UniqueParse, ASN-0034) — supplies `E(a)` once S7b holds; T4 (HierarchicalParsing, ASN-0034) — positive-component constraint on present fields delivering `E(a)₁ ≥ 1`, underwriting postcondition (b); S7b — provides `E(a)` via `zeros(a) = 3`; S7c — provides `#E(a) ≥ 2`.

**S7d (Document allocation discipline).** Every document is addressed by a document-level tumbler (`zeros = 2`) allocated via T10a's allocator discipline (ASN-0034) under the owning user's prefix. Distinct documents arise from distinct allocation events.

Nelson's baptism principle covers it directly: the user-level allocator baptises documents under the user's prefix in the same way each document's allocator baptises elements under the document's prefix.

*Formal Contract (S7d):*
- *Axiom (design requirement):* Every document tumbler `d` satisfies `zeros(d) = 2` and is the result of an allocation event under T10a; distinct documents arise from distinct allocation events.
- *Postconditions:* By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers — the cross-document uniqueness premise for S7's identification argument.
- *Depends:* T10a (AllocatorDiscipline, ASN-0034) — allocation events; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation, here at `zeros = 2`; T4 (HierarchicalParsing, ASN-0034) — field correspondence at `zeros = 2`; GlobalUniqueness (ASN-0034) — uniqueness across allocation events.

With S7a, S7b, and S7d established, we can state structural attribution.

**S7 (Structural attribution).** For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = N(a).0.U(a).0.D(a)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system. Since document creation is an allocation event within a system conforming to T10a, GlobalUniqueness (ASN-0034) directly guarantees that distinct documents have distinct tumblers, and therefore distinct document-level prefixes. It is not metadata that can be stripped or forged — it IS the address. To retrieve the content, the system must know its I-address; to know its I-address is to know its origin.

S7 follows from S7a (document-scoped allocation ensures the document-level prefix identifies the allocating document), S7b (element-level restriction ensures all three identifying fields are present), S7d (document tumblers are themselves products of T10a allocation events, supplying the precondition for GlobalUniqueness), T4 (HierarchicalParsing, ASN-0034), and GlobalUniqueness (ASN-0034) (distinct document allocation events produce distinct document tumblers). Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

We note a subtlety. S7 identifies the document that ALLOCATED the I-address — the document where the content was first created. This is distinct from the document where the content currently appears. When content is transcluded from document B into document A, the reader viewing A sees the content, but S7 traces it to B. The distinction between "where I am reading" (Vstream context, document A) and "where this came from" (Istream structure, document B) is precisely the two-stream separation made visible.

Gregory's implementation reveals two mechanisms for origin lookup. The I-address prefix itself encodes the originating document (used during address allocation to scope the search range). Separately, each arrangement entry carries an explicit `homedoc` field recording the allocating document (used during retrieval). At the abstract level, S7 says only that the information is present in the address — it does not prescribe how an implementation extracts it.

*Proof.* We wish to show that for every `a ∈ dom(Σ.C)`, the function `origin(a) = N(a).0.U(a).0.D(a)` is well-defined, uniquely identifies the document that allocated `a`, and that this identification is permanent and unseverable.

**Well-definedness.** By S7b (element-level I-addresses), `zeros(a) = 3`, and by T10a.4 (T4PreservationUnderDiscipline, ASN-0034), `a` is T4-valid; hence T4's field-decomposition machinery applies to `a`. By T4 (HierarchicalParsing, ASN-0034), `zeros(a) = 3` means `a` contains exactly three zero-valued field separators, and the partial projections supplied by T4b (UniqueParse, ASN-0034) — `N(a)`, `U(a)`, `D(a)`, `E(a)` — extract the node, user, document, and element fields respectively, each as a finite sequence of strictly positive natural numbers. T4's positive-component constraint guarantees every non-separator component is strictly positive, and T4's non-empty field constraint guarantees each present field has at least one component. The projections `N(a)`, `U(a)`, and `D(a)` are therefore all well-defined with at least one strictly positive component each. The truncation `origin(a)` — formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field — is a well-defined tumbler satisfying `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy.

**Identification.** By S7a (document-scoped allocation), every I-address is allocated under the tumbler prefix of the document that created it. The document-level prefix of `a` — precisely `origin(a)`, the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`. This is not a lookup or annotation: the address structurally encodes its provenance. S7a ensures that `origin(a)` IS the allocating document's tumbler.

**Uniqueness across documents.** By S7d (document allocation discipline), every document tumbler is itself the product of an allocation event under T10a's discipline: a document is created by allocating a document-level address under the owning user's prefix, and distinct documents arise from distinct allocation events. For documents `d₁ ≠ d₂`, S7d supplies the required premise — distinct allocation events — and GlobalUniqueness (ASN-0034) then guarantees that the resulting document-level tumblers are distinct. By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison. Therefore, for any `a₁, a₂ ∈ dom(Σ.C)` allocated under distinct documents: `origin(a₁) ≠ origin(a₂)`. The origin function discriminates allocating documents without ambiguity.

**Permanence.** By S0 (content immutability), once `a ∈ dom(Σ.C)`, then `a ∈ dom(Σ'.C)` for all successor states `Σ'` — the address persists. Since `a` is a tumbler — a fixed sequence of components, not a mutable reference — and `origin(a)` is computed from the components of `a` alone via T4's deterministic field decomposition, `origin(a)` yields the same result in every state in which `a` exists. By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused. The attribution cannot be severed because it is not a separate datum attached to the content — it is a structural property of the address itself. To retrieve content at `a`, a system must know `a`; to know `a` is to know `origin(a)`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), S7d (document allocation discipline), T4 (HierarchicalParsing, ASN-0034), T4b (UniqueParse, ASN-0034) — supplies the projections `N(a)`, `U(a)`, `D(a)`, `E(a)` from which `origin(a)` is computed, T10a (allocator discipline, ASN-0034), and T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation. The strict equality `zeros(a) = 3` itself comes from S7b axiomatically.
- *Postconditions:* (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.


## Span decomposition

The arrangement `M(d)` maps individual V-positions to I-addresses. Because `dom(M(d))` is finite (S8-fin), the mapping always admits a *finite* decomposition into correspondence runs — this is the existence claim we establish here. Whether contiguous V-ranges that correspond ordinally to contiguous I-ranges can be *coalesced* into longer maximal runs — the compression that would make finite representation compact — is a separate question.

Before defining correspondence runs, we must establish the structure of `dom(M(d))` more carefully.

**S8-fin (Finite arrangement).** For each document `d`, `dom(Σ.M(d))` is finite. A document contains finitely many V-positions at any given state.

This is a design requirement on every reachable state: no document arrangement is permitted to hold infinitely many V-positions.

*Formal Contract:*
- *Axiom (design requirement):* For every state `Σ` and document `d`, `dom(Σ.M(d))` is a finite set.
- *Postconditions:* `|dom(Σ.M(d))| < ∞` — the arrangement has finite cardinality. Consequently `ran(Σ.M(d))` is finite (image of a finite set under a function).
- *Frame:* No constraint on the unbounded growth of `dom(C)`; only individual arrangements are required to be finite at any given state.

**S8a (V-position well-formedness).** A V-position is, by definition, an element-field tumbler of depth at least 2. From this structural commitment the zero-count and componentwise-positivity conjuncts follow:

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

A V-position represents the element field of a full document-scoped address — the fourth field in the T4 field structure. Its first component `v₁` is the subspace identifier (1 for text, 2 for links); the `0` in full tumbler notation (e.g., `N.0.U.0.D.0.2.1`) is a field separator, not a subspace identifier. The depth constraint `#v ≥ 2` parallels S7c for I-address element fields: it ensures the subspace identifier `v₁` and the within-subspace ordinal `[v₂, ..., v_m]` occupy distinct components. The domain and range of `M(d)` live in structurally different tumbler subsets: `dom(M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2 ∧ (A i : tᵢ > 0)}` (element-field tumblers of depth at least 2), while `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b). Since all V-positions in subspace `s` extend the single-component prefix `[s]`, T5 (ContiguousSubtrees, ASN-0034) guarantees they form a contiguous interval under T1 — grounding the application of tumbler ordering properties to V-positions and justifying S8-depth's reference to "within a subspace."

*Proof.* A V-position is, by definition, an isolated element field of depth at least 2 (paralleling S7c's element field for I-addresses), so `zeros(v) = 0` and `#v ≥ 2` hold by definition. Componentwise positivity follows: every component of `v` lies in T0's carrier ℕ, and `zeros(v) = 0` forces each to be `≠ 0`, hence `≥ 1` by **Nat-pos** — the elementary fact that for `n ∈ ℕ`, `n ≠ 0 ⟹ n ≥ 1` (immediate from NAT-discrete at `m = 0`); in particular the subspace identifier `v₁ ≥ 1`. ∎
*Formal Contract:*
- *Definition:* A V-position is, by definition, an isolated element field of depth at least 2 — paralleling S7c for I-address element fields.
- *Preconditions:* The element-field definitional commitment (a V-position is an isolated element field of depth ≥ 2 with no field separators); T0 — components are natural numbers.
- *Postconditions:* `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`.
- *Depends:* T0 (ASN-0034) — supplies the ℕ-valued component carrier on which `vᵢ ∈ ℕ` for every component; NAT-discrete (NatDiscreteness, ASN-0034) — underwrites Nat-pos (the `n ≠ 0 ⟹ n ≥ 1` fact, immediate from NAT-discrete at `m = 0`), which discharges the positivity step: `vᵢ ≠ 0` (delivered by `zeros(v) = 0`) gives `vᵢ ≥ 1`, hence `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.

**subspace (V-position subspace identifier).** For any tumbler `v` of depth `#v ≥ 1`, define:

`subspace(v) = v₁`

extracting the subspace identifier as the first component of a V-position.

*Formal Contract:*
- *Signature:* `subspace : T → ℕ` — projects the first component of a tumbler.
- *Preconditions:* `v ∈ T`, `#v ≥ 1` (so that `v₁` is well-defined as the first component of a non-empty tumbler).
- *Definition:* `subspace(v) = v₁`.
- *Postconditions:* (a) `subspace(v) ∈ ℕ` — the projected component inherits T0's ℕ-valued carrier (ASN-0034). (b) When `v` satisfies S8a, `subspace(v) ≥ 1` — S8a's componentwise positivity conjunct `(A i : 1 ≤ i ≤ #v : vᵢ > 0)` at `i = 1` delivers `v₁ ≥ 1`.
- *Depends:* T0 (ASN-0034) — ℕ-valued component carrier underwriting postcondition (a); S8a — componentwise positivity at `i = 1` underwriting postcondition (b).

**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. Any correct implementation must satisfy this constraint.

*Formal Contract:*
- *Axiom (design requirement):* `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ subspace(v₁) = subspace(v₂) : #v₁ = #v₂)`.
- *Postconditions:* Within a subspace `s` of document `d`, there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`. Distinct subspaces may have distinct depths.
- *Depends:* S8a — for the lower bound `m_s ≥ 2`.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: position `s.x` is followed by `s.(x+1)`, where `+1` is NAT addition on the ordinal component. We reserve the symbol `+` for NAT addition on components and indices throughout this ASN; tumbler ordinal displacement is always written `shift(v, k)` (equivalently `v ⊕ δ(k, m)` per ASN-0034), never `v + k`.

We extend `shift` to `k = 0` by convention: define `shift(v, 0) = v` (identity); for `k ≥ 1`, `shift(v, k) = v ⊕ δ(k, #v)` per OrdinalShift (ASN-0034). OrdinalShift's precondition is `n ≥ 1`; the extension to `k = 0` is purely notational — no arithmetic is performed. For I-addresses, `shift(a, 0) = a` and `shift(a, k) = a ⊕ δ(k, #a)` for `k ≥ 1`. This is well-defined: the action point of `δ(k, #a)` is `#a`, which falls at the element field's last component — S7c guarantees element-field depth `δ ≥ 2`, so the last component of the full address *is* the element ordinal's deepest position — and TumblerAdd's prefix rule copies all earlier components (node, user, document fields, their separators, and the subspace identifier) unchanged, producing a result of length `#a`.

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that the arrangement preserves ordinal displacement within the run:

`(A k : 0 ≤ k < n : Σ.M(d)(shift(v, k)) = shift(a, k))`

At `k = 0` this is the base case `M(d)(v) = a`. Each subsequent `k` increments both the V-ordinal and the I-ordinal by the same amount. Within a correspondence run, each step forward in Vstream corresponds to the same step forward in Istream.

**S8 (Finite span decomposition).** For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the V-positions: every V-position in `dom(Σ.M(d))` falls in exactly one run — `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ)))`

(b) Within each run: `Σ.M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for all `k` with `0 ≤ k < nⱼ`

Each run represents a contiguous block of content that entered the arrangement as a unit — characters typed sequentially, or a span transcluded whole.

*Proof.* We construct a finite decomposition satisfying both conjuncts and prove it partitions `dom(M(d))`.

**Existence.** By S8-fin, `dom(M(d))` is finite. By S2 (ArrangementFunctionality), `M(d)` is a function, so each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)`. By S3 (referential integrity), `a ∈ dom(Σ.C)`. For each such `v`, form the singleton run `(v, a, 1)`. Conjunct (b) requires `M(d)(shift(v, k)) = shift(a, k)` for all `k` with `0 ≤ k < 1` — the only such `k` is `0`, where `shift(v, 0) = v` and `shift(a, 0) = a` by convention, so the identity reduces to `M(d)(v) = a`, which holds by construction. Since `dom(M(d))` is finite, the collection of singletons is finite. The singleton decomposition witnesses existence.

**Coverage.** Each `v ∈ dom(M(d))` lies in its own singleton's interval: `v ≤ v < shift(v, 1)`, where the right inequality holds because `shift(v, 1) > v` by TS4 (ShiftStrictIncrease, ASN-0034). So every V-position falls in at least one run.

**Uniqueness within a subspace.** Let `v, w ∈ dom(M(d))` be distinct V-positions with `v₁ = w₁ = S`. By S8-depth, `#v = #w = m` for some common depth `m`. We show `w ∉ [v, shift(v, 1))` via a clean lemma that abstracts away from the specific pair `(v, w)`.

**Within-subspace incompatibility lemma.** Let `v` be as above (a V-position with `v₁ = S`, `#v = m ≥ 2`, satisfying S8a). For any tumbler `t` with `t₁ = S`, `#t = m`, and `t ≠ v`: `t ∉ [v, shift(v, 1))`.

*Proof of lemma.* Suppose for contradiction that `t ∈ [v, shift(v, 1))`, i.e. `v ≤ t < shift(v, 1)`. Since `#t = #v = m`, the sequences diverge at some first position `j ≤ m`. The shared first component `t₁ = v₁ = S` forces `j ≥ 2`. At `m = 2` this further forces `j = m = 2`, leaving only Case j = m below; for `m ≥ 3`, both branches `2 ≤ j < m` and `j = m` are possible. Both branches yield contradictions.

*Case j < m.* Then `tᵢ = vᵢ` for `i < j`. The lemma's hypothesis `t ≠ v` combined with `v ≤ t` (from `t ∈ [v, shift(v, 1))`) strengthens to `v < t` — the non-strict relation `v ≤ t` resolves to strict `<` once equality is ruled out. T1(i) applied to `v < t` with first divergence at component `j` (valid since `j ≤ m = min(m, m)`) then yields `tⱼ > vⱼ`. Since `shift(v, 1)ⱼ = vⱼ` (as `j < m`), and `tᵢ = vᵢ = shift(v, 1)ᵢ` for `i < j`, the first divergence between `t` and `shift(v, 1)` is at position `j` with `tⱼ > shift(v, 1)ⱼ`, giving `t > shift(v, 1)` by T1(i) — contradicting `t < shift(v, 1)`.

*Case j = m.* Then `tᵢ = vᵢ` for `i < m`. Since `shift(v, 1)ᵢ = vᵢ` for `i < m` by TumblerAdd's prefix rule (the action point of `δ(1, m)` is `m`, so all components at positions `i < m` are copied from `v` unchanged), we get `tᵢ = shift(v, 1)ᵢ` for `i < m`, so the first divergence between `t` and `shift(v, 1)` is at position `m`. Since `tᵢ = vᵢ` for `i < m` and `t ≠ v` (with `#t = #v = m`), the divergence at `j = m` between `t` and `v` is also real: `t_m ≠ v_m`. Combined with `v ≤ t`, this gives `v < t`, and T1(i) applied to `v < t` with first divergence at `m` yields strict `t_m > v_m`; NAT-discrete (ASN-0034) at `(m, n) := (v_m, t_m)` promotes the strict inequality `v_m < t_m` to `v_m + 1 ≤ t_m`, i.e., `t_m ≥ v_m + 1`. From `t < shift(v, 1)` with first divergence at `m`: T1(i) gives `t_m < shift(v, 1)_m`, and the setup identity `shift(v, 1)_m = v_m + 1` (TumblerAdd at the action point; `v_m + 1 ∈ ℕ` by NAT-closure, ASN-0034) rewrites this to `t_m < v_m + 1`. But `t_m ≥ v_m + 1` and `t_m < v_m + 1` are incompatible by NAT-order's exactly-one trichotomy (ASN-0034), instantiated at `(t_m, v_m + 1)` — the clause `¬(a < b ∧ b ≤ a)` excludes the conjunction of the two inequalities. Contradiction. ∎ *(lemma)*

*Application to w.* The hypotheses `w₁ = v₁ = S`, `#w = m` (S8-depth), and `w ≠ v` are exactly the lemma's antecedents, so `w ∉ [v, shift(v, 1))`. Since all V-positions in subspace `S` share depth `m` (S8-depth) and the lemma applies to every such position distinct from `v`, no distinct V-position in the same subspace falls in `v`'s singleton interval.
**Uniqueness across subspaces.** Let `v ∈ dom(M(d))` with `v₁ = S₁` and `w ∈ dom(M(d))` with `w₁ = S₂`, where `S₁ ≠ S₂`. By S8a, `v` and `w` extend the single-component prefixes `[S₁]` and `[S₂]` respectively, and both have depth `≥ 2`. These prefixes are non-nesting: `[S₁] ≼ [S₂]` would require `S₁ = S₂` (both length-1 tumblers, so equality requires componentwise agreement by T3), contradicting `S₁ ≠ S₂`; symmetrically `[S₂] ⋠ [S₁]`.

For `m ≥ 2` (the only case under S8a), the successor `shift(v, 1)` also extends `[S₁]`: by OrdinalShift (ASN-0034), `shift(v, 1) = v ⊕ δ(1, m)`, and since `δ(1, m)` has action point `m`, TumblerAdd's prefix rule (ASN-0034) copies every component at positions `i < m` from `v` unchanged. Since `m ≥ 2`, this includes position 1, giving `shift(v, 1)₁ = v₁ = S₁`.

Since `[S₁] ≼ v` and `[S₁] ≼ shift(v, 1)` and `v ≤ shift(v, 1)` by TS4 (ShiftStrictIncrease, ASN-0034), T5 (ContiguousSubtrees, ASN-0034) gives: for any `t` with `v ≤ t ≤ shift(v, 1)`, `[S₁] ≼ t`. Every element of `[v, shift(v, 1))` therefore extends `[S₁]`. By T10 (ASN-0034), since `[S₁]` and `[S₂]` are non-nesting prefixes, any tumbler extending `[S₁]` is distinct from any tumbler extending `[S₂]`. In particular, `w` (which extends `[S₂]`) cannot belong to `[v, shift(v, 1))`.

**Conclusion.** The singleton runs cover every V-position in `dom(M(d))` (coverage) and no V-position falls in two distinct singleton intervals (uniqueness within and across subspaces). The singletons partition `dom(M(d))`. Since `dom(M(d))` is finite (S8-fin), the decomposition is finite, establishing both conjuncts (a) and (b). ∎

*Formal Contract:*
- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); referential integrity (S3); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` (S8a); within each subspace, all V-positions share a common depth (S8-depth).
- *Postconditions:* (*Existence.*) There exists a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` satisfying (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ)))` and (b) `(A j, k : 0 ≤ k < nⱼ : M(d)(shift(vⱼ, k)) = shift(aⱼ, k))`. The proof exhibits the singleton decomposition (every `nⱼ = 1`), for which conjunct (b) reduces to the base case `M(d)(vⱼ) = aⱼ` at `k = 0`.
- *Depends:* (*Local properties*) S2 (ArrangementFunctionality) — each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)`; S3 (referential integrity) — `M(d)(v) ∈ dom(Σ.C)`; S8a — `zeros(v) = 0`, `#v ≥ 2`, and componentwise positivity of V-positions; S8-depth — a common depth `m` for every V-position in a fixed subspace; S8-fin — finite `dom(M(d))`. (*Foundation claims, ASN-0034*) T1 (TumblerOrdering) case (i) — first-divergence comparison; T3 (CanonicalRepresentation) — equates tumblers with their canonical component sequences; T4 (HierarchicalParsing) — partitions tumblers into N/U/D/E fields; T5 (ContiguousSubtrees) — a prefix's extensions form a contiguous interval under T1; T10 — non-nesting prefixes generate disjoint tumbler subtrees; TS4 (ShiftStrictIncrease) — `v < shift(v, 1)`; TumblerAdd, OrdinalShift, OrdinalDisplacement — the action-point semantics of `δ(k, m)`, the three-region component formula, and the action-point identity `shift(v, 1)_m = v_m + 1`. NAT-discrete (NatDiscreteness) — the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n`. NAT-closure (NatArithmeticClosureAndIdentity) — closure of ℕ under addition places `v_m + 1` in ℕ. NAT-order (NatStrictTotalOrder) — the exactly-one trichotomy clause `¬(a < b ∧ b ≤ a)`.

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
- *Depends:* T0 (ℕ-valued carrier, ASN-0034); ActionPoint (ASN-0034) — the postcondition `actionPoint(w_ord) = actionPoint(w) − 1` follows from ActionPoint's definition applied to the index-shifted sequence `(w_ord)ⱼ = w_{j+1}`.
- *Frame:* Pure function on the component sequence of `w` — no state is read or modified.

The definitions above decompose V-positions into subspace context and ordinal operand. We now show that `ord` and `⊕` commute.

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
- *Preconditions:* `v ∈ T`, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.
- *Postconditions:* (a) `ord(v ⊕ w) = ord(v) ⊕ w_ord`. (b) `subspace(v ⊕ w) = subspace(v)`. (c) `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`. (Derivations of (b) and (c) are given in the proof body above.)
- *Depends:* ord, w_ord, vpos (definitions above); TumblerAdd (PositionAdvance, ASN-0034) — the three-region component formula; TA0 (length preservation, ASN-0034) — for part (c); ActionPoint (ASN-0034) — for the implicit `actionPoint(w) ≤ m` bound.
- *Frame:* Both sides are computed from `v` and `w` alone — no state is consulted.

**OrdAddS8a** — *AdditionPreservesS8a* (LEMMA). For a V-position `v` satisfying S8a with `#v = m ≥ 2`, and a displacement `w` with `w₁ = 0`, `#w = m`, `Pos(w)` (TA-Pos, ASN-0034): `v ⊕ w` satisfies S8a if and only if all components of `w_ord` after its action point are positive.

*Proof.* Let `r = v ⊕ w` with `k = actionPoint(w) ≥ 2`. By TumblerAdd, the components of `r` partition into three regions:

- `r₁ = v₁ ≥ 1` (by S8a on `v`, and `w₁ = 0` so `1 < k` and TumblerAdd copies from `v`).
- For `2 ≤ i < k`: `rᵢ = vᵢ ≥ 1` (by S8a on `v`).
- At `i = k`: `rₖ = vₖ + wₖ ≥ 1 > 0`, from `vₖ ≥ 1` (S8a on `v`) and `wₖ ∈ ℕ`.
- For `k < i ≤ m`: `rᵢ = wᵢ` (copied from the displacement).

As established for OrdAddHom's three-region enumeration, the boundary regimes of `k` collapse one or both side regions to the empty range (here the middle range `2 ≤ i < k` at `k = 2`, the trailing range `k < i ≤ m` at `k = m`); the case analysis remains correct under these collapses, since empty ranges contribute nothing and the unconditionally positive components stay positive.

Components `r₁` through `rₖ` are unconditionally positive. S8a requires `zeros(r) = 0` and `(A i : 1 ≤ i ≤ #r : rᵢ > 0)`, which reduces to: every component is positive. The only components that can fail are `r_{k+1}, ..., r_m = w_{k+1}, ..., w_m` — exactly the tail components of `w`, which are the tail components of `w_ord` (since `(w_ord)_j = w_{j+1}` and the action point of `w_ord` is `k - 1`). Therefore:

`v ⊕ w satisfies S8a ⟺ (A i : k < i ≤ m : wᵢ > 0) ⟺ all tail components of w_ord are positive`

The second postcondition form follows by connecting through OrdAddHom: `ord(v ⊕ w) = ord(v) ⊕ w_ord`, and since `ord(v) ∈ S` (componentwise positive by S8a on `v`), `ord(v ⊕ w) ∈ S` reduces to whether `w_ord`'s tail past its action point is positive — exactly the condition `(A i : k < i ≤ m : wᵢ > 0)` derived above. Hence `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`. Instance (b) above confirms the boundary: `w_ord = [4, 0]` has a zero after the action point, and `v ⊕ w = [1, 7, 0]` fails S8a. ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T` satisfying S8a, `#v = m ≥ 2`; `w ∈ T`, `Pos(w)` (TA-Pos, ASN-0034), `#w = m`, `w₁ = 0`.
- *Postconditions:* `v ⊕ w satisfies S8a ⟺ (A i : actionPoint(w) < i ≤ m : wᵢ > 0)`. Equivalently, `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a`.
- *Depends:* OrdAddHom (lemma above); TumblerAdd (PositionAdvance, ASN-0034) — three-region component formula; ActionPoint (ASN-0034) — for the implicit `actionPoint(w) ≤ m` bound; S8a (V-position well-formedness) — supplies `vₖ ≥ 1` at the action-point component.

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

Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." This statement is specific to the text subspace (S = 1), where Nelson's "addresses 1 through 100" describes character positions. The properties below (D-CTG, D-MIN, D-CTG-depth, D-SEQ) bind `S = 1` in their formal statements and constrain only the text subspace; contiguity semantics for other subspaces are out of scope for this ASN.

Write `S = subspace(v) = v₁` for the subspace identifier (the first component of the element-field V-position), and `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` for the set of V-positions in subspace S of document d. The specialization to the text subspace is `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}`. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**D-CTG (VContiguity).** For each document d, V_1(d) (the text subspace) is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`

In words: within the text subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

*Formal Contract:*
- *Axiom (design requirement):* `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`.
- *Preconditions:* `subspace(v) = 1`; V-positions share a common depth (S8-depth).
- *Postconditions:* V_1(d) is either empty or occupies every position strictly between its extremes (at the fixed depth).
- *Frame:* D-CTG is a constraint on well-formed text-subspace arrangements.
- *Depends:* S8a (V-position well-formedness); S8-depth (common depth within subspace); T1 (TumblerOrdering, ASN-0034) — defines the order.

For the text subspace at depth m = 2, this is a finite condition: the intermediates between [1, a] and [1, b] are the finitely many [1, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_1(d) occupies a single unbroken block of ordinals.

At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction: all positions in V_1(d) must share components 2 through m − 1. The intuition — formalized as D-CTG-depth and proved below — is that if two positions diverged before the last component, then any choice of natural number n could be slotted into the next component to yield an intermediate; D-CTG would force all such intermediates into V_1(d), producing infinitely many positions and contradicting S8-fin.

**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_1(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_1(d) be non-empty with common depth `m` (S8-depth) and `m ≥ 3` (non-triviality bound, per the Preconditions). Suppose for contradiction that V_1(d) contains two positions v₁ and v₂ with v₁ < v₂ (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j, and (v₁)ⱼ < (v₂)ⱼ (the inequality follows from v₁ < v₂ by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

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
- *Preconditions:* V_1(d) non-empty; common depth `m` (S8-depth); `m ≥ 3` (the lemma's non-triviality bound, additional to S8-depth — at `m = 2` the conclusion holds vacuously since the range of shared components 2 through `m − 1` is empty).
- *Postconditions:* `(A v₁, v₂ ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of V_1(d) reduces to contiguity of the m-th (last) component.
- *Depends:* (*Local properties*) D-CTG (VContiguity) — any tumbler strictly between two positions in subspace 1 at depth `m` lies in `V_1(d)`; S8a — `m ≥ 2` and componentwise positivity of V-positions; S8-depth — common depth `#w = m`; S8-fin — finiteness of `V_1(d)`. (*Foundation claims, ASN-0034*) T0(a) (UnboundedComponentValues) — for any bound `M`, a natural-number witness `n > M`; T1 case (i) (TumblerOrdering) — first-divergence comparison; T3 (CanonicalRepresentation) — distinct component sequences yield distinct tumblers.

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

**D-MIN (VMinimumPosition).** For each document d with V_1(d) non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in the text subspace per S8-depth), and every component is 1.

At depth 2 this gives min(V_1(d)) = [1, 1]. Combined with D-CTG and S8-fin, a document with n text elements occupies V-positions [1, 1] through [1, n] — matching Nelson's "addresses 1 through 100."

*Formal Contract:*
- *Axiom (design requirement):* `V_1(d) ≠ ∅ ⟹ min(V_1(d)) = [1, 1, ..., 1]` of length `m_1` (the common depth per S8-depth).
- *Preconditions:* V_1(d) non-empty; common depth `m_1` (S8-depth) with `m_1 ≥ 2` (S8a).
- *Postconditions:* Every component of `min(V_1(d))` equals 1; in particular the text subspace identifier `min(V_1(d))₁ = 1` and the within-subspace ordinal starts at the minimum positive value.
- *Depends:* S8a, S8-depth, T1 (TumblerOrdering, ASN-0034) — defines `min`.

We now derive the general form: the contiguity, minimum, and finiteness constraints together force V_1(d) into a single block of last-component values. The proof below establishes this in four steps.

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
- *Depends:* (*Local properties*) D-CTG (VContiguity) — any tumbler strictly between attained positions in subspace 1 at depth `m` lies in `V_1(d)`; D-CTG-depth (SharedPrefixReduction) — at `m ≥ 3`, all positions in `V_1(d)` share components 2 through `m − 1`; D-MIN (VMinimumPosition) — `min(V_1(d)) = [1, …, 1]`; S8a — `m ≥ 2`; S8-depth — the common depth `m`; S8-fin — finiteness of `V_1(d)`. (*Foundation claims, ASN-0034*) T1 case (i) (TumblerOrdering) — first-divergence comparison.

D-CTG is a design constraint on well-formed document states. It constrains which arrangement modifications constitute well-formed editing operations. We verify the base case: before any operations, dom(M(d)) = ∅ for all d (the arrangement is a partial function; no content has been allocated, so no V-mapping exists), so V_1(d) = ∅. D-CTG holds vacuously (no u, q exist to trigger its antecedent), and D-MIN holds vacuously (its antecedent requires V_1(d) non-empty).

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

**Definition (ValidInsertionPosition, non-empty case).** For a document `d` with `V_1(d) ≠ ∅`, the *binary* predicate `ValidInsertionPosition(d, v)` is satisfied when:

- The common V-position depth `m` of V_1(d) is fixed by S8-depth and read from state — it is *not* a parameter of the predicate. By S8a, `m ≥ 2`.
- Setting `N = |V_1(d)|`, the predicate holds iff `v = shift(min(V_1(d)), j)` for some `j ∈ {0, 1, ..., N}` (taking `shift(·, 0)` as the identity, so the `j = 0` case is `v = min(V_1(d))`).

There are exactly `N + 1` valid insertion positions: the `N` positions coinciding with existing V-positions `v₀` through `v_{N−1}`, plus the append position `shift(min(V_1(d)), N)`.

**Definition (ValidFirstInsertionPosition, empty case).** For a document `d` with `V_1(d) = ∅`, the *ternary* predicate `ValidFirstInsertionPosition(d, v, m)` is satisfied when `m ∈ ℕ` with `m ≥ 2` and `v = [1, 1, ..., 1]` of depth `m`. Here `m` is an operational input chosen by the placing operation — distinct values of `m` identify distinct valid positions. The strand model fixes only the lower bound `m ≥ 2`; the specific value is an allocation convention.

For `m ≥ 2`, `δ(n, m)` has action point `m > 1`, so TumblerAdd copies component 1 unchanged and the subspace identifier is preserved. This is the canonical minimum position required by D-MIN. Basic INSERT typically commits to `m = 2`.

In both predicates, `v₁ = 1` is the text subspace identifier.

By D-MIN, `min(V_1(d)) = [1, 1, ..., 1]` of depth `m` (where `m` is the state-fixed common depth in the non-empty case, or the chosen depth in the empty case). By OrdinalShift and TumblerAdd, `shift([1, 1, ..., 1], j) = [1, 1, ..., 1] ⊕ δ(j, m)`; since `δ(j, m)` has action point `m` and `m ≥ 2`, TumblerAdd copies components 1 through `m − 1` unchanged and sets the last component to `1 + j`. The explicit form for the non-empty case is `shift(min(V_1(d)), j) = [1, 1, ..., 1 + j]`. Distinctness of the `N + 1` valid positions is the one step worth spelling out: for `j, j' ∈ {0, ..., N}` with `j ≠ j'`, the last components `1 + j` and `1 + j'` differ (NAT-order, ASN-0034), so the two length-`m` tumblers diverge at position `m` and are distinct by T3 (CanonicalRepresentation, ASN-0034). Hence the predicate is satisfied by exactly `N + 1` distinct positions.

*Formal Contract (ValidInsertionPosition, non-empty case).*
- *Signature:* `ValidInsertionPosition(d, v)` — a *binary* predicate on document `d` and V-position `v`. The common V-position depth `m` is determined by `d` via S8-depth and read from state.
- *Preconditions:* Document `d` with `V_1(d) ⊆ dom(M(d))` non-empty; D-CTG holds on V_1(d); D-MIN gives `min(V_1(d)) = [1, ..., 1]` and D-SEQ gives `V_1(d) = {[1, ..., 1, k] : 1 ≤ k ≤ N}` (both needed to discharge the explicit form (d)); `m ≥ 2` is the common depth of V_1(d) by S8-depth and S8a.
- *Definition:* `ValidInsertionPosition(d, v)` holds iff, writing `N = |V_1(d)|`, `v = shift(min(V_1(d)), j)` for some `j ∈ {0, 1, ..., N}` (with `shift(·, 0) = identity`).
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m` (the state-fixed common depth). (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d`, exactly `N + 1` values of `v` satisfy the predicate. (d) The explicit form is `v = [1, 1, ..., 1 + j]` with last component `1 + j` and all preceding components equal to 1.
- *Depends:* D-MIN, D-CTG, D-CTG-depth, D-SEQ; S8a, S8-fin, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

*Formal Contract (ValidFirstInsertionPosition, empty case).*
- *Signature:* `ValidFirstInsertionPosition(d, v, m)` — a *ternary* predicate on document `d`, V-position `v`, and depth `m`. The depth `m` is an operational input chosen by the placing operation; the strand model fixes only the lower bound `m ≥ 2`.
- *Preconditions:* Document `d` with `V_1(d) = ∅`; `m ∈ ℕ` with `m ≥ 2`.
- *Definition:* `ValidFirstInsertionPosition(d, v, m)` holds iff `v = [1, 1, ..., 1]` of depth `m`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m`. (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d` and `m`, exactly one value of `v` satisfies the predicate. (d) Once the position is placed, S8-depth fixes the depth at `m` for all subsequent positions in the text subspace, after which validity of further insertion positions is governed by `ValidInsertionPosition(d, v)`.
- *Depends:* D-MIN; S8a, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

### Valid insertion position examples

**Non-empty case (binary predicate).** Let subspace S = 1 and suppose V₁(d) = {[1, 1], [1, 2], [1, 3]}, so N = 3 and min(V₁(d)) = [1, 1]. The depth `m = 2` is read from state via S8-depth. The values of `v` satisfying `ValidInsertionPosition(d, v)` are:

- j = 0: v = min(V₁(d)) = [1, 1]
- j = 1: v = shift([1, 1], 1) = [1, 2]
- j = 2: v = shift([1, 1], 2) = [1, 3]
- j = 3: v = shift([1, 1], 3) = [1, 4]

That gives N + 1 = 4 positions. After an operation places new content at, say, [1, 2] — with whatever displacement mechanism the operation defines — the resulting V₁(d) must satisfy D-CTG and D-MIN. Verifying this is the operation's obligation, not the predicate's.

**Empty case (ternary predicate).** V₁(d) = ∅. Choosing depth m = 2, the unique `v` satisfying `ValidFirstInsertionPosition(d, v, 2)` is `[1, 1]`. D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands. Choosing m = 3 instead, `ValidFirstInsertionPosition(d, v, 3)` is satisfied uniquely by `v = [1, 1, 1]`; by T3, this is a different tumbler.


## The separation theorem

We can now state the property that Nelson calls "the architectural foundation of everything" as an immediate corollary of S0 rather than a separate axiom.

**S9 (Two-stream separation), corollary of S0.** S9 is S0 read directionally: arrangement-only transitions (`Σ'.M(d) ≠ Σ.M(d)`) cannot alter `C`, since S0 already holds for every transition unconditionally.

This realises Nelson's design: "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." The two state components are coupled only through S3 (referential integrity): arrangements depend on the content store — S3 requires every V-reference to resolve — but the content store is independent of all arrangements. Changes to any `M(d)` cannot break `C`; changes to `C` could break `M`, which is precisely why `C` is immutable.

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

- *Right side: `shift(1.0.1.0.1.0.1.1, 3)`.* The I-address `a = 1.0.1.0.1.0.1.1` has depth `#a = 8` (three field-separator zeros plus five non-separator components), so `shift(a, 3) = a ⊕ δ(3, 8) = [1, 0, 1, 0, 1, 0, 1, 1] ⊕ [0, 0, 0, 0, 0, 0, 0, 3]` (action point 8 — the element ordinal's last component). TumblerAdd copies components 1 through 7 from `a` unchanged — including the three separator zeros at positions 2, 4, 6 (so `zeros(shift(a, 3)) = zeros(a) = 3` — the prefix rule copies every position before the action point unchanged, preserving the zero/nonzero status of each) and the subspace identifier `subspace_I(a) = E(a)₁ = 1` at position 7 — and sets component 8 to `1 + 3 = 4`, yielding `[1, 0, 1, 0, 1, 0, 1, 4] = 1.0.1.0.1.0.1.4`.

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
| S7a | Document-scoped allocation: every I-address is allocated under the originating document's prefix | design; uses T4, T4b, T10a, T10a.4 (ASN-0034), S7b |
| S7b | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | design; uses T4, T4b, T10a.4, S0 (ASN-0034) |
| S7c | Element-field depth: `(A a ∈ dom(C) :: #E(a) ≥ 2)` — subspace identifier and content ordinal occupy distinct components | design; uses T4b (ASN-0034), S7b |
| S7d | Document allocation discipline: every document is addressed by a document-level tumbler (`zeros = 2`) allocated via T10a under the owning user's prefix; distinct documents arise from distinct allocation events | design; uses T10a, T10a.4, T4 (ASN-0034) |
| subspace_I(a) | I-address subspace identifier: `subspace_I(a) = E(a)₁`; well-defined when S7c holds | introduced |
| S7 | Structural attribution: `origin(a) = N(a).0.U(a).0.D(a)` — full document prefix | from S7a, S7b, S7d, S0, S4, T4, T4b, T3, T10a.4, GlobalUniqueness (ASN-0034) |
| S8-fin | Finite arrangement: `dom(M(d))` is finite for every document `d` | design requirement |
| S8a | V-position well-formedness: `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` — element-field tumblers of depth ≥ 2 with componentwise positive entries | definition (V-positions are isolated element fields of depth ≥ 2, paralleling S7c; `zeros(v) = 0` and `#v ≥ 2` are definitional); positivity derived from `zeros = 0` via T0, NAT-discrete (ASN-0034) |
| subspace(v) | V-position subspace identifier: `subspace(v) = v₁`; well-defined when `#v ≥ 1` | introduced; uses T0 (ASN-0034), S8a |
| S8-depth | Fixed-depth V-positions: `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` | design; uses S8a |
| S8 | Span decomposition: `dom(M(d))` decomposes into finitely many correspondence runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for `0 ≤ k < nⱼ` | theorem from S2, S3, S8-fin, S8a, S8-depth, T1, T3, T4, T5, T10, TumblerAdd, OrdinalShift, OrdinalDisplacement, TS4, NAT-discrete, NAT-closure, NAT-order (ASN-0034) |
| ord(v) | Ordinal extraction: ord(v) = [v₂, ..., vₘ]; when v satisfies S8a, ord(v) ∈ S | introduced |
| vpos(S, o) | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord for any o ∈ T; satisfies S8a when S ≥ 1 and all oᵢ > 0 | introduced |
| w_ord | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for displacement w with w₁ = 0 | introduced |
| OrdAddHom | (a) ord(v ⊕ w) = ord(v) ⊕ w_ord; (b) subspace(v ⊕ w) = subspace(v); (c) v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord) | lemma from ord, w_ord, TumblerAdd, TA0 (ASN-0034) |
| OrdAddS8a | v ⊕ w satisfies S8a ⟺ all tail components of w after the action point are positive; equivalently ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a | lemma from OrdAddHom, S8a, TumblerAdd (ASN-0034) |
| OrdShiftHom | ord(shift(v, n)) = shift(ord(v), n); shift(v, n) unconditionally satisfies S8a when v does | corollary from OrdAddHom, OrdAddS8a, OrdinalShift, OrdinalDisplacement (ASN-0034) |
| D-CTG | V-position contiguity: V_1(d) forms a contiguous ordinal range with no gaps — design constraint on well-formed document states | design; uses S8a, S8-depth, T1 (ASN-0034) |
| D-MIN | V-position minimum: non-empty V_1(d) has minimum [1, 1, ..., 1] with every component equal to 1 — design constraint | design requirement |
| D-CTG-depth | Shared prefix reduction (applies wherever D-CTG holds): at depth m ≥ 3, all positions in V_1(d) share components 2 through m − 1, so contiguity reduces to the last component | corollary of D-CTG, S8a, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034) |
| D-SEQ | Sequential positions: non-empty V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 | from D-CTG, D-CTG-depth, D-MIN, S8a, S8-fin, S8-depth, T1 (ASN-0034) |
| ValidInsertionPosition | Binary predicate `ValidInsertionPosition(d, v)` (non-empty case): when V_1(d) ≠ ∅, m is the common depth of V_1(d) (state-determined via S8-depth), and v = shift(min(V_1(d)), j) for j ∈ {0, ..., N} where N = |V_1(d)| | introduced |
| ValidFirstInsertionPosition | Ternary predicate `ValidFirstInsertionPosition(d, v, m)` (empty case): when V_1(d) = ∅, m ≥ 2 is an operational input chosen by the placing operation, and v = [1, 1, ..., 1] of depth m | introduced |
| S9 | Two-stream separation: arrangement changes cannot alter stored content | named directional reading of S0 (no formal content beyond S0) |


## Open Questions

What constraints must the content store's value domain `Val` satisfy — must all entries be uniform in type, or must `Val` support heterogeneous content (text, links, media) as first-class distinctions?

Must the span decomposition of an arrangement have a unique maximal form (fewest possible runs), or can multiple valid decompositions of different cardinality coexist for the same arrangement?

What must the system guarantee about the computability of the sharing inverse — given an I-address, what is the cost bound for determining which documents currently reference it?

Under what conditions, if any, may the referential integrity invariant S3 be temporarily violated — must it hold at every observable state, or only at quiescent states between operations?

What abstract property distinguishes content that exists but is unreachable from all current arrangements from content that exists and is reachable — and must the system maintain this distinction as queryable state?

Does each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) preserve D-CTG and D-MIN?

What invariants must the displacement mechanism satisfy so that insertion at a ValidInsertionPosition preserves D-CTG, D-MIN, and S2?

The strand model fixes only the lower bound m ≥ 2 for V-position depth in an empty subspace; the specific value is a one-time allocation convention chosen by the first-placing operation, not a strand-level commitment. What operation-layer constraints determine the canonical choice of m (e.g., m = 2 for basic INSERT/DELETE versus deeper subdivisions Nelson contemplated)? What downstream capabilities — nested hierarchies, link subdivision, future extensibility — does each depth choice unlock or foreclose?

What must an operation guarantee about existing V-to-I mappings when it inserts at a position that coincides with an occupied V-position?

The strand model treats subspace alignment — `subspace(v) = subspace_I(M(d)(v))` for every V-position — as an operations-layer preservation obligation rather than a state-level invariant on arrangements. Which editing operations must establish this alignment for the V-positions they produce, and under what allocation conventions is preservation automatic versus requiring explicit operation-level enforcement?

Under what conditions on w does the subtraction homomorphism ord(v ⊖ w) = ord(v) ⊖ w_ord hold, given TA7a's conditional S-membership results for subtraction?

What are the precise conditions for the round-trip property (ord(v) ⊕ w_ord) ⊖ w_ord = ord(v)?
