## Question 1 [theory]

> In the design, are content and link addresses produced by a single allocator under each document, or by two distinct sibling allocators — and if distinct, what spawning mechanism establishes the link allocator?

# Two Distinct Sibling Allocators

Content (bytes) and links are addressed by **two distinct sibling subspaces** under each document/version, not by a single allocator. They share the document/version as parent but have separate numbering schemes.

## The Address Structure

Within a document's version, the document-local address space partitions by a numeric subspace marker:

| Subspace | Address Pattern | Contents |
|----------|-----------------|----------|
| Bytes | `N.0.U.0.D.V.0.1.x` | Text content (rearrangeable in Vstream) |
| Links | `N.0.U.0.D.V.0.2.N` | Links whose home is this document |

The curated source records this explicitly with examples:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

And for the byte subspace:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." (4/30)

## Why They Must Be Distinct

The two subspaces have fundamentally different semantics:

- **Bytes (subspace 1)** are Vstream positions — they shift on INSERT/DELETE/REARRANGE:
  > "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)
- **Links (subspace 2)** are creation-ordered and permanent:
  > "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Mixing them under a single allocator would couple link identity to byte arrangement — which would break link survivability under editing.

## Spawning Mechanism

The curated sources describe the **address-space convention** (subspaces "1" and "2" reserved by position-digit) but do not explicitly describe a runtime "spawn the link allocator" act. The two subspaces appear to be **implicit in the tumbler scheme itself** — established by convention at document creation, not by a separate FEBE operation. CREATENEWDOCUMENT establishes the document address; both subspaces exist under it by structural convention.

The curated source also hints at further subdivision being open-ended:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

NEED_RAW: 4/30-4/31 — to verify whether Nelson describes the byte/link split as a runtime allocator-spawning act vs. a static convention of the tumbler scheme, and to confirm the exact "1"/"2" subspace literals (the curated note in `i-space-addresses.md` mentions a "3" digit for the link serial, which may conflict with the "2" form quoted above).
