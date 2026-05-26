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

*Working reference frame.* This ASN operates in the ASN-0047 transition-model frame layered over the ASN-0093 allocation substrate. The layered frame supplies the full operation vocabulary the projection responds to — K.σ (ASN-0093) together with K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.δ, K.ρ (ASN-0047) — together with the extended-state invariants S3★ (GeneralizedReferentialIntegrity), S3★-aux (SubspaceExhaustiveness), CL-OWN, CL-UNIQ, and the per-subspace amendments D-CTG★, D-MIN★, D-SEQ★. The projection function defined in the next section consults only `coverage(e)` and `Σ.M(d)`; whenever an operation's frame holds `Σ.M(d)` constant, projection invariance follows by LP4. In sub-frames that lack link-subspace machinery — pre-extension states where no K.μ⁺_L can fire and `S3` (ASN-0036) suffices in place of S3★ — the projection function, LP4, and the per-document frame lemmas LP5–LP8 hold structurally identically; the ASN-0036 base frame is a strict subset of the ASN-0047 operation vocabulary. Two claims require the link-subspace machinery and do not survive descent to the ASN-0036 base frame intact: LP9's K.μ⁺_L sub-case (the operation itself is absent there), and LP20's per-subspace corollary refinement (which splits the range by S3★'s two-target clause, strictly stronger than S3's single-target content-subspace clause). The discussion below cites operations and invariants from the ASN-0047 + ASN-0093 frame and flags the two link-subspace-specific points at their use sites.

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

Three degenerate configurations follow directly from the definition and require no separate treatment in subsequent claims. The projection of the empty endset is uniformly empty: `project(∅, d, Σ) = ∅` for every `d ∈ dom(Σ.M), Σ` (i.e., wherever `project` is defined), since `coverage(∅)` is the empty union over an empty index set. The projection through an empty arrangement is uniformly empty: `project(e, d, Σ) = ∅` for every `d ∈ dom(Σ.M), Σ` with `dom(Σ.M(d)) = ∅`, since the set comprehension ranges over the empty domain. A link with empty from/to endsets but a non-empty type endset (admitted by L3 of ASN-0043, which requires only the type slot to be non-empty) has empty projections at slots 1 and 2 regardless of any document's state; only the type slot's projection can be non-empty.

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

**LP4 — ArrangementSpecificity**: For every transition `Σ → Σ'`, every endset `e`, and every document `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`:
```
Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)
```

The projection function depends on exactly two inputs: `coverage(e)` and `Σ.M(d)`. The first is a pure function of the endset `e`, which appears unchanged on both sides of the equality — `coverage(e)` is therefore identical between the two projections. The second is the arrangement, equal by hypothesis. Both inputs agree pointwise, so the set comprehension produces identical results. The projection cannot displace without `Σ.M(d)` displacing.

*Frame note.* LP4 quantifies `d` over `dom(Σ.M) ∩ dom(Σ'.M)` so that both sides of the hypothesis `Σ'.M(d) = Σ.M(d)` and both sides of the conclusion `project(e, d, Σ') = project(e, d, Σ)` are well-defined under the same membership obligation. The downstream applications below (LP5, LP6, LP7, LP8, LP14, etc.) all instantiate `d ∈ dom(Σ.M)` and rely on M1 (ASN-0093) — `dom(Σ.M) ⊆ dom(Σ'.M)` for every transition in the considered vocabulary — to lift this to `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`. The monotonicity M1 is therefore a load-bearing premise of LP4's downstream uses; should a future reference frame admit transitions that remove documents from `dom(M)`, LP4's intersection form remains correct as stated, but the LP5–LP8 corollaries below would need re-derivation against the changed frame.

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

**LP8 — Document-Registration Invariance**: For any document-registration transition `Σ → Σ'` — either K.σ (ASN-0093) or K.δ in the IsDocument case (ASN-0047) — registering a fresh document `d_new` (with `d_new ∉ dom(Σ.M)`, `dom(Σ'.M) = dom(Σ.M) ∪ {d_new}`, `Σ'.M(d_new) = ∅`, and `Σ'.M(d) = Σ.M(d)` for every `d ∈ dom(Σ.M)`) and any endset `e`, both:

(a) Pre-state preservation: `(A d ∈ dom(Σ.M) :: project(e, d, Σ') = project(e, d, Σ))`.

(b) Newly-registered emptiness: `project(e, d_new, Σ') = ∅`.

Both K.σ (ASN-0093) and K.δ-IsDocument (ASN-0047) satisfy the document-registration form named in the hypothesis: both extend `dom(M)` by one fresh document, initialise the new document's arrangement to `∅`, and preserve every pre-existing arrangement pointwise. Their effects on the `Σ.M` component are structurally identical for the purposes of projection. The two operations are therefore covered by a single claim under the hypothesis above, without requiring a separate displacement claim per operation.

Postcondition (a) follows by LP4 applied to each `d ∈ dom(Σ.M)`: the document-registration frame holds `Σ'.M(d) = Σ.M(d)` for every such `d`. Postcondition (b) follows from the definition of `project`: with `d_new ∈ dom(Σ'.M)` (so the projection is defined) and `dom(Σ'.M(d_new)) = ∅`, the set comprehension `{v ∈ dom(Σ'.M(d_new)) : Σ'.M(d_new)(v) ∈ coverage(e)}` ranges over the empty domain and is empty. Both postconditions are commitments — LP18 (resurrection) requires the well-defined empty projection through a newly-registered document until a K.μ⁺ or K.μ⁺_L fires; (a) and (b) together establish that no displacement occurs at registration time, neither at pre-existing documents nor at the new one.

*Remark on K.δ.* ASN-0047 includes K.δ as a unified entity-creation operation spanning nodes, accounts, and documents. The K.δ-IsNode and K.δ-IsAccount cases have frame `(A d :: M'(d) = M(d))` — no arrangement is modified — so LP4 applied to every `d ∈ dom(Σ.M) = dom(Σ'.M)` yields projection invariance. The K.δ-IsDocument case is covered directly by LP8 above, whose hypothesis explicitly admits both K.σ and K.δ-IsDocument as document-registration operations. Each K.δ kind therefore reduces to either LP4 or LP8, and no separate displacement claim is required.

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

*K.μ⁺_L's additional constraints leave (E1) and (E2) intact.* K.μ⁺_L imposes three constraints absent from K.μ⁺: (a) the target `ℓ` is a link address that must satisfy `ℓ ∉ ran(Σ.M(d))` (first-arrangement), (b) the new V-position has fixed depth `m_L = 2` (LinkVPositionDepthAxiom of ASN-0047), and (c) the new V-position is link-subspace (`subspace(v_ℓ) = s_L`) rather than content-subspace. Each constraint *restricts* the set of admissible extensions but does not alter the structural form of any extension that is admitted.

K.μ⁺_L's effect clause (ASN-0047) asserts `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {v_ℓ} ⊃ dom(Σ.M(d))` — strict containment is part of the effect clause as stated by ASN-0047, so (E1) follows directly. The agreement clause `(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))` follows from the same effect clause `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`: the operation adds a new mapping at `v_ℓ` without disturbing existing entries, so (E2) holds. The constraints (a)–(c) affect which `ℓ` and which `v_ℓ` may appear in any specific K.μ⁺_L event, but they do not modify the way `Σ'.M(d)` relates to `Σ.M(d)` on the prior domain or how the domain grows. LP9's argument consumes only (E1) and (E2); it is invariant under these constraint-level differences. (The per-subspace dependence of D-CTG★/D-MIN★ in ASN-0047 governs *which* V-positions K.μ⁺_L may select — placing the new link-subspace V-position contiguously after the current `V_{s_L}(d)` maximum, or at its minimum if the subspace is empty — but does not affect the structural form of (E1)/(E2).)

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

**LP-Comp — CompositeDisplacement**: Every reachable sequence `Σ →* Σ'` decomposes into a finite chain of atomic transitions `Σ = Σ_0 → Σ_1 → ... → Σ_n = Σ'`, each governed by exactly one of LP4–LP14 according to its operation kind. For every endset `e` and every document `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`, the projection `project(e, d, ·)` evolves stepwise: at each `Σ_i → Σ_{i+1}`, projection displacement is given by LP4 (when `Σ_{i+1}.M(d) = Σ_i.M(d)`), LP5–LP8 (frame transitions on `d`), LP9 (extension), LP10 (contraction), LP11 (reordering), or LP14 (K.ρ frame). By induction on chain length, cumulative displacement is the composition of these per-step displacements: a chain of K.μ⁺/K.μ⁺_L instances yields cumulative projection growth by transitive containment of the per-step inclusions of LP9; a chain of K.μ⁻ instances yields cumulative shrinkage by transitive containment of the per-step inclusions of LP10; a chain of K.μ~ instances yields a cumulative bijection by composition in `Sym(dom(Σ.M(d)))` of the per-step witnessing bijections of LP11 when K.μ~-FIX holds at each step; and all other operations contribute identity at each occurrence. The base case is the empty chain (`Σ = Σ'`), under which the projection is trivially unchanged. Multi-step claims that quantify over reachable sequences — LP18 (resurrection), LP19 (tight boundary exclusion across `Σ_e →* Σ_n`) — discharge their conclusions through this composition principle: state-invariant facts (LP3★ coverage, LP19a freshness on a single allocation step) propagate through without re-application of intermediate per-step lemmas, while the per-step lemmas themselves cover any projection movement that does occur between named states.

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

LP12 characterises discoverability at a fixed state. The matching question for *displacement* is: given a particular editing operation, what must already hold at the pre-state for discoverability to survive into the post-state? K.μ⁻ is the only K.μ family member that can *destroy* discoverability (K.μ⁺ and K.μ⁺_L can only enlarge projections by LP9; K.μ~ rebinds without altering the I-addresses reached by LP11), so it is the natural site for a weakest-precondition derivation. We compute wp explicitly.

**LP12a — ContractionDiscoverabilityWP**: Fix a K.μ⁻ operation on document `d ∈ dom(Σ.M)` with retention parameters `(n'_{s_C}, n'_{s_L})` admissible under K.μ⁻'s precondition, and let
```
R := ⋃ {[S, 1, ..., 1, k] : S ∈ {s_C, s_L} ∧ 1 ≤ k ≤ n'_S}
```
denote the resulting retention set — determined by the parameters and the per-subspace V-position depths, fixed before the transition fires. For every link `a ∈ dom(Σ.L)`, the weakest precondition on the pre-state `Σ` under which `discoverable_from(a, d, Σ')` holds in the post-state `Σ' = K.μ⁻[d, R](Σ)` is:
```
wp(K.μ⁻[d, R], discoverable_from(a, d, ·))
  ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ) ∩ R ≠ ∅)
```

Derivation. We work backward from the postcondition. By the discoverable_from definition applied at `Σ'`, and using LP2 (which fixes both `a ∈ dom(Σ'.L)` and `|Σ'.L(a)| = |Σ.L(a)|`) to keep the slot index range stable:
```
discoverable_from(a, d, Σ')
  ⟺ (E i : 1 ≤ i ≤ |Σ.L(a)| : project(a, i, d, Σ') ≠ ∅)
```

We reduce `project(a, i, d, Σ')` to a predicate on the pre-state. K.μ⁻'s effect (ASN-0047) gives `dom(Σ'.M(d)) = R` with agreement `Σ'.M(d)(v) = Σ.M(d)(v)` for every `v ∈ R`. LP10's exact-difference formula, applied to the endset `Σ.L(a).eᵢ` (with `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` by LP2 so the coverage is unchanged), yields:
```
project(a, i, d, Σ) ∖ project(a, i, d, Σ') = {v ∈ dom(Σ.M(d)) ∖ R : Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)}
```
Since `project(a, i, d, Σ) ⊆ dom(Σ.M(d))` by the projection definition, the difference is precisely the subset of the pre-state projection that fell outside `R`. The complement within the pre-state projection — `project(a, i, d, Σ) ∩ R` — is exactly the post-state projection: for `v ∈ project(a, i, d, Σ) ∩ R`, the agreement clause gives `Σ'.M(d)(v) = Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)` with `v ∈ dom(Σ'.M(d))`, so `v ∈ project(a, i, d, Σ')`; conversely, every `v ∈ project(a, i, d, Σ')` satisfies `v ∈ R ⊆ dom(Σ.M(d))` and `Σ.M(d)(v) = Σ'.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`, so `v ∈ project(a, i, d, Σ) ∩ R`. Hence:
```
project(a, i, d, Σ') = project(a, i, d, Σ) ∩ R
```
The per-slot non-emptiness biconditional `project(a, i, d, Σ') ≠ ∅ ⟺ project(a, i, d, Σ) ∩ R ≠ ∅` then lifts existentially over slots — preserving the biconditional because the slot range is unchanged — to produce the wp statement.

Equivalently, via LP12's coverage-range characterisation applied to `Σ'`, and using LP3's coverage equation `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`:
```
discoverable_from(a, d, Σ')
  ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ {Σ.M(d)(v) : v ∈ R} ≠ ∅)
```
where `ran(Σ'.M(d)) = {Σ.M(d)(v) : v ∈ R}` by the K.μ⁻ agreement clause. This is the same wp predicate expressed by intersecting coverage with the V-restricted range, rather than the projection with `R` — the two forms are interchangeable.

*Boundary case — empty retention.* K.μ⁻ admits maximal contraction with `n'_{s_C} = n'_{s_L} = 0`, producing `R = ∅`, provided the pre-state has at least one position so that the strict-shrink clause `(E S :: n'_S < n_S)` is discharged. At `R = ∅` the wp specialises:
```
(E i : project(a, i, d, Σ) ∩ ∅ ≠ ∅) ≡ (E i : ∅ ≠ ∅) ≡ false
```
The wp evaluates to false unconditionally — no pre-state projection, however large, can render discoverability preservable when the entire arrangement of `d` is deleted. The link `a` itself persists by LP13, but discoverability from this specific document is unrecoverable until a subsequent K.μ⁺ or K.μ⁺_L re-introduces a coverage I-address (LP18, resurrection). This boundary case isolates the precise sense in which storage and discoverability are independently regulated: storage cannot be undone by any contraction, but discoverability from a specific document can be — by exhaustive deletion of that document's arrangement.

*Second boundary case — content-subspace empty, link-subspace retained.* When `n'_{s_C} = 0` but `n'_{s_L} > 0`, the retention set reduces to `R = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n'_{s_L}} ⊆ V_{s_L}(d)` — only link-subspace V-positions are retained. For any link whose endsets are canonically constructed in the content subspace, the wp also evaluates to false on this retention pattern. The argument requires structural machinery (the set `F` of substrate-emittable addresses and its interval characterisation via LP-Fin Corollary) developed in the "Boundary and Width Behaviour" section below; we defer the derivation to LP12b — ContentCanonicalLinkSubspaceWPFalse — stated immediately after LP-Fin Corollary in that section. The case exhibits the wp's *per-subspace sensitivity*: the retention set's subspace partition — not merely its total cardinality — determines whether the wp is satisfiable for a given link.

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
Every `a ∈ F` has `#a = #d + 3`, `zeros(a) = 3`, and `#E(a) = 2` by direct inspection of the structural form. Moreover, every `a ∈ F` satisfies T4 (HierarchicalParsing, ASN-0034) — we discharge each of T4's four conjuncts: (i) `zeros(a) ≤ 3` from the zero count just established (the two zeros of `d` plus the separator zero introduced at position `#d + 1`, with `s ∈ {s_C, s_L}` and `k ≥ 1` contributing no further zeros); (ii) no adjacent zero components — `d`'s two internal zeros are non-adjacent by `d`'s T4-validity, the last component of `d` is non-zero by `d`'s T4 endpoint clause, the separator zero at position `#d + 1` is preceded by this non-zero `d`-tail and followed by `s ∈ {s_C, s_L} ≥ 1`, so no zero-pair arises at the join; (iii) `a_1 = d_1 ≠ 0` from `d`'s T4 leading-component clause; (iv) `a_{#a} = k ≥ 1 ≠ 0` from the chain-index constraint. Equivalently, T4-validity of `a` follows directly from ChainElementT4Validity (ASN-0093) applied to any sub-allocator chain that would emit `a`. An address outside `F` cannot be the target of any K.α/K.λ emission. In particular, the sub-allocator anchors `b_C(d) = [d, 0, s_C]` and `b_L(d) = [d, 0, s_L]` of ASN-0093 have `#E = 1` and so lie outside `F`; they are anchors of chains, not chain elements.

`F` is countably infinite. By T0(a) and T0(b) of ASN-0034, the set of T4-valid document tumblers is itself infinite (component values are unbounded and tumbler length is unbounded), and each contributes a countably infinite chain in each of the two subspaces. The universal quantifier `(A t ∈ F : s ≤ t < s ⊕ ℓ : …)` in the tightness predicate therefore ranges over an infinite domain. Decidability of this quantifier rests on a finitude lemma about the interval's interaction with `F`'s structural form — *a finitude that holds for canonical spans (`#ℓ = #s`) but fails for non-canonical spans*, as the proof below establishes. The canonical restriction is therefore load-bearing both for LP-Fin and for the well-definedness of the tightness predicate stated below.

**LP-Fin — IntervalFinitude for Canonical Spans**: For every *canonical* span `(s, ℓ)` — meaning `s ∈ F` (so `s = [d_0, 0, s', k_s]` for some T4-valid `d_0` with `zeros(d_0) = 2`, subspace `s' ∈ {s_C, s_L}`, chain index `k_s ≥ 1`) and `ℓ = δ(n, #s)` for some `n ≥ 1` (equivalently `#ℓ = #s` with `ℓ` an ordinal displacement, OrdinalDisplacement of ASN-0034) — the set `F ∩ [s, s ⊕ ℓ)` is finite.

Compute `s ⊕ ℓ` first. By OrdinalDisplacement (ASN-0034), `actionPoint(ℓ) = #s = #d_0 + 3`. By TumblerAdd's piecewise rule (ASN-0034), positions `1..#s - 1` of `s ⊕ ℓ` are prefix-copied from `s` and position `#s` becomes `s_{#s} + ℓ_{#s} = k_s + n`. Hence `s ⊕ ℓ = [d_0, 0, s', k_s + n]` with `#(s ⊕ ℓ) = #s = #d_0 + 3`.

Let `a = [d, 0, s'', k] ∈ F ∩ [s, s ⊕ ℓ)`; then `#a = #d + 3`. The argument shows `#d ≤ #d_0`, after which finiteness is immediate.

*Suppose `#d > #d_0`.* Examine the relation of `d` to `d_0` on positions `1..#d_0`. Two sub-cases.

(i) `d_0 ≼ d` — positions `1..#d_0` of `a` (which are the first `#d_0` components of `d`) agree with `d_0`. Position `#d_0 + 1` of `a` is `d_{#d_0 + 1}` — well-defined since `#d > #d_0`. The constraint `zeros(d) = 2 = zeros(d_0)` combined with `d_0 ≼ d` forces every position of `d` strictly beyond `#d_0` to be non-zero: `d_0` already contributes both of `d`'s permitted zeros at positions `≤ #d_0`. By T0's carrier ℕ, `d_{#d_0 + 1} ≥ 1`. Position `#d_0 + 1` of `s ⊕ ℓ` is `0` — the separator in `s`'s structural form, preserved by TumblerAdd's prefix-copy region since `#d_0 + 1 < #s = actionPoint(ℓ)`. So `a_{#d_0 + 1} ≥ 1 > 0 = (s ⊕ ℓ)_{#d_0 + 1}` with agreement on positions `1..#d_0`, and by T1 case (i) at position `#d_0 + 1`, `a > s ⊕ ℓ` — contradicting `a < s ⊕ ℓ`.

(ii) `d` disagrees with `d_0` at some position `j ≤ #d_0`. Let `j` be the first such position. Then positions `1..j - 1` of `a` (which are `d_1..d_{j-1}`) equal positions `1..j - 1` of both `s` and `s ⊕ ℓ` (which are `d_{0,1}..d_{0,j-1}` by `s`'s structural form and TumblerAdd's prefix-copy region). At position `j`, `a_j = d_j ≠ d_{0,j} = s_j = (s ⊕ ℓ)_j`. By T1 case (i) at position `j`, either `d_j < d_{0,j}` (yielding `a < s` by the same divergence at the same position, contradicting `a ≥ s`) or `d_j > d_{0,j}` (yielding `a > s ⊕ ℓ`, contradicting `a < s ⊕ ℓ`). Contradiction either way.

Both sub-cases yield contradiction. Hence `#d ≤ #d_0`.

*Finiteness from the bound — case decomposition on `#d`.* The sub-case (ii) argument, applied symmetrically to `#d ≤ #d_0`, shows that `d` must agree with `d_0` on positions `1..#d` (any disagreement would yield `a < s` or `a > s ⊕ ℓ` at the disagreement position). Hence `d` is the length-`#d` prefix of `d_0`, uniquely determined by `#d`.

Admissibility further requires `d` to be T4-valid with `zeros(d) = 2`. By F's structural definition (the conjunct `zeros(d) = 2 ∧ d satisfies T4` in F's set-builder formula above) applied to the canonical-span hypothesis `s ∈ F`, `d_0` is T4-valid with `zeros(d_0) = 2`; let `z_1 < z_2 ≤ #d_0` denote `d_0`'s two zero positions. For `d` (a prefix of `d_0`) to satisfy `zeros(d) = 2`, both zero positions must lie within `d`'s index range, so `#d ≥ z_2`. T4's endpoint clause `d_{#d} ≠ 0` excludes `#d = z_2` (since `d_{z_2} = d_{0, z_2} = 0`), forcing `#d > z_2`. Combined with `#d ≤ #d_0`, the admissible range is `#d ∈ {z_2 + 1, …, #d_0}`.

We split this range into two sub-cases.

*Sub-case A — `z_2 < #d < #d_0` contributes zero candidates.* Suppose `z_2 < #d < #d_0`. Position `#d + 1` of `d_0` is a non-zero component: the only zeros of `d_0` lie at `z_1, z_2 ≤ z_2`, and `#d + 1 ≥ z_2 + 2 > z_2`, so `d_0[#d + 1] ≠ 0`, hence `d_0[#d + 1] ≥ 1` by T0's carrier ℕ. The candidate `a = [d, 0, s'', k] ∈ F` has `a_{#d + 1} = 0` (the separator zero introduced by the structural form). Position `#d + 1 ≤ #d_0` lies within `d_0`'s prefix in `s = [d_0, 0, s', k_s]` (writing `s' = X ∈ {s_C, s_L}` for the span's subspace), giving `s_{#d + 1} = d_0[#d + 1] ≥ 1`. Position `#d + 1` of `s ⊕ ℓ` agrees with `s` by prefix-copy: the canonical assumption `ℓ = δ(n, #s)` gives `actionPoint(ℓ) = #s = #d_0 + 3` (OrdinalDisplacement, ASN-0034), and `#d + 1 ≤ #d_0 < #s` places this position in TumblerAdd's prefix-copy region, so `(s ⊕ ℓ)_{#d + 1} = s_{#d + 1} ≥ 1`. With prior-position agreement on `1..#d` (since `d` is the length-#d prefix of `d_0`), T1 case (i) at divergence position `#d + 1` yields `a < s` from `a_{#d + 1} = 0 < s_{#d + 1}` — contradicting `a ≥ s`. The sub-case admits no candidates.

*Sub-case B — `#d = #d_0` contributes exactly `n` candidates.* Suppose `#d = #d_0`. Then `d = d_0`, and the candidate has form `a = [d_0, 0, s'', k]` with `#a = #d_0 + 3 = #s`. Compare `a` with `s = [d_0, 0, X, k_s]` and `s ⊕ ℓ`:

- Positions `1..#d_0 + 1`: all three coincide. `a` and `s` carry `d_0` on positions `1..#d_0` and zero at position `#d_0 + 1` (the separator in both structural forms); `s ⊕ ℓ` agrees with `s` by prefix-copy on positions `1..#s − 1`, and `#d_0 + 1 < #s`.
- Position `#d_0 + 2`: `a` has `s''`, `s` has `X`, `s ⊕ ℓ` has `X` (prefix-copy, `#d_0 + 2 < #s`).
- Position `#s = #d_0 + 3`: `a` has `k`, `s` has `k_s`, `s ⊕ ℓ` has `k_s + n` (TumblerAdd at the action point: `s_{#s} + ℓ_{#s} = k_s + n`).

*Subspace component (position `#d_0 + 2`).* If `s'' ≠ X`, T1 case (i) at position `#d_0 + 2` with prior-position agreement decides the order. By SubspaceConventionAxiom (ASN-0093), `s_C = 1 < 2 = s_L`. If `s'' < X`, then `a < s` (contradicting `a ≥ s`); if `s'' > X`, then `a > s ⊕ ℓ` (contradicting `a < s ⊕ ℓ`). Either branch excludes the candidate, forcing `s'' = X` for any admissible candidate.

*Chain index (position `#s`).* With `s'' = X`, divergence falls at position `#s`. T1 case (i) at position `#s` with prior-position agreement gives the equivalence `a ∈ [s, s ⊕ ℓ) ⟺ k_s ≤ k < k_s + n`. Exactly `n` integer values of `k` satisfy this constraint.

*Total.* Sub-case A contributes `0` candidates at each admissible `#d` in the open range `(z_2, #d_0)`; sub-case B contributes exactly `n` candidates at `#d = #d_0`. Summing across the admissible range:
```
|F ∩ [s, s ⊕ ℓ)| = 0 + ⋯ + 0 + n = n
```
which is finite. (When `#d_0 = z_2 + 1`, sub-case A's range is empty and the sum reduces directly to `n`.)

**LP-Fin Corollary — CanonicalIntervalCharacterisation.** For canonical span `(s, ℓ)` with `s = [d_0, 0, X, k_s]` (where `X ∈ {s_C, s_L}`) and `ℓ = δ(n, #s)`:
```
F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}
```
Every `t ∈ F ∩ [s, s ⊕ ℓ)` satisfies `subspace_I(t) = X` and `origin(t) = d_0`. The interval contains no F-candidates from any chain other than `A_X(d_0)`: cross-document chains are excluded by the proof's `#d ≤ #d_0` bound (sub-cases (i) and (ii) of the bound argument) together with sub-case A's separator argument at lengths `z_2 < #d < #d_0`; the same-document cross-subspace chain `A_Y(d_0)` with `Y ≠ X` is excluded by sub-case B's subspace-component step (which forces `s'' = X`). This corollary discharges LP12a's second boundary case (Discoverability and Survival section, above) by lifting "the span starts in the content subspace" to "the entire coverage avoids `dom(L)`"; the discharge is stated as LP12b immediately below.

**LP12b — ContentCanonicalLinkSubspaceWPFalse.** We discharge LP12a's second boundary case (deferred from the "Discoverability and Survival" section above), in which a K.μ⁻ transition on document `d` uses retention parameters `n'_{s_C} = 0` and `n'_{s_L} > 0`. Let `a ∈ dom(Σ.L)` be a link such that every span `(s, ℓ) ∈ Σ.L(a).eᵢ` (for every slot `i`) is canonical (`ℓ = δ(n, #s)` for some `n ≥ 1`) with `s = [d_s, 0, s_C, k_s]` for some T4-valid document `d_s` and chain index `k_s ≥ 1`. The retention set is `R = {[s_L, 1, ..., 1, k] : 1 ≤ k ≤ n'_{s_L}} ⊆ V_{s_L}(d)` — only link-subspace V-positions retained. We show `project(a, i, d, Σ) ⊆ V_{s_C}(d)`, from which `project(a, i, d, Σ) ∩ R ⊆ V_{s_C}(d) ∩ V_{s_L}(d) = ∅` follows, and the wp evaluates to false.

The argument turns on the absence of link addresses from coverage: `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅`. By StoreT4Validity and the chain-element structural form of ASN-0093, every `ℓ' ∈ dom(Σ.L)` inhabits some sub-allocator chain `A_L(d')` and so has structural form `[d', 0, s_L, k']` with `#E(ℓ') = 2` — placing `dom(Σ.L) ⊆ F`. For a single span `(s, ℓ) ∈ Σ.L(a).eᵢ` with `s = [d_s, 0, s_C, k_s]` and `ℓ = δ(n, #s)`, the coverage is the interval `[s, s ⊕ ℓ)`; rewriting via `dom(Σ.L) ⊆ F`:
```
[s, s ⊕ ℓ) ∩ dom(Σ.L) = F ∩ [s, s ⊕ ℓ) ∩ dom(Σ.L)
```
LP-Fin Corollary applied at `X = s_C` gives `F ∩ [s, s ⊕ ℓ) = {[d_s, 0, s_C, k] : k_s ≤ k < k_s + n}` — every F-candidate in the interval has subspace identifier `s_C`. By L0 (ASN-0093), every element of `dom(Σ.L)` has subspace identifier `s_L`; by SubspaceConventionAxiom (`s_C ≠ s_L`), no address with subspace identifier `s_C` can inhabit `dom(Σ.L)`. Hence `F ∩ [s, s ⊕ ℓ) ∩ dom(Σ.L) = ∅`, and so `[s, s ⊕ ℓ) ∩ dom(Σ.L) = ∅` per span. Taking the union over the spans of the endset, `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅`.

Now constrain the projection by subspace. Suppose `v ∈ project(a, i, d, Σ)` with `subspace(v) = s_L`. By S3★ (ASN-0047), `Σ.M(d)(v) ∈ dom(Σ.L)`; by the projection definition, `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ)`. Hence `Σ.M(d)(v) ∈ coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅` — contradiction. So no link-subspace V-position lies in the projection, and `project(a, i, d, Σ) ⊆ V_{s_C}(d)`. The wp then yields `project(a, i, d, Σ) ∩ R ⊆ V_{s_C}(d) ∩ V_{s_L}(d) = ∅` (the two subspace V-position sets are disjoint by S3★-aux and SC-NEQ: every `v ∈ dom(Σ.M(d))` has `subspace(v) ∈ {s_C, s_L}` by S3★-aux, but no `v` can carry both identifiers). Existentially over slots, `(E i : project(a, i, d, Σ) ∩ R ≠ ∅)` is false — discharging LP12a's wp on this retention pattern for the canonical-content-subspace class of links.

The case exhibits the wp's *per-subspace sensitivity*: the retention set's subspace partition — not merely its total cardinality — determines whether the wp is satisfiable for a given link.

*Non-canonical spans yield infinite intersections.* For `(s, ℓ)` satisfying T12 but with `#ℓ < #s`, TumblerAdd's result-length identity gives `#(s ⊕ ℓ) = #ℓ < #s`. We show that the chain `A_X(d_0)` itself — same document, same subspace as `s` — supplies infinitely many F-candidates in `[s, s ⊕ ℓ)`, uniformly across the entire `#ℓ < #s` range (including the sub-range `#d_0 < #ℓ < #s`), using only within-chain elements without invoking descendant constructions. The descendant trap of LP-Fin's positive proof (sub-case (i) above) — the contradiction `a_{#d_0 + 1} ≥ 1 > 0 = (s ⊕ ℓ)_{#d_0 + 1}` driven by component disagreement at position `#d_0 + 1` — is unavailable in the present setting on two grounds. When `#ℓ ≤ #d_0`, the trap cannot be sprung because position `#d_0 + 1` exceeds `#(s ⊕ ℓ) = #ℓ` and so falls outside the T1 comparison range. When `#d_0 < #ℓ < #s`, position `#d_0 + 1` re-enters the comparison range, but the trap is potentially closable rather than guaranteed sprung; descendant candidates need not be excluded uniformly. The within-chain argument that follows is parametric in `#ℓ` and discharges both sub-ranges by a single divergence at position `actionPoint(ℓ) ≤ #ℓ`.

By ActionPoint (ASN-0034), `1 ≤ actionPoint(ℓ) ≤ #ℓ`; combined with `#ℓ < #s`, this yields `actionPoint(ℓ) ≤ #ℓ < #s`. Let `k_ℓ := actionPoint(ℓ)`, so `1 ≤ k_ℓ ≤ #ℓ < #s = #d_0 + 3`. Writing `X ∈ {s_C, s_L}` for the subspace component of `s` (so `s = [d_0, 0, X, k_s]`), the chain `A_X(d_0)` has elements `t_k^X(d_0) = [d_0, 0, X, k]` for `k ≥ 1`, each of length `#s` and each agreeing with `s` on positions `1..#s − 1` by structural form (they differ from `s` only at position `#s`). Fix any `k ≥ 1` and compare `t_k^X(d_0)` with `s ⊕ ℓ`: the T1 case (i) comparison range is `≤ min(#t_k^X(d_0), #(s ⊕ ℓ)) = min(#s, #ℓ) = #ℓ`. At positions `1..k_ℓ − 1`, TumblerAdd's prefix-copy region gives `(s ⊕ ℓ)_i = s_i`, and the structural agreement on `1..#s − 1` gives `t_k^X(d_0)_i = s_i`, so the two agree on positions `1..k_ℓ − 1`. At position `k_ℓ`, TumblerAdd's action-point step gives `(s ⊕ ℓ)_{k_ℓ} = s_{k_ℓ} + ℓ_{k_ℓ}`, with `ℓ_{k_ℓ} ≥ 1` by ActionPoint; since `k_ℓ < #s`, position `k_ℓ` remains in the structural-agreement region, so `t_k^X(d_0)_{k_ℓ} = s_{k_ℓ} < s_{k_ℓ} + ℓ_{k_ℓ} = (s ⊕ ℓ)_{k_ℓ}`. By T1 case (i) at divergence position `k_ℓ ≤ #ℓ`, `t_k^X(d_0) < s ⊕ ℓ` for every `k ≥ 1`. For the lower bound, `t_k^X(d_0) ≥ s` for every `k ≥ k_s`: equality at `k = k_s` by structural identity, strict inequality at `k > k_s` by ChainEnumerationInjectivity (ASN-0093). Hence `{t_k^X(d_0) : k ≥ k_s} ⊆ F ∩ [s, s ⊕ ℓ)`, an infinite subset within a single sub-allocator chain, and `|F ∩ [s, s ⊕ ℓ)| = ℵ₀` holds uniformly across the entire `#ℓ < #s` range.

Concrete witness: take `s = [1, 0, 1, 0, 1, 0, 1, 1]` (so `#s = 8`, `d_0 = [1, 0, 1, 0, 1]`, `zeros(d_0) = 2`, `X = 1`, `k_s = 1`) and `ℓ = [0, 0, 0, 1]` (so `#ℓ = 4` and `actionPoint(ℓ) = 4 ≤ #s = 8`, satisfying T12). Then `s ⊕ ℓ = [1, 0, 1, 1]` (length 4, via TumblerAdd's prefix-copy on positions 1–3 and sum at position 4: `0 + 1 = 1`). For each `k ≥ 1`, the chain element `t_k^1(d_0) = [1, 0, 1, 0, 1, 0, 1, k]` is in F by direct inspection: `zeros = 3` (the two zeros of `d_0` at positions 2 and 4, plus the separator at position 6), no adjacent zeros (each separator is bordered by nonzero components), `t_k^1(d_0)_1 = 1 ≠ 0`, and `t_k^1(d_0)_8 = k ≥ 1 ≠ 0`. Verification that `t_k^1(d_0) ∈ [s, s ⊕ ℓ)`: at position 4 (the action point of `ℓ`), `t_k^1(d_0)_4 = 0 < 1 = (s ⊕ ℓ)_4`, with positions 1–3 agreeing, so `t_k^1(d_0) < s ⊕ ℓ` by T1 case (i); at position 8, `t_k^1(d_0)_8 = k ≥ 1 = s_8`, with positions 1–7 agreeing, so `t_k^1(d_0) ≥ s` (equality at `k = 1`, strict above) by T1 case (i). Hence `{t_k^1(d_0) : k ≥ 1} ⊆ F ∩ [s, s ⊕ ℓ)`, an infinite set within a single sub-allocator chain. The canonical assumption `ℓ = δ(n, #s)` is therefore load-bearing for LP-Fin's finitude conclusion — the within-chain witness above breaks finitude uniformly across the entire `#ℓ < #s` range. LP-Fin's reliance on the action-point identification `actionPoint(ℓ) = #s` (OrdinalDisplacement, ASN-0034) means non-canonical forms with `#ℓ = #s` but `ℓ` not an ordinal displacement (some nonzero component before position `#s`, equivalently `actionPoint(ℓ) < #s`) also fall outside the canonical scope. We verify the within-chain construction extends to this case explicitly. Fix the chain `A_X(d_0)` exactly as above, with elements `t_k^X(d_0) = [d_0, 0, X, k]` of length `#s` agreeing with `s` on positions `1..#s − 1` (chain elements differ from `s` only at position `#s`). Set `k_ℓ := actionPoint(ℓ)`; the non-ordinal hypothesis combined with `#ℓ = #s` gives `1 ≤ k_ℓ < #s`. For any `k ≥ k_s`, compare `t_k^X(d_0)` with `s ⊕ ℓ`. The T1 comparison range is `≤ min(#t_k^X(d_0), #(s ⊕ ℓ)) = min(#s, #ℓ) = #s` — extending all the way through `#s`, where previously (`#ℓ < #s`) the bound `min(#s, #ℓ) = #ℓ` truncated comparison shy of `#s`. *Upper bound:* at positions `1..k_ℓ − 1`, TumblerAdd's prefix-copy region gives `(s ⊕ ℓ)_i = s_i`, and structural agreement gives `t_k^X(d_0)_i = s_i`, so the two agree. At position `k_ℓ < #s`, TumblerAdd's action-point step gives `(s ⊕ ℓ)_{k_ℓ} = s_{k_ℓ} + ℓ_{k_ℓ}` with `ℓ_{k_ℓ} ≥ 1` (ActionPoint), while `t_k^X(d_0)_{k_ℓ} = s_{k_ℓ}` (structural agreement at this position since `k_ℓ < #s`); hence `t_k^X(d_0)_{k_ℓ} < (s ⊕ ℓ)_{k_ℓ}`. By T1 case (i) at divergence position `k_ℓ ≤ #ℓ = #s`, `t_k^X(d_0) < s ⊕ ℓ`. The post-comparison region at positions `k_ℓ + 1..#s` carries `ℓ`'s tail on `s ⊕ ℓ` via TumblerAdd's tail-copy and chain-element fixed values on `t_k^X(d_0)`, but T1 case (i) decides the order at the earlier divergence position `k_ℓ` — so the tail values, including the now-in-range last position `#s`, do not need consultation. *Lower bound:* identical to the `#ℓ < #s` argument — equality at `k = k_s` by structural identity (`t_{k_s}^X(d_0) = [d_0, 0, X, k_s] = s`), strict inequality at `k > k_s` by ChainEnumerationInjectivity (ASN-0093). Hence `{t_k^X(d_0) : k ≥ k_s} ⊆ F ∩ [s, s ⊕ ℓ)` for the `#ℓ = #s` non-ordinal case as well, breaking finitude. The tightness predicate excludes such spans by definitional canonical-form rather than via finitude — see ground (ii) below.

The achievability arguments below proceed under the canonical assumption — every span exhibited has `ℓ = δ(n, #s)` — and exhaust `F ∩ [s, s ⊕ ℓ)` by structural partition. The count within each structural case is finite by LP-Fin (in its canonical form), and the case analysis is decidable from `s`, `ℓ`, and the structural form of `F`-candidates without enumerating `F`.

An endset `e` is *tight at state `Σ_e`* iff every span `(s, ℓ) ∈ e` is *canonical* — `ℓ = δ(n, #s)` for some `n ≥ 1`, equivalently `#ℓ = #s` with `ℓ` an ordinal displacement (OrdinalDisplacement, ASN-0034) — and satisfies:
```
s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)  ∧  (A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))
```

The first conjunct says the span starts at an allocated address; the second says every substrate-emittable address in the span's reach is already allocated. The canonical-span requirement ensures the universal quantifier ranges over a finite set (LP-Fin, below), so the predicate is decidable at every state. Tightness is a state-relative predicate; in the canonical use case `Σ_e` is the state at which `e` was incorporated into a link, but the predicate is well-defined at any state.

*Non-canonical spans are unconditionally non-tight, on two structurally distinct grounds.* (i) For spans satisfying T12 with `#ℓ < #s`, LP-Fin's non-canonical remark (above) gives `|F ∩ [s, s ⊕ ℓ)| = ℵ₀`, while `dom(Σ_e.C) ∪ dom(Σ_e.L)` is finite at every reachable state (by C-fin and L-fin of ASN-0093). The universal quantifier of the tightness predicate therefore cannot be discharged at any state — there always exist substrate-emittable addresses in the span's reach that no construction discipline could have pre-allocated. This case demonstrates that the canonical requirement is structurally necessary for predicate decidability, not merely a stylistic convention. (ii) For spans with `#ℓ = #s` but `ℓ` not an ordinal displacement (some nonzero component before position `#s`), or for spans with `#ℓ > #s`: non-tight by the tightness predicate's *definitional* canonical-form requirement `ℓ = δ(n, #s)`; the predicate excludes such spans by construction, independent of the finitude argument. In ground (ii) the universal quantifier might or might not be decidable depending on the specific structural form of `ℓ`, but the question does not arise — the predicate is restricted to canonical spans by definition. No state, and no editing trajectory leading to a state, can render a non-canonical span tight. The distinction between "could be made tight with discipline" and "cannot be tight at any state" is decided by the structural form `ℓ = δ(n, #s)` alone — i.e., by the full canonical form, not merely by `#ℓ = #s` — and not by the contents of the stores.

*Achievability (under canonical-ℓ assumption).* **The analysis below restricts to canonical spans** — those with `ℓ = δ(n, #s)` for some `n ≥ 1`, equivalently `#ℓ = #s` with `ℓ` an ordinal displacement (OrdinalDisplacement, ASN-0034). Non-canonical spans (`#ℓ < #s`) fall outside the tight-endset domain by the structural non-tightness result just established above, so achievability of tight construction addresses only canonical spans.

The non-empty case is reached by the canonical construction. Span endpoints are drawn from currently-allocated content, and the displacement is the canonical ordinal displacement `ℓ = δ(n, #s)`; by OrdinalDisplacement's postcondition, `actionPoint(ℓ) = #s`. The action-point identification `k_ℓ = #s` used throughout the case analyses below is therefore a *consequence of the construction's specification* (the canonical construction picks ordinal-displacement spans), not a property derivable from C0 of ASN-0058 (C0 governs well-formed content references, which require additional preconditions not in force here for arbitrary endset spans). The reach is set at or before the relevant chain's next emission point. By LP-Fin (in its canonical form), only finitely many `F`-candidates can interfere with any such span; the case analysis below exhausts that finite set by structural partition.

Each of the four cross-document interference arguments below — same-document cross-subspace, non-nesting documents, descendant documents, ancestor documents — leans on the canonical assumption via prefix-copy reasoning that requires `actionPoint(ℓ) = #s ≥ #d_0 + 1` (so that `s`'s separator at position `#d_0 + 1`, and more generally positions `1..#s - 1`, lie within the prefix-copy region of `s ⊕ ℓ` and are preserved verbatim from `s`). For non-canonical `ℓ` with `#ℓ < #s`, `#(s ⊕ ℓ) = #ℓ` and the T1 comparison may terminate before reaching position `#d_0 + 1`, so the descendant case (which divergence-detects at position `#d_0 + 1`) and the ancestor case (which divergence-detects at position `#d' + 1 ≤ #d_0 + 1`) need not close. This is the same structural failure as LP-Fin's non-canonical remark, viewed at the case-analysis level rather than the finitude level — and it is the reason achievability is restricted to the canonical regime in the first place.

*Relationship to LP-Fin Corollary.* The four cross-chain interference arguments below — same-document cross-subspace (both directions), non-nesting documents, descendant documents, ancestor documents — are direct consequences of LP-Fin Corollary, which already establishes `F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}` (every F-candidate in the interval shares the span's subspace identifier `X` and origin `d_0`, so cross-chain candidates contribute nothing). We retain the per-case verification for two reasons. First, motivational clarity: each case exhibits the specific T1 divergence position that rules out one structurally distinct family of interfering candidates (`#d_0 + 2` for same-document cross-subspace, `j ≤ min(#d_0, #d')` for non-nesting, `#d_0 + 1` for descendant, `#d' + 1` for ancestor), and these positional arguments are exactly the per-family sub-arguments that combine to discharge the LP-Fin Corollary's structural exclusion. Second, this section additionally establishes tightness against `A_X(d_0)`'s own *future* emissions via the emission-frontier choice `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` — a condition that constrains `n` against the chain-index frontier `m` and is not implied by LP-Fin Corollary alone (the corollary characterises interval membership but does not say which of those indices are allocated at `Σ_e`). Readers who accept the corollary may skim the four cross-chain sub-cases as concrete instances of its structural exclusion clause; the within-chain emission-frontier argument carries content beyond the corollary and is load-bearing for achievability.

Fix the span's starting chain. The three cross-document cases (non-nesting, descendant, ancestor) make no use of the span's subspace identifier — their arguments hinge on the prefix relation between `d_0` and `d' ≠ d_0`, with the decisive divergence falling at a position `≤ #d_0 + 1` (within `d_0`'s document-level prefix, or at the separator immediately after). The span's subspace component at position `#d_0 + 2` plays no role in these arguments, so a single statement of each cross-document case covers spans on `A_C(d_0)` and on `A_L(d_0)` without modification. The same-document cross-subspace case is the only case whose argument depends structurally on the span's subspace: the interfering chain's component at position `#d_0 + 2` is distinguished from the span's at the same position, and the *direction* of the resulting T1 exclusion flips between the two arrangements (span on `A_C(d_0)` excludes `A_L(d_0)` interferers above the interval; span on `A_L(d_0)` excludes `A_C(d_0)` interferers below). We verify both sub-cases explicitly.

Choose `ℓ = δ(n, #s)` with `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` where `X ∈ {C, L}` is the span's subspace and `m` is `A_X(d_0)`'s currently-allocated chain-index maximum at `Σ_e`. Chain elements of `A_X(d_0)` with index `> m` lie at or above `inc(t_m^X(d_0), 0)` by ChainEnumerationInjectivity (ASN-0093), so none fall in `[s, s ⊕ ℓ)` — the span is tight against `A_X(d_0)`'s own future emissions. Interference from chains other than `A_X(d_0)` splits into four exhaustive cases: same-document cross-subspace (the chain `A_Y(d_0)` with `Y ∈ {C, L} \ {X}` on `d_0` itself), and three cross-document cases parameterised by the prefix relation between `d_0` and a distinct document tumbler `d' ≠ d_0` — non-nesting (neither `d_0` nor `d'` is a prefix of the other), descendant of `d_0` (`d_0 ≺ d'`), and ancestor of `d_0` (`d' ≺ d_0`). The three cross-document cases are exhaustive on `d' ≠ d_0` because Divergence (ASN-0034) splits any pair of distinct tumblers into component-divergence (case (i), non-nesting once prefix-nesting is excluded) and prefix-divergence (case (ii), one a proper prefix of the other). The same-document cross-subspace case completes the partition over all sub-allocator chains other than the one the span is built on.

*Same document, cross subspace (span on `A_C(d_0)`).* The span is built on `A_C(d_0)`'s chain, so `s` carries `s_C` at position `#d_0 + 2` (by the structural form `s = [d_0, 0, s_C, k_s]`). The image `s ⊕ ℓ` agrees with `s` at this position: since `ℓ = δ(n, #s)` is an ordinal displacement, OrdinalDisplacement (ASN-0034) supplies `actionPoint(ℓ) = #s = #d_0 + 3`, and position `#d_0 + 2 < #s` falls in TumblerAdd's prefix-copy region, so `(s ⊕ ℓ)_{#d_0 + 2} = s_{#d_0 + 2} = s_C`. The interfering chain is `A_L(d_0)`, whose elements `b` have structural form `[d_0, 0, s_L, k]` (ASN-0093), so `b_{#d_0 + 2} = s_L`. Positions `1..#d_0 + 1` agree between `b`, `s`, and `s ⊕ ℓ` (all carry `d_0` followed by `0` at position `#d_0 + 1`, established by the chain structure for `b` and by prefix-copy reasoning for `s ⊕ ℓ`). By SubspaceConventionAxiom (ASN-0093, `s_C = 1`, `s_L = 2`), `s_L > s_C`, and T1 case (i) at divergence position `#d_0 + 2` gives `b > s ⊕ ℓ` (since `b_{#d_0 + 2} = s_L > s_C = (s ⊕ ℓ)_{#d_0 + 2}`), so `b ∉ [s, s ⊕ ℓ)`. The interfering chain elements are excluded *above* the interval.

*Same document, cross subspace (span on `A_L(d_0)`).* The span is built on `A_L(d_0)`'s chain, with `s = [d_0, 0, s_L, k_s]`, so `s` carries `s_L` at position `#d_0 + 2`. The image `s ⊕ ℓ` again agrees with `s` at this position by the same prefix-copy argument (canonical `ℓ = δ(n, #s)`, `actionPoint(ℓ) = #s = #d_0 + 3`, `#d_0 + 2 < #s`), so `(s ⊕ ℓ)_{#d_0 + 2} = s_L`. The interfering chain is `A_C(d_0)`, whose elements `b` have structural form `[d_0, 0, s_C, k]`, so `b_{#d_0 + 2} = s_C`. Positions `1..#d_0 + 1` agree between `b`, `s`, and `s ⊕ ℓ` exactly as in the previous sub-case. By SubspaceConventionAxiom, `s_C < s_L`, and T1 case (i) at divergence position `#d_0 + 2` now gives `b < s` (since `b_{#d_0 + 2} = s_C < s_L = s_{#d_0 + 2}`), so `b ∉ [s, s ⊕ ℓ)`. The interfering chain elements are excluded *below* the interval — the conclusion `b ∉ [s, s ⊕ ℓ)` is preserved, but the sign of the exclusion has flipped relative to the `A_C(d_0)`-span case above.

*Non-nesting documents.* By Divergence (ASN-0034) applied to `d_0` and `d'`, case (i) applies — case (ii) would require one to be a prefix of the other, contradicting non-nesting — so there is a position `j ≤ min(#d_0, #d')` with `d_{0,j} ≠ d'_j` and `d_{0,i} = d'_i` for `1 ≤ i < j`. Chain elements `b` of `A_sub'(d')` carry `d'` as a prefix (by TA5(b) and the chain structure of ASN-0093), so `b_i = d'_i` for `1 ≤ i ≤ #d'`; in particular `b_j = d'_j` since `j ≤ #d'`. Similarly `s` carries `d_0` as a prefix, so `s_i = d_{0,i}` for `1 ≤ i ≤ #d_0`; in particular `s_j = d_{0,j}` since `j ≤ #d_0`. The image `s ⊕ ℓ` agrees with `s` at position `j`: since `ℓ = δ(n, #s)` is the canonical ordinal-displacement, OrdinalDisplacement (ASN-0034) gives `actionPoint(ℓ) = #s = #d_0 + 3 > j` (since `j ≤ #d_0`), so position `j` lies in TumblerAdd's prefix-copy region where `(s ⊕ ℓ)_j = s_j`. Positions `1..j-1` agree between `b` and both `s` and `s ⊕ ℓ` via the same prefix-agreement and prefix-copy facts. By T1 case (i) of ASN-0034 at the divergence position `j`, the comparison splits on the sign of `d'_j - d_{0,j}`: if `d'_j < d_{0,j}` then `b_j < s_j` and so `b < s`, placing `b` below the interval `[s, s ⊕ ℓ)`; if `d'_j > d_{0,j}` then `b_j > (s ⊕ ℓ)_j` and so `b > s ⊕ ℓ`, placing `b` above. Either way `b ∉ [s, s ⊕ ℓ)`.

*Descendant documents.* Consider documents `d'` standing in a proper prefix relation `d_0 ≺ d'`. The argument is structural — it depends on the form `d'` must take given that `d_0 ≺ d'` and both are T4-valid documents, not on the specific K.δ operation chain by which `d'` was reached. (For context: the K.δ rules (ASN-0047) admit descendants of `d_0` via the document creation operations `k ∈ {0, 1}` — `inc(_, 1)` creates a new version extending the current document by one non-zero component, and `inc(_, 0)` advances a version's last non-zero component without introducing zeros. The `k = 2` rule is forbidden once `zeros(t) = 2` is reached, which is the case at every document tumbler. Descendants of `d_0` are therefore reachable by chains that interleave `inc(_, 0)` and `inc(_, 1)` steps starting from an initial `inc(d_0, 1)`, never by `inc(_, 2)`.) The structural property we extract is independent of the specific interleaving and of `d'`'s depth.

By Prefix (PrefixRelation, ASN-0034), `d_0 ≺ d'` unfolds to `#d_0 < #d'` and `d'_i = d_{0,i}` for `1 ≤ i ≤ #d_0`. Set `q := #d' - #d_0 ≥ 1` and write the extension as `d' = [d_0, x_1, x_2, …, x_q]` where `x_i := d'_{#d_0 + i}`.

*Each `x_i ≥ 1`.* By F's structural definition (the conjunct `zeros(d) = 2 ∧ d satisfies T4` in F's set-builder formula above) applied to both documents — `d_0` via the canonical-span hypothesis `s ∈ F`, and `d'` via its role as the document parameter of any chain element of `A_C(d')` or `A_L(d')` that could lie in `F ∩ [s, s ⊕ ℓ)` — `d_0` and `d'` are T4-valid with `zeros(d_0) = zeros(d') = 2`. The prefix `d_0` contributes exactly two zeros to `d'` (at the two separator positions encoded by `d_0`'s field structure, both at positions `≤ #d_0`). Therefore positions `#d_0 + 1, …, #d_0 + q` of `d'` contribute zero zeros to `d'`, i.e., each `x_i ≠ 0`. T0's carrier ℕ forces `x_i ≥ 1` from `x_i ≠ 0`. (We do not need the no-adjacent-zeros conjunct of T4 here; the zero-count balance alone suffices.) In particular `x_1 ≥ 1` — the only structural fact the proof below depends on; the values of `x_2, ..., x_q` and `q` itself drop out of the argument.

We show directly — without induction on `q` — that for every descendant `d'` of `d_0` at any depth `q ≥ 1`, every chain element of `A_C(d')` (resp. `A_L(d')`) lies strictly above `s ⊕ ℓ`, so that `b ∉ [s, s ⊕ ℓ)`. Chain elements of `A_C(d')` have form `[d', 0, s_C, k] = [d_0, x_1, …, x_q, 0, s_C, k]` (depth `#d_0 + q + 3`) — they carry `d'` as a prefix by ASN-0093's chain structure, and `d'` in turn carries `d_0` as a prefix by the unfolding of `d_0 ≺ d'` above. Compare with `s = [d_0, 0, s_C, k_s]` and `s ⊕ ℓ`, both of length `#s = #d_0 + 3`. Positions `1..#d_0` agree between the chain element and both `s` and `s ⊕ ℓ`: the chain element carries `d_0` on these positions by the prefix relations just stated; `s` carries `d_0` on these positions by its structural form; `s ⊕ ℓ` agrees with `s` on these positions because the canonical `ℓ = δ(n, #s)` is an ordinal displacement whose action point `actionPoint(ℓ) = #s` (OrdinalDisplacement, ASN-0034) falls at the last position of `s`, so positions `1..#s - 1` lie in TumblerAdd's prefix-copy region and `(s ⊕ ℓ)_i = s_i` for `1 ≤ i < #s`, in particular for `1 ≤ i ≤ #d_0 < #s`. At the divergence position `#d_0 + 1`, the chain element has value `x_1 ≥ 1`, while `s` has value `0` (the separator at position `#d_0 + 1` in `s`'s structural form) and `s ⊕ ℓ` also has value `0` (by the prefix-copy reasoning above, since `#d_0 + 1 < #s`). By T1 case (i) at the divergence position `#d_0 + 1` with `x_1 ≥ 1 > 0 = (s ⊕ ℓ)_{#d_0 + 1}`, the chain element exceeds `s ⊕ ℓ`.

The conclusion: tightness is preserved against every descendant of `d_0` at every depth, regardless of the specific K.δ operation chain by which the descendant was constructed. The argument turns on `x_1 ≥ 1` (the depth-1 extension component, established by zero-count balance) alone, independent of `q`.

*Ancestor documents.* Consider documents `d'` standing in a proper prefix relation `d' ≺ d_0`. As in the descendant case, the argument is structural: it depends on the form `d_0` must take given that `d' ≺ d_0` and both are T4-valid documents, not on the specific K.δ chain by which `d_0` was reached from `d'`. (For context: descendants of `d'` are reachable by interleaved `inc(_, 0)` and `inc(_, 1)` chains starting with `inc(d', 1)`, never `inc(_, 2)` once `zeros = 2` is achieved; this is symmetric to the descendant case above.)

By Prefix applied to `d' ≺ d_0`, `#d' < #d_0` and `d_{0, i} = d'_i` for `1 ≤ i ≤ #d'`. Set `r := #d_0 - #d' ≥ 1` and write `d_0 = [d', y_1, y_2, …, y_r]` where `y_i := d_{0, #d' + i}`. The zero-count balance argument (symmetric to the descendant case): `zeros(d') = zeros(d_0) = 2` by F's structural definition applied to both documents (`d_0` via the canonical-span hypothesis `s ∈ F`, `d'` via its role as the document parameter of any chain element of `A_C(d')` or `A_L(d')` that could lie in `F ∩ [s, s ⊕ ℓ)`), the prefix `d'` contributes its two zeros to `d_0` at positions `≤ #d'`, so positions `#d' + 1, …, #d' + r` of `d_0` contribute zero zeros and each `y_i ≠ 0`, hence `y_i ≥ 1` by T0's carrier ℕ. In particular `y_1 ≥ 1` — the structural fact the proof needs.

We show directly — without induction on `r` — that for every ancestor `d'` of `d_0` at any depth `r ≥ 1`, every chain element `b` of `A_C(d')` (resp. `A_L(d')`) lies strictly below `s`. Chain elements have the form `[d', 0, s_C, k]` (resp. with `s_L`) for `k ≥ 1`, so `#b = #d' + 3`. Positions `1..#d'` agree between `b` and `s`: `b` carries `d'` as prefix by ASN-0093's chain structure; `s` carries `d_0` as prefix, and the unfolding of `d' ≺ d_0` gives `d_{0,i} = d'_i` for `1 ≤ i ≤ #d'`. At position `#d' + 1`: `b_{#d' + 1} = 0` (the separator immediately after `d'`'s prefix in any chain element of `A_C(d')`), while `s_{#d' + 1} = d_{0, #d' + 1} = y_1 ≥ 1`. The image `s ⊕ ℓ` agrees with `s` at position `#d' + 1` since `ℓ = δ(n, #s)` is an ordinal displacement with `actionPoint(ℓ) = #s > #d' + 1` (OrdinalDisplacement, ASN-0034; the inequality holds because `#d' < #d_0` gives `#d' + 1 ≤ #d_0 < #d_0 + 3 = #s`), placing position `#d' + 1` in TumblerAdd's prefix-copy region where `(s ⊕ ℓ)_{#d' + 1} = s_{#d' + 1} = y_1`. T1 case (i) at the divergence position `#d' + 1` with `b_{#d'+1} = 0 < y_1 = s_{#d'+1}` yields `b < s`.

The conclusion: tightness is preserved against every ancestor at every depth, regardless of the specific K.δ chain by which `d_0` was constructed from the ancestor. The argument turns on `y_1 ≥ 1` (the depth-1 extension component, established by zero-count balance) alone, independent of `r`.

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

**LP19 — TightEndsetBoundaryExclusion**: Let `e` be an endset tight at `Σ_e`, and let `Σ_e →* Σ_n → Σ_{n+1}` be a reachable transition sequence whose final step is a K.μ⁺ (or K.μ⁺_L) transition operating on document `d`. K.μ⁺ may add multiple mappings `{(v_1, a_1), …, (v_k, a_k)} = dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` in a single step; LP19's hypothesis selects, *per pair*, only those whose I-address was freshly K.α/K.λ-allocated on the prefix. Formally, for every pair `(v_new, a_new) ∈ dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` such that `a_new` was freshly allocated by a K.α (or K.λ) step on the prefix `Σ_e →* Σ_n`:
```
v_new ∉ project(e, d, Σ_{n+1})
```
Pairs added at the same K.μ⁺ step whose I-address is *not* freshly allocated on the prefix — typically transclusion pairs whose `a_j ∈ dom(Σ_n.C) ∪ dom(Σ_n.L)` — fall outside this lemma's hypothesis and are governed instead by LP9's general growth characterisation, which admits growth when the transcluded `a_j ∈ coverage(e)`.

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

Furthermore, the two per-subspace inclusions *partition* the projection's full range. By S3★-aux (SubspaceExhaustiveness), every `v ∈ dom(Σ.M(d))` satisfies `subspace(v) ∈ {s_C, s_L}`; restricting to `project(e, d, Σ) ⊆ dom(Σ.M(d))`, the same dichotomy holds. Hence:
```
{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = {Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C}
                                   ∪ {Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L}
```
The union is exhaustive by S3★-aux; the two summands are jointly the full projection range. Together with the per-subspace inclusions above, this gives a complete characterisation of `{Σ.M(d)(v) : v ∈ project(e, d, Σ)}` as a partition into a content-subspace component (contained in `coverage(e) ∩ dom(Σ.C)`) and a link-subspace component (contained in `coverage(e) ∩ dom(Σ.L)`), with no other contributions.

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
- The link cannot fail to be discoverable from a document whose arrangement maps to any I-address in any of its endsets' coverage (LP12). LP12 is a per-state biconditional, not a temporal invariant; discoverability is determined afresh at each state by `coverage ∩ ran`.
- At any state, the link is not discoverable from a document whose arrangement contains no entry mapping to any I-address in coverage (LP12, contrapositive). The same per-state reading applies — a subsequent K.μ⁺ or K.μ⁺_L can re-establish discoverability (LP18), and a subsequent K.μ⁻ can withdraw it (LP10, LP12a).
- The link's discoverability cannot be made to depend on which document created it or which document allocated its linked content (LP12 references only coverage and range, indifferent to provenance).
- Boundary insertion of newly allocated content into a tightly constructed link's reach cannot grow that reach (LP19).

The trust relationship between the link holder and the system is asymmetric. The system commits unconditionally to LP2, LP3, and S0 (together with L12 of ASN-0043) — to the permanence of every stored object. The system commits conditionally to LP9–LP18 — to the discoverability of the link, contingent on what the document holders choose to do with their arrangements. The holder cannot prevent another document holder from deleting the linked content from their own arrangement (subject to their own ownership rules). The holder can rely on the content persisting somewhere in `dom(Σ.C)` permanently, but cannot rely on it persisting in any particular `ran(Σ.M(d))` indefinitely. Survival of discoverability requires only that *somewhere* in the system, *some* document still arranges *some* of the linked content. This is the strongest guarantee the architecture provides, and it is sufficient for the holder's purpose: the link's content can be re-introduced via transclusion at any time, and the link will then be re-projected at the new V-positions automatically and without any action by the holder.

## A Worked Trace

To make the displacement concrete, we trace a small example. Consider:

- A link `a` with endset `e₁ = {(i₁, δ(5, #i₁))}` — pinning the span's start at `i₀ := i₁` (the first traced chain element) and its width at the canonical ordinal displacement `ℓ := δ(5, #i₁)` (OrdinalDisplacement, ASN-0034) of depth `#i₁` and value 5, so that `i₀ ⊕ ℓ = shift(i₁, 5)`. The span is well-formed by T12 since `Pos(δ(5, #i₁))` holds and `actionPoint(δ(5, #i₁)) = #i₁ ≤ #i₁`. By T12, `coverage(e₁) = {t ∈ T : i₁ ≤ t < shift(i₁, 5)}` — the entire half-open T1-interval, not merely a discrete set. The I-addresses `i₁, i₂, i₃, i₄` are pairwise sibling chain elements of a single content sub-allocator `A_C(d_alloc)` for some `d_alloc ∈ dom(Σ.M)` — by SubAllocatorAxiom.ChainDiscipline (ASN-0093), all four share the common chain length `#d_alloc + 3` (ChainUniformLength, ASN-0093), and by ChainEnumerationInjectivity (ASN-0093) the enumeration `n ↦ tₙ` is strictly increasing under T1, so distinct chain indices yield distinct addresses ordered consistently with chain-index order. Concretely, the chain is rooted so that `iₖ = shift(i₁, k − 1)` for `k = 1, 2, 3, 4` — each `inc(·, 0)` step advances the final chain component by one (TA5(c) on the trailing nonzero significant position, ASN-0034) — and the same enumeration carries `i₁` to `shift(i₁, 4)` (the would-be fifth chain element, whether or not emitted) at a strictly smaller T1 position than `shift(i₁, 5)`. Hence `i₁ < i₂ < i₃ < i₄ < shift(i₁, 5)` and `i₁, …, i₄ ∈ dom(Σ.C)`; the interval `coverage(e₁)` contains these four addresses (along with any other tumbler lying strictly below `shift(i₁, 5)`). For trace clarity we follow only these four, since they are precisely the addresses in `coverage(e₁) ∩ ran(Σ.M(d₁))` for the document considered below — and by LP12 the projection through `d₁` is governed by that intersection, not by the full coverage.
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

The projection has shrunk by `{v₄}` (per LP10's exact characterisation), and the retained set `{v₁, v₂, v₃}` is the D-SEQ★-admissible prefix permitted by K.μ⁻. The I-address `i₄` is still in `dom(Σ.C)` by S0, but no longer in `ran(Σ_1.M(d₁))`. The link's coverage is unchanged — still the half-open interval `{t ∈ T : i₁ ≤ t < shift(i₁, 5)}`, of which `{i₁, i₂, i₃, i₄}` remain the traced members.

Now suppose another document `d₂` is registered and transcludes `i₄` via K.σ followed by K.μ⁺ (the accompanying K.ρ step required by ValidComposite★'s J1★ coupling, which records `(i₄, d₂) ∈ R`, is elided from the displayed arrangement since projection does not consult `R`), producing state `Σ_2`:
```
Σ_2.M(d₂) = {w₁ ↦ i₄}
project(a, 1, d₂, Σ_2) = {w₁}
```

The link is now discoverable from both `d₁` (where the projection is `{v₁, v₂, v₃}` reaching `{i₁, i₂, i₃}`) and `d₂` (where the projection is `{w₁}` reaching `{i₄}`). Together the two projections reach the four traced I-addresses `{i₁, i₂, i₃, i₄}` — the entirety of `coverage(e₁)` that bears on these documents' ranges — despite no single document containing all four.

*Branch point — alternative continuation from `Σ_1`.* The next step does *not* follow `Σ_2`. We return to `Σ_1` (the post-K.μ⁻ state, before any `d₂` registration) and explore a separate continuation that isolates K.μ~ behaviour. In this branch, `d₂` is never introduced; `dom(Σ_1.M)` retains its pre-`Σ_2` membership. We rename the post-K.μ~ state `Σ_3` to flag that it is a sibling of `Σ_2` under `Σ_1`, not a successor of `Σ_2`.

To exhibit projection motion clearly under K.μ~, consider slot 2 of the link, with endset `e₂ = {(i₁, δ(1, #i₁))}` — a single unit-width span (PrefixSpanCoverage form, ASN-0043) starting at `i₁`, where `δ(1, #i₁) = [0, ..., 0, 1]` of length `#i₁` is the canonical unit-depth ordinal displacement (OrdinalDisplacement, ASN-0034). The span `(i₁, δ(1, #i₁))` is well-formed by T12 since `Pos(δ(1, #i₁))` holds and `actionPoint(δ(1, #i₁)) = #i₁ ≤ #i₁`. By PrefixSpanCoverage (ASN-0043), `coverage(e₂) = {t ∈ T : i₁ ≼ t}`. Since `i₂, i₃, i₄` are sibling chain elements of `i₁` (sharing length `#i₁` but differing at the last component, by ASN-0093's chain enumeration via `inc(·, 0)`), none of them satisfies `i₁ ≼ ·` (a proper-prefix relation between equal-length tumblers would require equality by T3, which is ruled out by the distinct chain indices). Hence `coverage(e₂) ∩ {i₁, i₂, i₃, i₄} = {i₁}`, and so `coverage(e₂) ∩ ran(Σ_1.M(d₁)) = {i₁}` — only the I-address `i₁` from `d₁`'s current range lies in this slot's coverage. The construction is admissible by L4 of ASN-0043, which imposes no constraint on which I-addresses an endset references; we follow only the intersection with `d₁`'s range, since by LP12 that intersection is what governs projection through `d₁`. At `Σ_1`:
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
| LP4 | For `d ∈ dom(Σ.M) ∩ dom(Σ'.M)`: `Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)` — arrangement specificity (downstream lifts via M1 from `d ∈ dom(Σ.M)`) | introduced |
| LP5 | Cross-document independence: projection through `d` unaffected by edits to `d' ≠ d` (frames over K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) | introduced |
| LP6 | K.α (content allocation) does not displace any projection | introduced |
| LP7 | K.λ (link allocation) does not displace existing projections | introduced |
| LP8 | Document-registration invariance (K.σ of ASN-0093 or K.δ-IsDocument of ASN-0047): (a) `(A d ∈ dom(Σ.M) : project(e, d, Σ') = project(e, d, Σ))`; (b) `project(e, d_new, Σ') = ∅` | introduced |
| LP14 | K.ρ (provenance recording) does not displace any projection | introduced |
| LP9 | K.μ⁺ and K.μ⁺_L can only enlarge projection; new V-positions come from new arrangement entries | introduced |
| LP10 | K.μ⁻ can only shrink projection; lost V-positions come from removed arrangement entries | introduced |
| LP11 | K.μ~ rebinds projection: `project(e, d, Σ') = π(project(e, d, Σ))` via bijection π | introduced |
| LP-Comp | Composite displacement across reachable `Σ →* Σ'`: decomposition into atomic steps each governed by exactly one of LP4–LP14; induction-on-chain-length composes per-step displacements (cumulative growth from chains of LP9, cumulative shrinkage from chains of LP10, cumulative bijection from chains of LP11); discharges multi-step claims (LP18, LP19) that quantify over reachable sequences. | introduced |
| discoverable_from | `discoverable_from(a, d, Σ) ≡ (E i : project(a, i, d, Σ) ≠ ∅)` (defined when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`) | introduced |
| LP12 | `discoverable_from(a, d, Σ) ⟺ (E i : coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)` | introduced |
| LP12a | Contraction discoverability wp: `wp(K.μ⁻[d, R], discoverable_from(a, d, ·)) ≡ (E i : project(a, i, d, Σ) ∩ R ≠ ∅)`, where `R` is the K.μ⁻ retention set; reduces to `false` at `R = ∅` | introduced |
| LP12b | Discharges LP12a's content-canonical-link-subspace boundary case: for `a ∈ dom(Σ.L)` whose every span is canonical with `s = [d_s, 0, s_C, k_s]`, and any K.μ⁻ retention parameters `n'_{s_C} = 0, n'_{s_L} > 0`, the wp evaluates to `false` — derived via LP-Fin Corollary applied at `X = s_C` to give `coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅` | introduced |
| LP13 | Unconditional link persistence: `Σ →* Σ' ∧ a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)` — independent of any discoverability | introduced |
| LP16 | Transclusion confers discoverability: shared I-addresses transfer discoverability across documents | introduced |
| LP17 | Ghost projection: orphaned links persist in `dom(Σ.L)` with empty projections everywhere | introduced |
| LP18 | Resurrection: re-introducing a coverage I-address via K.μ⁺ or K.μ⁺_L restores discoverability | introduced |
| tight | `tight(e, Σ_e)` ≡ every span `(s, ℓ) ∈ e` is canonical (`ℓ = δ(n, #s)` for some `n ≥ 1`), `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)`, and every substrate-emittable address in `[s, s ⊕ ℓ)` is allocated at `Σ_e`. Non-canonical spans are unconditionally non-tight at every state. | introduced |
| LP-Fin | Interval finitude (canonical): `(A s, ℓ : s ∈ F ∧ ℓ = δ(n, #s) for some n ≥ 1 : |F ∩ [s, s ⊕ ℓ)| < ∞)` — only finitely many `F`-candidates fall within any canonical span's reach. Non-canonical spans are unconditionally non-tight on two structurally distinct grounds: (i) `#ℓ < #s` and (ii) `#ℓ = #s` with `ℓ` non-ordinal (`actionPoint(ℓ) < #s`) both yield `|F ∩ [s, s ⊕ ℓ)| = ℵ₀` (finitude failure, by the within-chain construction); (iii) `#ℓ > #s` is excluded by the tightness predicate's *definitional* canonical-form requirement `ℓ = δ(n, #s)`. | introduced |
| LP-Fin Corollary | Canonical interval characterisation: for canonical `(s, ℓ)` with `s = [d_0, 0, X, k_s]` and `ℓ = δ(n, #s)`, `F ∩ [s, s ⊕ ℓ) = {[d_0, 0, X, k] : k_s ≤ k < k_s + n}` — every F-candidate in the interval inherits the span's subspace identifier `X` and origin `d_0`. Used in LP12a's boundary case to derive `coverage ∩ dom(L) = ∅` from content-subspace canonical construction. | introduced |
| LP19a | Tight freshness: under tight construction, K.α/K.λ-allocated addresses fall outside `coverage(e)` | introduced |
| LP19 | Tight endset boundary exclusion: K.μ⁺/K.μ⁺_L mapping to such an address cannot grow `project(e, d, ·)` | introduced |
| LP20 | Range confinement: `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = coverage(e) ∩ ran(Σ.M(d))`; corollary via S3★ gives `⊆ coverage(e) ∩ (dom(Σ.C) ∪ dom(Σ.L))`; per-subspace refinement partitions the range into content-subspace and link-subspace components via S3★-aux | introduced |
| LP21 | Representation invariance: equal coverage implies equal projection | introduced |

*Numbering note.* Labels LP1, LP15 are deliberately absent. LP14 and LP15 from earlier drafts of this ASN were collapsed in revision; LP14 has been reclaimed here to label the K.ρ frame lemma added in this revision. LP1 was never assigned. LP19a is introduced in this revision to separate the tight-freshness claim from its projection consequence (LP19); both labels are introduced here. LP-Fin (the interval-finitude lemma) is introduced in the current revision to discharge the decidability claim of the tightness predicate's universal quantifier over `F`; this revision restricts LP-Fin to canonical spans (`#ℓ = #s` with `ℓ` an ordinal displacement) — the earlier general statement is unsound because non-canonical spans admit infinitely many `F`-candidates within their reach, and the tightness predicate is now confined to canonical spans on which the universal quantifier is finitely discharged. Non-canonical spans are unconditionally non-tight. The LP-Fin Corollary (CanonicalIntervalCharacterisation) was added in the current revision to make LP-Fin's structural content explicit: the finitude proof's case decomposition not only bounds `|F ∩ [s, s ⊕ ℓ)|` but characterises the intersection exactly as the `n`-element chain segment rooted at the span's start. This sharpening is what LP12a's boundary case (content-subspace empty, link-subspace retained) needs to derive `coverage ∩ dom(L) = ∅` from canonical content-subspace construction. LP12a is introduced in this revision to supply the explicit weakest-precondition derivation for discoverability preservation under K.μ⁻ — the building blocks were already present (LP10's exact-difference formula and LP12's coverage-range characterisation), but the wp synthesis was left implicit. LP12b is introduced in this revision to give the deferred discharge of LP12a's content-canonical-link-subspace boundary case a tracked label — the earlier revision named the discharge "LP12a Boundary Case Application" inline, leaving the forward reference from the Discoverability and Survival section pointing at an unlabelled passage that did not appear in the master claims table. LP-Comp (CompositeDisplacement) is introduced in this revision to make explicit the composition principle that earlier drafts left implicit: any reachable `Σ →* Σ'` decomposes into atomic transitions each governed by exactly one of LP4–LP14, with cumulative displacement obtained by composition; this principle underwrites the multi-step claims LP18 and LP19 without requiring their proofs to re-derive intermediate-state projection evolution. Other labels (LP2 through LP21, omitting LP15) preserve their revision-history identities.

## Open Questions

What invariants must a reverse-discovery primitive preserve when, given a V-position in some document, it returns the set of links whose projections contain that V-position?

Under what conditions must the projection of an endset through a document be expressible as a finite union of contiguous V-ranges, given that K.μ~ can scatter formerly contiguous projections into arbitrary subsets of the V-domain?

What guarantees must the system provide about the *V-order* of positions within a single projection — does the V-order of projected positions reflect the I-order of their underlying I-addresses, and under what arrangement-shape conditions is this reflection preserved by K.μ~?

What invariants must the system maintain when a link's endset references the address of another link (rather than content) — under what conditions must the discovery of one link induce the discovery of the other?

Under what conditions must the system commit to producing identical projections for two documents that have undergone "the same" sequence of editing operations, given that arrangement state is per-document and operations are not directly comparable across documents?

What invariants must hold across a fork composite when the source document's link-subspace V-positions are not transcluded into the new document — how does this affect the projection of the source document's home-document-allocated links through the new document?
