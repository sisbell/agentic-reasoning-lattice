# ASN-0097: Link Projection Displacement

*2026-05-24*

A link is created in some state `Σ` with endsets that reference specific I-addresses. The state then evolves: documents are arranged and rearranged, content is added, versions are forked, transclusions appear. Across all this, what does the link holder still hold? What survives without modification, what is permitted to change, and how is the change constrained?

The answer is two-layered. The link's *structure* — its address in `dom(L)`, its value (the tuple of endsets), its arity, its slot assignments, the coverage of each endset — is absolutely permanent. No reachable state alters any of these. By contrast, the link's *projection* into any particular document's V-space — the set of V-positions that currently realize the link's endset coverage in that document — is computed live from the current arrangement and may shift, narrow, or vanish. The link is never broken by such changes; what changes is only how it currently *appears* through one or another document's view.

We call this two-layered behavior *projection displacement*: the projection is displaced by arrangement changes, while the link's structure remains in place.

## Setting

We work over states `Σ = (C, L, E, M, R)` introduced in the foundation ASNs. Three components are central here:

- `Σ.C : T ⇀ Val` — the content store (ASN-0036). By `S0`, once `a ∈ dom(Σ.C)`, then `a ∈ dom(Σ'.C)` and `Σ'.C(a) = Σ.C(a)` in every successor state. The store is append-only with immutable values.
- `Σ.L : T ⇀ Link` — the link store (ASN-0043). By `L12`, once `ℓ ∈ dom(Σ.L)`, then `ℓ ∈ dom(Σ'.L)` and `Σ'.L(ℓ) = Σ.L(ℓ)` in every successor. The store is append-only with immutable values.
- `Σ.M : D × T ⇀ T` — the family of per-document arrangements (ASN-0036). For each `d ∈ E_doc`, `Σ.M(d)` maps V-positions to I-addresses. Unlike `C` and `L`, an individual `Σ.M(d)` may both grow and shrink across transitions: the transition vocabulary (ASN-0047) provides `K.μ⁺` for extension, `K.μ⁻` for contraction, and `K.μ~` for rearrangement.

A link value (L3, ASN-0043) is a tuple of `N ≥ 3` endsets `(e₁, ..., e_N)`, each `eᵢ ∈ Endset` — a finite set of well-formed I-space spans. The *coverage* of an endset (ASN-0043) is

`cov(e) = (∪ (s, w) ∈ e : {t ∈ T : s ≤ t < s ⊕ w})`

— the set of I-addresses the endset references. Coverage is a set in `T`. It is independent of the particular span decomposition `e` happens to use: two endsets whose span tuples differ but whose denoted address sets are equal have the same coverage.

## Foundation Contracts

The proofs in this ASN rest on specific contracts established in ASN-0006, ASN-0036, ASN-0043, and ASN-0047. We restate the load-bearing ones inline so the reasoning here is independently checkable. Each contract below is named so the proofs can cite it without consulting the originating ASN.

**From the global identity foundation (ASN-0006).**

- **T10a (GlobalUniqueness).** Every allocator produces an address that has never previously been allocated; allocator freshness is a global guarantee on the address space, not merely local to a subspace.

**From the address-space and arrangement foundation (ASN-0036).**

- **S0 (ContentImmutability).** `(A Σ → Σ', a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`. Once allocated, a content address remains in `dom(C)` forever, and its stored value never changes.
- **S1 (StoreMonotonicity).** `(A Σ → Σ' :: dom(Σ.C) ⊆ dom(Σ'.C))`. The content store grows monotonically across transitions.
- **S3 (ReferentialIntegrity).** For each `d ∈ E_doc`, `ran(Σ.M(d)) ⊆ dom(Σ.C)`. We flag here that the exact reading of `dom(Σ.C)` on the RHS — whether it admits link addresses (i.e., `dom(C)` is to be read as `dom(C) ∪ dom(L)` in the stratified interpretation, or as text-content only) — is a foundation-level question this ASN cannot settle. Where the proof depends on a stratified reading, we state local premises at the point of use (see Π15a).
- **S8a (SubspaceProjection).** The I-address space `T` is partitioned by a `subspace : T → S` function; for every `t ∈ T`, `subspace(t)` identifies which subspace `t` inhabits. The partition extends to V-positions: every `v ∈ dom(Σ.M(d))` has `subspace(v) ∈ S`.

**From the link foundation (ASN-0043).**

- **L0 (LinkAddressing).** Link addresses inhabit a distinct subspace `s_L ⊆ T`; text-content addresses inhabit `s_C ⊆ T`; `s_L ∩ s_C = ∅`.
- **L0a (LinkSubspaceMembership).** `(A ℓ ∈ dom(Σ.L) :: subspace(ℓ) = s_L)`. (Equivalently, `dom(Σ.L) ⊆ s_L`.)
- **L1c (LinkAllocatorFreshness).** When `K.λ` allocates `ℓ` from pre-state `Σ_pre`, `ℓ ∉ dom(Σ_pre.L)`. (Derived from T10a applied to the link subspace.)
- **L3 (LinkValueShape).** A link value is a tuple `(e₁, ..., e_N)` of `N ≥ 3` endsets; each `eᵢ ∈ Endset` is a finite set of well-formed I-space spans.
- **L6 (LinkValueEquality).** Link values are equal iff their endset tuples are componentwise equal: `v₁ = v₂ ⟺ (A i :: v₁.eᵢ = v₂.eᵢ)`. The slot index `i ∈ {1, ..., N}` is a primitive positional accessor.
- **L7 (LinkDirectionalRoles).** Each link slot index `i ∈ {1, ..., N}` has a directional role assigned by the link's type. The role assignment is a fixed function `Role : LinkType × ℕ → Direction` that is Σ-external (a constant function on its domain, not a component of any state `Σ`).
- **L12 (LinkValuePermanence).** `(A Σ → Σ', ℓ ∈ dom(Σ.L) :: ℓ ∈ dom(Σ'.L) ∧ Σ'.L(ℓ) = Σ.L(ℓ))`. The link store is append-only with immutable values.
- **L14 (LinkSubspaceDisjointness).** `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`. (A direct consequence of L0 + L0a + S0-allocator placement of content addresses in `s_C`.)

**From the transition-vocabulary foundation (ASN-0047).**

- **K.α (ContentAllocation).** Allocates a fresh address `a_new` to `dom(C)` with `a_new ∉ dom(Σ_pre.C)` (freshness, via T10a applied to `s_C`). *Frame:* writes only to `Σ.C`; for every `d ∈ E_doc`, `Σ'.M(d) = Σ.M(d)`; `Σ'.L = Σ.L`.
- **K.λ (LinkAllocation).** Allocates a fresh link `ℓ` to `dom(L)` with value `v = (e₁, ..., e_N)`; `ℓ ∉ dom(Σ_pre.L)` (L1c freshness). *Frame:* writes only to `Σ.L`; for every `d ∈ E_doc`, `Σ'.M(d) = Σ.M(d)`; `Σ'.C = Σ.C`.
- **K.μ⁺ (ArrangementExtension).** For target document `d`, extends `Σ.M(d)` to `Σ'.M(d)` with `dom(Σ'.M(d)) ⊇ dom(Σ.M(d))` and `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ.M(d))` (existing pairs preserved). *Frame:* writes only to `Σ.M(d)`; `Σ.M(d') = Σ'.M(d')` for `d' ≠ d`; `Σ.C` and `Σ.L` unchanged.
- **K.μ⁻ (ArrangementContraction).** For target `d`, contracts `Σ.M(d)` to `Σ'.M(d)` with `dom(Σ'.M(d)) ⊆ dom(Σ.M(d))` and `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ dom(Σ'.M(d))` (retained pairs preserved). *Frame:* writes only to `Σ.M(d)`; `Σ.M(d') = Σ'.M(d')` for `d' ≠ d`; `Σ.C` and `Σ.L` unchanged.
- **K.μ~ (ArrangementRearrangement).** For target `d`, transforms `Σ.M(d)` to `Σ'.M(d)` via a bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))` satisfying `Σ'.M(d)(π(v)) = Σ.M(d)(v)`. **K.μ~-FIX:** the bijection has equal domain and codomain — `dom(Σ'.M(d)) = dom(Σ.M(d))`. *Frame:* writes only to `Σ.M(d)`; `Σ.M(d') = Σ'.M(d')` for `d' ≠ d`; `Σ.C` and `Σ.L` unchanged.

**Local precondition on link allocation (this ASN).**

- **K.λ-cov-nonempty (local axiom).** For every slot `i ∈ {1, ..., N}` of a value allocated by `K.λ`, `cov(eᵢ) ≠ ∅`: every endset denotes at least one I-address. This is a local strengthening adopted in this ASN; we discuss the alternative — admitting `cov(eᵢ) = ∅` and observing that every projection claim then holds vacuously — in the empty-endset note in §The Projection.

These twelve contracts (plus the local K.λ-cov-nonempty premise) are the complete external dependency of the proofs that follow. Where a proof cites e.g. "L12", "K.μ⁺", or "S0", the cited contract is the inline statement above.

## The Projection

We need a bridge between the link's I-address endsets and the V-positions a reader sees in a document. We call this bridge the *projection*.

**Definition (Projection).** Given a state `Σ`, a document `d ∈ E_doc`, and an endset `e`, the *projection of `e` into `d` at `Σ`* is

`proj(d, e, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(e)}`

— the V-positions in `d` whose arrangement target lies in `e`'s coverage.

For a link `ℓ ∈ dom(Σ.L)` and slot index `i ∈ {1, ..., |Σ.L(ℓ)|}`, we write `proj(d, ℓ, i, Σ)` for `proj(d, Σ.L(ℓ).eᵢ, Σ)`.

A useful complement records *which I-addresses* the projection reaches in `d`:

`iproj(d, e, Σ) = cov(e) ∩ ran(Σ.M(d))`

Where `proj(d, e, Σ) ⊆ dom(Σ.M(d))` lives in V-space, `iproj(d, e, Σ) ⊆ T` lives in I-space, and the two are connected by the arrangement: `iproj(d, e, Σ) = Σ.M(d)(proj(d, e, Σ))`.

*Proof of the bridge equality.* ⊆: Let `a ∈ iproj(d, e, Σ) = cov(e) ∩ ran(Σ.M(d))`. From `a ∈ ran(Σ.M(d))` pick `v ∈ dom(Σ.M(d))` with `Σ.M(d)(v) = a`; combined with `Σ.M(d)(v) = a ∈ cov(e)`, this gives `v ∈ proj(d, e, Σ)`, hence `a = Σ.M(d)(v) ∈ Σ.M(d)(proj(d, e, Σ))`. ⊇: Let `a ∈ Σ.M(d)(proj(d, e, Σ))`; pick `v ∈ proj(d, e, Σ)` with `a = Σ.M(d)(v)`. From `v ∈ proj(d, e, Σ)`: `v ∈ dom(Σ.M(d))` gives `a ∈ ran(Σ.M(d))`, and `Σ.M(d)(v) ∈ cov(e)` gives `a ∈ cov(e)`. Hence `a ∈ cov(e) ∩ ran(Σ.M(d)) = iproj(d, e, Σ)`. □

The projection function consults only `Σ.M(d)` and the endset `e`. No history of how `M(d)` was constructed, no link's home document, no auxiliary registry, no other document's arrangement appears in the definition. This locality is the first nontrivial property we shall establish.

*Boundary case: empty coverage.* An endset with no spans, or with every span of zero width, satisfies `cov(e) = ∅` and is a degenerate input to `proj`. The definitions handle this case uniformly: `proj(d, e, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ ∅} = ∅`, and `iproj(d, e, Σ) = ∅ ∩ ran(Σ.M(d)) = ∅`, for every `d` and every `Σ`. Every claim in this ASN concerning `proj` and `iproj` (Π5–Π11, Π13–Π14, Π16–Π17) holds *vacuously* when `cov(e) = ∅` — set-equality and inclusion claims between two empty sets are trivially true, and existential claims (Π17's `(E i :: ...) ≠ ∅`) cannot witness a slot with empty coverage. Two abstract postures are coherent. The first is to admit `cov(e) = ∅` and rely on the vacuous reading throughout; nothing in Π5–Π17 breaks. The second — which we recommend at the link-allocation contract — is to forbid empty endsets at creation via the local precondition `K.λ-cov-nonempty` stated in §Foundation Contracts. The two postures are interchangeable for the projection theorems below; they diverge only in what counts as a well-formed link at the time of `K.λ`. Where it matters in a proof, we will state the assumption locally.

## Permanence of Link Structure

The first claims concern what does not change. Each is a structural consequence of `L12`; together they say that whatever was true of `ℓ`'s value at creation is true forever.

**Π0 (LinkValuePermanence).** For every state transition `Σ → Σ'`:

`(A ℓ : ℓ ∈ dom(Σ.L) :: ℓ ∈ dom(Σ'.L) ∧ Σ'.L(ℓ) = Σ.L(ℓ))`

Inherited from L12. The transition vocabulary (ASN-0047) provides no operation that modifies an existing entry in `L`; `K.λ` adds a new entry, and every other operation has a frame condition that leaves `L` unchanged.

**Π1 (ArityPermanence).** `|Σ'.L(ℓ)| = |Σ.L(ℓ)|` — the number of endsets is fixed at creation. Direct consequence of Π0.

**Π2 (SlotPermanence).** `Σ'.L(ℓ).eᵢ = Σ.L(ℓ).eᵢ` for every slot `i`. Link equality is component-wise tuple equality (L6, ASN-0043), so Π0 forces each slot to be preserved.

**Π3 (CoveragePermanence).** `cov(Σ'.L(ℓ).eᵢ) = cov(Σ.L(ℓ).eᵢ)`. The set of I-addresses each endset references is permanent. Coverage is a function of the endset, and the endset is permanent by Π2.

**Π4 (DirectionalPermanence).** The role of each slot — which is the *from*-endset, which is the *to*-endset, which is the *type*-endset under the StandardTriple convention, or whatever role assignment is in force for higher-arity links — is determined by slot position alone. *Proof.* By Π0, `Σ'.L(ℓ) = Σ.L(ℓ)`. By L6 (link equality is component-wise tuple equality, with slot index a primitive positional accessor), tuple-level equality forces slot-wise equality at every index: `Σ'.L(ℓ).eᵢ = Σ.L(ℓ).eᵢ` for every `i ∈ {1, ..., |Σ.L(ℓ)|}` (this is the content of Π2). By L7, there is a fixed function `Role : LinkType × ℕ → Direction` that assigns each slot index its directional role, parameterized by the link's type — given a link of type `τ`, the role of slot `i` is `Role(τ, i)`. Per L7, this function is Σ-external: `Role` is a constant function on its domain, not a component of any state `Σ`, and `Role` therefore appears in no operation's write set. (Explicitly: the write sets of the transition vocabulary — K.α writes to `Σ.C`, K.λ writes to `Σ.L`, K.μ⁺/μ⁻/μ~ write to `Σ.M(d)` — are disjoint from anything reachable through `Role`.) Hence for every transition `Σ → Σ'`, `Role` is the same function in both states. Composing the two preservations — the slot's contents at each index (Π2 via L6 + Π0) and the role-by-index function `Role` (L7 via the frame conditions of the transition vocabulary) — the directional role `Role(τ_ℓ, i)` of every slot `i` of `ℓ` is preserved across `Σ → Σ'`. □

The structure of `ℓ` — address, value, arity, endsets, coverage, slot positions, directional roles — is, taken together, the *invariant content of the link*. The link holder can treat all of it as fixed.

## Projection Properties

The projection, in contrast, is computed afresh in each state.

**Π5 (ProjectionLocality).** `proj(d, e, Σ)` depends only on `Σ.M(d)` and `cov(e)`:

`(A Σ, Σ', d, e : Σ.M(d) = Σ'.M(d) : proj(d, e, Σ) = proj(d, e, Σ'))`

*Proof.* By definition, `proj(d, e, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(e)}`. The defining set is syntactically a function of two operands: the partial map `Σ.M(d)` (consulted both for its domain and pointwise for the membership predicate) and the address set `cov(e)`. Given `Σ.M(d) = Σ'.M(d)`, both operands of the definition agree between `Σ` and `Σ'`, so the defined sets `{v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(e)}` and `{v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ cov(e)}` are element-wise identical. □

If two states agree on `M(d)`, their projections into `d` agree, irrespective of any other difference. In particular, the projection does not depend on:

- which document allocated `ℓ` (its origin, derivable via L1c of ASN-0043 from `ℓ`'s tumbler — but never consulted);
- any history of how `M(d)` was constructed (which `K.μ⁺` / `K.μ⁻` / `K.μ~` events led to it);
- the arrangement `M(d')` of any other document `d' ≠ d`;
- the contents of `C` other than what `M(d)` currently references.

This is what an alternative implementation must guarantee for cross-document linking to be sound. Whatever auxiliary indexes the implementation employs for efficiency, the *value* returned by the projection function is constrained to be a function of `M(d)` and `cov(e)` alone.

**Π6 (CrossDocumentIndependence).** For `d ≠ d'`:

`proj(d, e, Σ)` and `proj(d', e, Σ)` are computed independently of each other — formally, each is determined by a state component disjoint from the one determining the other.

*Proof.* `Σ.M : D × T ⇀ T` is a family indexed by document; for `d ≠ d'`, `Σ.M(d)` and `Σ.M(d')` are independent fibres of this family — modifying one does not constrain the other. Apply Π5 to `proj(d, e, ·)`: its value depends only on `Σ.M(d)` and `cov(e)`. Apply Π5 to `proj(d', e, ·)`: its value depends only on `Σ.M(d')` and `cov(e)`. Hence for any two states `Σ, Σ'` with `Σ.M(d) = Σ'.M(d)` (but `Σ.M(d')` and `Σ'.M(d')` arbitrary), Π5 gives `proj(d, e, Σ) = proj(d, e, Σ')`; the projection into `d` is invariant under arbitrary variation of `M(d')`. Symmetrically for the projection into `d'`. Each projection is therefore a function of state components disjoint from those determining the other, and computing either does not require consulting the other. □

A single link projects into many documents simultaneously; each projection is determined by that document's arrangement alone.

**Π7 (CoverageEquivalence).** Two endsets with identical coverage produce identical projections:

`cov(e₁) = cov(e₂) ⟹ (A d, Σ :: proj(d, e₁, Σ) = proj(d, e₂, Σ))`

*Proof.* By definition, `proj(d, eⱼ, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(eⱼ)}` for `j ∈ {1, 2}`. The endset operand enters this definition only through `cov(·)`; nothing else about `eⱼ` is consulted. Under the hypothesis `cov(e₁) = cov(e₂)`, the membership predicates `Σ.M(d)(v) ∈ cov(e₁)` and `Σ.M(d)(v) ∈ cov(e₂)` coincide pointwise, so the two defined sets are equal. □

Different span decompositions of the same coverage set are projection-indistinguishable. Coverage — not the literal span tuple — is the observable through projection.

## Behavior Under State Transitions

We now examine how the projection responds to each elementary operation that touches `M`.

**Π8 (ProjectionUnderExtension).** For `K.μ⁺` extending `Σ.M(d)` to `Σ'.M(d)` with `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))` and `(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`:

(a) Prior projection is retained: `proj(d, e, Σ) ⊆ proj(d, e, Σ')`.

*Proof.* Let `v ∈ proj(d, e, Σ)`. Then `v ∈ dom(Σ.M(d))` and `Σ.M(d)(v) ∈ cov(e)` by definition of `proj`. The K.μ⁺ contract gives `dom(Σ.M(d)) ⊆ dom(Σ'.M(d))`, so `v ∈ dom(Σ'.M(d))`. The same contract gives `Σ'.M(d)(v) = Σ.M(d)(v)` for `v ∈ dom(Σ.M(d))`, so `Σ'.M(d)(v) ∈ cov(e)`. Therefore `v ∈ proj(d, e, Σ')`. □

(b) Newly added positions whose I-target lies in `cov(e)` enter the projection:

`proj(d, e, Σ') ∖ proj(d, e, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ cov(e)}`

*Proof.* We show both inclusions.

⊆: Let `v ∈ proj(d, e, Σ') ∖ proj(d, e, Σ)`. From membership in the left projection, `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) ∈ cov(e)`. From non-membership in the right projection, either `v ∉ dom(Σ.M(d))` or `Σ.M(d)(v) ∉ cov(e)`. Suppose for contradiction `v ∈ dom(Σ.M(d))`. Then by the K.μ⁺ contract `Σ.M(d)(v) = Σ'.M(d)(v) ∈ cov(e)`, giving `v ∈ proj(d, e, Σ)` — contradicting our hypothesis. So `v ∉ dom(Σ.M(d))`. Combined with `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) ∈ cov(e)`, `v` lies in the right-hand set.

⊇: Let `v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))` with `Σ'.M(d)(v) ∈ cov(e)`. Directly, `v ∈ proj(d, e, Σ')`. And `v ∉ dom(Σ.M(d))` immediately gives `v ∉ proj(d, e, Σ)`. So `v ∈ proj(d, e, Σ') ∖ proj(d, e, Σ)`. □

Extension can only grow the projection.

**Π9 (ProjectionUnderContraction).** For `K.μ⁻` contracting `Σ.M(d)` to `Σ'.M(d)` with `dom(Σ'.M(d)) ⊂ dom(Σ.M(d))` and `(A v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`:

(a) Retained positions keep their projection status: `proj(d, e, Σ') = proj(d, e, Σ) ∩ dom(Σ'.M(d))`.

*Proof.* Both inclusions.

⊆: Let `v ∈ proj(d, e, Σ')`. Then `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) ∈ cov(e)`. The K.μ⁻ contract gives `dom(Σ'.M(d)) ⊂ dom(Σ.M(d))`, so `v ∈ dom(Σ.M(d))`, and `Σ.M(d)(v) = Σ'.M(d)(v) ∈ cov(e)`. Hence `v ∈ proj(d, e, Σ)`, and combined with `v ∈ dom(Σ'.M(d))`, we obtain `v ∈ proj(d, e, Σ) ∩ dom(Σ'.M(d))`.

⊇: Let `v ∈ proj(d, e, Σ) ∩ dom(Σ'.M(d))`. From `proj(d, e, Σ)`, `v ∈ dom(Σ.M(d))` and `Σ.M(d)(v) ∈ cov(e)`. From `dom(Σ'.M(d))`, the K.μ⁻ contract gives `Σ'.M(d)(v) = Σ.M(d)(v) ∈ cov(e)`. So `v ∈ proj(d, e, Σ')`. □

(b) `proj(d, e, Σ') ⊆ proj(d, e, Σ)`. The projection can only shrink.

*Proof.* Immediate from (a): `proj(d, e, Σ') = proj(d, e, Σ) ∩ dom(Σ'.M(d)) ⊆ proj(d, e, Σ)`. □

This is the *partial survival* case: even when `K.μ⁻` removes some V-positions from `proj(d, e, Σ)`, others may remain. The projection narrows; the link itself is not broken. If `K.μ⁻` removes every position in `proj(d, e, Σ)`, the projection in `d` becomes empty — but the link's structure, by Π0–Π3, is still intact, and the projection in some other document `d'` may still be non-empty.

**Π10 (ProjectionUnderRearrangement).** For `K.μ~` permuting `Σ.M(d)` via bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))` with `Σ'.M(d)(π(v)) = Σ.M(d)(v)`:

(a) The I-projection is invariant: `iproj(d, e, Σ') = iproj(d, e, Σ)`.

*Proof.* It suffices to show `ran(Σ'.M(d)) = ran(Σ.M(d))`; then `iproj(d, e, Σ') = cov(e) ∩ ran(Σ'.M(d)) = cov(e) ∩ ran(Σ.M(d)) = iproj(d, e, Σ)`.

⊆: Let `a ∈ ran(Σ'.M(d))`. Then there exists `v' ∈ dom(Σ'.M(d))` with `Σ'.M(d)(v') = a`. Since `π` is a bijection onto `dom(Σ'.M(d))`, there exists `v ∈ dom(Σ.M(d))` with `π(v) = v'`. The K.μ~ contract gives `Σ.M(d)(v) = Σ'.M(d)(π(v)) = Σ'.M(d)(v') = a`. Hence `a ∈ ran(Σ.M(d))`.

⊇: Let `a ∈ ran(Σ.M(d))`. Then there exists `v ∈ dom(Σ.M(d))` with `Σ.M(d)(v) = a`. The contract gives `Σ'.M(d)(π(v)) = Σ.M(d)(v) = a`, and `π(v) ∈ dom(Σ'.M(d))`. Hence `a ∈ ran(Σ'.M(d))`. □

(b) The V-projection is permuted: `proj(d, e, Σ') = {π(v) : v ∈ proj(d, e, Σ)}`.

*Proof.* Both inclusions.

⊇: Let `v' ∈ {π(v) : v ∈ proj(d, e, Σ)}`, so `v' = π(v)` for some `v ∈ proj(d, e, Σ)`. From `v ∈ proj(d, e, Σ)`, `v ∈ dom(Σ.M(d))` and `Σ.M(d)(v) ∈ cov(e)`. Then `π(v) ∈ dom(Σ'.M(d))` (π's codomain), and `Σ'.M(d)(π(v)) = Σ.M(d)(v) ∈ cov(e)` (by the contract). So `v' = π(v) ∈ proj(d, e, Σ')`.

⊆: Let `v' ∈ proj(d, e, Σ')`. Then `v' ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v') ∈ cov(e)`. By bijectivity of `π : dom(Σ.M(d)) → dom(Σ'.M(d))`, there exists a unique `v ∈ dom(Σ.M(d))` with `π(v) = v'`. The contract gives `Σ.M(d)(v) = Σ'.M(d)(π(v)) = Σ'.M(d)(v') ∈ cov(e)`. So `v ∈ proj(d, e, Σ)`, and `v' = π(v) ∈ {π(v) : v ∈ proj(d, e, Σ)}`. The ⊆ direction is where bijectivity is essential: without injectivity of `π` we could not invert `π` to recover `v`, and without surjectivity onto `dom(Σ'.M(d))` we could not guarantee that every `v' ∈ proj(d, e, Σ')` is a `π`-image at all. □

K.μ~-FIX (ASN-0047) gives `dom(Σ'.M(d)) = dom(Σ.M(d))`. Rearrangement preserves the *set of (V, I) pairs* up to permutation of V-positions; the projection's image in I-space is exactly preserved.

**Π11 (ProjectionFollowsContent).** Synthesizing Π8–Π10 at the I-level: for every K.μ-class transition `Σ → Σ'` on `M(d)`, the I-projection's evolution is monotone in the operation's effect on `ran(M(d))`:

(a) Under `K.μ⁺` extension: `iproj(d, e, Σ) ⊆ iproj(d, e, Σ')`.

*Proof.* The K.μ⁺ contract ensures `dom(Σ'.M(d)) ⊇ dom(Σ.M(d))` with `Σ'.M(d)(v) = Σ.M(d)(v)` on `dom(Σ.M(d))`. Hence `ran(Σ.M(d)) ⊆ ran(Σ'.M(d))`, and intersecting with `cov(e)` preserves the inclusion. □

(b) Under `K.μ⁻` contraction: `iproj(d, e, Σ') ⊆ iproj(d, e, Σ)`.

*Proof.* For `v ∈ dom(Σ'.M(d)) ⊂ dom(Σ.M(d))`, `Σ'.M(d)(v) = Σ.M(d)(v)`. So every value in `ran(Σ'.M(d))` already appears in `ran(Σ.M(d))`, giving `ran(Σ'.M(d)) ⊆ ran(Σ.M(d))`. Intersecting with `cov(e)` preserves the inclusion. □

(c) Under `K.μ~` rearrangement: `iproj(d, e, Σ') = iproj(d, e, Σ)`. (Identical to Π10(a).)

(d) **Transition closed form.** Define the range-additions and range-removals of the transition as `Δran⁺ := ran(Σ'.M(d)) ∖ ran(Σ.M(d))` and `Δran⁻ := ran(Σ.M(d)) ∖ ran(Σ'.M(d))`. For every K.μ-class transition on `M(d)`:

`iproj(d, e, Σ') = (iproj(d, e, Σ) ∖ Δran⁻) ∪ (cov(e) ∩ Δran⁺)`

*Proof.* We compute:

```
(iproj(d, e, Σ) ∖ Δran⁻) ∪ (cov(e) ∩ Δran⁺)
= {def of iproj}
  ((cov(e) ∩ ran(Σ.M(d))) ∖ Δran⁻) ∪ (cov(e) ∩ Δran⁺)
= {Δran⁻ = ran(Σ.M(d)) ∖ ran(Σ'.M(d)), so ran(Σ.M(d)) ∖ Δran⁻ = ran(Σ.M(d)) ∩ ran(Σ'.M(d))}
  (cov(e) ∩ ran(Σ.M(d)) ∩ ran(Σ'.M(d))) ∪ (cov(e) ∩ Δran⁺)
= {distribute cov(e) ∩ -}
  cov(e) ∩ ((ran(Σ.M(d)) ∩ ran(Σ'.M(d))) ∪ Δran⁺)
= {ran(Σ'.M(d)) = (ran(Σ.M(d)) ∩ ran(Σ'.M(d))) ∪ Δran⁺ — partitioning ran(Σ'.M(d)) into shared and added}
  cov(e) ∩ ran(Σ'.M(d))
= {def of iproj}
  iproj(d, e, Σ')
```

□

The three cases (a)–(c) are specializations. Under `K.μ⁺`, the contract preserves all `(v ↦ a)` pairs on `dom(Σ.M(d))`, so `ran(Σ.M(d)) ⊆ ran(Σ'.M(d))` and `Δran⁻ = ∅`; the closed form reduces to `iproj(d, e, Σ') = iproj(d, e, Σ) ∪ (cov(e) ∩ Δran⁺)`, recovering (a). Under `K.μ⁻`, no new pairs are introduced, so `ran(Σ'.M(d)) ⊆ ran(Σ.M(d))` and `Δran⁺ = ∅`; the closed form reduces to `iproj(d, e, Σ') = iproj(d, e, Σ) ∖ Δran⁻`, recovering (b). Under `K.μ~`, Π10(a) gives `ran(Σ.M(d)) = ran(Σ'.M(d))`, so `Δran⁻ = Δran⁺ = ∅`, recovering (c). The closed form thus unifies the three case analyses into one calculational identity: I-projection evolution is a difference-of-sets in `ran(M(d))` — the projection gains exactly the newly-arranged range-addresses that lie in coverage, and loses exactly the dropped range-addresses that were in coverage.

The V-projection may be wholesale displaced (Π10(b) shows it can be permuted arbitrarily), but the I-projection's evolution is computable from the operation's effect on `ran(M(d))` alone. This is the *strap-between-bytes* principle formalized: editing operations displace V-positions, but the link's coverage in I-space remains a fixed target. The projection tracks the content.

**Π12 (CrossDocumentFrame).** For any transition `Σ → Σ'` whose write set on `M` is confined to a single target document `d'` (i.e., `Σ.M(d) = Σ'.M(d)` for every `d ≠ d'`), projections into other documents are unchanged:

`(A d, e : d ≠ d' :: proj(d, e, Σ) = proj(d, e, Σ'))`

*Proof.* For `d ≠ d'`, the confinement hypothesis gives `Σ.M(d) = Σ'.M(d)`. Π5 then gives `proj(d, e, Σ) = proj(d, e, Σ')` for every endset `e`. □

The document-targeted arrangement operations `K.μ⁻`, `K.μ⁺`, `K.μ~` (per ASN-0047) all satisfy this confinement on `M`. The non-document-targeted operations `K.α` and `K.λ` modify `C` and `L` respectively but leave every `M(d)` untouched; their interaction with projections is handled separately by Π13 and Π14 below.

**Π13 (ContentAllocationFrame).** `K.α` extends `dom(C)` but does not modify any `M(d)`:

`(A d, e :: proj(d, e, Σ) = proj(d, e, Σ'))`

across every `K.α`-transition.

*Proof.* The K.α frame condition (ASN-0047) writes only to `Σ.C`: every `M(d)` is in K.α's read-only frame, so `Σ'.M(d) = Σ.M(d)` for every `d ∈ E_doc`. By Π5, `Σ.M(d) = Σ'.M(d)` gives `proj(d, e, Σ) = proj(d, e, Σ')` for every endset `e`. Universally quantifying over `d` and `e` discharges the claim. □

A newly allocated content address is not in any arrangement until a subsequent `K.μ⁺` places it; its presence in `dom(C)` alone does not affect any existing projection.

A separate question — distinct from this frame condition — is whether the newly allocated address may already lie in `cov(eᵢ)` for some pre-existing link's endset `eᵢ`. The frame condition above is unconditional: `K.α` alone does not change any `M(d)`, so the projection cannot change at the `K.α` step, regardless of whether the new address lies in some endset's coverage. The interaction only manifests at a subsequent `K.μ⁺` that arranges the new address; whether that arrangement enters some projection depends on coverage, which is decided at link creation.

We therefore separate two questions. (i) Is `K.α` projection-preserving? Yes — by frame condition, unconditionally. (ii) Are newly allocated addresses excluded from the coverage of pre-existing links? This depends on a structural choice in the link-allocation rule, which we now name explicitly.

**Open structural axiom: The Coverage-at-Creation Rule (CCR).** Let `Σ₀` be the state in which `K.λ` allocates a link `ℓ` with endsets `(e₁, …, e_N)`. Two policies are possible:

- *CCR-restricted*: at link creation, each `cov(eᵢ) ⊆ dom(Σ₀.C)`. Endsets reference only addresses then in the content store.
- *CCR-open*: at link creation, each `cov(eᵢ) ⊆ T`. Endsets may reference any addresses in the address space, including those not yet allocated; we refer to such addresses as *ghost* references — addresses present in the abstract space but absent from `dom(Σ₀.C)`.

We do not select between these policies in this ASN. Each yields a coherent specification — the proofs below are policy-agnostic except where they speak about the post-allocation behavior of newly-allocated `K.α` addresses, and we factor the dependent claims through the chosen policy explicitly (see R13 conditional, below, and the worked-example Step 6 sub-trace). The selection is a structural axiom belonging to the link-allocation foundation rather than to this ASN, and the two policies differ in observable consequence: under CCR-restricted a fresh `a_new` cannot enter any pre-existing endset's coverage; under CCR-open it can, provided the endset was created reaching forward to `a_new`. We catalogue the divergence below and leave the selection open.

**Π14 (LinkAllocationFrame).** `K.λ` extends `dom(L)` but does not modify any `M(d)`:

`(A d, e :: proj(d, e, Σ) = proj(d, e, Σ'))`

across every `K.λ`-transition.

*Proof.* The K.λ frame condition (ASN-0047) writes only to `Σ.L`: every `M(d)` is in K.λ's read-only frame, so `Σ'.M(d) = Σ.M(d)` for every `d ∈ E_doc`. By Π5, `Σ.M(d) = Σ'.M(d)` gives `proj(d, e, Σ) = proj(d, e, Σ')` for every endset `e`. Universally quantifying over `d` and `e` discharges the claim. □

Applied pointwise to endsets of pre-existing links — for every `ℓ ∈ dom(Σ.L)` and slot index `i`, instantiate the universally quantified equation with `e := Σ.L(ℓ).eᵢ` — this yields `proj(d, ℓ, i, Σ) = proj(d, ℓ, i, Σ')`. The newly allocated link's endsets exist in `Σ'.L` but not in `Σ.L`; there is no projection to compare for the new link, only forward from `Σ'`.

## Independence from Arrangement

The structure of `Σ.L` is logically independent of the structure of any `Σ.M(d)`. We make this precise in two parts: (a) an unarranged-link state is consistent — the existence of `ℓ` in `dom(L)` does not require `ℓ` to appear in the range of any `M(d)`; and (b) removing `ℓ` from the range of some `M(d)` leaves `Σ.L` unchanged.

**Π15a (UnarrangedLinkConsistency).** It is consistent with the transition vocabulary for a state `Σ` to satisfy

`ℓ ∈ dom(Σ.L) ∧ ¬(E d ∈ E_doc, v ∈ dom(Σ.M(d)) :: Σ.M(d)(v) = ℓ)`

*Proof.* `K.λ` (ASN-0047) allocates `ℓ` by adding it to `dom(L)` and is constrained by Π14 to leave every `M(d)` untouched. Let `Σ_pre` be the state immediately before such a `K.λ`; let `Σ` be the immediate successor. Then `ℓ ∈ dom(Σ.L)`, and for every `d ∈ E_doc`, `Σ.M(d) = Σ_pre.M(d)`. Our task is to show that no `M(d)` in `Σ_pre` maps any V-position to `ℓ`.

We need a subspace-aware referential-integrity premise. The address space partitions into a text-content subspace `s_C` and a link subspace `s_L` (L0) with `s_L ∩ s_C = ∅`. V-positions inherit this partition by the `subspace` projection (S8a) — every V-position `v ∈ dom(Σ.M(d))` has a subspace identifier `subspace(v)`. We write `M(d)|_{s_C}` and `M(d)|_{s_L}` for the restrictions of `M(d)` to V-positions in the text-content and link subspaces respectively; their domains are disjoint and their union recovers `M(d)`, so `ran(Σ.M(d)) = ran(Σ.M(d)|_{s_C}) ∪ ran(Σ.M(d)|_{s_L})`.

The proof requires a stratified referential-integrity premise — that V-positions in the link subspace arrange link addresses, and V-positions in the text subspace arrange text-content addresses. The foundation invariant S3 — `ran(Σ.M(d)) ⊆ dom(Σ.C)` — does not on its face speak to this stratification. Whether S3 should be read as a single global constraint or as a stratified family of constraints is a foundation-level question this ASN cannot settle: under the global reading, `dom(Σ.C)` would have to be enlarged to include link addresses for the link-subspace fibre to be coherent; under the stratified reading, two disjoint range constraints replace the single one. We do not select between these readings for the foundation. Instead, we adopt two local structural premises that are sufficient for this proof and that any foundation-level reading consistent with the link/text subspace partition must imply:

`(S3-text, local axiom)` `ran(Σ.M(d)|_{s_C}) ⊆ dom(Σ.C)|_{s_C}` — text-subspace V-positions arrange `s_C`-resident content.

`(S3-link, local axiom)` `ran(Σ.M(d)|_{s_L}) ⊆ dom(Σ.L)` — link-subspace V-positions arrange allocated-link addresses.

These are stated as **local axioms of this ASN**, not as derivations from S3 nor as a modification of S3. They constrain a stratum of the document arrangement that the original S3 leaves underspecified; whether the foundation invariant should be revised to make this stratification global, or whether `dom(C)` should be interpreted as `dom(C) ∪ dom(L)` in the original S3 to recover consistency, is a question for foundation-level revision and is beyond the scope of this ASN. The local axioms suffice for Π15a; future ASNs depending on the original S3 are not affected by this local choice, since the local axioms strengthen no foundation claim — they speak about disjoint subspace fibres of `M(d)`. L14 (`dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`) ensures that `(S3-text)` and `(S3-link)` together do not over-constrain `ran(M(d))`: the two strata range over disjoint regions of `T`.

We now derive `ℓ ∉ ran(Σ_pre.M(d))` in four explicit steps.

(i) *Allocator freshness over `L`.* The K.λ allocator discipline (L1c, ASN-0043, derived from T10a's GlobalUniqueness) produces `ℓ` fresh with respect to the prior link store: `ℓ ∉ dom(Σ_pre.L)`.

(ii) *Allocator type.* The K.λ allocator allocates link addresses, which by L0 (ASN-0043) inhabit the link subspace: `subspace_I(ℓ) = s_L`, equivalently `ℓ ∈ s_L`.

(iii) *Address-space disjointness.* By L0 and the subspace partition, `s_L ∩ s_C = ∅`. Combined with (ii), `ℓ ∉ s_C`.

(iv) *Combining strata.* Per `(S3-link)`, `ran(Σ_pre.M(d)|_{s_L}) ⊆ dom(Σ_pre.L)`; by (i), `ℓ ∉ dom(Σ_pre.L)`, so `ℓ ∉ ran(Σ_pre.M(d)|_{s_L})`. Per `(S3-text)`, `ran(Σ_pre.M(d)|_{s_C}) ⊆ dom(Σ_pre.C)|_{s_C} ⊆ s_C`; by (iii), `ℓ ∉ s_C`, so `ℓ ∉ ran(Σ_pre.M(d)|_{s_C})`. The decomposition `ran(Σ_pre.M(d)) = ran(Σ_pre.M(d)|_{s_C}) ∪ ran(Σ_pre.M(d)|_{s_L})` then gives `ℓ ∉ ran(Σ_pre.M(d))`.

Since `Σ.M(d) = Σ_pre.M(d)` for every `d ∈ E_doc`, the same holds in `Σ`. The witness exists. □

**Π15b (ReverseOrphaningPreservesL).** For any K.μ⁻ transition `Σ → Σ'` on some `M(d)` that drops a V-position `v` previously arranging `ℓ` (`Σ.M(d)(v) = ℓ`):

`Σ'.L = Σ.L ∧ Σ'.L(ℓ) = Σ.L(ℓ)`

regardless of whether `ℓ` remains in `ran(Σ'.M(d))` (via some other position) or vanishes entirely.

*Proof.* `K.μ⁻`'s frame condition (ASN-0047) modifies only the target `M(d)`; in particular, `dom(L)` and the value `L(·)` are not in its write set. By L12 (ASN-0043), `Σ.L = Σ'.L` follows: link values are immutable. From `ℓ ∈ dom(Σ.L)` and `Σ.L = Σ'.L`, we obtain `ℓ ∈ dom(Σ'.L)` and `Σ'.L(ℓ) = Σ.L(ℓ)`. □

Together, Π15a and Π15b express bidirectional independence: a link can exist in `L` without being arranged anywhere (Π15a), and a link can be removed from a document's arrangement without disturbing its presence in `L` (Π15b). We call a link in either of these states *reverse-orphaned* from the document in question — present in `L`, absent from `M(d)`.

Reverse orphaning does not impair the projection mechanism. Every claim in the preceding sections continues to apply: the reverse-orphaned link's endsets project into any document whose arrangement reaches the link's coverage I-addresses, exactly as before. The link's *self-arrangement* (whether it appears in some document's link-subspace V-stream) is a different matter from its *endset projection* (the V-positions reached by following its endset coverage).

## Backward Lookup: Discovery

The forward projection direction — link to V-positions — has a backward dual. Given a V-region in some document, which links are reached?

**Definition (Reach).** A link `ℓ` *reaches* a V-region `V_q ⊆ dom(Σ.M(d))` iff some endset's projection intersects `V_q`:

`reaches(ℓ, d, V_q, Σ) ≡ (E i :: proj(d, ℓ, i, Σ) ∩ V_q ≠ ∅)`

This V-side definition has an I-side equivalent that we now establish as a named lemma, since it is load-bearing for the discovery claims below.

**RB (ReachBridge).** Reach has an I-side reformulation in terms of the V-region's I-image:

`reaches(ℓ, d, V_q, Σ) ⟺ (E i :: cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) ≠ ∅)`

*Proof.* For each slot `i`, we show that `proj(d, ℓ, i, Σ) ∩ V_q ≠ ∅ ⟺ cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) ≠ ∅`; existential quantification over slots then gives the full claim. This is the bridge equality (proved at the definition of `iproj`) restricted to `V_q`.

(⟹): Let `v ∈ proj(d, ℓ, i, Σ) ∩ V_q`. From `v ∈ proj(d, ℓ, i, Σ)`, `v ∈ dom(Σ.M(d))` and `Σ.M(d)(v) ∈ cov(Σ.L(ℓ).eᵢ)`. Combined with `v ∈ V_q`, we have `v ∈ V_q ∩ dom(Σ.M(d)) = dom(Σ.M(d)|_{V_q})`, hence `Σ.M(d)(v) ∈ ran(Σ.M(d)|_{V_q})`. Combined with `Σ.M(d)(v) ∈ cov(Σ.L(ℓ).eᵢ)`, the intersection `cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q})` is non-empty.

(⟸): Let `α ∈ cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q})`. From `α ∈ ran(Σ.M(d)|_{V_q})`, pick `v ∈ dom(Σ.M(d)|_{V_q}) = V_q ∩ dom(Σ.M(d))` with `Σ.M(d)(v) = α`. Then `Σ.M(d)(v) = α ∈ cov(Σ.L(ℓ).eᵢ)` and `v ∈ dom(Σ.M(d))`, so `v ∈ proj(d, ℓ, i, Σ)`. Combined with `v ∈ V_q`, the intersection `proj(d, ℓ, i, Σ) ∩ V_q` is non-empty. □

**Π16 (ReachLocality).** Whether a link reaches a V-region is computable from `Σ.L`, `Σ.M(d)|_{V_q}`, and the region `V_q` alone:

`(A Σ, Σ', ℓ, d, V_q : Σ.L = Σ'.L ∧ Σ.M(d)|_{V_q} = Σ'.M(d)|_{V_q} : reaches(ℓ, d, V_q, Σ) ⟺ reaches(ℓ, d, V_q, Σ'))`

*Proof.* We invoke RB (ReachBridge, proved above) to re-express both sides of the equivalence in I-terms. From `Σ.L = Σ'.L` we obtain `Σ.L(ℓ).eᵢ = Σ'.L(ℓ).eᵢ` for every slot `i`, hence `cov(Σ.L(ℓ).eᵢ) = cov(Σ'.L(ℓ).eᵢ)`. From `Σ.M(d)|_{V_q} = Σ'.M(d)|_{V_q}` — equality of partial maps on the same domain — we obtain `ran(Σ.M(d)|_{V_q}) = ran(Σ'.M(d)|_{V_q})`. Both operands of the intersection `cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q})` therefore agree between `Σ` and `Σ'`, so the intersection is non-empty in `Σ` iff non-empty in `Σ'`. Existential quantification over slots preserves the equivalence; applying RB again to translate back: `reaches(ℓ, d, V_q, Σ) ⟺ reaches(ℓ, d, V_q, Σ')`. □

No provenance — neither the document that allocated `ℓ`, nor the document where the I-addresses originated, nor any history of which document first arranged those I-addresses — participates in the reach relation. The relation is intrinsic to the current state.

**Π17 (PartialReach).** Non-empty intersection of coverage with the V-region's image suffices for reach:

`cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) ≠ ∅ ⟹ reaches(ℓ, d, V_q, Σ)`

*Proof.* Assume `cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) ≠ ∅`. Pick a witness `α` in the intersection. From `α ∈ ran(Σ.M(d)|_{V_q})` we obtain a V-position `v ∈ V_q ∩ dom(Σ.M(d))` with `Σ.M(d)(v) = α`. Combined with `α ∈ cov(Σ.L(ℓ).eᵢ)`, we have `Σ.M(d)(v) ∈ cov(Σ.L(ℓ).eᵢ)`, hence `v ∈ proj(d, ℓ, i, Σ)` by definition of `proj`. Since additionally `v ∈ V_q`, `v ∈ proj(d, ℓ, i, Σ) ∩ V_q`, so this intersection is non-empty. Existentially quantifying over slots, `reaches(ℓ, d, V_q, Σ)` holds by definition. □

A region that arranges only some I-addresses of `cov(eᵢ)` — for instance, a document that transcludes only a few bytes of a longer linked passage — still discovers the link through those bytes. Reach is intersection, not containment.

## What the Link Holder Can Rely On

We assemble the guarantees the link holder receives. Suppose `ℓ` was allocated in state `Σ₀` with endsets `(e₁, ..., e_N)`. For every state `Σ` reachable from `Σ₀`:

**(R1)** The link address persists: `ℓ ∈ dom(Σ.L)`. (Π0)

**(R2)** The link value persists: `Σ.L(ℓ) = Σ₀.L(ℓ)`. (Π0)

**(R3)** Each endset's coverage persists: `cov(Σ.L(ℓ).eᵢ) = cov(Σ₀.L(ℓ).eᵢ)`. (Π3)

**(R4)** Arity, slot assignments, and directional roles are unchanged. (Π1, Π2, Π4)

**(R5)** For every document `d` and slot `i`, `proj(d, ℓ, i, Σ)` is computable from `Σ.M(d)` and `cov(ℓ.eᵢ)` alone — no history, no provenance, no external state. (Π5)

**(R6)** If `a ∈ cov(ℓ.eᵢ)` is in `ran(Σ.M(d))`, then `a ∈ iproj(d, ℓ, i, Σ)`, and some V-position in `proj(d, ℓ, i, Σ)` maps to `a`. (Definition + Π5)

**(R7)** If `a ∈ cov(ℓ.eᵢ)` is not in `ran(Σ.M(d))`, then `a` is silently absent from `iproj(d, ℓ, i, Σ)`. The link is not broken; it simply has nothing in `d` for `a`. (Definition)

**(R8)** Partial absence is benign. Other I-addresses in `cov(ℓ.eᵢ)`, if present in `ran(Σ.M(d))`, continue to be reached. The projection narrows; the rest survives. (Π9)

**(R9)** Reintroduction is possible. If `a ∈ cov(ℓ.eᵢ)` and `a ∈ dom(Σ.C)` but `a ∉ ran(Σ.M(d))`, some future state `Σ'` (reachable via `K.μ⁺`) can have `a ∈ ran(Σ'.M(d))`, restoring `a` to `iproj(d, ℓ, i, Σ')`. The content's permanence in `dom(C)` (S0) is what makes this possible. (Π8 + S0)

**(R10)** Cross-document independence. If `proj(d, ℓ, i, Σ) = ∅`, the projection `proj(d', ℓ, i, Σ)` for some other document `d'` may still be non-empty. The link is universally available; presence in any single document is local. (Π6)

**(R11)** Reverse orphaning is benign. If the link itself is unarranged in any document's link subspace, the link's structure is unaffected, and projections of its endsets into any document continue to be well-defined. (Π15a + Π15b)

**(R12)** Discovery is preserved. For any V-region in any document that arranges some I-address in `cov(ℓ.eᵢ)`, the link is discoverable from that region by the reach relation, intrinsic to the current state. (Π16, Π17)

**(R13, conditional).** *Provided CCR-restricted holds at link creation*, new content does not silently extend the link. Because coverage is permanent (Π3) and newly allocated addresses (via `K.α`) lie outside `dom(Σ₀.C)` and therefore outside `cov(eᵢ)` for every endset created at or before `Σ₀`, inserting new content adjacent to or within a linked region does not enlarge the projection to include the new bytes. The strap holds its original bytes, not their new neighbors. (Π3 + Π13 + CCR-restricted)

Under CCR-open, R13 must be read with a caveat: a link's endset may reference ghost addresses that are later realized by `K.α` + `K.μ⁺`, and the projection grows accordingly via Π8. This is not a corruption — it is the design-intended behavior of hierarchical and forward-reference endsets, which deliberately embrace content not yet allocated when the link was made. R13's "no silent extension" guarantee is thus contingent on CCR-restricted, not absolute.

## A Worked Example

To confirm that the claims survive a non-trivial state, we trace through a small scenario.

**Initial state `Σ₀`.** A link `ℓ` has been allocated with coverage `cov(e) = {a₅, a₆, a₇}` for some endset `e ∈ Σ₀.L(ℓ)`. Three documents are arranged:

- `Σ₀.M(d) = {0 ↦ a₅, 1 ↦ a₆, 2 ↦ a₇, 3 ↦ a₈}` — the principal document of our trace.
- `Σ₀.M(d') = {0 ↦ a₆, 1 ↦ a₉}` — a second document arranging `a₆ ∈ cov(e)` and an unrelated `a₉ ∉ cov(e)`. This lets us witness R10 (cross-document independence).
- `Σ₀.M(d_link) = {0 ↦ ℓ}` — a third document whose link-subspace arrangement includes `ℓ` itself at V-position `0` of `d_link`. Here the V-position `0` is shorthand for the first V-position in `s_L` of `d_link`, so this entry lives in `M(d_link)|_{s_L}` and falls under `(S3-link)` (`ran ⊆ dom(Σ.L)`). (Per ASN-0043, the link store `L` and a document's link-subspace arrangement are distinct: a link is born in `L` by `K.λ`, but whether it is *arranged* in some document's link-subspace V-stream is a separate matter — what we are about to vary.) This lets us witness R11 (reverse orphaning).

The starting projections and I-projections are:

- `proj(d, e, Σ₀) = {v ∈ {0, 1, 2, 3} : Σ₀.M(d)(v) ∈ {a₅, a₆, a₇}} = {0, 1, 2}`
- `iproj(d, e, Σ₀) = {a₅, a₆, a₇} ∩ {a₅, a₆, a₇, a₈} = {a₅, a₆, a₇}`
- `proj(d', e, Σ₀) = {v ∈ {0, 1} : Σ₀.M(d')(v) ∈ {a₅, a₆, a₇}} = {0}`
- `iproj(d', e, Σ₀) = {a₅, a₆, a₇} ∩ {a₆, a₉} = {a₆}`

All three coverage addresses are reached by `d`; only `a₆` is reached by `d'`. The link `ℓ` is itself arranged at V-position `0` of `d_link`.

**Step 1: K.μ⁻ removing V-position 1 (`Σ₀ → Σ₁`).** Contract `Σ₀.M(d)` by dropping position `1`:

`Σ₁.M(d) = {0 ↦ a₅, 2 ↦ a₇, 3 ↦ a₈}`

with `dom(Σ₁.M(d)) = {0, 2, 3} ⊂ {0, 1, 2, 3} = dom(Σ₀.M(d))` and the K.μ⁻ contract `Σ₁.M(d)(v) = Σ₀.M(d)(v)` for `v ∈ {0, 2, 3}`.

Verify Π9(a) — `proj(d, e, Σ₁) = proj(d, e, Σ₀) ∩ dom(Σ₁.M(d))`:

- LHS: `proj(d, e, Σ₁) = {v ∈ {0, 2, 3} : Σ₁.M(d)(v) ∈ cov(e)} = {0, 2}`
- RHS: `proj(d, e, Σ₀) ∩ dom(Σ₁.M(d)) = {0, 1, 2} ∩ {0, 2, 3} = {0, 2}`

Equal. ✓

Verify Π9(b) — `proj(d, e, Σ₁) ⊆ proj(d, e, Σ₀)`:

- `{0, 2} ⊆ {0, 1, 2}`. ✓

The I-projection in `Σ₁`:

`iproj(d, e, Σ₁) = {a₅, a₆, a₇} ∩ {a₅, a₇, a₈} = {a₅, a₇}`

The contraction has lost the witness for `a₆`. The link still has `a₆` in its coverage (Π3), but no V-position in `Σ₁` realizes it. This is the *partial survival* case: `proj` and `iproj` narrowed, the link itself is intact.

Cross-document frame (Π12): the operation's write set is `M(d)`, so `Σ₁.M(d') = Σ₀.M(d')` and `Σ₁.M(d_link) = Σ₀.M(d_link)`. Hence `proj(d', e, Σ₁) = {0}` and `iproj(d', e, Σ₁) = {a₆}` (both unchanged), and `ℓ ∈ ran(Σ₁.M(d_link))` (still arranged).

**Step 2: K.μ~ swapping V-positions 0 and 2 (`Σ₁ → Σ₂`).** Let `π` be the bijection `dom(Σ₁.M(d)) → dom(Σ₂.M(d))` with `π(0) = 2`, `π(2) = 0`, `π(3) = 3`. The K.μ~ contract `Σ₂.M(d)(π(v)) = Σ₁.M(d)(v)` yields:

- `Σ₂.M(d)(2) = Σ₁.M(d)(0) = a₅`
- `Σ₂.M(d)(0) = Σ₁.M(d)(2) = a₇`
- `Σ₂.M(d)(3) = Σ₁.M(d)(3) = a₈`

So `Σ₂.M(d) = {0 ↦ a₇, 2 ↦ a₅, 3 ↦ a₈}`, and `dom(Σ₂.M(d)) = dom(Σ₁.M(d)) = {0, 2, 3}` (K.μ~-FIX).

Verify Π10(a) — `iproj(d, e, Σ₂) = iproj(d, e, Σ₁)`:

- `iproj(d, e, Σ₂) = {a₅, a₆, a₇} ∩ {a₇, a₅, a₈} = {a₅, a₇}`
- `iproj(d, e, Σ₁) = {a₅, a₇}`

Equal. ✓ The I-image is invariant under rearrangement.

Verify Π10(b) — `proj(d, e, Σ₂) = {π(v) : v ∈ proj(d, e, Σ₁)}`:

- LHS: `proj(d, e, Σ₂) = {v ∈ {0, 2, 3} : Σ₂.M(d)(v) ∈ cov(e)} = {0, 2}` (since `Σ₂.M(d)(0) = a₇ ∈ cov(e)`, `Σ₂.M(d)(2) = a₅ ∈ cov(e)`, `Σ₂.M(d)(3) = a₈ ∉ cov(e)`)
- RHS: `{π(v) : v ∈ {0, 2}} = {π(0), π(2)} = {2, 0} = {0, 2}`

Equal. ✓ The V-projection set is the same here, but only because we happened to swap two positions both lying in the projection; in general the V-set can differ.

Verify Π11 transition synthesis. From `Σ₀` to `Σ₂`:

- Step 1 (K.μ⁻): `iproj(d, e, Σ₁) = {a₅, a₇} ⊆ {a₅, a₆, a₇} = iproj(d, e, Σ₀)`. (Π11b inclusion holds.)
- Step 2 (K.μ~): `iproj(d, e, Σ₂) = {a₅, a₇} = iproj(d, e, Σ₁)`. (Π11c equality holds.)
- Overall: `a₆` was lost only at the K.μ⁻ step; the K.μ~ step did not lose or recover any coverage address. The transition history of `iproj` is monotone-with-the-operation.

Cross-document frame again applies: `Σ₂.M(d') = Σ₁.M(d')` and `Σ₂.M(d_link) = Σ₁.M(d_link)` by Π12, so `proj(d', e, Σ₂) = {0}`, `iproj(d', e, Σ₂) = {a₆}`, and `ℓ ∈ ran(Σ₂.M(d_link))` — all unchanged.

**Step 3: K.μ⁻ removing V-positions `{0, 2}` from `M(d)` (`Σ₂ → Σ₃`).** Now we drop every position currently in `proj(d, e, Σ₂)`. Set `V_drop = {0, 2}`. The K.μ⁻ contract gives `dom(Σ₃.M(d)) = {3}` and `Σ₃.M(d)(3) = Σ₂.M(d)(3) = a₈`, so

`Σ₃.M(d) = {3 ↦ a₈}`

The projection in `d`:

- `proj(d, e, Σ₃) = {v ∈ {3} : Σ₃.M(d)(v) ∈ {a₅, a₆, a₇}} = ∅` — no projecting V-position survives.
- `iproj(d, e, Σ₃) = {a₅, a₆, a₇} ∩ {a₈} = ∅` — no coverage address remains in range.

Check against the wp characterization derived in §Weakest Preconditions below: `wp(K.μ⁻[V_drop], iproj(d, e) ≠ ∅) ≡ proj(d, e, Σ₂) ⊄ V_drop`. Here `proj(d, e, Σ₂) = {0, 2} ⊆ {0, 2} = V_drop`, so the precondition for non-empty post-projection fails — and indeed `iproj(d, e, Σ₃) = ∅`. ✓

Also check Π11(d) (transition closed form). Here `Δran⁻ = ran(Σ₂.M(d)) ∖ ran(Σ₃.M(d)) = {a₇, a₅, a₈} ∖ {a₈} = {a₅, a₇}` and `Δran⁺ = {a₈} ∖ {a₇, a₅, a₈} = ∅` (K.μ⁻ adds no new range-values). The closed form predicts `iproj(d, e, Σ₃) = (iproj(d, e, Σ₂) ∖ Δran⁻) ∪ (cov(e) ∩ Δran⁺) = ({a₅, a₇} ∖ {a₅, a₇}) ∪ (cov(e) ∩ ∅) = ∅ ∪ ∅ = ∅`. ✓

Cross-document frame: `Σ₃.M(d') = Σ₂.M(d')` by Π12, so `proj(d', e, Σ₃) = {0}` and `iproj(d', e, Σ₃) = {a₆}` — both *unchanged*. This is the **R10 witness**: `proj(d, e, Σ₃) = ∅` while simultaneously `proj(d', e, Σ₃) = {0} ≠ ∅`. Emptying the projection in one document leaves the projection in another document — and hence the link's discoverability through that document — entirely intact. `ℓ` itself is still arranged in `d_link`: `Σ₃.M(d_link) = Σ₂.M(d_link) = {0 ↦ ℓ}`.

**Step 4: K.μ⁻ on `M(d_link)` removing V-position `0` (`Σ₃ → Σ₄`).** Now we *reverse-orphan* `ℓ` — drop the sole V-position of `d_link` that arranges `ℓ`. The K.μ⁻ contract gives `dom(Σ₄.M(d_link)) = ∅`, so

`Σ₄.M(d_link) = ∅`

Now `ℓ ∉ ran(Σ₄.M(d_link))`, and (because we set up `d_link` as the *only* document arranging `ℓ`) `ℓ ∉ ran(Σ₄.M(d''))` for every `d'' ∈ E_doc`. The link is unarranged in every document's link subspace.

Apply Π15b: K.μ⁻ on `M(d_link)` leaves `Σ.L` and every link value untouched. Hence `Σ₄.L = Σ₃.L = Σ₀.L`, `ℓ ∈ dom(Σ₄.L)`, and `cov(Σ₄.L(ℓ).e) = {a₅, a₆, a₇} = cov(Σ₀.L(ℓ).e)`. The endset's coverage is permanent regardless of whether `ℓ` itself is arranged anywhere.

Cross-document frame (Π12) on the projection side: the write set is `M(d_link)`, so `Σ₄.M(d) = Σ₃.M(d) = {3 ↦ a₈}` and `Σ₄.M(d') = Σ₃.M(d') = {0 ↦ a₆, 1 ↦ a₉}`. Therefore:

- `proj(d, e, Σ₄) = ∅`, `iproj(d, e, Σ₄) = ∅` (carried over from Σ₃).
- `proj(d', e, Σ₄) = {0}`, `iproj(d', e, Σ₄) = {a₆}` (carried over from Σ₃).

This is the **R11 witness**: `ℓ` is reverse-orphaned (no document arranges it), yet the endset projection of `ℓ` into `d'` continues to function exactly as before. The link's *self-arrangement* (whether it appears in some document's link-subspace V-stream) is independent of its *endset projection* (the V-positions reached by following its endset coverage). Furthermore, by Π16/Π17, the link remains discoverable via `d'` from any V-region of `d'` containing position `0` — for instance, `reaches(ℓ, d', {0}, Σ₄)` holds because `a₆ ∈ cov(Σ₄.L(ℓ).e) ∩ ran(Σ₄.M(d')|_{0})`.

**Step 5 (counterfactual): a hypothetical K.μ⁺ adding `(4 ↦ a₆)` to `M(d)` (`Σ₄ → Σ₅`).** From the doubly-degraded state of Σ₄ (empty `proj(d, e, ·)`, reverse-orphaned `ℓ`), extend `M(d)` by placing `a₆` at a fresh V-position:

`Σ₅.M(d) = {3 ↦ a₈, 4 ↦ a₆}`

with `dom(Σ₅.M(d)) = {3, 4} ⊃ {3} = dom(Σ₄.M(d))` and the K.μ⁺ contract preserving `Σ₅.M(d)(3) = a₈`.

- `iproj(d, e, Σ₅) = {a₅, a₆, a₇} ∩ {a₈, a₆} = {a₆}` — partial recovery: the V-projection of `e` into `d` is non-empty again.
- `proj(d, e, Σ₅) = {v ∈ {3, 4} : Σ₅.M(d)(v) ∈ cov(e)} = {4}` — V-position `4` now realizes the coverage address `a₆`.

Verify Π11(d) closed form: `Δran⁺ = {a₈, a₆} ∖ {a₈} = {a₆}` and `Δran⁻ = {a₈} ∖ {a₈, a₆} = ∅`. The closed form predicts `iproj(d, e, Σ₅) = (∅ ∖ ∅) ∪ ({a₅, a₆, a₇} ∩ {a₆}) = ∅ ∪ {a₆} = {a₆}`. ✓

This is R9 (reintroduction) in its strongest form: *even from a state with empty I-projection in `d` and a reverse-orphaned `ℓ`*, a single `K.μ⁺` placing a coverage address `a₆ ∈ dom(Σ.C)` into `M(d)` restores `a₆` to the projection. The link's coverage permanence (Π3) and the content's permanence in `dom(Σ.C)` (S0) together suffice; neither emptying the projection in `d` nor unarranging `ℓ` itself permanently extinguishes the projection's recoverability.

**Step 6: K.α + K.μ⁺ illustrating R13's two CCR policies (`Σ₅ → Σ₇`).** R13 is the only synthesized guarantee whose behavior depends on the choice between CCR-restricted and CCR-open. The worked example so far has not exhibited the divergence; we now exhibit it under both policies.

From `Σ₅`, suppose `K.α` allocates a fresh content address `a_new` (with `a_new ∉ dom(Σ₅.C)`, by K.α's freshness clause) — call the intermediate post-state `Σ₆`. Then a subsequent `K.μ⁺` extends `M(d)` to place `a_new` at a new V-position 5, "between" the existing arrangement and the link's earlier reach:

`Σ₇.M(d) = {3 ↦ a₈, 4 ↦ a₆, 5 ↦ a_new}`

with `dom(Σ₇.M(d)) = {3, 4, 5} ⊃ {3, 4} = dom(Σ₆.M(d))` and `Σ₇.M(d)(v) = Σ₆.M(d)(v) = Σ₅.M(d)(v)` for `v ∈ {3, 4}` (K.μ⁺ contract). Note that `Σ₆.M = Σ₅.M` by K.α's frame condition (Π13), so the substantive change to `M(d)` is concentrated at K.μ⁺. The question is whether `a_new ∈ iproj(d, e, Σ₇)` — equivalently, whether the projection grows beyond `{a₆}`.

*Policy (i) — CCR-restricted.* Under this policy, link allocation `K.λ` at `Σ₀` enforced `cov(e) ⊆ dom(Σ₀.C)`. We chain three appeals. (a) K.α's freshness gives `a_new ∉ dom(Σ₅.C)`. (b) S1 (StoreMonotonicity) gives `dom(Σ₀.C) ⊆ dom(Σ₅.C)`. (c) Combining contrapositively, `a_new ∉ dom(Σ₀.C) ⊇ cov(e) = {a₅, a₆, a₇}`, so `a_new ∉ cov(e)`. Apply Π11(d): `Δran⁺ = ran(Σ₇.M(d)) ∖ ran(Σ₅.M(d)) = {a₈, a₆, a_new} ∖ {a₈, a₆} = {a_new}` and `Δran⁻ = ∅`; the closed form predicts
 
`iproj(d, e, Σ₇) = (iproj(d, e, Σ₅) ∖ ∅) ∪ (cov(e) ∩ {a_new}) = {a₆} ∪ ∅ = {a₆}`.

The new content does not enter the projection. The V-projection accordingly remains `proj(d, e, Σ₇) = {4}` — V-position 5 maps to `a_new ∉ cov(e)` and is excluded. This is R13's "strap holds its original bytes" guarantee, witnessed concretely.

*Policy (ii) — CCR-open.* Under this policy, `K.λ` at `Σ₀` was permitted to allocate `e` with ghost references — I-addresses present in `T` but not yet in `dom(Σ₀.C)`. Suppose `e` was created with `cov(e) = {a₅, a₆, a₇, a_new}` — i.e., the endset deliberately reached forward to `a_new` as a ghost reference at link creation. By coverage permanence (Π3), this coverage is fixed across all reachable states, so `cov(Σ₅.L(ℓ).e) = cov(Σ₇.L(ℓ).e) = {a₅, a₆, a₇, a_new}`. At `Σ₅`, however, `a_new ∉ dom(Σ₅.C)` (the K.α step has not yet occurred) and `a_new ∉ ran(Σ₅.M(d)) = {a₈, a₆}`, so `iproj(d, e, Σ₅) = cov(e) ∩ {a₈, a₆} = {a₆}` — the ghost reference contributes nothing while `a_new` is unallocated and unarranged. After K.α (now `a_new ∈ dom(Σ₆.C)`) and K.μ⁺ (now `a_new ∈ ran(Σ₇.M(d))`), apply Π11(d): `Δran⁺ = {a_new}` and `cov(e) ∩ Δran⁺ = {a_new}`; the closed form predicts

`iproj(d, e, Σ₇) = ({a₆} ∖ ∅) ∪ ({a_new}) = {a₆, a_new}`.

The projection has grown by `a_new` — exactly the design-intended behavior of forward-reference endsets. R13's "no silent extension" guarantee does not apply under CCR-open, and indeed the V-projection now includes V-position 5: `proj(d, e, Σ₇) = {4, 5}`.

*The divergence.* The two policies produce different post-projections from identical sequences of K.α + K.μ⁺ on identical-looking arrangements, depending entirely on what `cov(e)` was permitted to reach at `K.λ`. The divergence is not observable from `M(d)` alone — it is encoded in `cov(e)`, fixed forever at link allocation by Π3, and the two policies allocate different coverage sets at the same `K.λ` event. R9 (the Step 5 reintroduction of `a₆`) is unaffected by the choice — `a₆` was in `cov(e)` and `dom(Σ₀.C)` under both policies, so neither policy excludes it — but R13 is genuinely divided.

## Weakest Preconditions

We now derive a weakest-precondition expression — a backward calculation of which initial states satisfy a chosen postcondition under a given transition.

**wp(K.μ⁻, iproj(d, e) ≠ ∅).** Question: which states `Σ` admit a K.μ⁻ contraction that *fails* to empty `d`'s I-projection of `e`?

Let `V_drop = dom(Σ.M(d)) ∖ dom(Σ'.M(d))` be the set of V-positions removed by the contraction; the K.μ⁻ contract fixes `Σ'.M(d)(v) = Σ.M(d)(v)` on `dom(Σ'.M(d)) = dom(Σ.M(d)) ∖ V_drop`. The postcondition `iproj(d, e, Σ') ≠ ∅` expands to

`cov(e) ∩ ran(Σ'.M(d)) ≠ ∅`

We compute, by definition of `ran` and the contract:

```
cov(e) ∩ ran(Σ'.M(d)) ≠ ∅
= {def of ran}
  (E v ∈ dom(Σ'.M(d)) :: Σ'.M(d)(v) ∈ cov(e))
= {dom(Σ'.M(d)) = dom(Σ.M(d)) ∖ V_drop ; Σ'.M(d)(v) = Σ.M(d)(v) on this domain}
  (E v ∈ dom(Σ.M(d)) ∖ V_drop :: Σ.M(d)(v) ∈ cov(e))
= {def of proj}
  (E v ∈ proj(d, e, Σ) ∖ V_drop :: true)
= {non-emptiness of difference}
  proj(d, e, Σ) ⊄ V_drop
```

Hence

`wp(K.μ⁻[V_drop], iproj(d, e) ≠ ∅) ≡ proj(d, e, Σ) ⊄ V_drop`

In words: a K.μ⁻ that drops exactly `V_drop` from `M(d)` preserves a non-empty I-projection iff some V-position in `proj(d, e, Σ)` is retained — equivalently, the projecting set is *not* a subset of the dropped set. The weakest condition on `Σ` is therefore that at least one currently-projecting V-position survives the contraction.

The corner cases are illuminating:

- If `proj(d, e, Σ) = ∅` already, the precondition fails for any non-empty `V_drop` (vacuously: `∅ ⊆ V_drop`), correctly predicting that the projection cannot become non-empty under K.μ⁻ (which can only shrink — Π9b).
- If `V_drop ∩ proj(d, e, Σ) = ∅`, the precondition holds trivially: dropping non-projecting positions cannot affect the I-projection (Π9a + invariance of `iproj` under range-preserving contractions).
- If `V_drop ⊇ proj(d, e, Σ)`, the precondition fails: dropping every projecting position empties the projection.

This wp characterization is the link holder's diagnostic: to preserve discoverability in `d`, the operator must retain at least one V-position currently in `proj(d, e, Σ)`. Symmetrically, an editor wishing to *break* the link's local visibility in `d` (without affecting it in `L`) must drop the entire projection set.

## Three Modes of Displacement

The same projection function governs three operational scenarios, each a different mode of *projection displacement*.

**Mode I: Editing.** A sequence of `K.μ⁺`, `K.μ⁻`, `K.μ~` operations on `M(d)` modifies how content is arranged in document `d`. The link's structure is untouched (R1–R4). The projection in `d` follows the content via I-address identity (Π11): V-positions may shift under rearrangement (Π10); the projection may narrow under contraction (Π9) or grow under extension (Π8). In every case, every I-address in `cov(eᵢ)` that survives in `ran(M(d))` is still in `iproj(d, ℓ, i, Σ)`, and the V-position currently realizing it is in `proj(d, ℓ, i, Σ)`. The strap stays attached to the bytes; only their current V-positions change.

The boundary insertion case is contingent on CCR-restricted: when `K.α` allocates a new content address `a_new` and a subsequent `K.μ⁺` places `a_new` in `M(d)` adjacent to or amid a linked region, `a_new ∉ cov(eᵢ)` *provided* CCR-restricted held at link creation. The chain of justification has three steps. (i) The K.α allocator discipline (ASN-0047, drawing on T10a's GlobalUniqueness) produces `a_new` fresh with respect to the K.α-pre-state `Σ_k`: `a_new ∉ dom(Σ_k.C)`. (ii) S1 (StoreMonotonicity, ASN-0036) gives `dom(Σ₀.C) ⊆ dom(Σ_k.C)` for any forward-reachable `Σ₀ → ... → Σ_k`. (iii) Contrapositively, freshness at `Σ_k` (`a_new ∉ dom(Σ_k.C)`) combined with the inclusion `dom(Σ₀.C) ⊆ dom(Σ_k.C)` yields `a_new ∉ dom(Σ₀.C)`. Under CCR-restricted, `cov(eᵢ) ⊆ dom(Σ₀.C)`, so `a_new ∉ cov(eᵢ)`. Under CCR-restricted no "boundary rule" is needed; the I-address algebra excludes the new bytes by construction. Under CCR-open, a ghost endset may already cover `a_new`, and the projection grows accordingly — by design, not by accident (R13 conditional).

**Mode II: Versioning and Transclusion.** This mode depends on a structural property of versioning operations that we now state and name explicitly, rather than borrowing it from another ASN.

**Versioning Assumption (VA).** A versioning operation that creates a fresh document `d_v ∈ E_doc` as a version of `d ∈ E_doc` produces an initial arrangement satisfying `ran(Σ.M(d_v)) ⊆ ran(Σ.M(d))` in the immediate post-state `Σ`. That is, `d_v`'s arrangement initially reaches only I-addresses already reached by `d`'s arrangement; no fresh I-addresses are coined by the versioning act itself.

We adopt VA as a local axiom for this mode of analysis. It is consistent with Nelson's design intent that a version *shares* content with its source (rather than replicating it) and with the I-pool / V-arrangement separation that underpins Mode III. It also constrains only the *initial* post-fork state: subsequent K.μ-transitions on `d_v` may add to or remove from `ran(Σ.M(d_v))` independently of `d`, which is exactly what Π8, Π9, Π10 already govern. A separate ASN may derive VA from a more primitive versioning contract; here we use VA without further derivation.

Under VA, in the immediate post-fork state `Σ`, the I-projection into `d_v` is bounded above by the I-projection into `d`:

`iproj(d_v, e, Σ) = cov(e) ∩ ran(Σ.M(d_v)) ⊆ cov(e) ∩ ran(Σ.M(d)) = iproj(d, e, Σ)`

— the first equality is the definition of `iproj`, the inclusion follows from VA by intersecting with `cov(e)`, and the second equality is again the definition. Hence any I-address that `cov(e)` reaches via `d`'s arrangement and that is also retained in `d_v`'s inherited arrangement appears in `iproj(d_v, e, Σ)`; the link projects into `d_v` accordingly. By Π5, this projection is computed locally from `M(d_v)` and `cov(e)` alone; by Π6, it is independent of `d`'s subsequent state and of any version's lineage. Whether the two I-projections are equal or proper depends on what fraction of `ran(Σ.M(d))` was carried over to `M(d_v)` at forking and how `M(d_v)` subsequently evolves.

Transclusion (and general inter-document sharing) is the same phenomenon viewed differently: any document whose arrangement reaches a shared I-address inherits the link's projection at that address. A "link to one version" is a "link to all versions" precisely because every version shares the I-addresses of the source (Π11, Π17). The link is not bound to any one document; it follows the content through every document that arranges that content.

**Mode III: Permanence Beyond Arrangement.** Even if every document currently arranging some I-address `a ∈ cov(eᵢ)` contracts via `K.μ⁻` to remove `a`, the address remains in `dom(C)` permanently (S0). The link's coverage still contains `a` (Π3). A future state can re-arrange `a` into some document via `K.μ⁺`, restoring `a` to that document's projection (R9). The link is never destroyed by deletion from any single document or even from all documents; its projection may be temporarily empty everywhere, but the link's structure and the validity of its coverage persist forever.

Across all three modes, projection displacement is bounded by the elementary transitions and their frame conditions. The link holder relies on the structural invariants (R1–R4, R11) unconditionally and on R13 conditionally on CCR-restricted; the projection's local adaptation (R5–R10, R12) is a controlled, computable consequence of arrangement changes — never a corruption, never a loss of the link itself.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Π0 | LinkValuePermanence: `(A Σ → Σ', ℓ ∈ dom(Σ.L) :: Σ'.L(ℓ) = Σ.L(ℓ))` | introduced |
| Π1 | ArityPermanence: `\|Σ'.L(ℓ)\| = \|Σ.L(ℓ)\|` across every transition | introduced |
| Π2 | SlotPermanence: `Σ'.L(ℓ).eᵢ = Σ.L(ℓ).eᵢ` for every slot `i` | introduced |
| Π3 | CoveragePermanence: `cov(Σ'.L(ℓ).eᵢ) = cov(Σ.L(ℓ).eᵢ)` | introduced |
| Π4 | DirectionalPermanence: slot positions and directional roles are immutable | introduced |
| Π5 | ProjectionLocality: `proj(d, e, Σ)` depends only on `Σ.M(d)` and `cov(e)` | introduced |
| Π6 | CrossDocumentIndependence: `proj(d, e, Σ)` and `proj(d', e, Σ)` are independent for `d ≠ d'` | introduced |
| Π7 | CoverageEquivalence: `cov(e₁) = cov(e₂) ⟹ proj(d, e₁, Σ) = proj(d, e₂, Σ)` | introduced |
| Π8 | ProjectionUnderExtension: `K.μ⁺` can only grow the projection | introduced |
| Π9 | ProjectionUnderContraction: `K.μ⁻` can only shrink the projection | introduced |
| Π10 | ProjectionUnderRearrangement: `K.μ~` permutes V-projection, preserves I-projection | introduced |
| Π11 | ProjectionFollowsContent: `iproj` is monotone with `ran(M(d))` across K.μ-transitions (Π11a–c); closed form `iproj(d, e, Σ') = (iproj(d, e, Σ) ∖ Δran⁻) ∪ (cov(e) ∩ Δran⁺)` (Π11d) | introduced |
| Π12 | CrossDocumentFrame: operations on `M(d')` do not affect `proj(d, ·, ·)` for `d ≠ d'` | introduced |
| Π13 | ContentAllocationFrame: `K.α` does not affect any existing projection | introduced |
| Π14 | LinkAllocationFrame: `K.λ` does not affect any existing projection | introduced |
| Π15a | UnarrangedLinkConsistency: `ℓ ∈ dom(Σ.L)` is consistent with `ℓ ∉ ran(Σ.M(d))` for every `d` | introduced |
| Π15b | ReverseOrphaningPreservesL: K.μ⁻ on `M(d)` removing `ℓ` from `ran` leaves `Σ.L` unchanged | introduced |
| Π16 | ReachLocality: reach depends only on `L`, `M(d)\|_{V_q}`, and the V-region | introduced |
| Π17 | PartialReach: non-empty coverage-range intersection suffices for reach | introduced |
| RB | ReachBridge: `reaches(ℓ, d, V_q, Σ) ⟺ (E i :: cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)\|_{V_q}) ≠ ∅)` — I-side reformulation of reach used by Π16 | introduced |
| S3-text | Stratified text-subspace referential integrity: `ran(Σ.M(d)\|_{s_C}) ⊆ dom(Σ.C)\|_{s_C}` — local axiom adopted in Π15a's proof; not a modification of foundation S3 | local axiom |
| S3-link | Stratified link-subspace referential integrity: `ran(Σ.M(d)\|_{s_L}) ⊆ dom(Σ.L)` — local axiom adopted in Π15a's proof; not a modification of foundation S3 | local axiom |
| Role | `Role : LinkType × ℕ → Direction` — the Σ-external slot-role function from L7, named explicitly here and invoked in Π4 | introduced (named) |
| K.λ-cov-nonempty | For every slot `i` of a `K.λ`-allocated value, `cov(eᵢ) ≠ ∅` | local axiom (recommended) |
| Σ.proj | `proj(d, e, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(e)}` | introduced |
| Σ.iproj | `iproj(d, e, Σ) = cov(e) ∩ ran(Σ.M(d))` | introduced |
| Σ.reaches | `reaches(ℓ, d, V_q, Σ) ≡ (E i :: proj(d, ℓ, i, Σ) ∩ V_q ≠ ∅)` | introduced |
| CCR | Coverage-at-Creation Rule: structural choice between CCR-restricted (`cov(eᵢ) ⊆ dom(Σ₀.C)`) and CCR-open (`cov(eᵢ) ⊆ T`, ghost references permitted) | open axiom |
| VA | Versioning Assumption: the immediate post-fork state satisfies `ran(Σ.M(d_v)) ⊆ ran(Σ.M(d))` | local axiom |

## Open Questions

What abstract conditions on the transition vocabulary are sufficient to guarantee that the projection function is single-valued for every reachable state?

What is the minimal information a discovery primitive must consult to be complete — must it consult the entire `Σ.L`, or can it be restricted to a smaller subset determined by the I-addresses in `ran(Σ.M(d)|_{V_q})`?

Under what conditions can a state make `proj(d, e, Σ) = ∅` for every `d ∈ E_doc` simultaneously, and what abstract guarantee ensures that some subsequent state can restore a non-empty projection?

What guarantees must hold on a composite transition that contracts every projection of a link to empty and then re-extends some of them — does the order of operations affect the reachable post-state, or is the final projection a path-independent function of the cumulative changes to each `M(d)`?

Can the projection function be lifted to operate on endset *unions* and *intersections* in a way that distributes over the lift — that is, does `proj(d, e₁ ∪ e₂, Σ) = proj(d, e₁, Σ) ∪ proj(d, e₂, Σ)` follow from the definitions, and what abstract structure does this give to the space of projections?

What abstract guarantee constrains how the projection of an endset across a document boundary — when `cov(e)` contains I-addresses originating in multiple documents — relates to the per-document projections summed together?

Should the abstract specification settle the Coverage-at-Creation Rule as CCR-restricted, CCR-open, or as a per-endset parameter, and what abstract property of discoverability or boundary insertion does each choice preserve or sacrifice?
