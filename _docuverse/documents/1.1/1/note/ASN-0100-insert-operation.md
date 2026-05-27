# ASN-0100: INSERT Operation

*2026-05-27*

## The Question

When new content is inserted at a position in a document's Vstream, what is the precise post-state? Three sub-questions structure the inquiry:

- *What is allocated* — what new state appears in the content store and in the document's arrangement?
- *What shifts* — which existing V→I mappings change position, and by how much?
- *What invariants must hold after completion* — and atomically, with no observable intermediate state in which some invariant is violated?

The answer must be sharp enough that an implementation can be measured against it, and abstract enough that two implementations meeting the spec are externally indistinguishable.

## Background: The Two-Stream Asymmetry

The foundation distinguishes two address spaces. The content store `C : T ⇀ Val` assigns content values to I-addresses; once `a ∈ dom(C)`, the binding is permanently fixed (S0). The arrangement `M(d) : T ⇀ T` assigns I-addresses to V-positions within document `d`; arrangements are mutable, but only in a controlled way.

INSERT acts on both, but asymmetrically. It *grows* `C` by appending fresh entries; it never alters existing entries, never reassigns I-addresses, never identifies one I-address with another. It *grows and rearranges* `M(d)`; it never alters the underlying I-addresses, only the V-positions at which they are observed.

This asymmetry is the architectural pivot. Existing content keeps its permanent I-address across INSERT. Its V-position within `d` may shift, but the I-address — and the value stored there — is invariant. Since links attach to I-addresses (not V-positions), insertion cannot break them. The I-address is the *identity* of a piece of content; the V-position is the *current location* of that identity within an arrangement.

We shall see that every constraint on INSERT — what may shift, what must be preserved, what counts as atomic — flows from this single asymmetry.

## The Operation's Inputs

INSERT takes three arguments: a target document `d ∈ dom(M)`, a V-position `p` at which the insertion begins, and a sequence of new content values `⟨v₀, v₁, …, v_{n−1}⟩` with `n ≥ 1`.

We restrict attention to the *content subspace* `s_C` of `d` — Nelson's text content. (The link subspace `s_L` is governed by a structurally similar but distinct extension operation; the present analysis does not cover it.)

The position `p` must be a *valid insertion position* in `V_{s_C}(d)`. We unpack this:

  `subspace(p) = s_C ∧ #p = m_C`

where `m_C` is the common depth of `V_{s_C}(d)` (by S8-depth on the text subspace). For non-empty `V_{s_C}(d)` with current cardinality `N = |V_{s_C}(d)|`:

  `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ N}`

This yields `N + 1` admissible positions: `j = 0` inserts before the first character, `j = N` after the last, and `j ∈ {1, …, N−1}` in the interior.

For empty `V_{s_C}(d)`, the caller chooses a depth `m ≥ 2` and the single admissible position is `[s_C, 1, …, 1]` of length `m`. This first insertion fixes `m_C = m` for all subsequent text-subspace operations on `d`.

The condition `n ≥ 1` rules out a degenerate empty-insertion case. The values `v_k` must be elements of the content type `Val`; the abstract specification places no further constraint on their structure.

These preconditions are necessary; we shall verify they are jointly sufficient.

## Discovering the Three Effects

We reason from the intent backward to the formal specification. INSERT splices `n` new content units into `d`'s arrangement at V-position `p`. Three effects must obtain together.

### Effect One: Allocation

The new content units do not exist in `dom(C)` before the operation. Nelson is unambiguous (Q1, Q5, Q8): INSERT creates *new* content with *fresh* I-addresses. The operation does not reuse, alias, or identify with any pre-existing I-address.

The freshness comes from `d`'s content sub-allocator `A_C(d)`, by the substrate's allocation discipline. We require `n` addresses:

  `a_k = A_C(d)`'s `k`-th emission at the operation, for `0 ≤ k < n`

By the substrate's chain discipline (FirstEmissionFreshness; ChainPrefixExtension), each `a_k` satisfies `a_k ∉ dom(C) ∪ dom(L)` at the operation's pre-state; each has `origin(a_k) = d`; each is structurally produced by the sub-allocator's `inc(·, 0)` chain starting from its first emission. The addresses `a_0, a_1, …, a_{n−1}` form a contiguous initial segment extension of the sub-allocator's chain. In particular `a_{k+1} = inc(a_k, 0)` for `k ≥ 0`, and `a_0` is either `[d.0.s_C.1]` (if `d` had no prior content) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(C) : origin(a) = d}`.

The post-state content store:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `C'(a_k) = v_k` for `0 ≤ k < n`
  `C'(a) = C(a)` for `a ∈ dom(C)`

The third clause is the most important. The pre-existing content is *not touched*. Its values are preserved bit-for-bit; its addresses persist in the post-state. This is the foundational permanence guarantee S0.

### Effect Two: Placement

The new I-addresses must appear at V-positions `p, shift(p, 1), …, shift(p, n−1)`. The mapping is exact:

  `(A k : 0 ≤ k < n : M'(d)(shift(p, k)) = a_k)`

By S8a, every shift(p, k) lies in the same subspace as `p` (the b clause of OrdAddHom applied to `w = δ(k, m_C)`), so `subspace(shift(p, k)) = s_C` and `#shift(p, k) = m_C`. The new V-positions are well-formed inhabitants of `V_{s_C}(d')`.

### Effect Three: Shift

Every existing V-position `v ∈ V_{s_C}(d)` with `v ≥ p` must remap. The content there does not change — it keeps its I-address — but its V-position advances by `n`:

  `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

The right region is the source of the shift; the shifted-right region is its image. The two are related by the order-preserving and injective shift map (TS1, TS2 from the foundation). The image of the shift map is exactly `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N}` when we write `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`.

For positions `v ∈ V_{s_C}(d)` with `v < p` (the left region), the arrangement is unchanged.

For positions in subspaces other than `s_C` — including the link subspace — the arrangement is unchanged.

For other documents `d' ≠ d`, the arrangement is unchanged.

These exhaust the cases.

## The Operation: Formal Contract

We now state INSERT as a transition `Σ → Σ'`.

**Operation:** `INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)`

**Preconditions:**
- `d ∈ dom(M)`
- `subspace(p) = s_C`
- `#p = m_C` (the common depth of `V_{s_C}(d)` if non-empty; the caller's chosen depth `m ≥ 2` if empty)
- `p` is a valid insertion position: either `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ |V_{s_C}(d)|}` for non-empty `V_{s_C}(d)`, or `p = [s_C, 1, …, 1]` of depth `m` for empty `V_{s_C}(d)`
- `n ≥ 1`
- `v_k ∈ Val` for each `0 ≤ k < n`

**Effect — Content Store:**
Let `a_0, a_1, …, a_{n−1}` denote `n` successive emissions of `A_C(d)` produced at this transition. Then:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `(A k : 0 ≤ k < n : C'(a_k) = v_k)`
  `(A a : a ∈ dom(C) : C'(a) = C(a))`

**Effect — Arrangement of `d`, text subspace:**
Three disjoint regions:

  *Left* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

  *Insertion* — `(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)`

  *Shifted right* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

The post-state's text-subspace domain is exactly the union: `V_{s_C}(d') = `Left positions ∪ Insertion positions ∪ Shifted-right positions.

**Frame Conditions:**
- `L' = L`. The link store is unchanged: no link is created, modified, or destroyed.
- `dom(M') = dom(M)`. No new document is registered; INSERT does not create documents.
- `(A d' : d' ∈ dom(M) ∧ d' ≠ d : M'(d') = M(d'))`. Other documents' arrangements are unchanged.
- `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`. Other subspaces of `d` — in particular `V_{s_L}(d)` — are unchanged.

## Verifying the Invariants

The post-state Σ' must satisfy every system invariant. We verify the principal ones.

### Permanence of existing content (S0)

The content-store effect's third clause asserts `(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`. This is S0 verbatim. The first clause `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` adds new addresses without removing any; the new addresses are fresh by the sub-allocator's freshness lemma, so no overwrite occurs. Store monotonicity `dom(C) ⊆ dom(C')` follows.

The consequence Nelson emphasises (Q5): a reader holding any pre-state I-address `a ∈ dom(C)` retrieves the same value `C'(a) = C(a)` from the post-state. The reader needs no knowledge of where in any document's Vstream that content now lies.

### Cross-document independence (Q3)

The frame `(A d' : d' ≠ d : M'(d') = M(d'))` directly enforces independence: no document other than `d` has its arrangement altered. Coupled with `L' = L` and content-store preservation, this means that any document `d'` that transcludes content from `d` continues to map the same V-positions to the same I-addresses, and those I-addresses continue to resolve to the same values.

The two documents may share I-addresses through transclusion, but the cross-document frame and content preservation together ensure that the shared I-addresses' values and the *other* document's mappings are unaffected.

### Arrangement functionality (S2)

We verify that `M'(d)` is a function: no V-position has two distinct image I-addresses.

The Left, Insertion, and Shifted-right regions are pairwise disjoint as sets of V-positions. Writing `p = [s_C, 1, …, 1, p_m]`:

- *Left ∩ Insertion = ∅.* Left positions have last component `< p_m`; Insertion positions have last component in `{p_m, p_m + 1, …, p_m + n − 1}`.

- *Insertion ∩ Shifted-right = ∅.* Insertion positions have last component in `{p_m, …, p_m + n − 1}`. Shifted-right positions image `v` with last component `≥ p_m` to a position with last component `≥ p_m + n`. Hence Shifted-right positions have last component `≥ p_m + n`, strictly greater than Insertion positions.

- *Left ∩ Shifted-right = ∅.* Left last components are `< p_m`; Shifted-right last components are `≥ p_m + n ≥ p_m + 1`.

Within each region the mapping is uniquely defined: Left and Shifted-right by `M(d)` applied to a unique source position (the Shifted-right source is recoverable from the image by `shift(·, −n)` — but we need only existence and uniqueness, which is given by TS2's injectivity of shift); Insertion by the sequence `a_0, a_1, …, a_{n−1}` indexed by `k`. So `M'(d)` is a well-defined function.

For other subspaces and other documents, `M'` equals `M`, which is already a function by the pre-state S2.

### Referential integrity (S3)

We verify `(A v ∈ dom(M'(d)) : M'(d)(v) ∈ dom(C'))`.

For Left and Shifted-right positions: the image is `M(d)(v')` for some pre-state position `v' ∈ dom(M(d))`, so by pre-state S3 the image lies in `dom(C)`, and by store monotonicity `dom(C) ⊆ dom(C')`.

For Insertion positions: the image is `a_k ∈ dom(C')` by the content-store effect.

For positions in subspaces other than `s_C` of `d`, and for positions in other documents: unchanged by frame; S3 follows from the pre-state.

### Sequential text-subspace structure (D-CTG, D-MIN, D-SEQ)

Suppose `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` with `N ≥ 1`, and `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`. Then:

- Left positions: `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}` — empty if `p_m = 1`.
- Insertion positions: `{[s_C, 1, …, 1, p_m + j] : 0 ≤ j < n} = {[s_C, 1, …, 1, k] : p_m ≤ k < p_m + n}`.
- Shifted-right positions: `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N} = {[s_C, 1, …, 1, k] : p_m + n ≤ k ≤ N + n}` — empty if `p_m = N + 1`.

Their union is `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, which is exactly the sequential structure required by D-SEQ with new cardinality `N + n`. The minimum `[s_C, 1, …, 1]` is in the union, so D-MIN holds. The integer range `{1, …, N + n}` of last-component values is contiguous, so D-CTG holds.

For the empty pre-state case (`V_{s_C}(d) = ∅`) with `p = [s_C, 1, …, 1]` of depth `m`: post-state `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}`, satisfying all three predicates with `m_C := m`.

### Cross-subspace isolation

The frame `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` directly preserves all subspaces of `d` other than the text subspace. In particular, `V_{s_L}(d') = V_{s_L}(d)`, and link-subspace mappings are unchanged.

The isolation has a structural foundation independent of the explicit frame. The shift operation `shift(v, n) = v ⊕ δ(n, #v)` modifies only the last component of `v` at depth `m_C`. Even if it were applied to a position in `V_{s_L}(d)`, by OrdAddHom (b clause) the subspace identifier — the first component — would be preserved; the position would not migrate to the text subspace. But INSERT never applies shift to non-text positions in the first place. The subspace identifier is part of the V-position's structure, and INSERT's shift is scoped strictly to `s_C`.

Gregory's implementation realises this isolation via a two-blade "knife" whose blades bracket the text subspace; link-subspace crums are classified as outside the shift region and are uniformly left untouched. The structural property is what we verify abstractly; the knife is one (efficient) implementation.

### Link store unchanged (L12, L0, L1, L3)

`L' = L` directly preserves every link's address and value. Every `ℓ ∈ dom(L)` has `L'(ℓ) = L(ℓ)` — endsets are pointwise preserved. The subspace partition L0, the element-level structure L1, and the N-endset structure L3 are all properties of `L` alone and so hold of `L'` trivially.

### Coverage and link discoverability

For every link `ℓ ∈ dom(L)` and every slot `i`, the endset `Σ.L(ℓ).e_i` is a set of spans. Each span `(s, ℓ_w)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ_w}` — a purely combinatorial property of the span representation, consulting no state component. Since `L' = L`, `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` for every link and every slot.

For the projection `project(ℓ, i, d', Σ) = {v ∈ dom(Σ.M(d')) : Σ.M(d')(v) ∈ coverage(Σ.L(ℓ).e_i)}`:

- *For `d' ≠ d`:* `M'(d') = M(d')` by frame, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`.
- *For `d' = d`, link subspace:* link-subspace mappings are unchanged by frame; the link-subspace contribution to projection is unchanged.
- *For `d' = d`, text subspace:* the post-state mappings include the Left identities, the Insertion images (mapping new positions to fresh `a_k`), and the Shifted-right images (mapping `shift(v, n)` to `M(d)(v)`). Every pre-state mapping `v → M(d)(v)` re-appears in the post-state either as `v → M(d)(v)` (Left) or `shift(v, n) → M(d)(v)` (Shifted right). The I-address is preserved across the shift; only the V-position changes.

So every pre-state V-position contributing to the projection contributes a post-state V-position to the same projection (with the same I-address). Pre-state discoverability is preserved:

  `discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ')`

New discoverability is possible only via the Insertion images. A fresh `a_k` lies in `coverage(Σ.L(ℓ).e_i)` only if the endset includes `a_k` in its span coverage. For *tight* endsets — those bounded to address ranges already populated at the time the endset was specified — this cannot happen: the freshness of `a_k` (it was not in `dom(C) ∪ dom(L)` at any earlier state) places it outside the tight coverage. For non-tight endsets, a fresh `a_k` may indeed land in coverage, and this is by intent: non-tight endsets are designed to capture later-allocated content within their declared range.

### Provenance

Each new I-address `a_k` has `origin(a_k) = d`. The mapping `shift(p, k) ↦ a_k` places `a_k` in `ran(M'(d))`. If the system maintains a provenance relation tracking which documents have ever contained which I-addresses, INSERT extends this relation by `{(a_k, d) : 0 ≤ k < n}`. For Shifted-right positions, no new provenance entry is needed: the I-address `M(d)(v)` was already in `ran(M(d))` and the pair `(M(d)(v), d)` was already recorded.

### What is *not* allocated

INSERT does *not* allocate new documents (`dom(M') = dom(M)`), does *not* allocate new links (`L' = L`), and does *not* allocate I-addresses outside `dom(C)`'s content subspace (every `a_k` has `subspace_I(a_k) = s_C`). The allocation footprint is precisely `n` content-subspace I-addresses scoped to `d`.

## Atomicity and Canonical Order

Nelson requires that after INSERT, the system is in "canonical order" — every structural invariant holds simultaneously. Equivalently: no observable intermediate state exists in which any invariant is violated.

The formal specification above states INSERT as a single transition `Σ → Σ'`, not as a sequence of substeps. By the SequentialTransitionAxiom of the substrate, this transition is atomic and uninterruptible: its preconditions are evaluated at `Σ` and its effect committed to `Σ'` in one indivisible step.

The intermediate states that *would* arise from a literal decomposition are not states of the abstract system at all. Consider three candidate decompositions:

- *Allocation alone.* Performing `n` allocations into `dom(C)` produces a state where `a_0, …, a_{n−1}` exist in the content store but are unreferenced by any `M(d)`. This intermediate satisfies S0, S2, S3, but does not constitute an INSERT — it is half the work.

- *Allocation plus placement, no shift.* Adding `M(d)(shift(p, k)) = a_k` to the previous intermediate, without shifting the right region, collides with existing positions whenever `p` is mid-document. If the pre-state has content at positions `p, p+1, …, p+N−1` and we attempt to write `a_0` at position `p` while `M(d)(p)` already binds the original content, S2 fails — two values at one V-position. The intermediate violates functionality.

- *Shift without placement.* Shifting the right region without writing the Insertion images leaves positions `p, shift(p, 1), …, shift(p, n−1)` *empty* in `dom(M(d))`. With the Shifted-right region now occupying positions `p+n` onward, the text-subspace last-component values form `{1, …, p−1} ∪ {p+n, …, p+N+n−1}` — a sequence with a gap of width `n` starting at position `p`. D-CTG fails.

Each decomposition produces an intermediate that violates a key invariant. The only way to maintain canonical order is to perform the complete transition atomically, with all three effects (allocation, placement, shift) becoming visible simultaneously at the post-state.

This is what Nelson calls "all changes, once made, leave the file remaining in canonical order, which was an internal mandate of the system." The abstract specification realises this mandate by declaring INSERT a single transition; implementations realise it via transactional sequencing, locking, copy-on-write, or log-and-commit — but the choice is below the level of abstraction at which INSERT is specified. The system observer sees `Σ` and then `Σ'`, never anything between.

## Position Constraints

We claim INSERT is permitted at any valid insertion position — beginning, middle, end, and on the first insertion into an empty document.

For non-empty `V_{s_C}(d)` with cardinality `N`, the `N + 1` valid positions correspond to:

- `j = 0`: insertion at the very beginning. Left is empty (no `v < p`); the entire pre-state text subspace shifts by `n`.
- `j = N`: insertion at the end. Shifted-right is empty (no `v ≥ p`, since `p = shift(min, N)` and `max(V_{s_C}(d)) = shift(min, N−1) < p`); no shift occurs.
- `j ∈ {1, …, N−1}`: interior insertion. Both Left and Shifted-right are non-empty; both are realised.

For empty `V_{s_C}(d)`, the unique valid position is `[s_C, 1, …, 1]` of the chosen depth `m ≥ 2`.

The edge cases require no special handling in the specification. The universal forms of the three regions handle them uniformly: when one region is empty, its quantifier-bounded clauses are vacuously satisfied; the operation's effect specialises correctly.

The "no positional constraint" intent (Q6) is borne out: the operation is uniformly defined across the position space. The specific *append* operation Nelson lists as a separate convenience (APPEND) is the `j = N` case of INSERT — distinct in name only, since the caller does not need to know `N` if a separate API offers append directly, but identical in semantic effect.

## INSERT vs. COPY: Identity Through Allocation

Nelson (Q8) distinguishes INSERT from COPY — two operations that may produce visually identical Vstream effects but completely different Istream consequences. We address the distinction only to fix the identity character of INSERT; COPY's full operation specification is out of scope for this ASN.

INSERT allocates *fresh* I-addresses for new content. The defining clause of the content-store effect — `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` with each `a_k` fresh — is the structural guarantee that the new content is new. Each `a_k` has `origin(a_k) = d`: attribution accrues to `d`'s owner, royalties (if priced) flow to `d`'s account.

Two independent users who INSERT the word "the" into their respective documents produce two distinct addresses, two distinct origins; neither is a copy or transclusion of the other. The system tracks identity by allocation event, not by value. If their bytes happen to coincide — both authors wrote "the" — the system observes this as two unrelated allocations, not one shared content.

COPY (out of scope here) creates V→I mappings to *existing* I-addresses without allocating new content. The original document remains the home of the bytes; attribution stays with the original author. The Vstream effect can be made indistinguishable from an INSERT — the same V-positions populated with the same visible content — but the underlying Istream identity is fundamentally different.

The identity-by-allocation property of INSERT is foundational. All higher-level properties of the system — traceability of content to its author, royalty accounting, link survivability, version comparison via shared identity — depend on it. An implementation that silently de-duplicated content during INSERT (identifying identical bytes from independent allocations) would violate this property and corrupt every dependent guarantee. The specification therefore forbids it: each `a_k` is a *fresh* address, produced by `A_C(d)`'s allocator chain, with no negotiation of equivalence.

## Bounding the Scope

The specification given here is INSERT for the content subspace. It does not cover:

- Insertion into the link subspace; the foundation's `K.μ⁺_L` is a structurally different operation with its own semantics, and link allocation through `K.λ` differs from content allocation through `K.α` in the requirement of an N-endset value structure.
- COPY, which creates V→I references without content allocation. Out of scope.
- DELETE and REARRANGE; these are governed by other transitions in the substrate's vocabulary.
- Version derivation. INSERT does not create versions; a separate K.δ-style entity-creation operation handles that.
- Inter-server replication. The specification describes INSERT within a single local state; cross-server propagation is the BEBE protocol's concern.

What the specification *does* cover is the precise per-state effect of one INSERT on one document at one position, including every invariant that must continue to hold after the operation.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| INS.def | INSERT(d, p, ⟨v_0, …, v_{n−1}⟩) is an atomic transition Σ → Σ' specified by preconditions, allocation effect, arrangement effect, and frame conditions | introduced |
| INS.pre | INSERT preconditions: d ∈ dom(M); p valid in text subspace of d (per ValidInsertionPosition or ValidFirstInsertionPosition); n ≥ 1; v_k ∈ Val | introduced |
| INS.alloc | INSERT allocates exactly n fresh I-addresses from d's content sub-allocator A_C(d); each a_k satisfies origin(a_k) = d and a_k ∉ dom(C) ∪ dom(L) at the pre-state | introduced |
| INS.C | dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}; C'(a_k) = v_k; ∀a ∈ dom(C): C'(a) = C(a) | introduced |
| INS.M-left | Text-subspace positions v < p in dom(M(d)) appear unchanged in M'(d) | introduced |
| INS.M-insert | M'(d)(shift(p, k)) = a_k for 0 ≤ k < n | introduced |
| INS.M-shift | For v ∈ V_{s_C}(d) with v ≥ p: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v) | introduced |
| INS.frame.subspace | Non-content subspaces of d are unchanged: M'(d) agrees with M(d) on positions with subspace ≠ s_C | introduced |
| INS.frame.doc | Other documents' arrangements are unchanged: ∀d' ≠ d: M'(d') = M(d') | introduced |
| INS.frame.L | L' = L: link store entirely unchanged | introduced |
| INS.frame.dom | dom(M') = dom(M): no new documents registered | introduced |
| INS.inv.immut | Content immutability S0 preserved: dom(C) ⊆ dom(C') and pointwise values preserved | introduced |
| INS.inv.identity | Permanent I-address identity preserved: ∀a ∈ dom(C): a ∈ dom(C'), C'(a) = C(a), origin(a) unchanged | introduced |
| INS.inv.func | M'(d) is a function (S2 preserved); Left, Insertion, Shifted-right regions are pairwise disjoint | introduced |
| INS.inv.refint | Referential integrity S3 preserved: ran(M'(d)) ⊆ dom(C') | introduced |
| INS.inv.seq | D-CTG, D-MIN, D-SEQ preserved in text subspace: V_{s_C}(d') is sequential with cardinality |V_{s_C}(d)| + n | introduced |
| INS.inv.cross-subspace | Cross-subspace isolation: V_{s_L}(d') = V_{s_L}(d) with mappings unchanged | introduced |
| INS.inv.cross-doc | Cross-document isolation: arrangements of all d' ≠ d unchanged | introduced |
| INS.inv.coverage | Endset coverage unchanged for every link: coverage depends only on L, which is preserved | introduced |
| INS.inv.discov | Pre-state discoverability preserved: every link discoverable from any document at Σ remains discoverable at Σ' | introduced |
| INS.atomicity | INSERT is atomic: no observable intermediate state violates any invariant; decompositions into allocation, placement, or shift alone each violate at least one of S2, D-CTG, or S3 | introduced |
| INS.position | INSERT permitted at any valid position: N+1 interior/boundary positions for non-empty V_{s_C}(d), plus first-insertion position for empty case | introduced |
| INS.identity | INSERT creates fresh content identity: each a_k is a new allocation with origin(a_k) = d; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence | introduced |

## Open Questions

- What must INSERT preserve about its post-state's relationship to the pre-state's link projections — must every pre-state projection's image be a contiguous sub-set of the post-state projection's image, or only a subset?
- Under what abstract conditions can an environment satisfy the atomicity guarantee, and what must an implementation provide to recover canonical order after a partial failure?
- What invariants must an analogous insertion operation preserve when the target is the link subspace rather than the text subspace?
- What is the abstract relationship between content allocation and provenance recording — must the provenance pair `(a_k, d)` be added simultaneously with the content allocation, or may it lag behind?
- Is INSERT closed under composition with itself — i.e., if `Σ →INSERT→ Σ_1 →INSERT→ Σ_2`, is there always a single INSERT from `Σ` to `Σ_2`, or do the intermediate effects accumulate in ways that no single INSERT can reproduce?
- What does the abstract specification say about concurrent INSERTs targeting the same V-position from independent agents — must the system serialise them, and if so, on what basis is the order chosen?
- Must INSERT operate on values atomically as a sequence, or may an implementation chunk a long insertion into smaller pieces while preserving observable equivalence at the abstract level?
- What derived properties of a document — current size, last-modified marker, total I-address footprint — does INSERT update, and which of these are part of the abstract state versus derivable from it?
