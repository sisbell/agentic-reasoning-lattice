## Question 1 [theory]

> When new content is placed at a position within a document, what must the system guarantee about the identity of that content — is it given a permanent identity at the moment of insertion, distinct from the document's arrangement of it?

# Content Identity at Insertion

**Yes.** When new content is placed into a document, the system gives it a permanent identity — an **Istream (I-address)** — at the moment of insertion, and that identity is strictly distinct from the document's **arrangement** of the content (its **Vstream / V-address**). This separation of content-identity from arrangement is the foundational guarantee on which links, transclusion, versioning, and historical backtrack all depend.

## The two address spaces

Xanadu maintains two distinct address spaces (`i-space-v-space.md`):

- **Istream (Invariant Space)** — where content *permanently lives*; addresses are "absolute and immutable" and the content at an Istream address "never changes."
- **Vstream (Virtual/Version Space)** — the document's *arrangement* of that content; a view that can be rearranged across versions.

The guarantee at insertion is therefore twofold: the byte acquires a permanent home (its identity), while its position in the document is merely the current arrangement.

## What INSERT actually does

The INSERT operation distinguishes these two effects explicitly. Per `operations.md` (4/66):

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

Note what changes and what does not: the *V-stream addresses* of following characters shift (arrangement is mutable), but the inserted content itself is added to permanent storage and receives a stable identity.

## The identity is permanent; the arrangement is ephemeral

The V-address — the position in the document — is explicitly described as changeable, while the byte's underlying identity is not (`i-space-v-space.md`, 4/11):

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

And from `v-space-addresses.md` (4/30), the permanence of identity beneath the mutable ordering is the key invariant:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

This is the crux: links attach to *the bytes themselves* (their permanent Istream identity), not to their arrangement positions — which is exactly why insertion shifting V-addresses does not break anything.

## Why the identity must be permanent at the moment of creation

The append-only storage model (`permascroll.md`, `storage.md`) means content is "filed, as it were, chronologically" and never overwritten (2/14):

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

Tumbler addressing guarantees that this identity, once assigned, is never invalidated by subsequent insertions (`tumblers.md`, 4/19):

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

## Consequences of this guarantee

Because identity is fixed at insertion and held separate from arrangement:

- **Links survive editing** — they bind to the permanent identity, not the position (`link-survivability.md`, 4/42): *"A Xanadu link is not between points, but between spans of data... If any of the bytes are left to which a link is attached, that link remains on them."*
- **Deletion never destroys identity** — DELETE removes content from the Vstream arrangement only; the Istream identity persists (`delete-semantics.md`, 4/9).
- **Versions share identity** — each version is a different Vstream arrangement over the same immutable Istream content (`versions.md`).
- **Origin is traceable** — the Document field of the I-address encodes where the byte was born (`origin-traceability.md`, 4/26).

## Summary

At the instant content is inserted, the system guarantees it a **permanent, immutable Istream identity** that is **distinct from the document's Vstream arrangement** of it. The arrangement may be continually re-ordered, shifted by later insertions, or removed from view — but the content's identity, once assigned, "will always return that exact content" and remains the stable anchor for links, transclusions, and historical reconstruction.
