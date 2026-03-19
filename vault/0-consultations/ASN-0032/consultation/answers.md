# Consultation Answers — Link Ontology

**Inquiry:** What is a link in the Xanadu system? What are links for, what do they connect, and what must be true about them as permanent objects in the docuverse?
**Date:** 2026-03-12 14:17
**Questions:** 10 (6 nelson, 4 gregory) — trimmed from 20; removed 3,4,8,9,11,14,16,17,19,20 (out of scope: discovery, operations, versioning)

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
