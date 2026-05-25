## Question 1 [theory]

> Did the design contemplate endsets whose coverage spans both content and link subspaces, and was FOLLOWLINK expected to return cross-subspace results?

# On Cross-Subspace Endsets and FOLLOWLINK

## Cross-subspace endsets: yes, by construction

The design absolutely contemplated endsets whose coverage spans both content (bytes) and link subspaces. This follows necessarily from three architectural commitments:

**1. The tumbler address space is unified.** Bytes and links both live in tumbler-space, addressed in the same scheme. Within a document, bytes occupy `1.x` and links occupy `0.2.N`, but these are subspaces of one address line, not separate namespaces.

**2. Endsets are arbitrary span-sets.** From [endsets](endsets.md):

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." [LM 4/43]

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" [LM 4/45]

**3. Spans explicitly cover heterogeneous combinations.** This is the decisive point. From [spans](spans.md):

> "Thus we may have spans of characters, spans of links, spans of documents, spans of versions, and spans covering large combinations of them--including spans of servers with all their contents." [LM 4/24]

A span like `N.0.U.0.D.V.0.1` (designating "all elements" in version V via the 1-position convention) inherently sweeps both the byte subspace and the link subspace. From spans:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." [LM 4/38]

This is not an edge case — it's the natural consequence of spans being subtrees of the docuverse, where the content of a span is implicit in its boundaries.

## FOLLOWLINK: not in the original 17

I must be precise here. FOLLOWLINK is **not** among the 17 commands in XU.87.1. My link operations were:

- **MAKELINK** — create a link
- **FINDLINKSFROMTOTHREE** — search by endset constraints
- **FINDNUMOFLINKSFROMTOTHREE** — count matches
- **FINDNEXTNLINKSFROMTOTHREE** — paginate
- **RETRIEVEENDSETS** — "returns a list of all link end-sets that are in <spec set>" [LM 4/70]

To "follow" a link in my design meant a two-step front-end pattern: RETRIEVEENDSETS to get the endsets, then RETRIEVEV on those endsets to fetch material. And critically, **RETRIEVEV was already cross-subspace by design** — from [operations](operations.md):

> "RETRIEVEV: This returns the material (text and links) determined by <spec set>." [LM 4/67]

So the cross-subspace return was contemplated and built into retrieval from the start.

## Answer to the specific question

**Yes** to the first part: endsets covering both subspaces were a deliberate design property, falling out of the universal tumbler line and the rule that spans cover subtrees.

**For FOLLOWLINK as a single operation:** since it isn't in my original protocol, I cannot point to a specification of what it returns. But the design intent is unambiguous — any operation that resolves an endset to its contents should return whatever the endset covers. If the endset spans both bytes and links (and per LM 4/24 it certainly may), the return must include both. RETRIEVEV already worked this way.

NEED_RAW: 4/55–4/60, 4/61–4/70 — to verify whether any "follow"-type operation appears in the FEBE protocol text and to confirm whether RETRIEVEV's "text and links" return is qualified anywhere with respect to mixed-subspace spec-sets.
