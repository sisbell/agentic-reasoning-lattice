# Consultation Answers — Link Discovery

**Inquiry:** What guarantees must link discovery provide? If content A links to content B, under what conditions can B discover the link? What about transcluded content?
**Date:** 2026-02-23 18:22
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> If I create a link from my document to yours, must the system guarantee that you can discover that link exists?

### Nelson's Answer

# Yes — Bidirectional Link Discovery Is a Core Guarantee

Nelson is emphatic on this point. The system must allow anyone reading a document to discover all links pointing INTO it, not just the links going OUT from it. This is one of Xanadu's defining departures from conventional hyperlinks.

## The Explicit Promise

Nelson states the guarantee directly:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." [LM 2/46]

And for windowed (transcluded) content, he makes the bidirectionality explicit:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

## How It Works Architecturally

The FEBE protocol provides the operation `FINDLINKSFROMTOTHREE`, which searches links by constraining **any combination** of the three endsets:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

To discover links pointing at your document, you search with your document's address in the **to-set** parameter. The system indexes links by all three endsets, not just by their origin. Nelson guarantees this scales:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

## The In-Link / Out-Link Distinction

Nelson explicitly distinguishes the two directions and notes the ownership asymmetry:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

Your in-links are **not under your control** — they belong to whoever created them, at their addresses. But you **can discover them**. This is the other side of the link freedom coin:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

You relinquish control over in-links precisely because they are discoverable. If in-links were invisible to you, there would be nothing to relinquish.

## Filtering the Avalanche

Nelson anticipates that popular documents will accumulate vast numbers of in-links, and provides for filtering:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

He calls this "sieving" — narrowing the in-link results by attributes like location, author, and time.

## The Deeper Principle

Bidirectional discovery is not a convenience feature. It is what makes Xanadu's vision of literature as an interconnected system actually work. If you could create links but the target could never discover them, you would have the web — one-way links, no backlinks, the "backlinks problem" unsolved.

Nelson designed the system so that the web of connections IS the literature. Every link you make to my document becomes part of the discoverable context around my document. My readers can find your commentary, your citations, your refutations — all without my permission and without my ability to suppress them.

**In short:** Yes, the system guarantees in-link discovery. It is a structural property of the architecture, not an optional feature.

---

## Question 2 [nelson]

> Does the right to discover incoming links belong to the content owner, the content itself, or anyone who can read the content?

### Nelson's Answer

## Who Has the Right to Discover Incoming Links?

**Anyone who can read the content.** The right belongs to the reader, not the owner.

Nelson is consistent and explicit on this point. He frames incoming link discovery as a **reader's capability**, not an owner's privilege:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." [LM 2/46]

> "However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

The subject is always "the reader" — whoever is currently accessing the content.

### The Owner Explicitly Loses Control Over In-Links

Nelson draws a sharp line between out-links (owner-controlled) and in-links (not):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

And from the publication contract:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

The owner relinquishes control over incoming links at publication. This includes both the creation of those links and their discoverability.

### The FEBE Protocol Confirms This

The link search operation `FINDLINKSFROMTOTHREE` takes a home-set, from-set, to-set, and three-set as parameters — but no owner credential or access-control parameter:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

The search is constrained only by address ranges, not by identity. Anyone who can issue a FEBE request can search for links into any published content.

### The Access Boundary Is Readability, Not Ownership

The access model is binary: private documents are accessible "only by the owner and his or her associates," while published documents are "available to anyone" [LM 2/42]. So:

| Document State | Who Can Discover In-Links |
|---|---|
| **Published** | Anyone — all readers |
| **Private** | Owner and designees only (because they're the only readers) |

For published content, the right to discover incoming links is **universal**. For private content, it's restricted only because reading itself is restricted — not because link discovery has its own access layer.

### Why This Matters Architecturally

Nelson treats bidirectional link discovery as a **system property**, not a per-document policy:

> "Xanadu's three-endset structure with bidirectional indexing means EVERY link is discoverable from EITHER end (and from its type)."

The system indexes all links by all three endsets. Filtering is the reader's prerogative:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

The reader decides what to see. The system provides everything.

### Summary

The right to discover incoming links belongs to **anyone who can read the content**. For published documents, that means everyone. Nelson is unambiguous: the author relinquishes control over in-links at publication, the reader is the agent of discovery, and the protocol imposes no ownership check on link search. This is not a feature but a structural property of the docuverse — bidirectional discoverability is what makes Xanadu's link model fundamentally different from one-way hyperlinks.

---

## Question 3 [nelson]

> If content is transcluded from document A into document B, and someone links to that content in document B, must document A also be able to discover that link?

### Nelson's Answer

## Yes — and this is architecturally guaranteed, not optional.

The answer follows from three principles Nelson states explicitly:

### 1. Links attach to bytes (I-space), not positions (V-space)

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Links survive editing precisely because they bind to permanent I-space addresses, not ephemeral V-space positions. If links pointed to V-space, they would break on every edit.

### 2. Transcluded content shares I-space addresses with the source

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When document B transcludes content from document A, those bytes in B's V-stream are *the same I-space bytes* as in A. There is no copy — the V-to-I mapping in B points to A's I-space addresses.

### 3. Therefore: the link points to A's bytes regardless of where it was created

If someone creates a link to that content as it appears in document B, the link's endset resolves to I-space addresses that *are* A's content. The link doesn't know or care that the user was "looking at document B" when they created it. It's a strap attached to bytes — and those bytes are A's bytes.

When A's owner (or any reader of A) asks "What connects here from other documents?", the search matches on I-space addresses. The link made "to B's content" matches, because the I-space addresses are identical.

Nelson confirms this principle explicitly for the analogous case of **versions**:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Versions share I-space content the same way transclusions do. A link to content in version 2 is discoverable from version 1, because the I-space addresses are shared. The same logic applies to transclusion: a link to content transcluded into B is discoverable from A.

### The search mechanism confirms this

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

FINDLINKSFROMTOTHREE searches by span overlap. If you search for links to A's I-space address range, any link whose endset overlaps that range is returned — including links made via B's V-space that resolved to the same I-space addresses.

And FINDDOCSCONTAINING works the same way:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This operation explicitly crosses transclusion boundaries — it finds content wherever it appears, because it operates on I-space identity.

### What this means for users

Nelson's bidirectional discovery guarantee applies across transclusion:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

If you are reading document A, and someone linked to your content as it appeared in document B, you see that link. This is not a special feature — it falls out automatically from the fact that links bind to bytes and transclusion shares bytes.

### The deeper point

This is one of the properties that makes Xanadu fundamentally different from the web. On the web, linking to a quotation of content X is completely unrelated to linking to original content X — they're different URLs, different bytes, no connection. In Xanadu, they are *the same bytes*. A link to the quotation IS a link to the original. The web of connections grows automatically through transclusion, without anyone needing to maintain it.

---

## Question 4 [nelson]

> Can a link creator restrict the target from knowing the link exists, or must all links be discoverable by both endpoints?

### Nelson's Answer

## Links Must Be Discoverable By Both Endpoints

Nelson's design is unambiguous on this point for published content: **link creators cannot hide links from their targets.** Bidirectional discovery is a core architectural guarantee, not an optional feature.

### The Explicit Design

Nelson states the principle directly:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." [LM 2/46]

The windowing section reinforces this as a symmetric guarantee:

> "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

### The Two-Sided Coin

Nelson frames this as an inseparable bargain between link freedom and link visibility:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

The logic is explicit: you cannot have link freedom (anyone can link to anything) without link visibility (the target can discover all incoming links). One entails the other. The publication contract requires authors to accept both sides.

### The Search Mechanism Confirms This

The FEBE protocol's link search operates on all three endsets symmetrically:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

> "If the home-set is the whole docuverse, all links between these two elements are returned." [LM 4/63]

The system indexes links by **all** endsets. Alice can search for links TO her content across the entire docuverse. There is no mechanism described for a link creator to opt out of this indexing.

Nelson further guarantees that scale doesn't degrade this:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

### The Unspecified Edge Case: Private Documents

There is one genuine tension Nelson does not resolve. He states users can link "privately or publicly" [LM 2/43], and private documents are restricted:

> "A private document may be read and linked-to only by the owner and his or her associates." [LM 2/42]

If Bob creates a private document containing a link to Alice's published content, can Alice discover that link? Two principles collide:

- **Privacy**: "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]
- **Bidirectional discovery**: Alice should see "all these outside connections without appreciable delay." [LM 2/46]

Exposing that Bob's private document links to Alice reveals something about Bob's private document's contents. Nelson does not explicitly address this conflict. The publication contract's "relinquishment" language applies to the **target** author (accepting incoming links), not to the **link creator** (hiding outgoing links from private documents).

### Summary

| Scenario | Link discoverable by target? |
|----------|------------------------------|
| Published link → published content | **Yes** — explicitly required |
| Published link → private content | N/A — private content not accessible |
| Private link → published content | **Unspecified** — privacy vs. discovery tension |

For the core use case — published documents in the docuverse — the answer is clear: **all links are discoverable by both endpoints, and link creators have no mechanism to prevent this.** This is not incidental but foundational to Nelson's vision of literature as a self-organizing web of visible connections.

---

## Question 5 [nelson]

> When content has been linked to, must the system preserve the ability to discover that link permanently, or can link discovery expire?

### Nelson's Answer

## Link Discovery Must Be Permanent

Nelson's design requires that link discovery persist as long as the linked content exists. This follows from multiple interlocking principles.

### Links Are Permanent Content

Links are first-class objects in tumbler-space with their own permanent addresses. They are stored in I-space, subject to the same permanence guarantee as text bytes:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

A link is not metadata attached to a document — it is content owned by its creator, stored at a permanent location. The append-only storage model applies to links exactly as it applies to text.

### Permanence of Documents Depends on Discoverable Links

Nelson's argument for why published documents cannot be withdrawn is explicitly grounded in the links others have made to them:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

If link discovery could expire, the entire rationale for permanent publication collapses. The document stays published *because* links depend on it. If those links become undiscoverable, the permanence obligation loses its justification — and the links themselves lose their value.

### Bidirectional Discovery Is a Standing Capability

Nelson describes in-link discovery not as a time-limited service but as a permanent user capability:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

The FEBE protocol's link search operations (`FINDLINKSFROMTOTHREE`, `FINDNUMOFLINKSFROMTOTHREE`, `FINDNEXTNLINKSFROMTOTHREE`) take no expiration parameter. They search over specified regions of the docuverse with no temporal cutoff. And Nelson explicitly guarantees scalability of this search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This guarantee addresses the concern that accumulating links might make search impractical. Nelson's answer is not "old links expire" but "the search mechanism scales."

### Even Deleted Links Are Preserved

When a link owner explicitly deletes their own link, the system does not destroy it:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

If even *owner-deleted* links await historical backtrack rather than vanishing, then non-deleted links certainly cannot expire from discoverability.

### Time-Based Filtering Is User Choice, Not System Expiration

Nelson does mention time as a filtering attribute:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

But this is *sieving* — a user-directed narrowing of results for convenience. The links outside the filter still exist and remain discoverable. A user who asks "show me all links" gets all links, regardless of age.

### The One Genuine Constraint: Economic

The only mechanism by which link discovery could lapse is economic. Storage requires ongoing payment from the link's owner (the owner of the link's home document). Nelson states:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily." [LM 4/5]

If the owner of a link's home document stops paying storage rental, that document (and its links) might become inaccessible — not by design intent, but by economic failure. This is the same constraint that applies to all content. Nelson does not design expiration into the system; he acknowledges that perpetual storage has perpetual costs.

### Summary

Link discovery must be permanent. This is not stated as a single axiom but follows necessarily from:

1. Links are content with permanent tumbler addresses (permanence guarantee)
2. Document permanence is justified by the links pointing to them (circular dependency resolved by making both permanent)
3. Bidirectional link search is a standing FEBE capability with no expiration parameter
4. Even owner-deleted links are preserved for historical backtrack
5. The search mechanism is designed to scale with accumulating links, not to shed old ones

The system provides time-based *filtering* as a user convenience, but never time-based *expiration* as a system behavior. Link discovery can only lapse through economic failure (unpaid storage), which is a constraint on all content, not a designed feature of the link system.

---

## Question 6 [nelson]

> If a document has a thousand incoming links, must the system guarantee it can find all of them, or only those from published documents?

### Nelson's Answer

# Link Discovery: All or Only Published?

The system must guarantee it can find **all of them** — with the caveat that access control limits what any particular user can see.

## Nelson's Completeness Requirement

Nelson is explicit that link search must be comprehensive:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

The FINDLINKSFROMTOTHREE operation returns "a list of **all links** which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

When the home-set is the whole docuverse, "**all links** between these two elements are returned." [LM 4/63]

The user-facing expectation is equally unqualified:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown **all these outside connections** without appreciable delay." [LM 2/46]

There is no "up to a thousand" limit, no sampling, no best-effort. The system finds them all.

## The Privacy Qualification

However, Nelson's access model creates a necessary filter. Documents are either private or published:

> "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

A link stored in a private document is **part of that private document's contents**. Its home document determines ownership: "Its home document indicates who owns it, and not what it points to." [LM 4/12]

So: if Alice stores a link in her private document pointing to Bob's published document, that link is Alice's private content. Bob — and the general public — should not be able to discover it through link search, because discovering it would reveal information about Alice's private document.

Nelson does not explicitly address this intersection. He describes link search completeness and document privacy as separate concerns. But the principles compel the following conclusion:

## What the System Must Guarantee

For a document with a thousand incoming links:

| Link's home document | Who sees it in link search |
|---|---|
| Published | Everyone |
| Private (your own) | You |
| Private (another user's, you're a designee) | You |
| Private (another user's, you're not a designee) | Nobody except owner and designees |

The system guarantees **completeness within the user's access horizon**. It must find every link the querying user is authorized to see — all of them, not some of them. But it must not leak links from documents the user cannot access.

## Not a Practical Limitation for Published Literature

Nelson's vision centers on published literature. The publication contract explicitly requires:

> "each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

And anyone may link publicly:

> "each user is free to link to anything privately or publicly." [LM 2/43]

For the common case — published documents linked to by published links — the answer is simple: the system must find all thousand. The privacy qualification matters only for the subset of links stored in private documents, which by definition are not part of the public literature.

## Implementation Note

Nelson acknowledges that XU.87.1 did not implement private documents at all: "Private documents. (Currently all documents are visible to all users.)" [LM 4/79]. In that implementation, all links are visible to all users, making the question moot — the system finds all of them, period.

## Summary

The system must find **all** incoming links, not merely those from published documents. Nelson's language — "all links," "all these outside connections" — admits no partial discovery. The only constraint is access control: a user sees every link whose home document they are authorized to read. For the published docuverse, that means all of them.

---

## Question 7 [nelson]

> Does publication change what link discovery guarantees apply — can unpublished links to published content remain hidden?

### Nelson's Answer

# Publication Status and Link Discovery

Yes, publication status decisively affects link discovery. Unpublished links to published content remain hidden. This follows directly from three interacting principles in Nelson's design.

## Links Live in Documents; Documents Have Access Rules

Links are stored in their **home document**, and the home document determines both ownership and access:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it." [LM 2/31]

Documents are either private (owner and designees only) or published (anyone):

> "A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

If Alice's private document contains a link pointing to Bob's published document, that link is part of Alice's private document. Access rules for Alice's document govern visibility of the link.

## Nelson Explicitly Distinguishes Private and Public Linking

The critical sentence:

> "Each user is free to link to anything **privately or publicly**." [LM 2/43]

The word "privately" here is not incidental. It means: you can create links that only you (and your designees) can see. The link exists, but it is not discoverable by others. This is the direct mechanism for personal annotation — marginalia that remain yours until you choose to share them.

## Privacy Would Be Violated Otherwise

Nelson states a hard constraint on the system:

> "The network will not, may not monitor what is read or what is written in private documents." [LM 2/59]

If the system revealed to Bob's readers that Alice's private document contains links pointing to Bob's work, the system would effectively be disclosing what Alice has written in her private document. This violates the privacy guarantee.

## What Link Discovery Actually Promises

Nelson's discovery guarantee is:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?' — and be shown all these outside connections without appreciable delay." [LM 2/46]

The phrase "all these outside connections" must be read as **all accessible connections** — those in documents the querier has permission to see. The FEBE protocol's link search confirms this scoping:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The `home-set` parameter constrains which documents are searched for links. Access control filters what the querier can see within that set.

## The Publication Act Changes Visibility

When Alice **publishes** her document, her links become discoverable by everyone. This is a deliberate social act — the same "solemn event" Nelson describes for content publication applies to the links within that document. Before publication, Alice's annotations are private marginalia. After publication, they enter the shared web of connections.

This creates an asymmetry that is entirely intentional:

| Scenario | Bob's readers see Alice's links? |
|----------|----------------------------------|
| Alice's document is **private**, links point to Bob's published work | **No** — link hidden by access rules |
| Alice's document is **published**, links point to Bob's published work | **Yes** — fully discoverable |
| Alice designates Carol as associate | **Carol sees them**, others do not |

## Summary

Publication status of the **link's home document** — not the target document — determines discoverability. A private link to published content remains hidden from unauthorized users. This is not a gap or edge case; it is a direct consequence of three explicit design principles working together:

1. Links belong to their home document [LM 4/12]
2. Private documents are accessible only to owner and designees [LM 2/42]
3. The system may not disclose what is written in private documents [LM 2/59]

Nelson designed this deliberately. The ability to link "privately" [LM 2/43] is the mechanism for personal annotation — notes, bookmarks, working connections — that become social only when the author chooses to publish.

---

## Question 8 [nelson]

> If I transclude your content into my document and then someone links to that passage, who has the right to discover the link — you, me, or both?

### Nelson's Answer

## Both — and this falls out naturally from the architecture.

The answer requires tracing how links, transclusion, and I-space interact.

### Links attach to bytes, not positions

Links point to I-space addresses — the permanent identity of content, not its current arrangement in any document:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

### Transcluded bytes are logically present in both documents

When you transclude my content, my I-space bytes become part of your V-space arrangement. But they retain their I-space identity:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The bytes are **native** to my document and **logically part of** yours.

### Link discovery works through I-space

When Carol creates a link whose to-set points to that passage, the link's endset resolves to my I-space addresses — because that's where the bytes permanently live, regardless of which document's V-space they currently appear in.

**I discover the link** because searching for links to my I-space content finds it directly. The link's to-set matches my native byte addresses.

**You discover the link** because your front end resolves your V-space positions to the underlying I-space addresses, then searches for links to those addresses. Nelson's bidirectional discovery guarantee applies to any document position:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

The phrase "a given document or place in the document" includes transcluded content. The system doesn't distinguish between native and transcluded content for discovery purposes.

### The FINDDOCSCONTAINING operation confirms this

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

The system explicitly tracks which documents contain which I-space content. Both your document and mine contain the same bytes. Any link pointing to those bytes is discoverable from either document.

### Ownership is a separate question

Discovery and ownership are distinct:

- **Carol** owns the link (it lives at her address, in her home document)
- **Neither you nor I** can delete Carol's link — only Carol can
- **Both you and I** can discover it through link search

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

### Why this is architecturally inevitable

This isn't a special case requiring extra machinery. It falls out from three design choices:

1. Links attach to I-space bytes (survivability)
2. Transclusion shares I-space addresses (reference, not copy)
3. Link search matches on I-space spans (bidirectional discovery)

If links attached to V-space positions, they would break on editing and would only be discoverable from one document. By attaching to I-space, every document containing those bytes — whether as native content or as transclusion — sees the same links. The web of connections propagates through the web of shared content automatically.

This is one of the deepest consequences of the I-space/V-space separation. It means that linking to transcluded content simultaneously enriches every document that transcludes that content. The literature becomes, as Nelson intended, "socially self-constructing."

---

## Question 9 [nelson]

> Must the system guarantee that link discovery is complete — that every link to a piece of content is findable — or only that discovered links are genuine?

### Nelson's Answer

## Link Discovery: Completeness vs. Soundness

Nelson specifies **completeness as the intent** but acknowledges **practical limits** imposed by distribution. Soundness (genuineness) is architecturally guaranteed and never in question.

### The Completeness Intent

Nelson's protocol language is unambiguous. FINDLINKSFROMTOTHREE:

> "This returns a list of **all** links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The word "all" is a completeness claim. Similarly, the user-facing guarantee for in-link discovery:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'—and be shown **all these outside connections** without appreciable delay." [LM 2/46]

Nelson does not say "some" or "a sample of" or "those currently known." He says **all**.

### The Performance Guarantee Supports Completeness

The key search guarantee is about non-interference:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

This states that irrelevant links do not degrade search for relevant ones — a guarantee that only matters if the system is attempting to find **every** matching link. If the system only promised "some genuine results," there would be no need to guarantee that junk links don't slow the search down.

### Soundness Is Architectural, Not a Design Choice

Discovered links are guaranteed genuine by the addressing structure itself. Links are concrete objects in tumbler-space with their own permanent addresses. The search satisfaction model is well-defined:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

There is no mechanism by which the system could return a link that doesn't exist. Links are stored objects at real addresses — you either find them or you don't. False positives are structurally impossible.

### Distribution Creates Practical Incompleteness

Nelson simultaneously describes a distributed system where completeness is aspirational rather than absolute:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

Each server holds only a subset:

> "Each server contains a map and a subset of the whole—a microcosm that shrinks and grows." [LM 4/71]

And when the system cannot fully satisfy a request, Nelson acknowledges graceful degradation:

> "When the system can't fully satisfy a request, a Resource Unit (RU) becomes the user's friend—the back-end's sophisticated allocation system working on your behalf." [LM 4/59, paraphrased in curated source]

This implies the system **can** fail to return all matching links — not as a design feature, but as a transient network reality.

### The Distinction

| Property | Status | Basis |
|----------|--------|-------|
| **Soundness** (discovered links are genuine) | Architecturally guaranteed | Links are real objects at permanent addresses; no false-positive mechanism exists |
| **Completeness** (all matching links are discovered) | Specified as intent; subject to network reality | Protocol says "all"; distribution means "all currently reachable" |

Nelson designs for completeness — the protocol specifies it, the search guarantees assume it, the user-facing promise requires it. But the distributed architecture he describes cannot deliver it unconditionally when nodes are partitioned or unavailable.

### The Deeper Point

Nelson never frames this as a tradeoff. He does not say "we sacrifice completeness for performance" or "we only guarantee soundness." He designs a system that **should** return all links, builds data structures (enfilades) and protocols (BEBE forwarding, subrepresentation) to achieve this, and acknowledges that the network's inherent unreliability will sometimes prevent it.

The answer to your question: Nelson specifies **both**. Soundness is structural and unconditional. Completeness is specified as the requirement and designed for, but subject to the realities of distribution that Nelson himself identifies.

---

## Question 10 [nelson]

> When the same content appears in multiple documents through sharing, must a link targeting one appearance be discoverable from all appearances, or only the one explicitly targeted?

### Nelson's Answer

## All Appearances — Not Just the One Targeted

Nelson's architecture requires that a link targeting shared content be discoverable from **every document** containing that content, not only the document where the link was originally aimed. This follows from the intersection of several explicit design principles.

### The Core Mechanism: Links Attach to I-Space

Links do not point to documents or positions — they point to **bytes identified by their permanent I-space addresses**:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

When content is transcluded, it is not copied — the transclusion **shares the same I-addresses** as the original:

> "Transcluded content SHARES the same I-address. This is how the system distinguishes 'wrote the same words' from 'quoted from the original.'" (sporgl-provenance design intent, derived from 4/10-4/11)

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Since the link attaches to I-addresses, and transclusion means those same I-addresses appear in multiple documents, the link is structurally connected to the content everywhere it appears.

### Nelson States This Explicitly for Versions

For versions of the same document, Nelson is direct:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

The mechanism that makes this work is **shared I-space origin**. Versions share I-addresses because CREATENEWVERSION copies the V-space mapping, not the content. The same mechanism — shared I-addresses — is what makes transclusion work across different documents.

### The Search Protocol Confirms It

FINDLINKSFROMTOTHREE searches by address matching on endsets:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

The search matches on **address ranges**, not on document identity. If a link's to-set covers I-addresses 100–200, any search specifying those I-addresses will find the link — regardless of which document the searcher is browsing.

FINDDOCSCONTAINING makes the inverse direction explicit:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

The system can identify all documents sharing content. Combined with bidirectional link discovery, this means: from any appearance, you can find the content's I-addresses, then find all links to those addresses.

### Bidirectional Discovery Is a Stated Guarantee

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

Nelson does not qualify this with "only if the link was made to this particular document." The reader asks about **content at a place**, and the system returns connections. If the content at that place shares I-addresses with content elsewhere (via transclusion), the connections follow.

### The Practical Scenario

Suppose Alice writes a paragraph (I-addresses 100–200). Bob transcludes it into his document. Carol creates a comment link targeting Alice's paragraph (to-set: I-addresses 100–200).

A reader browsing Bob's document sees Alice's paragraph. They ask "What connects here?" The front end translates Bob's V-space positions into I-addresses (via the POOM mapping), discovers I-addresses 100–200, and searches for links to that range. Carol's comment link is found — because it targets those I-addresses, not "Alice's document specifically."

This is the whole point of I-space/V-space separation: links follow content identity, not document arrangement.

### What Nelson Does Not Address

Nelson does not explicitly walk through this cross-document transclusion scenario in a single passage. The answer is a logical consequence of:

1. Links attach to I-addresses [LM 4/42]
2. Transclusion shares I-addresses [LM 4/11]
3. Link search matches on addresses [LM 4/69]
4. Refractive following works across shared I-space [LM 2/26]
5. Bidirectional discovery is guaranteed [LM 2/46]

Each of these is explicitly stated. Their conjunction — that links are discoverable from all appearances of shared content — is architecturally necessary, even if Nelson never wrote "a link to transcluded content is visible from every document containing that transclusion" in those exact words.

---

## Question 11 [gregory]

> When `findlinksfromtothreesp` searches the spanfilade for links overlapping a given I-address range, does it require the query I-span to overlap the link's source endset, target endset, or type endset — or does overlap with ANY of the three endsets produce a match?

### Gregory's Answer

## KB Synthesis

From the KB, `findlinksfromtothreesp` searches each of the three endset types **separately** in distinct ORGLRANGE subspaces, then **intersects** the results.

## Endset-Type Specificity

[INT-SPORGL-LINK-INDEX] (Finding 0035) establishes that the three endset types are indexed as separate ORGLRANGE subspaces:
- `LINKFROMSPAN = 1` (source/FROM endset)
- `LINKTOSPAN = 2` (target/TO endset)
- `LINKTHREESPAN = 3` (type/THREE endset)

Each provided spec is searched **only against its corresponding endset subspace**. A `from_spec` matches links whose FROM endset overlaps the query I-addresses; it does not search TO or THREE endsets. The [SS-RETRIEVE-ENDSETS] entry confirms this: `retrieveendsetsfromspanf()` calls `retrievesporglsetinrange()` separately for each endset type with its own ORGLRANGE prefix.

## AND Semantics for Multiple Specs

When multiple specs are provided, the results are combined via intersection. [SS-FIND-LINKS] Finding 0029 makes this explicit:

> `find_links(source_spec, target_spec)` ≡ `find_links(source_spec) ∩ find_links(target_spec)`

The same finding's cross-endpoint search matrix confirms:
- Source deleted, target intact → search by source: **not found**; search by target: **found**
- This demonstrates each spec tests only its corresponding endset

[SS-FIND-LINKS] Finding 0035 further supports this: `intersectlinksets()` in `spanf2.c:46-120` is described as O(n×m) or O(n×m×p), the latter covering three-way intersection when all three specs are provided.

## Summary

`findlinksfromtothreesp` does **not** use OR semantics (overlap with ANY endset). Instead:

1. Each non-NOSPECS parameter is matched against its own indexed endset type in the spanfilade
2. Results from each matched endset type are intersected (AND semantics)
3. Passing NOSPECS for an endset type excludes it from intersection — that dimension imposes no constraint

So a link is returned only if its FROM endset overlaps the from_spec (when provided) **and** its TO endset overlaps the to_spec (when provided) **and** its THREE endset overlaps the three_spec (when provided).

## Code Exploration

Now I have everything I need. Let me put together the complete answer.

---

## Answer: How `findlinksfromtothreesp` Matches Links

**Short answer:** Overlap with ANY single endset does **not** produce a match on its own. The function performs **three independent, type-restricted searches** — one per endset — then returns their **intersection**. A link qualifies only if it satisfies **all specified endset constraints**.

---

### How Links Are Stored in the Spanfilade

`insertendsetsinspanf` [do2.c:116–128] calls `insertspanf` three times, once per endset:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // do2.c:119
insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,   LINKTOSPAN)     // do2.c:120
insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN) // do2.c:123
```

The constants are defined at [xanadu.h:36–38]:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
```

Inside `insertspanf` [spanf1.c:15–54], each endset member becomes a crum in the 2D spanfilade with:
- **SPANRANGE** = content address of the endset member (the I-span the link points into)
- **ORGLRANGE** = `prefixtumbler(linkISA, spantype)` — the link's own ISA prefixed by its endset type (1, 2, or 3)
- **ORGLRANGE width** = zero (`tumblerclear(&crumwidth.dsas[ORGLRANGE])`) [spanf1.c:23]

So the three endsets occupy **three distinct ORGLRANGE sectors**:
- FROM endsets live at ORGLRANGE `1.linkISA`
- TO endsets live at ORGLRANGE `2.linkISA`
- THREE endsets live at ORGLRANGE `3.linkISA`

---

### The Search: Three Independent Lookups

`findlinksfromtothreesp` [spanf1.c:56–103]:

```c
fromlinkset = tolinkset = threelinkset = NULL;     // spanf1.c:69
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)
    specset2sporglset(taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

if (fromvspecset) {
    sporglset2linkset(taskptr, spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return(TRUE); }     // spanf1.c:78–82
}
if (tovspecset) {
    sporglset2linkset(taskptr, spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return(TRUE); }       // spanf1.c:86–90
}
if (threevspecset) {
    sporglset2linkset(taskptr, spanfptr, threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return(TRUE); }    // spanf1.c:94–98
}
intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // spanf1.c:100
```

Each `sporglset2linkset` call passes a **different** `spantype`. Inside `sporglset2linksetinrange` [sporgl.c:256–262]:

```c
if (orglrange) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream);  // sporgl.c:257
    prefixtumbler(&orglrange->width,  0,        &range.width);   // sporgl.c:258
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, ...);         // sporgl.c:259
}
```

`prefixtumbler` [tumble.c:641–651] prepends `spantype` as the leading tumbler component. So:
- The FROM search queries ORGLRANGE sector `1.*` — **only FROM endset crums**
- The TO search queries ORGLRANGE sector `2.*` — **only TO endset crums**
- The THREE search queries ORGLRANGE sector `3.*` — **only THREE endset crums**

There is no cross-sector contamination. The SPANRANGE axis is the content overlap query; the ORGLRANGE axis is type-gated by the prefix.

---

### The Combination: Intersection, Not Union

`intersectlinksets` [spanf2.c:46–120] combines the three per-endset results:

```c
// If exactly ONE linkset is non-null, return it directly — no intersection needed
if (linkset1 && !linkset2 && !linkset3)  *linkset4ptr = linkset1;  // spanf2.c:64
else if (!linkset1 && linkset2 && !linkset3) *linkset4ptr = linkset2;  // spanf2.c:66
else if (!linkset1 && !linkset2 && linkset3) *linkset4ptr = linkset3;  // spanf2.c:68
else *linkset4ptr = NULL;

// Two non-null: pairwise intersection
for (; temp1; ...) for (temp2 = linkset2; ...) {
    if (tumblereq(&temp1->address, &temp2->address)) ...  // spanf2.c:98

// Three non-null: triple intersection
for (...) for (...) for (temp3 = linkset3; ...) {
    if (tumblereq(&temp1->address, &temp2->address)
     && tumblereq(&temp2->address, &temp3->address)) ...  // spanf2.c:109–110
```

A link appears in the output only if its ISA address is present in **every non-NULL** intermediate linkset.

---

### Early-Exit Semantics Make It Strict AND

There is also a fail-fast short-circuit [spanf1.c:78–98]: if any **specified** specset query returns zero links, the function **immediately** returns `NULL` without running the remaining queries. This means the function behaves as a logical AND across all specified constraints.

---

### Conclusion

`findlinksfromtothreesp` does **not** produce a match when a query I-span overlaps with ANY of the three endsets. Instead:

| Behavior | How it works |
|---|---|
| Each specset is searched in its own endset sector | `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN` prefix separates the sectors [xanadu.h:36–38, sporgl.c:257] |
| NULL specsets are simply skipped | Not treated as "match all" — they contribute no linkset [spanf1.c:70–99] |
| Non-NULL specsets are AND-ed together | `intersectlinksets` returns only links present in every non-NULL result [spanf2.c:64–118] |
| Any non-NULL specset that matches nothing short-circuits to empty | Early return at spanf1.c:79, 87, 95 |

To find links where **any** endset overlaps a given range, a caller would have to invoke `findlinksfromtothreesp` three separate times (once with only `fromvspecset` set, once with only `tovspecset`, once with only `threevspecset`) and merge the resulting linksets externally. The function itself has no union mode.

---

## Question 12 [gregory]

> The "three" in `FINDNEXTNLINKSFROMTOTHREE` takes three specset arguments — does each argument constrain a specific endset (source, target, type), and can any of the three be left empty to mean "unconstrained on this endset"?

### Gregory's Answer

## KB Synthesis

**Yes** to both parts, with an important caveat on the third argument.

## Three Specset Arguments: FROM, TO, THREE

Each argument constrains a distinct endset type, corresponding directly to the three ORGLRANGE subspaces in the spanfilade:

| Argument | Endset | ORGLRANGE constant |
|----------|--------|--------------------|
| First | Source (FROM) | LINKFROMSPAN = 1 |
| Second | Target (TO) | LINKTOSPAN = 2 |
| Third | Type (THREE) | LINKTHREESPAN = 3 |

[SS-RETRIEVE-ENDSETS]: RETRIEVEENDSETS searches the spanfilade using exactly these three ORGLRANGE prefixes independently.

## NOSPECS = Unconstrained on That Endset

Any of the three can be passed as NOSPECS (empty), meaning that endset is unconstrained. When NOSPECS is passed for an endset, the search is not restricted on that dimension. This is confirmed by [SS-FIND-LINKS] Finding 0005:

- `find_links(source_specs)` → finds by source only  
- `find_links(NOSPECS, target_specs)` → finds by target only  
- `find_links(source_specs, target_specs)` → must match both

## AND Semantics When Multiple Are Specified

When two or more non-empty specsets are provided, the system uses AND semantics — all specified endpoints must have V-stream presence for a link to be returned. [SS-FIND-LINKS] Finding 0029 gives the full matrix: deleting source content removes links from source-based search but target-based search still finds them. The `intersectlinksets()` call in `spanf2.c:46-120` implements this as set intersection across the results from each endset search. [SS-FIND-LINKS] Finding 0035.

## Critical Caveat: The Third Argument (Type) Is Broken

[EC-TYPE-FILTER-NONFUNCTIONAL] documents that type filtering via the third argument does not work:

> `find_links(source, NOSPECS, type_spec)` returns empty results even when unfiltered search finds links of those types.

This is a pre-existing bug. The type argument is accepted without error but produces empty results when used as a filter. All three arguments share the same `findlinksfromtothreesp()` call path, but the type endset filtering appears to be non-functional in practice.

Additionally, [EC-FIND-LINKS-GLOBAL] / [PRE-FIND-LINKS] Finding 0069 notes that the orgl-range (document scoping) parameter is also effectively ignored due to the `TRUE||!homeset` guard in `sporglset2linkset()` — but this is a separate issue from the from/to/three endset filtering, which does work for the first two arguments.

## Summary

- **First arg** (FROM/source): functional — constrains search to links whose source endset shares I-addresses with the specset
- **Second arg** (TO/target): functional — constrains search to links whose target endset shares I-addresses with the specset  
- **Third arg** (THREE/type): accepted but non-functional — always returns empty when used as a filter
- **NOSPECS** for any arg: unconstrained on that endset
- **Multiple non-NOSPECS args**: AND semantics via `intersectlinksets()`

## Code Exploration

I now have all the source I need. Here is the complete answer.

---

## `FINDNEXTNLINKSFROMTOTHREE`: Three Arguments, Three Endsets

### 1. Yes — each argument constrains exactly one endset

The three specset parameters map one-to-one onto the three link endsets. The names are consistent across every layer of the code:

```
fromvspecset   →  FROM endset   →  LINKFROMSPAN = 1   [xanadu.h:36]
tovspecset     →  TO endset     →  LINKTOSPAN   = 2   [xanadu.h:37]
threevspecset  →  THREE endset  →  LINKTHREESPAN = 3  [xanadu.h:38]
```

This mapping is explicit in `fns.c:219-234`:
```c
void findnextnlinksfromtothree(typetask *taskptr)
{
  typespecset fromvspecset, tovspecset, threevspecset;
  ...
  getfindnextnlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, ...)
  && dofindnextnlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset, ...)
```

The wire parser in `get1fe.c:115-121` reads them in the same order:
```c
bool getfindnextnlinksfromtothree(...)
{
  return
     getfindlinksfromtothree (taskptr, fromvspecsetptr, tovspecsetptr, threevspecsetptr, homesetptr)
  && gettumbler (taskptr, lastlinkptr)
  && getnumber (taskptr, nptr);
}
```

And `getfindlinksfromtothree` at `get1fe.c:104-113` calls `getspecset` three times, once per endset constraint, in from/to/three order.

---

### 2. Yes — any or all three can be empty (NULL) to mean "unconstrained on this endset"

The core search function is `findlinksfromtothreesp` in `spanf1.c:56-103`. Every specset is guarded by a pointer check before it is used:

```c
fromlinkset = tolinkset = threelinkset = NULL;        // spanf1.c:69

if (fromvspecset)                                      // spanf1.c:70
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
if (tovspecset)                                        // spanf1.c:72
    specset2sporglset (taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
if (threevspecset)                                     // spanf1.c:74
    specset2sporglset (taskptr, threevspecset, &threesporglset, NOBERTREQUIRED);

if (fromvspecset) {                                    // spanf1.c:76
    sporglset2linkset (..., fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
    if (!fromlinkset) { *linksetptr = NULL; return (TRUE); }
}
if (tovspecset) {                                      // spanf1.c:84
    sporglset2linkset (..., tosporglset, &tolinkset, orglrange, LINKTOSPAN);
    if (!tolinkset) { *linksetptr = NULL; return (TRUE); }
}
if (threevspecset) {                                   // spanf1.c:92
    sporglset2linkset (..., threesporglset, &threelinkset, orglrange, LINKTHREESPAN);
    if (!threelinkset) { *linksetptr = NULL; return (TRUE); }
}

intersectlinksets(taskptr, fromlinkset, tolinkset, threelinkset, linksetptr);  // spanf1.c:100
```

A NULL specset skips both the `specset2sporglset` conversion and the `sporglset2linkset` spanfilade lookup entirely. The corresponding link set stays NULL.

Then `intersectlinksets` (`spanf2.c:63-79`) treats a NULL link set as "not a constraint" — it uses whichever non-NULL link sets are present:

```c
/* If only one linkset is non-null, then just use it */
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;
else if (!linkset1 && linkset2 && !linkset3)
    *linkset4ptr = linkset2;
else if (!linkset1 && !linkset2 && linkset3)
    *linkset4ptr = linkset3;
else
    *linkset4ptr = NULL;
```

So with two active constraints the full three-way (or two-way) intersection is computed; with only one active constraint that link set is returned directly.

**How to send an empty specset on the wire:** `getspecset` (`get2fe.c:147-159`) reads a count first. If the count is `0`, it sets `*specsetptr = NULL` and returns `TRUE` immediately. Sending `0~` for any of the three specset arguments produces a NULL pointer, which the backend treats as "unconstrained on this endset."

---

### 3. Important edge case: leaving ALL THREE empty yields an empty result, not "all links"

If all three specsets are NULL, no spanfilade lookup runs at all. All three link sets stay NULL. Then `intersectlinksets` falls through to:
```c
else
    *linkset4ptr = NULL;   // spanf2.c:71
```

The result is an empty link set, not "every link in the system." The operation requires at least one constraint to produce any output.

---

### 4. Bonus: `FINDNEXTNLINKSFROMTOTHREE` is disabled in safe mode

`init.c:71-76` shows that when the backend starts with `safe=TRUE`, `FINDNEXTNLINKSFROMTOTHREE` (and `FINDNUMOFLINKSFROMTOTHREE`) are replaced by `nullfun`, which immediately returns `REQUESTFAILED`:

```c
if (safe) {
    requestfns[SOURCEUNIXCOMMAND] = nullfun;
    requestfns[NAVIGATEONHT] = nullfun;
    requestfns[FINDNUMOFLINKSFROMTOTHREE] = nullfun;
    requestfns[FINDNEXTNLINKSFROMTOTHREE] = nullfun;   // init.c:75
}
```

Notably, `FINDLINKSFROMTOTHREE` (request 30) is **not** disabled in safe mode — only its counted/paginated variants are.

---

### Summary

| Argument | Endset | Constant | NULL means |
|---|---|---|---|
| `fromvspecset` | FROM | `LINKFROMSPAN = 1` | Skip from-endset constraint |
| `tovspecset` | TO | `LINKTOSPAN = 2` | Skip to-endset constraint |
| `threevspecset` | THREE | `LINKTHREESPAN = 3` | Skip three-endset constraint |

Yes, any of the three can be left empty (sent as count `0` on the wire) to make that endset unconstrained. The active constraints are intersected; inactive ones are ignored. Leaving all three empty returns an empty result, not the full link universe.

---

## Question 13 [gregory]

> When a link's source endset spans I-addresses `[.0.1.3, .0.1.7]` and only bytes `.0.1.5` through `.0.1.7` remain in any POOM after partial deletion, does `find_links` still discover the link through the surviving partial overlap, or does it require full endset coverage?

### Gregory's Answer

## KB Synthesis

**Yes, partial overlap is sufficient. The link will be discovered.**

## Mechanism

`find_links` operates by converting the query specset to I-addresses (via the current POOM state), then searching the spanfilade for intersection. The defining rule [ST-FIND-LINKS]:

> `find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`

Partial overlap suffices — even a single shared I-address is enough. The concrete example in [ST-FIND-LINKS] (Finding 0028b §2) demonstrates this directly: a document containing only "EF" (I-addresses I.5, I.6) discovers a link whose source endpoint spans "DEF" (I-addresses I.4, I.5, I.6), because `{I.5, I.6} ∩ {I.4, I.5, I.6} ≠ ∅`.

## Applied to Your Scenario

- Link source endset: I-addresses `[.0.1.3, .0.1.7]` (5 bytes)
- Surviving POOM content: `.0.1.5` through `.0.1.7`
- Search I-addresses derived from POOM: `{.0.1.5, .0.1.6, .0.1.7}`
- Intersection: `{.0.1.5, .0.1.6, .0.1.7} ∩ {.0.1.3, ..., .0.1.7}` = non-empty → **link returned**

## Why the Spanfilade Preserves Discoverability

The spanfilade entry indexing the link's full range `[.0.1.3, .0.1.7]` is **never modified by DELETE**. The spanfilade is write-only [INV-SPANF-WRITE-ONLY] — no operation removes entries from it. DELETE modifies only the POOM (removing I-address mappings from V-space), not the spanfilade index. So the link remains indexed at all five I-addresses regardless of deletions [INT-DELETE-SPANF-DIVERGENCE].

## Consistent with Partial-Deletion Behavior

This is confirmed explicitly in [PRE-FIND-LINKS] (Finding 0029, sections 1, 3, 8):

> "Partial delete is tolerated — as long as any portion of the original linked span remains, the link is discoverable."

And in [INV-LINK-CONTENT-TRACKING] (Finding 0019):

> "Partial deletion shrinks endsets: When part of a linked region is deleted, the link shrinks to cover only the surviving content"

So `find_links` discovers the link; `follow_link(link, SOURCE)` subsequently returns only the surviving portion — the endset V-address spans correspond to whichever of `.0.1.5–.0.1.7` currently has POOM mappings, not the original `.0.1.3–.0.1.7`.

## What Would Break Discovery

Discovery fails only when **all** endset I-addresses are removed from every POOM — i.e., when none of `.0.1.3` through `.0.1.7` appear in any document's POOM. In that case the query produces an empty I-address set, and the intersection is empty [EC-ORPHANED-LINK].

## Code Exploration

I now have everything needed. Let me trace the complete execution path and write the answer.

---

## Answer

**`find_links` discovers the link through the surviving partial overlap. It does not require full endset coverage.**

Here is the full code trace, with every claim cited.

---

### 1. How the endset is indexed at link creation

`docreatelink` [`do1.c:195`] converts the from-endset V-spec to an I-sporglset and writes it into the spanfilade:

```c
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

`insertendsetsinspanf` [`do2.c:116`] calls `insertspanf` for each endset type:

```c
insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)
```

`insertspanf` [`spanf1.c:15`] inserts a 2D crum into the spanfilade:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // I-address of endset content
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```

For a from-endset spanning I-addresses `.0.1.3` to `.0.1.7`, the spanfilade stores a crum whose **SPANRANGE = \[.0.1.3, .0.1.7)** and **ORGLRANGE = link ISA prefixed with `LINKFROMSPAN`**. That entry persists permanently.

---

### 2. Deletion does NOT touch the spanfilade

`dodeletevspan` [`do1.c:158`]:

```c
return (
   findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
&& deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
/* ht stuff */ );
```

`deletevspanpm` [`orglinks.c:145`]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` operates on the **POOM** (the document's V→I mapping tree). There is no call to `insertspanf`, no call to `deletend` on `spanf`, no spanfilade write of any kind. After deleting bytes `.0.1.3`–`.0.1.5` from the POOM, the spanfilade crum for the link's from-endset still records SPANRANGE = **\[.0.1.3, .0.1.7)** unchanged.

---

### 3. The find_links call chain

`findlinksfromtothree` [`fns.c:189`] → `dofindlinksfromtothree` [`do1.c:348`]:

```c
bool dofindlinksfromtothree(...) {
    return findlinksfromtothreesp(taskptr, spanf, fromvspecset, ...);
}
```

`findlinksfromtothreesp` [`spanf1.c:56`]:

```c
if (fromvspecset)
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
...
sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                   orglrange, LINKFROMSPAN);
```

`specset2sporglset` [`sporgl.c:14`] converts the V-spec query through the POOM (via `vspanset2sporglset` → `vspanset2ispanset`). If the query addresses the surviving bytes at whatever V-position they now occupy, this produces an **I-sporgl with origin `.0.1.5`, width 2** (i.e., I-span `[.0.1.5, .0.1.7)`).

`sporglset2linkset` [`sporgl.c:222`] → `sporglset2linksetinrange` [`sporgl.c:239`]:

```c
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                              &range, ORGLRANGE, (typeisa*)infoptr);
```

Here `span1` = the query I-sporgl `[.0.1.5, .0.1.7)`.

---

### 4. The overlap test — the critical code

`retrieverestricted` [`retrie.c:56`] computes `span1end = span1start + span1ptr->width`:

```c
movetumbler (&span1ptr->stream, &span1start);       // .0.1.5
tumbleradd (&span1start, &span1ptr->width, &span1end); // .0.1.7
```

Then calls `retrieveinarea` → `findcbcinarea2d` → `crumqualifies2d` [`retrie.c:270`] for every crum candidate, including the one representing the stored endset `[.0.1.3, .0.1.7)`:

```c
endcmp = iszerotumbler (span1end) ? TOMYRIGHT
       : whereoncrum (crumptr, offset, span1end, index1);   // query end = .0.1.7
if ( endcmp <=/*=*/ ONMYLEFTBORDER){
    return(FALSE);
}
startcmp = whereoncrum (crumptr, offset, span1start, index1); // query start = .0.1.5
if( (startcmp > THRUME)){
    return (FALSE);
}
```

The position constants [`common.h:86-90`]:

```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
#define ONMYRIGHTBORDER 1
#define TOMYRIGHT       2
```

For the stored endset crum whose SPANRANGE left = `.0.1.3`, right = `.0.1.7`:

| Query point | `whereoncrum` result | Value |
|---|---|---|
| `.0.1.7` (query end == crum right) | `ONMYRIGHTBORDER` | **+1** |
| `.0.1.5` (query start strictly inside crum) | `THRUME` | **0** |

**Check 1:** `endcmp (1) <= ONMYLEFTBORDER (-1)` → **FALSE** — crum is not rejected.

**Check 2:** `startcmp (0) > THRUME (0)` → **FALSE** — crum is not rejected.

`crumqualifies2d` returns **TRUE**. The crum passes. `findcbcinarea2d` [`retrie.c:229`] adds it to the context list, which flows back through `sporglset2linksetinrange` → `beheadtumbler` to extract the link ISA → `onlinklist` appends it to the result set.

---

### 5. Conclusion

**`find_links` discovers the link through the surviving partial overlap.** Full endset coverage is not required. The reason is two-fold and entirely code-grounded:

1. **The spanfilade is never updated on deletion.** `dodeletevspan` [`do1.c:158`] calls only `deletevspanpm` [`orglinks.c:145`], which calls `deletend` exclusively on the document POOM. No spanfilade write occurs. The original endset I-span `[.0.1.3, .0.1.7)` persists in the spanfilade after bytes `.0.1.3`–`.0.1.5` are removed from all POOMs.

2. **`crumqualifies2d` implements a partial-overlap test, not containment.** [`retrie.c:282-300`] The two rejection conditions are: (a) query end ≤ crum start, (b) query start ≥ crum end. Any strictly positive overlap passes. In our case the surviving query `[.0.1.5, .0.1.7)` overlaps the stored endset `[.0.1.3, .0.1.7)` over the shared interval `[.0.1.5, .0.1.7)`, so the crum qualifies.

A corollary: even if *all* bytes of the endset are deleted from every POOM, the link remains discoverable by direct I-address query, because the spanfilade is never pruned. The link discovery mechanism is purely address-range-based and permanently retains every endset that was ever registered.

---

## Question 14 [gregory]

> When FOLLOWLINK resolves a discovered link's endsets back to V-addresses via `span2spanset`, and some endset I-addresses are unreferenced (not in any current POOM), does it return the surviving subset of V-addresses, or does it return nothing if any portion is missing?

### Gregory's Answer

## KB Synthesis

FOLLOWLINK returns the **surviving subset** — only the I-addresses with current POOM mappings are converted; the unreferenced ones are silently dropped.

The mechanism is documented in [SS-FOLLOWLINK]:

> `linksporglset2specset()` converts I-addresses to V-addresses by looking them up in the specified `homedoc`'s POOM. The conversion calls `span2spanset()` which uses `retrieverestricted()` against the document's orgl. If an I-address has no POOM mapping, `retrieverestricted` returns NULL and the I-address is **silently dropped** — no V-span is added to the result.

This is formalized as a universal invariant in [INV-ITOV-FILTERING]:

> `∀ op returning V-addresses: v ∈ result(op) → ∃ d, i : poom.d(v) = i ∧ i ∈ dom.ispace`

And the three-case behavior is spelled out explicitly in [EC-GHOST-LINK]:

1. **All endset I-addresses live** → full result returned
2. **Some unreferenced** → partial result; only live addresses converted to V-spans
3. **All unreferenced** → empty result `[]`; operation still succeeds (not an error)

[EC-LINK-PARTIAL-SURVIVAL] reinforces that validity is **per-I-span, not per-endset**: content removal affects individual sporgls within an endset independently. The link remains a valid link object as long as the permanent layer (I-space) is intact; what varies is how many of its endset I-addresses have current POOM mappings.

The code site is `backend/orglinks.c:446-448` where the NULL context check silently skips the V-span addition.

## Code Exploration

I now have enough to answer the question precisely. Let me trace the complete call chain from the code.

---

## Answer: FOLLOWLINK returns the surviving subset of V-addresses

The behavior is **partial/subset return**, not all-or-nothing. Here is the full call chain with citations.

---

### The FOLLOWLINK call chain

**`followlink` → `dofollowlink`** [`fns.c:114–127`, `do1.c:223–232`]

```c
// do1.c:223–232
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  return (
     link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
  && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                            sporglset, specsetptr, NOBERTREQUIRED));
}
```

Two distinct phases with different failure semantics.

---

### Phase 1: `link2sporglset` — extracting I-addresses from the link's POOM

[`sporgl.c:67–95`]

```c
bool link2sporglset(typetask *taskptr, typeisa *linkisa, typesporglset *sporglsetptr, INT whichend, int type)
{
  ...
  tumblerincrement (&zero, 0, whichend, &vspan.stream);
  tumblerincrement (&zero, 0, 1, &vspan.width);
  if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
      sporglptr = (typesporgl *)taskalloc(...);
      contextintosporgl ((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
      *sporglsetptr = (typesporglset)sporglptr;
      ...
    }
    contextfree (context);
    return (TRUE);
  } else {
    return (FALSE);   // ← all-or-nothing at this level
  }
}
```

This phase **is** all-or-nothing: if the link's POOM has no endset registered at V-address `whichend`, `retrieverestricted` returns NULL, and the whole `dofollowlink` fails immediately. The I-addresses of the endset exist as stored sporgls inside the link's POOM.

---

### Phase 2: `linksporglset2specset` → `sporglset2vspanset` → `ispan2vspanset` → `permute` → `span2spanset`

This phase converts those stored I-addresses back to V-addresses in the home document's POOM. **This is where partial/subset behavior lives.**

**`linksporglset2specset`** [`sporgl.c:97–123`] iterates each sporgl and calls `linksporglset2vspec` [`sporgl.c:127–137`], which initializes `vspanset = NULL` and then calls:

**`sporglset2vspanset`** [`sporgl.c:141–176`] which calls `ispan2vspanset` for each sporgl's I-span:

```c
vspansetptr = ispan2vspanset (taskptr, orgl, &ispan, vspansetptr);
```

**`ispan2vspanset`** [`orglinks.c:389–394`] delegates immediately to `permute`:

```c
typevspanset *ispan2vspanset(typetask *taskptr, typeorgl orgl, typeispan *ispanptr, typevspanset *vspansetptr)
{
  typespanset *permute();
  return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
```

**`permute`** [`orglinks.c:404–422`] iterates each I-span and calls `span2spanset`:

```c
typespanset *permute(..., typespanset restrictionspanset, ...)
{
  typespanset *save;
  save = targspansetptr;    // saves the head insertion pointer
  for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
  }
  return (save);            // returns head, not NULL on failure
}
```

---

### The critical function: `span2spanset`

[`orglinks.c:425–454`]

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, typespanset restrictionspanptr,
                           INT restrictionindex, typespanset *targspansetptr, INT targindex)
{
  typecontext *context, *c, *retrieverestricted();
  typespan foundspan;
  typespan *nextptr;
  typeitem *onitemlist();

  context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                               (typespan*)NULL, targindex, (typeisa*)NULL);
  for (c = context; c; c = c->nextcontext) {
    context2span (c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist (taskptr, (typeitem*)&foundspan,
                                     (typeitemset*)targspansetptr);
  }
  if(!context){
    return(targspansetptr);   // ← KEY LINE: return unchanged tail pointer
  }
  contextfree (context);
  return (&nextptr->next);    // advance tail pointer past last appended span
}
```

**The key behavior is at `orglinks.c:446–448`:**

When `retrieverestricted` returns NULL (I-address not present in any POOM crum), `context` is NULL. The accumulation loop is skipped entirely. The function returns `targspansetptr` **unchanged** — the tail pointer to the output list is not moved, and **no V-span is emitted for this I-address**.

`permute` continues to the next restriction I-span. If the next one IS referenced, `span2spanset` finds it, emits a V-span via `onitemlist`, and returns the new tail.

---

### What the caller receives

Back in `linksporglset2specset` [`sporgl.c:115–120`]:

```c
} else {
  linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
}
((typeitemheader *)specset)->next = NULL;
*specsetptr = specset;
specsetptr = (typespecset *)&((typeitemheader *)specset)->next;
```

The vspec node is **always** created and appended. If the I-addresses produced no V-spans (all unreferenced), `specptr->vspanset` remains NULL (initialized at `sporgl.c:135`). If some produced V-spans, `vspanset` contains only those. The function returns `TRUE` either way.

---

### Summary

| Situation | Behavior |
|---|---|
| Link has no endset at `whichend` | `link2sporglset` returns FALSE → `dofollowlink` fails entirely |
| Endset I-addresses exist, ALL map to V-addresses | Full vspanset returned |
| Endset I-addresses exist, SOME are unreferenced | **Surviving subset of V-addresses returned**; unreferenced I-spans silently skipped by `span2spanset` at `orglinks.c:446–448` |
| Endset I-addresses exist, ALL are unreferenced | Empty vspanset (NULL); vspec node returned but with null content; `linksporglset2specset` still returns TRUE |

The design is **permissive and partial**: `span2spanset` does not propagate a failure signal when an I-address has no POOM mapping — it simply produces no output for that I-span and advances to the next. There is no all-or-nothing check at the span-to-vspan conversion level. The caller gets whatever V-addresses could be resolved from whichever I-addresses still exist in a current POOM.

---

## Question 15 [gregory]

> If document A creates a link with source=A's content and target=B's content, and then document C transcludes B's content via COPY, does `find_links` called on document C with C's V-span for the transcluded content discover A's link through the target endset overlap?

### Gregory's Answer

## KB Synthesis

Yes. The link is discoverable from C through the target endset overlap. Here is the chain of reasoning:

**Step 1: Link creation indexes B's I-addresses in the spanfilade**

When A creates the link with `target = B's content`, `domakelink` converts B's V-span to I-addresses via `vspanset2sporglset`, then calls `insertendsetsinspanf` to index those I-addresses in the spanfilade tagged as `LINKTOSPAN`. [SS-LINK-ENDPOINT, ST-LINK-CREATE, INT-SPORGL-LINK-INDEX]

**Step 2: COPY shares B's I-addresses into C**

When C transcludes B's content via COPY, the operation calls `docopy` → `insertpm`, which places B's existing I-addresses into C's POOM — no new I-addresses are allocated. C now contains the same I-addresses as B for that content. [ST-VCOPY (Finding 0002, 0018), INT-SPORGL-TRANSCLUSION]

**Step 3: find_links on C resolves to the same I-addresses**

`find_links(from_spec=C's V-span)` converts C's V-span → I-addresses (the shared ones from B) via `specset2ispanset`. The spanfilade search checks: do these I-addresses appear in any link endpoint? They do — in A's link's target endset. [SS-FIND-LINKS (Finding 0028), PRE-FIND-LINKS]

**The governing invariant:**

> `find_links(S) = {link ∈ all_links | endpoints(link) ∩ query_range ≠ ∅}` — [SS-SPANF-OPERATIONS]

Since C's content shares I-addresses with B's content, and A's link's target endset was indexed with those I-addresses, the intersection is non-empty and A's link is returned.

**Confirmed by Finding 0026** ([INT-LINK-TRANSCLUSION]):

> "When a link targets transcluded content, `find_links` discovers the link through both the document containing the transclusion AND the original source document."

That finding demonstrates the same mechanism in the analogous case (find_links on B's content discovering a link whose target points at A's *copy* of B's content). The direction you describe is symmetric and governed by the same spanfilade I-address intersection logic.

**General principle** ([INV-LINK-GLOBAL-VISIBILITY]):

> A link is discoverable from any document whose content shares I-address identity with any of the link's endpoints — whether the link targets that document or another.

So yes: `find_links` called on C with C's V-span for the transcluded B content discovers A's link through target endset overlap. The call need not specify a `to` spec explicitly; any endpoint match suffices.

## Code Exploration

I now have all the code evidence I need. Let me deliver the complete answer.

---

## Answer: Yes — through I-address mediation

**find_links called on document C with C's V-span for transcluded B content DOES discover A's link.** The mechanism is a three-step chain, all mediated through permascroll I-addresses.

---

## Execution Trace

### Step 1 — A creates a link targeting B's content

Entry: `createlink` [fns.c:100-112] → `docreatelink` [do1.c:195-221]

**Converting B's V-spec to I-addresses** [do1.c:215]:
```c
specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
```
`specset2sporglset` [sporgl.c:14-33] iterates the specset. For each `VSPECID` item it calls `vspanset2sporglset` [sporgl.c:35-65]:
```c
if (!findorgl(taskptr, granf, docisa, &orgl, type))
    return (NULL);
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    for (; ispanset; ispanset = ispanset->next) {
        sporglset = (typesporgl *) taskalloc(...);
        movetumbler(docisa, &sporglset->sporgladdress);      // B's ISA
        movetumbler(&ispanset->stream, &sporglset->sporglorigin); // B's I-address
        movetumbler(&ispanset->width,  &sporglset->sporglwidth);
    }
}
```
This resolves B's V-span through B's POOM (via `vspanset2ispanset` → `permute` [orglinks.c:397-422] → `retrieverestricted` on B's orgl). Result: **I_B** — the permascroll I-addresses underlying B's content.

**Indexing in the spanfilade** [do1.c:219 → do2.c:120]:
```c
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, ...)
// calls:
insertspanf(taskptr, spanf, linkisaptr, tosporglset, LINKTOSPAN)
```
Inside `insertspanf` [spanf1.c:15-54]:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]); // link_ISA + LINKTOSPAN
// for each sporgl in tosporglset:
movetumbler(&sporglset->sporglorigin, &crumorigin.dsas[SPANRANGE]); // I_B
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
**Spanfilade now contains:** `(SPANRANGE = I_B, ORGLRANGE = link_ISA prefixed with LINKTOSPAN)`

---

### Step 2 — C transcludes B's content via COPY

Entry: `copy` [fns.c:35-47] → `docopy` [do1.c:45-65]

```c
specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)  // converts B's V-spec → I_B
&& findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)    // finds C's orgl
&& insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)     // inserts into C's POOM
&& insertspanf(taskptr, spanf, docisaptr, ispanset, DOCISPAN)  // indexes in spanf for doc lookup
```
`insertpm` [orglinks.c:75-134] inserts a 2D crum into C's POOM:
```c
movetumbler(&lstream, &crumorigin.dsas[I]);  // I_B (from ispanset)
movetumbler(vsaptr,   &crumorigin.dsas[V]);  // C's V-address for the transcluded content
insertnd(taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
```
**C's POOM now has:** `C_Vaddr → I_B`. C's V-positions for the transcluded content map to the same permascroll I-addresses as B's content.

---

### Step 3 — find_links called on C's V-span for the transcluded content

Entry: `findlinksfromtothree` [fns.c:189-202] → `dofindlinksfromtothree` [do1.c:348-353] → `findlinksfromtothreesp` [spanf1.c:56-103]

**Converting C's V-spec to I-addresses** [spanf1.c:72-73]:
```c
if (tovspecset)
    specset2sporglset(taskptr, tovspecset, &tosporglset, NOBERTREQUIRED);
```
`specset2sporglset` → `vspanset2sporglset` [sporgl.c:35-65] finds C's orgl and calls `vspanset2ispanset` → `permute` [orglinks.c:397-422] → `retrieverestricted` on **C's POOM**.

C's POOM (built in Step 2) maps C's V-address → I_B. So `tosporglset` resolves to **I_B** — the exact same I-addresses.

**Querying the spanfilade** [spanf1.c:84-90]:
```c
if (tovspecset) {
    sporglset2linkset(taskptr, (typecuc*)spanfptr, tosporglset, &tolinkset, orglrange, LINKTOSPAN);
```
`sporglset2linkset` [sporgl.c:222-237] forces `homeset` to a width-100 universe (the `TRUE||!homeset` guard [sporgl.c:227]) — the orgl range parameter is effectively ignored (see Finding 0069). Then `sporglset2linksetinrange` [sporgl.c:239-269]:
```c
for (; sporglset; ...) {
    prefixtumbler(&orglrange->stream, spantype, &range.stream); // LINKTOSPAN prefix
    context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE,
                                 &range, ORGLRANGE, NULL);
    // sporglset->sporglorigin = I_B (from Step 2's tosporglset)
    // range = LINKTOSPAN space
```
`retrieverestricted` [retrie.c:56-85] → `retrieveinarea` [retrie.c:87-110] → `findcbcinarea2d` [retrie.c:229-268] searches the spanfilade 2D B-tree for crums where:
- **SPANRANGE overlaps I_B** — matches the spanf entry from Step 1 (which has SPANRANGE = I_B)
- **ORGLRANGE is in LINKTOSPAN space** — matches (link_ISA + LINKTOSPAN prefix is in that range)

`crumqualifies2d` [retrie.c:270-305] confirms the match. The leaf crum is found.

**Extracting the link ISA** [sporgl.c:263-265]:
```c
beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
onlinklist(taskptr, linksetptr, &linksa);
```
`beheadtumbler` strips the LINKTOSPAN prefix digit, yielding A's link ISA. It is added to the returned link set.

**`find_links` returns A's link.**

---

## Why This Works — The Invariant

The three operations compose through a single invariant: **B's permascroll I-addresses (I_B) are stable across all three operations.**

| Operation | What happens to I_B |
|-----------|---------------------|
| A creates link targeting B | `specset2sporglset` on B's V-spec → I_B stored in spanfilade under LINKTOSPAN |
| C transcludes B via COPY | `specset2ispanset` on B's V-spec → I_B stored in C's POOM as C's V-addr mapping |
| find_links called on C's V-span | `specset2sporglset` on C's V-spec → C's POOM returns I_B → spanfilade query hits I_B under LINKTOSPAN → A's link returned |

The permascroll is the universal referent. Neither A nor C needs to know about each other. Any document that maps to I_B via its POOM — whether it is B itself, a version of B, or an independent transclusion of B in C — will produce the same I-address set and will find the same spanfilade entries.

---

## Empirical Corroboration

This exact mechanism is confirmed by existing golden tests:

**`golden/interactions/link_both_endpoints_transcluded.json`** [lines 71-79]:
```json
{
  "op": "find_links",
  "from": "target_origin",
  "by": "target",
  "result": ["1.1.0.1.0.3.0.2.1"],
  "comment": "Target origin should find link by target search"
}
```
Here `link_doc` transcludes `target_origin`'s content and creates a link targeting that transclusion. Searching `target_origin` by target finds the link — because both resolve to the same I-addresses. The question's scenario is the strict converse: the link targets B directly, and C independently transcludes B. The I-address chain is identical.

**`golden/links/link_to_transcluded_content.json`** [lines 59-65]:
```json
{
  "op": "find_links",
  "to": "B's original content",
  "result": ["1.1.0.1.0.3.0.2.1"],
  "comment": "Does link to A's transcluded content appear when searching B?"
}
```
A link whose target is a transclusion of B is discoverable from B itself — same I-address mechanism.

The specific scenario of the question (link targets B directly, C is an independent third party that transcludes B, and we search from C) is the composition of these two already-confirmed behaviors, with no new code path involved.

---

## Question 16 [gregory]

> When two documents each INSERT the string "Hello" independently (producing different I-addresses), and a link is created on one document's "Hello", is the link completely invisible from the other document — confirming that discovery is purely I-address identity, never byte-value equality?

### Gregory's Answer

## KB Synthesis

Yes, the link is completely invisible from the other document. Discovery is purely I-address identity; byte-value equality plays no role.

## Reasoning

**Independent INSERTs produce distinct I-addresses.**

[SS-CONTENT-IDENTITY / Finding 0018] establishes this directly:

> "Content identity in udanax-green is based on I-addresses (immutable positions in the permascroll), not textual value. Two documents containing identical text created independently do NOT share content identity — `compare_versions` returns an empty result. Identity is determined by *when and where* content was created."

The concrete example given: `Source1: "From source one" → I-address X`, `Source2: "From source two" → I-address Y`, `compare_versions(source1, source2) → []`. Even if both sources contained identical text, independently created content has distinct I-addresses.

**Why the I-addresses differ:** [INV-MONOTONIC / Finding 0033] shows that I-address allocation is a monotonically increasing counter queried against the granfilade state — each INSERT allocates at `max_iaddr(granf) + 1`. Document A's "Hello" allocates α₁..α₅; by the time Document B inserts "Hello", the counter has advanced (or is in a different document's subspace), yielding β₁..β₅ where `{α₁..α₅} ∩ {β₁..β₅} = ∅`.

**Link discovery is set-intersection on I-addresses only.**

[SS-FIND-LINKS / Finding 0028]:

> "`find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }`"

When `find_links` is called from Document B:
- B's content maps to I-addresses β₁..β₅
- Link L's source endpoint maps to α₁..α₅
- Intersection = ∅
- L is not returned

The broken orgl-dimension filter [EC-FIND-LINKS-GLOBAL / Finding 0069] does not help here — it makes the search globally unbounded in the *document* dimension, but the span (I-address) dimension filter still works correctly. A global scan of all links in the system still finds no match, because L's I-addresses are genuinely distinct from B's I-addresses.

**Byte-value equality is never consulted.**

The system has no mechanism to compare content by value anywhere in the link discovery path. [SS-SPORGL / Finding 0013] and [INT-SPORGL-LINK-INDEX / Finding 0035] confirm that `find_links` converts V-spans to I-spans via the POOM and searches the spanfilade by I-address range — the actual bytes stored at those I-addresses are never read during discovery.

## Summary

```
Document A: INSERT "Hello" → I-addresses α₁..α₅
Document B: INSERT "Hello" → I-addresses β₁..β₅  (α ≠ β)
Link L: created on Document A's "Hello" (endpoint = α₁..α₅)

find_links(from Document B's "Hello"):
  query I-addresses = {β₁..β₅}
  L.source I-addresses = {α₁..α₅}
  intersection = ∅
  → L not returned
```

The link is completely invisible from Document B. This is the defining property of Xanadu's intensional content identity: identity is determined by *origin* (when and where content was created), never by byte-value equality.

## Code Exploration

I now have all the evidence needed. Here is my complete analysis.

---

## Answer: Link Discovery Is Purely I-Address Identity — Never Byte-Value Equality

**Yes, confirmed by code.** When two documents each independently `INSERT` the string "Hello", they receive **distinct, unrelated I-addresses** (permascroll locations). A link created on document A's "Hello" is completely invisible when querying from document B's "Hello". There is no byte-value comparison at any point in the pipeline.

---

## The Full Evidence Chain

### Step 1: Independent Inserts Get Distinct I-Addresses

Every call to `doinsert` [`do1.c:87-123`] calls:

```c
inserttextingranf(taskptr, granf, &hint, textset, &ispanset)
```

which delegates immediately to `inserttextgr` [`granf2.c:83-109`]:

```c
bool inserttextgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr,
                  typetextset textset, typeispanset *ispansetptr)
{
    tumbler lsa, spanorigin;
    ...
    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, &lsa))  // allocates next I-addr
        return (FALSE);
    movetumbler (&lsa, &spanorigin);
    for (; textset; textset = textset->next) {
        locinfo.infotype = GRANTEXT;
        locinfo.granstuff.textstuff.textlength = textset->length;
        movmem(textset->string, locinfo.granstuff.textstuff.textstring, ...);  // stores raw bytes
        insertseq ((typecuc*)fullcrumptr, &lsa, &locinfo);
        tumblerincrement (&lsa, 0, textset->length, &lsa);  // advances by byte count
    }
    ...
    movetumbler (&spanorigin, &ispanptr->stream);
    tumblersub (&lsa, &spanorigin, &ispanptr->width);
    *ispansetptr = ispanptr;
    return (TRUE);
}
```
[`granf2.c:83-109`]

The address allocator `findisatoinsertgr` → `findisatoinsertmolecule` [`granf2.c:130-156`, `158-181`] works by finding the **highest previously allocated address under the document's hint** via `findpreviousisagr`, then incrementing beyond it:

```c
static int findisatoinsertmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    ...
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);
    ...
    tumblerincrement (&lowerbound, 0, 1, isaptr);  // next sequential slot
    ...
}
```
[`granf2.c:158-181`]

**The allocated address `lsa` depends only on what's already in the granfilade — never on the byte content being stored.** Doc A's "Hello" (the first insert) gets `ISA_A`. Doc B's "Hello" (inserted later) gets `ISA_B = ISA_A + 5` (or further along, depending on how many bytes have been inserted globally). They share no I-address.

`movmem(textset->string, ...)` at [`granf2.c:98`] is a raw byte copy — it copies without hashing, interning, or deduplication.

---

### Step 2: Link Creation Stores I-Addresses, Not Byte Values

`docreatelink` [`do1.c:195-221`]:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset, ...)
{
    ...
    specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
    ...
    insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, ...)
    ...
}
```

`specset2sporglset` → `vspanset2sporglset` [`sporgl.c:35-65`] converts V-addresses → I-addresses by calling `vspanset2ispanset` (a POOM lookup), then packages each result as a **sporgl**:

```c
movetumbler (docisa, &sporglset->sporgladdress);
movetumbler(&ispanset->stream, &sporglset->sporglorigin);  // I-address!
movetumbler (&ispanset->width, &sporglset->sporglwidth);   // I-width!
```
[`sporgl.c:52-56`]

`insertendsetsinspanf` → `insertspanf` [`spanf1.c:15-54`] indexes this into the spanfilade:

```c
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);  // key = I-address
movetumbler (&lwidth, &crumwidth.dsas[SPANRANGE]);
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);
```
[`spanf1.c:49-51`]

The spanfilade is a 2D enfilade keyed by:
- **ORGLRANGE**: `prefix(link_isa, LINKFROMSPAN/LINKTOSPAN)` — which link, which endpoint
- **SPANRANGE**: the I-address of the endpoint's content

Doc A's link endpoint is stored at `SPANRANGE = ISA_A`. **No byte content is ever stored in the spanfilade.**

---

### Step 3: Link Discovery Searches by I-Address

`findlinksfromtothreesp` [`spanf1.c:56-103`]:

```c
bool findlinksfromtothreesp(...)
{
    ...
    specset2sporglset (taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
    ...
    sporglset2linkset (taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset,
                       orglrange, LINKFROMSPAN);
    ...
}
```

`sporglset2linkset` → `sporglset2linksetinrange` [`sporgl.c:239-268`]:

```c
context = retrieverestricted(spanfptr,
    (typespan*)sporglset, SPANRANGE,   // search key = I-address of query
    &range,              ORGLRANGE,    // restrict to link range
    (typeisa*)infoptr);
```
[`sporgl.c:259`]

`retrieverestricted` → `findcbcinarea2d` [`retrie.c:229-268`] walks the spanfilade and calls `crumqualifies2d` which uses `whereoncrum` to test interval overlap:

```c
bool crumqualifies2d(typecorecrum *crumptr, typedsp *offset,
    tumbler *span1start, tumbler *span1end, INT index1,
    tumbler *span2start, tumbler *span2end, INT index2, ...)
{
    endcmp = whereoncrum(crumptr, offset, span1end, index1);
    if (endcmp <= ONMYLEFTBORDER) return(FALSE);
    startcmp = whereoncrum(crumptr, offset, span1start, index1);
    if (startcmp > THRUME) return(FALSE);
    ...
}
```
[`retrie.c:270-305`]

The query's SPANRANGE is Doc B's I-address `ISA_B`. The stored link's SPANRANGE is `ISA_A`. Since `ISA_A ≠ ISA_B` and they don't overlap, `crumqualifies2d` returns `FALSE` for every crum belonging to the link. **The link is never found.**

`sporglset2linkset` exits with `*linksetptr = NULL`, and `findlinksfromtothreesp` returns `TRUE` with an empty link set [`spanf1.c:78-82`]:

```c
if (!fromlinkset) {
    *linksetptr = NULL;
    return (TRUE);  // success, but zero results
}
```

---

### Why Transclusion IS Different

The existing Finding 0026 / Finding 0028b (and scenarios in `discovery.py`) document that links **are** discoverable across documents when content is **transcluded**. That works because `vcopy` (= `docopy`) calls `insertpm` [`orglinks.c:75-134`] which inserts the **same I-address range** (`lstream = ISA_A`) into the destination document's POOM at a new V-position. Both documents then map to the same I-address, so `vspanset2ispanset` for either document produces `ISA_A`, and the link stored at `ISA_A` is found.

**Independent inserts never share I-addresses.** There is no mechanism by which `inserttextgr` could deduplicate or reuse an existing I-address. `findisatoinsertmolecule` looks only at tumbler arithmetic (finding the next sequential slot), never at byte content.

---

## Definitive Architecture Proof

```
Granfilade (permascroll):
  ISA_A  →  bytes "Hello"   ← Doc A's insert
  ISA_B  →  bytes "Hello"   ← Doc B's insert (different address, same bytes)

Spanfilade (link index):
  ORGLRANGE: link_X / LINKFROMSPAN
  SPANRANGE: ISA_A            ← link stored here
                ISA_B           ← nothing here

Query from Doc B's "Hello":
  V-address → POOM B → ISA_B
  retrieverestricted(SPANRANGE = ISA_B)
    → crumqualifies2d: ISA_A ∩ ISA_B = ∅ → FALSE for all crums
  → linkset = NULL
```

---

## Summary

| Claim | Code Location | Evidence |
|-------|--------------|---------|
| Each insert gets a unique I-address | `granf2.c:83-109` (`inserttextgr`), `granf2.c:158-181` (`findisatoinsertmolecule`) | Sequential allocation from `findpreviousisagr` + increment; never reads byte content |
| Byte content is stored without deduplication | `granf2.c:98` (`movmem`) | Raw `movmem` copy, no hash, no equality check |
| Links store I-addresses as endpoints | `sporgl.c:52-56` (`vspanset2sporglset`), `spanf1.c:49-51` (`insertspanf`) | `sporglorigin` = I-stream, indexed in SPANRANGE dimension |
| Link discovery queries by I-address | `sporgl.c:239-268` (`sporglset2linksetinrange`) | `retrieverestricted(..., SPANRANGE, ...)` with query I-address |
| Non-overlapping I-addresses produce zero results | `retrie.c:270-305` (`crumqualifies2d`) | Interval comparison; `ISA_A ∩ ISA_B = ∅ → FALSE` |

**Conclusion:** Discovery in udanax-green is purely I-address identity. Two independent inserts of "Hello" are as unrelated as two inserts of "Goodbye" — they happen to encode the same bytes at different permascroll addresses, and that coincidence is invisible to every layer of the system. A link on one is completely invisible from the other.

---

## Question 17 [gregory]

> After REARRANGE fragments a contiguous endset span into two non-contiguous V-regions within the same document, does `find_links` called with a V-span covering only ONE of those two regions still discover the link, or must the query span cover both fragments?

### Gregory's Answer

## KB Synthesis

**Yes** — querying with a V-span covering only one of the two fragments still discovers the link.

## Reasoning

**Step 1: What REARRANGE does to I-addresses**

From [INV-REARRANGE-IDENTITY], REARRANGE is a pure V-address permutation that preserves all I-addresses. The set of I-addresses in the document is unchanged; only V-positions change. After a pivot that splits a contiguous endpoint region into two V-regions, each fragment still maps to the same I-addresses that the link endpoint originally referenced — just at different V-positions.

**Step 2: How `find_links` operates**

From [SS-FIND-LINKS] (Finding 0028), the search predicate is:

```
find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }
```

**Partial overlap suffices.** A search specset that shares even one I-address with a link endpoint discovers the link. This is demonstrated explicitly: a document containing only "link" (4 chars from the 14-char "hyperlink text") discovers the link created on the full phrase.

**Step 3: Application to the fragmented case**

When you query with a V-span covering only one fragment:
1. That V-span is converted to I-addresses via the document's POOM
2. Those I-addresses are a *subset* of the link endpoint's full I-address set
3. The intersection is non-empty (it equals that subset)
4. Therefore the link is returned

**Direct confirmation from the KB**

[EC-PIVOT-LINK-FRAGMENTATION] (Finding 0019) directly documents this scenario. After a pivot, the link's endsets become fragmented into multiple spans, and `find_links` actually returns the link *twice* — once per fragment matched. This confirms that either fragment independently satisfies the discovery condition.

**Note on AND semantics**

[ST-FIND-LINKS] (Finding 0029) establishes that `find_links(source, target)` with *both* endpoints specified requires both to be present. But in a single-endpoint query — e.g., `find_links(source_spec, NOSPECS)` — only the one specified endpoint must be present. Querying with a V-span covering one fragment is a single-endpoint query against the I-addresses in that fragment, which is sufficient.

## Summary

A V-span covering either fragment independently discovers the link, because `find_links` intersects the query's I-addresses against the link's endpoint I-addresses, and REARRANGE guarantees the I-addresses are preserved in both fragments. The partial-overlap rule makes each fragment a valid discovery path.

## Code Exploration

I now have everything needed for a definitive answer. Let me trace the complete execution path.

---

## Answer

**Yes: a V-span covering only ONE of the two V-regions finds the link.** The query does not need to cover both fragments. This is a structural consequence of how the spanfilade is indexed — by I-space, not V-space — and how `retrieverestricted` performs intersection matching.

Here is the full code trace.

---

### 1. REARRANGE touches only the POOM; the spanfilade is never updated

`fns.c:159–173` (`rearrange`) → `do1.c:34–43` (`dorearrange`) → `orglinks.c:137–142` (`rearrangepm`):

```c
bool rearrangepm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typecutseq *cutseqptr)
{
    rearrangend((typecuc*)docorgl, cutseqptr, V);   // only the POOM, V-dim
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`rearrangend` (`edit.c:78–160`) shifts the `cdsp.dsas[V]` displacement fields of crums in the document's POOM tree. It calls `makecutsnd`, then walks children and applies `diff[i]` offsets to their V-displacements (`edit.c:125`), then calls `recombine` and `splitcrumupwards`. **The spanfilade (`spanf`) is not touched at any point during REARRANGE.**

---

### 2. When a link was created, its endsets were stored as I-spans in the spanfilade

`do1.c:195–221` (`docreatelink`) ultimately calls `insertendsetsinspanf` (`do2.c:116–128`), which calls `insertspanf` (`spanf1.c:15–54`):

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
// ...
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

The SPANRANGE coordinate of each spanfilade crum is the **I-span** (`sporglorigin`, `sporglwidth`) of the link's endset — a permascroll address. The ORGLRANGE coordinate is the link ISA prefixed by `spantype` (1 for FROM, 2 for TO, 3 for THREE). These records are **permanent and unaffected by any subsequent REARRANGE**.

---

### 3. `find_links` converts the query V-span to I-spans via the current POOM

`fns.c:189–202` (`findlinksfromtothree`) → `do1.c:348–353` (`dofindlinksfromtothree`) → `spanf1.c:56–103` (`findlinksfromtothreesp`):

```c
if (fromvspecset)
    specset2sporglset(taskptr, fromvspecset, &fromsporglset, NOBERTREQUIRED);
// ...
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN);
```

`specset2sporglset` (`sporgl.c:14–33`) → `vspanset2sporglset` (`sporgl.c:35–65`):

```c
if (!findorgl(taskptr, granf, docisa, &orgl, type)) ...  // get CURRENT POOM
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);
    // convert each I-span to a sporgl
}
```

`vspanset2ispanset` (`orglinks.c:397–402`) → `permute` (`orglinks.c:404–422`) → `span2spanset` (`orglinks.c:425–454`) → `retrieverestricted` on the POOM (V-dimension query), then `context2span` (`context.c:176–212`):

```c
if (tumblercmp(&grasp.dsas[idx1], &lowerbound) == LESS) {
    tumblerincrement(&grasp.dsas[idx2], 0, (INT)tumblerintdiff(&lowerbound, &grasp.dsas[idx1]), &grasp.dsas[idx2]);
}
if (tumblercmp(&reach.dsas[idx1], &upperbound) == GREATER) {
    tumblerincrement(&reach.dsas[idx2], 0, -tumblerintdiff(&reach.dsas[idx1], &upperbound), &reach.dsas[idx2]);
}
```

`context2span` clips the crum's I-extent to exactly the I-sub-range that corresponds to the query V-span. So querying with V-fragment `[Va, Vm]` produces sporglset containing I-span `[Ia, Im]` — a proper **subset** of the link's full endset I-span `[Ia, Ib]`.

---

### 4. The spanfilade search uses intersection, not equality

`sporglset2linkset` (`sporgl.c:222–237`) → `sporglset2linksetinrange` (`sporgl.c:239–269`):

```c
context = retrieverestricted(spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

`retrieverestricted` (`retrie.c:56–85`) → `retrieveinarea` (`retrie.c:87–110`) → `findcbcinarea2d` (`retrie.c:229–268`) → **`crumqualifies2d`** (`retrie.c:270–305`):

```c
endcmp = iszerotumbler(span1end) ? TOMYRIGHT : whereoncrum(crumptr, offset, span1end, index1);
if (endcmp <= ONMYLEFTBORDER) return(FALSE);           // crum is entirely to the RIGHT of query end → skip

startcmp = whereoncrum(crumptr, offset, span1start, index1);
if (startcmp > THRUME) return(FALSE);                  // crum is entirely to the LEFT of query start → skip

// otherwise: INTERSECTS → qualify
```

This is a standard **interval intersection** test: the spanfilade crum qualifies if its SPANRANGE interval `[Ia, Ib]` overlaps with the query interval `[Ia, Im]`. Since `[Ia, Im]` is a prefix of `[Ia, Ib]`, both start at `Ia`, so:

- `whereoncrum` with `span1end = Im` on the crum whose left boundary is `Ia`: `Im > Ia` → not ONMYLEFTBORDER → passes first check
- `whereoncrum` with `span1start = Ia` on a crum starting at `Ia`: ONMYLEFTBORDER → not THRUME-exceeded → passes second check

The crum qualifies. The link's ISA is extracted via `beheadtumbler` at `sporgl.c:264` and appended to the linkset.

---

### 5. The same holds for the second fragment

Querying with V-fragment `[Vn, Vb]` maps via the current POOM to I-span `[Im, Ib]` (the tail of the original endset I-span). Again `[Im, Ib]` intersects `[Ia, Ib]`, so the link is found identically.

---

### Conclusion

After REARRANGE fragments the endset's V-region into two non-contiguous pieces, **a V-span query covering only ONE of those fragments is sufficient to discover the link**. The query does not need to cover both.

This holds because of three invariants:

1. **REARRANGE does not touch the spanfilade** (`orglinks.c:137–142`). It only adjusts V-displacements in the document POOM via `rearrangend`.

2. **The spanfilade is I-space indexed.** Link endsets are stored as I-spans (permascroll addresses) at insertion time (`spanf1.c:49–51`). These are invariant under any REARRANGE.

3. **Spanfilade retrieval uses intersection, not equality** (`retrie.c:270–305`). Any query I-span that overlaps any portion of the stored endset I-span will match the link. A partial V-fragment maps to a partial I-subset of the endset, which always overlaps the stored full endset I-span.

The design is intentional: Xanadu links are tied to permascroll identities (I-space), not virtual document positions (V-space). Rearranging content changes where it appears in the virtual document but not what it is. A link to content X finds X regardless of how many times that content is moved, split, or rearranged in V-space.

---

## Question 18 [gregory]

> When `sporglset2linkset` uses the hardcoded `TRUE||!homeset` override to search globally, does it search ALL link orgls across ALL documents in the system, or is the search still bounded by the I-address range of the query specset?

### Gregory's Answer

## KB Synthesis

The search is bounded by the I-address range of the query specset on the span dimension, but globally unbounded on the orgl dimension.

## Two Independent Dimensions

The spanfilade is a 2D enfilade with two independent search axes [INT-SPORGL-LINK-INDEX]:

- **SPANRANGE** (I-address / content axis): derived from the query specset, converted to I-addresses via `vspanset2sporglset`. This filter is applied normally.
- **ORGLRANGE** (document/link origin axis): normally the `homedocids` parameter. This is what `TRUE||!homeset` overrides.

## What the Override Does

From [EC-FIND-LINKS-GLOBAL] and [PRE-FIND-LINKS] (Finding 0069):

The `sporglset2linkset()` override replaces the caller's orgl range with `{stream: 0, width: 100}` — a hardcoded range starting at tumbler zero with width 100 mantissa digits. This makes the orgl-dimension search cover every link orgl in the entire system (all documents, all link ISAs within realistic tumbler ranges).

The SPANRANGE filter from the query specset is **untouched** by this override. `retrieverestricted()` downstream still receives both dimension restrictions; the override only affects one of them [INT-SPORGL-LINK-INDEX].

## Net Result

```
Effective search = { link ∈ ALL_LINKS_IN_SYSTEM
                   | endpoint_iaddrs(link) ∩ query_iaddrs ≠ ∅ }
```

A link anywhere in the system will be returned if and only if any of its endpoint I-addresses intersect with the I-address range derived from the query specset. The search is not "completely unbounded" — it is bounded by content identity intersection on the span axis. But within that constraint, it searches across every document's links with no orgl-level scoping.

[EC-FIND-LINKS-GLOBAL] states this directly: "A call intended to find links only within a specific document will also return links from every other document, **as long as the span-dimension (I-address) match succeeds**."

This is why transclusion makes links visible globally [INT-LINK-TRANSCLUSION]: once I-addresses are shared, the span-dimension match fires for any document holding those addresses, and the orgl-dimension override ensures the matching link orgls — wherever they live — are all returned.

## Code Exploration

---

## Answer: What `TRUE||!homeset` Searches

### The Global `spanf` Is the Only Link Index

There is a **single system-wide link spanfilade**, `spanf`, created at startup `[entexit.c:45]`:
```c
spanf = (typespanf) createenf (SPAN);
```

Every link endpoint in the entire system is indexed in this one structure. There is no per-document link spanfilade. The ORGLRANGE dimension of `spanf` encodes `spantype . docISA` — the link-end type prefixed to the document ISA — to distinguish which document "owns" each entry.

---

### The `TRUE||!homeset` Override

`sporglset2linkset` `[sporgl.c:222-237]`:
```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
                      typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;
    *linksetptr = NULL;
    if (TRUE||!homeset) {                   // always true
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100; // hard-coded cap
        nullhomeset.next = NULL;
        homeset = &nullhomeset;
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

The condition `TRUE||!homeset` is a short-circuit: `!homeset` is **never evaluated**. The caller-supplied `homeset` is unconditionally discarded, and `nullhomeset` is substituted.

Note also that the primary caller, the FEBE handler `findlinksfromtothree` `[fns.c:198]`, already passes `NULL` for `homeset`:
```c
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
                            (typeispan*)NULL/*homeset*/, &linkset))
```
So the client-provided `homeset` is discarded **twice**: once at the FEBE handler level, and once inside `sporglset2linkset`. (The variant `findnumoflinksfromtothree` at `[fns.c:213]` does pass the real `homeset`, but it still hits the `TRUE||` override.)

---

### What ORGLRANGE Range Is Searched

`sporglset2linksetinrange` `[sporgl.c:257-259]` constructs an ORGLRANGE restriction from `orglrange` (the `nullhomeset`) using `prefixtumbler`:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler(&orglrange->width,  0,        &range.width);
```

`prefixtumbler` `[tumble.c:641-651]` prepends `bint` as a new leading component:
```c
int prefixtumbler(tumbler *aptr, INT bint, tumbler *cptr) {
    tumblerclear (&temp1);
    temp1.mantissa[0] = bint;
    movetumbler (aptr, &temp2);
    if (!iszerotumbler (&temp2)) temp2.exp -= 1;  // shift aptr down one level
    tumbleradd (&temp1, &temp2, cptr);
}
```

With `nullhomeset.stream = 0` (zero tumbler) and `spantype = LINKFROMSPAN = 1` `[xanadu.h:36]`:
- `temp2` is zero → exp NOT decremented  
- `range.stream = {mantissa[0]=1, exp=0}` = the tumbler `1`

With `nullhomeset.width = {mantissa[0]=100, exp=0}` and `bint=0`:
- `temp1 = {0}` (zero, since bint=0)
- `temp2 = {100, exp=-1}` (the 100-tumbler shifted down one level)
- `range.width = {mantissa[0]=100, exp=-1}`

The resulting ORGLRANGE endpoint `range.stream + range.width`:
Using `absadd` `[tumble.c:460-484]` on `{1, exp=0}` + `{100, exp=-1}`:
- answer.exp = 0 (the higher exp)
- ansmant[0] = 1 (from aptr[0])
- ansmant[1] = 0 + 100 = 100 (aptr[1] + bptr[0])
- Result: `{1, 100, 0, ..., exp=0}` = the tumbler `1.100`

**The ORGLRANGE search range is `[1, 1.100)` for LINKFROMSPAN.**

---

### Does This Cover All Documents?

In `insertspanf` `[spanf1.c:22]`, a link endpoint for document ISA `docisa` under `spantype` is stored at ORGLRANGE:
```c
prefixtumbler(isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);
```

For any document with `docISA = 1.1.0.1` (typical), the stored ORGLRANGE = `1.1.1.0.1`.

Range check: Is `1.1.1.0.1` within `[1, 1.100)`?  
- Compare `{1,1,1,0,1}` vs `{1,100}` using `abscmp` `[tumble.c:87]`: mantissa[0] equal (1=1), mantissa[1] = 1 < 100 → **LESS → THRUME (within range)** ✓

For **any** document whose ISA has `mantissa[0] = 1` (which is all real Xanadu documents — the `1` is the universal system prefix), the ORGLRANGE after `prefixtumbler` will have `mantissa[1] = 1`. Since `1 < 100`, **all such documents fall within the range `[spantype, spantype.100]`**.

The "100" is an empirical constant, not a semantic boundary derived from the query. It is large enough to encompass the entire first-component namespace of real Xanadu document ISAs.

---

### Is the SPANRANGE Still Bounded by the Query Specset?

**Yes.** In `sporglset2linksetinrange` `[sporgl.c:259]`, `retrieverestricted` is called with **two** independent constraints:

```c
context = retrieverestricted(spanfptr,
    (typespan*)sporglset, SPANRANGE,   // I-address content from query
    &range,             ORGLRANGE,     // doc/orgl space = the wide synthetic range
    (typeisa*)infoptr);
```

- **SPANRANGE** = the I-addresses of the content encoded in `sporglset` (derived from the query specset). This is the primary discriminator for which links are found, and it comes entirely from the caller's specset. The `TRUE||!homeset` override does **not** affect this dimension.
- **ORGLRANGE** = the `[spantype, spantype.100]` range. This is what the override globalizes.

The search finds all links in the global `spanf` where the content I-address (SPANRANGE) overlaps the query sporglset's I-address **and** the entry's link-orgl address (ORGLRANGE) falls in `[spantype, spantype.100]`.

---

### Summary

| Dimension | What the `TRUE||!homeset` override does |
|-----------|----------------------------------------|
| **ORGLRANGE** (which link orgls / documents) | Overrides caller-supplied range with synthetic `[spantype, spantype.100]`, which **practically covers all documents** in the system (all with `docISA.mantissa[0] = 1`) |
| **SPANRANGE** (content I-addresses) | **Unchanged** — still fully bounded by the I-addresses in the query specset |

**The `TRUE||!homeset` override makes `sporglset2linkset` search across ALL link orgls in ALL documents in the system** (within the single global `spanf`), rather than restricting to a specific document's orgl range. The search is **not** bounded by any I-address range from the query in the ORGLRANGE dimension. However, it **is still bounded by the query specset's I-addresses** via the SPANRANGE constraint — that is what determines *which links* are found.

The `width.mantissa[0] = 100` is a hardcoded implementation assumption that the entire document address space fits within 100 sub-units of the spantype prefix, not a semantic guard derived from the query. If a document ISA had its first component ≥ 100 (impossible in normal operation), its links would be silently missed.

---

## Question 19 [gregory]

> If a link is created in document A, and then A's link subspace entry is deleted via DELETEVSPAN on `0.2.x` (reverse orphaning), can document B — which transcludes A's source content — still discover the link through `find_links`, since the spanfilade entry persists?

### Gregory's Answer

## KB Synthesis

**Yes.** Document B can still discover the link. Here is the full reasoning:

## Three Independent Storage Layers

Link creation writes to all three layers [SS-THREE-LAYER-MODEL]:

1. **I-space** — link orgl at a permanent I-address
2. **Spanfilade** — DOCISPAN/endpoint entries mapping source content I-addresses → link ISA
3. **POOM** — V-position 2.x entry in A's document enfilade

`DELETEVSPAN(0.2.x)` on document A affects **only layer 3** (the POOM). Specifically:

> `delete(D, 2.x, r) ⟹ ispace' = ispace ∧ spanfilade' = spanfilade` [FC-LINK-DELETE-ISOLATION]

The code confirms this: `deletevspanpm` calls `deletend` on the document's orgl (POOM only), with no call to any spanf function [ST-DELETE, Finding 0057].

## Why B Still Finds the Link

`find_links` operates by converting B's query specset to I-addresses, then searching the spanfilade for endpoint overlap [ST-FIND-LINKS]:

```
find_links(S) = { L | I-addresses(S) ∩ I-addresses(L.source) ≠ ∅ }
```

This search is **entirely in I-space** — it never consults A's (or B's) POOM. Since:

- The spanfilade entry for the link's source endpoint I-addresses was **not removed** by DELETEVSPAN (the spanfilade is write-only, append-only) [INV-SPANF-WRITE-ONLY]
- B's transclusion of A's source content means B's POOM holds the **same I-addresses** as A's source content [INT-LINK-TRANSCLUSION, ST-VCOPY]
- Those I-addresses still intersect the spanfilade's index for the link

B's `find_links` query on B's transcluded content will hit the still-intact spanfilade entry and return the link.

## This Is the "Reverse Orphan" State

This scenario is explicitly catalogued as [EC-REVERSE-ORPHAN]:

> **Reverse orphan**: the link does NOT exist in the POOM but is fully intact — link orgl exists, endsets resolve correctly, and discovery via `find_links` works.

The concrete postcondition from Finding 0040:
```
After DELETEVSPAN(2.1) on document A:
  find_links(source_specs) → [link_id]   ← spanfilade intact
  follow_link(link_id, SOURCE) → works   ← link orgl intact
  retrieve_vspanset(A) → no link span    ← POOM entry removed
```

B's transclusion of A's source content makes B an additional discovery path for the link — one that is entirely independent of whether A's own POOM retains the link entry [INT-LINK-TRANSCLUSION, INV-LINK-GLOBAL-VISIBILITY].

## Summary

| Layer | After DELETEVSPAN on A's 2.x | Effect on B's find_links |
|-------|------------------------------|--------------------------|
| I-space (link orgl) | Intact | No effect — link still exists |
| Spanfilade (endpoint index) | Intact | B's I-addresses still match |
| A's POOM (2.x entry) | Removed | Irrelevant — find_links doesn't use POOM |

**B discovers the link.** The DELETEVSPAN severs A's structural containment of the link, but the link remains fully discoverable from any document sharing the source content's I-addresses — which B does by virtue of transclusion.

## Code Exploration

I now have all the evidence needed. Here is the full answer.

---

## Answer: Yes — Document B Can Still Discover the Link

The short answer is **yes**, with complete certainty grounded in the code. Deleting document A's link-subspace POOM entry (`dodeletevspan` on V=2.x) has **no effect on the spanfilade**. The spanfilade entries created at link-creation time persist intact, and the `find_links` query path from document B never touches document A's POOM at all.

Here is the full trace.

---

## 1. What Link Creation Actually Writes

`docreatelink` [do1.c:195–221] performs two independent write operations:

```c
// [A] Register the link in document A's POOM at link-subspace V-address
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)           // do1.c:212

// [B] Write endpoint I-addresses → link ISA into the global spanfilade
&& insertendsetsinspanf (taskptr, spanf, linkisaptr,
                         fromsporglset, tosporglset, threesporglset)  // do1.c:219
```

**Write [A]** calls `docopy` → `insertpm` [orglinks.c:75], which inserts a crum into document A's granfilade (POOM) mapping the link-subspace V-address (`2.1`, `2.2`, ...) to the link's own ISA in I-space.

The link VSA is computed by `findnextlinkvsa` [do2.c:151–167]:
```c
tumblerclear (&firstlink);
tumblerincrement (&firstlink, 0, 2, &firstlink);  // mantissa[0] = 2
tumblerincrement (&firstlink, 1, 1, &firstlink);  // mantissa[1] = 1  → "2.1"
```
So links occupy V=2.x in document A's POOM.

**Write [B]** calls `insertendsetsinspanf` [do2.c:116–128] → `insertspanf` [spanf1.c:15–53] for FROM, TO, and THREE endpoints. For each endpoint sporgl, `insertspanf` inserts a 2D crum into the **global spanfilade** (`spanf`):

```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // spanf1.c:22 — link ISA w/ type prefix
// ...
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);   // spanf1.c:49 — I-addr of endpoint content
movetumbler (&lwidth,  &crumwidth.dsas[SPANRANGE]);    // spanf1.c:50
insertnd(taskptr, (typecuc*)spanfptr, &crumorigin, &crumwidth, &linfo, SPANRANGE);  // spanf1.c:51
```

The spanfilade crum maps:
- **SPANRANGE** dimension: I-addresses of the link endpoint content
- **ORGLRANGE** dimension: link ISA prefixed with LINKFROMSPAN / LINKTOSPAN / LINKTHREESPAN

These two writes — document A's POOM crum and the global spanfilade crum — are **structurally independent**. The spanfilade `(spanf)` and the granfilade `(granf)` are separate enfilades.

---

## 2. What DELETEVSPAN Actually Deletes

`dodeletevspan` [do1.c:158–167]:

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)   // open doc A's organule
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)        // delete from that orgl
  /*&& TRUE*/ /* ht stuff */ );
}
```

`deletevspanpm` [orglinks.c:145–152]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
  if (iszerotumbler(&vspanptr->width))
    return (FALSE);
  deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);  // cuts from docorgl only
  logbertmodified(docisaptr, user);
  return (TRUE);
}
```

`deletend` [edit.c:31–76] takes `(typecuc*)docorgl` — **document A's organule from `granf`** — as its target. It cuts V-range nodes from that POOM tree and adjusts displacements. The operation is scoped to `docorgl` exclusively.

**There is no call to any spanfilade function.** Furthermore, inspection of `spanf1.c` and `spanf2.c` in their entirety confirms: **no deletion function exists for the spanfilade**. Only `insertspanf` (writes), `findlinksfromtothreesp`, `findnumoflinksfromtothreesp`, `retrieveendsetsfromspanf`, and `finddocscontainingsp` (reads) exist. There is no `deletespanf`, no `removespanf`, no cleanup of any kind (Finding 0057, confirmed independently here).

---

## 3. How find_links Queries from Document B

`dofindlinksfromtothree` [do2.c:348–353]:

```c
bool dofindlinksfromtothree(typetask *taskptr, typespecset fromvspecset,
    typespecset tovspecset, typespecset threevspecset,
    typeispan *orglrangeptr, typelinkset *linksetptr)
{
  bool findlinksfromtothreesp();
  return findlinksfromtothreesp(taskptr, spanf, fromvspecset, tovspecset,
                                 threevspecset, orglrangeptr, linksetptr);
}
```

`findlinksfromtothreesp` [spanf1.c:56–103] for a query `fromvspecset = {docisa: B, vspanset: [B's range]}`:

**Step 1** — `specset2sporglset` [sporgl.c:14–33] → `vspanset2sporglset` [sporgl.c:35–65]:

```c
if (!findorgl (taskptr, granf, docisa, &orgl, type))   // opens doc B's organule
    return (NULL);
for (; vspanset; vspanset = vspanset->next) {
    (void) vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);   // B's V→I via B's POOM
    // ... packages result as sporgl with sporgladdress=B, sporglorigin/width=I-addr
}
```

This converts B's V-spans to I-spans by traversing **document B's POOM**. Document B transcludes A's text content, so B's POOM holds crums mapping B's V-addresses to the same I-addresses that were written by `docopy` when B transcluded from A. Document A's POOM is never opened here.

**Step 2** — `sporglset2linkset` [sporgl.c:222–237] → `sporglset2linksetinrange` [sporgl.c:239–269]:

```c
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE,
                               &range, ORGLRANGE, (typeisa*)infoptr);   // queries spanf
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE], &linksa);
    onlinklist (taskptr, linksetptr, &linksa);   // collects link ISAs
}
```

This queries the **global spanfilade** with the I-addresses from step 1 in the SPANRANGE dimension, constrained to `range` (which is `prefixtumbler(&orglrange->stream, spantype, ...)` — the LINKFROMSPAN or LINKTOSPAN prefix) in the ORGLRANGE dimension. It returns whatever link ISAs the spanfilade has indexed for those I-addresses.

The spanfilade crum for this link was written at `docreatelink` time and has **not been touched by `dodeletevspan`**. It is still present.

---

## 4. The Complete Information Flow

```
LINK CREATION (docreatelink):
  docreatelink [do1.c:195]
    → docopy [do1.c:212]
         → insertpm [orglinks.c:75]
              → insertnd on docorgl (doc A's POOM)          ← WRITE A's POOM
    → insertendsetsinspanf [do1.c:219]
         → insertspanf [spanf1.c:15]
              → insertnd on spanf (global spanfilade)        ← WRITE spanf

DELETION (dodeletevspan on V=2.x in A):
  dodeletevspan [do1.c:158]
    → deletevspanpm [orglinks.c:145]
         → deletend on docorgl (doc A's POOM)               ← REMOVES A's POOM crum
    (no spanf call)                                          ← spanf UNTOUCHED

FIND_LINKS FROM B:
  dofindlinksfromtothree [do2.c:348]
    → findlinksfromtothreesp [spanf1.c:56]
         → specset2sporglset [sporgl.c:14]
              → vspanset2sporglset [sporgl.c:35]
                   → findorgl on granf with doc B           ← opens B's POOM (not A's)
                   → vspanset2ispanset → permute            ← B's V→I conversion
         → sporglset2linkset [sporgl.c:222]
              → sporglset2linksetinrange [sporgl.c:239]
                   → retrieverestricted on spanf            ← queries global spanfilade
                   (finds link ISA — still there)           ← LINK FOUND
```

---

## 5. The Precise Reason It Works

Document B's `find_links` query succeeds because:

1. **Transclusion shares I-addresses** (Finding 0002): When B transcluded A's text content, B's POOM stored crums pointing to the same permascroll I-addresses that were used as the link endpoint.

2. **The spanfilade is keyed on I-addresses**: The entries written by `insertendsetsinspanf` at link creation time map `(I-address of endpoint content) → (link ISA with type prefix)`. These I-addresses are content-identity addresses, not document-specific.

3. **`dodeletevspan` is strictly POOM-scoped**: It calls `deletend` only on document A's organule (`docorgl`) in `granf`. It has no knowledge of the spanfilade and makes no calls into `spanf1.c` or `spanf2.c`.

4. **No spanfilade deletion function exists**: There is no code path anywhere in the system that removes spanfilade entries written by `insertendsetsinspanf`. The spanfilade is write-only with respect to link indexing.

5. **B's POOM is never touched**: The find_links query path opens B's organule to do V→I conversion, then queries the global spanfilade. Document A's organule — whose POOM crum was deleted — is never opened during this query.

---

## 6. One Subtle Caveat

If `find_links` is called **from document A** (not B) with a vspec using A's V-addresses in the text subspace (V=1.x), it would still work too: `specset2sporglset` would open A's POOM, convert V=1.x to I-addresses via A's text crums (which are untouched by the link-subspace delete — Finding 0038 confirms V=1.x and V=2.x are subspace-independent), and then query the spanfilade normally.

The deleted crum was at V=2.x in A (link subspace). Text crums live at V=1.x. The `deletend` call with `{stream: 2.x, width: ...}` only removes crums within that V-range. Text crums at V=1.x survive untouched.

---

## Summary

**The spanfilade entry persists, and document B can discover the link.** `DELETEVSPAN` on document A's link-subspace entry (`V=2.x`) calls `deletend` on A's POOM organule only [`orglinks.c:149`]. The global spanfilade — which indexes `(I-address of link endpoint content) → (link ISA)` — is never modified. The `find_links` query from document B traverses B's POOM for V→I conversion, then queries the spanfilade directly. Since both B's POOM and the spanfilade are untouched by the deletion, the link is discovered successfully.

This is an instance of the broader architectural property confirmed in Finding 0057: **the spanfilade is write-only**. There is no `deletespanf` function. Entries accumulate but are never removed, making the spanfilade a permanent historical record of link-endpoint associations, independent of the current POOM state of any document.

---

## Question 20 [gregory]

> When `find_links` returns multiple links matching the same I-address range, does the implementation guarantee any ordering among the results — by link creation order, by link I-address, or by document of origin — or is the order determined solely by spanfilade tree traversal?

### Gregory's Answer

## KB Synthesis

The KB does not contain explicit findings on `find_links` result ordering. Here is what can be synthesized:

**What the KB tells us about the retrieval mechanism:**

The spanfilade is a 2D enfilade (SPAN type). Retrieval from N-dimensional enfilades uses `incontextlistnd()`, which performs insertion-sort by the left boundary in the queried dimension as contexts are discovered during B-tree traversal [SS-CONTEXT-LIST]. This is the same sorting mechanism documented for POOM queries.

The result of `findlinksfromtothreesp()` is a linked list built during this traversal [SS-PAGINATE-LINKS]. The pagination cursor mechanism linearly scans this list, implying the order is deterministic across calls (given no structural tree changes between calls).

**What the KB tells us about tree structure:**

For SPAN enfilades, dimension 0 is ORGLRANGE (link I-space) and dimension 1 is SPANRANGE (V-space) [SS-ENFILADE-TREE, Finding 0066]. The diagonal sort key `dsas[0] + dsas[1]` governs rebalancing but not necessarily retrieval ordering directly — `incontextlistnd()` sorts by `totaloffset.dsas[index]` for the queried dimension.

The tree shape is also path-dependent: different insertion histories produce different sibling orderings even for identical content [INV-ENFILADE-CONFLUENCE]. The retrieval-independence invariant [INV-RETRIEVAL-TREE-INDEPENDENCE] holds that query results are independent of tree structure for POOM, but this is asserted specifically for V-sorted POOM retrieval — the KB does not assert the equivalent explicitly for spanfilade link results.

**What the KB does NOT tell us:**

None of the findings document the observable sort key for `find_links` results: whether by link creation order, link I-address (ORGLRANGE boundary), content I-address matched (SPANRANGE boundary), or document of origin. The orgl-dimension filter is permanently disabled (`TRUE||` guard), so document-of-origin cannot be an ordering criterion in practice [EC-FIND-LINKS-GLOBAL].

**Conclusion:**

The ordering is determined solely by spanfilade tree traversal combined with `incontextlistnd()` accumulation, but the KB provides no findings that specify which dimension's left boundary governs the sort, and no findings that confirm or deny stability across tree rebalancing events. Creation order, link ISA order, and document-of-origin order are all unaddressed by the KB. This question is not answerable from the KB as it stands.

## Code Exploration

I now have everything I need to give a complete, source-cited answer. Here is the full analysis:

---

## Ordering of `find_links` Results: Full Analysis

The short answer: **order is entirely determined by spanfilade tree traversal, keyed on the I-address (SPANRANGE) of the link's endpoint — not by link creation order, link ISA, or document of origin.** A secondary incidental effect causes links sharing the exact same I-span endpoint to appear in creation order (earliest first), but this is an unguaranteed artifact of two opposing mechanisms that happen to cancel.

---

### Call Chain

```
fns.c:findlinksfromtothree
  → do1.c:dofindlinksfromtothree          [do1.c:348-353]
    → spanf1.c:findlinksfromtothreesp      [spanf1.c:56-103]
      → sporgl.c:sporglset2linkset         [sporgl.c:222-237]
        → sporgl.c:sporglset2linksetinrange [sporgl.c:239-269]
          → retrie.c:retrieverestricted    [retrie.c:56-85]
            → retrie.c:retrieveinarea      [retrie.c:87-110]
              → retrie.c:findcbcinarea2d   [retrie.c:229-268]
                → context.c:incontextlistnd [context.c:75-111]
      → spanf2.c:intersectlinksets        [spanf2.c:46-120]
```

---

### Step 1: The Spanfilade Is 2D — ORGLRANGE × SPANRANGE

From `wisp.h:15-16`:
```c
#define ORGLRANGE 0
#define SPANRANGE 1
```

When a link endpoint is inserted via `insertspanf` [spanf1.c:22-51]:
```c
prefixtumbler (isaptr, spantype, &crumorigin.dsas[ORGLRANGE]);  // link ISA prefixed with from/to/three
movetumbler (&lstream, &crumorigin.dsas[SPANRANGE]);             // I-address of the endpoint
insertnd(taskptr,(typecuc*)spanfptr,&crumorigin,&crumwidth,&linfo,SPANRANGE);
```

So the spanfilade organizes entries by SPANRANGE (the endpoint I-address) as the primary dimension, with ORGLRANGE (prefixed link ISA) as the secondary.

---

### Step 2: Retrieval Uses SPANRANGE as the Sort Index

In `sporglset2linksetinrange` [sporgl.c:259]:
```c
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

This calls `retrieveinarea` → `findcbcinarea2d` with `index1 = SPANRANGE, index2 = ORGLRANGE`.

In `findcbcinarea2d` [retrie.c:252-265], at each leaf node:
```c
for (; crumptr; crumptr = getrightbro (crumptr)) {
    if (!crumqualifies2d (...)) continue;
    if (crumptr->height != 0) {
        findcbcinarea2d (findleftson ((typecuc*)crumptr), &localoffset, ...);  // recurse
    } else {
        context = makecontextfromcbc ((typecbc*)crumptr, (typewid*)offsetptr);
        incontextlistnd (headptr, context, index1);   // index1 = SPANRANGE
    }
}
```

**The sort key passed to `incontextlistnd` is `SPANRANGE`** — the I-address of the link's endpoint in the permascroll.

---

### Step 3: `incontextlistnd` Sorts by SPANRANGE

From `context.c:74-111`, with constants from `common.h:86-88`:
```c
#define TOMYLEFT       -2
#define ONMYLEFTBORDER -1
#define THRUME          0
```

```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd (c, &grasp, (typedsp*)NULL);
    ...
    /* on beginning */
    if (whereoncontext (clist, &grasp.dsas[index], index) < THRUME) {  // < 0, i.e., TOMYLEFT or ONMYLEFTBORDER
        c->nextcontext = clist;
        *clistptr = c;
        return(0);
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            /* in middle */
            if ((whereoncontext (clist, ...) > ONMYLEFTBORDER)
                && (whereoncontext (nextc, ...) < ONMYLEFTBORDER)) {
                ...insert between clist and nextc...
            }
        }
    }
    /* on end */
    clist->nextcontext = c;
}
```

This maintains the context list in ascending SPANRANGE order. A new context is placed before any existing entry whose left border equals the new context's start position (because `ONMYLEFTBORDER (-1) < THRUME (0)` triggers the "insert at beginning" branch). This makes **same-start entries accumulate via prepend**.

---

### Step 4: Link List Built from Sorted Context List

Back in `sporglset2linksetinrange` [sporgl.c:263-267]:
```c
for (c = context; c; c = c->nextcontext) {
    beheadtumbler(&c->totaloffset.dsas[ORGLRANGE],&linksa);  // extract link ISA
    onlinklist (taskptr, linksetptr, &linksa);                // append to link list
}
```

`onlinklist` [spanf2.c:26-44] appends with duplicate-checking but **does not sort**:
```c
for (temp = *linksetptr; nextlink = temp->next; temp = nextlink) {
    if (tumblereq (&temp->address, linkisaptr))
        return(0);   // skip duplicate
}
temp->next = linkset;   // append to end
```

So the link list inherits the SPANRANGE sort order of the context list.

---

### Step 5: Secondary Tie-Break — Same I-Span Endpoints

When two links share the exact same endpoint I-span, the relative ordering results from two opposing mechanisms:

**Insertion (`insertcbcnd` [insertnd.c:260-262]):**
```c
new = createcrum (0, (INT)father->cenftype);
reserve (new);
adopt (new, SON, (typecorecrum*)father);   // SON = LEFTMOSTSON (enf.h:137)
```

`SON = LEFTMOSTSON` [enf.h:137], so newly created crums become the **leftmost** sibling. `findcbcinarea2d` traverses **left-to-right** via `getrightbro`, so more recently created links are encountered **first**.

**Context list insertion (`incontextlistnd`):**  
For contexts with the same SPANRANGE start, each new one is **prepended before the current head** (ONMYLEFTBORDER < THRUME). So if traversal encounters L2 (recently created, leftmost) before L1 (older, rightmost):
- Process L2: list = [C2]
- Process L1: same start → prepend → list = [C1, C2]

The two effects cancel: reverse traversal order + reverse context-list insertion = **forward creation order** for same-I-span links. L1 (created first) appears before L2 (created later).

**This is an implementation artifact, not a design guarantee.**

---

### Step 6: Intersection — Order Follows the Primary List

In `findlinksfromtothreesp` [spanf1.c:56-103], after building per-endpoint link sets, `intersectlinksets` [spanf2.c:46-120] combines them.

When only one endpoint constraint is specified:
```c
if (linkset1 && !linkset2 && !linkset3)
    *linkset4ptr = linkset1;    // returns the list unchanged
```

When two or three endpoints are specified, temp1 (the "from" list, or whichever is set) drives the result order [spanf2.c:96-104]:
```c
for (; temp1; temp1 = temp1->next) {
    for (temp2 = linkset2; temp2; temp2 = temp2->next) {
        if (tumblereq (&temp1->address, &temp2->address)) {
            linkset4 = makelinkitem (taskptr, &temp1->address);
            *linkset4ptr = linkset4;
            linkset4ptr = &linkset4->next;
        }
    }
}
```

The intersection result follows `temp1`'s order. `temp2` and `temp3` only determine membership.

---

### Definitive Answer

| Ordering criterion | Guaranteed? | Source |
|---|---|---|
| By SPANRANGE (I-address of link endpoint) | **Yes** — implicit, via `incontextlistnd` | `retrie.c:263`, `context.c:75-111` |
| By link creation order | **No** — incidental artifact for same-I-span only | `insertnd.c:262` + `context.c:90` |
| By link ISA (ORGLRANGE) | **No** — ORGLRANGE is not the sort key | `retrie.c:263` passes `index1=SPANRANGE` |
| By document of origin | **No** — no such logic exists anywhere in this path | — |

**The order is determined solely by spanfilade tree traversal.** The spanfilade is organized primarily by the I-address (SPANRANGE) of the link's endpoint. Results emerge in ascending permascroll order of the endpoint I-address. For multiple links whose endpoints overlap the same I-span exactly, traversal order is incidentally equivalent to creation order (earliest first), but only because `insertcbcnd`'s LEFTMOSTSON placement and `incontextlistnd`'s same-start prepend behavior happen to cancel each other out. No code in this path sorts by creation time, link ISA, or document of origin.
