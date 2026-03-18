# ASN-0049: COPY Operation — Transclusion as Identity-Preserving Arrangement Extension

*2026-03-18*

We ask: what happens when content from one document appears in another without duplication? The question separates into three parts — what is shared, what is independent, and what invariants hold across the connection. The answer turns on a single architectural choice: COPY creates new arrangement without creating new content. Every guarantee of transclusion follows from this distinction.


## The central distinction

The two-space model (ASN-0036) separates content storage C : T ⇀ Val from content arrangement M(d) : T ⇀ T. This separation opens a choice. When we want content from document d_s to appear in document d_t, there are exactly two mechanisms:

(a) *Allocation*: invoke K.α to create fresh I-addresses, store identical content values, then invoke K.μ⁺ to map new V-positions to these fresh addresses. The content in d_t has a different identity — same value, different address.

(b) *Reference*: invoke K.μ⁺ to map new V-positions in d_t directly to the I-addresses already present in ran(M(d_s)). No new content is allocated. The identity of the content is shared.

INSERT uses mechanism (a). COPY uses mechanism (b). Nelson states the design intent without qualification:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Gregory confirms the implementation realises this exactly:

> "COPY is the identity-preserving operation... COPY shares the source's existing I-addresses in the target document's POOM." [ST-COPY, Finding 0064]

> "docopy never calls findisatoinsertgr or inserttextingranf. Contrast with INSERT, which calls those to allocate fresh I-addresses." [INV-IADDR-PROVENANCE]


## Source projection

COPY requires a mechanism to extract I-addresses from a source document. The source is specified as V-positions in d_s; we must resolve them through d_s's arrangement to obtain the I-addresses they reference.

**Definition — Projection.** For d ∈ E_doc and V-span (v, n) with n ≥ 1 and [v, v ⊕ [n]) ⊆ dom(M(d)), the *projection* is:

`proj(d, v, n)(k) = M(d)(v ⊕ [k])    for 0 ≤ k < n`

where v ⊕ [k] denotes ordinal increment within the subspace (TA7a, ASN-0034). The projection is well-defined by S2 (arrangement functional) and yields values in dom(C) by S3 (referential integrity).

The projection is a pure query — it reads M(d) without modifying any state component. Its image decomposes by S8 (span decomposition, ASN-0036) into correspondence runs. We record this decomposition for later use.

**Lemma — Projection decomposition.** There exist I-spans (a₁, w₁), ..., (aₘ, wₘ) such that:

(i) `(+ j : 1 ≤ j ≤ m : wⱼ) = n` — the widths sum to the source width.

(ii) `(A j : 1 ≤ j ≤ m :: (A k : 0 ≤ k < wⱼ :: proj(d, v, n)((+ i : 1 ≤ i < j : wᵢ) + k) = aⱼ ⊕ [k]))` — within each span, I-addresses are contiguous.

(iii) `(A j : 1 ≤ j < m :: aⱼ ⊕ [wⱼ] ≠ aⱼ₊₁)` — adjacent spans are I-address non-contiguous (maximality).

*Derivation.* By S8, M(d) restricted to the text subspace decomposes into correspondence runs. The V-span [v, v ⊕ [n]) intersects some of these runs. Interior runs are included whole; boundary runs are clipped. Clipping a run (v_r, a_r, n_r) at offset δ produces a sub-run with I-start a_r ⊕ [δ] and width n_r − δ (or the clip width, whichever is smaller). The clipped sub-run preserves the correspondence property because `M(d)((v_r ⊕ [δ]) ⊕ [k]) = a_r ⊕ [δ + k] = (a_r ⊕ [δ]) ⊕ [k]` by associativity of tumbler addition (ASN-0034). ∎

The number m of I-spans in the projection reflects the fragmentation of the source content in I-space. Content created by a single INSERT is a single run (by sequential allocation). Content assembled from multiple INSERTs, or content that has been rearranged, may fragment into multiple runs.


## The V-shift

COPY, like INSERT, must make room in the target document's arrangement when the insertion point falls within existing content. The mechanism is the same: shift existing V-positions forward to create a gap. We define this locally, noting the essential properties.

**Definition — V-shift.** For insertion point p in the text subspace of d_t with ordinal p̂ = ord(p) and width n ≥ 1, define:

`σ(v) = v` when ord(v) < p̂ or v is not in the text subspace

`σ(v) = v ⊕ [n]` when v is in the text subspace and ord(v) ≥ p̂

The shift satisfies: injectivity (distinct inputs produce distinct outputs), order preservation (v₁ < v₂ implies σ(v₁) < σ(v₂) within the text subspace), gap creation (no position maps into [p̂, p̂ + n)), and subspace confinement (σ is the identity outside the text subspace). These follow from the reasoning in TA7a (subspace closure, ASN-0034) and T7 (subspace disjointness, ASN-0034).


## COPY as composite transition

We assemble the full operation. COPY of n content units from document d_s at V-position p_s into document d_t at V-position p_t is a composite transition (ASN-0047, ValidCompositeTransition) consisting of three phases. Let p̂_s = ord(p_s) and p̂_t = ord(p_t).

**CP0** (*COPY precondition*). `d_s ∈ E_doc ∧ d_t ∈ E_doc ∧ n ≥ 1 ∧ [p_s, p_s ⊕ [n]) ⊆ dom(M(d_s)) ∧ S8a(p_t)`

The source span must exist in d_s, and the target position must be well-formed. When d_s = d_t, the precondition is evaluated against the pre-state arrangement.

**Phase 1** — *Arrangement shift* (K.μ~). Apply the bijection σ to M(d_t)'s domain:

`(A v : v ∈ dom(M(d_t)) : M₁(d_t)(σ(v)) = M(d_t)(v))`

with dom(M₁(d_t)) = σ(dom(M(d_t))). This is a valid K.μ~ reordering: σ is injective, and ran(M₁(d_t)) = ran(M(d_t)) since only V-positions change. Frame: C₁ = C; E₁ = E; R₁ = R; M₁(d') = M(d') for d' ≠ d_t.

When d_s = d_t: the projection proj(d_s, p_s, n) was computed from M(d_s) = M(d_t) in the *pre-state*, before this shift. The shift changes V-positions in d_t but does not alter the I-addresses that the projection resolved.

When dom(M(d_t)) has no text-subspace positions with ordinal ≥ p̂_t — insertion at the end, or into an empty document — σ is the identity, and Phase 1 is a no-op.

**Phase 2** — *Arrangement extension* (K.μ⁺). Add n new mappings at the V-positions in the gap. Let q_k denote the text-subspace V-position with ordinal p̂_t + k, for 0 ≤ k < n. Then:

`(A k : 0 ≤ k < n : M'(d_t)(q_k) = proj(d_s, p_s, n)(k))`

That is, `M'(d_t)(q_k) = M(d_s)(p_s ⊕ [k])` — the I-address at source V-position p_s + k.

The precondition for K.μ⁺ requires each target address to be in dom(C). We have M(d_s)(p_s ⊕ [k]) ∈ dom(C) by S3 applied to d_s. Phase 1 held C in frame (C₁ = C), so the addresses remain in dom(C₁). The new V-positions satisfy S8a (subspace identifier ≥ 1, ordinal ≥ 1, all components positive) and S8-depth (same depth as p_t). Frame: C' = C₁ = C; E' = E; R' = R; M'(d') = M(d') for d' ≠ d_t.

**Phase 3** — *Provenance recording* (K.ρ). For each I-address a ∈ ran(M'(d_t)) \ ran(M(d_t)), record (a, d_t) ∈ R'. Frame: C' unchanged; E' unchanged; M' unchanged.

**No K.α appears.** This is the defining distinction from INSERT. INSERT consists of K.α (allocation), K.μ~ (shift), K.μ⁺ (extension), K.ρ (provenance). COPY omits K.α entirely. The content store is untouched.


## Coupling constraints

We verify the coupling constraints of ASN-0047.

**J0** (AllocationRequiresPlacement): dom(C') \ dom(C) = ∅ because no K.α occurs. The quantifier `(A a : a ∈ dom(C') \ dom(C) : ...)` is vacuously satisfied. ✓

**J1** (ExtensionRecordsProvenance): Each a ∈ ran(M'(d_t)) \ ran(M(d_t)) has (a, d_t) ∈ R' via Phase 3. To confirm a is genuinely new: if a ∈ ran(M(d_t)) already, then a ∉ ran(M'(d_t)) \ ran(M(d_t)), so no provenance recording is needed for previously-referenced addresses (P2 ensures any prior (a, d_t) ∈ R persists). ✓

**J1'** (ProvenanceRequiresExtension): Each (a, d_t) ∈ R' \ R satisfies a ∈ ran(M'(d_t)) \ ran(M(d_t)) by Phase 3's construction. ✓

The intermediate states satisfy their elementary preconditions: K.μ~ requires d_t ∈ E_doc (by CP0); K.μ⁺ requires M(d_s)(p_s ⊕ [k]) ∈ dom(C₁) (established by S3 on d_s and Phase 1's frame C₁ = C); K.ρ requires a ∈ dom(C') ∧ d_t ∈ E_doc (both satisfied). COPY is a valid composite transition. ✓


## Identity preservation

We now state the property that distinguishes COPY from every other arrangement-modifying operation.

**C0** (*identity preservation*). For every COPY transition Σ → Σ':

`dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a))`

No new address enters dom(C). No existing content value changes. The content store is held completely in frame.

*Derivation.* The elementary decomposition of COPY contains no K.α. K.μ~, K.μ⁺, and K.ρ all hold C in frame (by their frame conditions in ASN-0047). The composite therefore holds C in frame. ∎

S0 (content immutability, ASN-0036) guarantees that no operation *modifies* existing content. C0 is stronger: it guarantees that COPY does not even *extend* dom(C). The set of content identities in the system is unchanged by COPY.

**C0a** (*pre-existing references*). After COPY:

`ran(M'(d_t)) \ ran(M(d_t)) ⊆ ran(M(d_s))`

Every I-address newly appearing in d_t's arrangement was already referenced by d_s's arrangement.

*Derivation.* By Phase 2, for each k ∈ [0, n), M'(d_t)(q_k) = M(d_s)(p_s ⊕ [k]) ∈ ran(M(d_s)). By Phase 1, all other mappings in M'(d_t) are carried from M(d_t) — M'(d_t)(σ(v)) = M(d_t)(v). The only new I-addresses in ran(M'(d_t)) come from Phase 2, hence from ran(M(d_s)). ∎


## Postcondition and frame

**C1** (*COPY postcondition*). The post-state Σ' = (C', E', M', R') satisfies:

(a) `dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a))` — content unchanged

(b) `E' = E`

(c) `(A d' : d' ≠ d_t : M'(d') = M(d'))`

(d) `dom(M'(d_t)) = σ(dom(M(d_t))) ∪ {q_k : 0 ≤ k < n}`

(e) `(A v ∈ dom(M(d_t)) :: M'(d_t)(σ(v)) = M(d_t)(v))` — existing mappings preserved (shifted)

(f) `(A k : 0 ≤ k < n : M'(d_t)(q_k) = M(d_s)(p_s ⊕ [k]))` — new mappings from source

(g) `R' ⊇ R ∧ (A a ∈ ran(M'(d_t)) \ ran(M(d_t)) :: (a, d_t) ∈ R')`

Clause (f) references M(d_s) in the *pre-state*. The projection is evaluated before placement occurs. When d_s = d_t, this is the arrangement before the gap is made.

**C-frame** (*COPY frame*). What COPY does not change:

(a) `(A a ∈ dom(C) :: C'(a) = C(a))` — existing content untouched

(b) `E' = E` — no entity created or destroyed

(c) `(A d' : d' ≠ d_t : M'(d') = M(d'))` — other documents untouched, including d_s when d_s ≠ d_t

(d) `R' ⊇ R` — existing provenance preserved


## Preservation

We verify that COPY maintains the invariants established by ASN-0036 and ASN-0047.

**S0 (ContentImmutability).** Holds by C1(a) directly. COPY does not modify C at all.

**S3 (ReferentialIntegrity).** We ask: is every I-address in ran(M'(d_t)) in dom(C')? For shifted positions, M'(d_t)(σ(v)) = M(d_t)(v), and M(d_t)(v) ∈ dom(C) by pre-state S3, and dom(C) = dom(C') by C0. For new positions, M'(d_t)(q_k) = M(d_s)(p_s ⊕ [k]) ∈ dom(C) by pre-state S3 on d_s, and dom(C) = dom(C') by C0. ✓

**S2 (ArrangementFunctional)** for M'(d_t). The domain is σ(dom(M(d_t))) ∪ {q_k : 0 ≤ k < n}. These two sets are disjoint by gap creation (σ maps no position into [p̂_t, p̂_t + n)). Within each set, the mapping is functional: σ(dom(M(d_t))) inherits functionality from M(d_t) via the bijection σ; the new positions map to well-defined I-addresses via the projection. ✓

**S8a, S8-depth, S8-fin.** Shifted positions preserve S8a and depth by subspace closure (TA7a). New positions q_k: subspace identifier ≥ 1 and ordinal p̂_t + k ≥ 1, so all components positive; depth matches the subspace's common depth. Finiteness: |dom(M'(d_t))| = |dom(M(d_t))| + n, finite. ✓

**P0 (ContentPermanence).** By C1(a). ✓

**P1 (EntityPermanence).** By C1(b): E' = E ⊇ E. ✓

**P2 (ProvenancePermanence).** By C1(g): R' ⊇ R. ✓

**P4 (ProvenanceBounds).** We need Contains(Σ') ⊆ R'. For (a, d') ∈ Contains(Σ'): if d' ≠ d_t, then M'(d') = M(d') by C-frame(c), so (a, d') ∈ Contains(Σ) ⊆ R ⊆ R'. If d' = d_t, then either a ∈ ran(M(d_t)) (giving (a, d_t) ∈ Contains(Σ) ⊆ R ⊆ R') or a ∈ ran(M'(d_t)) \ ran(M(d_t)) (giving (a, d_t) ∈ R' by C1(g)). ✓

**P6, P7, P7a.** P6 (ExistentialCoherence): no fresh I-addresses, so no new origins to verify; existing origins survive by P1. P7 (ProvenanceGrounding): for new (a, d_t) ∈ R' \ R, a ∈ ran(M'(d_t)) ⊆ dom(C) = dom(C'). P7a (ProvenanceCoverage): dom(C') = dom(C), so pre-state P7a suffices. ✓


## Document isolation

Clause C-frame(c) — `(A d' : d' ≠ d_t : M'(d') = M(d'))` — deserves emphasis. The source document's arrangement is read but never modified. This is not an incidental frame condition; it is the architectural guarantee that makes transclusion safe.

**C2** (*source invariance*). When d_s ≠ d_t:

`M'(d_s) = M(d_s)`

The source document's arrangement is identical before and after COPY. COPY reads M(d_s) to resolve the projection; it writes only to M(d_t).

*Derivation.* Every elementary transition in COPY's decomposition (K.μ~, K.μ⁺, K.ρ) modifies at most one arrangement — K.μ~ and K.μ⁺ target d_t specifically — and holds all other arrangements in frame. ∎

This generalises. Not only does COPY not modify the source, but *no subsequent operation on the target can affect the source*, and *no subsequent operation on the source can affect the target*:

**C3** (*arrangement independence*). For documents d₁, d₂ ∈ E_doc with d₁ ≠ d₂, and any valid transition Σ → Σ' that modifies only d₁'s arrangement:

`M'(d₂) = M(d₂)`

*Derivation.* Every elementary transition that modifies an arrangement (K.μ⁺, K.μ⁻, K.μ~) takes a single document parameter and holds all other arrangements in frame. Composite transitions, being sequences of elementary transitions, preserve this per-document isolation. ∎

Nelson states this as a design guarantee:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Gregory confirms the mechanism:

> "makegappm operates on a single POOM tree. There is no global POOM registry, no mechanism to enumerate other documents' orgl trees, and no lookup path from a V-position to all POOMs that share I-addresses at this position."

The shared I-addresses are citations, not structural couplings. Two documents that cite the same I-address do not become entangled.


## Isolation under subsequent operations

C3 has concrete consequences when operations follow a COPY. We trace the three arrangement-modifying operations applied to the source.

**C3a** (*INSERT into source*). INSERT(d_s, v, text) after COPY(d_s, p_s, n, d_t, p_t):

(i) Allocates fresh I-addresses for text (K.α). These addresses are not in dom(C) at COPY time, hence not in ran(M(d_t)) — they are unknown to d_t.

(ii) Modifies M(d_s) — shifts V-positions, adds new mappings.

(iii) Has no effect on M(d_t) — by C3.

The transcluding document continues to reference the same I-addresses at the same V-positions. The fresh content in d_s has addresses that d_t has never seen (by GlobalUniqueness, ASN-0034).

**C3b** (*DELETE from source*). DELETE(d_s, v, w) after COPY:

(i) Removes V→I mappings from M(d_s) — by K.μ⁻.

(ii) Does not remove the I-addresses from dom(C) — by S0 (content immutability).

(iii) Has no effect on M(d_t) — by C3.

This is perhaps the most consequential case. The source author deletes content from their own document. The content persists in I-space (S0), and d_t's arrangement still references it. The target is unaffected. Nelson is explicit:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

We can state this in weakest-precondition form. Let a be an I-address with a ∈ ran(M(d_t)) ∩ ran(M(d_s)):

`wp(DELETE(d_s, ...), a ∈ ran(M(d_t)) ∧ a ∈ dom(C) ∧ C(a) unchanged)`

`= {C3 gives M(d_t) in frame; S0 gives C in frame}`

`a ∈ ran(M(d_t)) ∧ a ∈ dom(C)`

which holds by hypothesis. The target's view of the shared content is immune to source-side deletion. ∎

**C3c** (*REARRANGE in source*). K.μ~ on d_s:

(i) Changes V-positions within M(d_s), preserving ran(M(d_s)).

(ii) Has no effect on M(d_t) — by C3.

The source author reorders their document freely. The target is unaware of the rearrangement because it does not reference d_s's V-positions — it references I-addresses, which are unaffected by V-space operations.


## Transitivity of identity

We turn to a subtler property. When d_b transcludes content from d_a, and d_c transcludes that content from d_b, what I-addresses does d_c hold?

**C4** (*transitive identity*). Let COPY(d_a, v_a, n, d_b, v_b) produce state Σ₁, and COPY(d_b, v_b, n, d_c, v_c) produce state Σ₂. Then:

`(A k : 0 ≤ k < n : M₂(d_c)(v_c ⊕ [k]) = M₀(d_a)(v_a ⊕ [k]))`

The chain d_a → d_b → d_c is *transparent*. d_c holds d_a's original I-addresses. No intermediate identity is created.

*Derivation.* From the first COPY, by C1(f):

`M₁(d_b)(v_b ⊕ [k]) = M₀(d_a)(v_a ⊕ [k])    for 0 ≤ k < n`

From the second COPY, by C1(f):

`M₂(d_c)(v_c ⊕ [k]) = M₁(d_b)(v_b ⊕ [k])    for 0 ≤ k < n`

Substituting:

```
M₂(d_c)(v_c ⊕ [k])
= M₁(d_b)(v_b ⊕ [k])         {C1(f), second COPY}
= M₀(d_a)(v_a ⊕ [k])         {C1(f), first COPY}
```

The chain telescopes. ∎

This generalises by induction to chains of arbitrary length. For any sequence d₀ → d₁ → ... → d_r of COPYs over the same content, every document in the chain holds d₀'s original I-addresses.

Gregory confirms the mechanism:

> "After A→B transclusion: poom(B)[v_b] = I_a (A's original I-address). After B→C transclusion, vspanset2sporglset runs against B, reads the same I_a from B's POOM, and writes it into C: poom(C)[v_c] = I_a (still A's original I-address). The chain telescopes to a single flat identity assignment."

**C4a** (*chain indistinguishability*). The state produced by COPY(d_a, v_a, n, d_c, v_c) — a direct COPY — is indistinguishable from the state produced by the two-hop chain d_a → d_b → d_c, as far as d_c's arrangement is concerned. The I-addresses at the same V-positions are identical. No query against d_c can determine whether the content arrived directly or through an intermediary.


## Origin traceability

By S7 (structural attribution, ASN-0036), every I-address a ∈ dom(C) encodes its origin document in its tumbler structure: origin(a) extracts the document-level prefix N.0.U.0.D. This is the document that first allocated the address — the document in which INSERT was called.

COPY preserves I-addresses unchanged (C0). Therefore:

**C5** (*origin preservation*). For every V-position q_k created by COPY:

`origin(M'(d_t)(q_k)) = origin(M(d_s)(p_s ⊕ [k]))`

The origin of the content, as encoded in the I-address, is the document that originally allocated it — which may be d_s, or (by C4) may be some earlier document in a transclusion chain. The origin is not d_t, unless d_t happens to be the document that originally created the content.

This is not metadata that can be stripped or falsified. The origin IS the address. To retrieve the content at all, the system must request it from the home location identified by origin(a). Attribution is a structural consequence of addressing.

Nelson states this guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]


## Correspondence runs under COPY

The arrangement's text subspace decomposes into correspondence runs (S8, ASN-0036). We trace how COPY transforms this decomposition in d_t.

Let {(vⱼ, aⱼ, nⱼ) : 1 ≤ j ≤ m_t} be d_t's pre-COPY run decomposition, ordered by V-ordinal. Let [(a'₁, w₁), ..., (a'_{m_s}, w_{m_s})] be the projection decomposition of the source span (the I-spans being copied).

**C6** (*run transformation*). One valid post-COPY run decomposition is:

(a) *Before-runs*: runs entirely below p̂_t are unchanged.

(b) *After-runs*: runs entirely at or above p̂_t are V-shifted by n, I-addresses unchanged.

(c) *Split run*: if the insertion point falls within a run, it splits into two fragments, as for INSERT.

(d) *New runs*: the m_s I-spans from the projection decomposition become m_s correspondence runs at V-positions q_0, q_{w₁}, q_{w₁+w₂}, etc. — each I-span contributes one run.

**C7** (*run count bound*). If m_t is d_t's pre-COPY run count and m_s is the number of I-spans in the projection decomposition, the post-COPY run count is at most m_t + m_s + 1.

*Derivation.* Before-runs and after-runs contribute their original count (m_t, or m_t − 1 + 2 = m_t + 1 if a split occurs). The source's m_s I-spans contribute at most m_s new runs. Total: at most m_t + 1 + m_s = m_t + m_s + 1 when a split occurs; m_t + m_s otherwise. ∎

The bound m_s — the number of I-spans — is determined by the source content's I-space fragmentation, not by the byte count. A single contiguous source region (m_s = 1) adds at most 2 runs regardless of width. A heavily fragmented source adds more. This cost is structural: the arrangement's complexity grows with the complexity of the content's provenance, not with the content's size.


## Link discovery through shared content

Links in Xanadu attach to I-space addresses, not V-space positions. When content is transcluded, the shared I-addresses create a bridge for link discovery. We develop a minimal link model — enough to state the discovery property. Full link specification is deferred to a separate investigation.

**Definition — Link endset.** A link l has endsets from(l), to(l), three(l), each a set of I-spans. The I-spans reference addresses in dom(C).

**Definition — Discoverable links.** For document d and V-span (v, n), the *discoverable links* are:

`discover(d, v, n) = {l : (E j : 1 ≤ j ≤ m :: endset(l) ∩ (aⱼ, wⱼ) ≠ ∅)}`

where [(a₁, w₁), ..., (aₘ, wₘ)] = proj(d, v, n) decomposed into I-spans, and ∩ denotes I-span overlap (non-empty intersection of the address ranges).

This definition operates entirely in I-space. The V-span is projected to I-spans, and links are discovered by I-span intersection. The V-addresses — which differ between documents — play no role in discovery.

**C8** (*link discovery invariance*). If two documents d₁, d₂ share I-addresses at V-spans (v₁, n) and (v₂, n) — meaning `(A k : 0 ≤ k < n : M(d₁)(v₁ ⊕ [k]) = M(d₂)(v₂ ⊕ [k]))` — then:

`discover(d₁, v₁, n) = discover(d₂, v₂, n)`

The discoverable links are identical, because the projections yield identical I-spans.

*Derivation.* proj(d₁, v₁, n)(k) = M(d₁)(v₁ ⊕ [k]) = M(d₂)(v₂ ⊕ [k]) = proj(d₂, v₂, n)(k) for all k. The projections are pointwise equal, so their I-span decompositions are identical. The discovery query, being a function of I-spans alone, returns the same result. ∎

This is the mechanism by which links "follow" transcluded content. A link created on content in d_a is discoverable from d_b (after COPY) because both documents' projections resolve to the same I-addresses. C1(f) establishes the shared I-addresses; C8 converts that sharing into link discovery equivalence.

**Corollary (C8a — transitivity of discovery).** By C4 (transitive identity), link discovery is transitive across COPY chains. If a link is discoverable from d_a's content, it is discoverable from d_c in a chain d_a → d_b → d_c, because d_c holds d_a's I-addresses.

Gregory confirms:

> "find_links operates purely on I-address intersection in the spanf enfilade. Since C holds I_a, and the spanf was indexed on I_a when the link was created on A's content, find_links on C returns the link."

**Endset resolution.** While link *discovery* is document-independent (it depends only on I-addresses), link endset *resolution* — mapping a link's endset I-addresses back to V-positions — is document-dependent. Given a link l and a document d, the resolved positions are:

`resolve(l, end, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ endset(l, end)}`

Different documents yield different V-positions for the same link endset. This is by design: each document has its own V-space, and the V-positions are local to that space.

Gregory confirms the parametric nature:

> "followlink(link, whichend, homedoc) = { v | ∃ i ∈ endset(link, whichend) : poom.homedoc(v) = i }. The caller explicitly specifies which document's POOM to resolve against."


## The containment record

ASN-0047 defines the provenance record R ⊆ T_elem × E_doc and the coupling constraint J1: when COPY extends d_t's arrangement with I-addresses not previously in ran(M(d_t)), provenance is recorded. P2 guarantees provenance is permanent — once (a, d) ∈ R, the entry persists through all subsequent transitions.

The containment query — "which documents contain content at I-address a?" — is answered by the provenance record:

`contains(a) = {d : (a, d) ∈ R}`

**C9** (*containment monotonicity*). COPY extends the containment record:

`(A a ∈ ran(M'(d_t)) \ ran(M(d_t)) :: (a, d_t) ∈ R')`

And no prior record is removed (P2): `R' ⊇ R`.

**C9a** (*containment superset*). For any I-address a and any reachable state:

`{d : a ∈ ran(M(d))} ⊆ {d : (a, d) ∈ R}`

The containment query may return false positives — documents that once contained but no longer contain the content — but never false negatives. This is P4 (ASN-0047) restated for a specific I-address.

The gap between the containment record and current reality is permanent. After COPY(d_s, p_s, n, d_t, p_t) followed by DELETE of the transcluded content from d_t, R records (a, d_t) but a ∉ ran(M(d_t)). The record is a historical journal, not a current-state index. Gregory confirms:

> "The spanfilade is structurally append-only — no deletion function exists. After DELETE, the POOM no longer contains the mapping, but the spanfilade still claims the document contains those I-addresses. This divergence is permanent."

A consumer of the containment query must post-filter through I-to-V resolution (checking whether the reported I-addresses actually appear in each document's current arrangement) to distinguish live containment from historical containment.

Nelson provides a dedicated operation for this query:

> "FINDDOCSCONTAINING: This returns a list of all documents containing any portion of the material included by <vspec set>." [LM 4/70]


## Self-transclusion

S5 (unrestricted sharing, ASN-0036) permits the same I-address to appear at multiple V-positions within a single arrangement. COPY with d_s = d_t exercises this permission.

**C10** (*self-transclusion*). COPY(d, p_s, n, d, p_t) with p_t ≠ p_s produces a state where:

`(A k : 0 ≤ k < n : M'(d)(p_t ⊕ [k]) = M(d)(p_s ⊕ [k]))`

and the original content is also present (at shifted positions if p_s ≥ p_t, at original positions if p_s < p_t). The arrangement M'(d) maps two distinct V-positions to the same I-address:

`(E v₁, v₂ : v₁ ≠ v₂ : M'(d)(v₁) = M'(d)(v₂))`

S2 (arrangement functional) is not violated: each V-position maps to exactly one I-address. The arrangement need not be injective — multiple V-positions may map to the same I-address — and S2 never required injectivity.

The consequence for link endset resolution: when a link's endset overlaps a shared I-address a, and a appears at V-positions v₁ and v₂ in d, resolution produces both:

`resolve(l, end, d) ⊇ {v₁, v₂}    when a ∈ endset(l, end)`

Gregory confirms:

> "incontextlistnd accumulates both V-positions. Both contexts appear in the returned list."


## Version creation and transclusion

Version creation (Fork, ASN-0047) produces a new document d_new with ran(M'(d_new)) ⊆ ran(M(d_src)). If d_src contains transcluded content — I-addresses originally allocated by some other document d_orig — those addresses flow into d_new unchanged.

**C11** (*version preserves transclusion identity*). If M(d_src)(v ⊕ [k]) = a_k for 0 ≤ k < n, and Fork(d_src, d_new) populates M'(d_new), then:

`(A k : 0 ≤ k < n : M'(d_new)(v' ⊕ [k]) = a_k)`

where v' is the corresponding V-position in d_new. The version holds the same I-addresses as d_src, which are the same I-addresses as d_orig. By C4, this makes the version discoverable through `discover` for any link created against any document in the transclusion chain.

*Derivation.* Fork is defined (ASN-0047) with ran(M'(d_new)) ⊆ ran(M(d_src)). The I-addresses a_k ∈ ran(M(d_src)) are therefore eligible for inclusion in M'(d_new). No K.α occurs in Fork. The I-addresses are unchanged. ∎

Gregory confirms:

> "CREATENEWVERSION copies the text subspace by calling docopyinternal → insertpm, which places existing I-addresses into the new POOM without allocating fresh ones."

Version creation is, at the arrangement level, a bulk COPY of the source document's text subspace. The identity-preserving mechanism is the same: K.μ⁺ without K.α.


## Worked example

We verify the postconditions against concrete values. Let document d_s have arrangement M(d_s) = {[1] ↦ [x], [2] ↦ [x+1], [3] ↦ [x+2], [4] ↦ [x+3], [5] ↦ [x+4]} — five characters forming a single correspondence run ([1], [x], 5). Let document d_t have M(d_t) = {[1] ↦ [y], [2] ↦ [y+1], [3] ↦ [y+2]} — three characters, run ([1], [y], 3), where [y] and [x] are in different ownership prefixes (different documents, different origin).

We COPY the middle three characters from d_s — V-positions [2] through [4] — into d_t at V-position [2].

**Source projection.** proj(d_s, [2], 3)(k) = M(d_s)([2+k]) for k = 0, 1, 2:

- k=0: M(d_s)([2]) = [x+1]
- k=1: M(d_s)([3]) = [x+2]
- k=2: M(d_s)([4]) = [x+3]

Projection decomposition: one I-span ([x+1], 3). m_s = 1.

**Phase 1** (shift). σ on d_t with p̂_t = 2, n = 3:

- σ([1]) = [1] — below insertion, unchanged
- σ([2]) = [2] ⊕ [3] = [5], σ([3]) = [3] ⊕ [3] = [6] — shifted by 3

After Phase 1: M₁(d_t) = {[1] ↦ [y], [5] ↦ [y+1], [6] ↦ [y+2]}. Gap at [2], [3], [4].

**Phase 2** (extension). Fill the gap:

- M'(d_t)([2]) = M(d_s)([2]) = [x+1]
- M'(d_t)([3]) = M(d_s)([3]) = [x+2]
- M'(d_t)([4]) = M(d_s)([4]) = [x+3]

Post-state: M'(d_t) = {[1] ↦ [y], [2] ↦ [x+1], [3] ↦ [x+2], [4] ↦ [x+3], [5] ↦ [y+1], [6] ↦ [y+2]}.

**Verification.** C1(f): M'(d_t)([2]) = [x+1] = M(d_s)([2]). ✓ C1(e): M'(d_t)(σ([1])) = M'(d_t)([1]) = [y] = M(d_t)([1]). ✓ C0: dom(C') = dom(C) — no new addresses. ✓ C-frame(c): M'(d_s) = M(d_s) — source untouched. ✓

**Run decomposition.** Pre-COPY: 1 run ([1], [y], 3). Post-COPY:

- ([1], [y], 1) — before-run (clipped: only position [1] is below p̂_t = 2)
- ([2], [x+1], 3) — new run from source projection
- ([5], [y+1], 2) — after-run, shifted

Three runs. Consistent with C7: m_t + m_s + 1 = 1 + 1 + 1 = 3 (split case with the original run split at the insertion point). ✓

**Origin check.** origin([x+1]) encodes d_s's document prefix (where the content was originally INSERTed). origin([y]) encodes d_t's prefix. After COPY, d_t's arrangement contains content with two distinct origins. The system can always tell which characters came from which original document — C5. ✓

**Phase 3** (provenance). Record ([x+1], d_t), ([x+2], d_t), ([x+3], d_t) in R'. These I-addresses were not previously in ran(M(d_t)), so fresh provenance entries are required.

**Transitivity test.** If document d_c now COPYs [2] through [4] from d_t:

proj(d_t, [2], 3)(k) = M'(d_t)([2+k]) = [x+1+k]. These are d_s's original I-addresses. By C4, d_c holds d_s's addresses directly — the intermediate d_t is transparent.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| CP0 | d_s ∈ E_doc ∧ d_t ∈ E_doc ∧ n ≥ 1 ∧ source span ⊆ dom(M(d_s)) ∧ S8a(p_t) | introduced |
| C0 | dom(C') = dom(C) — COPY allocates no new content identities | introduced |
| C0a | ran(M'(d_t)) \ ran(M(d_t)) ⊆ ran(M(d_s)) — new references come from source | introduced |
| C1 | COPY postcondition: content unchanged, entities unchanged, cross-doc frame, V-shift + new mappings, provenance extended | introduced |
| C-frame | C held in frame; E held in frame; M(d') for d' ≠ d_t held in frame; R extended | introduced |
| C2 | M'(d_s) = M(d_s) — source invariance | introduced |
| C3 | wp(op on d₁, M'(d₂) = M(d₂)) for d₁ ≠ d₂ — arrangement independence | introduced |
| C4 | (A k : 0 ≤ k < n : M₂(d_c)(v_c ⊕ [k]) = M₀(d_a)(v_a ⊕ [k])) — transitive identity, chains telescope | introduced |
| C4a | Direct COPY and multi-hop chain produce identical arrangements in the target | introduced |
| C5 | origin(M'(d_t)(q_k)) = origin(M(d_s)(p_s ⊕ [k])) — origin preservation | introduced |
| C6 | Post-COPY run decomposition: before/after/split/new runs | introduced |
| C7 | Post-COPY run count ≤ m_t + m_s + 1 | introduced |
| C8 | Shared I-addresses ⟹ identical discoverable link sets | introduced |
| C8a | Link discovery transitive across COPY chains | introduced |
| C9 | (A a ∈ ran(M'(d_t)) \ ran(M(d_t)) :: (a, d_t) ∈ R') — containment monotonicity | introduced |
| C9a | {d : a ∈ ran(M(d))} ⊆ {d : (a, d) ∈ R} — containment superset (= P4) | introduced |
| C10 | Self-transclusion: M'(d) may map distinct V-positions to the same I-address | introduced |
| C11 | Fork preserves transclusion I-addresses: version holds original chain's addresses | introduced |
| proj | proj(d, v, n)(k) = M(d)(v ⊕ [k]) — source projection | introduced |
| discover | discover(d, v, n) = links whose endsets overlap proj(d, v, n) | introduced |
| resolve | resolve(l, end, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ endset(l, end)} | introduced |


## Open Questions

What invariants must a containment query satisfy regarding the gap between historical provenance and current arrangement state — specifically, must a correct implementation provide an efficient path from the containment superset to current containment?

What constraints must COPY's source specification satisfy with respect to subspace boundaries — may the source span cross from the text subspace into the link subspace, or must it be confined to a single subspace?

Must COPY transitions be atomic with respect to arrangement queries from concurrent readers, or may a reader observe an intermediate state where some but not all of the new mappings are present?

What invariants distinguish a version-anchored transclusion (content frozen at a specific version) from a position-tracking transclusion (content that tracks the source's current arrangement)?

What ordering constraints must hold between the source span and the target position during self-transclusion to ensure well-definedness of the projection from the pre-state?

What must the system guarantee about endset resolution when the resolving document has deleted transcluded content — must resolution produce an empty result, or may it return stale positions from the historical containment record?

Under what conditions can COPY from two different source documents produce I-address contiguity in the target, and what implications does this have for run consolidation correctness?
