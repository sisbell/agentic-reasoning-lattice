# ASN-0093: Allocation Substrate

A Xanadu-style substrate maintains three address-keyed stores: the content store, the link store, and the document-arrangement function. Each store is grown by an allocation primitive that extends the store's domain at a fresh key with structural invariants on the new entry. ASN-0043 introduced the link store and its structural invariants (L0/L1/L1a/L1b/L1c/L3/L12/L14); ASN-0036 introduced the content store and arrangement function. The factoring is downward from a fuller transition model: the central rewrite is one notational substitution — `E_doc` (the set of entities classified `IsDocument`) is replaced by `dom(M)` (the set of allocated documents in the arrangement function), so the substrate-layer claims can be stated without reference to the entity set. Beyond that substitution, the substrate adds content-side commitments absent from the inherited models — C1b (content element-field depth, with no ASN-0036 counterpart), the C-clause of L0 (content subspace partition), and C1c (content allocator conformance) — stated here as substrate-level invariants rather than inherited from ASN-0036/0043. Inherited link-side and arrangement-side claims discharge from their counterparts; the added content-side invariants are proved within this note. Higher-layer transition models fold both into a larger state model that also tracks entity allocation and arrangement provenance — `Σ = (C, L, E, M, R)` — and supply the operational primitives for the full state.

This note extracts the *allocation-substrate* layer: the three allocation primitives (K.σ, K.α, K.λ) and the structural invariants on `(Σ.C, Σ.L, Σ.M)` they preserve. The substrate requires no commitment to `Σ.E` (the entity set) or `Σ.R` (the provenance relation). Higher-layer concerns — arrangement mutation, entity stratification, provenance recording — are deferred to higher-layer ASNs that compose this substrate's primitives with additional disciplines.


## Scope

Downstream ASNs that operate on the link store without needing arrangement mutation, entity stratification, or provenance recording can cite this substrate directly. Downstream ASNs that need any of the deferred machinery cite a higher-layer transition model that itself depends on this substrate.

**Provided.** Three primitive operations and the structural invariants on `(C, L, M)` they preserve:

- **Operations:** `K.σ` (document registration), `K.α` (content allocation), `K.λ` (link allocation)
- **Invariants:** M0–M1 (arrangement-function shape), C0–C1c + C2 + C-fin (content store), L0–L14 + L-fin (link store)
- **Sub-allocator chains:** the content/link chains are the ASN-0040 sibling streams `A_C(d) = S(b_C(d), 1)`, `A_L(d) = S(b_L(d), 1)`
- **Chain disciplines (ASN-0040 citations):** ChainElementT4Validity (B6(a)), ChainUniformLength + ChainUniformZeroCount (SiblingStream postconditions / B5a), ChainEnumerationInjectivity (S0), ChainPrefixExtension (S1), DisjointSubAllocatorChains (B7)
- **Transition-indexed lemmas:** ChainMembershipForOrigin (matching ASN-0040 B1), StoreT4Validity, FirstEmissionFreshness (proved by simultaneous induction with the stated invariants), Cross-document disjointness (ASN-0040 B7)
- **Derived chain identity:** ChainDiscipline — the sub-allocator chains coincide with the ASN-0040 sibling streams `S(b_·(d), 1)`; FirstEmission is a further derived lemma

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

**Terminology.** "Document" in this substrate means "element of `dom(M)`" — a purely structural notion (a T4-valid tumbler with `zeros = 2` registered into the arrangement function's domain). A higher-layer entity-hierarchy refinement (e.g., `IsDocument(e) ∧ e ∈ E`) is a strict tightening: every document admitted by that refinement is a substrate document, but the substrate admits documents that may not pass the higher-layer entity-hierarchy discipline.

The initial state is `Σ₀ = (∅, ∅, ∅)` — no content, no links, no documents.

**Subspace identifiers.** As in ASN-0043, `s_C` and `s_L` denote the content-subspace and link-subspace first-element-field values. This substrate commits to two axioms governing them:

- **SubspaceConventionAxiom (FixedSubspaceIdentifiers).** `s_C = 1 ∧ s_L = 2`. The distinctness `s_C ≠ s_L` (abbreviated **SC-NEQ**) and the sibling relation `s_L = s_C + 1` are immediate consequences. Pinned by Nelson's design (LM 4/30–4/31) and Gregory's `xanadu.h:144–146` / `granf2.c:162` / `do2.c:94`.

- **SequentialTransitionAxiom (SequentialAtomicTransitions).** Transitions `Σ → Σ'` are atomic, uninterruptible, and totally ordered: each transition evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step, with no intermediate state in which a transition has begun but not committed.


## Arrangement-function invariants

**M0 (DocumentTumblerWellFormed).**

  `(A d ∈ dom(M) :: ValidAddress(d) ∧ zeros(d) = 2)`

Every allocated document address is a T4-valid tumbler with exactly two zero components (i.e., a document-level address per S7d of ASN-0036). Discharged from `K.σ`'s precondition (below) and inductively across transitions.

**Definitional identification.** Throughout this substrate, `ValidAddress(d) ≡ d satisfies T4 (HierarchicalParsing, ASN-0034)` — the two terms are interchangeable. T4's four conjuncts are: `zeros(d) ≤ 3`, no adjacent zero components, `d[1] ≠ 0`, and `d[#d] ≠ 0`. The substrate uses `ValidAddress(d)` in operation preconditions and invariants for readability; any foundation claim whose precondition names T4-validity discharges that precondition directly via this identification.

**M1 (ArrangementMonotonicity).**

  `(A Σ → Σ' :: dom(M) ⊆ dom(M'))`

`dom(M)` is non-decreasing across all transitions. The substrate admits no transition that removes a document from `dom(M)`. Discharged from the frame conditions of every transition kind: `K.σ` extends `dom(M)` by one element; `K.α` and `K.λ` hold `M` in frame.


## Content store invariants

**C0 (ContentImmutability).**

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ (A a : a ∈ dom(C) : C'(a) = C(a)))`

Append-only with immutable values: `dom(C)` is non-decreasing, and no transition alters the value bound to an existing key. This is ASN-0036's S0/S1 restated for the substrate. Restated here (rather than inherited silently) so the substrate is self-contained — symmetric to L12 on the link side.

**C1 (ContentElementLevel).**

  `(A a ∈ dom(C) :: zeros(a) = 3)`

Every content address is an element-level tumbler. This is ASN-0036's S7b restated for the substrate. Discharged from `K.α`'s precondition.

**C1b (ContentElementFieldDepth).**

  `(A a ∈ dom(C) :: #E(a) ≥ 2)`

Every content address has at least two element-field components — the content-side analog of L1b. ASN-0036 carries no content-side `#E(a) ≥ 2` invariant, so this is added here as a substrate-level commitment (parallel to the L0 C-clause). Discharged from `K.α`'s precondition. Because `E(·)` is T4b's structural projection on the address alone (ASN-0034), depending on no state component, any transition that holds the store in frame leaves the keys unchanged and so transfers each prior key's `#E ≥ 2` unchanged; the same holds for L1b on the link side.

**C1c (ContentAllocatorConformance).** Every content address `a ∈ dom(C)` has a T10a-conforming step sequence from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `n ≥ 1`, `t₀ = origin(a)`, and `tₙ = a`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` zero-count side condition); additionally, `k₁ = 2` (the first step is a depth-2 increment off the document seed) and `(A i : 1 ≤ i ≤ n : #tᵢ > #origin(a))` (every intermediate length strictly exceeds the seed's). The chain witnesses `a`'s structural producibility from its home document via the content sub-allocator chain. This is the content-side analog of L1c, stated in parallel form.

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

Every link address has its home document allocated — the substrate form of the higher-layer `origin(a) ∈ E_doc` invariant under the intro's `E_doc` → `dom(M)` substitution.

**L1b (LinkElementFieldDepth).**

  `(A a ∈ dom(L) :: #E(a) ≥ 2)`

Every link address has at least two element-field components.

**L1c (LinkAllocatorConformance).** Every link address `ℓ ∈ dom(L)` has a *T10a-conforming step sequence* from its home document to `ℓ`: a finite sequence `(t₀, t₁, …, tₙ)` with `n ≥ 1`, `t₀ = origin(ℓ)`, and `tₙ = ℓ`, where each step `tᵢ = inc(tᵢ₋₁, kᵢ)` with `kᵢ ∈ {0, 1, 2}` satisfies T10a's per-step admissibility constraints (T4-validity preservation, including the `kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2` zero-count side condition); additionally, `k₁ = 2` (the first step is a depth-2 increment off the document seed) and `(A i : 1 ≤ i ≤ n : #tᵢ > #origin(ℓ))` (every intermediate length strictly exceeds the seed's). The chain witnesses `ℓ`'s structural producibility from its home document via the link sub-allocator. This is ASN-0043's L1c restated for the substrate. The L1c chain exhibition below establishes all clauses of this form at every K.λ event.

**L3 (NEndsetStructure).**

  `(A a ∈ dom(L) :: |L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |L(a)| : L(a).eᵢ ∈ Endset) ∧ L(a).e₃ ≠ ∅)`

Every link is a sequence of at least three endsets, with the type endset (slot 3) non-empty. This is ASN-0043's L3 restated for the substrate. The three-endset convention (slot 1 = from, slot 2 = to, slot 3 = type, written `(F, G, Θ)`) is preserved as the default form for worked examples and notational convenience but not enforced structurally — the substrate admits arbitrary arity `N ≥ 3`.

**L12 (LinkImmutability).**

  `(A Σ → Σ' : (A a : a ∈ dom(L) : a ∈ dom(L') ∧ L'(a) = L(a)))`

Once allocated, a link's address persists in `dom(L)` and its value is permanently fixed across all transitions.

**L14 (StoreDisjointness).**

  `dom(C) ∩ dom(L) = ∅`

Derived from L0 + SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034): every content address has `E(·)₁ = s_C`, every link address has `E(·)₁ = s_L`, and `s_C ≠ s_L`, so the domains are disjoint. (The discharge matrix records the StoreT4Validity dependency that supplies T7's T4-validity precondition.)

**L-fin (LinkStoreFiniteness).**

  `|dom(L)| < ∞`

The link store is finite at every reachable state. Discharged inductively from `Σ₀.L = ∅` and `K.λ`'s singleton extension.


## Address sub-allocators under documents

The content and link subspaces are organised as sibling element-field sub-allocators rooted at each document. For each `d ∈ dom(M)`, two element-field anchors sit immediately under `d`:

- `b_C(d) := [d.0.s_C]` — the **content sub-allocator anchor** (one-component element field with `E₁ = s_C`, `zeros = 3`, `#E = 1`)
- `b_L(d) := [d.0.s_L]` — the **link sub-allocator anchor** (one-component element field with `E₁ = s_L`, `zeros = 3`, `#E = 1`)

These anchors are *structurally producible* by T10a `inc` steps from `d`: `b_C(d) = inc(d, 2)` (TA5(d), `k = 2`) and `b_L(d) = inc(b_C(d), 0)` (TA5(c)). The anchors themselves are *not* in `dom(C) ∪ dom(L)` — content and link addresses have `#E ≥ 2` (C1; L1b above), and the anchors have `#E = 1` — so they inhabit the foundation carrier set `T` as structural witnesses without occupying any state component.

**Active sub-allocator chains.** Define: a sub-allocator chain `A_C(d)` (resp. `A_L(d)`) is *active at state* `Σ` iff `d ∈ dom(M)` at `Σ`. Concretely, "active" is the predicate under which K.α (resp. K.λ) admits the chain as the emission source for an address with `origin(·) = d`: the operation's precondition requires `d ∈ dom(M)`, which is exactly the activation condition. Permanence of activation — once `d ∈ dom(M)`, the chain stays active at every successor state — follows from M1 (ArrangementMonotonicity).

**Sub-allocator chains are ASN-0040 sibling streams (ChainDiscipline).** Each sub-allocator chain is an instance of ASN-0040's `SiblingStream`. Writing `S(p, k)` for the stream `c₁ = inc(p, k)`, `cₙ₊₁ = inc(cₙ, 0)` (SiblingStream, ASN-0040):

  `A_C(d) = S(b_C(d), 1)`  and  `A_L(d) = S(b_L(d), 1)`,

since each chain's first emission is `inc(anchor, 1)` — `t_1^C(d) = inc(b_C(d), 1) = [d.0.s_C.1]`, `t_1^L(d) = inc(b_L(d), 1) = [d.0.s_L.1]` — and successive elements advance by `inc(·, 0)`, coinciding by construction with the SiblingStream recurrence at `p = b_·(d)`, `k = 1`. The depth parameter is `1` in both cases, so the streams append no interior zero. In particular, each chain's closure under `inc(·, 0)` — used downstream to place a freshly emitted sibling `inc(a_prev, 0)` (resp. `inc(ℓ_prev, 0)`) onto the chain — is exactly the SiblingStream recurrence. We refer to this derived identity as **ChainDiscipline**.

Both anchors satisfy ASN-0040's `B6` (ValidDepth) at depth `1`: `b_C(d)` and `b_L(d)` are T4-valid with `zeros = 3` (one separator inserted at position `#d + 1` under M0's T4-valid, `zeros = 2` document `d`), depth `1 ∈ {1, 2}`, and `zeros(b_·(d)) + (1 − 1) = 3 ≤ 3`. Consequently every ASN-0040 result whose precondition is `B6(p, d)` — `B6(a)`'s stream-T4-validity conclusion, the `SiblingStream` postconditions, `S0` (StreamOrdering), `S1` (StreamPrefix), `B5a` (SiblingZerosPreservation), `B7` (NamespaceDisjointness), `B1` (ContiguousPrefix), and `B9` (UnboundedExtent) — applies to `A_C(d)` and `A_L(d)` directly. ASN-0040's `SiblingStream` is infinite, defined for every `n ≥ 1`, so a chain element exists at every index for the emission rule's pinning step to land on.

**Lemma (FirstEmission).** The first emission of each chain has a determinate structural form:
  - *Content chain first-emit:* `t_1^C(d) = inc(b_C(d), 1) = [d.0.s_C.1]` — `E(·)₁ = s_C`, `origin(·) = d`, `#E(·) = 2`, `zeros(·) = 3`, and T4-valid.
  - *Link chain first-emit:* `t_1^L(d) = inc(b_L(d), 1) = [d.0.s_L.1]` — structurally analogous, with `s_L` in place of `s_C`.

*Proof.* By ChainDiscipline, `A_C(d) = S(b_C(d), 1)` with first element `c₁ = inc(b_C(d), 1)`. ASN-0040's SiblingStream postcondition `cₙ = [p₁, …, p_{#p}, 0…0, n]` (with `d − 1 = 0` interior zeros at depth `1`) gives `c₁ = [b_C(d)₁, …, b_C(d)_{#b_C(d)}, 1]`; since `b_C(d) = [d.0.s_C]`, this is `[d.0.s_C.1]`, whence `E(·)₁ = s_C`, `#E(·) = 2`, `origin(·) = d`, and `zeros(·) = 3`. T4-validity is TA5a's `k = 1` case, whose side condition `zeros(b_C(d)) ≤ 3` is discharged by `b_C(d)`'s T4-validity (T4 forces `zeros ≤ 3`) — here `b_C(d) = inc(d, 2)` is T4-valid by TA5a's `k = 2` case, whose side condition `zeros(d) ≤ 2` is discharged by M0's `zeros(d) = 2` (verified under *Sub-allocator chains are ASN-0040 sibling streams* above). The link case is symmetric, with `b_L(d) = inc(b_C(d), 0)` T4-valid by TA5a's unconditionally-preserving `k = 0` case. ∎

**Per-chain disciplines (ASN-0040 citations).** Each discipline below is named for the substrate's local reference and discharged by the cited ASN-0040 result applied to the sibling stream `A_C(d) = S(b_C(d), 1)` (resp. `A_L(d) = S(b_L(d), 1)`), whose parent `(b_·(d), 1)` is `B6`-valid (verified above).

- **ChainElementT4Validity.** Every element of `A_C(d)` (resp. `A_L(d)`) is T4-valid. *Source: ASN-0040 B6(a) (ValidDepth sufficiency)* — for `B6`-valid `(p, d)`, every `cₙ ∈ S(p, d)` satisfies T4.

- **ChainUniformLength.** For each `d ∈ dom(M)`, all elements of `A_C(d)` (resp. `A_L(d)`) have length `#d + 3`. *Source: ASN-0040 SiblingStream postcondition* `#cₙ = #p + d` — with `p = b_·(d)` (`#p = #d + 2`) and depth `1`, `#cₙ = #d + 3` for every `n`.

- **ChainEnumerationInjectivity.** The enumeration of `A_C(d)` (resp. `A_L(d)`) is strictly increasing under T1, `m < n ⟹ t_m < t_n`; hence `n ↦ t_n` is injective and (by T1 trichotomy) order-preserving in both directions, `m < n ⟺ t_m < t_n`. *Source: ASN-0040 S0 (StreamOrdering)* — `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`.

- **ChainUniformZeroCount.** Every element of `A_C(d)` (resp. `A_L(d)`) has `zeros = 3`. *Source: ASN-0040 SiblingStream postcondition* (`cₙ = [p₁ … p_{#p}, 0…0, n]` with `d − 1 = 0` interior zeros at depth `1` and `n ≥ 1` positive), equivalently *B5a (SiblingZerosPreservation)*, `zeros(inc(t, 0)) = zeros(t)`: `zeros(cₙ) = zeros(b_·(d)) = 3` for every `n`.

- **DisjointSubAllocatorChains.** `A_C(d)` and `A_L(d)` are disjoint as address sets, and addresses produced by `A_C(d)` (resp. `A_L(d)`) carry `E(·)₁ = s_C` (resp. `s_L`). *Source: ASN-0040 B7 (NamespaceDisjointness)* — `S(b_C(d), 1) ∩ S(b_L(d), 1) = ∅`, since `(b_C(d), 1) ≠ (b_L(d), 1)` (the anchors disagree at position `#d + 2`, `s_C` vs `s_L`, by SC-NEQ) and both parents are `B6`-valid. The subspace-identifier reading follows from ChainPrefixExtension: every element of `A_C(d)` agrees with `b_C(d)` at position `#d + 2`, where the value is `s_C` (resp. `s_L` for `A_L(d)`).

- **ChainPrefixExtension.** Every element of an active sub-allocator chain extends its anchor under the prefix relation:

    `(A d ∈ dom(M), t ∈ A_C(d) :: b_C(d) ≼ t)`
    `(A d ∈ dom(M), t ∈ A_L(d) :: b_L(d) ≼ t)`

  *Source: ASN-0040 S1 (StreamPrefix)* — `(A n : n ≥ 1 : p ≼ cₙ)`, applied at `p = b_C(d)` (resp. `b_L(d)`).

**Lemma (ChainMembershipForOrigin).** At every reachable state `Σ`, every entry of `dom(C)` (resp. `dom(L)`) inhabits the content (resp. link) sub-allocator chain of its origin, and forms a *contiguous initial segment* of that chain. Letting `A_C(d) = (t_1, t_2, t_3, …)` denote the enumeration of `d`'s content sub-allocator chain (with `t_1` the first emission and `t_{n + 1} = inc(t_n, 0)`), and `A_L(d) = (s_1, s_2, s_3, …)` the analogous link chain:

- `(A d ∈ dom(M) :: (E m_d ≥ 0 :: dom(C) ∩ {a' ∈ T : origin(a') = d} = {t_1, …, t_{m_d}}))` (content contiguous prefix; `{t_1, …, t_0} = ∅` by convention)
- `(A d ∈ dom(M) :: (E n_d ≥ 0 :: dom(L) ∩ {ℓ' ∈ T : origin(ℓ') = d} = {s_1, …, s_{n_d}}))` (link contiguous prefix)

The weaker subset inclusion `dom(C) ∩ {a' : origin(a') = d} ⊆ A_C(d)` (and its link analogue) is the immediate corollary of the contiguous-prefix form; downstream consumers cite either form as needed. The contiguity matches ASN-0040's B1 (ContiguousPrefix) for the baptismal registry: the content and link sub-allocator chains have the same "always-extend-by-one-from-the-current-frontier" discipline as Nelson's baptism.

*Proof.* Induction on transition sequences from `Σ₀`.

*Base.* At `Σ₀`, both `dom(C)` and `dom(L)` are empty, so both inclusions hold vacuously for every `d`.

*Step.* Assume both inclusions hold at `Σ`. The substrate admits three transition kinds:

- *K.σ(d_new):* `C` and `L` are in frame, so for every `d` already in `dom(M)` the intersection set is unchanged and the contiguous-prefix postcondition transfers at the same `m_d` (resp. `n_d`). For the freshly registered `d_new`, the intersection sets are empty in `Σ'`. *Content clause derivation:* By the inductive hypothesis on C2 at `Σ`, every `a ∈ dom(C(Σ))` satisfies `origin(a) ∈ dom(M(Σ))`. By K.σ's precondition, `d_new ∉ dom(M(Σ))`. Therefore `origin(a) ≠ d_new` for every `a ∈ dom(C(Σ))`. Since `C` is in frame (`C(Σ') = C(Σ)`), `dom(C(Σ')) ∩ {a' : origin(a') = d_new} = dom(C(Σ)) ∩ {a' : origin(a') = d_new} = ∅ = {t_1, …, t_0}`, witnessing `m_{d_new} = 0` at `Σ'`. *Link clause derivation:* Symmetric, using the inductive hypothesis on L1a at `Σ` together with K.σ's precondition `d_new ∉ dom(M(Σ))` and frame on `L`, yielding `n_{d_new} = 0`.

- *K.α(d, a, v):* Only `dom(C)` grows, by one element `a` with `origin(a) = d`. For `d' ∈ dom(M)` with `d' ≠ d`, the intersection set `dom(C') ∩ {a' : origin(a') = d'} = dom(C) ∩ {a' : origin(a') = d'}` is unchanged (the new `a` has `origin(a) = d ≠ d'`), so the contiguous-prefix postcondition transfers at the same `m_{d'}`. For `d` itself, two sub-cases via the K.α emission rule:
  - *First emission* (`{a' ∈ dom(C) : origin(a') = d} = ∅`; equivalently `m_d = 0` at `Σ` by IH): by the FirstEmission lemma, `a = [d.0.s_C.1] = t_1` is the first emission of `A_C(d)`'s chain. The intersection set at `Σ'` is `{a} = {t_1}`, witnessing `m_d = 1` at `Σ'`.
  - *Subsequent emission* (`{a' ∈ dom(C) : origin(a') = d} ≠ ∅`; equivalently `m_d ≥ 1` at `Σ` by IH): by IH, the prior intersection is `{t_1, …, t_{m_d}}`. By ChainEnumerationInjectivity, `n ↦ t_n` is strictly increasing under T1, so `t_1 < t_2 < … < t_{m_d}` and the lex-order maximum of `{t_1, …, t_{m_d}}` is `t_{m_d}`. Hence `a_prev := max{a' ∈ dom(C) : origin(a') = d} = t_{m_d}`. By ChainDiscipline, `A_C(d)` is closed under `inc(·, 0)`, so `a = inc(t_{m_d}, 0) = t_{m_d + 1}`. The new intersection set at `Σ'` is `{t_1, …, t_{m_d}, t_{m_d + 1}} = {t_1, …, t_{m_d + 1}}`, witnessing the chain index `m_d + 1` at `Σ'`.

  The link contiguous-prefix postcondition is unchanged by frame on `dom(L)`.

- *K.λ(d, ℓ, (e₁, …, eₙ)):* Symmetric to K.α with content↔link, using the FirstEmission lemma for the first-emit branch (placing `ℓ = s_1`, witnessing `n_d = 1`) and ChainDiscipline for the subsequent-emit branch (placing `ℓ = s_{n_d + 1}` from `ℓ_prev = s_{n_d}` by ChainEnumerationInjectivity, witnessing `n_d + 1` at `Σ'`). The content contiguous-prefix postcondition is unchanged by frame on `dom(C)`. ∎

**Corollary (StoreT4Validity).** At every reachable state `Σ`, every entry of `dom(C) ∪ dom(L)` is a T4-valid tumbler:

  `(A a ∈ dom(C) :: ValidAddress(a))`
  `(A ℓ ∈ dom(L) :: ValidAddress(ℓ))`

*Proof.* For any `a ∈ dom(C)`, ChainMembershipForOrigin places `a ∈ A_C(origin(a))` (well-defined since `origin(a) ∈ dom(M)` by C2). By ChainElementT4Validity, every element of `A_C(origin(a))` is T4-valid; hence `a` is T4-valid. The link case is symmetric: `ℓ ∈ dom(L)` lies in `A_L(origin(ℓ))` by ChainMembershipForOrigin, and ChainElementT4Validity gives T4-validity of every element. ∎

This corollary discharges the T4-validity precondition of T7 (FirstElementFieldDistinction, ASN-0034) wherever T7 is cited against `dom(C)` and `dom(L)`.

**Lemma (FirstEmissionFreshness).** At every reachable state `Σ`, the first emission of an active sub-allocator chain — the address that K.α (resp. K.λ) commits when the corresponding first-emit predicate fires — is fresh against `dom(C) ∪ dom(L)`:

  - *Content first-emit:* Under the K.α first-emit predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`, the first emission `a = [d.0.s_C.1]` of `A_C(d)` satisfies `a ∉ dom(C) ∪ dom(L)` at the K.α event that commits `a`.
  - *Link first-emit:* Under the K.λ first-emit predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`, the first emission `ℓ = [d.0.s_L.1]` of `A_L(d)` satisfies `ℓ ∉ dom(L) ∪ dom(C)` at the K.λ event that commits `ℓ`.

The proof below derives freshness from L0, SC-NEQ, ChainPrefixExtension, ChainMembershipForOrigin, Cross-document disjointness, StoreT4Validity, ChainElementT4Validity, and T7, all consumed at the pre-state `Σ`. ChainMembershipForOrigin, StoreT4Validity, and Cross-document disjointness are established under the same simultaneous-induction discipline. Throughout this proof, the new key's subspace identifier is read from FirstEmission's structural form, not from L0 at `Σ'`, which would be circular under the simultaneous induction (L0 at `Σ'` itself depends on FirstEmissionFreshness).

*Proof.*

*Content case, against `dom(C)`.* Under the first-emit predicate at the pre-state `Σ`, every `a' ∈ dom(C)` has `origin(a') ≠ d`. (i) `a = [d.0.s_C.1]` is the first emission of `A_C(d)`, so by ChainPrefixExtension (base case), `b_C(d) ≼ a`. (ii) For every `a' ∈ dom(C)` with `origin(a') ≠ d`: ChainMembershipForOrigin at `Σ` places `a' ∈ A_C(origin(a'))` (well-defined since `origin(a') ∈ dom(M)` by C2), and ChainPrefixExtension gives `b_C(origin(a')) ≼ a'`. (iii) Cross-document disjointness applied to `(d, origin(a'))` gives `b_C(d) ⋠ b_C(origin(a')) ∧ b_C(origin(a')) ⋠ b_C(d)`. (iv) T10 (PartitionIndependence, ASN-0034) closes: `a ≠ a'`.

*Content case, against `dom(L)`.* StoreT4Validity at `Σ` gives T4-validity of every `ℓ ∈ dom(L)`; `a` is T4-valid by ChainElementT4Validity applied to `A_C(d)` (whose first emission `[d.0.s_C.1]` is T4-valid by the FirstEmission lemma). The subspace identifiers split by source: by L0 at `Σ`, `E(ℓ)₁ = s_L` for the pre-existing peer `ℓ ∈ dom(L)`; for the new key `a` we read `E(a)₁ = s_C` from the FirstEmission lemma's structural form `a = [d.0.s_C.1]`. By SC-NEQ, `s_C ≠ s_L`; `zeros(a) = zeros(ℓ) = 3` by FirstEmission's structural form and L1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `a ≠ ℓ`.

*Link case, against `dom(L)`.* Under the first-emit predicate at the pre-state `Σ`, every `ℓ' ∈ dom(L)` has `origin(ℓ') ≠ d`. (i) `ℓ = [d.0.s_L.1]` is the first emission of `A_L(d)`, so by ChainPrefixExtension (base case, link clause), `b_L(d) ≼ ℓ`. (ii) For every `ℓ' ∈ dom(L)` with `origin(ℓ') ≠ d`: ChainMembershipForOrigin at `Σ` places `ℓ' ∈ A_L(origin(ℓ'))` (well-defined since `origin(ℓ') ∈ dom(M)` by L1a — the link-side counterpart of C2), and ChainPrefixExtension (link clause) gives `b_L(origin(ℓ')) ≼ ℓ'`. (iii) Cross-document disjointness applied to `(d, origin(ℓ'))` in its `b_L` form gives `b_L(d) ⋠ b_L(origin(ℓ')) ∧ b_L(origin(ℓ')) ⋠ b_L(d)`. (iv) T10 (PartitionIndependence, ASN-0034) closes: `ℓ ≠ ℓ'`.

*Link case, against `dom(C)`.* StoreT4Validity at `Σ` gives T4-validity of every `a ∈ dom(C)`; `ℓ` is T4-valid by ChainElementT4Validity applied to `A_L(d)` (whose first emission `[d.0.s_L.1]` is T4-valid by the FirstEmission lemma). The subspace identifiers split by source: by L0 at `Σ`, `E(a)₁ = s_C` for the pre-existing peer `a ∈ dom(C)`; for the new key `ℓ` we read `E(ℓ)₁ = s_L` from the FirstEmission lemma's structural form `ℓ = [d.0.s_L.1]`. By SC-NEQ, `s_C ≠ s_L`; `zeros(ℓ) = zeros(a) = 3` by FirstEmission's structural form and C1. T7 (FirstElementFieldDistinction, ASN-0034) closes: `ℓ ≠ a`. ∎

**Note (L0 discharge / subspace auto-conformance).** At a K.α (resp. K.λ) event, L0's content-subspace precondition `E(a)₁ = s_C` (resp. link-subspace `E(ℓ)₁ = s_L`) is automatically satisfied by the pinned emission, requiring no caller choice. *First-emit branch:* the FirstEmission lemma pins `a = [d.0.s_C.1]` (resp. `ℓ = [d.0.s_L.1]`), so `E(·)₁` is read by inspection. *Subsequent-emit branch:* `a = inc(a_prev, 0) ∈ A_C(d)` by ChainDiscipline's closure under `inc(·, 0)` applied to `a_prev ∈ A_C(d)` (ChainMembershipForOrigin at `Σ`), and DisjointSubAllocatorChains gives `E(·)₁ = s_C` for every element of `A_C(d)` (resp. `s_L` for `A_L(d)`).

**Note (L14 new-key discharge).** When K.α commits a fresh `a` (resp. K.λ commits a fresh `ℓ`), disjointness from each committed peer in the opposite store follows from L0 + SC-NEQ + StoreT4Validity + T7: the new key carries `E(·)₁ = s_C` (resp. `s_L`) by the L0 discharge note, each opposite-store peer carries the complementary identifier by IH-L0, `s_C ≠ s_L` by SC-NEQ, and StoreT4Validity discharges T7's T4-validity precondition (new key via ChainElementT4Validity on its chain, peer via IH). T7 then closes `a ≠ ℓ`. At prior keys IH-L14 transfers by frame on the opposite store.


## Cross-document disjointness chain

**Lemma (Cross-document disjointness; ASN-0040 B7).** For any two distinct documents `d₁, d₂ ∈ dom(M)` with `d₁ ≠ d₂`, the link sub-allocator chains `A_L(d₁) = S(b_L(d₁), 1)` and `A_L(d₂) = S(b_L(d₂), 1)` are disjoint, and likewise the content chains:

  `A_L(d₁) ∩ A_L(d₂) = ∅`  and  `A_C(d₁) ∩ A_C(d₂) = ∅`.

Hence no link (resp. content) address allocated under `d₁` coincides with any allocated under `d₂`. Equivalently, the anchors are prefix-incomparable, `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` for `p_i := b_L(d_i)` (resp. `b_C(d_i)`), so T10 (PartitionIndependence, ASN-0034) closes extension-disjointness directly; consumers may cite either the B7 form or the T10 form.

*Proof.* By M0, both `d₁, d₂` are T4-valid with `zeros = 2`, so (as established under *Sub-allocator chains are ASN-0040 sibling streams*) `b_L(d₁), b_L(d₂)` are T4-valid with `zeros = 3` and `(b_L(d₁), 1)`, `(b_L(d₂), 1)` satisfy `B6`. They are distinct: `d₁ ≠ d₂` forces `b_L(d₁) ≠ b_L(d₂)` — each anchor reproduces its document on positions `1..#d_i` — so `(b_L(d₁), 1) ≠ (b_L(d₂), 1)`. ASN-0040's B7 (NamespaceDisjointness) then gives `S(b_L(d₁), 1) ∩ S(b_L(d₂), 1) = ∅`. The same argument with `b_C` in place of `b_L` gives content disjointness.

*Anchor prefix-incomparability (T10 form).* The anchors `p_i = b_·(d_i)` are length-`+2` extensions of `d_i` (positions `1..#d_i` reproduce `d_i`, position `#d_i + 1` is the separator `0`, position `#d_i + 2` is `s_·`). When `d₁`, `d₂` are prefix-incomparable, a document-level divergence position `k ≤ min(#d₁, #d₂)` lifts unchanged to the anchors. When one properly prefixes the other (WLOG `d₁ ≺ d₂`), the anchors still diverge at the separator position `k = #d₁ + 1`: `p₁[k] = 0` while `p₂[k] = d₂[k] ≠ 0` (by M0 at both documents, `d₂` carries `d₁`'s two zeros at the shared positions and, having `zeros(d₂) = 2`, no further zero, so position `#d₁ + 1 ≤ #d₂` is nonzero). Either way `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (Prefix, ASN-0034), and T10 gives `a ≠ b` for any `a` extending `p₁`, `b` extending `p₂`. ∎

Cross-subspace collisions between `dom(C)` and `dom(L)` are prevented by L14 (StoreDisjointness, above), itself derived from L0 + SC-NEQ + T7.


## Substrate primitive operations

The substrate admits three primitive transitions, one per state component. Each is atomic — its precondition is evaluated against `Σ` and its effect committed to `Σ'` in a single indivisible step; no intermediate state with the transition partially applied is admitted.

*Parameter semantics.* For `K.α(d, a, v)` and `K.λ(d, ℓ, (e₁, …, eₙ))`, the address parameters `a` and `ℓ` appear in the operation signatures but their values are not free choices of the caller: the preconditions deterministically pin them from `(d, Σ)`. Specifically, the first-emit predicate forces `a = [d.0.s_C.1]` (resp. `ℓ = [d.0.s_L.1]`); the subsequent-emit predicate forces `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` (resp. `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)`). The pinning is total: `(d, Σ)` determines the conforming address uniquely.

### K.σ (DocumentRegistration)

Extends `dom(M)` by registering a new document address with an empty arrangement.

*Precondition:*
- `d ∉ dom(M)` (fresh document address)
- `ValidAddress(d) ∧ zeros(d) = 2` (T4-valid, document-level — discharges M0 at the new key)

*Effect:* `dom(M') = dom(M) ∪ {d}`, with `M'(d) = ∅` and `M'(d') = M(d')` for every `d' ∈ dom(M)`.

*Frame:* `C' = C; L' = L`

*Freshness from `zeros`.* K.σ needs no explicit `d ∉ dom(C) ∪ dom(L)` clause and no anchor-disjointness clause, because both follow from a single `zeros` gap. C1 forces `zeros(a) = 3` for every `a ∈ dom(C)`, L1 forces `zeros(ℓ) = 3` for every `ℓ ∈ dom(L)`, and every sub-allocator anchor `b_C(d') = [d'.0.s_C]`, `b_L(d') = [d'.0.s_L]` likewise has `zeros = 3` (inheriting each of `d'`'s two zeros plus the separator inserted at position `#d' + 1`). K.σ's precondition pins `zeros(d) = 2`. Since no address can simultaneously satisfy `zeros = 2` and `zeros = 3`, `d` collides with neither store entry nor anchor: `d ∉ dom(C) ∪ dom(L)` and `d ≠ b_C(d'), b_L(d')` for every `d' ∈ dom(M)` are both forced by the precondition list together with C1/L1.

K.σ opens the content and link sub-allocator frontiers `A_C(d)` and `A_L(d)` under `d` — available once `d ∈ dom(M)` (see *Active sub-allocator chains* above) — for subsequent K.α and K.λ emissions.

*K.σ admissibility scope.* K.σ's precondition is structural-only: it makes no commitment about *which* document addresses are admissible beyond T4-validity and `zeros(d) = 2`. The discipline that constrains which tumblers are introduced (Nelson's hierarchical baptism, T10a allocator conformance for the document allocator, etc.) is a higher-layer commitment; the substrate's only commitment is that whatever `d` is introduced satisfies M0 going forward. In particular, K.σ admits configurations broader than Nelson's hierarchical baptism — a tumbler `d` with `zeros(d) = 2` whose prefix corresponds to no allocated node or account is structurally admissible at this layer. Downstream ASNs that lift entity-hierarchy discipline (entity stratification, lineage, version-allocator activation — see Scope, *Entity allocation*) tighten K.σ's precondition accordingly.

### K.α (ContentAllocation)

Extends `dom(C)` with a fresh content address scoped to an allocated document.

*Binding precondition:*
- `d ∈ dom(M)` (home document exists)
- `a` is produced by `d`'s content sub-allocator `A_C(d)`:
  - *First emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} = ∅`): `a = [d.0.s_C.1]`. Freshness against `dom(C) ∪ dom(L)` is supplied by FirstEmissionFreshness.
  - *Subsequent emission* (predicate: `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`): `a = inc(a_prev, 0)` (TA5(c)) where `a_prev := max{a' ∈ dom(C) : origin(a') = d}`, the next sibling on `A_C(d)`'s `inc(·, 0)` chain. The `max` is well-defined because the set is finite (C-fin restricted by `origin(·) = d`). Freshness of `a` against `dom(C) ∪ dom(L)` is discharged by three governing results: within-document freshness against `dom(C)` via ChainEnumerationInjectivity + ChainMembershipForOrigin (the strictly increasing chain order separates `a = t_{n_prev + 1}` from every prior `t_m`); cross-document freshness against `dom(C)` via ChainPrefixExtension + Cross-document disjointness + T10; cross-subspace freshness against `dom(L)` via the same machinery that derives L14, applied to the fresh key `a` against each committed peer `ℓ ∈ dom(L)` (ChainElementT4Validity + L0 + SC-NEQ + T7).
- `v ∈ Val` (well-formed content value)

*Derived structural facts.* The chain-emission clause pins `a` uniquely from `(d, Σ)`, and the following are its consequences, not independent constraints: `zeros(a) = 3` (ChainUniformZeroCount), `E(a)₁ = s_C` (DisjointSubAllocatorChains, see L0 discharge note), `#E(a) ≥ 2` (FirstEmission / ChainUniformLength), `origin(a) = d` (chain rooted at `b_C(d)` via ChainPrefixExtension), and `a ∉ dom(C) ∪ dom(L)` (the freshness conclusions above).

*Effect:* `C' = C ∪ {a ↦ v}`

*Frame:* `L' = L; dom(M') = dom(M); (A d' ∈ dom(M) :: M'(d') = M(d'))`

The explicit `dom(M') = dom(M)` clause makes domain equality unambiguous alongside the pointwise function equality. Under partial-function semantics the two together force `M' = M`, so C2 and L1a at `Σ` transfer to `Σ'` directly: `origin(a') ∈ dom(M)` implies `origin(a') ∈ dom(M')`.

Cross-document disjointness for content allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_C(d)` and `p₂ := b_C(d')`.

### K.λ (LinkAllocation)

Extends `dom(L)` with a fresh link address scoped to an allocated document.

Signature: `K.λ(d, ℓ, (e₁, …, eₙ))` where the link value is a finite sequence of `N` endsets.

*Binding precondition:*
- `d ∈ dom(M)` (home document exists)
- `ℓ` is produced by `d`'s link sub-allocator `A_L(d)`:
  - *First emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`): `ℓ = [d.0.s_L.1]`, the determinate first emission of `A_L(d)`. Freshness against `dom(L) ∪ dom(C)` is supplied by FirstEmissionFreshness.
  - *Subsequent emission* (predicate: `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`): `ℓ = inc(ℓ_prev, 0)` (TA5(c)) where `ℓ_prev := max{ℓ' ∈ dom(L) : origin(ℓ') = d}`, the next sibling on `A_L(d)`'s `inc(·, 0)` chain. The `max` is well-defined because the set is finite (L-fin restricted by `origin(·) = d`). Freshness of `ℓ` against `dom(L) ∪ dom(C)` is discharged by three governing results: within-document freshness against `dom(L)` via ChainEnumerationInjectivity + ChainMembershipForOrigin (the strictly increasing chain order separates `ℓ = s_{n_prev + 1}` from every prior `s_m`); cross-document freshness against `dom(L)` via ChainPrefixExtension + Cross-document disjointness + T10; cross-subspace freshness against `dom(C)` via the same machinery that derives L14, applied to the fresh key `ℓ` against each committed peer `a ∈ dom(C)` (ChainElementT4Validity + L0 + SC-NEQ + T7).
- `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` (well-formed link value with mandatory non-empty type endset at slot 3 — L3). The arity-3 default `(F, G, Θ)` (slot 1 = from, slot 2 = to, slot 3 = type) is the StandardTriple convention retained for worked examples and notational compactness; the substrate admits arbitrary arity `N ≥ 3`.

*Derived structural facts.* As in K.α, the chain-emission clause pins `ℓ` uniquely from `(d, Σ)`, and the following are its consequences, not independent constraints: `zeros(ℓ) = 3` (ChainUniformZeroCount), `E(ℓ)₁ = s_L` (DisjointSubAllocatorChains, see L0 discharge note), `#E(ℓ) ≥ 2` (FirstEmission / ChainUniformLength), `origin(ℓ) = d` (chain rooted at `b_L(d)`), and `ℓ ∉ dom(L) ∪ dom(C)` (the freshness conclusions above).

*Effect:* `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`

*Frame:* `C' = C; dom(M') = dom(M); (A d' ∈ dom(M) :: M'(d') = M(d'))`

The explicit `dom(M') = dom(M)` clause makes domain equality unambiguous alongside the pointwise function equality. Under partial-function semantics the two together force `M' = M`, so C2 and L1a at `Σ` transfer to `Σ'` directly: `origin(ℓ') ∈ dom(M)` implies `origin(ℓ') ∈ dom(M')`.

Cross-document disjointness for link allocations is supplied by the Cross-document disjointness chain lemma (above), applied with `p₁ := b_L(d)` and `p₂ := b_L(d')`.

*Forward allocation, derivable.* The within-document forward-allocation property `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` is not stated as a precondition because it is a derivable consequence of the emission rules — symmetrically with K.α. In the subsequent-emission case, `ℓ = inc(max{prev}, 0)` and TA5(a) gives `inc(t, 0) > t`, so `ℓ > max{prev} ≥ ℓ'` for every `ℓ' ∈ dom(L)` with `origin(ℓ') = d`. In the first-emission case the universal antecedent `{ℓ' : origin(ℓ') = d} = ∅` is vacuous. The same derivation applies to K.α's content emissions; neither operator carries the clause as a precondition.


## Worked example

To make the substrate's operation concrete, we trace a small scenario step-by-step starting from `Σ₀ = (∅, ∅, ∅)`.

*Arity convention.* The K.λ invocations below use the arity-3 default `(F, G, Θ)` (StandardTriple — slot 1 from, slot 2 to, slot 3 type) for notational compactness. This is one admissible instance of K.λ's general signature `K.λ(d, ℓ, (e₁, …, eₙ))` with `N = 3`; the substrate admits arbitrary `N ≥ 3` per L3, and any higher-arity link value satisfying the precondition would be equally well-formed.

*Fix a document address.* Let `d = [1, 0, 2, 0, 5]` — `#d = 5`, with zeros at positions 2 and 4 so `zeros(d) = 2`, with positive first and last components (1 and 5) and no adjacent zeros, hence T4-valid. By T4b, its projections are `N(d) = [1]`, `U(d) = [2]`, `D(d) = [5]`. By SubspaceConventionAxiom, `s_C = 1` and `s_L = 2`.

*Step 1 — `K.σ(d)` (document registration).* Precondition: `d ∉ dom(M₀) = ∅` ✓; `ValidAddress(d) ∧ zeros(d) = 2` ✓. Effect commits `dom(M₁) = {d}` with `M₁(d) = ∅`; `C₁ = ∅`, `L₁ = ∅`. Both `A_C(d)` and `A_L(d)` are active under `d` (since `d ∈ dom(M₁)`; see *Active sub-allocator chains* above). Verifying invariants at `Σ₁ = (∅, ∅, {d ↦ ∅})`: M0 holds (the single key `d` satisfies `zeros = 2`); M1 holds (`∅ ⊆ {d}`); all C-/L-invariants and L14, L-fin, C-fin are vacuous or trivial on empty stores.

*Step 2 — `K.α(d, a, v)` (first content emission).* Pinning the address from `Σ₁`: the predicate `{a' ∈ dom(C₁) : origin(a') = d} = ∅` selects the first-emit case, so `a = [d.0.s_C.1] = [1, 0, 2, 0, 5, 0, 1, 1]`. Witness it via the C1c chain `(t₀, t₁, t₂)`:
- `t₀ = d = [1, 0, 2, 0, 5]`
- `t₁ = inc(d, 2)`: TA5(d) at `k = 2` gives the structural form, appending `[0, 1]` to yield `[1, 0, 2, 0, 5, 0, 1] = b_C(d)`. Admissibility: TA5a at `k = 2` requires `zeros(d) ≤ 2`; M0 gives `zeros(d) = 2 ≤ 2`, satisfied — hence `t₁` is T4-valid; TA5(d) gives `zeros(t₁) = 3`.
- `t₂ = inc(b_C(d), 1)`: TA5(d) at `k = 1` gives the structural form, appending `1` to yield `[1, 0, 2, 0, 5, 0, 1, 1] = a`. Admissibility: TA5a at `k = 1` requires `zeros(t₁) ≤ 3`, discharged by `t₁`'s T4-validity (T4 forces `zeros ≤ 3`), so `t₂` is T4-valid given `t₁` T4-valid; TA5(d) gives `zeros(t₂) = 3`, `#E(t₂) = 2`.

Verifying preconditions: `a ∉ dom(C₁) ∪ dom(L₁) = ∅` ✓; `zeros(a) = 3` ✓; `E(a) = [1, 1]` so `E(a)₁ = 1 = s_C` ✓; `#E(a) = 2 ≥ 2` ✓; `origin(a) = N(a).0.U(a).0.D(a) = [1].0.[2].0.[5] = d` ✓. Freshness of `a` against `dom(C₁) ∪ dom(L₁)` is supplied by FirstEmissionFreshness, here vacuously since the predecessor stores are empty.

Effect: `C₂ = {a ↦ v}`; `L₂ = ∅`; `M₂ = M₁`. Verifying invariants at `Σ₂`: C0 (extended at fresh `a`), C1 (`zeros(a) = 3`), C1b (`#E(a) = 2`), C1c (chain exhibited above), C2 (`origin(a) = d ∈ dom(M₂)`), C-fin (`|dom(C₂)| = 1 < ∞`) all hold at the new key.

*Step 3 — `K.λ(d, ℓ, F, G, Θ)` (first link emission).* Pinning from `Σ₂`: the predicate `{ℓ' ∈ dom(L₂) : origin(ℓ') = d} = ∅` selects the first-emit case, so `ℓ = [d.0.s_L.1] = [1, 0, 2, 0, 5, 0, 2, 1]`. Witness via the L1c chain `(t₀, t₁, t₂, t₃)`:
- `t₀ = d = [1, 0, 2, 0, 5]`
- `t₁ = inc(d, 2) = [1, 0, 2, 0, 5, 0, 1] = b_C(d)` (admissibility as in Step 2)
- `t₂ = inc(b_C(d), 0)`: TA5(c) at `k = 0` gives the structural form, incrementing `b_C(d)`'s rightmost nonzero component (position 7, from `1` to `2`) to yield `[1, 0, 2, 0, 5, 0, 2] = b_L(d)`. By SubspaceConventionAxiom, `s_L = 2 = s_C + 1`, matching position 7. Admissibility: TA5a at `k = 0` is unconditionally T4-preserving, so `t₂` is T4-valid given `b_C(d)` T4-valid (from Step 2).
- `t₃ = inc(b_L(d), 1)`: TA5(d) at `k = 1` gives the structural form, appending `1` to yield `[1, 0, 2, 0, 5, 0, 2, 1] = ℓ`. Admissibility: TA5a at `k = 1` requires `zeros(b_L(d)) ≤ 3`, discharged by `b_L(d)`'s T4-validity (T4 forces `zeros ≤ 3`), so `t₃` is T4-valid given `b_L(d)` T4-valid. `zeros(ℓ) = 3`, `#E(ℓ) = 2`.

Verifying preconditions: `ℓ ∉ dom(L₂) ∪ dom(C₂) = {a}`. Disagreement at position 7 (`a₇ = 1` vs `ℓ₇ = 2`) gives `ℓ ≠ a`, confirming the L0 + SC-NEQ + T7 derivation: the two addresses sit in disjoint subspaces. `zeros(ℓ) = 3` ✓; `E(ℓ) = [2, 1]` so `E(ℓ)₁ = 2 = s_L` ✓; `#E(ℓ) = 2 ≥ 2` ✓; `origin(ℓ) = d` ✓. Freshness supplied by FirstEmissionFreshness.

Effect: `L₃ = {ℓ ↦ (F, G, Θ)}`; `C₃ = C₂`; `M₃ = M₂`. Verifying invariants at `Σ₃`: L0/L1/L1a/L1b/L1c/L3/L12 all hold at the new key per the matrix; L14 holds non-trivially: `dom(C₃) ∩ dom(L₃) = {a} ∩ {ℓ} = ∅` (verified by E(·)₁ disagreement); L-fin holds (`|dom(L₃)| = 1 < ∞`).

*Step 4 — `K.α(d, a', v')` (second content emission, subsequent-emit branch).* Pinning from `Σ₃`: `{a'' ∈ dom(C₃) : origin(a'') = d} = {a}` is non-empty, so the subsequent-emit branch fires with `a' = inc(max{a}, 0) = inc(a, 0)`. Since `sig(a) = 8` with value `1`, TA5(c) gives `a' = [1, 0, 2, 0, 5, 0, 1, 2]`. The C1c chain extends `a`'s chain by one step: `(t₀, t₁, t₂, a')` with `a' = inc(t₂, 0) = inc(a, 0)`. Admissibility of the new step: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `a'` is T4-valid given `a` T4-valid (the latter from Step 2's chain exhibition); TA5(c) gives the structural form. Freshness against `dom(C₃) = {a}` discharged by ChainEnumerationInjectivity (within-chain injectivity) applied to `A_C(d)`'s chain (per ChainDiscipline); freshness against `dom(L₃) = {ℓ}` discharged by L0 + SC-NEQ + T7.

Verifying preconditions: `a' ∉ dom(C₃) ∪ dom(L₃) = {a, ℓ}` ✓ (since `a' > a` strictly by TA5(a), and `E(a')₁ = 1 ≠ 2 = E(ℓ)₁`); structural preconditions inherit from `a` via the inc rule (TA5(b) preserves `zeros`, `E(·)₁`, and `origin(·)`).

Effect: `C₄ = {a ↦ v, a' ↦ v'}`; `L₄ = L₃`; `M₄ = M₃`. All invariants continue to hold at `Σ₄`.

*Step 5 — `K.σ(d')` (second document registration).* Fix a second document address `d' = [1, 0, 2, 0, 5, 3]`. Verifying T4-validity: `#d' = 6`, zeros at positions 2 and 4 only (`zeros(d') = 2`), no adjacent zeros (positions (2,3) = (0,2) and (4,5) = (0,5)), first component `d'[1] = 1 ≠ 0`, last component `d'[6] = 3 ≠ 0`. By T4b, `N(d') = [1]`, `U(d') = [2]`, `D(d') = [5, 3]`. Precondition: `d' ∉ dom(M₄) = {d}` ✓ (distinct since `#d = 5 ≠ 6 = #d'`); `ValidAddress(d') ∧ zeros(d') = 2` ✓. Effect: `dom(M₅) = {d, d'}`, with `M₅(d') = ∅` and `M₅(d) = M₄(d) = ∅`. `A_C(d')` and `A_L(d')` become active at `Σ₅` (per the *Active sub-allocator chains* definition: `d' ∈ dom(M₅)`), alongside the already-active `A_C(d)` and `A_L(d)`.

*Verifying the Cross-document disjointness lemma at Σ₅.* Apply with `d₁ = d`, `d₂ = d'`. Since `d ≠ d'` and both anchors are `B6`-valid, ASN-0040's B7 gives `A_·(d) ∩ A_·(d') = ∅` directly. Illustrating the equivalent anchor-incomparability (T10 form): component-by-component, `d'[1..5] = [1, 0, 2, 0, 5] = d` with `#d < #d'`, so `d ≺ d'` (the properly-prefixing case). The anchors are `p₁ = b_L(d) = [1, 0, 2, 0, 5, 0, 2]` (length 7) and `p₂ = b_L(d') = [1, 0, 2, 0, 5, 3, 0, 2]` (length 8). At the separator index `k = #d + 1 = 6`:
- `p₁[6] = 0` (the zero separator inserted by the `b_L` construction at position `#d + 1`)
- `p₂[6] = d'[6] = 3 ≠ 0` (`d'` carries its two zeros at positions 2 and 4 by `zeros(d') = 2`, so position 6 must be nonzero per the T4 zero-count argument)
- `k = 6 ≤ min(#p₁, #p₂) = 7` ✓

Thus `p₁[6] = 0 ≠ 3 = p₂[6]`, witnessing `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`. The same divergence holds at position 6 for the content anchors `b_C(d) = [1, 0, 2, 0, 5, 0, 1]` and `b_C(d') = [1, 0, 2, 0, 5, 3, 0, 1]`. By T10, every link allocated under `d` (extending `b_L(d)`) differs from every link allocated under `d'` (extending `b_L(d')`); same for content.

*Verifying invariants at Σ₅.* M0 holds: `d` and `d'` both satisfy `ValidAddress ∧ zeros = 2`. M1 holds: `{d} ⊆ {d, d'}`. C0/C1/C1b/C1c/C2/C-fin hold by frame on `C` (unchanged from `Σ₄`); in particular, C2 carries the prior content keys `a, a'` whose `origin = d ∈ dom(M₅)`, preserved by M1's extension. L0/L1/L1a/L1b/L1c/L3/L12/L-fin hold by frame on `L` (unchanged from `Σ₄`); L1a holds for `ℓ` since `origin(ℓ) = d ∈ dom(M₅)`. L14: `dom(C₅) ∩ dom(L₅) = {a, a'} ∩ {ℓ} = ∅` (verified by `E(a)₁ = E(a')₁ = s_C ≠ s_L = E(ℓ)₁`). ChainMembershipForOrigin transfers: `dom(C₅) ∩ {a'' : origin(a'') = d} = {a, a'} ⊆ A_C(d)` (per Steps 2 and 4); `dom(C₅) ∩ {a'' : origin(a'') = d'} = ∅ ⊆ A_C(d')` (vacuous, first emission still pending); similarly for `L`.

*Step 6 — `K.α(d', a'', v'')` (first content emission under `d'`).* Pinning the address from `Σ₅`: `{a''' ∈ dom(C₅) : origin(a''') = d'} = ∅` (the content keys `a, a'` have `origin = d ≠ d'`), so the first-emit branch fires with `a'' = [d'.0.s_C.1] = [1, 0, 2, 0, 5, 3, 0, 1, 1]` (length 9). The C1c chain `(t₀, t₁, t₂)`:
- `t₀ = d' = [1, 0, 2, 0, 5, 3]`
- `t₁ = inc(d', 2)`: TA5(d) at `k = 2` gives the structural form, appending `[0, 1]` to yield `[1, 0, 2, 0, 5, 3, 0, 1] = b_C(d')` with `zeros = 3`. Admissibility: TA5a at `k = 2` requires `zeros(d') ≤ 2`; M0 gives `zeros(d') = 2 ≤ 2`, satisfied — hence `t₁` is T4-valid.
- `t₂ = inc(b_C(d'), 1)`: TA5(d) at `k = 1` gives the structural form, appending `1` to yield `a'' = [1, 0, 2, 0, 5, 3, 0, 1, 1]`. Admissibility: TA5a at `k = 1` requires `zeros(t₁) ≤ 3`, discharged by `t₁`'s T4-validity (T4 forces `zeros ≤ 3`), so `a''` is T4-valid given `t₁` T4-valid. `zeros(a'') = 3`, `#E(a'') = 2`.

Verifying preconditions: `a'' ∉ dom(C₅) ∪ dom(L₅) = {a, a', ℓ}`. *Cross-document freshness* against `{a, a'}` (both with `origin = d ≠ d'`): by Cross-document disjointness at Step 5, `b_C(d) ⋠ b_C(d') ∧ b_C(d') ⋠ b_C(d)`; `a, a'` extend `b_C(d)` (Steps 2, 4) while `a''` extends `b_C(d')`, so by T10, `a'' ≠ a` and `a'' ≠ a'`. *Sub-space freshness* against `ℓ`: `E(a'')₁ = 1 = s_C ≠ 2 = s_L = E(ℓ)₁` by L0 + SC-NEQ, so `a'' ≠ ℓ`. Other preconditions: `zeros(a'') = 3` ✓; `E(a'') = [1, 1]`, `E(a'')₁ = s_C` ✓; `#E(a'') = 2` ✓; `origin(a'') = N(a'').0.U(a'').0.D(a'') = [1].0.[2].0.[5, 3] = d'` ✓. (FirstEmissionFreshness applied to `A_C(d')` supplies the same conclusion compactly; the derivation above exhibits the underlying mechanism it bundles.)

Effect: `C₆ = C₅ ∪ {a'' ↦ v''} = {a ↦ v, a' ↦ v', a'' ↦ v''}`; `L₆ = L₅`; `M₆ = M₅`. Invariants at `Σ₆`: C0 (existing values unchanged), C1 (`zeros(a'') = 3`), C1b (`#E(a'') = 2`), C1c (chain exhibited above), C2 (`origin(a'') = d' ∈ dom(M₆)`), C-fin (`|C₆| = 3 < ∞`); ChainMembershipForOrigin extends: `{a''} ⊆ A_C(d')` by FirstEmission.

*Step 7 — `K.λ(d', ℓ'', F'', G'', Θ'')` (first link emission under `d'`).* Pinning from `Σ₆`: `{ℓ''' ∈ dom(L₆) : origin(ℓ''') = d'} = ∅` (`origin(ℓ) = d ≠ d'`), so the first-emit branch fires with `ℓ'' = [d'.0.s_L.1] = [1, 0, 2, 0, 5, 3, 0, 2, 1]` (length 9). The L1c chain `(t₀, t₁, t₂, t₃)`:
- `t₀ = d'`
- `t₁ = inc(d', 2) = b_C(d')` (admissibility as in Step 6)
- `t₂ = inc(b_C(d'), 0) = [1, 0, 2, 0, 5, 3, 0, 2] = b_L(d')` (TA5(c) gives the structural form, advancing `sig(b_C(d')) = 8` from `s_C = 1` to `s_L = 2`; SubspaceConventionAxiom gives `s_L = s_C + 1`. TA5a at `k = 0` is unconditionally T4-preserving, so `t₂` is T4-valid given `b_C(d')` T4-valid.)
- `t₃ = inc(b_L(d'), 1) = ℓ''` (TA5(d) at `k = 1` gives the structural form, appending `1`. TA5a at `k = 1` requires `zeros(b_L(d')) ≤ 3`, discharged by `b_L(d')`'s T4-validity (T4 forces `zeros ≤ 3`), so `ℓ''` is T4-valid given `b_L(d')` T4-valid. `zeros(ℓ'') = 3`, `#E(ℓ'') = 2`.)

Verifying preconditions: `ℓ'' ∉ dom(L₆) ∪ dom(C₆) = {ℓ, a, a', a''}`. *Cross-document freshness* against `{ℓ}` (origin = d ≠ d'): by Cross-document disjointness at Step 5, `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`; `ℓ` extends `b_L(d)` (Step 3) while `ℓ''` extends `b_L(d')`, so by T10, `ℓ'' ≠ ℓ`. *Sub-space freshness* against `{a, a', a''}`: each content address has `E(·)₁ = s_C = 1 ≠ 2 = s_L = E(ℓ'')₁`, so `ℓ'' ≠ a, a', a''`. Other preconditions: `zeros(ℓ'') = 3` ✓; `E(ℓ'') = [2, 1]`, `E(ℓ'')₁ = s_L` ✓; `#E(ℓ'') = 2` ✓; `origin(ℓ'') = d'` ✓.

Effect: `L₇ = L₆ ∪ {ℓ'' ↦ (F'', G'', Θ'')}`; `C₇ = C₆`; `M₇ = M₆`. Invariants at `Σ₇`: L0 (`E(ℓ'')₁ = s_L`), L1 (`zeros(ℓ'') = 3`), L1a (`origin(ℓ'') = d' ∈ dom(M₇)`), L1b (`#E(ℓ'') = 2`), L1c (chain exhibited above), L3 (triple endset with non-empty `Θ''`), L12 (existing link `ℓ ↦ (F, G, Θ)` unchanged), L14 (`dom(C₇) ∩ dom(L₇) = {a, a', a''} ∩ {ℓ, ℓ''} = ∅` by SC-NEQ), L-fin (`|L₇| = 2 < ∞`); ChainMembershipForOrigin extends: `{ℓ''} ⊆ A_L(d')` by FirstEmission, witnessing `n_{d'} = 1`.

*Step 8 — `K.λ(d, ℓ_new, F_new, G_new, Θ_new)` (second link emission under `d`, subsequent-emit branch).* Pinning the address from `Σ₇`: `{ℓ''' ∈ dom(L₇) : origin(ℓ''') = d} = {ℓ}` (note `origin(ℓ'') = d' ≠ d`), so the subsequent-emit branch fires with `ℓ_new = inc(max{ℓ}, 0) = inc(ℓ, 0)`. By ChainMembershipForOrigin's contiguous-prefix form at `Σ₇`, `dom(L₇) ∩ {ℓ''' : origin(ℓ''') = d} = {s₁}` with `ℓ = s₁`, so the lex-order max is `s₁` and `ℓ_new = s₂`. Since `sig(ℓ) = 8` with value `1`, TA5(c) gives `ℓ_new = [1, 0, 2, 0, 5, 0, 2, 2]`. The L1c chain extends `ℓ`'s chain by one step: `(t₀, t₁, t₂, t₃, t₄)` with `t₀ = d`, `t₁ = b_C(d)`, `t₂ = b_L(d)`, `t₃ = ℓ`, `t₄ = inc(ℓ, 0) = ℓ_new`. Admissibility of the new step: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `ℓ_new` is T4-valid given `ℓ` T4-valid (the latter from Step 3's chain exhibition); TA5(c) gives the structural form.

Verifying preconditions: `ℓ_new ∉ dom(L₇) ∪ dom(C₇) = {ℓ, ℓ'', a, a', a''}`.
- *Within-chain freshness against `ℓ`:* by ChainMembershipForOrigin at `Σ₇`, `ℓ ∈ A_L(d)` at chain index 1. By ChainDiscipline, `ℓ_new = inc(ℓ, 0) ∈ A_L(d)` at chain index 2. ChainEnumerationInjectivity gives `s₁ < s₂`, hence `ℓ ≠ ℓ_new`. (Concrete check: `ℓ_new` differs from `ℓ` at position 8, where `ℓ[8] = 1 ≠ 2 = ℓ_new[8]`.)
- *Cross-document freshness against `ℓ''`:* (a) `ℓ_new = inc(ℓ, 0)` extends `b_L(d)` — by IH on ChainMembershipForOrigin at `Σ₇`, `ℓ ∈ A_L(d)`; by ChainDiscipline's closure under `inc(·, 0)`, `ℓ_new = inc(ℓ, 0) ∈ A_L(d)` as a chain element; ChainPrefixExtension at `Σ₇` gives `b_L(d) ≼ ℓ_new` (concrete check: positions `1..7` of `ℓ_new = [1, 0, 2, 0, 5, 0, 2, 2]` are `[1, 0, 2, 0, 5, 0, 2] = b_L(d)`). (b) `ℓ'' ∈ A_L(d')` by ChainMembershipForOrigin at `Σ₇`, and `b_L(d') ≼ ℓ''` by ChainPrefixExtension. (c) Cross-document disjointness at `(d, d')` (verified in Step 5) gives `b_L(d) ⋠ b_L(d') ∧ b_L(d') ⋠ b_L(d)`. T10 (PartitionIndependence, ASN-0034) closes: `ℓ_new ≠ ℓ''`.
- *Sub-space freshness against `{a, a', a''}`:* StoreT4Validity at `Σ₇` gives T4-validity of `a, a', a''`; `ℓ_new` is T4-valid by chain-element T4-validity (TA5a-propagation along `A_L(d)`'s chain from FirstEmission's T4-valid output). L0 supplies `E(·)₁ = s_C = 1` for content and `E(ℓ_new)₁ = s_L = 2` (preserved from `ℓ` by TA5(c) since position 7 of `ℓ_new` carries `2`); `zeros(ℓ_new) = zeros(a) = 3` by L1/C1. SC-NEQ + T7 (FirstElementFieldDistinction, ASN-0034) closes: `ℓ_new ≠ a, a', a''`.

Other preconditions: `zeros(ℓ_new) = 3` (ChainUniformZeroCount — preserved under `inc(·, 0)` per ChainDiscipline, anchored at FirstEmission's `zeros = 3`) ✓; `E(ℓ_new) = [2, 2]`, `E(ℓ_new)₁ = 2 = s_L` ✓; `#E(ℓ_new) = 2` ✓; `origin(ℓ_new) = d` (TA5(b) preserves positions `1..7`, including the document-level prefix and the field-separator structure that origin's truncation depends on) ✓.

Effect: `L₈ = L₇ ∪ {ℓ_new ↦ (F_new, G_new, Θ_new)} = {ℓ ↦ (F, G, Θ), ℓ'' ↦ (F'', G'', Θ''), ℓ_new ↦ (F_new, G_new, Θ_new)}`; `C₈ = C₇`; `M₈ = M₇`. Invariants at `Σ₈`: L0–L1c hold at the new key as verified above; L3 (triple endset, non-empty `Θ_new`) ✓; L12 (existing values `ℓ ↦ ·` and `ℓ'' ↦ ·` unchanged) ✓; L14 ✓; L-fin (`|L₈| = 3`) ✓. ChainMembershipForOrigin extends: `dom(L₈) ∩ {ℓ''' : origin(ℓ''') = d} = {ℓ, ℓ_new} = {s₁, s₂}` (contiguous prefix of `A_L(d)`, witnessing `n_d = 2`).

*Step 9 — `K.σ(d_alt)` (third document registration, prefix-incomparable with prior documents).* Fix `d_alt = [1, 0, 3, 0, 7]` — `#d_alt = 5`, with zeros at positions 2 and 4 (`zeros(d_alt) = 2`), no adjacent zeros (positions (2,3) = (0,3) and (4,5) = (0,7)), `d_alt[1] = 1 ≠ 0` and `d_alt[5] = 7 ≠ 0`, hence T4-valid. By T4b, `N(d_alt) = [1]`, `U(d_alt) = [3]`, `D(d_alt) = [7]`.

Verify `d_alt ∉ dom(M₈) = {d, d'}`. Compare with `d = [1, 0, 2, 0, 5]`: position 3 disagrees (`d[3] = 2 ≠ 3 = d_alt[3]`), so `d_alt ≠ d`. Compare with `d' = [1, 0, 2, 0, 5, 3]`: position 3 disagrees similarly, so `d_alt ≠ d'`. The other K.σ precondition `ValidAddress(d_alt) ∧ zeros(d_alt) = 2` ✓.

Effect: `dom(M₉) = {d, d', d_alt}`, with `M₉(d_alt) = ∅` and `M₉(d) = M₉(d') = ∅` unchanged. `C₉ = C₈`, `L₉ = L₈`. Once `d_alt ∈ dom(M₉)`, the chains `A_C(d_alt)` and `A_L(d_alt)` are available (see *Active sub-allocator chains* above), alongside those already available for `d` and `d'`.

*Verifying the Cross-document disjointness lemma at `Σ₉` for the prefix-incomparable pair `(d, d_alt)`.* Since `d ≠ d_alt` and both anchors are `B6`-valid, ASN-0040's B7 gives `A_·(d) ∩ A_·(d_alt) = ∅`. Illustrating the anchor-incomparability (T10 form): `d` and `d_alt` are prefix-incomparable — position 3 of `d = [1, 0, 2, 0, 5]` is `2`, of `d_alt = [1, 0, 3, 0, 7]` is `3`, both within native domains, so neither prefixes the other. This document-level divergence at `k = 3` lifts to the anchors `p₁ = b_L(d) = [1, 0, 2, 0, 5, 0, 2]` and `p₂ = b_L(d_alt) = [1, 0, 3, 0, 7, 0, 2]`: `p₁[3] = 2 ≠ 3 = p₂[3]` at `k = 3 ≤ min(#p₁, #p₂) = 7`, witnessing `b_L(d) ⋠ b_L(d_alt) ∧ b_L(d_alt) ⋠ b_L(d)` (Prefix, ASN-0034); the same divergence holds for the content anchors `b_C(d)`, `b_C(d_alt)`. By T10, every link (resp. content) allocated under `d_alt` differs from every one allocated under `d`. The pair `(d', d_alt)` is analogous: `d'[3] = 2 ≠ 3 = d_alt[3]` gives the same position-3 divergence.

*Verifying invariants at `Σ₉`.* M0 holds at `d_alt`: precondition pins `ValidAddress(d_alt) ∧ zeros(d_alt) = 2`; M0 at the prior keys `d, d'` transfers by frame on those entries. M1: `{d, d'} ⊆ {d, d', d_alt}`. C0/C1/C1b/C1c/C2/C-fin hold by frame on `C`; C2 carries the prior content keys' origins `d` (for `a, a'`) and `d'` (for `a''`), all preserved by M1's extension. L0/L1/L1a/L1b/L1c/L3/L12/L-fin hold by frame on `L`; L1a carries `origin(ℓ) = origin(ℓ_new) = d` and `origin(ℓ'') = d'`, preserved by M1. L14: `dom(C₉) ∩ dom(L₉) = {a, a', a''} ∩ {ℓ, ℓ'', ℓ_new} = ∅` (verified by L0's `E(·)₁` partition and StoreT4Validity + T7). ChainMembershipForOrigin transfers at `Σ₉`: under `d`, content gives `{a, a'} = {t₁, t₂}` with `m_d = 2` and link gives `{ℓ, ℓ_new} = {s₁, s₂}` with `n_d = 2`; under `d'`, content gives `{a''} = {t₁}` with `m_{d'} = 1` and link gives `{ℓ''} = {s₁}` with `n_{d'} = 1`; under `d_alt`, both intersections are `∅` with `m_{d_alt} = n_{d_alt} = 0` (vacuous, first emissions under `d_alt` still pending). StoreT4Validity transfers by frame on `C` and `L` together with M1's monotonicity preserving the chain-membership witnesses.

The extended example confirms invariants M0, M1, C0–C2, C-fin, L0–L14, L-fin at each successor state across three documents, exercises both first-emit and subsequent-emit branches of K.α (Steps 2, 4, 6) and K.λ (Steps 3, 7, 8), verifies the Cross-document disjointness lemma (ASN-0040 B7) for both a prefix-comparable document pair (Step 5, `d ≺ d'`) and a prefix-incomparable pair (Step 9, `(d, d_alt)` and `(d', d_alt)`), underwrites cross-document freshness at Steps 6, 7, and 8, and exhibits the ChainMembershipForOrigin lemma's contiguous-prefix postcondition together with the ChainPrefixExtension lemma at every emission past the first.


## Discharge of stated invariants

**Simultaneous-induction framing.** The properties this note establishes decompose into two groups by their quantification structure:

- *Chain-indexed properties (state-independent, once chains are fixed).* ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, and ChainPrefixExtension all quantify over the sub-allocator chains supplied by ChainDiscipline; their conclusions are determined per-chain (once the chain is fixed at `d`'s K.σ-time activation, the conclusion holds once-and-for-all for every chain index `n ≥ 1`). Each is a direct ASN-0040 citation (B6(a), the SiblingStream postconditions, S0, B5a, S1, B7) applied to the sibling stream `S(b_·(d), 1)`, as recorded in the *Address sub-allocators under documents* section. No induction over substrate-level transitions is required.
- *Transition-indexed properties (state-dependent).* The stated invariants (M0, M1, C0, C1, C1b, C1c, C2, C-fin, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin) together with the ChainMembershipForOrigin lemma, the StoreT4Validity corollary, and the FirstEmissionFreshness lemma are proved by *simultaneous induction* over transition sequences from `Σ₀`. The inductive hypothesis at each step is the *conjunction* of every transition-indexed property at the current state `Σ`; the inductive step exhibits each holding at `Σ'` using the conjoined IH. No inductive step uses a conclusion derived in the same step. The per-transition discharges are recorded in the discharge matrix below and in the ChainMembershipForOrigin proof above.

Each transition-indexed invariant is discharged by induction on transition sequences from `Σ₀`. The inductive step is recorded as a per-(invariant, transition) matrix; entries describe how each transition kind preserves or discharges each invariant.

**Base case verification (at `Σ₀ = (∅, ∅, ∅)`).** Most invariants are vacuously satisfied: M0/M1/C1/C1b/C1c/C2/L0/L1/L1a/L1b/L1c/L3 quantify over `dom(C)`, `dom(L)`, or `dom(M)`, all empty at `Σ₀`. C0 and L12 quantify over transitions `Σ → Σ'`, vacuous at `Σ₀` until the first transition fires. Three invariants are non-vacuous but trivially satisfied at `Σ₀`:

- **L14** (`dom(C) ∩ dom(L) = ∅`): at `Σ₀`, both stores empty, so `∅ ∩ ∅ = ∅` — trivially true.
- **L-fin** (`|dom(L)| < ∞`): `|∅| = 0 < ∞` — trivially true.
- **C-fin** (`|dom(C)| < ∞`): `|∅| = 0 < ∞` — trivially true.

*Derived lemmas at Σ₀.* ChainPrefixExtension (transition-independent in conclusion, but quantified over `d ∈ dom(M)`) holds vacuously at `Σ₀` since `dom(M₀) = ∅`. ChainMembershipForOrigin holds vacuously: for every `d` (vacuous since `dom(M₀) = ∅`), both `dom(C₀) ∩ {a' : origin(a') = d} = ∅ ∩ … = ∅ = {t_1, …, t_0}` witnessing `m_d = 0` and similarly `n_d = 0` for the link clause. StoreT4Validity holds vacuously over the empty stores. FirstEmissionFreshness has no firing context at `Σ₀` (no K.α or K.λ event has fired), so the predicate ranges over no events. The other chain-indexed disciplines (ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains) are state-independent ASN-0040 citations holding for every sibling stream `S(b_·(d), 1)` — including the vacuously empty family of sub-allocator chains at `Σ₀`.

The base case holds.

**Inductive step.** Per (invariant, transition):

| Invariant | K.σ | K.α | K.λ |
|---|---|---|---|
| **M0** (DocumentTumblerWellFormed) | Discharged at new key: precondition pins `ValidAddress(d) ∧ zeros(d) = 2` | Preserved: `M` in frame | Preserved: `M` in frame |
| **M1** (ArrangementMonotonicity) | Discharged: effect extends `dom(M)` by union | Preserved: `M` in frame | Preserved: `M` in frame |
| **C0** (ContentImmutability) | Preserved: `C` in frame | Discharged: effect extends `dom(C)` at fresh `a` with value `v`; value at existing keys unaltered (definitional in effect clause) | Preserved: `C` in frame |
| **C1** (ContentElementLevel) | Preserved: `C` in frame | Discharged at new key: precondition pins `zeros(a) = 3` | Preserved: `C` in frame |
| **C1b** (ContentElementFieldDepth) | Preserved: `C` in frame (`E(·)` structural — see C1b) | Discharged at new key: precondition pins `#E(a) ≥ 2` | Preserved: `C` in frame |
| **C1c** (ContentAllocatorConformance) | Preserved: `C` in frame | Discharged at new key via the T10a-conforming step sequence (see *C1c chain exhibition* below — first-emit and subsequent-emit cases) | Preserved: `C` in frame |
| **C2** (ContentScopedAllocation) | Preserved: vacuously (no new content); for prior keys `a ∈ dom(C)`, `origin(a) ∈ dom(M) ⊆ dom(M')` (`C` in frame, M1 extends `dom(M)`) | Discharged at new key: precondition pins `origin(a) = d ∧ d ∈ dom(M)`; preserved at prior keys (`origin(·)` is structural, M1 extends `dom(M)`) | Preserved: `C` in frame; prior keys preserved by M1 |
| **L0** (SubspacePartition) | Preserved: `L`, `C` in frame | Preserved on L-clause (`L` in frame); discharged at new key on C-clause via `E(a)₁ = s_C` precondition — auto-satisfied (see L0 discharge note) | Discharged at new key on L-clause via `E(ℓ)₁ = s_L` precondition — auto-satisfied (see L0 discharge note); preserved on C-clause (`C` in frame) |
| **L1** (LinkElementLevel) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `zeros(ℓ) = 3` |
| **L1a** (LinkScopedAllocation) | Preserved: vacuously (no new link); for prior keys `ℓ ∈ dom(L)`, `origin(ℓ) ∈ dom(M) ⊆ dom(M')` (M1 extends `dom(M)`) | Preserved: `L` in frame; prior keys preserved by M1 | Discharged at new key: precondition pins `origin(ℓ) = d ∧ d ∈ dom(M)`; prior keys preserved by M1 |
| **L1b** (LinkElementFieldDepth) | Preserved: `L` in frame (`E(·)` structural — see C1b) | Preserved: `L` in frame (see C1b) | Discharged at new key: precondition pins `#E(ℓ) ≥ 2` |
| **L1c** (LinkAllocatorConformance) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key via the T10a-conforming step sequence (see *L1c chain exhibition* below — first-emit and subsequent-emit cases) |
| **L3** (NEndsetStructure) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged at new key: precondition pins `|L(ℓ)| ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` |
| **L12** (LinkImmutability) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: effect extends `dom(L)` at fresh `ℓ`; value at existing keys unaltered (definitional) |
| **L14** (StoreDisjointness) | Preserved by frame: `C`, `L` both in frame, so IH-L14 (`dom(C) ∩ dom(L) = ∅`) transfers directly | Discharged at the new key `a` (see L14 new-key discharge note); prior keys by IH-L14 + frame on `L` | Discharged at the new key `ℓ`, symmetric (see L14 new-key discharge note); prior keys by IH-L14 + frame on `C` |
| **L-fin** (LinkStoreFiniteness) | Preserved: `L` in frame | Preserved: `L` in frame | Discharged: `|dom(L')| = |dom(L)| + 1`; finiteness closed under +1 |
| **C-fin** (ContentStoreFiniteness) | Preserved: `C` in frame | Discharged: `|dom(C')| = |dom(C)| + 1`; finiteness closed under +1 | Preserved: `C` in frame |

*Lemma preservation across transitions.* The transition-indexed lemmas additionally discharged at each step:

| Lemma | K.σ | K.α | K.λ |
|---|---|---|---|
| **ChainMembershipForOrigin** | Preserved: `C`, `L` in frame; for the freshly registered `d_new`, both intersection sets `dom(C') ∩ {a' : origin(a') = d_new}` and `dom(L') ∩ {ℓ' : origin(ℓ') = d_new}` are `∅`, witnessing `m_{d_new} = n_{d_new} = 0` (see lemma proof above) | Preserved at `d' ≠ d` by frame on `dom(C)|_{d'}`; at `d` extended at chain index `m_d + 1` (first-emit by FirstEmission, subsequent-emit by ChainDiscipline + ChainEnumerationInjectivity placing `a = t_{m_d + 1}`); link clause unchanged by frame on `dom(L)` | Symmetric to K.α (content↔link); see lemma proof above |
| **StoreT4Validity** | Preserved: `C`, `L` in frame, so the existing T4-validity of every entry transfers; no new key | Preserved at prior keys (`C` in frame); at the new key `a`, T4-validity from ChainElementT4Validity applied to `A_C(d)` (every chain element is T4-valid by chain induction grounded at FirstEmission's T4-valid first emission, covering both first-emit and subsequent-emit branches) | Symmetric (content↔link); at the new key `ℓ`, ChainElementT4Validity applied to `A_L(d)` (every chain element is T4-valid by chain induction grounded at FirstEmission's T4-valid first emission, covering both first-emit and subsequent-emit branches) |
| **FirstEmissionFreshness** | No firing context: K.σ does not commit a content/link first emission | Discharged at the K.α event when the first-emit predicate fires, by FirstEmissionFreshness (lemma above) | Symmetric to K.λ (content↔link) |

The chain-indexed disciplines (ChainElementT4Validity, ChainUniformLength, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains, ChainPrefixExtension) are not state-dependent in their conclusions and so require no per-transition discharge; their once-and-for-all status as ASN-0040 citations is established in *Per-chain disciplines* above.

*C1c chain exhibition.* The substrate's C1c is "every content address has a T10a-conforming step sequence from its home document." For `K.α`'s discharge, two sub-cases:

**First-emit case** (`a = [d.0.s_C.1]`, predicate `{a' ∈ dom(C) : origin(a') = d} = ∅`). The T10a-conforming step sequence witnessing C1c is two inc steps from `d`:

  `(t₀, t₁, t₂)` where `t₀ = d`, `t₁ = inc(d, 2) = b_C(d)`, `t₂ = inc(b_C(d), 1) = [d.0.s_C.1] = a`

Per-step admissibility:

- `t₁ = inc(d, 2)`: TA5a (IncrementPreservesT4, ASN-0034) at `k = 2` requires `zeros(d) ≤ 2`; by M0, `zeros(d) = 2`, satisfied — hence `t₁` is T4-valid. TA5(d) at `k = 2` gives the structural form: `zeros(t₁) = 2 + (2 − 1) = 3` and `#t₁ = #d + 2`. The value at position `#d + 2` is `1 = s_C` (per SubspaceConventionAxiom), establishing `E(t₁)₁ = s_C` and `#E(t₁) = 1`.
- `t₂ = inc(b_C(d), 1)`: TA5a at `k = 1` requires `zeros(t₁) ≤ 3`, discharged by `t₁`'s T4-validity (T4 forces `zeros ≤ 3`), so `t₂` is T4-valid given `t₁` T4-valid. TA5(d) at `k = 1` gives the structural form: the new component appended at position `#b_C(d) + 1` is `1`, so `zeros(t₂) = 3 + 0 = 3` (k = 1 introduces no new zero), with `#E(t₂) = 2` and `E(t₂)₁ = s_C` inherited from `t₁` per TA5(b).

C1c's strengthened clauses: `k₁ = 2` by construction (step 1 above); `n = 2 ≥ 1` ✓; `#t₁ = #d + 2 > #d` and `#t₂ = #d + 3 > #d`, so `(A i : 1 ≤ i ≤ 2 : #tᵢ > #origin(a))` holds.

**Subsequent-emit case** (`a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`, predicate `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`). Let `a_prev = max{a' ∈ dom(C) : origin(a') = d}`. By the inductive hypothesis on C1c, `a_prev` has a T10a-conforming step sequence `(t₀, …, t_n)` with `t₀ = d`, `t_n = a_prev`, `k₁ = 2`, and `(A i : 1 ≤ i ≤ n : #tᵢ > #d)`. The chain for `a` extends this by one step: `(t₀, …, t_n, t_{n+1})` with `t_{n+1} = inc(t_n, 0) = inc(a_prev, 0) = a`. Per-step admissibility of the new step `t_{n+1} = inc(a_prev, 0)`: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `t_{n+1}` is T4-valid given `a_prev` T4-valid (the latter supplied by ChainElementT4Validity applied to `A_C(d)`'s chain at `a_prev`); TA5(c) at `k = 0` gives the structural form (length preservation, single-position modification at `sig(a_prev)`). Within-chain freshness against the rest of `A_C(d)`'s chain is discharged by ChainEnumerationInjectivity applied to `(a_prev, a)`, with both indices established to inhabit `A_C(d)` by ChainMembershipForOrigin (`a_prev ∈ A_C(d)` from the inductive hypothesis applied at `Σ`) and ChainDiscipline's closure under `inc(·, 0)` (`a = inc(a_prev, 0) ∈ A_C(d)`); cross-document collisions with other documents' content chains are ruled out by the Cross-document disjointness lemma. C1c's strengthened clauses on the extended chain: `k₁ = 2` is inherited unchanged from the IH chain; `n + 1 ≥ 1` ✓; for the new step, TA5(c) gives `#t_{n+1} = #t_n > #d` (so the universal `#tᵢ > #d` extends to `i = n + 1`).

*L1c chain exhibition.* The substrate's L1c is "every link address has a T10a-conforming step sequence from its home document." For `K.λ`'s discharge, two sub-cases:

**First-emit case** (`ℓ = [d.0.s_L.1]`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`). The T10a-conforming step sequence witnessing L1c is three inc steps from `d`:

  `(t₀, t₁, t₂, t₃)` where `t₀ = d`, `t₁ = inc(d, 2) = b_C(d)`, `t₂ = inc(b_C(d), 0) = b_L(d)`, `t₃ = inc(b_L(d), 1) = [d.0.s_L.1] = ℓ`

Per-step admissibility:

- `t₁ = inc(d, 2)`: TA5a (IncrementPreservesT4, ASN-0034) at `k = 2` requires `zeros(d) ≤ 2`; by M0, `zeros(d) = 2`, satisfied — hence `t₁` is T4-valid. TA5(d) at `k = 2` gives the structural form: `zeros(t₁) = 2 + (2 − 1) = 3`.
- `t₂ = inc(b_C(d), 0)`: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `t₂` is T4-valid given `b_C(d)` T4-valid. TA5(c) at `k = 0` gives the structural form: length is preserved and the sibling component is advanced from `s_C` to `s_L`. By SubspaceConventionAxiom, `s_C = 1` and `s_L = 2`, so `inc([d.0.1], 0) = [d.0.2] = b_L(d)`. This step's correctness depends substantively on `s_L = s_C + 1`; the SubspaceConventionAxiom underwrites it.
- `t₃ = inc(b_L(d), 1)`: TA5a at `k = 1` requires `zeros(b_L(d)) ≤ 3`, discharged by `b_L(d)`'s T4-validity (T4 forces `zeros ≤ 3`), so `t₃` is T4-valid given `b_L(d)` T4-valid. TA5(d) at `k = 1` gives the structural form: `zeros(t₃) = 3 + 0 = 3` (k = 1 introduces no new zero), with `#E(t₃) = 2`.

L1c's strengthened clauses: `k₁ = 2` by construction (step 1 above); `n = 3 ≥ 1` ✓; `#t₁ = #d + 2 > #d`, `#t₂ = #d + 2 > #d`, `#t₃ = #d + 3 > #d`, so `(A i : 1 ≤ i ≤ 3 : #tᵢ > #origin(ℓ))` holds.

Note that the C1c first-emit chain has *two* inc steps (`d → b_C(d) → a`) while the L1c first-emit chain has *three* (`d → b_C(d) → b_L(d) → ℓ`) — they are not parallel chains differing only in a single-step substitution. The link chain must traverse the additional `inc(b_C(d), 0) = b_L(d)` step because the link subspace anchor sits one sibling-component beyond the content subspace anchor.

**Subsequent-emit case** (`ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)`, predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`). Let `ℓ_prev = max{ℓ' ∈ dom(L) : origin(ℓ') = d}`. By the inductive hypothesis on L1c, `ℓ_prev` has a T10a-conforming step sequence `(t₀, …, t_n)` with `t₀ = d`, `t_n = ℓ_prev`, `k₁ = 2`, and `(A i : 1 ≤ i ≤ n : #tᵢ > #d)`. The chain for `ℓ` extends this by one step: `(t₀, …, t_n, t_{n+1})` with `t_{n+1} = inc(t_n, 0) = inc(ℓ_prev, 0) = ℓ`. Per-step admissibility of the new step `t_{n+1} = inc(ℓ_prev, 0)`: TA5a at `k = 0` is unconditionally T4-preserving (no side condition), so `t_{n+1}` is T4-valid given `ℓ_prev` T4-valid (the latter supplied by ChainElementT4Validity applied to `A_L(d)`'s chain at `ℓ_prev`); TA5(c) at `k = 0` gives the structural form (length preservation, single-position modification at `sig(ℓ_prev)`). Within-chain freshness against the rest of `A_L(d)`'s chain is discharged by ChainEnumerationInjectivity applied to `(ℓ_prev, ℓ)`, with both indices established to inhabit `A_L(d)` by ChainMembershipForOrigin (`ℓ_prev ∈ A_L(d)` from the inductive hypothesis applied at `Σ`) and ChainDiscipline's closure under `inc(·, 0)` (`ℓ = inc(ℓ_prev, 0) ∈ A_L(d)`); cross-document collisions with other documents' link chains are ruled out by the Cross-document disjointness lemma. L1c's strengthened clauses on the extended chain: `k₁ = 2` is inherited unchanged from the IH chain; `n + 1 ≥ 1` ✓; for the new step, TA5(c) gives `#t_{n+1} = #t_n > #d` (so the universal `#tᵢ > #d` extends to `i = n + 1`).


## Properties Introduced

| ID | Name | Status | Source |
|---|---|---|---|
| M0 | DocumentTumblerWellFormed | INV | Substrate, established at K.σ (precondition pins `ValidAddress(d) ∧ zeros(d) = 2` at the new key); preserved at K.α/K.λ by frame on `M` |
| M1 | ArrangementMonotonicity | INV | Substrate, established at K.σ by union extension `dom(M') = dom(M) ∪ {d}`; preserved at K.α/K.λ by frame on `M` |
| C0 | ContentImmutability | INV | Substrate, restated from ASN-0036's S0/S1; established at K.α (effect extends `dom(C)` with new pair and leaves existing values unchanged); preserved at K.σ/K.λ by frame on `C` |
| C1 | ContentElementLevel | INV | Substrate, restated from ASN-0036's S7b; established at K.α (precondition pins `zeros(a) = 3` at the new key); preserved at K.σ/K.λ by frame on `C` |
| C1b | ContentElementFieldDepth | INV | Substrate-level commitment (content-side analog of L1b; ASN-0036 carries no content-side `#E(a) ≥ 2` invariant); established at K.α (precondition pins `#E(a) ≥ 2` at the new key); preserved at K.σ/K.λ by frame on `C` |
| C1c | ContentAllocatorConformance | INV | Substrate, content-side analog of L1c, stated in parallel form (including `k₁ = 2` and `#tᵢ > #origin(a)` clauses); established at K.α via the C1c chain exhibition (first-emit chain has two steps `(d → b_C(d) → a)` with `k₁ = 2`, `k₂ = 1` and lengths `#d → #d + 2 → #d + 3`, all strictly exceeding `#d`; subsequent-emit extends a length-monotone chain by `inc(·, 0)` and inherits `k₁ = 2`). The first-emit gap is closed by the FirstEmission lemma, subsequent-emit by ChainDiscipline (ChainEnumerationInjectivity); preserved at K.σ/K.λ by frame on `C` |
| C2 | ContentScopedAllocation | INV | Substrate, content-side analog of L1a; established at K.α (precondition pins `origin(a) = d ∧ d ∈ dom(M)` at the new key); preserved at K.σ/K.λ by frame on `C` and M1's monotonicity of `dom(M)` |
| L0 | SubspacePartition | INV | L-clause from ASN-0043; C-clause added here. Established at K.α (C-clause, via `E(a)₁ = s_C` precondition) and K.λ (L-clause, via `E(ℓ)₁ = s_L` precondition); preserved at K.σ by frame on both `C` and `L` |
| L1 | LinkElementLevel | INV | ASN-0043; established at K.λ (precondition pins `zeros(ℓ) = 3` at the new key); preserved at K.σ/K.α by frame on `L` |
| L1a | LinkScopedAllocation | INV | ASN-0043 (refactored: `E_doc` → `dom(M)`); established at K.λ (precondition pins `origin(ℓ) = d ∧ d ∈ dom(M)` at the new key); preserved at K.σ/K.α by frame on `L` and M1's monotonicity of `dom(M)` |
| L1b | LinkElementFieldDepth | INV | ASN-0043; established at K.λ (precondition pins `#E(ℓ) ≥ 2` at the new key); preserved at K.σ/K.α by frame on `L` |
| L1c | LinkAllocatorConformance | INV | ASN-0043, restated verbatim including the `k₁ = 2` and `#tᵢ > #origin(ℓ)` clauses. Established at K.λ via the L1c chain exhibition (first-emit chain has three steps `(d → b_C(d) → b_L(d) → ℓ)` with `k₁ = 2`, `k₂ = 0`, `k₃ = 1` and monotonically increasing lengths `#d → #d + 2 → #d + 2 → #d + 3`, all strictly exceeding `#d`; subsequent-emit extends a length-monotone chain by `inc(·, 0)` and inherits `k₁ = 2` from the prior chain). The first-emit gap is closed by the FirstEmission lemma, subsequent-emit by ChainDiscipline (ChainEnumerationInjectivity); preserved at K.σ/K.α by frame on `L` |
| L3 | NEndsetStructure | INV | ASN-0043; established at K.λ (precondition pins `|L(ℓ)| ≥ 3 ∧ (e₃) ≠ ∅`); preserved at K.σ/K.α by frame on `L` |
| L12 | LinkImmutability | INV | ASN-0043; established at K.λ (effect extends `dom(L)` with new pair and leaves existing values unchanged); preserved at K.σ/K.α by frame on `L` |
| L14 | StoreDisjointness | INV (derived) | L0 + SC-NEQ + StoreT4Validity + T7 |
| L-fin | LinkStoreFiniteness | INV (derived) | Inductively from `Σ₀.L = ∅` + K.λ |
| C-fin | ContentStoreFiniteness | INV (derived) | Inductively from `Σ₀.C = ∅` + K.α |
| ChainDiscipline | ContentLinkSubAllocatorChainDiscipline | LEMMA (derived) | The content/link sub-allocator chains are the ASN-0040 sibling streams `A_C(d) = S(b_C(d), 1)`, `A_L(d) = S(b_L(d), 1)` (SiblingStream, ASN-0040): `c₁ = inc(anchor, 1)` (first emission), `cₙ₊₁ = inc(cₙ, 0)`, coinciding by construction with the K.α/K.λ emission rules. Each parent `(b_·(d), 1)` is `B6`-valid (T4-valid anchor, `zeros = 3`, depth `1`, `zeros + (1−1) = 3 ≤ 3`), so all `B6`-preconditioned ASN-0040 results apply. |
| FirstEmission | FirstEmission | LEMMA (derived) | The first emission of `A_C(d)` (resp. `A_L(d)`) is `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`), T4-valid. Discharged by ChainDiscipline + ASN-0040's SiblingStream postcondition `cₙ = [p₁,…,p_{#p},0…0,n]` + TA5a (`k = 1` preserves T4 on a T4-valid input). |
| ChainElementT4Validity | ChainElementT4Validity | CITATION | Every element of `A_C(d)` (resp. `A_L(d)`) is T4-valid. Cites ASN-0040 B6(a) (ValidDepth sufficiency) at `B6(b_·(d), 1)`. |
| ChainUniformLength | ChainUniformLength | CITATION | All elements of `A_C(d)` (resp. `A_L(d)`) have length `#d + 3`. Cites ASN-0040's SiblingStream postcondition `#cₙ = #p + d` at `p = b_·(d)`, depth `1`. |
| ChainEnumerationInjectivity | ChainEnumerationInjectivity | CITATION | The enumeration of `A_C(d)` (resp. `A_L(d)`) is strictly increasing under T1; hence injective and (by T1 trichotomy) order-preserving in both directions. Cites ASN-0040 S0 (StreamOrdering). |
| ChainUniformZeroCount | ChainUniformZeroCount | CITATION | Every element of `A_C(d)` (resp. `A_L(d)`) has `zeros = 3`. Cites ASN-0040's SiblingStream postcondition (`d − 1 = 0` interior zeros at depth `1`) / B5a (SiblingZerosPreservation). |
| DisjointSubAllocatorChains | DisjointSubAllocatorChains | CITATION | `A_C(d) ∩ A_L(d) = ∅`, with addresses of `A_C(d)` (resp. `A_L(d)`) carrying `E(·)₁ = s_C` (resp. `s_L`). Cites ASN-0040 B7 (NamespaceDisjointness) at the distinct `B6`-valid parents `(b_C(d), 1)`, `(b_L(d), 1)` (anchors disagree at position `#d + 2`, `s_C` vs `s_L`, by SC-NEQ). |
| ChainPrefixExtension | ChainPrefixExtension | CITATION | Every chain element extends its anchor under Prefix: `b_C(d) ≼ t` for `t ∈ A_C(d)`, `b_L(d) ≼ t` for `t ∈ A_L(d)`. Cites ASN-0040 S1 (StreamPrefix) at `p = b_·(d)`; the abstract-stream quantifier covers chain elements not yet committed. |
| ChainMembershipForOrigin | ChainMembershipForOrigin | LEMMA | Inductive invariant in *contiguous-prefix form* at every reachable state: `dom(C) ∩ {a' : origin(a') = d} = {t₁, …, t_{m_d}}` is a contiguous initial segment of `A_C(d)` (mirror for `L`). The subset inclusion `dom(C) ∩ {a' : origin(a') = d} ⊆ A_C(d)` is the weaker corollary. Proved by induction over transitions using the FirstEmission lemma (first-emit branches placing `t₁`) and ChainDiscipline + ChainEnumerationInjectivity (subsequent-emit branches placing `t_{m_d + 1} = inc(t_{m_d}, 0)`). Licenses application of ChainEnumerationInjectivity to `(a_prev, a)` and `(ℓ_prev, ℓ)` in K.α/K.λ subsequent-emit cases; the contiguous-prefix form matches ASN-0040's B1 (ContiguousPrefix). |
| StoreT4Validity | StoreT4Validity | LEMMA (derived) | Derived from ChainMembershipForOrigin + ChainElementT4Validity: every entry of `dom(C) ∪ dom(L)` inhabits a sub-allocator chain whose every element is T4-valid. |
| FirstEmissionFreshness | FirstEmissionFreshness | LEMMA (derived) | Derived from the first-emit predicate + L0 + ChainPrefixExtension + ChainMembershipForOrigin + StoreT4Validity + Cross-document disjointness + SC-NEQ + T7 + ChainElementT4Validity. At every K.α (resp. K.λ) event firing the first-emit predicate, the first emission `[d.0.s_C.1]` (resp. `[d.0.s_L.1]`) is fresh against `dom(C) ∪ dom(L)`. |
| Cross-doc disjointness | ASN-0040 B7 lemma | CITATION | `A_·(d₁) ∩ A_·(d₂) = ∅` for distinct `d₁, d₂ ∈ dom(M)`. Cites ASN-0040 B7 (NamespaceDisjointness) at the distinct `B6`-valid parents `(b_·(d₁), 1)`, `(b_·(d₂), 1)` (distinct since `d₁ ≠ d₂` forces `b_·(d₁) ≠ b_·(d₂)`). The equivalent anchor prefix-incomparability `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (from M0 + T4 + Prefix, ASN-0034) plus T10 (PartitionIndependence) gives the alternative T10 form consumers may cite. |
| SubspaceConventionAxiom | FixedSubspaceIdentifiers | AXIOM | Substrate commitment: `s_C = 1 ∧ s_L = 2`; pinned by Nelson (LM 4/30–4/31) and Gregory (`xanadu.h:144–146`, `granf2.c:162`, `do2.c:94`). Underwrites L14 derivation and the L1c chain exhibition. |
| SequentialTransitionAxiom | SequentialAtomicTransitions | AXIOM | Substrate commitment: `Σ → Σ'` is atomic, uninterruptible, totally ordered. |
| K.σ | DocumentRegistration | OP | Substrate-level document introduction into `dom(M)` |
| K.α | ContentAllocation | OP | Substrate-level content emission |
| K.λ | LinkAllocation | OP | Substrate-level link emission |


## Open Questions

- *Link withdrawal — which invariant must a withdrawal mechanism revisit?* A withdrawal mechanism (deferred per Scope) admits at least three formulations: (a) a *value transition* that mutates `L(a)`, (b) an *arrangement-side* retraction that leaves `L(a)` intact, and (c) an *embedded-marker* (tombstone) scheme. The load-bearing constraint is L12's value-equality clause `L'(a) = L(a)`: formulation (a) must restate L12 (its domain-persistence clause may stand), while (b) and (c) leave L12 intact. Which of the three to adopt — and whether L12 must be weakened — is the design decision the withdrawal ASN must make.

- *Higher-arity link discipline.* L3 admits arbitrary `N ≥ 3`. Should a higher layer impose an upper bound on arity, or constrain slot interpretation or relations between slots — for example, fixing the StandardTriple convention as a structural commitment rather than a notational default?

- *Concurrency.* `K.σ`, `K.α`, and `K.λ` are stated as atomic transitions; what discipline governs concurrent emission across multiple allocators?

- *Sub-allocator stratification beyond `A_C(d)` and `A_L(d)`.* Future subspace identifiers `s ≥ 3` would require parallel sub-allocators; the present axiom commits to exactly two (content and link). What discipline coordinates a third subspace?
