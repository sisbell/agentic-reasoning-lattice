## Question 1 [theory]

> When a reader asks SHOWORIGIN over a V-span containing link-subspace positions, did the design intend the operation to report the link's origin document (treating links as first-class transcludable content), or was SHOWORIGIN intended to apply only to content-subspace material?

Speaking as Ted Nelson on design intent:

First, a correction on terminology — **SHOWORIGIN isn't among the 17 commands of XU.87.1** I documented. The FEBE operation closest to "show origin" is **FINDDOCSCONTAINING**, which "returns a list of all documents containing any portion of the material included by <vspec set>" (4/70). So your question is really about whether origin-reporting operations were intended to apply uniformly across both subspaces.

**The design intent is clear: origin reporting applies to anything in tumbler-space, including links.**

Three principles compel this:

1. **Links are first-class citizens with home documents.** "Its home document indicates who owns it, and not what it points to" (4/12). The address structure `N.0.U.0.D.V.0.2.N` structurally encodes the link's home — origin lookup on a link address is just reading the document field of its tumbler.

2. **Origin traceability is universal.** "You always know where you are, and can at once ascertain the home document of any specific word or character" (2/40). I never qualified this with "...but not for links." The principle was meant to be exceptionless.

3. **Links are returnable as document material.** RETRIEVEV "returns the material (text and links) determined by <spec set>" (4/67). And RETRIEVEDOCVSPANSET returns counts for "both the number of characters of text and the number of links in document" (4/68). The protocol treats both subspaces as constituting the document.

So when a V-spec set traverses link-subspace positions (the `0.2.N` range), origin-reporting should resolve each link to its home document — the document where MAKELINK was executed with that link's specification. This is not link-as-special-case; it's the same structural lookup that works for bytes.

The deeper reason: I designed the link mechanism so links *could* be the targets of other links (link-to-link, compound links, faceted classifications at 4/49-4/51). That entire layer of meta-structure only works if links are addressable, transcludable, and traceable — which means origin-reporting must work on them.

NEED_RAW: 4/63, 4/70 (page-230, page-237) for FINDDOCSCONTAINING's exact span semantics — specifically whether the operation's vspec-set was specified to accept link-subspace addresses, or whether the implementation was permitted to restrict it to `0.1.x` positions. The principle says yes; the protocol grammar in those pages would confirm.
