## Question 6 [nelson]

> Can the existence of a link be concealed from a user who has permission to view the referenced content but not the document that defines the link?

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
