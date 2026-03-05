# Links and Transcluded Content

**Yes.** Links that point to content in its original document also apply when that same content appears in a transcluding document. This is not a special feature but an architectural consequence of how I-space, V-space, links, and transclusion interact.

## The Mechanism

The answer follows from three design facts:

**1. Links attach to I-space addresses, not V-space positions.**

> "A Xanadu link is not between points, but between spans of data." [LM 4/42]

Links point to the permanent identity of bytes (I-space), not to their current arrangement in any particular document (V-space).

**2. Transclusion shares I-space addresses.**

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

When Bob transcludes content from Alice's document, Bob's document creates a V-space mapping to the *same* I-space addresses. The bytes are not copied — they are referenced. Both documents point to identical I-space content.

**3. Therefore, any link targeting those I-space addresses applies in both documents.**

If Carol creates a link whose endset points to I-addresses X through Y, and those addresses appear in both Alice's document (natively) and Bob's document (by transclusion), Carol's link connects to the content in both places.

## Nelson's Explicit Confirmation (for Versions)

Nelson states this principle explicitly for the case of versions, which share I-space content through the same mechanism as transclusion:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Versions share I-space addresses just as transclusions do. The principle is identical: shared I-space identity means shared link applicability.

## Supporting Operations

Two FEBE operations confirm the system is designed to work this way:

**FINDDOCSCONTAINING** — finds all documents containing specified material, regardless of where native copies are located:

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

This operation exists precisely because the system tracks where content appears across transclusions.

**FINDLINKSFROMTOTHREE** — searches links by endset address ranges:

> "This returns a list of all links which are (1) in \<home set\>, (2) from all or any part of \<from set\>, and (3) to all or any part of \<to set\> and \<three set\>." [LM 4/69]

When a reader asks "what links connect to this passage?" while reading Bob's transcluding document, the system resolves the V-space position to I-space, finds the same I-addresses as in Alice's original, and discovers all links targeting that content.

## Bidirectional Discovery

Nelson explicitly requires that readers can discover all connections to any content they are viewing:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'— and be shown all these outside connections without appreciable delay." [LM 2/46]

This guarantee applies regardless of whether you are reading the content in its native document or in a transcluding document. The content is the same bytes at the same I-addresses; the links are the same links.

## The Deeper Point

This behavior is what makes transclusion fundamentally different from copying. A copy severs the content from its identity — and therefore from its links. A transclusion preserves identity — and therefore preserves all connections.

> "Note also that he or she who makes a paper copy or disk is losing all dynamic link connections, and is left with the inert, non-interactive copy. And that will be a considerable deprivation in the world we are talking about." [LM 2/48]

The "dynamic link connections" that copying destroys are precisely the connections that transclusion preserves. When content appears by transclusion, it brings its entire web of links with it — annotations, citations, comments, counterpart links — because those links attach to the content's permanent identity, not to the document that happens to display it.