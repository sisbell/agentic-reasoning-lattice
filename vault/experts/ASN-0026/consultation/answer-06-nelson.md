## Question 6 [nelson]

> If content is added to permanent storage but no document currently arranges it, does that content still exist and remain retrievable?

## Yes — Content in I-Space Always Exists, But Addressability Is Through V-Space

The content **exists permanently**. I-space is append-only; nothing is ever removed from it. But "retrievable" requires some nuance about *how* you reach it.

### The Existence Guarantee

I-space is the permanent home of all content:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." — 2/14

Every byte created gets a permanent I-address that will always return that exact content. This is unconditional. No operation in the system removes content from I-space.

### The Addressability Question

The FEBE protocol provides exactly **one** content retrieval command: `RETRIEVEV`, which works through V-space addresses. There is no `RETRIEVEI`. Nelson is explicit that I-space addresses are internal:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." — 4/11

Users work in V-space. I-space is the back end's domain.

### The "Deleted Bytes" State

Nelson directly addresses content that exists in I-space but has been removed from a document's current V-space arrangement. The diagram on page 4/9 labels this state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

Three key phrases here:

1. **"not currently addressable"** — No current V-space arrangement maps to this content, so `RETRIEVEV` through the current document won't find it.

2. **"awaiting historical backtrack functions"** — Previous versions of the document still arrange this content in their V-space. You can always reconstruct those arrangements: "when you ask for a given part of a given version at a given time, it comes to your screen" (2/15).

3. **"may remain included in other versions"** — If other documents transclude this content, their V-space arrangements still reference it, and it remains fully addressable through those documents.

### The Practical Paths to Retrieval

Content that no *current* document arranges is still reachable through:

| Path | Mechanism |
|------|-----------|
| **Historical backtrack** | Request a previous version that included the content — its V-space arrangement is reconstructed on demand |
| **Transclusion in other documents** | Other documents that window this content still reference its I-address |
| **Links** | Links point to I-space; a link to this content still resolves even after V-space deletion |
| **FINDDOCSCONTAINING** | Can discover which documents (including historical versions) contain the material |

Additionally, Nelson confirms that deletion from one document does not affect others:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." — 4/11

### The Theoretical Edge Case

Could content exist in I-space with *no* V-space arrangement ever having referenced it? In practice, no. Every content-creation operation (`INSERT`, `APPEND`) simultaneously creates I-space content *and* a V-space mapping. There is no FEBE command to write directly to I-space without placing content in a document. So "orphaned" I-space content only arises through deletion — and deletion preserves historical versions.

### Summary

The content **exists** unconditionally and permanently. It is **retrievable** through historical backtrack, through other documents that transclude it, and through links that reference its I-address. What it is *not* is "currently addressable" through the document that deleted it from its present arrangement — but that is a narrow constraint on one access path, not on existence or retrievability in general.

Nelson designed the system so that the question "does it still exist?" always has the answer yes. The only question is which V-space arrangement you use to reach it.
