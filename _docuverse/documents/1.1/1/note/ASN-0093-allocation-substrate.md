# ASN-0093: Allocation Substrate

A Xanadu-style substrate maintains three address-keyed stores: the content store, the link store, and the document-arrangement function. Each store is grown by an allocation primitive that extends the store's domain at a fresh key with structural invariants on the new entry. ASN-0043 introduced the link store and its structural invariants (L0/L1/L1a/L1b/L1c/L3/L12/L14); ASN-0036 introduced the content store and arrangement function. Higher-layer transition models fold both into a larger state model that also tracks entity allocation and arrangement provenance — `Σ = (C, L, E, M, R)` — and supply the operational primitives for the full state.

This note extracts the *allocation-substrate* layer: the three allocation primitives (K.σ, K.α, K.λ) and the structural invariants on `(Σ.C, Σ.L, Σ.M)` they preserve. The substrate requires no commitment to `Σ.E` (the entity set) or `Σ.R` (the provenance relation). Downstream ASNs that reason about address allocation into the three stores without lifting the entity/provenance layer can depend on this note directly, without inheriting the additional state components or their associated invariants. Higher-layer concerns — arrangement mutation, entity stratification, provenance recording — are deferred to higher-layer ASNs that compose this substrate's primitives with additional disciplines.

The factoring is downward from a fuller transition model: every operation and invariant here is identical to its counterpart in the fuller model except for one notational substitution — `E_doc` (the set of entities classified `IsDocument`) is replaced by `dom(M)` (the set of allocated documents in the arrangement function), so the substrate-layer claims can be stated without reference to the entity set.


## Scope

Downstream ASNs that operate on the link store without needing arrangement mutation, entity stratification, or provenance recording can cite this substrate directly. Downstream ASNs that need any of the deferred machinery cite a higher-layer transition model that itself depends on this substrate.

**Provided.** Three primitive operations and the structural invariants on `(C, L, M)` they preserve:

- **Operations:** `K.σ` (document registration), `K.α` (content allocation), `K.λ` (link allocation)
- **Invariants:** M0–M1 (arrangement-function shape), C0–C1c + C2 + C-fin (content store), L0–L14 + L-fin (link store)
- **Lemma:** Cross-document disjointness (T10 + Prefix + M0)
- **Axiom:** SubAllocatorAxiom (four clauses: Exists, Disjoint, FirstEmission, ChainDiscipline)

**Substrate axioms:** SubspaceConventionAxiom pinning `s_C = 1 ∧ s_L = 2`; SequentialTransitionAxiom committing transitions to atomic and sequential.

**Deferred to higher-layer ASNs:**

- **Arrangement mutation.** `K.μ⁺`, `K.μ⁻`, `K.μ~`, `K.μ⁺_L` — operations that modify `M(d)` for an existing `d ∈ dom(M)`. The substrate fixes `M(d)` at `∅` on registration and leaves it unmodified thereafter. Consequently, arrangement-side invariants from ASN-0036 (S2, S3, S8a, S8-depth, S8-fin, D-CTG, D-MIN) hold vacuously here since `M(d) = ∅` for every `d ∈ dom(M)`; arrangement-extension primitives that would make them non-trivial are deferred to a higher-layer ASN.
- **Entity allocation.** The substrate's `K.σ` is the document-registration primitive without the entity-hierarchy machinery. A higher-layer document-introduction primitive rebuilds itself as `K.σ` plus entity-set tracking, lineage discipline, and version-allocator activation.
- **Provenance recording.** A provenance-emission primitive and the provenance relation `R`. The substrate has no `R` component.
- **Coupling constraints.** Higher-layer coupling invariants binding K.α to K.μ⁺ etc. are out of scope; the substrate's `K.α` and `K.λ` stand independently.
- **Link withdrawal.** Nelson's tombstone-style withdrawal (LM 4/9) is not expressible at this layer. Closing the gap is deferred to a higher-layer ASN that may extend the substrate with an explicit retraction mechanism — e.g., a future tombstoning ASN.


## State model

The substrate-level state is

> **Σ = (C, L, M)**

where

- `C : T ⇀ Val` is the content store (per ASN-0036): a partial function from element-level tumblers to content values. `Val` is the content value type defined in ASN-0036.
- `L : T ⇀ Link` is the link store (per ASN-0043): a partial function from element-level tumblers to link values, each a sequence of `N ≥ 3` endsets `(e₁, e₂, …, eₙ) ∈ Endset^N`. `Link` and `Endset` are defined in ASN-0043; the StandardTriple convention (slot 1 = from, slot 2 = to, slot 3 = type, written `(F, G, Θ)` for the arity-3 default) is preserved.
- `M : T ⇀ (T ⇀ T)` is the arrangement function (per ASN-0036): a partial function whose domain `dom(M)` is the set of allocated document addresses, mapping each to its V-position-to-I-address arrangement

`dom(M)` is the set of tumblers committed by `K.σ` events (defined below). A document is *allocated* iff `d ∈ dom(M)`; content addresses with `origin(a) = d` and link addresses with `origin(ℓ) = d` may be emitted only when `d ∈ dom(M)`. The `origin(·)` function is the tumbler-projection defined in ASN-0036 (truncation to the `zeros = 2` prefix); it is a pure structural projection on tumblers and depends on no state component.

**Note on `M`'s shape.** In a higher-layer entity-stratified model, `M` is total with the convention `M(e) = ∅` for `e ∉ E_doc`, and "allocated document" means `e ∈ E_doc`. In this substrate, `M` is partial: `dom(M)` is precisely the set of allocated documents, and the convention "`M(d) = ∅` outside the domain" is replaced by `M(d)` being undefined outside `dom(M)`. This is a semantic shift, not a notational one — the substrate's vocabulary for "document allocated" runs through `dom(M)` rather than through `E_doc`.

**Design rationale for retaining `M`.** The substrate could replace `M` with a set `D ⊆ T` (since `M(d) = ∅` throughout this layer). `M` is retained as a partial function for *downward compatibility*: higher-layer ASNs that compose this substrate with arrangement mutation extend `M(d)` from `∅` rather than re-introducing a new state component. Keeping `M` here makes the lift to a higher-layer transition model trivial: a higher-layer arrangement-extension primitive unfreezes what `K.σ` registers at `M(d) = ∅`.

**Terminology.** "Document" in this substrate means "element of `dom(M)`" — a purely structural notion (a T4-valid tumbler with `zeros = 2` registered into the arrangement function's domain). A higher-layer entity-hierarchy refinement (e.g., `IsDocument(e) ∧ e ∈ E`) is a strict tightening: every document admitted by that refinement is a substrate document, but the substrate admits documents that may not pass the higher-layer entity-hierarchy discipline.

The initial state is `Σ₀ = (∅, ∅, ∅)` — no content, no links, no documents.

**Subspace identifiers.** As in ASN-0043, `s_C` and `s_L` denote the content-subspace and link-subspace first-element-field values. This substrate commits to two axioms governing them:

- **SubspaceConventionAxiom (FixedSubspaceIdentifiers).** `s_C = 1 ∧ s_L = 2`. The distinctness `s_C ≠ s_L` (abbreviated **SC-NEQ**) and the sibling relation `s_L = s_C + 1` are immediate consequences. Pinned by Nelson's design (LM 4/30–4/31) and Gregory's `xanadu.h:144–146` / `granf2.c:162` / `do2.c:94`. SC-NEQ underwrites L14 (StoreDisjointness) and the L0 partition; the sibling relation underwrites the L1c chain exhibition's step `inc(b_C(d), 0) = b_L(d)`.

- **SequentialTransitionAxiom (SequentialAtomicTransitions).** Transitions `Σ → Σ'` are atomic, uninterruptible, and totally ordered: each transition evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step, with no intermediate state in which a transition has begun but not committed.


## Arrangement-function invariants

**M0 (DocumentTumblerWellFormed).**

  `(A d ∈ dom(M) :: ValidAddress(d) ∧ zeros(d) = 2)`

Every allocated document address is a T4-valid tumbler with exactly two zero components (i.e., a document-level address per S7d of ASN-0036). Discharged from `K.σ`'s precondition (below) and inductively across transitions.

**Definitional identification.** Throughout this substrate, `ValidAddress(d) ≡ d satisfies T4 (HierarchicalParsing, ASN-0034)` — the two terms are interchangeable. T4's four conjuncts are: `zeros(d) ≤ 3`, no adjacent zero components, `d[1] ≠ 0`, and `d[#d] ≠ 0`. The substrate uses `ValidAddress(d)` in operation preconditions and invariants for readability; downstream derivations citing T10a, T10a.4, T10a.5, T10a.7, T10a.8, TA5a, TA5-SigValid, T7, or any other foundation claim whose precondition names T4-validity discharge that precondition directly via this identification.

**M1 (ArrangementMonotonicity).**

  `(A Σ → Σ' :: dom(M) ⊆ dom(M'))`

`dom(M)` is non-decreasing across all transitions. The substrate admits no transition that removes a document from `dom(M)`. Discharged from the frame conditions of every transition kind: `K.σ` extends `dom(M)` by one element; `K.α` and `K.λ` hold `M` in frame.

`M1` underwrites every "remains in dom(M)" claim used downstream and is what allows SubAllocatorAxiom.Exists's "remain active at every reachable state in which `d ∈ dom(M)`" to be read as a permanent activation once `d` enters `dom(M)`.


## Content store invariants

**C0 (ContentImmutability).**

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

Append-only with immutable values: `dom(C)` is non-decreasing, and no transition alters the value bound to an existing key. This is ASN-0036's S0/S1 restated for the substrate. Restated here (rather than inherited silently) so the substrate is self-contained — symmetric to L12 on the link side.

**C1 (ContentElementLevel).**

  `(A a ∈ dom(C) :: zeros(a) = 3)`

Every content address is an element-level tumbler. This is ASN-0036's S7b restated for the substrate. Discharged from `K.α`'s precondition.

**C1b (ContentElementFieldDepth).**

  `(A a ∈ dom(C) :: #E(a) ≥ 2)`

Every content address has at least two element-field components — the content-side analog of L1b. This is ASN-0036's S7c restated for the substrate. Discharged from `K.α`'s precondition.

**C1c (ContentAllocatorConformance).** Every content address `a ∈ dom(C)` has a structural inc-chain from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `t₀ = origin(a)` and `tₙ = a`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints. The chain witnesses `a`'s structural producibility from its home document via the content sub-allocator chain. This is the content-side analog of L1c. The bootstrap gap (no T10a-tracked allocator domain for the anchor traversal and first emission) is closed by SubAllocatorAxiom.FirstEmission for the content sub-allocator chain; subsequent emissions inherit T10a.7 (EnumerationInjectivity) via SubAllocatorAxiom.ChainDiscipline.

**C2 (ContentScopedAllocation).**

  `(A a ∈ dom(C) :: origin(a) ∈ dom(M))`

Every content address has its home document allocated — the content-side analog of L1a. Discharged from `K.α`'s precondition and M1.

**C-fin (ContentStoreFiniteness).**

  `|dom(C)| < ∞`

The content store is finite at every reachable state — the content-side analog of L-fin. Discharged inductively from `Σ₀.C = ∅` and `K.α`'s singleton extension. C-fin is what makes the set `{a' ∈ dom(C) : origin(a') = d}` finite at every reachable state, in turn making the `max` invoked in `K.α`'s subsequent-emission precondition well-defined.


## Link store invariants

All invariants below are stated against the reachable-state quantifier — they hold at every `Σ` reachable from `Σ₀` via the transitions defined later in this note.

**L0 (SubspacePartition).**

  `(A a ∈ dom(L) :: E(a)₁ = s_L)`
  `(A a ∈ dom(C) :: E(a)₁ = s_C)`

Every link address has subspace identifier `s_L`; every content address has subspace identifier `s_C`. The L-clause is from ASN-0043; the C-clause is added here as a substrate-level commitment — ASN-0043 carries only the L-clause, and the substrate pins both as joint preconditions of its sub-allocator discipline.

**L1 (LinkElementLevel).**

  `(A a ∈ dom(L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

**L1a (LinkScopedAllocation).**

  `(A a ∈ dom(L) :: origin(a) ∈ dom(M))`

Every link address has its home document allocated. (Replaces the entity-stratified `origin(a) ∈ E_doc` form of higher-layer models — at the substrate layer, the relevant predicate is "the document exists in the arrangement function's domain.")

**L1b (LinkElementFieldDepth).**

  `(A a ∈ dom(L) :: #E(a) ≥ 2)`

Every link address has at least two element-field components.

**L1c (LinkAllocatorConformance).** Every link address `ℓ ∈ dom(L)` has a *structural inc-chain* from its home document to `ℓ`: a finite sequence `(t₀, t₁, …, tₙ)` with `t₀ = origin(ℓ)` and `tₙ = ℓ`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, zero-count side conditions). The chain witnesses `ℓ`'s structural producibility from its home document via the link sub-allocator.

The substrate states L1c in its per-step inc-rule form — not as the stronger "every intermediate `tᵢ` inhabits a T10a-tracked allocator's domain at the state of emission." The strong form fails for the anchor traversal and the first emission, which inhabit no T10a-tracked allocator domain at the moment of allocation; SubAllocatorAxiom.FirstEmission (below) closes the bootstrap gap by licensing the first emission directly, and SubAllocatorAxiom.ChainDiscipline carries subsequent emissions onto the sub-allocator's `inc(·, 0)` chain.

**L3 (NEndsetStructure).**

  `(A a ∈ dom(L) :: |L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |L(a)| : L(a).eᵢ ∈ Endset) ∧ L(a).e₃ ≠ ∅)`

Every link is a sequence of at least three endsets, with the type endset (slot 3) non-empty. This is ASN-0043's L3 restated for the substrate. The three-endset convention (slot 1 = from, slot 2 = to, slot 3 = type, written `(F, G, Θ)`) is preserved as the default form for worked examples and notational convenience but not enforced structurally — the substrate admits arbitrary arity `N ≥ 3`.

**L12 (LinkImmutability).**

  `(A Σ → Σ' : (A a : a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))`

Once allocated, a link's address persists in `dom(L)` and its value is permanently fixed across all transitions.

**L14 (StoreDisjointness).**

  `dom(C) ∩ dom(L) = ∅`

Derived from L0 + SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034): every content address has `E(·)₁ = s_C`, every link address has `E(·)₁ = s_L`, and `s_C ≠ s_L`, so the domains are disjoint.

**L-fin (LinkStoreFiniteness).**

  `|dom(L)| < ∞`

The link store is finite at every reachable state. Discharged inductively from `Σ₀.L = ∅` and `K.λ`'s singleton extension.


## Address sub-allocators under documents

The content and link subspaces are organised as sibling element-field sub-allocators rooted at each document. For each `d ∈ dom(M)`, two element-field anchors sit immediately under `d`:

- `b_C(d) := [d.0.s_C]` — the **content sub-allocator anchor** (one-component element field with `E₁ = s_C`, `zeros = 3`, `#E = 1`)
- `b_L(d) := [d.0.s_L]` — the **link sub-allocator anchor** (one-component element field with `E₁ = s_L`, `zeros = 3`, `#E = 1`)

These anchors are *structurally producible* by T10a `inc` steps from `d`: `b_C(d) = inc(d, 2)` (TA5(d), `k = 2`) and `b_L(d) = inc(b_C(d), 0)` (TA5(c)). The anchors themselves are *not* in `dom(C) ∪ dom(L)` — content and link addresses have `#E ≥ 2` (C1; L1b above), and the anchors have `#E = 1` — so they inhabit the foundation carrier set `T` as structural witnesses without occupying any state component.

**Active sub-allocator chains.** Define: a sub-allocator chain `A_C(d)` (resp. `A_L(d)`) is *active at state* `Σ` iff `d ∈ dom(M)` at `Σ`. Concretely, "active" is the predicate under which K.α (resp. K.λ) admits the chain as the emission source for an address with `origin(·) = d`: the operation's precondition requires `d ∈ dom(M)`, which is exactly the activation condition. By M1 (ArrangementMonotonicity), once `d` enters `dom(M)` via K.σ, it remains so at every successor state, so once a sub-allocator chain is activated it remains active permanently.

**SubAllocatorAxiom (Axiom, ContentLinkSubAllocatorExistence).** For each `d ∈ dom(M)`, two sub-allocator chains are simultaneously activated under `d` at the moment of `d`'s registration into `dom(M)` (by `K.σ`). The substrate treats these chains as *T10a-discipline-satisfying chains* — finite `inc(·, 0)`-extension chains whose elements inherit the per-chain disciplines of T10a (T10a.1, T10a.7, T10a.8) — without claiming that `A_C(d)` and `A_L(d)` are embedded in T10a's global allocator tree as standalone allocators with spawning triples. The substrate makes no commitment about whether an implementation realises `A_C(d)`/`A_L(d)` as standalone T10a allocators or as discipline-conforming chains within a flatter allocator structure; only the per-chain disciplines below are asserted. Four clauses, independently citable as discharge premises:

- *Existence (SubAllocatorAxiom.Exists).* For every `d ∈ dom(M)`, the content sub-allocator chain `A_C(d)` (anchored at `b_C(d)`) and the link sub-allocator chain `A_L(d)` (anchored at `b_L(d)`) are active (per the *Active sub-allocator chains* definition above). By M1 (ArrangementMonotonicity), once `d ∈ dom(M)` it remains so at every successor state, and the sub-allocator chains correspondingly remain active permanently.

- *Disjointness (SubAllocatorAxiom.Disjoint).* Addresses produced by `A_C(d)` satisfy `E(·)₁ = s_C`; addresses produced by `A_L(d)` satisfy `E(·)₁ = s_L`. No address is produced by both sub-allocator chains.

- *First-emission namespace property (SubAllocatorAxiom.FirstEmission).* The first emission of each sub-allocator chain carries a freshness commitment evaluated at the K.α (resp. K.λ) event that commits the address as the chain's first emission (not at the earlier K.σ event that activated the chain; in general the K.σ event and the first-emission K.α/K.λ event are distinct, separated by zero or more intervening transitions):
  - *Content chain first-emit:* the first address `a` produced by `A_C(d)` satisfies `a ∉ dom(C) ∪ dom(L)` at the K.α event that emits `a`, with `E(a)₁ = s_C`, `origin(a) = d`, `#E(a) = 2`. Concretely: `a = [d.0.s_C.1]`.
  - *Link chain first-emit:* the first address `ℓ` produced by `A_L(d)` satisfies `ℓ ∉ dom(L) ∪ dom(C)` at the K.λ event that emits `ℓ`, with `E(ℓ)₁ = s_L`, `origin(ℓ) = d`, `#E(ℓ) = 2`. Concretely: `ℓ = [d.0.s_L.1]`.

- *T10a-discipline-satisfying chains (SubAllocatorAxiom.ChainDiscipline).* From the first emission onward, `A_C(d)` and `A_L(d)` are T10a-discipline-satisfying chains: each is the `inc(·, 0)`-extension chain rooted at its first emission, and the elements of each chain inherit T10a.7 (EnumerationInjectivity — distinct chain indices produce distinct addresses), T10a.1 (UniformSiblingLength — all chain elements share the same length), and T10a.8 (UniformSiblingZeroCount — all chain elements share `zeros = 3` since the first emission has `zeros = 3` per FirstEmission). This clause does *not* claim that `A_C(d)` and `A_L(d)` are embedded in T10a's global allocator tree as standalone allocators with `(parent, spawnPt, spawnParam)` triples; it claims only that each chain's emissions satisfy the per-chain disciplines T10a guarantees for sibling streams. T10a.7 underwrites within-chain freshness for emissions past the first; the Cross-document disjointness lemma (below) underwrites cross-document freshness. Together these supply the substrate's freshness obligations without invoking T10a's global allocator-tree structure. M1's monotonicity carries the "remain active" property forward across all subsequent transitions.

SubAllocatorAxiom.FirstEmission underwrites the bootstrap (where no prior `inc`-history exists in the chain's frontier and T10a.7 is therefore inapplicable to the first emission); SubAllocatorAxiom.ChainDiscipline + T10a.7 underwrites every subsequent emission's within-chain freshness; the Cross-document disjointness lemma underwrites cross-document freshness. Together the four clauses cover the full sub-allocator chain lifecycle from activation through arbitrary emission.

*Remark — T10a chain-lemma applicability to non-tree-embedded chains.* SubAllocatorAxiom.ChainDiscipline asserts that `A_C(d)` and `A_L(d)` inherit T10a.1 (UniformSiblingLength), T10a.7 (EnumerationInjectivity), and T10a.8 (UniformSiblingZeroCount), but explicitly does not embed them in T10a's global allocator tree as standalone allocators. T10a's stated precondition for each of these three lemmas in ASN-0034 names "an allocator A conforming to T10a"; that precondition appears unmet for chains the substrate does not embed in the tree. The substrate cannot therefore invoke T10a.4 (T4PreservationUnderDiscipline) directly — T10a.4's proof inducts on allocator tree depth with a strengthened hypothesis quantifying over `dom(A)`, requiring the chain to be embedded in T10a's allocator tree. Instead, the substrate independently re-establishes T10a.4's *conclusion* (chain-wide T4-validity) for the sub-allocator chains: SubAllocatorAxiom.FirstEmission supplies a T4-valid first emission (concrete structural form `[d.0.s_C.1]` resp. `[d.0.s_L.1]`, T4-valid by inspection given M0's T4-validity of `d`), and TA5a (IncrementPreservesT4) applied per-step from this T4-valid starting point — unconditionally at `k = 0` for every subsequent `inc(·, 0)` step — propagates T4-validity to every chain element without invoking T10a.4 or its tree-embedding hypothesis.

Inspection of the proofs of T10a.1, T10a.7, and T10a.8 in ASN-0034 confirms that the three lemmas decompose into two groups with distinct dependency profiles. *Group 1 (no T4-validity required): T10a.1 and T10a.7.* T10a.1 (UniformSiblingLength) depends only on T10a's per-step `inc(·, 0)` recurrence together with TA5(c) (length preservation); its proof invokes neither T4-validity nor TA5-SigValid. T10a.7 (EnumerationInjectivity) depends only on T10a's per-step recurrence together with TA5(a) (strict monotonicity), T1(a) (irreflexivity of `<`), T1(c) (transitivity of `<`), NAT-order, NAT-sub, NAT-addassoc, and NAT-wellorder; T4-validity and TA5-SigValid play no role. *Group 2 (chain-wide T4-validity required): T10a.8.* T10a.8 (UniformSiblingZeroCount) cites T10a.4 (T4PreservationUnderDiscipline) to obtain T4-validity of every sibling and TA5-SigValid to pin `sig(t_n) = #t_n` at every chain element — the citation that propagates the tree-embedding requirement through T10a.8 transitively even though T10a.8's own proof structure does not invoke `(parent, spawnPt, spawnParam)` or the cross-allocator results. The substrate substitutes the TA5a-based per-step propagation above for that T10a.4 citation, removing the tree-embedding dependency from T10a.8 when applied to sub-allocator chains. None of T10a.1, T10a.7, or T10a.8 (under this substitution) invokes the spawning-triple machinery, the tree-embedding structure itself, or T10a's cross-allocator results (T10a.5/T10a.6). Hence T10a.1 and T10a.7 apply to any sequence `(c₁, c₂, …)` with `c_{n+1} = inc(c_n, 0)`, and T10a.8 additionally requires the first element to be T4-valid — both conditions are met by the chains `A_C(d)` and `A_L(d)` supplied by ChainDiscipline, whose first elements are T4-valid by FirstEmission. This justifies invoking T10a.1, T10a.7, and T10a.8 on the sub-allocator chains throughout this note.

**Lemma (ChainPrefixExtension).** At every reachable state `Σ`, every element of an active sub-allocator chain extends its anchor under the prefix relation:

  `(A d ∈ dom(M), t ∈ A_C(d) :: b_C(d) ≼ t)`
  `(A d ∈ dom(M), t ∈ A_L(d) :: b_L(d) ≼ t)`

*Proof.* Direct induction over each chain's enumeration `(t_1, t_2, t_3, …)` with `t_1` the first emission and `t_{n+1} = inc(t_n, 0)`.

*Base (chain index 1).* By SubAllocatorAxiom.FirstEmission, the content chain's first emission is the concrete form `[d.0.s_C.1]`, which is `b_C(d) = [d.0.s_C]` (length `#d + 2`) extended by the single component `1` at the new last position (length `#d + 3`). Componentwise, `[d.0.s_C.1]` agrees with `b_C(d)` at positions `1..#d + 2`, and the length condition `#b_C(d) = #d + 2 ≤ #d + 3 = #[d.0.s_C.1]` holds. By Prefix (PrefixRelation, ASN-0034), `b_C(d) ≼ [d.0.s_C.1]`. The link case is symmetric: `[d.0.s_L.1]` extends `b_L(d) = [d.0.s_L]` by `1` to length `#d + 3`, so `b_L(d) ≼ [d.0.s_L.1]`.

*Step (chain index `n + 1`).* Assume `b_C(d) ≼ t_n` for `t_n ∈ A_C(d)`. The next element is `t_{n + 1} = inc(t_n, 0)`. By SubAllocatorAxiom.ChainDiscipline, `A_C(d)` inherits T10a.1 (UniformSiblingLength) from FirstEmission, so `#t_n = #d + 3`. By the chain-element T4-validity established in the *T10a chain-lemma applicability* remark above (FirstEmission's T4-valid first emission + TA5a per-step under `k = 0` unconditional preservation), `t_n` is T4-valid; TA5-SigValid (SigOnValidAddresses, ASN-0034) then pins `sig(t_n) = #t_n = #d + 3`. TA5(c) gives `#t_{n + 1} = #t_n` and confines the modification to position `sig(t_n) = #t_n` (TA5(b) and TA5(c)'s single-position-modification clause jointly preserve positions `1..#t_n − 1`). Since `#b_C(d) = #d + 2 = #t_n − 1`, the prefix `b_C(d)` lives entirely within the preserved positional range, so `t_{n + 1}` agrees with `t_n` (and thus with `b_C(d)`) at positions `1..#b_C(d)`. The length condition `#b_C(d) = #d + 2 ≤ #d + 3 = #t_{n + 1}` holds. By Prefix, `b_C(d) ≼ t_{n + 1}`. The link case is symmetric, with `b_L(d)` in place of `b_C(d)` and `A_L(d)` in place of `A_C(d)`. ∎

The corollary is consumed in three places: (i) the *FirstEmission's freshness conclusion* derivation in the *Remark — derivable clauses* below; (ii) the K.α and K.λ subsequent-emit *cross-document freshness* derivations (where freshly emitted addresses must be exhibited as extending their home document's anchor before T10 applies); (iii) the ChainMembershipForOrigin lemma's contiguous-prefix postcondition below (indirectly, by underwriting the prefix-relation premises consumed by the chain-membership argument).

*Remark — derivable clauses.* Two of the four axiom clauses are derivable from the other two together with foundation-level claims; they are stated in the axiom for citation convenience rather than as primitive content.

- *Disjoint follows from FirstEmission + ChainDiscipline.* FirstEmission pins the first emission's concrete form `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`), fixing `E(·)₁` at `s_C` (resp. `s_L`). ChainDiscipline extends each chain by `inc(·, 0)` steps; for T4-valid `t` with `#E(t) ≥ 2`, TA5-SigValid gives `sig(t) = #t` and the element-field index `1` (carrying `E₁`) sits at position `#d + 2 ≤ #t − 1`, so TA5(c)'s single-position modification at `sig(t) = #t` leaves `E₁` untouched (TA5(b) propagates positions `1..#t` agreement, so `E₁` is preserved by every chain step). Hence every chain element inherits the first emission's `E₁` value, and SC-NEQ (`s_C ≠ s_L`) forces the two chains' images to be disjoint.
- *FirstEmission's freshness conclusion `a ∉ dom(C) ∪ dom(L)` follows from the first-emit predicate + L0 + ChainPrefixExtension + ChainMembershipForOrigin + StoreT4Validity + Cross-document disjointness + SC-NEQ + T7.* Under the K.α first-emit predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`, every `a' ∈ dom(C)` has `origin(a') ≠ d`. *Against `dom(C)`:* (i) `a = [d.0.s_C.1]` is the first emission of `A_C(d)`, so by ChainPrefixExtension (base case) `b_C(d) ≼ a`. (ii) For every `a' ∈ dom(C)` with `origin(a') ≠ d`, ChainMembershipForOrigin (below) at the pre-state places `a' ∈ A_C(origin(a'))` (well-defined since `origin(a') ∈ dom(M)` by C2), and ChainPrefixExtension gives `b_C(origin(a')) ≼ a'`. (iii) Cross-document disjointness applied to `(d, origin(a'))` gives `b_C(d) ⋠ b_C(origin(a')) ∧ b_C(origin(a')) ⋠ b_C(d)`. (iv) T10 (PartitionIndependence, ASN-0034) closes: `a ≠ a'`. *Against `dom(L)`:* StoreT4Validity (below) at the pre-state gives T4-validity of every `ℓ ∈ dom(L)`; `a` is T4-valid by the chain-element T4-validity argument (FirstEmission's T4-valid `[d.0.s_C.1]` by inspection given M0's T4-valid `d`). By L0, `E(ℓ)₁ = s_L` and `E(a)₁ = s_C`; by SC-NEQ, `s_C ≠ s_L`; `zeros(a) = zeros(ℓ) = 3` by FirstEmission's structural form and L1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `a ≠ ℓ`. The K.λ first-emit derivation is symmetric (mutatis mutandis: `b_L` in place of `b_C`, content↔link store roles, `s_L`↔`s_C`).

A leaner axiom retaining only Exists + FirstEmission's *structural* form (concrete tumbler `[d.0.s_C.1]` resp. `[d.0.s_L.1]`) + ChainDiscipline suffices. Disjoint and FirstEmission's freshness conclusion are retained inside the axiom block so that downstream proofs cite a single axiom name rather than reassembling the derivation each time.

**Lemma (ChainMembershipForOrigin).** At every reachable state `Σ`, every entry of `dom(C)` (resp. `dom(L)`) inhabits the content (resp. link) sub-allocator chain of its origin, and forms a *contiguous initial segment* of that chain. Letting `A_C(d) = (t_1, t_2, t_3, …)` denote the enumeration of `d`'s content sub-allocator chain (with `t_1` the first emission and `t_{n + 1} = inc(t_n, 0)`), and `A_L(d) = (s_1, s_2, s_3, …)` the analogous link chain:

- `(A d ∈ dom(M) :: (E m_d ≥ 0 :: dom(C) ∩ {a' ∈ T : origin(a') = d} = {t_1, …, t_{m_d}}))` (content contiguous prefix; `{t_1, …, t_0} = ∅` by convention)
- `(A d ∈ dom(M) :: (E n_d ≥ 0 :: dom(L) ∩ {ℓ' ∈ T : origin(ℓ') = d} = {s_1, …, s_{n_d}}))` (link contiguous prefix)

The weaker subset inclusion `dom(C) ∩ {a' : origin(a') = d} ⊆ A_C(d)` (and its link analogue) is the immediate corollary of the contiguous-prefix form; downstream consumers cite either form as needed. The contiguity matches ASN-0040's B1 (ContiguousPrefix) for the baptismal registry: the content and link sub-allocator chains have the same "always-extend-by-one-from-the-current-frontier" discipline as Nelson's baptism. The further *partition* claim — pairwise disjointness of the chains across distinct origins together with joint coverage of `dom(C)` and `dom(L)` — is recoverable as a corollary but not needed by downstream consumers: covering follows from C2 + L1a (every store entry has `origin(·) ∈ dom(M)`); cross-document disjointness `A_C(d) ∩ A_C(d') = ∅` for `d ≠ d'` (and the link analogue) follows from the Cross-document disjointness lemma applied at the first-emission anchors `b_C(d)`, `b_L(d)`.

*Proof.* Induction on transition sequences from `Σ₀`.

*Base.* At `Σ₀`, both `dom(C)` and `dom(L)` are empty, so both inclusions hold vacuously for every `d`.

*Step.* Assume both inclusions hold at `Σ`. The substrate admits three transition kinds:

- *K.σ(d_new):* `C` and `L` are in frame, so for every `d` already in `dom(M)` the intersection set is unchanged and the contiguous-prefix postcondition transfers at the same `m_d` (resp. `n_d`). For the freshly registered `d_new`, the intersection sets are empty in `Σ'`. *Content clause derivation:* By the inductive hypothesis on C2 at `Σ`, every `a ∈ dom(C(Σ))` satisfies `origin(a) ∈ dom(M(Σ))`. By K.σ's precondition, `d_new ∉ dom(M(Σ))`. Therefore `origin(a) ≠ d_new` for every `a ∈ dom(C(Σ))`. Since `C` is in frame (`C(Σ') = C(Σ)`), `dom(C(Σ')) ∩ {a' : origin(a') = d_new} = dom(C(Σ)) ∩ {a' : origin(a') = d_new} = ∅ = {t_1, …, t_0}`, witnessing `m_{d_new} = 0` at `Σ'`. *Link clause derivation:* Symmetric, using the inductive hypothesis on L1a at `Σ` together with K.σ's precondition `d_new ∉ dom(M(Σ))` and frame on `L`, yielding `n_{d_new} = 0`.

- *K.α(d, a, v):* Only `dom(C)` grows, by one element `a` with `origin(a) = d`. For `d' ∈ dom(M)` with `d' ≠ d`, the intersection set `dom(C') ∩ {a' : origin(a') = d'} = dom(C) ∩ {a' : origin(a') = d'}` is unchanged (the new `a` has `origin(a) = d ≠ d'`), so the contiguous-prefix postcondition transfers at the same `m_{d'}`. For `d` itself, two sub-cases via the K.α emission rule:
  - *First emission* (`{a' ∈ dom(C) : origin(a') = d} = ∅`; equivalently `m_d = 0` at `Σ` by IH): by SubAllocatorAxiom.FirstEmission, `a = [d.0.s_C.1] = t_1` is the first emission of `A_C(d)`'s chain. The intersection set at `Σ'` is `{a} = {t_1}`, witnessing `m_d = 1` at `Σ'`.
  - *Subsequent emission* (`{a' ∈ dom(C) : origin(a') = d} ≠ ∅`; equivalently `m_d ≥ 1` at `Σ` by IH): by IH, the prior intersection is `{t_1, …, t_{m_d}}`. The lex-order maximum of this finite set is `t_{m_d}` by T10a.7 (EnumerationInjectivity)'s strict monotonicity `t_i < t_j` for `i < j` (applicability justified by the *T10a chain-lemma applicability* remark), so `a_prev := max{a' ∈ dom(C) : origin(a') = d} = t_{m_d}`. By SubAllocatorAxiom.ChainDiscipline, `A_C(d)` is closed under `inc(·, 0)`, so `a = inc(t_{m_d}, 0) = t_{m_d + 1}`. The new intersection set at `Σ'` is `{t_1, …, t_{m_d}, t_{m_d + 1}} = {t_1, …, t_{m_d + 1}}`, witnessing the chain index `m_d + 1` at `Σ'`.

  The link contiguous-prefix postcondition is unchanged by frame on `dom(L)`.

- *K.λ(d, ℓ, (e₁, …, eₙ)):* Symmetric to K.α with content↔link, using SubAllocatorAxiom.FirstEmission for the first-emit branch (placing `ℓ = s_1`, witnessing `n_d = 1`) and SubAllocatorAxiom.ChainDiscipline for the subsequent-emit branch (placing `ℓ = s_{n_d + 1}` from `ℓ_prev = s_{n_d}` by T10a.7, witnessing `n_d + 1` at `Σ'`). The content contiguous-prefix postcondition is unchanged by frame on `dom(C)`. ∎

This lemma is the inductive invariant that licenses application of T10a.7 (EnumerationInjectivity) to `(a_prev, a)` in the K.α subsequent-emit case and to `(ℓ_prev, ℓ)` in the K.λ subsequent-emit case: T10a.7 (applicability justified by the *T10a chain-lemma applicability* remark above) requires both indices to inhabit the same chain, and ChainMembershipForOrigin supplies that membership for the predecessor.

**Corollary (StoreT4Validity).** At every reachable state `Σ`, every entry of `dom(C) ∪ dom(L)` is a T4-valid tumbler:

  `(A a ∈ dom(C) :: ValidAddress(a))`
  `(A ℓ ∈ dom(L) :: ValidAddress(ℓ))`

*Proof.* For any `a ∈ dom(C)`, ChainMembershipForOrigin places `a ∈ A_C(origin(a))` (well-defined since `origin(a) ∈ dom(M)` by C2). By SubAllocatorAxiom.FirstEmission the chain's first emission is the concrete structural form `[origin(a).0.s_C.1]`, T4-valid by direct inspection given M0's T4-valid `origin(a)`: its components reproduce `origin(a)`'s positive boundary and zero-count structure with the addition of one zero separator at position `#origin(a) + 1` and two positive components `s_C` and `1` at positions `#origin(a) + 2, #origin(a) + 3`, satisfying T4's no-adjacent-zeros, positive-endpoint, and `zeros = 3 ≤ 3` conjuncts. TA5a (IncrementPreservesT4, ASN-0034) applied per-step under `k = 0` (unconditional T4-preservation) propagates T4-validity from the first emission to every subsequent chain element. Hence `a` is T4-valid. The link case is symmetric: `ℓ ∈ dom(L)` lies in `A_L(origin(ℓ))` by ChainMembershipForOrigin, the first emission `[origin(ℓ).0.s_L.1]` is T4-valid by inspection, and TA5a propagates. ∎

This corollary discharges the T4-validity precondition of T7 (FirstElementFieldDistinction, ASN-0034) wherever T7 is cited against `dom(C)` and `dom(L)` — in particular, in the L14 discharge (matrix below) and in the FirstEmission derivable-clauses Remark above against `dom(L)`.


## Cross-document disjointness chain

**Lemma (Cross-document disjointness; T10 + Prefix + M0).** For any two distinct documents `d₁, d₂ ∈ dom(M)` with `d₁ ≠ d₂`, the link sub-allocator anchors `p₁ := b_L(d₁) = [d₁.0.s_L]` and `p₂ := b_L(d₂) = [d₂.0.s_L]` satisfy

  `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`

so by T10 (PartitionIndependence, ASN-0034), every address extending `p₁` differs from every address extending `p₂`. The same lemma holds with `b_C` in place of `b_L` for content allocations.

*Proof.* By M0, both `d₁, d₂ ∈ dom(M)` are T4-valid tumblers with `zeros(d_i) = 2`. Case-split on the document-level prefix relationship: prefix-comparable or prefix-incomparable.

*Case A — Prefix-comparable.* WLOG `d₁ ≼ d₂` and `d₁ ≠ d₂`, so `#d₁ < #d₂` and the component `d₂[#d₁+1]` is well-defined. The prefix relation gives `d₂[k] = d₁[k]` for `1 ≤ k ≤ #d₁`, so `d₂`'s first `#d₁` positions contain `d₁`'s two zero components; for `zeros(d₂) = 2` to hold (M0 at `d₂`), `d₂[#d₁+1] ≠ 0`.

The anchors are length-`+2` extensions of their respective document addresses: `#p_i = #d_i + 2`, with `p_i[k] = d_i[k]` for `1 ≤ k ≤ #d_i`, `p_i[#d_i + 1] = 0`, and `p_i[#d_i + 2] = s_L`. From `#d₁ < #d₂` we obtain `#p₁ ≤ #p₂` (in fact `#p₁ < #p₂`).

At position `k = #d₁ + 1`:
- `k ≤ #p₁` since `k = #d₁ + 1 ≤ #d₁ + 2 = #p₁`
- `k ≤ #p₂` since `k = #d₁ + 1 < #d₂ + 2 = #p₂` (using `#d₁ < #d₂`)

So `k ≤ min(#p₁, #p₂)`. The values:
- `p₁[k] = p₁[#d₁ + 1] = 0` (the zero separator inserted by the `b_L` construction)
- `p₂[k] = p₂[#d₁ + 1] = d₂[#d₁ + 1] ≠ 0` (by the T4 zero-count argument above; `#d₁ + 1 ≤ #d₂` since `#d₁ < #d₂`)

Thus `p₁[k] = 0 ≠ p₂[k]` at an index within both anchors, witnessing `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` via the position-divergence clause of Prefix (ASN-0034).

*Case B — Prefix-incomparable.* `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` at the document level. The joint conjunction does not directly yield a position divergence at `k ≤ min(#d₁, #d₂)`: in asymmetric-length subcases, one of the two `⋠` clauses is satisfied by the failure of Prefix's length conjunct alone, supplying no component-divergence witness; the position-divergence witness must be extracted from the *other* clause. We case-split on the length relationship between `d₁` and `d₂`, exhaustive by NAT-order's at-least-one trichotomy at `(#d₁, #d₂)`.

*Sub-case B.i — `#d₁ ≤ #d₂`.* The length conjunct `#d₁ ≤ #d₂` of `d₁ ≼ d₂` holds, so `d₁ ⋠ d₂` must be witnessed by failure of the component conjunct: there exists `i` with `1 ≤ i ≤ #d₁` and `d₂[i] ≠ d₁[i]`. Take `k := i`; then `k ≤ #d₁ = min(#d₁, #d₂)` and `d₁[k] ≠ d₂[k]`. (At equality `#d₁ = #d₂`, the same argument also applies symmetrically through `d₂ ⋠ d₁`; T3 (CanonicalRepresentation, ASN-0034) provides an alternative route, since `d₁ ≠ d₂` together with `#d₁ = #d₂` forces a position divergence.)

*Sub-case B.ii — `#d₂ < #d₁`.* Symmetric: the length conjunct of `d₂ ≼ d₁` holds, so `d₂ ⋠ d₁` is witnessed by some `i` with `1 ≤ i ≤ #d₂` and `d₁[i] ≠ d₂[i]`. Take `k := i`; then `k ≤ #d₂ = min(#d₁, #d₂)`.

In either sub-case the witness `k` satisfies `k ≤ min(#d₁, #d₂)`. From `#p_i = #d_i + 2`, NAT-addcompat's strict successor lifts `#d_i ≤ #p_i`, so `min(#d₁, #d₂) ≤ min(#p₁, #p₂)`. The anchors are length-`+2` extensions agreeing with `d_i` at positions `1..#d_i`, so `p₁[k] = d₁[k] ≠ d₂[k] = p₂[k]` at an index within both anchors, witnessing `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` via the position-divergence clause of Prefix (ASN-0034).

*Closure.* T10 (PartitionIndependence, ASN-0034) applies uniformly: for any `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`, we have `a ≠ b`. Every link address allocated under `d₁` extends `p₁ = b_L(d₁)`; every link address allocated under `d₂` extends `p₂ = b_L(d₂)`. Therefore no link allocated under `d₁` can coincide with any link allocated under `d₂`. The same argument with `b_C(d_i)` in place of `b_L(d_i)` gives cross-document content disjointness. ∎

Cross-subspace collisions between `dom(C)` and `dom(L)` are prevented by L14 (StoreDisjointness, above), itself derived from L0 + SC-NEQ + T7.


## Substrate primitive operations

The substrate admits three primitive transitions, one per state component. Each is atomic — its precondition is evaluated against `Σ` and its effect committed to `Σ'` in a single indivisible step; no intermediate state with the transition partially applied is admitted.

*Parameter semantics.* For `K.α(d, a, v)` and `K.λ(d, ℓ, (e₁, …, eₙ))`, the address parameters `a` and `ℓ` appear in the operation signatures but their values are not free choices of the caller: the preconditions deterministically pin them from `(d, Σ)`. Specifically, the first-emit predicate forces `a = [d.0.s_C.1]` (resp. `ℓ = [d.0.s_L.1]`); the subsequent-emit predicate forces `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` (resp. `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)`). A caller is expected to compute the address from the current state via this pinning rule before invoking the operation; supplying a stale or otherwise non-conforming value causes the precondition check to fail. Implementations may treat the address as an output computed from `(d, Σ)` rather than as a free input; the substrate's semantics is unchanged in either reading because the pinning is total.

### K.σ (DocumentRegistration)

Extends `dom(M)` by registering a new document address with an empty arrangement.

*Precondition:*
- `d ∉ dom(M)` (fresh document address)
- `ValidAddress(d) ∧ zeros(d) = 2` (T4-valid, document-level — discharges M0 at the new key)

*Effect:* `dom(M') = dom(M) ∪ {d}`, with `M'(d) = ∅` and `M'(d') = M(d')` for every `d' ∈ dom(M)`.

*Frame:* `C' = C; L' = L`

*Cross-store freshness.* K.σ has no explicit `d ∉ dom(C) ∪ dom(L)` clause because cross-store freshness is automatic from the substrate's invariants: C1 forces `zeros(a) = 3` for every `a ∈ dom(C)`, L1 forces `zeros(ℓ) = 3` for every `ℓ ∈ dom(L)`, and K.σ's precondition pins `zeros(d) = 2`. Since no address can simultaneously satisfy `zeros = 2` and `zeros = 3`, `d ∉ dom(C) ∪ dom(L)` is forced by the precondition list together with C1/L1.

K.σ activates `A_C(d)` and `A_L(d)` per SubAllocatorAxiom.Exists, opening the content and link sub-allocator frontiers under `d` for subsequent K.α and K.λ emissions. K.σ is the substrate-level document-introduction primitive; higher-layer ASNs that need entity stratification, lineage discipline, or version-allocator activation compose K.σ with their own additional preconditions (e.g., a higher-layer document-introduction primitive rebuilds itself as K.σ-plus-entity-set-tracking-plus-lineage-discipline-plus-version-allocator-activation).

This substrate makes no commitment about *which* document addresses are admissible at K.σ beyond T4-validity and `zeros(d) = 2`. The discipline that constrains which tumblers are introduced (Nelson's hierarchical baptism, T10a allocator conformance for the document allocator, etc.) is a higher-layer commitment; the substrate's only commitment is that whatever `d` is introduced satisfies M0 going forward. In particular, K.σ admits address-space configurations broader than Nelson's hierarchical baptism — a tumbler `d` with `zeros(d) = 2` whose prefix corresponds to no allocated node or account is structurally admissible at this layer. Downstream ASNs that lift entity-hierarchy discipline tighten K.σ's precondition accordingly.

### K.α (ContentAllocation)

Extends `dom(C)` with a fresh content address scoped to an allocated document.

*Precondition:*
- `d ∈ dom(M)` (home document exists)
- `a ∉ dom(C) ∪ dom(L)` (fresh address — L14)
- `zeros(a) = 3 ∧ E(a)₁ = s_C` (element-level, content subspace — C1, L0)
- `#E(a) ≥ 2` (C1b)
- `origin(a) = d` (scoped to home document — C2)
- `a` is produced by `d`'s content sub-allocator `A_C(d)`:
  - *First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`. Freshness against `dom(C) ∪ dom(L)` is pinned by SubAllocatorAxiom.FirstEmission directly.
  - *Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(a_prev, 0)` (TA5(c)) where `a_prev := max{a' ∈ dom(C) : origin(a') = d}`, the next sibling on `A_C(d)`'s `inc(·, 0)` chain. The `max` is well-defined because the set is finite (C-fin restricted by `origin(·) = d`). *Within-document freshness against `dom(C)`* is discharged by combining T10a.7 with the max-property of `a_prev`. Let `n_prev` be the chain index of `a_prev` within `A_C(d)`. For every `a' ∈ dom(C)` with `origin(a') = d`: (i) ChainMembershipForOrigin places `a' ∈ A_C(d)` at some chain index `m`; (ii) T10a.7 (EnumerationInjectivity, applicability justified by the *T10a chain-lemma applicability* remark) gives strict monotonicity `m < n ⟹ t_m < t_n`, whose contrapositive `t_m ≥ t_n ⟹ m ≥ n` combined with `a' ≤ a_prev` (the lex-order max-property) yields `m ≤ n_prev`; (iii) SubAllocatorAxiom.ChainDiscipline places `a = inc(a_prev, 0)` at chain index `n_prev + 1`, so T10a.7 then yields `a' = t_m ≤ t_{n_prev} = a_prev < t_{n_prev + 1} = a`, hence `a' ≠ a`. The max-property of `a_prev` alone bounds `dom(C)_d`'s chain indices from above. (ChainMembershipForOrigin's stronger contiguous-prefix postcondition identifies the prior intersection as `{t_1, …, t_{m_d}}` with `a_prev = t_{m_d}` and `a = t_{m_d + 1}`, but the freshness argument needs only the subset form.) *Cross-document freshness against `dom(C)`* (for `a' ∈ dom(C)` with `origin(a') ≠ d`) is discharged in three steps: (a) `a = inc(a_prev, 0)` extends `b_C(d)` — by IH on ChainMembershipForOrigin at `Σ`, `a_prev ∈ A_C(d)`; by ChainPrefixExtension at `Σ`, `b_C(d) ≼ a_prev`; ChainPrefixExtension's step argument (TA5(b)/(c) at `k = 0` preserving positions `1..#a_prev − 1` under TA5-SigValid pinning `sig(a_prev) = #a_prev`) carries the prefix relation forward, giving `b_C(d) ≼ a`. (b) For every `a' ∈ dom(C)` with `origin(a') ≠ d`: ChainMembershipForOrigin at `Σ` places `a' ∈ A_C(origin(a'))` (well-defined since `origin(a') ∈ dom(M)` by C2 at `Σ`), and ChainPrefixExtension at `Σ` gives `b_C(origin(a')) ≼ a'`. (c) Cross-document disjointness applied to `(d, origin(a'))` gives `b_C(d) ⋠ b_C(origin(a')) ∧ b_C(origin(a')) ⋠ b_C(d)`; T10 (PartitionIndependence, ASN-0034) closes: `a ≠ a'`. *Freshness against `dom(L)`* is discharged by L0 + SC-NEQ + StoreT4Validity + T7: StoreT4Validity at `Σ` gives T4-validity of every `ℓ ∈ dom(L)`; `a` is T4-valid by chain-element T4-validity (since `a ∈ A_C(d)` by ChainDiscipline's closure under `inc(·, 0)` applied to `a_prev`, and FirstEmission + TA5a propagation gives T4 along the chain); L0 supplies `E(a)₁ = s_C ≠ s_L = E(ℓ)₁` (SC-NEQ); `zeros(a) = zeros(ℓ) = 3` by C1/L1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `a ≠ ℓ`. (Equivalently the conclusion may be cited via L14 at the pre-state — the two routes derive the same fact.)
- `v ∈ Val` (well-formed content value)

*Effect:* `C' = C ∪ {a ↦ v}`

*Frame:* `L' = L; (A d' :: M'(d') = M(d'))`

Cross-document disjointness for content allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_C(d)` and `p₂ := b_C(d')`.

### K.λ (LinkAllocation)

Extends `dom(L)` with a fresh link address scoped to an allocated document.

Signature: `K.λ(d, ℓ, (e₁, …, eₙ))` where the link value is a finite sequence of `N` endsets.

*Precondition:*
- `d ∈ dom(M)` (home document exists)
- `ℓ ∉ dom(L) ∪ dom(C)` (fresh address — L14)
- `zeros(ℓ) = 3 ∧ E(ℓ)₁ = s_L` (element-level, link subspace — L0, L1)
- `#E(ℓ) ≥ 2` (L1b)
- `origin(ℓ) = d` (scoped to home document — L1a)
- `ℓ` is produced by `d`'s link sub-allocator `A_L(d)`:
  - *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`, the determinate first emission of `A_L(d)`. Freshness against `dom(L) ∪ dom(C)` is pinned by SubAllocatorAxiom.FirstEmission directly.
  - *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(ℓ_prev, 0)` (TA5(c)) where `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`, the next sibling on `A_L(d)`'s `inc(·, 0)` chain. The `max` is well-defined because the set is finite (L-fin restricted by `origin(·) = d`). *Within-document freshness against `dom(L)`* is discharged by combining T10a.7 with the max-property of `ℓ_prev`. Let `n_prev` be the chain index of `ℓ_prev` within `A_L(d)`. For every `ℓ' ∈ dom(L)` with `origin(ℓ') = d`: (i) ChainMembershipForOrigin places `ℓ' ∈ A_L(d)` at some chain index `m`; (ii) T10a.7 (EnumerationInjectivity, applicability justified by the *T10a chain-lemma applicability* remark) gives strict monotonicity `m < n ⟹ t_m < t_n`, whose contrapositive combined with `ℓ' ≤ ℓ_prev` (the lex-order max-property) yields `m ≤ n_prev`; (iii) SubAllocatorAxiom.ChainDiscipline places `ℓ = inc(ℓ_prev, 0)` at chain index `n_prev + 1`, so T10a.7 then yields `ℓ' = t_m ≤ t_{n_prev} = ℓ_prev < t_{n_prev + 1} = ℓ`, hence `ℓ' ≠ ℓ`. The max-property of `ℓ_prev` alone bounds `dom(L)_d`'s chain indices from above. (ChainMembershipForOrigin's stronger contiguous-prefix postcondition identifies the prior intersection as `{s_1, …, s_{n_d}}` with `ℓ_prev = s_{n_d}` and `ℓ = s_{n_d + 1}`, but the freshness argument needs only the subset form.) *Cross-document freshness against `dom(L)`* (for `ℓ' ∈ dom(L)` with `origin(ℓ') ≠ d`) is discharged in three steps: (a) `ℓ = inc(ℓ_prev, 0)` extends `b_L(d)` — by IH on ChainMembershipForOrigin at `Σ`, `ℓ_prev ∈ A_L(d)`; by ChainPrefixExtension at `Σ`, `b_L(d) ≼ ℓ_prev`; ChainPrefixExtension's step argument (TA5(b)/(c) at `k = 0` preserving positions `1..#ℓ_prev − 1` under TA5-SigValid pinning `sig(ℓ_prev) = #ℓ_prev`) carries the prefix relation forward, giving `b_L(d) ≼ ℓ`. (b) For every `ℓ' ∈ dom(L)` with `origin(ℓ') ≠ d`: ChainMembershipForOrigin at `Σ` places `ℓ' ∈ A_L(origin(ℓ'))` (well-defined since `origin(ℓ') ∈ dom(M)` by L1a at `Σ`), and ChainPrefixExtension at `Σ` gives `b_L(origin(ℓ')) ≼ ℓ'`. (c) Cross-document disjointness applied to `(d, origin(ℓ'))` gives `b_L(d) ⋠ b_L(origin(ℓ')) ∧ b_L(origin(ℓ')) ⋠ b_L(d)`; T10 (PartitionIndependence, ASN-0034) closes: `ℓ ≠ ℓ'`. *Freshness against `dom(C)`* is discharged by L0 + SC-NEQ + StoreT4Validity + T7: StoreT4Validity at `Σ` gives T4-validity of every `a ∈ dom(C)`; `ℓ` is T4-valid by chain-element T4-validity (since `ℓ ∈ A_L(d)` by ChainDiscipline's closure, with FirstEmission + TA5a propagation); L0 supplies `E(ℓ)₁ = s_L ≠ s_C = E(a)₁` (SC-NEQ); `zeros(ℓ) = zeros(a) = 3` by L1/C1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `ℓ ≠ a`. (Equivalently the conclusion may be cited via L14 at the pre-state.)
- `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` (well-formed link value with mandatory non-empty type endset at slot 3 — L3). The arity-3 default `(F, G, Θ)` (slot 1 = from, slot 2 = to, slot 3 = type) is the StandardTriple convention retained for worked examples and notational compactness; the substrate admits arbitrary arity `N ≥ 3`.

*Effect:* `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`

*Frame:* `C' = C; (A d' :: M'(d') = M(d'))`

Cross-document disjointness for link allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_L(d)` and `p₂ := b_L(d')`.

*Forward allocation, derivable.* The within-document forward-allocation property `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` is not stated as a precondition because it is a derivable consequence of the emission rules — symmetrically with K.α. In the subsequent-emission case, `ℓ = inc(max{prev}, 0)` and TA5(a) gives `inc(t, 0) > t`, so `ℓ > max{prev} ≥ ℓ'` for every `ℓ' ∈ dom(L)` with `origin(ℓ') = d`. In the first-emission case the universal antecedent `{ℓ' : origin(ℓ') = d} = ∅` is vacuous. The same derivation applies to K.α's content emissions; neither operator carries the clause as a precondition.


## Worked example

To make the substrate's operation concrete, we trace a small scenario step-by-step starting from `Σ₀ = (∅, ∅, ∅)`.

*Arity convention.* The K.λ invocations below use the arity-3 default `(F, G, Θ)` (StandardTriple — slot 1 from, slot 2 to, slot 3 type) for notational compactness. This is one admissible instance of K.λ's general signature `K.λ(d, ℓ, (e₁, …, eₙ))` with `N = 3`; the substrate admits arbitrary `N ≥ 3` per L3, and any higher-arity link value satisfying the precondition would be equally well-formed.

*Fix a document address.* Let `d = [1, 0, 2, 0, 5]` — `#d = 5`, with zeros at positions 2 and 4 so `zeros(d) = 2`, with positive first and last components (1 and 5) and no adjacent zeros, hence T4-valid. By T4b, its projections are `N(d) = [1]`, `U(d) = [2]`, `D(d) = [5]`. By SubspaceConventionAxiom, `s_C = 1` and `s_L = 2`.

*Step 1 — `K.σ(d)` (document registration).* Precondition: `d ∉ dom(M₀) = ∅` ✓; `ValidAddress(d) ∧ zeros(d) = 2` ✓. Effect commits `dom(M₁) = {d}` with `M₁(d) = ∅`; `C₁ = ∅`, `L₁ = ∅`. By SubAllocatorAxiom.Exists, both `A_C(d)` and `A_L(d)` chains are active under `d`. Verifying invariants at `Σ₁ = (∅, ∅, {d ↦ ∅})`: M0 holds (the single key `d` satisfies `zeros = 2`); M1 holds (`∅ ⊆ {d}`); all C-/L-invariants and L14, L-fin, C-fin are vacuous or trivial on empty stores.

*Step 2 — `K.α(d, a, v)` (first content emission).* Pinning the address from `Σ₁`: the predicate `{a' ∈ dom(C₁) : origin(a') = d} = ∅` selects the first-emit case, so `a = [d.0.s_C.1] = [1, 0, 2, 0, 5, 0, 1, 1]`. Witness it via the C1c chain `(t₀, t₁, t₂)`:
- `t₀ = d = [1, 0, 2, 0, 5]`
- `t₁ = inc(d, 2)`: TA5(d) at `k = 2` appends `[0, 1]`, yielding `[1, 0, 2, 0, 5, 0, 1] = b_C(d)`. Admissibility: M0 gives `zeros(d) = 2 ≤ 2`, satisfying T10a's `k = 2` side condition; TA5(d) gives `zeros(t₁) = 3`, T4-valid.
- `t₂ = inc(b_C(d), 1)`: TA5(d) at `k = 1` appends `1`, yielding `[1, 0, 2, 0, 5, 0, 1, 1] = a`. Admissibility: `k = 1` has no zero-count side condition; `zeros(t₂) = 3`, T4-valid; `#E(t₂) = 2`.

Verifying preconditions: `a ∉ dom(C₁) ∪ dom(L₁) = ∅` ✓; `zeros(a) = 3` ✓; `E(a) = [1, 1]` so `E(a)₁ = 1 = s_C` ✓; `#E(a) = 2 ≥ 2` ✓; `origin(a) = N(a).0.U(a).0.D(a) = [1].0.[2].0.[5] = d` ✓. Freshness of `a` against `dom(C₁) ∪ dom(L₁)` is pinned by SubAllocatorAxiom.FirstEmission directly.

Effect: `C₂ = {a ↦ v}`; `L₂ = ∅`; `M₂ = M₁`. Verifying invariants at `Σ₂`: C0 (extended at fresh `a`), C1 (`zeros(a) = 3`), C1b (`#E(a) = 2`), C1c (chain exhibited above), C2 (`origin(a) = d ∈ dom(M₂)`), C-fin (`|dom(C₂)| = 1 < ∞`) all hold at the new key.

*Step 3 — `K.λ(d, ℓ, F, G, Θ)` (first link emission).* Pinning from `Σ₂`: the predicate `{ℓ' ∈ dom(L₂) : origin(ℓ') = d} = ∅` selects the first-emit case, so `ℓ = [d.0.s_L.1] = [1, 0, 2, 0, 5, 0, 2, 1]`. Witness via the L1c chain `(t₀, t₁, t₂, t₃)`:
- `t₀ = d = [1, 0, 2, 0, 5]`
- `t₁ = inc(d, 2) = [1, 0, 2, 0, 5, 0, 1] = b_C(d)` (admissibility as in Step 2)
- `t₂ = inc(b_C(d), 0)`: TA5(c) at `k = 0` increments `b_C(d)`'s rightmost nonzero component (position 7, from `1` to `2`), yielding `[1, 0, 2, 0, 5, 0, 2] = b_L(d)`. By SubspaceConventionAxiom, `s_L = 2 = s_C + 1`, matching position 7. Admissibility: TA5(c) is unconditionally T4-preserving.
- `t₃ = inc(b_L(d), 1)`: TA5(d) at `k = 1` appends `1`, yielding `[1, 0, 2, 0, 5, 0, 2, 1] = ℓ`. `zeros(ℓ) = 3`, T4-valid, `#E(ℓ) = 2`.

Verifying preconditions: `ℓ ∉ dom(L₂) ∪ dom(C₂) = {a}`. Disagreement at position 7 (`a₇ = 1` vs `ℓ₇ = 2`) gives `ℓ ≠ a`, confirming the L0 + SC-NEQ + T7 derivation: the two addresses sit in disjoint subspaces. `zeros(ℓ) = 3` ✓; `E(ℓ) = [2, 1]` so `E(ℓ)₁ = 2 = s_L` ✓; `#E(ℓ) = 2 ≥ 2` ✓; `origin(ℓ) = d` ✓. Freshness pinned by SubAllocatorAxiom.FirstEmission.

Effect: `L₃ = {ℓ ↦ (F, G, Θ)}`; `C₃ = C₂`; `M₃ = M₂`. Verifying invariants at `Σ₃`: L0/L1/L1a/L1b/L1c/L3/L12 all hold at the new key per the matrix; L14 holds non-trivially: `dom(C₃) ∩ dom(L₃) = {a} ∩ {ℓ} = ∅` (verified by E(·)₁ disagreement); L-fin holds (`|dom(L₃)| = 1 < ∞`).

*Step 4 — `K.α(d, a', v')` (second content emission, subsequent-emit branch).* Pinning from `Σ₃`: `{a'' ∈ dom(C₃) : origin(a'') = d} = {a}` is non-empty, so the subsequent-emit branch fires with `a' = inc(max{a}, 0) = inc(a, 0)`. Since `sig(a) = 8` with value `1`, TA5(c) gives `a' = [1, 0, 2, 0, 5, 0, 1, 2]`. The C1c chain extends `a`'s chain by one step: `(t₀, t₁, t₂, a')` with `a' = inc(t₂, 0) = inc(a, 0)`. Admissibility of the new step: TA5(c) at `k = 0` is unconditionally T4-preserving; freshness against `dom(C₃) = {a}` discharged by T10a.7 (within-chain injectivity) applied to `A_C(d)`'s chain (per SubAllocatorAxiom.ChainDiscipline); freshness against `dom(L₃) = {ℓ}` discharged by L0 + SC-NEQ + T7.

Verifying preconditions: `a' ∉ dom(C₃) ∪ dom(L₃) = {a, ℓ}` ✓ (since `a' > a` strictly by TA5(a), and `E(a')₁ = 1 ≠ 2 = E(ℓ)₁`); structural preconditions inherit from `a` via the inc rule (TA5(b) preserves `zeros`, `E(·)₁`, and `origin(·)`).

Effect: `C₄ = {a ↦ v, a' ↦ v'}`; `L₄ = L₃`; `M₄ = M₃`. All invariants continue to hold at `Σ₄`.

*Step 5 — `K.σ(d')` (second document registration).* Fix a second document address `d' = [1, 0, 2, 0, 5, 3]`. Verifying T4-validity: `#d' = 6`, zeros at positions 2 and 4 only (`zeros(d') = 2`), no adjacent zeros (positions (2,3) = (0,2) and (4,5) = (0,5)), first component `d'[1] = 1 ≠ 0`, last component `d'[6] = 3 ≠ 0`. By T4b, `N(d') = [1]`, `U(d') = [2]`, `D(d') = [5, 3]`. Precondition: `d' ∉ dom(M₄) = {d}` ✓ (distinct since `#d = 5 ≠ 6 = #d'`); `ValidAddress(d') ∧ zeros(d') = 2` ✓. Effect: `dom(M₅) = {d, d'}`, with `M₅(d') = ∅` and `M₅(d) = M₄(d) = ∅`. By SubAllocatorAxiom.Exists, `A_C(d')` and `A_L(d')` become active at `Σ₅` (per the *Active sub-allocator chains* definition: `d' ∈ dom(M₅)`), alongside the already-active `A_C(d)` and `A_L(d)`.

*Verifying the Cross-document disjointness lemma at Σ₅.* Apply with `d₁ = d`, `d₂ = d'`. Component-by-component: `d'[1..5] = [1, 0, 2, 0, 5] = d`, with `#d < #d'`, so `d ≼ d' ∧ d ≠ d'`. Case A fires. The anchors are `p₁ = b_L(d) = [1, 0, 2, 0, 5, 0, 2]` (length 7) and `p₂ = b_L(d') = [1, 0, 2, 0, 5, 3, 0, 2]` (length 8). At index `k = #d + 1 = 6`:
- `p₁[6] = 0` (the zero separator inserted by the `b_L` construction at position `#d + 1`)
- `p₂[6] = d'[6] = 3 ≠ 0` (`d'` carries its two zeros at positions 2 and 4 by `zeros(d') = 2`, so position 6 must be nonzero per the T4 zero-count argument)
- `k = 6 ≤ min(#p₁, #p₂) = 7` ✓

Thus `p₁[6] = 0 ≠ 3 = p₂[6]`, witnessing `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`. The same divergence holds at position 6 for the content anchors `b_C(d) = [1, 0, 2, 0, 5, 0, 1]` and `b_C(d') = [1, 0, 2, 0, 5, 3, 0, 1]`. By T10, every link allocated under `d` (extending `b_L(d)`) differs from every link allocated under `d'` (extending `b_L(d')`); same for content.

*Verifying invariants at Σ₅.* M0 holds: `d` and `d'` both satisfy `ValidAddress ∧ zeros = 2`. M1 holds: `{d} ⊆ {d, d'}`. C0/C1/C1b/C1c/C2/C-fin hold by frame on `C` (unchanged from `Σ₄`); in particular, C2 carries the prior content keys `a, a'` whose `origin = d ∈ dom(M₅)`, preserved by M1's extension. L0/L1/L1a/L1b/L1c/L3/L12/L-fin hold by frame on `L` (unchanged from `Σ₄`); L1a holds for `ℓ` since `origin(ℓ) = d ∈ dom(M₅)`. L14: `dom(C₅) ∩ dom(L₅) = {a, a'} ∩ {ℓ} = ∅` (verified by `E(a)₁ = E(a')₁ = s_C ≠ s_L = E(ℓ)₁`). ChainMembershipForOrigin transfers: `dom(C₅) ∩ {a'' : origin(a'') = d} = {a, a'} ⊆ A_C(d)` (per Steps 2 and 4); `dom(C₅) ∩ {a'' : origin(a'') = d'} = ∅ ⊆ A_C(d')` (vacuous, first emission still pending); similarly for `L`.

*Step 6 — `K.α(d', a'', v'')` (first content emission under `d'`).* Pinning the address from `Σ₅`: `{a''' ∈ dom(C₅) : origin(a''') = d'} = ∅` (the content keys `a, a'` have `origin = d ≠ d'`), so the first-emit branch fires with `a'' = [d'.0.s_C.1] = [1, 0, 2, 0, 5, 3, 0, 1, 1]` (length 9). The C1c chain `(t₀, t₁, t₂)`:
- `t₀ = d' = [1, 0, 2, 0, 5, 3]`
- `t₁ = inc(d', 2)`: T10a admits `k = 2` since `zeros(d') = 2 ≤ 2`; TA5(d) at `k = 2` appends `[0, 1]`, yielding `[1, 0, 2, 0, 5, 3, 0, 1] = b_C(d')` with `zeros = 3`, T4-valid.
- `t₂ = inc(b_C(d'), 1)`: TA5(d) at `k = 1` appends `1`, yielding `a'' = [1, 0, 2, 0, 5, 3, 0, 1, 1]`. `zeros(a'') = 3`, T4-valid, `#E(a'') = 2`.

Verifying preconditions: `a'' ∉ dom(C₅) ∪ dom(L₅) = {a, a', ℓ}`. *Cross-document freshness* against `{a, a'}` (both with `origin = d ≠ d'`): by Cross-document disjointness at Step 5, `b_C(d) ⋠ b_C(d') ∧ b_C(d') ⋠ b_C(d)`; `a, a'` extend `b_C(d)` (Steps 2, 4) while `a''` extends `b_C(d')`, so by T10, `a'' ≠ a` and `a'' ≠ a'`. *Sub-space freshness* against `ℓ`: `E(a'')₁ = 1 = s_C ≠ 2 = s_L = E(ℓ)₁` by L0 + SC-NEQ, so `a'' ≠ ℓ`. Other preconditions: `zeros(a'') = 3` ✓; `E(a'') = [1, 1]`, `E(a'')₁ = s_C` ✓; `#E(a'') = 2` ✓; `origin(a'') = N(a'').0.U(a'').0.D(a'') = [1].0.[2].0.[5, 3] = d'` ✓. (Freshness is also pinned directly by SubAllocatorAxiom.FirstEmission applied to `A_C(d')` — both routes are available; the derivation here exhibits the underlying mechanism.)

Effect: `C₆ = C₅ ∪ {a'' ↦ v''} = {a ↦ v, a' ↦ v', a'' ↦ v''}`; `L₆ = L₅`; `M₆ = M₅`. Invariants at `Σ₆`: C0 (existing values unchanged), C1 (`zeros(a'') = 3`), C1b (`#E(a'') = 2`), C1c (chain exhibited above), C2 (`origin(a'') = d' ∈ dom(M₆)`), C-fin (`|C₆| = 3 < ∞`); ChainMembershipForOrigin extends: `{a''} ⊆ A_C(d')` by FirstEmission.

*Step 7 — `K.λ(d', ℓ'', F'', G'', Θ'')` (first link emission under `d'`).* Pinning from `Σ₆`: `{ℓ''' ∈ dom(L₆) : origin(ℓ''') = d'} = ∅` (`origin(ℓ) = d ≠ d'`), so the first-emit branch fires with `ℓ'' = [d'.0.s_L.1] = [1, 0, 2, 0, 5, 3, 0, 2, 1]` (length 9). The L1c chain `(t₀, t₁, t₂, t₃)`:
- `t₀ = d'`
- `t₁ = inc(d', 2) = b_C(d')` (admissibility as in Step 6)
- `t₂ = inc(b_C(d'), 0) = [1, 0, 2, 0, 5, 3, 0, 2] = b_L(d')` (TA5(c) advances `sig(b_C(d')) = 8` from `s_C = 1` to `s_L = 2`; SubspaceConventionAxiom gives `s_L = s_C + 1`)
- `t₃ = inc(b_L(d'), 1) = ℓ''` (TA5(d) at `k = 1` appends `1`; `zeros(ℓ'') = 3`, T4-valid, `#E(ℓ'') = 2`)

Verifying preconditions: `ℓ'' ∉ dom(L₆) ∪ dom(C₆) = {ℓ, a, a', a''}`. *Cross-document freshness* against `{ℓ}` (origin = d ≠ d'): by Cross-document disjointness at Step 5, `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`; `ℓ` extends `b_L(d)` (Step 3) while `ℓ''` extends `b_L(d')`, so by T10, `ℓ'' ≠ ℓ`. *Sub-space freshness* against `{a, a', a''}`: each content address has `E(·)₁ = s_C = 1 ≠ 2 = s_L = E(ℓ'')₁`, so `ℓ'' ≠ a, a', a''`. Other preconditions: `zeros(ℓ'') = 3` ✓; `E(ℓ'') = [2, 1]`, `E(ℓ'')₁ = s_L` ✓; `#E(ℓ'') = 2` ✓; `origin(ℓ'') = d'` ✓.

Effect: `L₇ = L₆ ∪ {ℓ'' ↦ (F'', G'', Θ'')}`; `C₇ = C₆`; `M₇ = M₆`. Invariants at `Σ₇`: L0 (`E(ℓ'')₁ = s_L`), L1 (`zeros(ℓ'') = 3`), L1a (`origin(ℓ'') = d' ∈ dom(M₇)`), L1b (`#E(ℓ'') = 2`), L1c (chain exhibited above), L3 (triple endset with non-empty `Θ''`), L12 (existing link `ℓ ↦ (F, G, Θ)` unchanged), L14 (`dom(C₇) ∩ dom(L₇) = {a, a', a''} ∩ {ℓ, ℓ''} = ∅` by SC-NEQ), L-fin (`|L₇| = 2 < ∞`); ChainMembershipForOrigin extends: `{ℓ''} ⊆ A_L(d')` by FirstEmission, witnessing `n_{d'} = 1`.

*Step 8 — `K.λ(d, ℓ_new, F_new, G_new, Θ_new)` (second link emission under `d`, subsequent-emit branch).* Pinning the address from `Σ₇`: `{ℓ''' ∈ dom(L₇) : origin(ℓ''') = d} = {ℓ}` (note `origin(ℓ'') = d' ≠ d`), so the subsequent-emit branch fires with `ℓ_new = inc(max{ℓ}, 0) = inc(ℓ, 0)`. By ChainMembershipForOrigin's contiguous-prefix form at `Σ₇`, `dom(L₇) ∩ {ℓ''' : origin(ℓ''') = d} = {s₁}` with `ℓ = s₁`, so the lex-order max is `s₁` and `ℓ_new = s₂`. Since `sig(ℓ) = 8` with value `1`, TA5(c) gives `ℓ_new = [1, 0, 2, 0, 5, 0, 2, 2]`. The L1c chain extends `ℓ`'s chain by one step: `(t₀, t₁, t₂, t₃, t₄)` with `t₀ = d`, `t₁ = b_C(d)`, `t₂ = b_L(d)`, `t₃ = ℓ`, `t₄ = inc(ℓ, 0) = ℓ_new`. Admissibility of the new step: TA5(c) at `k = 0` is unconditionally T4-preserving.

Verifying preconditions: `ℓ_new ∉ dom(L₇) ∪ dom(C₇) = {ℓ, ℓ'', a, a', a''}`.
- *Within-chain freshness against `ℓ`:* by ChainMembershipForOrigin at `Σ₇`, `ℓ ∈ A_L(d)` at chain index 1. By SubAllocatorAxiom.ChainDiscipline, `ℓ_new = inc(ℓ, 0) ∈ A_L(d)` at chain index 2. T10a.7 (EnumerationInjectivity, applicability justified by the *T10a chain-lemma applicability* remark) gives `s₁ ≠ s₂`, i.e., `ℓ ≠ ℓ_new`. (Concrete check: `ℓ_new` differs from `ℓ` at position 8, where `ℓ[8] = 1 ≠ 2 = ℓ_new[8]`.)
- *Cross-document freshness against `ℓ''`:* (a) `ℓ_new = inc(ℓ, 0)` extends `b_L(d)` — by IH on ChainMembershipForOrigin at `Σ₇`, `ℓ ∈ A_L(d)`; by ChainPrefixExtension at `Σ₇`, `b_L(d) ≼ ℓ`; the step argument of ChainPrefixExtension (TA5(b)/(c) at `k = 0` preserving positions `1..#ℓ − 1 = 7` under TA5-SigValid pinning `sig(ℓ) = #ℓ = 8`) carries the prefix relation forward to `ℓ_new`, giving `b_L(d) ≼ ℓ_new` (concrete check: positions `1..7` of `ℓ_new = [1, 0, 2, 0, 5, 0, 2, 2]` are `[1, 0, 2, 0, 5, 0, 2] = b_L(d)`). (b) `ℓ'' ∈ A_L(d')` by ChainMembershipForOrigin at `Σ₇`, and `b_L(d') ≼ ℓ''` by ChainPrefixExtension. (c) Cross-document disjointness at `(d, d')` (verified in Step 5) gives `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`. T10 (PartitionIndependence, ASN-0034) closes: `ℓ_new ≠ ℓ''`.
- *Sub-space freshness against `{a, a', a''}`:* StoreT4Validity at `Σ₇` gives T4-validity of `a, a', a''`; `ℓ_new` is T4-valid by chain-element T4-validity (TA5a-propagation along `A_L(d)`'s chain from FirstEmission's T4-valid output). L0 supplies `E(·)₁ = s_C = 1` for content and `E(ℓ_new)₁ = s_L = 2` (preserved from `ℓ` by TA5(c) since position 7 of `ℓ_new` carries `2`); `zeros(ℓ_new) = zeros(a) = 3` by L1/C1. SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034) closes: `ℓ_new ≠ a, a', a''`.

Other preconditions: `zeros(ℓ_new) = 3` (T10a.8 — UniformSiblingZeroCount — preserved under `inc(·, 0)` per ChainDiscipline, anchored at FirstEmission's `zeros = 3`) ✓; `E(ℓ_new) = [2, 2]`, `E(ℓ_new)₁ = 2 = s_L` ✓; `#E(ℓ_new) = 2` ✓; `origin(ℓ_new) = d` (TA5(b) preserves positions `1..7`, including the document-level prefix and the field-separator structure that origin's truncation depends on) ✓.

Effect: `L₈ = L₇ ∪ {ℓ_new ↦ (F_new, G_new, Θ_new)} = {ℓ ↦ (F, G, Θ), ℓ'' ↦ (F'', G'', Θ''), ℓ_new ↦ (F_new, G_new, Θ_new)}`; `C₈ = C₇`; `M₈ = M₇`. Invariants at `Σ₈`: L0–L1c hold at the new key as verified above; L3 (triple endset, non-empty `Θ_new`) ✓; L12 (existing values `ℓ ↦ ·` and `ℓ'' ↦ ·` unchanged) ✓; L14 ✓; L-fin (`|L₈| = 3`) ✓. ChainMembershipForOrigin extends: `dom(L₈) ∩ {ℓ''' : origin(ℓ''') = d} = {ℓ, ℓ_new} = {s₁, s₂}` (contiguous prefix of `A_L(d)`, witnessing `n_d = 2`).

*Step 9 — `K.σ(d_alt)` (third document registration, prefix-incomparable with prior documents).* Fix `d_alt = [1, 0, 3, 0, 7]` — `#d_alt = 5`, with zeros at positions 2 and 4 (`zeros(d_alt) = 2`), no adjacent zeros (positions (2,3) = (0,3) and (4,5) = (0,7)), `d_alt[1] = 1 ≠ 0` and `d_alt[5] = 7 ≠ 0`, hence T4-valid. By T4b, `N(d_alt) = [1]`, `U(d_alt) = [3]`, `D(d_alt) = [7]`.

Verify `d_alt ∉ dom(M₈) = {d, d'}`. Compare with `d = [1, 0, 2, 0, 5]`: position 3 disagrees (`d[3] = 2 ≠ 3 = d_alt[3]`), so `d_alt ≠ d`. Compare with `d' = [1, 0, 2, 0, 5, 3]`: position 3 disagrees similarly, so `d_alt ≠ d'`. The other K.σ precondition `ValidAddress(d_alt) ∧ zeros(d_alt) = 2` ✓.

Effect: `dom(M₉) = {d, d', d_alt}`, with `M₉(d_alt) = ∅` and `M₉(d) = M₉(d') = ∅` unchanged. `C₉ = C₈`, `L₉ = L₈`. By SubAllocatorAxiom.Exists, `A_C(d_alt)` and `A_L(d_alt)` activate at `Σ₉`, alongside the already-active chains for `d` and `d'`.

*Verifying the Cross-document disjointness lemma at `Σ₉` for the prefix-incomparable pair `(d, d_alt)` — Case B sub-case B.i.* The document prefixes are prefix-incomparable: position 3 of `d = [1, 0, 2, 0, 5]` is `2`, position 3 of `d_alt = [1, 0, 3, 0, 7]` is `3`, both within native domains `{1, …, 5}`, so neither is a prefix of the other. Length comparison: `#d = 5 = #d_alt`, so NAT-order's trichotomy at `(#d, #d_alt)` selects sub-case **B.i** with `#d ≤ #d_alt` (equality holds; the argument fires symmetrically as B.ii via `d_alt ⋠ d`). The length conjunct `#d ≤ #d_alt` of `d ≼ d_alt` holds, so `d ⋠ d_alt` must be witnessed by failure of the component conjunct — at position `i = 3`, `d[3] = 2 ≠ 3 = d_alt[3]`. Take `k := 3`. Then `k = 3 ≤ 5 = #d = #d_alt = min(#d, #d_alt)` ✓, and `d[k] ≠ d_alt[k]` ✓.

Lift to the anchors `p₁ = b_L(d) = [1, 0, 2, 0, 5, 0, 2]` (length 7) and `p₂ = b_L(d_alt) = [1, 0, 3, 0, 7, 0, 2]` (length 7). From `#p_i = #d_i + 2`, NAT-addcompat's strict successor lifts `#d_i ≤ #p_i`, so `min(#d, #d_alt) = 5 ≤ 7 = min(#p₁, #p₂)`. The anchors are length-`+2` extensions agreeing with their documents at positions `1..#d_i`, so `p₁[3] = d[3] = 2 ≠ 3 = d_alt[3] = p₂[3]` at index `k = 3 ≤ min(#p₁, #p₂) = 7`. This witnesses `b_L(d) ⋠ b_L(d_alt) ∧ b_L(d_alt) ⋠ b_L(d)` via the position-divergence clause of Prefix (PrefixRelation, ASN-0034). The same divergence at position 3 holds for `b_C(d) = [1, 0, 2, 0, 5, 0, 1]` and `b_C(d_alt) = [1, 0, 3, 0, 7, 0, 1]`. By T10, every link (resp. content) allocated under `d_alt` differs from every link (resp. content) allocated under `d`.

A symmetric Case B argument applies to the pair `(d', d_alt)`: position-3 divergence between `d' = [1, 0, 2, 0, 5, 3]` and `d_alt = [1, 0, 3, 0, 7]` (`d'[3] = 2 ≠ 3 = d_alt[3]`). Length comparison: `#d' = 6 > 5 = #d_alt`, so sub-case **B.ii** fires (`#d_alt < #d'`); the witness is the same `k = 3`, lying within both native domains.

*Verifying invariants at `Σ₉`.* M0 holds at `d_alt`: precondition pins `ValidAddress(d_alt) ∧ zeros(d_alt) = 2`; M0 at the prior keys `d, d'` transfers by frame on those entries. M1: `{d, d'} ⊆ {d, d', d_alt}`. C0/C1/C1b/C1c/C2/C-fin hold by frame on `C`; C2 carries the prior content keys' origins `d` (for `a, a'`) and `d'` (for `a''`), all preserved by M1's extension. L0/L1/L1a/L1b/L1c/L3/L12/L-fin hold by frame on `L`; L1a carries `origin(ℓ) = origin(ℓ_new) = d` and `origin(ℓ'') = d'`, preserved by M1. L14: `dom(C₉) ∩ dom(L₉) = {a, a', a''} ∩ {ℓ, ℓ'', ℓ_new} = ∅` (verified by L0's `E(·)₁` partition and StoreT4Validity + T7). ChainMembershipForOrigin transfers at `Σ₉`: under `d`, content gives `{a, a'} = {t₁, t₂}` with `m_d = 2` and link gives `{ℓ, ℓ_new} = {s₁, s₂}` with `n_d = 2`; under `d'`, content gives `{a''} = {t₁}` with `m_{d'} = 1` and link gives `{ℓ''} = {s₁}` with `n_{d'} = 1`; under `d_alt`, both intersections are `∅` with `m_{d_alt} = n_{d_alt} = 0` (vacuous, first emissions under `d_alt` still pending). StoreT4Validity transfers by frame on `C` and `L` together with M1's monotonicity preserving the chain-membership witnesses.

The extended example confirms invariants M0, M1, C0–C2, C-fin, L0–L14, L-fin at each successor state across three documents, exercises both first-emit and subsequent-emit branches of K.α (Steps 2, 4, 6) and K.λ (Steps 3, 7, 8), verifies the Cross-document disjointness lemma in both Case A (prefix-comparable, Step 5 with `d ≼ d'`) and Case B (prefix-incomparable; sub-case B.i with `#d = #d_alt`, sub-case B.ii with `#d_alt < #d'`, Step 9), underwrites cross-document freshness at Steps 6, 7, and 8, and exhibits the ChainMembershipForOrigin lemma's contiguous-prefix postcondition together with the ChainPrefixExtension lemma at every emission past the first.


## Discharge of stated invariants

**Simultaneous-induction framing.** All stated invariants together with the ChainPrefixExtension lemma, the ChainMembershipForOrigin lemma, and the StoreT4Validity corollary are proved by *simultaneous induction* over transition sequences from `Σ₀`. The inductive hypothesis at each step is the *conjunction* of every stated invariant, lemma, and corollary at the current state `Σ`; the inductive step exhibits each holding at `Σ'` using the conjoined IH. No inductive step uses a conclusion derived in the same step. This framing is needed because ChainMembershipForOrigin's K.α/K.λ subsequent-emit cases consume C2/L1a as IH at `Σ`, while the discharge matrix's K.α/K.λ subsequent-emit freshness derivations consume ChainMembershipForOrigin, ChainPrefixExtension, and StoreT4Validity at `Σ`; the lemmas and the matrix invariants are mutually entangled and sound only under this simultaneous-induction discipline. The ChainPrefixExtension and ChainMembershipForOrigin proofs above (in the SubAllocatorAxiom section) record the corresponding per-transition discharges for those lemmas; StoreT4Validity transfers via frame at K.σ and via the per-step TA5a argument from FirstEmission's T4-valid first emission at K.α/K.λ.

Each invariant is discharged by induction on transition sequences from `Σ₀`. The inductive step is recorded as a per-(invariant, transition) matrix; entries describe how each transition kind preserves or discharges each invariant.

**Base case verification (at `Σ₀ = (∅, ∅, ∅)`).** Most invariants are vacuously satisfied: M0/M1/C1/C1b/C1c/C2/L0/L1/L1a/L1b/L1c/L3 quantify over `dom(C)`, `dom(L)`, or `dom(M)`, all empty at `Σ₀`. C0 and L12 quantify over transitions `Σ → Σ'`, vacuous at `Σ₀` until the first transition fires. Three invariants are non-vacuous but trivially satisfied at `Σ₀`:

- **L14** (`dom(C) ∩ dom(L) = ∅`): at `Σ₀`, both stores empty, so `∅ ∩ ∅ = ∅` — trivially true.
- **L-fin** (`|dom(L)| < ∞`): `|∅| = 0 < ∞` — trivially true.
- **C-fin** (`|dom(C)| < ∞`): `|∅| = 0 < ∞` — trivially true.

The base case holds.

**Inductive step.** Per (invariant, transition):

| Invariant | K.σ | K.α | K.λ |
|---|---|---|---|
| **M0** (DocumentTumblerWellFormed) | Discharged at new key: precondition pins `ValidAddress(d) ∧ zeros(d) = 2` | Preserved: `M` in frame | Preserved: `M` in frame |
| **M1** (ArrangementMonotonicity) | Discharged: effect extends `dom(M)` by union | Preserved: `M` in frame | Preserved: `M` in frame |
| **C0** (ContentImmutability) | Preserved: `C` in frame | Discharged: effect extends `dom(C)` at fresh `a` with value `v`; value at existing keys unaltered (definitional in effect clause) | Preserved: `C` in frame |
| **C1** (ContentElementLevel) | Preserved: `C` in frame | Discharged at new key: precondition pins `zeros(a) = 3` | Preserved: `C` in frame |
| **C1b** (ContentElementFieldDepth) | Preserved: `C` in frame | Discharged at new key: precondition pins `#E(a) ≥ 2` | Preserved: `C` in frame |
| **C1c** (ContentAllocatorConformance) | Preserved: `C` in frame | Discharged at new key via the structural inc-chain (see *C1c chain exhibition* below — first-emit and subsequent-emit cases) | Preserved: `C` in frame |
| **C2** (ContentScopedAllocation) | Preserved: vacuously (no new content); for prior keys `a ∈ dom(C)`, `origin(a) ∈ dom(M) ⊆ dom(M')` (`C` in frame, M1 extends `dom(M)`) | Discharged at new key: precondition pins `origin(a) = d ∧ d ∈ dom(M)`; preserved at prior keys (`origin(·)` is structural, M1 extends `dom(M)`) | Preserved: `C` in frame; prior keys preserved by M1 |
| **L0** (SubspacePartition) | Preserved: `L`, `C` in frame | Preserved on L-clause (`L` in frame); discharged at new key on C-clause via `E(a)₁ = s_C` precondition | Discharged at new key on L-clause via `E(ℓ)₁ = s_L` precondition; preserved on C-clause (`C` in frame) |
| **L1** (LinkElementLevel) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `zeros(ℓ) = 3` |
| **L1a** (LinkScopedAllocation) | Preserved: vacuously (no new link); for prior keys `ℓ ∈ dom(L)`, `origin(ℓ) ∈ dom(M) ⊆ dom(M')` (M1 extends `dom(M)`) | Preserved: `L` in frame; prior keys preserved by M1 | Discharged at new key: precondition pins `origin(ℓ) = d ∧ d ∈ dom(M)`; prior keys preserved by M1 |
| **L1b** (LinkElementFieldDepth) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `#E(ℓ) ≥ 2` |
| **L1c** (LinkAllocatorConformance) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key via the structural inc-chain (see *L1c chain exhibition* below — first-emit and subsequent-emit cases) |
| **L3** (NEndsetStructure) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `|L(ℓ)| ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` |
| **L12** (LinkImmutability) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: effect extends `dom(L)` at fresh `ℓ`; value at existing keys unaltered (definitional) |
| **L14** (StoreDisjointness) | Holds at Σ' by direct derivation: L0(Σ') + SC-NEQ + StoreT4Validity(Σ') + T7. L0 supplies `E(a)₁ = s_C` for `a ∈ dom(C)` and `E(ℓ)₁ = s_L` for `ℓ ∈ dom(L)`; SC-NEQ supplies `s_C ≠ s_L`; StoreT4Validity supplies T4-validity of every entry of `dom(C) ∪ dom(L)` (T7's precondition); C1/L1 supply `zeros(a) = zeros(ℓ) = 3`. T7 (FirstElementFieldDistinction, ASN-0034) closes: differing `E(·)₁` ⟹ `a ≠ ℓ`. All four premises hold at Σ' | Holds at Σ': same derivation | Holds at Σ': same derivation |
| **L-fin** (LinkStoreFiniteness) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: `|dom(L')| = |dom(L)| + 1`; finiteness closed under +1 |
| **C-fin** (ContentStoreFiniteness) | Preserved: `C` in frame | Discharged: `|dom(C')| = |dom(C)| + 1`; finiteness closed under +1 | Preserved: `C` in frame |

*C1c chain exhibition.* The substrate's C1c is "every content address has a structural inc-chain from its home document." For `K.α`'s discharge, two sub-cases:

**First-emit case** (`a = [d.0.s_C.1]`, predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`). The structural inc-chain witnessing C1c is two inc steps from `d`:

  `(t₀, t₁, t₂)` where `t₀ = d`, `t₁ = inc(d, 2) = b_C(d)`, `t₂ = inc(b_C(d), 1) = [d.0.s_C.1] = a`

Per-step admissibility:

- `t₁ = inc(d, 2)`: T10a admits `k = 2` when `zeros(spawnPt) ≤ 2`; by M0, `zeros(d) = 2`, satisfied. TA5(d) at `k = 2` yields `zeros(t₁) = 2 + (2 − 1) = 3` and `#t₁ = #d + 2`, T4-valid. The value at position `#d + 2` is `1 = s_C` (per SubspaceConventionAxiom), establishing `E(t₁)₁ = s_C` and `#E(t₁) = 1`.
- `t₂ = inc(b_C(d), 1)`: TA5(d) at `k = 1` has no zero-count side condition; the new component appended at position `#b_C(d) + 1` is `1`. `zeros(t₂) = 3 + 0 = 3` (k = 1 introduces no new zero), T4-valid, with `#E(t₂) = 2` and `E(t₂)₁ = s_C` inherited from `t₁` per TA5(b).

**Subsequent-emit case** (`a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`, predicate `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`). Let `a_prev = max{a' ∈ dom(C) : origin(a') = d}`. By the inductive hypothesis on C1c, `a_prev` has a structural inc-chain `(t₀, …, t_n)` with `t₀ = d` and `t_n = a_prev`. The chain for `a` extends this by one step: `(t₀, …, t_n, t_{n+1})` with `t_{n+1} = inc(t_n, 0) = inc(a_prev, 0) = a`. Per-step admissibility of the new step `t_{n+1} = inc(a_prev, 0)`: TA5(c) at `k = 0` is unconditionally T4-preserving; within-chain freshness against the rest of `A_C(d)`'s chain is discharged by T10a.7 (EnumerationInjectivity, applicability justified by the *T10a chain-lemma applicability* remark) applied to `(a_prev, a)`, with both indices established to inhabit `A_C(d)` by ChainMembershipForOrigin (`a_prev ∈ A_C(d)` from the inductive hypothesis applied at `Σ`) and SubAllocatorAxiom.ChainDiscipline's closure under `inc(·, 0)` (`a = inc(a_prev, 0) ∈ A_C(d)`); cross-document collisions with other documents' content chains are ruled out by the Cross-document disjointness lemma.

*L1c chain exhibition.* The substrate's L1c is "every link address has a structural inc-chain from its home document." For `K.λ`'s discharge, two sub-cases:

**First-emit case** (`ℓ = [d.0.s_L.1]`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`). The structural inc-chain witnessing L1c is three inc steps from `d`:

  `(t₀, t₁, t₂, t₃)` where `t₀ = d`, `t₁ = inc(d, 2) = b_C(d)`, `t₂ = inc(b_C(d), 0) = b_L(d)`, `t₃ = inc(b_L(d), 1) = [d.0.s_L.1] = ℓ`

Per-step admissibility:

- `t₁ = inc(d, 2)`: T10a admits `k = 2` when `zeros(spawnPt) ≤ 2`; by M0, `zeros(d) = 2`, satisfied. TA5(d) at `k = 2` yields `zeros(t₁) = 2 + (2 − 1) = 3`, T4-valid.
- `t₂ = inc(b_C(d), 0)`: TA5(c) at `k = 0` is unconditionally T4-preserving and length-preserving, with the sibling component advanced from `s_C` to `s_L`. By SubspaceConventionAxiom, `s_C = 1` and `s_L = 2`, so `inc([d.0.1], 0) = [d.0.2] = b_L(d)`. This step's correctness depends substantively on `s_L = s_C + 1`; the SubspaceConventionAxiom underwrites it.
- `t₃ = inc(b_L(d), 1)`: TA5(d) at `k = 1` has no zero-count side condition; `zeros(t₃) = 3 + 0 = 3` (k = 1 introduces no new zero), T4-valid, with `#E(t₃) = 2`.

Note that the C1c first-emit chain has *two* inc steps (`d → b_C(d) → a`) while the L1c first-emit chain has *three* (`d → b_C(d) → b_L(d) → ℓ`) — they are not parallel chains differing only in a single-step substitution. The link chain must traverse the additional `inc(b_C(d), 0) = b_L(d)` step because the link subspace anchor sits one sibling-component beyond the content subspace anchor.

**Subsequent-emit case** (`ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`). Let `ℓ_prev = max{ℓ' ∈ dom(L) : origin(ℓ') = d}`. By the inductive hypothesis on L1c, `ℓ_prev` has a structural inc-chain `(t₀, …, t_n)` with `t₀ = d` and `t_n = ℓ_prev`. The chain for `ℓ` extends this by one step: `(t₀, …, t_n, t_{n+1})` with `t_{n+1} = inc(t_n, 0) = inc(ℓ_prev, 0) = ℓ`. Per-step admissibility of the new step `t_{n+1} = inc(ℓ_prev, 0)`: TA5(c) at `k = 0` is unconditionally T4-preserving; within-chain freshness against the rest of `A_L(d)`'s chain is discharged by T10a.7 (EnumerationInjectivity, applicability justified by the *T10a chain-lemma applicability* remark) applied to `(ℓ_prev, ℓ)`, with both indices established to inhabit `A_L(d)` by ChainMembershipForOrigin (`ℓ_prev ∈ A_L(d)` from the inductive hypothesis applied at `Σ`) and SubAllocatorAxiom.ChainDiscipline's closure under `inc(·, 0)` (`ℓ = inc(ℓ_prev, 0) ∈ A_L(d)`); cross-document collisions with other documents' link chains are ruled out by the Cross-document disjointness lemma.


## Properties Introduced

| ID | Name | Status | Source |
|---|---|---|---|
| M0 | DocumentTumblerWellFormed | INV | Substrate, established at K.σ (precondition pins `ValidAddress(d) ∧ zeros(d) = 2` at the new key); preserved at K.α/K.λ by frame on `M` |
| M1 | ArrangementMonotonicity | INV | Substrate, established at K.σ by union extension `dom(M') = dom(M) ∪ {d}`; preserved at K.α/K.λ by frame on `M` |
| C0 | ContentImmutability | INV | Substrate, restated from ASN-0036's S0/S1; established at K.α (effect extends `dom(C)` with new pair and leaves existing values unchanged); preserved at K.σ/K.λ by frame on `C` |
| C1 | ContentElementLevel | INV | Substrate, restated from ASN-0036's S7b; established at K.α (precondition pins `zeros(a) = 3` at the new key); preserved at K.σ/K.λ by frame on `C` |
| C1b | ContentElementFieldDepth | INV | Substrate, restated from ASN-0036's S7c (content-side analog of L1b); established at K.α (precondition pins `#E(a) ≥ 2` at the new key); preserved at K.σ/K.λ by frame on `C` |
| C1c | ContentAllocatorConformance | INV | Substrate, content-side analog of L1c; established at K.α via the C1c chain exhibition (first-emit gap closed by SubAllocatorAxiom.FirstEmission, subsequent-emit by SubAllocatorAxiom.ChainDiscipline (T10a.7)); preserved at K.σ/K.λ by frame on `C` |
| C2 | ContentScopedAllocation | INV | Substrate, content-side analog of L1a; established at K.α (precondition pins `origin(a) = d ∧ d ∈ dom(M)` at the new key); preserved at K.σ/K.λ by frame on `C` and M1's monotonicity of `dom(M)` |
| L0 | SubspacePartition | INV | L-clause from ASN-0043; C-clause added here. Established at K.α (C-clause, via `E(a)₁ = s_C` precondition) and K.λ (L-clause, via `E(ℓ)₁ = s_L` precondition); preserved at K.σ by frame on both `C` and `L` |
| L1 | LinkElementLevel | INV | ASN-0043; established at K.λ (precondition pins `zeros(ℓ) = 3` at the new key); preserved at K.σ/K.α by frame on `L` |
| L1a | LinkScopedAllocation | INV | ASN-0043 (refactored: `E_doc` → `dom(M)`); established at K.λ (precondition pins `origin(ℓ) = d ∧ d ∈ dom(M)` at the new key); preserved at K.σ/K.α by frame on `L` and M1's monotonicity of `dom(M)` |
| L1b | LinkElementFieldDepth | INV | ASN-0043; established at K.λ (precondition pins `#E(ℓ) ≥ 2` at the new key); preserved at K.σ/K.α by frame on `L` |
| L1c | LinkAllocatorConformance | INV | Substrate commitment: per-step inc-rule conformance. Established at K.λ via the L1c chain exhibition (first-emit gap closed by SubAllocatorAxiom.FirstEmission, subsequent-emit by SubAllocatorAxiom.ChainDiscipline (T10a.7)); preserved at K.σ/K.α by frame on `L` |
| L3 | NEndsetStructure | INV | ASN-0043; established at K.λ (precondition pins `|L(ℓ)| ≥ 3 ∧ (e₃) ≠ ∅`); preserved at K.σ/K.α by frame on `L` |
| L12 | LinkImmutability | INV | ASN-0043; established at K.λ (effect extends `dom(L)` with new pair and leaves existing values unchanged); preserved at K.σ/K.α by frame on `L` |
| L14 | StoreDisjointness | INV (derived) | L0 + SC-NEQ + StoreT4Validity + T7 |
| L-fin | LinkStoreFiniteness | INV (derived) | Inductively from `Σ₀.L = ∅` + K.λ |
| C-fin | ContentStoreFiniteness | INV (derived) | Inductively from `Σ₀.C = ∅` + K.α |
| SubAllocatorAxiom | ContentLinkSubAllocatorExistence | AXIOM | Four clauses: Exists, Disjoint, FirstEmission, ChainDiscipline. Asserts T10a-discipline-satisfying chains (T10a.1, T10a.7, T10a.8) without claiming embedding in T10a's global allocator tree. Disjoint and FirstEmission's freshness conclusion are derivable from the remaining clauses (see *Remark — derivable clauses*); kept in the axiom for citation convenience. |
| ChainPrefixExtension | ChainPrefixExtension | LEMMA | Derived from SubAllocatorAxiom.FirstEmission (base case, concrete structural forms `[d.0.s_C.1]` and `[d.0.s_L.1]`) + SubAllocatorAxiom.ChainDiscipline + TA5(b)/(c) + TA5-SigValid + chain-element T4-validity (step case). Every chain element extends its anchor under Prefix: `b_C(d) ≼ t` for `t ∈ A_C(d)`, `b_L(d) ≼ t` for `t ∈ A_L(d)`. Consumed in cross-document freshness derivations (K.α/K.λ first-emit and subsequent-emit) and in the FirstEmission derivable-clauses Remark. |
| ChainMembershipForOrigin | ChainMembershipForOrigin | LEMMA | Inductive invariant in *contiguous-prefix form* at every reachable state: `dom(C) ∩ {a' : origin(a') = d} = {t₁, …, t_{m_d}}` is a contiguous initial segment of `A_C(d)` (mirror for `L`). The subset inclusion `dom(C) ∩ {a' : origin(a') = d} ⊆ A_C(d)` is the weaker corollary. Proved by induction over transitions using SubAllocatorAxiom.FirstEmission (first-emit branches placing `t₁`) and ChainDiscipline + T10a.7 (subsequent-emit branches placing `t_{m_d + 1} = inc(t_{m_d}, 0)`). Licenses application of T10a.7 to `(a_prev, a)` and `(ℓ_prev, ℓ)` in K.α/K.λ subsequent-emit cases; the contiguous-prefix form matches ASN-0040's B1 (ContiguousPrefix). |
| StoreT4Validity | StoreT4Validity | LEMMA (derived) | Derived from ChainMembershipForOrigin + chain-element T4-validity (FirstEmission's T4-valid first emission + TA5a per-step under `k = 0` unconditional preservation, propagated along `A_C(d)` and `A_L(d)`'s chains). Every entry of `dom(C) ∪ dom(L)` is T4-valid. Used to discharge T7's precondition in the L14 derivation and in the FirstEmission derivable-clauses Remark against `dom(L)`. |
| Cross-doc disjointness | T10 + Prefix + M0 lemma | LEMMA | Derived from M0 + T4 + T10 + Prefix (ASN-0034); T4's zero-count argument underwrites the Case A divergence step. Case B (prefix-incomparable) extracts a position-divergence witness `k ≤ min(#d₁, #d₂)` by sub-case analysis on length (B.i: `#d₁ ≤ #d₂`; B.ii: `#d₂ < #d₁`), since the joint `⋠`-conjunction can be satisfied by length alone on one side in asymmetric-length sub-cases. The lemma operates directly at document-level anchors (T4-validity + zeros = 2) rather than through T10a.2/T10a.5, because the sub-allocator-pair disjointness it establishes is between document-level prefixes, not between sub-allocator allocation events. |
| SubspaceConventionAxiom | FixedSubspaceIdentifiers | AXIOM | Substrate commitment: `s_C = 1 ∧ s_L = 2`; pinned by Nelson (LM 4/30–4/31) and Gregory (`xanadu.h:144–146`, `granf2.c:162`, `do2.c:94`). Underwrites L14 derivation and the L1c chain exhibition. |
| SequentialTransitionAxiom | SequentialAtomicTransitions | AXIOM | Substrate commitment: `Σ → Σ'` is atomic, uninterruptible, totally ordered. |
| K.σ | DocumentRegistration | OP | Substrate-level document introduction into `dom(M)` |
| K.α | ContentAllocation | OP | Substrate-level content emission |
| K.λ | LinkAllocation | OP | Substrate-level link emission |


## Open Questions

- *Link withdrawal.* The substrate admits no withdrawal of `dom(L)` entries (L12 enforces immutability). Nelson's tombstone-style withdrawal (LM 4/9) is not expressible at this layer. Closing the gap is deferred to a higher-layer ASN that may extend the substrate with an explicit retraction mechanism — e.g., a future tombstoning ASN.

- *Higher-arity link discipline.* L3 admits arbitrary `N ≥ 3` (matching ASN-0043's foundation form). The substrate enforces no upper bound on arity and no constraints on the semantics of slots beyond the type endset at slot 3. Higher-layer ASNs may impose further constraints on arity, slot interpretation, or relations between slots if needed for specific link semantics — for example, a layer that fixes the StandardTriple convention as a structural commitment rather than a notational default.

- *Document address discipline.* K.σ's precondition is structural-only (`ValidAddress(d) ∧ zeros(d) = 2 ∧ d ∉ dom(M)`). The substrate admits any T4-valid document-level tumbler. Nelson's hierarchical baptism (where node-account-document chains are enforced) is a higher-layer commitment; a higher-layer document-introduction primitive tightens K.σ's precondition with the additional discipline.

- *Concurrency.* `K.σ`, `K.α`, and `K.λ` are stated as atomic transitions; the discipline for concurrent emission across multiple allocators is not addressed at this layer.

- *Sub-allocator stratification beyond `A_C(d)` and `A_L(d)`.* Future subspace identifiers `s ≥ 3` would require parallel sub-allocators; the present axiom commits to exactly two (content and link).

- *Arrangement extension primitives.* The substrate fixes `M(d) = ∅` at K.σ-time and never re-modifies. Higher-layer arrangement-extension primitives extend arrangements; downstream ASNs needing arrangement mutation depend on those higher-layer primitives.
