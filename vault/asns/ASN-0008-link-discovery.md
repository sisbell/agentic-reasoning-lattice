# ASN-0008: Link Discovery

*2026-02-23*

We wish to understand what link discovery must guarantee. The question is not how a particular index structure works, but what any correct implementation must promise: if content A links to content B, under what conditions can B discover that link? What about content transcluded across documents? Who has the right to discover, and when may discovery legitimately fail?

Xanadu's most radical claim is that every link is discoverable from *either end*. This is what separates it from the web, where links are one-directional and the "backlinks problem" remains unsolved. We seek the formal properties that constitute this guarantee. We discover that they flow from three sources: the addressing model (links reference I-space identity), the access model (publication determines visibility), and a completeness commitment (the system returns *all* matching links, not a sample).


## The state we need

We work with a minimal vocabulary. Let the system state Sigma contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr -> Content`. Once allocated, addresses persist (permanence) and content never changes (immutability).
- **poom(d)**: for each document d, a mapping from virtual positions to addresses, `poom(d) : Pos -> Addr`. This is mutable — editing operations change it.
- **links**: the set of all link objects in the system. Each link has a home document, three endsets (from, to, type), and a permanent I-space address.
- **spanindex**: a persistent index mapping I-address ranges to link identifiers, tagged by endset role.
- **access(d)**: the access status of document d — either `published` or `private(S)` where S is the set of authorized users.

We assume the following properties (derived from first principles but stated here for self-containment):

**P0 (Address permanence).** `(A a : a in dom.ispace : a in dom.ispace')` — no operation removes an address.

**P1 (Content immutability).** `(A a : a in dom.ispace : ispace'.a = ispace.a)` — content at an address never changes.

**P2 (V-space mutability).** Editing operations modify `poom(d)` while leaving `ispace` unchanged.

We write `iaddrs(L.e)` for the set of all I-addresses covered by the spans in endset e of link L. We write `iaddrs(poom(d))` for the range of `poom(d)` — the set of all I-addresses that appear in document d's current arrangement.


## The discovery question

We are looking for the weakest precondition under which a reader can discover a link. Suppose Alice creates a link L with `L.to` referencing some content. Bob is reading a document that contains that content. Under what conditions does `findlinks(to=Bob's content)` return L?

The question factors into three independent concerns:

1. **Identity**: does Bob's content share I-addresses with L's endset? (The intersection question.)
2. **Access**: is the link's home document visible to Bob? (The publication question.)
3. **Completeness**: if the answer to (1) and (2) is yes, does the system guarantee L is returned? (The exhaustiveness question.)

We address each in turn.


## Discovery medium: I-address identity

The first and deepest guarantee is that link discovery is mediated *purely* through I-address identity — never through byte-value equality, never through V-space position, never through document membership.

**LD0 (I-address identity).** A link L is discoverable from a query specifying I-address set Q on endset role e if and only if Q intersects the I-addresses of L.e:

  `L in findlinks(e=Q) <=> iaddrs(L.e) intersection Q != empty`

This is strict. Two documents containing the independently-typed string "Hello" share no I-addresses — each INSERT allocates fresh addresses from the monotonically advancing permascroll counter. A link to one document's "Hello" is completely invisible from the other. The system never compares byte content during discovery; it compares addresses. Gregory confirms this at every level: the span index is keyed on I-address ranges, the query converts V-spans to I-spans through the POOM, and the retrieval function (`crumqualifies2d`) performs an interval overlap test on those I-addresses, never consulting the bytes stored at those addresses.

Conversely, two documents that *share* I-addresses — through transclusion, through versioning, or through any mechanism that places the same I-address in multiple POOMs — automatically share link discoverability. This is not a feature that must be implemented; it is a structural consequence of LD0.

We pause to appreciate what LD0 excludes. A content-addressable system (like a CAS hash table) would equate identical byte sequences. Xanadu does not. Identity is *provenance* — where and when content was created — not *value*. Two users typing the same words at different times produce different I-addresses and share nothing. This is deliberate: it is what makes transclusion meaningful. Transclusion is "I reference *your specific content*," not "I happen to contain the same bytes."


## Partial overlap suffices

LD0 says intersection must be non-empty. We must be precise about what "non-empty" means: a single shared I-address is enough.

**LD1 (Partial overlap sufficiency).** If a link's endset spans I-addresses `{a_1, ..., a_n}` and the query's I-addresses share even one address `a_k` with this set, the link is discovered:

  `{a_k} subset iaddrs(L.e) intersection Q => L in findlinks(e=Q)`

This matters because editing can fragment a link's V-space appearance. Suppose L.from spans I-addresses `[i_1, i_5]` as a contiguous V-region. After INSERT places new content in the middle, L.from's V-appearance splits into two fragments: one covering `[i_1, i_3]` and one covering `[i_4, i_5]`. A query covering only the first fragment — whose I-addresses are `{i_1, i_2, i_3}` — intersects `{i_1, ..., i_5}` non-emptily. The link is discovered.

After REARRANGE, the same I-addresses may scatter to arbitrary V-positions. After DELETE, some I-addresses may leave all POOMs entirely. In every case, a query on any surviving fragment discovers the link, because the span index was written at link creation time using the full I-address range and is never modified by subsequent editing operations. Gregory confirms: the span index is write-only with respect to link entries. No DELETE, REARRANGE, or INSERT ever removes or modifies a span index entry. The index records the full original endset I-range permanently.

This permanence of the index combined with partial overlap means that link discovery is *maximally resilient* to editing: a link remains discoverable as long as any portion of its endset content remains referenced by any POOM anywhere in the system.


## Conjunction semantics

When a query constrains multiple endset roles simultaneously, the constraints compose by conjunction:

**LD2 (Conjunction of constraints).** `findlinks(from=A, to=B) = findlinks(from=A) intersection findlinks(to=B)`.

A link must satisfy ALL specified constraints. An unconstrained role imposes no restriction — passing "unconstrained" for the to-set means every link with a matching from-set qualifies, regardless of its to-set. The conjunction is strict: if the from-constraint matches but the to-constraint does not, the link is not returned.

Gregory confirms the mechanism: each non-empty constraint is searched independently against its dedicated sector of the span index (FROM, TO, and THREE endsets occupy distinct address prefixes). The per-constraint results are then intersected. If any single non-empty constraint produces zero results, the system short-circuits and returns an empty set without executing the remaining searches.

There is an important edge case: specifying no constraints at all returns an empty result, not all links. The system requires at least one constraint to produce output. This is a design choice, not a logical necessity — but it prevents accidental retrieval of the entire link universe.


## The access boundary

We now turn to the second concern: who may discover a link? The answer involves the publication status of the link's *home document*, which determines the link's visibility.

**LD3 (Publication governs link visibility).** The discoverability of a link L is determined by the access status of L's home document:

  `visible(L, user) <=> access(L.home) = published \/ authorized(user, L.home)`

Nelson separates documents into exactly two states: private ("may be read and linked-to only by the owner and his or her associates" [LM 2/42]) and published ("available to anyone" [LM 2/42]). A link stored in a published document is visible to everyone. A link stored in a private document is visible only to the owner and designated associates.

This is a property of the *link's home document*, not of the *content it references*. Alice may create a published link pointing to Bob's published content, and the whole world can discover it. Alice may also create a private link pointing to the same content, and only Alice (and her associates) can see it. Both links exist simultaneously; their visibility differs because their home documents differ.

**LD4 (Privacy preserves asymmetry).** A link in a private document pointing to published content must remain invisible to unauthorized users:

  `access(L.home) = private(S) /\ user not-in S => L not-in findlinks(*, user)`

Nelson states the hard constraint: "The network will not, may not monitor what is read or what is written in private documents" [LM 2/59]. If Alice's private document contains a link to Bob's published work, revealing that link to Bob would disclose information about Alice's private document. The privacy guarantee takes precedence over the completeness guarantee.

This is the one place where two Xanadu principles collide. Nelson specifies that link discovery should return "all these outside connections without appreciable delay" [LM 2/46]. He also specifies that private documents are inviolable. The resolution is that "all" means "all *visible* connections" — completeness is defined relative to the user's access horizon.

We can now state the full discovery predicate:

**LD5 (Discovery predicate).** For a query by user u with constraint C:

  `findlinks(C, u) = {L in links : satisfies(L, C) /\ visible(L, u)}`

where `satisfies(L, C)` is the I-address intersection test of LD0 applied to each constrained endset role (LD2), and `visible(L, u)` is the access test of LD3. The system returns exactly those links that match the query and are accessible to the querying user. No more, no less.


## The publication contract

The interaction between links and publication deserves separate attention, because it establishes a social contract that is central to the system's design.

**LD6 (Link freedom).** Any user may create a link whose endsets reference any published content:

  `access(d) = published => (A user : may_create_link(user, endsets_touching(d)))`

Nelson: "each user is free to link to anything privately or publicly" [LM 2/43]. No permission is required.

**LD7 (Irrevocable in-link visibility).** The author of published content cannot suppress the discoverability of published links pointing to that content:

  `access(d) = published /\ access(L.home) = published /\ iaddrs(L.e) intersection iaddrs(poom(d)) != empty => L in findlinks(e=d's content, any user)`

Nelson frames this as a two-sided coin: "On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract" [LM 2/43].

The reasoning is tight. If you publish, others may link to you. If others link to you, readers of your work may discover those links. You cannot have one without the other. The publication act is a contractual acceptance of both.

Nelson distinguishes in-links from out-links: "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not" [LM 2/31]. You control what links you create (out-links). You do not control what links others create that point at you (in-links). And crucially, you cannot suppress the discoverability of those in-links.


## Bidirectional discovery

We now state the symmetry property that makes all of this cohere:

**LD8 (Bidirectional discovery).** The discovery mechanism treats all three endset roles identically. A link is discoverable from its from-side, its to-side, or its type-side with equal ease:

  `findlinks(from=A) discovers links whose from-set touches A`
  `findlinks(to=A) discovers links whose to-set touches A`
  `findlinks(type=A) discovers links whose type touches A`

No endset role is privileged. The system indexes all three roles symmetrically.

Nelson: "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay" [LM 2/46]. And symmetrically for transclusion: "it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time" [LM 2/37].

Gregory confirms the implementation is symmetric: the span index stores entries for all three endset roles in structurally identical sectors (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3). Each sector is searched identically. The only asymmetry Gregory documents is a bug: the type-endset filter is non-functional in the existing implementation, returning empty results when used as a constraint. But this is an implementation defect, not a design intent. The abstract guarantee is full three-way symmetry.

Bidirectional discovery is what solves the backlinks problem. If Alice links to Bob's published document, Bob's readers can discover Alice's link by querying with the to-set constraint matching Bob's content. They do not need to know Alice exists, or where Alice's document is, or even that the link was created. The system finds it.


## The discovery right

We are now ready to answer the question: who has the right to discover incoming links?

**LD9 (Reader discovery right).** The right to discover links pointing at content belongs to anyone who can read that content:

  `can_read(user, content_at(d, v)) => user may execute findlinks(to=iaddrs(poom(d).v))`

Nelson is consistent: the subject of the discovery guarantee is always "the reader," never "the owner." "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'" [LM 2/46]. The FEBE protocol's link search operations take no owner credential or access-control parameter — the search is constrained only by address ranges. Anyone who can issue a FEBE request can search for links into any content they can read.

For published content, the right is universal — every user can read it, so every user can discover links to it. For private content, the right is restricted to the owner and designated associates, but this is because reading itself is restricted, not because link discovery has its own access layer.

Together with LD3, this gives us the complete access picture:

| Content status | Link's home status | Who discovers? |
|---|---|---|
| Published | Published | Everyone |
| Published | Private (user's own) | User only |
| Published | Private (other, authorized) | User and associates |
| Published | Private (other, unauthorized) | Nobody outside that circle |
| Private | (any) | Only those who can read the content |


## Transclusion transparency

We now derive what is perhaps the most powerful consequence of I-address-mediated discovery: that link discovery is automatically transparent across transclusion boundaries.

Suppose document A contains content at I-addresses `{a_1, ..., a_n}`. Document B transcludes this content — B's POOM maps some V-positions to the same I-addresses `{a_1, ..., a_n}`. Now Carol creates a link L with `L.to` referencing these I-addresses (perhaps by clicking on the content while viewing it in document B).

**LD10 (Transclusion-spanning discovery).** A link discoverable from one document is discoverable from every document sharing the relevant I-addresses:

  `iaddrs(L.e) intersection iaddrs(poom(d_1)) != empty /\ iaddrs(poom(d_1)) intersection iaddrs(poom(d_2)) supseteq iaddrs(L.e) intersection iaddrs(poom(d_1)) => iaddrs(L.e) intersection iaddrs(poom(d_2)) != empty`

More concretely: if A's reader discovers L by querying for links to A's I-addresses, and B's POOM contains those same I-addresses, then B's reader discovers L too — by converting B's V-positions to I-addresses through B's POOM, which yields the same I-addresses, which intersect L's endset identically.

The mechanism is not magical. It is a syllogism:

1. Carol's link L has `L.to = {a_1, ..., a_n}` (endsets reference I-addresses, LD0).
2. A's POOM maps to `{a_1, ..., a_n}` (content is native to A).
3. B's POOM maps to `{a_1, ..., a_n}` (transclusion shares I-addresses, by definition).
4. A query from A converts V-positions to I-addresses through A's POOM, yielding `{a_1, ..., a_n}`, which intersects L.to. L is found.
5. A query from B converts V-positions to I-addresses through B's POOM, yielding `{a_1, ..., a_n}`, which intersects L.to. L is found.

Steps 4 and 5 are structurally identical. The system does not know or care whether the content is "original" or "transcluded." I-addresses are I-addresses. This is the operational content of Nelson's statement: "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26]. Versions share I-addresses the same way transclusions do; the discovery mechanism is the same.

**LD11 (No transclusion depth limit).** If C transcludes from B which transcludes from A, C's POOM still maps to A's original I-addresses (transclusion preserves I-addresses at every step). A link to A's content is discoverable from C by exactly the same mechanism:

  `(A d in documents : iaddrs(poom(d)) intersection iaddrs(L.e) != empty => L in findlinks(e=d's addresses, user)) (modulo access)`

The depth of the transclusion chain is irrelevant. What matters is whether the document's POOM contains the relevant I-addresses.

This property is what Nelson means by "socially self-constructing" literature. Every link made to any appearance of shared content automatically enriches *every other appearance* of that content. My commentary on your paragraph is discoverable by every reader of every document that transcludes your paragraph. The web of connections grows through the web of shared content without anyone maintaining it.


## Discovery permanence

Link discovery is not time-limited. It persists as long as the link exists and the query conditions are satisfiable.

**LD12 (Discovery permanence).** The discoverability of a link does not expire:

  `L in findlinks(C, u) at time t /\ satisfies(L, C) at time t' /\ visible(L, u) at time t' => L in findlinks(C, u) at time t'`

where `satisfies` is evaluated against the current state at time t'.

This follows from three facts working together:

First, links are permanent I-space objects (P0 applied to link subspace). A link once created cannot be removed from I-space. "New items may be continually inserted in tumbler-space while the other addresses remain valid" [LM 4/19].

Second, the span index is append-only. Gregory confirms that no operation ever removes entries from the span index. DELETE removes V-space mappings from POOMs but does not touch span index entries. The span index is a permanent record of every endset I-address range that has ever been registered.

Third, the FEBE protocol's link search operations take no expiration parameter. They search over specified regions of the address space with no temporal cutoff. Nelson's answer to the accumulation concern is not "old links expire" but "the search mechanism scales": "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60].

Even owner-deleted links persist: "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]. If even explicitly deleted links await historical recovery rather than vanishing, non-deleted links certainly cannot expire.

Nelson does acknowledge one mechanism by which discoverability could lapse: economic failure. Storage requires ongoing payment. If a link's home document's owner stops paying, the document (and its links) may become inaccessible. But this is a constraint on all content, not a designed feature of the link system. The system provides time-based *filtering* as a user convenience ("What links come in from last week?" [LM 2/47]) but never time-based *expiration* as a system behavior.


## Completeness and soundness

We now address the third concern: given that a link exists, is visible, and its endset intersects the query, does the system guarantee it is returned?

**LD13 (Soundness).** Every link returned by discovery genuinely satisfies the query:

  `L in findlinks(C, u) => satisfies(L, C) /\ visible(L, u)`

Soundness is structural and unconditional. Links are concrete objects at permanent addresses. The search is a range intersection test on those addresses. There is no mechanism by which the system could return a phantom link — one that does not exist at any address. False positives are impossible by construction: the span index maps I-address ranges to link identifiers, and the link at that identifier either exists or it does not.

**LD14 (Completeness).** Every link that satisfies the query and is visible to the user is returned:

  `satisfies(L, C) /\ visible(L, u) => L in findlinks(C, u)`

Nelson's language is unambiguous. FINDLINKSFROMTOTHREE returns "a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>" [LM 4/69]. The word "all" is a completeness claim. "If the home-set is the whole docuverse, all links between these two elements are returned" [LM 4/63]. The reader should see "all these outside connections without appreciable delay" [LM 2/46].

Together, LD13 and LD14 state that discovery is *exact*:

  `findlinks(C, u) = {L in links : satisfies(L, C) /\ visible(L, u)}`

This is the strongest possible guarantee. The result set is precisely the set of matching, visible links — no more, no less.

**LD15 (Distribution caveat).** Nelson simultaneously describes a distributed system where transient network failures may prevent completeness:

  `"It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]`

Each server holds only a subset of the docuverse: "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows" [LM 4/71]. Completeness (LD14) is the specified requirement and design target. Soundness (LD13) holds unconditionally. Completeness may be approximated under network partition, but the system must converge to full completeness when connectivity is restored. We note this as a boundary of the guarantee, not a weakening of it.


## The global search property

We observe that the discovery mechanism has a structural property that is worth stating explicitly: link search is *global* with respect to the span index's document dimension.

**LD16 (Global span search).** Link discovery searches all link endsets in the system, not only those belonging to a specific document:

  `findlinks(e=Q) = {L in links : (E s in L.e : iaddrs(s) intersection Q != empty) /\ visible(L, user)}`

The search is not scoped to a "home document" range in practice, despite the protocol accepting a home-set parameter. Gregory confirms that the implementation unconditionally overrides the home-set parameter with a range covering the entire address space. The specification should therefore not rely on document-scoped link search as a meaningful operation.

This globality is what makes bidirectional discovery work across the entire docuverse. When Bob asks "what links point at my content?", the answer comes from all published links everywhere, not from some subset. The system indexes all link endsets from all documents in a single searchable structure, and queries traverse this structure bounded only by I-address range, not by document of origin.


## Scale independence

The completeness guarantee must hold regardless of scale:

**LD17 (Scale-independent discovery).** The count of non-matching links in the system does not impede discovery of matching ones:

  `cost(findlinks(C, u)) is independent of |{L in links : not satisfies(L, C)}|`

Nelson states this as a first-class requirement: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60]. This is not a complexity class guarantee — it is a design constraint on the indexing mechanism. Irrelevant links must be eliminated without examination.

The requirement is achievable because the span index is organized by I-address range. A query for links to I-addresses `[a, b]` needs to examine only that region of the index, regardless of how many links exist outside that region. Nelson anticipated that popular content would accumulate vast numbers of in-links and provided for user-side filtering ("sieving") rather than system-side truncation.


## V-space independence

We can now derive a key robustness property: V-space operations do not affect discoverability.

**LD18 (V-space independence of discovery).** For any V-space operation op in {INSERT, DELETE, REARRANGE, COPY}:

  `L in findlinks(e=Q) before op /\ Q subset iaddrs(poom(d)) before op /\ Q intersection iaddrs(poom(d)) != empty after op => L in findlinks(e=Q') after op`

where Q' is the I-addresses derived from the querier's V-span after the operation.

*Argument.* We consider each operation:

**INSERT.** INSERT adds fresh I-addresses to poom(d) and shifts existing V-positions. It does not modify the span index, it does not modify any link's endsets. The I-addresses that were in poom(d) before INSERT remain in poom(d) after INSERT (at shifted V-positions). If those I-addresses intersected L.e before, they still intersect L.e after. The only new I-addresses are freshly allocated; they cannot appear in any pre-existing link's endset.

**DELETE.** DELETE removes V-space mappings from poom(d). The span index is untouched. If the deleted content includes I-addresses that were the *only* I-addresses connecting the query to L.e, then after deletion the query may no longer intersect L.e — but the link is still discoverable from any other document whose POOM still contains those I-addresses. Discovery from the specific document d may be lost; discovery from the system as a whole is not (as long as any POOM anywhere still references the relevant I-addresses).

**REARRANGE.** REARRANGE moves V-positions without removing any I-addresses from the POOM. The set `iaddrs(poom(d))` is unchanged (only V-positions change). Therefore the I-address intersection with L.e is unchanged. Discovery is fully preserved.

**COPY.** COPY adds I-address mappings to a target document's POOM. It never removes mappings. Therefore discoverability can only increase, never decrease: the target document gains the ability to discover links through the newly shared I-addresses.

The asymmetry between DELETE and the other operations is notable. INSERT, REARRANGE, and COPY cannot reduce discoverability from any document. DELETE can reduce discoverability from a specific document (by removing the V-space reference to the relevant I-addresses) but not from the system as a whole — the span index entry persists, and any other document sharing those I-addresses still provides a discovery path.


## The reverse-orphan anomaly

Gregory reveals an instructive edge case. A link occupies V-position 2.x in its home document's POOM. If DELETEVSPAN is applied to this V-region, the link is removed from the document's current arrangement — but the span index entries created at link-creation time persist. The link becomes what we may call a *reverse orphan*: it has no V-space presence in its home document, but it remains fully discoverable through the span index and its I-space content is intact.

**LD19 (Span index persistence through link deletion).** Removing a link from a document's V-space arrangement does not remove its entries from the span index:

  `deletevspan(d, 2.x) => spanindex' = spanindex`

This means a "deleted" link is still discoverable from any document whose POOM shares I-addresses with the link's endsets. The link can even be followed — its endsets resolve correctly because the link's I-space content (including the endset data) is permanent.

This property is consistent with the broader design. Nelson states that "DELETED LINKS" are "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. The link is removed from the current *view* but not from the permanent *store*. Discovery through the span index — which is a permanent structure — continues to find it.

Whether this is a desirable property or a consistency gap depends on what "deleted" means. If deletion is intended to remove a link from the discoverable universe, the span index should be updated. If deletion merely removes the link from one document's current arrangement (analogous to deleting content from V-space while it persists in I-space), the span index correctly reflects the permanent state. Nelson's language ("awaiting historical backtrack functions") suggests the latter interpretation — deletion is a V-space operation on links just as it is on content.


## The filtering right

Nelson anticipates that popular content will accumulate vast numbers of incoming links. He provides for filtering as a reader capability:

**LD20 (User-controlled sieving).** The system provides filtering mechanisms that narrow what the user *chooses to see*, not what the system *can return*:

  `sieve(findlinks(C, u), criteria) subset findlinks(C, u)`

Nelson: "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]. Sieving is the reader's prerogative. Remove all sieve criteria and the complete result set is returned.

This is a deliberate design choice against editorial filtering: "Some advocates of Artificial Intelligence would have computers decide what the reader shall see. As a filtering service this may be just what you want — but the danger is its evolving into a circumscription of your rights, where the choice is no longer yours" [LM 3/21]. The system provides completeness; the user controls relevance.


## Formal summary

We collect the architecture. The discovery predicate (LD5) is the conjunction of an I-address intersection test (LD0, LD1, LD2) and an access test (LD3, LD4). Satisfaction requires only partial overlap (LD1), operates by conjunction when multiple endsets are constrained (LD2), and treats all three endset roles symmetrically (LD8).

The access boundary is publication status of the link's home document (LD3). The right to discover belongs to anyone who can read the content (LD9). Published content's author cannot suppress incoming link visibility (LD7). Private links remain invisible to unauthorized users (LD4).

Discovery is exact: sound (LD13, unconditionally) and complete (LD14, within the access domain and subject to network availability LD15). It is global (LD16), scale-independent (LD17), permanent (LD12), and transparent across transclusion (LD10, LD11).

V-space operations cannot reduce system-wide discoverability (LD18), though DELETE on a specific document may remove that document's discovery path. The span index persists through all operations including link deletion from V-space (LD19).

The power of the design is that transclusion transparency (LD10) is not a separate mechanism but a structural consequence of I-address identity (LD0). The system does not need transclusion-aware link search. It needs I-address search. Transclusion, versioning, and any future mechanism that shares I-addresses across documents will automatically inherit link discovery — without a single line of discovery-specific logic being changed.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| LD0 | Link discovery is mediated purely through I-address intersection; byte-value equality and V-space position are never consulted | introduced |
| LD1 | Partial overlap of even a single I-address suffices for discovery | introduced |
| LD2 | Multiple endset constraints compose by conjunction; unconstrained roles impose no restriction; all-unconstrained yields empty | introduced |
| LD3 | Discoverability of a link is determined by the access status of its home document (published vs private) | introduced |
| LD4 | A link in a private document is invisible to unauthorized users, even if it points to published content | introduced |
| LD5 | Discovery predicate: findlinks returns exactly those links that satisfy the query AND are visible to the user | introduced |
| LD6 | Any user may create a link whose endsets reference any published content | introduced |
| LD7 | The author of published content cannot suppress discoverability of published incoming links | introduced |
| LD8 | Discovery is symmetric across all three endset roles (from, to, type) — no role is privileged | introduced |
| LD9 | The right to discover links belongs to anyone who can read the referenced content | introduced |
| LD10 | A link discoverable from one document is discoverable from every document sharing the relevant I-addresses (transclusion transparency) | introduced |
| LD11 | Transclusion depth is irrelevant to discovery; any document whose POOM contains the relevant I-addresses suffices | introduced |
| LD12 | Link discovery does not expire; it persists as long as the link exists and query conditions are satisfiable | introduced |
| LD13 | Soundness: every returned link genuinely satisfies the query (unconditional) | introduced |
| LD14 | Completeness: every matching, visible link is returned (specified requirement) | introduced |
| LD15 | Distribution caveat: completeness may be approximated under network partition but must converge when restored | introduced |
| LD16 | Link search is global — it searches all link endsets in the system, not scoped to a home document | introduced |
| LD17 | Scale-independent discovery: non-matching links do not impede search for matching ones | introduced |
| LD18 | V-space operations (INSERT, DELETE, REARRANGE, COPY) do not affect the span index; only the POOM query path changes | introduced |
| LD19 | Deleting a link from a document's V-space does not remove its span index entries; the link remains discoverable | introduced |
| LD20 | User-controlled sieving narrows display without reducing system capability; removing all filters yields the complete result | introduced |
| P0 | No operation removes an address from I-space (assumed) | introduced |
| P1 | Content at an I-space address never changes (assumed) | introduced |
| P2 | Editing operations modify V-space (poom) while leaving I-space unchanged (assumed) | introduced |


## Open Questions

What must the system guarantee about the atomicity of link creation with respect to the span index — must all three endset entries be indexed atomically, or may a partially-indexed link be observable during creation?

Must the system guarantee that discovery results for a given query are deterministic across invocations, or may the ordering of results vary?

When a link's home document transitions from private to published, must previously-invisible links become immediately discoverable, or may the system defer visibility updates?

What must the system guarantee about discovery performance when a single I-address range participates in thousands of link endsets — must response time be bounded, or is best-effort acceptable?

Under what conditions may the span index legitimately diverge from the set of existing links — and if divergence is permitted (e.g., entries for links whose home documents have been deleted), what consistency guarantees must the system provide?

Must the system guarantee that link discovery through FINDDOCSCONTAINING (finding all documents sharing given I-addresses) composes correctly with FINDLINKSFROMTOTHREE, or are these independent capabilities with potentially inconsistent views?

What must the system guarantee when a link's type endset is used as a query constraint — is type-based discovery a first-class guarantee on par with from-set and to-set discovery, or may it be degraded?

When the economic layer causes a link's home document to become inaccessible due to unpaid storage, must the system guarantee that the link becomes discoverable again if payment resumes, or may the span index entries be garbage-collected?
