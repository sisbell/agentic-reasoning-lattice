## Question 1 [nelson]

> Once content is assigned an address in the system, may any operation — editing, deletion, or reorganization — ever cause that address to refer to different content?

# No. An I-space address is permanently bound to its content.

This is one of the most fundamental invariants of the system. Once a byte is created and assigned its I-space address, no operation — editing, deletion, rearrangement, versioning, transclusion, or any other — can ever cause that address to refer to different content.

## The guarantee is structural, not policy

The system has **two address spaces**, and they behave differently:

**I-space (invariant space):** Content lives here permanently. Addresses are absolute and immutable.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**V-space (virtual space):** A document's current arrangement of content. V-addresses *do* shift with editing — that is their nature:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

But V-addresses are positional indices into an arrangement. They do not *name* content — they locate it within a view. The I-address is the name.

## Why no operation can violate this

**Editing** changes V-space arrangements only. I-space is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

**Deletion** removes content from V-space, not I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

**Rearrangement** is a pure V-space operation. The I-space addresses of the rearranged bytes are unchanged.

**Versioning** creates a new V-space arrangement over the same I-space content:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

**Transclusion (COPY)** creates a V-space reference to existing I-space content. No new I-space content is created; the original I-address is shared.

## The tumbler guarantee

At the addressing level, Nelson is explicit:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The forking mechanism ensures new addresses are always created *below* existing ones — by adding digits to the right. No existing address is ever reassigned or reinterpreted.

## Why this matters

The entire system depends on this invariant:

- **Links survive editing** because they point to I-space addresses, not V-space positions: "links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

- **Attribution is structural** because the I-address encodes the home document: "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

- **Correspondence works** because shared I-space origin is how the system identifies matching parts across versions.

- **Transclusion works** because including content by reference requires that the reference always resolves to the same content.

## Summary

| Address space | Can it refer to different content? | Why |
|---|---|---|
| **I-space** | **Never.** | Append-only; addresses are permanent bindings to content |
| **V-space** | Positions shift with editing | V-addresses are ephemeral indices into an arrangement, not content identifiers |

The I-space address is the identity of the content. To allow it to refer to something else would destroy permanence, attribution, link survivability, transclusion integrity, and version correspondence — effectively every guarantee the system makes.
