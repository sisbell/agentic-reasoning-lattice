# Consultation Answers — FINDLINKS Operation

**Inquiry:** Given a region of Vstream content, how does the system discover all links whose endsets reference the same Istream addresses? What determines the result set and what guarantees govern completeness?
**Date:** 2026-03-21 16:53
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When content from the permanent storage layer appears in a document's arranged sequence, does link discovery match against the content's original permanent identity or its position in the current arrangement?

### Nelson's Answer

## Link discovery matches against permanent Istream identity, not Vstream position.

The evidence from Literary Machines is unambiguous on this point.

### Links attach to bytes, not positions

Nelson explicitly states that links are "to the bytes themselves":

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

And more precisely:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap between bytes" metaphor is critical. The strap attaches to the bytes' permanent identity (Istream address), not to where those bytes happen to sit in the current arrangement (Vstream position). That is the entire basis of link survivability:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

If links matched against Vstream position, they would break on every INSERT (which shifts all subsequent V-addresses). Survivability is only possible because matching occurs against Istream identity, which never changes.

### Endsets map to the permanent address space

Link endsets — the from-set, to-set, and type — map to positions on the universal tumbler line:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

These are permanent addresses. The endsets are stored as Istream spans, which is why they persist across edits to any document they reference.

### Transclusion makes this consequential

When content from document A appears in document B via transclusion (COPY), it shares the same Istream addresses:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The FINDDOCSCONTAINING operation exploits this directly — it finds all documents containing particular content by matching on shared Istream origin:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

So when you search for links FROM a paragraph that was transcluded into your document, the system resolves the V-positions to their underlying I-addresses and searches against those. A link originally made to that content in its home document will be discovered, because the I-addresses match.

### The architectural logic

The separation works like this:

1. **User selects content** — specified as a Vstream range (e.g., "bytes 50–100 in this document")
2. **System resolves to Istream** — the POOM (positional enfilade) maps V→I, yielding the permanent addresses of those bytes
3. **Link search matches on Istream** — FINDLINKSFROMTOTHREE compares the resolved I-addresses against stored link endsets
4. **Results returned** — links whose endsets overlap the queried I-addresses are found, regardless of which documents currently arrange that content or where it sits in their Vstreams

This is why Nelson can guarantee that "a link to one version of a Prismatic Document is a link to all versions" [LM 2/26] — because versions share Istream content, and link discovery matches on that shared identity.

### Summary

Vstream position is ephemeral and user-facing. Istream identity is permanent and system-facing. Links are stored against Istream. Discovery matches against Istream. The front end translates the user's Vstream selections into Istream addresses before searching. This is not an implementation choice — it is the architectural invariant that makes link survivability, version-spanning links, and transclusion-aware discovery possible.

---

## Question 2 [nelson]

> Must the system guarantee that every link whose endsets reference the queried content is returned, or may it return a partial result?

### Nelson's Answer

## The System Guarantees Completeness

Nelson specifies that link search must return **all** matching links, not partial results. The evidence is unambiguous across multiple layers of the specification.

### The Protocol Command Is Explicit

FINDLINKSFROMTOTHREE:

> "This returns a list of **all links** which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The word "all" is the guarantee. The operation does not say "some links," "a sample of links," or "links up to a limit." It returns all links satisfying the criteria.

### The Count Operation Confirms It

FINDNUMOFLINKSFROMTOTHREE exists specifically to count matching links before retrieval. This only makes sense if the system knows the complete set. You cannot count what you haven't found.

### Pagination Handles Volume, Not Incompleteness

FINDNEXTNLINKSFROMTOTHREE provides pagination — "no more than \<nlinks\> items past that link on that list" [LM 4/69]. This handles what Nelson calls "avalanches of material" from link searches. But pagination is a delivery mechanism over a complete result set, not an admission of partial results.

### The Performance Guarantee Reinforces Completeness

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This is a performance guarantee that makes completeness practical. Nelson is saying: the system can find all matching links efficiently even in a universe full of non-matching links. If partial results were acceptable, this guarantee would be unnecessary — you'd just stop early.

### The User-Facing Promise

From the user perspective, Nelson is equally explicit:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown **all** these outside connections without appreciable delay." [LM 2/46]

Again: "all these outside connections." Not "representative connections" or "nearby connections."

### The Satisfaction Model

The search semantics define precisely what "matching" means:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

This is a deterministic predicate. Every link in the docuverse either satisfies the request or it does not. The system returns all that satisfy.

### One Acknowledged Practical Limitation

Nelson does acknowledge resource constraints through the Resource Unit concept — when the system "can't fully satisfy a request," the RU works "on your behalf." And separately:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

These are acknowledged **practical realities** of a distributed system, not semantic relaxations. The architectural intent remains completeness. Network partitions may temporarily prevent access to some links, but the system's subrepresentation model (each server maintaining "a continuously valid model or subrepresentation of the entire docuverse" [LM 4/72]) is designed to minimize such gaps.

### Summary

The guarantee is completeness. Every link whose endsets match the query criteria must be returned. Pagination handles delivery of large result sets. The performance guarantee (4/60) ensures that non-matching links do not degrade search. Network partitions are a practical concern addressed by architectural redundancy, not by weakening the completeness guarantee.

NEED_RAW: [4/58-4/60] — The curated sources cover the key quotes from these pages, but the full discussion of the satisfaction model and the "junk-link problem" may contain additional nuance about edge cases in search completeness.

---

## Question 3 [nelson]

> Must link discovery span all documents in the system, or is it bounded to links defined within the same document as the queried content?

### Nelson's Answer

## Link discovery spans the entire docuverse

Nelson is unambiguous: link discovery is **not** bounded to the document containing the queried content. It must span all documents in the system. This is architecturally necessary and explicitly specified at multiple levels.

### The protocol proves it

The `FINDLINKSFROMTOTHREE` operation takes a **home-set** parameter that controls where to search for links. Nelson specifies:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

The home-set can be narrowed for efficiency, but the *default scope* is the entire docuverse.

### The user-facing guarantee demands it

Nelson states the reader's right explicitly:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'—and be shown all these outside connections without appreciable delay." [LM 2/46]

"From other documents" — not just within the current document.

### The link storage model requires it

Links live in their **home document**, which is determined by who created the link — not by what the link points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

If Alice creates a comment link pointing to Bob's text, that link lives in Alice's document. Bob can only discover it if the system searches *across* documents. A document-local search would miss every incoming link from every other user. This would defeat the entire purpose of the link mechanism.

### The system is designed for global link scale

Nelson addresses the performance concern directly:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This guarantee only matters if the search space includes links from across the docuverse. If search were document-local, the junk-link scaling problem wouldn't arise.

### The link mechanism's stated purpose is system-wide

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

"The whole corpus" — not individual documents.

### Filtering narrows scope; the default is global

Nelson provides filtering ("sieving") for managing the flood of cross-document links:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

Filtering presupposes a global search that returns too much. If search were document-local, filtering would rarely be needed.

---

**Summary:** Link discovery must span the entire docuverse. The home-set parameter on `FINDLINKSFROMTOTHREE` allows *narrowing* the scope, but the architecture indexes links globally by all three endsets, enabling bidirectional discovery across all documents. A system that only found links within the queried document would violate the backlink guarantee, the cross-document connection guarantee, and the fundamental purpose of the link mechanism.

---

## Question 4 [nelson]

> If the same content appears in multiple documents through sharing, must a query against one appearance discover links attached to every other appearance of that identical content?

### Nelson's Answer

# Yes — This Is a Structural Consequence, Not an Optional Feature

The answer is an unqualified **yes**. A query against any appearance of shared content must discover links attached to every other appearance. This falls directly out of three architectural properties that Nelson specifies:

## 1. Links Attach to I-Addresses, Not V-Positions

Links are "straps between bytes" — they bind to content identity (Istream addresses), not to positions in any particular document's arrangement (Vstream):

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

The endsets of a link map to the universal tumbler line — the Istream address space:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

## 2. Transclusion Shares I-Addresses

When content is transcluded (via the COPY operation), the new document's Vstream maps to the **same** Istream addresses as the original. No new bytes are created:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The included bytes have the same I-addresses in every document where they appear. Content identity is based on origin, not on which document currently displays it.

## 3. Link Search Operates on I-Address Ranges

FINDLINKSFROMTOTHREE searches by constraining endsets against span ranges on the tumbler line:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

These constraints are I-address ranges. A link satisfies the search if its endsets overlap the specified ranges:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

## The Consequence

If content at I-address range [X, X+100] appears in Document A (natively) and Document B (via transclusion), and a link's endset points to [X, X+50], then:

- Querying from Document A finds the link (the I-addresses match)
- Querying from Document B finds the **same** link (the I-addresses are **identical** — they are the same bytes)

The query doesn't ask "what links to this document?" It asks "what links to these bytes?" The bytes are the same bytes regardless of which document's arrangement you're viewing them through.

Nelson provides a dedicated operation that makes this explicit:

> "FINDDOCSCONTAINING: This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

The phrase "regardless of where the native copies are located" confirms that content identity transcends document boundaries.

## The Critical Distinction

This applies **only to structurally shared content** — content that shares I-addresses through transclusion. Two authors who independently type "to be or not to be" create content at **different** I-addresses. Their content is identical in value but distinct in identity. Links to one do not appear on the other.

This is by design. As Nelson's architecture dictates: identity comes from origin (which document created the bytes), not from value (what the bytes happen to say).

## Why This Matters

This property is what makes the "two-way reading" guarantee work:

> "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/40]

If links did not follow content across transclusions, a reader viewing a passage in a compound document would see a different set of connections than a reader viewing the same passage in its home document. The web of literature would fragment at every transclusion boundary. Nelson's entire vision of interconnected literature depends on links following content, not positions.

---

## Question 5 [nelson]

> When a link's endset partially overlaps the queried region — covering some but not all of the specified content — must that link appear in the discovery result?

### Nelson's Answer

## Yes — partial overlap is sufficient.

Nelson specifies this directly through the FINDLINKSFROMTOTHREE operation:

> "This returns a list of all links which are (1) in \<home set\>, (2) from **all or any part of** \<from set\>, and (3) to **all or any part of** \<to set\> and \<three set\>." [LM 4/69]

The phrase "any part of" is the key. A link whose from-set touches even a single byte within the queried region satisfies condition (2). The same applies to the to-set and three-set.

### The satisfaction model

The general rule from 4/58:

> "A link satisfies a search request if **one span of each endset** satisfies a corresponding part of the request." [LM 4/58]

This is what Nelson calls **the AND of the ORs**:

- **OR across spans within an endset**: A link's endset may be a discontiguous set of spans. At least *one* span must intersect the query region for that endset to be satisfied.
- **AND across endsets**: All three endsets (from, to, type) must independently be satisfied.

So a link with a from-set that partially overlaps the queried from-region, and a to-set that partially overlaps the queried to-region, and a type matching the queried type — that link appears in the result.

### Why this follows from the architecture

Links attach to spans of bytes, not points. A link whose endset covers bytes 50–200 and a query for bytes 100–300 share bytes 100–200. Nelson designed span-based linking precisely so these geometric relationships work naturally:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The "strap" metaphor reinforces this: if you query a region and a strap crosses into that region, you find the strap. You don't need the strap to be entirely within the region.

### Performance guarantee

Nelson also guarantees that non-matching links don't slow things down:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This means the system can efficiently find partially-overlapping links without scanning the universe of non-overlapping ones.

### Summary

A link appears in discovery results whenever its endset **intersects** the queried region — full containment is not required. This is explicitly stated by the "any part of" language in the FINDLINKSFROMTOTHREE specification [LM 4/69] and follows naturally from the span-based, geometrically-addressed link model.

---

## Question 6 [nelson]

> Can the existence of a link be concealed from a user who has permission to view the referenced content but not the document that defines the link?

### Nelson's Answer

## Yes — Link Concealment Follows from Document Privacy

The short answer: a link stored in a private document is invisible to users who lack access to that document, even if those users can see the content the link references. Nelson never states this as an explicit rule, but it follows necessarily from three principles he does state.

### The Logical Chain

**1. Links are contents of their home document.**

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents." [LM 2/31]

> "Its home document indicates who owns it, and not what it points to." [LM 4/12]

**2. Documents are either private or published, with binary access.**

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

**3. Users can link privately.**

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly." [LM 2/43]

If links are document contents, and private document contents are accessible only to the owner and designees, then links in private documents are accessible only to the owner and designees. A user reading published content that happens to be referenced by a link in someone else's private document would never discover that link.

### The Bidirectional Discovery Tension

This creates a tension with Nelson's promise of bidirectional link discovery:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

"All these outside connections" must be read as "all connections the user is authorized to see." The FINDLINKSFROMTOTHREE operation searches by home-set, from-set, to-set, and type — but the home-set implicitly constrains what's visible:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

If the home-set is "the whole docuverse," the protocol says "all links between these two elements are returned" [LM 4/63]. But this was written in a context where private documents were **not implemented**:

> "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]

So the protocol description assumes universal visibility. The interaction between link search and document privacy was never resolved in the specification.

### What This Means Concretely

Consider: Alice creates a private document containing a link from paragraph 3 of Bob's published essay to paragraph 7 of Carol's published essay. Dave reads both essays.

- **Dave cannot discover Alice's link.** It lives in Alice's private document, which Dave cannot access.
- **Alice sees the link** when querying connections on either essay.
- **Alice's designees** see it too.
- **The link still structurally exists** — it has an I-address, it occupies tumbler space — but it is invisible to unauthorized users.

This is consistent with how private documents work generally: private content exists but is accessible only to the owner and designees. Links are content. Private links are private content.

### The Privacy Constraint

Nelson's privacy principle reinforces this:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

If the system revealed the *existence* of links in private documents (even without revealing their content), it would leak information about what the owner wrote in private. The system would effectively be monitoring private writing activity.

### Summary

Link concealment is not an explicit Xanadu feature — it is an emergent property of document privacy applied to links-as-contents. Nelson designed a system where (a) links live in documents, (b) documents can be private, and (c) private means inaccessible to non-designees. The logical consequence is that a private link is invisible to anyone who cannot access its home document, regardless of their access to the referenced content.

The specification gap is that Nelson never worked out how FINDLINKSFROMTOTHREE should filter results by access control, because private documents were never implemented in XU.87.1. An implementation would need to add access-control filtering to link search — returning only links whose home documents the querying user is authorized to read.

---

## Question 7 [nelson]

> Does the design treat links originating from the content and links pointing to the content as equally discoverable, or does directionality affect what the query returns?

### Nelson's Answer

## Equal Discoverability: The Design Is Symmetric

The short answer: **both directions are equally discoverable.** Directionality is a semantic property of links (what "from" and "to" mean in context), not a constraint on what queries can find. The system indexes links by all three endsets and supports search from any direction.

---

### The Single Search Operation

There is one link search operation, and it handles all directions through a single mechanism:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." — 4/69

The operation takes four constraint parameters: home-set, from-set, to-set, and three-set (type). Any parameter can be set to the entire docuverse (unconstrained). This means:

- **Find what links FROM this content:** constrain the from-set, leave to-set as whole docuverse
- **Find what links TO this content:** constrain the to-set, leave from-set as whole docuverse
- **Find links OF a specific type:** constrain the three-set
- **Find links in a specific home document:** constrain the home-set

The same operation, the same indexing, the same performance guarantee. No asymmetry.

### The Satisfaction Model

Link search uses what Nelson calls "the AND of the ORs":

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." — 4/58

Each endset is checked independently against the corresponding constraint. The system does not privilege from-set over to-set or vice versa.

### The Performance Guarantee

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." — 4/60

This applies regardless of direction. Whether you're searching for outgoing or incoming links, the system scales the same way.

---

### Semantic Directionality vs. Structural Symmetry

Links are semantically directional — they have a from-set and a to-set with user-defined meaning:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" — 4/42

A citation link goes FROM the citing passage TO the source. A comment link goes FROM the commentary TO the subject. The direction carries meaning.

But structurally, the system treats both ends identically:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." — 4/43

All three endsets follow the same convention, use the same indexing, and support the same search operations.

---

### The In-Link / Out-Link Distinction

Nelson does distinguish between a document's **out-links** (links it contains) and **in-links** (links stored elsewhere pointing to it):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." — 2/31

But this distinction is about **ownership**, not **discoverability**. Out-links are owned by the document's owner. In-links are owned by whoever created them. Both are fully discoverable:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." — 2/46

Nelson explicitly requires that in-links (the "harder" direction in most systems) be shown "without appreciable delay." This is the backlinks problem, and the design solves it by indexing all endsets symmetrically.

---

### Summary

| Property | From-set | To-set | Type (3-set) |
|----------|----------|--------|--------------|
| Searchable? | Yes | Yes | Yes |
| Same operation? | Yes — FINDLINKSFROMTOTHREE | Same | Same |
| Same indexing? | Yes | Yes | Yes |
| Performance guarantee? | Same | Same | Same |
| Arbitrary span-set? | Yes | Yes | Yes |

Directionality tells you what a link **means**. It does not affect what a query **returns**. The design is structurally symmetric across all three endsets.

---

## Question 8 [nelson]

> Is the set of discovered links guaranteed to have a defined order, and if so, what property determines that order?

### Nelson's Answer

## Link Order in Search Results

**Yes, discovered links are guaranteed to have a defined order.** This is established by two properties: the permanent tumbler addresses of links, and the pagination mechanism that depends on stable ordering.

### Evidence for Defined Order

The `FINDNEXTNLINKSFROMTOTHREE` operation makes ordering mandatory. It returns:

> "no more than \<nlinks\> items past that link on that list." (4/69)

The phrase "past that link on that list" requires a stable, deterministic ordering — otherwise you could not resume pagination from a known position.

### What Determines the Order

**Within a single document**, the order is explicitly creation order (order of arrival), encoded permanently in the link's tumbler address:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Links are addressed sequentially — `...0.2.1` is the first link created, `...0.2.755` is the 755th — and unlike bytes, **links are not rearrangeable**:

> "Unlike bytes (which can be rearranged in Vstream), links keep their creation-order addresses permanently."

**Across documents**, the tumbler line provides a total ordering. All tumblers form a linear sequence through depth-first tree traversal. Since every link has a unique tumbler address, the tumbler line defines a total order over all links in the docuverse.

### The Search Constraint Model

The search itself uses a satisfaction model to determine *which* links are returned:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

The `home-set` parameter constrains *where* to look for links. If the home-set is the whole docuverse, all matching links are returned. If it's a single document, only that document's links are searched. The ordering of results follows the tumbler-line position of the links found.

### Implications

This design means:
- Pagination is deterministic — you can resume exactly where you left off
- The order is permanent — it never changes, since link addresses never change
- Within a document, order reflects chronological creation
- Across documents, order reflects the tumbler-line hierarchy (server → account → document → link instance)

NEED_RAW: [4/58-4/60, 4/69] — The curated sources establish that pagination requires stable ordering and that link addresses are permanent creation-order, but do not contain an explicit statement like "results are returned in tumbler order." The raw pages for the search model and `FINDNEXTNLINKSFROMTOTHREE` may contain a more explicit specification of result ordering.

---

## Question 9 [nelson]

> If a new link referencing the content is created after the content already exists, must the system make that link immediately discoverable or is eventual appearance acceptable?

### Nelson's Answer

## Link Discovery Timing: Immediate vs. Eventual

Nelson's design implies **immediate local discoverability** with **eventual cross-network propagation** — but he frames the user-facing guarantee in terms of responsiveness, not synchronization timing.

### Local Server: Immediate

MAKELINK is synchronous — it "creates a link in document \<doc id\>" and "returns the id of the link made" [4/68]. Once the back end returns the link ID, that link is indexed locally:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [4/41]

"Thereafter maintained" means: once created, the back end takes responsibility. There is no deferred-indexing concept. The link exists and is searchable on its home server from the moment MAKELINK returns.

### Cross-Network: Eventual, Not Instant

The BEBE protocol describes an explicitly eventual model for cross-server awareness:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [4/72]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [4/72]

The key phrase is **"continuously valid"** — not "continuously complete." Each server's model is always internally consistent but grows and shrinks with demand. Material migrates between servers for specific reasons:

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [4/71]

Point 2 explicitly mentions index material — link indexes propagate between servers, but driven by demand, not instant broadcast.

### The Forwarding Backstop

Even when a server's subrepresentation hasn't yet received a new link, BEBE provides a forwarding mechanism:

> "First, by the forwarding of requests as they fan out from users to servers able to supply" [4/70]

So a link search that can't be fully satisfied locally gets forwarded to servers that can supply the answer. This means a newly created link is **always discoverable** — either through the local subrepresentation (if propagated) or through forwarding to the home server (if not yet propagated). The question is latency, not availability.

### The User-Facing Guarantee

Nelson states the user expectation clearly:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [2/46]

**"Without appreciable delay"** is the guarantee — not "instantaneously" and not "within N milliseconds." This is a responsiveness standard, not a synchronization guarantee. It applies to showing connections that exist, mediated by the BEBE forwarding and subrepresentation system.

### The Search Efficiency Guarantee

Nelson also guarantees that scale doesn't degrade search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [4/60]

This is about filtering efficiency, not propagation timing — but it reinforces that link search should remain fast regardless of how many links exist in the system.

### Summary

| Scope | Timing | Mechanism |
|-------|--------|-----------|
| Home server | Immediate | MAKELINK is synchronous; back-end indexes on return |
| Remote server (cached) | Eventual | BEBE subrepresentation propagates with demand |
| Remote server (uncached) | On-demand | BEBE forwards request to home server |
| User experience | "Without appreciable delay" | Forwarding + subrepresentation together |

Nelson designed for a system where link creation is **locally atomic** and **network-eventually-discoverable**, with forwarding as the completeness backstop. He does not require instant global visibility, but he does require that the system never returns "link not found" when forwarding would find it — the system should do the work of finding it transparently.

The architecture is what we would now call **eventual consistency with read-forwarding** — each node is always valid, propagation happens continuously, and queries that can't be satisfied locally are forwarded to authoritative sources.

---

## Question 10 [nelson]

> When the queried region spans content drawn from multiple distinct original sources, must the system independently discover links to each source and merge the results into a single complete set?

### Nelson's Answer

## Yes — and the mechanism is the generalized span-set search

Nelson's architecture guarantees that querying a compound region returns links to **all** constituent content, regardless of how many original sources contributed. But the mechanism is not "independently discover and merge" as a multi-step pattern — it falls out naturally from the span-set generalization.

### Why the problem exists

A document's Vstream can include bytes from multiple Istream origins:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Links attach to **Istream addresses**, not Vstream positions. So a Vstream region spanning three sources maps to three disjoint I-address ranges. Links to each source live at different positions on the tumbler line.

### How the architecture handles it

The FEBE protocol is explicitly generalized for this case:

> "However, the commands for links and connectivity (material shared between documents and versions) are more esoteric, particularly since they have been generalized for the interconnection of broken lists of spans." [LM 4/61]

"Broken lists of spans" is precisely a disjoint span-set crossing multiple sources. The flow:

1. **V-to-I resolution** — The front-end (or middle-end) resolves the Vstream region into its constituent Istream spans. These may be disjoint and span multiple documents.

2. **Span-set construction** — The resulting I-spans form a request set:

   > "A request set is a set of spans, or spanset, presented to the back end in the FEBE protocol... The manipulation of request sets is an important aspect of what front-end functions do." [LM 4/37]

3. **Unified search** — FINDLINKSFROMTOTHREE accepts this span-set as a single argument and returns all matching links:

   > "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

4. **Satisfaction across the set** — A link matches if any of its endset spans intersects any span in the request:

   > "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

### The user-facing guarantee

Nelson states the guarantee in user terms:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

"A given place in the document" is a Vstream reference. The user points at content; the system finds **all** links, whether the bytes originated natively or were transcluded from one or many sources.

And the efficiency guarantee holds regardless of the span-set's complexity:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

### The endset generalization confirms this

Nelson designed endsets to be arbitrary span-sets across the entire docuverse:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

If endsets can be disjoint and cross-document, search arguments can be too. The machinery is symmetric.

### Summary

The semantic answer is **yes**: the system must find links to every original source and return a complete, unified result. But architecturally, this is not a "discover independently then merge" pattern — it is a single span-set search over a disjoint set of I-addresses. The V-to-I resolution (a front-end or middle-end responsibility) produces the disjoint span-set; FINDLINKSFROMTOTHREE searches it as one operation. The "broken lists of spans" generalization [LM 4/61] exists precisely to handle compound content whose identity is scattered across the Istream.

---

## Question 11 [gregory]

> When `vspanset2sporglset` walks the POOM to convert a V-span query into I-spans, how does it handle a single V-span that maps to multiple non-contiguous I-address ranges — does it emit one sporgl per contiguous I-run, and is the splitting purely driven by POOM crum boundaries?

### Gregory's Answer

## KB Synthesis

Yes, `vspanset2sporglset` emits one sporgl per contiguous I-run. The splitting is driven by POOM crum boundaries, with the important caveat that crum boundaries virtually always coincide with I-address discontinuities by construction.

## The Call Chain

The conversion path is [ST-LINK-CREATE] (Finding 0037):

```
V-span
  → vspanset2sporglset (sporgl.c:35-65)
    → vspanset2ispanset  (orgls.c:397-402)
      → permute           (orgls.c:404-422)
        → span2spanset    (orgls.c:425-454)
          → retrieverestricted  (retrie.c:56-85)
```

`retrieverestricted` discovers all POOM crums whose V-range overlaps the query span. Each qualifying crum produces one context entry in the returned list. Back up in `vspanset2sporglset`, the inner loop at `sporgl.c:49-58` iterates over every I-span in that list and emits one sporgl per entry — no consolidation step exists. So yes, one sporgl per contiguous I-run.

## Why Crum Boundaries = I-Address Discontinuities

The two are essentially the same thing, by [ST-VCOPY] (Finding 0046). During insertion, `isanextensionnd` merges a new POOM mapping into an existing crum **only when both** conditions hold: (1) same `homedoc` (I-address origin document), and (2) the new range starts exactly where the existing crum ends — contiguous in **both** V and I dimensions. Separate crums therefore always represent either different homedocs or non-contiguous I-addresses (or both). There is no steady-state where two adjacent crums have the same homedoc and contiguous I-addresses — the insertion path would have merged them.

The exception: REARRANGE can displace crums across the POOM without re-running `isanextensionnd` [ST-REARRANGE] (Finding 0056). After a pivot, you could theoretically have two adjacent crums that, after displacement, now abut in I-space even though they came from different sources. Those would still produce two separate sporgls.

## Concrete Confirmation

From [ST-LINK-CREATE] (Finding 0037), when document C contains "AABB" where "AA" was transcluded from A and "BB" from B:

```
Input: 1 V-span covering all of "AABB" (V 1.1 width 0.4)

POOM crums in C:
  crum₁: V[1.1..1.3) → I-addrs from A's permascroll  (homedoc = A)
  crum₂: V[1.3..1.5) → I-addrs from B's permascroll  (homedoc = B)

retrieverestricted returns: 2 context entries
inner loop emits:           2 sporgls
  sporgl₁: origin=I-addr(A,"AA"), width=0.2, doc=C
  sporgl₂: origin=I-addr(B,"BB"), width=0.2, doc=C
```

The front end sees one contiguous V-selection; the backend decomposes it into identity-preserving I-span segments via POOM crum structure. This same mechanism is why [EC-PIVOT-LINK-FRAGMENTATION] can produce multiple endset spans after a rearrange — pivot can create crum boundaries that weren't there before, multiplying the I-spans returned for any subsequent endset query on that region.

---

## Code Exploration

I now have everything needed to trace the full execution path. Here is the complete answer.

---

## How `vspanset2sporglset` splits one V-span into multiple I-address sporgls

### Entry point [`sporgl.c:35–65`]

```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    ispanset = NULL;
    if (!findorgl(taskptr, granf, docisa, &orgl, type))   // [44]
        return (NULL);
    for (; vspanset; vspanset = vspanset->next) {         // [47] one V-span at a time
        (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset); // [48]
        for (; ispanset; ispanset = ispanset->next) {     // [49] one sporgl per ispan
            sporglset = ...
            movetumbler(docisa,           &sporglset->sporgladdress);  // [53]
            movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // [54]
            movetumbler(&ispanset->width,  &sporglset->sporglwidth);   // [55]
        }
    }
}
```

The outer loop advances through the V-span set one span at a time. After the inner `for` loop exhausts `ispanset` to NULL, the next outer iteration starts with a fresh `ispanset = NULL`. **One sporgl is emitted unconditionally for each ispan returned from `vspanset2ispanset`.**

---

### V→I conversion chain

**`vspanset2ispanset`** [`orglinks.c:397–402`] just calls:
```c
return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);
```
`V=1`, `I=0` are defined in `wisp.h:19–20`.

**`permute`** [`orglinks.c:404–422`] iterates over the restriction span list (in this call, one V-span) and calls `span2spanset` for each:
```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next)
    targspansetptr = span2spanset(..., restrictionspanset, V, targspansetptr, I);
return (save);  // returns pointer to head of ispan list
```

**`span2spanset`** [`orglinks.c:425–454`] is where the actual POOM walk happens:
```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, V,
                              (typespan*)NULL, I, (typeisa*)NULL);  // [435]
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, V, &foundspan, I);          // [443]
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr);  // [444]
}
```

---

### The POOM tree walk: `findcbcinarea2d` [`retrie.c:229–268`]

`retrieverestricted` [`retrie.c:56–85`] is called with `span2ptr = NULL`, making `span2start = span2end = 0`. It calls `retrieveinarea` which dispatches to `findcbcinarea2d` since `cenftype == POOM`.

`findcbcinarea2d` walks all sibling crums recursively:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {          // [252]
    if (!crumqualifies2d(crumptr, offsetptr,
          span1start, span1end, V,                         // V-span restriction
          span2start(=0), span2end(=0), I, NULL))          // I: unconstrained
        continue;
    if (crumptr->height != 0) {
        dspadd(offsetptr, &crumptr->cdsp, &localoffset, POOM);
        findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...); // [259] recurse
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr); // [262]
        incontextlistnd(headptr, context, V);               // [263] sort by V
    }
}
```

**`crumqualifies2d`** [`retrie.c:270–305`] checks the V-span constraint strictly, and the I-span constraint leniently:

```c
endcmp = iszerotumbler(span2end) ? TOMYRIGHT : ...;  // [292] span2end==0 → TOMYRIGHT always
// → I-dimension filter always passes
startcmp = whereoncrum(crumptr, offset, span2start(0), I);
// span2start==0 → every crum qualifies (origin ≥ 0)
```

So **the I-dimension filter is a no-op** (zero spans are treated as "match everything"). The qualifying filter is entirely driven by the V-span bounds. Every leaf POOM crum whose V-extent overlaps the query V-span produces exactly one context. 

**`incontextlistnd`** [`context.c:75–111`] inserts contexts into a V-ordered list (by `grasp.dsas[V]`), so the returned list is in increasing V-address order.

---

### Per-crum context → I-span: `context2span` [`context.c:176–212`]

Each context captures the crum's 2D accumulated displacement. `makecontextfromcbc` [`context.c:151–174`] records:
- `context->totaloffset`: `typedsp` = `typewid` = struct with `tumbler dsas[MAXLOXIZE]`
  - `dsas[I=0]` = I-address of this crum's origin
  - `dsas[V=1]` = V-address of this crum's origin
- `context->contextwid`: the crum's 2D width in both I and V dimensions

`context2span` clips both ends proportionally:

```c
// [186] lowerbound = query V-start, upperbound = query V-end
prologuecontextnd(context, &grasp, &reach);  // [188] grasp/reach = abs 2D crum bounds

// Clip I-start if crum starts before query V-start
if (tumblercmp(&grasp.dsas[V], &lowerbound) == LESS) {      // [191]
    tumblerincrement(&grasp.dsas[I], 0,
        (INT)tumblerintdiff(&lowerbound, &grasp.dsas[V]),    // [194]
        &grasp.dsas[I]);
}
// Clip I-end if crum extends past query V-end
if (tumblercmp(&reach.dsas[V], &upperbound) == GREATER) {   // [197]
    tumblerincrement(&reach.dsas[I], 0,
        -tumblerintdiff(&reach.dsas[V], &upperbound),        // [200]
        &reach.dsas[I]);
}
movetumbler(&grasp.dsas[I], &foundspanptr->stream);          // [206]
tumblersub(&reach.dsas[I], &grasp.dsas[I], &foundspanptr->width); // [207]
```

The clipping is proportional integer arithmetic: the I-offset shift equals exactly the V-overflow (this works because the POOM stores content with V-width and I-width locked together by construction via `insertnd` at `orglinks.c:130`).

---

### No merging pass exists

Back in `span2spanset` [`orglinks.c:444`], the function `onitemlist` simply appends the new ispan to the end of the list — there is no adjacency check, no consolidation. A `cleanupvspanlist` / `consolidatespans` function is visible in `orglinks.c:297–312` and `orglinks.c:412–413`, but both are **dead code** — wrapped in `#ifdef UnDEFined` and commented out respectively:

```c
// orglinks.c:412–413 (commented out):
/*consolidatespans(restrictionspanset);
foospanset("restrictionset after consolidation is ",restrictionspanset); */

// orglinks.c:263–312 (inside #ifdef UnDEFined block):
int cleanupvspanlist(typetask *taskptr, typevspanset *vspansetptr)
{ ... adjacent-span merging ... }
```

---

### Summary

**Yes — one sporgl per contiguous I-run, and the splitting is purely driven by POOM crum boundaries.**

The mechanism in detail:

1. `findcbcinarea2d` traverses the POOM tree recursively, testing each crum against the query V-span via `crumqualifies2d`. Every leaf crum whose V-extent overlaps the query yields exactly one context [`retrie.c:262–263`].

2. If a single V-span's address range spans content from *N* distinct POOM leaf crums (because that content was originally inserted from *N* non-contiguous I-address ranges), `retrieverestricted` returns a context list of length *N*.

3. `context2span` converts each context to one I-span, applying proportional clipping at both ends where the crum overflows the query V-bounds [`context.c:191–207`].

4. `vspanset2sporglset` emits one `typesporgl` per I-span, with no merging [`sporgl.c:50–57`]. Adjacent I-runs that happen to be consecutive at the tumbler level are **not** coalesced — consolidation code exists but is disabled.

The grain of splitting is therefore the POOM bottom-crum boundary. Two positions that are adjacent in V-space but were inserted from non-contiguous I-addresses will always appear as separate sporgls, each carrying its own `sporglorigin`/`sporglwidth` pair.

---

## Question 12 [gregory]

> In `findlinksfromtothreesp`, what is the exact overlap predicate between the query I-spans and a link's endset I-spans — must there be any byte-level intersection, or does the spanfilade store coarser granularity entries that could miss partial-span overlaps?

### Gregory's Answer

## KB Synthesis

## Overlap Predicate in `findlinksfromtothreesp`

The predicate is **range intersection at I-address granularity** — any non-empty overlap between the query I-span and a stored link endset I-span is sufficient to return the link. There is no coarser-granularity approximation that would cause missed partial-span overlaps.

### What the spanfilade stores

[SS-DOCISPAN] (Finding 0047) establishes that `insertspanf` makes one `insertnd` call per `typeispan` struct, where each `typeispan` represents a contiguous range (start, width). So a link endpoint corresponding to k contiguous bytes is stored as one B-tree entry covering `[start, start+width)` — not k individual byte entries. When a V-span maps to non-contiguous I-addresses (e.g., content transcluded from multiple sources), [ST-LINK-CREATE] (Finding 0037) shows this produces multiple separate sporgls — one per contiguous I-address region — each independently indexed.

### How the search works

[INT-SPORGL-LINK-INDEX] (Finding 0035) describes the call chain: the query specset is converted to I-spans (V→I translation via sporgl conversion), then `retrievesporglsetinrange()` searches the 2D spanfilade using SPANRANGE and ORGLRANGE restrictions. The B-tree traversal (`findcbcinarea2d`) uses `whereoncrum` / `intervalcmp` [SS-INTERVAL-CMP] to classify each crum against the query range — a five-way predicate (`TOMYLEFT`, `ONMYLEFTBORDER`, `THRUME`, `ONMYRIGHTBORDER`, `TOMYRIGHT`). Any crum whose stored I-span interval has **any overlap** with the query interval is descended into and returned.

The overlap criterion is therefore: `stored_start < query_end AND query_start < stored_end` (standard half-open interval intersection). Even a single overlapping I-address triggers a match.

### Confirmed by partial-overlap examples

[SS-FIND-LINKS] (Finding 0028) provides the definitive empirical confirmation:

```
Link source: "DEF" stored as I-span [I.4, I.7)
Query (document transcluding "EF"): I-span [I.5, I.7)
Intersection: [I.5, I.7) ≠ ∅  → link returned
```

"Partial overlap suffices — a search specset that shares even one I-address with a link endpoint will discover that link."

### No coarser-granularity miss scenario

The per-contiguous-region storage granularity does **not** cause misses. If a link endpoint spans bytes 4–6 stored as a single range `[4, 7)`, a query for byte 5 only (`[5, 6)`) still intersects `[4, 7)` and returns the link. The only scenario where a partial query fails to find a link is if the query I-span genuinely does not overlap any stored endset I-span — which is semantically correct, not a granularity artifact.

The one caveat is [EC-FIND-LINKS-GLOBAL] (Finding 0069): the ORGLRANGE filter parameter is effectively ignored due to a `TRUE||` bug in `sporglset2linkset`, so the orgl-dimension restriction never narrows results. The span-dimension (I-address content) filter is the only operative predicate.

---

## Code Exploration

Now I have a complete, precise picture. Here is the full answer.

---

## `findlinksfromtothreesp`: Exact Overlap Predicate Analysis

### Call Chain

`findlinksfromtothreesp` (spanf1.c:56–103) converts up to three endpoint specsets to I-span–based sporglsets, calls `sporglset2linkset` for each, then intersects the three resulting linksets:

```c
// spanf1.c:71–99
specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
...
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`sporglset2linksetinrange` (sporgl.c:239–269) is where the actual spanfilade query fires:

```c
// sporgl.c:257–259
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width, 0, &range.width);
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, ...);
```

This calls `retrieverestricted` → `retrieveinarea` → `findcbcinarea2d` (retrie.c:229–268), which traverses the spanfilade tree and tests each subtree with `crumqualifies2d`.

---

### The Exact Overlap Predicate — `crumqualifies2d` (retrie.c:270–305)

The predicate runs in two passes, one per axis.

**SPANRANGE axis (index1) — query I-span vs. stored I-span:**

```c
// retrie.c:282–290
endcmp = iszerotumbler(span1end) ? TOMYRIGHT
                                  : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <=/*=*/ ONMYLEFTBORDER) return FALSE;    // line 283

startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return FALSE;                 // line 287
```

`whereoncrum` (retrie.c:345–398) computes where a tumbler address falls relative to a crum's half-open interval `[left, right)` where `left = offset[index] + crum.cdsp[index]` and `right = left + crum.cwid[index]`:

```
TOMYLEFT        (-2)  address < left
ONMYLEFTBORDER  (-1)  address == left
THRUME          ( 0)  left < address < right
ONMYRIGHTBORDER (+1)  address == right
TOMYRIGHT       (+2)  address > right
```

The two guards reduce to:
- `endcmp <= ONMYLEFTBORDER` disqualifies → i.e., `query_end ≤ crum_left` → return false
- `startcmp > THRUME` disqualifies → i.e., `query_start ≥ crum_right` → return false

**Surviving condition is therefore:**

```
query_start < crum_right   AND   query_end > crum_left
```

This is standard **strict half-open interval overlap**. Expressed in span terms, a query I-span `[Q, Q+Qw)` overlaps a stored entry `[E, E+Ew)` iff:

```
Q < E + Ew   AND   Q + Qw > E
```

Adjacency (where `Q + Qw == E`, i.e., spans touch but share no byte) is **excluded** — the `<=` at line 283 catches `endcmp == ONMYLEFTBORDER`, meaning "query ends exactly at the crum's left edge" → no match. There is no off-by-one that would accidentally include touching-but-not-overlapping spans.

**ORGLRANGE axis (index2) — link type + document ISA filter:**

```c
// retrie.c:292–300
endcmp = iszerotumbler(span2end) ? TOMYRIGHT
                                  : whereoncrum(crumptr, offset, span2end, index2);
if (endcmp < ONMYLEFTBORDER) return FALSE;   // note: < not <=

startcmp = whereoncrum(crumptr, offset, span2start, index2);
if (startcmp > THRUME) return FALSE;
```

This axis filters by link type (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) and document ISA range. Notably this uses `< ONMYLEFTBORDER` (strict, not `<=`), so ORGLRANGE is slightly more inclusive at the boundary — a stored link whose ISA exactly equals `span2end` is not excluded.

---

### Granularity: What Is Stored in the Spanfilade?

In `insertspanf` (spanf1.c:15–53), each sporgl (I-span of an endset) is inserted as **one crum**:

```c
// spanf1.c:27–51
movetumbler(&((typeispan*)sporglset)->stream, &lstream);    // exact stream origin
movetumbler(&((typeispan*)sporglset)->width, &lwidth);      // exact width
...
movetumbler(&lstream, &crumorigin.dsas[SPANRANGE]);
movetumbler(&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

There is **no coarsening, no aggregation**. The SPANRANGE coordinates of the stored crum are the exact tumbler stream and width of the link's endset I-span. One link endset I-span → one leaf crum in the spanfilade.

Interior nodes of the enfilade tree carry a `cwid` that is the **bounding box** of all descendants — used only to prune whole subtrees during `findcbcinarea2d`'s recursion (retrie.c:252–259). This pruning is strictly conservative: it can skip subtrees that definitely don't overlap, but cannot miss any crum that qualifies. No false negatives are possible.

---

### Tumbler Precision

A tumbler is a fixed-point number with 16 mantissa digits (`NPLACES = 16`, common.h:53). The smallest nonzero unit is tumbler `0.0...01` (one in the least-significant place). Text bytes in udanax-green are addressed as consecutive integer tumblers (each character increments by 1). Therefore the granularity of the overlap predicate is exactly **one character / one addressable byte**.

---

### Summary

| Question | Answer |
|---|---|
| Overlap predicate | `query_start < entry_end AND query_end > entry_start` — strict half-open interval intersection at tumbler precision |
| Adjacent (touching) spans | **Not considered overlapping** — `<=` at retrie.c:283 excludes `query_end == entry_start` |
| Stored granularity | One crum per link endset I-span; exact (stream, width) stored with no coarsening |
| Could coarser storage miss partial-span overlaps? | **No.** Leaf crums store I-spans exactly; interior bounding boxes only prune, never discard qualifying entries |
| Byte-level intersection required? | Yes — any two I-spans sharing at least one byte will match; sub-byte overlap is impossible since the addressable unit is one character |

---

## Question 13 [gregory]

> The `sporglset2linkset` function has `TRUE||!homeset` hardcoded, making link search always global — was there ever a working document-scoped mode, and is the hardcoded width of 100 in that path sufficient to cover all possible link I-address ranges, or can it silently truncate results?

### Gregory's Answer

## KB Synthesis

## `sporglset2linkset`: Document-Scoped Mode and Width-100 Sufficiency

### Was there ever a working document-scoped mode?

Almost certainly not in the surviving codebase — but one was clearly designed.

The guard `if (TRUE||!homeset)` is textbook debug-disabled code. The intended condition was `if (!homeset)`: supply the default wide range only when the caller provides no homeset. A caller providing a `homeset` (a specific document's ISA as an orgl-range specifier) was supposed to get document-scoped results. The `TRUE||` prefix collapses both branches into always-use-default, permanently defeating the scoping [EC-FIND-LINKS-GLOBAL].

`findlinksfromtothreesp()` in `spanf1.c:56-103` faithfully passes its `orglrange` argument to `sporglset2linkset`, and `dofindlinksfromtothree()` constructs that argument from the caller's `homedocids` parameter. The full plumbing exists; only the final dispatch inside `sporglset2linkset` is broken. The `homedocids` filter in `find_links` is accepted without error and silently ignored [EC-HOMEDOCIDS-FILTER-BROKEN], consistent with this being a latent, never-enabled feature rather than a regressed one.

### Is width 100 sufficient, or does it silently truncate?

It depends on deployment scale. The answer is **no truncation in practice for the test docuverse, but yes truncation is possible in larger deployments**.

The ORGLRANGE dimension stores link ISAs (structured as `node.0.user.0.doc.0.2.link_number`). The range is `[zero_tumbler, zero_tumbler + 100)` — where `100` here is a single mantissa position holding the integer one hundred, not three separate digits. From [SS-TUMBLER] (Finding 0031), each mantissa slot is an `INT`, not a decimal digit.

For a tumbler like `1.1.0.1.0.1.0.2.1`:
```
mantissa = [1, 1, 0, 1, 0, 1, 0, 2, 1, 0, ...]  (mantissa[0] = 1)
```
The tumbler total order compares mantissa lexicographically at the same exponent [INV-TUMBLER-TOTAL-ORDER]. At position 0: `1 < 100`, so this ISA is **inside** the range `[0, 100)`.

**What would fall outside?** Any ISA whose `mantissa[0] ≥ 100` — i.e., a node number of 100 or higher. In the udanax-green test environment (single node `1.x`, few users), `mantissa[0]` is always 1, so the range is adequate. In a docuverse with 100+ nodes, links allocated under those nodes would have `mantissa[0] ≥ 100` and be **silently invisible** to all `find_links` queries — no error, just empty or incomplete results.

The comment "effectively unbounded for any realistic deployment" [EC-FIND-LINKS-GLOBAL] reflects the assumption that the ORGL addressing space stays below 100 at its first digit. For the experiment-scale systems this code was built for, that was true. For a production multi-node docuverse, it is a latent scalability bug.

### Summary

| Question | Answer |
|----------|--------|
| Document-scoped mode ever worked? | No — plumbing exists, `TRUE||` disabled dispatch before it could function |
| Width 100 sufficient for test systems? | Yes — single-node ISAs have `mantissa[0]=1`, well within `[0,100)` |
| Width 100 sufficient at scale? | No — any node with ordinal ≥ 100 produces ISAs outside the range, silently dropped |

---

## Code Exploration

I now have everything needed. Here is the full analysis.

---

## Analysis: `sporglset2linkset` — Document-Scoped Mode and the Width-100 Constant

### 1. The Function: `sporgl.c:222–237`

```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
                      typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;

    *linksetptr = NULL;
    if (TRUE||!homeset) {                          // ← always TRUE
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;       // ← hardcoded limit
        nullhomeset.next = NULL;
        homeset = &nullhomeset;
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

### 2. Was Document-Scoped Mode Ever Working?

**Yes — and it was deliberately disabled, at two separate layers.**

#### Layer 1: `TRUE||!homeset` — `sporgl.c:227`

The condition `TRUE||!homeset` means the `!homeset` branch is **unreachable dead code**. This is not an accident; it's a deliberate short-circuit. If it had read just `!homeset`, the function would use caller-supplied homeset (document scope) when given, or fall back to the global nullhomeset when NULL. The `TRUE||` prefix kills that entirely.

The signature `typeispan *homeset` was designed to accept a caller-specified I-address range restricting which link orgl coordinates to search. That parameter is now always overridden.

#### Layer 2: `fns.c:198` — The FEBE Handler Explicitly Drops the Homeset

At the FEBE protocol boundary, even the parsed homeset from the client is discarded before it reaches the engine:

```c
// fns.c:197-199
   getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                           (typeispan*)NULL/*homeset*/, &linkset))
```

The comment `/*homeset*/` makes the intent explicit — the variable is parsed, then deliberately replaced with NULL. Note that the `findnumoflinksfromtothree` and `findnextnlinksfromtothree` handlers (`fns.c:213`, `fns.c:230`) do pass `homeset` through — but it is discarded anyway at `sporgl.c:227`.

#### Why Was It Disabled?

Multiple comment threads in the code tell the same story:

- `sporgl.c:251`: `if (FALSE/*trying to kluge links followable thru versions */&&...)`
- `spanf1.c:245`: `(typeisa*)NULL/*kluge to make links show thru to version &sporglptr->sporgladdress*/`
- `sporgl.c:134`: `movetumbler(homedoc/*&sporglset->sporgladdress*/, &specptr->docisa)`

The problem is **versioning**. When a new version of a document is created, it gets a new V-address and eventually a new I-address. If link search were restricted to a specific document I-address, links created against the old version would become invisible to queries on the new version — because the link endpoint's I-address points to the old version's orgl. Making the search unconditionally global is the workaround: you find all links across all versions.

So: document-scoped link lookup was an intended design feature, disabled sometime in the early-to-mid 1980s (the comments use 1984-era datestamps) when versioning made it semantically incorrect. It was never re-enabled.

---

### 3. The Width-100 Constant — `sporgl.c:230`

```c
nullhomeset.width.mantissa[0] = 100;
```

This sets the nullhomeset width tumbler to the value `100` (exp=0, mantissa[0]=100). In `sporglset2linksetinrange` it is passed through `prefixtumbler` twice:

```c
// sporgl.c:257-258
prefixtumbler(&orglrange->stream, spantype, &range.stream);   // → spantype.0
prefixtumbler(&orglrange->width, 0, &range.width);            // → 0.100
```

Tracing `prefixtumbler` (`tumble.c:641–651`) for the width case (aptr={exp=0, mantissa[0]=100}, bint=0):

1. `temp1 = {mantissa[0]=0}` → zero tumbler (bint=0)
2. `temp2 = {exp=0, mantissa[0]=100}`; since non-zero: `temp2.exp -= 1` → `exp=-1`
3. `tumbleradd(zero, {exp=-1, mant[0]=100})` → `{exp=-1, mant[0]=100}` = `0.100`

Adding start (`spantype`) + width (`0.100`) via `absadd` (`tumble.c:444`):
- start: `{exp=0, mant[0]=spantype}`
- width: `{exp=-1, mant[0]=100}`
- result: `{exp=0, mant=[spantype, 100, 0, ...]}` = `spantype.100`

**The ORGLRANGE query interval is `[spantype, spantype.100)`.** This covers all link I-addresses whose orgl key starts with `spantype.D` where `D < 100` (first digit of the link I-address).

#### Does It Truncate?

This depends on what I-addresses are actually generated for links.

When a link is inserted via `insertspanf` (`spanf1.c:22`):
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

If the link I-address is `A.B.C...`, the orgl key is `spantype.A.B.C...`. The search range `[spantype, spantype.100)` catches all links where `A < 100`.

In udanax-green's allocator, the root node has I-address `1`, accounts are created as `1.0.N` (N=1,2,...), and links/documents under an account are `1.0.N.0.M`. The **first digit `A` is always `1`** (everything descends from the root `1`). Since `1 < 100`, **the threshold is never reached under normal operation**.

#### When Could It Truncate?

Silently, if an I-address namespace were constructed with a first digit ≥ 100. For example, a link I-address `100.0.1.0.1` would produce orgl key `spantype.100.0.1.0.1`. Comparing this to the right boundary `spantype.100`:

```
mantissa: [spantype, 100, 0, 1, 0, 1, ...]  vs  [spantype, 100, 0, 0, ...]
                                   ↑                                ↑
                  mantissa[3]=1               mantissa[3]=0  → GREATER
```

`spantype.100.0.1.0.1 > spantype.100` → the enfilade node is TOMYRIGHT of the range → **silently missed, no error**.

This is a latent hazard, but one that does not trigger in the existing codebase because the Xanadu address allocator always produces addresses under root `1`. The 100 chosen is effectively arbitrary — there is nothing in the code that bounds the first digit of generated I-addresses to stay under 100; it just happens to always be 1.

---

### Summary

| Question | Answer |
|---|---|
| Was document-scoped mode ever working? | Almost certainly yes — it was deliberately disabled at two layers: `TRUE\|\|` in `sporgl.c:227` and `(typeispan*)NULL/*homeset*/` in `fns.c:198`, to avoid links becoming invisible across version boundaries |
| Why disabled? | Versioning: link endpoints reference old-version I-addresses; restricting search by document I-address would lose links after versioning. Global search is the workaround (`sporgl.c:251`, `spanf1.c:245`) |
| Can width=100 truncate? | Not in practice — all standard udanax-green I-addresses have first digit `1` (< 100). But if any I-address with first digit ≥ 100 existed, its links would be silently omitted with no error, no truncation warning, and no indication of missing results |
| Is the threshold tight? | No — there is 99× headroom versus any actual address generated by the allocator, but nothing enforces that the allocator stays below 100 |

---

## Question 14 [gregory]

> When `find_links` is called with the three-way filter (from/to/three), how does the spanfilade search combine the three endset constraints — does it intersect candidate sets from each endset type independently, or does it search one endset and then filter by the others?

### Gregory's Answer

## KB Synthesis

## Three-Way Filter: Independent Search Then Intersection

The spanfilade searches each endset type independently and then intersects the resulting candidate sets.

### How the spanfilade is structured for this

The spanfilade indexes link endpoints across three distinct ORGLRANGE subspaces, differentiated by a prefix value:
- `LINKFROMSPAN = 1` — from-endset entries
- `LINKTOSPAN = 2` — to-endset entries  
- `LINKTHREESPAN = 3` — type/three-endset entries

[SS-RETRIEVE-ENDSETS] (Finding 0035) documents this directly: `retrieveendsetsfromspanf()` "defines three search spaces using ORGLRANGE prefixes... then for each endset type calls `retrievesporglsetinrange()` which searches the spanfilade with SPANRANGE and ORGLRANGE restrictions." Each of the three searches is independent — the SPANRANGE dimension carries the content I-address, while ORGLRANGE partitions by endpoint type.

### The intersection step

[SS-FIND-LINKS] (Finding 0035) names the combining function: `intersectlinksets()` at `backend/spanf2.c:46-120`, with complexity **O(n·m) or O(n·m·p)** depending on how many non-NOSPECS arguments are supplied. The O(n·m·p) form confirms three independent candidate lists being intersected pairwise.

[SS-FIND-LINKS] (Finding 0029) documents the AND semantics:

> When both source and target specs are provided, both endpoints must have V-stream presence for the link to be found. Single-endpoint search (passing NOSPECS for the other) requires only that endpoint's presence.

And formalizes it: `find_links(source_spec, target_spec)` ≡ `find_links(source_spec) ∩ find_links(target_spec)`.

### Summary

The mechanism is:
1. For each non-NOSPECS argument, convert the V-spec to I-addresses (sporglset)
2. Search the spanfilade restricted to the corresponding ORGLRANGE subspace (LINKFROMSPAN, LINKTOSPAN, or LINKTHREESPAN), producing a candidate link set for each
3. Intersect the resulting sets via `intersectlinksets()` — links must appear in **all** supplied candidate sets to be returned

Passing NOSPECS for an argument skips that search entirely; the absent constraint does not contribute a candidate set and thus does not constrain the intersection. [SS-FIND-LINKS] (Finding 0029) also notes that `find_links` with a zero-tumbler cursor (NOSPECS) starts from the beginning of whichever sets were searched.

One important caveat: the orgl-range dimension filter (intended to scope searches to a specific home document) is effectively disabled — `sporglset2linkset()` replaces whatever orgl range the caller passes with a hardcoded global range [EC-FIND-LINKS-GLOBAL] (Finding 0069). So while the three-endset intersection works correctly, there is no functional scoping by document.

---

## Code Exploration

## How `find_links` Combines Three Endset Constraints

The answer is: **it searches each endset independently, then intersects the three candidate sets.** It does not search one endset and filter by the others.

---

### Execution Path

**`fns.c` (entry point)**

`findlinksfromtothree()` [fns.c:189-202] receives three specsets and delegates:

```c
getfindlinksfromtothree(taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree(taskptr, fromvspecset, tovspecset, threevspecset, ...)
```

**`do1.c` (delegation)**

`dofindlinksfromtothree()` [do1.c:348-353] is a pure pass-through to the spanfilade:

```c
return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset, threevspecset, orglrangeptr, linksetptr);
```

---

### Core Algorithm: `findlinksfromtothreesp()` [spanf1.c:56-103]

This is the key function. It operates in two distinct phases:

**Phase 1 — Three independent spanfilade searches:**

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

if (fromvspecset) {
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); }  // early exit
}
if (tovspecset) {
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }    // early exit
}
if (threevspecset) {
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return(TRUE); } // early exit
}
```

Each call to `sporglset2linkset()` passes a different endset-type flag — `LINKFROMSPAN`, `LINKTOSPAN`, `LINKTHREESPAN` — so each search queries a distinct index region of the spanfilade. The three searches produce three independent link candidate sets.

Note the **short-circuit early exit**: if any intermediate result is empty, the whole result is immediately empty. This is an optimization, not a filter.

**Phase 2 — Intersection:**

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

---

### Intersection Logic: `intersectlinksets()` [spanf2.c:46-120]

With all three sets non-null, it uses triple-nested loops:

```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        for (temp3 = linkset3; temp3; temp3 = temp3->next) {
            if (tumblereq(&temp1->address, &temp2->address)
                && tumblereq(&temp2->address, &temp3->address)) {
                linkset4 = makelinkitem(taskptr, &temp1->address);
                *linkset4ptr = linkset4;
                linkset4ptr = &linkset4->next;
            }
        }
    }
}
```

A link is included in the final result only if its tumbler address appears in **all three** independent search results. The condition `temp1==temp2 && temp2==temp3` (via `tumblereq`) enforces this. `intersectlinksets()` also handles degenerate cases where only one or two filters were specified [spanf2.c:65-73], returning the sole non-null set directly without looping.

---

### Answer

The spanfilade search performs **three independent scans** — one per endset type, using the type-specific index — and then **intersects the three resulting link sets**. It does not search one endset and filter by the others. The three `sporglset2linkset()` calls are fully independent; only `intersectlinksets()` combines them, via an O(n³) triple-nested loop that requires a link to appear in all three candidate sets.

---

## Question 15 [gregory]

> After candidate links are found via the spanfilade, `link2sporglset` extracts I-addresses from the link orgl in the granfilade — does this extraction read the link's actual endset spans, or does it rely on the spanfilade's indexed copy, and can these ever diverge?

### Gregory's Answer

## KB Synthesis

`link2sporglset` reads exclusively from the **granfilade link orgl** — the permanent, canonical record. It never consults the spanfilade.

## Two separate read paths

**FOLLOWLINK** uses `link2sporglset()` (`sporgl.c:67-95`), which calls `retrieverestricted()` against the granfilade to extract I-addresses from the link orgl at the requested endset position (0.1, 0.2, or 0.3) [SS-FOLLOWLINK]. No POOM check and no spanfilade access occur here.

**RETRIEVEENDSETS** works the other direction entirely: it takes a content region, converts it to I-addresses via sporglset, and searches the spanfilade using ORGLRANGE prefixes (LINKFROMSPAN=1, LINKTOSPAN=2, LINKTHREESPAN=3) to find links whose indexed I-addresses overlap [SS-RETRIEVE-ENDSETS]. The spanfilade is an inverted index (I-address → link ISA), serving discovery; the link orgl is the forward store (link ISA → endpoint I-addresses), serving retrieval.

## Can they diverge?

**Under normal operation: no.** At `CREATELINK` time, `docreatelink` writes both structures from the same sporglset [ST-CREATE-LINK]:
1. Creates the link orgl in the granfilade (permanent)
2. Indexes endpoint I-addresses in the spanfilade via `insertendsetsinspanf`

Both the granfilade link orgl and the spanfilade entries are written once and never modified — the granfilade is append-only and the spanfilade is write-only [INV-SPANF-WRITE-ONLY]. So under crash-free operation they represent the same I-address set.

**Under a crash: yes.** `docreatelink` performs these two writes sequentially with no transactional mechanism [INV-DUAL-ENFILADE-CONSISTENCY]. A crash between them leaves the link orgl in the granfilade with no spanfilade entries. The result: the link is followable by ID (orgl is authoritative) but undiscoverable by content-identity search (no spanfilade index). This is the consistency risk the KB identifies as the main threat to the dual-enfilade invariant.

**One important asymmetry**: the spanfilade can also contain *stale* entries from deleted content that no longer appears in any POOM [EC-STALE-SPANF-REFERENCE, INT-DELETE-SPANF-DIVERGENCE], but stale spanfilade entries for *content* do not affect what the link orgl says about its endpoints — the link orgl stores the original endpoint specification permanently. What `link2sporglset` returns is always the creation-time specification, unaffected by any subsequent content deletion.

---

## Code Exploration

I now have all the code I need to answer definitively. Here is the full analysis:

---

## Answer: `link2sporglset` reads from the link's granfilade orgl — never the spanfilade

### The two data structures written at link creation

`docreatelink` (do1.c:195–221) populates **both** structures from the same `fromsporglset`/`tosporglset` in a single chained expression:

```c
/* do1.c:218–219 */
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset,
                         &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

**`insertendsetsinorgl`** (do2.c:130–149) calls `insertpm` (orglinks.c:75–134) for each endset. `insertpm` stores a 2D crum in the link's POOM enfilade:

- **I-dimension** (`crumorigin.dsas[I]`, `crumwidth.dsas[I]`): the actual I-span — origin from `unpacksporgl`'s `lstream`, width from `lwidth`  [orglinks.c:105–109]
- **V-dimension** (`crumorigin.dsas[V]`, `crumwidth.dsas[V]`): the V-address from `setlinkvsas` (do2.c:169–180):  FROM → `1.1`, TO → `2.1`, THREE → `3.1`

```c
/* orglinks.c:130–131 */
insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
tumbleradd (vsaptr, &crumwidth.dsas[V], vsaptr);
```

**`insertendsetsinspanf`** (do2.c:116–128) calls `insertspanf` (spanf1.c:15–54) for each endset. `insertspanf` stores a 2D crum in the **global spanfilade** (`spanf`), keyed by:

- **SPANRANGE** (`crumorigin.dsas[SPANRANGE]`, `crumwidth.dsas[SPANRANGE]`): the same I-span
- **ORGLRANGE** (`crumorigin.dsas[ORGLRANGE]`): `linkisaptr` prefixed by the endset type constant (`LINKFROMSPAN=1`, `LINKTOSPAN=2`, `LINKTHREESPAN=3`  [xanadu.h:36–38])

```c
/* spanf1.c:22 */
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

---

### `link2sporglset` reads the granfilade — never the spanfilade

```c
/* sporgl.c:67–95 */
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
  typeorgl orgl;
  tumbler zero;
  typevspan vspan;
  ...
  if (!findorgl (taskptr, granf, linkisa, &orgl, type)){    /* ← granfilade */
      return (FALSE);
  }
  tumblerclear (&zero);
  tumblerincrement (&zero, 0, whichend, &vspan.stream);     /* stream = whichend */
  tumblerincrement (&zero, 0/*1*/, 1, &vspan.width);        /* width  = 1        */
  if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
      for (c = context; c; c = c->nextcontext) {
          sporglptr = (typesporgl *)taskalloc(taskptr,sizeof (typesporgl));
          contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
          ...
      }
      ...
  }
}
```

Three observations:

**1. `findorgl` goes to `granf`**, the global granfilade root [sporgl.c:77]. `fetchorglgr` returns the link's own POOM sub-enfilade node. This is the link's canonical data store — not `spanf`.

**2. `retrieverestricted` is called on `orgl`**, the link's POOM node [sporgl.c:83]. The arguments `V` (index1) and `I` (index2) make it a V→I lookup: find I-space crumbs whose V-position overlaps `[whichend, whichend+1)`. Since `setlinkvsas` stored FROM at `1.1`, TO at `2.1`, THREE at `3.1`, the query range `[1,2)` correctly contains `1.1` for FROM; `[2,3)` contains `2.1` for TO, etc.

**3. `contextintosporgl` extracts I-space** from the context result [sporgl.c:86, sporgl.c:205–220]:

```c
/* sporgl.c:211, 219 */
movetumbler(&context->totaloffset.dsas[index],&sporglptr->sporglorigin);
movetumbler (&context->contextwid.dsas[index], &sporglptr->sporglwidth);
```

`index` = `I`. So the sporgl's origin and width are read from the **I** dimension of the crum, which is exactly the I-span that `insertpm` stored. The V-address serves only as the lookup key — it is not propagated into the output sporgl.

The spanfilade variable `spanf` does not appear anywhere in `link2sporglset`, `contextintosporgl`, `findorgl`, or `retrieverestricted` (which dispatches on `fullcrumptr->cenftype` — POOM/SPAN/GRAN — not on which global variable was passed).

The complete downstream path from `dofollowlink` (do1.c:223–232) also avoids the spanfilade:

- `linksporglset2specset` (sporgl.c:97–123): for sporgls with a non-zero address, calls `linksporglset2vspec` → `sporglset2vspanset` → `ispan2vspanset` (orglinks.c:389–394) → `permute` → `span2spanset` (orglinks.c:425–454) → `retrieverestricted((typecuc*)orgl, ...)` on the **document's** POOM orgl. The spanfilade is not consulted at any step.

---

### The `doretrieveendsets` path reads the spanfilade

`doretrieveendsets` (do1.c:369–374) → `retrieveendsetsfromspanf` (spanf1.c:190–235) is an entirely separate operation. It:

1. Converts the link's vspec to a sporglset via `specset2sporglset` (which goes through the granfilade to do V→I)
2. Then calls `retrievesporglsetinrange` (spanf1.c:237–267), which calls `retrieverestricted` on **`spanf`** — the global spanfilade:

```c
/* spanf1.c:245 */
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE,
                               whichspace, ORGLRANGE, (typeisa*)NULL/*kluge...*/);
```

This reads the spanfilade's indexed copy. `link2sporglset` and `doretrieveendsets` access different data structures and could in principle return different I-spans.

---

### Can the two structures diverge?

**At write time, they are identical**: Both `insertendsetsinorgl` and `insertendsetsinspanf` consume the same `fromsporglset`/`tosporglset` objects created from the same user-supplied specsets. Under a successful link creation, the I-spans stored in the granfilade orgl and the I-spans indexed in the spanfilade are the same.

**Partial failure is a live divergence path**: The two writes are sequenced with `&&` (do1.c:218–219). There is no rollback for the granfilade write if the spanfilade write fails. If `insertendsetsinorgl` succeeds and `insertendsetsinspanf` fails — or fails mid-way (it calls `insertspanf` for FROM, then TO, then THREE separately; do2.c:119–126) — the granfilade will have some or all endsets while the spanfilade has fewer:

```c
/* do2.c:118–126 */
if (!(
  insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
  &&insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
      return (FALSE);   /* orgl already written; no rollback */
if (threesporglset) {
    if(!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN)){
        return (FALSE);
    }
}
```

In that scenario: `link2sporglset` (granfilade) succeeds and returns correct endsets; the spanfilade-based candidate search (`sporglset2linksetinrange`) fails to find the link via the missing endset. The structures diverge silently.

**No post-creation modification path exists**: Neither `domakelink` nor `docreatelink` updates endsets after the initial write. There is no "edit link endsets" operation. So divergence from modification is not a concern.

**Ordering may differ**: The granfilade POOM traversal returns crumbs in V-order (FROM before TO before THREE). The spanfilade SPAN traversal in `retrievesporglsetinrange` returns crumbs in I-address order. If a link's endsets happen to span non-contiguous I-space regions, the two paths will return the same set of I-spans but in different order.

---

### Summary

`link2sporglset` reads **exclusively from the link's granfilade orgl** (the link's own POOM enfilade node). The call at sporgl.c:77 passes `granf` to `findorgl`; the `retrieverestricted` at sporgl.c:83 queries the returned `orgl` POOM node in V-space; `contextintosporgl` at sporgl.c:86 extracts the I-dimension from each result crum. The spanfilade is not accessed at any point in this path.

The spanfilade holds a **parallel index** written at link creation from the same sporglset data. It is read only by the "find links by content region" path (`sporglset2linksetinrange` → `retrieverestricted` on `spanf`), not by `link2sporglset`. The two structures *can* diverge if `insertendsetsinorgl` succeeds but `insertendsetsinspanf` fails, because no rollback mechanism exists for the granfilade write. In that case, `link2sporglset` returns the correct endsets (from the granfilade), while the spanfilade-based candidate search does not find the link via its missing endset index entries.

---

## Question 16 [gregory]

> When resolving a discovered link's endsets back to V-addresses via `linksporglset2specset`, how does the I→V conversion handle an I-address that maps to multiple V-positions within the same document (e.g., after self-transclusion) — does it return all V-positions or just the first found?

### Gregory's Answer

## KB Synthesis

## I→V Conversion Returns All V-Positions

The conversion returns **all** V-positions, not just the first found.

### The Mechanism

`linksporglset2specset` follows the call chain documented in [SS-FOLLOWLINK]:

```
link2sporglset() → linksporglset2specset() → span2spanset() → retrieverestricted()
```

`retrieverestricted()` drives the POOM B-tree traversal via `findcbcinarea2d()`. The critical property is in [SS-POOM-MULTIMAP]: this traversal **iterates all siblings at each level and recurses into all qualifying subtrees**, accumulating every matching leaf node. The accumulation function `incontextlistnd()` performs insertion-sort into a linked list and **never replaces existing entries** — it only appends new ones. There is no early-exit after the first match.

The POOM is explicitly a multimap (`Multimap<(VPosition, IAddress)>`), and `ispan2vspanset` has return type `Set<VSpan>` with the postcondition `|result| >= 1` when the I-address exists [SS-POOM-MULTIMAP].

### Concrete Confirmation

From [SS-POOM-MULTIMAP] (Finding 0039), for a document with "B" at V-positions 1.2, 1.4, and 1.5 all referencing I-address `i_B`:

```
ispan2vspanset(poom, i_B) = {
  VSpan(1.2, width=0.1),
  VSpan(1.4, width=0.1),
  VSpan(1.5, width=0.1)
}
```

All three V-positions are returned.

### Ordering

The result is sorted by V-address via `incontextlistnd`'s insertion-sort [INV-RETRIEVAL-V-SORTED], and this ordering is independent of tree structure [INV-RETRIEVAL-TREE-INDEPENDENCE].

### Implication for Link Endset Resolution

When `linksporglset2specset` resolves a link endset containing an I-address that was self-transcluded N times within the home document, it produces N V-spans — one per V-position referencing that I-address. This is precisely the behavior noted in [INV-LINK-IDENTITY-DISCOVERY]: links are discoverable from *all* V-positions sharing an I-address, and the endset resolution mirrors this by reporting all of them.

The silent-drop behavior noted in [SS-FOLLOWLINK] (when `retrieverestricted` returns NULL) only applies when **no** POOM entry exists for the I-address — not as a cardinality limit on multiple entries.

---

## Code Exploration

Now I have everything needed. Here is the complete answer:

---

## I→V Conversion in `linksporglset2specset`: All V-Positions Are Returned

The conversion returns **all** V-positions, not just the first. The full call chain is exhaustive at every layer. Here is the trace.

---

### Layer 1 — `linksporglset2specset` [`sporgl.c:97–123`]

```c
for (; sporglset; sporglset = (typesporglset)((typeitemheader*)sporglset)->next) {
    specset = (typespecset) taskalloc(taskptr, sizeof(typevspec));
    if (iszerotumbler(&((typesporgl *)sporglset)->sporgladdress)) {
        // pure I-span: zero address means no home doc
        ((typeitemheader *)specset)->itemid = ISPANID;
        ...
    } else {
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
    }
    ((typeitemheader *)specset)->next = NULL;
    *specsetptr = specset;
    specsetptr = (typespecset *)&((typeitemheader *)specset)->next;  // [sporgl.c:120]
}
```

Every sporgl item in the input list produces one output `specset` item. The `specsetptr` pointer is advanced at line 120, building a linked list. **No early exit.**

For sporgls with a non-zero `sporgladdress` (the normal case — the endset has a known home document in I-space), conversion delegates to `linksporglset2vspec` → `sporglset2vspanset` [`sporgl.c:141`] → `ispan2vspanset` [`orglinks.c:389`].

---

### Layer 2 — `ispan2vspanset` / `permute` [`orglinks.c:389–422`]

```c
typevspanset *ispan2vspanset(...) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);  // [orglinks.c:393]
}

typespanset *permute(...) {
    save = targspansetptr;
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                     restrictionindex, targspansetptr, targindex);
    }
    return (save);  // [orglinks.c:421]
}
```

`permute` iterates over all restriction spans in the input set (in this case the single I-span), accumulating results into `targspansetptr`.

---

### Layer 3 — `span2spanset` [`orglinks.c:425–454`]

This is the critical function:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr,
                             restrictionindex, (typespan*)NULL, targindex, (typeisa*)NULL);
// [orglinks.c:435]

for (c = context; c; c = c->nextcontext) {          // [orglinks.c:439]
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan,
                                    (typeitemset*)targspansetptr);
}
if (!context) {
    return(targspansetptr);   // [orglinks.c:447] — only on empty result
}
contextfree(context);
return (&nextptr->next);      // [orglinks.c:453]
```

`retrieverestricted` returns a **linked list** of contexts — one per matching enfilade crum. The `for` loop at line 439 processes **every context** in that list. `onitemlist` at line 444 appends each converted V-span to the growing result list. The only early return (line 447) fires only when `retrieverestricted` finds **nothing** at all.

---

### Layer 4 — `retrieverestricted` → `findcbcinarea2d` [`retrie.c:56–268`]

`retrieverestricted` [`retrie.c:56`] → `retrieveinarea` [`retrie.c:87`] → `findcbcinarea2d` [`retrie.c:229`]:

```c
for (; crumptr; crumptr = getrightbro(crumptr)) {  // [retrie.c:252]
    if (!crumqualifies2d(crumptr, ...)) {
        continue;
    }
    if (crumptr->height != 0) {
        findcbcinarea2d(findleftson((typecuc*)crumptr), &localoffset, ...);  // recursive
    } else {
        context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd(headptr, context, index1);  // [retrie.c:263] — APPEND
    }
}
```

This recursively traverses the entire POOM enfilade. At every **leaf crum** (`height == 0`) that passes `crumqualifies2d`, a context is created and **appended** to `*headptr` via `incontextlistnd`. The traversal is exhaustive: no crum is skipped once qualified, and there is no early `return` after the first match.

After self-transclusion, the same I-range appears as a mapping source in **multiple** crums (the original insertion and the transcluded copy), each at a different V-position. `findcbcinarea2d` finds all of them.

---

### Layer 5 — `incontextlistnd` [`context.c:75–111`]

```c
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    ...
    if (!clist) { *clistptr = c; return(0); }          // first item
    if (whereoncontext(...) < THRUME) {                 // insert at head
        c->nextcontext = clist; *clistptr = c; return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {  // insert in middle
            if (...) { ...; return(0); }
        }
    }
    clist->nextcontext = c;   // [context.c:110] — insert at tail
}
```

`incontextlistnd` maintains a **sorted linked list**. It always inserts — it never discards a result. Every context created by `findcbcinarea2d` ends up in the list.

---

### Answer

**All V-positions are returned.** When an I-address maps to N distinct V-positions (e.g., after self-transclusion: the original at V=1.0.1 and the copy at V=1.0.3), `findcbcinarea2d` finds both leaf crums, `incontextlistnd` appends both to the context list, and `span2spanset`'s `for (c = context; c; c = c->nextcontext)` loop at [`orglinks.c:439`] converts both to V-spans and appends both to the result via `onitemlist`. The final `vspanset` handed back through `ispan2vspanset` → `sporglset2vspanset` → `linksporglset2vspec` is a linked list with one entry per V-position.

The only coalescing that could reduce this count is `putvspaninlist` [`orglinks.c:329`], which merges adjacent/overlapping spans. But `span2spanset` uses `onitemlist` (not `putvspaninlist`), which does **no merging** — it simply appends. So distinct V-positions from self-transclusion emerge as distinct entries in the returned set.

---

## Question 17 [gregory]

> For a link whose source endset spans a range of I-addresses and only a subset of those I-addresses appear in the querying document's POOM, does `find_links` still return that link, or must the entire endset I-range be present for the link to match?

### Gregory's Answer

## KB Synthesis

**Yes, partial overlap suffices.** A link is returned by `find_links` whenever the query's I-address set has a non-empty intersection with the link's endpoint I-addresses — there is no requirement for the full endset to be present.

This is stated explicitly in [SS-FIND-LINKS] (Finding 0028):

> The search is purely set-intersection on I-addresses: `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`. **Partial overlap suffices** — a search specset that shares even one I-address with a link endpoint will discover that link.

The concrete example there makes this precise: a link whose source covers I-addresses `{I.4, I.5, I.6}` is returned when the querying document contains only `{I.5, I.6}` (transcluded "EF" from a 14-char source "hyperlink text"). The two-address intersection is sufficient.

The mechanism works through the spanfilade. Each I-address (or contiguous I-span) in a link's endset is individually indexed in the spanf at link creation time [SS-SPANF-OPERATIONS], [INT-SPORGL-LINK-INDEX]. When `find_links` runs, it converts the query specset to I-spans via V→I conversion, then searches the spanfilade for any overlap. A single matching I-span triggers the link's inclusion in the result.

Importantly, `follow_link` on a link discovered this way returns the **complete original endset**, not just the subset that enabled discovery [SS-FOLLOW-LINK] (Finding 0028):

> Even when a link is found via partial I-address overlap from a transclusion, `follow_link` returns the full endpoint as it was specified at link creation time.

This behavior also appears in [EC-SEARCH-SPEC-BEYOND-BOUNDS] — after content is partially deleted from a document, `find_links` still returns links whose remaining content overlaps the query, confirming that partial endset coverage is the normal operating model.

---

## Code Exploration

I have traced the complete execution path. Here is the full answer.

---

## Does `find_links` Require the Full Endset I-Range or Only Overlap?

**Short answer:** Partial overlap is sufficient. `find_links` returns the link if **any** I-address contributed by the querying document's POOM overlaps with any I-address in the link's stored endset range. The entire endset I-range does not need to be present.

---

## Execution Path

### Entry point: `fns.c:189` → `do1.c:348` → `spanf1.c:56`

`findlinksfromtothree` [fns.c:189] dispatches to `dofindlinksfromtothree` [do1.c:348], which is a thin wrapper:

```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset, ...)
{
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, ...);
}
```

The real work happens in `findlinksfromtothreesp` [spanf1.c:56–103].

---

### Step 1: V → I Translation via the Querying Document's POOM

`findlinksfromtothreesp` [spanf1.c:70–71]:

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
```

`specset2sporglset` [sporgl.c:14] calls `vspanset2sporglset` [sporgl.c:35] which:

1. Opens the querying document's POOM via `findorgl` [sporgl.c:44]
2. For each V-span, calls `vspanset2ispanset` [sporgl.c:48] → `permute` [orglinks.c:404] → `span2spanset` [orglinks.c:425]
3. `span2spanset` calls `retrieverestricted` on the POOM to find what I-addresses correspond to those V-positions

This V→I translation is **bounded by what the querying document's POOM actually maps**. If the querying document's POOM covers only a subset of the link's endset I-range, the resulting `fromsporglset` contains only those partial I-addresses — e.g., `[A, A+x]` where the link's endset is `[A, B]` with `x < B−A`.

---

### Step 2: Spanfilade Lookup — Overlap, Not Containment

`findlinksfromtothreesp` [spanf1.c:76–83]:

```c
if (fromvspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return (TRUE); }
}
```

`sporglset2linkset` [sporgl.c:222] creates a broad default `orglrange` with width=100 (covering all links) and calls `sporglset2linksetinrange` [sporgl.c:239] for each I-span in the query:

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                             &range, ORGLRANGE, (typeisa*)infoptr);
```

This asks the spanfilade: *"find all entries whose SPANRANGE (= the link's stored endset I-range) intersects with my query SPANRANGE (= the querying document's I-addresses)."*

The spanfilade stores, for each link endset, entries of the form `(SPANRANGE=link_endset_I_range, ORGLRANGE=link_ISA)` — inserted at link creation time by `insertspanf` [spanf1.c:15].

---

### Step 3: The Overlap Predicate in `crumqualifies2d`

`retrieverestricted` [retrie.c:56] → `retrieveinarea` [retrie.c:87] → `findcbcinarea2d` [retrie.c:229] → **`crumqualifies2d` [retrie.c:270]**.

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset,
                     tumbler *span1start, tumbler *span1end, INT index1,
                     tumbler *span2start, tumbler *span2end, INT index2, ...)
{
    endcmp = iszerotumbler(span1end) ? TOMYRIGHT
           : whereoncrum(crumptr, offset, span1end, index1);
    if (endcmp <= ONMYLEFTBORDER) return (FALSE);   // [retrie.c:282-284]

    startcmp = whereoncrum(crumptr, offset, span1start, index1);
    if (startcmp > THRUME) return (FALSE);           // [retrie.c:286-290]
    ...
    return (TRUE);
}
```

In plain terms, a spanfilade crum (representing the link's endset I-range `[A, B]`) passes if and only if:

> `query_end > A` **AND** `query_start < B`

That is: the query range **overlaps** the crum's range. There is no containment requirement in either direction. The check is symmetric overlap.

So if the querying document contributes I-range `[A, A+x]` (a strict subset of the link's `[A, B]`):

- `query_end = A+x > A` (crum start) → passes the first check
- `query_start = A < B` (crum end) → passes the second check
- The crum **qualifies** → the link ISA is extracted and added to `fromlinkset`

---

### Step 4: Per-Endset Sets Are Intersected, Not Unioned

After collecting `fromlinkset`, `tolinkset`, and optionally `threelinkset`, `findlinksfromtothreesp` calls:

```c
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // spanf1.c:100
```

`intersectlinksets` [spanf2.c:46] computes the **set intersection**: a link is in the result only if it appears in all provided non-null endset link-sets. But the per-endset lookup itself uses overlap, so a link whose source endset I-range partially overlaps the query will appear in `fromlinkset`, and therefore can survive the intersection.

---

## Conclusion

`find_links` uses **I-address overlap** — not containment — as its matching criterion. The determination is made in `crumqualifies2d` [retrie.c:270–305], which applies:

```
query_end > link_endset_start  AND  query_start < link_endset_end
```

If a link's source endset spans I-addresses `[A, B]` and the querying document's POOM maps only a subset `[A, A+x]` (with `x < B−A`) of that range to V-addresses, then:

- The V→I translation produces a sporglset covering only `[A, A+x]`
- The spanfilade overlap check finds the link's `[A, B]` entry, because `A+x > A` and `A < B`
- **The link is returned**

The entire endset I-range does **not** need to be present in the querying document's POOM. Any non-empty intersection between the querying document's I-addresses and the link's endset I-range is sufficient for the link to be found.

---

## Question 18 [gregory]

> The spanfilade indexes one DOCISPAN entry per contiguous I-span at creation time — if a link's endset references I-addresses that were inserted as separate operations (producing multiple I-spans), does the spanfilade store multiple entries per endset, and does the search correctly aggregate them?

### Gregory's Answer

## KB Synthesis

Yes — multiple entries are stored, and search aggregates them correctly.

**Spanfilade storage per endset:**

When a link is created, [INT-SPORGL-LINK-INDEX] (Finding 0013) documents the path: `insertendsetsinspanf()` receives a sporglset and iterates over it, inserting one spanfilade entry per sporgl. A sporgl represents one contiguous I-address region. From [ST-LINK-CREATE] (Finding 0037):

> `vspanset2sporglset` calls `vspanset2ispanset` which walks the POOM to discover all I-address regions, producing one I-span per contiguous region. The front end sees a simple contiguous selection; the backend decomposes it into identity-preserving references.

So for a link whose endset V-span maps to N non-contiguous I-regions (e.g., content transcluded from multiple sources), N sporgls are created and N spanfilade entries are indexed. [SS-DOCISPAN] (Finding 0047) confirms the per-span granularity: `insertspanf` loops over the `ispanset` linked list making one `insertnd` call per `typeispan` struct.

**Search aggregation:**

The search operates over all spanning entries and aggregates by link ISA. From [SS-FIND-LINKS] (Finding 0035):

> `intersectlinksets()`: `backend/spanf2.c:46-120` — O(n*m) or O(n*m*p) intersection

The intersection finds the link if *any* of its indexed I-spans overlaps the query. [EC-LINK-PARTIAL-SURVIVAL] confirms this per-span independence directly:

> Because each I-span in a link endset independently tracks its content, partial survival is possible. If document A (source of "AA") is deleted but document B (source of "BB") remains, the link endset retains the I-span for "BB" while the I-span for "AA" becomes unresolvable. The link survives partially.

So yes to both parts: the spanfilade stores one entry per I-span in the endset (not one per endset), and the intersection-based search correctly returns the link if any constituent entry matches — with no additional aggregation logic needed because the link ISA is embedded in each entry.

---

## Code Exploration

I now have all the source I need. Here is the complete, citation-backed answer.

---

## Answer: Spanfilade Indexing of Multi-I-span Endsets

### Short answer

**Yes and yes.** When an endset references I-addresses from N separate insert operations (producing N I-spans), `insertspanf` stores N separate spanfilade entries — one per I-span. The search in `sporglset2linksetinrange` iterates over all query I-spans and unions the results before intersection, so all matching entries are found. There is one deduplication edge case (last-element check missing in `onlinklist`) noted below.

---

### 1. Insertion: one spanfilade entry per I-span

`insertspanf` [spanf1.c:15–53] receives a `sporglset` that may contain multiple items — one per contiguous I-span. The ORGLRANGE key (the link ISA prefixed with spantype) is fixed **before** the loop:

```c
// spanf1.c:22–23
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
tumblerclear (&crumwidth.dsas[ORGLRANGE]);
```

Then for **each item** in the sporglset the SPANRANGE key is overwritten with that item's stream/width, and a separate `insertnd` is called:

```c
// spanf1.c:25–52
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    if (((typeitemheader *)sporglset)->itemid == ISPANID) {
        movetumbler (&((typeispan *)sporglset)->stream, &lstream);
        movetumbler (&((typeispan *)sporglset)->width, &lwidth);
        movetumbler (isaptr, &linfo.homedoc);
    } else if (((typeitemheader *)sporglset)->itemid == SPORGLID) {
        movetumbler (&((typesporgl *)sporglset)->sporglorigin, &lstream);
        movetumbler (&((typesporgl *)sporglset)->sporglwidth, &lwidth);
        movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
    } else if (((typeitemheader *)sporglset)->itemid == TEXTID) { ... }
    movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);
    movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
    insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE); // ← one call per I-span
}
```

So for a link whose from-endset covers text inserted in two separate operations (yielding I-spans A and B), `insertspanf` writes two distinct enfilade nodes:

| SPANRANGE key | ORGLRANGE key |
|---|---|
| A.stream / A.width | LINKFROMSPAN . linkISA |
| B.stream / B.width | LINKFROMSPAN . linkISA |

---

### 2. Three separate `insertspanf` calls — one per endset

`insertendsetsinspanf` [do2.c:116–128], called from `docreatelink` [do1.c:219], runs `insertspanf` once per endset:

```c
// do2.c:116–128
bool insertendsetsinspanf(...) {
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)
     && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))
        return (FALSE);
    if (threesporglset)
        if (!insertspanf(taskptr,spanfptr,linkisaptr,threesporglset,LINKTHREESPAN))
            return (FALSE);
    return(TRUE);
}
```

If the from-endset has N I-spans and the to-endset has M I-spans, the link contributes N+M (plus optional three-endset spans) entries to the spanfilade — all sharing the same ORGLRANGE key (`spantype . linkISA`) but each with a distinct SPANRANGE key.

---

### 3. Search: iterates each query I-span, unions results

`sporglset2linksetinrange` [sporgl.c:239–269] iterates the **query** sporglset — which also may contain multiple I-spans — calling `retrieverestricted` once per I-span:

```c
// sporgl.c:250–268
for (; sporglset; sporglset = (typesporglset)((typeitemheader *)sporglset)->next) {
    ...
    if (orglrange) {
        prefixtumbler(&orglrange->stream, spantype, &range.stream);
        prefixtumbler(&orglrange->width, 0, &range.width);
        context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                     &range, ORGLRANGE, (typeisa*)infoptr);
    } else {
        context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                     (typespan*)NULL, ORGLRANGE, (typeisa*)infoptr);
    }
    for (c = context; c; c = c->nextcontext) {
        beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
        onlinklist(taskptr, linksetptr, &linksa);  // accumulate
    }
    contextfree(context);
}
```

The outer loop (`sporglset2linkset` at sporgl.c:234) iterates over the passed `homeset`:

```c
// sporgl.c:226–236 — note the unconditional override
if (TRUE||!homeset) {   // ← "TRUE" means homeset parameter is always ignored
    tumblerclear(&nullhomeset.stream);
    tumblerclear(&nullhomeset.width);
    nullhomeset.width.mantissa[0] = 100;
    nullhomeset.next = NULL;
    homeset = &nullhomeset;
}
for (; homeset; homeset = homeset->next)
    sporglset2linksetinrange(taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
```

The `if (TRUE||...)` unconditionally replaces the orglrange with a wide synthetic span (stream=0, width=100). After `prefixtumbler`, the ORGLRANGE restriction becomes `[spantype.0, spantype.0+100)` — wide enough to match any link ISA less than 100. This is a hardcoded kluge (the comment in the nearby falsy branch at sporgl.c:251 reads `"trying to kluge links followable thru versions"`). It means the orglrange passed from the FEBE layer is silently ignored at the spanfilade search level.

---

### 4. Deduplication via `onlinklist`

`onlinklist` [spanf2.c:26–44] is intended to deduplicate: if the same link ISA appears in the results of two separate `retrieverestricted` calls (because two I-spans in the query both matched the same link), the second occurrence should be dropped:

```c
// spanf2.c:38–44
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq(&temp->address, linkisaptr))
        return(0);  // already in list
}
temp->next = linkset;  // append
```

**Off-by-one bug:** the loop condition is `nextlink = temp->next`, which terminates when `temp` reaches the last element (its `->next` is NULL). The last element's address is never checked. If the ISA of the last-appended link matches the incoming ISA, a duplicate is silently added. In normal operation each `retrieverestricted` returns each matching link once, so duplicates across I-span iterations are the main risk path — and only the tail of the list is unguarded.

---

### 5. Per-endset results are intersected

`findlinksfromtothreesp` [spanf1.c:56–103] calls `sporglset2linkset` for each specified endset, with an early-exit optimization:

```c
// spanf1.c:76–100
if (fromvspecset) {
    sporglset2linkset(..., fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); } // short-circuit
}
if (tovspecset) {
    sporglset2linkset(..., tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }
}
if (threevspecset) { ... }
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);
```

`intersectlinksets` [spanf2.c:46–120] computes the set intersection with a nested loop: O(N×M) for two sets, O(N×M×P) for three. Only link ISAs appearing in all queried per-endset results survive.

---

### Summary table

| Step | Location | What happens for multi-I-span endset |
|---|---|---|
| Link creation | `insertendsetsinspanf` [do2.c:116] | Calls `insertspanf` once per endset |
| Per-endset indexing | `insertspanf` [spanf1.c:25–52] | Loops: one `insertnd` call per I-span in the sporglset |
| 2D key layout | `insertspanf` [spanf1.c:22,49–50] | ORGLRANGE = `spantype . linkISA` (fixed); SPANRANGE = individual I-span (varies per entry) |
| Search per I-span | `sporglset2linksetinrange` [sporgl.c:250–267] | Loops: one `retrieverestricted` call per query I-span; accumulates results |
| Deduplication | `onlinklist` [spanf2.c:38–43] | Deduplicates link ISAs, but **last element unchecked** → potential tail duplicate |
| orglrange filter | `sporglset2linkset` [sporgl.c:227] | `if (TRUE\|\|...)` unconditionally ignores the passed orglrange; uses width=100 synthetic span |
| Final aggregation | `intersectlinksets` [spanf2.c:95–118] | N-way intersection across the three endset result lists |

**Bottom line:** The spanfilade does store one entry per I-span, not one per endset. The search iterates all query I-spans and unions matching link ISAs before intersection — so multi-I-span endsets are correctly found and aggregated. The `onlinklist` off-by-one is a latent deduplication bug that could produce duplicate entries in the per-endset result list in edge cases, but the final intersection still yields the correct set of matching links as long as duplicates don't suppress a needed entry.

---

## Question 19 [gregory]

> When `FOLLOWLINK` / `RETRIEVEENDSETS` returns a link's endsets and some referenced I-addresses exist in no current POOM, what exactly does `span2spanset` do during I→V conversion — does it silently drop the unreachable portions and return a truncated specset, or does it signal incompleteness?

### Gregory's Answer

## KB Synthesis

`span2spanset` silently drops unreachable portions and returns a truncated specset with no signal of incompleteness.

The mechanism is documented in [SS-FOLLOWLINK] / [INV-ITOV-FILTERING] (Finding 0048):

> `span2spanset()` uses `retrieverestricted()` against the document's orgl. If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is **silently dropped** — no V-span is added to the result.

Code reference: `backend/orglinks.c:425-449`, lines 446-448.

This behavior is universal across all I→V conversion paths. [INV-ITOV-FILTERING] states it as a system-wide invariant:

> Unreferenced I-addresses are silently excluded from V-address results. No operation that performs I→V conversion will ever return a V-address for an unreferenced I-address.

The three observable outcome cases from [EC-GHOST-LINK] are:

| Endset state | Result |
|---|---|
| All I-addresses have POOM mappings | Full specset |
| Some I-addresses unreachable | Partial specset (live ones only) |
| All I-addresses unreachable | Empty `[]` — operation still returns success |

In no case does the operation signal incompleteness to the caller. A caller receiving a partial or empty result from FOLLOWLINK/RETRIEVEENDSETS cannot distinguish "the endset genuinely covers only this content" from "some content exists in I-space but has no current V-position mapping."

The formal invariant is: `result(op) ⊆ { v | ∃ i : poom.d(v) = i }` — results are always a subset of currently-mapped V-positions. There is no "truncation flag" or error code. Completeness verification requires the caller to independently check whether the returned specsets cover all expected I-address ranges, which requires knowledge of what those ranges should be.

---

## Code Exploration

Now I have everything I need. Let me trace the complete execution chain for both operations.

---

## Answer: What `span2spanset` Does When I-Addresses Are Unreachable

The answer is **silent drop with no incompleteness signal**. Here is the complete traced path.

---

### Call Chain: FOLLOWLINK

```
fns.c:followlink
  → dofollowlink [do1.c:223]
      → link2sporglset [sporgl.c:67]         # reads I-spans from link POOM
      → linksporglset2specset [sporgl.c:97]
          → linksporglset2vspec [sporgl.c:127]
              → sporglset2vspanset [sporgl.c:141]
                  → ispan2vspanset [orglinks.c:389]
                      → permute [orglinks.c:404]
                          → span2spanset [orglinks.c:425]   ← KEY FUNCTION
```

### Call Chain: RETRIEVEENDSETS

```
fns.c:retrieveendsets
  → doretrieveendsets [do1.c:369]
      → retrieveendsetsfromspanf [spanf1.c:190]
          → retrievesporglsetinrange [spanf1.c:237]     # reads from spanfilade
          → linksporglset2specset [sporgl.c:97]
              → linksporglset2vspec [sporgl.c:127]
                  → sporglset2vspanset [sporgl.c:141]
                      → ispan2vspanset [orglinks.c:389]
                          → permute [orglinks.c:404]
                              → span2spanset [orglinks.c:425]   ← SAME KEY FUNCTION
```

Both paths converge on the same I→V conversion machinery.

---

### The Critical Function: `span2spanset` [orglinks.c:425–454]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
                          INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
    typecontext *context, *c, *retrieverestricted();
    typespan foundspan;
    typespan *nextptr;

    context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                                 (typespan*)NULL, targindex, (typeisa*)NULL);

    for (c = context; c; c = c->nextcontext) {
        context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
        nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
    }
    if(!context){
        return(targspansetptr);   // ← returns unchanged pointer, no error
    }
    contextfree (context);
    return (&nextptr->next);
}
```

The function calls `retrieverestricted` on the link's POOM (ORGL), restricted to the I-span in question, asking for V-dimension output.

---

### What `retrieverestricted` Returns for Unmapped I-Addresses

`retrieverestricted` [retrie.c:56–85] delegates to `retrieveinarea` → `findcbcinarea2d` [retrie.c:229–268]:

```c
int findcbcinarea2d(..., typecontext **headptr, ...) {
    for (; crumptr; crumptr = getrightbro(crumptr)) {
        if (!crumqualifies2d(...)) {
            continue;                // skip non-intersecting crums
        }
        if (crumptr->height != 0) {
            findcbcinarea2d(findleftson(...), ...);   // recurse
        } else {
            context = makecontextfromcbc(...);
            incontextlistnd(headptr, context, index1);  // only appended when found
        }
    }
}
```

`headptr` is initialized to `NULL` before the call [retrie.c:93]. If no POOM crum has an I-coordinate range overlapping the queried I-span, **no `incontextlistnd` call ever fires** and `headptr` stays NULL. `retrieverestricted` returns NULL.

---

### What Happens Back in `span2spanset` When Context Is NULL

```c
context = retrieverestricted(...);        // returns NULL — I-span has no V-mapping

for (c = context; c; c = c->nextcontext) {  // loop body never executes
    ...
}
if(!context){
    return(targspansetptr);   // ← returns the UNMODIFIED output list pointer
}
```

`targspansetptr` is returned without any new span appended. **No V-span is added for the unreachable portion. No error is raised.**

---

### What Happens Further Up the Chain

**`permute` [orglinks.c:404–422]** iterates over all input I-spans and calls `span2spanset` for each. Spans that map to nothing are silently skipped. The final return value is `save` — the original head of the output list:

```c
typespanset *permute(...) {
    save = targspansetptr;
    for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
        targspansetptr = span2spanset(...);  // may add nothing for this span
    }
    return (save);   // may be partially or fully empty
}
```

**`sporglset2vspanset` [sporgl.c:141–176]** does not check whether `ispan2vspanset` added anything:

```c
vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);  // return ignored
```

**`linksporglset2vspec` [sporgl.c:127–137]** initializes `vspanset` to NULL, then calls `sporglset2vspanset`. If the I→V conversion finds nothing, the field stays NULL and no error is raised:

```c
specptr->vspanset = NULL;
sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
// specptr->vspanset may remain NULL — no check
```

**`linksporglset2specset` [sporgl.c:97–123]** always returns TRUE regardless of whether the conversion produced any V-addresses:

```c
bool linksporglset2specset(...) {
    *specsetptr = NULL;
    for (; sporglset; ...) {
        specset = taskalloc(..., sizeof(typevspec));
        ...
        linksporglset2vspec(...);    // may produce empty vspanset
        ...
        *specsetptr = specset;       // the shell VSPEC is installed anyway
        ...
    }
    return (TRUE);   // always TRUE
}
```

**`retrieveendsetsfromspanf` [spanf1.c:190–235]** and **`dofollowlink` [do1.c:223–232]** both propagate a TRUE success status unconditionally when the structural operations succeed, regardless of whether the resulting specsets are empty.

---

### Conclusion: Silent Drop, No Incompleteness Signal

When `span2spanset` encounters I-addresses that have no V-mapping in the POOM:

1. **`retrieverestricted` returns NULL** — the 2D tree search finds no qualifying crums [retrie.c:93, 97, 107].
2. **`span2spanset` returns `targspansetptr` unchanged** [orglinks.c:446–448] — the `if(!context)` guard exits with no entries added, no error.
3. **`permute` returns a partially or fully empty V-span set** [orglinks.c:421] — missing I-spans silently produce no output.
4. **`linksporglset2vspec` leaves `vspanset = NULL`** [sporgl.c:135] if nothing mapped.
5. **`linksporglset2specset` returns TRUE** [sporgl.c:122] with a VSPEC shell whose `vspanset` is NULL.
6. **The top-level FOLLOWLINK/RETRIEVEENDSETS handlers report success** — `putfollowlink` / `putretrieveendsets` are called with a specset that may contain endset entries with empty vspansets [fns.c:124, fns.c:358].

There is **no error code, no partial-result flag, no callback, and no way for the caller to distinguish** "this I-span had a V-mapping that was returned" from "this I-span had no V-mapping and was silently dropped." The returned specset is simply truncated — shorter than what the stored I-spans would imply — with no annotation indicating the gap.

---

## Question 20 [gregory]

> Is there any mechanism that guarantees spanfilade completeness — that every link's endset I-spans are fully indexed — or can races, crashes, or partial `insertendsetsinspanf` failures leave a link permanently undiscoverable even though its orgl exists in the granfilade?

### Gregory's Answer

## KB Synthesis

## Spanfilade Completeness: No Guarantee Across Crashes

The KB gives a clear answer: **within a session, link creation is atomic, so no race can leave a link half-indexed; but crashes can produce a permanently undiscoverable link whose orgl exists in the granfilade.**

---

### What prevents races

The event loop is strictly single-threaded and run-to-completion [INV-ATOMICITY, INV-SEQUENTIAL-DISPATCH]. `docreatelink` executes its three steps — (1) create link orgl in granf, (2) insert link reference in document's 2.x POOM, (3) call `insertendsetsinspanf` — as a single uninterruptible unit before `select()` is re-entered [ST-CREATE-LINK, SS-GRANF-OPERATIONS]. No other FEBE operation can interleave. So in-memory state is always consistent after link creation completes.

---

### What the KB says about crash consistency

**Durability is session-level, not operation-level** [SS-DURABILITY-BOUNDARY, INV-DURABILITY-BOUNDARY]. After a crash, only crums previously evicted by the grim reaper survive. Recent in-memory state is lost. If the crash occurs before any crum is evicted:

- All three link-creation changes are lost together — no inconsistency, the link simply never happened from the disk's perspective.

But the grim reaper complicates things. It evicts crums based on age across all enfilades indiscriminately [SS-CACHE-MECHANISM, INT-CROSS-ENFILADE-EVICTION]:

> "Memory pressure from one subsystem (e.g., a large link search loading many spanfilade crums) can evict modified crums from another subsystem (e.g., recently inserted text atoms)."

This means a granf crum containing the link orgl could be evicted and written to disk while the corresponding spanf crum (holding the endset index) has not yet been evicted. A crash at that point leaves the link orgl on disk but the endset indexing absent.

**`writeenfilades()` on clean exit introduces the same gap** [EC-CRASH-MID-WRITE]:

> "A crash between these two writes leaves the granfilade updated but the spanfilade stale — violating the cross-enfilade consistency invariant."

The function writes granf root then spanf root sequentially, with no atomic commit.

---

### The KB's explicit acknowledgment

[INV-DUAL-ENFILADE-CONSISTENCY] states directly:

> "there is no transactional mechanism documented — if the sequence is interrupted partway, the enfilades can desynchronize."

The resulting state matches a **reverse orphan** [EC-REVERSE-ORPHAN]: the link orgl is accessible directly by link ID via `follow_link` (because I-space is intact), but `find_links` cannot discover it (because the spanf index entry is missing). Unlike a standard reverse orphan created by `DELETEVSPAN(2.x)`, this one cannot be fixed by normal operations — there is no `insertspanf` that a caller can invoke to repair the index.

---

### Summary

| Threat | Protected? | Mechanism |
|--------|-----------|-----------|
| Race between sessions | Yes | Single-threaded event loop [INV-SEQUENTIAL-DISPATCH] |
| Partial `insertendsetsinspanf` within a session | Yes | Run-to-completion atomicity [INV-ATOMICITY] |
| Grim reaper evicting granf before spanf | **No** | Shared age-based eviction, no cross-enfilade ordering [INT-CROSS-ENFILADE-EVICTION] |
| Crash between granf/spanf writes at exit | **No** | Sequential writes, no fsync, no transaction log [EC-CRASH-MID-WRITE] |

There is no mechanism — no write ordering, no journal, no checksum, no startup validation [EC-NO-STARTUP-VALIDATION] — that guarantees spanfilade completeness after a crash. A link can exist permanently in the granfilade yet be undiscoverable via content-identity search.

---

## Code Exploration

Now I have everything I need for a complete answer.

---

## Spanfilade Completeness: No Guarantee

There is no mechanism in udanax-green that guarantees every link's endset I-spans are fully indexed in the spanfilade. Multiple distinct failure paths can permanently leave a link's orgl in the granfilade with no corresponding spanfilade entries, making it undiscoverable via `findlinksfromtothreesp`.

---

### The `docreatelink` Call Sequence

The authoritative entry point is `docreatelink` in `do1.c:195-221`:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr, ...)
{
    makehint (DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf (taskptr, granf, &hint, linkisaptr)   // 1. Creates orgl in granfilade
      && tumbler2spanset (...)
      && findnextlinkvsa (...)
      && docopy (...)                                             // 4. Copies link ISA into doc POOM
      && findorgl (...)
      && specset2sporglset (x3)
      && setlinkvsas (...)
      && insertendsetsinorgl (...)                               // 8. Endsets into link's own orgl
      && insertendsetsinspanf (...)                              // 9. Endsets indexed in spanfilade
    );
}
```

Step 1 (`createorglingranf`) and step 9 (`insertendsetsinspanf`) are separated by seven independent operations. There is no rollback if anything between them fails.

---

### Failure Mode 1: `insertspanf` Always Returns TRUE

`insertspanf` at `spanf1.c:51` calls `insertnd` but **discards its return value**:

```c
// spanf1.c:51
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

Then at `spanf1.c:53`:

```c
return (TRUE);
```

This is unconditional. `insertspanf` always returns `TRUE` regardless of whether `insertnd` actually succeeded. `insertendsetsinspanf` (`do2.c:116-128`) therefore cannot detect a failed index insertion:

```c
bool insertendsetsinspanf(...){
    bool insertspanf();
    if (!(
        insertspanf(taskptr,spanfptr,linkisaptr,fromsporglset,LINKFROMSPAN)   // always TRUE
        && insertspanf(taskptr,spanfptr,linkisaptr,tosporglset,LINKTOSPAN)))  // always TRUE
        return (FALSE);   // unreachable via normal control flow
    ...
    return(TRUE);
}
```

If `insertnd` silently fails inside any of those three `insertspanf` calls, `docreatelink` returns `TRUE` to its caller, the FEBE layer sends success to the client, but some or all of the endset I-spans are not indexed.

---

### Failure Mode 2: Partial `insertendsetsinspanf` via Abort

`qerror` is defined in `genf.c:546-551`:

```c
INT qerror(char *message)
{
    fprintf (stderr, "Error: %s\n",message);
    abort();        // genf.c:549 — terminates immediately
    return(1);
}
```

And `gerror` is a macro alias: `common.h:119: #define gerror(s) qerror(s)`.

Every disk error path (`disk.c:221`, `disk.c:334`) and enfilade integrity check calls `qerror`, which calls `abort()`. If this fires during the first of the three `insertspanf` calls (e.g., LINKFROMSPAN written, LINKTOSPAN not yet started), the process dies instantly without calling `writeenfilades`. The in-memory state is lost — **but so was any chance of rollback**. Whether this leaves the on-disk state corrupted depends on whether `writeenfilades` had been called before the abort:

- If the in-memory dirty state was not yet flushed: consistent loss (both granf and spanf at their last clean state).
- If `writeenfilades` was in progress at the time of abort: see Failure Mode 3.

---

### Failure Mode 3: Crash During `writeenfilades`

`writeenfilades` at `corediskout.c:68-88` writes granfilade and spanfilade **sequentially** to two fixed disk locations:

```c
int writeenfilades(void)
{
    temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
    ...
    orglwrite (&temporgl);   // corediskout.c:79 — writes granfilade to disk

    temporgl.cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
    ...
    orglwrite (&temporgl);   // corediskout.c:87 — writes spanfilade to disk
}
```

`GRANFDISKLOCATION` and `SPANFDISKLOCATION` are separate fixed block positions (`coredisk.h:119-120`). There is no atomicity between these two `orglwrite` calls — no shadow paging, no WAL, no atomic rename.

If a signal arrives between line 79 and line 87 (e.g., SIGHUP triggers `crash()` at `socketbe.c:186-194`), the crash handler does:

```c
void crash(int signum)
{
    for (i = 0; i < 32; i++)
        close(i);   // socketbe.c:191 — no writeenfilades
    exit(9);        // socketbe.c:193
}
```

On restart, `initkluge` at `corediskin.c:18-41` reads both structures back from their fixed locations:

```c
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = GRANFDISKLOCATION;
inorgl (tempcbc);   // reads granfilade — newer version, with link orgl
...
tempcbc->cinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = SPANFDISKLOCATION;
inorgl (tempcbc);   // reads spanfilade — older version, without endset entries
```

**Result**: The granfilade contains the link's orgl. The spanfilade has no entries for its endsets. The link is permanently undiscoverable. There is no cross-validation step in `initkluge` and no repair scan anywhere in the codebase.

---

### Failure Mode 4: Mid-Sequence `docreatelink` Failure

If any step between `createorglingranf` (step 1) and `insertendsetsinspanf` (step 9) returns FALSE — e.g., `specset2sporglset` fails — `docreatelink` returns FALSE and `fns.c:111` calls `putrequestfailed`. The client is told the operation failed. But the in-memory granfilade has already been modified by `createorglingranf`. On the next `writeenfilades`, the orphan link orgl is flushed to disk with no spanfilade entries.

There is no compensating step, no orgl deletion on failure, no task-scoped rollback.

---

### No Recovery Mechanism

The persistence model (`disk.c`) uses raw `lseek`/`write` to `enf.enf`:

```c
// disk.c:328-334
if (lseek (enffiledes, (long) diskblocknumber*NUMBYTESINLOAF, 0) < 0) { ... }
if (write (enffiledes, (char*)loafptr, sizeof(*loafptr)) <= 0) { ... }
```

There is no write-ahead log, no journal, no fsync ordering guarantee, and no shadow copy with atomic rename. `diskflush` (`corediskout.c:58-64`) simply calls `writeenfilades` and re-initializes the in-core tree; it does not provide any transactional guarantee.

The `cashedisk.c` hash cache is compiled but disabled — `writethruhash` is commented out in `disk.c:305`:

```c
/**writethruhash(loafptr,diskblocknumber);*/   // disk.c:305
```

---

### Summary Table

| Failure Scenario | Granfilade State | Spanfilade State | Outcome |
|---|---|---|---|
| `insertnd` fails silently inside `insertspanf` | Link orgl present | Endset(s) not indexed | Link permanently undiscoverable; `docreatelink` returns TRUE |
| `qerror`/`abort()` during `insertendsetsinspanf` | Dirty in memory | Dirty in memory | Both lost if abort before flush; consistent but data lost |
| Crash between `orglwrite(granf)` and `orglwrite(spanf)` in `writeenfilades` | Flushed to disk (new) | Not flushed (old) | Permanent orgl/spanf divergence after restart |
| `docreatelink` fails mid-chain after `createorglingranf` | Orphan orgl in memory → flushed on next `writeenfilades` | No entries | Link permanently undiscoverable |
| Clean process crash (SIGPIPE) before any `writeenfilades` | At last clean checkpoint | At last clean checkpoint | Consistent; session changes lost but no divergence |

**Conclusion**: The spanfilade can be left permanently incomplete by any of the above paths. The most structurally concerning is the unconditional `return (TRUE)` in `insertspanf` (`spanf1.c:53`), which severs the error-propagation chain entirely and makes silent spanfilade omissions invisible to all callers. The sequential (non-atomic) write of the two enfilades in `writeenfilades` (`corediskout.c:79,87`) provides the second structural gap that a mid-flush crash exploits to create permanent orgl/spanf divergence.
