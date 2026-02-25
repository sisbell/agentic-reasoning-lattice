# ASN-0008: Link Discovery

*2026-02-23*

We wish to understand what link discovery must guarantee. The question is not how a particular index structure works, but what any correct implementation must promise: if content A links to content B, under what conditions can B discover that link? What about content transcluded across documents? Who has the right to discover, and when may discovery legitimately fail?

Xanadu's most radical claim is that every link is discoverable from *either end*. This is what separates it from the web, where links are one-directional and the "backlinks problem" remains unsolved. We seek the formal properties that constitute this guarantee. We discover that they flow from three sources: the addressing model (links reference I-space identity), the access model (publication determines visibility), and a completeness commitment (the system returns *all* matching links, not a sample).


## The state we need

We work with a minimal vocabulary. Let the system state Sigma contain:

- **ispace**: a partial function from addresses to content, `ispace : Addr -> Content`. Once allocated, addresses persist (permanence) and content never changes (immutability).
- **poom(d)**: for each document d, a mapping from virtual positions to addresses, `poom(d) : Pos -> Addr`. This is mutable — editing operations change it.
- **links**: the set of all fully-registered link objects in the system. A link L joins `links` when it has been assigned a permanent I-space address and all three of its endset entries (from, to, type) have been recorded in the span index. Prior to this point, L is not yet a member of `links` and no property in this ASN applies to it. This definition makes completeness (LD14) achievable — the system cannot be required to find a link whose index entries do not yet exist — and pushes atomicity concerns to the creation operation's postcondition.
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

1. **Satisfaction**: does Bob's content share I-addresses with L's endset? (The intersection question.)
2. **Access**: is the link's home document visible to Bob? (The publication question.)
3. **Completeness**: if the answer to (1) and (2) is yes, does the system guarantee L is returned? (The exhaustiveness question.)

We address each in turn.


## Discovery medium: I-address identity

The first and deepest guarantee is that link satisfaction is mediated *purely* through I-address identity — never through byte-value equality, never through V-space position, never through document membership.

**LD0 (I-address satisfaction).** A link L *satisfies* a constraint specifying I-address set Q on endset role e if and only if Q intersects the I-addresses of L.e:

  `satisfies(L, e=Q) <=> iaddrs(L.e) intersection Q != empty`

We separate satisfaction from discovery deliberately. Satisfaction is the pure I-address intersection test — it asks whether a link's endset overlaps a query region, without regard to who is asking. Discovery (LD5, below) composes satisfaction with visibility. This layering is essential: a link in a private document may satisfy a constraint without being discoverable by an unauthorized user. The biconditional holds for satisfaction, not for discovery.

The test is strict. Two documents containing the independently-typed string "Hello" share no I-addresses — each INSERT allocates fresh addresses from the monotonically advancing permascroll counter. A link to one document's "Hello" is completely invisible from the other. The system never compares byte content during satisfaction; it compares addresses. Gregory confirms this at every level: the span index is keyed on I-address ranges, the query converts V-spans to I-spans through the POOM, and the retrieval function (`crumqualifies2d`) performs an interval overlap test on those I-addresses, never consulting the bytes stored at those addresses.

Conversely, two documents that *share* I-addresses — through transclusion, through versioning, or through any mechanism that places the same I-address in multiple POOMs — automatically share link satisfaction. This is not a feature that must be implemented; it is a structural consequence of LD0.

We pause to appreciate what LD0 excludes. A content-addressable system (like a CAS hash table) would equate identical byte sequences. Xanadu does not. Identity is *provenance* — where and when content was created — not *value*. Two users typing the same words at different times produce different I-addresses and share nothing. This is deliberate: it is what makes transclusion meaningful. Transclusion is "I reference *your specific content*," not "I happen to contain the same bytes."

We note two boundary conditions. First, if Q = empty, then `iaddrs(L.e) intersection Q = empty` for all L, so no link satisfies the constraint; this is well-defined and sensible — a query for nothing finds nothing. Second, every link has three endsets, and each must be non-empty: `(A L : L in links : iaddrs(L.from) != empty /\ iaddrs(L.to) != empty /\ iaddrs(L.type) != empty)`. A link with an empty endset would be unreachable from that role — no query could ever discover it via the empty side. Since LD8 (below) guarantees symmetric discoverability from all three roles, empty endsets would violate this symmetry. We therefore require non-empty endsets as a precondition on link creation.


## Partial overlap suffices

LD0 says intersection must be non-empty. We must be precise about what "non-empty" means: a single shared I-address is enough.

**LD1 (Partial overlap sufficiency).** If a link's endset spans I-addresses `{a_1, ..., a_n}` and the query's I-addresses share even one address `a_k` with this set, the link satisfies the constraint:

  `{a_k} subset iaddrs(L.e) intersection Q => satisfies(L, e=Q)`

This matters because editing can fragment a link's V-space appearance. Suppose L.from spans I-addresses `[i_1, i_5]` as a contiguous V-region. After INSERT places new content in the middle, L.from's V-appearance splits into two fragments: one covering `[i_1, i_3]` and one covering `[i_4, i_5]`. A query covering only the first fragment — whose I-addresses are `{i_1, i_2, i_3}` — intersects `{i_1, ..., i_5}` non-emptily. The link satisfies the constraint.

After REARRANGE, the same I-addresses may scatter to arbitrary V-positions. After DELETE, some I-addresses may leave all POOMs entirely. In every case, a query on any surviving fragment satisfies the link, because the span index was written at link creation time using the full I-address range and is never modified by subsequent editing operations. Gregory confirms: the span index is write-only with respect to link entries. No DELETE, REARRANGE, or INSERT ever removes or modifies a span index entry. The index records the full original endset I-range permanently.

This permanence of the index combined with partial overlap means that link satisfaction is *maximally resilient* to editing: a link remains satisfiable as long as any portion of its endset content remains referenced by any POOM anywhere in the system.


## Conjunction semantics

When a query constrains multiple endset roles simultaneously, the constraints compose by conjunction:

**LD2 (Conjunction of constraints).** `satisfies(L, C) = (A e in constrained(C) : satisfies(L, e=C.e))` — a link satisfies a multi-role constraint if and only if it satisfies each constrained role independently.

For queries with multiple constrained roles, this yields the expected intersection: `findlinks(from=A, to=B, u) = findlinks(from=A, u) intersection findlinks(to=B, u)`. An unconstrained role imposes no restriction — passing "unconstrained" for the to-set means every link with a matching from-set qualifies, regardless of its to-set. The conjunction is strict: if the from-constraint matches but the to-constraint does not, the link does not satisfy.

Gregory confirms the mechanism: each non-empty constraint is searched independently against its dedicated sector of the span index (FROM, TO, and THREE endsets occupy distinct address prefixes). The per-constraint results are then intersected. If any single non-empty constraint produces zero results, the system short-circuits and returns an empty set without executing the remaining searches.

**LD2a (Non-vacuous query precondition).** A well-formed query must constrain at least one endset role:

  `|constrained(C)| >= 1`

This is a precondition on `findlinks`, not a consequence of conjunction semantics. The conjunction of zero predicates is vacuously true, which would classify every link as satisfying — clearly not the intended behavior. Rather than overriding standard logical semantics, we simply require that every query specifies at least one constraint. A query with no constraints is ill-formed and produces no result.


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

**LD5 (Discovery predicate).** For a query by user u with constraint C (where C satisfies LD2a):

  `findlinks(C, u) = {L in links : satisfies(L, C) /\ visible(L, u)}`

where `satisfies(L, C)` is the I-address intersection test of LD0 composed across constrained roles by LD2, and `visible(L, u)` is the access test of LD3. The system returns exactly those links that satisfy the query and are accessible to the querying user. No more, no less.


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

We now derive what is perhaps the most powerful consequence of I-address-mediated discovery: that link satisfaction is automatically transparent across transclusion boundaries.

**LD10 (I-address sharing implies shared satisfaction).** Any document whose POOM shares at least one I-address with a link's endset can discover that link:

  `iaddrs(L.e) intersection iaddrs(poom(d)) != empty => satisfies(L, e=iaddrs(poom(d)))`

This follows directly from LD0 — it is the definition of satisfaction applied to a document's I-address set. We state it separately because its consequences are profound. Transclusion is one mechanism by which I-address sharing arises: if document B transcludes content from document A, then B's POOM contains some of A's I-addresses, and any link whose endset touches those shared addresses is satisfiable from both A and B. But the property is more general than transclusion. Versioning, copying with shared identity, or any future mechanism that places the same I-address in multiple POOMs will inherit the same discovery transparency — without any modification to the discovery mechanism.

The system does not know or care whether the content is "original" or "transcluded." I-addresses are I-addresses. This is the operational content of Nelson's statement: "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26]. Versions share I-addresses the same way transclusions do; the satisfaction mechanism is the same.

Note that partial transclusion yields partial discovery. If document A's POOM maps to `{a_1, ..., a_5}` and document B transcludes only a subrange, say B's POOM contains `{a_3, a_4}`, then a link L with `L.to = {a_1, a_2}` is satisfiable from A but not from B — B's POOM shares no I-addresses with L.to. A link L' with `L'.to = {a_3, a_4, a_5}` is satisfiable from both A (full overlap) and B (partial overlap via `{a_3, a_4}`). Partial overlap suffices (LD1).

**LD11 (No transclusion depth limit).** If C transcludes from B which transcludes from A, C's POOM still maps to A's original I-addresses (transclusion preserves I-addresses at every step). A link to A's content is satisfiable from C by exactly the same mechanism:

  `(A d in documents : iaddrs(poom(d)) intersection iaddrs(L.e) != empty => satisfies(L, e=iaddrs(poom(d)))) (modulo access)`

The depth of the transclusion chain is irrelevant. What matters is whether the document's POOM contains the relevant I-addresses.

This property is what Nelson means by "socially self-constructing" literature. Every link made to any appearance of shared content automatically enriches *every other appearance* of that content. My commentary on your paragraph is discoverable by every reader of every document that transcludes your paragraph. The web of connections grows through the web of shared content without anyone maintaining it.


## Discovery permanence

Link discovery is not time-limited. The structural properties of the system ensure that satisfaction, once established, cannot be revoked.

**LD12a (Link permanence).** A link, once fully registered, cannot be removed from the system:

  `L in links at time t => (A t' : t' >= t : L in links at t')`

This follows from P0 applied to the link subspace. A link once created occupies a permanent I-space address. "New items may be continually inserted in tumbler-space while the other addresses remain valid" [LM 4/19]. Even owner-deleted links persist: "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]. If even explicitly deleted links await historical recovery rather than vanishing, non-deleted links certainly cannot be removed.

**LD12b (Span index permanence).** An entry, once recorded in the span index, cannot be removed:

  `entry in spanindex at time t => (A t' : t' >= t : entry in spanindex at t')`

Gregory confirms that no operation ever removes entries from the span index. DELETE removes V-space mappings from POOMs but does not touch span index entries. The span index is a permanent record of every endset I-address range that has ever been registered.

From LD12a and LD12b we derive the permanence of satisfaction:

**LD12 (Satisfaction permanence).** If a link satisfies a constraint at time t, it satisfies the same constraint at every later time:

  `satisfies(L, C) at time t => (A t' : t' >= t : satisfies(L, C) at t')`

*Proof.* Satisfaction (LD0) depends on `iaddrs(L.e) intersection Q != empty`. The set `iaddrs(L.e)` is determined by L's endset spans, which are recorded in I-space (immutable by P1) and indexed in the span index (permanent by LD12b). Neither the endset content nor its index entries can change or disappear. Therefore if the intersection is non-empty at t, it remains non-empty at every t' >= t.

The full discovery permanence follows: if `satisfies(L, C)` holds at t and `visible(L, u)` holds at t', then `L in findlinks(C, u)` at t' — by LD5. The satisfaction half cannot lapse (just shown). The visibility half depends on access state, which may change (publication, de-authorization); if visibility is maintained, discovery is maintained.

The FEBE protocol's link search operations take no expiration parameter. They search over specified regions of the address space with no temporal cutoff. Nelson's answer to the accumulation concern is not "old links expire" but "the search mechanism scales": "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" [LM 4/60].

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

This is the strongest possible guarantee. The result set is precisely the set of matching, visible links — no more, no less. We emphasize that `links` is the set of fully-registered links (as defined in "The state we need") — a link whose span index entries are not yet complete is not in `links` and is not subject to LD14.

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

We can now derive a key robustness property: V-space operations do not affect satisfaction.

**LD18 (Span index invariance under V-space operations).** For any V-space operation op in {INSERT, DELETE, REARRANGE, COPY} applied to document d:

  `spanindex' = spanindex`

No V-space operation modifies the span index. This is the structural foundation of V-space independence: the span index records endset I-address ranges at link creation time, and no subsequent editing operation alters those records.

The consequence for discovery depends on the relationship between the querier and the document being modified. We distinguish two cases.

**Case 1: Cross-document queries.** If the querier is reading a document d' != d, the operation on d does not modify d''s POOM. The querier's V-span maps to the same I-addresses before and after the operation. Therefore:

  `satisfies(L, e=Q) before op => satisfies(L, e=Q) after op`

where Q = iaddrs derived from the querier's V-span in d'. Discovery is entirely unaffected.

**Case 2: Same-document queries.** If the querier is reading document d — the document being modified — the querier's V-positions may shift, and the I-addresses at those positions may change. We write Q for the I-addresses at the querier's V-span before the operation, and Q' = iaddrs(poom'(d).v') for the I-addresses at the querier's (possibly shifted) V-span v' after the operation. The effect on discovery depends on the operation:

**INSERT.** INSERT adds fresh I-addresses at position p and shifts V-positions beyond p. The I-addresses that were in poom(d) before INSERT remain in poom(d) after INSERT — at shifted V-positions. If the querier's V-span was entirely before p, Q' = Q. If the querier's V-span was beyond p, the V-positions shift but map to the same I-addresses, so Q' = Q. If the querier's V-span straddled p, the new content is interleaved but the original I-addresses remain, so Q' supseteq Q. In all cases Q' supseteq Q, and satisfaction is preserved.

**DELETE.** DELETE removes V-space mappings from poom(d). If the deleted region overlaps the querier's V-span, some I-addresses in Q may not appear in Q'. Specifically, Q' = Q minus the I-addresses of the deleted region. If Q' intersection iaddrs(L.e) is non-empty, satisfaction is preserved. If Q' intersection iaddrs(L.e) is empty — because the deleted content was the sole overlap — satisfaction from this document is lost. But the link remains satisfiable from any other document whose POOM still contains those I-addresses, and the span index entry persists. System-wide discoverability is not reduced.

**REARRANGE.** REARRANGE permutes V-positions without removing any I-addresses from the POOM. The set `iaddrs(poom(d))` is unchanged (only V-positions change). If the querier's V-span is defined as a fixed V-range, different I-addresses may now occupy that range, and Q' may differ from Q. But the total set of I-addresses in the document is unchanged, so any link satisfiable from d's full content before REARRANGE remains satisfiable after.

**COPY.** COPY adds I-address mappings to a target document's POOM. It never removes mappings. Therefore Q' supseteq Q for any querier in the target document, and discoverability can only increase.

The asymmetry between DELETE and the other operations is notable. INSERT, REARRANGE, and COPY cannot reduce the I-address set in any document's POOM (INSERT and COPY add; REARRANGE permutes). DELETE can reduce the I-address set in a specific document, which may sever that document's discovery path to a link — but the span index entry persists, and any other document sharing those I-addresses still provides a discovery path.


## The reverse-orphan anomaly

Gregory reveals an instructive edge case. A link occupies V-position 2.x in its home document's POOM. If DELETEVSPAN is applied to this V-region, the link is removed from the document's current arrangement — but the span index entries created at link-creation time persist. The link becomes what we may call a *reverse orphan*: it has no V-space presence in its home document, but it remains fully discoverable through the span index and its I-space content is intact.

**LD19 (Link deletion is a V-space operation).** Removing a link from a document's V-space arrangement does not remove its entries from the span index. The span index is permanent. A deleted link remains discoverable:

  `deletevspan(d, 2.x) => spanindex' = spanindex`

Link deletion is a V-space operation, just as content deletion is a V-space operation. The link is removed from the current *view* but not from the permanent *store*. This is the specified behavior, not an anomaly.

The evidence is threefold. First, this parallels the treatment of content: DELETE removes content from a document's arrangement while the content persists in I-space. Links, being I-space objects, follow the same pattern. Second, Nelson explicitly states that "DELETED LINKS" are "not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9] — the language presumes persistence beyond deletion. Third, Gregory confirms that no code path in the implementation removes span index entries for any reason.

A "deleted" link is therefore still discoverable from any document whose POOM shares I-addresses with the link's endsets. The link can even be followed — its endsets resolve correctly because the link's I-space content (including the endset data) is permanent. The link's owner has removed it from their document's current arrangement; they have not removed it from the universe.


## A worked example

We trace a concrete scenario through the core properties to verify they compose correctly.

**Setup.** Document d has POOM `{v1 -> i3, v2 -> i4, v3 -> i5}`, so `iaddrs(poom(d)) = {i3, i4, i5}`. A link L has `L.to = span(i4, 2)`, covering I-addresses `{i4, i5}`. L is in a published document and all participants have access. The span index contains an entry mapping `[i4, i5]` to L for the to-role.

**Query from d.** A reader selects v2–v3 in document d. The system converts this V-span to I-addresses through d's POOM: Q = `{i4, i5}`. We check LD0: `iaddrs(L.to) intersection Q = {i4, i5} intersection {i4, i5} = {i4, i5} != empty`. So `satisfies(L, to=Q)` holds. Visibility holds (both documents published). By LD5, `L in findlinks(to=Q, user)`.

**DELETE v2 from d.** After deletion, d's POOM becomes `{v1 -> i3, v2 -> i5}` (v3 shifts to v2). Now `iaddrs(poom(d)) = {i3, i5}`. The span index is unchanged (LD18). A reader selects v2 in the modified document. Q' = `{i5}`. We check LD0: `iaddrs(L.to) intersection Q' = {i4, i5} intersection {i5} = {i5} != empty`. By LD1, partial overlap suffices. `satisfies(L, to=Q')` holds. L is still discovered from d, despite the deletion removing i4 from d's POOM.

**Transclusion to d2.** Document d2 transcludes from d's original content, with POOM `{v1 -> i4}`. So `iaddrs(poom(d2)) = {i4}`. A reader selects v1 in d2. Q'' = `{i4}`. We check LD0: `iaddrs(L.to) intersection Q'' = {i4, i5} intersection {i4} = {i4} != empty`. `satisfies(L, to=Q'')` holds. By LD10, d2's POOM shares I-address i4 with L.to, so the link is satisfiable from d2. L is discovered from d2 — a document that was not involved in the link's creation.

**Orphaned I-addresses.** Now suppose d also deletes v2 (the remaining reference to i5), yielding POOM `{v1 -> i3}`. And suppose d2's transclusion is the only surviving POOM reference to i4. If d2 is also edited to remove its reference to i4, then `iaddrs(L.to) = {i4, i5}` appears in no POOM anywhere. The span index still contains the entry `[i4, i5] -> L`. No document provides a V-space path to i4 or i5, so no user can construct Q such that Q intersects `{i4, i5}` through normal reading. L's satisfaction is formally intact — if anyone could present Q = `{i4}`, they would find L — but no V-space path reaches those addresses. L is *latently satisfiable* but *practically undiscoverable*: it persists in the span index, awaiting a future operation (transclusion, version retrieval, historical backtrack) that reintroduces its I-addresses into a POOM.


## The filtering right

Nelson anticipates that popular content will accumulate vast numbers of incoming links. He provides for filtering as a reader capability:

**LD20 (User-controlled sieving).** The system provides filtering mechanisms that narrow what the user *chooses to see*, not what the system *can return*:

  `sieve(findlinks(C, u), criteria) subset findlinks(C, u)`

Nelson: "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]. Sieving is the reader's prerogative. Remove all sieve criteria and the complete result set is returned.

This is a deliberate design choice against editorial filtering: "Some advocates of Artificial Intelligence would have computers decide what the reader shall see. As a filtering service this may be just what you want — but the danger is its evolving into a circumscription of your rights, where the choice is no longer yours" [LM 3/21]. The system provides completeness; the user controls relevance.


## Formal summary

We collect the architecture. The discovery predicate (LD5) is the conjunction of an I-address satisfaction test (LD0, LD1, LD2) and an access test (LD3, LD4). Satisfaction requires only partial overlap (LD1), operates by conjunction when multiple endsets are constrained (LD2), requires at least one constraint (LD2a), and treats all three endset roles symmetrically (LD8).

The access boundary is publication status of the link's home document (LD3). The right to discover belongs to anyone who can read the content (LD9). Published content's author cannot suppress incoming link visibility (LD7). Private links remain invisible to unauthorized users (LD4).

Discovery is exact: sound (LD13, unconditionally) and complete (LD14, within the access domain and subject to network availability LD15). It is global (LD16), scale-independent (LD17), permanent (LD12, via structural permanence of links LD12a and span index LD12b), and transparent across I-address sharing including transclusion (LD10, LD11).

V-space operations do not modify the span index (LD18). Cross-document queries are entirely unaffected; same-document queries may see shifted V-positions but satisfaction is preserved for INSERT, REARRANGE, and COPY, and reduced only by DELETE removing the sole overlapping I-addresses. Link deletion is a V-space operation — span index entries persist (LD19).

Links whose endset I-addresses appear in no POOM are latently satisfiable but practically undiscoverable — they persist in the span index awaiting reintroduction of their I-addresses into a POOM.

The power of the design is that transclusion transparency (LD10) is not a separate mechanism but a structural consequence of I-address satisfaction (LD0). The system does not need transclusion-aware link search. It needs I-address search. Transclusion, versioning, and any future mechanism that shares I-addresses across documents will automatically inherit link discovery — without a single line of discovery-specific logic being changed.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| LD0 | `satisfies(L, e=Q) <=> iaddrs(L.e) intersection Q != empty` — satisfaction is a pure I-address intersection test, independent of access | introduced |
| LD1 | Partial overlap of even a single I-address suffices for satisfaction | introduced |
| LD2 | Multiple endset constraints compose by conjunction across constrained roles | introduced |
| LD2a | A well-formed query must constrain at least one endset role (`\|constrained(C)\| >= 1`) | introduced |
| LD3 | Discoverability of a link is determined by the access status of its home document (published vs private) | introduced |
| LD4 | A link in a private document is invisible to unauthorized users, even if it points to published content | introduced |
| LD5 | `findlinks(C, u) = {L in links : satisfies(L, C) /\ visible(L, u)}` — discovery is satisfaction composed with visibility | introduced |
| LD6 | Any user may create a link whose endsets reference any published content | introduced |
| LD7 | The author of published content cannot suppress discoverability of published incoming links | introduced |
| LD8 | Discovery is symmetric across all three endset roles (from, to, type) — no role is privileged; all endsets must be non-empty | introduced |
| LD9 | The right to discover links belongs to anyone who can read the referenced content | introduced |
| LD10 | Any document whose POOM shares at least one I-address with L.e can satisfy a query for L (I-address sharing implies shared satisfaction) | introduced |
| LD11 | Transclusion depth is irrelevant to discovery; any document whose POOM contains the relevant I-addresses suffices | introduced |
| LD12a | `L in links at t => L in links at t'` for all t' >= t (link permanence) | introduced |
| LD12b | `entry in spanindex at t => entry in spanindex at t'` for all t' >= t (span index permanence) | introduced |
| LD12 | `satisfies(L, C) at t => satisfies(L, C) at t'` for all t' >= t (satisfaction permanence, derived from LD12a + LD12b + P1) | introduced |
| LD13 | Soundness: every returned link genuinely satisfies the query (unconditional) | introduced |
| LD14 | Completeness: every satisfying, visible link in `links` (fully-registered) is returned | introduced |
| LD15 | Distribution caveat: completeness may be approximated under network partition but must converge when restored | introduced |
| LD16 | Link search is global — it searches all link endsets in the system, not scoped to a home document | introduced |
| LD17 | Scale-independent discovery: non-matching links do not impede search for matching ones | introduced |
| LD18 | `spanindex' = spanindex` for all V-space operations; cross-document queries unaffected, same-document queries require V-span re-resolution | introduced |
| LD19 | Link deletion is a V-space operation; span index entries are permanent; a deleted link remains discoverable | introduced |
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
