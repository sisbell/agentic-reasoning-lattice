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

## The Projection

We need a bridge between the link's I-address endsets and the V-positions a reader sees in a document. We call this bridge the *projection*.

**Definition (Projection).** Given a state `Σ`, a document `d ∈ E_doc`, and an endset `e`, the *projection of `e` into `d` at `Σ`* is

`proj(d, e, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(e)}`

— the V-positions in `d` whose arrangement target lies in `e`'s coverage.

For a link `ℓ ∈ dom(Σ.L)` and slot index `i ∈ {1, ..., |Σ.L(ℓ)|}`, we write `proj(d, ℓ, i, Σ)` for `proj(d, Σ.L(ℓ).eᵢ, Σ)`.

A useful complement records *which I-addresses* the projection reaches in `d`:

`iproj(d, e, Σ) = cov(e) ∩ ran(Σ.M(d))`

Where `proj(d, e, Σ) ⊆ dom(Σ.M(d))` lives in V-space, `iproj(d, e, Σ) ⊆ T` lives in I-space, and the two are connected by the arrangement: `iproj(d, e, Σ) = Σ.M(d)(proj(d, e, Σ))`.

The projection function consults only `Σ.M(d)` and the endset `e`. No history of how `M(d)` was constructed, no link's home document, no auxiliary registry, no other document's arrangement appears in the definition. This locality is the first nontrivial property we shall establish.

## Permanence of Link Structure

The first claims concern what does not change. Each is a structural consequence of `L12`; together they say that whatever was true of `ℓ`'s value at creation is true forever.

**Π0 (LinkValuePermanence).** For every state transition `Σ → Σ'`:

`(A ℓ : ℓ ∈ dom(Σ.L) :: ℓ ∈ dom(Σ'.L) ∧ Σ'.L(ℓ) = Σ.L(ℓ))`

Inherited from L12. The transition vocabulary (ASN-0047) provides no operation that modifies an existing entry in `L`; `K.λ` adds a new entry, and every other operation has a frame condition that leaves `L` unchanged.

**Π1 (ArityPermanence).** `|Σ'.L(ℓ)| = |Σ.L(ℓ)|` — the number of endsets is fixed at creation. Direct consequence of Π0.

**Π2 (SlotPermanence).** `Σ'.L(ℓ).eᵢ = Σ.L(ℓ).eᵢ` for every slot `i`. Link equality is component-wise tuple equality (L6, ASN-0043), so Π0 forces each slot to be preserved.

**Π3 (CoveragePermanence).** `cov(Σ'.L(ℓ).eᵢ) = cov(Σ.L(ℓ).eᵢ)`. The set of I-addresses each endset references is permanent. Coverage is a function of the endset, and the endset is permanent by Π2.

**Π4 (DirectionalPermanence).** The role of each slot — which is the *from*-endset, which is the *to*-endset, which is the *type*-endset under the StandardTriple convention, or whatever role assignment is in force for higher-arity links — is determined by slot position alone (L6, L7, ASN-0043). Slot positions are permanent by Π2; no transition swaps, reorders, or relabels slots; no transition reinterprets the directional role of an existing slot.

The structure of `ℓ` — address, value, arity, endsets, coverage, slot positions, directional roles — is, taken together, the *invariant content of the link*. The link holder can treat all of it as fixed.

## Projection Properties

The projection, in contrast, is computed afresh in each state.

**Π5 (ProjectionLocality).** `proj(d, e, Σ)` depends only on `Σ.M(d)` and `cov(e)`:

`(A Σ, Σ', d, e : Σ.M(d) = Σ'.M(d) : proj(d, e, Σ) = proj(d, e, Σ'))`

If two states agree on `M(d)`, their projections into `d` agree, irrespective of any other difference. In particular, the projection does not depend on:

- which document allocated `ℓ` (its origin, derivable via L1c of ASN-0043 from `ℓ`'s tumbler — but never consulted);
- any history of how `M(d)` was constructed (which `K.μ⁺` / `K.μ⁻` / `K.μ~` events led to it);
- the arrangement `M(d')` of any other document `d' ≠ d`;
- the contents of `C` other than what `M(d)` currently references.

This is what an alternative implementation must guarantee for cross-document linking to be sound. Whatever auxiliary indexes the implementation employs for efficiency, the *value* returned by the projection function is constrained to be a function of `M(d)` and `cov(e)` alone.

**Π6 (CrossDocumentIndependence).** For `d ≠ d'`:

`proj(d, e, Σ)` and `proj(d', e, Σ)` are computed independently of each other.

A single link projects into many documents simultaneously; each projection is determined by that document's arrangement alone.

**Π7 (CoverageEquivalence).** Two endsets with identical coverage produce identical projections:

`cov(e₁) = cov(e₂) ⟹ (A d, Σ :: proj(d, e₁, Σ) = proj(d, e₂, Σ))`

Different span decompositions of the same coverage set are projection-indistinguishable. Coverage — not the literal span tuple — is the observable through projection.

## Behavior Under State Transitions

We now examine how the projection responds to each elementary operation that touches `M`.

**Π8 (ProjectionUnderExtension).** For `K.μ⁺` extending `Σ.M(d)` to `Σ'.M(d)` with `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))` and `(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`:

(a) Prior projection is retained: `proj(d, e, Σ) ⊆ proj(d, e, Σ')`.

(b) Newly added positions whose I-target lies in `cov(e)` enter the projection:

`proj(d, e, Σ') ∖ proj(d, e, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ cov(e)}`

Extension can only grow the projection.

**Π9 (ProjectionUnderContraction).** For `K.μ⁻` contracting `Σ.M(d)` to `Σ'.M(d)` with `dom(Σ'.M(d)) ⊂ dom(Σ.M(d))` and `(A v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`:

(a) Retained positions keep their projection status: `proj(d, e, Σ') = proj(d, e, Σ) ∩ dom(Σ'.M(d))`.

(b) `proj(d, e, Σ') ⊆ proj(d, e, Σ)`. The projection can only shrink.

This is the *partial survival* case: even when `K.μ⁻` removes some V-positions from `proj(d, e, Σ)`, others may remain. The projection narrows; the link itself is not broken. If `K.μ⁻` removes every position in `proj(d, e, Σ)`, the projection in `d` becomes empty — but the link's structure, by Π0–Π3, is still intact, and the projection in some other document `d'` may still be non-empty.

**Π10 (ProjectionUnderRearrangement).** For `K.μ~` permuting `Σ.M(d)` via bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))` with `Σ'.M(d)(π(v)) = Σ.M(d)(v)`:

(a) The I-projection is invariant: `iproj(d, e, Σ') = iproj(d, e, Σ)`.

(b) The V-projection is permuted: `proj(d, e, Σ') = {π(v) : v ∈ proj(d, e, Σ)}`.

K.μ~-FIX (ASN-0047) gives `dom(Σ'.M(d)) = dom(Σ.M(d))`. Rearrangement preserves the *set of (V, I) pairs* up to permutation of V-positions; the projection's image in I-space is exactly preserved.

**Π11 (ProjectionFollowsContent).** Synthesizing Π8–Π10: if a state transition leaves some I-address `a ∈ cov(e)` mapped to a V-position in `M(d)` — possibly at a different V-position than before — then the projection in `Σ'` contains `a`'s new V-position. The link's projection clings to I-addresses, not to V-positions.

Symbolically, for any `a ∈ cov(e)`:

`a ∈ ran(Σ'.M(d)) ⟹ (E v ∈ proj(d, e, Σ') :: Σ'.M(d)(v) = a)`

This is the *strap-between-bytes* principle formalized: editing operations displace V-positions, but the link's coverage in I-space remains a fixed target. The projection tracks the content.

**Π12 (CrossDocumentFrame).** Operations whose effect on `M` is confined to a single document leave projections into other documents untouched. For any transition `Σ → Σ'` and documents `d ≠ d'`:

`(A op : op modifies only M(d') :: (A e :: proj(d, e, Σ) = proj(d, e, Σ')))`

`K.α`, `K.λ`, `K.δ`, `K.μ⁻`, `K.μ⁺`, `K.μ⁺_L`, `K.μ~`, and `K.ρ` all carry such a frame on documents other than their target (per ASN-0047). The projection into `d` is invariant under any operation that does not touch `M(d)`.

**Π13 (ContentAllocationFrame).** `K.α` extends `dom(C)` but does not modify any `M(d)`:

`(A d, e, ℓ ∈ dom(Σ.L) : proj(d, e, Σ) = proj(d, e, Σ'))`

across every `K.α`-transition. A newly allocated content address is not in any arrangement until a subsequent `K.μ⁺` places it; its presence in `dom(C)` alone does not affect any existing projection. Moreover, by Π3, the newly allocated address is not in the coverage of any existing endset — coverage was fixed at the link's creation, which precedes the address's allocation.

This is the *boundary insertion* property in disguise: when new content arrives adjacent to a linked region, the new content has a fresh I-address that is not in the existing link's coverage; the link's projection therefore does not silently expand to include the new content. No special rule is required to exclude it; the I-address algebra excludes it automatically.

**Π14 (LinkAllocationFrame).** `K.λ` extends `dom(L)` but does not modify any `M(d)`:

`(A d, e, ℓ ∈ dom(Σ.L) : proj(d, e, Σ) = proj(d, e, Σ'))`

across every `K.λ`-transition. The newly allocated link's endsets exist in `Σ'.L` but not in `Σ.L`; there is no projection to compare for the new link, only forward from `Σ'`.

## Independence from Arrangement

**Π15 (LinkArrangementIndependence).** The existence of a link in `L` and the validity of its value are independent of whether the link itself is arranged at any V-position in any document:

`(A ℓ ∈ dom(Σ.L), Σ → Σ' :: ℓ ∈ dom(Σ'.L) ∧ Σ'.L(ℓ) = Σ.L(ℓ))`

regardless of whether `(E d, v :: Σ.M(d)(v) = ℓ)` or `(E d, v :: Σ'.M(d)(v) = ℓ)`.

A link arranged in some document's link subspace via `K.μ⁺_L` can later be removed from that arrangement via `K.μ⁻` without affecting the link's existence in `dom(L)` or the validity of its endsets. We say the link is *reverse-orphaned* from that document — present in `L`, absent from `M(d)`.

Reverse orphaning does not impair the projection mechanism. Every claim in the preceding sections continues to apply: the reverse-orphaned link's endsets project into any document whose arrangement reaches the link's coverage I-addresses, exactly as before. The link's *self-arrangement* (whether it appears in some document's link-subspace V-stream) is a different matter from its *endset projection* (the V-positions reached by following its endset coverage).

## Backward Lookup: Discovery

The forward projection direction — link to V-positions — has a backward dual. Given a V-region in some document, which links are reached?

**Definition (Reach).** A link `ℓ` *reaches* a V-region `V_q ⊆ dom(Σ.M(d))` iff some endset's projection intersects `V_q`:

`reaches(ℓ, d, V_q, Σ) ≡ (E i :: proj(d, ℓ, i, Σ) ∩ V_q ≠ ∅)`

Equivalently:

`reaches(ℓ, d, V_q, Σ) ≡ (E i :: cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) ≠ ∅)`

**Π16 (ReachLocality).** Whether a link reaches a V-region is computable from `Σ.L`, `Σ.M(d)|_{V_q}`, and the region `V_q` alone:

`(A Σ, Σ', ℓ, d, V_q : Σ.L = Σ'.L ∧ Σ.M(d)|_{V_q} = Σ'.M(d)|_{V_q} : reaches(ℓ, d, V_q, Σ) ⟺ reaches(ℓ, d, V_q, Σ'))`

No provenance — neither the document that allocated `ℓ`, nor the document where the I-addresses originated, nor any history of which document first arranged those I-addresses — participates in the reach relation. The relation is intrinsic to the current state.

**Π17 (PartialReach).** Non-empty intersection of coverage with the V-region's image suffices for reach:

`(E α : α ∈ cov(Σ.L(ℓ).eᵢ) ∩ ran(Σ.M(d)|_{V_q}) :: reaches(ℓ, d, V_q, Σ))`

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

**(R11)** Reverse orphaning is benign. If the link itself is unarranged in any document's link subspace, the link's structure is unaffected, and projections of its endsets into any document continue to be well-defined. (Π15)

**(R12)** Discovery is preserved. For any V-region in any document that arranges some I-address in `cov(ℓ.eᵢ)`, the link is discoverable from that region by the reach relation, intrinsic to the current state. (Π16, Π17)

**(R13)** New content does not silently extend the link. Because coverage is permanent (Π3) and newly allocated addresses (via `K.α`) are not in any existing endset's coverage (they did not exist when the link was made), inserting new content adjacent to or within a linked region does not enlarge the projection to include the new bytes. The strap holds its original bytes, not their new neighbors. (Π3 + Π13)

## Three Modes of Displacement

The same projection function governs three operational scenarios, each a different mode of *projection displacement*.

**Mode I: Editing.** A sequence of `K.μ⁺`, `K.μ⁻`, `K.μ~` operations on `M(d)` modifies how content is arranged in document `d`. The link's structure is untouched (R1–R4). The projection in `d` follows the content via I-address identity (Π11): V-positions may shift under rearrangement (Π10); the projection may narrow under contraction (Π9) or grow under extension (Π8). In every case, every I-address in `cov(eᵢ)` that survives in `ran(M(d))` is still in `iproj(d, ℓ, i, Σ)`, and the V-position currently realizing it is in `proj(d, ℓ, i, Σ)`. The strap stays attached to the bytes; only their current V-positions change.

The boundary insertion case is automatic: when `K.α` allocates a new content address `a_new` and a subsequent `K.μ⁺` places `a_new` in `M(d)` adjacent to or amid a linked region, `a_new ∉ cov(eᵢ)` because `cov` is permanent (Π3) and `a_new` did not exist at link creation. The new V-position is not in the projection. No "boundary rule" is needed; the I-address algebra excludes the new bytes by construction (R13).

**Mode II: Versioning and Transclusion.** Forking a document `d` to a version `d_v` (via the `K.δ` + `K.μ⁺` composite J4 in ASN-0047) places `d_v` in `E_doc` and arranges `d_v` such that `ran(M(d_v)) ⊆ ran(M(d))` — sharing I-addresses with the source. By Π5 and Π6, any link whose endsets reach `ran(M(d))` may also reach `ran(M(d_v))`, and the projection into `d_v` is computed locally from `M(d_v)`. Whatever I-addresses `M(d_v)` covers from `cov(eᵢ)`, the link projects into `d_v` accordingly — independently of whether `d_v`'s arrangement was constructed wholesale or piecewise, independently of `d`'s current state, and independently of any version's lineage.

Transclusion (and general inter-document sharing) is the same phenomenon viewed differently: any document whose arrangement reaches a shared I-address inherits the link's projection at that address. A "link to one version" is a "link to all versions" precisely because every version shares the I-addresses of the source (Π11, Π17). The link is not bound to any one document; it follows the content through every document that arranges that content.

**Mode III: Permanence Beyond Arrangement.** Even if every document currently arranging some I-address `a ∈ cov(eᵢ)` contracts via `K.μ⁻` to remove `a`, the address remains in `dom(C)` permanently (S0). The link's coverage still contains `a` (Π3). A future state can re-arrange `a` into some document via `K.μ⁺`, restoring `a` to that document's projection (R9). The link is never destroyed by deletion from any single document or even from all documents; its projection may be temporarily empty everywhere, but the link's structure and the validity of its coverage persist forever.

Across all three modes, projection displacement is bounded by the elementary transitions and their frame conditions. The link holder relies on the structural invariants (R1–R4, R11, R13); the projection's local adaptation (R5–R10, R12) is a controlled, computable consequence of arrangement changes — never a corruption, never a loss of the link itself.

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
| Π11 | ProjectionFollowsContent: every surviving I-address in coverage remains in projection | introduced |
| Π12 | CrossDocumentFrame: operations on `M(d')` do not affect `proj(d, ·, ·)` for `d ≠ d'` | introduced |
| Π13 | ContentAllocationFrame: `K.α` does not affect any existing projection | introduced |
| Π14 | LinkAllocationFrame: `K.λ` does not affect any existing projection | introduced |
| Π15 | LinkArrangementIndependence: link existence in `L` is independent of arrangement in any `M(d)` | introduced |
| Π16 | ReachLocality: reach depends only on `L`, `M(d)\|_{V_q}`, and the V-region | introduced |
| Π17 | PartialReach: non-empty coverage-range intersection suffices for reach | introduced |
| Σ.proj | `proj(d, e, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ cov(e)}` | introduced |
| Σ.iproj | `iproj(d, e, Σ) = cov(e) ∩ ran(Σ.M(d))` | introduced |
| Σ.reaches | `reaches(ℓ, d, V_q, Σ) ≡ (E i :: proj(d, ℓ, i, Σ) ∩ V_q ≠ ∅)` | introduced |

## Open Questions

What abstract conditions on the transition vocabulary are sufficient to guarantee that the projection function is single-valued for every reachable state?

What is the minimal information a discovery primitive must consult to be complete — must it consult the entire `Σ.L`, or can it be restricted to a smaller subset determined by the I-addresses in `ran(Σ.M(d)|_{V_q})`?

Under what conditions can a state make `proj(d, e, Σ) = ∅` for every `d ∈ E_doc` simultaneously, and what abstract guarantee ensures that some subsequent state can restore a non-empty projection?

What guarantees must hold on a composite transition that contracts every projection of a link to empty and then re-extends some of them — does the order of operations affect the reachable post-state, or is the final projection a path-independent function of the cumulative changes to each `M(d)`?

Can the projection function be lifted to operate on endset *unions* and *intersections* in a way that distributes over the lift — that is, does `proj(d, e₁ ∪ e₂, Σ) = proj(d, e₁, Σ) ∪ proj(d, e₂, Σ)` follow from the definitions, and what abstract structure does this give to the space of projections?

What abstract guarantee constrains how the projection of an endset across a document boundary — when `cov(e)` contains I-addresses originating in multiple documents — relates to the per-document projections summed together?
