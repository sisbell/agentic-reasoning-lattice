# ASN-0036 Formal Statements

*Source: ASN-0036-streams.md (revised 2026-03-28) — Extracted: 2026-03-28*

## Σ.C — ContentStore

`Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values. `T` is the set of tumblers (ASN-0034); `Val` is an unspecified set of content values. The domain `dom(Σ.C)` is the set of I-addresses at which content has been stored.

In words: the content store maps permanent Istream addresses to stored content. It is partial because not every tumbler carries content — only addresses at which content has actually been stored belong to the domain. The content type is opaque at this level; the store is indifferent to whether it holds text, links, or media.

*Formal Contract:*
- *Axiom:* `Σ.C : T ⇀ Val` — the content store is a partial function from tumblers to content values.
- *Definition:* `dom(Σ.C) = {a ∈ T : Σ.C(a) is defined}` — the set of I-addresses at which content has been stored.


## Σ.M(d) — ArrangementForDocument

`Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers. The domain `dom(Σ.M(d))` is the set of V-positions currently active in `d`; the range `ran(Σ.M(d))` is the set of I-addresses that `d` currently references.

In words: an arrangement specifies which content appears in a document and in what order, by mapping virtual document positions to permanent content-store addresses. It is partial because only active positions belong to the domain. Editing a document changes the arrangement without touching the content store.

*Formal Contract:*
- *Axiom:* `Σ.M(d) : T ⇀ T` — the arrangement of document `d` is a partial function from V-position tumblers to I-address tumblers.
- *Definition:* `dom(Σ.M(d)) = {v ∈ T : Σ.M(d)(v) is defined}` — the set of V-positions currently active in `d`.
- *Definition:* `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}` — the set of I-addresses that `d` currently references.


## S0 — ContentImmutability

For every state transition `Σ → Σ'`:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

In words: once content is stored at an address, that address and its value are fixed for all future states. No operation may overwrite or remove existing content — operations may only add new content at fresh addresses.

*Formal Contract:*
- *Invariant:* `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)` for every transition `Σ → Σ'`
- *Axiom:* imposed as a design constraint on all content-store operations


## S1 — StoreMonotonicity

`[dom(Σ.C) ⊆ dom(Σ'.C)]`

In words: the content store grows monotonically — addresses are never removed. S1 is a corollary of S0 (content immutability) and a specialisation of T8 (allocation permanence, ASN-0034) from the abstract address space to the content store specifically. Together with S0, it establishes the content store as an append-only log.

*Formal Contract:*
- *Preconditions:* S0 (content immutability).
- *Invariant:* `dom(Σ.C) ⊆ dom(Σ'.C)` for every transition `Σ → Σ'`.

## S2 — Arrangement functionality

For each document `d`, `Σ.M(d)` is a function — each V-position maps to exactly one I-address:

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) is uniquely determined)`

In words: a document's virtual byte stream is unambiguous at every position — no V-position can simultaneously display two different pieces of content, even when the underlying I-addresses are drawn from multiple Istreams.

*Formal Contract:*
- *Axiom:* For each document `d`, `Σ.M(d)` is a function — every `v ∈ dom(Σ.M(d))` maps to exactly one I-address.


## S3 — Referential integrity

`(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`

In words: every V-position in every document's arrangement maps to an I-address that actually exists in the content store — arrangements contain no dangling references. Content must exist before or simultaneously with the mapping that references it; S1 guarantees that once present, content cannot be removed, so a valid reference can never become dangling after the fact.

*Formal Contract:*
- *Preconditions:* State transitions satisfy S1 (store monotonicity).
- *Axiom:* Every arrangement-modifying operation introducing a mapping `M(d)(v) = a` ensures `a ∈ dom(Σ'.C)` in the post-state.
- *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`


## S4 — Origin-based identity

For I-addresses `a₁`, `a₂` produced by distinct allocation events:

`a₁ ≠ a₂`

regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.

In words: two independent writings of the same content produce distinct I-addresses; only transclusion — reuse of an existing I-address — indicates shared origin. Identity is structural and address-based, not value-based: `a₁ = a₂` is the decidable structural test for shared content, requiring no value comparison.

*Formal Contract:*
- *Preconditions:* `a₁, a₂ ∈ dom(Σ.C)` produced by distinct allocation events within a system conforming to the tumbler axioms of ASN-0034 (T9, T10, T10a, TA5).
- *Postconditions:* `a₁ ≠ a₂`, regardless of whether `Σ.C(a₁) = Σ.C(a₂)`.
- *Frame:* The content store `C` and value domain `Val` play no role in the proof — distinctness is a property of the addressing scheme alone.


## S5 — Unrestricted sharing

The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

In words: the invariants S0–S3 impose no finite cap on how many times a single I-address may be referenced — the same content can appear at arbitrarily many V-positions across any number of documents, and also at arbitrarily many positions within a single document. This is the architectural anti-constraint that makes unrestricted transclusion possible.

*Formal Contract:*
- *Preconditions:* `N ∈ ℕ` arbitrary.
- *Postconditions:* There exists a state `Σ` satisfying S0 (content immutability), S1 (store monotonicity), S2 (arrangement functionality), and S3 (referential integrity) such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).
- *Frame:* S0–S3 are the only invariants checked. The constructions are minimal — single I-address, trivial arrangements — to isolate the consistency claim from other architectural properties.


## S6 — Persistence independence

The membership of `a` in `dom(Σ.C)` is independent of all arrangements:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)]`

regardless of any changes to any `Σ.M(d)`.

In words: content in the store persists permanently regardless of whether any arrangement currently references it. Unreferenced ("orphaned") content is never reclaimed — the system makes no provision for garbage collection — because historical version reconstruction depends on the availability of Istream fragments from prior arrangements.

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` and state transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Postconditions:* `a ∈ dom(Σ'.C)`, with no condition on the arrangement functions `Σ.M(d)` or `Σ'.M(d)` for any document `d`.
- *Frame:* The arrangement functions `M(d)` are unconstrained — S6 holds for all possible values of `Σ'.M(d)`, including `Σ'.M(d) = ∅`.

## S7a — Document-scoped allocation

For every `a ∈ dom(Σ.C)`, the document-level prefix `(fields(a).node).0.(fields(a).user).0.(fields(a).document)` identifies the document whose owner allocated `a`.

In words: every Istream content address structurally encodes the document that created it. The document-level prefix — formed by truncating the element field — identifies the allocating document directly, without a separate lookup table.

*Formal Contract:*
- *Preconditions:* S7b (element-level I-addresses) ensures `zeros(a) = 3` for all `a ∈ dom(Σ.C)`, so that T4's `fields(a)` yields node, user, document, and element fields.
- *Axiom:* For every `a ∈ dom(Σ.C)`, the document-level prefix `(fields(a).node).0.(fields(a).user).0.(fields(a).document)` identifies the document whose owner allocated `a`.

---

## S7b — Element-level I-addresses

`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

In words: every content address in the arrangement is an element-level tumbler — the finest granularity in the four-level hierarchy. This ensures each address encodes all four identifying fields: node, user, document, and element.

*Formal Contract:*
- *Axiom:* `(A a ∈ dom(Σ.C) :: zeros(a) = 3)`

---

## S7 — Structural attribution

For every `a ∈ dom(Σ.C)`, define:

`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)`

This is the document-level tumbler `N.0.U.0.D` obtained by truncating the element field of `a`.

In words: every content address permanently and uniquely identifies its allocating document via `origin`. Attribution is structural — it is computed from the address itself, not from attached metadata — so it cannot be stripped, forged, or severed. The distinction between where content currently appears (Vstream context) and where it was created (Istream structure) is made visible by this function.

*Formal Contract:*
- *Preconditions:* `a ∈ dom(Σ.C)` in a system conforming to S0 (content immutability), S4 (origin-based identity), S7a (document-scoped allocation), S7b (element-level I-addresses), T4 (FieldSeparatorConstraint, ASN-0034), GlobalUniqueness (ASN-0034), and T10a (allocator discipline, ASN-0034).
- *Definition:* `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — the document-level prefix of `a`, obtained by truncating the element field.
- *Postconditions:* (a) `origin(a)` is well-defined and is a document-level tumbler with `zeros(origin(a)) = 2`. (b) `origin(a)` is the tumbler of the document that allocated `a`. (c) For `a₁, a₂` allocated under distinct documents, `origin(a₁) ≠ origin(a₂)`. (d) `origin(a)` is invariant across all states in which `a ∈ dom(Σ.C)`.
- *Frame:* The content values `Σ.C(a)` and arrangement functions `Σ.M(d)` play no role — attribution is a property of the addressing scheme alone.

---

## S8-fin — Finite arrangement

For each document `d`, `dom(Σ.M(d))` is finite for every reachable state Σ.

In words: a document contains only finitely many V-positions at any point in time. This is enforced as a design invariant: every arrangement-modifying operation may only add or remove finitely many positions.

*Formal Contract:*
- *Invariant:* `dom(Σ.M(d))` is finite for every document `d` and every reachable state Σ.
- *Axiom:* Every arrangement-modifying operation adds or removes only finitely many V-positions — finiteness of each operation's effect is a design constraint enforced by construction.

---

## S8a — V-position well-formedness

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`

In words: every V-position is an element-field tumbler containing no field separators and with all components strictly positive. The first component `v₁` is the subspace identifier (e.g., 1 for text, 2 for links); the constraint `v₁ ≥ 1` is universally true — not a guard — and is load-bearing for cross-subspace partition proofs that invoke T5 and T10.

*Formal Contract:*
- *Axiom:* V-positions are element-field tumblers — the fourth field in T4's decomposition of element-level addresses.
- *Preconditions:* T4 (FieldSeparatorConstraint, ASN-0034) — every non-separator component is strictly positive, every present field has at least one component.
- *Postconditions:* `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`.

## S8-depth — Fixed-depth V-positions

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

Within a subspace (same first component), all V-positions share the same tumbler depth. This enables depth-matched ordinal displacement: `δ(k, m) = [0, …, 0, k]` of length `m` advances only the last component while preserving depth and all prefix components, underpinning the definition of correspondence runs.

A *correspondence run* is a triple `(v, a, n)` — a V-position, an I-address, and a natural number `n ≥ 1` — such that `Σ.M(d)(v + k) = a + k` for `0 ≤ k < n`, where `v + 0 = v` (convention) and `v + k = v ⊕ δ(k, mᵥ)` for `k ≥ 1`.

*Formal Contract:*
- *Axiom:* `(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`
- *Definition:* `δ(k, m) = [0, …, 0, k]` of length `m`; for `k > 0`, `actionPoint(δ(k, m)) = m`. A *correspondence run* in document `d` is a triple `(v, a, n)` with `n ≥ 1` such that `Σ.M(d)(v) = a` and `(A k : 1 ≤ k < n : Σ.M(d)(v ⊕ δ(k, mᵥ)) = a ⊕ δ(k, mₐ))`, where `mᵥ = #v` and `mₐ = #a`. Shorthand: `v + 0 = v` (convention); `v + k = v ⊕ δ(k, mᵥ)` for `k ≥ 1`.


## S8 — Span decomposition

For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the V-positions: `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run: `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

Every finite document arrangement decomposes into a finite set of non-overlapping, exhaustive correspondence runs — contiguous blocks in which V-position ordinals and I-address ordinals advance in lockstep. Each run represents a contiguous block of content that entered the arrangement as a unit.

*Formal Contract:*
- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1)` (S8a); within each subspace, all V-positions share a common depth (S8-depth).
- *Postconditions:* There exists a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` satisfying (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))` and (b) `(A j, k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k)`.


### Arrangement contiguity

Write `S = subspace(v) = v₁` for the subspace identifier (the first component of the element-field V-position), and `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` for the set of V-positions in subspace `S` of document `d`. All V-positions in a given subspace share the same tumbler depth (S8-depth).


## D-CTG — V-position contiguity

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

Within each subspace, V-positions form a contiguous ordinal range with no gaps. If positions `[1, 3]` and `[1, 7]` are occupied, then every position `[1, k]` with `3 < k < 7` must also be occupied. At depth 2, combined with S8-fin, this means `V_S(d)` occupies a single unbroken block of ordinals.

*Formal Contract:*
- *Invariant:* `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`
- *Axiom:* Every arrangement-modifying operation preserves V-contiguity within each subspace — this is a design constraint enforced by construction, parallel to S8-fin.


## D-MIN — V-position minimum

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length `m` (the common depth of V-positions in subspace `S` per S8-depth), and every component after the first is 1.

For each non-empty subspace, the minimum V-position is the subspace identifier followed by all 1s. At depth 2, combined with D-CTG and S8-fin, a subspace with `n` elements occupies exactly `[S, 1]` through `[S, n]` — matching the "addresses 1 through 100" structure.

*Corollary (general form).* From D-MIN, D-CTG-depth, D-CTG, and S8-fin: `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite `n ≥ 1`, where the tuple has length `m` and all components 2 through `m − 1` equal 1.

*Formal Contract:*
- *Axiom:* `min(V_S(d)) = [S, 1, ..., 1]` for every document `d` and subspace `S` with `V_S(d)` non-empty, where the tuple has length `m` (S8-depth) and every post-subspace component is 1.


## D-CTG-depth — Shared prefix reduction

`(A v₁, v₂ ∈ V_S(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`

For depth `m ≥ 3`, all V-positions in a non-empty subspace share components 2 through `m − 1`. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth-2 case.

*Formal Contract:*
- *Preconditions:* `V_S(d)` non-empty; common depth `m ≥ 3` (S8-depth); D-CTG (VContiguity); `dom(M(d))` finite (S8-fin); T0(a) (UnboundedComponentValues, ASN-0034); T1(i) (TumblerOrdering, ASN-0034); T3 (CanonicalRepresentation, ASN-0034).
- *Postconditions:* `(A v₁, v₂ ∈ V_S(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of `V_S(d)` reduces to contiguity of the `m`-th (last) component.

## D-SEQ — Sequential positions (m ≥ 2)

For each document d and subspace S, if V_S(d) is non-empty and the common V-position depth m ≥ 2 (S8-depth), then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m. At depth 2 this gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}, matching Nelson's "addresses 1 through n."

The V-positions in any non-empty subspace form a contiguous sequence of depth-m tumblers with prefix [S, 1, …, 1] and final component ranging from 1 to n. Only the last component varies; all intermediate components are 1 and the first is the subspace identifier S.

*Formal Contract:*
- *Preconditions:* V_S(d) non-empty; common V-position depth m ≥ 2 (S8-depth); D-CTG (VContiguity); D-CTG-depth (SharedPrefixReduction, for m ≥ 3); D-MIN (VMinimumPosition); T1(i) (TumblerOrdering, ASN-0034); dom(M(d)) finite (S8-fin).
- *Postconditions:* `(E n : n ≥ 1 : V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n})` where each tuple has length m.

## ValidInsertionPosition — InsertionPositionDefinition

A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Write m for the common V-position depth in subspace S (S8-depth); m ≥ 2 is required as a precondition. Then either v = min(V_S(d)) (the j = 0 case) or v = shift(min(V_S(d)), j) for some j with 1 ≤ j ≤ N. In both cases, #v = m.

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. This is the canonical minimum position required by D-MIN. The choice of m is a one-time structural commitment: once any position is placed, S8-depth fixes the depth for all subsequent positions in the subspace.

In both cases, S = v₁ is the subspace identifier.

In the non-empty case, there are exactly N + 1 valid insertion positions: the N positions coinciding with existing V-positions v₀ through v_{N−1}, plus the append position shift(min(V_S(d)), N).

A valid insertion position is one of the N existing V-positions or the single append position one past the last, giving N+1 choices total; for an empty subspace, exactly one canonical first position at chosen depth m ≥ 2, which then locks the subspace's depth permanently. This defines the complete set of positions at which an insert operation may place new content while preserving D-CTG and D-MIN.

*Formal Contract:*
- *Preconditions:* d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1 (subspace identifier); if V_S(d) ≠ ∅, common V-position depth m ≥ 2.
- *Definition:* v is a valid insertion position in subspace S of d when: (1) V_S(d) ≠ ∅ with |V_S(d)| = N: v = min(V_S(d)) or v = shift(min(V_S(d)), j) for 1 ≤ j ≤ N; (2) V_S(d) = ∅: v = [S, 1, …, 1] of depth m ≥ 2.
- *Postconditions:* #v = m (depth preservation); v₁ = S (subspace identity); zeros(v) = 0 ∧ v > 0 (S8a consistency); in the non-empty case, exactly N + 1 valid positions, pairwise distinct by T3.

## S9 — Two-stream separation

No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

If any document's arrangement changes in a state transition, every address previously in the content store persists with its value unchanged. Arrangements reference content (via S3) but content is independent of all arrangements — a one-way dependency that makes content immutability sufficient to guarantee arrangement modifications can never corrupt stored data.

*Formal Contract:*
- *Preconditions:* State transition `Σ → Σ'` in a system satisfying S0 (content immutability).
- *Invariant:* `[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`.
- *Frame:* `Σ.C` — the content store is preserved unchanged across all transitions that modify any arrangement `Σ.M(d)`.
