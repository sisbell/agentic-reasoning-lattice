## Question 8 [theory]

> What invariant must the design preserve about content permanence when an editing operation removes a span from a document's current arrangement?

## The Invariant: Vstream Removal Without Istream Destruction

The invariant the design must preserve is: **deletion removes content from the document's current arrangement (Vstream) but never destroys it in permanent storage (Istream).** The bytes remain at their permanent Istream addresses forever, regardless of whether they appear in the document's current view.

This is the fundamental distinction between Vstream deletion and Istream permanence. As the delete-semantics design note states, DELETE in Xanadu "removes content from a document's Vstream (current arrangement) but does NOT remove it from Istream (permanent storage)."

### What the invariant guarantees

Nelson's architecture treats "DELETED BYTES" as a valid system state, annotated in the diagram on page 4/9:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

The three clauses of that annotation encode the invariant precisely:
1. **"not currently addressable"** — gone from the current Vstream arrangement
2. **"awaiting historical backtrack functions"** — recoverable from any previous version
3. **"may remain included in other versions"** — transclusions in other documents still resolve

### Why content must persist

The content store is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes flow into the storage system, filed, as it were, chronologically." (2/14)

And critically, deleted bytes survive in any document that transcluded them:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

### Consequences that depend on this invariant

Because Istream content survives Vstream deletion:

- **Links survive.** Links attach to bytes via Istream addresses, not Vstream positions: "If any of the bytes are left to which a link is attached, that link remains on them." (4/42)
- **Historical backtrack works.** Any previous arrangement can be reconstructed — "when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)
- **Originals are never damaged.** "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." (2/45)

### Summary

| Aspect | Affected by DELETE? |
|--------|---------------------|
| Vstream arrangement | YES — content removed from current view |
| Istream content | NO — bytes remain forever |
| Previous versions | NO — still contain the content |
| Transclusions in other docs | NO — still resolve |
| Links to the content | NO — still resolve to Istream |

The invariant in one sentence: **a delete is a Vstream operation that must leave Istream untouched** — nothing in Xanadu is ever truly destroyed, only made "not currently addressable" pending historical backtrack.
