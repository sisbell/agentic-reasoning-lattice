# ASN-0098: Link Projection Displacement

*2026-05-24*

## The Question

A link was created at some past state. Its endsets were fixed at that moment against the I-addresses then visible. The documents through which a holder might follow the link have since been edited — passages inserted, removed, rearranged. A new document may have transcluded some of the linked content. The original document may have lost it entirely. The holder asks: "Where, in the current state, does my link reach? What can I rely on?"

We are looking for abstract guarantees. What stays fixed about the link itself? Which V-positions do its endsets reach in any given document? How do those V-positions move under each kind of editing operation? Under what conditions does the link survive — and what, exactly, does "survive" mean when the link's stored data and the document's current state are two different things?

We must distinguish three things that the literature often runs together:
- The *link* — a stored value at an address in `dom(Σ.L)`.
- The *coverage* of an endset — the set of I-addresses the endset denotes.
- The *projection* of an endset through a document — the V-positions in that document's current arrangement whose I-addresses lie in the coverage.

The first two are static once the link is created. The third is a live computation: it consults the document's mutable arrangement. Every interesting guarantee about "link behaviour under editing" is, on examination, a guarantee about how this third quantity displaces — gains or loses V-positions, rearranges them — as the arrangement changes.

## State Components

We work over the state structure inherited from the foundations. Three components matter here.

The content store `Σ.C : T ⇀ Val` is append-only with immutable values (S0, S1 of ASN-0036). Once an I-address `a` is bound, `Σ.C(a)` cannot be removed or rewritten. The set `dom(Σ.C)` only grows.

For each document `d ∈ dom(Σ.M)`, the arrangement `Σ.M(d) : T ⇀ T` is a partial function from V-positions to I-addresses. The arrangement is mutable: the operations K.μ⁺ (content-subspace extension), K.μ⁺_L (link-subspace extension), K.μ⁻ (contraction), and K.μ~ (reordering) of ASN-0047 modify it. The set of allocated documents `dom(Σ.M)` is non-decreasing (M1 of ASN-0093).

The link store `Σ.L : T ⇀ Link` binds link addresses to link values (ASN-0043). A link value is a sequence of endsets `Σ.L(a) = (e₁, e₂, …, eₙ)` with `N ≥ 3` and a non-empty type endset at slot 3 (L3). Each endset `eᵢ ∈ Endset` is a finite set of well-formed spans. The link store is immutable: by L12, `(A Σ → Σ', a ∈ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`.

The two address spaces communicate through the `Σ.M(d)` mappings: V-positions in V-space resolve to I-addresses in I-space. Links inhabit a third role — stored at link-subspace I-addresses but referencing content-subspace I-addresses through their endsets — but for the projection question this role-distinction is immaterial. What matters is that endsets reference I-addresses, and arrangements map V-positions to I-addresses, and the bridge between them is computed live.

*Working reference frame.* This ASN operates in the ASN-0047 transition-model frame layered over the ASN-0093 allocation substrate. ASN-0047 supplies the full operation vocabulary the projection responds to — K.σ, K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.δ, K.ρ — together with the extended-state invariants S3★ (GeneralizedReferentialIntegrity), S3★-aux (SubspaceExhaustiveness), CL-OWN, CL-UNIQ, and the per-subspace amendments D-CTG★, D-MIN★, D-SEQ★. The projection function defined in the next section consults only `coverage(e)` and `Σ.M(d)`; whenever an operation's frame holds `Σ.M(d)` constant, projection invariance follows by LP4. In sub-frames that lack link-subspace machinery — pre-extension states where no K.μ⁺_L can fire and `S3` (ASN-0036) suffices in place of S3★ — the projection function, LP4, and the per-document frame lemmas LP4–LP8 hold structurally identically; the ASN-0036 base frame is a strict subset of the ASN-0047 operation vocabulary. Two claims require the link-subspace machinery and do not survive descent to the ASN-0036 base frame intact: LP9's K.μ⁺_L sub-case (the operation itself is absent there), and LP20's per-subspace corollary refinement (which splits the range by S3★'s two-target clause, strictly stronger than S3's single-target content-subspace clause). The discussion below cites operations and invariants from the ASN-0047 + ASN-0093 frame and flags the two link-subspace-specific points at their use sites.

## The Coverage of an Endset

For an endset `e ⊆ Span`, the *coverage* `coverage(e)` is the set of I-addresses denoted by `e`'s spans, defined in ASN-0043 as

```
coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})
```

Each span `(s, ℓ)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ}` by T12 of ASN-0034, where `s ⊕ ℓ ∈ T` exists by TA0 because `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` are well-formedness conditions of the span. Coverage is a set of I-addresses in `T`. Some of these I-addresses may be in `dom(Σ.C)` at the time the endset was constructed; some may not. Crucially, coverage is a *purely combinatorial* property of the endset's span representation — it does not consult any state component. Coverage depends on the spans; nothing else.

By L5 (EndsetSetSemantics, ASN-0043), an endset is an unordered set. Two endsets with the same set of spans have the same coverage. The lossy projection `Endset → 2^T` defined by `coverage` is not injective: distinct span decompositions can have identical coverage (for instance, splitting a single span at an interior point produces two spans whose coverage equals the original).

## The Projection Operation

For an endset `e`, a document `d ∈ dom(Σ.M)`, and a state `Σ`, define the *projection of `e` through `d` at `Σ`* as the set of V-positions in `d`'s arrangement whose I-addresses lie within `e`'s coverage:

```
project(e, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}
```

The precondition `d ∈ dom(Σ.M)` is what makes `Σ.M(d)` well-defined; we adopt the convention that `project(e, d, Σ)` is left undefined when `d ∉ dom(Σ.M)`, rather than assigning it a default value, so that every appeal to `project` carries the membership obligation explicitly. For a link `a ∈ dom(Σ.L)` with slot `i ∈ {1, …, |Σ.L(a)|}`, write `project(a, i, d, Σ) ≡ project(Σ.L(a).eᵢ, d, Σ)`, defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`.

The definition reads from two inputs:
- The endset, fixed once and for all by the link's creation (and immune to subsequent transitions, by L12).
- The arrangement `Σ.M(d)`, mutable and reflecting whatever edits `d` has undergone.

Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies. The endset stands still. Therefore every change in projection must be attributable to a change in `Σ.M(d)` — and we can characterise the change by examining what each editing operation does to `Σ.M(d)`.

The definition does not separately consult `Σ.C` or `Σ.L`. Content allocation that does not modify any `Σ.M(d)` cannot affect any projection. Link allocation that does not modify `Σ.M(d)` cannot affect existing projections. Document registration (K.σ) that only updates `dom(Σ.M)` and initialises arrangements to empty cannot retroactively affect existing projections through existing documents. The projection is sensitive only to its two inputs, and only one of them moves.

Three degenerate configurations follow directly from the definition and require no separate treatment in subsequent claims. The projection of the empty endset is uniformly empty: `project(∅, d, Σ) = ∅` for every `d, Σ`, since `coverage(∅)` is the empty union over an empty index set. The projection through an empty arrangement is uniformly empty: `project(e, d, Σ) = ∅` when `dom(Σ.M(d)) = ∅`, since the set comprehension ranges over the empty domain. A link with empty from/to endsets but a non-empty type endset (admitted by L3 of ASN-0043, which requires only the type slot to be non-empty) has empty projections at slots 1 and 2 regardless of any document's state; only the type slot's projection can be non-empty.

## Immutability of the Stored Link

Before we can reason about how projection displaces, we must pin down what does *not* move. The link's stored content — its address, its sequence of endsets, the spans within each endset — is structurally immutable. By L12 of ASN-0043, for every state transition `Σ → Σ'`, every `a ∈ dom(Σ.L)` persists in `dom(Σ'.L)` with `Σ'.L(a) = Σ.L(a)`: the address persists, and the sequence of endsets is preserved verbatim. No operation in the transition vocabulary overwrites a link's value or removes a link from the store. Two consequences specialise L12 to the slot- and coverage-level reasoning this ASN requires.

**LP2 — SlotInvariance**: For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot index `i ∈ {1, …, |Σ.L(a)|}`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ
```

L12 (ASN-0043) supplies two conclusions on the hypothesis `a ∈ dom(Σ.L)`: address persistence `a ∈ dom(Σ'.L)` (which makes the slot accessor on the left-hand side well-defined) and value preservation `Σ'.L(a) = Σ.L(a)`. The slot equation then follows by component projection on the sequence: equal sequences have equal entries at every position. In particular, the slot-position assignment fixed at link creation — from-set at slot 1, to-set at slot 2, type-set at slot 3, and any additional slots — is structurally preserved. No editing operation can swap, relabel, or alter which slot carries which endset. The directionality of a standard triple (which end is "from", which is "to") is encoded in slot position alone, and slot position is immutable.

**LP2★ — MultiStepSlotInvariance**: For every reachable state sequence `Σ →* Σ'`, every link `a ∈ dom(Σ.L)`, and every slot index `i ∈ {1, …, |Σ.L(a)|}`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ
```

This is the reflexive-transitive closure of LP2. Proof by induction on the length of the transition sequence. The empty sequence (`Σ = Σ'`) gives the conjunction by reflexivity. For the inductive step, suppose `Σ →* Σ_n → Σ'` with `Σ_n.L(a).eᵢ = Σ.L(a).eᵢ` and `a ∈ dom(Σ_n.L)` by induction hypothesis. The single step `Σ_n → Σ'` gives `a ∈ dom(Σ'.L)` and `Σ'.L(a).eᵢ = Σ_n.L(a).eᵢ` by LP2, so by transitivity of equality the full chain holds.

**LP3 — CoverageInvariance**: For every transition `Σ → Σ'`, every link `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

LP2 supplies both conjuncts: `a ∈ dom(Σ'.L)` directly (so the slot accessor on the left-hand side of the coverage equation is well-defined), and `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` from which the coverage equation follows by applying `coverage` to both sides. The set of I-addresses the link refers to is computed from its endsets; if the endsets are byte-identical between states, the coverage is identical between states. Combining L12 with LP2 and LP3: the link, the slot, and the I-addresses it reaches are all permanent. What can vary is only which of those I-addresses are currently arranged in any given document.

**LP3★ — MultiStepCoverageInvariance**: For every reachable state sequence `Σ →* Σ'`, every `a ∈ dom(Σ.L)`, and every slot `i`:
```
a ∈ dom(Σ'.L) ∧ coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)
```

This is the reflexive-transitive closure of LP3. Proof by induction on the length of the transition sequence. The empty sequence (`Σ = Σ'`) gives equality trivially. For the inductive step, suppose `Σ →* Σ_n → Σ'` with `coverage(Σ_n.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` and `a ∈ dom(Σ_n.L)` by induction hypothesis. The single step `Σ_n → Σ'` gives `a ∈ dom(Σ'.L)` and `coverage(Σ'.L(a).eᵢ) = coverage(Σ_n.L(a).eᵢ)` by LP3, so by transitivity of equality the full chain holds.

**Store Monotonicity★**: For every reachable state sequence `Σ →* Σ'`:
```
dom(Σ.C) ⊆ dom(Σ'.C)  ∧  dom(Σ.L) ⊆ dom(Σ'.L)
```

Each is the reflexive-transitive closure of the corresponding single-step monotonicity guarantee (C0 of ASN-0093 for content; L12 of ASN-0093 for links, in its membership-persistence consequence). The base case is the empty sequence (reflexive containment); the inductive step composes containments transitively.

These invariants pin down what a link holder owns. Subsequent operations by any party — even the holder, even the original creator — cannot rewrite the endsets. The link is, in this strict sense, a permanent record.

## Frame Conditions: When Projection Does Not Move

A projection moves only if its inputs move. Since the endset (and therefore its coverage) is fixed by LP3, the projection through a document moves only if that document's arrangement is modified — and even then, only if the modification affects V-positions whose I-addresses lie in the endset's coverage.

**LP4 — ArrangementSpecificity**: For every transition `Σ → Σ'`, every endset `e`, and every document `d ∈ dom(Σ.M)`:
```
Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)
```

The projection function depends on exactly two inputs: `coverage(e)` and `Σ.M(d)`. The first is a pure function of the endset `e`, which appears unchanged on both sides of the equality — `coverage(e)` is therefore identical between the two projections. The second is the arrangement, equal by hypothesis. The hypothesis `Σ'.M(d) = Σ.M(d)` requires `d ∈ dom(Σ'.M)` for the equation to be parseable; this is automatically satisfied because `d ∈ dom(Σ.M)` together with M1 (ASN-0093) gives `d ∈ dom(Σ'.M)`, so `project(e, d, Σ')` is well-defined. Both inputs agree pointwise, so the set comprehension produces identical results. The projection cannot displace without `Σ.M(d)` displacing.

**LP5 — Cross-Document Independence**: Every operation in the K.μ family (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) has frame `(A d' : d' ≠ d : M'(d') = M(d'))` — it modifies at most one document's arrangement per transition. By LP4 applied to each unmodified document:
```
(A d' ∈ dom(Σ.M), d' ≠ d : project(e, d', Σ') = project(e, d', Σ))
```

A link's projection through one document is unaffected by editing operations on a different document. Projections are *per-document* facts. The link itself is a single global object, but the V-positions it reaches in any given document depend only on that document's local state.

**LP6 — Content-Allocation Invariance**: The K.α operation (ASN-0093) modifies only `Σ.C` and has frame `(A d :: M'(d) = M(d))`; K.α also preserves `dom(Σ.M)`, so `dom(Σ.M) = dom(Σ'.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`:
```
project(e, d, Σ') = project(e, d, Σ)
```
for every endset `e` and every such `d`, whenever `Σ → Σ'` is a K.α transition.

Newly allocated I-addresses are invisible to projection until some subsequent K.μ⁺ adds an arrangement entry referencing them. This is the precise sense in which "insertion at the boundary of a linked passage" cannot extend the link's reach: insertion as a composite (allocate + arrange) splits into a K.α step (no projection effect) and a K.μ⁺ step. The K.μ⁺ step might add a V-position to the projection, but only if the new V-position's I-address is in `coverage(e)`. By T10a (AllocatorDiscipline, ASN-0034), each new K.α-allocated I-address is structurally distinct from all prior allocations; under tight construction the new I-address lies outside `coverage(e)` (LP19a below formalises this freshness claim), and the projection does not grow (LP19, the projection consequence). Without tightness, the new I-address could fall within a half-open coverage interval reaching past existing content; the precise condition under which boundary insertion is excluded is therefore tightness, not allocator behaviour alone.

The abstract guarantee is sharper than the "outside the strap" metaphor: the projection depends on coverage and arrangement alone, and content allocation alone (K.α) affects neither.

**LP7 — Link-Allocation Invariance**: The K.λ operation modifies only `Σ.L`; its frame is `(A d :: M'(d) = M(d))`, and K.λ preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`, `project(e, d, Σ') = project(e, d, Σ)` for every endset `e` and every such `d`. Creating a new link cannot retroactively affect the projection of any other link.

**LP8 — Entity-Registration Invariance**: For any K.σ transition `Σ → Σ'` registering a fresh document `d_new` (with `d_new ∉ dom(Σ.M)`, `dom(Σ'.M) = dom(Σ.M) ∪ {d_new}`, `Σ'.M(d_new) = ∅`, and `Σ'.M(d) = Σ.M(d)` for every `d ∈ dom(Σ.M)`) and any endset `e`, both:

(a) Pre-state preservation: `(A d ∈ dom(Σ.M) :: project(e, d, Σ') = project(e, d, Σ))`.

(b) Newly-registered emptiness: `project(e, d_new, Σ') = ∅`.

Postcondition (a) follows by LP4 applied to each `d ∈ dom(Σ.M)`: the K.σ frame holds `Σ'.M(d) = Σ.M(d)` for every such `d`. Postcondition (b) follows from the definition of `project`: with `d_new ∈ dom(Σ'.M)` (so the projection is defined) and `dom(Σ'.M(d_new)) = ∅`, the set comprehension `{v ∈ dom(Σ'.M(d_new)) : Σ'.M(d_new)(v) ∈ coverage(e)}` ranges over the empty domain and is empty. Both postconditions are commitments — LP18 (resurrection) requires the well-defined empty projection through a newly-registered document until a K.μ⁺ or K.μ⁺_L fires; (a) and (b) together establish that no displacement occurs at K.σ time, neither at pre-existing documents nor at the new one.

*Remark on K.δ.* ASN-0047 includes K.δ as a unified entity-creation operation spanning nodes, accounts, and documents. The K.δ-IsNode and K.δ-IsAccount cases have frame `(A d :: M'(d) = M(d))` — no arrangement is modified — so LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)` yields projection invariance. The K.δ-IsDocument case creates a new document `d_new` with `M'(d_new) = ∅`, which is the same scenario as LP8 above; in this ASN's reference frame K.σ (ASN-0093) is the document-registration operation, and K.δ-IsDocument is subsumed by the LP8 argument. Each K.δ kind therefore reduces to either LP4 or LP8, and no separate displacement claim is required.

**LP14 — ProvenanceRecording Invariance**: The K.ρ operation (ASN-0047), which records provenance by adding a pair to `Σ.R`, has frame `(A d :: M'(d) = M(d))` — it leaves every document's arrangement intact — and preserves `dom(Σ.M)`. By LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)`, `project(e, d, Σ') = project(e, d, Σ)` for every endset `e` and every such `d`, whenever `Σ → Σ'` is a K.ρ transition. Provenance bookkeeping does not displace any projection.

## Operation Effects on Projection

We now examine each operation that *can* displace a projection. The pattern is uniform: each K.μ operation modifies `Σ.M(d)` in a constrained way, and the projection follows mechanically.

**LP9 — Extension under K.μ⁺ and K.μ⁺_L**: For every extension transition `Σ → Σ'` operating on document `d` — either K.μ⁺ (content-subspace extension) or K.μ⁺_L (link-subspace extension) — and every endset `e`:
```
project(e, d, Σ) ⊆ project(e, d, Σ')
```

The proof relies on exactly two structural facts about the post-state arrangement:
- (E1) *Strict domain extension:* `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))`.
- (E2) *Prior-domain agreement:* `(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`.

Both K.μ⁺ and K.μ⁺_L (ASN-0047) supply (E1) and (E2) directly in their effect clauses, so the projection-level argument is identical for both: for any `v ∈ project(e, d, Σ)`, `v ∈ dom(Σ.M(d)) ⊆ dom(Σ'.M(d))` by (E1), and `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(e)` by (E2) and the definition of `project`, so `v ∈ project(e, d, Σ')`. The projection can only grow.

*K.μ⁺_L's additional constraints leave (E1) and (E2) intact.* K.μ⁺_L imposes three constraints absent from K.μ⁺: (a) the target `ℓ` is a link address that must satisfy `ℓ ∉ ran(Σ.M(d))` (first-arrangement), (b) the new V-position has fixed depth `m_L = 2` (LinkVPositionDepthAxiom of ASN-0047), and (c) the new V-position is link-subspace (`subspace(v_ℓ) = s_L`) rather than content-subspace. Each constraint *restricts* the set of admissible extensions but does not alter the structural form of any extension that is admitted. After K.μ⁺_L fires, K.μ⁺_L's effect clause (ASN-0047) directly states `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {v_ℓ}` and `v_ℓ ∉ dom(Σ.M(d))` (the latter discharged within ASN-0047 by a per-subspace verification, summarised in the next sentence); together these give (E1). The freshness `v_ℓ ∉ dom(Σ.M(d))` decomposes by subspace via S3★-aux: if `V_{s_L}(d) = ∅`, then `v_ℓ = [s_L, 1, ..., 1]` is the D-MIN★ minimum and differs from every element of `V_{s_C}(d)` at position 1 by SC-NEQ (since `subspace(v_ℓ) = s_L ≠ s_C = subspace(v)` for any `v ∈ V_{s_C}(d)`); if `V_{s_L}(d) ≠ ∅`, then `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (ShiftStrictIncrease, ASN-0034) excludes every element of `V_{s_L}(d)`, and the same subspace divergence at position 1 excludes every element of `V_{s_C}(d)`. The agreement clause `(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))` holds because the effect adds a new mapping at `v_ℓ` without disturbing existing entries — (E2) holds. The constraints (a)–(c) affect which `ℓ` and which `v_ℓ` may appear in any specific K.μ⁺_L event, but they do not modify the way `Σ'.M(d)` relates to `Σ.M(d)` on the prior domain or how the domain grows. LP9's argument consumes only (E1) and (E2); it is invariant under these constraint-level differences. (The per-subspace dependence of D-CTG★/D-MIN★ in ASN-0047 governs *which* V-positions K.μ⁺_L may select — placing the new link-subspace V-position contiguously after the current `V_{s_L}(d)` maximum, or at its minimum if the subspace is empty — but does not affect the structural form of (E1)/(E2).)

The new V-positions that enter the projection are exactly the new arrangement entries whose I-addresses fall in the coverage:
```
project(e, d, Σ') ∖ project(e, d, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ coverage(e)}
```

The forward inclusion (⊆): suppose `v ∈ project(e, d, Σ') ∖ project(e, d, Σ)`. Then `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) ∈ coverage(e)` by the first conjunct. For the second, either `v ∉ dom(Σ.M(d))` or `Σ.M(d)(v) ∉ coverage(e)`. The second alternative is excluded: if `v ∈ dom(Σ.M(d))`, the agreement clause gives `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(e)`, contradicting `v ∉ project(e, d, Σ)`. So `v ∉ dom(Σ.M(d))`, placing `v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))`. The reverse inclusion (⊇): if `v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))` with `Σ'.M(d)(v) ∈ coverage(e)`, then `v ∈ project(e, d, Σ')` directly; and `v ∉ project(e, d, Σ)` since `v ∉ dom(Σ.M(d))`.

When K.μ⁺ adds entries mapping V-positions to newly K.α-allocated I-addresses, the projection's behaviour depends on the construction discipline of the endset. For endsets *tightly constructed* — whose spans do not extend past the relevant sub-allocator's emission frontier at construction time (formalised below as LP19) — the newly allocated I-address lies outside coverage, and the projection does not grow. Without tightness, the new I-address could fall within a half-open coverage interval reaching past existing content, in which case the projection grows by that V-position. When K.μ⁺ adds entries mapping V-positions to *existing* I-addresses (the transclusion case), the projection grows by precisely those new V-positions whose mappings fall in coverage. This is the mechanism by which a link "comes into view" in a document that newly transcludes its target content. K.μ⁺_L exhibits the same growth behaviour for link-subspace V-positions when an existing link address is admitted into a home-document arrangement.

**LP10 — Contraction under K.μ⁻**: For every K.μ⁻ transition `Σ → Σ'` operating on `d`, and every endset `e`:
```
project(e, d, Σ') ⊆ project(e, d, Σ)
```

K.μ⁻ contracts `Σ.M(d)`: `dom(Σ'.M(d)) ⊂ dom(Σ.M(d))` with agreement on the retained domain. For any `v ∈ project(e, d, Σ')`, we have `v ∈ dom(Σ'.M(d)) ⊆ dom(Σ.M(d))` and `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(e)`, so `v ∈ project(e, d, Σ)`. The projection can only shrink.

The V-positions that leave the projection are exactly the arrangement entries removed by the operation:
```
project(e, d, Σ) ∖ project(e, d, Σ') = {v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d)) : Σ.M(d)(v) ∈ coverage(e)}
```

The forward inclusion (⊆): if `v ∈ project(e, d, Σ) ∖ project(e, d, Σ')`, then `v ∈ dom(Σ.M(d))` and `Σ.M(d)(v) ∈ coverage(e)` by the first conjunct, while the second forces either `v ∉ dom(Σ'.M(d))` or `Σ'.M(d)(v) ∉ coverage(e)`. The second alternative is excluded: if `v ∈ dom(Σ'.M(d)) ⊆ dom(Σ.M(d))`, the agreement clause gives `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(e)`, contradicting `v ∉ project(e, d, Σ')`. So `v ∉ dom(Σ'.M(d))`, placing `v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d))`. The reverse inclusion (⊇): if `v ∈ dom(Σ.M(d)) ∖ dom(Σ'.M(d))` with `Σ.M(d)(v) ∈ coverage(e)`, then `v ∈ project(e, d, Σ)` directly; and `v ∉ project(e, d, Σ')` since `v ∉ dom(Σ'.M(d))`.

When deletion removes V-positions whose I-addresses are in coverage, those V-positions leave the projection. The I-addresses themselves persist in `dom(Σ.C)` by S0; they are merely no longer in `ran(Σ.M(d))`. Other documents that still arrange those I-addresses are unaffected (LP5) — the link can still be projected through them.

The "partial deletion" case follows immediately: if some but not all V-positions of a contiguous projection are removed, the remaining V-positions stay in the projection. The link survives on whatever V-positions remain. This is Nelson's "if anything is left at each end" condition made precise.

*Boundary case — empty arrangement.* K.μ⁻'s precondition admits retention `n'_S = 0` for every subspace `S`, provided the pre-state has at least one position so that the strict-shrink clause `(E S :: n'_S < n_S)` is discharged (the pre-state condition `dom(Σ.M(d)) ≠ ∅` is required by the operation regardless). When `n'_S = 0` holds for both `s_C` and `s_L`, the post-state arrangement is empty: `dom(Σ'.M(d)) = ∅`. In this case `project(e, d, Σ') = ∅` for every endset `e`, since the comprehension ranges over the empty domain; the exact-difference formula reduces to `project(e, d, Σ) ∖ ∅ = project(e, d, Σ)` — every V-position that was in the pre-state projection has departed. The lemma's inclusion `project(e, d, Σ') ⊆ project(e, d, Σ)` holds vacuously.

**LP11 — Reordering under K.μ~**: For every K.μ~ transition `Σ → Σ'` operating on `d` via the witnessing bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))`, and every endset `e`:
```
project(e, d, Σ') = π(project(e, d, Σ))
```
and
```
ran(Σ'.M(d)) = ran(Σ.M(d))
```

The K.μ~ definition (ASN-0047) gives the bijection equation `(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))`. By K.μ~-FIX, `dom(Σ'.M(d)) = dom(Σ.M(d))`, so π permutes the domain. For any `v ∈ dom(Σ.M(d))`:

```
v ∈ project(e, d, Σ)
  ⟺ Σ.M(d)(v) ∈ coverage(e)               -- definition
  ⟺ Σ'.M(d)(π(v)) ∈ coverage(e)            -- bijection equation
  ⟺ π(v) ∈ project(e, d, Σ')              -- definition (π(v) ∈ dom(Σ'.M(d)))
```

The forward inclusion `π(project(e, d, Σ)) ⊆ project(e, d, Σ')` follows directly from the biconditional. For the reverse inclusion `project(e, d, Σ') ⊆ π(project(e, d, Σ))`, any `v' ∈ project(e, d, Σ') ⊆ dom(Σ'.M(d)) = dom(Σ.M(d))` has a unique preimage `v = π⁻¹(v')` under π's bijectivity on `dom(Σ.M(d))`; the biconditional applied to `v` gives `v ∈ project(e, d, Σ)`, so `v' = π(v) ∈ π(project(e, d, Σ))`. Both inclusions combine to the equality.

So the projection's V-positions move *with* the content they reach: `project(e, d, Σ') = π(project(e, d, Σ))`. The cardinality is preserved: `|project(e, d, Σ')| = |project(e, d, Σ)|`. The set of I-addresses reached by the projection is preserved exactly: `{Σ'.M(d)(v') : v' ∈ project(e, d, Σ')} = {Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))`.

The second postcondition `ran(Σ'.M(d)) = ran(Σ.M(d))` is derived by taking images on both sides of the bijection equation. For every `v ∈ dom(Σ.M(d))`, the equation gives `Σ'.M(d)(π(v)) = Σ.M(d)(v)`. Therefore `{Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))} = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))} = ran(Σ.M(d))`. By K.μ~-FIX, `dom(Σ'.M(d)) = dom(Σ.M(d))`, so π is a bijection from `dom(Σ.M(d))` onto `dom(Σ'.M(d))`, hence `{π(v) : v ∈ dom(Σ.M(d))} = dom(Σ'.M(d))`. Substituting `v' = π(v)` and re-indexing the image set, `{Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))} = {Σ'.M(d)(v') : v' ∈ dom(Σ'.M(d))} = ran(Σ'.M(d))`. Combining the two equalities yields `ran(Σ.M(d)) = ran(Σ'.M(d))`.

The displacement under K.μ~ is therefore a *rebinding*: same I-addresses, same number of V-positions, but at new locations in V-space. A projection that was contiguous in V-order before the reordering may become fragmented after; conversely, a fragmented projection may become contiguous. The shape of the projection is a property of the current arrangement, not of the link.

## Discoverability and Survival

We are now in a position to state Nelson's survivability guarantee precisely. The vague claim "links survive editing if anything is left at each end" becomes a sharp condition on `coverage ∩ ran`.

**Definition — Discoverability**: For `a ∈ dom(Σ.L)` and `d ∈ dom(Σ.M)`, the link `a` is *discoverable from document `d`* at state `Σ` iff some slot's projection through `d` is non-empty:
```
discoverable_from(a, d, Σ)
  defined when  a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)
  ≡             (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ≠ ∅)
```

The precondition `a ∈ dom(Σ.L)` is what makes `|Σ.L(a)|` and the slot accessor `Σ.L(a).eᵢ` well-defined; the precondition `d ∈ dom(Σ.M)` is what makes `project(a, i, d, Σ)` well-defined. The link is *discoverable* at `Σ` iff there exists some document from which it is discoverable.

**LP12 — DiscoverabilityCharacterisation**: For every link `a ∈ dom(Σ.L)`, document `d ∈ dom(Σ.M)`, and state `Σ`:
```
discoverable_from(a, d, Σ) ⟺ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
```

Direct from definitions. Per-slot first: `v ∈ project(a, i, d, Σ)` requires `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`, which requires some I-address in the coverage to be in the range. Conversely, any I-address `a*` in `coverage(eᵢ) ∩ ran(Σ.M(d))` is reached by some `v ∈ dom(Σ.M(d))` with `Σ.M(d)(v) = a*`, and that `v` lies in `project(a, i, d, Σ)`. This gives the per-slot biconditional `project(a, i, d, Σ) ≠ ∅ ⟺ coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`. Lifting existentially over `i ∈ {1, …, |Σ.L(a)|}` preserves the biconditional: `(E i : project(a, i, d, Σ) ≠ ∅) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)`. Unfolding the left-hand side via the `discoverable_from` definition completes the biconditional.

The phrase "anything is left at each end" can now be stated formally: discoverability from `d` requires that, for at least one slot `i`, `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`. For mere existence of the link, nothing is required at all — this is the substantive content of the next claim.

**LP13 — UnconditionalLinkPersistence**: For every reachable state sequence `Σ →* Σ'` and every link `a ∈ dom(Σ.L)`:
```
a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)
```

The conclusion holds independently of `Σ.M`, `Σ'.M`, `dom(Σ.M)`, `dom(Σ'.M)`, and any document's range. By L12 (ASN-0043) applied step-wise along the sequence, the link's address persists and its endset sequence is byte-identical at every intermediate state. The hypothesis `a ∈ dom(Σ.L)` is the only requirement; the conclusion never consults whether `a` is discoverable from any document.

The architectural separation LP13 commits to is that *storage* and *navigability* are independently regulated. LP12 characterises when a link is discoverable (a property of `coverage ∩ ran`); LP13 says the link's stored object persists regardless (a property of `Σ.L` alone). In particular: an orphaned link (LP17, having empty coverage-range intersection in every document at `Σ'`) and a discoverable link are stored identically in `Σ'.L`; the architecture distinguishes them only at the navigability layer. The "anything is left at each end" condition characterises navigability from `d`, not the link's existence. A link holder can rely on the stored object permanently; the holder cannot rely on discoverability from any particular document without further conditions on that document's arrangement (LP9–LP11 govern how those conditions evolve).

## Discovery Independence of Origin

We have characterised discoverability *from* a particular document. Now we ask: how does this relate to which document created the link, which document allocated the linked content, and which document the holder is following the link from?

Three documents may be in play for any given link reference:
- The *home document* of the link, `home(a)` = `origin(a)` — the document under whose tumbler prefix the link's address was allocated (L1a, ASN-0093).
- The *origin document* of each I-address in coverage, `origin(a*)` — the document under whose tumbler prefix `a*` was allocated.
- The *navigating document* `d` from which the holder follows the link.

These three may be the same, all different, or any combination. The discoverability of a link from `d` depends on none of them — only on the I-address content of `d`'s arrangement. This is visible by inspection of LP12: the right-hand side references `coverage(Σ.L(a).eᵢ)` and `ran(Σ.M(d))` and nothing else. The characterisation contains no reference to `home(a)` or to the origin documents of coverage I-addresses. The home document is a metadata property of the link's address (recoverable by tumbler projection — S7 of ASN-0036), not a constraint on where the link can be reached from. Similarly, origin is a metadata property of each coverage I-address, indifferent to whether `d` was the document that allocated the address or some unrelated document that has since transcluded it. A link can therefore be discovered from any document whose arrangement currently maps to any I-address in any of the link's endsets' coverage, regardless of provenance. The system commits to indifference of provenance at the point of discovery.

The transclusion mechanism is the architectural lever that activates this provenance-indifference.

**LP16 — TransclusionDiscoverability**: For any link `a ∈ dom(Σ.L)`, slot `i ∈ {1, …, |Σ.L(a)|}`, and documents `d_src, d_new ∈ dom(Σ.M)` at state `Σ`:
```
coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d_src)) ∩ ran(Σ.M(d_new)) ≠ ∅
  ⟹  discoverable_from(a, d_src, Σ) ∧ discoverable_from(a, d_new, Σ)
```

Let `a*` be any I-address in the triple intersection: `a* ∈ coverage(Σ.L(a).eᵢ)`, `a* ∈ ran(Σ.M(d_src))`, and `a* ∈ ran(Σ.M(d_new))`. By `a* ∈ ran(Σ.M(d_src))`, there exists `v_src ∈ dom(Σ.M(d_src))` with `Σ.M(d_src)(v_src) = a*`, so `v_src ∈ project(a, i, d_src, Σ)`, hence `project(a, i, d_src, Σ) ≠ ∅`. Symmetrically `v_new ∈ project(a, i, d_new, Σ)` for some `v_new`. By the discoverable_from definition (witnessed at slot `i`), both `discoverable_from(a, d_src, Σ)` and `discoverable_from(a, d_new, Σ)` hold.

The triple intersection is exactly the condition transclusion produces: when `d_new` transcludes some content from `d_src` (via a fork composite or any K.μ⁺ that adds arrangement entries mapping V-positions to I-addresses already in `ran(Σ.M(d_src))`), the shared I-addresses are members of `ran(Σ.M(d_src)) ∩ ran(Σ.M(d_new))`. If any of these shared I-addresses also lies in `coverage(Σ.L(a).eᵢ)` for some link `a` and slot `i`, the lemma's hypothesis is met. Discoverability extends to every document that transcludes any I-address in coverage. No notification of the link is required; the link is *passively* discoverable from `d_new` simply because `d_new` arranges the I-address.

This is the architectural mechanism behind Nelson's "a link to one version is a link to all versions" claim and the cross-document discovery property: link discovery is a function of I-address intersection alone, and transclusion shares I-addresses by definition.

## Ghost Projection and Resurrection

We consider two corner cases: when nothing in the system reaches a link's coverage, and when re-introduction of content restores reachability.

**LP17 — GhostProjection**: Suppose at state `Σ` no document's arrangement reaches any I-address in `coverage(Σ.L(a).eᵢ)` for any slot `i`:
```
(A d ∈ dom(Σ.M), i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) = ∅)
```

Then by LP12, `project(a, i, d, Σ) = ∅` for every `d, i`. The link is *orphaned*: not discoverable from any document. By L12 (ASN-0043), `a` remains in `dom(Σ.L)` and `Σ.L(a)` is unchanged. The link is not destroyed; it is invisible to forward navigation, but its stored endsets continue to identify the I-addresses it once reached, and the I-addresses themselves continue to exist in `dom(Σ.C)` by S0.

**LP18 — Resurrection**: If `a` is orphaned at `Σ` and a subsequent transition sequence `Σ →* Σ'` introduces an arrangement entry `Σ'.M(d)(v) = a*` for some `d, v, a*` with `a* ∈ coverage(Σ.L(a).eᵢ)`, then `a` is discoverable from `d` at `Σ'`.

The transition sequence may include K.σ (registering a new document), K.μ⁺ or K.μ⁺_L (extending an existing arrangement, possibly via fork), or any other combination of operations that preserves the link store. The orphan premise supplies `a ∈ dom(Σ.L)`. Store Monotonicity★ applied to `Σ →* Σ'` lifts this to `a ∈ dom(Σ'.L)`, making the slot accessor `Σ'.L(a).eᵢ` well-defined at the post-state. (Equivalently, LP3★ supplies both `a ∈ dom(Σ'.L)` and the coverage equation in a single step; we cite the persistence half here to highlight the well-definedness obligation.) Because LP3★ keeps the link's coverage fixed across the entire sequence, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`, so the membership `a* ∈ coverage(Σ.L(a).eᵢ)` carries through to `a* ∈ coverage(Σ'.L(a).eᵢ)`. By the definition of `project`, `v ∈ project(a, i, d, Σ')` since `v ∈ dom(Σ'.M(d))` and `Σ'.M(d)(v) = a* ∈ coverage(Σ'.L(a).eᵢ)`. The link is resurrected.

This is the formal expression of Nelson's "reaching back through to a superseding version" mechanism. The system architecture admits resurrection because (i) the link's stored state is permanent (L12 of ASN-0043), (ii) the I-addresses it references are permanent (S0), (iii) the projection is a live computation that consults the current arrangement at the moment of query, and (iv) discovery is purely I-address-based, indifferent to provenance (LP12 references only coverage and range).

A link can pass through arbitrarily many states of orphanage and resurrection without any modification to its stored data. The link does not "know" that the content has been removed and re-introduced; it does not need to.

## Boundary and Width Behaviour

We address two further questions about the structural behaviour of projection under specific operation patterns.

We formalise the "boundary insertion does not extend the link" property by isolating the construction discipline that makes it hold. The naive formulation `coverage(e) ⊆ dom(Σ_e.C) ∪ dom(Σ_e.L)` is vacuous: by T1 case (ii) of ASN-0034, a span `(s, ℓ)` includes the zero-extension `s.0` (since `s ≺ s.0`, with `s.0 < s ⊕ ℓ` by a divergence argument at the action point `k ≤ #s` of `ℓ` where `(s.0)_k = s_k < s_k + ℓ_k = (s ⊕ ℓ)_k`), and by induction `s.0.0`, `s.0.0.0`, …; coverage is infinite while `dom(Σ_e.C) ∪ dom(Σ_e.L)` is finite (C-fin, L-fin of ASN-0093), so the containment fails for every non-empty endset. The architectural property we want is narrower: every address the substrate *could ever K.α/K.λ-emit* within the span's reach must already be allocated. Addresses like `s.0` carry a trailing zero and so violate T4-validity, which by T10a.4 (ASN-0034) excludes them from any allocator chain — their proliferation in `coverage(e)` is irrelevant to the boundary question.

By ASN-0093, every K.α/K.λ-allocated address is a chain element of some sub-allocator `A_C(d)` or `A_L(d)`, with structural form `[d, 0, s_C, k]` (resp. `[d, 0, s_L, k]`) for some T4-valid document tumbler `d` (i.e., `d ∈ T` with `zeros(d) = 2`) and some `k ≥ 1`. We do not require `d ∈ dom(Σ_e.M)` — future K.σ transitions can register additional documents whose chains then become active, and the tightness condition must guard against those too. The set of *substrate-emittable addresses* is the union of all such chain elements across all T4-valid document tumblers and both subspaces, defined formally as:
```
F = {a ∈ T : (E d ∈ T, s ∈ {s_C, s_L}, k ≥ 1 :: zeros(d) = 2 ∧ d satisfies T4 ∧ a = [d, 0, s, k])}
```
Every `a ∈ F` has `#a = #d + 3`, `zeros(a) = 3`, and `#E(a) = 2` by direct inspection of the structural form. An address outside `F` cannot be the target of any K.α/K.λ emission. In particular, the sub-allocator anchors `b_C(d) = [d, 0, s_C]` and `b_L(d) = [d, 0, s_L]` of ASN-0093 have `#E = 1` and so lie outside `F`; they are anchors of chains, not chain elements.

`F` is countably infinite. By T0(a) and T0(b) of ASN-0034, the set of T4-valid document tumblers is itself infinite (component values are unbounded and tumbler length is unbounded), and each contributes a countably infinite chain in each of the two subspaces. The universal quantifier `(A t ∈ F : s ≤ t < s ⊕ ℓ : …)` in the tightness predicate therefore ranges over an infinite domain. Nonetheless, the quantifier is decidable by structural analysis: each candidate `t ∈ F` has the determinate form `[d, 0, s, k]` for T4-valid `d`, subspace `s ∈ {s_C, s_L}`, and `k ≥ 1`, and the bounded constraint `s ≤ t < s ⊕ ℓ` reduces to a finite case split on these structural components under T1 comparison. The proofs that follow consult `F` only through structural analysis of candidate forms, never via enumeration; for any specific span `(s, ℓ)`, only those `(d, s, k)` triples whose lex position falls within the interval need be examined.

An endset `e` is *tight at state `Σ_e`* iff every span `(s, ℓ) ∈ e` satisfies:
```
s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)  ∧  (A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))
```

The first conjunct says the span starts at an allocated address; the second says every substrate-emittable address in the span's reach is already allocated. Tightness is a state-relative predicate; in the canonical use case `Σ_e` is the state at which `e` was incorporated into a link, but the predicate is well-defined at any state.

*Achievability.* The non-empty case is reached by the canonical construction: span endpoints drawn from currently-allocated content, with reach at or before the relevant chain's next emission point. For a span on `A_C(d_0)`'s chain with currently-allocated maximum at chain index `m`, choosing `s ⊕ ℓ ≤ inc(t_m^C(d_0), 0)` makes the span tight against `A_C(d_0)`'s own future emissions — chain elements with index `> m` lie at or above `inc(t_m^C(d_0), 0)` by ChainEnumerationInjectivity (ASN-0093), so none fall in `[s, s ⊕ ℓ)`. Interference from chains other than `A_C(d_0)` splits into four exhaustive cases: same-document cross-subspace (`A_L(d_0)` on `d_0` itself), and three cross-document cases parameterised by the prefix relation between `d_0` and a distinct document tumbler `d' ≠ d_0` — non-nesting (neither `d_0` nor `d'` is a prefix of the other), descendant of `d_0` (`d_0 ≺ d'`), and ancestor of `d_0` (`d' ≺ d_0`). The three cross-document cases are exhaustive on `d' ≠ d_0` because Divergence (ASN-0034) splits any pair of distinct tumblers into component-divergence (case (i), non-nesting once prefix-nesting is excluded) and prefix-divergence (case (ii), one a proper prefix of the other). The same-document case completes the partition over all sub-allocator chains other than the one the span is built on.

*Same document, cross subspace.* The span is built on `A_C(d_0)`'s chain, so `s` carries `s_C` at position `#d_0 + 2` (by the structural form `s = [d_0, 0, s_C, k_s]`). The image `s ⊕ ℓ` agrees with `s` at this position: by C0 (ASN-0058) the action point of `ℓ` is `k_ℓ = #s = #d_0 + 3`, and position `#d_0 + 2 < k_ℓ` falls in TumblerAdd's prefix-copy region, so `(s ⊕ ℓ)_{#d_0 + 2} = s_{#d_0 + 2} = s_C`. Chain elements `b` of `A_L(d_0)` have structural form `[d_0, 0, s_L, k]` (ASN-0093), so `b_{#d_0 + 2} = s_L`. Positions `1..#d_0 + 1` agree between `b`, `s`, and `s ⊕ ℓ` (all carry `d_0` followed by `0` at position `#d_0 + 1`, established by the chain structure for `b` and by prefix-copy reasoning for `s ⊕ ℓ`). By SC-NEQ (ASN-0093, `s_C ≠ s_L`, with `s_L = s_C + 1` under SubspaceConventionAxiom) and T1 case (i) at divergence position `#d_0 + 2`, `b > s ⊕ ℓ`, so `b ∉ [s, s ⊕ ℓ)`. The symmetric case — span built on `A_L(d_0)`, with interference from `A_C(d_0)` elements — runs identically with `s_C` and `s_L` exchanged at position `#d_0 + 2`, yielding `b < s` instead of `b > s ⊕ ℓ`; either way `b` lies outside `[s, s ⊕ ℓ)`.

*Non-nesting documents.* By Divergence (ASN-0034) applied to `d_0` and `d'`, case (i) applies — case (ii) would require one to be a prefix of the other, contradicting non-nesting — so there is a position `j ≤ min(#d_0, #d')` with `d_{0,j} ≠ d'_j` and `d_{0,i} = d'_i` for `1 ≤ i < j`. Chain elements `b` of `A_sub'(d')` carry `d'` as a prefix (by TA5(b) and the chain structure of ASN-0093), so `b_i = d'_i` for `1 ≤ i ≤ #d'`; in particular `b_j = d'_j` since `j ≤ #d'`. Similarly `s` carries `d_0` as a prefix, so `s_i = d_{0,i}` for `1 ≤ i ≤ #d_0`; in particular `s_j = d_{0,j}` since `j ≤ #d_0`. The image `s ⊕ ℓ` agrees with `s` at position `j`: by C0 (ASN-0058), `ℓ` has action point `k_ℓ = #s = #d_0 + 3 > j` (since `j ≤ #d_0`), so position `j` lies in TumblerAdd's prefix-copy region where `(s ⊕ ℓ)_j = s_j`. Positions `1..j-1` agree between `b` and both `s` and `s ⊕ ℓ` via the same prefix-agreement and prefix-copy facts. By T1 case (i) of ASN-0034 at the divergence position `j`, the comparison splits on the sign of `d'_j - d_{0,j}`: if `d'_j < d_{0,j}` then `b_j < s_j` and so `b < s`, placing `b` below the interval `[s, s ⊕ ℓ)`; if `d'_j > d_{0,j}` then `b_j > (s ⊕ ℓ)_j` and so `b > s ⊕ ℓ`, placing `b` above. Either way `b ∉ [s, s ⊕ ℓ)`.

*Descendant documents.* The second case is documents `d'` standing in a proper prefix relation `d_0 ≺ d'`. The argument is structural — it depends on the form `d'` must take given that `d_0 ≺ d'` and both are T4-valid documents, not on the specific K.δ operation chain by which `d'` was reached. (For context: the K.δ rules (ASN-0047) admit descendants of `d_0` via the document creation operations `k ∈ {0, 1}` — `inc(_, 1)` creates a new version extending the current document by one non-zero component, and `inc(_, 0)` advances a version's last non-zero component without introducing zeros. The `k = 2` rule is forbidden once `zeros(t) = 2` is reached, which is the case at every document tumbler. Descendants of `d_0` are therefore reachable by chains that interleave `inc(_, 0)` and `inc(_, 1)` steps starting from an initial `inc(d_0, 1)`, never by `inc(_, 2)`.) The structural property we extract is independent of the specific interleaving.

By Prefix (PrefixRelation, ASN-0034), `d_0 ≺ d'` unfolds to `#d_0 < #d'` and `d'_i = d_{0,i}` for `1 ≤ i ≤ #d_0`. Set `q := #d' - #d_0 ≥ 1` and write the extension as `d' = [d_0, x_1, x_2, …, x_q]` where `x_i := d'_{#d_0 + i}`.

*Each `x_i ≥ 1`.* By M0 (ASN-0093) applied to both documents, `d_0` and `d'` are T4-valid with `zeros(d_0) = zeros(d') = 2`. The prefix `d_0` contributes exactly two zeros to `d'` (at the two separator positions encoded by `d_0`'s field structure, both at positions `≤ #d_0`). Therefore positions `#d_0 + 1, …, #d_0 + q` of `d'` contribute zero zeros to `d'`, i.e., each `x_i ≠ 0`. T0's carrier ℕ forces `x_i ≥ 1` from `x_i ≠ 0`. (We do not need the no-adjacent-zeros conjunct of T4 here; the zero-count balance alone suffices.)

We prove by induction on `q ≥ 1` that every chain element of `A_C(d')` (resp. `A_L(d')`) for any descendant `d'` at depth `q` lies strictly above `s ⊕ ℓ`, so that `b ∉ [s, s ⊕ ℓ)`. The induction hypothesis at depth `q` is the structural form just established: every such `d'` satisfies (i) `d_{0,i} = d'_i` for `1 ≤ i ≤ #d_0`, (ii) `d'_{#d_0 + 1} = x_1 ≥ 1`, and (iii) `#d' = #d_0 + q`.

*Base case (q = 1).* A depth-1 descendant has `d' = [d_0, x_1]` with `x_1 ≥ 1` (by the structural argument above) and `#d' = #d_0 + 1`. Chain elements of `A_C(d')` therefore have form `[d_0, x_1, 0, s_C, k]` (depth `#d_0 + 4`) — they carry `d'` as a prefix by ASN-0093's chain structure. Compare with `s = [d_0, 0, s_C, k_s]` and `s ⊕ ℓ`, both of length `#s = #d_0 + 3`. At position `#d_0 + 1` the chain element has value `x_1 ≥ 1`, while `s` has value `0` and `s ⊕ ℓ` also has value `0`: positions `1..#s - 1` of `s ⊕ ℓ` lie in TumblerAdd's prefix-copy region (since the action point `k_ℓ = #s` of `ℓ` falls at the last position by C0 of ASN-0058), so `(s ⊕ ℓ)_{#d_0 + 1} = s_{#d_0 + 1} = 0`. Positions `1..#d_0` agree between the chain element and both `s` and `s ⊕ ℓ` (chain element by ASN-0093's chain structure, `s` and `s ⊕ ℓ` by their structural form and prefix-copy). By T1 case (i) at the divergence position `#d_0 + 1`, the chain element exceeds `s ⊕ ℓ`.

*Inductive step (q → q + 1).* Suppose every depth-`q` descendant satisfies the structural form, and consider a depth-`(q+1)` descendant `d''`. By the structural argument applied directly to `d''` at the outset (which only uses M0 and Prefix), `d''_i = d_{0,i}` for `1 ≤ i ≤ #d_0` and `d''_{#d_0 + 1} = x_1 ≥ 1`. Chain elements of `A_C(d'')` carry `d''` as a prefix, so positions `1..#d_0` agree with `d_0` and position `#d_0 + 1` carries value `x_1 ≥ 1`. The comparison with `s` and `s ⊕ ℓ` at position `#d_0 + 1` is identical to the base case: chain element has value `x_1 ≥ 1`, both `s` and `s ⊕ ℓ` have value `0`. T1 case (i) at position `#d_0 + 1` again yields the chain element strictly above `s ⊕ ℓ`.

The induction concludes: tightness is preserved against every descendant of `d_0` at every depth, regardless of the specific K.δ operation chain by which the descendant was constructed.

*Ancestor documents.* The third case is documents `d'` standing in a proper prefix relation `d' ≺ d_0`. As in the descendant case, the argument is structural: it depends on the form `d_0` must take given that `d' ≺ d_0` and both are T4-valid documents, not on the specific K.δ chain by which `d_0` was reached from `d'`. (For context: descendants of `d'` are reachable by interleaved `inc(_, 0)` and `inc(_, 1)` chains starting with `inc(d', 1)`, never `inc(_, 2)` once `zeros = 2` is achieved; this is symmetric to the descendant case above.)

By Prefix applied to `d' ≺ d_0`, `#d' < #d_0` and `d_{0, i} = d'_i` for `1 ≤ i ≤ #d'`. Set `r := #d_0 - #d' ≥ 1` and write `d_0 = [d', y_1, y_2, …, y_r]` where `y_i := d_{0, #d' + i}`. The zero-count balance argument (symmetric to the descendant case): `zeros(d') = zeros(d_0) = 2` by M0, the prefix `d'` contributes its two zeros to `d_0` at positions `≤ #d'`, so positions `#d' + 1, …, #d' + r` of `d_0` contribute zero zeros and each `y_i ≠ 0`, hence `y_i ≥ 1` by T0's carrier ℕ. In particular `y_1 ≥ 1` — the structural fact the proof needs.

We prove by induction on `r ≥ 1` that every chain element `b` of `A_C(d')` (resp. `A_L(d')`) lies strictly below `s`. The induction hypothesis at depth `r` is the structural form of `d_0` relative to `d'`: (i) `d_{0,i} = d'_i` for `1 ≤ i ≤ #d'`, (ii) `d_{0, #d' + 1} = y_1 ≥ 1`, and (iii) `#d_0 = #d' + r`.

*Base case (r = 1).* Then `d_0 = [d', y_1]` with `y_1 ≥ 1` (by the zero-count argument) and `#d_0 = #d' + 1`. Chain elements `b` of `A_C(d')` (resp. `A_L(d')`) have the form `[d', 0, s_C, k]` (resp. with `s_L`) for `k ≥ 1`, so `#b = #d' + 3 < #d' + 4 = #d_0 + 3 = #s`. Positions `1..#d'` agree between `b` and `s`: `b` carries `d'` as prefix by the chain structure of ASN-0093; `s` carries `d_0` as prefix and (i) gives `d_{0,i} = d'_i` for `i ≤ #d'`. At the divergence position `#d' + 1`: `b_{#d' + 1} = 0` (separator immediately after `d'`'s prefix in any chain element of `A_C(d')`), while `s_{#d' + 1} = d_{0, #d' + 1} = y_1 ≥ 1`. The image `s ⊕ ℓ` agrees with `s` at position `#d' + 1`, since `ℓ` has action point `k_ℓ = #s > #d' + 1` so this position falls in TumblerAdd's prefix-copy region. T1 case (i) at position `#d' + 1` with `b_{#d'+1} = 0 < y_1 = s_{#d'+1}` yields `b < s`.

*Inductive step (r → r + 1).* Suppose every depth-`r` ancestor satisfies the structural form. Consider an ancestor `d''` at depth `r + 1` from `d_0`, i.e., `d'' ≺ d_0` with `#d_0 - #d'' = r + 1`. Applying the same structural argument (M0 + Prefix + zero-count balance) directly to `d''` and `d_0` yields: (i) `d_{0,i} = d''_i` for `1 ≤ i ≤ #d''`, (ii) `d_{0, #d'' + 1} = z ≥ 1` for some `z`, and (iii) `#d_0 = #d'' + r + 1`. Chain elements `b''` of `A_C(d'')` have the form `[d'', 0, s_C, k]`, so `b''_{#d'' + 1} = 0` while `s_{#d'' + 1} = d_{0, #d'' + 1} = z ≥ 1`; positions `1..#d''` agree between `b''` and `s` as in the base case; `s ⊕ ℓ` agrees with `s` at position `#d'' + 1` since `k_ℓ = #s > #d'' + 1`. T1 case (i) at position `#d'' + 1` again yields `b'' < s`.

The induction concludes: tightness is preserved against every ancestor at every depth, regardless of the specific K.δ chain by which `d_0` was constructed from the ancestor.

*Worked numerical example.* Let `d` be a T4-valid document with `s_C = 1`, and write `m = #d + 3` for the common length of `A_C(d)`'s chain-element addresses (so for every span `s = [d.0.1.k_s]` rooted on this chain, `#s = m`). Suppose `A_C(d)` has emitted three chain elements at the current state `Σ_e`:
```
t_1^C(d) = [d.0.1.1],  t_2^C(d) = [d.0.1.2],  t_3^C(d) = [d.0.1.3]   — all in dom(Σ_e.C)
```
All three have length `m`. The next chain element (not yet emitted) is `t_4^C(d) = [d.0.1.4]`; subsequent elements are `t_5^C(d) = [d.0.1.5]`, and so on.

*Tight example.* Construct the endset `e = {(s, ℓ)}` with `s = [d.0.1.1]` and `ℓ = δ(3, m) = [0, 0, …, 0, 3]` of length `m` — a length-`m` ordinal displacement (OrdinalDisplacement, ASN-0034) that is zero everywhere except at the final position, which holds 3. Its action point is `m`, so `actionPoint(ℓ) = m = #s`, and by TA0 (ASN-0034) `s ⊕ ℓ ∈ T` with `#(s ⊕ ℓ) = m`; TumblerAdd's prefix-copy region preserves positions `1..m-1` of `s`, and position `m` is summed to `s_m + ℓ_m = 1 + 3 = 4`. Hence `s ⊕ ℓ = [d.0.1.4]`, and `coverage(e) = {t ∈ T : [d.0.1.1] ≤ t < [d.0.1.4]}`. The substrate-emittable addresses in `[s, s ⊕ ℓ)` are exactly `t_1^C(d), t_2^C(d), t_3^C(d)` (chain elements of `A_C(d)` with index in `{1, 2, 3}`; index `≥ 4` is excluded by the half-open upper bound `< [d.0.1.4]`, and cross-document chain elements are excluded by the cross-chain interference arguments above). All three are in `dom(Σ_e.C)`, so the tightness condition holds: `e` is tight at `Σ_e`. Now suppose a K.α transition fires next on `A_C(d)`, producing `a_new = t_4^C(d) = [d.0.1.4]`. By half-open semantics, `a_new = s ⊕ ℓ ∉ [s, s ⊕ ℓ) = coverage(e)` — LP19a holds, and any subsequent K.μ⁺ mapping a V-position to `a_new` does not extend the projection of `e` (LP19).

*Non-tight contrast.* Construct instead `e' = {(s, ℓ')}` with the same `s = [d.0.1.1]` but `ℓ' = δ(4, m) = [0, 0, …, 0, 4]` of length `m`. Then `s ⊕ ℓ' = [d.0.1.5]` (same prefix-copy reasoning, with the final summed component now `1 + 4 = 5`), and `coverage(e') = {t ∈ T : [d.0.1.1] ≤ t < [d.0.1.5]}`. The substrate-emittable addresses in this interval are `t_1^C(d), t_2^C(d), t_3^C(d), t_4^C(d)`. At `Σ_e`, `t_4^C(d) ∈ F` but `t_4^C(d) ∉ dom(Σ_e.C)` — so the tightness condition's second conjunct fails on the witness `t_4^C(d) ∈ F ∩ [s, s ⊕ ℓ')`. The endset `e'` is *not* tight at `Σ_e`. After K.α fires producing `a_new = t_4^C(d) = [d.0.1.4]`, we have `a_new ∈ [s, s ⊕ ℓ') = coverage(e')`. If a subsequent K.μ⁺ maps a V-position `v_new` to `a_new`, then `v_new` enters `project(e', d, ·)` by LP9 — boundary insertion extends the (non-tight) reach. The single integer-component difference between `ℓ = δ(3, m)` and `ℓ' = δ(4, m)` is the entire difference between tight construction and a span whose reach extends past the current emission frontier; the architecture admits both, but only the first is immune to absorbing fresh allocations.

We separate two claims: first, that fresh allocations cannot enter a tight endset's coverage; second, that the consequent K.μ⁺/K.μ⁺_L step cannot grow the projection by the resulting V-position.

**LP19a — TightFreshness**: For any endset `e` tight at `Σ_e`, any reachable state sequence `Σ_e →* Σ`, and any K.α (or K.λ) transition `Σ → Σ'` allocating a fresh address `a_new`:
```
a_new ∉ coverage(e)
```

The K.α step emits `a_new` from sub-allocator `A_C(d_alloc)` for some `d_alloc ∈ dom(Σ.M)`; symmetrically K.λ emits from `A_L(d_alloc)`. By the chain structure of ASN-0093, `a_new` is a chain element of `A_C(d_alloc)` (resp. `A_L(d_alloc)`), so `a_new ∈ F`. K.α's precondition (ASN-0093) requires `a_new ∉ dom(Σ.C) ∪ dom(Σ.L)`; K.λ's precondition requires `ℓ ∉ dom(Σ.L) ∪ dom(Σ.C)` — the same freshness condition with operand order swapped. By Store Monotonicity★ applied to `Σ_e →* Σ`, `dom(Σ.C) ⊇ dom(Σ_e.C)` and `dom(Σ.L) ⊇ dom(Σ_e.L)`. So `a_new ∉ dom(Σ_e.C) ∪ dom(Σ_e.L)`.

Suppose for contradiction `a_new ∈ coverage(e)`. Then `a_new ∈ [s, s ⊕ ℓ)` for some span `(s, ℓ) ∈ e`. The tightness condition at `Σ_e`, applied with the substrate-emittable `a_new ∈ F` lying in `[s, s ⊕ ℓ)`, yields `a_new ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)` — contradicting the freshness conclusion. Therefore `a_new ∉ coverage(e)`.

**LP19 — TightEndsetBoundaryExclusion**: For any endset `e` tight at `Σ_e`, any reachable state sequence `Σ_e →* Σ_n` whose prefix contains a K.α (or K.λ) transition allocating a fresh address `a_new`, and any K.μ⁺ (or K.μ⁺_L) transition `Σ_n → Σ_{n+1}` that extends `Σ_n.M(d)` by a mapping `(v_new, a_new)`:
```
v_new ∉ project(e, d, Σ_{n+1})
```

The K.α (or K.λ) step that allocated `a_new` lies on the prefix `Σ_e →* Σ_n`, so LP19a applied at that step yields `a_new ∉ coverage(e)`. Since `coverage(e)` is a deterministic function of `e`'s spans (per the coverage definition of ASN-0043) and `e` is a fixed endset value across the entire sequence — `coverage` consults no state component — the membership `a_new ∉ coverage(e)` carries through unchanged to `Σ_{n+1}`. The K.μ⁺ (or K.μ⁺_L) transition `Σ_n → Σ_{n+1}` adds the mapping `(v_new, a_new)`, giving `v_new ∈ dom(Σ_{n+1}.M(d))` and `Σ_{n+1}.M(d)(v_new) = a_new ∉ coverage(e)`. The projection definition then excludes `v_new` from `project(e, d, Σ_{n+1})`.

Tightness is a construction discipline, not a structural invariant the system enforces. The system permits endsets whose spans extend past the relevant sub-allocator's current emission frontier; such endsets are not tight, and an `a_new` allocated within their forward extent (a substrate-emittable address inside `[s, s ⊕ ℓ)`) would in fact enter the coverage — LP9's growth behaviour then applies. The architectural significance of LP19 is that the canonical construction — selecting span endpoints among I-addresses resident at construction time, with reach at or before the chain's next emission point — produces tight endsets, and tight endsets are immune to absorbing addresses produced by subsequent K.α or K.λ. Boundary insertion as a composite (K.α + K.μ⁺) cannot enlarge a tight link's reach.

**LP20 — RangeConfinement**: For every endset `e`, document `d`, state `Σ`:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))
```

The equality follows directly from the projection definition. Unfold:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)}
  = {Σ.M(d)(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) ∈ coverage(e)}
  = {a : a ∈ ran(Σ.M(d)) ∧ a ∈ coverage(e)}
  = coverage(e) ∩ ran(Σ.M(d))
```
The first step is the definition of `project`; the second renames `a = Σ.M(d)(v)` and observes that the image set equals `ran(Σ.M(d))` filtered by coverage membership; the third is set intersection.

*Corollary (store-confinement form).* Composing the equality with S3★ (GeneralizedReferentialIntegrity, ASN-0047) yields the weaker inclusion:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} ⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))
```

Split by V-position subspace, the corollary refines to:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C} ⊆ coverage(e) ∩ dom(Σ.C)
{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L} ⊆ coverage(e) ∩ dom(Σ.L)
```

The corollary's per-subspace argument draws two facts from ASN-0047. S3★-aux (SubspaceExhaustiveness) discharges exhaustiveness — every `v ∈ dom(Σ.M(d))` satisfies `subspace(v) ∈ {s_C, s_L}`, so no V-position escapes the two-case analysis. S3★ (GeneralizedReferentialIntegrity) supplies the per-subspace targets: for content-subspace V-positions, `Σ.M(d)(v) ∈ dom(Σ.C)`; for link-subspace V-positions, `Σ.M(d)(v) ∈ dom(Σ.L)`. Either way, the V-positions in the projection always correspond to I-addresses that have been allocated. The projection cannot "see" hypothetical future addresses; the equality is the precise statement of what is reached, and the inclusion records what store the reached addresses inhabit.

**LP21 — RepresentationInvariance**: For any two endsets `e₁, e₂` with `coverage(e₁) = coverage(e₂)`:
```
project(e₁, d, Σ) = project(e₂, d, Σ)
```

The projection depends only on coverage, not on the span decomposition of the endset. Two endsets with the same coverage are interchangeable for projection purposes. This is a direct corollary of the definition: the set comprehension references `coverage(e)`, not the spans within `e`.

## What the Link Holder Can Rely On

We have established a catalogue of guarantees. We now consolidate them into a holder-facing summary.

The holder owns the link `a` and possesses, at minimum, knowledge of its address and the endsets at each slot. Across any state evolution `Σ →* Σ'`:

- The address `a` remains in `dom(Σ'.L)` (Store Monotonicity★).
- The endsets `Σ'.L(a).eᵢ` are byte-identical to `Σ.L(a).eᵢ` for every slot (LP2★).
- The slot ordering is preserved — what was at slot 1 is still at slot 1, the type endset is still at slot 3 (LP2★).
- The coverage of each endset is fixed — `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` (LP3★).
- The I-addresses in coverage all remain in `dom(Σ'.C)` if they were ever in `dom(Σ.C)` (Store Monotonicity★), with their content values unchanged (S0, applied step-wise across the sequence).

What can vary:

- Which documents the link can be discovered from. This depends on which documents currently arrange any I-address in any endset's coverage (LP12). Documents may transclude the linked content (gaining discoverability — LP9, LP16), or delete it (losing discoverability — LP10), at any time.
- The specific V-positions of any projection. These reflect the document's current arrangement and shift as the document is edited (LP9, LP10, LP11).
- The shape of any projection — contiguous, fragmented, partial — depends on the arrangement, not on the link.

What is *not* possible:

- The link cannot have its endsets rewritten (L12, ASN-0043).
- The link cannot have its slots permuted (LP2).
- The link cannot have its coverage altered by any external party (LP3).
- The link cannot be made un-discoverable while there exists any document arranging any I-address in any of its endsets' coverage (LP12).
- The link cannot be discovered from a document with no arrangement entry mapping to any I-address in coverage (LP12, contrapositive).
- The link's discoverability cannot be made to depend on which document created it or which document allocated its linked content (LP12 references only coverage and range, indifferent to provenance).
- Boundary insertion of newly allocated content into a tightly constructed link's reach cannot grow that reach (LP19).

The trust relationship between the link holder and the system is asymmetric. The system commits unconditionally to LP2, LP3, and S0 (together with L12 of ASN-0043) — to the permanence of every stored object. The system commits conditionally to LP9–LP18 — to the discoverability of the link, contingent on what the document holders choose to do with their arrangements. The holder cannot prevent another document holder from deleting the linked content from their own arrangement (subject to their own ownership rules). The holder can rely on the content persisting somewhere in `dom(Σ.C)` permanently, but cannot rely on it persisting in any particular `ran(Σ.M(d))` indefinitely. Survival of discoverability requires only that *somewhere* in the system, *some* document still arranges *some* of the linked content. This is the strongest guarantee the architecture provides, and it is sufficient for the holder's purpose: the link's content can be re-introduced via transclusion at any time, and the link will then be re-projected at the new V-positions automatically and without any action by the holder.

## A Worked Trace

To make the displacement concrete, we trace a small example. Consider:

- A link `a` with endset `e₁ = {(i₀, ℓ)}`. By T12 (ASN-0034), `coverage(e₁) = {t ∈ T : i₀ ≤ t < i₀ ⊕ ℓ}` — the entire half-open interval, not merely a discrete set. The I-addresses `i₁, i₂, i₃, i₄` satisfy `i₀ ≤ i₁ < i₂ < i₃ < i₄ < i₀ ⊕ ℓ` and `i₁, …, i₄ ∈ dom(Σ.C)`; the interval `coverage(e₁)` contains these four addresses (along with any other tumbler lying in the interval). For trace clarity we follow only these four, since they are precisely the addresses in `coverage(e₁) ∩ ran(Σ.M(d₁))` for the document considered below — and by LP12 the projection through `d₁` is governed by that intersection, not by the full coverage.
- A document `d₁` whose content subspace arranges these four I-addresses in order: `Σ.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₃ ↦ i₃, v₄ ↦ i₄}`, with `v_k = [s_C, 1, …, 1, k]` so the sequence `(v₁, v₂, v₃, v₄)` satisfies D-SEQ★ at content-subspace count `n_{s_C} = 4`.

At state `Σ`:
```
project(a, 1, d₁, Σ) = {v₁, v₂, v₃, v₄}
```

Apply K.μ⁻ retaining the first three content-subspace positions (so `n'_{s_C} = 3`), producing state `Σ_1`:
```
Σ_1.M(d₁) = {v₁ ↦ i₁, v₂ ↦ i₂, v₃ ↦ i₃}
project(a, 1, d₁, Σ_1) = {v₁, v₂, v₃}
```

The projection has shrunk by `{v₄}` (per LP10's exact characterisation), and the retained set `{v₁, v₂, v₃}` is the D-SEQ★-admissible prefix permitted by K.μ⁻. The I-address `i₄` is still in `dom(Σ.C)` by S0, but no longer in `ran(Σ_1.M(d₁))`. The link's coverage is unchanged — still the half-open interval `{t ∈ T : i₀ ≤ t < i₀ ⊕ ℓ}`, of which `{i₁, i₂, i₃, i₄}` remain the traced members.

Now suppose another document `d₂` is registered and transcludes `i₄` via K.σ followed by K.μ⁺, producing state `Σ_2`:
```
Σ_2.M(d₂) = {w₁ ↦ i₄}
project(a, 1, d₂, Σ_2) = {w₁}
```

The link is now discoverable from both `d₁` (where the projection is `{v₁, v₂, v₃}` reaching `{i₁, i₂, i₃}`) and `d₂` (where the projection is `{w₁}` reaching `{i₄}`). Together the two projections reach the four traced I-addresses `{i₁, i₂, i₃, i₄}` — the entirety of `coverage(e₁)` that bears on these documents' ranges — despite no single document containing all four.

*Branch point — alternative continuation from `Σ_1`.* The next step does *not* follow `Σ_2`. We return to `Σ_1` (the post-K.μ⁻ state, before any `d₂` registration) and explore a separate continuation that isolates K.μ~ behaviour. In this branch, `d₂` is never introduced; `dom(Σ_1.M)` retains its pre-`Σ_2` membership. We rename the post-K.μ~ state `Σ_3` to flag that it is a sibling of `Σ_2` under `Σ_1`, not a successor of `Σ_2`.

To exhibit projection motion clearly under K.μ~, consider slot 2 of the link, with endset `e₂` chosen so that `coverage(e₂) ∩ ran(Σ_1.M(d₁)) = {i₁}` — only the I-address `i₁` from `d₁`'s current range lies in this slot's coverage (admissible by L4 of ASN-0043, which imposes no constraint on which I-addresses an endset references; for trace clarity we follow only the intersection with `d₁`'s range, since by LP12 that intersection is what governs projection through `d₁`). At `Σ_1`:
```
project(a, 2, d₁, Σ_1) = {v₁}
```
— a strict subset of `dom(Σ_1.M(d₁)) = {v₁, v₂, v₃}`, because among the V-positions of `Σ_1.M(d₁)` only `v₁` maps to an I-address in `coverage(e₂)`.

Now (still in this alternative branch from `Σ_1`) apply K.μ~ to `d₁` via a bijection `π` that permutes the V-positions, fixing `dom(Σ_1.M(d₁))` setwise (per K.μ~-FIX of ASN-0047). The K.μ~ operates on the `Σ_1`-state arrangement directly, so the references to `Σ_1.M(d₁)` on both sides of the bijection equation point to the same source state:
```
π(v₁) = v₃, π(v₂) = v₂, π(v₃) = v₁
Σ_3.M(d₁) = {v₃ ↦ i₁, v₂ ↦ i₂, v₁ ↦ i₃}
project(a, 1, d₁, Σ_3) = {v₃, v₂, v₁} = π(project(a, 1, d₁, Σ_1))
project(a, 2, d₁, Σ_3) = {v₃} = π({v₁}) = π(project(a, 2, d₁, Σ_1))
```

The slot-2 projection moves: it was `{v₁}` at `Σ_1`, it is `{v₃}` at `Σ_3`. The I-address `i₁` is now carried at V-position `v₃` rather than `v₁` — the projection followed its content from `v₁` to `π(v₁) = v₃`. The slot-1 projection set looks unchanged ({v₁, v₂, v₃} as a set) only because it happens to coincide with the entire domain; per-V-position, the binding has shifted (v₁ now carries i₃ rather than i₁, etc.).

Per LP11, both projections' V-positions are permuted by `π`, and the set of I-addresses reached is unchanged within each slot. The link "followed its content" through the reordering.

At no point during either branch of this trace did the link itself change. The link's address, endsets, coverage, and slot ordering remained byte-identical from `Σ` through `Σ_2` (the transclusion branch) and from `Σ` through `Σ_3` (the reordering branch). What displaced was the projection, and the displacement was entirely a function of the operations applied to the documents' arrangements.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| LP2 | `(A Σ → Σ', a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| : Σ'.L(a).eᵢ = Σ.L(a).eᵢ)` — slot invariance | introduced |
| LP2★ | Multi-step slot invariance: for `Σ →* Σ'`, `a ∈ dom(Σ.L)`, slot `i`, `a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ` | introduced |
| LP3 | `(A Σ → Σ', a, i : a ∈ dom(Σ.L) : coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))` — coverage invariance | introduced |
| LP3★ | Multi-step coverage invariance: for `Σ →* Σ'`, `a ∈ dom(Σ.L)`, slot `i`, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` | introduced |
| Store Monotonicity★ | `Σ →* Σ' ⟹ dom(Σ.C) ⊆ dom(Σ'.C) ∧ dom(Σ.L) ⊆ dom(Σ'.L)` | introduced |
| project | `project(e, d, Σ) ≡ {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}` (defined when `d ∈ dom(Σ.M)`) — the live projection function | introduced |
| LP4 | `Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)` — arrangement specificity | introduced |
| LP5 | Cross-document independence: projection through `d` unaffected by edits to `d' ≠ d` (frames over K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) | introduced |
| LP6 | K.α (content allocation) does not displace any projection | introduced |
| LP7 | K.λ (link allocation) does not displace existing projections | introduced |
| LP8 | K.σ (document registration): (a) `(A d ∈ dom(Σ.M) : project(e, d, Σ') = project(e, d, Σ))`; (b) `project(e, d_new, Σ') = ∅` | introduced |
| LP14 | K.ρ (provenance recording) does not displace any projection | introduced |
| LP9 | K.μ⁺ and K.μ⁺_L can only enlarge projection; new V-positions come from new arrangement entries | introduced |
| LP10 | K.μ⁻ can only shrink projection; lost V-positions come from removed arrangement entries | introduced |
| LP11 | K.μ~ rebinds projection: `project(e, d, Σ') = π(project(e, d, Σ))` via bijection π | introduced |
| discoverable_from | `discoverable_from(a, d, Σ) ≡ (E i : project(a, i, d, Σ) ≠ ∅)` (defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`) | introduced |
| LP12 | `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)` | introduced |
| LP13 | Unconditional link persistence: `Σ →* Σ' ∧ a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)` — independent of any discoverability | introduced |
| LP16 | Transclusion confers discoverability: shared I-addresses transfer discoverability across documents | introduced |
| LP17 | Ghost projection: orphaned links persist in `dom(Σ.L)` with empty projections everywhere | introduced |
| LP18 | Resurrection: re-introducing a coverage I-address via K.μ⁺ or K.μ⁺_L restores discoverability | introduced |
| tight | `tight(e, Σ_e)` ≡ for every span `(s, ℓ) ∈ e`, `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)` and every substrate-emittable address in `[s, s ⊕ ℓ)` is allocated at `Σ_e` | introduced |
| LP19a | Tight freshness: under tight construction, K.α/K.λ-allocated addresses fall outside `coverage(e)` | introduced |
| LP19 | Tight endset boundary exclusion: K.μ⁺/K.μ⁺_L mapping to such an address cannot grow `project(e, d, ·)` | introduced |
| LP20 | Range confinement: `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))`; corollary via S3★ gives `⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))` | introduced |
| LP21 | Representation invariance: equal coverage implies equal projection | introduced |

*Numbering note.* Labels LP1, LP15 are deliberately absent. LP14 and LP15 from earlier drafts of this ASN were collapsed in revision; LP14 has been reclaimed here to label the K.ρ frame lemma added in this revision. LP1 was never assigned. LP19a is introduced in this revision to separate the tight-freshness claim from its projection consequence (LP19); both labels are introduced here. Other labels (LP2 through LP21, omitting LP15) preserve their revision-history identities.

## Open Questions

What invariants must a reverse-discovery primitive preserve when, given a V-position in some document, it returns the set of links whose projections contain that V-position?

Under what conditions must the projection of an endset through a document be expressible as a finite union of contiguous V-ranges, given that K.μ~ can scatter formerly contiguous projections into arbitrary subsets of the V-domain?

What guarantees must the system provide about the *V-order* of positions within a single projection — does the V-order of projected positions reflect the I-order of their underlying I-addresses, and under what arrangement-shape conditions is this reflection preserved by K.μ~?

What invariants must the system maintain when a link's endset references the address of another link (rather than content) — under what conditions must the discovery of one link induce the discovery of the other?

Under what conditions must the system commit to producing identical projections for two documents that have undergone "the same" sequence of editing operations, given that arrangement state is per-document and operations are not directly comparable across documents?

What invariants must hold across a fork composite when the source document's link-subspace V-positions are not transcluded into the new document — how does this affect the projection of the source document's home-document-allocated links through the new document?
