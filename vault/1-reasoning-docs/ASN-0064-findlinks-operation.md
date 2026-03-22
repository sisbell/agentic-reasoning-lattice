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

**F1 — ResolutionFragmentation (LEMMA).** For document d with canonical block decomposition B = {β₁, ..., βₘ} (ASN-0058, M11) and a V-span σ_V, the set resolve(d, {σ_V}) admits representation as a span-set of at most m spans.

*Proof.* Each block βⱼ = (vⱼ, aⱼ, nⱼ) contributes at most one I-span to the result. Within a single block, M(d)(vⱼ + k) = aⱼ + k (B3, Consistency), so a contiguous set of V-positions maps to a contiguous set of I-addresses. The intersection V(βⱼ) ∩ ⟦σ_V⟧ is contiguous by S0 (Convexity, ASN-0053). If this intersection contains positions vⱼ + c through vⱼ + c + w − 1 (for some c, w with 0 ≤ c and 1 ≤ w ≤ nⱼ − c), the corresponding I-addresses are aⱼ + c through aⱼ + c + w − 1: a single I-span. Blocks with empty intersection contribute nothing. ∎

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

When both the endset and the query are expressed as span-sets, the overlap test reduces to pairwise span intersection. Two spans σ₁ = (s₁, ℓ₁) and σ₂ = (s₂, ℓ₂) have non-empty intersection exactly when:

`⟦σ₁⟧ ∩ ⟦σ₂⟧ ≠ ∅ ⟺ s₁ < reach(σ₂) ∧ s₂ < reach(σ₁)`

where reach(σ) = start(σ) ⊕ width(σ) (ASN-0053, SpanReach). This follows from SpanClassification (SC, ASN-0053): the disjoint cases — separated (i) and adjacent (ii) — are exactly those where at least one inequality fails. The overlapping cases (iii)–(v) are those where both hold. We verify the boundary:

*Adjacent spans do not overlap.* If reach(σ₁) = start(σ₂), then s₂ < reach(σ₁) becomes s₂ < s₂, which is false. The half-open interval convention means the boundary point belongs to σ₂ but not σ₁; they share no element.

**F2 — OverlapSufficiency (INV).**

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
- F_Q ⊆ T is the *from-constraint*
- G_Q ⊆ T is the *to-constraint*
- Θ_Q ⊆ T is the *type-constraint*

A constraint is *unrestricted* when it equals T (the full tumbler space). An unrestricted constraint imposes no filtering on the corresponding endset. The home-set defaults to E_doc (all documents) when unrestricted.

At the user-facing level, constraints are specified as V-span-sets in specific documents. The front end resolves each constraint independently through its respective document's arrangement, producing I-address sets. A single constraint may reference content across multiple documents:

`resolve_spec({(d₁, Σ₁), ..., (dₖ, Σₖ)}) = ⋃_{i=1}^{k} resolve(dᵢ, Σᵢ)`

The from-constraint might say "content at V-positions 50–100 in document A and V-positions 200–250 in document B." After resolution, this becomes a single I-address set against which from-endsets are tested.

**Definition — Satisfaction.** A link at address ℓ ∈ dom(Σ.L), with Σ.L(ℓ) = (F, G, Θ), *satisfies* query Q = (H, F_Q, G_Q, Θ_Q) when:

```
satisfies(ℓ, Q)  ≡  home(ℓ) ∈ H
                   ∧ (F_Q = T  ∨  overlaps(F, F_Q))
                   ∧ (G_Q = T  ∨  overlaps(G, G_Q))
                   ∧ (Θ_Q = T  ∨  overlaps(Θ, Θ_Q))
```

where home(ℓ) = origin(ℓ) is the document-level prefix of the link's tumbler address (ASN-0043, LinkHome).

The predicate is deterministic: given a link ℓ and query Q, satisfaction is decidable from Σ.L(ℓ), the link's endsets, and Q alone (no external oracle or probabilistic test).

**F3 — SatisfactionDeterminism (LEMMA).**

`satisfies(ℓ, Q)` is decidable from `ℓ`, `Q`, and `Σ.L(ℓ)` alone.

*Proof.* home(ℓ) is computable from ℓ by T4 (HierarchicalParsing, ASN-0034). Membership in H is decidable. Each overlap test reduces to pairwise span intersection (the biconditional above), which is decidable by T2 (IntrinsicComparison) applied to the four endpoint tumblers. Since each endset is finite (ASN-0043, Endset), there are finitely many span pairs to test. ∎

**Definition — FINDLINKS Result.** The result of a discovery query Q is:

`findlinks(Q) = {ℓ ∈ dom(Σ.L) : satisfies(ℓ, Q)}`


## Completeness

Nelson is unambiguous: the system must return *all* matching links.

> "This returns a list of **all links** which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The word "all" is the guarantee. The operation does not return "some links," a sample, or a best-effort approximation.

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

**F4 — Completeness (INV).**

The FINDLINKS operation must return exactly findlinks(Q):

`result(Q) = findlinks(Q)`

This is both *complete* (no satisfying link omitted) and *sound* (no non-satisfying link included):

```
(A ℓ ∈ dom(Σ.L) : satisfies(ℓ, Q) : ℓ ∈ result(Q))       — completeness
(A ℓ ∈ result(Q) : satisfies(ℓ, Q))                        — soundness
```

The count operation (FINDNUMOFLINKSFROMTOTHREE) confirms complete knowledge — you cannot count what you have not found. The performance guarantee reinforces that completeness is practical at scale:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is a commitment about the indexing architecture: the system can find all matching links without scanning non-matching ones. The guarantee matters because the docuverse may contain arbitrarily many links, most of which will not match any given query. Completeness without this guarantee would be theoretically correct but practically unusable.


## Cross-Document Discovery

We now derive a consequence that Nelson considers fundamental. Because link discovery operates on I-addresses, and because transclusion shares I-addresses across documents, a link is discoverable from any document containing the referenced content.

**F5 — CrossDocumentIdentity (LEMMA).**

`(A d₁, d₂ ∈ E_doc, a ∈ T :`
`  a ∈ ran(M(d₁)) ∧ a ∈ ran(M(d₂))`
`  ⟹ (A ℓ : overlaps(Σ.L(ℓ).from, {a}) : ℓ ∈ findlinks((E_doc, {a}, T, T))))`

When the same I-address a appears in both documents (through transclusion), querying either document for that content discovers the same links.

*Derivation.* Let v₁ ∈ dom(M(d₁)) with M(d₁)(v₁) = a, and similarly v₂ ∈ dom(M(d₂)) with M(d₂)(v₂) = a. Then resolve(d₁, {v₁}) = {a} = resolve(d₂, {v₂}). The resolved I-address set is identical. Since satisfies(ℓ, Q) depends only on the I-address sets in Q and the link's endsets (F3), the same links satisfy both queries. By F4 (Completeness), both queries return the same result. ∎

This is not a feature to be designed in. It is a structural consequence of three properties: links reference I-addresses (L3, ASN-0043), transclusion preserves I-addresses (COPY creates no new content — ASN-0067, C0), and search matches on I-addresses (F2). Remove any one and the property vanishes.

The consequence extends to the full scope of the docuverse. Link discovery is not bounded to the document containing the queried content:

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

The home-set parameter allows narrowing the search (to links stored in specific documents), but the default is global. A link whose home document is on the far side of the network must still be found, provided it satisfies the query.

**One critical distinction.** The cross-document property depends on *identity-sharing*, not *value-coincidence*. Two users who independently type "to be or not to be" create content at different I-addresses — content identical in value but distinct in identity. Links to one do not appear when querying the other. Identity comes from origin, not from what the content happens to say.

`(A a₁, a₂ : origin(a₁) ≠ origin(a₂) ∨ a₁ ≠ a₂ :`
`  C(a₁) = C(a₂) does not imply that findlinks with query {a₁} = findlinks with query {a₂})`

This is the Xanadu distinction between structural sharing (transclusion, which preserves identity) and coincidental duplication (which does not).


## Endset Symmetry

The three endsets are structurally interchangeable in the search mechanism. Nelson treats them identically:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

**F6 — EndsetSymmetry (INV).**

All three endsets — from, to, type — are searchable with the same overlap predicate, the same performance guarantee, and the same completeness requirement.

```
(A e₁, e₂ ∈ {from, to, type}, Q ⊆ T :
  the mechanism for testing overlaps(Σ.L(ℓ).e₁, Q)
  is identical to that for overlaps(Σ.L(ℓ).e₂, Q))
```

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

where published(d) indicates the document is publicly available, and authorized(u, d) indicates the user has been granted access (as owner or designee).

**F7 — VisibilityFiltering (INV).**

The user-visible result is the intersection of the full result with the set of accessible links:

```
visible(Q, u) = {ℓ ∈ findlinks(Q) : accessible(home(ℓ), u)}
```

Two sub-properties hold:

(a) *No omission of accessible links.* Every link that satisfies Q and whose home document the user can access appears in the result:

`(A ℓ : satisfies(ℓ, Q) ∧ accessible(home(ℓ), u) : ℓ ∈ visible(Q, u))`

(b) *No leakage of inaccessible links.* No link whose home document is inaccessible appears in the result, nor is any information about such links revealed:

`(A ℓ : ¬accessible(home(ℓ), u) : ℓ ∉ visible(Q, u))`

Nelson reinforces the non-leakage requirement:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

Revealing the existence of a link in a private document would leak information about what the owner wrote. The system must not disclose the count, the content, or even the existence of private links to unauthorized users.

We note that this interacts with F4 (Completeness): the completeness guarantee applies to the visible result. The system returns all *accessible* matching links. Private links are not "missing" from the result — they are filtered by a separate, well-defined predicate.

Nelson acknowledged that the interaction between link search and document privacy was never fully resolved in the specification:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

The protocol description of FINDLINKSFROMTOTHREE assumes universal visibility. An implementation must add access-control filtering on top of the satisfaction predicate.


## Result Ordering and Pagination

The result set has a defined total order. Every link has a unique tumbler address (L11a, ASN-0043), and the tumbler order (T1, ASN-0034) provides a total ordering over all tumblers. Within a single document, links are ordered by creation:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

**F8 — ResultTotalOrder (INV).**

`findlinks(Q)` is totally ordered by the tumbler ordering (T1) on link addresses:

`(A ℓ₁, ℓ₂ ∈ findlinks(Q) : ℓ₁ ≠ ℓ₂ : ℓ₁ < ℓ₂ ∨ ℓ₂ < ℓ₁)`

The order is permanent — link addresses never change (T8, AllocationPermanence) — so the position of a link in any result set is fixed for all time.

This ordering supports pagination. The FINDNEXTNLINKSFROMTOTHREE operation returns:

> "no more than \<nlinks\> items past that link on that list." [LM 4/69]

The phrase "past that link on that list" requires a stable, deterministic ordering — otherwise resumption from a known position would be undefined. The tumbler order provides this. Pagination is a delivery mechanism over a complete result set, not a concession to incomplete search.

**Definition — Pagination.** For a result set R = findlinks(Q), a cursor c ∈ dom(Σ.L), and a count n ≥ 1:

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

`reverse(d, e) ⊆ {v : M(d)(v) ∈ coverage(e)}`

When coverage(e) contains I-addresses not in ran(M(d)) — because the referenced content is not (or is no longer) arranged in document d — those addresses contribute no V-positions to the result. The omission is not signaled. The caller cannot distinguish "this endset covers exactly what was returned" from "some endset content is not present in this document."

*Why this matters.* A link's endset is determined at creation time (L12, LinkImmutability, ASN-0043) and references specific I-addresses. But the document through which the user is viewing the content may not contain all of those I-addresses in its current arrangement. Content may have been partially deleted from the viewing document, or the endset may reference content that was never part of this document at all (the link could have been created in a different context). In all such cases, the reverse resolution silently returns a partial result.

This creates a fundamental asymmetry:

- *Discovery* is complete: all matching links are found (F4).
- *Display* may be partial: a discovered link's endsets may not fully resolve in the viewing document.

The asymmetry follows from the architecture. Discovery operates on I-addresses, which are permanent (S0, ContentImmutability). Display operates through arrangements, which are mutable and document-specific. The resolved I-address set used in discovery is a snapshot of what the querying document contained at query time. The link's endsets may reference a broader set of I-addresses than any single document currently arranges.


## Query Purity

Link discovery is a pure observation — it reads the current state but does not modify it.

**F11 — QueryPurity (INV).**

For every state Σ and every query Q, the FINDLINKS operation produces a result without altering any state component:

```
C' = C
L' = L
(A d :: M'(d) = M(d))
E' = E
R' = R
```

The system state before and after FINDLINKS is identical. This follows from the nature of the operation: it evaluates the satisfaction predicate over existing links and returns addresses. No content is allocated, no arrangement is modified, no link is created. The only effect is the communication of the result to the querier.


## Implementation Observations

Gregory's implementation grounds several abstract properties in concrete mechanisms. We record these observations without elevating them to abstract requirements.

*Dual indexing.* The implementation maintains two data structures: the granfilade stores each link's canonical endset data (the link's own POOM), while the spanfilade provides an inverted index from I-addresses to link addresses. Discovery uses the spanfilade; endset retrieval uses the granfilade. The two are written from the same data at link creation time but with no transactional guarantee binding them. A crash between writing the granfilade and the spanfilade can leave a link canonically present but undiscoverable — the link's orgl exists but no spanfilade entry indexes its endsets. This is a consistency gap in the implementation, not a property of the specification. The abstract requirement (F4) demands completeness; the implementation achieves it only under crash-free operation.

*Independent search and intersection.* The three-endset satisfaction predicate is evaluated by searching each endset type independently (using distinct spanfilade subspaces keyed by endset type), producing three candidate sets, and then intersecting them. This is algebraically equivalent to evaluating the conjunction directly, but the independent-search-then-intersect strategy enables per-endset indexing. The intersection is O(n·m·p) in the sizes of the three candidate sets. An alternative implementation using a different data structure (say, a multi-dimensional index) would satisfy the same abstract properties.

*Document-scoped mode.* The home-set parameter, which should restrict search to links owned by specific documents, was deliberately disabled in the implementation (`TRUE||!homeset` in the dispatch function). The disabling is related to versioning: when a document is versioned, its new version receives a new address, and links created against the old version would become invisible under document-scoped search. The workaround — making all search global — satisfies the abstract completeness requirement at the cost of the home-set filtering capability.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| F0 | resolve(d, Q_V) ⊆ dom(Σ.C) — resolved I-addresses are grounded in the content store | introduced |
| F1 | A single V-span resolves to at most m I-spans, where m is the block count | introduced |
| F2 | Partial overlap between endset coverage and query set suffices for matching | introduced |
| F3 | satisfies(ℓ, Q) is decidable from ℓ, Q, and Σ.L(ℓ) alone | introduced |
| F4 | findlinks(Q) returns exactly the set of satisfying links (complete and sound) | introduced |
| F5 | Shared I-addresses across documents yield shared link discovery | introduced |
| F6 | All three endsets (from, to, type) are searchable with identical mechanism | introduced |
| F7 | Result filtered by home document accessibility; no leakage of inaccessible links | introduced |
| F8 | findlinks(Q) is totally ordered by tumbler order on link addresses | introduced |
| F9 | Reverse resolution (I→V) may yield multiple V-positions per I-address | introduced |
| F10 | Reverse resolution silently omits I-addresses absent from the viewing document | introduced |
| F11 | FINDLINKS is a pure query; all state components are in the frame | introduced |
| Σ.resolve | resolve(d, Q_V) = {M(d)(v) : v ∈ Q_V ∩ dom(M(d))} | introduced |
| Σ.satisfies | AND-of-ORs: home-set ∧ (from-overlap) ∧ (to-overlap) ∧ (type-overlap) | introduced |
| Σ.findlinks | findlinks(Q) = {ℓ ∈ dom(Σ.L) : satisfies(ℓ, Q)} | introduced |
| Σ.reverse | reverse(d, a) = {v ∈ dom(M(d)) : M(d)(v) = a} | introduced |
| Σ.visible | visible(Q, u) = {ℓ ∈ findlinks(Q) : accessible(home(ℓ), u)} | introduced |


## Open Questions

What must the system guarantee about the interaction between link visibility and link counting — must FINDNUMOFLINKSFROMTOTHREE return a count consistent with the access-filtered result, or the unfiltered total?

When a link's endset contains spans in both the content subspace and the link subspace (L4(c)), must discovery treat both subspaces identically, or may the system restrict endset matching to content-subspace I-addresses?

What must the completeness guarantee become under network partition — must the system report that the result may be incomplete, or is silent partial return acceptable?

If a link has an empty from-endset and the query's from-constraint is unrestricted, does the link satisfy the from-condition — and if so, is this the intended behavior for links whose from-endset was empty at creation?

What invariants must pagination maintain when links are created concurrently with an ongoing paginated traversal — must new links appear in subsequent pages, or is the result frozen at query initiation?

What must the system guarantee about result stability across repeated queries against the same state — must identical queries against an unmodified state produce identical results in identical order?

Must reverse resolution signal partial coverage (some endset I-addresses could not be mapped to V-positions), or is the silent-omission behavior a specification-level design choice?

What is the relationship between the home-set filter and the access-control filter — are they independent predicates, or does accessibility subsume the home-set?
