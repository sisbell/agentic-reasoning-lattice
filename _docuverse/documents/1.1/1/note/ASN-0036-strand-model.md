# ASN-0036: Strand Model

*2026-03-14; revised 2026-03-21, 2026-03-22, 2026-03-22, 2026-03-28, 2026-04-09, 2026-04-11, 2026-05-29*

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
- *Axiom (domain restriction):* `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` — arrangements map only V-positions; every active key is a zero-free tumbler of depth at least 2 (a subspace identifier followed by a within-subspace ordinal).
- *Definition:* `dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.
- *Definition:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.

We call this paired state the *strand*: the two-component object `(Σ.C, Σ.M)` — an immutable content store woven together with the family of mutable arrangements that reference it. The remainder of this ASN derives the invariants that govern a strand.

## The content store

We ask: what must `C` guarantee? Nelson requires that any historical version be reconstructable, that content transcluded across documents maintain its meaning, and that attribution be permanent. Working backward from these guarantees — what must `C` satisfy for them to hold?

Suppose `C(a)` could change from value `w` to `w'` in some state transition. Then every document whose arrangement maps a V-position to `a` would silently show different content — with no editing operation having touched any arrangement. Historical versions, which reconstruct their state by reassembling Istream fragments, would silently present altered text. Content transcluded from one document into another would mutate without the including document's knowledge or consent. Nelson: "Users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." Mutation of `C(a)` damages every original that contains `a`.

We therefore require:

**S0 (Content immutability).** For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

Once content is stored at address `a`, both the address and its value are fixed for all future states. This is the central invariant of the two-stream architecture.

*Formal Contract:*
- *Axiom (design requirement):* For every state transition `Σ → Σ'`, `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`.
- *Postconditions:* (a) Domain persistence — `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)`. (b) Value preservation — `a ∈ dom(Σ.C) ⟹ Σ'.C(a) = Σ.C(a)`.
- *Frame:* No condition on arrangements — the postcondition holds for arbitrary `Σ'.M(d)` and arbitrary changes to any document's arrangement.

**S1 (Store monotonicity).** `[dom(Σ.C) ⊆ dom(Σ'.C)]`

S0 and S1 together establish `C` as an *append-only log*. New entries may be added — each at a fresh address guaranteed unique by T9 and T10 (ASN-0034) — but no existing entry may be modified or removed.

Nelson states this as an explicit design commitment: "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." Gregory's implementation confirms the commitment. Of the seventeen FEBE commands Nelson specifies, none modifies existing Istream content. There is no MODIFY, UPDATE, or REPLACE operation. The absence is structural — the protocol provides no mechanism for mutating stored content.

*Proof.* We wish to show that for every state transition `Σ → Σ'`, `dom(Σ.C) ⊆ dom(Σ'.C)`.

Let `a ∈ dom(Σ.C)` be arbitrary. By S0 (content immutability), `a ∈ dom(Σ.C)` implies the conjunction `a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)`. The first conjunct yields `a ∈ dom(Σ'.C)` directly. Since `a` was chosen arbitrarily from `dom(Σ.C)`, we have established `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C))`, which is `dom(Σ.C) ⊆ dom(Σ'.C)` by definition of subset inclusion. ∎

*Formal Contract:*
- *Preconditions:* State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Postconditions:* `dom(Σ.C) ⊆ dom(Σ'.C)`.


## The arrangement and referential integrity

Vstream is where mutability lives. Each document's arrangement `M(d)` maps V-positions to I-addresses, presenting stored content as a readable sequence. Unlike `C`, arrangements change freely — content can be added, removed, and reordered.

**S2 (Arrangement functionality).** For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

This is inherent in the concept of a "virtual byte stream." Nelson: "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." Each position in the stream shows exactly one piece of content, regardless of native origin — a V-position cannot simultaneously contain two different things, even when the I-addresses appearing in a single arrangement are scattered across multiple documents' Istreams.

*Formal Contract:*
- *Axiom (definitional):* `Σ.M(d) : T ⇀ T` is a (partial) function — `(A d, v, a₁, a₂ : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a₁ ∧ Σ.M(d)(v) = a₂ : a₁ = a₂)`.
- *Postconditions:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` is a well-defined set.

The bridge between the two state components is a well-formedness condition:

**S3 (Referential integrity).** `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

Every V-reference resolves. If a document's arrangement says "at position `v`, display the content at I-address `a`," then `a` must be in `dom(C)`. There are no dangling references.

Any transition that establishes a V-mapping `M(d)(v) = a` must therefore have `a ∈ dom(Σ'.C)` in the post-state. S1 (store monotonicity) then guarantees that once `a` enters `dom(C)` it remains, so a valid reference cannot become dangling through any subsequent state transition.

Content unreferenced by any current arrangement still persists. Since S0's antecedent is `a ∈ dom(Σ.C)` alone, not conditioned on whether `a` appears in any `ran(M(d))`, such content is never reclaimed. Nelson requires this for history — he calls such content "deleted bytes — not currently addressable, awaiting historical backtrack functions, may remain included in other versions," and version reconstruction depends on the availability of Istream fragments from prior arrangements.

*Formal Contract (S3):*
- *Axiom (well-formedness invariant):* In every state `Σ`, `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — equivalently, `ran(Σ.M(d)) ⊆ dom(Σ.C)`.
- *Preservation across transitions:* For an operation that adds a V-mapping `M(d)(v) = a`, the post-state must satisfy `a ∈ dom(Σ'.C)` — the I-address must exist in the post-state.
- *Frame:* S3 asserts `ran(M(d)) ⊆ dom(C)` only; the converse `dom(C) ⊆ ⋃_d ran(M(d))` is not asserted.
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

GlobalUniqueness (ASN-0034) establishes the following invariant: for every pair of addresses `a, b` produced by distinct allocation events in any reachable system state, `a ≠ b`. The invariant's precondition requires only that `a₁` and `a₂` arise from distinct allocation events under T10a — it places no condition on the values `Σ.C(a₁)` and `Σ.C(a₂)`. Since `a₁` and `a₂` are produced by distinct allocation events by hypothesis, GlobalUniqueness yields `a₁ ≠ a₂` directly. ∎

*Formal Contract:*
- *Preconditions:* `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to T10a (allocator discipline, ASN-0034).
- *Postconditions:* `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.
- *Frame:* The content store `C` and value domain `Val` play no role in the proof — distinctness is a property of the addressing scheme alone.


## Sharing

The arrangement function `M(d)` need not be injective. This is not a deficiency but a design requirement — it is what makes transclusion work.

**S5 (Unrestricted sharing).** The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

In any particular state, the sharing multiplicity of each address is a definite finite number — possibly zero for orphaned content — but no invariant imposes a uniform bound that holds across all states.

Nelson: "The virtual byte stream of a document may include bytes from any other document." And: "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely." Transclusion is recursive and unlimited.

Gregory confirms the unbounded nature at the implementation level. The global index that records which documents reference which I-addresses accumulates entries without cap — "no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism anywhere in the code path." Each referential inclusion adds one entry. The only constraints are physical resources (memory and disk), not architectural limits.

S4 and S5 together make quotation a first-class structural relationship: any number of documents can quote the same passage, and the system knows they are all quoting — not independently writing — because they share I-addresses.

*Proof.* We wish to show that for every `N ∈ ℕ`, there exists a genuine strand state `Σ` in which some I-address has sharing multiplicity exceeding `N`. We give two constructions — one for cross-document sharing, one for within-document sharing — each succeeding for arbitrary `N`. S0 and S1 are transition invariants (`Σ → Σ'`): they constrain transitions only and impose no condition on an isolated state. The remaining requirements are state-level: the genuine state predicates S2 and S3, plus the always-on well-formedness invariants the model imposes on every state — S7b (`zeros(a) = 3` for every `a ∈ dom(Σ.C)`), the domain-restriction axiom on `Σ.M(d)` (`zeros(v) = 0 ∧ #v ≥ 2`, equivalently S8a), and S8-fin (finite arrangements). Each construction verifies all of these together with the multiplicity count, so the witnessing states are genuine strand states, not bare models of S0–S3.

**Cross-document construction.** Fix `N ∈ ℕ`. Define state `Σ_N = (C_N, M_N)` by:

- `C_N = {a ↦ w}` for the explicit element-level I-address `a = [1, 0, 1, 0, 1, 0, 1, 1]` and arbitrary value `w ∈ Val`.
- `N + 1` documents `d₁, …, d_{N+1}` with explicit witnesses `dᵢ = [1, 0, 1, 0, i]` for `i = 1, …, N + 1`. The `dᵢ` are pairwise distinct by T3 (CanonicalRepresentation, ASN-0034) since they have distinct last components — all S5 requires of them, since the state predicates treat `d` only as an index into `M`. Fix a single V-position `v = [1, 1]` shared across all `N + 1` documents, and define each arrangement as `M_N(dᵢ) = {v ↦ a}`. The pairs `(dᵢ, v)` are distinct since the `dᵢ` are distinct.

We verify each invariant. S2 (arrangement functionality): each `M_N(dᵢ)` contains a single entry `{v ↦ a}` — the domain has one element, so uniqueness of the image is immediate; `M_N(dᵢ)` is a function. S3 (referential integrity): the sole I-address referenced by any arrangement is `a`, and `a ∈ dom(C_N)` by construction. S7b (element-level I-addresses): `a = [1, 0, 1, 0, 1, 0, 1, 1]` has exactly three zero components (positions 2, 4, 6), so `zeros(a) = 3`, and `dom(C_N) = {a}` contains only this address. Domain-restriction axiom on `M_N(dᵢ)`: the sole active V-position `v = [1, 1]` satisfies `zeros(v) = 0` and `#v = 2 ≥ 2`; equivalently (S8a) both components are positive and `#v ≥ 2`. S8-fin: each `dom(M_N(dᵢ))` is the singleton `{v}` and `dom(C_N)` is the singleton `{a}`, all finite. Thus `Σ_N` is a genuine strand state.

The sharing multiplicity of `a` in `Σ_N` is `|{(d, v) : v ∈ dom(M_N(d)) ∧ M_N(d)(v) = a}| = N + 1`, since each of the `N + 1` documents contributes exactly one pair `(dᵢ, v)` (with the same fixed `v = [1, 1]` across all `i`). Thus the multiplicity exceeds `N`.

**Within-document construction.** Fix `N ∈ ℕ`. Define state `Σ'_N = (C'_N, M'_N)` by:

- `C'_N = {a ↦ w}` for the explicit element-level I-address `a = [1, 0, 1, 0, 1, 0, 1, 1]` and arbitrary value `w ∈ Val`.
- One document `d = [1, 0, 1, 0, 1]` with `M'_N(d) = {v₁ ↦ a, v₂ ↦ a, …, v_{N+1} ↦ a}` where `vₖ = [1, k]` for `k = 1, …, N + 1` — pairwise distinct V-positions (distinctness follows from distinct last components by T3, ASN-0034).

We verify each invariant. S2 (arrangement functionality): the `vᵢ` are pairwise distinct by construction (distinct last components, T3 — CanonicalRepresentation, ASN-0034), so each V-position maps to exactly one I-address (namely `a`); `M'_N(d)` is a well-defined function. S3 (referential integrity): the sole referenced I-address `a` satisfies `a ∈ dom(C'_N)` by construction. S7b: `a = [1, 0, 1, 0, 1, 0, 1, 1]` has `zeros(a) = 3` and `dom(C'_N) = {a}`. Domain-restriction axiom on `M'_N(d)`: every `vₖ = [1, k]` with `k ≥ 1` has `zeros(vₖ) = 0` and `#vₖ = 2 ≥ 2` (equivalently S8a: both components positive, depth ≥ 2). S8-fin: `dom(M'_N(d)) = {v₁, …, v_{N+1}}` and `dom(C'_N) = {a}` are both finite. Thus `Σ'_N` is a genuine strand state.

The within-document sharing multiplicity is `|{v : v ∈ dom(M'_N(d)) ∧ M'_N(d)(v) = a}| = N + 1 > N`.

**Conclusion.** Since both constructions yield genuine strand states for arbitrary `N ∈ ℕ`, sharing multiplicity exceeding any given finite bound is consistent with the full state model — S0–S3 together with the always-on well-formedness invariants (S7b, the domain-restriction axiom, S8-fin). No finite cap on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|` is entailed by these invariants — neither across documents nor within a single document. ∎

*Formal Contract:*
- *Preconditions:* `N ∈ ℕ` arbitrary.
- *Postconditions:* There exists a genuine strand state `Σ` — satisfying S0 (content immutability), S1 (store monotonicity), S2 (arrangement functionality), S3 (referential integrity), S7b (element-level I-addresses), the domain-restriction axiom on `Σ.M(d)`, and S8-fin (finite arrangements) — such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).
- *Depends:* S0, S1, S2, S3, S7b, S8-fin, the domain-restriction axiom, S8a, T0 (ASN-0034), T3 (ASN-0034), T4 (ASN-0034).


## Structural attribution

Every V-position can be traced to the document that originally created its content.

The projection `D(a)` is well-defined only when `zeros(a) ≥ 2` (per T4's field correspondence: `zeros = 0` is node-only, `zeros = 1` is node+user, `zeros ≥ 2` has a document field). Since Istream addresses designate content elements within documents, we require:

**S7b (Element-level I-addresses).** We require that every address in `dom(Σ.C)` is an element-level tumbler: `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.

This is a design requirement: content resides at the element level — the finest level of the four-level tumbler hierarchy. Node, user, and document-level tumblers identify containers, not content. By T4's field correspondence, `zeros(a) = 3` means all four identifying fields — node, user, document, element — are present, and the element field contains the content-level address.

*Formal Contract (S7b):*
- *Axiom (design requirement):* `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`.
- *Postconditions:* By T4's field correspondence, all four identifying fields — node, user, document, element — are present and the element field exists. The projections `N(a)`, `U(a)`, `D(a)`, `E(a)` supplied by T4b are all well-defined.
- *Depends:* T4 (HierarchicalParsing, ASN-0034) — field correspondence; T4b (UniqueParse, ASN-0034) — projection definitions; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4-validity (no adjacent zeros, `a₁ ≠ 0 ∧ a_{#a} ≠ 0`) and the bound `zeros(a) ≤ 3`.

**S7a (Document-scoped allocation).** Every Istream address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` — the tumbler `N(a).0.U(a).0.D(a)` obtained by truncating the element field, where `N(a)`, `U(a)`, `D(a)` are the partial projections supplied by T4b (UniqueParse, ASN-0034) — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`.

Nelson's baptism principle establishes it: "The owner of a given item controls the allocation of the numbers under it." A document owner baptises element addresses under that document's prefix — there is no mechanism for allocating I-addresses outside the creating document's subtree. "You always know where you are, and can at once ascertain the home document of any specific word or character." Nelson says the home document can be ascertained directly from the address — not from a separate lookup table. The native/non-native distinction ("Native bytes of a document are those actually stored under its control") is computable only because I-addresses are scoped under their originating documents. Gregory's implementation corroborates this: the I-address prefix itself encodes the originating document, used during allocation to scope the search range.

*Formal Contract (S7a):*
- *Axiom (design requirement):* `(A a : a ∈ dom(Σ.C) :: the document-level prefix N(a).0.U(a).0.D(a) is the tumbler of the document whose owner performed the allocation that placed a into dom(C))`. By S7b (stated above), every `a ∈ dom(Σ.C)` satisfies `zeros(a) = 3`, so T4b's projections `N(a)`, `U(a)`, `D(a)` are everywhere defined on the domain over which the axiom quantifies.
- *Depends:* T4 (HierarchicalParsing, ASN-0034) — defines the prefix structure; T4b (UniqueParse, ASN-0034) — defines projections `N`, `U`, `D`; S7b (Element-level I-addresses) — supplies `zeros(a) = 3` for every `a ∈ dom(Σ.C)`; T10a (AllocatorDiscipline, ASN-0034) — establishes the baptism principle; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation.

**S7d (Document allocation discipline).** Every document is addressed by a document-level tumbler (`zeros = 2`) arising from an allocation event under T10a's allocator discipline (ASN-0034). Distinct documents arise from distinct allocation events.

*Formal Contract (S7d):*
- *Axiom (design requirement):* Every document tumbler `d` satisfies `zeros(d) = 2` and is the result of an allocation event under T10a; distinct documents arise from distinct allocation events.
- *Postconditions:* By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers.
- *Depends:* T10a (AllocatorDiscipline, ASN-0034) — allocation events; T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation, here at `zeros = 2`; T4 (HierarchicalParsing, ASN-0034) — field correspondence at `zeros = 2`; GlobalUniqueness (ASN-0034) — uniqueness across allocation events.

**S7 (Structural attribution).** For every `a ∈ dom(Σ.C)`, define the *origin* as the document-level prefix obtained by truncating the element field:

`origin(a) = N(a).0.U(a).0.D(a)`

This is the full document tumbler `N.0.U.0.D` — uniquely identifying the allocating document across the system.

Since I-addresses are permanent (S0) and unique (S4), this attribution is permanent and unseverable.

We note a subtlety. S7 identifies the document that ALLOCATED the I-address — the document where the content was first created. This is distinct from the document where the content currently appears. When content is transcluded from document B into document A, the reader viewing A sees the content, but S7 traces it to B. The distinction between "where I am reading" (Vstream context, document A) and "where this came from" (Istream structure, document B) is precisely the two-stream separation made visible.

*Proof.* We wish to show that for every `a ∈ dom(Σ.C)`, the function `origin(a) = N(a).0.U(a).0.D(a)` is well-defined, uniquely identifies the document that allocated `a`, and that this identification is permanent and unseverable.

**Well-definedness.** By S7b (element-level I-addresses), `zeros(a) = 3`, and by T10a.4 (T4PreservationUnderDiscipline, ASN-0034), `a` is T4-valid; hence T4's field-decomposition machinery applies to `a`. By T4 (HierarchicalParsing, ASN-0034), `zeros(a) = 3` means `a` contains exactly three zero-valued field separators, and the partial projections supplied by T4b (UniqueParse, ASN-0034) — `N(a)`, `U(a)`, `D(a)`, `E(a)` — extract the node, user, document, and element fields respectively, each as a finite sequence of strictly positive natural numbers. T4's positive-component constraint guarantees every non-separator component is strictly positive, and T4's non-empty field constraint guarantees each present field has at least one component. The projections `N(a)`, `U(a)`, and `D(a)` are therefore all well-defined with at least one strictly positive component each. The truncation `origin(a)` — formed by concatenating the node field, a zero separator, the user field, a zero separator, and the document field — is a well-defined tumbler satisfying `zeros(origin(a)) = 2`, placing it at the document level in T4's hierarchy.

**Identification.** By S7a (document-scoped allocation), every I-address is allocated under the tumbler prefix of the document that created it. The document-level prefix of `a` — precisely `origin(a)`, the tumbler `N.0.U.0.D` obtained by truncating the element field — identifies the document whose owner performed the allocation that placed `a` into `dom(C)`. This is not a lookup or annotation: the address structurally encodes its provenance. S7a ensures that `origin(a)` IS the allocating document's tumbler.

**Uniqueness across documents.** By S7d's postcondition, distinct documents have distinct document-level tumblers. By T3 (CanonicalRepresentation, ASN-0034), this distinctness is decidable by component-wise comparison. Therefore, for any `a₁, a₂ ∈ dom(Σ.C)` allocated under distinct documents: `origin(a₁) ≠ origin(a₂)`. The origin function discriminates allocating documents without ambiguity.

**Permanence.** By S0 (content immutability), once `a ∈ dom(Σ.C)`, then `a ∈ dom(Σ'.C)` for all successor states `Σ'` — the address persists. Since `a` is a tumbler — a fixed sequence of components, not a mutable reference — and `origin(a)` is computed from the components of `a` alone via T4's deterministic field decomposition, `origin(a)` yields the same result in every state in which `a` exists. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S7a (document-scoped allocation), S7b (element-level I-addresses), S7d (document allocation discipline), T4 (HierarchicalParsing, ASN-0034), T4b (UniqueParse, ASN-0034) — supplies the projections `N(a)`, `U(a)`, `D(a)`, `E(a)` from which `origin(a)` is computed, T10a (allocator discipline, ASN-0034), and T10a.4 (T4PreservationUnderDiscipline, ASN-0034) — T4 preservation. The strict equality `zeros(a) = 3` itself comes from S7b axiomatically.
- *Postconditions:* (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.


## Singleton span partition

The arrangement `M(d)` maps individual V-positions to I-addresses. Because `dom(M(d))` is finite (S8-fin), the mapping always admits a *finite* partition into singleton intervals, one per V-position — this is the existence claim we establish here.

**S8-fin (Finite arrangement).** For each document `d`, `dom(Σ.M(d))` is finite. This is a design requirement on every reachable state: no document arrangement is permitted to hold infinitely many V-positions.

*Formal Contract:*
- *Axiom (design requirement):* For every state `Σ` and document `d`, `dom(Σ.M(d))` is a finite set.
- *Postconditions:* `|dom(Σ.M(d))| < ∞` — the arrangement has finite cardinality. Consequently `ran(Σ.M(d))` is finite (image of a finite set under a function).
- *Frame:* No constraint on the unbounded growth of `dom(C)`; only individual arrangements are required to be finite at any given state.

**S8a (V-position componentwise positivity and depth).** This is the per-component form of the domain-restriction axiom. Over ℕ (T0), `zeros(v)` (T4) counts the components equal to `0`, so `zeros(v) = 0` iff every component is positive; combined with the axiom's depth floor `#v ≥ 2`, this gives:

`(A v ∈ dom(Σ.M(d)) :: #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`

*Formal Contract:*
- *Preconditions:* The domain-restriction axiom on `Σ.M(d)` — every `v ∈ dom(Σ.M(d))` satisfies `zeros(v) = 0 ∧ #v ≥ 2`; T0 — components are natural numbers.
- *Postconditions:* `(A v ∈ dom(Σ.M(d)) :: #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))`.
- *Depends:* `Σ.M(d)` domain-restriction axiom — supplies `zeros(v) = 0` and `#v ≥ 2` for every active V-position; T0 (ASN-0034) — supplies the ℕ-valued component carrier.

**subspace (V-position subspace identifier).** For any tumbler `v` of depth `#v ≥ 1`, define:

`subspace(v) = v₁`

extracting the subspace identifier as the first component of a V-position.

*Formal Contract:*
- *Signature:* `subspace : T → ℕ` — projects the first component of a tumbler.
- *Preconditions:* `v ∈ T`, `#v ≥ 1` (so that `v₁` is well-defined as the first component of a non-empty tumbler).
- *Definition:* `subspace(v) = v₁`.

**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)`

Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. Any correct implementation must satisfy this constraint.

*Formal Contract:*
- *Axiom (design requirement):* `(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)`.
- *Postconditions:* Within a subspace `s` of document `d`, there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`. Distinct subspaces may have distinct depths.
- *Depends:* S8a — for the lower bound `m_s ≥ 2`.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: a position `v` is followed by `shift(v, 1)` (equivalently `v ⊕ δ(1, #v)` per OrdinalShift, ASN-0034), the next ordinal at the same depth.

For each V-position `v`, its *singleton interval* is the half-open tumbler interval `[v, shift(v, 1))`, where `shift(v, 1) = v ⊕ δ(1, #v)` per OrdinalShift (ASN-0034) is the next ordinal at the same depth. By OrdinalShift's postconditions, for `m = #v ≥ 2`, `shift(v, 1)` agrees with `v` on positions `1 ≤ i < m` and sets `shift(v, 1)_m = v_m + 1`, so it preserves the subspace identifier `v₁` while incrementing only the ordinal component.

**S8 (Singleton span partition).** For each document `d`, the singleton intervals `{[vⱼ, shift(vⱼ, 1)) : vⱼ ∈ dom(Σ.M(d))}` — one per V-position — partition the V-positions of `dom(Σ.M(d))`, and each interval carries a well-defined label `aⱼ ∈ dom(Σ.C)` (the *labeled partition*):

(a) Every V-position falls in exactly one singleton interval — `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, 1)))`

(b) The labeling `vⱼ ↦ aⱼ` is well-defined: the label `aⱼ = Σ.M(d)(vⱼ)` exists and is unique because `Σ.M(d)` is a function (S2), and `aⱼ ∈ dom(Σ.C)` by referential integrity (S3).

*Proof.* We construct a finite decomposition satisfying both conjuncts and prove it partitions `dom(M(d))`.

**Existence.** By S8-fin, `dom(M(d))` is finite. When `dom(M(d)) = ∅`, the singleton collection is empty — the empty partition — and conjuncts (a), (b) hold vacuously. Otherwise, by S2 (ArrangementFunctionality), `M(d)` is a function, so each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)`; by S3 (referential integrity), `a ∈ dom(Σ.C)`. For each such `v`, form the singleton interval `[v, shift(v, 1))` with label `a` — this is the labeled partition of conjunct (b), well-defined precisely because S2 makes the label unique and S3 places it in `dom(Σ.C)`. Since `dom(M(d))` is finite, the collection of singletons is finite. The singleton decomposition witnesses existence.

**Coverage.** Each `v ∈ dom(M(d))` lies in its own singleton's interval: `v ≤ v < shift(v, 1)`, where the right inequality holds because `shift(v, 1) > v` by TS4 (ShiftStrictIncrease, ASN-0034). So every V-position falls in at least one singleton interval.

**Uniqueness within a subspace.** Let `v, w ∈ dom(M(d))` be distinct V-positions with `v₁ = w₁ = S`. By S8-depth, `#v = #w = m` for some common depth `m`. We show `w ∉ [v, shift(v, 1))` via the following lemma.

**Within-subspace incompatibility lemma.** Let `v` be as above (a V-position with `v₁ = S`, `#v = m ≥ 2`, satisfying S8a). For any tumbler `t` with `t₁ = S`, `#t = m`, and `t ≠ v`: `t ∉ [v, shift(v, 1))`.

*Proof of lemma.* Suppose for contradiction that `t ∈ [v, shift(v, 1))`, i.e. `v ≤ t < shift(v, 1)`. Since `#t = #v = m`, the sequences diverge at some first position `j ≤ m`. The shared first component `t₁ = v₁ = S` forces `j ≥ 2`. At `m = 2` this further forces `j = m = 2`, leaving only Case j = m below; for `m ≥ 3`, both branches `2 ≤ j < m` and `j = m` are possible. Both branches yield contradictions.

*Case j < m.* Then `tᵢ = vᵢ` for `i < j`. The lemma's hypothesis `t ≠ v` combined with `v ≤ t` (from `t ∈ [v, shift(v, 1))`) strengthens to `v < t` — the non-strict relation `v ≤ t` resolves to strict `<` once equality is ruled out. T1(i) applied to `v < t` with first divergence at component `j` (valid since `j ≤ m = min(m, m)`) then yields `tⱼ > vⱼ`. Since `shift(v, 1)ⱼ = vⱼ` (as `j < m`), and `tᵢ = vᵢ = shift(v, 1)ᵢ` for `i < j`, the first divergence between `t` and `shift(v, 1)` is at position `j` with `tⱼ > shift(v, 1)ⱼ`, giving `t > shift(v, 1)` by T1(i) — contradicting `t < shift(v, 1)`.

*Case j = m.* Then `tᵢ = vᵢ` for `i < m`. By OrdinalShift (ASN-0034), `shift(v, 1)ᵢ = vᵢ` for `i < m`, so `tᵢ = shift(v, 1)ᵢ` for `i < m` and the first divergence between `t` and `shift(v, 1)` is at position `m`. Since `tᵢ = vᵢ` for `i < m` and `t ≠ v` (with `#t = #v = m`), the divergence at `j = m` between `t` and `v` is also real: `t_m ≠ v_m`. Combined with `v ≤ t`, this gives `v < t`, and T1(i) applied to `v < t` with first divergence at `m` yields strict `t_m > v_m`; NAT-discrete (ASN-0034) at `(m, n) := (v_m, t_m)` promotes the strict inequality `v_m < t_m` to `v_m + 1 ≤ t_m`, i.e., `t_m ≥ v_m + 1`. From `t < shift(v, 1)` with first divergence at `m`: T1(i) gives `t_m < shift(v, 1)_m`, and the identity `shift(v, 1)_m = v_m + 1` (OrdinalShift, ASN-0034; `v_m + 1 ∈ ℕ` by NAT-closure, ASN-0034) rewrites this to `t_m < v_m + 1`. But `t_m ≥ v_m + 1` and `t_m < v_m + 1` are incompatible by NAT-order's exactly-one trichotomy (ASN-0034), instantiated at `(t_m, v_m + 1)` — the clause `¬(a < b ∧ b ≤ a)` excludes the conjunction of the two inequalities. Contradiction. ∎ *(lemma)*

*Application to w.* The hypotheses `w₁ = v₁ = S`, `#w = m` (S8-depth), and `w ≠ v` are exactly the lemma's antecedents, so `w ∉ [v, shift(v, 1))`. Since all V-positions in subspace `S` share depth `m` (S8-depth) and the lemma applies to every such position distinct from `v`, no distinct V-position in the same subspace falls in `v`'s singleton interval.
**Uniqueness across subspaces.** Let `v ∈ dom(M(d))` with `v₁ = S₁` and `w ∈ dom(M(d))` with `w₁ = S₂`, where `S₁ ≠ S₂`. By S8a, `v` and `w` extend the single-component prefixes `[S₁]` and `[S₂]` respectively, and both have depth `≥ 2`. These prefixes are non-nesting: `[S₁] ≼ [S₂]` would require `S₁ = S₂` (both length-1 tumblers, so equality requires componentwise agreement by T3), contradicting `S₁ ≠ S₂`; symmetrically `[S₂] ⋠ [S₁]`.

For `m ≥ 2` (the only case under S8a), the successor `shift(v, 1)` also extends `[S₁]`: by OrdinalShift (ASN-0034), `shift(v, 1)` agrees with `v` on positions `i < m`, and since `m ≥ 2` this includes position 1, giving `shift(v, 1)₁ = v₁ = S₁`.

Since `[S₁] ≼ v` and `[S₁] ≼ shift(v, 1)` and `v ≤ shift(v, 1)` by TS4 (ShiftStrictIncrease, ASN-0034), T5 (ContiguousSubtrees, ASN-0034) gives: for any `t` with `v ≤ t ≤ shift(v, 1)`, `[S₁] ≼ t`. Every element of `[v, shift(v, 1))` therefore extends `[S₁]`. By T10 (ASN-0034), since `[S₁]` and `[S₂]` are non-nesting prefixes, any tumbler extending `[S₁]` is distinct from any tumbler extending `[S₂]`. In particular, `w` (which extends `[S₂]`) cannot belong to `[v, shift(v, 1))`.

**Conclusion.** The singleton intervals cover every V-position in `dom(M(d))` (coverage) and no V-position falls in two distinct singleton intervals (uniqueness within and across subspaces). The singletons therefore partition the V-positions of `dom(M(d))`. Since `dom(M(d))` is finite (S8-fin), the decomposition is finite, establishing both conjuncts (a) and (b). ∎

*Formal Contract:*
- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); referential integrity (S3); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` (S8a); within each subspace, all V-positions share a common depth (S8-depth).
- *Postconditions:* The finite set of singleton intervals `{[vⱼ, shift(vⱼ, 1)) : vⱼ ∈ dom(M(d))}` partitions the V-positions of `dom(M(d))`: (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, 1)))`. (b) The labeling `vⱼ ↦ aⱼ = M(d)(vⱼ)` is well-defined (established in the proof), yielding the labeled partition.
- *Depends:* (*Local properties*) S2 (ArrangementFunctionality) — each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)`; S3 (referential integrity) — `M(d)(v) ∈ dom(Σ.C)`; S8a — `zeros(v) = 0`, `#v ≥ 2`, and componentwise positivity of V-positions; S8-depth — a common depth `m` for every V-position in a fixed subspace; S8-fin — finite `dom(M(d))`. (*Foundation claims, ASN-0034*) T1 (TumblerOrdering) case (i) — first-divergence comparison; T3 (CanonicalRepresentation) — equates tumblers with their canonical component sequences; T5 (ContiguousSubtrees) — a prefix's extensions form a contiguous interval under T1; T10 — non-nesting prefixes generate disjoint tumbler subtrees; TS4 (ShiftStrictIncrease) — `v < shift(v, 1)`; TumblerAdd, OrdinalShift, OrdinalDisplacement — the action-point semantics of `δ(k, m)`, the three-region component formula, and the action-point identity `shift(v, 1)_m = v_m + 1`. NAT-discrete (NatDiscreteness) — the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n`. NAT-closure (NatArithmeticClosureAndIdentity) — closure of ℕ under addition places `v_m + 1` in ℕ. NAT-order (NatStrictTotalOrder) — the exactly-one trichotomy clause `¬(a < b ∧ b ≤ a)`.

## Arrangement contiguity

Nelson states that the Vstream is always a "dense, contiguous sequence" — after removal, "the v-stream addresses of any following characters in the document are [decreased] by the length of the [deleted] text" [LM 4/66]. The Vstream has no concept of empty positions: "if you have 100 bytes, you have addresses 1 through 100." Nelson's "addresses 1 through 100" describes character positions, so the contiguity properties below are stated for the text subspace (S = 1).

Abbreviate `S = subspace(v) = v₁` (per S8a), and write `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` for the set of V-positions in subspace S of document d. The specialization to the text subspace is `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}`. All V-positions in a given subspace share the same tumbler depth (S8-depth).

**D-CTG (VContiguity).** For each document d, V_1(d) (the text subspace) is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`

The guard `zeros(v) = 0` restricts the consequent to S8a-conforming tumblers, so the contiguity demand ranges only over intermediates that could be V-positions.

In words: within the text subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

*Formal Contract:*
- *Axiom (design requirement):* `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`.
- *Preconditions:* `subspace(v) = 1`; V-positions share a common depth (S8-depth).
- *Postconditions:* V_1(d) is either empty or occupies every position strictly between its extremes (at the fixed depth).
- *Frame:* D-CTG is a constraint on well-formed text-subspace arrangements.
- *Depends:* S8a (V-position well-formedness); S8-depth (common depth within subspace); T1 (TumblerOrdering, ASN-0034) — defines the order.

For the text subspace at depth m = 2, this is a finite condition: the intermediates between [1, a] and [1, b] are the finitely many [1, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_1(d) occupies a single unbroken block of ordinals.

**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_1(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_1(d) be non-empty with common depth `m` (S8-depth) and `m ≥ 3` (non-triviality bound, per the Preconditions). Suppose for contradiction that V_1(d) contains two positions u and x with u < x (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, uᵢ = xᵢ for all i < j, and uⱼ < xⱼ (the inequality follows from u < x by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

We construct infinitely many intermediates. For any natural number n > uⱼ₊₁, define w of length m by:

- wᵢ = uᵢ for 1 ≤ i ≤ j (agreeing with u on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (an empty range when j = m − 1, in which case wⱼ₊₁ = w_m is already the last component; otherwise this clause fills components j + 2 through m).

Then w has depth m (it has m components by construction), and subspace(w) = w₁ = u₁ = 1 (since j ≥ 2, the first component is copied from u). We verify u < w < x:

- **w > u**: w agrees with u on components 1 through j. At component j + 1, wⱼ₊₁ = n > uⱼ₊₁. Since j + 1 ≤ m = min(m, m), by T1(i), w > u.
- **w < x**: w agrees with x on components 1 through j − 1 (since u and x agree on these components by the definition of j). At component j, wⱼ = uⱼ < xⱼ. Since j ≤ m − 1 ≤ min(m, m), by T1(i), w < x.

We also verify that w satisfies S8a — necessary because D-CTG ranges over V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a. By construction, every component of w is at least 1: wᵢ = uᵢ ≥ 1 for i ≤ j by S8a applied to u; wⱼ₊₁ = n > uⱼ₊₁ ≥ 1 (again by S8a on u); and wᵢ = 1 for j + 2 ≤ i ≤ m. Hence zeros(w) = 0 and `(A i : 1 ≤ i ≤ #w : wᵢ > 0)`. Combined with #w = m ≥ 3 ≥ 2, w satisfies S8a — so the candidate w qualifies for D-CTG's consequent.

Since u < w < x, subspace(w) = 1, #w = m = #u, and w satisfies S8a, D-CTG requires w ∈ V_1(d). We now exhibit infinitely many admissible values of n. T0(a) (UnboundedComponentValues, ASN-0034) supplies, for any natural-number bound M, one witness n ∈ ℕ with n > M. Iterating: starting from M₀ = uⱼ₊₁, T0(a) supplies n₁ > M₀; setting M₁ = n₁, T0(a) supplies n₂ > M₁ ≥ n₁; continuing, we obtain a strictly increasing sequence n₁ < n₂ < n₃ < … of natural numbers, all exceeding uⱼ₊₁. The sequence is infinite and pairwise distinct. Distinct values of n yield distinct tumblers w (they differ at component j + 1, so by T3, CanonicalRepresentation, ASN-0034, they are unequal). This produces infinitely many distinct positions in V_1(d), contradicting S8-fin (dom(M(d)) is finite).

Therefore no two positions in V_1(d) can disagree at any component j with 2 ≤ j ≤ m − 1. All positions share components 2 through m − 1, and contiguity reduces to contiguity of the last component (component m) alone. ∎

*Formal Contract:*
- *Preconditions:* V_1(d) non-empty; common depth `m` (S8-depth); `m ≥ 3` (the lemma's non-triviality bound, additional to S8-depth — at `m = 2` the conclusion holds vacuously since the range of shared components 2 through `m − 1` is empty).
- *Postconditions:* `(A u, x ∈ V_1(d), j : 2 ≤ j ≤ m − 1 : uⱼ = xⱼ)`. Contiguity of V_1(d) reduces to contiguity of the m-th (last) component.
- *Depends:* (*Local properties*) D-CTG (VContiguity) — any tumbler strictly between two positions in subspace 1 at depth `m` lies in `V_1(d)`; S8a — `m ≥ 2` and componentwise positivity of V-positions; S8-depth — common depth `#w = m`; S8-fin — finiteness of `V_1(d)`. (*Foundation claims, ASN-0034*) T0(a) (UnboundedComponentValues) — for any bound `M`, a natural-number witness `n > M`; T1 case (i) (TumblerOrdering) — first-divergence comparison; T3 (CanonicalRepresentation) — distinct component sequences yield distinct tumblers.

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

**D-MIN (VMinimumPosition).** For each document d with V_1(d) non-empty:

`min(V_1(d)) = [1, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in the text subspace per S8-depth), and every component is 1.

At depth 2 this gives min(V_1(d)) = [1, 1].

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

D-CTG is a design constraint on well-formed document states. We verify the base case: before any operations, dom(M(d)) = ∅ for all d (the arrangement is a partial function; no content has been allocated, so no V-mapping exists), so V_1(d) = ∅. D-CTG holds vacuously (no u, q exist to trigger its antecedent), and D-MIN holds vacuously (its antecedent requires V_1(d) non-empty).

## Valid insertion position

We work with the arrangement M(d) and the contiguity constraint D-CTG from above, restricted to the text subspace `S = 1`, using `V_1(d)` as fixed at the abbreviation paragraph above.

When V_1(d) is contiguous with |V_1(d)| = N positions, we write its elements as v₀, v₁, ..., v_{N−1} where v₀ is the minimum (D-MIN) and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ).

**Definition (ValidInsertionPosition, non-empty case).** For a document `d` with `V_1(d) ≠ ∅`, the *binary* predicate `ValidInsertionPosition(d, v)` is satisfied when:

- The common V-position depth `m` of V_1(d) is fixed by S8-depth. By S8a, `m ≥ 2`.
- Setting `N = |V_1(d)|`, the predicate holds iff `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`.

**Definition (ValidFirstInsertionPosition, empty case).** For a document `d` with `V_1(d) = ∅`, the *ternary* predicate `ValidFirstInsertionPosition(d, v, m)` is satisfied when `m ∈ ℕ` with `m ≥ 2` and `v = [1, 1, ..., 1]` of depth `m`.

*Formal Contract (ValidInsertionPosition, non-empty case).*
- *Signature:* `ValidInsertionPosition(d, v)` — a *binary* predicate on document `d` and V-position `v`. The common V-position depth `m` is determined by `d` via S8-depth and read from state.
- *Preconditions:* Document `d` with `V_1(d) ⊆ dom(M(d))` non-empty; D-CTG holds on V_1(d); D-MIN gives `min(V_1(d)) = [1, ..., 1]` and D-SEQ gives `V_1(d) = {[1, ..., 1, k] : 1 ≤ k ≤ N}` (both needed to discharge the explicit form (d)); `m ≥ 2` is the common depth of V_1(d) by S8-depth and S8a.
- *Definition:* `ValidInsertionPosition(d, v)` holds iff, writing `N = |V_1(d)|`, `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m` (the state-fixed common depth). (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d`, exactly `N + 1` values of `v` satisfy the predicate. (d) The explicit form is `v = [1, 1, ..., 1 + j]` with last component `1 + j` and all preceding components equal to 1.
- *Derivation:* By D-MIN, `min(V_1(d)) = [1, 1, ..., 1]` of depth `m`. By OrdinalShift (ASN-0034), for `m ≥ 2` shift preserves components `1 ≤ i < m` and increments position `m`, so `shift([1, ..., 1], j) = [1, ..., 1, 1 + j]` for `j ≥ 1`; at `j = 0` the position is `min(V_1(d)) = [1, ..., 1]` directly by D-MIN — the same form with last component `1` — so no extension of OrdinalShift (which requires `n ≥ 1`) to `n = 0` is invoked. This is (d). Every component is then `≥ 1` — the leading `m − 1` equal 1, the last `1 + j ≥ 1` — so `zeros(v) = 0` with componentwise positivity (b), and the preserved leading component fixes `v₁ = 1` as the text subspace identifier. For `j ≠ j'` in `{0, ..., N}` the last components `1 + j ≠ 1 + j'` (NAT-order, ASN-0034), so the length-`m` tumblers diverge at position `m` and are distinct by T3 (ASN-0034), giving exactly `N + 1` positions (c).
- *Depends:* D-MIN, D-CTG, D-CTG-depth, D-SEQ; S8a, S8-fin, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

*Formal Contract (ValidFirstInsertionPosition, empty case).*
- *Signature:* `ValidFirstInsertionPosition(d, v, m)` — a *ternary* predicate on document `d`, V-position `v`, and depth `m`.
- *Preconditions:* Document `d` with `V_1(d) = ∅`; `m ∈ ℕ` with `m ≥ 2`.
- *Definition:* `ValidFirstInsertionPosition(d, v, m)` holds iff `v = [1, 1, ..., 1]` of depth `m`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m`. (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d` and `m`, exactly one value of `v` satisfies the predicate.
- *Depends:* D-MIN; S8a, S8-depth; OrdinalShift, TumblerAdd, T3 (ASN-0034).

### Valid insertion position examples

**Non-empty case (binary predicate).** Let subspace S = 1 and suppose V₁(d) = {[1, 1], [1, 2], [1, 3]}, so N = 3 and min(V₁(d)) = [1, 1]. The depth `m = 2` is read from state via S8-depth. The values of `v` satisfying `ValidInsertionPosition(d, v)` are:

- j = 0: v = min(V₁(d)) = [1, 1]
- j = 1: v = shift([1, 1], 1) = [1, 2]
- j = 2: v = shift([1, 1], 2) = [1, 3]
- j = 3: v = shift([1, 1], 3) = [1, 4]

That gives N + 1 = 4 positions. Any successor state whose `V₁(d)` gains a position at, say, [1, 2] must still satisfy D-CTG and D-MIN.

**Empty case (ternary predicate).** V₁(d) = ∅. Choosing depth m = 2, the unique `v` satisfying `ValidFirstInsertionPosition(d, v, 2)` is `[1, 1]`. D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands. Choosing m = 3 instead, `ValidFirstInsertionPosition(d, v, 3)` is satisfied uniquely by `v = [1, 1, 1]`; by T3, this is a different tumbler.


## Worked example

We instantiate the state model with specific tumblers to ground the abstractions. Consider two documents: document `d₁` at tumbler `1.0.1.0.1` and document `d₂` at tumbler `1.0.1.0.2`. The user creates `d₁` with the text "hello" (five characters), then creates `d₂` which transcludes three characters ("llo") from `d₁` and appends two new characters ("ws"). At each state we exhibit the singleton partition S8 proves and check the design constraints (S0, S3, S7, D-SEQ).

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

*Check S0*: no prior content existed, so the implication holds vacuously. *Check S3*: every V-reference resolves — `ran(M(d₁)) ⊆ dom(C)`. *Check S7*: for `a = 1.0.1.0.1.0.1.3`, `origin(a) = 1.0.1.0.1 = d₁` — the document-level prefix directly identifies the allocating document. *Verify S8 (singleton partition)*: each of the five V-positions is its own singleton. For `v = 1.1 = [1, 1]` (depth `m = 2`), the interval is `[1.1, shift(1.1, 1)) = [[1, 1], [1, 2])`, where `shift([1, 1], 1) = [1, 2]` by OrdinalShift (ASN-0034) with `n = 1` (component 1 preserved, last component `1 + 1 = 2`). This interval contains exactly the V-position `1.1` — the next V-position `1.2 = [1, 2]` is excluded by the half-open upper bound. The five singletons `{[1.k, 1.(k+1)) : 1 ≤ k ≤ 5}` partition `V₁(d₁) = {1.1, …, 1.5}`, and conjunct (b) holds at each: `M(d₁)(1.k) = 1.0.1.0.1.0.1.k`.

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

*Check S0*: all 5 prior entries in `dom(C)` remain with unchanged values. The transition added 2 new entries. *Check S3*: every V-reference in `M(d₂)` resolves — positions `1.1`–`1.3` reference I-addresses from `d₁` (which exist by S1), positions `1.4`–`1.5` reference the newly allocated addresses. *Check S7*: for `a = 1.0.1.0.1.0.1.4` (the second 'l' in `d₂`), `origin(a) = 1.0.1.0.1 = d₁` — attribution traces to the originating document, not to `d₂` where the content currently appears. *Check S5*: the I-address `1.0.1.0.1.0.1.3` now appears in both `ran(M(d₁))` and `ran(M(d₂))` — sharing multiplicity is 2. *Verify S8 (singleton partition)*: the five V-positions `1.1`–`1.5` each form a singleton interval `[1.k, 1.(k+1))`, together partitioning `dom(M(d₂))`; conjunct (b) gives `M(d₂)(1.k)` equal to the tabulated I-address (note that contiguous V-positions need not map to contiguous I-addresses — `1.3` maps to `…1.5` while `1.4` maps to `…2.1`). *Check D-SEQ*: V₁(d₁) is unchanged — {[1, k] : 1 ≤ k ≤ 5}, D-SEQ with n = 5. V₁(d₂) = {[1, k] : 1 ≤ k ≤ 5}, D-SEQ with n = 5. Both satisfy D-CTG and D-MIN.

**After deleting "llo" from d₁** — state Σ₃. DELETE removes V-positions `1.3`–`1.5` from `M(d₁)`:

| V-position `v` | `M(d₁)(v)` |
|---|---|
| `1.1` | `1.0.1.0.1.0.1.1` |
| `1.2` | `1.0.1.0.1.0.1.2` |

*Check S0*: all 7 entries in `dom(C)` remain. The I-addresses `1.0.1.0.1.0.1.3`–`.5` are no longer in `ran(M(d₁))` but persist in `dom(C)`; these three addresses are now "orphaned" from `d₁`'s perspective, but still referenced by `M(d₂)` — persistence is unconditional (S0). *Check two-stream separation (S0 frame)*: the deletion modified `M(d₁)` but `C` is unchanged — separation holds. *Verify S8 (singleton partition)*: the now-two V-positions `1.1` and `1.2` each form a singleton interval, partitioning the two-element `dom(M(d₁))`; `M(d₂)` is unchanged. *Check D-SEQ*: V₁(d₁) = {[1, k] : 1 ≤ k ≤ 2}, D-SEQ with n = 2. D-CTG holds (no gaps in 1..2) and D-MIN holds (min = [1, 1]). V₁(d₂) is unchanged — D-SEQ with n = 5.

The lifecycle above exercises the contiguity constraints at depth 2 on every well-formed state (Σ₁–Σ₃: D-CTG, D-MIN, D-SEQ all hold).

**Contiguity violation (depth 2).** Consider the candidate `V₁(d) = {[1,1], [1,3]}`. Now `[1,2]` is an intermediate between `[1,1]` and `[1,3]` that is absent — D-CTG is violated. A state with a gap in the ordinal range between occupied extremes is not a well-formed document arrangement.

**Higher depth (depth 3).** Let document `d'` have `M(d') = {[1,1,1] ↦ a₁, [1,1,2] ↦ a₂, [1,1,3] ↦ a₃}`, so `V₁(d') = {[1,1,1], [1,1,2], [1,1,3]}`. *D-CTG check*: the only intermediate at subspace 1 and depth 3 between the extremes `[1,1,1]` and `[1,1,3]` is `[1,1,2]`, which is present. ✓ *D-MIN check*: `min(V₁(d')) = [1,1,1] = [S, 1, 1]`, all post-subspace components equal to 1. ✓

**Contiguity violation (depth ≥ 3).** Suppose instead `V₁(d') = {[1,1,1], [1,2,1]}`. D-CTG requires every intermediate with subspace 1 and depth 3 between `[1,1,1]` and `[1,2,1]` to be present. But `[1,1,2], [1,1,3], [1,1,4], …` are all intermediates — infinitely many, contradicting S8-fin. This is D-CTG-depth in action: positions differing before the last component cannot coexist in a finite arrangement.

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
| S7b | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | design; uses T4, T4b, T10a.4 (ASN-0034) |
| S7d | Document allocation discipline: every document is addressed by a document-level tumbler (`zeros = 2`) arising from an allocation event under T10a; distinct documents arise from distinct allocation events | design; uses T10a, T10a.4, T4 (ASN-0034) |
| S7 | Structural attribution: `origin(a) = N(a).0.U(a).0.D(a)` — full document prefix | from S7a, S7b, S7d, S0, S4, T4, T4b, T3, T10a.4, GlobalUniqueness (ASN-0034) |
| S8-fin | Finite arrangement: `dom(M(d))` is finite for every document `d` | design requirement |
| Σ.M(d) domain restriction | `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` — arrangements map only V-positions | axiom (definitional) |
| S8a | V-position componentwise positivity and depth: `(A v ∈ dom(M(d)) :: #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0))` — per-component form of the domain-restriction axiom, equivalent by T0 | from the domain-restriction axiom, T0 (ASN-0034) |
| subspace(v) | V-position subspace identifier: `subspace(v) = v₁`; well-defined when `#v ≥ 1` | introduced; uses T0 (ASN-0034) |
| S8-depth | Fixed-depth V-positions: `(A d, u, w : u ∈ dom(M(d)) ∧ w ∈ dom(M(d)) ∧ subspace(u) = subspace(w) : #u = #w)` | design; uses S8a |
| S8 | Singleton span partition: the singleton intervals `[vⱼ, shift(vⱼ, 1))` partition the V-positions of `dom(M(d))` (a); labeling `vⱼ ↦ aⱼ = M(d)(vⱼ)` well-defined by S2, S3 (b), defining the labeled partition | theorem (a) from S2, S3, S8-fin, S8a, S8-depth, T1, T3, T5, T10, TumblerAdd, OrdinalShift, OrdinalDisplacement, TS4, NAT-discrete, NAT-closure, NAT-order (ASN-0034); (b) labeling by S2, S3 |
| D-CTG | V-position contiguity: V_1(d) forms a contiguous ordinal range with no gaps — design constraint on well-formed document states | design; uses S8a, S8-depth, T1 (ASN-0034) |
| D-MIN | V-position minimum: non-empty V_1(d) has minimum [1, 1, ..., 1] with every component equal to 1 — design constraint | design requirement |
| D-CTG-depth | Shared prefix reduction (applies wherever D-CTG holds): at depth m ≥ 3, all positions in V_1(d) share components 2 through m − 1, so contiguity reduces to the last component | corollary of D-CTG, S8a, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034) |
| D-SEQ | Sequential positions: non-empty V_1(d) = {[1, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 | from D-CTG, D-CTG-depth, D-MIN, S8a, S8-fin, S8-depth, T1 (ASN-0034) |
| ValidInsertionPosition | Binary predicate `ValidInsertionPosition(d, v)` (non-empty case): when V_1(d) ≠ ∅, m is the common depth of V_1(d) (state-determined via S8-depth), and v = min(V_1(d)) or v = shift(min(V_1(d)), j) for j ∈ {1, ..., N} where N = |V_1(d)| | introduced |
| ValidFirstInsertionPosition | Ternary predicate `ValidFirstInsertionPosition(d, v, m)` (empty case): when V_1(d) = ∅, m ≥ 2, and v = [1, 1, ..., 1] of depth m | introduced |


## Open Questions

What constraints must the content store's value domain `Val` satisfy — must all entries be uniform in type, or must `Val` support heterogeneous content (text, links, media) as first-class distinctions?

Must every arrangement admit a unique *maximal* correspondence-run decomposition — a minimal set of runs `(vⱼ, aⱼ, nⱼ)`, each preserving ordinal displacement `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for `0 ≤ k < nⱼ` — or can decompositions of different cardinality coexist for the same arrangement?

What must the system guarantee about the computability of the sharing inverse — given an I-address, what is the cost bound for determining which documents currently reference it?

Under what conditions, if any, may the referential integrity invariant S3 be temporarily violated — must it hold at every observable state, or only at quiescent states between operations?

What abstract property distinguishes content that exists but is unreachable from all current arrangements from content that exists and is reachable — and must the system maintain this distinction as queryable state?

What must each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) — and the displacement mechanism underlying insertion at a ValidInsertionPosition — guarantee in order to preserve the contiguity invariants D-CTG, D-MIN, and S2, including the case where insertion coincides with an occupied V-position?

The strand model fixes only the lower bound m ≥ 2 for V-position depth in an empty subspace; the specific value is a one-time allocation convention chosen by the first-placing operation, not a strand-level commitment. What operation-layer constraints determine the canonical choice of m (e.g., m = 2 for basic INSERT/DELETE versus deeper subdivisions Nelson contemplated)? What downstream capabilities — nested hierarchies, link subdivision, future extensibility — does each depth choice unlock or foreclose?

The strand model treats subspace alignment — a V-position's subspace identifier `subspace(v) = v₁` matching the first element-field component of the I-address `M(d)(v)` it maps to — as an operations-layer preservation obligation rather than a state-level invariant on arrangements. Which editing operations must establish this alignment for the V-positions they produce, and under what allocation conventions is preservation automatic versus requiring explicit operation-level enforcement?
