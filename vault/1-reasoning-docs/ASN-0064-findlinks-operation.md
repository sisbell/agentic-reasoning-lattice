# ASN-0064: FINDLINKS Operation

*2026-03-21*

We are looking for a formal specification of link discovery: given a region of content visible in a document, which links reference that content, and what guarantees govern the result? The question has two parts — what determines membership in the result set, and whether the result is complete.

Two foundations are already in place. Links are triples of endsets, each endset a finite set of spans over Istream addresses (ASN-0043, L3). A document's arrangement M(d) maps Vstream positions to Istream addresses (ASN-0036, Σ.M(d)). The user sees positions; links reference addresses. Between these two spaces stands a resolution step that translates what the user points at into what the system searches against.

The central insight is Nelson's:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

Links attach to content identity — permanent I-addresses — not to position in any particular document's arrangement. This is not merely an implementation convenience; it is the architectural invariant that makes link survivability, cross-document discovery, and transclusion-aware search possible.


## From Positions to Identity

A user selects content by pointing at Vstream positions in a document. To search for links, the system must first translate these positions into the Istream addresses against which links are stored.

**Definition — Resolution.** For document d ∈ E_doc and a set of V-positions Q_V:

`resolve(d, Q_V) = {M(d)(v) : v ∈ Q_V ∩ dom(M(d))}`

When the selection is given as a V-span-set Σ_V (ASN-0053):

`resolve(d, Σ_V) = resolve(d, ⟦Σ_V⟧)`

The resolution function is the image of M(d) restricted to the selection. It is well-defined because M(d) is a function (S2, ArrangementFunctionality). The result sits inside the content store:

**F0 — ResolutionGrounding (LEMMA).**

`(A d ∈ E_doc, Q_V : resolve(d, Q_V) ⊆ dom(Σ.C))`

*Proof.* Every element of resolve(d, Q_V) is M(d)(v) for some v ∈ dom(M(d)). By S3 (ReferentialIntegrity), M(d)(v) ∈ dom(C). ∎

This grounding is what connects the user's view to the link store: the resolved set consists of permanent content addresses — the same kind of addresses that link endsets reference.

We observe that a single contiguous V-span may resolve to multiple disjoint I-address ranges. This happens whenever the V-span crosses a block boundary in the document's block decomposition (ASN-0058). Consider a document whose text-subspace arrangement contains two mapping blocks β₁ = (v₁, a₁, n₁) and β₂ = (v₂, a₂, n₂) with v₂ = v₁ + n₁ (V-adjacent) but a₂ ≠ a₁ + n₁ (not I-adjacent). A V-span covering both blocks resolves to two separate I-runs: one under a₁ and one under a₂. The content was originally created in — or transcluded from — different sources; the arrangement remembers.

**F1 — ResolutionFragmentation (LEMMA).** For document d with canonical block decomposition B = {β₁, ..., βₘ} (ASN-0058, M11) and a V-span σ_V, the set resolve(d, ⟦σ_V⟧) partitions into at most m contiguous I-address runs, one per block whose V-extent intersects ⟦σ_V⟧.

*Proof.* Each block βⱼ = (vⱼ, aⱼ, nⱼ) contributes at most one I-span to the result. Within a single block, M(d)(vⱼ + k) = aⱼ + k (B3, Consistency), so a contiguous set of V-positions maps to a contiguous set of I-addresses. We must show that V(βⱼ) ∩ ⟦σ_V⟧ is contiguous. Suppose vⱼ + c ∈ V(βⱼ) ∩ ⟦σ_V⟧ and vⱼ + c' ∈ V(βⱼ) ∩ ⟦σ_V⟧ with c < c'. For any integer k with c ≤ k ≤ c': first, vⱼ + k ∈ V(βⱼ) since 0 ≤ k < nⱼ; second, ordinal increments preserve order (TA-strict, ASN-0034), giving vⱼ + c ≤ vⱼ + k ≤ vⱼ + c' in T1, so vⱼ + k ∈ ⟦σ_V⟧ by S0 (Convexity, ASN-0053). Therefore vⱼ + k ∈ V(βⱼ) ∩ ⟦σ_V⟧. (Note: V(βⱼ) itself is not convex in unrestricted T1 — extension tumblers of depth greater than m lie between consecutive ordinal increments — but the argument requires only the T1-convexity of ⟦σ_V⟧, applied to the depth-m positions in V(βⱼ).) If this intersection contains positions vⱼ + c through vⱼ + c + w − 1 (for some c, w with 0 ≤ c and 1 ≤ w ≤ nⱼ − c), the corresponding I-addresses are aⱼ + c through aⱼ + c + w − 1. The I-addresses in this run — aⱼ + c through aⱼ + c + w − 1 — are all element-level (S7b, ASN-0036). When compact representation is needed, the run is described by the I-span (aⱼ + c, δ(w, d_I)) where d_I = #(aⱼ + c); note that the span denotation ⟦(aⱼ + c, δ(w, d_I))⟧ is a superset of the run (it includes extension tumblers of greater depth), but the element-level members are exactly the run's I-addresses. Blocks with empty intersection contribute nothing. ∎

Nelson acknowledges this multiplicity explicitly: the FEBE commands "have been generalized for the interconnection of broken lists of spans" (LM 4/61). A single user selection over a compound document — one built from transcluded fragments — may reference content scattered across the Istream. The search must handle this disjoint query set as a single operation.


## The Overlap Predicate

With resolution in place, we can ask: when does a link's endset "reference" the queried content? Nelson answers directly:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The phrase "any part of" is the key. A link need not cover the entire queried region to match. A single byte of overlap suffices.

**Definition — EndsetOverlap.** An endset e overlaps an I-address set Q when:

`overlaps(e, Q) ≡ coverage(e) ∩ Q ≠ ∅`

By the definition of coverage (ASN-0043):

`overlaps(e, Q) ≡ (E (s, ℓ) : (s, ℓ) ∈ e : ⟦(s, ℓ)⟧ ∩ Q ≠ ∅)`

A single span in the endset achieving non-empty intersection suffices. When e = ∅ (the empty endset), overlaps(e, Q) is false for all Q — there is no span to provide the intersection. This is the disjunctive half: OR across the spans within an endset.

Span-level overlap admits an efficient endpoint test. Two spans σ₁ = (s₁, ℓ₁) and σ₂ = (s₂, ℓ₂) have non-empty denotation intersection exactly when:

`⟦σ₁⟧ ∩ ⟦σ₂⟧ ≠ ∅ ⟺ s₁ < reach(σ₂) ∧ s₂ < reach(σ₁)`

where reach(σ) = start(σ) ⊕ width(σ) (ASN-0053, SpanReach). This follows from SpanClassification (SC, ASN-0053): the disjoint cases — separated (i) and adjacent (ii) — are exactly those where at least one inequality fails. The overlapping cases (iii)–(v) are those where both hold. We verify the boundary:

*Adjacent spans do not overlap.* If reach(σ₁) = start(σ₂), then s₂ < reach(σ₁) becomes s₂ < s₂, which is false. The half-open interval convention means the boundary point belongs to σ₂ but not σ₁; they share no element.

**F2 — OverlapSufficiency (LEMMA).**

`(A ℓ ∈ dom(Σ.L), e ∈ {from, to, type}, Q ⊆ T :`
`  coverage(Σ.L(ℓ).e) ∩ Q ≠ ∅ ⟹ ℓ satisfies the e-constraint of Q)`

Partial overlap is sufficient. A link whose from-endset spans I-addresses [a, a + 100) matches a query for I-addresses [a + 50, a + 200). The shared I-addresses [a + 50, a + 100) are enough. Full containment is not required in either direction.

This is the geometrically natural consequence of span-based linking. As Nelson puts it: "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes" (LM 4/42). The "strap" crosses into the queried region; we find the strap.

Gregory's implementation confirms the strict half-open interval test at every level of the search. The overlap predicate in the spanfilade traversal (`crumqualifies2d`) uses exactly the conditions `query_start < entry_end` and `query_end > entry_start`. Adjacent entries — where the query's end coincides with the entry's start — are excluded.


## The Satisfaction Predicate

A query constrains up to four dimensions. Nelson calls this "the AND of the ORs":

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

The outer level is conjunction: all specified constraints must be satisfied simultaneously. The inner level is disjunction: within each endset, any span achieving overlap is sufficient. We formalize each layer.

**Definition — DiscoveryQuery.** A discovery query is a tuple Q = (H, F_Q, G_Q, Θ_Q) where:

- H ⊆ E_doc is the *home-set*: the set of documents whose links to search
- F_Q is the *from-constraint*: either T (unrestricted) or a finite set of I-addresses F_Q ⊂ T
- G_Q is the *to-constraint*: either T (unrestricted) or a finite set of I-addresses G_Q ⊂ T
- Θ_Q is the *type-constraint*: either T (unrestricted) or a finite set of I-addresses Θ_Q ⊂ T

A constraint equal to T imposes no filtering on the corresponding endset. The home-set defaults to E_doc (all documents) when unrestricted. The from- and to-constraints are produced by resolution and are subsets of dom(Σ.C) (by F0); the type-constraint may reference addresses outside dom(Σ.C) (by L9, TypeGhostPermission, ASN-0043).

At the user-facing level, constraints are specified as V-span-sets in specific documents. The front end resolves each constraint independently through its respective document's arrangement, producing I-address sets. A single constraint may reference content across multiple documents:

`resolve_spec({(d₁, Σ₁), ..., (dₖ, Σₖ)}) = ⋃_{i=1}^{k} resolve(dᵢ, Σᵢ)`

The from-constraint might say "content at V-positions 50–100 in document A and V-positions 200–250 in document B." After resolution, this becomes a single finite I-address set against which from-endsets are tested. Each per-document resolution produces a finite set (subset of the finite dom(M(dᵢ)) by S8-fin, ASN-0036); by F1, each decomposes into at most m contiguous runs.

**Definition — Satisfaction.** A link at address ℓ ∈ dom(Σ.L), with Σ.L(ℓ) = (F, G, Θ), *satisfies* query Q = (H, F_Q, G_Q, Θ_Q) when:

```
satisfies(ℓ, Q)  ≡  home(ℓ) ∈ H
                   ∧ (F_Q = T  ∨  overlaps(F, F_Q))
                   ∧ (G_Q = T  ∨  overlaps(G, G_Q))
                   ∧ (Θ_Q = T  ∨  overlaps(Θ, Θ_Q))
```

where home(ℓ) = origin(ℓ) is the document-level prefix of the link's tumbler address (ASN-0043, LinkHome).

The predicate is deterministic: given a link ℓ and query Q, satisfaction is decidable from Σ.L(ℓ), the link's endsets, and Q alone (no external oracle or probabilistic test). Each overlap test evaluates `coverage(e) ∩ Q_e` for a finite I-address set Q_e — the intersection is well-defined and exact, without the ambiguity that would arise from testing against span denotations (which include non-element-level tumblers between element-level addresses).

**F3 — SatisfactionDeterminism (LEMMA).**

`satisfies(ℓ, Q)` is decidable from `ℓ`, `Q`, and `Σ.L(ℓ)` alone.

*Proof.* home(ℓ) is computable from ℓ by T4 (HierarchicalParsing, ASN-0034). Membership in H is decidable. Each overlap test `overlaps(e, Q_e)` checks whether `coverage(e) ∩ Q_e ≠ ∅` for a finite I-address set Q_e. Expanding: `(E (s, ℓ) ∈ e, a ∈ Q_e : s ≤ a < s ⊕ ℓ)`. Each comparison is decidable by T2 (IntrinsicComparison). The endset e is finite (ASN-0043, Endset) and Q_e is finite (by DiscoveryQuery), so finitely many tests are required. ∎

**Definition — FINDLINKS Result.** The result of a discovery query Q is:

`findlinks(Q) = {ℓ ∈ dom(Σ.L) : satisfies(ℓ, Q)}`

**Assumption — LinkEntityCoherence.** For every ℓ ∈ dom(Σ.L):

`origin(ℓ) ∈ E_doc`

This parallels P6 (ExistentialCoherence, ASN-0047), which establishes `origin(a) ∈ E_doc` for content addresses a ∈ dom(C). The analogous property for link addresses depends on a link-creation transition (analogous to K.α for content) whose postcondition must include this guarantee. No foundation currently defines this transition; we assume the property here.


## Completeness

Nelson is unambiguous: the system must return *all* matching links.

> "This returns a list of **all links** which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The word "all" is the guarantee. The operation does not return "some links," a sample, or a best-effort approximation.

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

**F4 — Completeness (INV).**

The FINDLINKS operation takes a query Q and returns findlinks(Q). It is both *complete* (no satisfying link omitted) and *sound* (no non-satisfying link included):

```
(A ℓ ∈ dom(Σ.L) : satisfies(ℓ, Q) : ℓ ∈ findlinks(Q))       — completeness
(A ℓ ∈ findlinks(Q) : satisfies(ℓ, Q))                        — soundness
```

Both follow directly from the definition of findlinks(Q) = {ℓ ∈ dom(Σ.L) : satisfies(ℓ, Q)}.

The count operation (FINDNUMOFLINKSFROMTOTHREE) confirms complete knowledge — you cannot count what you have not found. The performance guarantee reinforces that completeness is practical at scale:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is a commitment about the indexing architecture: the system can find all matching links without scanning non-matching ones. The guarantee matters because the docuverse may contain arbitrarily many links, most of which will not match any given query. Completeness without this guarantee would be theoretically correct but practically unusable.


## Worked Example

We verify the definitions against a concrete scenario. Let p = 1.0.1.0.1.0 and q = 1.0.1.0.2.0 be document-level prefixes extended through the third field separator, so that p.s.k and q.s.k denote element-level I-addresses (subspace s, ordinal k). All element-level addresses have depth 8.

Document d (at address 1.0.1.0.1) has V-position depth 2 and two mapping blocks (ASN-0058):

- β₁ = ([1,1], p.1.1, 3): V-positions [1,1] through [1,3] map to I-addresses p.1.1 through p.1.3
- β₂ = ([1,4], q.1.1, 2): V-positions [1,4] through [1,5] map to I-addresses q.1.1 through q.1.2

The blocks are V-adjacent ([1,4] = [1,1] + 3) but not I-adjacent — β₂'s content originates from document 1.0.1.0.2, transcluded into d.

**A link that matches.** Let ℓ reside at address p.2.1 (link subspace of document 1.0.1.0.1), with from-endset F = {(p.1.2, δ(2, 8))}. The reach is p.1.2 ⊕ δ(2, 8) = p.1.4 (TumblerAdd at action point 8 increments the last component: 2 + 2 = 4). So coverage(F) = {t : p.1.2 ≤ t < p.1.4}. The to- and type-endsets are irrelevant to this query.

The user selects V-positions [1,2] through [1,5], given as V-span σ_V = ([1,2], δ(4, 2)). Since reach(σ_V) = [1,2] ⊕ [0,4] = [1,6], the V-positions in dom(M(d)) ∩ ⟦σ_V⟧ are {[1,2], [1,3], [1,4], [1,5]} — by S8-depth, all V-positions have depth 2, so extension tumblers in ⟦σ_V⟧ (e.g. [1,2,1], [1,3,5]) do not intersect dom(M(d)). This selection crosses the block boundary between β₁ and β₂ — the F1 fragmentation scenario.

*Resolution.* resolve(d, ⟦σ_V⟧) produces two I-runs:

- From β₁: V [1,2], [1,3] → I p.1.2, p.1.3
- From β₂: V [1,4], [1,5] → I q.1.1, q.1.2

The from-constraint is the finite I-address set F_Q = {p.1.2, p.1.3, q.1.1, q.1.2}, compactly representable as the span-set {(p.1.2, δ(2, 8)), (q.1.1, δ(2, 8))}.

*Overlap test.* coverage(F) = {t : p.1.2 ≤ t < p.1.4}. The I-address p.1.2 is in both coverage(F) and F_Q, so coverage(F) ∩ F_Q ≠ ∅. overlaps(F, F_Q) = true.

*Satisfaction.* Query Q = (E_doc, F_Q, T, T):

- home(ℓ) = origin(p.2.1) = 1.0.1.0.1 ∈ E_doc ✓ (by LinkEntityCoherence)
- F_Q ≠ T and overlaps(F, F_Q) = true ✓
- G_Q = T ✓
- Θ_Q = T ✓

Therefore ℓ ∈ findlinks(Q).

**A link that does not match.** Let ℓ' reside at q.2.1 with from-endset F' = {(q.1.5, δ(1, 8))}. Its coverage: {t : q.1.5 ≤ t < q.1.6}. The I-addresses in F_Q under prefix q are q.1.1 and q.1.2; since q.1.5 > q.1.2, no element of F_Q falls in coverage(F'). The I-addresses under prefix p are below all q-prefixed addresses by T1, so they too lie outside coverage(F'). coverage(F') ∩ F_Q = ∅, so overlaps(F', F_Q) = false. Link ℓ' does not satisfy Q.


## Cross-Document Discovery

We now derive a consequence that Nelson considers fundamental. Because link discovery operates on I-addresses, and because transclusion shares I-addresses across documents, a link is discoverable from any document containing the referenced content.

**F5 — CrossDocumentIdentity (LEMMA).**

`(A d₁, d₂ ∈ E_doc, v₁, v₂ :`
`  v₁ ∈ dom(M(d₁)) ∧ v₂ ∈ dom(M(d₂)) ∧ M(d₁)(v₁) = M(d₂)(v₂)`
`  ⟹ resolve(d₁, {v₁}) = resolve(d₂, {v₂}))`

When the same I-address appears in two documents through transclusion, resolving through either document produces the same I-address set. Since satisfies(ℓ, Q) depends only on the I-address sets in Q and the link's endsets — not on which document or V-positions produced them — identical resolved sets yield identical findlinks results for any choice of H, G_Q, Θ_Q.

*Derivation.* Let a = M(d₁)(v₁) = M(d₂)(v₂). Then resolve(d₁, {v₁}) = {M(d₁)(v₁)} = {a} = {M(d₂)(v₂)} = resolve(d₂, {v₂}). ∎

This is not a feature to be designed in. It is a structural consequence of three properties: links reference I-addresses (L3, ASN-0043), transclusion preserves I-addresses, and search matches on I-addresses (F2). Remove any one and the property vanishes.

The second property — that transclusion preserves I-address identity — follows from the foundations alone. When content is transcluded into a document, the operation adds V→I mappings via K.μ⁺ (ArrangementExtension, ASN-0047). The frame of K.μ⁺ holds C' = C: no content is allocated, no I-addresses are created. The new V-positions map to I-addresses already in dom(C), as required by K.μ⁺'s precondition and S3 (ReferentialIntegrity, ASN-0036). The I-addresses in the target document are the *same* I-addresses as in the source — not copies, not new allocations.

The consequence extends to the full scope of the docuverse. Link discovery is not bounded to the document containing the queried content:

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

The home-set parameter allows narrowing the search (to links stored in specific documents), but the default is global. A link whose home document is on the far side of the network must still be found, provided it satisfies the query.

**One critical distinction.** The cross-document property depends on *identity-sharing*, not *value-coincidence*. Two users who independently type "to be or not to be" create content at different I-addresses — content identical in value but distinct in identity. Links to one do not appear when querying the other. Identity comes from origin, not from what the content happens to say.

Value coincidence does not entail identity: `a₁ ≠ a₂ ∧ C(a₁) = C(a₂)` does not imply that queries constrained by a₁ and by a₂ produce the same findlinks result.

This is the Xanadu distinction between structural sharing (transclusion, which preserves identity) and coincidental duplication (which does not).


## Endset Symmetry

The three endsets are structurally interchangeable in the search mechanism. Nelson treats them identically:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

**F6a — EndsetUniformity (LEMMA).**

The overlap predicate `overlaps(e, Q)` is defined uniformly on `(Endset, Set)` and applies identically regardless of which slot the endset occupies. This follows from the type signature alone: all three endsets have type Endset (L3, ASN-0043), and the overlap test makes no reference to slot identity. F4 (Completeness) applies independently to each endset constraint.

**F6b — DiscoveryIndependence (DESIGN).**

Nelson's performance guarantee — "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" (LM 4/60) — applies equally to from-constrained, to-constrained, and type-constrained queries. The cost of evaluating a query constrained on endset slot e must not grow with the number of links whose slot e does not satisfy the constraint. No endset slot is privileged or degraded in discovery.

This symmetry is what makes backlinks a first-class operation. Nelson distinguishes a document's *out-links* (links it owns) from its *in-links* (links elsewhere that point to it):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

But this is a distinction of *ownership*, not *discoverability*. Both directions are equally searchable. To find links FROM some content: constrain the from-set, leave the to-set unrestricted. To find links TO some content: constrain the to-set, leave the from-set unrestricted. The same operation, the same index, the same guarantee. Nelson makes the user-facing promise:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

In-links — the "harder" direction in most linking systems — are discoverable with the same efficiency as out-links.


## Visibility and Access Control

The link store may contain links that the querying user is not authorized to see. Nelson's document privacy model admits private documents:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

Links are contents of their home document (LM 2/31, 4/12). Private documents' contents are inaccessible to non-designees. Therefore links in private documents are invisible to unauthorized users — even when those users can see the content that the links reference.

**Definition — Accessible.** For a user u and document d:

`accessible(d, u) ≡ published(d) ∨ authorized(u, d)`

where published(d) indicates the document is publicly available, and authorized(u, d) indicates the user has been granted access (as owner or designee). The predicates `published` and `authorized` are not defined by any foundation ASN; we state the following as a design requirement rather than a derived invariant, recording the intended access-control semantics.

**F7 — VisibilityFiltering (DESIGN).**

Visibility filtering is a separate, explicitly defined post-processing step applied to the complete findlinks(Q) result. The user-visible result is:

```
visible(Q, u) = {ℓ ∈ findlinks(Q) : accessible(home(ℓ), u)}
```

Two sub-properties hold:

(a) *No omission of accessible links.* Every link that satisfies Q and whose home document the user can access appears in the visible result:

`(A ℓ : satisfies(ℓ, Q) ∧ accessible(home(ℓ), u) : ℓ ∈ visible(Q, u))`

*Derivation.* If satisfies(ℓ, Q) holds, then ℓ ∈ findlinks(Q) by F4 (completeness). If additionally accessible(home(ℓ), u) holds, then ℓ ∈ visible(Q, u) by the definition of visible. ∎

(b) *No inclusion of inaccessible links.* No link whose home document is inaccessible appears in the visible result:

`(A ℓ : ¬accessible(home(ℓ), u) : ℓ ∉ visible(Q, u))`

*Derivation.* By the definition of visible(Q, u), membership requires accessible(home(ℓ), u). When this predicate is false, ℓ is excluded. ∎

Nelson reinforces the non-leakage requirement:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

Revealing the existence of a link in a private document would leak information about what the owner wrote. The set-membership exclusion in F7(b) ensures that inaccessible links do not appear in the result set. The stronger property — that no *information* about inaccessible links is revealed (count, existence, timing) — is an information-flow guarantee that exceeds what the set-membership formalization captures. An implementation satisfying F7(b) must additionally ensure that inaccessible links are not observable through side channels (e.g., constant-time filtering, no count disclosure of the unfiltered set).

The FINDLINKS operation itself (F4) is defined at the system level over the full link store. Visibility filtering is applied after discovery: the system returns all *accessible* matching links. Private links are not "missing" from the findlinks(Q) result — they are removed by a separate, well-defined predicate before presentation to the user.

Nelson acknowledged that the interaction between link search and document privacy was never fully resolved in the specification:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

The protocol description of FINDLINKSFROMTOTHREE assumes universal visibility. An implementation must add access-control filtering on top of the satisfaction predicate.


## Result Ordering and Pagination

The result set has a defined total order. Every link has a unique tumbler address (L11a, ASN-0043), and the tumbler order (T1, ASN-0034) provides a total ordering over all tumblers. Within a single document, links are ordered by creation:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

**F8 — ResultTotalOrder (LEMMA).**

`findlinks(Q)` is totally ordered by the tumbler ordering (T1) on link addresses:

`(A ℓ₁, ℓ₂ ∈ findlinks(Q) : ℓ₁ ≠ ℓ₂ : ℓ₁ < ℓ₂ ∨ ℓ₂ < ℓ₁)`

The order is permanent — link addresses never change (T8, AllocationPermanence) — so the position of a link in any result set is fixed for all time.

This ordering supports pagination. The FINDNEXTNLINKSFROMTOTHREE operation returns:

> "no more than \<nlinks\> items past that link on that list." [LM 4/69]

The phrase "past that link on that list" requires a stable, deterministic ordering — otherwise resumption from a known position would be undefined. The tumbler order provides this. Pagination is a delivery mechanism over a complete result set, not a concession to incomplete search.

**Definition — Pagination.** For a result set R = findlinks(Q), a cursor c ∈ T, and a count n ≥ 1:

`page(R, c, n) = {ℓ ∈ R : ℓ > c, and ℓ is among the first n elements of R greater than c under T1}`

The cursor c is the address of the last link returned in the previous page. The first page uses a cursor below all possible link addresses (such as the zero tumbler). By F8, the ordering is total and stable, so consecutive pages partition R without gaps or repetition.


## Reverse Resolution: From Endsets to Positions

After discovering a link, the user may wish to see where the link's endsets point — to highlight the referenced content in a specific document. This requires the inverse of the resolution function: given an I-address from a link's endset, find all V-positions in a document that map to it.

**Definition — ReverseResolution.** For document d ∈ E_doc and I-address a ∈ dom(Σ.C):

`reverse(d, a) = {v ∈ dom(M(d)) : M(d)(v) = a}`

For an endset e:

`reverse(d, e) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`

The reverse resolution has properties that discovery does not share.

**F9 — ReverseMultiplicity (LEMMA).**

`(A d ∈ E_doc, a ∈ dom(Σ.C) : |reverse(d, a)| is not bounded by 1)`

By S5 (UnrestrictedSharing, ASN-0036), the same I-address may appear at arbitrarily many V-positions within a single document. After self-transclusion, a byte of content may appear at positions 10, 47, and 203. Reverse resolution returns all three. Gregory confirms: the POOM traversal iterates all qualifying crums and accumulates every match; there is no early-exit after the first.

**F10 — ReverseSilentOmission (LEMMA).**

`(A d ∈ E_doc, e₁, e₂ :`
`  coverage(e₁) ∩ ran(M(d)) = coverage(e₂) ∩ ran(M(d))`
`  ⟹ reverse(d, e₁) = reverse(d, e₂))`

Reverse resolution depends only on the intersection of endset coverage with the document's arranged I-addresses. Two endsets with different total coverage but the same intersection with ran(M(d)) produce identical results — the I-addresses outside the arrangement are invisible.

*Proof.* By definition, reverse(d, e) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}. For any v ∈ dom(M(d)), M(d)(v) ∈ ran(M(d)), so M(d)(v) ∈ coverage(e) iff M(d)(v) ∈ coverage(e) ∩ ran(M(d)). When two endsets agree on this intersection, the set comprehension produces the same result. ∎

*Why this matters.* A link's endset is determined at creation time (L12, LinkImmutability, ASN-0043) and references specific I-addresses. But the document through which the user is viewing the content may not contain all of those I-addresses in its current arrangement. Content may have been partially deleted from the viewing document, or the endset may reference content that was never part of this document at all (the link could have been created in a different context). In all such cases, the reverse resolution silently returns a partial result.

This creates a fundamental asymmetry:

- *Discovery* is complete: all matching links are found (F4).
- *Display* may be partial: a discovered link's endsets may not fully resolve in the viewing document.

The asymmetry follows from the architecture. Discovery operates on I-addresses, which are permanent (S0, ContentImmutability). Display operates through arrangements, which are mutable and document-specific. The resolved I-address set used in discovery is a snapshot of what the querying document contained at query time. The link's endsets may reference a broader set of I-addresses than any single document currently arranges.


## Query Purity

Link discovery is a pure observation — it reads the current state but does not modify it.

**F11 — QueryPurity (LEMMA).**

FINDLINKS is not a state transition — it is a pure function from (Σ, Q) to a set:

`findlinks : Σ × Query → 𝒫(T)`

No elementary transition (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ from ASN-0047) is invoked. The function evaluates the satisfaction predicate over existing links and returns addresses. No content is allocated, no arrangement is modified, no link is created. The only effect is the communication of the result to the querier. (Note: the link store Σ.L, defined in ASN-0043, is not yet integrated into the formal system state Σ = (C, E, M, R) of ASN-0047. The purity claim — that FINDLINKS invokes no transition — does not depend on this integration; it follows from the function's definition as a set comprehension over existing state.)


## Implementation Observations

Gregory's implementation grounds several abstract properties in concrete mechanisms. We record these observations without elevating them to abstract requirements.

*Dual indexing.* The implementation maintains two data structures: the granfilade stores each link's canonical endset data (the link's own POOM), while the spanfilade provides an inverted index from I-addresses to link addresses. Discovery uses the spanfilade; endset retrieval uses the granfilade. The two are written from the same data at link creation time but with no transactional guarantee binding them. A crash between writing the granfilade and the spanfilade can leave a link canonically present but undiscoverable — the link's orgl exists but no spanfilade entry indexes its endsets. This is a consistency gap in the implementation, not a property of the specification. The abstract requirement (F4) demands completeness; the implementation achieves it only under crash-free operation.

*Independent search and intersection.* The three-endset satisfaction predicate is evaluated by searching each endset type independently (using distinct spanfilade subspaces keyed by endset type), producing three candidate sets, and then intersecting them. This is algebraically equivalent to evaluating the conjunction directly, but the independent-search-then-intersect strategy enables per-endset indexing. The intersection is O(n·m·p) in the sizes of the three candidate sets. An alternative implementation using a different data structure (say, a multi-dimensional index) would satisfy the same abstract properties.

*Document-scoped mode.* The home-set parameter, which should restrict search to links owned by specific documents, was deliberately disabled in the implementation (`TRUE||!homeset` in the dispatch function). The disabling is related to versioning: when a document is versioned, its new version receives a new address, and links created against the old version would become invisible under document-scoped search. The workaround — making all search global — satisfies the abstract completeness requirement at the cost of the home-set filtering capability.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| F0 | resolve(d, Q_V) ⊆ dom(Σ.C) — resolved I-addresses are grounded in the content store | introduced |
| F1 | A single V-span resolves to at most m contiguous I-address runs, where m is the block count | introduced |
| F2 | Partial overlap between endset coverage and query set suffices for matching | introduced |
| F3 | satisfies(ℓ, Q) is decidable from ℓ, Q (with finite I-address set constraints), and Σ.L(ℓ) | introduced |
| F4 | findlinks(Q) returns exactly the set of satisfying links (complete and sound) | introduced |
| F5 | Transclusion identity: resolve(d₁, {v₁}) = resolve(d₂, {v₂}) when M(d₁)(v₁) = M(d₂)(v₂) | introduced |
| F6a | Overlap predicate is uniform across endset slots (from, to, type) — follows from type signature | introduced |
| F6b | Discovery cost for endset slot e is independent of non-matching links; no slot privileged or degraded | introduced (design) |
| F7 | visible(Q, u) filters findlinks(Q) by home document accessibility; inaccessible links excluded from result set | introduced (design) |
| F8 | findlinks(Q) is totally ordered by tumbler order on link addresses | introduced |
| F9 | Reverse resolution (I→V) may yield multiple V-positions per I-address | introduced |
| F10 | reverse(d, e) depends only on coverage(e) ∩ ran(M(d)); unarranged I-addresses invisible | introduced |
| F11 | FINDLINKS is a pure function from (Σ, Q) to a set; no transition invoked | introduced |
| LinkEntityCoherence | origin(ℓ) ∈ E_doc for all ℓ ∈ dom(Σ.L) — assumed pending link-creation ASN | assumed |
| Σ.resolve | resolve(d, Q_V) = {M(d)(v) : v ∈ Q_V ∩ dom(M(d))} | introduced |
| Σ.satisfies | AND-of-ORs: home-set ∧ (from-overlap) ∧ (to-overlap) ∧ (type-overlap) | introduced |
| Σ.findlinks | findlinks(Q) = {ℓ ∈ dom(Σ.L) : satisfies(ℓ, Q)} | introduced |
| Σ.reverse | reverse(d, a) = {v ∈ dom(M(d)) : M(d)(v) = a} | introduced |
| Σ.visible | visible(Q, u) = {ℓ ∈ findlinks(Q) : accessible(home(ℓ), u)} | introduced (design) |


## Open Questions

What must the system guarantee about the interaction between link visibility and link counting — must FINDNUMOFLINKSFROMTOTHREE return a count consistent with the access-filtered result, or the unfiltered total?

When a link's endset contains spans in both the content subspace and the link subspace (L4(c)), must discovery treat both subspaces identically, or may the system restrict endset matching to content-subspace I-addresses?

What must the completeness guarantee become under network partition — must the system report that the result may be incomplete, or is silent partial return acceptable?

If a link has an empty from-endset and the query's from-constraint is unrestricted, does the link satisfy the from-condition — and if so, is this the intended behavior for links whose from-endset was empty at creation?

What invariants must pagination maintain when links are created concurrently with an ongoing paginated traversal — must new links appear in subsequent pages, or is the result frozen at query initiation?

What must the system guarantee about result stability across repeated queries against the same state — must identical queries against an unmodified state produce identical results in identical order?

Must reverse resolution signal partial coverage (some endset I-addresses could not be mapped to V-positions), or is the silent-omission behavior a specification-level design choice?

What is the relationship between the home-set filter and the access-control filter — are they independent predicates, or does accessibility subsume the home-set?
