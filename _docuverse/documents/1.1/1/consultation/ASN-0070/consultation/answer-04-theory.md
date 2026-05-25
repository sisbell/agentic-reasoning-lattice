## Question 4 [theory]

> How must the system handle an endset that refers to content which has been removed from every version of the document currently being viewed?

# Endsets Pointing to "Removed" Content

The premise needs unpacking, because in Xanadu "removed" doesn't mean what it means in conventional systems. When a user issues DELETEVSPAN, content disappears from the document's current Vstream arrangement, but it remains permanently in Istream. Page 4/9 explicitly catalogs DELETED BYTES as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

So your question really asks: what about an endset pointing to bytes that have been DELETEVSPAN'd from every version's Vstream arrangement of the document you're currently viewing?

## The Link Must Not Break

This is fundamental to my design:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The endset points to Istream — the permanent address space. Istream is append-only by design. Those bytes were never destroyed; they were only removed from the current visible arrangement. The strap is still attached.

The "if anything is left at each end" clause is satisfied automatically, because Istream bytes are never destroyed. That's the whole point of separating Istream from Vstream — to make this guarantee structural rather than aspirational.

## What the System Must Do

1. **Preserve the endset and the link object.** The link remains a first-class citizen of the docuverse.
2. **Honor link searches that include it.** FINDLINKSFROMTOTHREE must still return it; the bookkeeping does not change because Vstream changed.
3. **Allow retrieval via historical backtrack.** The "awaiting historical backtrack functions" annotation on 4/9 is not decoration — it is a system obligation.
4. **Honor FINDDOCSCONTAINING.** The content may live in other documents via transclusion:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

## What the Front-End May Decide

The semantic guarantee is that the link survives and the content remains addressable. *How* the front-end presents an endset whose target is not in the current Vstream view — whether to indicate it visually, offer "show me the historical version" navigation, fetch and inline the content from Istream, or fold to a version where the bytes remain visible — is a presentation decision, not a back-end one. I left this to front-end implementors deliberately, because reasonable presentations differ for citations, comments, threads, and so on.

## What Would Actually Break a Link

A link breaks only if "all bytes at an endset are deleted (nothing left to attach to)" *in Istream itself*. In a properly built Xanadu system, this cannot happen. The permascroll is append-only. There is no operation in FEBE that destroys Istream bytes. If an implementation ever lets Istream bytes vanish, it has broken the contract, not the link.

This is why I called the link a strap between bytes rather than a pointer to a position. A strap holds onto what it grasps. The bytes don't disappear; they may simply no longer be arranged where you are looking.
