# ASN-0059: INSERT Operation

*2026-03-20*

We are looking for the precise postcondition of INSERT — the operation that introduces new content into a document's arrangement. Nelson defines it in one sentence [LM 4/66]:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

From this we must extract a complete specification: what is allocated, what mapping changes occur, what is preserved unchanged, and what invariants the completed operation must satisfy. The discipline is to derive each guarantee from first principles, using the system state model (ASN-0047) and the block decomposition (ASN-0058), until the postcondition is tight enough that invariant-preservation obligations become routine.

We work with the system state Σ = (C, E, M, R) of ASN-0047. C is the content store (T ⇀ Val), E the entity set, M the arrangement function with M(d) : T ⇀ T for each document d, and R the provenance relation. The content store is append-only (S0, P0). The arrangement M(d) is the mutable layer. INSERT must specify exactly how it modifies M(d) while respecting C's immutability.


## Content Allocation

INSERT creates content that has never existed. This distinguishes it from operations that reference existing content — the distinction Nelson emphasizes (Q8) between producing new I-addresses and incorporating existing ones. INSERT receives a document identifier d, a V-position p (where to place the content), and a sequence of content values (val₁, ..., valₙ) with n ≥ 1. It must allocate n fresh I-addresses.

By T9 (ForwardAllocation, ASN-0034), addresses within a single allocator's stream are strictly monotonically increasing, and by T10a (AllocatorDiscipline), each successive allocation uses ordinal increment TA5(c). The resulting addresses form a contiguous run.

**I0 — FreshContiguousAllocation.**

(i) There exist a₁, ..., aₙ ∈ T with aᵢ ∉ dom(C) for 1 ≤ i ≤ n.

(ii) aᵢ₊₁ = aᵢ + 1 for 1 ≤ i < n, where + is ordinal increment via TA5(c).

(iii) origin(aᵢ) = d for 1 ≤ i ≤ n. The document prefix of each I-address identifies d as the allocating document (S7a).

(iv) C' = C ∪ {aᵢ ↦ valᵢ : 1 ≤ i ≤ n}.

By P0 (ContentPermanence), all prior content is preserved: for every a ∈ dom(C), we have a ∈ dom(C') and C'(a) = C(a). The new addresses are permanent — T8 (AllocationPermanence) guarantees they remain allocated in every subsequent state, and S0 (ContentImmutability) guarantees C'(aᵢ) = valᵢ forever.

Gregory's implementation evidence confirms the single-allocation model: `inserttextgr` packs all n bytes into one contiguous I-span regardless of how many text segments the caller provides (Q18). A single INSERT of n bytes produces one contiguous run of I-addresses. The resulting I-span is recorded as a single entry in the spanfilade (Q16), consistent with I0: the allocator processes the entire insertion as one contiguous batch.


## The Ordinal Shift

Before stating the arrangement effect, we must define what "increased by the length" means in tumbler arithmetic. Nelson says V-addresses of following characters "are increased by the length of the inserted text." We need this as a formal operation.

**Definition — OrdinalDisplacement.** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #p for insertion position p), we write δₙ.

**Definition — OrdinalShift.** For a V-position v of depth m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

By TumblerAdd (ASN-0034): shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the ordinal within the V-position's subspace by exactly n, leaving all higher-level components unchanged.

We need two properties of this shift before we can use it in the postcondition.

**I6 — ShiftOrderPreservation.**

`(A v₁, v₂ : #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Derivation.* Since #v₁ = #v₂ = m and v₁ ≠ v₂, the divergence point satisfies divergence(v₁, v₂) ≤ m. The action point of δₙ is m ≥ divergence(v₁, v₂). By TA1-strict (ASN-0034): v₁ ⊕ δₙ < v₂ ⊕ δₙ. ∎

The relative ordering of content is preserved through the shift. What was before other content remains before it after insertion — Nelson's guarantee that content appears "in its original relative order on either side" (Q2).

**I7 — ShiftInjectivity.**

`(A v₁, v₂ : #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Derivation.* By TA-MTO (ASN-0034): v₁ ⊕ δₙ = v₂ ⊕ δₙ iff (A i : 1 ≤ i ≤ m : v₁ᵢ = v₂ᵢ). The action point of δₙ is m, and agreement at positions 1..m for tumblers of length m means v₁ = v₂ by T3 (CanonicalRepresentation). ∎

Injectivity ensures the shift creates no collisions: distinct V-positions remain distinct after shifting.

Additionally, shift preserves structural properties. Subspace preservation requires m ≥ 2: ordinal increment via TA5(c) modifies position m = #v, so when m ≥ 2 the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁ — giving subspace(shift(v, n)) = subspace(v). When m = 1, shift([S], n) = [S + n] changes the subspace identifier; we exclude this by requiring #p ≥ 2 in I8(vi) below. By S8-depth, all V-positions in the subspace share p's depth, so m ≥ 2 holds throughout. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. So the shift preserves subspace membership, tumbler depth, and — since vₘ + n > 0 whenever vₘ ≥ 1 — the positivity required by S8a.


## The Arrangement Postcondition

We now state the full effect of INSERT on M(d). Write S = subspace(p) = p₁ for the subspace of the insertion point (the text subspace, with S ≥ 1 per S8a).

The arrangement partitions into four regions, each with a distinct guarantee.

**I1 — PreInsertionStability.** Content before the insertion point is unchanged:

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

Neither the V-position nor the I-address changes. Nelson is explicit: only "following characters" are affected [LM 4/66]. The content at V-position v reads exactly as before, at exactly the same V-position.

**I2 — ContentPlacement.** The new content occupies n consecutive V-positions starting at p:

`(A k : 0 ≤ k < n : p + k ∈ dom(M'(d)) ∧ M'(d)(p + k) = a₁ + k)`

where a₁ is the first allocated I-address from I0, and p + k and a₁ + k are k ordinal increments via TA5(c). At k = 0: M'(d)(p) = a₁ — the first new byte appears at the insertion point. The n new positions form a single mapping block (p, a₁, n) in the sense of ASN-0058.

**I3 — PostInsertionShift.** Content at or beyond p shifts forward by n ordinal positions:

`(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

The I-address is unchanged — only the V-position moves. This is Nelson's central guarantee (Q1, Q5): the permanent identity of every existing byte is invariant under insertion. "Since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30]. The shift moves content in the document's arrangement without touching the content's identity in the store.

**I4 — SubspaceStability.** V-positions in other subspaces are entirely untouched:

`(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

This is the abstract form of the subspace isolation guarantee. Gregory's implementation achieves this through the two-blade knife mechanism (Q10, Q17): the second blade is placed at the next subspace boundary, so the shift region is bounded by [blade₀, blade₁) ⊆ subspace S. Crums in other subspaces are visited during traversal but classified as "no shift" (case 2). At the abstract level, the property is simpler: INSERT in subspace S does not modify any mapping in subspace S' ≠ S. The key observation is that δₙ has its action point at depth m, which modifies only the ordinal component — it cannot cross the subspace boundary encoded in position 1.

**I5 — DocumentIsolation.** No other document's arrangement is affected:

`(A d' : d' ≠ d : M'(d') = M(d'))`

This follows from the Istream/Vstream separation: each document has its own independent arrangement (Nelson, Q3). When content is shared between documents through transclusion, both documents' arrangements point to the same I-addresses, but the arrangements themselves are independent structures. INSERT is scoped by the `<doc id>` parameter to a single document. Modifying document d's arrangement cannot change any other document's view.


### Domain Completeness

I1–I4 each establish that certain V-positions belong to dom(M'(d)). Let:

```
R₁ = {v ∈ dom(M(d)) : subspace(v) ≠ S}                          (by I4)
R₂ = {v ∈ dom(M(d)) : subspace(v) = S ∧ v < p}                   (by I1)
R₃ = {p + k : 0 ≤ k < n}                                          (by I2)
R₄ = {shift(v, n) : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p}    (by I3)
```

This gives R₁ ∪ R₂ ∪ R₃ ∪ R₄ ⊆ dom(M'(d)) — the ⊇ direction.

The ⊆ direction — that dom(M'(d)) contains no positions outside these four regions — follows from the composite transition structure. Step (ii) applies K.μ~ with bijection π mapping each same-subspace position v ≥ p to shift(v, n) and fixing all others; since π is a bijection, |dom| is preserved. Step (iii) applies K.μ⁺ adding exactly the n new mappings at p, p + 1, ..., p + (n − 1). No other step modifies M(d). Therefore |dom(M'(d))| = |dom(M(d))| + n.

We verify that R₁ through R₄ are pairwise disjoint. R₁ is disjoint from the others by subspace. R₂ has V-positions < p. R₃ occupies the interval [p, p + (n − 1)]. R₄ has V-positions ≥ shift(p, n) = p ⊕ δₙ: since δₙ > 0, by TA-strict (ASN-0034) we have p ⊕ δₙ > p, and more precisely shift(p, n) = p + n which is the V-position immediately after the R₃ interval. So R₃ ends at p + (n − 1) and R₄ begins at p + n — adjacent but not overlapping.

Since R₁ ∪ R₂ ∪ R₃ ∪ R₄ ⊆ dom(M'(d)), the four sets are pairwise disjoint, and |R₁| + |R₂| + |R₃| + |R₄| = |dom(M(d))| + n = |dom(M'(d))|, the inclusion is an equality:

`dom(M'(d)) = R₁ ∪ R₂ ∪ R₃ ∪ R₄`


## Block Decomposition Effect

We express INSERT's effect on the block decomposition of M(d) (ASN-0058). Let B be the current decomposition of the text-subspace arrangement. Each block β = (v, a, k) satisfies (A j : 0 ≤ j < k : M(d)(v + j) = a + j).

Since INSERT in subspace S leaves all other subspaces unchanged (I4), we separate B by subspace: B_S = {β = (v, a, k) ∈ B : subspace(v) = S} and B_other = B \ B_S. Only B_S is affected by the insertion; B_other passes through unchanged.

Partition B_S relative to the insertion point p. For each β = (v, a, k) ∈ B_S, exactly one of three conditions holds:

(a) *Entirely before:* v + k ≤ p. The block's V-extent lies entirely before p.

(b) *Entirely at or after:* v ≥ p. The block's V-extent starts at or beyond p.

(c) *Straddling:* v < p and v + k > p. The insertion point falls interior to the block. By B2 (Disjointness, ASN-0058), at most one block straddles p.

For case (c), we first establish that p agrees with v at positions 1..m−1. Ordinal increment via TA5(c) modifies only position m, so v + k agrees with v at positions 1..m−1. Suppose p diverges from v at some position j < m (the first such position). If pⱼ < vⱼ, then p < v by T1 — contradicting v < p. If pⱼ > vⱼ, then since (v + k)ⱼ = vⱼ < pⱼ and p agrees with v + k at positions 1..j−1, we get p > v + k by T1 — contradicting v + k > p. Therefore pᵢ = vᵢ for 1 ≤ i < m. The offset c = pₘ − vₘ satisfies 0 < c < k (from vₘ < pₘ < vₘ + k), and v + c = [v₁, ..., v_{m−1}, vₘ + c] = [p₁, ..., p_{m−1}, pₘ] = p. Split β at c into β_L = (v, a, c) and β_R = (p, a + c, k − c), per M4 (SplitDefinition, ASN-0058). By M5 (SplitPartition), ⟦β_L⟧ ∪ ⟦β_R⟧ = ⟦β⟧ with ⟦β_L⟧ ∩ ⟦β_R⟧ = ∅.

Define B_left = {blocks from case (a)} ∪ {β_L if case (c) applies}, and B_right = {blocks from case (b)} ∪ {β_R if case (c) applies}. Define the shifted block: for β = (v, a, k) ∈ B_right, let shift_block(β, n) = (shift(v, n), a, k) — the V-start shifts but the I-start and width are unchanged.

**I10 — BlockDecompositionEffect.** The post-INSERT decomposition is:

`B' = B_other ∪ B_left ∪ {(p, a₁, n)} ∪ {shift_block(β, n) : β ∈ B_right}`

where B_left and B_right are drawn from B_S, and B_other contributes its blocks unchanged.

*Verification of B1–B3.* Coverage (B1): B_other covers V-positions in subspaces S' ≠ S, unchanged by I4. Within subspace S: B_left covers pre-insertion positions (I1), (p, a₁, n) covers the n new positions (I2), and shifted blocks cover the shifted positions (I3). Disjointness (B2): B_other is disjoint from the subspace-S blocks by subspace. Within subspace S: B_left blocks have V-extents ending before p; the new block occupies [p, p + n − 1]; shifted blocks start at or beyond p + n. No overlap. Consistency (B3): for B_other, M'(d)(v + j) = M(d)(v + j) = a + j by I4 and original B3. For B_left, M'(d)(v + j) = M(d)(v + j) = a + j by I1 and original B3. For the new block, M'(d)(p + j) = a₁ + j by I2. For shifted blocks, we need M'(d)(shift(v, n) + j) = a + j. We verify shift(v, n) + j = shift(v + j, n). By M-aux (OrdinalIncrementAssociativity, ASN-0058), v + j = [v₁, ..., v_{m−1}, vₘ + j], so shift(v + j, n) = [v₁, ..., v_{m−1}, vₘ + j + n]. Meanwhile shift(v, n) = [v₁, ..., v_{m−1}, vₘ + n], so shift(v, n) + j = [v₁, ..., v_{m−1}, vₘ + n + j]. These are equal by commutativity of ℕ addition. Therefore M'(d)(shift(v, n) + j) = M'(d)(shift(v + j, n)) = M(d)(v + j) = a + j by I3. ∎

Gregory's implementation evidence illuminates one optimization over this abstract model. When the newly allocated I-address a₁ is contiguous with the preceding block's I-range (a₁ = a_prev + k_prev) and both share the same home document, the implementation coalesces the new content into the existing block by extending its width in place (Q11, Q13). `isanextensionnd` checks the ONMYRIGHTBORDER condition — the new content begins exactly where the existing crum ends — and if it matches, `dspadd` widens both the I and V components of the crum without allocating any new node.

At the abstract level, this is the observation that (p, a₁, n) and a V-adjacent, I-adjacent predecessor satisfy the merge condition M7 (ASN-0058), so the maximally merged decomposition combines them. The abstract specification does not prescribe whether coalescing occurs — it specifies only the mapping M'(d), which is the same either way (M3, RepresentationInvariance, ASN-0058).


### Worked Example

Consider document d with five characters at V-positions [1, 1] through [1, 5], mapped to contiguous I-addresses b, b + 1, ..., b + 4. The block decomposition is B = {([1, 1], b, 5)}.

INSERT two characters (val₁, val₂) at p = [1, 3]. Parameters: n = 2, S = 1, m = 2, δ₂ = [0, 2].

**I0:** Allocate a₁, a₂ with a₂ = a₁ + 1, origin(aᵢ) = d. Set C' = C ∪ {a₁ ↦ val₁, a₂ ↦ val₂}.

**Block split.** β = ([1, 1], b, 5) straddles p: [1, 1] < [1, 3] < [1, 6]. Both v and p agree at position 1 (v₁ = p₁ = 1), so c = p₂ − v₂ = 3 − 1 = 2. Split: β_L = ([1, 1], b, 2), β_R = ([1, 3], b + 2, 3).

**Arrangement effect:**

| V (before) | I (before) | Region | V (after) | I (after) |
|---|---|---|---|---|
| [1, 1] | b | I1 | [1, 1] | b |
| [1, 2] | b + 1 | I1 | [1, 2] | b + 1 |
| — | — | I2 | [1, 3] | a₁ |
| — | — | I2 | [1, 4] | a₁ + 1 |
| [1, 3] | b + 2 | I3 | [1, 5] | b + 2 |
| [1, 4] | b + 3 | I3 | [1, 6] | b + 3 |
| [1, 5] | b + 4 | I3 | [1, 7] | b + 4 |

I3 shifts: shift([1, 3], 2) = [1, 3] ⊕ [0, 2] = [1, 5], shift([1, 4], 2) = [1, 6], shift([1, 5], 2) = [1, 7]. Each shifted position preserves its I-address.

**I10 (block decomposition).** B' = {([1, 1], b, 2), ([1, 3], a₁, 2), ([1, 5], b + 2, 3)}.

B1 (coverage): 7 V-positions [1, 1]..[1, 7] partitioned among three blocks. B2 (disjointness): V-extents [1, 1]..[1, 2], [1, 3]..[1, 4], [1, 5]..[1, 7] are pairwise disjoint. B3 (consistency): first block by I1, second by I2, third by I3 with shift([1, 3 + j], 2) = [1, 5 + j]. Domain: |dom(M'(d))| = 5 + 2 = 7. ∎


## Insertion Position

We must state what insertion positions are valid.

**I8 — InsertionPrecondition.** INSERT(d, p, vals) requires:

(i) d ∈ E_doc (the document exists).

(ii) p satisfies S8a: all components strictly positive, zeros(p) = 0.

(iii) subspace(p) = S where S ≥ 1 (text subspace).

(iv) When V_S = {v ∈ dom(M(d)) : subspace(v) = S} is non-empty, #p equals the common depth of V_S (S8-depth). When V_S = ∅, #p establishes the depth for the subspace.

(v) n ≥ 1 (non-empty content).

(vi) #p ≥ 2. Ordinal increment via TA5(c) modifies position sig(v) = #v = m. Subspace preservation requires the modified position to differ from the subspace identifier at position 1, hence m ≥ 2.

Nelson specifies no restriction on p's ordinal range (Q6): INSERT is permitted "at any position, including the very beginning and the very end." APPEND [LM 4/67] is the convenience specialization where p = v_max + 1 — insertion at one past the current maximum V-position. For an empty document (M(d) = ∅), any valid text-subspace V-position serves as p.

### Contiguity

Nelson describes the Vstream as "a dense, contiguous sequence" [LM 4/30]. We capture this as a structural property.

**Definition — VContiguity.** The text-subspace V-positions of document d in subspace S are *contiguous* when, letting V_S = {v ∈ dom(M(d)) : subspace(v) = S}, either V_S = ∅ or:

`(A u, w : u ∈ V_S ∧ w ∈ V_S ∧ u < w : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < w : v ∈ V_S))`

Every intermediate tumbler of the same depth and subspace between two occupied positions is also occupied.

**I9 — ContiguityPreservation.** If V_S is contiguous before INSERT, and p satisfies v_min ≤ p ≤ v_max + 1 (where v_min, v_max are the minimum and maximum of V_S; for V_S = ∅ any p is valid), then V_S is contiguous after INSERT.

*Argument.* Before INSERT, V_S covers every text-subspace V-position between v_min and v_max. After INSERT: the pre-insertion region covers [v_min, p − 1] by I1. The new content covers [p, p + (n − 1)] by I2. The shifted region covers [p + n, v_max + n] by I3. Contiguity of the shifted positions follows from the identity shift(v + j, n) = shift(v, n) + j (proven in I10 below from commutativity of ℕ addition at position m): if the pre-shift positions are {p, p + 1, ..., v_max}, then the shifted positions are {shift(p, n), shift(p, n) + 1, ..., shift(p, n) + (v_max − p)} = {p + n, p + n + 1, ..., v_max + n} — contiguous with no gaps. These three intervals are adjacent: (p − 1) + 1 = p and (p + n − 1) + 1 = p + n. So V_S' = [v_min, v_max + n] with no gaps. ∎

When p > v_max + 1, the shift is vacuous — no V-positions satisfy v ≥ p — and a gap opens between v_max and p. Gregory's implementation permits this (Q12): `makegappm` detects the out-of-range origin at its guard clause (`tumblercmp(origin, reach) != LESS`) and returns immediately, performing no shifts. At the abstract level, this is well-defined by the postcondition — I3 applies to the empty set of positions ≥ p, so the effect is simply I2 (place new content) with I1 and I4 holding vacuously. But contiguity is lost. Whether the system should enforce contiguity as an invariant or permit callers to violate it remains an open question.


## INSERT as Composite Transition

We verify that INSERT decomposes into the elementary transitions of ASN-0047 and satisfies the coupling constraints.

The composite Σ → Σ' consists of:

(i) *Content allocation* — n applications of K.α: each allocates one I-address aᵢ with C' = C ∪ {aᵢ ↦ valᵢ}. Precondition: IsElement(aᵢ) ∧ origin(aᵢ) ∈ E_doc. By S7a (DocumentScopedAllocation), each aᵢ is allocated under d's prefix. Since d is a document address with zeros(d) = 2, and aᵢ extends d's prefix with one zero separator and an element field, zeros(aᵢ) = 3 — hence IsElement(aᵢ) by T4 (ASN-0034), and S7b is satisfied. The document prefix of aᵢ is then d itself, giving origin(aᵢ) = d ∈ E_doc by I8(i).

(ii) *Arrangement reordering* — K.μ~ on document d, *when the shift set is non-empty*. Let V_shift = {v ∈ dom(M(d)) : subspace(v) = S ∧ v ≥ p}. When V_shift ≠ ∅, apply K.μ~ with bijection π : v ↦ shift(v, n) for v ∈ V_shift and π(v) = v otherwise. By I6 (order preservation) and I7 (injectivity), π is well-behaved. It produces V-positions satisfying S8a (shift preserves positivity), S8-depth (shift preserves depth), and the multiset of I-addresses is preserved (only V-positions change). Precondition: d ∈ E_doc. Satisfied by I8(i). When V_shift = ∅ — inserting into an empty subspace or appending past all existing positions — step (ii) is omitted: K.μ~ requires strict contraction followed by strict extension, which is inapplicable when π is the identity. The composite then reduces to steps (i), (iii), (iv).

(iii) *Arrangement extension* — K.μ⁺: adds the n new mappings {p + k ↦ a₁ + k : 0 ≤ k < n}. Precondition: each a₁ + k ∈ dom(C') (satisfied after step (i)), new V-positions satisfy S8a and S8-depth (inherited from p), dom(M'(d)) is finite (|dom(M(d))| + n is finite by S8-fin).

(iv) *Provenance recording* — n applications of K.ρ: each records (aᵢ, d) ∈ R'. Precondition: aᵢ ∈ dom(C') ∧ d ∈ E_doc. Both satisfied.

**Elementary preconditions at intermediate states.** ASN-0047's ValidComposite requires each step's precondition to hold at the intermediate state where it executes. For K.α: each aᵢ must satisfy aᵢ ∉ dom(Cᵢ₋₁) where Cᵢ₋₁ is the content store after the preceding allocations. We have aᵢ ∉ dom(C) by I0(i). For i ≥ 2, we need aᵢ ∉ {a₁, ..., aᵢ₋₁}: I0(ii) gives aⱼ₊₁ = aⱼ + 1 > aⱼ by TA-strict (ASN-0034), so a₁ < a₂ < ... < aₙ — all distinct. Therefore aᵢ ∉ dom(C) ∪ {a₁, ..., aᵢ₋₁} = dom(Cᵢ₋₁). For K.μ⁺: the new V-positions {p + k : 0 ≤ k < n} must not already belong to dom(M(d)) at the point K.μ⁺ executes (i.e., after step (ii)). When step (ii) applies, every position in V_shift has been shifted to positions ≥ p + n by I3, and positions in subspace S below p remain below p by I1, so the interval [p, p + (n − 1)] is unoccupied. When step (ii) is omitted (V_shift = ∅), no positions in subspace S exist at or beyond p, so the interval is likewise unoccupied. Positions in other subspaces have different subspace identifiers and cannot collide.

**Coupling constraints.** J0 (AllocationRequiresPlacement): every a ∈ dom(C') \ dom(C) appears in M'(d) via step (iii). J1 (ExtensionRecordsProvenance): the new addresses in ran(M'(d)) \ ran(M(d)) are the a₁...aₙ, each recorded in R' by step (iv). The shifted entries contribute no new I-addresses to ran(M'(d)) — only their V-positions change. J1' (ProvenanceRequiresExtension): each new pair (aᵢ, d) ∈ R' \ R corresponds to aᵢ ∈ ran(M'(d)) \ ran(M(d)). These arguments hold identically whether step (ii) is present or omitted: K.μ~ contributes no new content to dom(C') and no new provenance to R', so the coupling constraints J0, J1, J1' depend only on steps (i), (iii), and (iv).

The frame conditions of the composite are: E' = E (no entities created or destroyed), and R' = R ∪ {(aᵢ, d) : 1 ≤ i ≤ n} (provenance extended, never contracted).

**Observation (Canonical Atomicity).** Nelson requires that every change leave the system "in canonical order, which was an internal mandate of the system" [LM 1/34]. In our model, this is the requirement that INSERT is a valid composite transition: the elementary steps are internally ordered but their intermediate states are not observable. The coupling constraints (J0, J1, J1') are evaluated on the composite as a whole. Nelson describes this as stronger than a transactional guarantee — it is a structural invariant (Q4). A system where INSERT could be observed mid-execution, with V-addresses shifted but content not yet placed, would violate canonical order. The transition from Σ to Σ' is atomic with respect to external observation.


## Invariant Preservation

We verify that INSERT preserves each foundation invariant.

**P0 (ContentPermanence).** C' ⊇ C and C'(a) = C(a) for a ∈ dom(C). Guaranteed by K.α's frame: each allocation extends C without modifying existing entries.

**P1 (EntityPermanence).** E' = E. INSERT does not create or destroy entities.

**P8 (EntityHierarchy).** E' = E, so the predicate is unchanged.

**P2 (ProvenancePermanence).** R' = R ∪ {(aᵢ, d) : 1 ≤ i ≤ n} ⊇ R.

**S0 (ContentImmutability).** Each K.α creates a new mapping a ↦ v; no existing entry in C is modified.

**S2 (ArrangementFunctionality).** M'(d) is a function — each V-position maps to exactly one I-address. The four regions (I1, I2, I3, I4) are pairwise disjoint (verified in Domain Completeness above), so no V-position receives two mappings. Within each region, functionality is inherited (I1, I4), by construction (I2), or by injectivity of the shift (I3 with I7).

**S3 (ReferentialIntegrity).** Every I-address in ran(M'(d)) is in dom(C'). For I1 and I3: the I-addresses are unchanged from ran(M(d)) ⊆ dom(C) ⊆ dom(C'). For I4: same argument. For I2: the I-addresses a₁ + k are in dom(C') by I0.

**S8a (VPositionWellFormedness).** All components of shift(v, n) are strictly positive: components 1..m−1 are unchanged (positive by S8a on v), and component m is vₘ + n ≥ 1 + 1 > 0. The new positions p + k inherit positivity from p.

**S8-depth (FixedDepthVPositions).** The shift preserves depth: #shift(v, n) = #v. Ordinal increment preserves depth: #(p + k) = #p. So all V-positions in subspace S retain equal depth.

**S8-fin (FiniteArrangement).** |dom(M'(d))| = |dom(M(d))| + n, finite since both terms are finite.

**P4 (ProvenanceBounds).** Contains(Σ') ⊆ R'. For the new pairs: (aᵢ, d) ∈ R' by step (iv). For existing pairs: Contains(Σ) ⊆ R ⊆ R'.

**P6 (ExistentialCoherence).** For new addresses: origin(aᵢ) = d ∈ E_doc = E'_doc. For existing addresses: P6 held in Σ and E' = E.

**P7 (ProvenanceGrounding).** For new pairs: aᵢ ∈ dom(C'). For existing pairs: a ∈ dom(C) ⊆ dom(C').

**P7a (ProvenanceCoverage).** For new addresses aᵢ: (aᵢ, d) ∈ R'. For existing addresses: already covered by R ⊆ R'.


## The INSERT/COPY Distinction

We note, without specifying, that INSERT is one of two mechanisms for placing content into a document's Vstream. The other — COPY (transclusion) — is architecturally distinct (Q8) and outside the scope of this ASN. The distinction is summarized for clarity:

INSERT allocates *fresh* I-addresses under the inserting document's prefix, making d the *home document* of the new content (I0(iii)). The content has no structural relationship to any prior content in the system — even textually identical content receives distinct I-addresses (S4, OriginBasedIdentity).

The architectural consequence is that every downstream guarantee — attribution via origin(a), discoverability via FINDDOCSCONTAINING, royalty computation, version correspondence — depends on whether content entered a document through INSERT (fresh allocation) or through the transclusion mechanism (reference to existing I-addresses). The Vstream presentation is identical in both cases; the Istream identity is fundamentally different.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| I0 | INSERT allocates n fresh contiguous I-addresses under d: aᵢ₊₁ = aᵢ + 1, origin(aᵢ) = d, C' = C ∪ {aᵢ ↦ valᵢ} | introduced |
| I1 | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : M'(d)(v) = M(d)(v)) | introduced |
| I2 | (A k : 0 ≤ k < n : M'(d)(p + k) = a₁ + k) | introduced |
| I3 | (A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : M'(d)(shift(v, n)) = M(d)(v)) | introduced |
| I4 | (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ S : M'(d)(v) = M(d)(v)) | introduced |
| I5 | (A d' : d' ≠ d : M'(d') = M(d')) | introduced |
| I6 | shift preserves strict order: v₁ < v₂ ⟹ shift(v₁, n) < shift(v₂, n) | introduced |
| I7 | shift is injective: shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂ | introduced |
| I8 | INSERT precondition: d ∈ E_doc, p satisfies S8a, subspace(p) ≥ 1, depth compatibility, #p ≥ 2, n ≥ 1 | introduced |
| I9 | INSERT preserves V-space contiguity when v_min ≤ p ≤ v_max + 1 | introduced |
| I10 | Block decomposition: B' = B_other ∪ B_left ∪ {(p, a₁, n)} ∪ {shift_block(β, n) : β ∈ B_right}, where B_left/B_right partition B_S (same subspace) and B_other is unchanged | introduced |
| OrdinalDisplacement | δ(n, m) = [0, ..., 0, n] of length m, action point m | introduced |
| OrdinalShift | shift(v, n) = v ⊕ δ(n, #v) | introduced |
| VContiguity | All intermediate positions of same depth and subspace between two occupied positions are occupied | introduced |


## Open Questions

- Must the V-space contiguity property hold as a system-wide invariant, or is it a precondition for which the caller is responsible?
- What serialization guarantees must the system provide when multiple INSERT operations target the same document concurrently?
- Must the effects of a completed INSERT be immediately visible to all concurrent retrieval operations, or may observation be deferred?
- What properties must a retrieval operation over the post-INSERT arrangement satisfy to faithfully render the contiguous document?
- When external state records a V-position, what must the system provide to allow that reference to be updated after INSERT shifts the position?
