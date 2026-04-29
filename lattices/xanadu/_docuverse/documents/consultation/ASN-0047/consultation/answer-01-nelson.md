## Question 1 [nelson]

> You describe the docuverse as containing "nothing except documents and their arbitrary links." If these are the only two things stored, what are the ways the docuverse can change?

# How the Docuverse Changes

You quote the essential statement from page 4/41:

> "The link mechanism ties together the whole corpus of materials on the Xanadu system. There is essentially nothing in the Xanadu system except documents and their arbitrary links." [LM 4/41]

Since the docuverse contains only documents and links, the ways it can change are precisely the operations that affect these two entities. Let me enumerate them.

## The Docuverse Grows

The fundamental mode of change is **growth**. The docuverse is append-only at the I-space level.

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### New Documents Are Created

**CREATENEWDOCUMENT** creates an empty document with a fresh tumbler address. **CREATENEWVERSION** creates a new document whose contents derive from an existing one, with the new address indicating ancestry [LM 4/65-4/66]. Both add permanent addresses to the docuverse that will never be reused or reassigned.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

### New Content Is Added

**INSERT** places new bytes at a position in a document. **APPEND** adds bytes to the end [LM 4/66-4/67]. In both cases, new content enters I-space permanently. The bytes receive permanent I-addresses encoding their origin—which server, which account, which document created them [LM 4/26].

### New Links Are Created

**MAKELINK** creates a link in a specified document, connecting a from-set to a to-set with a type designation. It returns the new link's address [LM 4/68]. Links are first-class citizens with their own tumbler addresses. They can point to any spans anywhere in the docuverse—including to other links [LM 4/49].

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

### New Addresses Fork Into Existence

The address space itself grows through forking. Servers spawn servers, accounts spawn accounts, documents spawn documents—each owner "baptizing" new addresses beneath their own [LM 4/17-4/20].

> "So the docuverse is all really one big forking document." [LM 4/18]

## Documents Are Rearranged

The second mode of change is **rearrangement of V-space**—the virtual arrangement that constitutes a document's current state.

### Content Is Rearranged

**REARRANGE** transposes two regions of text within a document [LM 4/67]. This changes V-space positions but touches nothing in I-space. The same bytes appear in a different order.

### Content Is Transcluded

**COPY** takes material specified by a span-set and places it in another document at a given position [LM 4/67]. This is transclusion—the copy shares I-addresses with the source. No new content is created in I-space; a new V-space mapping is created that references existing content.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

### Content Is Removed From View

**DELETEVSPAN** removes a span from a document's V-space [LM 4/66]. This is crucial: deletion does NOT destroy content. It removes content from the current arrangement only.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Links Are Removed From View

Links can also be deleted by their owner, entering a parallel "DELETED LINKS" state—"not currently addressable, awaiting historical backtrack functions, may remain included in other versions" [LM 4/9]. The link still exists in I-space.

## Documents Change State

The third mode of change is **state transition**—a document moves from private to published.

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone." [LM 2/42]

Publication is a solemn, deliberate act involving a contract [LM 2/42-2/43]. Once published, a document creates permanent obligations: the author cannot easily withdraw it because others will have linked to it.

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

## What Cannot Happen

Equally important is what the docuverse does NOT permit:

1. **I-space content is never destroyed.** There is no operation that removes bytes from permanent storage. "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version" [LM 2/14]—Xanadu rejects this entirely.

2. **Addresses are never reassigned.** A tumbler address, once baptized, permanently denotes that entity.

3. **History is never erased.** Every previous arrangement remains reconstructable. "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

4. **Links cannot be severed by non-owners.** You cannot delete someone else's link to your document. You can only delete content at your end, which may cause the link to lose its attachment—but only if ALL bytes at that end are removed [LM 4/42-4/43].

## Summary

The complete taxonomy of docuverse changes:

| Change | What grows or moves | I-space effect | V-space effect |
|--------|-------------------|----------------|----------------|
| Create document | New document address | None yet | New empty V-stream |
| Create version | New document from existing | None (shares I-content) | New V-stream arrangement |
| Insert/Append | New content bytes | Bytes added permanently | V-stream grows |
| Make link | New link | Link stored permanently | Link added to home document |
| Copy (transclude) | New reference | None (shares I-content) | V-stream references existing bytes |
| Rearrange | Content order | None | V-stream reordered |
| Delete content | Content hidden | None (bytes persist) | V-stream shrinks |
| Delete link | Link hidden | None (link persists) | Link removed from current view |
| Publish | Access state | None | Document becomes universally readable |
| Fork addresses | New sub-addresses | None | New positions available |

The docuverse is, at bottom, an ever-growing, never-shrinking accumulation. It adds documents, adds bytes, adds links, rearranges views—but never truly destroys. As I put it:

> "A document is really an evolving ONGOING BRAID." [LM 2/14]

The braid only grows more complex. It never unravels.
