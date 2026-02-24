# Consultation Answers — Document Lifecycle

**Inquiry:** What invariants govern document creation, ownership, and the relationship between documents in the docuverse? What does it mean to open, close, and create documents?
**Date:** 2026-02-24 02:40
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> When a new document is created, what permanent identity does the system assign, and can that identity ever be reused or reassigned to a different document?

### Nelson's Answer

## Document Identity: Assignment and Permanence

### What Identity Is Assigned

When a new document is created, the system assigns it a **permanent tumbler address** — a multi-part number within the universal addressing scheme. The CREATENEWDOCUMENT operation "creates an empty document. It returns the id of the new document" [LM 4/65].

The tumbler address encodes the document's position in the ownership hierarchy:

```
Node.0.User.0.Document.0.Element
```

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

The Document field itself identifies the document uniquely under its owner's account, and can be "continually subdivided, with new subfields in the tumbler indicating daughter documents and versions" [LM 4/29].

### How Identity Is Assigned

New document addresses are created through what Nelson calls **baptism** — the owner of an account designates new addresses by forking:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Documents are created sequentially under an account: if user 1.2 creates three documents, they become 1.2.0.1, 1.2.0.2, 1.2.0.3 — successive digits forked under the owner's number.

### Can the Identity Be Reused or Reassigned?

**No.** The design makes reuse structurally impossible through three reinforcing mechanisms:

**1. The permanence guarantee.** Nelson states this as a foundational property of the addressing system:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

If an address could be reassigned to a different document, it would no longer "remain valid" as a reference to the original — violating this guarantee.

**2. The forking mechanism is append-only.** New addresses are created by successive forking (2.1, 2.2, 2.3...). The process only moves forward. There is no "reclaim" or "reassign" operation in the protocol. CREATENEWDOCUMENT returns the *next* available address; it does not recycle old ones.

**3. I-space content is permanent.** Any content created under a document's address lives permanently in I-space:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

Even "deleted" bytes remain in I-space, "awaiting historical backtrack functions" [LM 4/9]. If a document address were reassigned, the original I-space content would become orphaned or ambiguous — contradicting the guarantee that "you always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40].

**4. Publication creates binding obligations.** Once published, a document's address becomes a dependency for others:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

Links made by other users point to the document's address. Reassigning that address would break their links — violating both the link survivability and non-destruction guarantees.

### Summary

A document receives a permanent tumbler address at creation, determined by sequential forking under the owner's account. That address can never be reused or reassigned. This is not merely a policy choice but a structural consequence of the addressing design: the forking mechanism only advances, I-space content is immutable, and the permanence guarantee requires that every address remain valid forever. Gaps left by unused or abandoned addresses are permanent — the cost of guaranteeing that every reference, once made, works indefinitely.

---

## Question 2 [nelson]

> What does ownership of a document mean — does the owner have exclusive control over its content, or only over who may modify it?

### Nelson's Answer

# Ownership in Xanadu: What It Means

Ownership grants **exclusive modification rights** but explicitly does **not** grant exclusive control over how content is used once published. Nelson draws a sharp line between modifying your document and controlling what others do with it.

## What the Owner Controls

**Modification is absolute.** Only the owner may change a document's content:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This covers all editing operations: INSERT, DELETE, REARRANGE, COPY-into, and APPEND.

**Out-links are under owner control.** The document's outgoing connections belong to the owner:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

**Address space is permanently owned.** The owner controls subdivision of their address range forever:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

**Privacy designation** is the owner's choice — documents are either private (owner and designees only) or published (everyone).

## What the Owner Does NOT Control

Publication creates binding obligations that **limit** the owner's control. These are not bugs — they are the design.

**Cannot prevent linking.** Others may link to your published work freely, and you relinquished the right to stop them:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

**Cannot prevent quotation.** Anyone may window (transclude) your published content:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

**Cannot easily withdraw published work.** Publication is nearly irrevocable:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

**Cannot prevent derivative versions.** Anyone can create a new document that windows your content with modifications:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

**Cannot control terminal use.** What happens after bytes are delivered is beyond the owner's reach:

> "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate, and anyone who plans to be vulnerable to 'misuse,' whatever he or she thinks that may be, had better keep his or her stuff off the system." [LM 2/47]

## The Tradeoff Is Explicit

Nelson separates the two goals of traditional copyright — **compensation** and **control** — and keeps only the first:

- You give up control over how your published work is used
- You never give up compensation for its use (automatic per-byte royalty)
- The system enforces payment, not permission

Link ownership follows the same principle. A link's home document determines who owns the link, not what the link points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

So Bob's annotation link pointing at Alice's document is Bob's property at Bob's address. Alice cannot delete it, even though it points into her work.

## Summary

| Right | Owner has it? |
|-------|--------------|
| Modify content | Yes — exclusive |
| Control out-links | Yes — exclusive |
| Subdivide address space | Yes — permanent |
| Set private/published | Yes |
| Withdraw private documents | Yes |
| Prevent incoming links | **No** — relinquished on publication |
| Prevent quotation/transclusion | **No** — pre-granted on publication |
| Withdraw published documents | **No** — except by lengthy due process |
| Prevent derivative versions | **No** — others can version freely |
| Control terminal-side use | **No** — explicitly beyond reach |

Ownership means: **you alone may change it, but once published, you cannot stop the world from using it.** The compensation flows automatically; the control does not.

---

## Question 3 [nelson]

> When a new version of a document is created, what is the relationship between the original and the new version — are they the same document or distinct documents with a shared history?

### Nelson's Answer

# Versions: Same Document or Distinct Documents?

The answer is **both, by design**. Nelson deliberately constructed a model where versions are simultaneously distinct documents with independent identities and manifestations of a single evolving entity with shared content. The tension is not a contradiction — it is the architecture.

## Versions Are Distinct Documents

CREATENEWVERSION is defined as creating a **new document**:

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document." [LM 4/66]

The new version receives its own tumbler address, its own ownership, and its own V-space arrangement. It is a first-class document in every operational sense — it can be independently edited, linked to, published, and managed.

## But Their Addresses Encode Ancestry

The returned address reveals the relationship:

> "The new document's id will indicate its ancestry." [LM 4/66]

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." [LM 4/29]

If document `1.0.2.0.5` is versioned, the new document might be `1.0.2.0.5.1` — a sub-address beneath the original. The ancestry is legible in the address itself.

Yet Nelson immediately qualifies this:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

The address structure *suggests* ancestry but does not *enforce* a specific derivation semantics. The numbering is a naming convention, not a semantic constraint.

## They Share I-Space Content

This is the deepest sense in which versions are "the same." CREATENEWVERSION does not copy content — it creates a new V-space arrangement that references the same I-space addresses as the original. The new version transcludes the entirety of the source document.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The new version's V-stream maps to I-addresses that belong to the original document. No new content bytes are created. The two documents share content identity, not just content value.

## No Version Is Primary

Nelson explicitly rejects the idea of a "main" version:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

He calls this **prismatic storage**:

> "We call this system of storage Prismatic because we may think of a given part, or section, as being prismatically refracted when we pass from one version to another." [LM 2/19]

All versions are equally valid views of a shared body of content, like light refracted through a prism into different spectra.

## Correspondence Makes Versions Navigable as One

Because versions share I-addresses, the system can compute which parts of one version correspond to which parts of another — automatically, without metadata:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

And links made to one version reach through to all versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

A link to version 1 is effectively a link to the same passage in version 7, if that passage still exists — because the link points to I-space content that both versions share.

## The "Ongoing Braid" Metaphor

Nelson's own metaphor resolves the apparent paradox:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." [LM 2/15]

The braid is one entity that grows through time. Each version is a cross-section of the braid at a particular moment. The cross-sections are distinct (different V-space arrangements), but the braid is continuous (shared I-space content, structural correspondence, refractive link following).

## Versioning by Inclusion

Even third-party versions work the same way:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." [LM 2/37]

Whether you version your own document (CREATENEWVERSION) or build a derivative of someone else's (windowing with modifications), the result is a distinct document that shares I-space content with its source. The mechanism is the same.

## Summary

| Aspect | Same or Distinct? |
|--------|-------------------|
| Tumbler address | **Distinct** — each version has its own address |
| Ownership | **Distinct** — each version has its own owner |
| V-space arrangement | **Distinct** — each version arranges content independently |
| I-space content | **Shared** — both reference the same permanent bytes |
| Correspondence | **Structural** — shared I-addresses make comparison automatic |
| Link traversal | **Unified** — links refractively follow across versions |
| Ontological status | **Equal** — no version is privileged as "the" document |

Nelson's design says: a version is a new document in every operational sense (own address, own owner, own arrangement), but it shares content identity with its source, and the system treats the family of versions as navigable facets of a single evolving literary entity. The docuverse is, after all, "all really one big forking document" [LM 4/18].

---

## Question 4 [nelson]

> Must the system guarantee that creating a new document leaves every existing document completely unchanged — its content, its links, its versions?

### Nelson's Answer

## Yes — by architectural necessity, not by explicit axiom

Nelson never states a single proposition like "CREATENEWDOCUMENT leaves all existing documents unchanged." But this guarantee follows from the convergence of several explicit design principles, each of which he does state.

### 1. Tumbler permanence guarantees address stability

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Creating a new document allocates a new tumbler address by forking — adding sub-digits to the owner's address. This cannot disturb existing addresses because the forking mechanism is explicitly designed to insert without invalidating:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

### 2. Ownership prohibits cross-document mutation

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

If creating document B could alter document A, this would violate ownership — B's creator might not own A. The ownership guarantee implicitly requires that document creation is a local operation with no side effects on other owners' property.

### 3. I-space immutability guarantees content preservation

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

I-space content is permanent and immutable. Creating a new document (even CREATENEWVERSION, which shares I-addresses with its source) does not modify existing I-space content. The new document creates a new V-space arrangement that references the same permanent I-space bytes. The source document's arrangement is untouched.

### 4. Non-destruction is an explicit guarantee

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

This is stated in the context of versioning by inclusion, but the principle is general: creating new documents never damages existing ones.

### 5. Links are unaffected

Creating a document (CREATENEWDOCUMENT) creates an empty document with no links. Even CREATENEWVERSION does not create links — it creates a new V-space arrangement over shared I-space content. No existing document gains or loses links from document creation.

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end)." [LM 4/41]

Links are created explicitly by users through MAKELINK, not as side effects of document creation.

### The architectural reason

The deeper answer is that Xanadu's I-space/V-space separation makes cross-document interference architecturally impossible for creation operations:

- **I-space** is append-only — new content is added; existing content is never modified
- **V-space** is per-document — each document has its own arrangement; no document's V-space references or depends on another document's V-space
- **Tumblers** are tree-structured — new addresses fork from existing ones without disturbing siblings

Nelson designed this deliberately. The entire system rests on the principle that content, once created, is permanent and undisturbed:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Summary

The guarantee holds for content, links, and versions alike. It is not stated as a single axiom but follows necessarily from permanence (addresses never break), ownership (only the owner modifies), immutability (I-space never changes), and non-destruction (originals are never damaged). Nelson's architecture makes it structurally impossible for document creation to have side effects on existing documents.

---

## Question 5 [nelson]

> What does it mean to "open" a document — does opening grant the user a private working copy, or does it expose the shared permanent original?

### Nelson's Answer

# "Opening" a Document in Xanadu

## Short Answer

Nelson does not specify an "open" operation. The concept does not exist in Literary Machines. There is no session model, no open/close lifecycle, and no private working copy. You interact directly with the shared permanent original — always.

## The FEBE Protocol Has No OPEN Command

The session-model extraction states this definitively:

> "Nelson does not specify a session model. The term 'BERT' does not appear in Literary Machines."

And more specifically:

> "No OPEN/CLOSE operations — Nelson's 17 commands establish no session state on a document."

The 17 FEBE commands are all stateless operations against document addresses. You name a document by its tumbler address, issue a command, and the back end responds. There is no prerequisite of "opening" the document first.

Nelson himself frames this as:

> "What the Xanadu storage and hypertext system does — and thus is — is defined by the commands to which it responds." [LM 4/61]

Those commands are INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND, RETRIEVEV, MAKELINK, and so on. None of them require prior session establishment on the target document.

## Reading: You Access the Shared Original Directly

When you read, you issue RETRIEVEV with a spec-set (a set of tumbler spans). The system returns the content from its permanent location. Nelson describes this as "part-pounce":

> "You pounce like a cat on a given thing, and it seems to be there, having been constructed while you wait, as it were, in midair." [LM 2/16]

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

There is no intermediate copy. The content is assembled on demand from the permanent I-space store and the document's V-space arrangement, then delivered to you. You are seeing the shared permanent original, reconstructed for your view.

## Writing: You Modify the Original OR Create a Version

Nelson's access model is binary, not modal:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

If you **own** the document, your modifications (INSERT, DELETE, REARRANGE) apply directly to it. There is no "checked out copy" — you are editing the shared original's V-space arrangement. But because I-space is append-only, all previous states remain accessible:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If you **do not own** the document, you cannot modify it. Instead, you create a new version:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

CREATENEWVERSION gives you a new document that transcludes the original's content. This new document is yours — at your address, under your control. But it is not a "private working copy" in the traditional sense. It is a new, permanent, independently addressable document in the docuverse.

## Why "Private Working Copy" Is Alien to the Design

The file-open paradigm assumes:
1. Open file → get private mutable copy
2. Edit copy in isolation
3. Save → overwrite shared original
4. Close → discard working state

Every step contradicts Nelson's architecture:

- **Step 1**: There are no copies. Content exists once in I-space. Documents are V-space arrangements over that content.
- **Step 2**: Edits are not isolated. They change the document's V-space arrangement directly.
- **Step 3**: There is no "save" that overwrites. I-space is append-only: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14] — Nelson designed Xanadu specifically to abolish this.
- **Step 4**: There is no state to discard. Every edit is permanent.

## What About Concurrency?

Nelson does not address concurrent editing of the same document. The session-model extraction notes:

> "No locking protocol — no mention of concurrent editing of the same document."

The implementation-level BERT mechanism (OPEN, CLOSE, READBERT, WRITEBERT, lock table, auto-branching on denial) is entirely Gregory's design, not Nelson's. It is consistent with Nelson's intent — particularly the principle that "writing always succeeds" through automatic version creation — but it is not specified in Literary Machines.

## Summary

| Question | Answer |
|----------|--------|
| Does Nelson specify "open"? | No. The term and concept are absent from FEBE. |
| Do you get a private copy? | No. You access the shared permanent original. |
| What happens when you read? | RETRIEVEV fetches from the permanent original. |
| What happens when you write (owner)? | Modifications apply directly to the original's V-space. |
| What happens when you write (non-owner)? | CREATENEWVERSION creates a new permanent document. |
| Is BERT/OPEN Nelson's design? | No. It is Gregory's implementation of the session layer Nelson left unspecified. |

The deepest point: in Xanadu, the question "private copy or shared original?" is a false dichotomy born from the file-system paradigm. Every document is both shared (accessible by address) and permanent (all states preserved). There is nothing to "open" because there is nothing to "close" — documents exist perpetually in the docuverse, and you interact with them by naming them and issuing commands.

---

## Question 6 [nelson]

> Can a document exist with no content at all, or must document creation always establish some initial content?

### Nelson's Answer

## A Document Can Exist With No Content

Nelson answers this directly through the CREATENEWDOCUMENT operation:

> "This creates an empty document. It returns the id of the new document." [LM 4/65]

The protocol explicitly creates a document with **zero content** — no bytes, no links. The document exists as a valid, addressable entity in the docuverse before any content is added.

## Why This Makes Architectural Sense

The ghost elements concept reinforces this. A document is fundamentally a **position on the tumbler line**, not a container that must hold something:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

A freshly created empty document is a "baptized" address — it has been claimed by an owner and assigned a permanent tumbler — but nothing is stored under it yet. It occupies a position between a ghost element (which has never been explicitly created) and a populated document.

## The Document Is the Address, Not the Content

Nelson's architecture separates identity from content. A document's existence is established by its tumbler address and ownership, not by whether it contains bytes:

> "The Xanadu document is the unit of the system. There is almost nothing in the Xanadu system but Xanadu documents." [LM 4/6]

> "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]

The typical workflow is: CREATENEWDOCUMENT (empty), then INSERT to add content. The document exists — owned, addressable, linkable — in the interval between creation and first insertion.

## Can Others Link To an Empty Document?

Yes. Since links point to tumbler addresses and link types can be ghost elements, there is no architectural barrier to linking to an empty document. The document address is valid from the moment of creation. Content can arrive later.

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

If you can link to a *node* or *account* with no stored content, you can certainly link to a created document that happens to be empty.

## Summary

Document creation establishes **identity and ownership**, not content. An empty document is a first-class entity: permanently addressed, owned, and linkable. Content is added subsequently through INSERT, APPEND, or COPY operations.

---

## Question 7 [nelson]

> When multiple users share a document, what guarantees govern simultaneous modification — must one user's changes be invisible to another until explicitly published?

### Nelson's Answer

# Simultaneous Modification in Xanadu

## The Short Answer

Nelson's design largely **sidesteps** the simultaneous modification problem through the ownership model. There is no specified concurrency protocol, no locking mechanism, and no isolation semantics in Literary Machines. The architecture makes the question mostly moot by restricting modification to a single owner.

## Ownership Eliminates Most Concurrent Modification

The foundational rule is singular ownership:

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." [LM 2/29]

This means "multiple users modifying the same document" is **not a scenario Nelson envisions**. If you want to modify someone else's document, you don't edit it — you create your own:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

## Writing Always Succeeds (Through Forking)

When you cannot modify a document (because you're not the owner), the system doesn't return an error — it redirects you to create a version:

> "Thus users may also republish documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." [LM 2/45]

CREATENEWVERSION creates a new document that transcludes the original's content, giving you your own copy to modify. Your changes live at YOUR address, under YOUR control. The original is untouched.

## Private vs. Published Governs Visibility

The visibility model is binary, not graduated:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

Your modifications to your own documents are **private by default** until you explicitly publish. Publication is a "solemn event" requiring contractual agreement — not something that happens automatically or incrementally.

> "Because publication is an important act, both for authors and readers, we make publication a solemn event, to be undertaken cautiously." [LM 2/42]

So in this sense, yes — one user's changes ARE invisible to others until explicitly published. But this isn't a concurrency mechanism; it's the basic privacy/publication model.

## What Nelson Does NOT Specify

The session model extraction makes this explicit — Nelson leaves unspecified:

- **No OPEN/CLOSE operations** — the 17 FEBE commands establish no session state
- **No read vs. write modes** — you own it (modify freely) or you don't (create a version)
- **No locking protocol** — no mention of concurrent editing of the same document
- **No session lifecycle** — no connect/authenticate/disconnect sequence
- **No transaction semantics** — no isolation levels, no commit/rollback

Nelson's protocol is stateless at the command level: you name a document by tumbler address, issue a command, the back end responds.

## The Multi-User Read Case

Nelson does briefly address multiple simultaneous *readers*:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." [LM 4/59]

But this concerns read performance optimization, not modification consistency.

## The Implementation Gap

The BERT (Back-End Request Token) mechanism — with OPEN, CLOSE, READBERT, WRITEBERT, lock tables, and denial-as-branching — is entirely Gregory's implementation invention, not Nelson's specification. Nelson's 17 FEBE commands include no session management. Gregory built BERT to handle the practical concurrency question Nelson left open, with the elegant property that write-denial triggers automatic version creation (consistent with Nelson's "writing always succeeds" principle).

## Summary

| Question | Nelson's Answer |
|----------|----------------|
| Can multiple users modify the same document? | **No** — only the owner modifies |
| What do non-owners do? | Create their own versions via CREATENEWVERSION |
| Are changes invisible until published? | **Yes** — private documents are owner-only; publication is explicit |
| What concurrency guarantees exist? | **None specified** — left to implementation |
| What about the owner editing from two terminals? | **Not addressed** |
| What about designees? | Can READ private documents, but modification is owner-only |

The design philosophy is clear: rather than solving concurrent modification with locks and isolation levels, Nelson eliminates the problem through ownership. Each person controls their own documents. "Collaboration" happens through transclusion, versioning, and linking — not through shared mutable state.

---

## Question 8 [nelson]

> Once a document has been created and published, can it ever be destroyed or made permanently inaccessible, or does permanence forbid this?

### Nelson's Answer

# Can a Published Document Be Destroyed?

The short answer: **permanence strongly forbids it, but Nelson does not make it absolutely impossible.** He provides a narrow exception through "lengthy due process" and one specific mechanism (peremptory challenge) for anonymous defamatory content.

## The General Rule: Published Means Permanent

Nelson is emphatic that publication creates a permanence obligation:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural, not merely philosophical. Other users will have linked to the document, and those links are **their property**:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Withdrawal would destroy other people's links — their intellectual property, created at their addresses, under their ownership. This is why permanence is not merely a preference but a contractual obligation accepted at the moment of publication.

## The Three Exceptions

### 1. "Lengthy Due Process"

Nelson acknowledges withdrawal is not absolutely forbidden — just extremely difficult:

> "Consequently its author may not withdraw it **except by lengthy due process.**" [LM 2/43]

He does not specify what this process looks like, but the phrase implies something analogous to legal proceedings — formal, slow, and with high barriers. The intent is clearly to make withdrawal rare and costly, not impossible.

### 2. Peremptory Challenge (Anonymous Content Only)

For anonymous ("John Doe") publication, Nelson provides a specific removal mechanism:

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

This applies only when the publisher is anonymous and absent. For accountable publishers (identified individuals or firms), peremptory challenge "no longer holds water" — removal would require negotiation or court order.

### 3. Privashing (Avoiding Permanence Entirely)

Nelson provides an explicit escape hatch for authors who want reach without permanence:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/48]

The tradeoff is explicit: privashed documents earn no royalties, and anyone who linked to them has no recourse if the author withdraws. This makes the permanence obligation a **deliberate choice** accepted through the act of formal publication.

## Supersession, Not Destruction

Nelson's preferred mechanism for "updating" is not replacement but supersession. The old version stays; a new version is published alongside it with a supersession link:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version." [LM 4/52]

Readers are directed to the new version, but the old one remains accessible. This preserves all existing links while guiding users to current content.

## The Economic Tension

Nelson's funding model requires **ongoing storage rental** paid by the content owner [LM 4/5, 5/11]. He states that "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily" [LM 4/5].

Nelson does **not** specify what happens when storage rental lapses. This creates an unresolved tension: permanence demands that content persist forever, but the economic model requires someone to keep paying. The vendor contract does require orderly transition of customer data upon cancellation — "Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16] — but what happens if no one assumes the cost is unstated.

## Summary

| Scenario | Can content be removed? |
|----------|------------------------|
| Published document, author wants to withdraw | Only through "lengthy due process" |
| Anonymous defamatory content, author absent | Yes, via peremptory challenge |
| Privashed document (private + unrestricted) | Yes, at any time by owner |
| Superseded document | No — old version stays, new one linked |
| Storage vendor fails | Content transitions to other vendors |
| Storage rental lapses | **Unspecified** — genuine gap |

The design intent is clear: **permanence is the default, and destruction is the extraordinary exception.** Nelson treats published content as analogous to printed books in libraries — the author cannot recall copies from every shelf. But unlike physical books, the system is designed so that content need never decay, burn, or go out of print. The entire architecture exists to make the permanence guarantee technically achievable across centuries, including distribution to "deep rock and deep space—Iron Mountain or the asteroid belt" [LM 3/25].

---

## Question 9 [nelson]

> If document A includes content from document B through transclusion, and someone creates a new version of document B, must document A still show the original content it referenced?

### Nelson's Answer

## Yes — and the answer follows from Xanadu's deepest architectural principle.

### The I-Space Guarantee

Transclusion works through **I-space addresses**, which are permanent and immutable. When document A transcludes content from document B, A's V-stream contains references to I-space addresses that belong to B. Those I-space addresses **never change**, regardless of what happens to B's versions.

Nelson is explicit about this:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Creating a new version of B does not alter B's I-space content — it creates a new V-space arrangement over the same permanent bytes. Document A's references to those bytes remain valid.

From the I-space/V-space separation:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

A's transclusion fetches bytes from their **home locations** in B's I-space. Those locations are permanent. Versioning B only changes B's V-space arrangement — it cannot touch I-space.

### The Two Windowing Modes

However, Nelson introduces an important nuance about *how* A experiences B's evolving content. There are two modes of windowing:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

**Time-fixed window:** A sees B's content as it was at a specific moment. New versions of B exist but A's view is frozen. The user can ask "What has this passage become?" to see the current state.

**Location-fixed window:** A tracks B's current arrangement. If B's owner rearranges content in a new version, A's view updates accordingly.

In **both** cases, the original I-space content remains accessible. The distinction is about which V-space arrangement of B's content document A presents to readers.

### Why This Must Be So

The non-destruction guarantee is fundamental:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And the append-only storage model ensures it:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content is never overwritten. Versions are new arrangements, not replacements. The "ongoing braid" accumulates; it never unravels.

### Summary

| Scenario | Does A still show original content? |
|----------|-------------------------------------|
| New version of B created | Yes — I-space unchanged |
| Content deleted from B's current version | Yes — bytes remain in I-space |
| Content rearranged in B | Yes (time-fixed: frozen view) or rearranged view (location-fixed) |
| B's owner publishes corrections | Original still accessible; A can show either |

The original content is **always** recoverable because transclusion references permanent I-space addresses. What may vary is which *arrangement* of B's content document A chooses to present — but the underlying bytes are eternal.

---

## Question 10 [nelson]

> What is the relationship between a user's account and the documents they create — does the system permanently record who created each document, and can this attribution ever be severed?

### Nelson's Answer

## Account–Document Attribution in Xanadu

The relationship between a user's account and their documents is **structural and permanent**, encoded directly in the tumbler address itself. It cannot be severed by any operation within the system.

### The Address IS the Attribution

Every tumbler address has four major fields:

```
Node.0.User.0.Document.0.Element
```

The **User field** is an indelible part of every document's address and every byte's I-space address. Nelson:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." [LM 4/26]

The owner controls subdivision of their address space forever:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

Documents are created *under* an account by the forking mechanism:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This means a document at address `1.0.3.0.27` permanently records that it was created under account 3 on node 1. This is not metadata attached to the document — it is the document's identity.

### Attribution Cannot Be Severed

Nelson makes this guarantee explicit:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

The reason attribution is unseverable is architectural, not policy-based. Content is fetched from its **home location** — the I-space address that encodes its origin:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When content is transcluded into another document, it is not copied — it is referenced by its permanent I-address. The fetching mechanism itself requires knowing the origin. There is no operation that reassigns content to a different account or rewrites the User field of an address.

### Ownership vs. Authorship

Nelson distinguishes between the account that *owns* a document (structural, permanent) and the *author* (a social claim, potentially disputable):

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company)." [LM 2/29]

The parenthetical is important: the User field identifies the *account*, not necessarily the person who typed the words. A publishing company's account owns the document even if an employee wrote it.

Author metalinks provide a separate, social layer of attribution that *can* be disputed:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." [LM 4/52, footnote]

So: **account ownership** (encoded in the address) is permanent and unseverable. **Authorship claims** (expressed through metalinks) are social assertions that can be made, disputed, or supplemented by anyone.

### The Anonymous Publication Case

Nelson explicitly supports anonymous "John Doe publication" [LM 2/60], but even anonymous content gets a tumbler address with a User field. The content is structurally attributed to *some* account — the real-world identity behind that account is simply unknown. The system still knows which account created the document; it just doesn't know (or enforce knowing) who the account holder is.

### Summary

| Aspect | Permanent? | Severable? |
|--------|-----------|------------|
| Account ownership (User field in address) | Yes — part of the tumbler | No — no operation can change it |
| Document origin (I-space address) | Yes — append-only | No — content is fetched by origin address |
| Authorship claim (Author metalink) | Persistent but disputable | Can be supplemented or contested via links |
| Real-world identity behind account | Depends on account type | Anonymous accounts hide identity by design |

The system permanently records *which account* created each document, and this attribution cannot be severed — it is the address itself, not a label attached to it.

---

## Question 11 [gregory]

> When CREATENEWDOCUMENT allocates a document address under a user's account (e.g., `1.1.0.2.0.N`), does it use `findisatoinsertnonmolecule` with the same query-and-increment pattern as link allocation, and what is the upper bound tumbler it searches against?

### Gregory's Answer

## KB Synthesis

Yes, CREATENEWDOCUMENT uses `findisatoinsertnonmolecule` with the same query-and-increment pattern. Here is what the KB establishes:

## Mechanism

From [SS-ADDRESS-ALLOC] / [ST-ADDRESS-ALLOC] (Finding 0021), the general document allocation algorithm in `findisatoinsertnonmolecule` is:

1. Compute upper bound: `upperbound = tumblerincrement(hintisa, depth-1, 1)` — the next sibling of the parent address
2. Call `findpreviousisagr` to find the highest existing address below `upperbound`
3. Apply containment check: verify the found address is actually under `hintisa`
4. If no child exists: allocate `hintisa.0.1` (first-child convention)
5. If child exists: truncate and increment to produce the next sibling

## CREATENEWDOCUMENT Hint Parameters

From [SS-ADDRESS-SPACE] (Finding 0021), the depth table for `makehint`:

| supertype | subtype | depth | Meaning |
|-----------|---------|-------|---------|
| ACCOUNT | DOCUMENT | 2 | Document under account |

So for CREATENEWDOCUMENT: `makehint(ACCOUNT, DOCUMENT, 0, account_addr, &hint)` sets `depth=2`.

## Upper Bound Computation

With `depth=2`, the upper bound is:

```
upperbound = tumblerincrement(account_addr, depth-1, 1)
           = tumblerincrement(account_addr, 1, 1)
```

The `rightshift=1` increments at the second-to-last digit position, producing the next sibling account address. For account `1.1.0.2`, this yields `1.1.0.3`.

The search is therefore bounded to addresses below `1.1.0.3` — equivalently, within the `1.1.0.2.*` subtree. The containment check then confirms any candidate is actually under `1.1.0.2`.

## Concrete Example (from Finding 0021)

- Account `1.1.0.2`, no existing documents → upper bound `1.1.0.3`, `findpreviousisagr` finds nothing under `1.1.0.2` → allocates first child `1.1.0.2.0.1`
- Account `1.1.0.2`, existing document `1.1.0.2.0.1` → finds `1.1.0.2.0.1`, truncates and increments → allocates `1.1.0.2.0.2`

## Corroboration from Version Allocation

Finding 0068 [ST-VERSION-OWNERSHIP] confirms the same code path applies when a user versions a document they do not own — that path also uses `makehint(ACCOUNT, DOCUMENT, 0, ...)` and is described as "identical to CREATE behavior," lending additional support that CREATENEWDOCUMENT follows exactly this pattern.

**Summary**: CREATENEWDOCUMENT uses `findisatoinsertnonmolecule` with `depth=2` (ACCOUNT→DOCUMENT), producing `upperbound = tumblerincrement(account_addr, 1, 1)` — the next sibling of the account address. The search covers the account's entire child subtree. The KB establishes this through the general mechanism (Finding 0021) and the version-of-unowned-document case which explicitly uses identical hint parameters (Finding 0068). The KB does not contain a finding that inspects CREATENEWDOCUMENT's source directly; this is inferred from the shared allocation dispatch in `findisatoinsertgr`.

## Code Exploration

I now have all the pieces needed to give a complete, cited answer. Let me assemble it.

---

## Full Answer

### Call Chain from Protocol Entry to Address Allocation

**`fns.c:276–286`** — `createnewdocument()` dispatches to `docreatenewdocument`:

```c
void createnewdocument(typetask *taskptr)
{
    typeisa newdocisa;
    bool docreatenewdocument();

    getcreatenewdocument();
    if (docreatenewdocument (taskptr, &newdocisa))
        putcreatenewdocument (taskptr, &newdocisa);
    else
        putrequestfailed (taskptr);
}
```

---

### Step 1 — `docreatenewdocument` builds the hint and calls `createorglingranf`

**`do1.c:234–241`**:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
    typehint hint;
    bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

`makehint` is defined at **`do2.c:78–84`** and simply stores the arguments into the hint struct:

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;   // ACCOUNT = 2
    hintptr->subtype   = typebelow;   // DOCUMENT = 3
    hintptr->atomtype  = typeofatom;  // 0
    movetumbler (isaptr, &hintptr->hintisa); // user's account tumbler, e.g. 1.1.0.2
}
```

Type constants confirmed at **`xanadu.h:140–143`**:

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
```

So the hint is `{supertype=ACCOUNT, subtype=DOCUMENT, atomtype=0, hintisa=<user account>}`.

---

### Step 2 — `createorglingranf` passes through to `createorglgr`

**`granf1.c:50–55`** — a thin wrapper:

```c
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr)
{
    bool createorglgr();
    return (createorglgr(taskptr, granfptr, hintptr, isaptr));
}
```

---

### Step 3 — `createorglgr` calls `findisatoinsertgr` to allocate the address

**`granf2.c:111–128`**:

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typegranbottomcruminfo locinfo;
    bool findisatoinsertgr();
    typecuc *createenf();

    if (!findisatoinsertgr ((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf (POOM);
    ...
    insertseq ((typecuc*)fullcrumptr, isaptr, &locinfo);
    ...
    return (TRUE);
}
```

The allocated `isaptr` is what becomes the new document's address.

---

### Step 4 — `findisatoinsertgr` routes by `subtype`

**`granf2.c:130–156`**:

```c
bool findisatoinsertgr(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    bool isaexistsgr();

    if (hintptr->subtype == ATOM) {
        if (!isaexistsgr (fullcrumptr, &hintptr->hintisa)) { ... return FALSE; }
        findisatoinsertmolecule (fullcrumptr, hintptr, isaptr);
    } else {
        findisatoinsertnonmolecule (fullcrumptr, hintptr, isaptr);
    }
    tumblerjustify(isaptr);
    return (TRUE);
}
```

Because `hint.subtype == DOCUMENT (3) != ATOM (4)`, the `else` branch is taken.

**CREATENEWDOCUMENT does use `findisatoinsertnonmolecule`.** ✓

---

### Step 5 — `findisatoinsertnonmolecule`: the full allocation algorithm

**`granf2.c:203–242`**:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    typeisa upperbound, lowerbound, truncated;
    INT depth, hintlength;
    bool lowerbound_under_hint;

    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
    // ACCOUNT(2) != DOCUMENT(3) → depth = 2

    hintlength = tumblerlength (&hintptr->hintisa);
    // e.g. 4 for account 1.1.0.2

    tumblerincrement (&hintptr->hintisa, depth - 1, 1, &upperbound);
    // depth - 1 = 1; see analysis below

    clear (&lowerbound, sizeof(lowerbound));
    findpreviousisagr ((typecorecrum*)fullcrumptr, &upperbound, &lowerbound);

    lowerbound_under_hint = FALSE;
    if (!iszerotumbler(&lowerbound)) {
        tumblertruncate(&lowerbound, hintlength, &truncated);
        lowerbound_under_hint = tumblereq(&truncated, &hintptr->hintisa);
    }

    if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
        /* Nothing under this hint - first child = hintisa.0.1 */
        tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
        // depth = 2 → appends 0.1
    } else {
        tumblertruncate (&lowerbound, hintlength + depth, isaptr);
        tumblerincrement(isaptr, tumblerlength(isaptr)==hintlength ? depth : 0, 1, isaptr);
    }
}
```

---

### The Upper Bound Calculation

`tumblerincrement` is defined at **`tumble.c:599–623`**:

```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    register INT idx;

    if (iszerotumbler (aptr)) { cptr->exp = -rightshift; cptr->mantissa[0] = bint; return; }
    if (aptr != cptr) movetumbler(aptr,cptr);
    for (idx = NPLACES ; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx = index of last non-zero digit in mantissa
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify (cptr);
}
```

**Semantics:** find the last significant digit position (`idx`), then add `bint` at position `idx + rightshift`. With `rightshift=1`, this appends one additional digit-slot to the right.

For account `1.1.0.N` (mantissa `[1, 1, 0, N, 0, ...]`, last nonzero at `idx=3`):

```
upperbound = tumblerincrement(1.1.0.N, rightshift=1, bint=1)
           → mantissa[3 + 1] += 1
           → mantissa[4] = 1
           → 1.1.0.N.1
```

**The upper bound is `1.1.0.N.1`** (one level deeper than the account address, with value 1).

All document addresses under that account have the form `1.1.0.N.0.M` (M ≥ 1), which are all numerically less than `1.1.0.N.1` (at the 5th component: `0 < 1`), so `findpreviousisagr` correctly retrieves the highest existing document under the account.

---

### Comparison with Link Allocation

The question asks whether the document pattern matches link allocation. They share the query-and-increment *structure* but use **different functions**:

| Operation | `makehint` call (`do1.c`) | `subtype` | Route in `findisatoinsertgr` | Upper bound formula |
|---|---|---|---|---|
| CREATENEWDOCUMENT | `makehint(ACCOUNT, DOCUMENT, 0, accountisa)` | DOCUMENT (3) | **`findisatoinsertnonmolecule`** | `tumblerincrement(accountisa, depth-1=1, 1)` → `accountisa.1` |
| CREATELINK | `makehint(DOCUMENT, ATOM, LINKATOM, docisa)` | ATOM (4) | **`findisatoinsertmolecule`** | `tumblerincrement(docisa, 2, atomtype+1=3)` → `docisa.0.3` |

Links route to `findisatoinsertmolecule` (`granf2.c:158–181`) because `ATOM == ATOM`. Documents route to `findisatoinsertnonmolecule` because `DOCUMENT != ATOM`.

`findisatoinsertmolecule` also calls `findpreviousisagr`, so the top-level pattern (search backwards from an upper bound, then increment) is shared — but the upper bound and increment logic differ.

---

### Summary

1. **Yes**, CREATENEWDOCUMENT allocates via `findisatoinsertnonmolecule` (`granf2.c:203`), reached through: `fns.c:282` → `do1.c:240` → `granf1.c:54` → `granf2.c:117` → `granf2.c:152`.

2. **The upper bound** is `tumblerincrement(&accountisa, depth-1=1, 1)` = **`accountisa.1`** — for account `1.1.0.2` the upper bound is `1.1.0.2.1`. (`tumble.c:621`: `mantissa[idx + rightshift] += bint`, where `rightshift=1`.)

3. The **query-and-increment pattern** is the same at the structural level as link allocation (find highest ISA below the upper bound, then increment to get the next free slot), but CREATENEWDOCUMENT dispatches to `findisatoinsertnonmolecule` while CREATELINK dispatches to `findisatoinsertmolecule`. These are sibling functions with different upper bound arithmetic — not the same function.

---

## Question 12 [gregory]

> What is the initial state of a freshly created document's POOM — is it an empty enfilade tree with a root node already allocated, or is the orgl created lazily on first INSERT?

### Gregory's Answer

## KB Synthesis

A freshly created document's POOM is **eagerly initialized** — a root node and bottom crum are allocated at document creation time, not lazily on first INSERT.

## Evidence

**[SS-ENFILADE-TREE] Finding 0058** is the direct answer:

> `createenf(POOM)` produces a minimal height-1 tree: a fullcrum with `isapex=TRUE`, `height=1`, containing a single bottom node (height-0) with zero width.

Code reference: `backend/credel.c:492-516` — `createenf`.

The zero width means the tree is logically empty (no content mapped), but the structure is physically present: one fullcrum with one zero-width bottom node.

## The "Never-Filled" vs "Delete-Everything" Distinction

**[EC-EMPTY-DOC] Finding 0058** makes the structural distinction explicit:

| State | Height | Fullcrum sons | Bottom nodes |
|-------|--------|---------------|--------------|
| Never-filled (`createenf`) | 1 | 1 (zero-width bottom) | 1 |
| After delete-everything | H (from prior growth) | 2+ (empty intermediates) | 0 |

Both states satisfy `is_empty(doc) ≡ dom(poom(doc)) = ∅`, but they are structurally non-equivalent. The never-filled state has a bottom crum; the delete-everything state does not.

This distinction is consequential: `firstinsertionnd()` assumes a bottom crum always exists. After delete-everything removes all bottom crums via `disown` + `subtreefree`, any subsequent INSERT or VCOPY crashes (Bug 0019) because `findleftson()` returns NULL. This confirms the initial bottom crum is load-bearing for the insertion code path, not merely decorative.

## When Is the POOM Created?

**[SS-GRANF-OPERATIONS] Finding 0012** identifies `createorglingranf()` as the primitive that creates new orgls (for both documents and links). **[ST-VERSION-CREATE] Finding 0032** shows this is called as step (1) of `docreatenewversion`. The same call creates document orgls during `CREATENEWDOCUMENT`.

`createorglingranf` allocates an orgl entry in the granf, and that allocation includes initializing the POOM enfilade via `createenf(POOM)`.

## Summary

The POOM is eagerly initialized at document creation. A fresh document has:
- A height-1 fullcrum (`isapex=TRUE`)
- One zero-width bottom node (`height=0`, `infotype=GRANNULL`)
- Both `cdsp = 0` and `cwid = 0` (satisfies `isemptyenfilade` check per **[EC-EMPTY-DOC] Finding 0066**)

The initial state is NOT the same as the post-delete-all state — `createenf` must be distinguished from "logically empty after operations."

## Code Exploration

I now have a complete picture. Here is the full answer.

---

## Answer: The POOM Is Allocated Eagerly, At Document Creation Time

### Call Chain

**`fns.c:282`** — `createnewdocument` receives the FEBE request and calls:

```c
docreatenewdocument(taskptr, &newdocisa)
```

**`do1.c:234-241`** — `docreatenewdocument` builds a hint and calls:

```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
return (createorglingranf(taskptr, granf, &hint, isaptr));
```

**`granf1.c:50-55`** — `createorglingranf` immediately delegates:

```c
return (createorglgr(taskptr, granfptr, hintptr, isaptr));
```

**`granf2.c:111-128`** — `createorglgr` is where the POOM is born:

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
  typegranbottomcruminfo locinfo;

  if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))
      return (FALSE);
  locinfo.infotype = GRANORGL;
  locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // ← POOM created here
  reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
  locinfo.granstuff.orglstuff.orglincore = TRUE;
  locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
  insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);       // stored in granfilade
  rejuvinate((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
  return (TRUE);
}
```

There is no lazy path here. The POOM enfilade is created unconditionally before `insertseq` stores the reference.

---

### What `createenf(POOM)` Produces

**`credel.c:492-516`** — `createenf(POOM)` allocates a **two-node tree immediately**:

```c
typecuc *createenf(INT enftype)
{
  typecuc *fullcrumptr;
  typecorecrum *ptr;

  fullcrumptr = (typecuc *) createcrum(1, enftype);  // allocate height-1 root
  fullcrumptr->cenftype = enftype;                   // = POOM
  fullcrumptr->isapex = TRUE;                        // marks this as the root
  fullcrumptr->isleftmost = TRUE;
  adopt(ptr = createcrum(0, enftype), SON, (typecorecrum*)fullcrumptr);
  // ↑ allocate height-0 bottom crum and attach as first child
  if (enftype == GRAN) {
      ((typecbc *)ptr)->cinfo.infotype = GRANNULL;   // POOM skips this
  }
  ivemodified(ptr);
  return (fullcrumptr);
}
```

The resulting tree:

| Node | Type | Height | `isapex` | `cwid` / `cdsp` |
|------|------|--------|----------|-----------------|
| fullcrum (root) | `typecuc` | 1 | TRUE | all zero |
| bottom crum (leaf) | `type2dcbc` | 0 | FALSE | all zero |

**`credel.c:541-596`** — `createcruminternal` confirms that for a POOM bottom crum (`height == 0`, `enftype == POOM`), the code path is:

```c
case POOM:
    crumsize = sizeof(type2dcbc);   // 2D bottom crum, not typecbc
    break;
...
clear(&ptr->cdsp, sizeof(ptr->cdsp));
clear(&ptr->cwid, sizeof(ptr->cwid));
...
clear(&((type2dcbc *)ptr)->c2dinfo, sizeof(...));   // zeroed 2D info
```

All widths and displacements are zero — the POOM is structurally present but empty.

---

### The "Empty" Test

**`orglinks.c:539-544`** — `isemptyorgl` simply checks whether both `cwid` and `cdsp` on the fullcrum are all-zero:

```c
bool isemptyorgl(typeorgl fullcrumptr)
{
    return (
       iszerolock((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock((tumbler*)&((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

A freshly-created POOM passes this test. The `doretrievedocvspanset` path (`do1.c:330-333`) short-circuits on this:

```c
if (isemptyorgl(docorgl)) {
    *vspansetptr = NULL;  /* Empty document returns empty vspanset */
    return TRUE;
}
```

---

### What Happens at First INSERT

**`insertnd.c:185-197`** — `doinsertnd` checks `isemptyenfilade(father)` and routes accordingly:

```c
if (isemptyenfilade(father)) {
    firstinsertionnd(father, origin, width, infoptr);
    return(FALSE);
}
```

**`insertnd.c:199-218`** — `firstinsertionnd` calls `findleftson(father)`. Because `createenf` already adopted a height-0 bottom crum as the POOM's first child, `findleftson` will return it — no new crum is allocated on first insert (unless the GC has reaped the leaf, in which case a fresh one is created at line 209). The first content is written directly into the existing leaf:

```c
ptr = findleftson(father);
if (!ptr) {
    ptr = createcrum(0, (INT)father->cenftype);   // fallback if reaped
    adopt(ptr, SON, (typecorecrum*)father);
}
movewisp(origin, &ptr->cdsp);
movewisp(width, &ptr->cwid);
move2dinfo(infoptr, &((type2dcbc *)ptr)->c2dinfo);
ivemodified(ptr);
```

---

### Summary

**The POOM is allocated eagerly, not lazily.**

When `docreatenewdocument` is called:

1. `createorglgr` (`granf2.c:111`) calls `createenf(POOM)` unconditionally.
2. `createenf` (`credel.c:492`) allocates a two-node in-memory enfilade tree: a height-1 fullcrum with `isapex=TRUE` and one height-0 `type2dcbc` leaf adopted as its first child.
3. All `cwid` and `cdsp` fields are zeroed — the tree is structurally present but reports empty via `isemptyorgl`.
4. The orgl pointer is stored immediately in the granfilade via `insertseq` and is available for lookup by `fetchorglgr` from that moment.
5. At first INSERT, `doinsertnd` detects `isemptyenfilade` and routes to `firstinsertionnd`, which writes content into the already-existing leaf crum. There is no deferred POOM allocation triggered by INSERT.

---

## Question 13 [gregory]

> When a document is opened via OPENDOCUMENT, what exactly is stored in the BERT entry — just the (document-address, connection-id, access-level) triple, or does it also cache a pointer to the document's orgl root?

### Gregory's Answer

## KB Synthesis

The KB describes the BERT entry structure explicitly in [SS-BERT] (Finding 0014):

```
BertEntry = { connection: ConnectionId, document: Tumbler, type: {READ, WRITE}, count: Nat }
```

Plus "created/modified flags" from the struct description at `bert.c:13-29`. That is the complete picture the KB provides — **no orgl pointer is described as part of the BERT entry**.

However, the KB also describes a separate mechanism. From [SS-DOCUMENT-LIFECYCLE] (Finding 0027):

> `findorgl` — checks if document orgl is in the **open list**; returns FALSE if not, causing the calling operation to fail

The log entry `orgl for 0.1.1.0.1.0.1~ not open in findorgl temp = 0` suggests `findorgl` searches for an actual orgl pointer in some structure — the KB calls it the "open list" — distinct from (or at least conceptually distinct from) the BERT table itself.

So from what the KB covers: the BERT entry is the (connection, document-tumbler, access-type, refcount, flags) tuple. Whether OPENDOCUMENT *also* loads the orgl pointer into a separate in-memory cache ("open list") that `findorgl` searches, and whether that cache is co-located with or separate from the BERT hash table, is **not answerable from the KB**. The KB confirms the open-list concept exists and that `findorgl` uses it, but does not describe whether it is stored inside the BERT entry, alongside it, or as a completely independent structure.

## Code Exploration

I have everything needed for a complete answer.

---

## What's Stored in a BERT Entry

**Short answer: only the (document-address, connection-id, access-level) triple plus three housekeeping fields. No orgl root pointer.**

### The `bertentry` struct

`bert.c:13-19`:

```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;
    int count;
} bertentry;
```

Six fields, nothing else:

| Field | Type | Meaning |
|---|---|---|
| `connection` | `int` | The connection/user ID (`user` global from `players.h`) |
| `documentid` | `tumbler` | Copy of the document tumbler (the address) |
| `created` | `char` | Boolean: did this session create the document? |
| `modified` | `char` | Boolean: was the document modified in this session? |
| `type` | `int` | Access level: `READBERT` or `WRITEBERT` |
| `count` | `int` | Reference count for nested opens |

These are the only six fields. There is no orgl root pointer, no cached disk pointer, no document tree reference of any kind.

### How the entry gets populated

`addtoopen()` in `bert.c:128-151` is the sole writer:

```c
tumblercopy(tp, &ptr->documentid);   // bert.c:140
ptr->connection = connection;         // bert.c:141
ptr->count = 1;                       // bert.c:142
ptr->created = created;               // bert.c:143
ptr->modified = FALSE;                // bert.c:144
ptr->type = type;                     // bert.c:145
```

All five non-count fields initialized. No orgl, no granfilade pointer.

### The call chain from OPENDOCUMENT

`fns.c:388-401` (`myopen`) → `doopen()` in `bert.c:264-322` → `addtoopen()` in `bert.c:128`.

`doopen` handles the three open modes (COPYIF, ONLY, COPY) and may call `docreatenewversion` first, but in every path the only thing written to the bert table is `addtoopen(…)`.

### Where the orgl root actually lives

Every document operation that needs the orgl calls `findorgl()` fresh each time, not bert. `do1.c:37-42` (`dorearrange`) is typical:

```c
bool findorgl(), rearrangepm();
return (
    findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)
 && rearrangepm(taskptr, docisaptr, docorgl, cutseqptr)
);
```

`findorgl` in `granf1.c:17-41` does two things:

1. Calls `checkforopen(isaptr, type, user)` — a bert table lookup — to gate on access level [`granf1.c:22`]. This is the *only* thing bert contributes to operation dispatch.
2. Calls `fetchorglgr(taskptr, granfptr, isaptr)` [`granf1.c:39`] to actually retrieve the orgl.

`fetchorglgr` in `granf2.c:22-78` traverses the granfilade using the document tumbler, finds the `GRANORGL` crum, pages it in via `inorgl()` if needed [`granf2.c:60`], and returns `context->corecrum->cinfo.granstuff.orglstuff.orglptr` [`granf2.c:62`].

### Summary

The BERT table is a pure access-control and session-tracking mechanism. It stores:
- **What**: the document tumbler (`documentid`)
- **Who**: which connection opened it (`connection`)
- **How**: the access level (`type`: read or write)
- **Housekeeping**: `created` (for garbage-collecting abandoned new versions on close), `modified` (guards same), `count` (nesting depth)

It does **not** cache anything about the document's internal structure. The orgl root is retrieved on every operation via `findorgl` → `fetchorglgr` → granfilade traversal from disk. The BERT entry is consulted only as a gating check (`checkforopen`) before that traversal proceeds.

---

## Question 14 [gregory]

> When CLOSEDOCUMENT is called, does the backend remove the BERT entry and release any cached orgl pointer, or does the orgl remain in the node cache until the grim reaper evicts it?

### Gregory's Answer

## KB Synthesis

This question is not fully answerable from the KB.

The KB documents the relevant subsystems but does not describe the specific CLOSEDOCUMENT execution path in detail.

**What the KB does establish:**

[SS-BERT] describes the BERT table structure — each entry records `(connection, document, access_type, count, created, modified)` flags — and that `doopen`/`doclose` are implemented in `do2.c`. The reference count field is noted but its lifecycle (when it is decremented and when the entry is removed) is not documented.

[SS-DOCUMENT-LIFECYCLE] establishes that `findorgl` checks whether a document orgl is in the "open list" before granting access. The open list is per-session state. However, the KB does not document how `doclose` modifies the open list or whether it touches the BERT table directly.

[SS-CACHE-MECHANISM] establishes that cached crums (including orgl crums) are evicted by the grim reaper based on `age >= OLD`, triggered by memory pressure — not by any document lifecycle event. There is no documented explicit release path tied to CLOSEDOCUMENT.

**What would be needed to answer:**

Direct inspection of `do2.c:doclose()` to determine whether it: (1) removes the BERT entry or decrements the reference count, (2) removes the document from the open list, and (3) explicitly marks the orgl crum for eviction or leaves it to the grim reaper's age-based mechanism.

Based on [SS-CACHE-MECHANISM]'s description of the cache as purely age-driven with no explicit per-operation release, the most likely behavior is that CLOSEDOCUMENT updates BERT state and the open list, but the orgl crum remains in the grim reaper's circular list until evicted by age — but this is inference, not a KB-supported claim.

## Code Exploration

I now have everything needed to answer the question. Let me compile the full trace.

---

## CLOSEDOCUMENT: BERT Removal and Orgl Lifecycle

### The Call Chain

`CLOSE` (request code 36, `requests.h:43`) is dispatched by `xanadu()` through `requestfns[CLOSE]` → `myclose` (`init.c:67`, `be.c:108`).

**`myclose`** (`fns.c:404-416`):
```c
void myclose(typetask *taskptr)
{
  tumbler t;
  bool getclose(), doclose();
    if(
        getclose(taskptr,&t)
        && doclose(taskptr,&t, user)) {
        putclose(taskptr);
    } else {
        putrequestfailed(taskptr);
    }
}
```
It decodes the tumbler, calls `doclose`, and sends the response. Nothing else.

---

### What `doclose` / `removefromopen` Does

**`doclose`** (`bert.c:325-336`) calls `removefromopen(tp, connection)`.

**`removefromopen`** (`bert.c:154-193`) does the following:

1. Computes `hash = hashoftumbler(tp)` and walks the `berttable[hash]` linked list to find the entry matching `(connection, documentid)`.
2. Decrements `bert->count`. If count is still > 0 (reference-counted), returns `TRUE` immediately — the entry stays.
3. If count reaches zero:
   - Evaluates `status = bert->created && !bert->modified` — if a document was created but never written to, calls `deleteversion(tp)` (which is currently a stub, `bert.c:348-353`).
   - **`efree(p->stuff)`** — frees the `bertentry` struct.
   - Splices the `conscell` out of the hash chain and **`efree`**s it.

The `bertentry` struct (`bert.c:13-19`) contains only: `connection`, `documentid` (tumbler), `created`, `modified`, `type`, `count`. **It contains no pointer to any orgl or gran crum.**

---

### Where the Orgl Lives

When a document is accessed, `findorgl` (`granf1.c:17-41`) first checks the BERT table for authorization, then calls `fetchorglgr` (`granf2.c:22-81`).

`fetchorglgr` navigates the gran enfilade (`granf`) to the bottom crum for the document address. If `orglincore` is false and `diskorglptr` is valid, it calls `inorgl(context->corecrum)` (`granf2.c:60`) to page in the orgl subtree. The orgl lives at:

```
corecrum->cinfo.granstuff.orglstuff.orglptr   (typecuc*, the apex of the POOM)
corecrum->cinfo.granstuff.orglstuff.orglincore (bool flag)
```

Every `createcrum` call links the new crum into the **grim reaper's circular list** (`credel.c:518-532`):
```c
ptr->nextcrum = grimreaper;
ptr->prevcrum = grimreaper->prevcrum;
grimreaper->prevcrum->nextcrum = ptr;
grimreaper->prevcrum = ptr;
```
All orgl crums — the apex POOM and its entire subtree — live in this list once allocated.

---

### What `doclose` Does NOT Do to the Orgl

`doclose` → `removefromopen` makes **no calls** to:
- `fetchorglgr` or `findorgl`
- `orglfree` (`credel.c:470-490`)
- `inorgl` / `orglwrite`
- Anything that touches `orglincore` or `orglptr`
- Anything that modifies crum `age` fields
- The grim reaper list

The BERT table and the node cache are **entirely orthogonal structures**.

---

### The Grim Reaper and Orgl Pinning

The grim reaper (`grimlyreap`, `credel.c:106-162`) is triggered inside `ealloc` when `falloc` finds no free memory (`credel.c:75`). It walks the circular crum list and calls `isreapable` on each candidate.

**`isreapable`** (`credel.c:164-289`) explicitly blocks eviction of any crum associated with an in-core orgl. The check appears in three places:

- **`credel.c:204`** (apex POOM, modified child scan):
  ```c
  if (p->height == 0 && p->cenftype == GRAN
      && ((typecbc *)p)->cinfo.infotype == GRANORGL
      && ((typecbc *)p)->cinfo.granstuff.orglstuff.orglincore) {
      return(FALSE);   // NOT reapable
  }
  ```
- **`credel.c:220`** and **`credel.c:254`**: identical guards for other traversal paths.
- **`credel.c:243-249`** (height-0 gran crum directly):
  ```c
  if (localreaper->cenftype == GRAN) {
      if (((typecbc *)localreaper)->cinfo.infotype == GRANORGL) {
          if (((typecbc *)localreaper)->cinfo.granstuff.orglstuff.orglincore) {
              return(FALSE);
          }
      }
  }
  ```

An orgl is only released from core in **`orglfree`** (`credel.c:470-490`):
```c
void orglfree(typecuc *ptr)
{
    // ...safety checks...
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglincore = FALSE;
    ((typecbc *)ptr->leftbroorfather)->cinfo.granstuff.orglstuff.orglptr = NULL;
    subtreefree((typecorecrum*)ptr);
}
```
`orglfree` is only called from `subtreefree` (`credel.c:429`) and from `reap` → `orglwrite` (which writes the orgl to disk before freeing it, `credel.c:309`). Neither path is triggered by CLOSEDOCUMENT.

---

### Summary

**CLOSEDOCUMENT (`CLOSE` → `myclose` → `doclose` → `removefromopen`):**

1. **Removes the BERT entry** from the `berttable` hash chain — freeing the `bertentry` and its `conscell` wrapper. This revokes access-control authorization for that `(connection, documentid)` pair.

2. **Does not touch the orgl at all.** No pointer to any enfilade node is stored in the BERT entry. The orgl, if it was ever loaded into core by a prior `fetchorglgr` call, remains in the grim reaper's circular list with `orglincore == TRUE`.

3. **The orgl remains pinned** against reaping for as long as `orglincore == TRUE`. The grim reaper (`grimlyreap`) explicitly skips any gran crum whose `orglincore` flag is set (`isreapable` returns `FALSE` in all four relevant branches, `credel.c:204`, `220`, `245-249`, `254`).

4. **The orgl is eventually evicted** only when `grimlyreap` → `reap` → `orglwrite` runs (triggered by memory pressure in `ealloc`), which writes the orgl subtree to disk, calls `orglfree`, sets `orglincore = FALSE` and `orglptr = NULL`, and then `subtreefree`s the crum tree.

In short: closing a document is a pure BERT-table operation. The orgl stays resident in the node cache, protected from the grim reaper by its `orglincore` flag, until memory pressure forces a write-out — completely independent of whether the document is open or closed in the BERT sense.

---

## Question 15 [gregory]

> Does the ownership check in `makehint` (do2.c:78-84) compare the user's account tumbler against the document's parent address using tumbler prefix matching, or does it use a separate ownership table?

### Gregory's Answer

## KB Synthesis

The ownership check does **not** occur inside `makehint` itself — `makehint` only encodes hierarchy levels from its parameters. The actual check happens in `docreatenewversion` at `do1.c:272-280`, which decides *which* `makehint` call to make.

From [SS-VERSION-ADDRESS Finding 0068]:

> The ownership check uses `tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)`.
> - Owned: `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` → depth=1 (version under source document)
> - Unowned: `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` → depth=2 (version under creating user's account)

The KB also explicitly characterizes the mechanism [ST-VERSION-OWNERSHIP Finding 0068]:

> "The ownership check uses account-level tumbler comparison (`tumbleraccounteq`), meaning ownership is determined by account prefix matching, not by an explicit permissions table."

So the two-part predicate is:
1. `tumbleraccounteq(isaptr, wheretoputit)` — compares the account-level prefix of the document's ISA against the current user's account tumbler (prefix matching)
2. `isthisusersdocument(isaptr)` — a secondary check (the KB does not reveal its internal mechanism beyond the name)

`makehint` itself [SS-ADDRESS-SPACE Finding 0021] only uses the supertype/subtype/depth arguments to set the hint's hierarchy level (`depth = (supertype == subtype) ? 1 : 2`). It receives the pre-selected hint ISA from the caller — it has no visibility into the ownership predicate.

**Summary:** Tumbler prefix matching via `tumbleraccounteq`, not a separate ownership table.

## Code Exploration

I now have all the information needed. Here is the full answer.

---

## The ownership check in `makehint` (do2.c:78-84)

### Bottom line first

**`makehint` itself contains no ownership check.** It is a pure struct-initialization function. The ownership logic lives in `checkforopen` (bert.c:52-87) and in callers of `makehint` that decide which hint to construct — notably `docreatenewversion` (do1.c:260-276). The mechanism used is **tumbler prefix matching**, not a separate ownership table.

---

### What `makehint` actually does

```c
// do2.c:78-84
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype = typebelow;
    hintptr->atomtype = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

It fills in a `typehint` struct (defined in `xanadu.h:148-153`):

```c
// xanadu.h:148-153
typedef struct {
    INT supertype;
    INT atomtype;
    INT subtype;
    typeisa hintisa;
} typehint;
```

The hint tells the granfilade (`granf2.c`) where in the address space to allocate a new ISA for a document, link, or content atom. `supertype` and `subtype` constrain the search range; `hintisa` is the anchor tumbler. No ownership check, no conditional logic, no table lookup.

---

### Where ownership is actually checked

**Location 1 — `checkforopen` (bert.c:52-87):**

```c
// bert.c:81-85
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
} else {
    return -1;
}
```

Before any write operation, `checkforopen` walks the BERT hash table (`berttable[]`, bert.c:29) looking for an existing open-document entry for `tp`. If nothing is open for write by another connection (`!foundnonread`), and the request is either a read or the document belongs to the current user, it returns 0 (proceed without creating a new version). Otherwise it returns −1 (a new version must be made via `docreatenewversion`).

The BERT table is an **open-document registry**, not an ownership table. It tracks which connection has which document open, and in what mode. Ownership itself is determined by `isthisusersdocument`, not by looking up a separate owner record.

**Location 2 — `docreatenewversion` (do1.c:260-276):**

```c
// do1.c:268-275
/* ECH 7-13 introduced test for ownership to do right thing for explicit creation
   of new version of someone else's document */
if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
    makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
} else {
    /* This does the right thing for new version of someone else's document, as it
       duplicates the behavior of docreatenewdocument */
    makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
}
```

Here ownership is checked *before* calling `makehint`, in order to decide *which* hint to build:
- If the document belongs to the current user → `DOCUMENT→DOCUMENT` hint: allocate the new version under the existing document's ISA.
- Otherwise → `ACCOUNT→DOCUMENT` hint: allocate the new version under the current user's account ISA (`wheretoputit` is `&taskptr->account`).

This is how "versioning someone else's document" works — the new version is placed in the current user's address space instead.

---

### How `isthisusersdocument` works: tumbler prefix matching

All three implementations of `isthisusersdocument` (for standalone, socket, and main-loop entry points) delegate immediately to `tumbleraccounteq`:

```c
// socketbe.c:197-201
int isthisusersdocument(tumbler *tp)
{
    /* was &(player[n_players].account)  !!!!!! GRRRR ECH */
    return tumbleraccounteq(tp, &(player[user].account));
}
```

```c
// be.c:171-176
int isthisusersdocument(tumbler *tp)
{
    bool result = tumbleraccounteq(tp, &taskptrx->account);
    return result;
}
```

`tumbleraccounteq` (tumble.c:38-70) is the ownership predicate. It performs **tumbler prefix matching**:

```c
// tumble.c:38-70
bool tumbleraccounteq(tumbler *aptr, tumbler *bptr)
{
    INT i, j_b;

    if (aptr->sign != bptr->sign) {
        return(FALSE);
    }

    /* Compare until account (bptr) terminates with two zeros.
       Document (aptr) may continue beyond the account's address space. */
    for (j_b = 0, i = 0; i < NPLACES; i++) {
        if (bptr->mantissa[i] == 0) {
            if (++j_b == 2) {
                return(TRUE);  /* Account terminated, document is under this account */
            }
            /* First zero - document may continue to sub-address, skip */
        } else {
            /* Non-zero in account - document must match exactly */
            if (aptr->mantissa[i] != bptr->mantissa[i]) {
                return(FALSE);
            }
        }
    }
    return (TRUE);
}
```

The logic: walk both tumblers' mantissa arrays. For each position where the account tumbler (`bptr`) is **non-zero**, the document tumbler (`aptr`) must match exactly. When the account terminates (two consecutive zero mantissa positions), the document is declared to belong to that account — the document ISA may extend further into the address space hierarchy beneath the account. This is prefix matching in the tumbler address space.

---

### Summary

| Question | Answer |
|---|---|
| Does `makehint` (do2.c:78-84) contain an ownership check? | **No.** It is a pure struct initializer. |
| Where is ownership checked? | `checkforopen` (bert.c:81) and `docreatenewversion` (do1.c:270), both via `isthisusersdocument`. |
| Does it use a separate ownership table? | **No.** There is no ownership table. The BERT table (`berttable[]`) tracks open-document state by connection, not ownership. |
| What mechanism determines ownership? | **Tumbler prefix matching** via `tumbleraccounteq` (tumble.c:38-70): the document's ISA tumbler is checked to see if it is a sub-address of the current user's account tumbler, by scanning mantissa positions until the account terminates with two zeros. |

---

## Question 16 [gregory]

> When CREATENEWVERSION allocates a version address as a child of the source document (e.g., `doc.0.1`), does the `.0.1` suffix occupy the same tumbler field level as the document's own `.0.N` element field, creating a deeper nesting level in the address hierarchy?

### Gregory's Answer

## KB Synthesis

The question's premise needs a correction: version addresses use **depth=1 allocation**, which appends a digit *without* a `.0.` field separator. The suffix is `.1`, not `.0.1`.

## Version Address Structure

From [SS-VERSION-ADDRESS] Finding 0068 and [SS-ADDRESS-ALLOC] Finding 0021:

| Source doc | Version address | Mechanism |
|-----------|----------------|-----------|
| `1.1.0.1.0.1` | `1.1.0.1.0.1.1` | depth=1: no `.0.` boundary |
| `1.1.0.1.0.1.1` | `1.1.0.1.0.1.1.1` | depth=1 again: grandchild |

`makehint(DOCUMENT, DOCUMENT, ...)` uses depth=1, which means `tumblerincrement(hintisa, depth-1=0, 1)` appends a digit at the last significant position — no `.0.` separator is inserted.

Contrast with ACCOUNT→DOCUMENT allocation (depth=2), which *does* cross a `.0.` boundary: `1.1.0.1` → `1.1.0.1.0.1`.

## Address Space Geometry

All three address types share the same numerical range under the document, but partition it by digit value at position 7 (0-indexed from the node prefix):

| Address type | Form | Digit at pos 7 | Example |
|---|---|---|---|
| Text element | `doc.0.3.N` | `0` (field sep) | `1.1.0.1.0.1.0.3.1` |
| Link element | `doc.0.2.N` | `0` (field sep) | `1.1.0.1.0.1.0.2.1` |
| Version | `doc.N` (N≥1) | `N` (non-zero) | `1.1.0.1.0.1.1` |

From [INV-TUMBLER-TOTAL-ORDER], since `0 < 1` at position 7, element addresses numerically precede version addresses within the same parent scope:

```
1.1.0.1.0.1.0.2.1  (link element)
1.1.0.1.0.1.0.3.5  (text element)
   < 1.1.0.1.0.1.1  (first version)
   < 1.1.0.1.0.1.2  (second version)
   < 1.1.0.1.0.2    (next sibling document)
```

## Allocation Navigates This Correctly

From [SS-ADDRESS-ALLOC] Finding 0068: the version allocator bounds its search at `1.1.0.1.0.2` (next sibling of the source doc), finds the highest existing address in that range (which may be a text element like `1.1.0.1.0.1.0.3.5`), then **truncates to length 7** (parent length + 1 for depth=1) and increments. Truncating `1.1.0.1.0.1.0.3.5` to 7 digits gives `1.1.0.1.0.1.0` → incrementing yields `1.1.0.1.0.1.1` — the correct first version address, leaping over the element address region.

## Answer

Version addresses (`doc.N`) and element addresses (`doc.0.field.N`) share the parent document's numerical address space but are **not at the same hierarchy level**. The `.0.` field separator in element addresses marks a structural boundary in the four-level `Node.0.User.0.Doc.0.Element` hierarchy; version addresses deliberately omit this separator, placing them between the document level and the element level in the tumbler ordering without formally crossing into a new hierarchy tier. [SS-ADDRESS-SPACE, SS-VERSION-ADDRESS, SS-ADDRESS-ALLOC]

## Code Exploration

I now have all the code evidence needed. Let me trace the complete execution path for `CREATENEWVERSION`.

---

## Answer

### Short answer

**No.** The version suffix is **not** `.0.1` — it is just `.1` (no zero separator). The golden tests confirm it. The version address does extend from within the document's address sub-space, but it does so via a different mechanism (depth=1, no zero separator) than the document's own element field allocation (depth=2, zero separator).

---

### Full trace

#### 1. `docreatenewversion` chooses the hint type [do1.c:260–278]

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    typehint hint;
    ...
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr)) {
        makehint (DOCUMENT, DOCUMENT, 0, isaptr/*wheretoputit*/, &hint);
    } else {
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);
    }
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
        return (FALSE);
    }
    ...
```

When the user **owns** the source document (same account), the hint is `(DOCUMENT, DOCUMENT, atomtype=0, hintisa=source_doc_isa)`.

#### 2. `makehint` fills the hint struct [do2.c:78–84]

```c
int makehint(INT typeabove, INT typebelow, INT typeofatom, typeisa *isaptr, typehint *hintptr)
{
    hintptr->supertype = typeabove;
    hintptr->subtype   = typebelow;
    hintptr->atomtype  = typeofatom;
    movetumbler (isaptr, &hintptr->hintisa);
}
```

`typehint` struct [xanadu.h:148–153]:
```c
typedef struct {
    INT supertype;   // DOCUMENT = 3
    INT subtype;     // DOCUMENT = 3
    INT atomtype;    // 0
    typeisa hintisa; // source doc ISA, e.g. mantissa [1,1,0,1,0,1,...]
} typehint;
```

#### 3. The critical `depth` calculation [granf2.c:203–242]

`createorglingranf` → `createorglgr` → `findisatoinsertgr` → **`findisatoinsertnonmolecule`**:

```c
static int findisatoinsertnonmolecule(typecuc *fullcrumptr, typehint *hintptr, typeisa *isaptr)
{
    INT depth, hintlength;
    ...
    depth = hintptr->supertype == hintptr->subtype ? 1 : 2;
    // DOCUMENT == DOCUMENT (3 == 3) → depth = 1
```

For the user-owns-document case: **`depth = 1`**.

For the ACCOUNT→DOCUMENT case (different user's doc): `depth = 2`.

#### 4. How depth determines the version address [granf2.c:235–241]

When nothing exists under the hint yet (first version):
```c
if (iszerotumbler(&lowerbound) || !lowerbound_under_hint) {
    tumblerincrement(&hintptr->hintisa, depth, 1, isaptr);
    //  ↑ rightshift = depth = 1
```

`tumblerincrement` [tumble.c:599–623]:
```c
int tumblerincrement(tumbler *aptr, INT rightshift, INT bint, tumbler *cptr)
{
    for (idx = NPLACES; aptr->mantissa[--idx] == 0 && idx > 0;);
    // idx = last non-zero position of hintisa
    cptr->mantissa[idx + rightshift] += bint;
    tumblerjustify(cptr);
}
```

For source doc `1.1.0.1.0.1` → mantissa `[1,1,0,1,0,1,0,0,…]`, last non-zero at **idx=5**:

```
mantissa[5 + 1] += 1  →  mantissa[6] = 1
Result: [1, 1, 0, 1, 0, 1, 1, 0, ...]
Printed: 1.1.0.1.0.1.1
```

**No zero separator at position 6.**

#### 5. `puttumbler` confirms the notation [put.c:26–46]

```c
int puttumbler(FILE *outfile, tumbler *tumblerptr)
{
    for(i = tumblerptr->exp; i < 0; ++i)
        fprintf(outfile, "0.");
    place = NPLACES;
    do {--place;} while(place > 0 && tumblerptr->mantissa[place] == 0);
    for(i = 0; i <= place; ++i) {
        putnum(outfile, tumblerptr->mantissa[i]);
        if (i < place) putc('.', outfile);
    }
}
```

Each mantissa position maps one-to-one to a `.`-separated field in the printed address. There is no grouping — `1.1.0.1.0.1.1` means mantissa `[1,1,0,1,0,1,1]`.

#### 6. Golden tests confirm [golden/versions/version_address_allocation.json]

```json
{ "op": "create_document", "result": "1.1.0.1.0.1",  "comment": "First document" },
{ "op": "create_document", "result": "1.1.0.1.0.2",  "comment": "Second document" },
{ "op": "create_version",  "from": "doc1",  "result": "1.1.0.1.0.1.1",  "comment": "If child: doc1.1  If sibling: account.0.2" },
{ "op": "create_version",  "from": "doc1",  "result": "1.1.0.1.0.1.2",  "comment": "Second version" },
{ "op": "create_version",  "from": "doc2",  "result": "1.1.0.1.0.2.1",  "comment": "Version of different doc" },
{ "op": "create_version",  "from": "version1", "result": "1.1.0.1.0.1.1.1", "comment": "Version chain" }
```

---

### Address sub-space comparison

| Entity | Address | Mantissa pos 6 | Separator? |
|--------|---------|---------------|------------|
| Document | `1.1.0.1.0.1` | — | Account→Doc uses `.0.` (depth=2) |
| **Version N** | `1.1.0.1.0.1.N` | **N (non-zero)** | **None — depth=1, no zero** |
| Text atom M | `1.1.0.1.0.1.0.1.M` | **0 (zero separator)** | Yes — depth=2 in molecule path |

Text atoms are allocated by `findisatoinsertmolecule` [granf2.c:158–181], which uses `rightshift=2` from the document ISA, leaving a **zero** at position 6 and putting the atom type at position 7. That zero at position 6 is what separates the element sub-space from the version sub-space.

Specifically, for the first text atom in `1.1.0.1.0.1`:
```
tumblerincrement(doc_isa, rightshift=2, TEXTATOM=1)
  → mantissa[5+2=7] = 1  →  [1,1,0,1,0,1,0,1,0,…]  =  1.1.0.1.0.1.0.1
tumblerincrement(above, rightshift=1, 1)
  → mantissa[7+1=8] = 1  →  [1,1,0,1,0,1,0,1,1,0,…]  =  1.1.0.1.0.1.0.1.1
```

Position 6 is **0** for elements. Position 6 is **N≥1** for versions. These sub-spaces are non-overlapping in the tumbler ordering (elements `< 1.1.0.1.0.1.1` because `0 < 1` at position 6).

---

### Direct answer to the question

The premise of the question is wrong in one respect and right in another:

- **Wrong:** The suffix is **not `.0.1`** — there is no zero separator before the version number. The version address is `doc.N`, not `doc.0.N`.
- **Right:** The version is allocated as a "child" of the source document in the sense that it lives in the address range `[doc, doc+1)`.

The version number N occupies **mantissa position `k+1`** (where k is the document's last non-zero index), which is the **same** positional index that elements use as their **zero separator**. But they use it differently: versions put a non-zero value there; elements put a zero there (then continue deeper). This is what keeps the two sub-spaces non-overlapping.

So: the version's `.N` field does NOT occupy the same level as the account's `.0.N` document field (that uses depth=2). It occupies a shallower level (depth=1, no zero separator). And it does not create a **deeper nesting level** in any hierarchical sense — it is merely the next mantissa position after the document's last digit, with no structural hierarchy boundary between them.

---

## Question 17 [gregory]

> Can a session open the same document multiple times with different access levels (e.g., READBERT then WRITEBERT), or does `checkforopen` reject the second open if the document already has a BERT entry for that connection?

### Gregory's Answer

## KB Synthesis

From the KB, the behavior depends on the direction of the access-level change.

**Downgrade (WRITE → READ): Rejected at the OPEN command level**

[PRE-OPEN-DOC] Finding 0006 states explicitly: "The backend rejects attempts to open a document that is already open in the current session, even if the requested access mode differs (e.g., opening as READ_WRITE then attempting READ_ONLY). Only one handle per document is permitted at a time. To change access mode, the document must be closed and reopened."

**Upgrade (READ → WRITE): Rejected at the `checkforopen` level**

[PRE-OPEN-DOC] Finding 0014 gives the full `checkforopen` state machine. For the same-connection WRITE request on a document currently open for READ: return value is `-1` (access denied). The protocol signal for `-1` is that the client should create a new version and open that instead ([INT-BERT-VERSION]).

**Same-level re-open: Varies**

The `checkforopen` matrix shows:
- Same-connection READ on a READ-open doc → returns `READ` (granted, returns existing level)
- Same-connection READ on a WRITE-open doc → returns `WRITE` (granted at the higher existing level, not a new open)
- Same-connection WRITE on a WRITE-open doc → returns `WRITE` (granted)

Note there is some tension in the KB here. Finding 0006 says the backend rejects any duplicate open (including same-mode), while Finding 0014's matrix shows same-connection, same-mode requests as granted. The distinction may be between the `OPEN` FEBE command behavior (Finding 0006, command-level rejection) and `checkforopen` being called internally during operation dispatch (Finding 0014, access-level verification). The two are separate code paths.

**Summary:** A session cannot hold two open handles on the same document simultaneously at any access level. To change access mode, the document must be closed and reopened. Attempting WRITE when already holding READ yields `-1` with a redirect to version creation; attempting READ when holding WRITE is handled by returning the existing WRITE level (not a new open).

## Code Exploration

I now have everything needed to answer thoroughly. Here is the complete analysis:

---

## Can a Session Open the Same Document Twice with Different Access Levels?

**Short answer:** No — not with the same tumbler ID. `checkforopen` does not outright "reject" the second open; it returns `-1`, which `doopen` then handles based on the `mode` (copy policy). The result is either a hard failure or the creation of a *new version*, never an upgrade of the existing BERT entry.

---

### Constant Definitions

From `backend/common.h:165-171`:
```c
#define NOBERTREQUIRED 0
#define READBERT 1
#define WRITEBERT 2

#define BERTMODEONLY   1    // client: CONFLICT_FAIL
#define BERTMODECOPYIF 2    // client: CONFLICT_COPY
#define BERTMODECOPY   3    // client: ALWAYS_COPY
```

From `febe/client.py:588-592`:
```python
(READ_ONLY, READ_WRITE) = (1, 2)
(CONFLICT_FAIL, CONFLICT_COPY, ALWAYS_COPY) = (1, 2, 3)
```

---

### The BERT Entry Structure

Each open document is represented as a `bertentry` in a global hash table [`bert.c:13-19`]:
```c
typedef struct {
    int connection;
    tumbler documentid;
    char created, modified;
    int type;     // READBERT or WRITEBERT
    int count;    // reference count for nested opens
} bertentry;
```

`addtoopen()` at `bert.c:128-151` **always creates a new entry** — it does not check for duplicates before inserting. The `type` field is set once at allocation [`bert.c:145`] and **never changed** by any code in the file.

---

### Step 1: First Open (READBERT / `READ_ONLY`)

`myopen()` [`fns.c:388-401`] calls `doopen()` → `checkforopen()` [`bert.c:279`].

`checkforopen()` [`bert.c:52-87`] scans the hash bucket. Finding no existing entry for this `(connection, documentid)`, it falls through to [`bert.c:81`]:
```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;   // "open required"
}
```

Back in `doopen()`, `openState == 0` → `addtoopen(tp, connection, FALSE, READBERT)` is called [`bert.c:282`]. A `bertentry` with `type=READBERT, count=1` is inserted into the table.

---

### Step 2: Second Open (WRITEBERT / `READ_WRITE`), Same Doc, Same Connection

`checkforopen()` loops over the hash bucket, finds the prior entry, and at [`bert.c:65-66`] matches both the tumbler and the connection:

```c
if (tumblereq(tp, &bert->documentid)) {
    if (connection == bert->connection) {
        switch (bert->type) {
            case READBERT:
                return (type == READBERT) ? READBERT : /* WRITE */ -1;  // bert.c:69
            case WRITEBERT:
                return WRITEBERT;                                         // bert.c:71
        }
    }
```

Since `bert->type == READBERT` and the requested `type == WRITEBERT`, the function returns **`-1`** (meaning "a new version must be made").

This is confirmed by the truth table embedded in the comment at `bert.c:44-50`:

```
Open state -->
type          Not Open    |   Open READ   |  Open WRITE
              !owned|owned | conn==|conn!= | conn==|conn!=
--------------+-----+-----+-------+-------+-------+------
READ             0  |  0  |  READ |   0   | WRITE |  -1
WRITE           -1  |  0  |  -1   |  -1   | WRITE |  -1
```

**WRITE requested, Open READ, `conn==` → `-1`.**

---

### Step 3: `doopen()` Handles `-1` Based on `mode`

`doopen()` at `bert.c:264-322` dispatches on `mode`:

#### `CONFLICT_FAIL` / `BERTMODEONLY` [`bert.c:300-317`]:
```c
case BERTMODEONLY:
    if (openState == -1 || openState == WRITEBERT) {
        return 0;  // failure
    }
```
The second open is **outright rejected**. `myopen()` in `fns.c:394-400` calls `putrequestfailed()`.

#### `CONFLICT_COPY` / `BERTMODECOPYIF` [`bert.c:288-299`]:
```c
case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);  // new tumbler in newtp
        addtoopen(newtp, connection, TRUE, type);                    // WRITEBERT on the NEW doc
    }
```
A **new version** is created. The write open succeeds, but it operates on a **different tumbler** (`newtp ≠ tp`). The original READBERT entry for `tp` remains untouched. You now have two separate bert entries for two different documents.

#### `ALWAYS_COPY` / `BERTMODECOPY` [`bert.c:273-277`]:
```c
if (mode == BERTMODECOPY) {
    docreatenewversion(taskptr, tp, &taskptr->account, newtp);
    addtoopen(newtp, connection, TRUE, type);
    return 1;
}
```
This branch runs **before** `checkforopen()` is even called. It always creates a new version regardless of open state.

---

### The Reverse: WRITEBERT First, READBERT Second

If the document is already open WRITEBERT and a READBERT is requested (same connection), `checkforopen()` hits `case WRITEBERT:` at `bert.c:70-71`:
```c
case WRITEBERT:
    return WRITEBERT;   // 2 > 0, "sufficiently open"
```

In `doopen()` with `CONFLICT_COPY`, `openState == WRITEBERT == 2`:
```c
} else if (type != WRITEBERT && openState != WRITEBERT) {   // TRUE && FALSE = FALSE
    incrementopen(tp, connection);
} else {
    docreatenewversion(...);    // another copy is made!
}
```
A new version is created again. With `CONFLICT_FAIL`, the `BERTMODEONLY` case returns failure because `openState == WRITEBERT`.

---

### `addtoopen()` Cannot Produce Duplicate Same-Doc Entries

`addtoopen()` always prepends without checking [`bert.c:136-150`]. However, in the normal flow, it is only called when `openState == 0` (no prior entry) or when creating a new version (a *different* tumbler via `newtp`). So the bert table can never contain two entries for the same `(connection, documentid)` pair through any normal code path.

---

### Summary

| Scenario | `checkforopen` returns | `CONFLICT_FAIL` result | `CONFLICT_COPY` result |
|---|---|---|---|
| READBERT open → WRITEBERT request (same conn) | `-1` | **Rejected** (open fails) | **New version created**; WRITEBERT on new tumbler |
| WRITEBERT open → READBERT request (same conn) | `WRITEBERT` (2) | **Rejected** (`openState == WRITEBERT`) | **New version created**; READBERT on new copy |
| READBERT open → READBERT request (same conn) | `READBERT` (1) | Increments count, same doc | Increments count, same doc |
| WRITEBERT open → WRITEBERT request (same conn) | `WRITEBERT` (2) | **Rejected** | **New version created** |

**`checkforopen` never "rejects" directly** — it returns `-1` or a positive value. The rejection or copy-creation decision lives in `doopen()` and is controlled by the `mode` parameter sent by the client. There is **no mechanism to upgrade a READBERT open to WRITEBERT on the same document tumbler**: the only path forward is either failure or a new copy.

---

## Question 18 [gregory]

> When CREATENEWDOCUMENT is called, does it create any spanfilade entries or granfilade entries for the new empty document, or is the document's existence recorded solely through its orgl allocation and address-space reservation?

### Gregory's Answer

## KB Synthesis

Based on the KB, CREATENEWDOCUMENT creates entries in exactly one layer and leaves the other untouched.

## Granfilade: One Entry Created

CREATENEWDOCUMENT allocates a new document orgl in the **granfilade** via `createorglingranf`, which calls `findisatoinsertnonmolecule` to perform query-and-increment allocation in the document address namespace [SS-ADDRESS-ALLOC, ST-ADDRESS-ALLOC]. This is the same mechanism VERSION uses for its first step.

The KB is explicit about this distinction in [FC-GRANF-ON-VERSION]:

> "CREATENEWVERSION does not modify the *content* portion of the granfilade... However, unlike DELETE, it DOES modify the granfilade by adding a *document address* entry."

CREATENEWDOCUMENT would do the same — only the document-address portion of the granfilade is touched. No content I-addresses are allocated (those come from `findisatoinsertmolecule`, only invoked by INSERT and COPY) [SS-ADDRESS-SPACE, Finding 0077].

An empty POOM enfilade structure is also initialized via `createenf()`. From [EC-EMPTY-DOC] Finding 0058, this produces a minimal height-1 tree: a fullcrum with one zero-width bottom node. This is the "never-filled" state, which is structurally distinct from a post-delete-everything state.

## Spanfilade: No Entries Created

DOCISPAN entries in the spanfilade are created only when `insertspanf(..., DOCISPAN)` is called, which happens inside `docopy()` — only invoked by INSERT and COPY operations [SS-DOCISPAN, ST-INSERT]. An empty document with no content placements generates no DOCISPAN entries.

Similarly, link endset entries in the spanfilade are created only by `insertendsetsinspanf()` during CREATELINK [SS-SPANF-OPERATIONS, ST-CREATE-LINK]. An empty document has no links.

## Summary

| Layer | Effect |
|-------|--------|
| Granfilade (document namespace) | One new orgl entry (address allocated) |
| Granfilade (content namespace) | Nothing — no content I-addresses |
| POOM | Minimal empty enfilade structure (`createenf()`) |
| Spanfilade (DOCISPAN) | Nothing — no content placed |
| Spanfilade (link index) | Nothing — no links created |

The document's existence is recorded by its orgl allocation in the granfilade document namespace, and it becomes discoverable via address (e.g., via `findorgl`) immediately. It becomes discoverable via content identity (e.g., `FINDDOCSCONTAINING`) only after the first INSERT or COPY operation places content and triggers `insertspanf(..., DOCISPAN)` [ST-INSERT, FC-CONTENT-SPANF-ISOLATION].

## Code Exploration

I now have the complete picture. Here is the full answer.

---

## CREATENEWDOCUMENT: What Gets Created?

**Short answer:** CREATENEWDOCUMENT creates exactly one granfilade entry — a `GRANORGL` crum with an attached empty POOM enfilade. No spanfilade entries are created. The document exists solely through its granfilade presence.

---

### Call Chain (with citations)

#### 1. FEBE dispatcher — `fns.c:276-286`

```c
void createnewdocument(typetask *taskptr) {
  typeisa newdocisa;
  bool docreatenewdocument();
    getcreatenewdocument();
    if (docreatenewdocument(taskptr, &newdocisa))
        putcreatenewdocument(taskptr, &newdocisa);
      else
        putrequestfailed(taskptr);
}
```

`getcreatenewdocument` parses no parameters — this operation takes no arguments from the client.

---

#### 2. Core operation — `do1.c:234-241`

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr) {
  typehint hint;
  bool createorglingranf();

    makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf(taskptr, granf, &hint, isaptr));
}
```

This is the **entire implementation**. It:
- Builds a hint with `supertype=ACCOUNT`, `subtype=DOCUMENT`, `atomtype=0`, anchored at `taskptr->account`
- Delegates entirely to `createorglingranf` on the global `granf`
- Calls **nothing else**: no `insertspanf`, no `insertendsetsinspanf`, no `insertpm`

---

#### 3. Granfilade wrapper — `granf1.c:50-55`

```c
bool createorglingranf(typetask *taskptr, typegranf granfptr, typehint *hintptr, typeisa *isaptr) {
  bool createorglgr();
    return (createorglgr(taskptr, (typecuc*)granfptr, hintptr, isaptr));
}
```

A pure pass-through to `createorglgr`.

---

#### 4. Core granfilade insertion — `granf2.c:111-128`

```c
bool createorglgr(typetask *taskptr, typegranf fullcrumptr, typehint *hintptr, typeisa *isaptr) {
  typegranbottomcruminfo locinfo;
  bool findisatoinsertgr();
  typecuc *createenf();

    if (!findisatoinsertgr((typecuc*)fullcrumptr, hintptr, isaptr))
        return (FALSE);
    locinfo.infotype = GRANORGL;
    locinfo.granstuff.orglstuff.orglptr = createenf(POOM);    /* empty POOM */
    reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    locinfo.granstuff.orglstuff.orglincore = TRUE;
    locinfo.granstuff.orglstuff.diskorglptr.diskblocknumber = DISKPTRNULL;
    locinfo.granstuff.orglstuff.diskorglptr.insidediskblocknumber = 0;
    insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);        /* into granf only */
    rejuvinate((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
    return (TRUE);
}
```

Three things happen:

**a. Address allocation** (`findisatoinsertgr` → `findisatoinsertnonmolecule`, `granf2.c:130-156`): With `supertype=ACCOUNT` and `subtype=DOCUMENT`, `depth=2`. The function calls `findpreviousisagr` to find the highest existing ISA under the account tumbler, then increments at depth 2 to produce the new document ISA (e.g., `account.0.1` for the first document under that account).

**b. Empty POOM creation** (`createenf(POOM)`, `credel.c:492-516`): Creates a new in-core POOM enfilade root. A POOM has `cwid = 0` and `cdsp = 0` — it is structurally empty. Its bottom crums are `type2dcbc` (two-dimensional), with no content entries.

**c. Granfilade insertion** (`insertseq` on `fullcrumptr` = `granf`): Inserts a `GRANORGL` crum into the granfilade at the newly computed ISA. The crum carries the pointer to the just-created empty POOM. This is the only structure updated.

**The spanfilade (`spanf`) is never touched.**

---

### The POOM is Empty — `orglinks.c:539-544`

The system itself tests for this when retrieving content from a new document (`do1.c:325-336`):

```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr) {
  typeorgl docorgl;
    if (!findorgl(taskptr, granf, docisaptr, &docorgl, READBERT))
        return FALSE;
    if (isemptyorgl(docorgl)) {
        *vspansetptr = NULL;   /* Empty document returns empty vspanset */
        return TRUE;
    }
    return retrievevspansetpm(taskptr, docorgl, vspansetptr);
}
```

And `isemptyorgl` (`orglinks.c:539-544`):

```c
bool isemptyorgl(typeorgl fullcrumptr) {
    return (
       iszerolock((tumbler*)&((typecuc*)fullcrumptr)->cwid, widsize(POOM))
    && iszerolock((tumbler*)&((typecuc*)fullcrumptr)->cdsp, dspsize(POOM)));
}
```

A freshly created POOM from `createenf(POOM)` has zero `cwid` and zero `cdsp`, so `isemptyorgl` returns TRUE immediately.

---

### Contrast with Operations That DO Write to Spanfilade

- **`doinsert`** (`do1.c:87-123`) → `docopy` → **`insertspanf`** on `spanf` (`do1.c:62`)
- **`docopy`** (`do1.c:45-65`) → **`insertspanf`** on `spanf` (`do1.c:62`)
- **`docreatelink`** (`do1.c:195-221`) → **`insertendsetsinspanf`** on `spanf` (`do1.c:219`)

None of these are called by `docreatenewdocument`.

---

### Conclusion

When `CREATENEWDOCUMENT` is called, exactly two things are created:

1. **One `GRANORGL` crum in the granfilade** — inserted at the newly allocated document ISA under the account tumbler (`do1.c:239`, `granf2.c:119-125`).

2. **One empty POOM enfilade** — the document's orgl, with zero width, no content, pointed to by the granfilade crum (`granf2.c:120`, `credel.c:492-516`).

The spanfilade is not written. No `GRANTEXT` crums are inserted. No orgl-link entries are made. The document's existence is recorded solely through its `GRANORGL` allocation in the granfilade and the empty POOM hanging off it. The document has no virtual address space, no permascroll identity, and no link end-set registrations until content is subsequently inserted.

---

## Question 19 [gregory]

> If two sessions have the same document open with READBERT, and one session upgrades to WRITEBERT, does the BERT mechanism detect the conflict and reject the upgrade, or is there a separate OPENDOCUMENTFORWRITING request that performs the exclusivity check?

### Gregory's Answer

## KB Synthesis

The KB addresses this directly through the `checkforopen` access matrix in `[PRE-OPEN-DOC]` (Finding 0014).

**BERT detects the conflict and denies the upgrade.**

The relevant rule from the `checkforopen` matrix:

> WRITE request on a document open for READ by **any** connection → **-1** (denied)

So if Session A and Session B both hold READBERT on a document, and either session requests WRITEBERT, `checkforopen` returns -1 regardless of which connection holds the existing READ access. The check is not just against the requesting connection's own prior access — it is against any concurrent reader.

There is no separate OPENDOCUMENTFORWRITING request mentioned in the KB. The access-type parameter (READ vs WRITE) is part of the standard open request, and `checkforopen` is called from `doopen` in `do2.c` during that operation. The function returns one of three outcomes: the granted access level, 0 (document needs to be opened first), or -1 (denied). `[PRE-OPEN-DOC]` notes this is called from `bert.c:43-50`.

The -1 result is not simply an error — per `[INT-BERT-VERSION]`, it is a protocol signal redirecting the front end to **create a new version** and open that version for writing instead. This is how BERT enforces non-destructive editing: write contention triggers versioning rather than blocking.

One important caveat from `[INV-WRITE-EXCLUSIVITY]` (Finding 0050): this BERT enforcement is **advisory at the mutation level**. The `checkforopen` gate applies when acquiring the BERT token (the open operation). However, for actual mutations (INSERT, DELETEVSPAN, etc.), the success response is sent before `doXXX` runs, so a non-compliant front end that skips token acquisition can still mutate. `[INT-BERT-FEBE]` characterizes BERT as a cooperative coordination protocol, not an enforced gate on mutations.

**Summary:** The upgrade from READ to WRITE is detected and rejected by `checkforopen` returning -1, with no separate OPENDOCUMENTFORWRITING mechanism. The rejection signals the client to branch via version creation. The exclusivity guarantee holds at the token-acquisition level but depends on front-end compliance for actual mutations.

## Code Exploration

I now have everything I need for a complete answer. Here it is:

---

## BERT Access Control: READBERT → WRITEBERT Conflict Analysis

### There is no separate OPENDOCUMENTFORWRITING request

There is a single `OPEN` request — opcode 35 [`requests.h:42`] — handled by `myopen()` [`fns.c:388–401`]. The same opcode is used for both read and write access. Two parameters differentiate them:

- **type**: `READBERT` (1) or `WRITEBERT` (2) [`common.h:166–167`]
- **mode**: `BERTMODEONLY` (1), `BERTMODECOPYIF` (2), or `BERTMODECOPY` (3) [`common.h:169–171`]

```c
// fns.c:388-401
void myopen(typetask *taskptr)
{
  tumbler t, newt;
  int type, mode;
  if (
      getopen(taskptr, &t, &type, &mode)
      &&  doopen(taskptr, &t, &newt, type, mode, user)) {
      putopen(taskptr, &newt);
  } else {
      putrequestfailed(taskptr);
  }
}
```

`getopen()` reads the tumbler, type integer, and mode integer off the wire [`get1fe.c:255–264`].

---

### The berttable: one entry per (session, document) pair

The in-memory structure is a hash table of `bertentry` records [`bert.c:13–29`]:

```c
typedef struct {
    int connection;    // which session (user fd)
    tumbler documentid;
    char created, modified;
    int type;          // READBERT or WRITEBERT
    int count;         // reference count for nested opens
} bertentry;
```

Each session's open is a separate entry. There is no way to mutate `type` in-place; the only operations are `addtoopen`, `incrementopen`, and `removefromopen`.

---

### `checkforopen()` — the conflict detection function

`bert.c:52–87` contains the decision logic:

```c
for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
    bert = p->stuff;
    if (tumblereq(tp, &bert->documentid)) {
        if (connection == bert->connection) {
            switch (bert->type) {
                case READBERT:
                    return (type == READBERT) ? READBERT : /* WRITE */ -1;
                case WRITEBERT:
                    return WRITEBERT;
            }
        } else {
            if (bert->type != READBERT) {
                foundnonread = TRUE;
            }
        }
    }
}
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
} else {
    return -1;
}
```

Return value semantics [`bert.c:38–51` comment]:
- `> 0` — already open at least at the requested level
- `0` — not open but can be opened (no blocking conflict)
- `-1` — conflict; would require a new version

---

### Tracing the exact scenario

**Setup: Session A and Session B both have READBERT on document D.**

After both opens, the berttable has two entries:
```
{conn=A, doc=D, type=READBERT}
{conn=B, doc=D, type=READBERT}
```

**Session A now sends `OPEN(D, WRITEBERT, mode)`.**

`checkforopen(D, WRITEBERT, A)` iterates the table:

1. Finds `{conn=A, type=READBERT}`. Since `connection == bert->connection`:
   - Enters the inner `switch` on `bert->type`
   - Case `READBERT`: evaluates `(type == READBERT) ? READBERT : -1`
   - `type` is `WRITEBERT`, so: **returns -1 immediately** [`bert.c:69`]

The function **never reaches Session B's entry**. The -1 is triggered by Session A's own pre-existing READBERT entry, not by Session B's presence.

---

### What happens on -1 depends entirely on mode

`doopen()` [`bert.c:264–322`] acts on the return value:

```c
openState = checkforopen(tp, type, connection);  // returns -1

switch (mode) {
case BERTMODECOPYIF:
    if (openState == -1) {
        docreatenewversion(taskptr, tp, &taskptr->account, newtp);
        addtoopen(newtp, connection, TRUE, type);  // WRITEBERT on new doc
    }
    ...
    return 1;
case BERTMODEONLY:
    if (openState == -1 || openState == WRITEBERT) {
        return 0;  // signals failure → putrequestfailed()
    }
    ...
}
```

- **`BERTMODECOPYIF`**: automatically creates a new version of D, registers it in the berttable as `{conn=A, type=WRITEBERT, created=TRUE}`, and returns the new document tumbler to the client. Session B continues reading the old D; Session A writes to the new D. [`bert.c:288–299`]
- **`BERTMODEONLY`**: `doopen()` returns 0, `myopen()` calls `putrequestfailed()`. The upgrade is flatly rejected. [`bert.c:300–317`]
- **`BERTMODECOPY`**: skips `checkforopen` entirely and unconditionally creates a new version [`bert.c:273–277`].

The new version created by `docreatenewversion()` is immediately registered with `addtoopen(newisaptr, user, TRUE, WRITEBERT)` inside `do1.c:292`, bypassing the BERT check (a direct insert, not a `doopen` call), because the document was just created and ownership is guaranteed.

---

### `isthisusersdocument()` and a subtlety about document owners

`isthisusersdocument()` [`be.c:171–176`, `socketbe.c:197–201`] checks whether the document tumbler falls within the requesting session's account prefix, using `tumbleraccounteq()` [`tumble.c:38–67`], which compares mantissa components up to the account's double-zero terminator.

This matters at the end of `checkforopen()`:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
}
```

If Session A **closes its own READBERT first** and then issues `OPEN(D, WRITEBERT)`:
- Only Session B's `{conn=B, type=READBERT}` remains
- Loop: `conn=B != A`, `type == READBERT` → `foundnonread` stays `FALSE`
- After loop: `!foundnonread` = true; `isthisusersdocument(D)` = true (if A created D)
- Returns **0** — not conflicted

`doopen()` with openState=0 then calls `addtoopen(tp, A, FALSE, WRITEBERT)` and returns the original document tumbler. **The document owner can open for write even while others have a READBERT**, as long as the owner's own READBERT is first closed. The decision table comment at `bert.c:44–51` marks `Open READ, conn!= → -1 for WRITE` but that applies only to non-owners; the closing check `isthisusersdocument` carves out an exception for owners.

---

### `findorgl()` — BERT checked on every operation, not just at open time

`granf1.c:17–41` shows that every granfilade lookup (which underlies reads, writes, link operations, etc.) calls `checkforopen()` independently:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr,
              typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {
            fprintf(stderr, "orgl for ... not open in findorgl temp = %d\n", temp);
            return FALSE;
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

Write operations pass `WRITEBERT` (e.g., `do1.c:40`, `do1.c:164`); read operations pass `READBERT` (e.g., `do1.c:318`, `do1.c:327`). The BERT table is consulted at each call, so the open table is enforced throughout the operation — not just at session start.

---

### Summary

| Mechanism | Answer |
|---|---|
| Separate "open for writing" request? | No. Single `OPEN` opcode (35), type parameter selects READ vs WRITE. |
| In-place READBERT → WRITEBERT upgrade? | No. `bertentry.type` is never mutated. |
| Conflict detected when upgrading? | Yes. `checkforopen` returns -1 when same session's existing READBERT entry is found and WRITEBERT is requested [`bert.c:69`]. |
| What causes the -1? | The requesting session's **own** READBERT entry, not other sessions' readers. |
| What happens on -1? | Mode-dependent: BERTMODECOPYIF creates a new version for write; BERTMODEONLY rejects with `putrequestfailed`. |
| Can owner write while others read? | Yes, if owner closes their own READBERT first — `isthisusersdocument` allows openState=0 for the owner even with foreign READBERTs present. |

---

## Question 20 [gregory]

> Does `findorgl` traverse a global document registry to locate a document's orgl root by address, or does it walk the granfilade B-tree using the document's I-address as a key — and what happens when `findorgl` is called for a document address that was never created?

### Gregory's Answer

## KB Synthesis

## `findorgl`: Mechanism and Failure Behavior

### How `findorgl` Works

`findorgl` walks the granfilade B-tree using the document's ISA (I-address) as the key. This is established by [SS-GRANF-OPERATIONS], which lists it as one of the four key granfilade operation classes: "`findorgl()` — locates an orgl by its ISA." Since the granfilade is a B-tree indexed by I-address ([SS-DUAL-ENFILADE]), the lookup is a standard tree traversal against `granf`, not a separate registry.

Beyond the B-tree lookup, `findorgl` performs two additional checks:

1. **Open-list membership**: [SS-DOCUMENT-LIFECYCLE] states that `findorgl` "checks if document orgl is in the open list; returns FALSE if not, causing the calling operation to fail." The backend log confirms: `orgl for 0.1.1.0.1.0.1~ not open in findorgl temp = 0`.

2. **BERT access control**: [EC-RESPONSE-BEFORE-CHECK] notes that `granf1.c:17-41` — `findorgl()` checks BERT via `checkforopen()`, returning FALSE on failure. Callers pass an access type: `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` [PRE-INSERT].

### For a Never-Created Document Address

The KB does not provide the exact ordering of checks inside `findorgl`, but the outcome is clear: either the B-tree traversal finds no entry for the ISA, or the open-list check fails (an uncreated document cannot be open). Either way, `findorgl` returns FALSE.

The calling operation then silently does nothing — but due to the response-before-check pattern [EC-RESPONSE-BEFORE-CHECK], most state-modifying callers (`doinsert`, `dodeletevspan`, `dorearrange`, `docopy`) have **already sent a success response** to the front end before `findorgl` executes. The front end receives no indication of the failure. The document state is unchanged; the operation is a silent no-op.

`CREATELINK` is the documented exception — it checks `docreatelink()` success before sending the response, so a failed `findorgl` there does produce a proper error reply [EC-RESPONSE-BEFORE-CHECK].

## Code Exploration

The user needs to approve the write. Here is the full answer based on the code read:

---

## `findorgl` — B-Tree Walk, Not a Global Registry

### Short Answer

`findorgl` walks the granfilade B-tree using the document's I-address as a key. It does **not** traverse a global document registry. The BERT table consulted first is a session-level access control structure, not a document registry. A never-created address causes a clean FALSE return — no crash.

---

### Phase 1: BERT Hash Table — Access Control Only [`granf1.c:22–38`]

```c
if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
    if (!isxumain) { return FALSE; }
}
```

`checkforopen` [`bert.c:52`] looks up `isaptr` in `berttable` — a 1327-bucket hash table (`berttable[NUMBEROFBERTTABLE]` at `bert.c:29`) of `bertentry` nodes, each holding `{connection, documentid, type, count}`. This table only contains documents **currently open in active sessions** (populated by `addtoopen` [`bert.c:128`]).

This is **not** a document existence check. It is a concurrency lock / permissions gate. When `type == NOBERTREQUIRED` [`common.h:165`], `checkforopen` short-circuits immediately at `bert.c:59–61` returning 1, and Phase 1 is skipped entirely. This is the path used by `docopyinternal` [`do1.c:75`] and other internal callers.

---

### Phase 2: Granfilade B-Tree Walk [`granf1.c:39`]

```c
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

`granf` is a single system-wide enfilade root (type `GRAN`), declared at `corediskout.c:21`, exported via `xanadu.h:13–14`, and initialized at startup:

```c
granf = (typegranf) createenf(GRAN);   // entexit.c:44
```

Every call site in the codebase passes this same global `granf` as `granfptr`. There is no per-document registry — all documents' orgl roots live as `GRANORGL`-type leaf nodes in this one global tree, keyed by I-address.

#### Inside `fetchorglgr` [`granf2.c:22`]

**1. Bounds check [`granf2.c:31–32`]:**
```c
if (tumblercmp(&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return NULL;
```
If `address` exceeds the tree's total width extent, return NULL immediately.

**2. B-tree descent [`granf2.c:34`]:**
```c
context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH);
```
`retrievecrums` [`retrie.c:15`] calls `findcbcseqcrum` [`retrie.c:167`], which recursively descends from root to leaf, at each internal node walking siblings and accumulating the `WIDTH` offset dimension, using `whereoncrum(ptr, offset, address, WIDTH)` to branch. This is a standard ordered B-tree search on the WIDTH index.

**3. Exact match check [`granf2.c:37–40`]:**
```c
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return NULL;
}
```
After reaching a leaf, the accumulated `totaloffset` must equal the requested address exactly. If the address was never inserted, the nearest leaf has a different offset — equality fails — NULL returned.

**4. Leaf type and orgl extraction [`granf2.c:51–80`]:**
The leaf's `cinfo.infotype` must be `GRANORGL` (= 2, defined at `wisp.h:70`). The leaf stores a `typegranorgl` struct [`wisp.h:88–93`]:

```c
typedef struct structgranorgl {
    struct structcuc *orglptr;       // the POOM enfilade root
    typediskloafptr diskorglptr;     // disk location if paged out
    bool orglincore;
} typegranorgl;
```

If `!orglincore`, the orgl is loaded from disk via `inorgl` before returning.

---

### What Happens for a Never-Created Address?

**Case A: `type == NOBERTREQUIRED` (internal callers):**
Phase 1 is skipped. `fetchorglgr` walks the B-tree:
- If address is within the tree's extent but not present: exact match fails at `granf2.c:37` → NULL returned.
- If address is beyond the tree's maximum extent: bounds check at `granf2.c:31` returns NULL immediately.

In both cases: `*orglptr = NULL`, `findorgl` returns FALSE [`granf1.c:40`]. No crash.

**Case B: `type == READBERT` or `WRITEBERT` (user-facing):**
The document has never been opened, so it is absent from the BERT table. `checkforopen` returns ≤ 0. In the DISTRIBUTION build, `findorgl` sets `*orglptr = NULL` and returns FALSE at `granf1.c:33–36`, without ever touching the B-tree. In the debug build, it prints to stderr and also returns FALSE at `granf1.c:27–30`.

---

### Data Flow Summary

```
findorgl(taskptr, granf, &docisa, &docorgl, READBERT)
│
├─ Phase 1: checkforopen(docisa, READBERT, user)    [bert.c:52]
│    └─ hash table lookup in berttable[1327]
│    └─ returns ≤ 0 if not "open" → *orglptr=NULL, return FALSE
│
└─ Phase 2: fetchorglgr(taskptr, granf, &docisa)    [granf2.c:22]
     ├─ bounds check: granf->cwid.dsas[WIDTH] vs docisa  [granf2.c:31]
     ├─ B-tree walk: retrievecrums → findcbcseqcrum       [retrie.c:15,167]
     │    └─ recursive descent, WIDTH dimension key
     ├─ exact match: totaloffset == docisa?               [granf2.c:37]
     │    └─ NO → crumcontextfree, return NULL
     └─ YES: extract GRANORGL leaf, load from disk if needed [granf2.c:51–80]
             return orglptr (POOM enfilade root)
```

---

### Key Source Citations

| Claim | Location |
|---|---|
| `findorgl` signature | `granf1.c:17` |
| BERT gate + return FALSE | `granf1.c:22–38` |
| Call to `fetchorglgr` | `granf1.c:39` |
| NOBERTREQUIRED short-circuit | `bert.c:59–61` |
| BERT hash table definition | `bert.c:27–29` |
| `granf` global var | `corediskout.c:21`, `xanadu.h:13–14` |
| `granf` initialization | `entexit.c:42–44` |
| `fetchorglgr` entry | `granf2.c:22` |
| Bounds check | `granf2.c:31–32` |
| `retrievecrums` call | `granf2.c:34` |
| Exact match check | `granf2.c:37–40` |
| `retrievecrums` → `findcbcseqcrum` | `retrie.c:15–30` |
| `findcbcseqcrum` B-tree walk | `retrie.c:167–189` |
| `typegranorgl` struct | `wisp.h:88–93` |
| `GRANORGL` constant | `wisp.h:70` |
