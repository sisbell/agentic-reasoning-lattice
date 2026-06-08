## Question 3 [theory]

> Must the act of transcluding content into a destination leave the source document completely unaware that it has been copied from?

No — and this is fundamental to Nelson's design. Transclusion is precisely the mechanism that *prevents* the source from being unaware. The whole point is that the connection from source to destination remains traceable from both ends.

## The Answer

A transclusion (Nelson's "window," "quote-link," or "inclusion") is inclusion by reference, not copy. Because the destination references the source's permanent I-address rather than duplicating the bytes, the source remains structurally connected to every document that includes it. This connection is discoverable from the source side.

### Two-way discovery is guaranteed

Nelson explicitly requires that you can ask, from the source, what windows to it:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." (windowing, 2/46 region)

The bidirectional "What connects here?" query covers this:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." (document-discovery, 2/46)

### The FEBE operation makes it explicit

`FINDDOCSCONTAINING` exists specifically to find transclusions of given content, regardless of where the copies live:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (operations, 4/63)

### Why the source *must* be aware: royalties

The economic model depends on the source being aware it has been transcluded. The original owner is paid every time their windowed content is delivered:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." (transclusion/versions, 2/45)

This automatic split is impossible if transclusion were invisible to the source.

### The contrast: a *copy* is what severs awareness

Nelson draws exactly this distinction. A true copy is "frozen and dead" precisely because it cuts the connection:

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy." (transclusion, 2/48)

> "The free-flowing, live documents on the network are subject to constant new use and linkage, and those new links continually become interactively available. Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." (transclusion, 2/48)

So the *absence* of source-awareness is the defining property of copying — the thing transclusion was invented to avoid.

## Summary

Transclusion must do the **opposite** of leaving the source unaware. By design it keeps the source permanently and discoverably connected: the source can enumerate every document that windows to it, the connection survives editing, and royalties flow automatically to the source owner. A connection that left the source unaware would be a mere copy — "frozen and dead" — not a transclusion.
