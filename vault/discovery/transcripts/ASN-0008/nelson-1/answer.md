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