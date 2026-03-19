# ASN-0048: INSERT Operation

*2026-03-18*

We ask: what happens when new content enters a document? The question sounds simple — an editor types a character; the system accommodates it. But accommodating it means several things at once: allocating permanent storage, rearranging a mutable structure, preserving every guarantee the system has made to every other document and every link in the docuverse. We want to know what INSERT must do, what it must not do, and what invariants it must preserve.

The two-space architecture (ASN-0036) gives us the framework. Content lives permanently in the store Σ.C : T ⇀ Val; each document d arranges a selection of that content via Σ.M(d) : T ⇀ T. INSERT must work in both spaces — it creates content in C (permanent, irrevocable) and rearranges M(d) to accommodate the new content (mutable, local). Every other component of the system state — every other document's arrangement, every provenance record, every entity — must survive undisturbed.

We develop the specification by asking what must be true afterward and working backward to what must happen.


## Content allocation

INSERT introduces content that has never existed. By K.α (ASN-0047), fresh content is allocated at an address a ∉ dom(C) with C'(a) = v for some value v ∈ Val. The precondition K.α(pre) demands IsElement(a) ∧ origin(a) ∈ E_doc — the address must be element-level and scoped to an existing document's prefix.

When we INSERT n content values into document d, we require n allocation events, producing addresses a₁, ..., aₙ. These addresses are not arbitrary; they are governed by the allocation discipline.

**I0** (*sequential allocation*). INSERT into document d allocates addresses a₁, ..., aₙ (n ≥ 1) such that:

(a) `(A i : 1 ≤ i ≤ n : aᵢ ∉ dom(C))` — freshness

(b) `(A i : 1 ≤ i ≤ n : origin(aᵢ) = d)` — scoped to d

(c) `(A i : 1 ≤ i < n : aᵢ < aᵢ₊₁)` — mutually ordered

(d) `(A a ∈ dom(C) : origin(a) = d : a < a₁)` — beyond all prior content of d

(e) `(A i : 1 ≤ i ≤ n : aᵢ = a₁ ⊕ [i − 1])` — contiguous block

Clause (c) follows from T9 (ForwardAllocation, ASN-0034) applied to the n sequential allocations within the same INSERT. Clause (e) — contiguity — follows from T10a (AllocatorDiscipline, ASN-0034): each sibling allocation is `inc(·, 0)`, which by TA5(c) increments at `sig(t)` by exactly 1. Since `inc(·, 0)` on an element-level address operates on the element ordinal — the last significant component — while the document prefix N.0.U.0.D.0 remains unchanged, we adopt an *ordinal-only formulation for I-addresses* analogous to TA7a's V-space formulation: within a single document's allocation stream, an I-address with element ordinal x is represented as `[x]` for arithmetic purposes, with the document prefix held as structural context. Closure follows by the same reasoning as TA7a: `[x] ⊕ [n] = [x + n]`, which under the full address is P.(x + n) for document prefix P — still under the same prefix. Then `a₁ = [x]` and `inc([x], 0) = [x + 1]`, so `a₂ = [x + 1] = a₁ ⊕ [1]`; by induction, `aᵢ = a₁ ⊕ [i − 1]`.

Clause (d) requires that a₁ exceeds every prior allocation under d's prefix. INSERT allocates exclusively via `inc(·, 0)` — sibling increments, no child spawning (T10a permits child spawning only via `inc(·, k')` with `k' > 0`, which INSERT does not use). Therefore d's entire content allocation history is a single sequential stream, and T9 directly orders every prior allocation before a₁.

Together (c) through (e) yield a contiguous block — n addresses in a row, all fresh, all scoped to d, all beyond anything d has ever allocated.

The conjunction of (a) through (d) has an immediate consequence for content identity. Two independent INSERTs of identical text produce distinct addresses. If document d₁ inserts "hello" and document d₂ independently inserts "hello," the resulting I-addresses occupy different ownership prefixes (by S7a and T10, ASN-0034). Even within the same document, if we delete content and later re-insert identical text, the new addresses are fresh — they do not reclaim the old ones. This is S4 (OriginBasedIdentity, ASN-0036) in action: identity is creation, not value. The I-address distinguishes "wrote the same words" from "quoted from the original." Nelson is unambiguous: two documents with identical text created independently have different I-addresses; transcluded content shares the same I-address. The address IS the distinction.


## The V-space shift

The arrangement M(d) maps V-positions to I-addresses. To insert n values at V-position p, we must make room: every existing mapping at or beyond p shifts forward by n, opening a gap into which the new content is placed. Nelson describes this directly: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

We work within a single subspace of document d's V-space — the text subspace, with subspace identifier s ≥ 1 (by S8a, ASN-0036). By S8-depth, all V-positions in this subspace share a common tumbler depth. By TA7a (SubspaceClosure, ASN-0034), arithmetic within the subspace reduces to natural-number addition on ordinals, with the subspace identifier held as structural context. We write ord(v) for the ordinal of V-position v within its subspace.

**Definition (V-shift).** For insertion point p with ord(p) = p̂ and width n ≥ 1, define the shift function σ on positions in dom(M(d)):

`σ(v) = v` when ord(v) < p̂ or v is not in the text subspace

`σ(v) = v ⊕ [n]` when v is in the text subspace and ord(v) ≥ p̂

where v ⊕ [n] denotes the V-position with ord(v ⊕ [n]) = ord(v) + n in the same subspace (well-defined by TA7a). The shift is the identity on every position outside the text subspace and on every text position before the insertion point.

We require four properties.

**I1** (*shift injectivity*). σ is injective on dom(M(d)).

*Derivation.* Consider distinct v₁, v₂ ∈ dom(M(d)). If neither is a text-subspace position at or beyond p̂, both map to themselves — distinct. If both are text-subspace positions with ordinal ≥ p̂, then ord(v₁) ≠ ord(v₂) gives ord(v₁) + n ≠ ord(v₂) + n — distinct. If exactly one has ordinal ≥ p̂ and the other has ordinal < p̂ (both in the text subspace), their images have ordinals < p̂ and ≥ p̂ + n respectively — distinct, since n ≥ 1 so p̂ + n > p̂. If they are in different subspaces, T7 (SubspaceDisjoint, ASN-0034) ensures the identity-mapped position differs from any shifted text position. ∎

**I2** (*order preservation*). For v₁, v₂ in the text subspace of dom(M(d)) with v₁ < v₂: σ(v₁) < σ(v₂).

*Derivation.* Three cases. Both below p̂: σ(v₁) = v₁ < v₂ = σ(v₂). Both at or above p̂: ord(v₁) < ord(v₂) gives ord(v₁) + n < ord(v₂) + n, hence σ(v₁) < σ(v₂). Mixed (v₁ below, v₂ at or above): σ(v₁) = v₁ with ordinal < p̂, and σ(v₂) with ordinal ≥ p̂ + n > p̂. Since within a subspace the ordinal determines the order (TA7a), σ(v₁) < σ(v₂). ∎

**I3** (*gap creation*). No position in dom(M(d)) maps under σ to a V-position with text-subspace ordinal in [p̂, p̂ + n).

*Derivation.* Positions with ordinal < p̂ map to themselves — ordinals still < p̂, outside the gap. Positions with ordinal ≥ p̂ map to ordinals ≥ p̂ + n — past the gap. Non-text-subspace positions map to themselves, remaining outside the text subspace. ∎

**I4** (*subspace confinement*). σ is the identity on every position whose subspace identifier differs from s. σ maps every text-subspace position to a text-subspace position.

The first clause follows from the definition. The second from TA7a: within a subspace, adding a positive ordinal displacement yields a position in the same subspace.

The conjunction of I1 through I4 tells us that σ is an order-preserving injection from dom(M(d)) into T that creates exactly the gap we need and disturbs nothing outside its subspace. This is the abstract content of the "gap-making" operation. The implementation achieves it in O(log N) time by modifying displacement fields at internal tree nodes, propagating the shift to all descendants without visiting them individually. That efficiency is valuable but implementation-specific; what any implementation must satisfy is the four properties above.


## INSERT as composite transition

We assemble the full operation. INSERT of values v₁, ..., vₙ into document d at V-position p is a composite transition (ASN-0047, ValidCompositeTransition) consisting of four phases.

**Phase 1** — *Content allocation* (K.α × n). For each i from 1 to n, allocate I-address aᵢ with C₁(aᵢ) = vᵢ. After this phase, dom(C₁) = dom(C) ∪ {a₁, ..., aₙ}. Frame: E₁ = E; M₁ = M; R₁ = R.

**Phase 2** — *Arrangement shift* (K.μ~). Apply the bijection σ to M(d)'s domain:

`(A v : v ∈ dom(M(d)) : M₂(d)(σ(v)) = M(d)(v))`

with dom(M₂(d)) = σ(dom(M(d))). This is a valid K.μ~ reordering: σ is injective (I1), and ran(M₂(d)) = ran(M(d)) since only V-positions change. Frame: C₂ = C₁; E₂ = E; R₂ = R; M₂(d') = M(d') for d' ≠ d.

When dom(M(d)) contains no text-subspace positions with ordinal ≥ p̂ — the append case, or insertion into an empty document — σ is the identity on all of dom(M(d)), and Phase 2 is a no-op.

**Phase 3** — *Arrangement extension* (K.μ⁺). Add n new mappings at the V-positions in the gap. Let pₖ denote the text-subspace V-position with ordinal p̂ + k, for 0 ≤ k < n. Then:

`(A k : 0 ≤ k < n : M'(d)(pₖ) = aₖ₊₁)`

The precondition for K.μ⁺ requires each aₖ₊₁ ∈ dom(C'), satisfied because Phase 1 placed them there and Phase 2 did not modify C. The new V-positions satisfy S8a (all components positive: subspace identifier s ≥ 1, ordinal p̂ + k ≥ p̂ ≥ 1) and S8-depth (same depth as p, which shares the subspace's common depth). Frame: C' = C₁; E' = E; R' = R; M'(d') = M(d') for d' ≠ d.

**Phase 4** — *Provenance recording* (K.ρ × n). For each i, record (aᵢ, d) ∈ R'. Frame: C' unchanged; E' unchanged; M' unchanged.

We verify the coupling constraints of ASN-0047:

- **J0** (AllocationRequiresPlacement): Each aᵢ ∈ dom(C') \ dom(C) appears at M'(d)(pᵢ₋₁) via Phase 3. ✓

- **J1** (ExtensionRecordsProvenance): Each aᵢ ∈ ran(M'(d)) \ ran(M(d)) has (aᵢ, d) ∈ R' via Phase 4. The set membership holds because aᵢ ∉ dom(C) (by I0(a)), and S3 (ReferentialIntegrity, ASN-0036) gives ran(M(d)) ⊆ dom(C), so aᵢ ∉ ran(M(d)). ✓

- **J1'** (ProvenanceRequiresExtension): Each (aᵢ, d) ∈ R' \ R satisfies aᵢ ∈ ran(M'(d)) \ ran(M(d)), established by the same argument as J1. ✓

The intermediate states satisfy their elementary preconditions: K.α requires origin(aᵢ) ∈ E_doc (satisfied since d ∈ E_doc, by I-pre below); K.μ~ requires d ∈ E_doc (E is unchanged across phases); K.μ⁺ requires aᵢ ∈ dom(C₂) (satisfied since Phase 1 allocated them and Phase 2's frame holds C₂ = C₁); K.ρ requires aᵢ ∈ dom(C') ∧ d ∈ E_doc (both satisfied).

We now state the precondition, postcondition, and frame.

**I-pre** (*INSERT precondition*). `d ∈ E_doc ∧ n ≥ 1 ∧ S8a(p)` — the document exists, at least one value is inserted, and the insertion point is a well-formed text-subspace V-position.

**I-post** (*INSERT postcondition*). The post-state Σ' = (C', E', M', R') satisfies:

(a) `dom(C') = dom(C) ∪ {a₁, ..., aₙ}` with `(A i :: C'(aᵢ) = vᵢ)` and `(A a ∈ dom(C) :: C'(a) = C(a))`

(b) `E' = E`

(c) `(A d' : d' ≠ d : M'(d') = M(d'))`

(d) `dom(M'(d)) = σ(dom(M(d))) ∪ {pₖ : 0 ≤ k < n}`

(e) `(A v ∈ dom(M(d)) :: M'(d)(σ(v)) = M(d)(v))`

(f) `(A k : 0 ≤ k < n : M'(d)(pₖ) = aₖ₊₁)`

(g) `R' = R ∪ {(aᵢ, d) : 1 ≤ i ≤ n}`

**I-frame** (*INSERT frame*). What INSERT does not change:

(a) `(A a ∈ dom(C) :: C'(a) = C(a))` — existing content untouched

(b) `E' = E` — no entity created or destroyed

(c) `(A d' : d' ≠ d : M'(d') = M(d'))` — other documents untouched

(d) `R' ⊇ R` — existing provenance preserved


## Preservation

We verify that INSERT maintains the invariants established by ASN-0036 and ASN-0047. The method: check each invariant against I-post.

**S0 (ContentImmutability).** For every a ∈ dom(C): a ∈ dom(C') and C'(a) = C(a). This is I-post(a) directly. INSERT extends C without modifying existing entries. We can state this as a weakest-precondition obligation:

`wp(INSERT, (A a : a ∈ dom(C) : C'(a) = C(a)))`
`= {I-frame(a)}`
`(A a : a ∈ dom(C) : C(a) = C(a))`
`= true`

**S3 (ReferentialIntegrity).** We ask: what must hold before INSERT for every V-position in dom(M'(d)) to map to an address in dom(C')? Working backward:

`wp(INSERT, (A v : v ∈ dom(M'(d)) : M'(d)(v) ∈ dom(C')))`

The domain splits into shifted positions σ(dom(M(d))) and new positions {pₖ}. For shifted positions, M'(d)(σ(v)) = M(d)(v), and Phases 2–4 hold C in their frame, so dom(C') = dom(C₁) = dom(C) ∪ {a₁, ..., aₙ}. The pre-state S3 gives M(d)(v) ∈ dom(C) ⊆ dom(C'). For new positions, M'(d)(pₖ) = aₖ₊₁, and we need aₖ₊₁ ∈ dom(C'). This holds because Phase 1 allocated aₖ₊₁ into C₁ and the frame conditions of Phases 2–4 preserve C₁ = C'. The phase ordering is load-bearing: Phase 1 (allocation) must precede Phase 3 (extension). If we swapped them — extending M(d) before allocating — then at the point K.μ⁺ executes, aₖ₊₁ ∉ dom(C), violating the K.μ⁺ precondition that each new mapping target an existing I-address.

**S2 (ArrangementFunctional)** for M'(d). We must show M'(d) is a function — no V-position has two images. The domain is σ(dom(M(d))) ∪ {pₖ : 0 ≤ k < n}. By I3 (gap creation), these two sets are disjoint: σ maps no position into the gap [p̂, p̂ + n), and the new positions lie exactly in that gap. Within each set, the mapping is functional: σ(dom(M(d))) inherits functionality from M(d) via the bijection σ; the new positions map injectively to a₁, ..., aₙ (which are distinct by I0(c)). ✓

**S8a (VPositionWellFormed).** Shifted positions σ(v) satisfy S8a because v does and the shift preserves the subspace identifier while adding a positive integer to a positive ordinal. New positions pₖ: the subspace identifier s ≥ 1 and the ordinal p̂ + k ≥ p̂ ≥ 1, so all components are strictly positive; zeros(pₖ) = 0 by construction. ✓

**S8-depth (FixedDepthPositions).** In the ordinal-only formulation per TA7a (ASN-0034), all text-subspace positions are single-component tumblers `[x]` with uniform depth 1. The shift does not change tumbler depth — adding a positive ordinal displacement yields another single-component tumbler. New positions pₖ = [p̂ + k] have the same depth 1. ✓

**S8-fin (FiniteArrangement).** dom(M(d)) is finite (pre-state); σ(dom(M(d))) has the same cardinality (σ is injective); adding n new positions yields |dom(M'(d))| = |dom(M(d))| + n, still finite. ✓

**P0 (ContentPermanence).** By I-frame(a). ✓

**P1 (EntityPermanence).** By I-post(b): E' = E ⊇ E. ✓

**P2 (ProvenancePermanence).** By I-post(g): R' = R ∪ {...} ⊇ R. ✓

**P4 (ProvenanceBounds).** We need Contains(Σ') ⊆ R', where Contains(Σ') = {(a, d') : d' ∈ E'_doc ∧ a ∈ ran(M'(d'))}. For (a, d') ∈ Contains(Σ'): if d' ≠ d, then M'(d') = M(d') by I-frame(c), so a ∈ ran(M(d')), giving (a, d') ∈ Contains(Σ) ⊆ R ⊆ R'. If d' = d, then either a ∈ ran(M(d)) (giving (a, d) ∈ Contains(Σ) ⊆ R ⊆ R') or a = aᵢ for some i (giving (aᵢ, d) ∈ R' by Phase 4). ✓

**P6 (ExistentialCoherence).** For fresh aᵢ ∈ dom(C') \ dom(C): origin(aᵢ) = d by I0(b), and d ∈ E_doc by I-pre, and E'_doc = E_doc by I-post(b), so origin(aᵢ) ∈ E'_doc. For existing a ∈ dom(C): pre-state P6 gives origin(a) ∈ E_doc = E'_doc. ✓

**P7 (ProvenanceGrounding).** For (aᵢ, d) ∈ R' \ R: aᵢ ∈ dom(C') by Phase 1. For (a, d') ∈ R: pre-state P7 gives a ∈ dom(C), and S1 gives dom(C) ⊆ dom(C'), so a ∈ dom(C'). ✓

**P7a (ProvenanceCoverage).** For fresh aᵢ ∈ dom(C') \ dom(C): (aᵢ, d) ∈ R' by Phase 4. For existing a ∈ dom(C): pre-state P7a gives (a, d') ∈ R for some d', and P2 gives R ⊆ R'. ✓


## Document isolation

Clause I-frame(c) — `(A d' : d' ≠ d : M'(d') = M(d'))` — deserves emphasis. It states that inserting content into document d cannot alter any other document's arrangement. Nelson is unequivocal: "Adding content to a document does not affect any other document." The mechanism is the two-space separation.

INSERT creates new I-addresses (which no other document references, since they are fresh) and shifts V-positions (which are local to d's arrangement). The frame conditions of each elementary transition confirm this: K.α holds all M in its frame; K.μ~ holds all M(d') for d' ≠ d in its frame; K.μ⁺ holds all M(d') for d' ≠ d in its frame; K.ρ holds all M in its frame.

We can make this sharper. Consider a document d' ≠ d that transcludes content from d — some a ∈ ran(M(d')) ∩ ran(M(d)). After INSERT into d:

- The content at a is unchanged: C'(a) = C(a) by S0.
- The address a remains in dom(C') by S1.
- The arrangement M'(d') = M(d') by isolation.

The transcluding document's arrangement points to the same I-addresses, which contain the same values. Not only is d' unaware that d was edited — there is nothing to be aware of. The I-space content that d' references has not been touched at any level.


## Subspace confinement

Property I4 confines the shift to the text subspace. We record the arrangement-level consequence.

**I5** (*subspace isolation*). INSERT into the text subspace of d does not alter d's link subspace arrangement:

`(A v ∈ dom(M(d)) : v₁ ≠ s : M'(d)(v) = M(d)(v))`

where s is the text subspace identifier. The link endpoints — from-endsets, to-endsets, type-endsets in subspaces distinct from s — remain at their original V-positions with their original I-address mappings.

The implementation achieves this by computing the shift boundary as the first position of the next subspace, `(s+1).1`, purely from the insertion address by tumbler arithmetic, without inspecting any data structure. Abstractly, the guarantee follows from I4 and T7 (SubspaceDisjoint, ASN-0034): σ is defined as the identity on every position whose subspace identifier differs from s, so no link-subspace position is moved. The shift, bounded to text-subspace ordinals, cannot reach into the link subspace — T7 ensures disjointness by the leading subspace component. Any implementation must ensure this separation — the V-shift operates within a single subspace and does not propagate across subspace boundaries.


## Link survival

We do not formalize links in this ASN, but we observe a critical consequence. Links in Xanadu attach to I-space addresses — to content identity, not V-space position. Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." A link endset is a set of I-space addresses.

INSERT creates fresh I-addresses (no existing link references them) and shifts V-positions (which links do not reference). Therefore:

**I6** (*link survival*). For any structure that references a set of I-addresses L ⊆ dom(C):

(a) `(A a ∈ L :: a ∈ dom(C'))` — every referenced address persists (by S1)

(b) `(A a ∈ L :: C'(a) = C(a))` — content at each address is unchanged (by S0)

(c) L itself is not modified — INSERT touches only C (by extension), M(d) (by shift and extension), and R (by extension). No other state component is altered.

Nelson states the survivability guarantee: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." For INSERT, the "if anything is left" clause is trivially satisfied — INSERT adds content, it never removes any. No byte at any link endset can be lost to an INSERT. The link survives with its full original content intact.


## Correspondence runs under INSERT

The arrangement's text subspace decomposes into correspondence runs (S8, ASN-0036): triples (v, a, n) where M(d)(v ⊕ [k]) = a ⊕ [k] for 0 ≤ k < n, meaning n consecutive V-positions map to n consecutive I-addresses. We trace how INSERT transforms this decomposition.

Let {(vⱼ, aⱼ, nⱼ) : 1 ≤ j ≤ m} be the pre-INSERT run decomposition, ordered so that ord(v₁) < ord(v₂) < ... < ord(vₘ). Let p̂ = ord(p) be the insertion ordinal and w = n the insertion width.

We partition the existing runs into three classes relative to p̂:

- *Before*: runs with ord(vⱼ) + nⱼ ≤ p̂ (entirely before the insertion point)
- *After*: runs with ord(vⱼ) ≥ p̂ (entirely at or after the insertion point)
- *Split*: runs with ord(vⱼ) < p̂ < ord(vⱼ) + nⱼ (the insertion point falls in their interior)

At most one run can be split, because the runs partition the V-positions and have disjoint ordinal ranges.

**I7** (*run transformation*). After INSERT of w values at ordinal p̂ with fresh I-addresses starting at a_new, one valid post-state run decomposition is:

(a) *Before-runs* are unchanged: (vⱼ, aⱼ, nⱼ). They lie entirely below p̂; σ is the identity on them. The I-address mappings are preserved by I-post(e).

(b) *After-runs* are V-shifted: (vⱼ', aⱼ, nⱼ) where ord(vⱼ') = ord(vⱼ) + w. The I-addresses are unchanged; only V-positions move. The correspondence property is preserved: M'(d)(vⱼ' ⊕ [k]) = M(d)(vⱼ ⊕ [k]) = aⱼ ⊕ [k] for 0 ≤ k < nⱼ.

(c) *Split run*: if run (vⱼ, aⱼ, nⱼ) is split at offset δ = p̂ − ord(vⱼ) where 0 < δ < nⱼ, it becomes two runs. The *left fragment* (vⱼ, aⱼ, δ) is unchanged — all its positions have ordinal < p̂. The *right fragment* has V-start at ordinal ord(vⱼ) + δ + w, I-start at aⱼ ⊕ [δ], and width nⱼ − δ. Its correspondence (using the I-address ordinal-only formulation): M'(d)((ord(vⱼ) + δ + w) + k) = M(d)((ord(vⱼ) + δ) + k) = aⱼ ⊕ [δ + k] = (aⱼ ⊕ [δ]) ⊕ [k] for 0 ≤ k < nⱼ − δ. (The last equality uses associativity of tumbler addition, ASN-0034.)

(d) *New run*: (p, a₁, w) — the freshly inserted content. Its correspondence: M'(d)(p̂ + k) = aₖ₊₁ = a₁ ⊕ [k] for 0 ≤ k < w, by I-post(f) and I0(e) (contiguity: aₖ₊₁ = a₁ ⊕ [k]).

The new content always forms a single correspondence run of width w. This is a direct consequence of I0(e): the w fresh I-addresses are contiguous, and the w gap positions are sequential by construction.

**I8** (*run count bound*). If m is the number of correspondence runs before INSERT, the number after is at most m + 2.

*Derivation.* Before-runs contribute their original count. After-runs contribute their original count (shifted but not split). At most one run is split into two fragments (contributing +1 to the count). The new run contributes +1. Total: m − 1 (the split run is gone) + 2 (its fragments) + 1 (new run) = m + 2 when a split occurs. When the insertion point falls between runs or at the edge of the arrangement, no split occurs and the count is m + 1. ∎

This bound is abstract — it constrains any implementation. Each INSERT adds bounded complexity to the arrangement's run structure. Note that I7 gives one valid decomposition — the canonical non-coalesced form. Since S8 (ASN-0036) guarantees existence of a decomposition but not uniqueness, adjacent runs may be merged when two conditions hold simultaneously: (1) the insertion point falls at a run boundary (V-position adjacency), and (2) the new run's I-start a₁ equals the left neighbor's I-end + 1 (I-address contiguity). Condition (2) requires no intervening allocations under d's prefix since the neighbor's content was allocated — the sequential-typing scenario. When both conditions hold, the coalesced decomposition has fewer runs than I8's bound; I8 bounds the non-coalesced count.


## Worked example

We verify the postconditions against concrete values. Let document d have arrangement M(d) = {[1] ↦ a, [2] ↦ b, [3] ↦ c, [4] ↦ d_addr} where a, b, c, d_addr are consecutive I-addresses with a = [x], b = [x+1], c = [x+2], d_addr = [x+3] for some x. This is a single correspondence run ([1], a, 4). We INSERT w = 2 values (v₁, v₂) at ordinal p̂ = 3.

**Phase 1** (allocation). I0 produces fresh addresses a₅ = [y], a₆ = [y+1] (contiguous by I0(e): a₆ = a₅ ⊕ [1]), with y > x + 3 (by I0(d): beyond all prior content of d).

**Phase 2** (shift). σ is the identity on positions with ordinal < 3, and shifts by 2 for ordinal ≥ 3:

- σ([1]) = [1], σ([2]) = [2] — below p̂, unchanged
- σ([3]) = [3] ⊕ [2] = [5], σ([4]) = [4] ⊕ [2] = [6] — shifted by w = 2

After Phase 2: M₂(d) = {[1] ↦ a, [2] ↦ b, [5] ↦ c, [6] ↦ d_addr}. Positions [3] and [4] are vacant — this is the gap (I3).

**Phase 3** (extension). Fill the gap: M'(d)([3]) = a₅, M'(d)([4]) = a₆.

Post-state arrangement: M'(d) = {[1] ↦ a, [2] ↦ b, [3] ↦ a₅, [4] ↦ a₆, [5] ↦ c, [6] ↦ d_addr}.

**Verification of I-post.** (d): dom(M'(d)) = {[1],[2],[5],[6]} ∪ {[3],[4]} = σ(dom(M(d))) ∪ {pₖ}. ✓ (e): M'(d)(σ([1])) = M'(d)([1]) = a = M(d)([1]), and similarly for [2], [3]→[5], [4]→[6]. ✓ (f): M'(d)([3]) = a₅ = a₅ ⊕ [0] and M'(d)([4]) = a₆ = a₅ ⊕ [1]. ✓

**Verification of I7 (run decomposition).** The original run ([1], a, 4) is split at δ = p̂ − ord(v₁) = 3 − 1 = 2:

- *Left fragment*: ([1], a, 2). Check: M'(d)([1+k]) = a ⊕ [k] for k = 0, 1 — M'(d)([1]) = a, M'(d)([2]) = b = a ⊕ [1]. ✓
- *New run*: ([3], a₅, 2). Check: M'(d)([3+k]) = a₅ ⊕ [k] for k = 0, 1 — M'(d)([3]) = a₅, M'(d)([4]) = a₆ = a₅ ⊕ [1]. ✓
- *Right fragment*: ([5], c, 2) with I-start a ⊕ [2] = c. Check: M'(d)([5+k]) = c ⊕ [k] for k = 0, 1 — M'(d)([5]) = c, M'(d)([6]) = d_addr = c ⊕ [1]. ✓

Pre-state: 1 run. Post-state: 3 runs = 1 + 2, confirming I8. **Phase 4** records (a₅, d) and (a₆, d) in R'.


## Invertibility and history

The V-shift σ is invertible. Given the insertion parameters (p̂, w), define the inverse:

`σ⁻¹(v) = v` when ord(v) < p̂

`σ⁻¹(v) = v ⊖ [w]` when ord(v) ≥ p̂ + w

where v ⊖ [w] is the position with ordinal ord(v) − w (well-defined by TA7a for ord(v) ≥ p̂ + w ≥ w + 1 > w). Positions with ordinal in [p̂, p̂ + w) — the inserted content — have no pre-image; they did not exist before INSERT.

**I9** (*INSERT invertibility*). The transition Σ →_{INSERT(d,p,n)} Σ' is invertible: given Σ' and (d, p, n), the pre-state Σ is uniquely determined.

*Derivation.* We recover each component:

- C: identify the fresh addresses as A_new = {M'(d)(pₖ) : 0 ≤ k < n}, then C = C' restricted to dom(C') \ A_new. The identification is correct because I0(a) guarantees A_new ∩ dom(C) = ∅.
- E: E = E' by I-post(b).
- M(d): remove the gap mappings from M'(d) and apply σ⁻¹ to the remaining positions. That is, M(d)(σ⁻¹(v)) = M'(d)(v) for v ∈ dom(M'(d)) with ord(v) ∉ [p̂, p̂ + n).
- M(d') for d' ≠ d: M(d') = M'(d') by I-frame(c).
- R: R = R' \ {(aᵢ, d) : 1 ≤ i ≤ n} where each aᵢ = M'(d)(pᵢ₋₁). The subtraction is correct because aᵢ ∉ dom(C) (by I0(a)), so by the contrapositive of P7 (ProvenanceGrounding, ASN-0047) — `(a, d) ∈ R ⟹ a ∈ dom(C)` — we have (aᵢ, d) ∉ R. Therefore R' \ {(aᵢ, d)} removes exactly what Phase 4 added.

Each component is uniquely determined. ∎

This invertibility is the formal backbone of Nelson's guarantee that "any previous instant can be reconstructed." The content store C grows monotonically (P0) and the provenance record R grows monotonically (P2); neither loses information. The arrangement M(d) changes non-monotonically — old V-positions are replaced by shifted V-positions — but the shift is a bijection parameterised by (p̂, w), and the new content is identifiable by its position in the gap. The pre-INSERT state is not stored as a separate snapshot; it is *computable* from the post-state and the operation parameters. Nelson's "append-only storage" combined with the algebraic structure of the shift makes history reconstruction a matter of arithmetic, not archive retrieval.


## Content identity and provenance

INSERT severs provenance from any external origin. If content is composed outside the system and INSERTed as new text, the system assigns fresh I-addresses under the inserting document's prefix. No structural record connects the new content to its external origin. Nelson is explicit: "If content was originally composed elsewhere and is then INSERTed as fresh text, the system assigns it new I-addresses... The connection to its prior existence is severed."

This is by design. The system preserves connections *within* the docuverse — transclusion (COPY) maintains I-address identity across documents, enabling automatic attribution, royalty flow, and origin tracing. INSERT, by contrast, is the act of *originating* content. The allocating account becomes the structural author:

`(A i : 1 ≤ i ≤ n : origin(aᵢ) = d)` — by I0(b)

The owner of d, encoded in d's tumbler prefix, is thereby the structural author of the new content. This is permanent and unalterable: I-addresses never change (T8, ASN-0034), and the tumbler prefix encodes identity intrinsically (T6, ASN-0034). The authorship of content created by INSERT is not metadata that can be stripped or forged — it is an arithmetic property of the address. Nelson distinguishes this structural provenance from social authorship claims: "The structural origin (I-address encoding account) is unalterable. The authorship claim (Author metalink) is a social assertion that third parties can dispute." The I-address is ground truth; metalinks are commentary.

The automatic royalty mechanism depends on this permanence. When any document containing the content is read, the system determines the owner by inspecting the I-addresses — "who wrote what, as determined automatically." Without I0's guarantee that INSERT always allocates under the inserting document's prefix, this automatic determination would be impossible.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| I0 | INSERT allocates contiguous, document-scoped, fresh I-addresses: `(A i : 1 ≤ i ≤ n : aᵢ = a₁ ⊕ [i − 1]) ∧ (A a ∈ dom(C) : origin(a) = d : a < a₁)` | introduced |
| I1 | The V-shift σ is injective on dom(M(d)) | introduced |
| I2 | σ preserves V-position ordering within the text subspace | introduced |
| I3 | σ creates a gap: positions with ordinal in [p̂, p̂ + n) are not in σ's image | introduced |
| I4 | σ is the identity outside the insertion subspace; maps text positions to text positions | introduced |
| I5 | INSERT into the text subspace does not alter d's link subspace arrangement | introduced |
| I6 | INSERT preserves all I-space content and addresses referenced by any link endset | introduced |
| I-pre | Precondition: d ∈ E_doc ∧ n ≥ 1 ∧ S8a(p) | introduced |
| I-post | Postcondition: C extended with n fresh entries, M(d) shifted and extended, other documents unchanged, provenance recorded | introduced |
| I-frame | Frame: existing C entries preserved, E unchanged, other documents' arrangements unchanged, existing R preserved | introduced |
| I7 | Correspondence run transformation: before-runs unchanged, after-runs V-shifted, at most one split, exactly one new run | introduced |
| I8 | Run count increases by at most 2 per INSERT | introduced |
| I9 | INSERT is invertible: pre-state uniquely recoverable from post-state and parameters (d, p, n) | introduced |


## Open Questions

What invariants must the version history satisfy when a document's arrangement evolves through a sequence of INSERTs — must every intermediate state be independently reconstructable, or only the final state of each committed transition?

Under what conditions may two adjacent correspondence runs be merged into one, and must a conforming implementation maintain a minimal run decomposition?

What must the system guarantee about I-address ordering across documents when multiple documents receive INSERTs concurrently on independent nodes?

Must INSERT be atomic — either fully completing or having no effect — or can a partially applied INSERT (content allocated but arrangement not yet extended) constitute a valid intermediate state?

What relationship must hold between a document and its forked descendant when the original receives an INSERT after the fork — must the forked version's arrangement remain independent of all subsequent edits to the original?

What must the system guarantee about the gap positions when the insertion point coincides with the maximum ordinal ever used in the subspace — can the shifted positions exceed any architectural bound on ordinal magnitude?
