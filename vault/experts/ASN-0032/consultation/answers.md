# Consultation Answers — Link Ontology

**Inquiry:** What is a link in the Xanadu system? What are links for, what do they connect, and what must be true about them as permanent objects in the docuverse?
**Date:** 2026-03-12 14:17
**Questions:** 20 (10 nelson, 10 gregory)

---

## Question 1 [nelson]

> What does a link actually connect — whole documents, specific spans of content within documents, or both?

### Nelson's Answer

# What Does a Link Connect?

**Both.** A link connects **arbitrary span-sets** — which can be specific byte ranges within documents, whole documents, or even collections spanning multiple documents. The mechanism is unified; there is no separate "document link" vs "span link."

## The Core Mechanism: Spans, Not Points

Nelson is explicit that links are not point-to-point:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Each link has three endsets (from-set, to-set, type), and each endset is an **arbitrary collection of spans**:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

A single endset can touch bytes scattered across multiple documents. This is the general case.

## Whole-Document Links: Metalinks

Nelson explicitly addresses whole-document linking through **metalinks**:

> "METALINKS: These are links expected to apply to whole documents, whether from outside or from inside." [LM 4/52]

Examples include Title links (from title text to the whole document), Author links (from author name to the whole document), and Supersession links (declaring one document replaces another). These use the same link mechanism — the endset simply spans the entire document rather than a fragment within it.

## The Scale Is Continuous

The span mechanism makes the scale continuous, from one byte to the entire docuverse:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." [LM 4/38]

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." [LM 4/24]

So a link's from-set could be a single word, a paragraph, a chapter, a whole document, or every document on a server — all using the same addressing and search machinery.

## Why This Matters

This design yields **link survivability**. Because links attach to bytes (via I-space addresses), not to positions:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

If links connected only whole documents, survivability would be trivial but the link would lack precision. If links connected only single points, they would be fragile. Span-based linking gives both precision and resilience — the strap stays attached to whatever bytes remain.

## Summary

A Xanadu link connects **span-sets to span-sets**, where each span-set can be:
- A single byte
- A contiguous passage
- A discontiguous collection of passages across multiple documents
- An entire document
- An entire account or server's worth of content

There is one mechanism, not two. Metalinks (whole-document links) are simply links whose endsets happen to span entire documents.

---

## Question 2 [nelson]

> Must every link be a permanent object in the docuverse with its own stable identity, just as documents and content are permanent?

### Nelson's Answer

# Are Links Permanent Objects in the Docuverse?

**Yes.** The evidence from Literary Machines is strong and consistent: links are permanent objects with stable identity, treated architecturally on par with content bytes.

## Links Are One of Only Two Stored Object Types

Nelson is explicit that the docuverse stores exactly two kinds of things:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Everything else — servers, accounts, documents — are "ghost elements" that exist only as conceptual positions in the address hierarchy. Links and bytes are the real, stored substance of the docuverse.

## Links Have Permanent Tumbler Addresses

Links occupy the `2.x` subspace within a document and are addressed by creation order. Crucially, this order is permanent:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

This means link `2.1` is always the first link created in that document, link `2.755` is always the 755th. Deleting link `2.5` does not renumber `2.6` through `2.N`. The address is stable and never reused.

This is stronger than the permanence of byte positions. Bytes can be rearranged in V-space (their visual positions shift with editing). Links cannot — they keep their creation-order addresses permanently.

## Link-to-Link Requires Stable Identity

The strongest architectural argument: because links have tumbler addresses, other links can point to them.

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." [LM 4/49]

If Alice creates a link and Bob creates a link-to-link pointing at Alice's link, Bob's link depends on Alice's link having a stable, resolvable address — exactly the same dependency that makes published documents permanent:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility." [LM 2/43]

Nelson does not explicitly extend this obligation to links targeted by other links, but the architectural logic is identical: if links can be targets, they must be reliable targets.

## "Deleted" Links Are Not Destroyed

Page 4/9 shows a diagram of a document's technical contents. Both deleted bytes and deleted links receive the **exact same description**:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This parallel treatment is telling. "Deleting" a link does not destroy it — it moves the link to a state of being "not currently addressable," just as deleting bytes removes them from V-space but preserves them in I-space. The link awaits historical backtrack (can be recovered from version history) and may persist in other versions of the document.

## The Overall Architecture

Putting it together:

| Property | Content Bytes | Links |
|----------|--------------|-------|
| Actually stored in tumbler-space | Yes [4/23] | Yes [4/23] |
| Permanent address | Yes (I-space) | Yes (creation order) [4/31] |
| Can be target of links | Yes | Yes [4/49] |
| "Deletion" = not currently addressable | Yes [4/9] | Yes [4/9] |
| Recoverable via historical backtrack | Yes [4/9] | Yes [4/9] |
| May persist in other versions | Yes [4/9] | Yes [4/9] |

Links enjoy the same permanence architecture as content. They are stored objects with permanent addresses, can be targets of other links, and are not destroyed by deletion — only rendered "not currently addressable."

## One Nuance

Links CAN be deleted by their owner (the owner of the link's home document). Nelson does not impose the same explicit withdrawal restriction on individual links that he imposes on published documents. But the deletion semantics — "awaiting historical backtrack functions, may remain included in other versions" — make clear that even "deleted" links are preserved in the system, just as "deleted" bytes are.

The system's permanence guarantee — "any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19] — applies to link addresses as much as to any other tumbler address. Once a link exists at address `N.0.U.0.D.V.0.2.1`, that address is permanently assigned and never recycled.

---

## Question 3 [nelson]

> Must a link remain valid and meaningful even after the content it connects has been edited, rearranged, or extended by its author?

### Nelson's Answer

# Yes. Absolutely. This Is the Whole Point.

A link **must** survive editing, rearrangement, and extension of the content it connects. This is not a nice-to-have feature — it is the architectural reason Xanadu's addressing system exists at all.

## The Mechanism: Straps Between Bytes

I designed links to attach to **spans of bytes**, not to positions between bytes. Think of a link as a strap binding bytes together:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived."
> — [LM 4/42]

The visual annotation on the following page makes this explicit:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"
> — [LM 4/43]

## Why This Works: I-Space vs V-Space

The deeper reason links survive editing is the separation of **I-space** (where content permanently lives) from **V-space** (the document's current arrangement).

When you edit a document, you change V-space — you rearrange, insert, delete from the current view. But the content itself remains at its permanent I-space address. Links point to I-space, not V-space. Therefore:

- **Insert** new content → V-space positions shift, but I-space addresses are unchanged. Links unaffected.
- **Rearrange** content → V-space order changes, but I-space identity unchanged. Links unaffected.
- **Delete** content → V-space mapping removed, but I-space content remains. Links still resolve to the I-space address.
- **Extend** with new material → new bytes get new I-space addresses. Existing links still point to existing bytes. Unaffected.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."
> — [LM 4/30]

## Links Across Versions

The question extends naturally to versioning. When a document is superseded by a new version, links made to the old version reach through into the new one:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version."
> — [LM 2/43]

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions."
> — [LM 2/26]

This is what I call **refractive following** — the system traces correspondence (shared I-space origin) to find the same content in a different version's arrangement. A link made to version 1 works in version 5, provided the bytes still exist somewhere.

## The Only Way a Link Breaks

A link breaks **only** when all the bytes at one of its endsets have been deleted from every version. As long as any bytes remain at each end, the link remains valid:

> "If any of the bytes are left to which a link is attached, that link remains on them."
> — [LM 4/42]

And even "deleted" bytes are not truly destroyed — they persist in I-space, recoverable through historical backtrack:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"
> — [LM 4/9]

## Why This Must Be So

Links create **permanence obligations**. Once others have linked to your published document, you cannot withdraw it — their links depend on its accessibility:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility."
> — [LM 2/43]

If links broke every time an author edited their document, the entire web of interconnected literature would be fragile and useless. The whole system exists to preserve the structure of literature — and that structure is made of links. If links don't survive editing, you don't have Xanadu. You have the World Wide Web, with its perpetual broken links and link rot.

## Summary

| Operation | Link survives? | Why |
|-----------|---------------|-----|
| **Insert** new content nearby | Yes | I-space addresses unchanged |
| **Rearrange** content order | Yes | Links follow bytes, not positions |
| **Delete** some linked bytes | Yes, if any remain | Partial survival by design |
| **Delete** all linked bytes | Structurally broken | But bytes persist in I-space for backtrack |
| **Extend** document | Yes | New bytes get new addresses; existing links unaffected |
| **Create new version** | Yes | Refractive following through correspondence |

The answer is not merely "yes" — it is that the entire architecture, from I-space/V-space separation to span-based endsets to tumbler addressing, was designed precisely to make this guarantee possible.

---

## Question 4 [nelson]

> Must a link be visible and discoverable from both ends — so that an author can always see who has linked to their content?

### Nelson's Answer

## Yes — Bidirectional Link Discovery Is a Core Guarantee

Nelson is emphatic on this point. The system architecturally ensures that for any published content, the author (or any reader) can discover all links pointing to it. This is not an optional feature but a structural property of how links work.

### The Explicit Guarantee

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

And from the windowing discussion:

> "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

### Why This Works Architecturally

Links are indexed by **all three endsets** (from, to, type). The FEBE operation `FINDLINKSFROMTOTHREE` searches across any combination:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

To find everything linking TO your document, you specify your document's address in the to-set parameter. The system returns all matching links regardless of who created them or where they live. Nelson guarantees this scales:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

### The Two-Sided Coin

Nelson frames this as inseparable from link freedom. You cannot have free linking without accepting discoverable incoming links:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

The author gives up **control** over incoming links — they cannot prevent or remove them. But they gain **visibility** — they can always see what connects to their work.

### Sieving the Avalanche

Nelson anticipated that popular documents would attract enormous numbers of incoming links, so he designed filtering:

> "Thus it becomes necessary to apply some kind of filter, saying, 'What links come in from Spain? From last week? From persons of importance to me?'" [LM 2/47]

> "This filtering by different attributes we call 'sieving', and it can only be set up for a comparatively small number of traits— say, location and author and time." [LM 2/47]

### The Private Link Nuance

One qualification: Nelson says users can link "privately or publicly" [LM 2/43]. A link in a private document would presumably be subject to that document's access restrictions. In XU.87.1 this is moot — "Currently all documents are visible to all users" [LM 4/79] — but in the full design, a private link to your published document may not be discoverable by you.

This is not a contradiction. The guarantee is that **the system provides the mechanism** for bidirectional discovery. Published links to published content are always discoverable from both ends. Private links respect their owner's privacy.

### Summary

Bidirectional link discovery is not merely supported — it is **required** by the architecture. The three-endset link structure with universal indexing means every published link is findable from the from-side, the to-side, or the type. An author can always see who has publicly linked to their work. This is what Nelson means when he says Xanadu solves "the backlinks problem" that conventional hyperlinks cannot.

---

## Question 5 [nelson]

> Does a link exist outside the documents it connects, as an independent object in the docuverse rather than being embedded inside one of them?

### Nelson's Answer

## Yes and No — Links Are Independent of What They Connect, But Not Free-Floating

The answer is both yes and no, and the distinction matters.

### Yes: A Link Is Independent of the Documents It Connects

A link does NOT live inside the documents it connects. It lives in its **home document**, which can be entirely separate from the documents at either end:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

The MAKELINK operation makes this explicit:

> "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents." (4/63)

So if Alice writes document A and Bob writes document B, Carol can create a link in her own document C that connects passages in A to passages in B. Carol's link lives at Carol's address, under Carol's ownership. Neither Alice nor Bob can delete it.

Links have their own tumbler addresses in the **2.x subspace** of their home document, their own endsets reaching out across the docuverse, and their own survival properties independent of the documents they connect.

### No: Nothing in Xanadu Is Truly Free-Floating

Every link must have a home document. There are no objects in the docuverse outside the document structure:

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." (2/29)

A link is always *part of* a document — it just isn't part of the documents it *connects*. The home document is where it physically resides, determines who owns it, and provides its tumbler address.

### The Design Intent

This separation of link residence from link targets is one of my most important architectural decisions. It solves the **marginalia problem**: how do you annotate someone else's work without modifying it?

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." (2/31)

Your links are YOUR property at YOUR address. They reach into other people's documents without touching them. The target author cannot delete your links — they can only delete content that the links point to. And even that won't necessarily kill the link, because links attach to spans of bytes and survive as long as any bytes remain at each end (4/42).

This is why I insisted that published documents cannot be withdrawn — other people's links depend on their continued existence. Those links are other people's property, stored at other people's addresses.

### Summary

A Xanadu link is **structurally independent** of the documents it connects — it lives in a separate home document, has its own address, and is owned by its creator. But it is not **ontologically independent** — it must always belong to some document. The docuverse contains documents and nothing else; links are elements within documents that happen to reach across the entire address space.

---

## Question 6 [nelson]

> Who owns a link — the person who created it, one of the connected document authors, or does ownership not apply to links?

### Nelson's Answer

## Link Ownership: The Creator Owns the Link

The answer is unambiguous: **the person who created the link owns it.** Ownership is determined by the link's *home document*, not by the documents it connects.

### The Core Rule

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user."
> — [LM 4/41]

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document."
> — [LM 4/12]

This is a deliberate separation of **ownership** from **application**. A link lives at an address in the creator's document space. That address determines who controls it — regardless of what content the link connects.

### Out-Links vs. In-Links

Nelson draws a sharp distinction between links you made (out-links) and links others made pointing to your content (in-links):

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not."
> — [LM 2/31]

If I create a comment link from my document to yours, that link is **mine**. It lives at my address. You cannot delete it, modify it, or prevent it. You control your content; I control my links.

### Why This Matters

This design solves the **marginalia problem**. In the paper world, your notes in your copy of a book don't reach anyone else. In Xanadu, your annotations are links that you own, stored at your address, but visible to anyone reading the annotated material. The target author has no veto power over your commentary.

It also explains why **published documents cannot be withdrawn**:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process."
> — [LM 2/43]

Other users' links — which are *their property* at *their addresses* — depend on the continued existence of the target content. Withdrawing a published document would break other people's property.

### The Address Structure Confirms This

Links within a document occupy the `2.x` subspace of that document's tumbler address:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

The `N.0.U.0.D` portion encodes node, account, and document — which identifies the owner. The link's permanent address is under the creator's account, not under the accounts of the connected documents' authors.

### Summary

| Question | Answer |
|----------|--------|
| Who owns a link? | The creator (owner of the link's home document) |
| Can the target author delete it? | No |
| Can the target author prevent it? | No — free linking is part of the publication contract |
| Can the creator delete it? | Yes — it's their property |
| Does ownership transfer? | No — the home address is permanent |

---

## Question 7 [nelson]

> Can a link ever be destroyed or retracted, or does permanence mean that once a link exists it must exist forever?

### Nelson's Answer

## Link Deletion in Xanadu: Yes, But Never Truly Destroyed

A link **can** be deleted by its owner — but "deleted" in Xanadu does not mean what it means elsewhere. The link enters a liminal state: gone from current view, but not destroyed.

### The Owner Can Delete

Links are owned property. The owner of a link's home document can remove it, just as they can delete bytes from their document:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

Nelson's technical diagram on page 4/9 explicitly lists **"DELETED LINKS"** as a valid document state, parallel to deleted bytes:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

### But Deletion Is Not Destruction

This is the critical Xanadu distinction. A "deleted" link is:

1. **Not currently addressable** — it disappears from the document's active view
2. **Awaiting historical backtrack** — it remains recoverable through version history
3. **Potentially alive in other versions** — if someone versioned your document before you deleted the link, their version still contains it

This follows the same principle as content deletion. Nelson rejects "destructive replacement" across the entire system. The append-only storage model means the link's I-space record persists even after V-space removal.

### Who Can and Cannot Delete

| Actor | Can they delete the link? |
|-------|--------------------------|
| Link owner (home document owner) | **Yes** — it's their property |
| Target document author | **No** — they can delete *content* the link points to, but not the link itself |
| Anyone else | **No** — ownership is absolute |

This asymmetry matters. If I link to your published document with a critical annotation, you cannot remove my link. You can only delete the content it points to — which would cause the link to lose its anchor (surviving only "if anything is left at each end" [LM 4/42]).

### The Permanence Tension

There is a real tension in Nelson's design between two principles:

**Permanence of addresses:** "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19] — the link's tumbler address never becomes invalid.

**Owner's right to withdraw:** "Only the owner has a right to withdraw a document or change it." [LM 2/29] — the owner can remove their own links.

Nelson resolves this through the V-space/I-space separation. The link's *address* in I-space remains permanently assigned. The link's *presence* in the document's current V-space arrangement can be removed. Historical backtrack can reconstruct the state where the link existed.

### Published Documents Add Friction

For published documents specifically, withdrawal is harder:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Since links live inside documents, a published document's links inherit this friction. Nelson doesn't specify whether individual links within a published document can be deleted independently of the document itself — but the "deleted links" state on 4/9 applies to document contents generally.

### Summary

Once a link exists, it can be **retracted from current view** by its owner, but it is **never truly destroyed**. The I-space record persists, version history preserves it, and other versions may still contain it. Permanence in Xanadu means the *record* of the link's existence survives even the owner's decision to remove it — you can always reconstruct the moment when it was there.

---

## Question 8 [nelson]

> How do links relate to quotation and transclusion — is a transclusion a special kind of link, or are they fundamentally different operations?

### Nelson's Answer

## Links and Transclusion: Architecturally Distinct

This is a question that reveals a common confusion, and I want to be precise about the architecture because I was admittedly looser with terminology in Chapter 2 than in Chapter 4.

**Transclusion and links are fundamentally different operations.** They operate at different levels of the system and are implemented by different FEBE commands.

### Transclusion Is a V-Space Structural Operation

Transclusion is performed by the **COPY** command. It makes bytes from one document appear in another document's virtual byte stream:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

The result is that non-native bytes become part of the document's V-stream:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

No link is created. The content simply appears in the document, fetched from its permanent I-space location. The system always knows the origin because:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

### Links Are Separate Meta-Virtual Structures

A link is created by the **MAKELINK** command — a different FEBE operation entirely. Links are connective units with their own addresses, their own owners, and three endsets (from, to, type):

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." [LM 4/41]

Links don't move or include content. They create navigable connections between content that exists independently.

### The Quote-Link Is Where the Confusion Arises

In Chapter 2, when describing the user experience, I used "quote-window" and "quote-link" somewhat interchangeably:

> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link." [LM 2/32]

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

But in the technical specification, I drew the distinction explicitly:

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated." [LM 4/53]

This is the critical sentence. A **quote-link** is a link that *marks* a transclusion — it is "the author's acknowledgment of material origin" [LM 4/53]. The **inclusion** (transclusion) is the structural fact; the quote-link is an optional annotation layered on top.

### How They Work Together

A compound document involves both mechanisms:

1. **COPY** operations that structurally include content from other documents in the V-stream (transclusion)
2. **MAKELINK** operations that optionally create quote-links marking those inclusions for the reader

An inclusion *without* a quote-link still works perfectly — the content appears, and the system can always trace its origin via I-addresses. But the reader may see no visual indication that the content came from elsewhere. The quote-link adds that visible signal.

Think of it through the glass pane metaphor:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else." [LM 2/34]

The clear glass — the window — is the transclusion (COPY). It is structural: content from below shows through. A quote-link would be a frame painted around that window, telling the reader "you are looking through to another document here."

### Why This Matters

The separation serves the principle that **attribution is structural, not metadata**:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This guarantee holds whether or not a quote-link exists, because the I-address of every byte encodes its origin. The quote-link is a courtesy to the reader; the I-space architecture is the guarantee to the system.

The separation also means transclusion can exist without cluttering the link space, and links can exist without requiring structural inclusion. You can link to a passage without quoting it. You can include a passage without explicitly marking it. The two mechanisms compose freely.

### Summary

| Mechanism | FEBE Command | What It Does | Creates a Link? |
|-----------|-------------|--------------|-----------------|
| **Transclusion** | COPY | Includes bytes in V-stream from another document's I-space | No |
| **Quote-Link** | MAKELINK | Marks an inclusion with visible attribution | Yes |
| **Ordinary Link** | MAKELINK | Connects spans without inclusion | Yes |

Transclusion is the plumbing. The quote-link is the label on the pipe. Both exist because literature needs both structural quotation and navigable connection — but they are not the same thing.

---

## Question 9 [nelson]

> Must the system guarantee that every version of a document preserves the links that were present at each point in its history?

### Nelson's Answer

## Yes — but the mechanism is implicit, not independently specified

Nelson's architecture strongly implies that link state is preserved per-version, but he never provides an explicit, separate guarantee for link history. The evidence comes from three converging lines.

### 1. Deleted links explicitly await historical backtrack

The strongest direct evidence is the status description for deleted links on page 4/9:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, **may remain included in other versions**.)" [LM 4/9]

This exactly parallels deleted bytes:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "may remain included in other versions" means that if you delete a link from version N, earlier versions that contained that link still show it. This only works if versions capture link state.

### 2. The general historical backtrack guarantee covers links

Nelson's version history guarantee is stated broadly:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

And the retrieval operation returns both content types together:

> **RETRIEVEV**: "This returns the material (text and links) determined by \<spec set\>." [LM 4/67]

If RETRIEVEV returns text *and* links, and the system promises reconstruction of any previous state, then that reconstructed state must include the links that existed at that time.

### 3. Links live in the append-only store

Links have permanent tumbler addresses in the `0.2.N` subspace, assigned in order of arrival:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The append-only model means these addresses are never reused. A link at `D.V.0.2.5` always refers to the 5th link created in that document. "Deleting" it removes it from the current V-space view but not from I-space — the same non-destructive semantics as byte deletion.

### What IS ambiguous

There is a genuine gap around **CREATENEWVERSION**:

> "This creates a new document with the contents of document \<doc id\>." [LM 4/66]

Nelson separately describes a document as consisting of "its contents (including history and alternatives) and its out-links" [LM 2/31]. Whether "contents" in the CREATENEWVERSION command includes out-links or only bytes is not explicit. The grammar of 2/31 could be read either way — "contents" as an umbrella term, or "contents" and "out-links" as distinct components.

However, the weight of evidence favors inclusion. Links are part of the document's tumbler subspace, retrieval returns both, and the deleted-link description explicitly references version preservation.

### What Nelson does NOT specify

- The **mechanism** for link-specific historical backtrack. Byte history has detailed infrastructure (enfilades, I-space/V-space separation). Link history has no corresponding architectural description.
- Whether link history is tracked with the same granularity as byte history (every individual change vs. version snapshots).
- How link deletion interacts with SHOWRELATIONOF2VERSIONS — whether version comparison reports link differences, not just content differences.

NEED_RAW: [4/9, 4/30-4/31] — to verify the full context of the deleted-links diagram and the link addressing details around version boundaries.

### Summary

The system **should** guarantee per-version link preservation. This follows from the explicit "may remain included in other versions" status of deleted links, the general historical backtrack promise, and the append-only storage model. But Nelson treats this as a consequence of the architecture's general properties rather than stating it as an independent guarantee — and the detailed mechanism for link history reconstruction is left unspecified.

---

## Question 10 [nelson]

> Can anyone create a link to any content in the docuverse, or must the system enforce permissions about who may link to what?

### Nelson's Answer

## Anyone May Link to Any Published Content — Without Permission

This is one of Nelson's most emphatically stated design principles. The system does **not** enforce permissions about who may link to published content. Link freedom is a contractual guarantee, not a conditional feature.

### The Core Rule

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

This is not optional. Relinquishing control over incoming links is a **condition of publication**:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

### Why No Link Permissions

The architecture makes link control by the target author structurally impossible — and intentionally so. Links are owned by their creators, stored at their creators' addresses, independent of the documents they connect:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

A document's in-links are explicitly outside the owner's control:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." [LM 2/31]

### The One Exception: Private Documents

The only access restriction applies to **private** (unpublished) documents. From the session model:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

This is an access control, not a link permission. You can't link to private content because you can't *see* it — not because linking is forbidden.

### The Deeper Principle

Link freedom is what makes the docuverse self-organizing. Nelson envisions literature as "socially self-constructing" through the collective link-making activity of all users. If authors could block incoming links, the web of interconnection that gives the system its value could not form.

The tradeoff is explicit and deliberate: you give up control over how your published work is referenced, but you never give up compensation for its use. Automatic royalties replace permission-based control.

> "There is no way whatever to ascertain or control what happens at the users' terminals. Therefore perforce all use whatever is legitimate, and anyone who plans to be vulnerable to 'misuse,' whatever he or she thinks that may be, had better keep his or her stuff off the system." [LM 2/47]

### Summary

| Content State | Can anyone link to it? | Author can block links? |
|---------------|----------------------|------------------------|
| **Published** | Yes — unconditionally | No — relinquished at publication |
| **Private** | Only owner and designees | N/A — access-controlled, not link-controlled |

The system enforces **no** permissions about who may link to published content. This is by design and by contract.

---

## Question 11 [gregory]

> When a link's source endset contains multiple non-contiguous I-spans (e.g., from content that was rearranged after link creation), does RETRIEVEENDSETS return all spans as a single specset, and does the ordering of spans within that specset carry semantic meaning?

### Gregory's Answer

## KB Synthesis

## RETRIEVEENDSETS with Non-Contiguous I-Spans

**Does it return all spans as a single specset?**

Yes, for each endset type. RETRIEVEENDSETS returns three specsets simultaneously (from-endset, to-endset, three-endset), and within each, all resolvable I-spans are included [SS-RETRIEVE-ENDSETS]. The conversion path (`retrievesporglsetinrange` → `linksporglset2specset`) iterates over every sporgl in the endset and converts each I-span to V-addresses via the querying document's POOM. I-addresses with no current POOM mapping are **silently dropped** without error [SS-FOLLOWLINK], [INV-ITOV-FILTERING]. So the returned specset is the set of *resolvable* spans, which may be smaller than the full endset if content was deleted.

**Does ordering carry semantic meaning?**

Yes, with a caveat about fragmentation artifacts.

The I-to-V conversion path uses `incontextlistnd()`, which performs insertion-sort by V-address left boundary during B-tree traversal [INV-RETRIEVAL-V-SORTED]. This ordering is independent of tree structure — it holds regardless of how splits or rebalances arranged the internal nodes [INV-RETRIEVAL-TREE-INDEPENDENCE]. The returned specset spans are therefore **sorted in ascending V-address order**.

This ordering is semantically meaningful in the same way SpecSet ordering is generally meaningful: consuming operations (retrieve, vcopy) process VSpecs in sequence order [INV-SPECSET-ORDER], so a V-sorted endset specset reflects document position order.

**The fragmentation caveat**

When linked content has been rearranged, the endset can fragment and even produce **duplicated spans** [EC-PIVOT-LINK-FRAGMENTATION]. For example, a link on "CD" → pivot → four spans reported (1.2 for 0.1 twice, 1.5 for 0.1 twice). This duplication arises from the underlying sporgl structure: each contiguous I-address region becomes a separate sporgl [SS-LINK-ENDPOINT], and if rearrangement causes the same content to appear at multiple V-positions, the V-sorted result may contain multiple entries for logically the same content. The ordering within these duplicates still follows V-address sort, but the caller cannot treat the returned spans as a canonical non-redundant partition [EC-MULTISPAN-LINK-DUPLICATION].

**Summary**

| Property | Answer |
|---|---|
| All spans in one specset? | Yes (per endset type), silently filtered to resolvable I-addresses |
| Ordering guarantee | Ascending V-address left boundary (via `incontextlistnd` insertion-sort) |
| Ordering semantics | Yes — positional order in current document, used by consuming operations |
| Duplicates possible? | Yes, after rearrangement of linked content |

---

## Code Exploration

Now I have all the source I need. Here is the complete answer.

---

## RETRIEVEENDSETS and Multi-Span Endset Ordering

### 1. Does RETRIEVEENDSETS return all spans as a single specset?

**Yes.** For a link whose endset contains multiple non-contiguous I-spans from the same document, RETRIEVEENDSETS returns a single `typespecset` containing exactly **one `typevspec`** element whose `vspanset` holds all the V-spans.

The full call chain:

**`fns.c:350`** — `retrieveendsets` invokes `doretrieveendsets`:
```c
void retrieveendsets(typetask *taskptr) {
    if (
       getretrieveendsets (taskptr, &specset)
    && doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset))
        putretrieveendsets (taskptr, fromset, toset, threeset);
```

**`do1.c:369`** — `doretrieveendsets` is a pure passthrough:
```c
bool doretrieveendsets(...) {
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

**`spanf1.c:190`** — `retrieveendsetsfromspanf` sets up three V-subspace probes (`fromspace` at mantissa[0]=LINKFROMSPAN=1, `tospace` at 2, `threespace` at 3) then executes the same pipeline for each endset:

```c
// spanf1.c:222-226
specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
&& retrievesporglsetinrange(taskptr, sporglset, &fromspace, &fromsporglset)
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

**`sporgl.c:97`** — `linksporglset2specset` converts the sporglset to a specset. For each sporgl with a non-zero `sporgladdress` (every content sporgl has a homedoc), it calls `linksporglset2vspec`:
```c
for (; sporglset; sporglset = ...) {
    specset = taskalloc(taskptr, sizeof(typevspec));
    if (iszerotumbler(&sporglset->sporgladdress)) {
        // stores as raw ISPANID
    } else {
        linksporglset2vspec(taskptr, homedoc, &sporglset, (typevspec*)specset, type);
    }
    ((typeitemheader*)specset)->next = NULL;
    *specsetptr = specset;
    specsetptr = (typespecset*)&((typeitemheader*)specset)->next;
}
```

**`sporgl.c:141`** — `sporglset2vspanset` (called from `linksporglset2vspec`) consumes **all consecutive sporgls with the same `sporgladdress`** in one pass:
```c
for (;;) {
    sporglptr = sporglptr->next;
    if (
       !sporglptr
    || !(sporglptr->itemid == SPORGLID)
    || !tumblereq (&sporglptr->sporgladdress, &(*sporglsetptr)->sporgladdress))
        return(0);   // ← breaks when homedoc changes
    *sporglsetptr = (typesporglset)sporglptr;   // ← advances outer loop pointer
    ...
    vspansetptr = ispan2vspanset(taskptr, orgl, &ispan, vspansetptr);
}
```

Because all I-spans in a single endset share the same document (same `sporgladdress`), this inner loop consumes all of them, folding their corresponding V-spans into a single `vspanset`. The outer loop in `linksporglset2specset` then advances past the last consumed sporgl (via the pointer update), so the result is **a single `typevspec` element** in the returned specset.

---

### 2. Does the ordering of spans within that specset carry semantic meaning?

**The ordering is mechanically determined by I-space address, not by document reading order.** Specifically:

#### Source of Ordering: `incontextlistnd` sorts by SPANRANGE

**`spanf1.c:237`** — `retrievesporglsetinrange` calls `retrieverestricted` to query the spanfilade for the link's I-span content entries, with `index1 = SPANRANGE`:
```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE, whichspace, ORGLRANGE, ...);
```

**`retrie.c:87`** — `retrieveinarea` calls `findcbcinarea2d`, which at each leaf calls:
```c
// retrie.c:262-263
context = makecontextfromcbc((typecbc*)crumptr, (typewid*)offsetptr);
incontextlistnd(headptr, context, index1);
```

**`context.c:75`** — `incontextlistnd` has an explicit comment and sorts insertion-position by `grasp.dsas[index]` (the SPANRANGE coordinate):
```c
/* put c on clist in index order */
int incontextlistnd(typecontext **clistptr, typecontext *c, INT index)
{
    prologuecontextnd(c, &grasp, (typedsp*)NULL);
    ...
    if (whereoncontext(clist, &grasp.dsas[index], index) < THRUME) {
        c->nextcontext = clist;
        *clistptr = c;   // ← insert at front if grasp is less
    } else {
        for (; nextc = clist->nextcontext; clist = nextc) {
            // insert in sorted position
        }
    }
}
```

So the **context list — and thus the sporglset** — is in ascending I-space address order.

#### How V-spans are ordered within the vspanset

Each sporgl's I-span is converted to V-span(s) via:

**`orglinks.c:389`** → **`orglinks.c:404`** → **`orglinks.c:425`**:
```c
typevspanset *ispan2vspanset(...) {
    return permute(taskptr, orgl, ispanptr, I, vspansetptr, V);
}
// permute calls span2spanset for each restriction span:
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                             (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan*)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
```

`onitemlist` (`orglinks.c:464`) **appends to the tail** — no sorting. The ordering of V-spans in the vspanset is therefore the POOM traversal order for each I-span restriction, which is again driven by `findcbcinarea2d` + `incontextlistnd` — i.e., **I-space order within each I-span lookup**.

Note: `putvspaninlist` (the V-tumbler-sorted insertion used in other contexts like `retrievevspansetpm`) is **not called here**. The endset V-spans are appended in I-space traversal order, not sorted by V-tumbler.

---

### Summary

| Property | Answer |
|---|---|
| All spans returned as single specset? | **Yes** — one `typevspec` whose `vspanset` contains all V-spans |
| Ordering mechanism | `incontextlistnd` sorts contexts by **SPANRANGE (I-space address)** |
| What "I-space order" means | Permascroll position of the original content fragment at time of insertion |
| After rearrangement | I-span order ≠ V-span (document) order; returned V-spans reflect **current V-positions** for those I-addresses, but ordered by their I-space origin, not current document reading order |
| Explicit semantic meaning of order | **None defined** — the ordering is a mechanical artifact of the enfilade traversal (ascending I-space), not a semantic guarantee like "primary span first" |

**Practical consequence:** If a link's source endset was created over content at V-positions [A, B, C] and content was subsequently rearranged so those positions moved to [C, A, B], RETRIEVEENDSETS returns all three spans in a single vspec but their order within the vspanset reflects the original **I-space addresses** (permascroll order), not the new document reading order. No semantic priority is encoded in position.

---

## Question 12 [gregory]

> The type endset references I-addresses at `1.0.2.x` in the global type namespace — what types were defined or envisioned, and does the type endset point to actual stored content in the granfilade (like a type name string) or to a conventionally assigned address?

### Gregory's Answer

## KB Synthesis

The KB has partial answers here — let me synthesize what's known and flag the gap.

## What Types Were Defined

From [SS-LINK-ENDPOINT] Finding 0024, the known type registry in the bootstrap document (doc 1) at `1.0.2.x`:

| Type     | Address     | Notes |
|----------|-------------|-------|
| JUMP     | `1.0.2.2`   | — |
| QUOTE    | `1.0.2.3`   | — |
| FOOTNOTE | `1.0.2.6`   | Parent of MARGIN |
| MARGIN   | `1.0.2.6.2` | Subtype of FOOTNOTE via containment |

The hierarchy is structural: MARGIN is a subtype of FOOTNOTE because `1.0.2.6.2` is contained within the tumbler range `1.0.2.6.*`, enabling range-match queries like "find all footnote-family links" [SS-LINK-ENDPOINT / Finding 0024].

## Content vs. Conventional Address

The KB is explicit that these are VSpec references that "participate in the same address/identity system as all other content" and are "content references, not metadata" [SS-LINK-ENDPOINT Finding 0024]. However, **the KB does not have a finding that confirms what is actually stored at those granfilade addresses** — whether there are actual content bytes (e.g., type name strings like "jump") or whether the addresses serve purely as identity tokens with no associated bytes.

What the KB does establish:

- The `link.type` field is a VSpec pointing into the bootstrap document's `1.0.2.*` subspace
- `QUOTE_TYPE` and `MARGIN_TYPE` are constructed in `febe/client.py` as VSpec objects referencing the bootstrap document [SS-LINK-ENDPOINT Finding 0024]
- Type endpoints occupy V-subspace `3.x` internally (`setlinkvsas()` increments digit 0 to 3 for type endpoints) [SS-SUBSPACE-CONVENTION Finding 0038]
- Type queries via address-range matching would work if type ISAs are indexed in the spanfilade — but whether bootstrap type addresses have DOCISPAN entries is not confirmed

## The Honest Answer

The design intent is clear: types are content-addressed objects in the bootstrap document, enabling type-based queries through the same I-address intersection mechanism used for source/target endpoint search. The tumbler containment hierarchy gives you subtype queries "for free" through range filtering.

Whether the bootstrap document actually contains readable text at those addresses (e.g., strings describing the link types) or just minimal placeholder content with assigned addresses — **the KB does not have a finding that resolves this**. This would require examining what `doinsert` (or equivalent bootstrapping code) places at `1.0.2.x` during system initialization.

---

## Code Exploration

Now I have everything I need. Let me compile the full answer.

---

## The Type Endset and `1.0.2.x` Addresses

### What the "Three Set" Is

When `docreatelink` is called [`do1.c:195`], it accepts a `threespecset` — the type endset — alongside the from/to specsets:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
```

All three endsets are stored in two places:
1. **In the link's own POOM (orgl)** via `insertendsetsinorgl` [`do1.c:218`], at fixed V-positions assigned by `setlinkvsas`
2. **In the global spanfilade** via `insertendsetsinspanf` [`do1.c:219`], tagged with span type `LINKTHREESPAN=3` [`xanadu.h:38`]

`setlinkvsas` assigns positions within the link's POOM [`do2.c:169-183`]:
```c
// from endset → position 0.1
// to   endset → position 0.2
// three (type) endset → position 0.3
tumblerincrement (threevsaptr, 0, 3, threevsaptr);
tumblerincrement (threevsaptr, 1, 1, threevsaptr);
```

These are positions within the **link's own orgl**, not the home document's address space.

---

### How the Type Specset Is Converted to Storage

`specset2sporglset` [`sporgl.c:14-33`] converts a VSpec to a sporgl (span + origin reference). For a type VSpec pointing to `LINK_TYPES_DOC` at V-span `1.0.2.X`:

```c
// sporgl.c:44-57
if (!findorgl (taskptr, granf, docisa, &orgl, type))
    return (NULL);   // ← if types doc doesn't exist, fails here
for (; vspanset; vspanset = vspanset->next) {
    vspanset2ispanset (taskptr, orgl, vspanset, &ispanset);
    // creates sporgl: {sporgladdress=docisa, sporglorigin=ispanset->stream, ...}
}
```

Then `insertendsetsinspanf` has an explicit NULL guard on the type set [`do2.c:122-126`]:
```c
if (threesporglset) {
    if(!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
        return (FALSE);
}
```

If `threesporglset` is NULL (because the types document doesn't exist or has no content at the target V-address), the `LINKTHREESPAN` entry is simply **never written to the spanfilade**. The link is stored without type information, silently.

---

### What Is `LINK_TYPES_DOC` and `1.0.2.X`?

From `client.py:597-612`:

```python
# Link type addresses - types are in document 1's link subspace (0.2)
# Full address format: 1.1.0.1.0.1.0.2.X where X is the type number
LINK_TYPES_DOC = Address(1, 1, 0, 1, 0, 1)  # Document 1 (bootstrap doc)

# Type numbers from the registry (link-types-relationship.md):
#   2.2 = jump, 2.3 = quote, 2.6 = footnote, 2.6.2 = footnote.margin
# Local address within doc: version.0.link_subspace.type = 1.0.2.X
JUMP_TYPE     = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 2), Offset(0, 1))])
QUOTE_TYPE    = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 3), Offset(0, 1))])
FOOTNOTE_TYPE = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6), Offset(0, 1))])
MARGIN_TYPE   = VSpec(LINK_TYPES_DOC, [Span(Address(1, 0, 2, 6, 2), Offset(0, 1))])
```

`1.0.2.X` is a **V-space address** within document `1.1.0.1.0.1`, structured as `version.0.link_subspace.type_number`. It is *not* a global I-address in the granfilade. The document's internal V-space is organized with link atoms in the `0.x` range and text in the `1.x` range [`finding 0009`], so `0.2.X` targets specific link positions within the link subspace.

The type assignments come from a non-existent `resources/link-registry/link-types-relationship.md` file referenced in the comment. The numbering (jump=2, quote=3, footnote=6, footnote.margin=6.2) is inherited from the original Xanadu specification/Literary Machines taxonomy. The non-contiguous gaps (1 unused, 4 and 5 skipped before footnote at 6) suggest the original registry had more types or reserved slots.

---

### Does the Granfilade Store Actual Content at Those Addresses?

**No, and there is no bootstrapping code to create it.**

`init.c` contains only function-dispatch initialization [`init.c:25-78`]. No document is created, no content is inserted. `be.c:37` establishes only the default account tumbler:
```c
tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */
```

For the type sporgl to resolve to anything, `LINK_TYPES_DOC = 1.1.0.1.0.1` would need to exist in the granfilade with content at V-positions `1.0.2.2`, `1.0.2.3`, etc. From the granfilade's address allocation logic [`granf2.c:158-181`], link atoms within document `D` are allocated at I-addresses `D.0.2.1`, `D.0.2.2`, ..., but only when explicitly created by client operations. None of this is pre-loaded.

As a result, in every session tested by this harness:
- `findorgl(granf, LINK_TYPES_DOC, ...)` returns NULL (document was never opened)
- `specset2sporglset` returns NULL for the type specset
- `threesporglset` is NULL
- The `if (threesporglset)` guard at `do2.c:122` is never taken
- All links are effectively **untyped from the backend's perspective**

This was first discovered as Bug 0005 (malformed type addresses), and the current client.py represents the *corrected* convention — but the backend is still never given a bootstrapped types document, so the corrected addresses still resolve to nothing.

---

### Intended Design vs. Actual Implementation

| Question | Answer | Source |
|----------|--------|--------|
| Are `1.0.2.x` hardcoded in C? | No — no constants, no special handling | `init.c`, `be.c`, `granf2.c` |
| What are `1.0.2.x`? | V-space addresses within a designated "types document" | `client.py:604` |
| What types were envisioned? | jump (2), quote (3), footnote (6), footnote.margin (6.2) | `client.py:605-608` |
| Does granfilade store type content? | No — never bootstrapped | `init.c:25-78` |
| What happens when type doc is missing? | Sporgl resolves to NULL; LINKTHREESPAN silently omitted | `sporgl.c:44`, `do2.c:122` |
| Where type content *would* live | As link atoms at `1.1.0.1.0.1.0.2.1`, `.0.2.2`, ... in granfilade | `granf2.c:170-175` |

In the intended design, the types document would be a bootstrapped "type registry" — a real document whose link atoms at specific V-positions define each type. The type endset would then be a sporgl that captures the I-address of a specific type-atom, enabling type-based link queries through `findlinksfromtothreesp` [`spanf1.c:92-98`] via the spanfilade. Instead, the convention exists only as client-side constants pointing to a document that was never created.

---

## Question 13 [gregory]

> Was link permanence — no delete operation exists for links in any storage layer — a deliberate design requirement of the Xanadu model, or an implementation simplification that happened to align with the "nothing is ever lost" philosophy?

### Gregory's Answer

## KB Synthesis

The KB evidence points strongly toward **deliberate design requirement**, not implementation convenience — though the two are tightly intertwined.

## The structural argument

Link permanence is not a free-standing policy; it is a derived consequence of two more fundamental choices:

1. **Content permanence**: I-addresses are append-only in the granfilade and write-only in the spanfilade [INV-IADDRESS-PERMANENT]. The KB explicitly states: "links — which are indexed by I-address — inherit this permanence" [INV-LINK-PERMANENCE]. Link permanence is derived from content permanence, not separately stipulated.

2. **The three-layer architecture**: [SS-THREE-LAYER-MODEL] shows a deliberate split: I-space (permanent), spanfilade (write-only/append-only per [INV-SPANF-WRITE-ONLY]), and POOM (mutable). CREATELINK writes to all three. `DELETEVSPAN(2.x)` removes only the POOM entry. This asymmetry is architecturally intentional — different layers have different mutability contracts.

## The "reverse orphan" tells you what was designed

The most telling evidence is the `DELETEVSPAN(2.x)` capability — the ability to remove a link from a document's POOM *without* deleting the link from I-space or spanfilade [EC-REVERSE-ORPHAN]. This provides the practical function users might want (making a link invisible in a document) while explicitly preserving the underlying permanent record. You don't accidentally design a two-tier system like this; it reflects a deliberate trade-off between user-facing mutability and underlying permanence.

## What isn't in the KB

The KB is derived from implementation findings, not design documents, so there are no direct Nelson quotes. However, [INV-LINK-PERMANENCE] frames this as "consistent with the broader Xanadu permanence model" — language that attributes it to design philosophy rather than omission.

The contrast with the disabled `levelpull` function [SS-ENFILADE-TREE] is instructive: that's an example of something that *should* exist but wasn't implemented. The KB contains no analogous language about DELETELINK being planned but missing. Instead, the FEBE protocol is noted to simply not have the opcode [INV-LINK-PERMANENCE].

## Summary

Link permanence is a structural consequence of content permanence (I-addresses never die) combined with a deliberately layered architecture that separates visible-state mutability (POOM) from identity-state permanence (I-space + spanfilade). The fact that `DELETEVSPAN(2.x)` exists as a "hide but don't destroy" operation strongly suggests the designers understood the tension and resolved it in favor of permanence — providing cosmetic removal rather than true deletion.

---

## Code Exploration

Now I have all the evidence I need. Let me compose the answer.

---

## Was Link Permanence Deliberate Design or Implementation Simplification?

**Answer: It was deliberate design — but the code reveals that "deliberate" means something specific here. It was not merely Nelson's philosophy imposed top-down; it was a structural consequence of architectural decisions that would have required substantial new machinery to undo.**

---

### 1. The Protocol Has No `DELETELINK` — By Construction, Not Omission

`backend/requests.h` defines every command the FEBE protocol supports. There are exactly 40 slots (`NREQUESTS = 40`, `xanadu.h:20`). The link-related slots are:

```c
/* backend/requests.h:33-40 */
#define FOLLOWLINK          18
#define CREATELINK          27
#define RETRIEVEENDSETS     28
#define FINDNUMOFLINKSFROMTOTHREE  29
#define FINDLINKSFROMTOTHREE       30
#define FINDNEXTNLINKSFROMTOTHREE  31
```

There is no `DELETELINK` constant, no gap number reserved for it, and no handler registered in the dispatch table (`backend/init.c:42-69`). The dispatch table fills its 40 slots by initializing everything to `nullfun` (which just calls `putrequestfailed`) and then selectively overwriting:

```c
/* backend/init.c:42-69 */
for (i = 0; i < NREQUESTS; ++i)
    requestfns[i] = nullfun;
...
requestfns[CREATELINK] = createlink;
requestfns[RETRIEVEENDSETS] = retrieveendsets;
/* ... no deletelink ... */
```

No slot is conspicuously unused in a way that suggests a planned-but-unimplemented delete. The 40-slot protocol is full, and none of the used slots is a link delete.

---

### 2. `createlink` Has No Structural Inverse

The FEBE-level handler at `backend/fns.c:100-112` calls `docreatelink`, which executes a five-step creation chain:

```c
/* backend/do1.c:208-220 */
return (
     createorglingranf (taskptr, granf, &hint, linkisaptr)   /* (1) allocate permanent I-address */
  && tumbler2spanset (taskptr, linkisaptr, &ispanset)
  && findnextlinkvsa (taskptr, docisaptr, &linkvsa)
  && docopy (taskptr, docisaptr, &linkvsa, ispanset)         /* (2) copy link ref into doc V-stream */
  && findorgl (taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
  && specset2sporglset (...)
  && setlinkvsas (...)
  && insertendsetsinorgl (...)                               /* (3) write endsets into link orgl */
  && insertendsetsinspanf (taskptr, spanf, linkisaptr, ...)  /* (4) append to spanfilade */
);
```

This creates link presence in **three independent structures**:

1. **Granfilade** — `createorglingranf` allocates a permanent I-address (a tumbler) in the address tree. There is no `deleteorglingranf`. The only traversal functions in `backend/granf1.c` are `findorgl`, `inserttextingranf`, `createorglingranf`, and `ispanset2vstuffset` — no delete, no deallocate.

2. **Document V-stream (POOM)** — `docopy` writes the link reference at a V-position < 1.0 (link subspace). This *can* be removed with `DELETEVSPAN` operating on the document — but that only removes the link's *presentation entry* in the document, not the link object itself. The semantic filter at `do1.c:377-411` explicitly distinguishes V < 1.0 (link metadata) from V ≥ 1.0 (transcludable text), treating them as categorically different.

3. **Spanfilade** — `insertendsetsinspanf` calls `insertspanf` (`backend/spanf1.c:15-53`), which calls `insertnd`. The spanfilade is an **append-only structure**: `insertnd` inserts new nodes but there is no `deletend` called from any link-related path. Spanfilade entries created by `CREATELINK` have no deletion pathway.

---

### 3. What `DELETEVSPAN` *Can* and *Cannot* Do

`DELETEVSPAN` exists (`requests.h:29`, handler at `fns.c:333-347`) and operates through `dodeletevspan` → `deletevspanpm` → `deletend` in `edit.c`. This deletes content from the **document's V-stream only** — it is a presentation-layer operation.

The comment at `do1.c:377-384` makes the layering explicit:

```c
/* Bug 009 SEMANTIC FIX: Filter vspanset to text subspace only (V >= 1.0).
 *
 * Link references at V-position 0.x are document metadata, not
 * transcludable content.
 */
```

So `DELETEVSPAN` operating on `V ≥ 1.0` removes text; operating on `V < 1.0` (link subspace) it could nominally remove the V-stream entry — but this does not touch the granfilade I-address, does not remove spanfilade entries, and leaves the link object fully accessible by its I-address. The link becomes *orphaned*, not deleted.

---

### 4. The Structural Argument: No Deletion Infrastructure Exists

A link delete operation would require all of the following, none of which exists:

- A **granfilade deallocation** path — freeing an I-address tumbler from the address tree. `granf2.c` only has `findisatoinsertmolecule`, `findisatoinsertnonmolecule`, and `createorglgr` (allocate). No free/reclaim.
- A **spanfilade deletion** path — removing LINKFROMSPAN/LINKTOSPAN/LINKTHREESPAN entries. `spanf1.c` has `insertspanf` and several find functions; no delete.
- A **link orgl teardown** — freeing the orgl node and its endset data from the document permutation matrix. `edit.c`'s `deletend` removes nodes from an enfilade by I-range, but it is only called from the `DELETEVSPAN` path and acts on V-space, not on the granfilade's link objects directly.

This is not the footprint of a feature that was planned and deferred. The deletion path would require an entirely new traversal strategy with inverse operations at every layer.

---

### 5. The `domakelink` Legacy Function

There are actually *two* link creation functions: the documented `docreatelink` (3-way: from/to/three, `do1.c:195`) and the older `domakelink` (2-way: from/to, `do1.c:169`). Neither has an inverse. The existence of two creation functions with no corresponding delete functions across both generations of the API reinforces that deletion was never part of the design iteration — it was absent from the beginning.

---

### 6. Conclusion

Link permanence is **both** a deliberate design requirement and a structural consequence of the architecture — these are not in tension. The code shows:

- **Design intention**: The 40-command FEBE protocol was laid out without allocating any slot to link deletion. This was not an oversight in a protocol designed to handle delete operations for content (`DELETEVSPAN:12`) but not links.

- **Architectural enforcement**: The three-layer storage model (granfilade I-address, POOM V-stream entry, spanfilade endpoint index) has append/insert operations at each layer but deletion only at the POOM V-stream layer. Even if you *wanted* to delete a link via `DELETEVSPAN` on the link subspace, you would succeed only in orphaning it — the I-address and spanfilade entries would remain.

- **The "nothing is ever lost" philosophy is not cosmetic**: It is load-bearing in the implementation. The enfilade structures are designed around the invariant that I-addresses, once allocated, remain valid. The `retrievecrums`/`retrieverestricted` traversal (`retrie.c`) assumes permanence; there is no "this I-address has been deleted" sentinel or tombstone mechanism anywhere in the codebase.

The design drew a categorical line: `DELETEVSPAN` is a **V-space operation** with no I-space side effects. `CREATELINK` has **permanent I-space effects**. This asymmetry is not accidental — it is the precise implementation of the Xanadu permanence axiom, applied specifically to the distinction between the mutable presentation layer and the immutable content/link layer.

---

## Question 14 [gregory]

> When an orphaned link (all endpoint content deleted from every V-stream) becomes discoverable again because its endpoint I-addresses reappear via transclusion into a new document, was this "resurrection" behavior an intended design property that users/applications were expected to rely on?

### Gregory's Answer

## KB Synthesis

Yes. This is intended behavior — a natural consequence of the foundational design principles, not an accident.

The resurrection property follows directly from three invariants that were deliberate design choices:

**1. I-addresses are permanent and never reused.**
[INV-IADDR-IMMUTABILITY, INV-NO-IADDR-REUSE] Once bytes are written to the permascroll, their addresses are fixed forever. Deleting content from a document's V-stream removes the POOM mapping but leaves the I-addresses intact in the granfilade. This was the design: "bytes never die, addresses never change."

**2. Transclusion shares I-addresses, not copies them.**
[ST-VCOPY] When any document transcludes content, it acquires the *same* I-addresses the original content held. There is no new allocation. This is precisely what makes transclusion semantically meaningful — shared identity, not shared bytes.

**3. The spanfilade (link index) is write-only.**
[INV-SPANF-WRITE-ONLY] There is no `deletespanf` function anywhere in the codebase. The link index grows monotonically. When a link is created, the I-address → link mapping is permanent. When those I-addresses reappear in any document via transclusion, the spanfilade already knows about the link. `find_links` does an I-address intersection against this permanent index, so it will find the link automatically. [INT-SPORGL-LINK-INDEX]

The `find_links` operation is defined as: return all links whose endpoint I-addresses have non-empty intersection with the search specset's I-addresses. [SS-FIND-LINKS] That definition contains no clause about "only if the content was never orphaned." It just asks: do these I-addresses appear? If a transclusion puts them somewhere, the answer is yes.

[INV-LINK-GLOBAL-VISIBILITY] documents that this global discoverability property "is not a new mechanism but an emergent invariant of the content-identity-based link model." [INT-LINK-TRANSCLUSION] formalizes it explicitly: `vcopy(content, src, dst) ⟹ ∀L :: I-addresses(L.source) ∩ I-addresses(content) ≠ ∅ ⟹ findable(L, dst)`.

**The "resurrection" scenario:**
If link L was created on content with I-addresses α₁..α₅, and all documents delete that content making L orphaned [EC-ORPHANED-LINK], L's link orgl still exists at its permanent I-address [INV-LINK-PERMANENCE] and the spanfilade still maps α₁..α₅ → L. When any document subsequently transcludes content from a source that has those I-addresses — even content that was previously deleted from other documents but persists in the granfilade — L becomes discoverable again. The system makes no distinction between "original" and "resurrected" discoverability.

**The one open question:**
[EC-ORPHANED-LINK, Finding 0005] notes as an open question "whether there should be a mechanism to find orphaned links" *directly* (bypassing the content-identity search path). That's a different capability from resurrection. Resurrection via transclusion was clearly intentional. Whether to provide a direct "find all orphaned links" query was less resolved.

The whole point of building the permanence architecture was that links follow content identity through any transformation — transclusion, versioning, or reappearance after deletion. Applications could rely on this.

---

## Code Exploration

---

## Link Resurrection via Transclusion: Code Analysis

### The Behavior in Question

When all V-stream appearances of a link endpoint's I-addresses are deleted, `find_links` returns nothing for that endpoint — the link is "orphaned." If those same I-addresses later reappear in any document via transclusion (COPY), the link becomes discoverable again. This is the resurrection behavior.

The code confirms this happens. Whether it was *intended* and whether users *were expected to rely on it* requires tracing the full architecture.

---

### 1. Link Endpoints Are Stored as Permanent I-Addresses

The `typesporgl` structure in `xanadu.h:115–121` defines link endpoint storage:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid itemid;
    tumbler sporglorigin;        /* span origin in I-address space */
    tumbler sporglwidth;         /* span width in I-address space */
    typeisa sporgladdress;       /* HOME DOCUMENT I-address */
} typesporgl;
```

All three fields are tumblers representing I-addresses. V-addresses are never stored in the link record itself — they are a conversion layer only. `orglinks.c:389–422` (functions `vspanset2ispanset`, `ispan2vspanset`, `permute`) shows that V↔I conversion is a query-time operation, not a storage operation.

When a link is created, `do1.c:195–221` (`docreatelink`) calls `specset2sporglset` to convert the caller's V-specsets into I-address sporgls, then stores those I-addresses permanently via `insertendsetsinorgl` and `insertendsetsinspanf`.

---

### 2. Deletion Is V-Space Only — I-Space Is Never Touched

`do1.c:158–167` (`dodeletevspan`):

```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
  typeorgl docorgl;
  bool findorgl(), deletevspanpm();

  return (
     findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
  && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr)
  /*&& TRUE*/ /* ht stuff */ );
}
```

`orglinks.c:145–152` (`deletevspanpm`):

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

`deletend` is called with dimension `V` [orglinks.c:149]. This removes the V→I crum from the document's POOM (in granf). The I-addresses in the granfilade are immutable — the granfilade has no delete operation. The bytes still exist. The I-addresses are just no longer mapped from any V-position in that document.

Critically: `deletevspanpm` makes **no call to remove spanfilade entries** [Finding 0057]. No `deletespanf` function exists anywhere in `spanf1.c` or `spanf2.c`. The spanfilade is structurally write-only.

---

### 3. Transclusion (COPY) Reuses Existing I-Addresses — Not Fresh Ones

`orglinks.c:100–113` (`insertpm`), called by `docopy`:

```c
for (; sporglset; sporglset = (typesporglset) sporglset->xxxxsporgl.next) {
    unpacksporgl (sporglset, &lstream, &lwidth, &linfo);
    movetumbler (&lstream, &crumorigin.dsas[I]);   /* I-address: REUSED, not allocated */
    movetumbler (&lwidth,  &crumwidth.dsas[I]);
    movetumbler (vsaptr,   &crumorigin.dsas[V]);   /* V-address: new position */
    ...
    insertnd (taskptr, (typecuc*)orgl, &crumorigin, &crumwidth, &linfo, V);
}
```

`lstream` and `lwidth` are the **existing** I-addresses from the source. They are placed directly into the new crum without any new allocation. The V-position is new (`vsaptr`), but the identity is preserved.

This contrasts sharply with `doinsert` [do1.c:87–123], which calls `inserttextingranf` to allocate *fresh* I-addresses from the granfilade. Re-typing deleted content creates entirely new I-addresses that have no relationship to the originals [Finding 0064].

---

### 4. `find_links` Queries by I-Address

`do2.c:14–46` (`specset2ispanset`) is the gateway: it converts a caller's V-specset (document + V-span) into an I-spanset by looking up the POOM enfilade (`vspanset2ispanset`, `orglinks.c:389–422`). If the V-span currently maps to certain I-addresses, those I-addresses become the search key.

`spanf1.c:56–103` (`findlinksfromtothreesp`) uses those I-addresses to query the spanfilade. `sporgl.c:239–269` (`sporglset2linksetinrange`) calls `retrieverestricted` on the spanfilade indexed by the SPANRANGE (I-address) dimension and returns any link whose endpoint overlaps.

**The implication**: when transcluded content places I-addresses back into some document's POOM, a caller querying that document's V-span will convert to those I-addresses and find any link whose endpoint contains them. The link record has not changed — its stored I-addresses are the same ones that were "gone" and are now "back."

This is empirically confirmed by Finding 0029, test `search_after_vcopy_source_deleted`:

```
Original: "linked" → create link → vcopy to Copy
Delete "linked" from Original
find_links(Original) → []
find_links(Copy)     → [link_id]  ← Still found via shared I-addresses
```

---

### 5. No Orphan Detection, No Garbage Collection

There is no code anywhere in the backend that:
- Checks whether a link's endpoint I-addresses are currently reachable in any V-stream
- Invalidates or removes links when their endpoint content disappears
- Maintains a reference count of "how many V-streams reference this I-address"

`do2.c:110–113` (`acceptablevsa`), called during COPY to validate insertion points:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
  return (TRUE);
}
```

This is a stub. Validation at the insertion layer is intentionally absent.

`dofollowlink` [do1.c:223–232] retrieves stored I-addresses and converts them to V-addresses via `linksporglset2specset`. It does not check whether the I-addresses currently exist in any V-stream before returning. The conversion may yield an empty result if no document maps those I-addresses to V-positions, but no error is raised.

---

### 6. Was Resurrection Intentional?

The code points to a clear architectural answer, though with one important qualification.

**The architecture makes resurrection structurally inevitable and precise.** The entire I-space/V-space separation exists to give content permanent identity independent of its current visible location. Links store I-addresses by design — there was no technical obstacle to storing V-addresses instead, but that choice was never made. The spanfilade being write-only, with no `deletespanf`, means the link-to-I-address index grows monotonically and never forgets.

Most tellingly: the behavior is *precise* in a way accidental features are not. **Only transclusion (COPY) resurrects links; re-insertion (INSERT) does not** [Finding 0064]. INSERT always allocates fresh I-addresses from the granfilade. Re-typing deleted text looks identical in V-space but creates a new I-space identity that has no relationship to any existing link. The resurrection works exclusively through the identity-preserving path.

If resurrection were an accident, you would not expect this precision. The system consistently distinguishes "same content" (same I-addresses, via COPY) from "new content that happens to look the same" (new I-addresses, via INSERT). Links track content, not appearance.

**`finddocscontainingsp`** [spanf1.c:151–188] provides further evidence: this function exists to enumerate all documents that contain a given I-span — the exact capability an application would need to discover whether orphaned link endpoints have "reappeared" somewhere. Its presence implies the designers anticipated this kind of traversal query.

**The qualification**: whether users/applications were explicitly *told to rely on this* is less certain from the code alone. Several implementation details suggest the system was incomplete at the time the code was preserved:
- `acceptablevsa` is a stub (`return (TRUE)` with no validation)
- `dodeletevspan` has `/*&& TRUE*/ /* ht stuff */` — a commented-out placeholder for "ht" (hypertext?) operations that were never implemented
- Finding 0024 documents that `follow_link(type_end)` returns empty when both endpoints are deleted, which appears to be a bug (the type endpoint references the bootstrap document, which was not deleted)
- The spanfilade's lack of cleanup is structurally consistent with the permascroll philosophy but is also structurally consistent with an incomplete implementation [Finding 0057]

---

### Conclusion

**The resurrection behavior is an architecturally intentional consequence of the Xanadu identity model, not a side effect.**

Links are bound to permanent content identity (I-addresses), not to current location in any V-stream. Deletion removes the V→I mapping but leaves the I-addresses, the link record, and the spanfilade index intact. Transclusion — by sharing I-addresses rather than creating new ones — makes those addresses reachable again through new V-contexts. The link's spanfilade entries, never removed, become active again when a query V-specset resolves to those I-addresses.

The precision of the behavior (COPY resurrects; INSERT does not) cannot be accidental. The existence of `finddocscontainingsp` as a first-class query implies the designers modeled the multi-document I-address graph as navigable.

Whether the intended *user contract* was that applications would be built to exploit this — e.g., "trancslude content from a backup document to revive its link network" — is a product design question the code cannot fully answer. What the code does establish is that the designers built a system where content identity is permanent, link semantics are defined over content identity, and no mechanism was ever added to short-circuit the revival pathway. That is an affirmative architectural choice, not an oversight.

**Key code citations:**
- Link endpoint storage as I-addresses: `xanadu.h:115–121` (`typesporgl`)
- V-only deletion, no I-space effect: `orglinks.c:149` (`deletend(..., V)`)
- Transclusion reuses I-addresses: `orglinks.c:105–109` (`movetumbler(&lstream, &crumorigin.dsas[I])`)
- Spanfilade write-only, no cleanup: `spanf1.c` (no `deletespanf` exists)
- Stub validation: `do2.c:110–113` (`acceptablevsa` returns TRUE)
- Multi-document query capability: `spanf1.c:151–188` (`finddocscontainingsp`)
- INSERT creates fresh I-addresses (no resurrection): `do1.c:87–123` (`inserttextingranf`)

---

## Question 15 [gregory]

> Can a single link endset legitimately reference content from multiple different documents (e.g., source endset contains I-spans from doc A and doc B), and if so, what is the intended semantic — does such a link assert a relationship across a composite selection?

### Gregory's Answer

## KB Synthesis

Yes, a single link endset can legitimately reference content from multiple different documents. This is a direct, automatic consequence of transclusion composing content from multiple sources.

**The mechanism** [SS-LINK-ENDPOINT, Finding 0037]:

When `domakelink` receives a V-span covering content transcluded from multiple sources, `vspanset2sporglset` converts the span to I-spans by walking the POOM. Because transcluded content from different documents occupies non-contiguous I-address regions (from different permascroll allocations), the conversion produces one sporgl per contiguous I-address region. Each sporgl carries its own `sporglorigin`, `sporglwidth`, and `sporgladdress` (source document ISA). The front end does not need to pre-split — the decomposition is automatic.

**Concrete example** [ST-LINK-CREATE, Finding 0037]:

```
Document C contains "AABB" at V 1.1..1.4 where:
  "AA" was transcluded from document A (I-addresses from A's permascroll)
  "BB" was transcluded from document B (I-addresses from B's permascroll)

create_link(source = V-span 1.1 width 0.4 in doc C, ...)

Input:  1 V-span covering "AABB"
Output: 2 sporgls in source endset:
  sporgl₁: origin = iaddr(A,"AA"), width = 0.2, doc = C
  sporgl₂: origin = iaddr(B,"BB"), width = 0.2, doc = C
```

**The semantic** [SS-SPORGL, Finding 0013; SS-LINK-ENDPOINT, Finding 0004]:

The link treats the entire V-span selection as a single composite endpoint — it asserts a relationship against the union of all content identities in that selection, across all their provenance origins. The `sporgladdress` field records which document each piece came from, but the link binds to the I-addresses themselves, not the document positions. This is consistent with the broader model: link endpoints are content identity references, not positional references.

**Partial survival** [EC-LINK-PARTIAL-SURVIVAL]:

Because each sporgl in the endset independently tracks its content, the multi-document structure has a concrete behavioral consequence: if document A's content is deleted, the endset retains the sporgl for B's content. The link partially survives — `follow_link` returns only the surviving B-derived portion [INV-LINK-CONTENT-TRACKING].

**Summary**: A multi-document endset is the normal outcome whenever a link is placed on composite (transcluded) content. The semantic is that the link binds to all constituent content identities as a single endpoint, spanning their multiple origins. There is no restriction or special treatment — the system handles it transparently via the sporgl mechanism.

---

## Code Exploration

Now I have everything I need to give a complete, code-grounded answer.

---

## Can a Single Link Endset Reference Content from Multiple Documents?

**Yes — architecturally, yes. Operationally, yes with a caveat at retrieval.**

Here is the full trace.

---

### 1. The Data Model

Each link has three endsets: `from`, `to`, and `three`. Internally, an endset is stored as a linked list of `typesporgl` structs. The critical field is `sporgladdress`:

```c
// xanadu.h — typesporgl
typedef struct structsporgl {
    struct structsporgl *next;
    typeitemid      itemid;
    tumbler sporglorigin;   // I-span start (position in permascroll)
    tumbler sporglwidth;    // I-span width
    typeisa sporgladdress;  // The document this I-span belongs to
} typesporgl;
```

`sporgladdress` is a per-sporgl document ISA. It is not a property of the endset as a whole — it is per-element. The architecture explicitly provides a per-span document reference. This is the foundation for multi-document endsets.

---

### 2. Creation Path — No Cross-Document Constraint

`docreatelink` [do1.c:195-221] calls `specset2sporglset` for each endset:

```c
// do1.c:214-216
&& specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
&& specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
&& specset2sporglset (taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
```

`specset2sporglset` [sporgl.c:14-33] iterates through the entire input specset, which is a linked list of items. Each `VSPECID` item has its own `docisa` field:

```c
// sporgl.c:19-28
for (; specset; specset = (typespecset)((typeitemheader*)specset)->next) {
    if (((typeitemheader *)specset)->itemid == ISPANID) {
        *sporglsetptr = (typesporglset)specset;
        ...
    } else if (((typeitemheader *)specset)->itemid == VSPECID) {
        if (!(sporglsetptr = vspanset2sporglset (taskptr,
            &((typevspec *)specset)->docisa,   // ← each vspec has its OWN docisa
            ((typevspec *)specset)->vspanset,
            sporglsetptr, type))) {
            return (FALSE);
        }
    }
}
```

A caller can pass a specset with multiple `VSPECID` items, each with a different `docisa`. There is **no check** anywhere in `specset2sporglset`, `vspanset2sporglset`, `insertendsetsinorgl` [do2.c:130-149], or `insertpm` [orglinks.c:75-134] that enforces same-document membership within an endset.

`vspanset2sporglset` [sporgl.c:35-65] faithfully records the source document in every sporgl it creates:

```c
// sporgl.c:53
movetumbler (docisa, &sporglset->sporgladdress);   // source doc stored per-sporgl
```

So **at creation time, a multi-document endset is accepted without complaint.**

---

### 3. Storage — Correct

`insertpm` [orglinks.c:100-131] iterates the sporglset and inserts each item into the link's orgl (POOM enfilade). It calls `unpacksporgl` which reads `sporgladdress` into `linfo.homedoc`:

```c
// sporgl.c:187
movetumbler (&((typesporgl *)sporglptr)->sporgladdress, &infoptr->homedoc);
```

`insertnd` then stores `linfo` in the crum's bottom-level info. Each crum in the link's enfilade carries its source document address. A multi-document endset produces correctly-labeled crums.

`insertspanf` [spanf1.c:15-54] — which indexes the endset into the spanfilade for link-lookup — also correctly stores per-sporgl addresses:

```c
// spanf1.c:33
movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);  // correct
```

**Storage is faithful. Multi-document endsets are stored correctly at the crum level.**

---

### 4. Retrieval — Partially Broken for Multi-Document Endsets

`dofollowlink` [do1.c:223-232]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr,
           &((typesporgl *)sporglset)->sporgladdress,   // ← FIRST sporgl's address only
           sporglset, specsetptr, NOBERTREQUIRED));
}
```

`link2sporglset` [sporgl.c:67-95] retrieves all sporgls from the endset via `contextintosporgl`, which correctly restores each sporgl's own `sporgladdress` from the crum's `homedoc`. So the sporglset coming out of `link2sporglset` is correct.

Then `linksporglset2specset` [sporgl.c:97-123] passes control to `linksporglset2vspec` [sporgl.c:127-137]:

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, typesporglset *sporglsetptr,
                        typevspec *specptr, int type)
{
    specptr->itemid = VSPECID;
    specptr->next = NULL;
    movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);  // LINE 134
    specptr->vspanset = NULL;
    sporglset2vspanset (taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

**Line 134 is the smoking gun.** The comment `/*&sporglset->sporgladdress*/` preserves the original intent: use each sporgl's own document address. The working code substitutes `homedoc` — the first sporgl's address passed in from `dofollowlink` — for all sporgls.

`sporglset2vspanset` [sporgl.c:141-176] compounds this: it calls `findorgl` with `homedoc` [line 152], and its inner loop [line 163] terminates as soon as a sporgl with a different `sporgladdress` is encountered:

```c
// sporgl.c:163
|| !tumblereq (&((typesporgl *)sporglptr)->sporgladdress,
               &((typesporgl *)(*sporglsetptr))->sporgladdress))
    return(0);   // stops at first sporgl from a different document
```

**Effect:** When following a link whose endset spans documents A and B, only the portion from document A (whichever happened to be first in the sporglset) is returned. The content from document B is silently dropped.

`retrieveendsetsfromspanf` [spanf1.c:190-235] — the alternative retrieval path — exhibits the same defect:

```c
// spanf1.c:224
&& linksporglset2specset (taskptr, &((typevspec *)specset)->docisa, fromsporglset, fromsetptr, NOBERTREQUIRED)
```

Here `homedoc` is the link's own document ISA rather than the first sporgl's address — equally wrong for multi-document endsets.

---

### 5. Intended Semantic

The architecture answers this directly through the data model. The `sporgladdress` field exists precisely to make endsets document-independent. An endset is not "content from document X" — it is "these I-spans, which happen to live in these documents." The I-span (permascroll address) is the primary identity; the document is secondary metadata needed to translate back to V-space.

The intended semantic of a multi-document endset is: **the link asserts a relationship across a composite selection drawn from multiple documents simultaneously.** The endpoint is not "some text in doc A" or "some text in doc B" — it is "this composite span of docuverse material, which happens to be transcluded into multiple documents." This is the core Xanadu model: links and transclusion operate on permanent, document-neutral I-addresses.

A link from {doc A para 1, doc B para 3} to {doc C section 2} would mean: the relationship holds between the combined selection of that paragraph and that passage on one side, and the section on the other. Useful for, e.g., linking two separately-sourced quotes that together support a claim.

---

### 6. Summary

| Layer | Multi-doc endset behavior |
|-------|--------------------------|
| API input | Accepted without restriction |
| `specset2sporglset` [sporgl.c:14] | Correctly converts each V-spec with its own `docisa` |
| `vspanset2sporglset` [sporgl.c:53] | Correctly stores source doc in each `sporgladdress` |
| `insertpm` / `insertnd` | Correctly stores `homedoc` per-crum |
| `insertspanf` [spanf1.c:33] | Correctly indexes by per-sporgl source doc |
| `link2sporglset` [sporgl.c:86] | Correctly reconstructs per-sporgl addresses via `contextintosporgl` |
| `linksporglset2vspec` [sporgl.c:134] | **Bug: uses first doc's address for all sporgls** |
| `sporglset2vspanset` [sporgl.c:163] | **Bug: stops at first cross-document sporgl** |

**Conclusion:** Multi-document endsets are legitimate by design — the `sporgladdress` field is the architectural provision for exactly this case. The intended semantic is a cross-docuverse composite selection: one link endpoint covers material from multiple documents as a unified whole. The implementation correctly stores such endsets, but the retrieval path in `linksporglset2vspec` [sporgl.c:134] and `sporglset2vspanset` [sporgl.c:152, 163] is broken — the commented-out `&sporglset->sporgladdress` code was replaced with a single `homedoc` reference, causing only the first document's content to be returned when following such a link.

---

## Question 16 [gregory]

> The `TRUE||!homeset` override in `sporglset2linkset` makes find_links search globally rather than scoped to a home document set — was global link discovery the original design intent, with the home-document filtering being dead code, or was scoped discovery intended but never completed?

### Gregory's Answer

## KB Synthesis

The `TRUE||!homeset` override is almost certainly a debugging artifact from an incomplete feature — scoped discovery was intended but never completed.

The evidence from the KB makes this clear on multiple levels:

**The code structure signals a bug, not design.** `if (TRUE||!homeset)` is a classic C debugging pattern for disabling a condition without deleting it. The semantically coherent original was `if (!homeset)`: "if no home set is provided, substitute the default permissive range." Prepending `TRUE||` disables the real condition while preserving it intact for later re-enabling. The hardcoded width of 100 was the fallback default, not an intentional "search everything" constant [EC-FIND-LINKS-GLOBAL].

**The caller faithfully passes the parameter through.** `findlinksfromtothreesp()` in `spanf1.c:56-103` accepts and passes `orglrange` to `sporglset2linkset`. If global search were the design intent, there would be no reason for the orgl range parameter to exist at the call site at all [PRE-FIND-LINKS / Finding 0069].

**Global content-identity-based discovery was the *primary* design — the orgl filter was a *secondary* scoping mechanism.** The entire link architecture is built around I-address intersection as the discovery mechanism [SS-LINK-ENDPOINT], [INV-LINK-GLOBAL-VISIBILITY], [INT-LINK-TRANSCLUSION]. The home document is for link *allocation* (where the link orgl lives) [SS-LINK-HOME-DOCUMENT], not for restricting discovery. The orgl-range filter in find_links was an additional opt-in restriction on top of content-identity search — it let you ask "among all links discoverable by content identity, return only those allocated under this document." That's a useful query but orthogonal to the core design.

**The `homedocids` filter being broken is consistent with known incompleteness.** The broken `homedocids` filter [EC-HOMEDOCIDS-FILTER-BROKEN] and the `TRUE||` override are related symptoms: orgl-range scoping was specified in the interface but the implementation was never finished or was disabled mid-development.

Bottom line: global content-identity-based discovery is the authentic design intent — that's what the whole I-address architecture is for. The orgl range filter was a planned extension to allow scoped queries, but it got disabled (`TRUE||`) at some point and was never re-enabled. The current global behavior is a consequence of that incomplete implementation, not the original vision.

---

## Code Exploration

Now I have all the evidence needed. Here is the complete answer:

---

## `TRUE||!homeset` in `sporglset2linkset`: Dead Code or Incomplete Feature?

**The answer is definitively: scoped link discovery was the original design intent. The `TRUE||` override is an in-progress development hack that was never removed, rendering an implemented protocol parameter permanently inert.**

---

### The Override

`sporgl.c:222–237`:
```c
int sporglset2linkset(typetask *taskptr, typecuc *spanfptr, typesporglset sporglset,
    typelinkset *linksetptr, typeispan *homeset, INT spantype)
{
  typeispan nullhomeset;

    *linksetptr = NULL;
    if (TRUE||!homeset) {                          // always true
        tumblerclear (&nullhomeset.stream);
        tumblerclear (&nullhomeset.width);
        nullhomeset.width.mantissa[0] = 100;       // hardcoded range
        nullhomeset.next = NULL;
        homeset = &nullhomeset;                    // discard caller's value
    }
    for (; homeset; homeset = homeset->next) {
        sporglset2linksetinrange (taskptr, spanfptr, sporglset, linksetptr, homeset, spantype);
    }
}
```

The condition `TRUE||!homeset` is a C idiom meaning *"I've decided to always take this branch for now."* It silently discards whatever homeset the caller computed and substitutes a hardcoded one. The else branch — use the caller's scope — is permanently dead.

---

### Evidence That Scoped Discovery Was The Design Intent

**1. The protocol actually reads and decodes a homeset from the client.**

`get1.c:121`:
```c
prompt (taskptr, "home documents\n");
if (!getspanset (taskptr, homesetptr, ISPANID))
    return (FALSE);
```

`get1fe.c:108–112` (FEBE binary protocol version):
```c
return (
   getspecset (taskptr, fromvspecsetptr)
&& getspecset (taskptr, tovspecsetptr)
&& getspecset (taskptr, threevspecsetptr)
&& getspanset (taskptr, homesetptr, ISPANID) && kluge());
```

This is not vestigial naming — it is actual protocol wire parsing. The client sends a homeset; the server reads and decodes it. Building a full round-trip for a parameter you intend to unconditionally ignore would be design nonsense.

**2. The prompt text "home documents\n" (`get1.c:121`) is user-facing design intent.**

It names the semantic concept explicitly: the user submits a set of home documents to scope the search.

**3. Three FEBE handlers exist with three different behaviors, showing an edit in-flight.**

`fns.c:196–201` — `findlinksfromtothree`:
```c
getfindlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
    (typeispan*)NULL/*homeset*/, &linkset))
```
Homeset is fetched then **explicitly NULLed**, with a comment preserving the original expression. The developer changed this one.

`fns.c:211–213` — `findnumoflinksfromtothree`:
```c
getfindnumoflinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset, &homeset)
&& dofindnumoflinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
    homeset, &numberoflinks))
```
Passes homeset directly — **not updated**.

`fns.c:228–230` — `findnextnlinksfromtothree`:
```c
getfindnextnlinksfromtothree (taskptr, &fromvspecset, &tovspecset, &threevspecset,
    &homeset, &lastlink, &n)
&& dofindnextnlinksfromtothree (taskptr, fromvspecset, tovspecset, threevspecset,
    homeset, &lastlink, &nextlinkset, &n))
```
Also passes homeset directly — **not updated**.

If the design was "always global," all three handlers would have been updated. They weren't. The `TRUE||` in `sporglset2linkset` makes the inconsistency moot, but it exposes the incomplete edit clearly.

**4. `kluge()` in `get1fe.c:198–202` is chained after homeset parsing and does nothing.**

```c
bool kluge(void)
{
/*  fclose (reallog);
    reallog = fopen("xueditlog","a");
*/  return (TRUE);
}
```

This function — explicitly named `kluge` — was inserted after homeset parsing in the FEBE path. Its body is entirely commented out; it always returns TRUE. It was a placeholder for work that was never completed.

**5. `TRUE||` is the canonical C hack for "always do this branch for now."**

In finished code, you either delete the else branch or restructure the condition. `TRUE||expr` preserves the else branch (making future restoration obvious) while ensuring it never executes. It reads as a temporary bypass left in place. Its companion — `/*TRUE||*/` in `insertnd.c:70` — shows the same pattern was used elsewhere and later removed, confirming this is a known development practice in this codebase.

---

### What the Hardcoded Substitute Actually Does

When the override fires, `nullhomeset` has:
- `stream = 0` (tumbler zero — no offset)
- `width.mantissa[0] = 100`

This is **not** the entire address space — it is a fixed range of 100 tumbler units from origin. In `sporglset2linksetinrange:257–259`:

```c
prefixtumbler(&orglrange->stream, spantype, &range.stream);
prefixtumbler (&orglrange->width, 0, &range.width);
context = retrieverestricted (spanfptr, (typespan*)sporglset, SPANRANGE, &range, ORGLRANGE, (typeisa*)infoptr);
```

The ORGL search range becomes `[spantype, spantype + 100)` in the organizational dimension. Since link endpoint type slots are small integers (LINKFROMSPAN, LINKTOSPAN, LINKTHREESPAN), a width of 100 is broad enough to cover all of them. It works as a "good enough" substitute for a real home-document bound — which is exactly the behavior expected from a development workaround.

---

### Conclusion

The `TRUE||!homeset` override is **unfinished implementation, not intentional design**. The scoped link discovery feature was:

1. **Designed** — with a named concept ("home documents") and protocol field
2. **Plumbed** — the parameter travels the full call chain from wire parsing through four function layers to `sporglset2linkset`
3. **Partially implemented** — the `sporglset2linksetinrange` function accepts and uses `orglrange` when non-NULL (`sporgl.c:256–262`); the downstream logic exists
4. **Bypassed** — via `TRUE||!homeset`, which was inserted when the scoping logic was not ready or known to be broken, substituting a hardcoded approximation
5. **Never completed** — the edit to NULL out homeset in `fns.c` was done for one of three handlers; the `kluge()` placeholder was never filled in; the `TRUE||` was never removed

The home-document filtering parameter is not dead code in the sense of having never meant anything — it meant exactly what its name says, was part of a real design, and was built into the protocol. What is dead is the execution path that would have honored it.

---

## Question 17 [gregory]

> CREATENEWVERSION copies text but not links, yet links remain discoverable from the version through shared I-addresses — was this asymmetry (links follow content identity rather than document membership) a core design principle, and were there discussions about whether versions should carry their own link copies?

### Gregory's Answer

## KB Synthesis

Yes, this asymmetry is a direct expression of a core design principle, though the *mechanism* that produces it has a pragmatic quality that suggests it was more emergent than explicitly debated.

## What the code shows

CREATENEWVERSION uses `retrievedocumentpartofvspanpm` to obtain the source document's extent before copying. That function reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the root crum — which points to position 1, the text subspace start. The link subspace (internally at 2.x) is structurally outside this vspan. The source code itself calls this mechanism "a kluge." [ST-VERSION-CREATE, Finding 0043/0046]

So the text-only copy is not a principled exclusion of links — it's what falls out of using the existing V-span retrieval path, which was designed around text extent.

## Why links still work from versions

The more interesting part is *why* this doesn't break anything. `find_links` doesn't read the document's POOM at all — it converts the query V-span to I-addresses, then searches the spanfilade index. Since the version shares permascroll I-addresses with the source for all copied text, the same spanfilade entries match. Links follow the content, not the document. [INT-LINK-VERSION, Finding 0046; SS-THREE-LAYER-MODEL]

This is the design principle: **links are indexed by content identity, not document membership**. A link is a relationship between I-addresses. Any document that contains those I-addresses — whether by original insertion, transclusion, or versioning — participates in that relationship automatically. [INV-LINK-GLOBAL-VISIBILITY; INT-LINK-TRANSCLUSION]

## The three-layer model makes this coherent

The three-layer architecture (I-space orgl, spanfilade DOCISPAN entries, POOM V-stream) separates "link existence" from "link containment in a document's POOM" from "link discoverability via content identity." [SS-THREE-LAYER-MODEL] These are genuinely independent predicates. CREATENEWVERSION not copying link POOM entries just means the version doesn't "list" the links in its vspanset — but the links remain fully alive and discoverable because the spanfilade is append-only and the I-addresses are permanent. [INV-SPANF-WRITE-ONLY; INV-LINK-PERMANENCE]

## On whether there were design discussions

The KB doesn't preserve any explicit design discussions about this choice. What I can tell you from the code is that the text-only copy mechanism reads as pragmatic — it reuses an existing vspan retrieval path rather than implementing a purpose-built "copy everything including links" path. The fact that link discovery still works correctly is a *consequence* of the identity architecture, not something that required special engineering in VERSION.

If we had explicitly designed a "version should carry its own link copies" model, we would have needed to copy the link POOM entries and re-register them in the spanfilade under the version's I-addresses — which would have been new I-addresses, breaking the identity chain back to the original. That would violate the core invariant. [INV-TRANSITIVE-IDENTITY] So the current behavior isn't just how it happened to be implemented — it's the only consistent behavior given the rest of the architecture.

The deeper principle: links belong to the *content web*, not to individual documents. Versions are just another way for documents to participate in that web by sharing content identity.

---

## Code Exploration

I now have all the source evidence needed. Here is the full answer.

---

## CREATENEWVERSION Asymmetry: Text Copies, Links Follow Identity

### What the Code Actually Does

**`docreatenewversion` [do1.c:260-299]** executes this sequence:

```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)  // 1. Get source vspan
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)  // 2. Copy into new doc
```

**Step 1: `doretrievedocvspanfoo` [do1.c:301-309]** calls `retrievedocumentpartofvspanpm` [orglinks.c:155-162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

This reads the root crum's V-displacement (`cdsp.dsas[V]`) and V-width (`cwid.dsas[V]`) directly. The document's text content lives at V-positions starting at `1.x` — that is what the root crum's displacement tracks. The link subspace lives at `0.x` V-positions and is *not reachable* by this single-span retrieval: it sits below position 1 in a different subtree of the POOM.

**Step 2: `docopyinternal` [do1.c:66-82]** does two things:

```c
if (!insertpm (taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;
if (!insertspanf (taskptr, spanf, docisaptr, ispanset, DOCISPAN)) return FALSE;
```

- `insertpm` writes V→I mapping entries into the new document's POOM — the version now has its own V-addresses mapping to the *same* I-addresses as the original's text content.
- `insertspanf` registers the new document ISA against those I-addresses in the spanf, with type `DOCISPAN = 4` [xanadu.h:39].

Link subspace entries (`0.x` V-positions) are **never touched**. They are not retrieved by `doretrievedocvspanfoo`, not passed through `docopyinternal`, and not registered in the spanf.

---

### Why Links Remain Discoverable

The spanf (span enfilade) is a global I-address index with four distinct "lanes" in its ORGLRANGE dimension [xanadu.h:36-39]:

```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

When a link is created via `docreatelink` [do1.c:195-221], `insertendsetsinspanf` registers the endpoints' I-addresses at `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`. This registration is purely by I-address — no document identity is encoded in the spanf key.

When `find_links` is called on a version, `findlinksfromtothreesp` [spanf1.c:56-103] executes:

1. `specset2sporglset` → `vspanset2sporglset` [sporgl.c:35-65]: translates V-positions to I-addresses by walking the version's POOM via `vspanset2ispanset` → `permute`.
2. `sporglset2linksetinrange` [sporgl.c:239-269]: queries the spanf with those I-addresses in the SPANRANGE dimension, retrieving entries in the ORGLRANGE dimension corresponding to link endpoint types (1/2/3).

The version's POOM maps *its* V-positions to the *same* I-addresses the original's text occupies. So the spanf lookup returns the same links regardless of which document's V-positions triggered it. Document identity is irrelevant to link discovery — only content identity (I-address) matters.

---

### The V-Address Subspace Architecture Is Explicit and Deliberate

The structural separation of text and link subspaces is encoded in the discriminator functions [orglinks.c:246-261]:

```c
bool istextcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
    return FALSE;
}

bool islinkcrum(typecorecrum *crumptr) {
    if(crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
    return FALSE;
}
```

`istextcrum`: a crum whose V-displacement has a zero second digit and single-story width — i.e., root-level content (V-position 1.0).  
`islinkcrum`: a crum displaced into `1.n` space where `n ≠ 0` — a link subspace entry.

`findvsatoappend` [orglinks.c:29-49] explicitly guards the boundary:

```c
tumblerincrement (&linkspacevstart, 0, 2, &linkspacevstart);   // linkspacevstart = 2.0
if (iszerolock(...) || (tumblercmp (&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement (vsaptr, 0, 1, vsaptr);   // no text: append at 1.1
    tumblerincrement (vsaptr, 1, 1, vsaptr);
}
```

This ensures text appends stay in the `1.x` range and never collide with link V-addresses. The architecture of the POOM is:

```
V-dimension layout:
  0.x  — unused / pre-text space
  1.x  — link subspace (link ISAs stored here as LINKATOM objects)
  ≥2.x — text subspace (content I-addresses)
```

*(Note: the comment in Finding 0043 labels these `0.x`=link and `1.x`=text, but the discriminator functions and `findvsatoappend` logic show the actual split is between root-level text displacement and sub-digit link displacement — the key point is that they occupy structurally distinct parts of the V-tree and are treated differently throughout the code.)*

---

### Evidence That the Asymmetry Was Explicitly Considered

The most direct code evidence of the design tension is in `sporgl.c:251`:

```c
if (FALSE/*trying to kluge links followable thru versions */&&
    ((typeitemheader *)sporglset)->itemid == SPORGLID) {
    infoptr = &linfo;
    movetumbler (&((typesporgl *)sporglset)->sporgladdress, &linfo.homedoc);
} else
    infoptr = NULL;
```

This is a **disabled kluge**. The `FALSE` short-circuits the branch. The comment — *"trying to kluge links followable thru versions"* — reveals that someone considered making link following version-aware: passing the source document's `sporgladdress` as a `homedoc` filter to `retrieverestricted`, which would have made the spanf query document-specific. That approach was abandoned. The null `infoptr` path (what actually runs) makes the lookup document-agnostic — I-addresses are queried globally, and every link indexed at those I-addresses is returned regardless of which document they were created from.

Additionally, `doretrievedocvspanfoo` [do1.c:302] carries the comment: *"this routine is a kluge not yet kluged."* The very name distinguishes it from `doretrievedocvspan` [do1.c:312-320], which is structurally identical code. The `foo` suffix suggests the text-only retrieval behavior was recognized as provisional — a workaround that happened to produce the right semantics (copy only text, not links) without being architecturally clean.

The `#ifdef UnDEFined` block in `orglinks.c:263-313` preserves an earlier `retrievevspansetpm` implementation that walked all crums recursively (`walkorglonvpm`), returning a list of all V-spans including link crums. This was disabled in favor of the current `is1story` test that separates text and link spans explicitly. That evolution shows the link/text discrimination was an active design refinement, not an initial assumption.

---

### Were There Discussions About Version-Owned Link Copies?

The code contains no trace of a function or mechanism for copying link subspace entries to a new document. To "copy links into a version" would require either:

1. **Creating new link orgls** — but each link has a unique ISA allocated from the granf; duplicating the orgl would create a new ISA, breaking the link identity that allows `follow_link` to return the original endpoints.
2. **Duplicating POOM link-subspace entries pointing to the same link orgls** — this would be structurally redundant: `find_links` doesn't consult a document's link subspace entries at all. It goes directly through the spanf's I-address index. A version's link subspace is never queried during link discovery.

The second alternative would have required a new code path in `docreatenewversion` and changes to `findlinksfromtothreesp` to also scan document link-subspace entries. No such path was ever written. The absence, combined with the disabled `FALSE/*trying to kluge links followable thru versions*/` in `sporgl.c:251`, suggests the I-address-only approach was the settled answer — and the other direction (document-local link ownership for versions) was tried conceptually and set aside.

---

### Summary

The asymmetry is structural and deliberate:

| Layer | What version gets | Mechanism |
|-------|-------------------|-----------|
| **POOM (granf)** | Text subspace only (1.x V-positions → same I-addresses as original) | `doretrievedocvspanfoo` reads only root crum displacement |
| **Link subspace (POOM)** | Nothing | `0.x` link entries not retrieved; no copy mechanism exists |
| **spanf (link index)** | Implicit access via shared I-addresses | V→I translation through version's POOM hits same I-addresses; spanf lookup is document-agnostic |

**Links follow content identity, not document membership.** This is not a side effect of the copy mechanics — it is the intended model, affirmed by the disabled `FALSE/*trying to kluge...*/` in `sporgl.c:251`, the explicit `istextcrum`/`islinkcrum` discriminators in `orglinks.c:246-261`, and the four-lane `LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`/`DOCISPAN` spanf architecture in `xanadu.h:36-39`.

The link-subspace entries in a document's POOM record which links are *housed in* that document (created from it, owned by it). That is separate from which links are *findable through* that document. Link discovery is purely I-address based. Versioning copies the I-address provenance (text) but not the ownership tokens (link subspace entries) — and the system was explicitly designed so that no one needs to copy the ownership tokens for discovery to work.

---

## Question 18 [gregory]

> Links are stored in the document's link subspace at `0.2.x` in the POOM — what is the significance of a link having a V-address within a specific document, given that links are discoverable globally via I-address overlap regardless of which document "owns" them?

### Gregory's Answer

## KB Synthesis

The significance is three-layered, and the layers serve distinct purposes:

## 1. The POOM entry makes a link part of the document's *visible content structure*

`retrieve_vspanset` and `retrieve_contents` operate through the POOM. A link at V-address `2.x` in the home document's POOM appears in the vspanset result and is returned by `retrieve_contents` as a link reference — it is structurally part of the document's content, not merely an annotation on it. Without the POOM entry, the document has no way to say "here are the links I contain" at the V-space level. [SS-THREE-LAYER-MODEL], [SS-VSPAN-VS-VSPANSET]

## 2. The home document establishes the link's permanent I-address namespace

Link I-addresses are allocated per-document under `docISA.2.x`. The home document at creation time determines where in the global granfilade the link orgl lives — permanently. This is separate from the POOM entry: the I-address is allocated whether or not the home doc's POOM retains the `2.x` mapping. [SS-ADDRESS-SPACE] Finding 0065, [SS-LINK-HOME-DOCUMENT]

## 3. The POOM entry is the only *mutable* layer of link membership

This is the architectural point: the three layers have different persistence properties:
- **I-space** (link orgl): append-only, permanent [INV-LINK-PERMANENCE]
- **Spanfilade**: write-only, permanent [INV-SPANF-WRITE-ONLY]
- **POOM (V-stream)**: mutable — the only layer that can be modified

`DELETEVSPAN(2.x)` removes the POOM entry while leaving the link fully intact and globally discoverable. The result is the "reverse orphan" state: `find_links` still finds the link (spanfilade intact), `follow_link` still works (I-space intact), but `retrieve_vspanset` no longer shows it and the document no longer "contains" it structurally. [SS-THREE-LAYER-MODEL], [EC-REVERSE-ORPHAN]

## The upshot

Global discoverability via I-address overlap is a property of the **spanfilade layer** — it has nothing to do with POOM membership. The home document's POOM entry serves as the document's *ownership record* and *presentation slot*: it determines which links a document can enumerate as its own, what appears in its vspanset, and what position in V-space the link occupies for pagination purposes.

In short: I-address overlap makes a link *findable from* a document; the POOM entry makes a link *contained by* a document. These are independent predicates that can diverge — a link created in document A is discoverable from document B via transclusion with no POOM entry in B, while a link can be removed from A's POOM (via DELETEVSPAN) and still be discoverable from A via the spanfilade. [FC-LINK-DELETE-ISOLATION], [INT-LINK-TRANSCLUSION]

---

## Code Exploration

Now I have everything I need. Let me write the full answer.

---

## The Significance of a Link's V-Address Within Its Owning Document

### What "owning" means structurally

When `docreatelink` runs, it does three separate things to establish a link:

**1. Allocates the link's ISA tumbler in the document's namespace** [do1.c:207–209]:
```c
makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
createorglingranf(taskptr, granf, &hint, linkisaptr)
```
The `makehint` call records `docisaptr` as the parent context for ISA allocation. The resulting `linkisaptr` tumbler is permanently scoped to the creating document's address space. This is not a runtime relationship — it's baked into the link's identity.

**2. Inserts the link's ISA into the document's POOM** [do1.c:211–212]:
```c
findnextlinkvsa(taskptr, docisaptr, &linkvsa)
docopy(taskptr, docisaptr, &linkvsa, ispanset)
```
`findnextlinkvsa` [do2.c:151–167] computes a V-address in the link subspace (starting at mantissa[0]=2, mantissa[1]=1 if the document has no prior links; otherwise just past the current reach), and `docopy` inserts the link's ISA there. The link is now part of the document's POOM content.

**3. Stores endpoints in the link's own orgl and in the global spanfilade** [do1.c:213–219]:
```c
findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
setlinkvsas(&fromvsa, &tovsa, &threevsa)
insertendsetsinorgl(taskptr, linkisaptr, link, &fromvsa, fromsporglset, ...)
insertendsetsinspanf(taskptr, spanf, linkisaptr, fromsporglset, tosporglset, ...)
```
The link's own orgl stores endpoint sporgl sets at fixed internal V-addresses (from=1.1, to=2.1, three=3.1) [do2.c:169–183]. The global spanfilade (`spanf`) gets entries keyed by the link's ISA in ORGLRANGE and the endpoint I-spans in SPANRANGE [spanf1.c:22–51].

---

### What the V-address ownership actually does

#### A. Version inheritance — links travel with their documents

`docreatenewversion` [do1.c:260–299] copies the *entire* V-span of the source document:
```c
doretrievedocvspanfoo(taskptr, isaptr, &vspan)
// vspan.stream and vspan.width cover text + link subspace
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec)
```
The V-span returned by `retrievedocumentpartofvspanpm` [orglinks.c:155–162] is the full root crum extent — it encompasses both text content and link references. Because link ISAs live in the document's link subspace, they're automatically duplicated into the new version's POOM. **A link is owned by whichever version of the document it was created in, and that link reference propagates forward through all derived versions.**

#### B. Write-access gating at creation time

`docopy` calls `findorgl(taskptr, granf, docisaptr, &docorgl, WRITEBERT)` [do1.c:55]. You need write access to the containing document to create a link in it. Without that, you can't call `findnextlinkvsa` successfully because the BERT check will fail.

However — critically — the link's *own* orgl is opened with `NOBERTREQUIRED` [do1.c:213]. Once a link exists, anyone can follow it regardless of whether they have access to the document that "owns" it.

#### C. POOM-level partitioning for text vs. link content

The code explicitly distinguishes link crums from text crums [orglinks.c:246–261]:
```c
bool istextcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[1] == 0 && is1story(&crumptr->cwid.dsas[V]))
        return TRUE;
}
bool islinkcrum(typecorecrum *crumptr) {
    if (crumptr->cdsp.dsas[V].mantissa[0] == 1 && crumptr->cdsp.dsas[V].mantissa[1] != 0)
        return TRUE;
}
```
`maxtextwid` [orglinks.c:240] skips link crums entirely: `if(ptr && !islinkcrum(ptr))`. The text extent of a document is measured without counting link references. `retrievevspansetpm` [orglinks.c:173–221] returns *two* separate V-spans: one for the text portion and one for the link portion, explicitly splitting them.

And `filter_vspanset_to_text_subspace` [do1.c:386–411] — added as a semantic fix — filters out all V < 1.0 content before version comparison, because:
```c
/* Link references at V-position 0.x are document metadata, not
 * transcludable content. They have unique ISAs, not permascroll addresses,
 * so comparing them is semantically undefined. */
```
The link subspace is explicitly categorized as *metadata*, not content.

---

### What the V-address ownership does NOT do

#### Link following ignores document ownership entirely

`dofollowlink` [do1.c:223–232]:
```c
link2sporglset(taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
linksporglset2specset(taskptr, &((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED)
```
The containing document is never consulted. The link is opened directly via its ISA tumbler, BERT is bypassed, and the endpoint sporgl set is read from the link's own orgl.

#### Link finding ignores document ownership entirely

`findlinksfromtothreesp` [spanf1.c:56–103] converts query specsets to sporglsets (V→I), then calls:
```c
sporglset2linkset(taskptr, (typecuc*)spanfptr, fromsporglset, &fromlinkset, orglrange, LINKFROMSPAN)
```
This searches the global spanfilade by I-span overlap. The spanfilade has no index keyed by which document owns the link. Any link whose endpoint I-spans overlap the query I-spans is returned, regardless of which document created it.

The disabled code in `retrievesporglsetinrange` [spanf1.c:245] is the tell:
```c
context = retrieverestricted((typecuc*)spanf, (typespan*)sporglptr, SPANRANGE, whichspace, ORGLRANGE,
    (typeisa*)NULL /*kluge to make links show thru to version &sporglptr->sporgladdress*/);
```
The `NULL` is passed where the home document ISA could have been used to *restrict* link retrieval to a specific document's links. The comment shows this was considered and rejected — passing `NULL` means every link in the spanfilade is eligible regardless of its home document. The alternative (using `&sporglptr->sporgladdress`) would have made link traversal version-aware by filtering links to those owned by a particular document version.

---

### The real answer to the question

The V-address within the document's link subspace serves three purposes:

1. **Tumbler namespace scoping**: The link's ISA is permanently allocated under the creating document's ISA via `makehint` [do1.c:207]. The link's identity is cryptographically/structurally tied to its creator document.

2. **Version propagation**: Because the link's ISA is stored in the document's POOM, it travels to all new versions of the document automatically. The link is permanently associated with the document *lineage*, not just a single version.

3. **Creation-time access control**: You need WRITEBERT on the containing document to create a link. After creation, the document association is irrelevant to link operation.

The V-address ownership does **not** matter for link following, finding, or access control at runtime. Links are globally discoverable through the spanfilade's I-space index — which is entirely document-agnostic. The containing document's V-address is metadata about provenance and lineage, not a functional constraint on link traversal.

The abandoned `homedoc` kluge [spanf1.c:245] reveals the original design tension: the Xanadu architecture *wanted* links to be version-aware (belonging to a particular document version), but the implementation settled on unconditional global discoverability. The V-address records what *would have* mattered, but the runtime machinery ignores it.

---

## Question 19 [gregory]

> For a link whose target endset spans a region that has been partially deleted (some I-addresses still in V-streams, others orphaned), FOLLOWLINK returns only the surviving portion after I→V filtering — was partial endset resolution an acceptable design outcome, or should the system have signaled incompleteness to the caller?

### Gregory's Answer

## KB Synthesis

The KB describes the behavior precisely but is silent on whether it reflects considered design intent or an oversight. Here's what I can synthesize:

**What the system actually does**

FOLLOWLINK silently drops I-addresses with no current POOM mapping via `span2spanset` / `retrieverestricted` returning NULL [INV-ITOV-FILTERING, SS-FOLLOWLINK]. The caller receives a partial result with no flag indicating incompleteness. From [EC-GHOST-LINK]: three result states exist (full, partial, empty), and all three return `works: true`.

**The case that partial resolution is the intended design**

The architecture treats V-space as a mutable projection over a permanent I-space. I-addresses never die [INV-CONTENT-IMMUTABILITY, INV-NO-IADDR-REUSE]. A "deleted" endpoint is not destroyed — it is merely unreferenced in the queried document's POOM at this moment. [EC-GHOST-LINK] notes explicitly: "Reconstitution is always possible since I-addresses are permanent (P0)." The design appears to say: the link is pointing at real, permanent content; the current V-view of that content is simply incomplete. Returning what's visible is honest.

This is internally consistent with [EC-LINK-PARTIAL-SURVIVAL]: "The link validity predicate is per-I-span, not per-endset." Each I-span is independently valid. A partial result isn't a defective result — it's the correct answer about which pieces of the endpoint are *currently visible*.

**The case for signaling incompleteness**

The silent filtering makes FOLLOWLINK unable to distinguish between two structurally different situations:

- A link created with a narrow endpoint (was always small)
- A link whose endpoint was wider but is now partially orphaned

A caller cannot tell whether it received the full intended span or a truncated remnant. This matters for any application that needs to reason about link integrity or display "broken link" UI. The KB records no mechanism for a caller to ask "how many I-spans are in the endset vs. how many resolved."

**My read**

The silence is a design choice consistent with the whole system's philosophy — V-space is ephemeral, I-space is the ground truth. Signaling incompleteness would require the system to hold an opinion about what the "intended" extent of an endset was at creation time versus now, which would mean tracking that original extent separately. The system doesn't do this anywhere; permanence means you always get the current truth, not a diff from some prior state.

The real cost of this choice shows up in [PRE-FOLLOWLINK]: "The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result." Empty success and partial success are treated identically to full success. For the Xanadu model, that's arguably correct — the permanent record has not changed, only the current document arrangement has. For practical application developers, it's a footgun.

**Bottom line**: Partial endset resolution appears to be an acceptable outcome *within the Xanadu permanence model*, not a signal that needs to propagate. But the system provides no affordance for distinguishing a whole endpoint from a fragment, which is a real expressiveness gap any spec should acknowledge as a known limitation rather than designed behavior.

Relevant entries: [SS-FOLLOWLINK], [INV-ITOV-FILTERING], [EC-GHOST-LINK], [EC-LINK-PARTIAL-SURVIVAL], [INV-CONTENT-IMMUTABILITY], [INV-LINK-PERMANENCE], [PRE-FOLLOWLINK], [EC-ORPHANED-LINK].

---

## Code Exploration

I now have enough confirmed source to give a thorough answer. Here it is.

---

## FOLLOWLINK and Partial Endset Resolution — A Code-Level Analysis

### The Execution Path

`followlink()` [fns.c:114–127] is the entry point:

```c
void followlink(typetask *taskptr)
{
  typeisa linkisa;
  typespecset specset;
  INT whichend;
  bool getfollowlink(), dofollowlink();

    if (
       getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)){
        putfollowlink (taskptr, specset);
      }else
        putrequestfailed (taskptr);
}
```

The chain is: `getfollowlink` → `dofollowlink` → `putfollowlink`, or `putrequestfailed`. The protocol has exactly two outcomes: **success with a specset** or **request failed**. There is no third response type for "partial success."

`dofollowlink()` [do1.c:223–232]:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend,NOBERTREQUIRED)
    && linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr, NOBERTREQUIRED));
}
```

Two steps, short-circuited with `&&`:
1. **`link2sporglset()`** — reads the link's own enfilade to extract the endset as I-spans.
2. **`linksporglset2specset()`** — converts those I-spans to V-spans in the target document.

---

### Step 1: Extracting the Endset as I-spans

`link2sporglset()` [sporgl.c:67–95]:

```c
tumblerclear (&zero);
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // V-position = whichend
tumblerincrement (&zero, 0, 1, &vspan.width);          // V-width = 1
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        sporglptr = (typesporgl *)taskalloc(taskptr, sizeof(typesporgl));
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
        *sporglsetptr = (typesporglset)sporglptr;
        sporglsetptr = (typesporglset *)&sporglptr->next;
    }
    contextfree (context);
    return (TRUE);
} else{
    return (FALSE);    // ← fails if NO crums found at this V-position
}
```

This queries the **link's own enfilade** — not the target document — for I-addresses stored at V-position `whichend`. This step is asking "what I-spans does this link say its endset is?" It does not filter by whether those I-spans are currently visible anywhere. As long as the link exists and has a non-empty endset recorded at V-position `whichend`, this succeeds and returns I-spans.

---

### Step 2: Converting I-spans to V-spans (where partial deletion bites)

`linksporglset2specset()` [sporgl.c:97–123] always returns `TRUE` [line 122]:

```c
    return (TRUE);
```

Regardless of what happened inside. It calls `linksporglset2vspec()` [sporgl.c:127–137] → `sporglset2vspanset()` [sporgl.c:141–176] → `ispan2vspanset()` [orglinks.c:389–394] → `permute()` [orglinks.c:404–422] → `span2spanset()` [orglinks.c:425–454].

`span2spanset()` is where the partial deletion is silently swallowed:

```c
context = retrieverestricted((typecuc*)orgl, restrictionspanptr, restrictionindex,
                              (typespan*)NULL, targindex, (typeisa*)NULL);
for (c = context; c; c = c->nextcontext) {
    context2span(c, restrictionspanptr, restrictionindex, &foundspan, targindex);
    nextptr = (typespan *)onitemlist(taskptr, (typeitem*)&foundspan, (typeitemset*)targspansetptr);
}
if(!context){           // ← NULL = no V-stream mapping for this I-span
    return(targspansetptr);   // ← return silently, contributing nothing
}
```

When `retrieverestricted()` returns `NULL` for a given I-span (because that I-span is no longer mapped into any V-stream — it is orphaned), the `for`-loop body never executes. The `if(!context)` branch [orglinks.c:446–448] returns with `targspansetptr` unchanged, adding **nothing** to the vspanset. No error, no flag, no log even in the debug build.

`permute()` [orglinks.c:404–422] loops over all I-spans in the restriction set, calling `span2spanset()` for each. If some return content and others silently return nothing, the caller sees only the content-returning ones:

```c
for (; restrictionspanset; restrictionspanset = restrictionspanset->next) {
    targspansetptr = span2spanset(taskptr, orgl, restrictionspanset,
                                  restrictionindex, targspansetptr, targindex);
}
return (save);    // ← returns the accumulated (possibly partial) set
```

---

### The Two Cases

**Case A — Total orphaning:** Every I-span in the endset has no V-stream mapping. `link2sporglset()` still succeeds (the link's own enfilade is intact). But then `linksporglset2specset()` will produce a `specset` containing a `VSPECID` entry whose `vspanset` is `NULL`. The caller receives a success response with an empty span set. (Or, if the link document itself no longer has any crums at V-position `whichend`, `link2sporglset()` fails at [sporgl.c:93] and the caller gets `REQUEST_FAILED`.)

**Case B — Partial orphaning:** Some I-spans still have V-mappings, others do not. `link2sporglset()` extracts all I-spans (they are intact in the link's enfilade). `linksporglset2specset()` iterates all sporgl entries. For orphaned I-spans, `span2spanset()` silently contributes nothing. For surviving I-spans, `span2spanset()` appends their corresponding V-spans. The returned `specset` contains **only the surviving portion**. `linksporglset2specset()` returns `TRUE`. `dofollowlink()` returns `TRUE`. `putfollowlink()` is called. **The caller has no way to detect that the result is incomplete.**

---

### Was This an Acceptable Design Outcome?

The code is unambiguous: **partial endset resolution was the implemented behavior, and incompleteness was never signaled.** The question is whether this was a conscious design decision or an oversight.

**The case that it was intentional:**

The Xanadu model treats I-addresses as permanent and V-streams as transient views. A link's endset is stored as I-spans in the link's own enfilade — permanent by construction. What `FOLLOWLINK` returns is "the current V-stream manifestation of those I-addresses." From this perspective, returning only the surviving portion is semantically correct: the system answers "here is where this endset appears right now," and if part of it appears nowhere, that part simply does not appear. This mirrors the general Xanadu philosophy that V-stream visibility is a property of a document's current state, not of the content itself.

The code structure supports this reading. `span2spanset()` at [orglinks.c:446–448] has an explicit `if(!context)` branch — it is not an omission, it is a handled case. The author knew it could happen and chose to return silently.

**The case that incompleteness signaling was missing:**

The FEBE protocol has no mechanism to report incompleteness. `putfollowlink()` transmits a `specset`; `putrequestfailed()` signals total failure. There is no middle response. Callers cannot distinguish:
- "This link had a 3-span endset and all 3 were resolved"
- "This link had a 3-span endset; 2 were resolved; 1 was orphaned"

`linksporglset2specset()` [sporgl.c:122] always returns `TRUE`, even when every `ispan2vspanset()` call produced an empty set. The result is structurally indistinguishable from a fully resolved one.

For any application relying on link integrity — transclusion auditing, citation completeness, referential consistency — the silent partial result is a protocol gap. The system provides no warranty of completeness and no mechanism to request one.

**The verdict from the code:**

The design treated "partial endset resolution" as a normal outcome of the I→V filtering step, consistent with the Xanadu model's distinction between permanent I-addresses and dynamic V-visibility. The system was not built to *promise* that every I-span in a link's endset would be reachable as a V-span at follow time. That would have required either a completeness guarantee on the I-stream (that no content ever truly disappears) or a richer protocol response type.

What the code does **not** do is give the caller tools to detect or respond to incompleteness. That is an omission — not necessarily a design error given the model, but a gap in the protocol surface. A system built on top of this would need to implement its own completeness check by fetching the endset's raw I-spans separately (via a different query path) and comparing against what `FOLLOWLINK` returned. The FEBE protocol as implemented offers no shortcut for this.

**Specific citations:**

| Claim | File:Line |
|---|---|
| Only two protocol outcomes: success or request-failed | `fns.c:124–126` |
| `link2sporglset` fails only if link's own enfilade is empty at `whichend` | `sporgl.c:83,92–93` |
| `linksporglset2specset` always returns TRUE | `sporgl.c:122` |
| Orphaned I-span silently contributes nothing to vspanset | `orglinks.c:446–448` |
| `permute` accumulates partial sets without error | `orglinks.c:414–416` |
| No incompleteness flag exists anywhere in `dofollowlink` chain | `do1.c:228–231` |

---

## Question 20 [gregory]

> Internal links (source and target both reference the same document) — what concrete use cases motivated support for same-document links, and does bidirectional follow-link on an internal link have different semantics than on a cross-document link?

### Gregory's Answer

## KB Synthesis

## Internal Links in Udanax-Green

**On motivation — what the code reveals**

The KB doesn't record Nelson's stated rationale, but the type registry tells the story. [SS-LINK-ENDPOINT] Finding 0024 shows four registered types:

| Type | Address | Subtype |
|------|---------|---------|
| JUMP | `1.0.2.2` | — |
| QUOTE | `1.0.2.3` | — |
| FOOTNOTE | `1.0.2.6` | — |
| MARGIN | `1.0.2.6.2` | under FOOTNOTE |

FOOTNOTE, MARGIN, and JUMP are all structurally suited to same-document linking. A footnote reference mark and its footnote text both live in the same document — separating them cross-document would be artificial. The MARGIN subtype (a kind of annotation attached to text in the same document) makes the intent explicit. JUMP could serve within-document navigation (e.g., a table of contents entry to its section heading).

The more fundamental reason is that link endpoints are content identities [SS-LINK-ENDPOINT] Finding 0004, and content identity is indifferent to document boundaries. The constraint `doc(source) != doc(target)` would have had to be added explicitly; it was never imposed.

**On bidirectional follow-link semantics**

The KB is unambiguous: internal and cross-document links are identical in every observable respect [ST-LINK-CREATE] Finding 0020.

```
follow_link(internal_link, SOURCE) → specset referencing this doc
follow_link(internal_link, TARGET) → specset referencing this doc
```

Both succeed. The endset is stored as I-addresses in the link orgl [SS-FOLLOWLINK] Finding 0048. FOLLOWLINK extracts those I-addresses, then resolves them through the `homedoc` parameter's POOM. For an internal link, both endpoints resolve through the same POOM — but the POOM lookup (`span2spanset` → `retrieverestricted`) treats each endset independently with no special-case logic for "same document."

One subtle point from [SS-FOLLOWLINK] Finding 0048: FOLLOWLINK takes a `homedoc` parameter that determines which document's POOM is used for I→V resolution. For a cross-document link, you might call `follow_link(L, TARGET, doc_B)` to get the target expressed in doc_B's V-space. For an internal link, you'd pass the same document for both endpoints. If you passed a *different* document (one that had transcluded the linked content), you'd get the endpoints expressed in that document's V-space instead — this works identically for internal vs. cross-document links, since it's purely content-identity-based [INV-ITOV-FILTERING].

The only thing the KB cannot answer here is whether link discovery (`find_links`) on a document might return an internal link *twice* — once from matching the source content and once from matching the target content within the same V-span. The multi-span duplication edge case [EC-MULTISPAN-LINK-DUPLICATION] was observed with multi-span creation but wasn't specifically tested for same-document source/target overlap. That's a gap in the findings.

---

## Code Exploration

---

## Answer: Internal Links — Use Cases and Bidirectional Follow-Link Semantics

### Why Same-Document Links Are Supported

`docreatelink` (do1.c:195-221) imposes **no check** that source and target belong to different documents:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
                  typespecset fromspecset, typespecset tospecset,
                  typespecset threespecset, typeisa *linkisaptr)
{
    ...
    specset2sporglset (taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
    specset2sporglset (taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)
    ...
}
```

Each endpoint is independently converted to a sporgl via `specset2sporglset` (sporgl.c:14-33), which resolves the VSpec's `docisa` field for each independently. If both VSpecs carry the same `docisa`, the resulting sporgls simply share `sporgladdress`. There is no "same-document prohibition" anywhere in the call chain — not in `docreatelink`, not in `specset2sporglset`, not in `insertendsetsinorgl` or `insertendsetsinspanf`.

This is by design. The uniform storage model (discussed in Finding 0009, 0011) treats all link endpoints as sporgl sets: the backend doesn't need to know whether the endpoints are in the same document or not. The link's own POOM stores source endset at V=1.1 and target endset at V=2.1 (set by `setlinkvsas`, do2.c:169-183), and those V-positions in the link's internal space are orthogonal to the question of whether the endpoint documents match.

---

### Concrete Use Cases

The four link types defined in the client API (`JUMP_TYPE`, `FOOTNOTE_TYPE`, `MARGIN_TYPE`, `QUOTE_TYPE`) all have natural same-document instantiations:

| Use Case | Canonical Link Type | Concrete Example |
|----------|--------------------|-|
| **Intra-document cross-reference** | JUMP | "See §3" in body → §3 heading, same doc |
| **Footnote** | FOOTNOTE | Footnote marker → footnote text at page bottom, same doc |
| **Margin annotation** | MARGIN | Main paragraph → margin gloss, same doc |
| **Glossary/Index** | JUMP | "glossary" (body) → "Glossary:" definition section, same doc |
| **Self-transcluded content** | JUMP | Original span → vcopy of same content inserted later in same doc |

The golden test `self_referential_link.json` is the glossary pattern: source="glossary", target="Glossary" both in document `1.1.0.1.0.1`. The link is created at `1.1.0.1.0.1.0.2.1` (first link in that document's link subspace, V=0.2.1) and both `follow_link(source)` and `follow_link(target)` succeed.

The design point is architectural, not incidental. Nelson's original Xanadu concept explicitly included footnotes and glossary links — operations that inherently live within a single document. The `FOOTNOTE_TYPE` constant exists in the client API precisely because same-document annotation links are a first-class intended use case.

---

### Does Bidirectional Follow-Link Have Different Semantics for Internal Links?

**No. The code path is identical.** Here is the full trace:

#### `dofollowlink` (do1.c:223-232)

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr,
                  typespecset *specsetptr, INT whichend)
{
    typesporglset sporglset;
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr,
                              &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

#### Step 1: `link2sporglset` (sporgl.c:67-95)

Opens the link's own orgl and searches its V-space at the slot for `whichend`:

```c
tumblerincrement (&zero, 0, whichend, &vspan.stream);  // slot 1/2/3
tumblerincrement (&zero, 0, 1,        &vspan.width);   // width covers that slot
context = retrieverestricted((typecuc*)orgl, &vspan, V, NULL, I, NULL);
```

`setlinkvsas` (do2.c:169-183) placed source at V≈1.1, target at V≈2.1, type at V≈3.1 in the link's own POOM. This is internal to the link orgl and has nothing to do with what document the endpoints belong to.

`contextintosporgl` (sporgl.c:205-220) extracts the stored 2D crum info:

```c
sporglptr->sporgladdress = context->context2dinfo.homedoc;
sporglptr->sporglorigin  = context->totaloffset.dsas[I];
sporglptr->sporglwidth   = context->contextwid.dsas[I];
```

`homedoc` was stored there at link-creation time by `unpacksporgl` (sporgl.c:183-187), which copied it from `sporglset->sporgladdress` — the document that owned that endpoint at creation time.

#### Step 2: `linksporglset2specset` → `linksporglset2vspec` (sporgl.c:97-137)

```c
int linksporglset2vspec(typetask *taskptr, typeisa *homedoc, ...)
{
    specptr->docisa = *homedoc;   // note the kluge: homedoc, not sporglset->sporgladdress
    sporglset2vspanset(taskptr, homedoc, sporglsetptr, &specptr->vspanset, type);
}
```

`sporglset2vspanset` calls `ispan2vspanset` → `permute` (orglinks.c:389-454) to convert the stored I-addresses back to current V-positions in `homedoc`'s orgl. Returns a VSpec with `docisa=homedoc` and the current V-spans for that content.

#### The only behavioral difference

For a **cross-document link** (A → B):
- `follow_link(LINK_SOURCE)` → sporgladdress stored = docA → returns VSpec{docA, source-spans}
- `follow_link(LINK_TARGET)` → sporgladdress stored = docB → returns VSpec{docB, target-spans}

For an **internal link** (A → A):
- `follow_link(LINK_SOURCE)` → sporgladdress stored = docA → returns VSpec{docA, source-spans}
- `follow_link(LINK_TARGET)` → sporgladdress stored = docA → returns VSpec{docA, target-spans}

Both endsets return VSpecs with the same `docid`, pointing to different V-spans within that document. Confirmed by `self_referential_link.json`:

```json
{ "op": "follow_link", "end": "target", "result": ["Glossary"] }
{ "op": "follow_link", "end": "source", "result": ["glossary"] }
```

The code path is identical. The only practical consequence for the caller: with a cross-document link you must open a different document handle to dereference the target content; with an internal link the same already-open handle serves both.

---

### The `homedoc` Kluge (sporgl.c:134)

One subtle asymmetry is worth noting. In `linksporglset2vspec`:

```c
movetumbler (homedoc/*&sporglset->sporgladdress*/, &specptr->docisa);
```

The comment reveals the original code used each sporgl's individual `sporgladdress`. It was later changed to use a single `homedoc` — the first sporgl's address, passed from `dofollowlink`. For all real-world endpoints (single-document, whether internal or cross-document), this makes no difference: all sporgls for one endset share the same `sporgladdress`. The kluge would only matter if a single link endpoint spanned content in multiple documents simultaneously, which the architecture does not prevent but which no test exercises.

For internal links specifically, this kluge is completely benign: both the `homedoc` argument and every sporgl's `sporgladdress` are the same document ISA.

---

### Summary Table

| Property | Cross-document link | Internal link |
|----------|---------------------|---------------|
| Restriction in `docreatelink` | None | None (same path) |
| Source sporgl `sporgladdress` | docA | docA |
| Target sporgl `sporgladdress` | docB | docA |
| `follow_link(LINK_SOURCE)` | VSpec{docA, src-spans} | VSpec{docA, src-spans} |
| `follow_link(LINK_TARGET)` | VSpec{docB, tgt-spans} | VSpec{docA, tgt-spans} |
| Code path difference | None | None |
| Caller consequence | Open two docs | One open handle suffices |

Same-document links are supported because the architecture is uniform by design — `docreatelink` has no prohibition, `specset2sporglset` resolves each endpoint independently, and all four link types have natural intra-document use cases (footnote, glossary, margin note, cross-reference). `follow_link` on an internal link executes the same code as on a cross-document link; the only observable difference is that both returned VSpecs name the same document ISA.
