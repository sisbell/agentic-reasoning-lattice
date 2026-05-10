# ASN-0050: DELETE Operation

*2026-03-18*

We ask: what happens when content is removed from a document's arrangement? The question is loaded — in conventional systems, "remove" means "destroy." In a system committed to content permanence, removal can mean only one thing: the arrangement changes; the content does not. But this deceptively simple answer opens a cascade of consequences. What happens to the gap? What happens to links? What happens to other documents? And what must the system preserve so that the removal can be undone — so that the prior arrangement, which included the now-invisible content, remains permanently reconstructible?

Nelson is unambiguous: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" The phrase "not currently addressable" is the entire design. The bytes are not gone — they are merely absent from the current arrangement. They survive in the content store, remain visible in any document that transcludes them, and can be recovered through version history. Gregory confirms the implementation: `deletend` operates exclusively on the document's V-to-I mapping; it never touches the content store. The `subtreefree` that follows a deletion reclaims mapping nodes, not content.

We will discover that DELETE is the simplest of the three editing operations. INSERT creates content and extends arrangements. COPY extends arrangements by sharing existing content. DELETE merely contracts an arrangement. It introduces nothing into C, E, or R. Its power lies entirely in what it does NOT do.


## V-space contiguity

Before we can define DELETE, we need an invariant that the foundations leave implicit but that Nelson's design requires. He states that V-addresses "always form a contiguous sequence starting at 1." Within the text subspace, using the ordinal representation of TA7a (ASN-0034), this means the set of active V-positions forms an unbroken interval.

**D0** (*V-contiguity*). For each d ∈ E_doc, there exists N(d) ≥ 0 such that the text-subspace portion of dom(M(d)) is exactly {[x] : 1 ≤ x ≤ N(d)}.

When N(d) = 0, the text subspace is empty. When N(d) ≥ 1, positions [1] through [N(d)] are all occupied with no gaps. This is stronger than S8-fin (which requires only finiteness) and S8a (which requires well-formed positions). It constrains the *shape* of the domain.

D0 holds in the initial state vacuously: every document starts with M(d) = ∅, so N(d) = 0 and the set of text-subspace V-positions is empty. INSERT preserves D0 by construction — the V-shift opens a contiguous gap and the extension fills it, yielding a domain of size N(d) + n that is still an unbroken interval. COPY preserves D0 by the same mechanism. We must verify that DELETE also preserves D0.


## The skip function

Let document d have N = N(d) text-subspace positions, and consider the deletion of the span starting at ordinal s with length ℓ, where 1 ≤ s, s + ℓ − 1 ≤ N, and ℓ ≥ 1. The positions to be removed are {[x] : s ≤ x < s + ℓ}. The positions that survive fall into two groups: those before the deletion ({[x] : 1 ≤ x < s}) and those after ({[x] : s + ℓ ≤ x ≤ N}).

We define the *skip function* σ : [1, N − ℓ] → [1, N] by:

`σ(x) = x` when 1 ≤ x < s

`σ(x) = x + ℓ` when s ≤ x ≤ N − ℓ

Three properties follow immediately.

**D1** (*skip monotonicity*). σ is strictly monotone: `(A x₁, x₂ : 1 ≤ x₁ < x₂ ≤ N − ℓ : σ(x₁) < σ(x₂))`.

*Derivation.* Three cases. Both below s: σ(x₁) = x₁ < x₂ = σ(x₂). Both at or above s: σ(x₁) = x₁ + ℓ < x₂ + ℓ = σ(x₂). Mixed (x₁ < s ≤ x₂): σ(x₁) = x₁ < s ≤ x₂ + ℓ = σ(x₂), where the middle inequality uses s ≤ x₂ + ℓ (since x₂ ≥ s gives x₂ + ℓ ≥ s + ℓ > s). ∎

**D2** (*skip range*). ran(σ) = [1, s) ∪ [s + ℓ, N] = [1, N] \ [s, s + ℓ).

*Derivation.* For x < s: σ(x) = x ∈ [1, s). For x ≥ s: σ(x) = x + ℓ ∈ [s + ℓ, N]. Conversely, every y ∈ [1, s) has preimage y, and every y ∈ [s + ℓ, N] has preimage y − ℓ ∈ [s, N − ℓ]. ∎

**D3** (*skip bijectivity*). σ is a bijection from [1, N − ℓ] to [1, N] \ [s, s + ℓ).

Immediate from D1 (injectivity from strict monotonicity) and D2 (surjectivity onto the surviving positions). The skip function maps the post-delete ordinal space bijectively onto the surviving pre-delete positions.


## DELETE as composite transition

We are looking for a state transition that removes a specified V-span and closes the gap. The foundations provide two elementary transitions for arrangement modification: K.μ⁻ (contraction — remove mappings) and K.μ~ (reordering — relabel V-positions). DELETE composes them.

**D-pre** (*DELETE precondition*). `d ∈ E_doc ∧ ℓ ≥ 1 ∧ 1 ≤ s ∧ s + ℓ − 1 ≤ N(d)`

The document exists, and the deletion span [s, s + ℓ) falls entirely within the current text-subspace arrangement. By D0, every position in the span is in dom(M(d)).

**Phase 1** — *Contraction* (K.μ⁻). Remove the V-positions in the deleted span:

`dom(M₁(d)) = dom(M(d)) \ {[x] : s ≤ x < s + ℓ}`

`(A v : v ∈ dom(M₁(d)) : M₁(d)(v) = M(d)(v))`

This is a valid K.μ⁻: the domain strictly decreases, and surviving mappings are unchanged. The K.μ⁻ precondition requires d ∈ E_doc (satisfied by D-pre). Frame: C₁ = C; E₁ = E; R₁ = R; M₁(d') = M(d') for d' ≠ d.

After Phase 1, the text-subspace V-positions form {[x] : 1 ≤ x < s} ∪ {[x] : s + ℓ ≤ x ≤ N} — a set with a gap. This violates D0. Phase 2 repairs the gap.

**Phase 2** — *Reordering* (K.μ~). Close the gap by shifting the right-hand positions left. Define the bijection π on the surviving text-subspace positions:

`π([x]) = [x]` when 1 ≤ x < s

`π([x]) = [x − ℓ]` when s + ℓ ≤ x ≤ N

On non-text-subspace positions, π is the identity. This is a valid K.μ~: π is a bijection from dom(M₁(d)) to a new domain (injectivity follows from the injectivity of subtraction; bijectivity from the fact that every ordinal in [1, N − ℓ] has exactly one preimage). The multiset of I-addresses is preserved: ran(M'(d)) = ran(M₁(d)) since π only relabels V-positions.

Frame: C' = C₁ = C; E' = E; R' = R; M'(d') = M(d') for d' ≠ d.

The composition of these two phases yields the postcondition we want. For any new ordinal x in [1, N − ℓ], the corresponding old ordinal is σ(x) — the skip function from the previous section. π inverts the direction: old position [σ(x)] becomes new position [x]. So:

`M'(d)([x]) = M₁(d)([σ(x)]) = M(d)([σ(x)])`

The first equality is Phase 2 (the reordering maps new position [x] to old surviving position [σ(x)]). The second is Phase 1 (surviving positions retain their mappings).

**D-post** (*DELETE postcondition*). The post-state Σ' = (C', E', M', R') satisfies:

(a) `(A x : 1 ≤ x ≤ N(d) − ℓ : M'(d)([x]) = M(d)([σ(x)]))`

(b) `dom(M'(d)) ∩ text-subspace = {[x] : 1 ≤ x ≤ N(d) − ℓ}`

(c) `C' = C`

(d) `E' = E`

(e) `(A d' : d' ≠ d : M'(d') = M(d'))`

(f) `R' = R`

Clause (b) confirms that D0 is preserved: the new text-subspace domain is the contiguous interval [1, N(d) − ℓ] = [1, N'(d)] where N'(d) = N(d) − ℓ. The gap has been closed.

**D-frame** (*DELETE frame*). What DELETE does not change:

(a) `(A a ∈ dom(C) :: C'(a) = C(a)) ∧ dom(C') = dom(C)` — content store entirely untouched

(b) `E' = E` — no entity created or destroyed

(c) `(A d' : d' ≠ d : M'(d') = M(d'))` — other documents untouched

(d) `R' = R` — provenance neither added nor removed

(e) `(A v ∈ dom(M(d)) : v not in text subspace : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` — link subspace arrangement of d untouched


## Coupling constraints

We verify that DELETE satisfies the coupling constraints of ASN-0047.

**J0** (AllocationRequiresPlacement): dom(C') \ dom(C) = ∅ because DELETE contains no K.α. The quantifier is vacuously satisfied. ✓

**J1** (ExtensionRecordsProvenance): We need every I-address newly appearing in an arrangement to have provenance recorded. But DELETE only *removes* I-addresses from ran(M(d)) and relabels surviving ones; it introduces no new I-addresses. Formally: ran(M'(d)) ⊆ ran(M(d)), because M'(d) maps each surviving position to its original I-address via σ. For d' ≠ d, M'(d') = M(d') by D-frame(c). So for every d'', ran(M'(d'')) \ ran(M(d'')) = ∅. The quantifier is vacuously satisfied. ✓

**J1'** (ProvenanceRequiresExtension): R' \ R = ∅ by D-frame(d). Vacuously satisfied. ✓

DELETE is a valid composite transition. It is, in a precise sense, the *quietest* of the three editing operations: it modifies exactly one component (the arrangement of one document) and touches nothing else in the entire system state.


## V-space confinement

The frame conditions deserve emphasis. D-frame(a) states that `dom(C') = dom(C)` — DELETE does not even extend the content store, let alone modify or retract it. Compare with INSERT (which extends C with fresh addresses) and COPY (which holds C completely in frame but could in principle interact with allocation). DELETE makes no contact with C whatsoever.

We can state this as a weakest-precondition obligation:

`wp(DELETE, (A a :: a ∈ dom(C) ≡ a ∈ dom(C') ∧ C'(a) = C(a)))`
`= {D-frame(a)}`
`true`

The obligation is discharged unconditionally. No precondition on C is needed for DELETE to preserve content integrity. This is because both phases — K.μ⁻ and K.μ~ — have C in their frame, and the composition of two transitions that each hold C in frame also holds C in frame.

D-frame(d) — `R' = R` — is equally striking. INSERT extends R (new content gets provenance records). COPY extends R (content appearing in a new document gets provenance records). DELETE leaves R unchanged, because:

- K.μ⁻ has R in its frame (J2, ASN-0047).
- K.μ~ has R in its frame (J3, ASN-0047).
- DELETE introduces no new I-addresses into any arrangement, so J1 and J1' are vacuous — there is nothing to record.

The provenance of every I-address that was ever in d's arrangement remains in R. The record that d once contained address a — the pair (a, d) ∈ R — persists through and beyond the deletion. This is the formal content of Nelson's guarantee that "any previous instant can be reconstructed": the system retains the *fact* that d once contained a, even after a is removed from d's current arrangement.


## Content survival

We are looking for what persists after deletion. Let A_del = {M(d)([s + k]) : 0 ≤ k < ℓ} be the set of I-addresses removed from d's arrangement.

**D4** (*content survival*). `(A a ∈ A_del :: a ∈ dom(C'))`

*Derivation.* S3 (referential integrity, ASN-0036) in the pre-state gives A_del ⊆ ran(M(d)) ⊆ dom(C). D-frame(a) gives dom(C') = dom(C). Therefore A_del ⊆ dom(C'). ∎

The I-addresses in A_del are no longer *referenced* by any V-position in d's current arrangement, but they remain *allocated* in the content store. The content values at those addresses are unchanged: C'(a) = C(a) for every a ∈ A_del.

This is where the two-space separation does its work. In a single-space system, removing content from the arrangement would be indistinguishable from destroying it. In the two-space model, "remove from arrangement" and "remove from existence" are structurally different operations — the first modifies M, the second would modify C. And the architecture forbids the second: S0 (content immutability, ASN-0036) and P0 (content permanence, ASN-0047) together guarantee that no operation ever removes an address from dom(C) or changes its associated value.

Nelson captures this with a distinction that sounds merely editorial but is architecturally load-bearing: "delete" means "remove from this arrangement," never "destroy."


## Cross-document isolation

**D5** (*cross-document isolation*). For any d' ≠ d:

`M'(d') = M(d')`

*Derivation.* D-frame(c). ∎

The consequences for transclusion are immediate. If document d' transcludes content from d — that is, ran(M(d')) ∩ ran(M(d)) ≠ ∅ — then after DELETE(d, s, ℓ):

(i) M'(d') = M(d') — d' sees no change whatsoever.

(ii) For every a ∈ ran(M(d')), C'(a) = C(a) by D-frame(a) — the content values d' references are unchanged.

(iii) If a ∈ A_del ∩ ran(M(d')), then a is no longer in ran(M'(d)) but remains in ran(M'(d')). The content is invisible through d but fully visible through d'.

Nelson states this directly: "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." The mechanism is the two-space separation: DELETE operates on M(d), and M(d') is a separate partial function. They share I-space addresses — the same content store — but they are independently modifiable. An edit in one cannot propagate to the other.


## Order preservation

DELETE removes a middle section and closes the gap, but it does not rearrange the surviving content. We record this formally.

**D6** (*order preservation*). For ordinals x₁, x₂ in the post-state with 1 ≤ x₁ < x₂ ≤ N − ℓ:

`σ(x₁) < σ(x₂)`

and therefore the relative order of I-address references among surviving positions is the same as in the pre-state.

*Derivation.* This is D1 (skip monotonicity). ∎

The surviving content appears in the same sequence. A reader examining the post-delete arrangement sees everything that was before the deletion point, followed by everything that was after it, with no reordering. The only change is the absence of the deleted span.


## Correspondence runs under DELETE

The text subspace decomposes into correspondence runs (S8, ASN-0036): triples (v, a, n) where M(d)([v + k]) = a ⊕ [k] for 0 ≤ k < n. We trace how DELETE transforms this decomposition. Let {(vⱼ, aⱼ, nⱼ) : 1 ≤ j ≤ m} be the pre-state runs, ordered so that v₁ < v₂ < ... < vₘ.

Each run's ordinal interval [vⱼ, vⱼ + nⱼ) interacts with the deletion interval [s, s + ℓ) in one of five ways. We classify them.

*Class B (before):* vⱼ + nⱼ ≤ s. The run lies entirely before the deletion. In the post-state, its V-positions are untouched (all ordinals < s), so it persists as (vⱼ, aⱼ, nⱼ). Check: M'(d)([vⱼ + k]) = M(d)([σ(vⱼ + k)]) = M(d)([vⱼ + k]) = aⱼ ⊕ [k] since σ is the identity for ordinals < s.

*Class A (after):* vⱼ ≥ s + ℓ. The run lies entirely after the deletion. In the post-state, every position shifts left by ℓ: the new ordinal start is vⱼ − ℓ. The run becomes (vⱼ − ℓ, aⱼ, nⱼ). Check: M'(d)([(vⱼ − ℓ) + k]) = M(d)([σ((vⱼ − ℓ) + k)]) = M(d)([(vⱼ − ℓ) + k + ℓ]) = M(d)([vⱼ + k]) = aⱼ ⊕ [k]. The I-addresses are unchanged; only V-positions move.

*Class D (deleted):* s ≤ vⱼ and vⱼ + nⱼ ≤ s + ℓ. The run lies entirely within the deletion. It vanishes from the post-state decomposition.

*Class L (left-truncated):* vⱼ < s and vⱼ + nⱼ > s and vⱼ + nⱼ ≤ s + ℓ. The deletion clips the run's right end. The surviving left fragment has width s − vⱼ. Post-state run: (vⱼ, aⱼ, s − vⱼ). Check: for 0 ≤ k < s − vⱼ, the ordinal vⱼ + k < s, so σ(vⱼ + k) = vⱼ + k and M'(d)([vⱼ + k]) = M(d)([vⱼ + k]) = aⱼ ⊕ [k]. ✓

*Class R (right-truncated):* vⱼ ≥ s and vⱼ < s + ℓ and vⱼ + nⱼ > s + ℓ. The deletion clips the run's left end. The surviving portion starts at old ordinal s + ℓ (the first survivor) with I-address aⱼ ⊕ [s + ℓ − vⱼ] and width nⱼ − (s + ℓ − vⱼ). After shifting, the new ordinal start is s + ℓ − ℓ = s. Post-state run: (s, aⱼ ⊕ [s + ℓ − vⱼ], nⱼ − (s + ℓ − vⱼ)). Check: for 0 ≤ k < nⱼ − (s + ℓ − vⱼ), the old ordinal is (s + ℓ) + k and σ⁻¹ gives new ordinal s + k. Then M'(d)([s + k]) = M(d)([(s + ℓ) + k]) = aⱼ ⊕ [(s + ℓ − vⱼ) + k] = (aⱼ ⊕ [s + ℓ − vⱼ]) ⊕ [k] by associativity of tumbler addition (ASN-0034). ✓

*Class S (split):* vⱼ < s and vⱼ + nⱼ > s + ℓ. The deletion falls in the run's interior. Two fragments survive. The left fragment is (vⱼ, aⱼ, s − vⱼ), unchanged in V-position. The right fragment starts at old ordinal s + ℓ with I-address aⱼ ⊕ [s + ℓ − vⱼ] and width nⱼ − (s + ℓ − vⱼ); after shifting, its new ordinal start is s. Post-state: (vⱼ, aⱼ, s − vⱼ) and (s, aⱼ ⊕ [s + ℓ − vⱼ], nⱼ − (s + ℓ − vⱼ)). The correspondence checks follow the same reasoning as classes L and R.

The left and right fragments of a split run are V-contiguous (the left ends at ordinal s − 1, the right begins at s) but I-noncontiguous: the left fragment's I-reach is aⱼ ⊕ [s − vⱼ], while the right's I-start is aⱼ ⊕ [s + ℓ − vⱼ]. These differ by ℓ — the deleted content's I-addresses form the gap. Gregory's implementation evidence confirms this: `span2spanset` returns two disjoint I-spans for the surviving fragments that are V-adjacent after the shift.

At most one run can be split, because each run has a disjoint ordinal range and a split requires the deletion to fall strictly within a run's interior.

**D7** (*run decomposition*). After DELETE(d, s, ℓ), one valid post-state run decomposition is obtained by classifying each pre-state run according to its interaction with [s, s + ℓ) as described above. The result has:

- Before-runs unchanged
- After-runs V-shifted by −ℓ, I-addresses unchanged
- Deleted runs removed
- Left-truncated and right-truncated runs clipped
- At most one split run producing two fragments

**D8** (*run count bound*). If m is the number of correspondence runs before DELETE and m_d is the number of runs entirely within the deleted span, the post-state run count is at most m − m_d + 1.

*Derivation.* Every before-run and after-run contributes 1 to the count. Every deleted run contributes 0. A left-truncated or right-truncated run contributes 1 (it loses width but remains one run). A split run contributes 2. At most one run can be split (contributing +1 relative to its original count of 1). The deleted runs contribute −m_d. Total: m − m_d + 1 when a split occurs, m − m_d otherwise. ∎

For a deletion that falls entirely within a single run (the common case of deleting a contiguous passage of originally-typed text), m_d = 0 and the count goes from m to m + 1 — one run is split into two. Gregory confirms this monotonic tendency: the implementation performs no post-delete compaction. Two crums that become I-address-contiguous after deletion remain separate permanently. The `isanextensionnd` merging check is wired exclusively into the INSERT path.

We note a consequence. The run count can grow unboundedly through repeated insert-delete cycles. Each INSERT adds at most 2 runs (I8, ASN-0048). Each DELETE of an interior span adds at most 1 run (from a split). Over a history of C insertions and D interior deletions, the run count is bounded by 1 + 2C + D (starting from 1 run). In practice this is the number of correspondence runs in the document's internal representation — the "fragmentation cost" of editing.


## The identity question

Having established that DELETE removes V-mappings while preserving I-space content, we face a natural question: if the deleted content is later re-introduced into the document, is it the "same" content?

The answer depends entirely on which operation is used.

**INSERT re-introduces by value.** If an editor deletes the word "hello" and later types "hello" again, INSERT allocates fresh I-addresses (by I0, ASN-0048): a₁', ..., a₅' with a_i' ∉ dom(C) at allocation time. By GlobalUniqueness (ASN-0034), a_i' ≠ a_i for every previously allocated address. The new content has the same *value* as the deleted content but a different *identity*. Any link whose endset referenced the original I-addresses will not resolve to the re-typed text. Any document transcluding the original I-addresses will not reflect the re-typed text. The provenance records will attribute the new text to the current document owner at the current time, not to the original author.

**COPY re-introduces by identity.** If instead the editor uses COPY to transclude the same I-addresses from a source that still contains them — a prior version of the document, or another document that transcludes the original content — the I-addresses are shared (by C0, ASN-0049). Links resolve. Transclusions reflect. Provenance traces to the original author.

**D9** (*identity distinction after deletion*). Let A_del = {M(d)([s + k]) : 0 ≤ k < ℓ} be the set of I-addresses removed by DELETE(d, s, ℓ). Then:

(a) A subsequent INSERT of character-identical content into d produces addresses A_new with `A_new ∩ A_del = ∅`.

(b) A subsequent COPY that transcludes from a source mapping to addresses in A_del places those same addresses into d's arrangement: for each a ∈ A_del ∩ ran(M(d_s)), the COPY maps a V-position in d to a.

*Derivation.* (a) By I0 (ASN-0048), INSERT allocates fresh addresses A_new ⊆ T \ dom(C'). By D4, A_del ⊆ dom(C'). Therefore A_new ∩ A_del = ∅. (b) By the COPY postcondition C1(f) (ASN-0049), M'(d)(q_k) = M(d_s)(p_s ⊕ [k]). If M(d_s)(p_s ⊕ [k]) = a ∈ A_del, then a appears in d's post-COPY arrangement. The I-address is the same object. ∎

This is S4 (OriginBasedIdentity, ASN-0036) in its most operationally consequential form. Identity is creation, not value. Two identical texts created independently are two different things. The same text re-transcluded from its original home is the same thing returning.


## Link endset persistence

We do not formalize links in this ASN, but we record a critical consequence of DELETE's frame conditions. Links in Xanadu attach to I-space addresses — to content identity, not V-space position. Nelson: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes."

A link endset is a set of I-space addresses. When DELETE removes a span from d's arrangement:

**D10** (*link target persistence*). For any set of I-addresses L ⊆ dom(C):

(a) `(A a ∈ L :: a ∈ dom(C'))` — every referenced address persists (by D-frame(a))

(b) `(A a ∈ L :: C'(a) = C(a))` — content at each address is unchanged (by D-frame(a))

(c) L itself is not modified — DELETE touches only M(d). No other state component is altered.

Nelson's survivability condition — "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end" — is always satisfied after a DELETE, because DELETE never removes I-space content. The bytes the link references still exist. The link survives unconditionally.

The nuance is in *resolution*, not *existence*. After DELETE, a link resolver that must convert I-addresses to V-positions in document d will find that some I-addresses in the endset have no current V-mapping in d. Gregory's implementation evidence is precise: `span2spanset`, when asked to resolve an endset that partially overlaps deleted content, returns V-spans only for the surviving fragments. The deleted interior produces no V-output — it is silently dropped. The result is two V-adjacent spans (the gap has closed in V-space) that are I-noncontiguous (the deleted content's I-addresses form the gap in I-space).

This partial resolution is not a failure mode. It is the correct behavior. The link still exists. The endset still references all the original I-addresses. The *resolution through a particular document's arrangement* may be partial, reflecting the fact that the document no longer includes all the linked content. The same endset resolved through a different document that transcludes the full range — or through a prior version of d — returns the complete set of V-positions.


## Historical retrievability

Nelson guarantees: "when you ask for a given part of a given version at a given time, it comes to your screen." This guarantee requires that the pre-delete arrangement M(d) be reconstructible after DELETE. We verify that the system preserves enough information.

**D11** (*DELETE invertibility*). The transition Σ →_{DELETE(d,s,ℓ)} Σ' is invertible: given Σ' and the parameters (d, s, ℓ), the pre-state arrangement M(d) is uniquely determined.

*Derivation.* We recover M(d) from M'(d) and (s, ℓ). The skip function σ is invertible (D3 gives bijectivity); its inverse σ⁻¹ maps old positions to new:

`σ⁻¹(y) = y` when 1 ≤ y < s

`σ⁻¹(y) = y − ℓ` when s + ℓ ≤ y ≤ N

For surviving positions: `M(d)([y]) = M'(d)([σ⁻¹(y)])` for y ∈ [1, N] \ [s, s + ℓ).

The I-addresses of the deleted positions are not recoverable from M'(d) alone. We need the deleted content's addresses — A_del — stored or derivable from the operation log. The provenance relation R contains (a, d) for every a ∈ A_del (from a prior INSERT or COPY that placed a in d's arrangement), but R does not record the V-positions those addresses occupied. Reconstruction of the V-ordering of deleted content requires the operation parameters (s, ℓ) together with the content that was at those positions.

This is precisely where the operation log — what Nelson calls the historical trace — is load-bearing. The system must record, for each DELETE, the triple (d, s, ℓ) and the sequence of I-addresses M(d)([s]), M(d)([s + 1]), ..., M(d)([s + ℓ − 1]) that were removed. With this information plus the post-state M'(d), the pre-state M(d) is uniquely and fully recoverable. ∎

The operational parameters alone do not suffice: we also need the deleted I-addresses. But the content store C is unchanged by DELETE, so the *values* of those I-addresses are permanently available. The challenge is knowing *which* I-addresses were removed and in *what order*. This is the job of the historical trace.

Nelson's model makes this natural. The append-only storage paradigm records "each change as it arrives, but keeping the former changes." DELETE, as a change, is recorded in the historical trace. The trace entry captures enough information to invert the operation: the parameters, the removed I-addresses, and thereby the complete prior arrangement.


## Preservation of invariants

We verify that DELETE maintains the invariants established by ASN-0036 and ASN-0047.

**D0 (V-Contiguity).** By D-post(b): dom(M'(d)) ∩ text-subspace = {[x] : 1 ≤ x ≤ N − ℓ}. This is a contiguous interval with N'(d) = N(d) − ℓ. ✓

**S0 (ContentImmutability).** D-frame(a): C' = C. For every a ∈ dom(C), a ∈ dom(C') and C'(a) = C(a). ✓

**S2 (ArrangementFunctional).** M'(d) is a function because M(d) is a function and σ is injective: M'(d)([x]) = M(d)([σ(x)]) maps distinct x to distinct σ(x), and M(d) resolves each uniquely. ✓

**S3 (ReferentialIntegrity).** For v ∈ dom(M'(d)), M'(d)(v) = M(d)([σ(ord(v))]) where σ(ord(v)) ∈ dom(M(d)). Pre-state S3 gives M(d)([σ(ord(v))]) ∈ dom(C), and dom(C) = dom(C') by D-frame(a). ✓

**S8a (VPositionWellFormed).** Positions with ordinal < s are unchanged. Positions with ordinal ≥ s in the post-state have old ordinal ≥ s + ℓ ≥ 2, and their new ordinal is positive (subtracting ℓ from an ordinal ≥ s + ℓ ≥ ℓ + 1 gives ≥ 1). ✓

**S8-depth (FixedDepthPositions).** Shifting by ℓ within the ordinal-only formulation does not change tumbler depth: [x − ℓ] has the same depth as [x]. ✓

**S8-fin (FiniteArrangement).** |dom(M'(d))| = |dom(M(d))| − ℓ, finite. ✓

**P0 (ContentPermanence).** D-frame(a): C' = C. ✓

**P1 (EntityPermanence).** D-frame(b): E' = E ⊇ E. ✓

**P2 (ProvenancePermanence).** D-frame(d): R' = R ⊇ R. ✓

**P4 (ProvenanceBounds).** We need Contains(Σ') ⊆ R'. For (a, d') ∈ Contains(Σ'): if d' ≠ d, M'(d') = M(d') by D-frame(c), so (a, d') ∈ Contains(Σ) ⊆ R = R'. If d' = d, a ∈ ran(M'(d)) ⊆ ran(M(d)) (DELETE only removes from ran), so (a, d) ∈ Contains(Σ) ⊆ R = R'. ✓


## Implementation observations

Gregory's implementation evidence reveals several concrete consequences of the abstract properties.

*Spanfilade over-approximation.* The implementation maintains a global content-discovery index (the spanfilade) that records which documents contain which I-addresses. DELETE does not update this index — it is append-only. After DELETE(d, s, ℓ), the index still reports that d contains the deleted I-addresses. The result is an over-approximation: the set of documents returned by `find_documents_containing(a)` is a superset of {d : a ∈ ran(M(d))}. This is architecturally tolerable because false positives can be filtered (check the current arrangement) while false negatives cannot be recovered (a document might never be discovered). If the same content is later re-transcluded into d via COPY, a second entry accumulates in the index without deduplication. Both stale and fresh entries coexist permanently.

*Fragmentation monotonicity.* The implementation performs no post-delete compaction of correspondence runs. Two runs that become I-address-contiguous after deletion (because the intervening content was removed) remain separate permanently. The `isanextensionnd` adjacency check is wired exclusively into the INSERT path. This means the number of internal mapping entries can only grow through editing cycles — DELETE reduces the total content but may increase the structural fragmentation.

*Subspace interaction.* DELETE's implementation-level isolation between text and link subspaces relies on an arithmetic guard (`strongsub`'s exponent comparison) that is fragile: it fails when the deletion width and the link-crum displacement share the same tumbler exponent class. The abstract specification D-frame(e) requires subspace isolation unconditionally. Any correct implementation must ensure that a text-subspace DELETE cannot shift, split, or destroy link-subspace entries.


## Worked example

We verify the postconditions against concrete values. Let d have arrangement M(d) = {[1] ↦ a, [2] ↦ b, [3] ↦ c, [4] ↦ d₀, [5] ↦ e₀} where a through e₀ are consecutive I-addresses forming a single run: a = [x], b = [x+1], c = [x+2], d₀ = [x+3], e₀ = [x+4]. N(d) = 5. We DELETE with s = 2, ℓ = 2 — removing positions [2] and [3] (content b and c).

**Skip function.** σ(1) = 1 (below s = 2). σ(2) = 2 + 2 = 4. σ(3) = 3 + 2 = 5.

**Post-state.** M'(d) = {[1] ↦ M(d)([σ(1)]) = a, [2] ↦ M(d)([σ(2)]) = M(d)([4]) = d₀, [3] ↦ M(d)([σ(3)]) = M(d)([5]) = e₀}. That is: M'(d) = {[1] ↦ a, [2] ↦ d₀, [3] ↦ e₀}. N'(d) = 3.

**D0 check.** dom(M'(d)) ∩ text-subspace = {[1], [2], [3]} = {[x] : 1 ≤ x ≤ 3}. Contiguous. ✓

**D4 check.** A_del = {b, c} = {[x+1], [x+2]}. Both remain in dom(C') = dom(C). ✓

**Run decomposition (D7).** The original single run ([1], a, 5) is Class S (split): the deletion [2, 4) falls in its interior. Left fragment: ([1], a, 1) — just position [1] mapping to a. Right fragment: old start is s + ℓ = 4, I-start is a ⊕ [4 − 1] = a ⊕ [3] = d₀, width is 5 − (2 + 2 − 1) = 5 − 3 = 2; after shift, new ordinal start is 2. Post-state run: (2, d₀, 2). Check: M'(d)([2]) = d₀ = d₀ ⊕ [0], M'(d)([3]) = e₀ = d₀ ⊕ [1]. ✓

Pre-state: 1 run. Post-state: 2 runs (one split). Count = 1 − 0 + 1 = 2, confirming D8.

**Frame checks.** C' = C, E' = E, R' = R, M'(d') = M(d') for all d' ≠ d. ✓

**D9 check (identity).** Suppose we now INSERT "bc" at position [2]. The INSERT allocates fresh addresses b', c' with b' ≠ b and c' ≠ c (by I0 and D4: b, c ∈ dom(C'), so b', c' ∉ dom(C') at allocation time means b' ≠ b, c' ≠ c). The "same text" is new content. Alternatively, if we COPY from a document d' where M(d')([j]) = b and M(d')([j+1]) = c, the COPY places b and c — the original addresses — back into d. The original content returns with its identity intact.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| D0 | V-contiguity: for each d, text-subspace dom(M(d)) = {[x] : 1 ≤ x ≤ N(d)} for some N(d) ≥ 0 | introduced |
| D1 | Skip function σ is strictly monotone on [1, N − ℓ] | introduced |
| D2 | ran(σ) = [1, N] \ [s, s + ℓ) — maps onto exactly the surviving positions | introduced |
| D3 | σ is a bijection from [1, N − ℓ] to the surviving positions | introduced |
| D-pre | Precondition: d ∈ E_doc ∧ ℓ ≥ 1 ∧ 1 ≤ s ∧ s + ℓ − 1 ≤ N(d) | introduced |
| D-post | Postcondition: M'(d)([x]) = M(d)([σ(x)]) for 1 ≤ x ≤ N − ℓ; contiguous domain; C, E, R unchanged; other documents unchanged | introduced |
| D-frame | Frame: C' = C (entire content store); E' = E; R' = R; other documents' arrangements; link subspace of d | introduced |
| D4 | Content survival: `(A a ∈ A_del :: a ∈ dom(C'))` | introduced |
| D5 | Cross-document isolation: `(A d' ≠ d :: M'(d') = M(d'))` | introduced |
| D6 | Order preservation: σ(x₁) < σ(x₂) for x₁ < x₂ among surviving positions | introduced |
| D7 | Run decomposition: pre-state runs transform by classification (B, A, D, L, R, S) into post-state runs | introduced |
| D8 | Run count bound: post-state ≤ m − m_d + 1 where m is pre-state count, m_d is fully deleted runs | introduced |
| D9 | Identity distinction: INSERT after DELETE creates new identity (A_new ∩ A_del = ∅); COPY restores same identity | introduced |
| D10 | Link target persistence: all I-addresses persist with unchanged content after DELETE | introduced |
| D11 | DELETE invertibility: pre-state M(d) uniquely recoverable from post-state, parameters, and deleted I-addresses | introduced |


## Open Questions

Must the historical trace record the full sequence of deleted I-addresses, or can the system reconstruct which addresses were removed from the operation parameters and the content store alone?

What invariants must a content discovery index satisfy — must it reflect current arrangements precisely, or is over-approximation (reporting documents that previously but no longer contain an address) an acceptable design?

Under what conditions does partial link resolution — returning V-spans for only the surviving fragments of an endset — degrade gracefully, and what must the system guarantee about the relationship between partial resolutions through different documents?

Must the run decomposition after DELETE be minimal (adjacent runs merged when I-contiguous), or may a conforming implementation maintain redundant run boundaries indefinitely?

What must the system guarantee about the interaction between DELETE and subspace boundaries — must text-subspace deletion be provably incapable of affecting the link subspace at the abstract level, and if so, what structural invariant provides this guarantee?

What constraints must version creation impose on the temporal relationship with DELETE — must a version snapshot capture the arrangement at a single instant, or may it interleave with an in-progress deletion?

When a document's entire text content is deleted but links remain, what must the system guarantee about the retrievability and addressing of the surviving link subspace?
