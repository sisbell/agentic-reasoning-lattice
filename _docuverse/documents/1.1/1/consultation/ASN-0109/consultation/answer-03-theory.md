## Question 3 [theory]

> Must reading a link's endsets reveal the identity of every document participating in the relationship, even documents the reader has never seen?

# Must reading a link's endsets reveal every participating document's identity?

**Yes — structurally and unavoidably, for identity (not content).** A link's endsets *are* sets of tumbler spans, and a tumbler span necessarily names the document it falls in. You cannot read an endset without reading the addresses it contains, and an address discloses its document by construction. This holds whether or not the reader has ever opened those documents.

## Why this is unavoidable

An endset is not a pointer to "a document the reader already has" — it is an arbitrary span-set mapped onto the universal address space:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." — 4/42

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse." — 4/43

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." — 4/45

Because every endset maps to the tumbler line, and a tumbler encodes Node.User.**Document**.Element, the document field is *inside the address you just retrieved*. The retrieval operation hands back exactly these spans:

> "This returns a list of all link end-sets that are in <spec set>." — 4/70 (RETRIEVEENDSETS)

So a from-set that touches three different authors' works will, when read, name all three documents — even ones the reader has never seen. This is the same property that makes the docuverse traceable everywhere:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." — 2/40

A discontiguous endset spanning many documents simply names *all* of them. There is no "summary" form of an endset that hides the participants; the participants are the endset.

## Two important qualifications

**1. Identity is disclosed; content is not.** Reading the endsets tells you *which* documents and *which* spans participate — their addresses. It does not deliver their bytes. Fetching content is a separate retrieval (RETRIEVEV), and that is where the private/published distinction and royalty apply. So a reader can learn that document X participates in a relationship without being able to read X.

**2. A "participating document" may be a ghost.** This is especially true of the type endset (the 3-set), whose address need not have anything stored at it:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." — 4/45

So some "documents" revealed by reading the endsets are conceptual positions in tumbler-space, not stored works. The endset still names them.

## Design intent

This is deliberate, not incidental. The whole point of the endset generalization — from point-to-point to set-to-set across the universal address space — is that a connection is *about named regions of the docuverse*, and those names are first-class and public within the link. The reader of a link is meant to be able to see the full shape of the relationship and navigate to any end of it, including ends in works they have not yet encountered. That is how the web of connection becomes traversable.

---

**One thing the curated sources do not settle:** whether endset *retrieval* is gated when an endset points into a **private** document the reader has not been granted. The architecture makes endsets name their documents by construction, and XU.87.1 is noted to have "all documents visible to all users" (4/79), so the question of withholding an endset's address purely on privacy grounds is not addressed in the verified material above. If you want my ruling on whether a private endset address should be suppressed at retrieval (identity-leak vs. traceability), that would go beyond what is explicitly specified.

NEED_RAW: 4/70 (full RETRIEVEENDSETS / RETRIEVEV wording), 4/55–4/60 (link search and any privacy/filtering provisions on endset disclosure)
