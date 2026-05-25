## Question 5 [theory]

> Must the result of a deletion comparison itself be a referenceable document that users can link to, share, and quote from?

# Must Deletion Comparison Results Be Referenceable Documents?

**No.** Comparison results are computed output, not stored documents.

## What Nelson Specifies

The operation `SHOWRELATIONOF2VERSIONS` returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. This is computational output - a transient response to a query - not a new persistent document.

Most FEBE operations behave this way. Nelson notes: "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments" [LM 4/61]. The others return metadata, lists, and computed relationships.

## The "Everything Is a Document" Principle

Nelson does say: "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document" [LM 2/29].

But this applies to *stored content*. The inputs to a comparison (the versions, the spans) are documents with permanent tumbler addresses. The computed *correspondence* between them is a relation - structurally implicit in shared Istream origin, not a stored artifact.

## How Users Can Make Findings Referenceable

If a user wants to preserve and share a comparison finding, the system offers two mechanisms:

1. **Counterpart links** - the explicit way to mark correspondences: "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages" [LM 4/53]. The link itself is a first-class object with its own tumbler address - referenceable, linkable, quotable.

2. **Write a document** - any user can compose a document discussing the comparison, with quote-links windowing into the relevant spans.

## Design Intent

The architecture cleanly separates:
- **Operations** (compute correspondence on demand from shared Istream)
- **Assertions** (counterpart links - user-created, persistent, referenceable)

Forcing every comparison result into a document would conflate query results with stored content. Nelson keeps these distinct: the system makes correspondence *discoverable* through structure; users *publish* findings when they choose.

NEED_RAW: 4/70 (to verify exact SHOWRELATIONOF2VERSIONS return semantics if precision matters for your design decision)
