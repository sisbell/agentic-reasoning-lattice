# ASN-0093: Allocation Substrate

A Xanadu-style substrate maintains three address-keyed stores: the content store, the link store, and the document-arrangement function. Each store is grown by an allocation primitive that extends the store's domain at a fresh key with structural invariants on the new entry. ASN-0043 introduced the link store and its structural invariants (L0/L1/L1a/L1b/L1c/L3/L12/L14), all of which the substrate restates verbatim (modulo the `E_doc` → `dom(M)` notational substitution at L1a); ASN-0036 introduced the content store and arrangement function. Higher-layer transition models fold both into a larger state model that also tracks entity allocation and arrangement provenance — `Σ = (C, L, E, M, R)` — and supply the operational primitives for the full state.

This note extracts the *allocation-substrate* layer: the three allocation primitives (K.σ, K.α, K.λ) and the structural invariants on `(Σ.C, Σ.L, Σ.M)` they preserve. The substrate requires no commitment to `Σ.E` (the entity set) or `Σ.R` (the provenance relation). Downstream ASNs that reason about address allocation into the three stores without lifting the entity/provenance layer can depend on this note directly, without inheriting the additional state components or their associated invariants. Higher-layer concerns — arrangement mutation, entity stratification, provenance recording — are deferred to higher-layer ASNs that compose this substrate's primitives with additional disciplines.

The factoring is downward from a fuller transition model: every operation and invariant here is identical to its counterpart in the fuller model except for one notational substitution — `E_doc` (the set of entities classified `IsDocument`) is replaced by `dom(M)` (the set of allocated documents in the arrangement function), so the substrate-layer claims can be stated without reference to the entity set.


## Scope

Downstream ASNs that operate on the link store without needing arrangement mutation, entity stratification, or provenance recording can cite this substrate directly. Downstream ASNs that need any of the deferred machinery cite a higher-layer transition model that itself depends on this substrate.

**Provided.** Three primitive operations and the structural invariants on `(C, L, M)` they preserve:

- **Operations:** `K.σ` (document registration), `K.α` (content allocation), `K.λ` (link allocation)
- **Invariants:** M0–M1 (arrangement-function shape), C0–C1c + C2 + C-fin (content store), L0–L14 + L-fin (link store)
- **Definition:** T10a-discipline-satisfying chain (structural-only — FirstElementValidity + SiblingRecurrence)
- **Chain lemmas:** ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension (derived from the structural Definition + foundation claims)
- **Transition-indexed lemmas:** ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness (proved by simultaneous induction with the stated invariants), Cross-document disjointness (T10 + Prefix + M0)
- **Axiom:** SubAllocatorAxiom (three clauses: Exists, FirstEmission structural form, ChainDiscipline)

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

**C1c (ContentAllocatorConformance).** Every content address `a ∈ dom(C)` has a structural inc-chain from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `n ≥ 1`, `t₀ = origin(a)`, and `tₙ = a`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` zero-count side condition); additionally, `k₁ = 2` (the first step is a depth-2 increment off the document seed) and `(A i : 1 ≤ i ≤ n : #tᵢ > #origin(a))` (every intermediate length strictly exceeds the seed's). The chain witnesses `a`'s structural producibility from its home document via the content sub-allocator chain. This is the content-side analog of L1c, stated in parallel form. The bootstrap gap (no T10a-tracked allocator domain for the anchor traversal and first emission) is closed by SubAllocatorAxiom.FirstEmission for the content sub-allocator chain; subsequent emissions inherit ChainEnumerationInjectivity via SubAllocatorAxiom.ChainDiscipline.

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

**L1c (LinkAllocatorConformance).** Every link address `ℓ ∈ dom(L)` has a *structural inc-chain* from its home document to `ℓ`: a finite sequence `(t₀, t₁, …, tₙ)` with `n ≥ 1`, `t₀ = origin(ℓ)`, and `tₙ = ℓ`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` zero-count side condition); additionally, `k₁ = 2` (the first step is a depth-2 increment off the document seed) and `(A i : 1 ≤ i ≤ n : #tᵢ > #origin(ℓ))` (every intermediate length strictly exceeds the seed's). The chain witnesses `ℓ`'s structural producibility from its home document via the link sub-allocator. This is ASN-0043's L1c restated for the substrate; the `k₁ = 2` and length-increasing clauses are preserved verbatim from the foundation form, not weakened. The L1c chain exhibition below establishes all clauses of this strengthened form at every K.λ event.

**Terminological note.** The substrate uses *structural inc-chain* as the nomenclature for what ASN-0043's L1c calls a *T10a-conforming step sequence*; the rename is purely terminological and the per-step admissibility content is identical. Both terms denote a sequence whose every step satisfies the per-step T10a admissibility envelope (TA5a's `k ∈ {0, 1, 2}` clauses with the `k = 2 ⟹ zeros ≤ 2` side condition) — neither commits the chain to be embedded in a global T10a allocator tree, since the substrate elsewhere disclaims tree embedding for the bootstrap traversal and first emission. The same terminological note applies to C1c's chain on the content side.

The substrate states L1c in its per-step inc-rule form — not as the stronger "every intermediate `tᵢ` inhabits a T10a-tracked allocator's domain at the state of emission." The strong form fails for the anchor traversal and the first emission, which inhabit no T10a-tracked allocator domain at the moment of allocation; SubAllocatorAxiom.FirstEmission (below) closes the bootstrap gap by licensing the first emission directly, and SubAllocatorAxiom.ChainDiscipline carries subsequent emissions onto the sub-allocator's `inc(·, 0)` chain. (Note that "per-step inc-rule form" here refers only to the contrast between *per-step admissibility* and *allocator-domain membership*; the foundation clauses `k₁ = 2` and `#tᵢ > #origin(ℓ)` are retained.)

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

**Active sub-allocator chains.** Define: a sub-allocator chain `A_C(d)` (resp. `A_L(d)`) is *active at state* `Σ` iff `d ∈ dom(M)` at `Σ`. Concretely, "active" is the predicate under which K.α (resp. K.λ) admits the chain as the emission source for an address with `origin(·) = d`: the operation's precondition requires `d ∈ dom(M)`, which is exactly the activation condition. Across-state permanence — once a sub-allocator chain is activated it remains active at every successor state — is not part of this definition; it is a *consequence* of M1 (ArrangementMonotonicity, established by the simultaneous induction described below) once M1 is in scope. The per-state activation condition stated here is the load-bearing notion; the across-state corollary is derived rather than postulated.

**Definition (T10a-discipline-satisfying chain).** A *T10a-discipline-satisfying chain* is an *infinite* sequence `(t_1, t_2, t_3, …)` of tumblers — indexed by every `n ∈ ℕ` with `n ≥ 1` — satisfying two structural conditions, both stated without reference to allocator-tree membership or spawning triples:

  (i) *FirstElementValidity:* `t_1` is T4-valid.
  (ii) *SiblingRecurrence:* `t_{n+1} = inc(t_n, 0)` for every `n ≥ 1`.

The infinity commitment is load-bearing: the substrate's chain lemmas conclude universally over `n ≥ 1` and K.α/K.λ admit unbounded subsequent emissions (B9-style unboundedness from ASN-0040 carries to the content and link sub-allocator chains), so the conceptual chain must furnish a chain element at every index — including those past any finite truncation point — for the lemmas to be applicable at the emission rule's pinning step. A finite truncation at length `k` would leave the universals' conclusions vacuous at indices `> k` and would leave K.α/K.λ's `(k+1)`-st subsequent-emit without a chain element to inhabit at chain index `k + 1`.

**Caveat on terminology.** The term *T10a-discipline-satisfying chain* is the substrate's name for a sequence satisfying only the two structural conditions above — a deliberate weakening of T10a's (AllocatorDiscipline, ASN-0034) full hypothesis. T10a additionally requires allocator-tree embedding via spawning triples `(parent(A), spawnPt(A), spawnParam(A))`, the `k' ∈ {1, 2}` child-spawning rule, the at-most-once `(t, k')` constraint, and an explicit allocator-tree structure; none of these are asserted by this Definition. The substrate elsewhere disclaims allocator-tree embedding ("makes no commitment about whether an implementation realises [these] as standalone T10a allocators..."), and the chain lemmas below cite only foundation claims whose preconditions are discharged by the Definition's two clauses — not by T10a's full discipline. A reader should not conclude from the name that a *T10a-discipline-satisfying chain* satisfies T10a; only the structural fragment is asserted.

The definition is purely structural. The lemmas ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, and ChainUniformZeroCount below — each cast against the Definition's structural preconditions alone — establish the per-chain disciplines (T4-validity propagation, uniform length, enumeration injectivity, uniform zero count) for every such chain, without invoking T10a's tree-embedding hypothesis or its cross-allocator results (T10a.5/T10a.6). Each lemma's proof mirrors the structure of its counterpart in ASN-0034 (T10a.1, T10a.7, T10a.8) but cites only foundation claims whose preconditions are discharged directly by the Definition; in particular, the chain-wide T4-validity needed by ChainUniformZeroCount is supplied locally by ChainElementT4Validity rather than by T10a.4 (T4PreservationUnderDiscipline, ASN-0034), whose proof inducts on allocator tree depth and requires tree embedding. The substrate uses this terminology to mark chains that satisfy these structural conditions while making no commitment about whether an implementation realises them as standalone T10a allocators with spawning triples or as discipline-conforming chains within a flatter structure.

**SubAllocatorAxiom (Axiom, ContentLinkSubAllocatorExistence).** For each `d ∈ dom(M)`, two sub-allocator chains are simultaneously activated under `d` at the moment of `d`'s registration into `dom(M)` (by `K.σ`). The substrate commits the chains to be *T10a-discipline-satisfying chains* (per the Definition above), without claiming that `A_C(d)` and `A_L(d)` are embedded in T10a's global allocator tree. Three clauses, independently citable as discharge premises:

- *Existence (SubAllocatorAxiom.Exists).* For every `d ∈ dom(M)`, the content sub-allocator chain `A_C(d)` (anchored at `b_C(d)`) and the link sub-allocator chain `A_L(d)` (anchored at `b_L(d)`) are active (per the *Active sub-allocator chains* definition above). The axiom commits *activation at every `Σ` in which `d ∈ dom(M)`* — it does not directly assert "once active, always active." The permanence reading (sub-allocator chains remain active at every successor state once `d` enters `dom(M)`) follows as a *consequence*, not as additional axiom content: it is the composition of this axiom with M1 (ArrangementMonotonicity, which is a substrate-level invariant established by simultaneous induction with the other transition-indexed invariants — see the *Simultaneous-induction framing* paragraph). At every `Σ` reachable from `Σ₀`, M1 supplies `d ∈ dom(M(Σ_init)) ⟹ d ∈ dom(M(Σ))` for every K.σ-introducing pre-state `Σ_init`, and the axiom then licenses activation of `A_C(d)` and `A_L(d)` at `Σ`. The axiom itself is a per-state existence statement; the across-state permanence is M1's contribution.

- *First emission structural form (SubAllocatorAxiom.FirstEmission).* The first emission of each chain has a concrete structural form:
  - *Content chain first-emit:* the first address produced by `A_C(d)` is `t_1^C(d) := [d.0.s_C.1]` — `E(·)₁ = s_C`, `origin(·) = d`, `#E(·) = 2`, `zeros(·) = 3`, and T4-valid by direct inspection given M0's T4-valid `d` (its components reproduce `d`'s positive boundary and zero-count structure with one zero separator added at position `#d + 1` and two positive components `s_C` and `1` at positions `#d + 2, #d + 3`, satisfying T4's no-adjacent-zeros, positive-endpoint, and `zeros = 3 ≤ 3` conjuncts).
  - *Link chain first-emit:* the first address produced by `A_L(d)` is `t_1^L(d) := [d.0.s_L.1]` — structurally analogous (with `s_L` in place of `s_C`); T4-valid by the same inspection.

  This clause carries only the structural form of the first emission. The freshness commitment `a ∉ dom(C) ∪ dom(L)` (resp. `ℓ ∉ dom(L) ∪ dom(C)`) at the K.α (resp. K.λ) event is *not* axiom content; it is restated as the derived lemma FirstEmissionFreshness below.

- *Chain discipline (SubAllocatorAxiom.ChainDiscipline).* Each chain `A_C(d)` (resp. `A_L(d)`) is a T10a-discipline-satisfying chain (per the Definition above), rooted at FirstEmission's `t_1^C(d)` (resp. `t_1^L(d)`). The two structural conditions are discharged thus: FirstElementValidity by FirstEmission (T4-validity established above by inspection); SiblingRecurrence by axiom (`t_{n+1} = inc(t_n, 0)`). The substrate makes no commitment about whether an implementation realises `A_C(d)`/`A_L(d)` as standalone T10a allocators or as discipline-conforming chains within a flatter allocator structure; only the structural Definition is asserted, and the four chain lemmas below derive the per-chain disciplines from it.

The substrate's freshness obligations decompose as: (i) within-chain freshness from ChainEnumerationInjectivity (below); (ii) cross-document freshness from the Cross-document disjointness lemma (later in this note); (iii) cross-subspace freshness from L14 / L0 + SC-NEQ + T7 plus StoreT4Validity. Together these cover the full sub-allocator chain lifecycle from activation through arbitrary emission.

*Earlier-draft note.* Two clauses present in earlier drafts — *Disjointness* (`A_C(d)` and `A_L(d)` produce addresses with `E(·)₁ = s_C` and `s_L` respectively) and *FirstEmission's freshness conclusion* — are not axiom content. They are restated as derived lemmas DisjointSubAllocatorChains and FirstEmissionFreshness below, respectively.

**Dependency ordering of the chain lemmas.** The six chain lemmas below are presented — and *proved* — in a fixed dependency order:

  ChainElementT4Validity → ChainUniformLength → ChainEnumerationInjectivity → ChainUniformZeroCount → DisjointSubAllocatorChains → ChainPrefixExtension

This ordering is load-bearing: each lemma's proof is permitted to cite the conclusions of all earlier lemmas in the list as fully established facts at every chain index `n ≥ 1`, but not the conclusions of any later lemma. Because each lemma proceeds by induction on the same chain-index variable `n`, an out-of-order citation would amount to a nested induction at the inductive step — i.e., re-proving an earlier lemma's full conclusion inside the step of a later one. By proving in dependency order and citing only prior lemmas, every inductive step consumes its premises as standalone prior facts (already universally quantified over all chain indices), not as parallel induction hypotheses. In particular:

- ChainElementT4Validity stands alone (no chain-lemma dependencies; cites only FirstElementValidity from the Definition and TA5a from ASN-0034 foundation).
- ChainUniformLength stands alone (cites only SiblingRecurrence and TA5(c) foundation; no T4-validity required).
- ChainEnumerationInjectivity stands alone (cites only SiblingRecurrence, TA5(a), T1(a)/T1(c) foundation; no T4-validity required).
- ChainUniformZeroCount cites ChainElementT4Validity at its step (for `t_n`'s T4-validity, supplying TA5-SigValid's precondition).
- DisjointSubAllocatorChains cites ChainElementT4Validity (chain-element T4-validity feeding TA5-SigValid) and ChainUniformLength (uniform length pinning `sig(t_n) = #d + 3` at every index).
- ChainPrefixExtension cites ChainElementT4Validity (for `t_n`'s T4-validity at the step) and ChainUniformLength (for `#t_n = #d + 3` at the step) — both as established prior facts, not via nested induction.

The substrate's transition-indexed proofs (ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, and the discharge matrix entries) are free to cite any of the six chain lemmas without restriction, because by the time those transition-indexed inductions fire, all six chain lemmas hold once-and-for-all on every T10a-discipline-satisfying chain.

**Lemma (ChainElementT4Validity).** Every element of a T10a-discipline-satisfying chain is T4-valid:

  `(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A n ≥ 1 :: t_n is T4-valid))`

*Proof.* Induction on chain index `n`.

*Base (n = 1).* FirstElementValidity (Definition (i)) supplies T4-validity of `t_1` directly.

*Step (n + 1).* Assume `t_n` is T4-valid. By SiblingRecurrence (Definition (ii)), `t_{n+1} = inc(t_n, 0)`. TA5a (IncrementPreservesT4, ASN-0034) applies at `k = 0` unconditionally (no zero-count side condition); the inductive hypothesis discharges TA5a's "input is T4-valid" precondition. Hence `t_{n+1}` is T4-valid. ∎

*Corollary (sub-allocator chains).* By SubAllocatorAxiom.ChainDiscipline, `A_C(d)` and `A_L(d)` are T10a-discipline-satisfying chains; hence every element of `A_C(d)` (resp. `A_L(d)`) is T4-valid. This corollary is consumed at every downstream site that previously appealed to the "T10a chain-lemma applicability" remark for chain-element T4-validity (ChainUniformZeroCount's step, ChainPrefixExtension's step, DisjointSubAllocatorChains, StoreT4Validity, FirstEmissionFreshness, and the K.α/K.λ subsequent-emit cross-subspace freshness derivations).

**Lemma (ChainUniformLength).** All elements of a T10a-discipline-satisfying chain share the length of `t_1`:

  `(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A n ≥ 1 :: #t_n = #t_1))`

*Proof.* Induction on `n`. *Base:* `#t_1 = #t_1` trivially. *Step:* assume `#t_n = #t_1`. By SiblingRecurrence, `t_{n+1} = inc(t_n, 0)`; by TA5(c), `#inc(t_n, 0) = #t_n`. Chaining: `#t_{n+1} = #t_n = #t_1`. ∎

The proof mirrors T10a.1 (UniformSiblingLength, ASN-0034) but is stated against the structural Definition's preconditions alone; no T4-validity is required, so ChainElementT4Validity is not consumed here.

*Corollary (sub-allocator chains).* For each `d ∈ dom(M)`, all elements of `A_C(d)` (resp. `A_L(d)`) have length `#d + 3` (since `t_1^C(d) = [d.0.s_C.1]` has length `#d + 3`, and analogously for `t_1^L(d)`).

**Lemma (ChainEnumerationInjectivity).** The enumeration of a T10a-discipline-satisfying chain is strictly increasing under T1:

  `(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A m, n ≥ 1 : m < n : t_m < t_n))`

In particular, `n ↦ t_n` is injective on chain indices: distinct chain indices map to distinct chain elements.

*Proof.* By SiblingRecurrence, `t_{k+1} = inc(t_k, 0)` for every `k ≥ 1`; by TA5(a), `inc(t_k, 0) > t_k`, so `t_k < t_{k+1}` at consecutive indices. T1(c) (transitivity of `<`) chains these for `m < n`: `t_m < t_{m+1} < … < t_n`, hence `t_m < t_n`. Injectivity follows from T1(a) (irreflexivity): if `t_m = t_n` with `m ≠ n`, WLOG `m < n` yields `t_m < t_m`, contradicting irreflexivity. The argument invokes TA5(a), T1(a), T1(c), and SiblingRecurrence alone — no T4-validity is required. ∎

The proof mirrors T10a.7 (EnumerationInjectivity, ASN-0034) but is stated against the structural Definition's preconditions alone.

*Corollary (within-chain freshness).* For each `d ∈ dom(M)` and each pair of distinct chain indices `m ≠ n` on `A_C(d)` (resp. `A_L(d)`), the two chain elements are distinct as tumblers; moreover the chain enumeration is order-preserving in both directions (`m < n ⟺ t_m < t_n`). This corollary discharges the substrate's within-chain freshness obligations at K.α and K.λ subsequent-emit branches.

**Lemma (ChainUniformZeroCount).** All elements of a T10a-discipline-satisfying chain share the zero count of `t_1`:

  `(A chain (t_1, t_2, t_3, …) satisfying FirstElementValidity ∧ SiblingRecurrence : (A n ≥ 1 :: zeros(t_n) = zeros(t_1)))`

*Proof.* Induction on `n`. *Base:* `zeros(t_1) = zeros(t_1)` trivially.

*Step:* Assume `zeros(t_n) = zeros(t_1)`. By ChainElementT4Validity, `t_n` is T4-valid; TA5-SigValid (SigOnValidAddresses, ASN-0034) then gives `sig(t_n) = #t_n`. By SiblingRecurrence, `t_{n+1} = inc(t_n, 0)`. TA5(b)'s `k = 0` clause supplies positional agreement at positions `1..#t_n` *except at* `sig(t_n)` — i.e., `(A i : 1 ≤ i ≤ #t_n ∧ i ≠ sig(t_n) : (t_{n+1})_i = (t_n)_i)`. TA5(c) then completes the modification at the excluded position: `sig(t_n) = #t_n`, length is preserved (`#t_{n+1} = #t_n`), and the value at `#t_n` advances from `(t_n)_{#t_n}` to `(t_n)_{#t_n} + 1`. By T4's positive-endpoint clause applied to T4-valid `t_n`, `(t_n)_{#t_n} ≥ 1`, so `(t_n)_{#t_n} + 1 ≥ 2 > 0`: the modified position remains non-zero, and equivalently was non-zero before. Combining the two clauses, the zero-index set is unchanged: at positions other than `#t_n` agreement holds by TA5(b) at `k = 0`, and at position `#t_n` both pre- and post-images are non-zero, so neither contributes. Hence `{i : 1 ≤ i ≤ #t_{n+1} ∧ (t_{n+1})_i = 0} = {i : 1 ≤ i ≤ #t_n ∧ (t_n)_i = 0}` and `zeros(t_{n+1}) = zeros(t_n) = zeros(t_1)`. ∎

The proof mirrors T10a.8 (UniformSiblingZeroCount, ASN-0034) but cites ChainElementT4Validity at the step (rather than T10a.4) — substituting the structural T4-validity derivation for the tree-embedding-based one. T10a.8's other dependencies (TA5(b)/(c), TA5-SigValid, T4, NAT-zero/discrete/order, NAT-closure, NAT-addcompat) are foundation claims that this proof consumes directly.

*Corollary (sub-allocator chains).* For each `d ∈ dom(M)`, every element of `A_C(d)` (resp. `A_L(d)`) has `zeros = 3` (since `t_1^C(d) = [d.0.s_C.1]` and `t_1^L(d) = [d.0.s_L.1]` both have `zeros = 3` by FirstEmission).

**Lemma (DisjointSubAllocatorChains).** Addresses produced by `A_C(d)` satisfy `E(·)₁ = s_C`; addresses produced by `A_L(d)` satisfy `E(·)₁ = s_L`. Hence by SC-NEQ (`s_C ≠ s_L`), no address is produced by both chains.

*Proof.* By SubAllocatorAxiom.FirstEmission, the first emission `t_1^C(d) = [d.0.s_C.1]` of `A_C(d)` has `E(·)₁ = s_C` at position `#d + 2`; the first emission `t_1^L(d) = [d.0.s_L.1]` of `A_L(d)` has `E(·)₁ = s_L` at position `#d + 2`. The first emission has length `#d + 3`. By ChainUniformLength, all elements of `A_C(d)` (resp. `A_L(d)`) have length `#d + 3`. By ChainElementT4Validity, every chain element is T4-valid; TA5-SigValid gives `sig(t_n) = #t_n = #d + 3` at every chain index `n`. By SiblingRecurrence, each step `t_{n+1} = inc(t_n, 0)` modifies only position `sig(t_n) = #d + 3` (TA5(c)'s single-position-modification clause); position `#d + 2` is preserved (TA5(b) gives positional agreement at positions `1..#t_n`). Hence every element of `A_C(d)` inherits `E₁ = s_C` from `t_1^C(d)`, and every element of `A_L(d)` inherits `E₁ = s_L` from `t_1^L(d)`. SC-NEQ then forces the two chains' images to be disjoint. ∎

**Lemma (ChainPrefixExtension).** At every reachable state `Σ`, every element of an active sub-allocator chain extends its anchor under the prefix relation:

  `(A d ∈ dom(M), t ∈ A_C(d) :: b_C(d) ≼ t)`
  `(A d ∈ dom(M), t ∈ A_L(d) :: b_L(d) ≼ t)`

*Quantifier scope.* `A_C(d)` and `A_L(d)` here denote the *conceptual* chains supplied by SubAllocatorAxiom.ChainDiscipline — the full `inc(·, 0)`-extension sequences `(t_1, t_2, t_3, …)` anchored at FirstEmission's first element — not the (proper) subsets of these chains realised in `dom(C)` (resp. `dom(L)`) at `Σ`. Equivalently, the conclusion holds for every `t = t_n` at every chain index `n ≥ 1`, *including chain elements not yet committed to `dom(C)` or `dom(L)` in any state*. The K.α and K.λ subsequent-emit derivations exploit this scope by citing the lemma directly at a freshly emitted address `a` (resp. `ℓ`) — which inhabits the conceptual chain by ChainDiscipline's closure under `inc(·, 0)` applied to `a_prev` (resp. `ℓ_prev`) — *before* `a` (resp. `ℓ`) is committed to `dom(C)` (resp. `dom(L)`).

*Proof.* Direct induction over each chain's enumeration `(t_1, t_2, t_3, …)` with `t_1` the first emission and `t_{n+1} = inc(t_n, 0)`.

*Base (chain index 1).* By SubAllocatorAxiom.FirstEmission, the content chain's first emission is the concrete form `[d.0.s_C.1]`, which is `b_C(d) = [d.0.s_C]` (length `#d + 2`) extended by the single component `1` at the new last position (length `#d + 3`). Componentwise, `[d.0.s_C.1]` agrees with `b_C(d)` at positions `1..#d + 2`, and the length condition `#b_C(d) = #d + 2 ≤ #d + 3 = #[d.0.s_C.1]` holds. By Prefix (PrefixRelation, ASN-0034), `b_C(d) ≼ [d.0.s_C.1]`. The link case is symmetric: `[d.0.s_L.1]` extends `b_L(d) = [d.0.s_L]` by `1` to length `#d + 3`, so `b_L(d) ≼ [d.0.s_L.1]`.

*Step (chain index `n + 1`).* Assume `b_C(d) ≼ t_n` for `t_n ∈ A_C(d)`. The next element is `t_{n + 1} = inc(t_n, 0)`. By ChainUniformLength (corollary on sub-allocator chains), `#t_n = #d + 3`. By ChainElementT4Validity (corollary on sub-allocator chains), `t_n` is T4-valid — supplied as a standalone fact established by a prior chain induction, not by a nested induction inside the present proof. TA5-SigValid (SigOnValidAddresses, ASN-0034) then pins `sig(t_n) = #t_n = #d + 3`. TA5(c) gives `#t_{n + 1} = #t_n` and confines the modification to position `sig(t_n) = #t_n` (TA5(b) and TA5(c)'s single-position-modification clause jointly preserve positions `1..#t_n − 1`). Since `#b_C(d) = #d + 2 = #t_n − 1`, the prefix `b_C(d)` lives entirely within the preserved positional range, so `t_{n + 1}` agrees with `t_n` (and thus with `b_C(d)`) at positions `1..#b_C(d)`. The length condition `#b_C(d) = #d + 2 ≤ #d + 3 = #t_{n + 1}` holds. By Prefix, `b_C(d) ≼ t_{n + 1}`. The link case is symmetric, with `b_L(d)` in place of `b_C(d)` and `A_L(d)` in place of `A_C(d)`. ∎

The corollary is consumed in three places: (i) the FirstEmissionFreshness lemma below; (ii) the K.α and K.λ subsequent-emit *cross-document freshness* derivations (where freshly emitted addresses must be exhibited as extending their home document's anchor before T10 applies); (iii) the ChainMembershipForOrigin lemma's contiguous-prefix postcondition below (indirectly, by underwriting the prefix-relation premises consumed by the chain-membership argument).

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
  - *Subsequent emission* (`{a' ∈ dom(C) : origin(a') = d} ≠ ∅`; equivalently `m_d ≥ 1` at `Σ` by IH): by IH, the prior intersection is `{t_1, …, t_{m_d}}`. By ChainEnumerationInjectivity, `n ↦ t_n` is strictly increasing under T1, so `t_1 < t_2 < … < t_{m_d}` and the lex-order maximum of `{t_1, …, t_{m_d}}` is `t_{m_d}`. Hence `a_prev := max{a' ∈ dom(C) : origin(a') = d} = t_{m_d}`. By SubAllocatorAxiom.ChainDiscipline, `A_C(d)` is closed under `inc(·, 0)`, so `a = inc(t_{m_d}, 0) = t_{m_d + 1}`. The new intersection set at `Σ'` is `{t_1, …, t_{m_d}, t_{m_d + 1}} = {t_1, …, t_{m_d + 1}}`, witnessing the chain index `m_d + 1` at `Σ'`.

  The link contiguous-prefix postcondition is unchanged by frame on `dom(L)`.

- *K.λ(d, ℓ, (e₁, …, eₙ)):* Symmetric to K.α with content↔link, using SubAllocatorAxiom.FirstEmission for the first-emit branch (placing `ℓ = s_1`, witnessing `n_d = 1`) and SubAllocatorAxiom.ChainDiscipline for the subsequent-emit branch (placing `ℓ = s_{n_d + 1}` from `ℓ_prev = s_{n_d}` by ChainEnumerationInjectivity, witnessing `n_d + 1` at `Σ'`). The content contiguous-prefix postcondition is unchanged by frame on `dom(C)`. ∎

This lemma is the inductive invariant that licenses application of ChainEnumerationInjectivity to `(a_prev, a)` in the K.α subsequent-emit case and to `(ℓ_prev, ℓ)` in the K.λ subsequent-emit case: ChainEnumerationInjectivity requires both indices to inhabit the same chain, and ChainMembershipForOrigin supplies that membership for the predecessor.

**Corollary (StoreT4Validity).** At every reachable state `Σ`, every entry of `dom(C) ∪ dom(L)` is a T4-valid tumbler:

  `(A a ∈ dom(C) :: ValidAddress(a))`
  `(A ℓ ∈ dom(L) :: ValidAddress(ℓ))`

*Proof.* For any `a ∈ dom(C)`, ChainMembershipForOrigin places `a ∈ A_C(origin(a))` (well-defined since `origin(a) ∈ dom(M)` by C2). By ChainElementT4Validity, every element of `A_C(origin(a))` is T4-valid; hence `a` is T4-valid. The link case is symmetric: `ℓ ∈ dom(L)` lies in `A_L(origin(ℓ))` by ChainMembershipForOrigin, and ChainElementT4Validity gives T4-validity of every element. ∎

This corollary discharges the T4-validity precondition of T7 (FirstElementFieldDistinction, ASN-0034) wherever T7 is cited against `dom(C)` and `dom(L)` — in particular, in the L14 discharge (matrix below) and in the FirstEmissionFreshness lemma below against `dom(L)`.

**Lemma (FirstEmissionFreshness).** At every reachable state `Σ`, the first emission of an active sub-allocator chain — the address that K.α (resp. K.λ) commits when the corresponding first-emit predicate fires — is fresh against `dom(C) ∪ dom(L)`:

  - *Content first-emit:* Under the K.α first-emit predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`, the first emission `a = [d.0.s_C.1]` of `A_C(d)` satisfies `a ∉ dom(C) ∪ dom(L)` at the K.α event that commits `a`.
  - *Link first-emit:* Under the K.λ first-emit predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`, the first emission `ℓ = [d.0.s_L.1]` of `A_L(d)` satisfies `ℓ ∉ dom(L) ∪ dom(C)` at the K.λ event that commits `ℓ`.

This lemma replaces the freshness conclusion that earlier drafts carried inside SubAllocatorAxiom.FirstEmission. The proof consumes ChainMembershipForOrigin and StoreT4Validity at the pre-state `Σ` (both established above) together with Cross-document disjointness (next section). All three are established under the same simultaneous-induction discipline (see the *Simultaneous-induction framing* paragraph in the discharge section); FirstEmissionFreshness is consumed at the K.α/K.λ first-emit precondition discharge in the next section, where the inductive hypothesis at the pre-state supplies its premises.

*Proof.* Take the content case; the link case is symmetric.

*Against `dom(C)`.* Under the first-emit predicate at the pre-state `Σ`, every `a' ∈ dom(C)` has `origin(a') ≠ d`. (i) `a = [d.0.s_C.1]` is the first emission of `A_C(d)`, so by ChainPrefixExtension (base case), `b_C(d) ≼ a`. (ii) For every `a' ∈ dom(C)` with `origin(a') ≠ d`: ChainMembershipForOrigin at `Σ` places `a' ∈ A_C(origin(a'))` (well-defined since `origin(a') ∈ dom(M)` by C2), and ChainPrefixExtension gives `b_C(origin(a')) ≼ a'`. (iii) Cross-document disjointness applied to `(d, origin(a'))` gives `b_C(d) ⋠ b_C(origin(a')) ∧ b_C(origin(a')) ⋠ b_C(d)`. (iv) T10 (PartitionIndependence, ASN-0034) closes: `a ≠ a'`.

*Against `dom(L)`.* StoreT4Validity at `Σ` gives T4-validity of every `ℓ ∈ dom(L)`; `a` is T4-valid by ChainElementT4Validity applied to `A_C(d)` (whose first emission `[d.0.s_C.1]` is T4-valid by SubAllocatorAxiom.FirstEmission). By L0, `E(ℓ)₁ = s_L` and `E(a)₁ = s_C`; by SC-NEQ, `s_C ≠ s_L`; `zeros(a) = zeros(ℓ) = 3` by FirstEmission's structural form and L1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `a ≠ ℓ`. ∎


## Cross-document disjointness chain

**Lemma (Cross-document disjointness; T10 + Prefix + M0).** For any two distinct documents `d₁, d₂ ∈ dom(M)` with `d₁ ≠ d₂`, the link sub-allocator anchors `p₁ := b_L(d₁) = [d₁.0.s_L]` and `p₂ := b_L(d₂) = [d₂.0.s_L]` satisfy

  `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`

so by T10 (PartitionIndependence, ASN-0034), every address extending `p₁` differs from every address extending `p₂`. The same lemma holds with `b_C` in place of `b_L` for content allocations.

*Proof.* By M0, both `d₁, d₂ ∈ dom(M)` are T4-valid tumblers with `zeros(d_i) = 2`. Case-split on the document-level prefix relationship: prefix-comparable or prefix-incomparable.

*Case A — Prefix-comparable.* WLOG `d₁ ≼ d₂` and `d₁ ≠ d₂`. Hence `d₁ ≺ d₂` (proper prefix). By Prefix's derived proper-prefix length postcondition (`p ≺ q ⟹ #p < #q`, established in PrefixRelation, ASN-0034), `#d₁ < #d₂`. This in turn gives `#d₁ + 1 ≤ #d₂` (NAT-discrete's forward direction), so position `#d₁ + 1` lies within `d₂`'s native domain `{1, …, #d₂}` and the component `d₂[#d₁+1]` is well-defined. The argument that `d₂[#d₁+1] ≠ 0` chains M0 at *both* documents: by M0 at `d₁`, `zeros(d₁) = 2`, so `d₁` has exactly two zero positions within `1..#d₁`. The prefix relation gives `d₂[k] = d₁[k]` for `1 ≤ k ≤ #d₁`, so `d₂` inherits those two zero positions at the same indices. By M0 at `d₂`, `zeros(d₂) = 2`, so `d₂` has no further zeros in its native domain; in particular `d₂[#d₁+1] ≠ 0`.

The anchors are length-`+2` extensions of their respective document addresses: `#p_i = #d_i + 2`, with `p_i[k] = d_i[k]` for `1 ≤ k ≤ #d_i`, `p_i[#d_i + 1] = 0`, and `p_i[#d_i + 2] = s_L`. From `#d₁ < #d₂` we obtain `#p₁ ≤ #p₂` (in fact `#p₁ < #p₂`).

At position `k = #d₁ + 1`:
- `k ≤ #p₁` since `k = #d₁ + 1 ≤ #d₁ + 2 = #p₁`
- `k ≤ #p₂` since `k = #d₁ + 1 < #d₂ + 2 = #p₂` (using `#d₁ < #d₂`)

So `k ≤ min(#p₁, #p₂)`. The values:
- `p₁[k] = p₁[#d₁ + 1] = 0` (the zero separator inserted by the `b_L` construction)
- `p₂[k] = p₂[#d₁ + 1] = d₂[#d₁ + 1] ≠ 0` (by the M0-at-both-`d₁`-and-`d₂` zero-count argument above; `#d₁ + 1 ≤ #d₂` since `#d₁ < #d₂`)

Thus `p₁[k] = 0 ≠ p₂[k]` at an index within both anchors. This witnesses `p₁ ⋠ p₂` via the component-disagreement direction of Prefix's negation (Prefix, ASN-0034): unfolding `p ⋠ q ≡ ¬(#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ))`, the negation reads `#p > #q ∨ (∃ i : 1 ≤ i ≤ #p : qᵢ ≠ pᵢ)`; at `(p, q) := (p₁, p₂)`, the existential disjunct is discharged by the witness `k = #d₁ + 1` with `k ≤ #p₁` and `p₂[k] ≠ p₁[k]`. For `p₂ ⋠ p₁`, the length-disjunct route applies directly: `#p₂ = #d₂ + 2 > #d₁ + 2 = #p₁`, so the length conjunct `#p₂ ≤ #p₁` of `p₂ ≼ p₁` fails outright, witnessing `p₂ ⋠ p₁` without need of a component-divergence index. (The component-disagreement direction also discharges `p₂ ⋠ p₁` at the same `k` and the same disagreement values — since `k = #d₁ + 1 ≤ #p₂` — providing an independent alternative witness.)

*Case B — Prefix-incomparable.* `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` at the document level. The joint conjunction does not directly yield a position divergence at `k ≤ min(#d₁, #d₂)`: in asymmetric-length subcases, one of the two `⋠` clauses is satisfied by the failure of Prefix's length conjunct alone, supplying no component-divergence witness; the position-divergence witness must be extracted from the *other* clause. We case-split on the length relationship between `d₁` and `d₂`, exhaustive by NAT-order's at-least-one trichotomy at `(#d₁, #d₂)`. Sub-cases B.i and B.ii are *exhaustive but not mutually exclusive*: B.i covers `#d₁ < #d₂` and `#d₁ = #d₂`, B.ii covers `#d₂ < #d₁`, and at equality both B.i and the mirror reading of B.ii fire symmetrically (the mirror reading extracts the same component witness from `d₂ ⋠ d₁` rather than `d₁ ⋠ d₂`). The proof structure is exhaustive across the trichotomy disjuncts.

*Sub-case B.i — `#d₁ ≤ #d₂` (covers `<` and `=`).* The length conjunct `#d₁ ≤ #d₂` of `d₁ ≼ d₂` holds, so `d₁ ⋠ d₂` must be witnessed by failure of the component conjunct: there exists `i` with `1 ≤ i ≤ #d₁` and `d₂[i] ≠ d₁[i]`. Take `k := i`; then `k ≤ #d₁ = min(#d₁, #d₂)` and `d₁[k] ≠ d₂[k]`. (At equality `#d₁ = #d₂`, the same argument also applies symmetrically through `d₂ ⋠ d₁`; T3 (CanonicalRepresentation, ASN-0034) provides an alternative route, since `d₁ ≠ d₂` together with `#d₁ = #d₂` forces a position divergence.)

*Sub-case B.ii — `#d₂ < #d₁` (strict `>`).* Symmetric: the length conjunct of `d₂ ≼ d₁` holds, so `d₂ ⋠ d₁` is witnessed by some `i` with `1 ≤ i ≤ #d₂` and `d₁[i] ≠ d₂[i]`. Take `k := i`; then `k ≤ #d₂ = min(#d₁, #d₂)`.

In either sub-case the witness `k` satisfies `k ≤ min(#d₁, #d₂)`. From `#p_i = #d_i + 2`, NAT-addcompat's strict successor lifts `#d_i ≤ #p_i`, so `min(#d₁, #d₂) ≤ min(#p₁, #p₂)`. The anchors are length-`+2` extensions agreeing with `d_i` at positions `1..#d_i`, so `p₁[k] = d₁[k] ≠ d₂[k] = p₂[k]` at an index within both anchors, witnessing `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` via the component-disagreement direction of Prefix's negation (Prefix, ASN-0034) — the existential disjunct of `¬(#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ))` discharged by `k` in both directions. (In sub-case B.ii where `#d₂ < #d₁`, the length-disjunct also discharges `p₁ ⋠ p₂` directly via `#p₁ > #p₂`, as an alternative independent of the component witness; in sub-case B.i with `#d₁ = #d₂`, the lengths agree and only the component-disagreement route applies.)

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

*Cross-anchor freshness.* For every `d' ∈ dom(M)`, the sub-allocator anchors `b_C(d') = [d'.0.s_C]` and `b_L(d') = [d'.0.s_L]` have `zeros = 3` (one inherited from each of `d'`'s two zeros, plus the separator inserted at position `#d' + 1`). K.σ's precondition `zeros(d) = 2` therefore rules out collision with any such anchor: `d` cannot equal `b_C(d')` or `b_L(d')` for any `d' ∈ dom(M)`, since equality would force `zeros(d) = 3` against the precondition. No separate clause is needed.

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
  - *First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`. Freshness against `dom(C) ∪ dom(L)` is supplied by FirstEmissionFreshness (which derives the conclusion from L0 + SC-NEQ + ChainPrefixExtension + ChainMembershipForOrigin + Cross-document disjointness + StoreT4Validity + T7 + ChainElementT4Validity at the pre-state).
  - *Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(a_prev, 0)` (TA5(c)) where `a_prev := max{a' ∈ dom(C) : origin(a') = d}`, the next sibling on `A_C(d)`'s `inc(·, 0)` chain. The `max` is well-defined because the set is finite (C-fin restricted by `origin(·) = d`). *Within-document freshness against `dom(C)`* is discharged by combining ChainEnumerationInjectivity with the max-property of `a_prev`. Let `n_prev` be the chain index of `a_prev` within `A_C(d)`. For every `a' ∈ dom(C)` with `origin(a') = d`: (i) ChainMembershipForOrigin places `a' ∈ A_C(d)` at some chain index `m`, with `a' = t_m`. (ii) By ChainEnumerationInjectivity, `n ↦ t_n` is strictly monotone under T1, hence injective and order-preserving in both directions. From `a' = t_m`, `a_prev = t_{n_prev}`, and `a' ≤ a_prev` (the lex-order max-property), conclude `m ≤ n_prev`. (iii) SubAllocatorAxiom.ChainDiscipline places `a = inc(a_prev, 0)` at chain index `n_prev + 1`, so ChainEnumerationInjectivity yields `a' = t_m ≤ t_{n_prev} = a_prev < t_{n_prev + 1} = a`, hence `a' ≠ a`. (ChainMembershipForOrigin's stronger contiguous-prefix postcondition identifies the prior intersection as `{t_1, …, t_{m_d}}` with `a_prev = t_{m_d}` and `a = t_{m_d + 1}`, but the freshness argument needs only the subset form.) *Cross-document freshness against `dom(C)`* (for `a' ∈ dom(C)` with `origin(a') ≠ d`) is discharged in three steps: (a) `a = inc(a_prev, 0)` extends `b_C(d)` — by IH on ChainMembershipForOrigin at `Σ`, `a_prev ∈ A_C(d)`; by SubAllocatorAxiom.ChainDiscipline's closure under `inc(·, 0)`, `a = inc(a_prev, 0) ∈ A_C(d)` as a chain element; ChainPrefixExtension at `Σ` (whose conceptual-chain quantifier scope covers `a` directly, since `a ∈ A_C(d)` as a conceptual chain element regardless of whether `a` is yet committed to `dom(C)`) gives `b_C(d) ≼ a`. (b) For every `a' ∈ dom(C)` with `origin(a') ≠ d`: ChainMembershipForOrigin at `Σ` places `a' ∈ A_C(origin(a'))` (well-defined since `origin(a') ∈ dom(M)` by C2 at `Σ`), and ChainPrefixExtension at `Σ` gives `b_C(origin(a')) ≼ a'`. (c) Cross-document disjointness applied to `(d, origin(a'))` gives `b_C(d) ⋠ b_C(origin(a')) ∧ b_C(origin(a')) ⋠ b_C(d)`; T10 (PartitionIndependence, ASN-0034) closes: `a ≠ a'`. *Freshness against `dom(L)`* is discharged by L0 + SC-NEQ + StoreT4Validity + T7: StoreT4Validity at `Σ` gives T4-validity of every `ℓ ∈ dom(L)`; `a` is T4-valid by ChainElementT4Validity (since `a ∈ A_C(d)` by ChainDiscipline's closure under `inc(·, 0)` applied to `a_prev`); L0 supplies `E(a)₁ = s_C ≠ s_L = E(ℓ)₁` (SC-NEQ); `zeros(a) = zeros(ℓ) = 3` by C1/L1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `a ≠ ℓ`. (Equivalently the conclusion may be cited via L14 at the pre-state — the two routes derive the same fact.)
- `v ∈ Val` (well-formed content value)

*Effect:* `C' = C ∪ {a ↦ v}`

*Frame:* `L' = L; dom(M') = dom(M); (A d' :: M'(d') = M(d'))`

The explicit `dom(M') = dom(M)` clause makes domain equality unambiguous alongside the pointwise function equality. Under partial-function semantics the two together force `M' = M`, so C2 and L1a at `Σ` transfer to `Σ'` directly: `origin(a') ∈ dom(M)` implies `origin(a') ∈ dom(M')`.

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
  - *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`, the determinate first emission of `A_L(d)`. Freshness against `dom(L) ∪ dom(C)` is supplied by FirstEmissionFreshness (which derives the conclusion from L0 + SC-NEQ + ChainPrefixExtension + ChainMembershipForOrigin + Cross-document disjointness + StoreT4Validity + T7 + ChainElementT4Validity at the pre-state).
  - *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(ℓ_prev, 0)` (TA5(c)) where `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`, the next sibling on `A_L(d)`'s `inc(·, 0)` chain. The `max` is well-defined because the set is finite (L-fin restricted by `origin(·) = d`). *Within-document freshness against `dom(L)`* is discharged by combining ChainEnumerationInjectivity with the max-property of `ℓ_prev`. Let `n_prev` be the chain index of `ℓ_prev` within `A_L(d)`. For every `ℓ' ∈ dom(L)` with `origin(ℓ') = d`: (i) ChainMembershipForOrigin places `ℓ' ∈ A_L(d)` at some chain index `m`, with `ℓ' = s_m`. (ii) By ChainEnumerationInjectivity, `n ↦ s_n` is strictly monotone under T1, hence injective and order-preserving in both directions. From `ℓ' = s_m`, `ℓ_prev = s_{n_prev}`, and `ℓ' ≤ ℓ_prev` (the lex-order max-property), conclude `m ≤ n_prev`. (iii) SubAllocatorAxiom.ChainDiscipline places `ℓ = inc(ℓ_prev, 0)` at chain index `n_prev + 1`, so ChainEnumerationInjectivity yields `ℓ' = s_m ≤ s_{n_prev} = ℓ_prev < s_{n_prev + 1} = ℓ`, hence `ℓ' ≠ ℓ`. (ChainMembershipForOrigin's stronger contiguous-prefix postcondition identifies the prior intersection as `{s_1, …, s_{n_d}}` with `ℓ_prev = s_{n_d}` and `ℓ = s_{n_d + 1}`, but the freshness argument needs only the subset form.) *Cross-document freshness against `dom(L)`* (for `ℓ' ∈ dom(L)` with `origin(ℓ') ≠ d`) is discharged in three steps: (a) `ℓ = inc(ℓ_prev, 0)` extends `b_L(d)` — by IH on ChainMembershipForOrigin at `Σ`, `ℓ_prev ∈ A_L(d)`; by SubAllocatorAxiom.ChainDiscipline's closure under `inc(·, 0)`, `ℓ = inc(ℓ_prev, 0) ∈ A_L(d)` as a chain element; ChainPrefixExtension at `Σ` (whose conceptual-chain quantifier scope covers `ℓ` directly, since `ℓ ∈ A_L(d)` as a conceptual chain element regardless of whether `ℓ` is yet committed to `dom(L)`) gives `b_L(d) ≼ ℓ`. (b) For every `ℓ' ∈ dom(L)` with `origin(ℓ') ≠ d`: ChainMembershipForOrigin at `Σ` places `ℓ' ∈ A_L(origin(ℓ'))` (well-defined since `origin(ℓ') ∈ dom(M)` by L1a at `Σ`), and ChainPrefixExtension at `Σ` gives `b_L(origin(ℓ')) ≼ ℓ'`. (c) Cross-document disjointness applied to `(d, origin(ℓ'))` gives `b_L(d) ⋠ b_L(origin(ℓ')) ∧ b_L(origin(ℓ')) ⋠ b_L(d)`; T10 (PartitionIndependence, ASN-0034) closes: `ℓ ≠ ℓ'`. *Freshness against `dom(C)`* is discharged by L0 + SC-NEQ + StoreT4Validity + T7: StoreT4Validity at `Σ` gives T4-validity of every `a ∈ dom(C)`; `ℓ` is T4-valid by ChainElementT4Validity (since `ℓ ∈ A_L(d)` by ChainDiscipline's closure); L0 supplies `E(ℓ)₁ = s_L ≠ s_C = E(a)₁` (SC-NEQ); `zeros(ℓ) = zeros(a) = 3` by L1/C1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `ℓ ≠ a`. (Equivalently the conclusion may be cited via L14 at the pre-state.)
- `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` (well-formed link value with mandatory non-empty type endset at slot 3 — L3). The arity-3 default `(F, G, Θ)` (slot 1 = from, slot 2 = to, slot 3 = type) is the StandardTriple convention retained for worked examples and notational compactness; the substrate admits arbitrary arity `N ≥ 3`.

*Effect:* `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`

*Frame:* `C' = C; dom(M') = dom(M); (A d' :: M'(d') = M(d'))`

The explicit `dom(M') = dom(M)` clause makes domain equality unambiguous alongside the pointwise function equality. Under partial-function semantics the two together force `M' = M`, so C2 and L1a at `Σ` transfer to `Σ'` directly: `origin(ℓ') ∈ dom(M)` implies `origin(ℓ') ∈ dom(M')`.

Cross-document disjointness for link allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_L(d)` and `p₂ := b_L(d')`.

*Forward allocation, derivable.* The within-document forward-allocation property `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` is not stated as a precondition because it is a derivable consequence of the emission rules — symmetrically with K.α. In the subsequent-emission case, `ℓ = inc(max{prev}, 0)` and TA5(a) gives `inc(t, 0) > t`, so `ℓ > max{prev} ≥ ℓ'` for every `ℓ' ∈ dom(L)` with `origin(ℓ') = d`. In the first-emission case the universal antecedent `{ℓ' : origin(ℓ') = d} = ∅` is vacuous. The same derivation applies to K.α's content emissions; neither operator carries the clause as a precondition.


## Worked example

To make the substrate's operation concrete, we trace a small scenario step-by-step starting from `Σ₀ = (∅, ∅, ∅)`.

*Arity convention.* The K.λ invocations below use the arity-3 default `(F, G, Θ)` (StandardTriple — slot 1 from, slot 2 to, slot 3 type) for notational compactness. This is one admissible instance of K.λ's general signature `K.λ(d, ℓ, (e₁, …, eₙ))` with `N = 3`; the substrate admits arbitrary `N ≥ 3` per L3, and any higher-arity link value satisfying the precondition would be equally well-formed.

*Fix a document address.* Let `d = [1, 0, 2, 0, 5]` — `#d = 5`, with zeros at positions 2 and 4 so `zeros(d) = 2`, with positive first and last components (1 and 5) and no adjacent zeros, hence T4-valid. By T4b, its projections are `N(d) = [1]`, `U(d) = [2]`, `D(d) = [5]`. By SubspaceConventionAxiom, `s_C = 1` and `s_L = 2`.

*Step 1 — `K.σ(d)` (document registration).* Precondition: `d ∉ dom(M₀) = ∅` ✓; `ValidAddress(d) ∧ zeros(d) = 2` ✓. Effect commits `dom(M₁) = {d}` with `M₁(d) = ∅`; `C₁ = ∅`, `L₁ = ∅`. By SubAllocatorAxiom.Exists, both `A_C(d)` and `A_L(d)` chains are active under `d`. Verifying invariants at `Σ₁ = (∅, ∅, {d ↦ ∅})`: M0 holds (the single key `d` satisfies `zeros = 2`); M1 holds (`∅ ⊆ {d}`); all C-/L-invariants and L14, L-fin, C-fin are vacuous or trivial on empty stores.

*Step 2 — `K.α(d, a, v)` (first content emission).* Pinning the address from `Σ₁`: the predicate `{a' ∈ dom(C₁) : origin(a') = d} = ∅` selects the first-emit case, so `a = [d.0.s_C.1] = [1, 0, 2, 0, 5, 0, 1, 1]`. Witness it via the C1c chain `(t₀, t₁, t₂)`:
- `t₀ = d = [1, 0, 2, 0, 5]`
- `t₁ = inc(d, 2)`: TA5(d) at `k = 2` gives the structural form, appending `[0, 1]` to yield `[1, 0, 2, 0, 5, 0, 1] = b_C(d)`. Admissibility: TA5a at `k = 2` requires `zeros(d) ≤ 2`; M0 gives `zeros(d) = 2 ≤ 2`, satisfied — hence `t₁` is T4-valid; TA5(d) gives `zeros(t₁) = 3`.
- `t₂ = inc(b_C(d), 1)`: TA5(d) at `k = 1` gives the structural form, appending `1` to yield `[1, 0, 2, 0, 5, 0, 1, 1] = a`. Admissibility: TA5a at `k = 1` applies unconditionally on T4-valid inputs (no zero-count side condition), so `t₂` is T4-valid given `t₁` T4-valid; TA5(d) gives `zeros(t₂) = 3`, `#E(t₂) = 2`.

Verifying preconditions: `a ∉ dom(C₁) ∪ dom(L₁) = ∅` ✓; `zeros(a) = 3` ✓; `E(a) = [1, 1]` so `E(a)₁ = 1 = s_C` ✓; `#E(a) = 2 ≥ 2` ✓; `origin(a) = N(a).0.U(a).0.D(a) = [1].0.[2].0.[5] = d` ✓. Freshness of `a` against `dom(C₁) ∪ dom(L₁)` is supplied by FirstEmissionFreshness, here vacuously since the predecessor stores are empty.

Effect: `C₂ = {a ↦ v}`; `L₂ = ∅`; `M₂ = M₁`. Verifying invariants at `Σ₂`: C0 (extended at fresh `a`), C1 (`zeros(a) = 3`), C1b (`#E(a) = 2`), C1c (chain exhibited above), C2 (`origin(a) = d ∈ dom(M₂)`), C-fin (`|dom(C₂)| = 1 < ∞`) all hold at the new key.

*Step 3 — `K.λ(d, ℓ, F, G, Θ)` (first link emission).* Pinning from `Σ₂`: the predicate `{ℓ' ∈ dom(L₂) : origin(ℓ') = d} = ∅` selects the first-emit case, so `ℓ = [d.0.s_L.1] = [1, 0, 2, 0, 5, 0, 2, 1]`. Witness via the L1c chain `(t₀, t₁, t₂, t₃)`:
- `t₀ = d = [1, 0, 2, 0, 5]`
- `t₁ = inc(d, 2) = [1, 0, 2, 0, 5, 0, 1] = b_C(d)` (admissibility as in Step 2)
- `t₂ = inc(b_C(d), 0)`: TA5(c) at `k = 0` gives the structural form, incrementing `b_C(d)`'s rightmost nonzero component (position 7, from `1` to `2`) to yield `[1, 0, 2, 0, 5, 0, 2] = b_L(d)`. By SubspaceConventionAxiom, `s_L = 2 = s_C + 1`, matching position 7. Admissibility: TA5a at `k = 0` is unconditionally T4-preserving, so `t₂` is T4-valid given `b_C(d)` T4-valid (from Step 2).
- `t₃ = inc(b_L(d), 1)`: TA5(d) at `k = 1` gives the structural form, appending `1` to yield `[1, 0, 2, 0, 5, 0, 2, 1] = ℓ`. Admissibility: TA5a at `k = 1` applies unconditionally on T4-valid inputs, so `t₃` is T4-valid given `b_L(d)` T4-valid. `zeros(ℓ) = 3`, `#E(ℓ) = 2`.

Verifying preconditions: `ℓ ∉ dom(L₂) ∪ dom(C₂) = {a}`. Disagreement at position 7 (`a₇ = 1` vs `ℓ₇ = 2`) gives `ℓ ≠ a`, confirming the L0 + SC-NEQ + T7 derivation: the two addresses sit in disjoint subspaces. `zeros(ℓ) = 3` ✓; `E(ℓ) = [2, 1]` so `E(ℓ)₁ = 2 = s_L` ✓; `#E(ℓ) = 2 ≥ 2` ✓; `origin(ℓ) = d` ✓. Freshness supplied by FirstEmissionFreshness.

Effect: `L₃ = {ℓ ↦ (F, G, Θ)}`; `C₃ = C₂`; `M₃ = M₂`. Verifying invariants at `Σ₃`: L0/L1/L1a/L1b/L1c/L3/L12 all hold at the new key per the matrix; L14 holds non-trivially: `dom(C₃) ∩ dom(L₃) = {a} ∩ {ℓ} = ∅` (verified by E(·)₁ disagreement); L-fin holds (`|dom(L₃)| = 1 < ∞`).

*Step 4 — `K.α(d, a', v')` (second content emission, subsequent-emit branch).* Pinning from `Σ₃`: `{a'' ∈ dom(C₃) : origin(a'') = d} = {a}` is non-empty, so the subsequent-emit branch fires with `a' = inc(max{a}, 0) = inc(a, 0)`. Since `sig(a) = 8` with value `1`, TA5(c) gives `a' = [1, 0, 2, 0, 5, 0, 1, 2]`. The C1c chain extends `a`'s chain by one step: `(t₀, t₁, t₂, a')` with `a' = inc(t₂, 0) = inc(a, 0)`. Admissibility of the new step: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `a'` is T4-valid given `a` T4-valid (the latter from Step 2's chain exhibition); TA5(c) gives the structural form. Freshness against `dom(C₃) = {a}` discharged by ChainEnumerationInjectivity (within-chain injectivity) applied to `A_C(d)`'s chain (per SubAllocatorAxiom.ChainDiscipline); freshness against `dom(L₃) = {ℓ}` discharged by L0 + SC-NEQ + T7.

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
- `t₁ = inc(d', 2)`: TA5(d) at `k = 2` gives the structural form, appending `[0, 1]` to yield `[1, 0, 2, 0, 5, 3, 0, 1] = b_C(d')` with `zeros = 3`. Admissibility: TA5a at `k = 2` requires `zeros(d') ≤ 2`; M0 gives `zeros(d') = 2 ≤ 2`, satisfied — hence `t₁` is T4-valid.
- `t₂ = inc(b_C(d'), 1)`: TA5(d) at `k = 1` gives the structural form, appending `1` to yield `a'' = [1, 0, 2, 0, 5, 3, 0, 1, 1]`. Admissibility: TA5a at `k = 1` applies unconditionally on T4-valid inputs, so `a''` is T4-valid given `t₁` T4-valid. `zeros(a'') = 3`, `#E(a'') = 2`.

Verifying preconditions: `a'' ∉ dom(C₅) ∪ dom(L₅) = {a, a', ℓ}`. *Cross-document freshness* against `{a, a'}` (both with `origin = d ≠ d'`): by Cross-document disjointness at Step 5, `b_C(d) ⋠ b_C(d') ∧ b_C(d') ⋠ b_C(d)`; `a, a'` extend `b_C(d)` (Steps 2, 4) while `a''` extends `b_C(d')`, so by T10, `a'' ≠ a` and `a'' ≠ a'`. *Sub-space freshness* against `ℓ`: `E(a'')₁ = 1 = s_C ≠ 2 = s_L = E(ℓ)₁` by L0 + SC-NEQ, so `a'' ≠ ℓ`. Other preconditions: `zeros(a'') = 3` ✓; `E(a'') = [1, 1]`, `E(a'')₁ = s_C` ✓; `#E(a'') = 2` ✓; `origin(a'') = N(a'').0.U(a'').0.D(a'') = [1].0.[2].0.[5, 3] = d'` ✓. (FirstEmissionFreshness applied to `A_C(d')` supplies the same conclusion compactly; the derivation above exhibits the underlying mechanism it bundles.)

Effect: `C₆ = C₅ ∪ {a'' ↦ v''} = {a ↦ v, a' ↦ v', a'' ↦ v''}`; `L₆ = L₅`; `M₆ = M₅`. Invariants at `Σ₆`: C0 (existing values unchanged), C1 (`zeros(a'') = 3`), C1b (`#E(a'') = 2`), C1c (chain exhibited above), C2 (`origin(a'') = d' ∈ dom(M₆)`), C-fin (`|C₆| = 3 < ∞`); ChainMembershipForOrigin extends: `{a''} ⊆ A_C(d')` by FirstEmission.

*Step 7 — `K.λ(d', ℓ'', F'', G'', Θ'')` (first link emission under `d'`).* Pinning from `Σ₆`: `{ℓ''' ∈ dom(L₆) : origin(ℓ''') = d'} = ∅` (`origin(ℓ) = d ≠ d'`), so the first-emit branch fires with `ℓ'' = [d'.0.s_L.1] = [1, 0, 2, 0, 5, 3, 0, 2, 1]` (length 9). The L1c chain `(t₀, t₁, t₂, t₃)`:
- `t₀ = d'`
- `t₁ = inc(d', 2) = b_C(d')` (admissibility as in Step 6)
- `t₂ = inc(b_C(d'), 0) = [1, 0, 2, 0, 5, 3, 0, 2] = b_L(d')` (TA5(c) gives the structural form, advancing `sig(b_C(d')) = 8` from `s_C = 1` to `s_L = 2`; SubspaceConventionAxiom gives `s_L = s_C + 1`. TA5a at `k = 0` is unconditionally T4-preserving, so `t₂` is T4-valid given `b_C(d')` T4-valid.)
- `t₃ = inc(b_L(d'), 1) = ℓ''` (TA5(d) at `k = 1` gives the structural form, appending `1`. TA5a at `k = 1` applies unconditionally on T4-valid inputs, so `ℓ''` is T4-valid given `b_L(d')` T4-valid. `zeros(ℓ'') = 3`, `#E(ℓ'') = 2`.)

Verifying preconditions: `ℓ'' ∉ dom(L₆) ∪ dom(C₆) = {ℓ, a, a', a''}`. *Cross-document freshness* against `{ℓ}` (origin = d ≠ d'): by Cross-document disjointness at Step 5, `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`; `ℓ` extends `b_L(d)` (Step 3) while `ℓ''` extends `b_L(d')`, so by T10, `ℓ'' ≠ ℓ`. *Sub-space freshness* against `{a, a', a''}`: each content address has `E(·)₁ = s_C = 1 ≠ 2 = s_L = E(ℓ'')₁`, so `ℓ'' ≠ a, a', a''`. Other preconditions: `zeros(ℓ'') = 3` ✓; `E(ℓ'') = [2, 1]`, `E(ℓ'')₁ = s_L` ✓; `#E(ℓ'') = 2` ✓; `origin(ℓ'') = d'` ✓.

Effect: `L₇ = L₆ ∪ {ℓ'' ↦ (F'', G'', Θ'')}`; `C₇ = C₆`; `M₇ = M₆`. Invariants at `Σ₇`: L0 (`E(ℓ'')₁ = s_L`), L1 (`zeros(ℓ'') = 3`), L1a (`origin(ℓ'') = d' ∈ dom(M₇)`), L1b (`#E(ℓ'') = 2`), L1c (chain exhibited above), L3 (triple endset with non-empty `Θ''`), L12 (existing link `ℓ ↦ (F, G, Θ)` unchanged), L14 (`dom(C₇) ∩ dom(L₇) = {a, a', a''} ∩ {ℓ, ℓ''} = ∅` by SC-NEQ), L-fin (`|L₇| = 2 < ∞`); ChainMembershipForOrigin extends: `{ℓ''} ⊆ A_L(d')` by FirstEmission, witnessing `n_{d'} = 1`.

*Step 8 — `K.λ(d, ℓ_new, F_new, G_new, Θ_new)` (second link emission under `d`, subsequent-emit branch).* Pinning the address from `Σ₇`: `{ℓ''' ∈ dom(L₇) : origin(ℓ''') = d} = {ℓ}` (note `origin(ℓ'') = d' ≠ d`), so the subsequent-emit branch fires with `ℓ_new = inc(max{ℓ}, 0) = inc(ℓ, 0)`. By ChainMembershipForOrigin's contiguous-prefix form at `Σ₇`, `dom(L₇) ∩ {ℓ''' : origin(ℓ''') = d} = {s₁}` with `ℓ = s₁`, so the lex-order max is `s₁` and `ℓ_new = s₂`. Since `sig(ℓ) = 8` with value `1`, TA5(c) gives `ℓ_new = [1, 0, 2, 0, 5, 0, 2, 2]`. The L1c chain extends `ℓ`'s chain by one step: `(t₀, t₁, t₂, t₃, t₄)` with `t₀ = d`, `t₁ = b_C(d)`, `t₂ = b_L(d)`, `t₃ = ℓ`, `t₄ = inc(ℓ, 0) = ℓ_new`. Admissibility of the new step: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `ℓ_new` is T4-valid given `ℓ` T4-valid (the latter from Step 3's chain exhibition); TA5(c) gives the structural form.

Verifying preconditions: `ℓ_new ∉ dom(L₇) ∪ dom(C₇) = {ℓ, ℓ'', a, a', a''}`.
- *Within-chain freshness against `ℓ`:* by ChainMembershipForOrigin at `Σ₇`, `ℓ ∈ A_L(d)` at chain index 1. By SubAllocatorAxiom.ChainDiscipline, `ℓ_new = inc(ℓ, 0) ∈ A_L(d)` at chain index 2. ChainEnumerationInjectivity gives `s₁ < s₂`, hence `ℓ ≠ ℓ_new`. (Concrete check: `ℓ_new` differs from `ℓ` at position 8, where `ℓ[8] = 1 ≠ 2 = ℓ_new[8]`.)
- *Cross-document freshness against `ℓ''`:* (a) `ℓ_new = inc(ℓ, 0)` extends `b_L(d)` — by IH on ChainMembershipForOrigin at `Σ₇`, `ℓ ∈ A_L(d)`; by SubAllocatorAxiom.ChainDiscipline's closure under `inc(·, 0)`, `ℓ_new = inc(ℓ, 0) ∈ A_L(d)` as a chain element; ChainPrefixExtension at `Σ₇` (conceptual-chain quantifier scope covers `ℓ_new` directly, since `ℓ_new ∈ A_L(d)` as a conceptual chain element regardless of whether `ℓ_new` is yet committed to `dom(L)`) gives `b_L(d) ≼ ℓ_new` (concrete check: positions `1..7` of `ℓ_new = [1, 0, 2, 0, 5, 0, 2, 2]` are `[1, 0, 2, 0, 5, 0, 2] = b_L(d)`). (b) `ℓ'' ∈ A_L(d')` by ChainMembershipForOrigin at `Σ₇`, and `b_L(d') ≼ ℓ''` by ChainPrefixExtension. (c) Cross-document disjointness at `(d, d')` (verified in Step 5) gives `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`. T10 (PartitionIndependence, ASN-0034) closes: `ℓ_new ≠ ℓ''`.
- *Sub-space freshness against `{a, a', a''}`:* StoreT4Validity at `Σ₇` gives T4-validity of `a, a', a''`; `ℓ_new` is T4-valid by chain-element T4-validity (TA5a-propagation along `A_L(d)`'s chain from FirstEmission's T4-valid output). L0 supplies `E(·)₁ = s_C = 1` for content and `E(ℓ_new)₁ = s_L = 2` (preserved from `ℓ` by TA5(c) since position 7 of `ℓ_new` carries `2`); `zeros(ℓ_new) = zeros(a) = 3` by L1/C1. SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034) closes: `ℓ_new ≠ a, a', a''`.

Other preconditions: `zeros(ℓ_new) = 3` (ChainUniformZeroCount — preserved under `inc(·, 0)` per ChainDiscipline, anchored at FirstEmission's `zeros = 3`) ✓; `E(ℓ_new) = [2, 2]`, `E(ℓ_new)₁ = 2 = s_L` ✓; `#E(ℓ_new) = 2` ✓; `origin(ℓ_new) = d` (TA5(b) preserves positions `1..7`, including the document-level prefix and the field-separator structure that origin's truncation depends on) ✓.

Effect: `L₈ = L₇ ∪ {ℓ_new ↦ (F_new, G_new, Θ_new)} = {ℓ ↦ (F, G, Θ), ℓ'' ↦ (F'', G'', Θ''), ℓ_new ↦ (F_new, G_new, Θ_new)}`; `C₈ = C₇`; `M₈ = M₇`. Invariants at `Σ₈`: L0–L1c hold at the new key as verified above; L3 (triple endset, non-empty `Θ_new`) ✓; L12 (existing values `ℓ ↦ ·` and `ℓ'' ↦ ·` unchanged) ✓; L14 ✓; L-fin (`|L₈| = 3`) ✓. ChainMembershipForOrigin extends: `dom(L₈) ∩ {ℓ''' : origin(ℓ''') = d} = {ℓ, ℓ_new} = {s₁, s₂}` (contiguous prefix of `A_L(d)`, witnessing `n_d = 2`).

*Step 9 — `K.σ(d_alt)` (third document registration, prefix-incomparable with prior documents).* Fix `d_alt = [1, 0, 3, 0, 7]` — `#d_alt = 5`, with zeros at positions 2 and 4 (`zeros(d_alt) = 2`), no adjacent zeros (positions (2,3) = (0,3) and (4,5) = (0,7)), `d_alt[1] = 1 ≠ 0` and `d_alt[5] = 7 ≠ 0`, hence T4-valid. By T4b, `N(d_alt) = [1]`, `U(d_alt) = [3]`, `D(d_alt) = [7]`.

Verify `d_alt ∉ dom(M₈) = {d, d'}`. Compare with `d = [1, 0, 2, 0, 5]`: position 3 disagrees (`d[3] = 2 ≠ 3 = d_alt[3]`), so `d_alt ≠ d`. Compare with `d' = [1, 0, 2, 0, 5, 3]`: position 3 disagrees similarly, so `d_alt ≠ d'`. The other K.σ precondition `ValidAddress(d_alt) ∧ zeros(d_alt) = 2` ✓.

Effect: `dom(M₉) = {d, d', d_alt}`, with `M₉(d_alt) = ∅` and `M₉(d) = M₉(d') = ∅` unchanged. `C₉ = C₈`, `L₉ = L₈`. By SubAllocatorAxiom.Exists, `A_C(d_alt)` and `A_L(d_alt)` activate at `Σ₉`, alongside the already-active chains for `d` and `d'`.

*Verifying the Cross-document disjointness lemma at `Σ₉` for the prefix-incomparable pair `(d, d_alt)` — Case B sub-case B.i.* The document prefixes are prefix-incomparable: position 3 of `d = [1, 0, 2, 0, 5]` is `2`, position 3 of `d_alt = [1, 0, 3, 0, 7]` is `3`, both within native domains `{1, …, 5}`, so neither is a prefix of the other. Length comparison: `#d = 5 = #d_alt`, so NAT-order's trichotomy at `(#d, #d_alt)` selects sub-case **B.i** (`#d ≤ #d_alt`, with equality holding here). At equality `#d = #d_alt`, sub-cases **B.i** and **B.ii** (`#d_alt < #d`) are not exclusive — B.ii's strict inequality fails but B.i's non-strict inequality holds with the equality disjunct active; symmetrically, applying the proof's machinery to the conjunct `d_alt ⋠ d` (rather than `d ⋠ d_alt`) would fire B.i in its mirror reading. The choice between the two extraction directions is arbitrary at equality; we pursue the `d ⋠ d_alt` reading below, but the mirror argument extracts the same position-divergence witness. The length conjunct `#d ≤ #d_alt` of `d ≼ d_alt` holds, so `d ⋠ d_alt` must be witnessed by failure of the component conjunct — at position `i = 3`, `d[3] = 2 ≠ 3 = d_alt[3]`. Take `k := 3`. Then `k = 3 ≤ 5 = #d = #d_alt = min(#d, #d_alt)` ✓, and `d[k] ≠ d_alt[k]` ✓.

Lift to the anchors `p₁ = b_L(d) = [1, 0, 2, 0, 5, 0, 2]` (length 7) and `p₂ = b_L(d_alt) = [1, 0, 3, 0, 7, 0, 2]` (length 7). From `#p_i = #d_i + 2`, NAT-addcompat's strict successor lifts `#d_i ≤ #p_i`, so `min(#d, #d_alt) = 5 ≤ 7 = min(#p₁, #p₂)`. The anchors are length-`+2` extensions agreeing with their documents at positions `1..#d_i`, so `p₁[3] = d[3] = 2 ≠ 3 = d_alt[3] = p₂[3]` at index `k = 3 ≤ min(#p₁, #p₂) = 7`. This witnesses `b_L(d) ⋠ b_L(d_alt) ∧ b_L(d_alt) ⋠ b_L(d)` via the position-divergence clause of Prefix (PrefixRelation, ASN-0034). The same divergence at position 3 holds for `b_C(d) = [1, 0, 2, 0, 5, 0, 1]` and `b_C(d_alt) = [1, 0, 3, 0, 7, 0, 1]`. By T10, every link (resp. content) allocated under `d_alt` differs from every link (resp. content) allocated under `d`.

A symmetric Case B argument applies to the pair `(d', d_alt)`: position-3 divergence between `d' = [1, 0, 2, 0, 5, 3]` and `d_alt = [1, 0, 3, 0, 7]` (`d'[3] = 2 ≠ 3 = d_alt[3]`). Length comparison: `#d' = 6 > 5 = #d_alt`, so sub-case **B.ii** fires (`#d_alt < #d'`); the witness is the same `k = 3`, lying within both native domains.

*Verifying invariants at `Σ₉`.* M0 holds at `d_alt`: precondition pins `ValidAddress(d_alt) ∧ zeros(d_alt) = 2`; M0 at the prior keys `d, d'` transfers by frame on those entries. M1: `{d, d'} ⊆ {d, d', d_alt}`. C0/C1/C1b/C1c/C2/C-fin hold by frame on `C`; C2 carries the prior content keys' origins `d` (for `a, a'`) and `d'` (for `a''`), all preserved by M1's extension. L0/L1/L1a/L1b/L1c/L3/L12/L-fin hold by frame on `L`; L1a carries `origin(ℓ) = origin(ℓ_new) = d` and `origin(ℓ'') = d'`, preserved by M1. L14: `dom(C₉) ∩ dom(L₉) = {a, a', a''} ∩ {ℓ, ℓ'', ℓ_new} = ∅` (verified by L0's `E(·)₁` partition and StoreT4Validity + T7). ChainMembershipForOrigin transfers at `Σ₉`: under `d`, content gives `{a, a'} = {t₁, t₂}` with `m_d = 2` and link gives `{ℓ, ℓ_new} = {s₁, s₂}` with `n_d = 2`; under `d'`, content gives `{a''} = {t₁}` with `m_{d'} = 1` and link gives `{ℓ''} = {s₁}` with `n_{d'} = 1`; under `d_alt`, both intersections are `∅` with `m_{d_alt} = n_{d_alt} = 0` (vacuous, first emissions under `d_alt` still pending). StoreT4Validity transfers by frame on `C` and `L` together with M1's monotonicity preserving the chain-membership witnesses.

The extended example confirms invariants M0, M1, C0–C2, C-fin, L0–L14, L-fin at each successor state across three documents, exercises both first-emit and subsequent-emit branches of K.α (Steps 2, 4, 6) and K.λ (Steps 3, 7, 8), verifies the Cross-document disjointness lemma in both Case A (prefix-comparable, Step 5 with `d ≼ d'`) and Case B (prefix-incomparable; sub-case B.i with `#d = #d_alt`, sub-case B.ii with `#d_alt < #d'`, Step 9), underwrites cross-document freshness at Steps 6, 7, and 8, and exhibits the ChainMembershipForOrigin lemma's contiguous-prefix postcondition together with the ChainPrefixExtension lemma at every emission past the first.


## Discharge of stated invariants

**Simultaneous-induction framing.** The properties this note establishes decompose into two groups by their quantification structure:

- *Chain-indexed properties (state-independent, once chains are fixed).* ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, and ChainPrefixExtension all quantify over the conceptual sub-allocator chains supplied by SubAllocatorAxiom.ChainDiscipline; their conclusions are determined per-chain (once the chain is fixed at `d`'s K.σ-time activation, the conclusion holds once-and-for-all for every chain index `n ≥ 1`). Their proofs above (in the *Address sub-allocators under documents* section) record those derivations directly from the structural Definition of T10a-discipline-satisfying chain plus foundation claims (TA5a, TA5(a)/(b)/(c), TA5-SigValid, T1, T4, Prefix, NAT-*). No induction over substrate-level transitions is required.
- *Transition-indexed properties (state-dependent).* The stated invariants (M0, M1, C0, C1, C1b, C1c, C2, C-fin, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin) together with the ChainMembershipForOrigin lemma, the StoreT4Validity corollary, and the FirstEmissionFreshness lemma are proved by *simultaneous induction* over transition sequences from `Σ₀`. The inductive hypothesis at each step is the *conjunction* of every transition-indexed property at the current state `Σ`; the inductive step exhibits each holding at `Σ'` using the conjoined IH. No inductive step uses a conclusion derived in the same step. This framing is needed because ChainMembershipForOrigin's K.α/K.λ subsequent-emit cases consume C2/L1a as IH at `Σ`, while the discharge matrix's K.α/K.λ subsequent-emit freshness derivations consume ChainMembershipForOrigin, ChainPrefixExtension (chain-indexed, available unconditionally), and StoreT4Validity at `Σ`; the lemmas and the matrix invariants are mutually entangled and sound only under this simultaneous-induction discipline. The ChainMembershipForOrigin proof above records the per-transition discharges; StoreT4Validity transfers via frame at K.σ and via ChainElementT4Validity (a chain-indexed property) at K.α/K.λ subsequent-emit, anchored at FirstEmission for the first-emit case; FirstEmissionFreshness is consumed at the corresponding K.α/K.λ first-emit precondition discharge and its proof appears above in the *Address sub-allocators under documents* section.

Each transition-indexed invariant is discharged by induction on transition sequences from `Σ₀`. The inductive step is recorded as a per-(invariant, transition) matrix; entries describe how each transition kind preserves or discharges each invariant.

**Base case verification (at `Σ₀ = (∅, ∅, ∅)`).** Most invariants are vacuously satisfied: M0/M1/C1/C1b/C1c/C2/L0/L1/L1a/L1b/L1c/L3 quantify over `dom(C)`, `dom(L)`, or `dom(M)`, all empty at `Σ₀`. C0 and L12 quantify over transitions `Σ → Σ'`, vacuous at `Σ₀` until the first transition fires. Three invariants are non-vacuous but trivially satisfied at `Σ₀`:

- **L14** (`dom(C) ∩ dom(L) = ∅`): at `Σ₀`, both stores empty, so `∅ ∩ ∅ = ∅` — trivially true.
- **L-fin** (`|dom(L)| < ∞`): `|∅| = 0 < ∞` — trivially true.
- **C-fin** (`|dom(C)| < ∞`): `|∅| = 0 < ∞` — trivially true.

*Derived lemmas at Σ₀.* ChainPrefixExtension (transition-independent in conclusion, but quantified over `d ∈ dom(M)`) holds vacuously at `Σ₀` since `dom(M₀) = ∅`. ChainMembershipForOrigin holds vacuously: for every `d` (vacuous since `dom(M₀) = ∅`), both `dom(C₀) ∩ {a' : origin(a') = d} = ∅ ∩ … = ∅ = {t_1, …, t_0}` witnessing `m_d = 0` and similarly `n_d = 0` for the link clause. StoreT4Validity holds vacuously over the empty stores. FirstEmissionFreshness has no firing context at `Σ₀` (no K.α or K.λ event has fired), so the predicate ranges over no events. The other chain-indexed lemmas (ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains) are state-independent and hold for every T10a-discipline-satisfying chain — including the vacuously empty family of sub-allocator chains at `Σ₀`.

The base case holds.

**Inductive step.** Per (invariant, transition):

| Invariant | K.σ | K.α | K.λ |
|---|---|---|---|
| **M0** (DocumentTumblerWellFormed) | Discharged at new key: precondition pins `ValidAddress(d) ∧ zeros(d) = 2` | Preserved: `M` in frame | Preserved: `M` in frame |
| **M1** (ArrangementMonotonicity) | Discharged: effect extends `dom(M)` by union | Preserved: `M` in frame | Preserved: `M` in frame |
| **C0** (ContentImmutability) | Preserved: `C` in frame | Discharged: effect extends `dom(C)` at fresh `a` with value `v`; value at existing keys unaltered (definitional in effect clause) | Preserved: `C` in frame |
| **C1** (ContentElementLevel) | Preserved: `C` in frame | Discharged at new key: precondition pins `zeros(a) = 3` | Preserved: `C` in frame |
| **C1b** (ContentElementFieldDepth) | Preserved: `C` in frame (`E(·)` is T4b's structural projection on the address alone, depending on no state component, so prior keys' `#E(a) ≥ 2` transfers unchanged under domain-equality of `C`) | Discharged at new key: precondition pins `#E(a) ≥ 2` | Preserved: `C` in frame |
| **C1c** (ContentAllocatorConformance) | Preserved: `C` in frame | Discharged at new key via the structural inc-chain (see *C1c chain exhibition* below — first-emit and subsequent-emit cases) | Preserved: `C` in frame |
| **C2** (ContentScopedAllocation) | Preserved: vacuously (no new content); for prior keys `a ∈ dom(C)`, `origin(a) ∈ dom(M) ⊆ dom(M')` (`C` in frame, M1 extends `dom(M)`) | Discharged at new key: precondition pins `origin(a) = d ∧ d ∈ dom(M)`; preserved at prior keys (`origin(·)` is structural, M1 extends `dom(M)`) | Preserved: `C` in frame; prior keys preserved by M1 |
| **L0** (SubspacePartition) | Preserved: `L`, `C` in frame | Preserved on L-clause (`L` in frame); discharged at new key on C-clause via `E(a)₁ = s_C`. *First-emit branch:* the precondition is structurally automatic, since SubAllocatorAxiom.FirstEmission pins `a = [d.0.s_C.1]` with `E(a)₁ = s_C` by inspection. *Subsequent-emit branch:* the precondition is automatically satisfied at `a = inc(a_prev, 0)` because DisjointSubAllocatorChains (a chain-indexed lemma) guarantees every element of `A_C(d)` has `E(·)₁ = s_C`; since `a ∈ A_C(d)` by ChainDiscipline's closure under `inc(·, 0)` applied to `a_prev ∈ A_C(d)` (the latter from ChainMembershipForOrigin at `Σ`), `E(a)₁ = s_C` follows without a caller-supplied choice | Discharged at new key on L-clause via `E(ℓ)₁ = s_L`. *First-emit branch:* the precondition is structurally automatic, since SubAllocatorAxiom.FirstEmission pins `ℓ = [d.0.s_L.1]` with `E(ℓ)₁ = s_L` by inspection. *Subsequent-emit branch:* the precondition is automatically satisfied at `ℓ = inc(ℓ_prev, 0)` because DisjointSubAllocatorChains (a chain-indexed lemma) guarantees every element of `A_L(d)` has `E(·)₁ = s_L`; since `ℓ ∈ A_L(d)` by ChainDiscipline's closure under `inc(·, 0)` applied to `ℓ_prev ∈ A_L(d)` (the latter from ChainMembershipForOrigin at `Σ`), `E(ℓ)₁ = s_L` follows without a caller-supplied choice. Preserved on C-clause (`C` in frame) |
| **L1** (LinkElementLevel) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `zeros(ℓ) = 3` |
| **L1a** (LinkScopedAllocation) | Preserved: vacuously (no new link); for prior keys `ℓ ∈ dom(L)`, `origin(ℓ) ∈ dom(M) ⊆ dom(M')` (M1 extends `dom(M)`) | Preserved: `L` in frame; prior keys preserved by M1 | Discharged at new key: precondition pins `origin(ℓ) = d ∧ d ∈ dom(M)`; prior keys preserved by M1 |
| **L1b** (LinkElementFieldDepth) | Preserved: `L` in frame (`E(·)` is T4b's structural projection on the address alone, depending on no state component, so prior keys' `#E(ℓ) ≥ 2` transfers unchanged under domain-equality of `L`) | Preserved: `L` in frame (same reasoning) | Discharged at new key: precondition pins `#E(ℓ) ≥ 2` |
| **L1c** (LinkAllocatorConformance) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key via the structural inc-chain (see *L1c chain exhibition* below — first-emit and subsequent-emit cases) |
| **L3** (NEndsetStructure) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `|L(ℓ)| ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` |
| **L12** (LinkImmutability) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: effect extends `dom(L)` at fresh `ℓ`; value at existing keys unaltered (definitional) |
| **L14** (StoreDisjointness) | Preserved by frame: `C` and `L` are both in frame, so `dom(C') = dom(C)` and `dom(L') = dom(L)`, and IH-L14 (`dom(C) ∩ dom(L) = ∅`) transfers directly to Σ'. No new key in either store; no fresh discharge required | Discharged at the new key `a`. At prior keys (`a' ∈ dom(C)`, `ℓ ∈ dom(L)`) IH-L14 supplies disjointness by frame on `L` (`L' = L`). For pairs `(a, ℓ)` with `ℓ ∈ dom(L) = dom(L')`: L0's C-clause at `a` is discharged from K.α's precondition `E(a)₁ = s_C`; L0's L-clause at `ℓ` is inherited from IH-L0 at Σ; SC-NEQ supplies `s_C ≠ s_L`; StoreT4Validity at `a` is discharged from ChainElementT4Validity applied to `A_C(d)` (every chain element is T4-valid by chain induction grounded at FirstEmission's T4-valid first emission, so the conclusion holds at both the first-emit branch where `a = t_1` and at any subsequent-emit branch where `a` is a later chain element of `A_C(d)`); StoreT4Validity at `ℓ` is inherited from IH-StoreT4Validity at Σ; C1 supplies `zeros(a) = 3` from K.α's precondition; L1 supplies `zeros(ℓ) = 3` from IH-L1 at Σ. T7 (FirstElementFieldDistinction, ASN-0034) closes: differing `E(·)₁` ⟹ `a ≠ ℓ` | Discharged at the new key `ℓ`, symmetric to K.α with content↔link. At prior keys IH-L14 supplies disjointness by frame on `C` (`C' = C`). For pairs `(a, ℓ)` with `a ∈ dom(C) = dom(C')`: L0's L-clause at `ℓ` is discharged from K.λ's precondition `E(ℓ)₁ = s_L`; L0's C-clause at `a` is inherited from IH-L0 at Σ; StoreT4Validity at `ℓ` is discharged from ChainElementT4Validity applied to `A_L(d)` (every chain element is T4-valid by chain induction grounded at FirstEmission's T4-valid first emission, so the conclusion holds at both the first-emit branch where `ℓ = s_1` and at any subsequent-emit branch where `ℓ` is a later chain element of `A_L(d)`); StoreT4Validity at `a` is inherited from IH-StoreT4Validity at Σ; L1 supplies `zeros(ℓ) = 3` from K.λ's precondition; C1 supplies `zeros(a) = 3` from IH-C1 at Σ. T7 closes |
| **L-fin** (LinkStoreFiniteness) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: `|dom(L')| = |dom(L)| + 1`; finiteness closed under +1 |
| **C-fin** (ContentStoreFiniteness) | Preserved: `C` in frame | Discharged: `|dom(C')| = |dom(C)| + 1`; finiteness closed under +1 | Preserved: `C` in frame |

*Lemma preservation across transitions.* The transition-indexed lemmas additionally discharged at each step:

| Lemma | K.σ | K.α | K.λ |
|---|---|---|---|
| **ChainMembershipForOrigin** | Preserved: `C`, `L` in frame; for the freshly registered `d_new`, both intersection sets `dom(C') ∩ {a' : origin(a') = d_new}` and `dom(L') ∩ {ℓ' : origin(ℓ') = d_new}` are `∅`, witnessing `m_{d_new} = n_{d_new} = 0` (see lemma proof above) | Preserved at `d' ≠ d` by frame on `dom(C)|_{d'}`; at `d` extended at chain index `m_d + 1` (first-emit by FirstEmission, subsequent-emit by ChainDiscipline + ChainEnumerationInjectivity placing `a = t_{m_d + 1}`); link clause unchanged by frame on `dom(L)` | Symmetric to K.α (content↔link); see lemma proof above |
| **StoreT4Validity** | Preserved: `C`, `L` in frame, so the existing T4-validity of every entry transfers; no new key | Preserved at prior keys (`C` in frame); at the new key `a`, T4-validity from ChainElementT4Validity applied to `A_C(d)` (every chain element is T4-valid by chain induction grounded at FirstEmission's T4-valid first emission, covering both first-emit and subsequent-emit branches) | Symmetric (content↔link); at the new key `ℓ`, ChainElementT4Validity applied to `A_L(d)` (every chain element is T4-valid by chain induction grounded at FirstEmission's T4-valid first emission, covering both first-emit and subsequent-emit branches) |
| **FirstEmissionFreshness** | No firing context: K.σ does not commit a content/link first emission | Discharged at the K.α event when the first-emit predicate fires (see lemma proof above): freshness against `dom(C)` via ChainPrefixExtension + ChainMembershipForOrigin + Cross-document disjointness + T10; freshness against `dom(L)` via L0 + SC-NEQ + StoreT4Validity + T7 | Symmetric to K.α (content↔link) |

The chain-indexed lemmas (ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension) are not state-dependent in their conclusions and require no per-transition discharge — their proofs above establish them once-and-for-all from the structural Definition.

*C1c chain exhibition.* The substrate's C1c is "every content address has a structural inc-chain from its home document." For `K.α`'s discharge, two sub-cases:

**First-emit case** (`a = [d.0.s_C.1]`, predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`). The structural inc-chain witnessing C1c is two inc steps from `d`:

  `(t₀, t₁, t₂)` where `t₀ = d`, `t₁ = inc(d, 2) = b_C(d)`, `t₂ = inc(b_C(d), 1) = [d.0.s_C.1] = a`

Per-step admissibility:

- `t₁ = inc(d, 2)`: TA5a (IncrementPreservesT4, ASN-0034) at `k = 2` requires `zeros(d) ≤ 2`; by M0, `zeros(d) = 2`, satisfied — hence `t₁` is T4-valid. TA5(d) at `k = 2` gives the structural form: `zeros(t₁) = 2 + (2 − 1) = 3` and `#t₁ = #d + 2`. The value at position `#d + 2` is `1 = s_C` (per SubspaceConventionAxiom), establishing `E(t₁)₁ = s_C` and `#E(t₁) = 1`.
- `t₂ = inc(b_C(d), 1)`: TA5a at `k = 1` applies unconditionally on T4-valid inputs (no zero-count side condition), so `t₂` is T4-valid given `t₁` T4-valid. TA5(d) at `k = 1` gives the structural form: the new component appended at position `#b_C(d) + 1` is `1`, so `zeros(t₂) = 3 + 0 = 3` (k = 1 introduces no new zero), with `#E(t₂) = 2` and `E(t₂)₁ = s_C` inherited from `t₁` per TA5(b).

C1c's strengthened clauses: `k₁ = 2` by construction (step 1 above); `n = 2 ≥ 1` ✓; `#t₁ = #d + 2 > #d` and `#t₂ = #d + 3 > #d`, so `(A i : 1 ≤ i ≤ 2 : #tᵢ > #origin(a))` holds.

**Subsequent-emit case** (`a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`, predicate `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`). Let `a_prev = max{a' ∈ dom(C) : origin(a') = d}`. By the inductive hypothesis on C1c, `a_prev` has a structural inc-chain `(t₀, …, t_n)` with `t₀ = d`, `t_n = a_prev`, `k₁ = 2`, and `(A i : 1 ≤ i ≤ n : #tᵢ > #d)`. The chain for `a` extends this by one step: `(t₀, …, t_n, t_{n+1})` with `t_{n+1} = inc(t_n, 0) = inc(a_prev, 0) = a`. Per-step admissibility of the new step `t_{n+1} = inc(a_prev, 0)`: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `t_{n+1}` is T4-valid given `a_prev` T4-valid (the latter supplied by ChainElementT4Validity applied to `A_C(d)`'s chain at `a_prev`); TA5(c) at `k = 0` gives the structural form (length preservation, single-position modification at `sig(a_prev)`). Within-chain freshness against the rest of `A_C(d)`'s chain is discharged by ChainEnumerationInjectivity applied to `(a_prev, a)`, with both indices established to inhabit `A_C(d)` by ChainMembershipForOrigin (`a_prev ∈ A_C(d)` from the inductive hypothesis applied at `Σ`) and SubAllocatorAxiom.ChainDiscipline's closure under `inc(·, 0)` (`a = inc(a_prev, 0) ∈ A_C(d)`); cross-document collisions with other documents' content chains are ruled out by the Cross-document disjointness lemma. C1c's strengthened clauses on the extended chain: `k₁ = 2` is inherited unchanged from the IH chain; `n + 1 ≥ 1` ✓; for the new step, TA5(c) gives `#t_{n+1} = #t_n > #d` (so the universal `#tᵢ > #d` extends to `i = n + 1`).

*L1c chain exhibition.* The substrate's L1c is "every link address has a structural inc-chain from its home document." For `K.λ`'s discharge, two sub-cases:

**First-emit case** (`ℓ = [d.0.s_L.1]`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`). The structural inc-chain witnessing L1c is three inc steps from `d`:

  `(t₀, t₁, t₂, t₃)` where `t₀ = d`, `t₁ = inc(d, 2) = b_C(d)`, `t₂ = inc(b_C(d), 0) = b_L(d)`, `t₃ = inc(b_L(d), 1) = [d.0.s_L.1] = ℓ`

Per-step admissibility:

- `t₁ = inc(d, 2)`: TA5a (IncrementPreservesT4, ASN-0034) at `k = 2` requires `zeros(d) ≤ 2`; by M0, `zeros(d) = 2`, satisfied — hence `t₁` is T4-valid. TA5(d) at `k = 2` gives the structural form: `zeros(t₁) = 2 + (2 − 1) = 3`.
- `t₂ = inc(b_C(d), 0)`: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `t₂` is T4-valid given `b_C(d)` T4-valid. TA5(c) at `k = 0` gives the structural form: length is preserved and the sibling component is advanced from `s_C` to `s_L`. By SubspaceConventionAxiom, `s_C = 1` and `s_L = 2`, so `inc([d.0.1], 0) = [d.0.2] = b_L(d)`. This step's correctness depends substantively on `s_L = s_C + 1`; the SubspaceConventionAxiom underwrites it.
- `t₃ = inc(b_L(d), 1)`: TA5a at `k = 1` applies unconditionally on T4-valid inputs (no zero-count side condition), so `t₃` is T4-valid given `b_L(d)` T4-valid. TA5(d) at `k = 1` gives the structural form: `zeros(t₃) = 3 + 0 = 3` (k = 1 introduces no new zero), with `#E(t₃) = 2`.

L1c's strengthened clauses: `k₁ = 2` by construction (step 1 above); `n = 3 ≥ 1` ✓; `#t₁ = #d + 2 > #d`, `#t₂ = #d + 2 > #d`, `#t₃ = #d + 3 > #d`, so `(A i : 1 ≤ i ≤ 3 : #tᵢ > #origin(ℓ))` holds.

Note that the C1c first-emit chain has *two* inc steps (`d → b_C(d) → a`) while the L1c first-emit chain has *three* (`d → b_C(d) → b_L(d) → ℓ`) — they are not parallel chains differing only in a single-step substitution. The link chain must traverse the additional `inc(b_C(d), 0) = b_L(d)` step because the link subspace anchor sits one sibling-component beyond the content subspace anchor.

**Subsequent-emit case** (`ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`). Let `ℓ_prev = max{ℓ' ∈ dom(L) : origin(ℓ') = d}`. By the inductive hypothesis on L1c, `ℓ_prev` has a structural inc-chain `(t₀, …, t_n)` with `t₀ = d`, `t_n = ℓ_prev`, `k₁ = 2`, and `(A i : 1 ≤ i ≤ n : #tᵢ > #d)`. The chain for `ℓ` extends this by one step: `(t₀, …, t_n, t_{n+1})` with `t_{n+1} = inc(t_n, 0) = inc(ℓ_prev, 0) = ℓ`. Per-step admissibility of the new step `t_{n+1} = inc(ℓ_prev, 0)`: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `t_{n+1}` is T4-valid given `ℓ_prev` T4-valid (the latter supplied by ChainElementT4Validity applied to `A_L(d)`'s chain at `ℓ_prev`); TA5(c) at `k = 0` gives the structural form (length preservation, single-position modification at `sig(ℓ_prev)`). Within-chain freshness against the rest of `A_L(d)`'s chain is discharged by ChainEnumerationInjectivity applied to `(ℓ_prev, ℓ)`, with both indices established to inhabit `A_L(d)` by ChainMembershipForOrigin (`ℓ_prev ∈ A_L(d)` from the inductive hypothesis applied at `Σ`) and SubAllocatorAxiom.ChainDiscipline's closure under `inc(·, 0)` (`ℓ = inc(ℓ_prev, 0) ∈ A_L(d)`); cross-document collisions with other documents' link chains are ruled out by the Cross-document disjointness lemma. L1c's strengthened clauses on the extended chain: `k₁ = 2` is inherited unchanged from the IH chain; `n + 1 ≥ 1` ✓; for the new step, TA5(c) gives `#t_{n+1} = #t_n > #d` (so the universal `#tᵢ > #d` extends to `i = n + 1`).


## Properties Introduced

| ID | Name | Status | Source |
|---|---|---|---|
| M0 | DocumentTumblerWellFormed | INV | Substrate, established at K.σ (precondition pins `ValidAddress(d) ∧ zeros(d) = 2` at the new key); preserved at K.α/K.λ by frame on `M` |
| M1 | ArrangementMonotonicity | INV | Substrate, established at K.σ by union extension `dom(M') = dom(M) ∪ {d}`; preserved at K.α/K.λ by frame on `M` |
| C0 | ContentImmutability | INV | Substrate, restated from ASN-0036's S0/S1; established at K.α (effect extends `dom(C)` with new pair and leaves existing values unchanged); preserved at K.σ/K.λ by frame on `C` |
| C1 | ContentElementLevel | INV | Substrate, restated from ASN-0036's S7b; established at K.α (precondition pins `zeros(a) = 3` at the new key); preserved at K.σ/K.λ by frame on `C` |
| C1b | ContentElementFieldDepth | INV | Substrate, restated from ASN-0036's S7c (content-side analog of L1b); established at K.α (precondition pins `#E(a) ≥ 2` at the new key); preserved at K.σ/K.λ by frame on `C` |
| C1c | ContentAllocatorConformance | INV | Substrate, content-side analog of L1c, stated in parallel form (including `k₁ = 2` and `#tᵢ > #origin(a)` clauses); established at K.α via the C1c chain exhibition (first-emit chain has two steps `(d → b_C(d) → a)` with `k₁ = 2`, `k₂ = 1` and lengths `#d → #d + 2 → #d + 3`, all strictly exceeding `#d`; subsequent-emit extends a length-monotone chain by `inc(·, 0)` and inherits `k₁ = 2`). The first-emit gap is closed by SubAllocatorAxiom.FirstEmission, subsequent-emit by SubAllocatorAxiom.ChainDiscipline (ChainEnumerationInjectivity); preserved at K.σ/K.λ by frame on `C` |
| C2 | ContentScopedAllocation | INV | Substrate, content-side analog of L1a; established at K.α (precondition pins `origin(a) = d ∧ d ∈ dom(M)` at the new key); preserved at K.σ/K.λ by frame on `C` and M1's monotonicity of `dom(M)` |
| L0 | SubspacePartition | INV | L-clause from ASN-0043; C-clause added here. Established at K.α (C-clause, via `E(a)₁ = s_C` precondition) and K.λ (L-clause, via `E(ℓ)₁ = s_L` precondition); preserved at K.σ by frame on both `C` and `L` |
| L1 | LinkElementLevel | INV | ASN-0043; established at K.λ (precondition pins `zeros(ℓ) = 3` at the new key); preserved at K.σ/K.α by frame on `L` |
| L1a | LinkScopedAllocation | INV | ASN-0043 (refactored: `E_doc` → `dom(M)`); established at K.λ (precondition pins `origin(ℓ) = d ∧ d ∈ dom(M)` at the new key); preserved at K.σ/K.α by frame on `L` and M1's monotonicity of `dom(M)` |
| L1b | LinkElementFieldDepth | INV | ASN-0043; established at K.λ (precondition pins `#E(ℓ) ≥ 2` at the new key); preserved at K.σ/K.α by frame on `L` |
| L1c | LinkAllocatorConformance | INV | ASN-0043, restated verbatim including the `k₁ = 2` and `#tᵢ > #origin(ℓ)` clauses. Established at K.λ via the L1c chain exhibition (first-emit chain has three steps `(d → b_C(d) → b_L(d) → ℓ)` with `k₁ = 2`, `k₂ = 0`, `k₃ = 1` and monotonically increasing lengths `#d → #d + 2 → #d + 2 → #d + 3`, all strictly exceeding `#d`; subsequent-emit extends a length-monotone chain by `inc(·, 0)` and inherits `k₁ = 2` from the prior chain). The first-emit gap is closed by SubAllocatorAxiom.FirstEmission, subsequent-emit by SubAllocatorAxiom.ChainDiscipline (ChainEnumerationInjectivity); preserved at K.σ/K.α by frame on `L` |
| L3 | NEndsetStructure | INV | ASN-0043; established at K.λ (precondition pins `|L(ℓ)| ≥ 3 ∧ (e₃) ≠ ∅`); preserved at K.σ/K.α by frame on `L` |
| L12 | LinkImmutability | INV | ASN-0043; established at K.λ (effect extends `dom(L)` with new pair and leaves existing values unchanged); preserved at K.σ/K.α by frame on `L` |
| L14 | StoreDisjointness | INV (derived) | L0 + SC-NEQ + StoreT4Validity + T7 |
| L-fin | LinkStoreFiniteness | INV (derived) | Inductively from `Σ₀.L = ∅` + K.λ |
| C-fin | ContentStoreFiniteness | INV (derived) | Inductively from `Σ₀.C = ∅` + K.α |
| T10a-discipline-satisfying chain | T10a-discipline-satisfying chain | DEF | Structural-only definition of a sequence `(t_1, t_2, …)` satisfying FirstElementValidity (`t_1` T4-valid) and SiblingRecurrence (`t_{n+1} = inc(t_n, 0)`). No reference to allocator-tree membership. Consumed by every chain lemma below and by SubAllocatorAxiom.ChainDiscipline. |
| SubAllocatorAxiom | ContentLinkSubAllocatorExistence | AXIOM | Three clauses: Exists, FirstEmission (structural form only — `[d.0.s_C.1]` resp. `[d.0.s_L.1]`, both T4-valid by inspection), ChainDiscipline (sub-allocator chains are T10a-discipline-satisfying chains per the Definition above). The earlier-draft *Disjointness* and *FirstEmission's freshness conclusion* clauses are restated below as derived lemmas DisjointSubAllocatorChains and FirstEmissionFreshness, not retained as axiom content. |
| ChainElementT4Validity | ChainElementT4Validity | LEMMA | Every element of a T10a-discipline-satisfying chain is T4-valid. Proved by chain induction: base from FirstElementValidity, step from TA5a (unconditional at `k = 0`). Consumed at ChainUniformZeroCount's step, ChainPrefixExtension's step, DisjointSubAllocatorChains, StoreT4Validity, FirstEmissionFreshness, and K.α/K.λ subsequent-emit cross-subspace freshness derivations. |
| ChainUniformLength | ChainUniformLength | LEMMA | All elements of a T10a-discipline-satisfying chain share the length of `t_1`. Proved by chain induction using TA5(c) (length preservation). Mirrors T10a.1 (UniformSiblingLength, ASN-0034) but cast against the structural Definition's preconditions alone — no T4-validity required. |
| ChainEnumerationInjectivity | ChainEnumerationInjectivity | LEMMA | The enumeration of a T10a-discipline-satisfying chain is strictly increasing under T1; hence `n ↦ t_n` is injective and order-preserving in both directions. Proved using TA5(a) + T1(a)/T1(c) on the recurrence — no T4-validity required. Mirrors T10a.7 (EnumerationInjectivity, ASN-0034). Consumed at ChainMembershipForOrigin's subsequent-emit step and at K.α/K.λ subsequent-emit within-document freshness derivations. |
| ChainUniformZeroCount | ChainUniformZeroCount | LEMMA | All elements of a T10a-discipline-satisfying chain share the zero count of `t_1`. Proved by chain induction: base trivial, step uses ChainElementT4Validity + TA5-SigValid + T4's positive-endpoint clause + TA5(b)/(c). Mirrors T10a.8 (UniformSiblingZeroCount, ASN-0034) but substitutes ChainElementT4Validity for T10a.4 (tree-embedding) at the chain-wide T4-validity step. |
| DisjointSubAllocatorChains | DisjointSubAllocatorChains | LEMMA | Addresses produced by `A_C(d)` satisfy `E(·)₁ = s_C`; addresses produced by `A_L(d)` satisfy `E(·)₁ = s_L`. By SC-NEQ, the two chains' images are disjoint. Proved using FirstEmission + ChainUniformLength + ChainElementT4Validity + TA5-SigValid + TA5(b)/(c). Replaces the former SubAllocatorAxiom.Disjoint axiom clause. |
| ChainPrefixExtension | ChainPrefixExtension | LEMMA | Every chain element extends its anchor under Prefix: `b_C(d) ≼ t` for `t ∈ A_C(d)`, `b_L(d) ≼ t` for `t ∈ A_L(d)`. Proved by chain induction: base from FirstEmission's concrete forms `[d.0.s_C.1]` and `[d.0.s_L.1]`; step uses ChainUniformLength + ChainElementT4Validity + TA5-SigValid + TA5(b)/(c) — no nested induction (`t_n`'s T4-validity is supplied as a complete prior fact by ChainElementT4Validity). Consumed in cross-document freshness derivations (K.α/K.λ first-emit and subsequent-emit) and in the FirstEmissionFreshness lemma. |
| ChainMembershipForOrigin | ChainMembershipForOrigin | LEMMA | Inductive invariant in *contiguous-prefix form* at every reachable state: `dom(C) ∩ {a' : origin(a') = d} = {t₁, …, t_{m_d}}` is a contiguous initial segment of `A_C(d)` (mirror for `L`). The subset inclusion `dom(C) ∩ {a' : origin(a') = d} ⊆ A_C(d)` is the weaker corollary. Proved by induction over transitions using SubAllocatorAxiom.FirstEmission (first-emit branches placing `t₁`) and ChainDiscipline + ChainEnumerationInjectivity (subsequent-emit branches placing `t_{m_d + 1} = inc(t_{m_d}, 0)`). Licenses application of ChainEnumerationInjectivity to `(a_prev, a)` and `(ℓ_prev, ℓ)` in K.α/K.λ subsequent-emit cases; the contiguous-prefix form matches ASN-0040's B1 (ContiguousPrefix). |
| StoreT4Validity | StoreT4Validity | LEMMA (derived) | Derived from ChainMembershipForOrigin + ChainElementT4Validity: every entry of `dom(C) ∪ dom(L)` inhabits a sub-allocator chain whose every element is T4-valid. Used to discharge T7's precondition in the L14 derivation and in the FirstEmissionFreshness lemma against `dom(L)`. |
| FirstEmissionFreshness | FirstEmissionFreshness | LEMMA (derived) | Derived from the first-emit predicate + L0 + ChainPrefixExtension + ChainMembershipForOrigin + StoreT4Validity + Cross-document disjointness + SC-NEQ + T7 + ChainElementT4Validity. At every K.α (resp. K.λ) event firing the first-emit predicate, the first emission `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`) is fresh against `dom(C) ∪ dom(L)`. Replaces the former freshness conclusion of SubAllocatorAxiom.FirstEmission. Consumed at K.α/K.λ first-emit precondition discharge. |
| Cross-doc disjointness | T10 + Prefix + M0 lemma | LEMMA | Derived from M0 + T4 + T10 + Prefix (ASN-0034); T4's zero-count argument underwrites the Case A divergence step. Case B (prefix-incomparable) extracts a position-divergence witness `k ≤ min(#d₁, #d₂)` by sub-case analysis on length (B.i: `#d₁ ≤ #d₂`; B.ii: `#d₂ < #d₁`), since the joint `⋠`-conjunction can be satisfied by length alone on one side in asymmetric-length sub-cases. The lemma operates directly at document-level anchors (T4-validity + zeros = 2) rather than through T10a.2/T10a.5, because the sub-allocator-pair disjointness it establishes is between document-level prefixes, not between sub-allocator allocation events. |
| SubspaceConventionAxiom | FixedSubspaceIdentifiers | AXIOM | Substrate commitment: `s_C = 1 ∧ s_L = 2`; pinned by Nelson (LM 4/30–4/31) and Gregory (`xanadu.h:144–146`, `granf2.c:162`, `do2.c:94`). Underwrites L14 derivation and the L1c chain exhibition. |
| SequentialTransitionAxiom | SequentialAtomicTransitions | AXIOM | Substrate commitment: `Σ → Σ'` is atomic, uninterruptible, totally ordered. |
| K.σ | DocumentRegistration | OP | Substrate-level document introduction into `dom(M)` |
| K.α | ContentAllocation | OP | Substrate-level content emission |
| K.λ | LinkAllocation | OP | Substrate-level link emission |


## Open Questions

- *Link withdrawal.* The substrate admits no withdrawal of `dom(L)` entries (L12 enforces both domain persistence `a ∈ dom(L) ⟹ a ∈ dom(L')` and value-equality `L'(a) = L(a)` across every transition). Nelson's diagram on LM 4/9 ("Technical Contents of a Document") places "DELETED LINKS" as a first-class subdivision — "*not currently addressable, awaiting historical backtrack functions, may remain included in other versions*" — which means the link's record is *preserved* in the docuverse, not removed: the address remains assigned and the underlying content persists, with withdrawal a bookkeeping marker over the preserved record. Three distinct composition paths are admissible from this substrate; the present substrate forecloses none of them and commits to none:

  - *(a) Arrangement-layer withdrawal (preserves L12 as stated).* In udanax-green the only operation resembling withdrawal is `DELETEVSPAN` on the link's V-position in its home document's POOM; this removes the arrangement-side reference (Σ.M(d) loses a V→I mapping) while leaving the link store entirely untouched. The link orgl persists, the spanfilade entries persist, and the link remains discoverable via `find_links` and followable via `follow_link`. A higher-layer ASN that introduces arrangement-mutation primitives (`K.μ⁻` or analogues) can model Nelson's withdrawal as POOM-side removal *without modifying* `dom(L)` or `L(·)`, so L12 holds unchanged.
  - *(b) Value-level tombstone (requires weakening L12's value-equality clause).* A higher-layer ASN that admits a distinguished tombstone value in `Link` (e.g., `Link* = Link ⊎ {⊥_tomb}`) and permits a transition `L(a) ↦ ⊥_tomb` would violate L12's value-equality `L'(a) = L(a)` — though it preserves L12's domain-persistence clause `a ∈ dom(L) ⟹ a ∈ dom(L')`. Such an extension is *not* a compositional extension of this substrate: it replaces L12 with a weaker invariant (e.g., L12-domain-only). Any higher-layer ASN taking this route must restate L12 explicitly and re-verify every downstream consumer that depends on value-equality.
  - *(c) Embedded tombstone marker (preserves L12 as stated).* A tombstone marker encoded *within* `Link`'s endset structure — e.g., a designated type endset value `Θ_tomb` reserved for withdrawn links, with the link's value `L(a) = (F, G, Θ_tomb)` committed at creation rather than at withdrawal — satisfies L12 verbatim. Withdrawal in this reading is not a transition on `L(a)` but a query-time interpretation of an already-immutable value. This path is the most conservative extension of the substrate.

  The substrate makes no commitment among (a), (b), (c). Closing the gap with operational semantics that match Nelson's LM 4/9 description is deferred to a higher-layer ASN; the choice among the three paths is that ASN's load-bearing design decision.

- *Higher-arity link discipline.* L3 admits arbitrary `N ≥ 3` (matching ASN-0043's foundation form). The substrate enforces no upper bound on arity and no constraints on the semantics of slots beyond the type endset at slot 3. Higher-layer ASNs may impose further constraints on arity, slot interpretation, or relations between slots if needed for specific link semantics — for example, a layer that fixes the StandardTriple convention as a structural commitment rather than a notational default.

- *Document address discipline.* K.σ's precondition is structural-only (`ValidAddress(d) ∧ zeros(d) = 2 ∧ d ∉ dom(M)`). The substrate admits any T4-valid document-level tumbler. Nelson's hierarchical baptism (where node-account-document chains are enforced) is a higher-layer commitment; a higher-layer document-introduction primitive tightens K.σ's precondition with the additional discipline.

- *Concurrency.* `K.σ`, `K.α`, and `K.λ` are stated as atomic transitions; the discipline for concurrent emission across multiple allocators is not addressed at this layer.

- *Sub-allocator stratification beyond `A_C(d)` and `A_L(d)`.* Future subspace identifiers `s ≥ 3` would require parallel sub-allocators; the present axiom commits to exactly two (content and link).

- *Arrangement extension primitives.* The substrate fixes `M(d) = ∅` at K.σ-time and never re-modifies. Higher-layer arrangement-extension primitives extend arrangements; downstream ASNs needing arrangement mutation depend on those higher-layer primitives.
